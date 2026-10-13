# Phase 0 research coverage audit — 35-domain refresh

**Audit basis:** October 13, 2026, 35 research datasets. This release adds original Saab Automobile USA MY2004–07 VIN documents and manufacturer-channel conditional service-kit provenance; earlier Phase 0 audit baselines remain in merged pull-request history. This is a census of saved records, **not** an independent recertification of every original Saab source, an estimate of percent complete, or an engineering safety certification. The earlier seven-domain baseline is superseded.

**Living guardrail:** `tools/phase0_audit.py` recalculates all numeric tables from `data/datasets/*.json`. Its checked-in companion `data/phase0-coverage-snapshot.json` is verified by unit tests and `python3 tools/phase0_audit.py --check`. A new research PR must refresh these numbers when datasets change; otherwise CI should fail.

<!-- BEGIN AUTO-GENERATED PHASE0 CENSUS -->
## Current database snapshot (automatically verified)

| Measure | Current records |
| --- | ---: |
| Research domains | 35 |
| Source records | 525 |
| Unique source URLs | 461 |
| Technical facts | 1034 |
| Diagnostic/correction issues | 85 |
| Part records | 80 |
| Explicit open research gaps | 261 |

A repeated URL is not independent corroboration. These are stored record counts,
**not** estimates of system completeness, part fitment confidence, failure rates,
or the probability that an individual vehicle is repairable.

### Source retrieval and evidence

| Source retrieval | Records |
| --- | ---: |
| `full_text` | 495 |
| `partial` | 3 |
| `search_excerpt` | 19 |
| `metadata_only` | 8 |

| Technical evidence | Facts + issues + parts |
| --- | ---: |
| `documented` | 1092 |
| `supplier_claim` | 98 |
| `inference` | 9 |

### Explicit application dimensions

A record may legitimately lack a dimension when its source is general. Missing
dimensions are **unknown**, never a blanket approval. Grouped applicability
is counted from individual groups, not from a misleading top-level union.

| Scope field explicitly present | Records out of facts + issues + parts |
| --- | ---: |
| `platforms` | 1141 / 1199 |
| `model_years` | 1044 / 1199 |
| `markets` | 204 / 1199 |
| `engine_codes` | 341 / 1199 |
| `transmission_codes` | 167 / 1199 |
| `body_styles` | 83 / 1199 |
| `vin_ranges` | 24 / 1199 |

### Technical record coverage by original Saab model year

Only facts/issues/parts with the **same applicability group** specifying both
platform and year are counted. Repeated records can appear in more than one
model-year row. Year-path names do not prove a given production revision.

#### Original 9-5, platform 9600

| Model year | Facts | Issues | Parts |
| ---: | ---: | ---: | ---: |
| 1998 | 16 | 3 | 8 |
| 1999 | 18 | 3 | 11 |
| 2000 | 22 | 3 | 14 |
| 2001 | 17 | 3 | 14 |
| 2002 | 29 | 5 | 19 |
| 2003 | 31 | 4 | 17 |
| 2004 | 60 | 7 | 20 |
| 2005 | 158 | 11 | 21 |
| 2006 | 153 | 16 | 20 |
| 2007 | 134 | 18 | 19 |
| 2008 | 181 | 26 | 19 |
| 2009 | 126 | 15 | 19 |

#### Second-generation 9-3, platform 9440

| Model year | Facts | Issues | Parts |
| ---: | ---: | ---: | ---: |
| 2003 | 20 | 15 | 18 |
| 2004 | 34 | 17 | 21 |
| 2005 | 75 | 16 | 21 |
| 2006 | 115 | 18 | 26 |
| 2007 | 26 | 11 | 22 |
| 2008 | 28 | 11 | 23 |
| 2009 | 21 | 11 | 23 |
| 2010 | 20 | 12 | 23 |
| 2011 | 24 | 12 | 22 |

### Parts evidence does not equal approved interchange

