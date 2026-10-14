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

The 360 assembly groups in `inventory.json` are a systematic research inventory,
including ordinary body/interior/HVAC and conditional equipment. They are not
360 verified installed parts or an exhaustive factory bill of materials.
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

Immediate remaining work: gearbox production/service-component matrices and
manual/Canada/convertible configuration enumeration; authenticated EPC identities
and supersessions for engine/timing/fuel/electronics; independent verification of
existing AS-PL/hub/brake donor leads; regional offerings and complete repair bills.
All other exact remaining assembly groups are in coverage's
`remaining_assembly_groups`. A product claim does not close its fitment/sourcing gap.

No configuration is ready for three-axis scoring: a verified production BOM,
regional replacements and full repair economics are not yet established.
The 37 inherited engineering cases plus the pump, plug and A/C compressor cases retain repair difficulty
and unresolved costs. Unknown totals are null, never zero or the pump sticker price.

## Second substantive batch: gearbox and ignition identities

The catalog now has seven separate transmission research records: OG9-5 AF30
(FA47, Aisin 50-40LE), OG9-5 FA57, NG9-3 FA57, NG9-3 AF40/TF-80SC, NG9-3 F40,
and separate unresolved five-speed manual records for each platform. An AF40 WIS
chapter does not establish its applicability to every North American B207.
FM55/FM57 tag-legend contradictions are preserved, and a tool called F35 does
not certify the installed gearbox. Assembly part numbers and the complete
engine/year/market/ratio matrices remain unverified.

