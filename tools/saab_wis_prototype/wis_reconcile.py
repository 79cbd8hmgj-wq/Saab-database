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
                urls[key].append({'id':src['id'],'path':label})
        for fact in data.get('facts', []):
            facts.append({**fact, 'path':label})
    return dict(urls), facts


def _subject(s):
    return re.sub(r'\s+', ' ', str(s)).strip().casefold()


def _number(s):
    try:
        return float(str(s).strip().replace(',', '.'))
    except (ValueError, TypeError):
        return None


def reconcile(review, source_urls, facts):
    records = []
    for candidate in review.get('candidates', []):
        url = _url(candidate.get('source_url'))
        if not url:
            raise ValueError('Candidate has invalid/non-SaabWISOnline source URL')
        sources = source_urls.get(url, [])
        matches, conflicts = [], []
        for fact in facts:
            if not sources or not set(fact.get('source_ids', [])) & {s['id'] for s in sources}:
                continue
            if _subject(fact.get('subject', '')) != _subject(candidate.get('subject','')):
                continue
            if str(fact.get('unit') or '').casefold() != str(candidate.get('unit') or '').casefold():
                continue
            a, b = _number(fact.get('value')), _number(candidate.get('raw_value'))
            if a is not None and b is not None:
                (matches if abs(a-b)<1e-9 else conflicts).append(fact['id'])
        records.append({
            'candidate_id':candidate.get('candidate_id'),
            'source_url':url,
            'source_status':'already_indexed' if sources else 'not_indexed',
            'existing_source_ids':[x['id'] for x in sources],
            'possible_fact_matches':sorted(set(matches)),
            'potential_conflicts':sorted(set(conflicts)),
            'decision':'manual_review',
            'reason':'Source or numeric similarity does not prove equivalent vehicle applicability or procedure context',
        })
    return {'schema':'wis-reconciliation-v0.1', 'writes_to_repository':False,
            'review_only':True, 'results':records,
            'counts':{'candidates':len(records),'indexed_sources':sum(x['source_status']=='already_indexed' for x in records),
                      'possible_matches':sum(bool(x['possible_fact_matches']) for x in records),
                      'potential_conflicts':sum(bool(x['potential_conflicts']) for x in records)}}


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