| Part-record metric | Count |
| --- | ---: |
| Records in research database | 80 |
| Have at least one recorded part relationship | 22 |
| Supported as a supplier claim | 52 |
| Explicitly marked as needing vehicle verification | 49 |

A relationship can be an aftermarket cross-reference, kit contents, or a
conditional supersession. Its existence does **not** make the replacement
VIN-approved, bidirectional, or suitable for a safety-critical repair.

### Distribution of recorded evidence by research domain

| Dataset domain | Sources | Facts | Issues | Parts | Gaps |
| --- | ---: | ---: | ---: | ---: | ---: |
| `b235_maintenance_fa57_identity` | 13 | 44 | 2 | 0 | 9 |
| `b235r_oil_pcv_2006_2008` | 17 | 31 | 2 | 7 | 9 |
| `corrections` | 27 | 9 | 20 | 26 | 7 |
| `cross_manufacturer_front_hub_pilot` | 4 | 7 | 0 | 1 | 5 |
| `cross_manufacturer_interchange_pilot` | 11 | 14 | 3 | 3 | 6 |
| `epc_provenance` | 10 | 12 | 0 | 2 | 5 |
| `high_cost_powertrain_diagnostics` | 17 | 35 | 3 | 2 | 9 |
| `ng93` | 25 | 70 | 0 | 0 | 8 |
| `ng93_body` | 8 | 25 | 0 | 0 | 6 |
| `ng93_early_mount_fuel` | 15 | 20 | 0 | 5 | 7 |
| `ng93_structure` | 21 | 30 | 0 | 1 | 8 |
| `official_us_vin_and_service_kit_provenance` | 7 | 15 | 3 | 2 | 6 |
| `og95` | 30 | 90 | 0 | 0 | 7 |
| `og95_2006_2008` | 7 | 25 | 0 | 0 | 6 |
| `og95_atf_thermal_turbo_bulletin` | 14 | 28 | 3 | 2 | 9 |
| `og95_body` | 10 | 25 | 0 | 0 | 5 |
| `og95_cooling_service_2006_2009` | 15 | 30 | 3 | 0 | 9 |
| `og95_ground_power_0709` | 13 | 44 | 2 | 0 | 6 |
| `og95_north_american_exhaust_fuel_wp6` | 8 | 14 | 3 | 0 | 5 |
| `og95_pcv_radiator_mount_provenance` | 16 | 31 | 3 | 8 | 9 |
| `og95_structure` | 12 | 16 | 0 | 1 | 5 |
| `og95_t7_cooling_0709` | 28 | 72 | 3 | 0 | 7 |
| `og95_t7_electrical` | 22 | 43 | 4 | 0 | 7 |
| `og95_turbo_oil_feed_solenoids` | 14 | 39 | 3 | 0 | 9 |
| `og95_turbo_tsb_2912494_fa57_triage` | 13 | 31 | 3 | 0 | 9 |
| `priority_brake_hydraulic_safety` | 19 | 25 | 4 | 0 | 8 |
| `priority_nonrunning_purchase_screen` | 13 | 20 | 4 | 0 | 8 |
| `priority_structural_corrosion_inspection` | 14 | 21 | 3 | 0 | 8 |
| `priority_usca_service_recall_baseline_wp7` | 13 | 27 | 6 | 0 | 8 |
| `priority_vehicle_identity_gates` | 13 | 15 | 2 | 0 | 6 |
| `repair_vs_replace_troubleshooting` | 17 | 31 | 4 | 0 | 9 |
| `replacements` | 8 | 10 | 0 | 5 | 3 |
| `simulation` | 20 | 40 | 0 | 0 | 15 |
| `subframe_parts_brake_lines` | 17 | 16 | 0 | 15 | 9 |
| `vin_gearbox_provenance` | 14 | 29 | 2 | 0 | 9 |

<!-- END AUTO-GENERATED PHASE0 CENSUS -->

