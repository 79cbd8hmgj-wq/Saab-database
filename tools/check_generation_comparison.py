"""Validate and render the bounded OG/NG purchase comparison."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data/engineering-dossiers/ng95-vs-og95-2006-2009-comparison-20261015.json'
REPORT = ROOT / 'docs/research/ng95-vs-og95-2006-2009-comparison-20261015.md'

def validate(d):
    dossiers = {k: json.loads((DATA.parent / v).read_text()) for k, v in d['linked_dossiers'].items()}
    refs = {s['id'] for s in d['sources']}
    refs.update('ng:' + s['id'] for s in dossiers['ng']['source_records'])
    refs.update('og:' + c['id'] for c in dossiers['og']['cases'])
    ids = [r['id'] for r in d['comparisons']]
    assert len(ids) == len(set(ids)), 'duplicate comparison'
    for row in d['comparisons']:
        assert row['evidence_refs'] and set(row['evidence_refs']) <= refs, 'unresolved source'
        assert row['remaining_unknown'], 'uncertainty required'
    for observation in d['supply_observations']:
        assert observation['advertised_unit_price'] > 0
        assert observation['observed_at_utc'].startswith(d['research_date'])
        assert observation['deliverable_inventory_confirmed'] is False, 'listing cannot confirm delivery'
        assert observation['installed_cost'] is None, 'no installed quote verified'
    assert all(d['purchase_protocol'].get(x) for x in ('STOP', 'HOLD', 'FINALIST'))
    assert d['critical_gaps'] and d['limits']
    return dossiers

def render(d):
    dossiers = validate(d)
    lines = ['# 2006–2009 9-5 automatic versus 2011 Turbo4', '',
             'Research date: ' + d['research_date'] + '. Partial evidence; no vehicle scoring or comparative failure-rate claim.', '',
             'Machine-readable source: [comparison dossier](../../data/engineering-dossiers/' + DATA.name + ').', '',
             '## Scope', '', d['scope']['older'], '', d['scope']['newer'], '',
             '## Repair and purchase differences', '']
    for row in d['comparisons']:
        lines += ['### ' + row['id'] + ' — ' + row['system'], '', '**2006–2009:** ' + row['older'], '', '**2011:** ' + row['newer'], '', '**Practical implication (engineering inference):** ' + row['practical_implication'], '', '**Unknown:** ' + row['remaining_unknown'], '', 'Evidence:']
        for ref in row['evidence_refs']:
            if ref.startswith('ng:'):
                s = next(s for s in dossiers['ng']['source_records'] if s['id'] == ref[3:])
                lines += ['', '- [' + ref + '](' + s['url'] + ') — ' + s['description']]
            elif ref.startswith('og:'):
                lines += ['', '- [' + ref + '](../../data/engineering-dossiers/' + d['linked_dossiers']['og'] + ') — existing case, with original applicability, citations and contradictions preserved.']
            else:
                s = next(s for s in d['sources'] if s['id'] == ref)
                lines += ['', '- [' + ref + '](' + s['url'] + ') — ' + s['classification'] + '; WIS years ' + str(s['applicable_model_years'])]
        lines += ['']
    lines += ['## Actual advertised parts observations', '', 'eSaabParts public product pages and storefront responses, 2026-10-15. Stock is displayed, not confirmed deliverable inventory. Prices are USD per listed unit.', '', '| Application / item | Seller SKU | Price | Displayed status |', '|---|---|---:|---|']
    for o in d['supply_observations']:
        lines += [f"| {o['application']} / {o['description']} | [{o['seller_sku']}]({o['url']}) | ${o['advertised_unit_price']:.2f} | {o['displayed_status']} |"]
    lines += ['', 'Warranty eligibility, shipping, tax, core charges, additional materials and installed costs are unverified. Exact timestamps and limits are in the JSON.', '']
    lines += ['- ' + x for x in d['cost_comparison_notes']]
    lines += ['', 'The newer prices and Bosch fitment evidence are retained in the [2011 component report](ng95-2011-component-repair-expansion-20261015.md).', '', '## Candidate decisions', '']
    lines += ['- **' + k + ':** ' + v for k,v in d['purchase_protocol'].items()]
    lines += ['', '## Limits', ''] + ['- ' + x for x in d['limits']]
    lines += ['', '## Prioritized remaining work', ''] + ['- ' + x for x in d['critical_gaps']]
    return '\n'.join(lines) + '\n'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--write-report', action='store_true')
    args = parser.parse_args()
    data = json.loads(DATA.read_text())
    result = render(data)
    if args.write_report:
        REPORT.write_text(result)
    else:
        assert REPORT.read_text() == result, 'comparison report drift'
    print('Generation comparison: sources, uncertainty, supply boundaries and report validated')
