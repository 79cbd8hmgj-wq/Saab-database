#!/usr/bin/env python3
"""Controlled, checkpointed, read-only SaabWISOnline pilot pipeline.

Phases (each separable and repeatable):
  1. discover+retrieve  - robots-checked, rate-limited, bounded BFS over *listing* pages;
                          raw HTML cached under --state-dir (never committed); checkpoint after every page.
  2. parse+extract      - offline, deterministic, from the cache (wis_candidates).
  3. reconcile          - offline, no-write comparison with data/datasets (wis_reconcile).
  4. report             - machine-readable measurements; coverage is NEVER claimed from a crawl alone.

Canonical datasets are never modified: the state dir may not be inside data/, docs/ or tests/.
"""
import argparse
import hashlib
import json
import os
import re
import time
from collections import deque
from datetime import datetime, timezone
from pathlib import Path

import wis_indexer as wi
import wis_candidates as wc
import wis_reconcile as wr

CHECKPOINT = 'checkpoint.json'
SCHEMA = 'wis-pilot-report-v0.1'


def _atomic_write(path, obj):
    tmp = Path(str(path) + '.tmp')
    tmp.write_text(json.dumps(obj, indent=2, ensure_ascii=False, sort_keys=True) + '\n', encoding='utf-8')
    os.replace(tmp, path)


def _raw_path(state_dir, url):
    return state_dir / 'raw' / (hashlib.sha256(wi.dedupe_key(url).encode()).hexdigest()[:24] + '.html')


def plan(start_url, subtree=None):
    start, prefix = wi.scope_prefix_for(start_url)
    nav = subtree or (urlsplit_path(start).rstrip('/') + '/')
    if not wi.within_scope(start, nav):
        raise ValueError('Start URL outside requested subtree')
    return start, prefix, nav


def urlsplit_path(url):
    return re.sub(r'^https://[^/]+', '', url)


