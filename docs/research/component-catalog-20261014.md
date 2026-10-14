# Component catalogue research — 14 October 2026

This working catalogue contains substantive service-part research and preserves
all existing evidence. It is incomplete and does not support vehicle scores.

## Deliverables and interpretation

`data/component-catalog/catalog.json` contains normalized components,
application claims, namespace-specific part numbers, original relationship
claims, A–E interchange edges, specifications, reliability records, dated
supplier offerings, repair procedures/scenarios, sources, gaps and a reuse index.
The index links all 1,572 original non-source records to their original files,
source IDs, scopes and review hashes. Original datasets are untouched.

The 359 assembly groups in `inventory.json` are a systematic research inventory,
including ordinary body/interior/HVAC and conditional equipment. They are not
359 verified installed parts or an exhaustive factory bill of materials.
`coverage.json` gives explicit product and assembly denominators for each platform
and the existing 16 systems, and exact groups lacking product claims. Multiple
revisions/products may belong to one group. No completeness percentage is claimed.

The current 79 vehicle configurations are the eligible subset of the existing
third-party US automatic/FWD/nonconvertible production register. They do not
enumerate Canada, manuals, convertibles or every engine/year/body combination.
Application claims retain unknown dimensions and original source cohorts.
Factory service numbers and manufacturer products are not automatically original
factory-installed components. VIN approval, comparative durability and full
repair totals remain separate fields.

## New component research

- [OG9-5 pump service diagram](https://www.esaabparts.com/viewparts.php?searchpart=1&section=314395817):
  pump/housing/gasket/connector seals and coolant pipes are recorded separately.
  Seller pipe references 55559405/55566450 divide at engine 7016569/7016570;
  this still needs authenticated EPC confirmation.
- [Metelli 24-0636](https://www.metelligroup.it/en/Home/ProductDetail?brand=metelli&code=24-0636):
  manufacturer specifications and named Aisin, Bosch, Delphi, Gates, HEPU, INA,
  SKF, Valeo and ACDelco references are searchable candidate edges. Renault
  references remain unverified OEM donor leads. No longevity advantage is proved.
- [GRAF seller offering](https://www.esaabparts.com/saab/parts/240636):
  advertised $59.96, six available. The $165.32 Saab pump price is a secondary
  alternate-table observation; the direct genuine-product page returned loading
  data. Neither is a complete repair cost or confirmed delivery.
- [NGK/Niterra 2024 UK catalogue](https://www.tekniwiki.com/fileadmin/emea/catalogues_pdf/4w_spark_and_glow_2024_web_small.pdf):
  engine-specific plug products and shared Signum/Vectra service applications
  are retained with calendar-month ranges. UK catalogue guidance is not
  North American factory approval. Existing T7 plug-specification conflict stays open.
- [MY2006 OG9-5 coolant-pump procedure](https://saabwisonline.com/9-5-9600/2006/2-engine/cooling-system/adjustment-replacement/coolant-pump-4-cyl):
  access, tools, seal dependencies and joint-specific torque records support a
  bill of materials. Missing labor, seal/consumable and landed costs keep totals null.

## Quarantined and conditional relationships

Both the retailer predecessor list and Metelli pump references include 92151823.
The retailer diagram distinguishes pump 93166829 from screw 92151823. The
cross-category edge is quarantined, not an approved pump replacement.

Existing official GM/Saab 12630084 evidence supports category A only for the
current dual-channel service SKU. It does not approve an original Chevrolet donor
assembly for every B207 VIN. ISM 32021815 is a category B conditional repair kit:
the original black sliding mechanism must remain usable. It is not a whole switch.

## Repository state and continuation

Inspection found main at `21a04c6` and the comparison branch at `32f5f30`, with
four comparison/reuse files not on main. Work continues on
`feature/saab-comparison-model-20261014`.
`research/reliability-improvements-batch3-20261014` at `9b29717` has unmerged work
and draft PR #80. Its claims were read as provisional; its merge state was not
assumed. The cooling batch revisits incomplete identity/contradiction evidence
and expands manufacturer, seal and pipe details.

Continue by reading the reuse index and querying a part before investigating it:

```sh
python tools/component_catalog.py --component 93166829
python tools/component_catalog.py --platform 9-3-9440 --component alternator
python tools/component_catalog.py --write
python tools/component_catalog.py --check
python tools/validate.py
python -m unittest discover -s tests -v
```

Author new findings in one `research-batch-*.json` file per substantive batch;
retain specific components, sources, applications and unknowns. Regenerate the
catalogue and coverage rather than editing generated outputs. Existing issue
identities remain canonical; reuse them rather than creating a new defect record.

Immediate remaining work: explicit gearbox-family/service-component records and
manual/Canada/convertible configuration enumeration; authenticated EPC identities
and supersessions for engine/timing/fuel/electronics; independent verification of
existing AS-PL/hub/brake donor leads; regional offerings and complete repair bills.
All other exact remaining assembly groups are in coverage's
`remaining_assembly_groups`. A product claim does not close its fitment/sourcing gap.

No configuration is ready for three-axis scoring: a verified production BOM,
regional replacements and full repair economics are not yet established.
The 37 inherited engineering cases plus the new pump case retain repair difficulty
and unresolved costs. Unknown totals are null, never zero or the pump sticker price.
