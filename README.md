# Saab database

A source-backed research database for Saab specifications, factory corrections,
parts relationships, and the information needed to evaluate replacements.

The first research pass focuses on the original-generation 9-5 (9600) and
second-generation 9-3 (9440), especially US/Canadian four-cylinder configurations.
It also records boundaries that matter when comparing adjacent model years,
engines, and platforms.

## Start here

- [Phase 0 coverage audit](docs/coverage-audit.md): **current 34-domain** evidence census, platform/model-year coverage and status of inspection, subsystem and interchange readiness gates.
- [MY2008 9-5 US/CA original service schedule and historic recall-status caveats](docs/research/priority-usca-service-recall-baseline-wp7.md): source-backed maintenance checks; NHTSA VIN lookup excludes most >15-year-old recalls, so an apparent zero does not clear historic Saab campaigns.
- [Phase 0 closure plan](docs/gap-closure-plan.md): prioritized blocker-driven work for vehicle identity, rust, brakes, high-cost no-running diagnostics and manufacturer fitment.
- [Reproducible Phase 0 snapshot](data/phase0-coverage-snapshot.json): machine-derived baseline checked against all datasets on every CI run.
- [Prioritized research backlog](docs/research-backlog.md): source-gathering tasks and acceptance criteria before simulation.
- [Research overview](docs/research-overview.md): scope, coverage, model-selection
  reasoning, and the limits of the initial research.
- [Evidence policy](docs/evidence-policy.md): what a recorded finding actually
  establishes.
- [Data contract](docs/data-contract.md): dataset fields and applicability rules.
- [Simulation readiness](docs/simulation-readiness.md): what can be evaluated from
  documents and what still needs measurements or engineering data.
- [Research reports](docs/research/): detailed notes from the individual research
  domains, including contradictions and gaps.
- [Non-running Saab safe purchase screen](docs/research/priority-nonrunning-purchase-screen.md):
  staged seller evidence, no-drive/crank triggers, misfire vs catalyst failure, B235 oil/FA57 and B207 compression condition limits.
- [Blank Phase 0 non-running inspection intake](data/inspection-templates/nonrunning-phase0.json):
  reproducible evidence requests with explicit unknown results; **not** an engine or transmission failure score.
- [Brakes and hydraulic-safety identification matrix](docs/research/priority-brake-hydraulic-safety.md):
  9-3 2006 brake levels and VIN option-row codes; 9-5 rotor dimensions and front caliper torque conflicts; parking brake and brake-line service boundaries.
- [Structural rust and underbody-safety inspection zones](docs/research/priority-structural-corrosion-inspection.md):
  original 9-5 SportCombi rear floor/subframe body mounts, 9-3 CV structural sill, NY inspection criteria and critical brake/fuel line dependencies.
- [Priority 9-5 / 9-3 identity and chassis worksheets](docs/research/priority-vehicle-identity-gates.md):
  Gate A/C work package 1; physical VIN/gearbox tags, model-year folder conflicts, FA57 vs AF40/F40 and side-specific suspension options without VIN-approved substitutions.
- [Initial North American MY2008 B235 exhaust, fuel and EVAP research](docs/research/og95-north-american-exhaust-fuel-wp6.md):
  two converter stages, oxygen sensor locations, EVAP and fuel-differential checks, NY legal replacement restrictions and unresolved 2008 wagon diagnosis.
- [Original US/Canada Saab service and historical safety recall campaigns](docs/research/priority-usca-service-recall-baseline-wp7.md):
  factory MY2008 9-5 maintenance, NHTSA 15-year lookup gap, 08V160 9-5 trim, 16V063 airbag and 14V318/Canadian convertible seatbelts; VIN-specific status remains unverified.
- [Cross-manufacturer replacement pilot: Saab/Opel/Fiat shared hub and front pads](docs/research/cross-manufacturer-interchange-pilot.md):
  source-gated candidate SKUs, donor-brand catalogue claims, and unresolved physical/electrical/ABS/brake-option checks; contrasts Saab-specific Nissens radiator and an older PCV false positive.