## Assessment of the original Phase 0 gates

| Milestone | Current judgment | Why it is not fully passed |
| --- | --- | --- |
| **Gate A: shopping reference** | **Partial; not certified** | Factory structural, failure and identity evidence exists. A non-running or rusty car still needs a vehicle-specific VIN/build and chassis/underbody inspection, realistic major-work exclusion criteria, and recall status. |
| **Gate B: system documentation** | **Not met** | Coverage is uneven; brakes, emissions/catalyst, fuel/EVAP, HVAC, late 9-3 B207 and genuine part assembly inventories remain patchy. A handful of targeted documents is not a complete subsystem account. |
| **Gate C: interchange research** | **Not met** | Part links include retailer claims, kits and cross-reference identifiers. No current VIN-filtered manufacturer WebEPC source is available to approve a complete candidate parts swap. |

Gate A permits *planning a qualified inspection*, not declaring an unknown Saab safe or ready to buy. Gates B/C require **evidence closure by defined assembly and vehicle configuration**, not an arbitrary total fact count.

## Qualitative subsystem assessment

**Legend:** Focused = multiple directly useful factory sources within selected years; Partial = some verified sources but no complete assembly/configuration matrix; Critical gap = missing information materially blocks an inspection, safe replacement, or parts order. Labels are analyst judgments and deliberately are **not quantitative percentages**.

| System | Original 9-5, especially US/CA B235 MY2004–09 | Second-gen 9-3, especially US/CA B207 MY2005–06 | Next missing acceptance evidence |
| --- | --- | --- | --- |
| VIN, market, build and powertrain identity | Partial / critical fitment gap | Partial / critical fitment gap | Correct year/engine/gearbox mapping, original VIN decoder, installed codes, build changes |
| Engine oil, PCV, sludge, compression | Focused for selected B235 years | Partial, B207 cold-intake valve issue documented | Year-specific mechanical limits and evidence of damage, safe non-running screen |
| Turbo, induction and charge air | Focused diagnosis / critical mechanical limits | Partial | Model/turbo-specific shaft wear limits, oil feed verification, boost hoses |
| Cooling, radiators, fan control | Focused 9-5 2007–09 / conflicted replacements | Partial / some quantity conflicts | Complete plumbing, exact manual vs automatic radiator and coolant variants |
| FA57, manual gearbox, driveline | Focused 9-5 automatic diagnostics / parts incomplete | Partial; early FA57 coolant bulletin is distinct | VIN/serial and TCM variants; complete repair and donor compatibility |
| Structural corrosion, subframes, mounting | Partial; critical for rusted 9-5 wagons | Partial | Zone-by-zone inspection sheet, body repair boundaries, metal thickness and load assessments by competent shop |
| Brake calipers, rotors and hydraulics | Partial / conflicting rotor applications | Partial / critical inventory | Rotor/caliper/carrier option matrix, line routing, hydraulic safety and measured wear |
| Suspension, steering, wheels | Partial | Partial | Configuration/option code, mounts, suspension geometry, spring/corrosion limits |
| Ignition, grounds, ECU and security | Focused Trionic 7 sources, still incomplete | Partial, limited detailed T8 and immobilizer inventory | Exact module hardware/software and wiring/connector dependencies |
| Exhaust, catalysts, emissions and EVAP | Critical gap | Critical gap | Factory catalyst/oxygen-sensor/EVAP fault isolation and market/OBD compliance |
| Fuel delivery and safety | Partial | Partial | Year-specific fuel plumbing, pump pressure, underbody route and safe leak isolation |
| HVAC, passenger comfort, electrics | Critical gap | Critical gap | Component inventory, sensors/motors, diagnostic and repair dependencies |
| Recalls and safety campaigns | Partial | Partial | Complete US/CA regulator campaigns, factory scope, official current VIN-status check |
| Maintenance intervals and consumable approvals | Partial | Partial | Complete year/engine/gearbox severe-service schedule and currently approved consumables |
| OEM parts, supersessions, substitutes | **Critical gap** | **Critical gap** | Saab WebEPC VIN-filtered OE numbers, original production changes and explicit direction of substitutions |

