# Phase 0 gap-closure plan: make the Saab database useful before simulation

**Plan date:** 2026-10-12. Based on [the new all-domain coverage audit](coverage-audit.md) and [machine snapshot](../data/phase0-coverage-snapshot.json). This is a research execution order, not a claim that any inspected car is roadworthy or that a candidate part is approved.

## Scope and decision rule

**First configurations:** original 9-5 9600, US/Canada MY2004–09, petrol B235E/R four-cylinder and installed manual or five-speed automatic variants; second-generation 9-3 9440, US/Canada MY2005–06, FWD B207 with exact engine, body and gearbox variants. Model-year names are a search boundary, not a blanket statement of hardware interchange.

**Objective:** screen affordable non-running/running candidate Saabs for structural safety and unacceptable engine/transmission rebuild risks; then identify verifiable repair and preventive-maintenance options. **We are deliberately not building a vehicle ranking algorithm, life simulator, guaranteed Toyota-equivalent upgrade plan, or automatic parts-order system.**

**Research work is meaningful when it closes a named vehicle-inspection or OEM-fitment blocker, not merely when it adds 20 more records.**

## Ordered work packages

| Order | Gate | Work package and immediate source-backed gap | Deliverable / exit condition | Do not advance by assumption |
| ---: | --- | --- | --- | --- |
| **1** | A/C | **Vehicle identity and build configuration:** original factory US/CA VIN decode, engine/gearbox/body/market, build/serial cutovers; vendor catalog identifiers are secondary. | One verified identity sheet each for MY2004–09 9-5 B235 and MY2005–06 9-3 B207, showing exact year-by-year gearbox and major assembly exceptions, and what still needs an actual VIN. | A gearbox family string, model-year folder or reused production suffix is not proof of interchange. |

**Work package 1 progress, 2026-10-13:** [Priority original 9-5 and NG9-3 identity worksheets](research/priority-vehicle-identity-gates.md) now distinguish the major 9-3 transmission families, the suspension chassis option row, and a further 9-5 MY2009/2010 WIS VIN table mismatch. **This package is not closed:** dated original US-market VIN code pages for 9-5 MY2005–07 and 9-3 MY2006 are now recovered; **MY2008–09 9-5, Canadian variants, actual vehicle tag readings and paid Saab VIN-filtered WebEPC results remain missing**. Proceed with work package 2 (structural corrosion and safety) in parallel with these unresolved gates.
**Work package 2 progress, 2026-10-13:** [The structural inspection map](research/priority-structural-corrosion-inspection.md) now distinguishes OG9-5 SportCombi rear floor/frame members, rear captive nut mounting versus serviceable bush and subframe; NG9-3 CV inner/centre sill and rear reinforcement; B207 and US 9-5 fuel/handbrake pipe interdependencies; and New York's actual suspension-attachment, brake and fuel inspection criteria. **Not fully closed:** the MY2008 9-5 wagon revision, measured body integrity, real VIN, safe lifting, rust thresholds, approved frame fitment and professional repair estimate remain unknown. Work package 3 (brake/line options and hydraulic safety) is next.

| **2** | A | **Structural rust and safety:** front/rear subframes, rear suspension pickup points, jacking points, sills, engine/suspension mounting, brake/fuel pipe corrosion. Separate 9-5 sedan vs SportCombi and 9-3 sedan vs convertible. | Source-cited region/zone inspection inventory with photo/measurement checklist, repairability boundaries, tools and qualified-inspector escalations. Unknown severity stays unknown. | Never infer that a structurally rusted 9-5 wagon is a cheap suspension repair, or that visible surface rust is automatically unsafe. |
**Work package 3 progress, 2026-10-13:** [Brake hardware and hydraulic safety matrix](research/priority-brake-hydraulic-safety.md) maps original 9-3 2006 VIN plate brake option slots 7–10, four rotor+caliper levels, rear carrier versus guide-pin loads, different parking brake systems and underbody line requirements. **Safety-critical source discrepancy:** original 9-5 2008 brake carrier installation prose quotes 4 Nm, but dedicated Saab table reads 140 Nm +45 degrees (4 Nm is rotor locking screw). A second unresolved 9-5 2006/2009 rotor sizing conflict blocks choosing a replacement by model year alone. **Not fully closed:** no actual VIN/installed brake measurements, original OE WebEPC assembly/line parts, ABS/ESP hydraulic bleed verification or resolved 9-5 technical erratum. Next work package 4: non-running drivetrain and exhaust damage exclusions.

