# U.S. Saab project cars: repair versus replace feasibility (Phase 0)

**Prepared 2026-10-13.** Scope is originally sold U.S. Saab 9-3 and 9-5, MY1998–2011, **factory automatic**, **front-wheel drive**, **no convertibles**. Canadian research is preserved without further work. This report is a **diagnostic purchase-screening guide and research-gap register**, not a reliability ranking, a parts approval, a repair quote or evidence that any particular car has a fault.

The machine-readable [14 source-scoped feasibility scenarios](../data/vehicle-catalogue/us-repair-replace-feasibility.json) reuse **37 already-researched references** from the original [high-cost powertrain](../data/datasets/high-cost-powertrain-diagnostics.json), [nonrunning purchase](../data/datasets/priority-nonrunning-purchase-screen.json), [repair-versus-replace](../data/datasets/repair-vs-replace-troubleshooting.json), [structural corrosion](../data/datasets/priority-structural-corrosion-inspection.json) and [Saab automatic transmission](../data/vehicle-catalogue/us-automatic-gearbox-evidence.json) datasets.

The [110-row applicability index](../data/vehicle-catalogue/us-repair-feasibility-coverage.json), produced by [`tools/build_us_repair_feasibility_coverage.py`](../tools/build_us_repair_feasibility_coverage.py), links scenario IDs to **configuration groups that warrant certain checks if a symptom or history is present**. **A group matching a scenario DOES NOT mean any Saab in that group has experienced the failure.** Year/body/engine and VIN applicability restrictions apply before parts or advice.

## Practical decision tiers

These tiers depend on a *verified fault*, not a make/model reputation:

- **Potentially DIY** — discrete fault found in hoses, sensors, ignition, external cooling, charge-air plumbing or bolt-on hardware **after** mechanical health, safety and proper exact-model procedure are confirmed.
- **Advanced DIY / specialist** — gearbox adaptation and diagnosis, accurate hot mechanical oil pressure, valve-body or solenoid diagnosis, B207 leakdown/valve sealing, safe subframe removal; may require Tech2, a lift, significant tooling or machining.
- **Usually reject unless a fully costed replacement/restoration is acceptable** — demonstrated lower-end bearing damage, confirmed coolant-contaminated FA57 requiring complete transmission replacement, persistent internal slipping after correct diagnosis, severely degraded structural mounting metal, or unsafe brake/fuel lines with no feasible repair budget.
- **Unknown condition** — nonrunning or untestable vehicle. Missing evidence does **not** mean "easy fix"; do not assume that a low asking price makes an engine, gearbox or chassis sound.

There are **no supported universal dollar prices or hours** in the sources reviewed. Every scenario deliberately stores `price_estimate_usd:null` and `labor_hours_estimate:null` pending quotes and part/VIN identification. No repair is guaranteed.

## 14 repair-feasibility scenarios

| ID | Subsystem / evidence scope | Repair-first question | Major risk if verified |
| --- | --- | --- | --- |
| 001 | **Early B205/B235**, original 9-3 and 9-5 within Saab U.S./CA TSB **210-2554** MY/VIN scope | Is pressure/pickup/PCV/chain fault separable from bearing damage? | **Short block** if bearings damaged; no-rebuild purchase normally reject |
| 002 | Original 9-5 **B235 MY2004–09** lubrication | Is the fault sender, accessible oil system or actual loss of mechanical pressure? | Internal engine damage; original early sludge bulletin not silently extended |
| 003 | Second-gen 9-3 **B207** rough cold start/compression | Ignition/fuel/ECM vs controlled leakdown and intake-valve sealing? | Machine-shop cylinder-head service or replacement engine |
| 004 | Early 9-3 **FA57 5AT MY2003–05**, **VIN-gated** | Is coolant contamination actually present and model/VIN within Saab **TA440-0702**? | Factory bulletin directs **complete transmission** replacement when coolant in ATF confirmed |
| 005 | Original 9-5 **FA57 MY2002–04** shift concerns | Tech2 DTC, software/adaptation, servo, speed sensor, valve housing before condemning gearbox? | Some cases ultimately require gearbox replacement |
| 006 | **MY2007 9-5 FA57** P0748 or CHECK GEARBOX | Solenoid circuit/harness/pressure fault or internal issue? | Internal transmission damage only after proper diagnosis |
| 007 | FWD 9-3 **B284L/AF40 6AT MY2006–08** | Is delayed shifting attributable to low ATF using *Saab* controlled level test? | Continued hard shifting requires specialist assessment |
| 008 | **MY2007 9-5 B235** underboost or turbo rattle | Wastegate linkage, diaphragm, boost pipes, control vs failed turbo? | Turbo assembly plus possible oil-feed issues |
| 009 | **MY2007 9-5 B235** overheating | External coolant leak/thermostat/cap vs heat-damaged engine? | Cylinder head/internal engine damage |
| 010 | **MY2005–08 9-5 B235** seller's "clogged catalytic converter" | Prove actual restriction AND misfire/oil-burning upstream cause; P0420 alone insufficient | Converter plus unresolved engine failure |
| 011 | Original **9-5 rear subframe / body anchor** | Sound shell + removable subframe, or corroded load-bearing floor/frame/captive nut? | Professional structural restoration / walk-away |
| 012 | Second-gen **9-3 rear subframe** | Replaceable rear subframe vs unsafe body anchor/fuel/brake line corrosion? | Structural shop intervention |
| 013 | **Every eligible vehicle** brake or fuel line safety | Any leaking, dangerously corroded lines, or unsafe hydraulics? | **No drive until repaired**; safety independent of engine condition |
| 014 | Original 9-5 FA57 **2002–09** gearbox removal | Is the transmission irreparable after diagnosis, and is a complete swap feasible with proper lifting, subframe and torque-converter support? | Major equipment/time/replacement cost |

