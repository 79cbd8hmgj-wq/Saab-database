# Phase 0 Gate A/B — non-running Saab purchase inspection protocol

**Research date:** 2026-10-13. Priority vehicles are **original 9-5 (9600), US/CA MY2004–09 B235E/R four-cylinder**, and **second-generation 9-3 (9440), US/CA MY2005–06 B207**.

**Market vs assembly-plant distinction:** **US/CA** denotes the destination/homologation/sales market of the vehicle, **not its country of assembly**. Original 9-5s were built in Trollhättan, Sweden ([Saab's first-generation production notice](https://saabworld.net/wp/final-first-generation-saab-9-5-produced/)); the 9-3's manufacturing included Trollhättan, with convertibles also assembled in Graz, Austria ([WardsAuto, March 2005](https://www.wardsauto.com/news/archive-wards-saab-honing-premium-status/767545/)). Cars we're researching are North American-market examples regardless of their build plant. Consequently **\`ej US/CA\`** on the factory catalyst bulletin explicitly means **excluded from US/Canadian service-bulletin applicability**, even if the engine family and factory are shared. Such evidence may inform possible failure mechanisms but cannot authorize a North American factory test or emissions part. The purpose is to distinguish a *potential* minor peripheral repair from evidence of expensive internal damage or substantial uncertainty. This is an **inspection intake protocol**, not a completed inspection, a prediction of repair cost, an emissions-law interpretation, a parts authorization, or a vehicle simulator.

The machine-readable [blank intake worksheet](../../data/inspection-templates/nonrunning-phase0.json) contains evidence fields, assessment categories and stop conditions. It contains **no actual vehicle result**, no automated score, no actual VIN and no assumed repair cost. The original [vehicle-identity](priority-vehicle-identity-gates.md), [structural corrosion](priority-structural-corrosion-inspection.md) and [brake safety](priority-brake-hydraulic-safety.md) gates must be completed separately.

## 1. Stage the assessment by safety and evidence, not by the seller's fault label

| Stage | Minimum evidence requested | What remains explicitly unknown | Stop/escalate |
| --- | --- | --- | --- |
| **A — Before viewing:** seller's reason for parking the car, last successful run/movement, last inspection, damage history, title/VIN privately, vehicle/gearbox build, ownership, visible leaks, no-start attempts and prior diagnosis | Engine turning, internal bearing/compression condition, gearbox clutch integrity and seller statement accuracy | **Do not buy on “just a sensor” or “just a clogged cat” without evidence** |
| **B — Passive cold exterior observations:** underhood and underside only where safely visible, fluid *levels/appearance*, oil/coolant mixing signs, obvious absent drivebelt/hoses, fuel drips, underbody structure, tire/wheel/brake support, crash or previous weld evidence | Compression, hot oil pressure, catalyst physical restriction, working transmission | **Fuel leak, coolant ingestion, severe rust, exposed electrical fault, oil-starvation history**: no start attempt or road test |
| **C — Read-only electrical record:** existing scan DTCs and freeze-frame/TCM and ECM status *only when electrical power is safely available*; do not clear codes, reset TCM or program modules | Internal failure if no codes present; why historical codes were erased | Code may identify an electrical branch, but **does not certify a cheap fix** |
| **D — Conditional specialized tests:** competent technician determines whether controlled mechanical rotation, cylinder compression/leakdown, oil pressure, fuel pressure, intake leak test, exhaust restriction and ATF/TCM diagnosis can be safely performed | No result until actually measured under **correct source-year conditions** | Stop if engine might be hydrolocked, oil-starved, severely overheated or damaged, or vehicle cannot be secured |
| **E — Economic disposition:** segregated structural, engine, gearbox, exhaust/emissions, safety, tow/storage quotes and repairs requiring shop tools | Any unknown estimate or major failure is **not** $0 | If a repair requires an engine/transmission rebuild or uncertain structural bodywork, user objective is **not satisfied without a verified alternative** |

**Never** run a full-throttle automatic-transmission stall test on an unproven used car; the existing [MY2006 FA57 analysis](og95-turbo-tsb2912494-fa57-triage.md) explicitly records factory time/stress limits and the separate prohibition on warming the gearbox by stall testing. Never intentionally heat the car to a transmission overtemperature threshold, operate with known fuel leakage, loosen hot cooling components, rev a potentially oil-starved engine, or disconnect catalyst/O2 hardware as a shortcut around a diagnosis.

## 2. The 2008 9-5 wagon with “rear subframe rust” and “clogged catalytic converter”

We have **not seen the VIN or inspected the car**. This is a worked *question plan*, not a diagnosis.

First independently confirm the **2008 B235 variant, original factory US/CA emissions arrangement and actual installed gearbox**, and inspect the **rear body attachment points, rear floor, brake/fuel pipes**, not only the bolt-on subframe. See [the earlier corrosion report](priority-structural-corrosion-inspection.md).

For the engine/exhaust diagnosis, factory [MY2007 B235E/R front exhaust service](https://saabwisonline.com/9-5-9600/2007/2-engine/exhaust-system/adjustment-replacement/front-exhaust-system-with-catalytic-converters-b235e-r) explicitly names **catalytic converters** as a front exhaust assembly and oxygen-sensor wiring; [MY2007 engine system diagram](https://saabwisonline.com/9-5-9600/2007/2-engine/intake-system/technical-description/system-diagram-intake-turbo-exhaust-4-cyl) separately shows primary and main converters, front/rear silencers and turbo. A seller's generic “cat” label does **not** establish *which converter*, whether the downstream pipes/silencers are blocked, whether the catalytic cells are damaged, or whether a restrictive exhaust is the sole reason a car will not run. These documents do **not** establish identical MY2008 US/CA part number or legality.

### Important bulletin scope restriction

Original [Saab bulletin **248-2506**](https://saabwisonline.com/9-5-9600/2008/2-engine/trionic-t7-4-cyl/bulletins-si-mi/248-2506-supplementary-fault-diagnosis-catalytic-converter-t7-and-t8) is dated **November 2004** and says **Market: ej US/CA**, i.e. **not United States/Canada**. It appears in a **MY2008 WIS mirror folder**, but the folder **does not override the market exclusion or make it a MY2008 US service authorization**. The bulletin also literally prints model “9-5 (9660)” while the platform folder is 9600; this publication inconsistency remains recorded.

For its *specified non-US/CA* population, Saab describes this meaningful causal path: spark failure or incorrect fuel mixture can send unburned fuel into a hot catalyst, permanently damage its honeycomb/cell structure and create exhaust restriction; the vehicle may not yet have registered a DTC. Saab provides a **supplemental Tech 2 quick check**, requiring **Tech 2 v114.000+**, engine running and coolant **over 60°C**, and produces one of **converter OK, low oxygen absorption, high back pressure**. It estimates pressure indirectly from MAF and MAP values and can be misled if either sensor is faulty. **High backpressure requires looking farther downstream** before blaming the converter. The test **cannot be performed on a non-running vehicle**. It is **not verified for US/CA vehicle authorization**, and its three statuses do not provide an actual physical backpressure gauge reading.

The later-year [MY2005 9-5 T7 P0420 excerpt](https://saabwisonline.com/9-5-9600/2005/2-engine/trionic-t7-4-cyl/fault-diagnosis-diagnostic-trouble-codes/p0420) calls it *three-way catalytic converter malfunction*, **not** “exhaust physically clogged.” [MY2007 P1301 excerpt](https://saabwisonline.com/9-5-9600/2007/2-engine/trionic-t7-4-cyl/fault-diagnosis-diagnostic-trouble-codes/p1301) is cylinder 1 catalyst-damaging misfire. Those two individual DTC pages were available only as indexed excerpts here; they are explicitly tagged `search_excerpt`, not promoted to fully reviewed technical procedures.

**US MY2008 safe purchase response:** request original codes/freeze frames, misfire/fueling history, the reason a technician concluded restriction, where and how they tested it, if/when the vehicle last ran, whether oil/coolant was lost or overheat occurred, what emission hardware is currently installed, and a written quote. Do not budget “just a converter” until the cause and location are independently verified by a competent service provider and US legal requirements respected.

## 3. Original 9-5 Trionic T7: no-start without engine rebuild assumptions

Factory [MY2006 four-cylinder T7 ignition discharge module description](https://saabwisonline.com/9-5-9600/2006/2-engine/trionic-t7-4-cyl/technical-description/ignition-discharge-module) shows a module with four ignition coils, main-relay power and **ground G7**; an open supply can set **P1310** and trigger fuel shutoff. DTC **P0300–P0304** denotes emissions-related misfires; **P1300–P1304** denotes catalyst-damaging misfires with a flashing CHECK ENGINE lamp. Red ignition modules are expressly excluded from the T7 application. Ignition has high-voltage hazards and cannot be safely tested by arbitrary spark jumping on a fuel-leaking car.

Factory [MY2007 T7 leak, fuel pressure and adaptation page](https://saabwisonline.com/9-5-9600/2007/2-engine/trionic-t7-4-cyl/adjustment-replacement/leak-check-fuel-pressure-flow-capacity-and-adaptation-procedures) says **power or rough-running problems can occur without diagnostic codes**. That page specifies an **intake system controlled pressure ceiling of 0.6 bar** with Saab plugs and pressure regulator. It differs from other year-specific charge-air cooler testing and should **not be cross-applied**. The same manual describes a **3.0 bar fuel-vs-intake pressure difference** under measured conditions, with special gauges, fire extinguisher, ventilation and a **high-load driving assessment**. That last test is **specialist-only for an already safe driving car**, **never** a seller-lot operation and not proof of fuel pressure on an engine that cannot start.

Saab's [MY2007 turbo/ECU replacement checklist](https://saabwisonline.com/9-5-9600/2007/2-engine/trionic-t7-4-cyl/fault-diagnosis-general/checklist-for-changing-turbocharger-and-engine-control-module) retains **original DTCs without clearing, module software, VIN/engine serial, injector type, misfires and live manifold/charge-air values**. On a nonrunner the live readings are simply **unavailable**, not “normal.” A separate [MY2007 enhanced ignition diagnostic](https://saabwisonline.com/9-5-9600/2007/2-engine/trionic-t7-4-cyl/fault-diagnosis-general/enhanced-ignition-discharge-module-for-trionic-7) requires a supported T7 software function and Tech 2. Historic TIS2000/SPS in a factory page is **not evidence** of working 2026 support.

## 4. Mechanical engine risks do not disappear because a sensor fault is plausible

### Original 9-5 B235

The [MY2009 factory oil-pressure table](https://saabwisonline.com/9-5-9600/2009/2-engine/basic-engine-4-cylinder-petrol/technical-data/lubricating-system) states **at least 2.5 bar at 2000 rpm, 105±2°C oil temperature and 10W-30 oil**. The separate oil **warning sender** triggers around **0.3–0.55 bar**. Therefore an unlit warning light is **not** evidence of a healthy crankshaft or bearing pressure. The MY2009 value is not automatically a verified MY2008 production-specific specification; earlier documented 2005 figures are in the [high-cost diagnostics](high-cost-powertrain-diagnostics.md) report. There is **no meaningful hot-pressure test on a non-running car**.

A non-running B235 with repeated low-pressure lamps, bottom-end knock, severe overheating or suspected oil pickup blockage requires substantial professional evaluation. The source-backed 1998–2003 sludge bulletin is **not itself an approval to extrapolate every campaign repair or warranty year to 2008**.

### Second-gen 9-3 B207

The [MY2006 9-3 B207 factory general data](https://saabwisonline.com/9-3-9440/2006/2-engine/4-cylinder-petrol/basic-engine/technical-data/general-data) lists **12.4 bar minimum compression** for the B207 engine variants. Its [compression procedure](https://saabwisonline.com/9-3-9440/2006/2-engine/4-cylinder-petrol/basic-engine/adjustment-replacement/engine-compression-test) requires isolating relay 8, ignition coils, spark plugs and operating the starter with a test lead until reading stabilizes, each cylinder independently. Such a test depends on a **safely crankable** engine, proper instruments, and safe electrical/fuel practices. If the engine is seized or might contain fluid, **do not force rotation**. Compression alone may not distinguish valve-seat/timing damage versus piston ring/bottom-end damage; controlled leakdown and mechanical diagnosis may be required.

Saab's separately sourced later-model B207 intake valve bulletin, documented in [existing high-cost diagnostics](high-cost-powertrain-diagnostics.md), does **not** authorize automatically diagnosing that condition on every 2005–06 9-3.

## 5. Transmission risk and repair economics without destructive testing

Existing research in [repair versus replacement](repair-vs-replace-troubleshooting.md), [MY2005/09 FA57 triage](og95-turbo-tsb2912494-fa57-triage.md) and [MY2008 temperature protection](og95-atf-thermal-turbo-bulletin.md) differentiates selector/output sensor and solenoid electrical faults from actual ratios, clutch overheating and fluid contamination. **Neither a DTC nor a smooth stationary selector engagement certifies a gearbox**. Fluid grade, level-access method, TCM programming and gearbox identity vary.

Seller's non-runner provides no verified drive under load, converter lock-up or controlled 80°C ATF level test. Do **not** run brake-stall load tests, blind adaptation resets, overheating tests or a dangerous test drive. Record “**mechanical transmission condition unknown**,” request credible records and obtain a qualified estimate. A possible cheap TCM sensor or solenoid repair is not evidence that internal clutches are intact.

## 6. Purchase stop decisions

| Evidence | Conservative classification | Why |
| --- | --- | --- |
| Seller provides only "bad catalytic converter", no measured restriction or root cause | **Insufficient evidence** | Restriction location, catalyst upstream misfire and internal engine condition unresolved |
| Engine never turns over or previously seized, loss of coolant/oil, possible hydrolock | **Do not crank / specialist required** | Additional damage may result from attempted start |
| Verified low factory-condition oil pressure, actual severe bottom-end knock/bearing failure, or defective compression/leakdown | **Major engine risk** | Rebuild/replacement cost cannot be treated as zero |
| Gearbox untestable because vehicle will not run | **Mechanical gearbox condition unknown** | Cannot certify transmission lifespan or shift integrity from electrical codes |
| Confirmed internal slipping or contamination, qualified gearbox diagnosis | **Major transmission risk** | User seeks to avoid gearbox rebuild |
| Unsafe rear subframe/captive mount, corroded brake/fuel line, hydraulic leak | **Stop road test/structural or hydraulic safety gate** | Safety problem independent of engine/catalyst economics |
| A genuine external failed sensor, hose, ignition circuit or other controllable fault, plus separately verified healthy internals | **Possible smaller repair, conditional** | Only when vehicle-specific controlled tests and costs support it |

We intentionally **do not rank** any car, fill unanswered test data with passing values, infer current parts availability, or guess repair price. A non-running $1,200 Saab can have multiple simultaneous defects; the request is for robust **evidence collection before purchase**, not for an optimistic diagnosis.

## 7. Open blockers and follow-on

The data is improved for **inspection design** but no stage has been conducted on a vehicle. We still lack **US/CA authorized MY2008 catalyst backpressure diagnostic applicability**, actual converter stage/condition and upstream root cause, MY2008 oil-pressure confirmation, controlled compression/leakdown and verified 2005/06 B207 applicability, transmission load observations and ATF labs, and written corrosion/exhaust/engine/gearbox quotes.

**Next research package:** precise exhaust/catalyst, fuel/EVAP and US/Canadian emissions-system mapping (work package 6) can complement the still-blocked OEM WebEPC manufacturer part numbering (work package 5). Both are separate from the present safe buyer-intake worksheet.
