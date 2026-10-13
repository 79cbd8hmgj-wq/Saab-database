# Phase 0: prioritized research backlog

This is a **database research plan**, not a simulation roadmap or an instruction to buy parts. **Current execution sequence:** use the [October 2026 Phase 0 gap-closure plan](gap-closure-plan.md) and [fresh all-domain coverage audit](coverage-audit.md) in preference to the original seven-domain baseline below. Gate A (inspection reference) is partial; Gates B (complete priority system documentation) and C (OEM interchange) are not yet met. Research tasks should close an actual inspection, structural safety or VIN-specific parts blocker—not merely add facts. Target platforms: OG 9-5 (`9-5-9600`), especially US/CA MY2004–2009 B235 configurations, and NG 9-3 (`9-3-9440`), initially US/CA MY2005–2006 B207 FWD. Other Saab variants remain eligible for future research; their absence here is not a negative reliability rating.

Priority definitions: **P0** = materially affects safe purchase screening, expensive engine/transmission avoidance or part ordering; **P1** = important completeness for DIY service and diagnosis; **P2** = engineering-depth research that can follow the core records.

## P0 — close safety, identity, drivetrain and specification gaps first

| ID | Research unit | Source leads / actions | Acceptance condition |
| --- | --- | --- | --- |
| P0-01 | Structural corrosion and body repair, both platforms | Factory body repair / rust-protection information; parts diagrams for front/rear subframes, jacking and suspension mounting points, sills, brake/fuel line routing, wagon rear structure; original service and official inspection criteria where applicable | Component/zone-oriented records with inspection locations, structural-vs-cosmetic distinction, applicable repairs and limits; clearly separate documented factory procedures from unverified rust anecdotes. Do not assign a universal safe rust threshold. |
| P0-02 | MY2006–2009 OG 9-5 2.3 powertrain coverage | Year-specific US/CA manuals, WIS revisions, engine and gearbox identity references; compare MY2005 and MY2009 findings against intervening years without filling by assumption | Enumerate B235R/trim and gearbox applications by year/market; add evidence-backed mechanical specs and production changes with year-scope. The original 5/5/2 figures were from the seven-domain baseline and are superseded by the live Phase 0 snapshot; do not treat record count alone as sufficiency. |
| P0-03 | MY2005–2006 NG 9-3 B207 FWD coverage | US/CA owner manuals, factory identity/VIN sheets, WIS revision history, gearbox and turbo charts | Distinguish documented B207 variants, transmission, trim and body styles; preserve later Griffin and 2.8 V6 boundaries rather than expanding them into B207 data. |
| P0-04 | Complete brake configurations and wear diagnosis | WIS brake matrix, rotor/caliper/carrier identification, line routing and hydraulic procedures; compare documented OE numbers and measured dimensions | Resolve or explicitly preserve OG 9-5 disc conflicts; provide brake-assembly evidence for NG 9-3; no auto-ordering recommendation based on a nominal year. |
| P0-05 | VIN/build/option identification and applicability | Factory VIN guides, chassis labels, EPC chassis identifiers, component revision and serial boundaries | Make a vehicle identity worksheet with separately stated VIN suffix, engine code, gearbox code, body, market and relevant option codes; do not infer full VINs or compare chassis suffixes as generic integers. |
| P0-06 | Engine/transmission high-cost failure screening | Original TSBs and WIS diagnostic procedures: OG 9-5 sludge/PCV/oil pressure; 9-3 ATF/cooler leakage, B207 intake valve/compression and coolant loss; other evidenced severe mechanisms | For each case record symptoms, distinguishing tests, thresholds and test conditions where available, major-work consequences, applicability and what a pre-purchase inspection cannot establish. |
| P0-07 | Complete safety campaigns and current recall process | NHTSA recall filings, Saab factory implementation bulletins, owner notices and VIN-specific official check mechanism | Keep regulatory population, repair implementation and actual car recall status separate; record geographic/registration/VIN restrictions and retrieval dates. No assumption that historical coverage means free work today. |
| P0-08 | Factory service schedule and condition-based inspections | US/CA owner/manual service schedules, severe-service instructions, service bulletins, fluid and filter approvals | Evidence-linked intervals and tests per engine/gearbox/year, with distinct historic factory specification vs present-day substitute approval; proposed preventive improvements must have rationale and limitations. |

## P1 — fill out repairable vehicle systems

