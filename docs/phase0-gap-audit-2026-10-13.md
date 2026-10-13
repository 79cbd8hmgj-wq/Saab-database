# Phase 0 independent gap audit and rebuild-platform decision checklist

**Audit date: 2026-10-13.** This reviews the existing [40-domain census](coverage-audit.md), [gap-closure plan](gap-closure-plan.md), [original research backlog](research-backlog.md) and source-linked research datasets. It is a **documentation and scope audit**, not an added first-party Saab source, an inspection, an OEM parts approval, a new reliability study or a score.

## Core problem identified

The repository has a substantial volume of *targeted* 9-5 B235 and 9-3 B207 research, but **does not yet offer symmetric, comparable screening of the full group of Saab models we might encounter cheaply**. Current priority configurations are reasonable research pilots, **not justified winners**. A source-rich 9-5 and catalogue-rich 9-3 cannot be ranked by counted articles, listed parts, number of recall bulletins, or anecdotal failure statements.

**Scope we have compared deeply:** original 9-5 MY2004–09 B235 manual/FA57 and NG9-3 MY2005–06 B207 FWD. **Not on the same footing:** early 9-5 1998–2003 PCV/engine variants, later 9-3 B207 2007–11, 9-3 B284 V6, 9-3 XWD and different body/gearbox configurations. Those variants require a separate **screening scope decision** before exclusion. This is not a statement that they are better or worse, nor that they all have the same US-market availability. Farther-out Saab/GM/Subaru derivatives (9-2X, 9-7X, etc.) have not been treated as drop-in candidates for this original Saab engineering comparison.

## Phase 0 blockers we should tackle before choosing a model

| Order | Audit item | Existing source-linked gap IDs (or **new question**) | What would change a purchase decision |
| --- | --- | --- | --- |
| 1 | **Universe of candidate Saabs** | New audit question `P0-U01` | Establish the actual year/engine/gearbox/body variants in the inexpensive market before comparing only B235 with B207 |
| 2 | **Costly engine and gearbox failures** | `nrscreen-gap-007`, `hcdiag-gap-002`, `hcdiag-gap-005`, `gateac-gap-003` | Evidence-backed safe test, actual condition and credible *repair without internal rebuild* / replace / walk-away cost for each configuration |
| 3 | **Rust of structural body and subframe mounting points** | `rustgate-gap-001`, `rustgate-gap-002`, `rustgate-gap-005`, `rustgate-gap-007` | A professional can distinguish a replaceable subframe from an unsafe or uneconomic rotten body mount, including wagon/convertible differences |
| 4 | **Original vehicle identity and parts** | `gateac-gap-001`, `gate5-gap-002`, `gate5-gap-004` | Original USA/CA year tables and actual original VIN filtered OE components; not seller shorthand or WIS-directory year |
| 5 | **Safety-critical brake/line uncertainty** | `hydbrake-gap-001`, `hydbrake-gap-002`, `hydbrake-gap-003` | Resolve original Saab 9-5 rotor/carrier contradictions and 9-3 brake option assemblies before selecting replacement parts or torque |
| 6 | **OEM maintenance and recall completion** | `wp7-gap-003`, `wp7-gap-004`, `wp7-gap-008`, `wp7-gap-001` | Actual service history, year-specific US/CA schedule and historical campaign completion; retain 2008 9-5 ATF contradiction |
| 7 | **Electronics, keys, diagnostic tooling** | `elec-g001`, `elec-g002`, `elec-g003`, `og95t7-gap-004` | Bound the cost and availability of T7/T8 ECU/DI, TWICE/CIM, immobilizer and qualified Tech2/clone services; require actual hardware |
| 8 | **Exact US-market sourced replacement economics** | `usparts-gap-001`, `usparts-gap-002`, `usparts-gap-003` | Comparable delivered price, availability, warranty, shipping, tools/labor and programming for genuinely matching parts |
| 9 | **9-3 B207 emissions, EVAP, underbody fuel** | `wp6-gap-005`, `early9three-gap-006` | Comparable factory US/CA intake-to-tailpipe and underbody-safe diagnosis against the better-researched 2008 B235 |
| 10 | **Comparable real-life durability** | `maint-gap-005`, `elec-g004`, `usparts-gap-003` | Matched repair/failure rates and severe-work exposures; without them, no ranked reliability probability |

## Under-tracked *systems* rather than merely unresolved part numbers

**These are new coverage questions, not discoveries that a part fails frequently.** Original subsystem-specific evidence has not yet been gathered systematically for both priority configurations:

- `P1-U01`: **Steering and suspension**: pump/rack, tie rods, struts/springs, rear links and body mount/geometry, power-steering hydraulics versus electrical variants as actually fitted; option codes, safety inspection, specialist equipment, costs.
- `P1-U02`: **HVAC and water ingress**: heat/defrost and A/C, blend/recirculation actuators, blower wiring, drains and water-damaged electrical paths, cost to restore a daily-driver interior by body/year.
- `P1-U03`: **Full electrical diagnosis toolchain**: fuse/bus/connector and ground maps, key/security pairing, Tech2 access, safe read-only controls and support availability. Existing T7 electrical pages are useful but not a complete vehicle-wide troubleshooting manual.

Current datasets can contain facts about these systems; **that is not the same as component/connection-level documentation for all target years**. [Machine-readable register](../data/audits/phase0-gap-register-20261013.json) labels existing gaps and new questions explicitly.

## Two different kinds of 'missing' that should not be conflated

- **Desk-research blockers:** Original Saab US/CA maintenance and VIN tables; primary parts diagrams, model/engine/options and original TSB scope; complete subsystem component and wire/pipe routing; actual US price observations. We can keep working on these without owning a Saab. Each search must record exact source/outcome and its limitations.
- **Vehicle/market evidence blockers:** Actual inspected structure, donor engine/gearbox fluids and function, VIN-specific Saab WebEPC, recall-completion history, donor component stamps, prices quoted to a specific repair. No amount of general documentation can certify an unseen car or prove its interchange. These should be marked `needs_specific_vehicle_data`, not 'research failed'.

## Recommended next Phase 0 sequence

**Work package A — broaden the selection denominator first.** Build a **configuration universe**: year range, body, engine family, gearbox and driveline for every Saab type realistically encountered in our search. Record common severe-work/parts blockers *only where original evidence exists*, and designate unresearched candidates honestly. Do not penalize an option for having fewer web results. This may change which engines/years deserve detailed research.

**Work package B — equalize catastrophic and structural screening.** Complete the engine/transmission non-running safe inspection and high-cost replacement matrix for the B235/FA57 and B207 with its true gearbox variants, plus wagon/sedan/convertible rust mounting evidence, brake system constraints and actual quote pathways.

**Work package C — fill critical subsystems, then revisit model choice.** First-party 9-3 emissions/EVAP/cooling, T8/T7 whole control/security interfaces, steering/suspension and HVAC; exact VIN-filtered OE fitment and comparable US parts acquisition prices. Only after these inputs should we produce an *evidence-limited qualitative* shortlist of Saab configurations.

### Exit rule

**Gate A partial; Gate B not met; Gate C not met.** We do not change the gate until the [existing acceptance criteria](gap-closure-plan.md) are met, which require source-located component/connection coverage and actual vehicle checks where applicable. Add true new `gaps` entries to datasets only alongside a correctly scoped source-search outcome; this standalone gap register adds **zero** facts or parts to the database. A green validator proves structural consistency, not engineering equivalence.