The source links, exact original factory procedure years, safety conditions, exclusions and open questions for each scenario are in the JSON. A **MY2007 procedure is not claimed to be an OEM-approved MY1999 or MY2011 procedure**.

## Manufacturer decisions that change the plan

**Early B205/B235:** Saab U.S./Canadian bulletin **210-2554 edition 3** provides a specific decision tree for chain/oil contamination complaints, including short-block replacement for confirmed bearing damage. The U.S. engine review links **28 source-derived production groups** to the bulletin's *potential* engine/year scope, **not to 28 known engine failures**. Do not apply this bulletin indiscriminately to B204, B207, B284, B308, 2011 A20NFT/LHU or later original 9-5 model years.

**Coolant in early 9-3 FA57 ATF:** [Saab TA440-0702](https://saabwisonline.com/9-3-9440/2005/4-transmission/automatic-transmission/5-speed-fa-57/bulletins-si-mi/ta440-0702-coolant-in-atf-oil) specifies **9-3 Sport Sedan MY2003–05 below VIN 51002378**, and separate convertible/diesel entries not part of this U.S. candidate set. **Ten** compiled U.S. 9440 five-speed model groups fall in a pre-screen year/automatic range, but **not all ten are proved to be below the VIN cutoff**. The source describes a heated-fluid test; **do not conduct its open-flame diagnostic technique as a DIY check**. Qualified contamination testing and original TSB-guided cooler diagnosis are needed before spending money.

**9-5 FA57 poor shifting:** [Saab TSB 440-2497](https://saabwisonline.com/9-5-9600/2003/4-transmission/automatic-transmission/bulletins-si-mi/440-2497-general-fault-diagnosis-for-automatic-transmission) describes 2002–04 five-speed-specific symptom-driven paths: sensor, TCM software, adaptation, servo cover, modified valve housing and some replacement-gearbox outcomes. It is strong evidence against **diagnosing all hard shifts as a dead gearbox**. It is not evidence that every failing FA57 is cheaply repairable.

**9-5 rear subframe:** Saab original WIS has an actual [rear-subframe captive-nut replacement procedure](https://saabwisonline.com/9-5-9600/2006/8-body/body/adjustment-replacement/nut-piece-rear-subframe), including floor access and protection. That procedure does **not** authorize driving with perforated unibody mounts or turning a structurally rotten floor into a safe DIY bolt-on repair.

## 110-group screening coverage audit

The index covers all **110** U.S. eligible compiled-production groups and includes a general brake/fuel safety check for every group. It maps **28 groups** to the early-sludge engine/year *bulletin screening*, **10 groups** to an early 9-3 FA57 *VIN-required cooler screening*, **17 groups** to MY2002–04 9-5 FA57 *shift diagnosis*, **64 groups** to original 9-5 rear body-anchor inspection, and **34 groups** to second-gen 9-3 rear subframe inspection. These group counts are **not failures, likelihood estimates, or current vehicles on the road**.

**14 of 110 groups remain without a specific powertrain repair-feasibility scenario**; they are all in early 9-3 **B204L**, original 9-5 **B308E V6**, or 2011 new 9-5 **2.0T (A20NFT/LHU factory VIN candidate)** groups. They do receive general safety/structure screening as applicable, but shouldn't be considered equally studied to the B235/B207 groups. Research must fill these gaps before any uniform "Toyota-level reliability" or reasonable DIY cost comparison.

### Priority unresolved evidence

1. **B204L, B308E and 2011 Turbo4** source-backed major failure differential tests, repair-versus-replace steps and original gearbox/engine mechanical service parts.
2. **Real local parts/labor costs** by exact car/year/VIN and cheapest safe repair path, not guesses or posted parts prices alone.
3. **Structural integrity** of original 9-5 rear subframe mounts and 9-3 body anchors across body styles, especially Northeast corrosion exposure.
4. **Detailed 9-3 MY2003–05 cooler bulletin VIN applicability**, completion history and any coolant ingress test result.
5. **Current legal emissions parts** and correct U.S. catalyst diagnostics for original 9-5, not a non-US technical bulletin substitute.
6. **Individual vehicle inspection:** VIN, factory engine/case plates, safe fluid/compression/pressure tests, verified TCM/engine codes, corrosion photographs, no-drive hazards, and complete itemized parts/labor estimate.

## Data-integrity policy and commands

The 14 decision scenarios reuse existing source records; **the technical database counts and Phase 0 gates are unchanged**, and the current source-derived matrix makes **zero statements about diagnosed real cars**.

```sh
python3 tools/build_us_repair_feasibility_coverage.py --check
python3 -m unittest discover -s tests -v
python3 tools/validate.py
python3 tools/phase0_audit.py --check
```

**Phase 0 remains Gate A partial, Gates B/C unmet.** This phase supports screening and research prioritization, not final rankings or guaranteed repairs.