| ID | Research unit | Required evidence and outcome |
| --- | --- | --- |
| P1-01 | T7/T8 and vehicle electronics | Fuse/relay/ground maps, wiring diagrams and connector pinouts, sensors/actuators, module communications, immobilizer pairing dependencies, safe diagnosis. Do not treat plug shape as software compatibility. |
| P1-02 | OEM parts catalogue and supersession chains | Capture part identity, assembly group, exact supported configurations, OEM supersession direction, required hardware and aftermarket reference **separately**. Supplier inventory and price must be timestamped rather than treated as durable fact. |
| P1-03 | Cooling and forced-induction assemblies | Hose routing, thermohydraulic service envelopes, coolant pump/thermostat/radiator fans, intercooler and turbo oil/coolant lines; catalogue/geometry compatibility distinguished from thermal-life claims. |
| P1-04 | Steering, chassis and fasteners | Detailed bushings, struts/springs, spring corrosion, mounts and linkages, installation torques, load limits and chassis code mapping. |
| P1-05 | HVAC, climate and passenger systems | A/C and heat circuits, ventilation actuators, blower/controls, wiring, service diagnostic steps and special tools; no inference from generic GM component similarity. |
| P1-06 | Exhaust, catalyst, emissions, fuel and EVAP | OEM diagrams, O2 and related sensors, catalyst variations, evap components, regulatory scope, diagnostic paths and repair requirements. |
| P1-07 | Practical DIY service procedures and tools | Service access, required specialty tools, safe lifting/support points, factory testing thresholds and non-destructive inspection techniques, with exact source and applicability. |
| P1-08 | Parts supply and current aftermarket choices | Revalidate manufacturer/catalogue source, exact SKU, physical dimensions, materials and supplier claims; record observation dates and avoid stock/price permanence. |

## P2 — depth after the core database is more complete

| ID | Research unit | Boundary |
| --- | --- | --- |
| P2-01 | ECU calibration and diagnostics | Research documented signal semantics, software/hardware IDs and lawful read-only acquisition. No acquired binaries or undocumented compatible-flash claim. |
| P2-02 | Engineering inputs | Collect measured operating ranges, vehicle/engine component geometry, material properties, load spectra, raw log provenance and uncertainty for possible later validated calculations. Do **not** run a performance/life simulator during this phase. |
| P2-03 | Independent durability evidence | Seek model/engine-specific fleet or component failure distributions with denominators, age, mileage, market, maintenance and censoring controls. If absent, retain unknown risk and use qualitative failure mechanisms only. |

## Definition of done for each research unit

1. Inventory applicable vehicle configurations and assemblies before recording specifications; explicitly mark anything unresolved.
2. Cite original publisher, document identity, retrieval strength, exact page/table/section, revision/publication date where available, and accessed date.
3. Preserve factory units, test temperature/conditions and verified platform–model-year–engine–gearbox–body–market pairings. Use grouped applicability for coupled scopes.
4. Record distinct failure mechanisms, symptoms, diagnostic differentiation and factory correction, **without** estimating a failure probability from a service bulletin.
5. Distinguish OEM part number and supersession from catalog cross-reference and independent engineering validation.
6. Add a gap when documentation is incomplete or contradictory. Never silently resolve a conflict or turn absent data into broad fitment.
7. Validate JSON and test query/applicability behavior. Update [coverage audit](coverage-audit.md) only when coverage actually changes.

## Current blocker-first execution and CI discipline

The original numbered P0/P1 items remain broad research categories. Actual next work should follow [ordered blockers and per-work-package exit criteria](gap-closure-plan.md): (1) VIN/gearbox/build, (2) structural rust and hydraulic safety, (3) exact brake/underbody configurations, (4) non-running major-work exclusion, (5) WebEPC OEM interchange, (6) emissions/catalyst/fuel, (7) recall/service scope, and (8) remaining 9-3/HVAC systems.

**Every database-changing research PR must refresh** the reproducible `data/phase0-coverage-snapshot.json` and auto-generated section of `docs/coverage-audit.md`; CI enforces agreement using `python3 tools/phase0_audit.py --check`. Passing this does not imply original source recertification.

## Phase 0 milestone gates (research only)

- **Gate A — shopping reference:** Complete P0 safety/structure/identity/drivetrain research for the priority 9-5 and 9-3 configurations. The record should be usable to plan an inspection, not to certify a car sight unseen.
- **Gate B — system documentation:** No priority subsystem remains unresearched *without* a named source-search outcome and gap description. Major model-year conflicts have either evidence-backed resolutions or explicit open restrictions.
- **Gate C — interchange research:** Part and dependency records are sufficiently specific to screen candidates for an individual car, while unresolved dimensions, programming, structural loading or tests continue to block approval.

No numerical record target or nominal percentage substitutes for these gates. These are proposed review criteria, not claims that the database presently meets them.
