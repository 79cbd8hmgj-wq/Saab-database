#!/usr/bin/env python3
"""Validate and render the scoped MY2011 Turbo4 dossier extension.

This checks evidence bookkeeping, not engineering truth, stock or vehicle health.
The original dataset census is intentionally not enlarged by this derived dossier.
"""
import argparse
import json
from collections import Counter
from datetime import datetime
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data/engineering-dossiers/ng95-2011-purchase-reliability-20261015.json'
REPORT = ROOT / 'docs/research/ng95-2011-component-repair-expansion-20261015.md'
AREAS = {
    'component_inventory_completeness', 'factory_identification_confidence',
    'failure_mechanism_research', 'original_supplier_identification',
    'factory_supersession_verification', 'cross_brand_interchange_validation',
    'current_US_replacement_availability', 'repair_procedure_coverage',
    'DIY_feasibility', 'actual_repair_cost_evidence', 'remaining_safety_critical_gaps',
}


def validate(d):
    errors = []
    def require(ok, message):
        if not ok:
            errors.append(message)
    scope = d['active_research_scope']
    require(scope['model_years'] == [2011] and scope['markets'] == ['US'], 'target market/year widened')
    require(scope['drive'] == 'FWD' and scope['body'] == 'production sedan', 'target drivetrain/body widened')
    require(scope['trims'] == ['Turbo4', 'Turbo4 Premium'] and scope['transmission_family'] == 'AF40', 'target trim/gearbox widened')
    require(scope['engine_codes'] == ['A20NFT', 'LHU'], 'target engine widened')
    source_ids = [x['id'] for x in d['source_records']]
    require(len(source_ids) == len(set(source_ids)), 'duplicate source ID')
    sources = set(source_ids)
    def refs(ids, context):
        require(bool(ids) and set(ids) <= sources, 'missing/unknown source: ' + context)
    components = d['component_inventory']
    ids = [x['id'] for x in components]
    require(len(ids) == len(set(ids)), 'duplicate component ID')
    known = set(ids)
    numbers = [x['catalogue_service_part_number'] for x in components if x['catalogue_service_part_number'] is not None]
    require(len(numbers) == len(set(numbers)), 'competing same-number component rows')
    systems = d['inventory_systems']
    system_ids = {x['id'] for x in systems}
    require(system_ids == {f'{i:02}' for i in range(1, 20)}, '19-system inventory requirements missing')
    routed = [cid for s in systems for cid in s['component_ids']]
    require(Counter(routed) == Counter(ids), 'component not assigned exactly once to system')
    for c in components:
        refs(c['evidence_source_ids'], c['id'])
        require(c['system_id'] in system_ids, 'invalid system: ' + c['id'])
        require(c['production_applicability']['research_scope_ref'] == 'active_research_scope', 'missing target scope')
        require(c['catalogue_service_part_number'] is None or isinstance(c['catalogue_service_part_number'], str), 'numeric part number')
        require(c['failure_research']['failure_frequency'] is None or c.get('frequency_study_source_ids'), 'unsourced failure frequency')
        if c['factory_installed_part_number'] is not None:
            refs(c.get('as_built_source_ids', []), 'factory-installed identity ' + c['id'])
        if c['vin_fitment_approved'] or c['physical_vehicle_verified']:
            refs(c.get('approval_source_ids', []), 'fitment approval ' + c['id'])
        for rel in c['retailer_supersession_claims']:
            refs(rel['evidence_source_ids'], 'retailer relationship ' + c['id'])
            require(rel['direction'] == 'old_to_new', 'supersession direction missing')
            if rel['manufacturer_approval_verified']:
                refs(rel.get('manufacturer_source_ids', []), 'manufacturer supersession ' + c['id'])
        if c['repair_procedure_source_ids']:
            refs(c['repair_procedure_source_ids'], 'procedure ' + c['id'])
    assessments = d['interchange_assessments']
    assessment_ids = {x['id'] for x in assessments}
    for c in components:
        require(set(c['replacement_option_ids']) <= assessment_ids, 'unknown replacement option')
    for a in assessments:
        refs(a['evidence_source_ids'], a['id'])
        require(set(a['component_ids']) <= known, 'unknown interchange component')
        require(a['category'] in 'ABCDE' and len(a['category']) == 1, 'invalid interchange class')
        if a['category'] in 'AB' or a['approved_drop_in']:
            refs(a.get('manufacturer_approval_source_ids', []), 'A/B promotion ' + a['id'])
        if a['category'] in 'CDE':
            require(not a['approved_drop_in'], 'C/D/E cannot silently approve drop-in')
        if a['durability_validated']:
            refs(a.get('durability_test_source_ids', []), 'durability ' + a['id'])
    observations = d['current_supply_observations']
    observation_ids = [x['id'] for x in observations]
    require(len(observation_ids) == len(set(observation_ids)), 'duplicate supply observation')
    for o in observations:
        refs(o['evidence_source_ids'], o['id'])
        try:
            datetime.fromisoformat(o['observed_at'])
        except ValueError:
            errors.append('invalid observation date ' + o['id'])
        require(o['currency'] == 'USD' and o['displayed_unit_price'] >= 0, 'invalid observed price')
        require(o['price_basis'] in {'seller_public_storefront_response_no_checkout',
                                     'retrieved_retail_page_no_checkout'}, 'unknown price observation method')
        if o['deliverable_inventory_confirmed']:
            refs(o.get('delivery_confirmation_source_ids', []), 'delivery claim ' + o['id'])
        require(o['warranty']['source_id'] in sources, 'missing warranty provenance')
    obs = {x['id']: x for x in observations}
    for c in components:
        require(set(c['observation_ids']) <= set(obs), 'unknown component supply link')
    for job in d['repair_economics']:
        refs(job['evidence_source_ids'], job['id'])
        total = Decimal('0')
        for line in job['known_part_lines']:
            o = obs.get(line['observation_id'])
            require(o is not None, 'unknown cost observation')
            if o is None:
                continue
            require(line['unit_price_usd'] == o['displayed_unit_price'], 'price copied incorrectly')
            extended = Decimal(str(o['displayed_unit_price'])) * line['quantity']
            require(extended == Decimal(str(line['extended_price_usd'])), 'bad line arithmetic')
            total += extended
        subtotal = job['observed_part_subtotal_usd']
        require((subtotal is None and not job['known_part_lines']) or
                (subtotal is not None and total == Decimal(str(subtotal))), 'bad subtotal')
        if job['all_in_repair_cost_usd'] is not None:
            refs(job.get('complete_quote_source_ids', []), 'all-in cost ' + job['id'])
    require({x['area'] for x in d['coverage_assessment']} == AREAS, 'independent coverage dimension missing')
    for item in d['service_findings'] + d['modernization_candidates'] + d['source_conflict_resolutions']:
        refs(item['evidence_source_ids'], item['id'])
    framework = d.get('inspection_framework')
    if framework:
        stage_ids = [x['id'] for x in framework['stages']]
        require(len(stage_ids) == len(set(stage_ids)), 'duplicate inspection stage')
        require(framework['disposition'] == 'HOLD', 'blank inspection must remain HOLD')
        for stage in framework['stages']:
            refs(stage['evidence_source_ids'], 'inspection ' + stage['id'])
            require(stage['result'] is None and stage['evidence_label'] == 'unresolved',
                    'research intake contains invented inspection result')
    return errors