| **3** | A/B | **Brakes and hydraulic routing:** rotor/caliper/carrier options and wheel fit, flex/rigid brake pipes, parking brake and safe hydraulic service. | Factory option matrix by priority configuration, installed-part identification method, primary specs and stopping/safety criteria for a prospective purchase. | An eSaabParts listing or generic 9-5 model year is not enough to order a safety-critical brake assembly. |
**Work package 4 progress, 2026-10-13:** [Non-running Saab purchase protocol](research/priority-nonrunning-purchase-screen.md) and [blank evidence template](../data/inspection-templates/nonrunning-phase0.json) now distinguish seller evidence, passive visual safety, read-only DTCs, conditional qualified tests, and actual shop cost. Original Saab catalyst bulletin 248-2506 **excludes US/Canada** and requires a **running engine** for its supplementary Tech2 check; it is not a US MY2008 9-5 wagon diagnosis. No VIN, measured engine, gearbox, catalyst restriction or structural report has been obtained, so **Gate A remains partial**. Next is manufacturer EPC replacement provenance (work package 5); emissions/catalyst component completeness remains in package 6.

| **4** | A/B | **Non-running drivetrain condition:** distinguish missing-signal / control faults from measured internal oil/bearing/compression or clutch damage. Include turbo feed and real coolant/catalyst side effects. | Conservative non-running inspection worksheet: seller-document checks, cold visual examinations, safe supported tests, test instruments, conditional professional checks, mandatory unknowns and high-cost stop signs. | No full-throttle gearbox stall test, hot-coolant opening, false turbo shaft threshold or 'cheap fix' diagnosis from symptoms alone. |
**Work package 5 progress, 2026-10-13:** [Manufacturer USA VIN and conditional replacement-kit provenance](research/official-us-vin-service-kit-provenance.md) recovered Saab Automobile USA MY2004–07 original 9-5/9-3 VIN tables (including the missing US MY2005/06), identifies position 7 original gearbox and position 8 original engine by factory-year, and documents the official 9-3 ISM **12801010 → 32021815** as a **service kit requiring reuse of the intact original black sliding mechanism**, not a complete drop-in part. [Blank manufacturer OE replacement verification worksheet](../data/inspection-templates/oem-replacement-verification.json) requires a real VIN, EPC application, forward part-replacement relation, physical part, fitting and programming before approval. **Not completed:** original full USA MY2008/09 VIN documents, Canadian variants, actual vehicle VIN or paid Saab WebEPC serial/option result, and reliable OEM subframe/radiator/brake/gearbox chains. Gate C remains **not met**. Public research can next advance package 6 (US/Canadian exhaust and emissions hardware), while VIN-specific fitment awaits actual approved access.

| **5** | C | **OEM parts identifiers and directed replacements:** obtain Saab official WebEPC VIN-filtered numbers/relations for radiator manual vs automatic, PCV hoses, turbo feed hardware, subframes, brakes, sensors and ECU/TCM; verify serial and calibration restrictions. | Verified original OE part ID and conditional forward supersession where manufacturer explicitly documents it; capture accompanying hardware, dimensions and unsupported combinations. Create per-part evidence status and dated availability. | Manufacturer WebEPC may require paid access. If not obtained, explicitly mark **blocked by OEM evidence**; never promote retail cross-reference into Saab-approved fitment. |
| **6** | B/A | **Emissions/exhaust/catalyst, fuel/EVAP:** diagnose excessive backpressure or failed catalyst, cause of damage (misfire/rich fuel/oil), legal emissions differences, fuel line safety. | Complete priority-platform component routing and symptom differential with original US/CA emissions applicability and safe tests, for buying a car described as having a clogged converter. | A claimed plugged converter is not proof the engine, oxygen sensors, exhaust or transmission is intact. |
**Work package 6 progress, 2026-10-13:** [Original MY2008 9-5 B235 exhaust and fuel/EVAP research](research/og95-north-american-exhaust-fuel-wp6.md) documents the primary/main converter architecture, T7 oxygen sensor wiring and electrical faults, EVAP integrity faults, controlled running-car fuel pressure differential and NY converter rules. **Unfinished:** VIN-certified US/Canadian exhaust part number, legal exact-fit new replacement, wagon backpressure and fuel-line/body inspection, and 9-3 B207 T8 coverage. **Gate B remains not met.**

| **7** | A/B | **Current safety campaign and service baseline:** complete US/CA original regulator and factory service scope; fluid, filters, belts, brake, fuel, coolant and severe-duty intervals by year. | Official VIN-status-check process with links and a scoped schedule/inspection plan distinguishing historic factory approvals from current substitute products. | A campaign's inclusion in a bulletin does not prove free/unperformed work for a particular VIN. |
| **8** | B | **Broader 9-3 and neglected systems:** NG9-3 T8, later B207 revisions, HVAC, dashboard/comfort, steering, suspension and parts dependencies. | Target configuration matrix with named source-search outcomes, diagram/connector coverage, unresolved exclusions and safe service limitations. | Do not call these systems complete because there are a few isolated mentions in older datasets. |

## Five mandatory fields for every Phase 0 blocker

Each future blocker should carry a stable ID linked to an original `gaps` record or a new gap, the **specific car/configuration and system**, the **missing authoritative evidence or physical measurement**, the **required pass evidence**, and the **gate blocked**. A future status such as `closed` must name the source locator or vehicle measurement, never just say 'researched'.