def collect(start_url, state_dir, repo_root, max_pages=60, delay=3.0, subtree=None, opener=None,
            sleep=time.sleep, resume=False):
    """Phase 1. Returns the checkpoint dict. Safe to interrupt and resume."""
    if max_pages < 1 or max_pages > 200: raise ValueError('max_pages must be within 1..200')
    if delay < 2: raise ValueError('delay must be >= 2 seconds')
    start, prefix, nav = plan(start_url, subtree)
    state_dir = wi.safe_output_path(state_dir, repo_root)
    (state_dir / 'raw').mkdir(parents=True, exist_ok=True)
    cp_path = state_dir / CHECKPOINT
    if cp_path.exists():
        if not resume:
            raise FileExistsError(f'{cp_path} exists; use resume=True or a fresh state dir')
        cp = json.loads(cp_path.read_text(encoding='utf-8'))
        if cp['start_url'] != start or cp['subtree'] != nav:
            raise ValueError('Checkpoint belongs to a different start URL/subtree')
    else:
        cp = {'schema': 'wis-checkpoint-v0.1', 'run_id': datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ'),
              'start_url': start, 'subtree': nav, 'scope_prefix': prefix, 'status': 'running',
              'queue': [start], 'seen': [], 'discovered': {wi.dedupe_key(start): {'url': start, 'kind': 'start'}},
              'hashes': {}, 'records': [], 'robots': None}
    opener = opener or wi.make_opener()
    robots = wi.robots_policy(opener)                        # fail closed
    cp['robots'] = {'checked_at': datetime.now(timezone.utc).isoformat(),
                    'start_allowed': robots.can_fetch(wi.USER_AGENT, start)}
    if not cp['robots']['start_allowed']:
        raise PermissionError('robots.txt does not permit the requested starting URL')
    queue, seen, fetched_any = deque(cp['queue']), set(cp['seen']), False
    try:
        while queue and len(cp['records']) < max_pages:
            url = queue.popleft()
            key = wi.dedupe_key(url)
            if key in seen: continue
            seen.add(key)
            kind = cp['discovered'].get(key, {}).get('kind', 'unknown')
            rec = {'requested_url': url, 'discovered_as': kind}
            if not robots.can_fetch(wi.USER_AGENT, url):
                rec.update(url=url, status='blocked_by_robots')
            else:
                if fetched_any: sleep(delay)
                fetched_any = True
                res = wi.fetch_document(opener, url, prefix, sleep=sleep, delay=delay)
                rec.update(url=res['final_url'] if res['status'] == 'ok' else url, status=res['status'],
                           http_status=res.get('http_status'), attempts=res['attempts'])
                if res['redirect_chain']: rec['redirect_chain'] = res['redirect_chain']
                if res.get('error_type'): rec['error_type'] = res['error_type']
                if res['status'] == 'ok':
                    fkey, raw = wi.dedupe_key(res['final_url']), res['raw']
                    sha = hashlib.sha256(raw).hexdigest()
                    if fkey != key and fkey in seen:
                        rec.update(status='duplicate_redirect_target')
                    elif not wi.within_scope(res['final_url'], nav):
                        rec.update(status='outside_subtree')
                    elif 'text/html' not in res['content_type']:
                        rec.update(status='non_html_skipped')
                    else:
                        seen.add(fkey)
                        rp = _raw_path(state_dir, res['final_url'])
                        rp.write_bytes(raw)
                        rec.update(html_sha256=sha, bytes=len(raw), fetched_at=datetime.now(timezone.utc).isoformat())
                        if sha in cp['hashes']:
                            rec['duplicate_content_of'] = cp['hashes'][sha]
                        else:
                            cp['hashes'][sha] = res['final_url']
                        page = wi.parse_page(wi.decode_html(raw, res['content_type']), res['final_url'], nav)
                        rec.update(heading=page['heading'], page_title=page['page_title'], image_refs=page['image_refs'])
                        follow = [l for l in page['child_links'] if l['kind'] in ('folder', 'document')]
                        rec['page_kind'] = 'listing' if follow else 'document'
                        rec['unclassified_links_not_followed'] = len(page['child_links']) - len(follow)
                        for link in follow:
                            k = wi.dedupe_key(link['url'])
                            if k not in cp['discovered']:
                                cp['discovered'][k] = {'url': link['url'], 'kind': link['kind'], 'label': link['label'],
                                                       'parent': res['final_url']}
                                queue.append(link['url'])
            cp['records'].append(rec)
            cp.update(queue=list(queue), seen=sorted(seen))
            _atomic_write(cp_path, cp)                       # checkpoint after every page
        cp['status'] = 'complete' if not queue else 'bounded_stop'
    except KeyboardInterrupt:
        cp.update(status='interrupted', queue=list(queue), seen=sorted(seen))
        _atomic_write(cp_path, cp)
        raise
    cp.update(queue=list(queue), seen=sorted(seen))
    _atomic_write(cp_path, cp)
    return cp


def _norm(s):
    return re.sub(r'\s+', ' ', s).strip().casefold()