def render(d):
    sources = {x['id']: x for x in d['source_records']}
    def evidence(ids):
        return ', '.join(f"[{sid.removeprefix('ng95-component-src-')}]({sources[sid]['url']})" for sid in ids)
    lines = [
        '# 2011 US Turbo4 FWD automatic: component and repair expansion', '',
        'Research date: 2026-10-15. **Incomplete; no scoring, purchase approval or verified donor swap.**', '',
        'This expands the [existing PR #82 dossier](../../data/engineering-dossiers/ng95-2011-purchase-reliability-20261015.json), '
        'retains its original facts/cases/supplier observations, and preserves the unmerged follow-up '
        '`94b2d4046445f539afd936580adf91811042c695`. Open PRs #80/#81 explicitly exclude 9650; their catalogue and scoring work is not target coverage.', '',
        'Only MY2011 US Turbo4/Turbo4 Premium A20NFT/LHU FWD factory AF40 automatic production sedans are targets. '
        'Historical V6/XWD backlog text stays in the original document for provenance and is outside this active research. '
        'European/other GM applications are component leads only.', '',
        '## What the identifiers establish', '',
        f"The register contains **{len(d['component_inventory'])} curated component identities**, organized under 19 systems. "
        'A service number from a merchant diagram is not an original installed part number. Those fields, original supplier, '
        'revision, factory supersessions and VIN approval remain explicitly unknown where unsupported. '
        'BorgWarner is identified by the factory LHU turbo description; its exact assembly number/revision remains unknown. '
        'No complete as-built component inventory has been verified.', '',
        'Existing evidence reused: `gmwp-part-001`, `hcdiag-issue-002`, `corrections-issue-011`, '
        '`corrections-issue-016`, `corrections-issue-020`, the six PR82 facts and eight investigation cases. '
        'New service findings are repair requirements, not new claims of common factory defects.', '',
        '## Consequential factory findings', '',
    ]
    for finding in d['service_findings']:
        lines += [f"- **{finding['id']}** — {finding['claim']} {evidence(finding['evidence_source_ids'])}"]
    lines += ['', 'The inherited cold-valve advisory remains a manufacturer-described possible mechanism, not a measured failure rate. '
              'A truly cold compression/leakdown evaluation remains necessary. A new valve part number or a seller claiming a rebuilt head '
              'does not prove a material improvement or a healthy engine. The manufacturer PDF redirect could not be refreshed during this batch; '
              'the original saved provenance remains intact.', '', '## Contradictions and scope controls', '']
    for resolution in d['source_conflict_resolutions']:
        lines += [f"- **{resolution['id']}** — {resolution['finding']} {evidence(resolution['evidence_source_ids'])}"]
    lines += ['', 'The revised airbag filing changes the documented population; it does not prove that any actual car has no open campaigns. '
              'The live NHTSA model API request failed, so no complete recall/TSB census or zero-recall claim is made.', '',
              '## Interchange assessments', '', '| Assessment | Class | Finding / remaining boundary |', '| --- | --- | --- |']
    for a in d['interchange_assessments']:
        lines.append(f"| {a['id'].removeprefix('ng95-interchange-')} | {a['category']} | {a['finding']} {evidence(a['evidence_source_ids'])} |")
    lines += ['', 'A = identical original supplier/number/revision/interfaces; B = approved directed OEM supersession; '
              'C = named aftermarket manufacturer cross-reference; D = engineering/number candidate; E = rejected claimed mapping. '
              '**No A or B approval is established.** AISIN fluid is C, not proof that a Toyota-labelled bottle or any other Aisin transmission part fits.', '',
              '## US supply observations', '',
              'Fifteen exact-product public storefront responses and one additional retrieved retailer page were read on 2026-10-15 without placing orders. '
              'Stock and lead times are seller assertions. Destination shipping, tax, core charges and deliverability are unknown. '
              'The three earlier baseline observations are retained separately.', '',
              '| Service / seller SKU | Description | Displayed USD | Seller availability |', '| --- | --- | ---: | --- |']
    for o in d['current_supply_observations']:
        url=sources[o['evidence_source_ids'][0]]['url']
        label = o['seller_sku'] if o['supplier'] != 'eSaabParts' else o['part_number']
        lines.append(f"| [{label}]({url}) | {o['description']} | ${o['displayed_unit_price']:.2f} | {o['stock_statement']} |")
    lines += ['', 'The current kit response is $92.50 versus an indexed $99.99; controller 55574324 now displays one available '
              'versus the cached backorder; exhaust solenoid 12679100 now displays $63.60 versus cached $53.12. Both observations '
              'remain in the data. A catalog price on an unavailable radiator/headlamp is not a purchasable restoration budget.', '',
              'General [seller warranty terms](https://www.esaabparts.com/warranty_and_returns.php) say most eligible OEM parts receive '
              '24 months/24,000 miles subject to conditions. Aftermarket parts have no warranty through the seller; manufacturer coverage '
              'needs verification. Socket 13320976 explicitly has no warranty. A/C warranty conditions require qualified installation, '
              'and compressor claims require additional component/service evidence. Verify exact eligibility and return exceptions before purchase.', '',
              'The Bosch 66814 alternative is supported by a manufacturer indexed OE reference and exact Turbo4 retailer application. It remains category C: original supplier/revision, package contents, delivery and warranty are not verified. Its $288.29 pump-only offer is an alternative to the $901.17 Saab-channel pump, not an additional line item or guaranteed installed saving.', '',
              '## Repair economics and DIY boundaries', '',
              'Subtotals below include only the observed line items. **They are not complete repair estimates or guaranteed minimum costs.** '
              'Every job separately retains unknown additional parts, fluids, shipping, tax, core, tools, programming, specialist labor, towing '
              'and contingency. No invented labor hours or installed quotes are provided.', '',
              '| Repair | Observed parts subtotal | Practical decision |', '| --- | ---: | --- |']
    for j in d['repair_economics']:
        value='Unknown' if j['observed_part_subtotal_usd'] is None else f"${j['observed_part_subtotal_usd']:.2f}"
        lines.append(f"| {j['title']} | {value} | {j['no_rebuild_feasibility']} |")
    lines += ['', 'The coolant-pump subtotal includes the pump and two standard pipe O-rings, conditional on renewing them. '
              'Verify boxed contents to avoid duplicate purchases. The primary timing kit omits the balance-chain/tensioner and gears; '
              'new actuator bolts and other disturbed seals/fluids/tools are not priced. AW1 service quantity is still unknown; '
              'the AISIN container volume has not been verified, so no per-litre saving or total ATF-service price is asserted.', '',
              '## Reliability improvements: evidence level', '']
    for a in d['modernization_candidates']:
        lines.append(f"- **{a['benefit_level']}** — {a['proposal']} {evidence(a['evidence_source_ids'])}")
    lines += ['', 'No candidate has independent durability-test evidence or a verified lifespan gain. '
              'No tuning, emissions defeat, safety-system bypass or generic preventive replacement interval is proposed.', '',
              '## Component identities and option restrictions', '',
              'All rows inherit the strict active research scope. Restrictions below are the source-specific conditions; '
              'a conditional catalogue row is not proof that its equipment was offered on either US target trim. '
              'Original installed numbers, revisions and official supersessions need factory/physical verification.', '']
    for system in d['inventory_systems']:
        lines += [f"### {system['id']}. {system['name']}", '', '| Service number | Component | Source restriction / evidence |', '| --- | --- | --- |']
        for c in d['component_inventory']:
            if c['system_id'] != system['id']:
                continue
            pn=c['catalogue_service_part_number'] or 'Unknown'
            lines.append(f"| {pn} | {c['description']} | {c['production_applicability']['source_restrictions']} {evidence(c['evidence_source_ids'])} |")
        lines += ['', '**Still required:** ' + '; '.join(system['outstanding_inventory_requirements']) + '.', '']
    lines += ['## Separate coverage states', '', '| Area | State | Basis |', '| --- | --- | --- |']
    for x in d['coverage_assessment']:
        lines.append(f"| {x['area']} | {x['status']} | {x['basis']} |")
    lines += ['', 'No system is claimed complete and no search is marked exhausted. Counts measure saved records, '
              'not the proportion of the vehicle verified. No failure-frequency denominator is available.', '',
              '## Prioritized remaining work', '']
    for x in d['prioritized_backlog']:
        lines.append(f"{x['priority']}. **{x['question']}** — {x['acceptance_evidence']}.")
    lines += ['', 'Use the [existing detailed lot worksheet](ng95-2011-turbo4-lot-inspection-worksheet-20261015.md) '
              'and its added component/diagnostic decision sequence before evaluating a real vehicle. '
              'Unknown faults remain HOLD; confirmed work outside the objective remains STOP. FINALIST is a request for further inspection and pricing.', '',
              '## Reproduction', '',
              '`python3 tools/check_ng95_components.py --check --summary` checks source references, hierarchy, '
              'scope boundaries, price arithmetic and generated-report consistency. '
              '`python3 tools/check_ng95_components.py --write-report` regenerates this document from the existing dossier. '
              'Passing checks does not validate mechanical fitment or turn a listing into stock.', '']
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--summary', action='store_true')
    parser.add_argument('--write-report', action='store_true')
    args = parser.parse_args()
    d = json.loads(DATA.read_text(encoding='utf-8'))
    errors = validate(d)
    report = render(d)
    if args.write_report and not errors:
        REPORT.write_text(report, encoding='utf-8')
    if args.check and (not REPORT.exists() or REPORT.read_text(encoding='utf-8') != report):
        errors.append('generated NG95 component report is stale')
    for error in errors:
        print('FAIL:', error)
    if args.summary or not errors:
        print(json.dumps({'components': len(d['component_inventory']), 'systems': len(d['inventory_systems']),
                          'supply_observations': len(d['current_supply_observations']),
                          'repair_cases': len(d['repair_economics']), 'errors': len(errors)}))
    return int(bool(errors))


if __name__ == '__main__':
    raise SystemExit(main())