**Interpretation:** Original 9-5 is currently the stronger documented platform, not necessarily the more reliable vehicle. The existing records cannot establish which model has a lower lifetime failure probability. The 2005 9-5 is heavily documented in year-scoped records; research density is not a failure-rate or buying ranking.

## Major unresolved bottlenecks and stop conditions

1. **Exact identification and original OEM parts chain.** Even when a source provides a gearbox family name, individual hardware, variant calibration or manufacturer parts supersession remains unknown. Do not approve an assembly, donor gearbox or electrical module solely because it looks similar or uses the same marketing name.
2. **Unsafe underbody and corrosion ambiguity.** A visibly rusty subframe, rear suspension mount, jacking location or brake line must be assessed by a competent inspector before road use or price-based assumption of an inexpensive repair. No invented generic rust-depth pass threshold.
3. **Brake and hydraulic assembly uncertainty.** Different rotor and caliper/carrier variants cannot be ordered by model-year shorthand; measure or read installed option and OEM EPC.
4. **High-cost engine and gearbox risk.** Factory diagnostic branches sometimes identify smaller causes (sensor, hose, valve, control software), but a documented possibility of a cheap fault does not establish that a specific engine/turbo/FA57 is mechanically intact.
5. **Exhaust and catalysts are a true purchase-screen blind spot.** For a non-running 9-5 described as having a “clogged catalytic converter,” confirm the actual restriction and whether prolonged heat, misfire or internal engine damage occurred; replacing the catalyst is not a guaranteed remedy.
6. **Year-presentation and cross-platform WIS conflicts.** Workshop year path, model name or reused transmission nickname cannot substitute for the original bulletin publication date, factory applicability, original part, full VIN or measured installation.
7. **Reliability outcome evidence.** No representative controlled miles-to-failure curves, component aging tests, costs for an actual vehicle or validated comparison to Toyota durability are available. The database supports fault isolation and sourcing questions, not a Toyota-equivalent guarantee.

## Acceptance milestones (non-numeric gate conditions)

### Gate A — inspection-ready research reference

For each priority vehicle configuration (**original 9-5 US/CA MY2004–09 B235 manual/automatic, and 9-3 US/CA MY2005–06 B207 FWD**): identify engine, gearbox, body and production restrictions; provide inspection zones for structure, safety and brakes; link source-supported signs distinguishing cosmetic from structural risks; map high-cost no-buy conditions to qualified diagnostic requirements; provide official recall lookup instructions and current source. Unknown VIN/build, rust severity or mechanical measurements must produce **unknown / specialist verification**, not a 'pass'.

### Gate B — documented priority vehicle systems

Every priority subsystem must have an explicit component and connection inventory for the selected configurations, the applicable first-party service specifications and common failure mechanisms, and an explicit *source-search record* for items not recoverable. Resolve source conflicts with an original authoritative record or keep a clearly bounded gap. Avoid promoting descriptive diagrams into specifications and copied WIS directory years into production changes.

### Gate C — responsible replacement candidate screening

For any proposed substitution, preserve installed OE part ID, VIN/engine/gearbox/market/option restrictions, genuine manufacturer-approved supersession direction **where evidenced**, dimensions/interfaces, safety and loading requirements, firmware/pairing/dependencies and installation tests. Supplier cross-references must remain supplier claims. If original manufacturer support cannot be obtained, mark **not approved / evidence pending**; do not assume bidirectional interchange.

## What this milestone changes

The expanded cross-maker evidence includes PFI wheel-hub, SKF catalogue, and option-restricted Saab/Opel brake-pad candidates. These remain source-scoped supplier claims and do not supersede the stronger original Schaeffler manufacturer FAG pilot; a shared aftermarket SKU does not certify an interchangeable original donor assembly.

