#!/usr/bin/env python3
"""Offline read-only reconciliation of WIS review candidates with Saab Database.

No network, no modification to canonical datasets, no automatic assertion of
fact equivalence or cross-brand part fitment.
"""
import argparse
import json
import re
from collections import defaultdict
from pathlib import Path
from wis_indexer import canonical_url


def _url(url):
    if not isinstance(url, str):
        return None
    key = canonical_url(url)
    return key.rstrip("/") if key else None


def load_repo_index(repo_root):
    root = Path(repo_root)
    datasets = root / 'data' / 'datasets'
    if not datasets.is_dir():
        raise FileNotFoundError(f'No Saab Database datasets directory at {datasets}')
    urls = defaultdict(list)
    facts = []
    for path in sorted(datasets.glob('*.json')):
        data = json.loads(path.read_text(encoding='utf-8'))
        if not isinstance(data, dict):
            raise ValueError(f'Expected dataset object: {path}')
        label = str(path.relative_to(root))
        for src in data.get('sources', []):
            key = _url(src.get('url'))
            if key:
                urls[key].append({'id':src['id'],'path':label,'url':src.get('url')})
        for fact in data.get('facts', []):
            facts.append({**fact, 'path':label})
    return dict(urls), facts


def _subject(s):
    return re.sub(r'\s+', ' ', str(s)).strip().casefold()


def _number(s):
    if isinstance(s, bool):
        return None
    try:
        return float(str(s).strip().replace(',', '.'))
    except (ValueError, TypeError):
        return None


_STOP = {'the', 'of', 'and', 'a', 'to', 'for', 'in', 'on', 'at', 'with'}


def _tokens(s):
    return {t for t in re.findall(r'[a-z0-9]+', str(s).casefold()) if t not in _STOP}


def _leaf_numbers(value):
    """Numeric leaves of a fact value (scalar, list or object such as {nominal, tolerance})."""
    if isinstance(value, bool) or value is None:
        return []
    if isinstance(value, (int, float)):
        return [float(value)]
    if isinstance(value, str):
        n = _number(value)
        return [] if n is None else [n]
    if isinstance(value, list):
        return [n for v in value for n in _leaf_numbers(v)]
    if isinstance(value, dict):
        return [n for v in value.values() for n in _leaf_numbers(v)]
    return []


def _candidate_numbers(raw):
    """All numbers in a candidate's printed value ("89 ± 2" -> 89, 2; "140 - 150" -> 140, 150)."""
    n = _number(raw)
    if n is not None:
        return [n]
    return [float(x.replace(',', '.')) for x in re.findall(r'\d+(?:[.,]\d+)?', str(raw or ''))]


def _label_strength(candidate_label, fact):
    """How closely the candidate's WIS row label matches the fact's own wording. Never proof of equivalence."""
    cand = _subject(candidate_label)
    if cand and cand in (_subject(fact.get('subject', '')), _subject(fact.get('locator', ''))):
        return 'exact'
    a = _tokens(candidate_label)
    best = 0.0
    for field in ('locator', 'subject', 'predicate'):
        b = _tokens(fact.get(field, ''))
        if a and b:
            best = max(best, len(a & b) / len(a | b))
    return 'high_token_overlap' if best >= 0.6 else None


def _caveats(candidate, fact):
    notes = []
    restr = candidate.get('applicability_restrictions') or {}
    if restr.get('engine_number') or restr.get('chassis_number'):
        notes.append('candidate_has_published_engine_or_chassis_boundary; existing fact scope not compared')
    if fact.get('unit') in (None, ''):
        notes.append('existing_fact_unit_not_stated_as_unit_field')
    if (fact.get('applicability') or {}).get('vin_ranges'):
        notes.append('existing_fact_has_vin_ranges')
    return notes