New factory sources: [AF30 designation legend](https://saabwisonline.com/9-5-9600/2001/4-transmission/automatic-transmission/technical-data/type-designation)
and [F40 manufacturing label example](https://saabwisonline.com/9-3-9440/2008/4-transmission/manual-gearbox/6-speed/technical-data/type-designation).
Neither example is a universal production tag.

[Saab Parts 55571391](https://webshop-fi.saabparts.com/productdetail/saabparts/55571391)
identifies NGK PFR6D10G as the current service product. It lists a broad petrol
application, but separately restricts BioPower/FlexFuel by year and engine serial.
The historical NGK B207L date split, UK2024 catalogue, US2019 catalogue and
factory B207E/L PFR6T specification are kept as distinct claims. Current service
replacement identity must not be mistaken for an original production revision.

The [dedicated MY2006 plug procedure](https://saabwisonline.com/9-3-9440/2006/2-engine/4-cylinder-petrol/engine-management-system-trionic-t8/adjustment-replacement/spark-plug-157)
and [compression-test procedure](https://saabwisonline.com/9-3-9440/2006/2-engine/4-cylinder-petrol/basic-engine/adjustment-replacement/engine-compression-test)
disagree on plug and coil fastener torques. Each source value remains in the
procedure record, and a blended installation instruction is blocked pending
authentic revision/joint confirmation.

[FCP NGK5542](https://www.fcpeuro.com/products/spark-plug-ngk-5542) advertises
$11.19 each, yielding a $44.76 four-plug subtotal. This excludes delivery, tax,
tools and shop labor. Finland's genuine plug offering is a separate EUR record;
it does not establish US/Canadian stock. Detailed warranty/core terms remain unknown.

Existing AS-PL, FAG, PFI, SKF and Delphi investigations now have specific
number-to-product candidate edges. The catalog does not turn their shared
aftermarket references into approved Opel/GM donors. The 5961610 engine-number
conflict is also explicitly linked to its two original source claims.

## Third substantive batch: ordinary HVAC components

The manufacturer and retailer findings distinguish NG9-3 compressor clutch
references 93184431/93189061 at chassis51041814/51041815 and OG9-5 blower
references at Y3046041/Y3046042. Blower motors and ACC regulators are separate
components; a motor candidate does not replace its regulator. ProParts lists
87349085 against earlier/later motor OE references, but that broad catalogue
claim has not independently resolved the housing/controller differences.

The two retailer ACC regulator titles overlap at chassis53512949. Manufacturer
short chassis notation differs. That boundary is explicitly unresolved; the
catalogue does not approve a universal regulator swap.

[Compressor service](https://saabwisonline.com/9-3-9440/2007/8-body/climate-system/heating-and-ventilation-a-c/adjustment-replacement/a-c-compressor-b207)
requires new PAD sealing washers, oil adjustment and refrigerant recovery,
evacuation, recharge and testing. Convertible access also requires front
reinforcement removal. The DIY scenario separates mechanical work from
outsourced refrigerant service; it does not describe the advertised compressor
price as an installed repair cost.

The [retailer diagram](https://www.esaabparts.com/viewparts.php?section=510187783)
advertises the Nissens compressor at $528.31 with four in its US warehouse.
Both chassis-specific clutch references are advertised at higher prices and
backorder. These observations justify obtaining complete competing repair
quotes; they do not prove a reliability advantage or cheaper installed result.
All observations retain source/date and checkout/Canada limitations.

## Coverage dashboard and readiness

The catalog contains **150 product identities and reference endpoints**, 125 application claims, 40 interchange edges, 19 dated offering observations and 40 repair scenarios. These are research records, not 150 verified installed components. Seven gearbox-family records are separate because a gearbox designation is not an assembly part number.

| System | 9440 research groups | 9440 groups with part claims | 9600 research groups | 9600 groups with part claims |
|---|---:|---:|---:|---:|
| Engine internals, oil delivery, PCV and sludge | 29 | 1 | 29 | 5 |
| Timing drive, valve train and intake valves | 27 | 1 | 27 | 0 |
| Turbocharger, oil feed, charge air and boost controls | 21 | 2 | 21 | 4 |
| Automatic/manual transmissions, differentials and drivetrain | 44 | 0 | 44 | 1 |
| Body shell, subframe, structural corrosion and safety mounts | 17 | 7 | 17 | 3 |
| Brake friction, hydraulics, ABS/ESC, lines and parking brake | 21 | 1 | 21 | 0 |
| Cooling, radiator/heat exchangers, fans and related ATF cooling | 24 | 2 | 24 | 10 |
| Fuel system, catalyst, OBD emissions and evaporative controls | 29 | 0 | 29 | 0 |
| ECUs, ignition, keys, anti-theft, software and programming | 15 | 4 | 15 | 2 |
| Alternator, starter, harnesses, connectors and grounds | 18 | 2 | 18 | 2 |
| Steering, suspension, wheel bearings and bushes | 29 | 2 | 29 | 0 |
| HVAC, heating/defog, A/C and water intrusion | 17 | 2 | 17 | 2 |
| Airbags, seatbelts and manufacturer/regulator campaigns | 12 | 2 | 12 | 1 |
| Interior, instruments, locks and comfort electronics | 18 | 0 | 18 | 0 |
| Body panels, glass, lighting and sealing | 31 | 0 | 25 | 0 |
| Factory service schedule, fluids, filters, plugs and routine wear | 8 | 0 | 8 | 0 |

The full JSON dashboard separately counts product records, factory-specified
identities, manufacturer service applications, verified VIN replacements,
verified cross-brand VIN alternatives, complete repair costs and unresolved
product records. Component-specific original installed identities, VIN-approved
replacement packages, donor approvals and complete installed costs remain
unestablished. This is a strict evidence definition, not a claim that available
parts do not fit. No whole-vehicle completeness percentage is asserted.

`data/component-catalog/readiness.json` explicitly records all 79 currently
enumerated configurations as unranked, with independent reliability, sourcing
and economics blockers. Manuals, Canada and convertibles remain outside that
register until actual source-backed configurations are added. The broader
research inventory includes them as investigation targets.

Validation: legacy datasets retain 567 sources, 1,107 facts, 92 issue identities,
89 part claims and 284 gaps. 364 automated tests passed. New guards reject
cross-product scope expansion, excluded engines/platforms, invalid gearbox
applications, promoted interchange leads, pump-to-screw substitutions,
unsourced records, mixed currencies, incomplete totals, supersession cycles
and unreviewed legacy evidence drift. Catalog checks run in the branch CI workflow.