def analyse(state_dir, repo_root):
    """Phases 2-4 from cache only (no network). Returns (report, candidates_doc, reconciliation)."""
    state_dir = Path(state_dir)
    cp = json.loads((state_dir / CHECKPOINT).read_text(encoding='utf-8'))
    sources, facts = wr.load_repo_index(repo_root)
    docs, all_candidates, errors = [], [], []
    for rec in cp['records']:
        if rec.get('status') != 'ok' or rec.get('page_kind') != 'document':
            continue
        entry = {'url': rec['url'], 'heading': rec.get('heading'), 'html_sha256': rec['html_sha256']}
        try:
            html = wi.decode_html(_raw_path(state_dir, rec['url']).read_bytes())
            result = wc.extract_candidates(html, rec['url'])
            prof = wc.profile_document(html)
        except Exception as exc:                                   # explicit failure record, never silent
            errors.append({'url': rec['url'], 'error_type': type(exc).__name__})
            entry['extraction_error'] = type(exc).__name__
            docs.append(entry)
            continue
        entry.update(tables=prof['tables'], paragraphs=prof['paragraphs'], list_items=prof['list_items'],
                     warning_paragraphs=prof['warning_paragraphs'], dtc_codes_seen=prof['dtc_codes_seen'],
                     image_refs=len(prof['image_refs']), candidates=len(result['candidates']),
                     review_required_rows=len(result['review_required']),
                     unsupported_tables=len(result['unsupported_tables']),
                     internal_conflicts=len(result['internal_conflicts']),
                     review_required_reasons=sorted({r['reason'] for r in result['review_required']}))
        if result['unsupported_tables'] or result['review_required']:
            entry['structure'] = 'partially_unsupported'
        elif result['candidates']:
            entry['structure'] = 'specification_table'
        elif prof['tables']:
            entry['structure'] = 'tables_without_candidates'
        else:
            entry['structure'] = 'prose_or_diagram_no_tables'
        docs.append(entry)
        all_candidates.extend(result['candidates'])
        entry['_review'] = result['review_required']
        entry['_internal'] = result['internal_conflicts']
    cand_doc = {'schema': wc.SCHEMA, 'candidates': all_candidates}
    recon = wr.reconcile(cand_doc, sources, facts)
    # cross-document: same normalised label+unit in >1 document
    groups = {}
    for c in all_candidates:
        groups.setdefault((_norm(c['subject']), c['unit']), []).append(c)
    dup, contra = [], []
    for (label, unit), items in sorted(groups.items()):
        urls = sorted({i['source_url'] for i in items})
        if len(urls) < 2: continue
        vals = {i['raw_value'] for i in items}
        (contra if len(vals) > 1 else dup).append({'label': label, 'unit': unit, 'documents': urls, 'values': sorted(vals)})
    listings = [r for r in cp['records'] if r.get('page_kind') == 'listing']
    retrieved_docs = [r for r in cp['records'] if r.get('status') == 'ok' and r.get('page_kind') == 'document']
    start_is_doc = any(r.get('page_kind') == 'document' and r.get('requested_url') == cp['start_url'] for r in cp['records'])
    disc_docs = {k: v for k, v in cp['discovered'].items() if v['kind'] == 'document' or (v['kind'] == 'start' and start_is_doc)}
    bad = [{'url': r['url'], 'status': r['status'], 'http_status': r.get('http_status'), 'error_type': r.get('error_type')}
           for r in cp['records'] if r.get('status') not in ('ok',)]
    recon_conflicts = sum(bool(r['potential_conflicts']) for r in recon['results'])
    internal = sum(d.get('internal_conflicts', 0) for d in docs)
    retrieved_urls = {wi.dedupe_key(r['url']) for r in cp['records'] if r.get('status') == 'ok'}
    unfetched = [v['url'] for k, v in cp['discovered'].items() if k not in retrieved_urls
                 and k not in {wi.dedupe_key(r['requested_url']) for r in cp['records']}]
    docs_matching_existing = sum(1 for d in docs if sources.get(wi.dedupe_key(d['url'])))
    report = {
        'schema': SCHEMA,
        'run': {'run_id': cp['run_id'], 'start_url': cp['start_url'], 'subtree': cp['subtree'],
                'collection_status': cp['status'], 'robots': cp['robots']},
        'measured': {
            'pages_requested': len(cp['records']),
            'listing_pages_retrieved': len(listings),
            'documents_discovered': len(disc_docs),
            'documents_retrieved': len(retrieved_docs),
            'documents_parsed': sum('extraction_error' not in d for d in docs),
            'candidate_specifications_extracted': len(all_candidates),
            'existing_source_matches_documents': docs_matching_existing,
            'existing_source_matches_candidates': recon['counts']['indexed_sources'],
            'candidates_unmatched_but_source_has_existing_facts': sum(
                1 for x in recon['results'] if x['same_source_fact_count'] and not x['match_details']),
            'potential_duplicate_facts': recon['counts']['possible_matches'],
            'potential_contradictions': {'against_existing_facts': recon_conflicts, 'within_one_document': internal,
                                         'across_documents': len(contra)},
            'candidates_requiring_review': len(all_candidates),
            'review_required_rows': sum(d.get('review_required_rows', 0) for d in docs),
            'documents_with_unsupported_structures': sum(d.get('structure') == 'partially_unsupported' for d in docs),
            'documents_without_structured_candidates': sum(d.get('candidates', 0) == 0 for d in docs),
            'missing_or_inaccessible_pages': bad,
            'extraction_errors': errors,
            'cross_document_potential_duplicates': dup,
            'cross_document_potential_contradictions': contra,
        },
        'estimated': {},
        'inventory': {
            'basis': 'navigation listing pages under the subtree only',
            'independent_inventory': False,
            'independent_inventory_note': 'robots.txt names a sitemap on a different host (v2.saabwisonline.com); not collected',
            'discovered_but_not_fetched': unfetched,
            'queue_remaining': len(cp['queue']),
        },
        'coverage_claim': {
            'claimed': False,
            'reason': 'A successful crawl is not a coverage claim: no independent document inventory, '
                      'and candidate extraction covers only recognised tables.',
        },
        'documents': [{k: v for k, v in d.items() if not k.startswith('_')} for d in docs],
        'notes': ['All candidates are review-only; none is a verified vehicle specification.',
                  'Year/model path is not proof of engine, market, or VIN applicability.'],
    }
    return report, cand_doc, recon