def reconcile(review, source_urls, facts):
    by_source = defaultdict(list)
    for fact in facts:
        for sid in fact.get('source_ids', []):
            by_source[sid].append(fact)
    records = []
    for candidate in review.get('candidates', []):
        url = _url(candidate.get('source_url'))
        if not url:
            raise ValueError('Candidate has invalid/non-SaabWISOnline source URL')
        sources = source_urls.get(url, [])
        source_ids = {s['id'] for s in sources}
        raw_url = str(candidate.get('source_url') or '')
        exact_url = any(s.get('url') == raw_url for s in sources) if any('url' in s for s in sources) else None
        same_source = {f['id']: f for sid in source_ids for f in by_source.get(sid, [])}
        matches, conflicts, details = [], [], []
        cand_numbers = _candidate_numbers(candidate.get('raw_value'))
        for fid, fact in same_source.items():
            legacy_subject = _subject(fact.get('subject', '')) == _subject(candidate.get('subject', ''))
            strength = 'exact' if legacy_subject else _label_strength(candidate.get('subject', ''), fact)
            if not strength:
                continue
            fact_unit = str(fact.get('unit') or '').casefold()
            cand_unit = str(candidate.get('unit') or '').casefold()
            if fact_unit and fact_unit != cand_unit:
                continue                                  # different stated unit: no numeric comparison
            leaves = _leaf_numbers(fact.get('value'))
            if not cand_numbers or not leaves:
                continue
            equal = all(any(abs(n - c) < 1e-9 for n in leaves) for c in cand_numbers)
            (matches if equal else conflicts).append(fid)
            details.append({'fact_id': fid, 'outcome': 'possible_duplicate' if equal else 'potential_conflict',
                            'label_match': strength, 'basis': 'same_source_url_and_row_label',
                            'unit_status': 'unit_field_equal' if fact_unit else 'fact_unit_unstated',
                            'caveats': _caveats(candidate, fact)})
        cross = sorted(f['id'] for f in facts
                       if f['id'] not in same_source and _label_strength(candidate.get('subject', ''), f) is not None
                       and set(f.get('source_ids', [])).isdisjoint(source_ids)
                       and str(f.get('unit') or '').casefold() == str(candidate.get('unit') or '').casefold())
        records.append({
            'candidate_id': candidate.get('candidate_id'),
            'source_url': url,
            'source_status': 'already_indexed' if sources else 'not_indexed',
            'source_match': None if not sources else ('exact_url' if exact_url else 'normalized_url' if exact_url is False else 'url_unknown'),
            'existing_source_ids': sorted(source_ids),
            'same_source_fact_count': len(same_source),
            'possible_fact_matches': sorted(set(matches)),
            'potential_conflicts': sorted(set(conflicts)),
            'match_details': details,
            'cross_source_label_overlaps': cross,
            'decision': 'manual_review',
            'reason': 'Source or numeric similarity does not prove equivalent vehicle applicability or procedure context',
        })
    return {'schema': 'wis-reconciliation-v0.2', 'writes_to_repository': False,
            'review_only': True, 'results': records,
            'counts': {'candidates': len(records),
                       'indexed_sources': sum(x['source_status'] == 'already_indexed' for x in records),
                       'possible_matches': sum(bool(x['possible_fact_matches']) for x in records),
                       'potential_conflicts': sum(bool(x['potential_conflicts']) for x in records),
                       'cross_source_overlaps': sum(bool(x['cross_source_label_overlaps']) for x in records)}}


def write_reconciliation(path, data):
    path=Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8') as f:
        json.dump(data,f,indent=2,ensure_ascii=False)
        f.write('\n')


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--repo-root',type=Path,required=True)
    p.add_argument('--review-file',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args()
    review=json.loads(args.review_file.read_text(encoding='utf-8'))
    sources,facts=load_repo_index(args.repo_root)
    result=reconcile(review,sources,facts)
    write_reconciliation(args.output,result)
    print(json.dumps(result['counts'],sort_keys=True))

if __name__=='__main__': main()