- [Original Saab USA VIN and conditional parts-kit provenance](docs/research/official-us-vin-service-kit-provenance.md):
  dated US MY2004–07 9-5/9-3 code tables, the 12801010 to conditional 32021815 ISM kit conversion and explicit 2008–09 OEM fitment gaps.
- [Blank OEM replacement-evidence verification worksheet](data/inspection-templates/oem-replacement-verification.json):
  original VIN, fitted part and directed Saab WebEPC applicability/revision/installation prerequisites required before approving a replacement.
- [Source-audited VIN, gearbox and WebEPC provenance](docs/research/vin-gearbox-provenance.md):
  independent MY2005/08 9-3 VIN codes, 9-5 WIS year-table conflicts, 9-5 vs 9-3 FA57 and TCM adaptation, and VIN-specific part-fitment evidence gates.
- [Original Saab turbo misdiagnosis bulletin 291-2494 and FA57 MY2005/09 safeguards](docs/research/og95-turbo-tsb2912494-fa57-triage.md):
  year-correct diagnostics, misleading shaft-play wording, TCM adaptation requirements, and non-DIY stall-test restrictions.
- [9-5 turbo oil-feed installation, FA57 solenoid bands and old bulletin identification](docs/research/og95-turbo-oil-feed-solenoids.md):
  factory MY2005/06/08 turbo service and MY2007–09 AT shift versus pressure-solenoid diagnosis without extrapolating early Dexron III bulletins.
- [9-5 ATF temperature protection and original turbo clip bulletin correction](docs/research/og95-atf-thermal-turbo-bulletin.md):
  MY2008/09 electronic fault diagnostics, overheating thresholds, TCM inputs and explicit exclusion of B235R/US/Canada from the January 2002 wastegate bulletin.
- [Repair versus replacement: turbo boost, 9-5 FA57 shifting and overheating](docs/research/repair-vs-replace-troubleshooting.md):
  original Saab diagnostic branches that identify low-cost candidates without mistaking them for a guaranteed healthy used engine or gearbox.
- [High-cost powertrain diagnosis](docs/research/high-cost-powertrain-diagnostics.md):
  original 9-5 B205/B235 oil-pressure, pickup and bearing-damage screening; 9-3 B207 cold compression; early FA57 coolant-in-ATF.
- [MY2006/08 B235R oil and PCV revision evidence](docs/research/b235r-oil-pcv-2006-2008.md):
  oil-pressure thresholds, 2008 US severe-service, B235R manual sump variants and cautious PCV supplier fitment research.
- [B235 MY2004–09 lubrication/PCV and FA57 identity](docs/research/b235-maintenance-fa57-identity.md):
  year-scoped oil pressure, PCV flow, preventive service limits, gearbox/TCM codes and transmission bulletin boundaries.
- [2007–09 9-5 factory ground and power distribution](docs/research/og95-ground-power-0709.md):
  year-scoped ground conductors, ignition supply modes, T7 component locators and petrol cooling-fan relay references.
- [2007–09 9-5 T7 cooling and electrical research](docs/research/og95-t7-cooling-0709.md):
  separately verified model-year feeds, coolant sensor thresholds, and petrol fan/pressure safeguards.
- [Original 9-5 Trionic 7 electrical diagnosis](docs/research/og95-t7-electrical.md):
  factory ECU supplies and grounds, crank/ignition diagnosis, and TWICE immobilizer requirements.
- [Original 9-5 MY2006–09 coolant service and oil-cooler VIN boundaries](docs/research/og95-cooling-service-2006-2009.md):
  three-year MY2007/08 coolant intervals, 7.4 L capacity, coolant chemistry, separate coolers, and source-date warnings on VIN torque thresholds.