def finalize(state_dir, repo_root, run_name=None):
    """Write report/candidates/reconciliation into state_dir without overwriting earlier outputs."""
    state_dir = wi.safe_output_path(state_dir, repo_root)
    report, cand_doc, recon = analyse(state_dir, repo_root)
    name = run_name or report['run']['run_id']
    outs = {}
    for suffix, obj in (('report', report), ('candidates', cand_doc), ('reconciliation', recon)):
        p = state_dir / f'{suffix}-{name}.json'
        with p.open('x', encoding='utf-8') as f:
            json.dump(obj, f, indent=2, ensure_ascii=False, sort_keys=True); f.write('\n')
        outs[suffix] = str(p)
    return report, outs


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--start', default=wi.ORIGIN + '/9-5-9600/2008/2-engine/cooling-system/')
    ap.add_argument('--state-dir', type=Path, required=True)
    ap.add_argument('--repo-root', type=Path, default=Path(__file__).resolve().parents[2])
    ap.add_argument('--max-pages', type=int, default=60)
    ap.add_argument('--delay', type=float, default=3.0)
    ap.add_argument('--resume', action='store_true')
    ap.add_argument('--dry-run', action='store_true', help='Print the plan only: no network, no writes')
    ap.add_argument('--run-name', help='Suffix for report files (default: run id); files are never overwritten')
    ap.add_argument('--analyse-only', action='store_true', help='Skip retrieval; analyse the existing cache offline')
    a = ap.parse_args()
    start, prefix, nav = plan(a.start)
    state = wi.safe_output_path(a.state_dir, a.repo_root)
    if a.dry_run:
        print(json.dumps({'dry_run': True, 'start': start, 'model_year_scope': prefix, 'subtree': nav,
                          'max_pages': a.max_pages, 'delay_seconds': a.delay, 'state_dir': str(state),
                          'checkpoint_exists': (state / CHECKPOINT).exists()}, indent=2))
        return
    if not a.analyse_only:
        cp = collect(a.start, state, a.repo_root, a.max_pages, a.delay, resume=a.resume)
        print(f"collection {cp['status']}: {len(cp['records'])} pages, queue remaining {len(cp['queue'])}")
    report, outs = finalize(state, a.repo_root, a.run_name)
    print(json.dumps({'measured': {k: v for k, v in report['measured'].items() if not isinstance(v, (list, dict))},
                      'outputs': outs}, indent=2))


if __name__ == '__main__':
    main()