A narrowly sourced fact may correctly apply to one year and still leave adjacent years unresolved. Reused URLs do not provide independent corroboration. Manufacturer part supersession, supplier reference, reverse interchange, physical fit and safety adequacy are distinct relationships.

## Vehicle inspection readiness categories

| Result | Evidence standard | Implication |
| --- | --- | --- |
| **Known factory configuration** | Documented scope plus matching actual vehicle identity, original build/installed hardware corroboration | Permits planning the proper inspection, **not** certification of condition. |
| **Ready for basic safe inspection** | Appropriate structural/safety inspection information and feasible no-disassembly observations with source references | Can inspect or request further documentation; still no purchase endorsement. |
| **Specialist required** | Structural integrity, gearbox contamination, severe overheating, internal compression/bearing issue or uncertain brake hydraulic safety | Avoid road use and major-spend commitment until professionally checked and costed. |
| **Evidence insufficient** | VIN/serial missing, source conflict, unknown actual vehicle measurements, or unauthenticated OEM fitment | Stop the fitment/reliability decision rather than filling the field with generic Saab facts. |

These are **qualitative gates**, not a numerical reliability score or pass/fail verdict on any actual car.

## Example use case already motivating this project

A **2008 9-5 wagon** offered with rear-subframe rust and a claimed clogged catalytic converter cannot be cleared by searching those two words in the database. Both conditions independently require diagnostic confirmation. The rear structure/suspension and underbody brake/fuel lines must be assessed for safe repairability; the exhaust restriction must be proved and its cause investigated before assuming an isolated inexpensive catalyst swap. The current research should help ask the correct questions, not replace actual inspection or predict a low-cost outcome.

## Phase 0 exit criteria (do not use record-count quotas)

- **Gate A:** An auditor can select a supported priority configuration and obtain a source-linked inspection plan covering exact identity, structure/brakes, critical engine/gearbox failure differentiation and recall process, with explicit unknown and specialist branches. No simulated vehicle data.
- **Gate B:** All priority subsystems are inventoried at component/connection level or each remaining omission has a named attempted first-party source-search result and applicability boundary. Conflicts remain visible and stop affected decisions.
- **Gate C:** Proposed replacement candidates have original part IDs and evidence-backed one-way supersessions, VIN/serial/market/body/gearbox/option conditions, mechanical interfaces and required software/hardware dependencies; missing OEM data explicitly blocks approval.

**Current status:** Gate A = partial, Gate B = not met, Gate C = not met. Do not promote any to 'passed' merely because the machine census grows.

## Working agreement for future PRs

1. Name **which work package and gate** the PR advances; explain what actual inspection or decision it unblocks.
2. Add verified scoped sources and newly supported facts **only when they close an identified gap**; keep gaps when missing VIN/OEM/measurement remains.
3. Avoid simultaneously opening numerous branches with overlapping inventory updates; one tested coherent PR at a time.
4. Update the dataset, inventory, source index and the reproducible Phase 0 snapshot. `python3 tools/phase0_audit.py --check` must pass alongside all existing tests.
5. Summarize **resolved versus still-blocked** acceptance criteria; no imaginary replacement approvals or percentage complete.

For the underlying existing research backlog and original P0 codes, see [research-backlog.md](research-backlog.md). For the numeric audit and current caveats, see [coverage-audit.md](coverage-audit.md).


### Work package 7 progress, 2026-10-13 (partial)

[Original MY2008 US/CA 9-5 service and historical recalls](research/priority-usca-service-recall-baseline-wp7.md) documents annual plus 10,000-mile manufacturer service, brake-fluid/fuel-line/exhaust and powertrain service intervals, and the crucial NHTSA **>15-year recall VIN-search blind spot**. The source-preserved MY2008 US/CA **60,000-mile ATF service checklist** conflicts with the annual-service **70,000 miles / 5 years** entry; no revision priority is established. The original US 08V160 MY2002–08 9-5 A-pillar, 16V063 MY2006–09 9-5 and MY2006–11 9-3 driver airbag with separate GM 15041/15043 programme notices, and MY2004–11 9-3 convertible 14V318 / Canada 2014228 retractor are now source recorded. The 2005–06 B207 US/CA interval, individual historical campaign completion and actual maintenance records are **not verified**. Gate A = partial; Gate B = not met; Gate C = not met. Work package 7 is not declared complete.


### Parallel Phase 0 workstream — cross-manufacturer replacement candidates (2026-10-13)

The [pilot research](research/cross-manufacturer-interchange-pilot.md) begins a strictly **research-only** shared GM/Opel/Fiat/aftermarket interchange inventory for MY2005–06 9-3 B207 FWD, contrasting a Saab-specific Nissens 9-5 automatic radiator and an **older, not-MY2008-proven** PCV kit. Catalogue SKF/PFI hub and common-brake-pad references are not approved donor fitments: actual VIN, OE maker parts, dimensions, ABS signal, brake codes, legal service and reliability testing are missing. This **does not close Gate C** or advance a simulator/reliability score. If a cross-marque common component is unproven, the database must retain it as a candidate rather than an approved replacement.