- [Original 9-5 PCV, radiator and engine mount provenance](docs/research/og95-pcv-radiator-mount-provenance.md):
  factory campaign eligibility, manual/automatic radiator interfaces, mount VIN torque cutover and supplier cross-reference caveats.
- [Official Saab EPC access and cross-reference conflicts](docs/research/saab-epc-provenance.md):
  manufacturer VIN workflow, bushing/subframe identifier collision, and research restrictions.
- [Early 9-3 mount and petrol fuel research](docs/research/ng93-early-mount-fuel.md):
  2003–2005 factory revisions, convertible chassis suffix boundaries, and fuel-line safety.
- [Subframe and brake-line parts research](docs/research/subframe-parts-brake-lines.md):
  documented OEM assembly candidates, installation limits, and hydraulic safety.
- [9-3 structural research](docs/research/ng93-structure.md): corrosion-protection scope,
  body repair rules and specific subframe/convertible differences.
- [9-5 structural research](docs/research/og95-structure.md): factory repair boundaries,
  rust and inspection-relevant mounting areas.
- [9-5 2006–2008 source supplement](docs/research/og95-2006-2008.md):
  North American specifications, WIS conflicts and source limits.
- [Datasets](data/datasets/): structured JSON with source IDs and original links.

As of October 13, 2026 the database contains **489 source records, 972 factual
records, 73 issue records, 76 part records, and 237 explicit gaps** across thirty-one
research domains. This is not a completeness score.
See [the source index](docs/source-index.md) and [machine-readable inventory](data/inventory.json).

## What this contains

- Engine, lubrication, cooling, drivetrain, chassis, and electrical specifications
  where primary documents support them.
- Factory bulletins/campaigns with model, engine, VIN, and component restrictions.
- Useful part numbers and documented supersession relationships.
- References to diagnostic and ECU-analysis resources, with reuse/license notes.
- Explicit missing-input records for fitment, thermal, structural, performance,
  and durability evaluation.

Each finding is scoped to its evidence. A catalogued part is not automatically a
verified substitute for a particular installed part. A supplier's thermal claim is
not a measured lifetime improvement. A model-selection preference is not a
statistical reliability ranking.

## Inspect and validate

The tools use Python's standard library and require Python 3.10 or newer.

```sh
python3 tools/validate.py
python3 -m unittest discover -s tests -v
python3 tools/query.py --summary
python3 tools/coverage.py --format markdown
python3 tools/coverage.py --format json
python3 tools/phase0_audit.py --check
python3 tools/query.py --engine B235R --category cooling
python3 tools/query.py --platform 9-3-9440 --year 2006
python3 tools/query.py --text "intake valve" --kind issues
```

Query filters help find source-scoped records. They do not issue a fitment approval.
Unspecified applicability is treated as unknown, not as universal compatibility.
By default an applicability filter excludes records lacking that field; use
`--include-unknown` to inspect those records too.
Engine-code filters are exact: a family-level `B207` entry is not silently expanded
to `B207R`. Search by platform/year or text as well when exploring family-scoped
records. VIN, component serial, registration-history, and installed-hardware
conditions still require interpretation of the full record and source.

The snapshot is a census of **stored records**, not a reliability percentage or a verified parts catalogue. CI now checks that the generated audit tables and snapshot remain synchronized after future research PRs. The human subsystem assessments and [gap-closure gates](docs/gap-closure-plan.md) remain deliberately conservative.

## Add a particular car later

Use [the vehicle-instance template](templates/vehicle-instance.json) to record
identity, installed components, observations, and measurements. The template has
no invented vehicle data. Do not treat factory nominal specifications as measured
condition on an individual car.

## Source material and reuse

This repository contains original summaries, extracted factual records, and links.
Original manuals, catalogues, manufacturer documentation, and referenced software
retain their own rights and licensing terms. No third-party license is extended to
the entire repository. Referenced software is not vendored or executed by this
database.