First cross-manufacturer pilot: direct Schaeffler FAG front wheel-hub cross-references for Saab and GM/Opel, with Saab WIS MY2006 hub/speed-sensor dependencies. A common aftermarket kit does not establish identity of a used donor hub or better durability; exact VIN, geometry, electrical and safety validation are open. Candidate-approval guards are now separate from the overall source count.

Original MY2008 Saab 9-5 US/Canada scheduled maintenance conflicts on automatic gearbox oil: a numbered 60,000-mile service checklist calls for replacement while the annual additional-work section lists 70,000 miles or 5 years. Both original statements are now stored separately, with explicit missing factory revision and vehicle inputs, and neither is promoted to a universal service recommendation.

The WP7 recall follow-up captures the original US 08V160 A-pillar noncompliance, Saab/GM 16V063 driver airbag programme notices 15041 and 15043, US 14V318 convertible-only driver belt retractor and Canadian 2014228 mirror recall. Registration history and VIN-specific completion are deliberately not inferred; old campaign remedies remain professional-service items rather than recommended DIY substitutions.

Work package 6 initial B235 evidence now documents two-stage MY2008 exhaust architecture, T7 O2 and EVAP circuits, safer fuel-differential diagnostics, and New York's conditional lawful converter replacement requirements. These are source-scoped facts only; the 2008 wagon still has no measured restriction, US/Canada VIN-matched OEM catalyst or fuel-line safety finding. Gate B remains unmet.

Work package 5 recovers dated USA 2004–07 9-5/9-3 VIN reference bulletins and a genuine conditionally serviced 9-3 ISM kit with mandatory original mechanism reuse. The original 2008–09 US VIN year pages and licensed VIN-specific EPC approval remain open. Work package 4 adds a blank non-running pre-purchase evidence intake and records the explicit US/Canada exclusion of Saab's historic catalyst diagnostic bulletin; the latter cannot authorize US-market procedures. No real car has been assessed. Work package 3 now maps 9-3 four brake hardware levels and identifies a dangerous 9-5 front-caliper torque discrepancy plus unresolved rotor-dimension conflict. Those conflicts block part/torque approval until authoritative verification. Work package 2 now adds source-linked 9-5 wagon underbody structure, NG9-3 CV sill/brace dependencies and NY DMV minimum safety checks; individual vehicle structural health and 2008 revision proof are still blocked. Work package 1 has now added scoped 9-5 and 9-3 physical identity worksheets, but the missing 2005–09/2006 VIN decoding and VIN-filtered WebEPC records remain explicit blockers. We should **stop** making consecutive micro-PRs solely to increase fact count. Each future research batch should reference a named Phase 0 gate and inspection- or interchange-blocking missing evidence, supply a real source outcome, and update the systematic audit. No release-quality parts recommendation, purchase score, or simulation claim follows from the current inventory.

The next work queue is in [the prioritized gap-closure plan](gap-closure-plan.md). Structural safety, vehicle identity and current OEM part applicability precede optional deeper boost/TCM numeric research.

## Reproduce and maintain

```sh
python3 tools/validate.py
python3 -m unittest discover -s tests -v
python3 tools/coverage.py --format json
python3 tools/phase0_audit.py --check
python3 tools/phase0_audit.py --format markdown
```

The snapshot is derived only from the saved files and cannot confirm individual source validity or a real Saab's condition. The human qualitative matrix requires explicit review when new domains or configurations are added.


## Work package 7 partial baseline (2026-10-13)

[Original US/Canada 2008 9-5 maintenance and historical recall lookup](research/priority-usca-service-recall-baseline-wp7.md) adds manufacturer-market scheduled inspections and explicit 15-year NHTSA VIN recall display limitations. This is not proof that individual vehicle recalls or servicing were completed. Gate A remains partial; B/C not met. The 2005–06 B207 US/CA service mileage remains unresolved.
