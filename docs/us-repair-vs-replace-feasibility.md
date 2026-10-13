# U.S. Saab repair-versus-replace feasibility matrix — Phase 0

**Research date: 2026-10-13.** Candidate universe: **110 compiled U.S. production configurations** of Saab 9-3/9-5 MY1999–2011 with **factory automatic, FWD and nonconvertible bodies**. Canadian records were not modified. This is a **decision and evidence plan**, not any particular vehicle's diagnosis, a probability-of-failure model, a parts approval or a priced build estimate.

The [scenario dataset](../data/vehicle-catalogue/us-repair-replace-feasibility.json) contains **14 repair-versus-replace scenarios** with **37 references already represented in the Saab project's existing research datasets and WIS engine/gearbox crosschecks**. The generated [110-group applicability crosswalk](../data/vehicle-catalogue/us-feasibility-coverage.json) links an engine, gearbox, structure or safety diagnostic research topic to the groups it *could* concern. It does **not** say the cars have those faults. All numeric part costs, total jobs and labor time are **unverified/null**; all frequency, VIN inspection, parts-interchange and replacement-approval flags remain **false**.

## Purchase decision categories

| Research result | Decision approach | Requirements before purchase |
| --- | --- | --- |
| Isolated external component fault — e.g. verified turbo actuator clip, cooling hose, sender | **Possible DIY project** | Original-year WIS procedure; exact VIN-specific part and tool inventory; demonstrate engine and gearbox fundamentally sound |
| Electrical/control/hydraulic fault — e.g. DTC P0748, FA57 servo-cover/valve housing/adaptation, AF40 low fluid | **Diagnose first** | TCM/engine codes, Tech2 and factory temperature-dependent tests; estimate only the fault actually established |
| Confirmed internal bearing damage, coolant-contaminated early 9-3 FA57, persistent proven internal gearbox fault | **No internal rebuild** | Walk away **or** separately price a VIN-compatible complete engine/gearbox replacement with specialist tooling; do not assume it is inexpensive |
| Structural metal failure at rear subframe anchorage, floor, rail or corrosion-compromised lifting/brake/fuel areas | **Safety hold / structural professional** | No road test until safe; qualified body/safety inspection and written restoration quote. A detachable subframe does not repair rusted unibody mounts |
| Unknown condition / nonrunning with no safe mechanical evidence | **Unassessed, not a cheap fix** | Seller permission and non-destructive mechanical tests, transport costs, VIN/codes, corrosion inspection; unresolved hard risks generally justify declining a marginal-price car |

The categories are conditional decisions consistent with the user's no-internal-engine-or-transmission-rebuild preference. They are **not predictions** about individual sellers' cars.

## Evidence-backed repair versus replacement scenarios

| ID | What appears wrong | Qualifying U.S. groups matched | What must be separated | DIY / specialist / stop |
| --- | --- | ---: | --- | --- |
| `us-feas-001` | **MY1999–03 B205/B235** sludge, chain or oil-pressure symptoms | **28** | Oil warning sensor/pickup/chain vs **measured bearing damage**; Saab US/CA 210-2554 ed.3 applies only within its engine/year scope | External service if proven and bearings sound; confirmed bearing damage: **short-block/replacement or walk away** |
| `us-feas-002` | MY2004–09 original 9-5 B235 low oil pressure | **30** | Actual hot pressure/sender/pickup versus internal bearing wear | Sensor/oil-system service may be DIY; confirmed lower-end failure outside internal rebuild goal |
| `us-feas-003` | MY2003–11 9-3 B207 cold misfire/compression | **28** | Ignition/fuel/T8 ECM vs measured **valve/cylinder sealing loss** | Isolated electronics DIY possible; proven mechanical sealing may need head/machine shop or replacement |
| `us-feas-004` | Early 9-3 **FA57 ATF with coolant**, M03–05 **VIN-limited** | **10** potential groups | Confirm coolant contamination and actual full VIN cutoff below bulletin; a group match **does not establish affected VIN** | Saab advice instructs **complete transmission replacement** if contamination clearly confirmed; not a simple flush |
| `us-feas-005` | Original 9-5 FA57 MY2002–04 harsh/late shift | **17** | Servo cover, SLS/SLT valve housing, sensor, TCM software/adaptation vs internal slip | Tech2 and gearbox-specific mechanical diagnosis before any assembly replacement |
| `us-feas-006` | Original 9-5 FA57 **MY2007 P0748** | **6** | Pressure-control solenoid electrical signal/harness vs internal hydraulic failure | Diagnose wiring/TCM first; DTC alone does not condemn complete gearbox |
| `us-feas-007` | 9-3 AF40 2006–08 delayed shifting | **6** | Saab TA440-0902 warm, running, Tech2-controlled **ATF level** versus deeper fault | Advanced DIY with tooling / specialist; low ATF is a documented differential, **not a universal cure** |
| `us-feas-008` | Original 9-5 MY2007 B235 underboost/rattle | **6** | Wastegate linkage/diaphragm/charge piping versus mechanically failed turbo/oil supply | Often externally diagnosable; replace turbo only with objective fault confirmation |
| `us-feas-009` | Original 9-5 MY2007 B235 overheating | **6** | External thermostat/coolant fault vs overheating-induced engine/head damage | Thermostat etc. can be DIY after diagnosis; unsafe engine until cause/damage checked |
| `us-feas-010` | Original 9-5 MY2005–08 B235 **seller claims clogged catalyst** | **19** | Misfire/fueling/boost/oil burning and measured restriction vs P0420-only claim | Diagnose upstream engine before paying for a legal catalyst replacement; no shortcut assumption |
| `us-feas-011` | Original 9-5 rear subframe/captive-nut/unibody corrosion | **64** screening groups | Detachable subframe or bushing vs structural rail/floor/mount anchor | Bolt-on service possible if sound mounts; structural metal failure: professional evaluation or walk away |
| `us-feas-012` | 9-3 9440 subframe/underbody/fuel-pipe rust | **34** screening groups | Replaceable rear suspension unit vs unsafe unibody anchors/pipe routing | No road use until safe; structural failures outside beginner DIY |
| `us-feas-013` | All eligible Saabs — brake/fuel pipe corrosion | **110** screening groups | Hydraulic/fuel safety inspection, affected components, body structure | **No road use if leaking or unsafe**; properly repaired and inspected before operation |
| `us-feas-014` | Original 9-5 MY2002–09 FA57 confirmed nonrepairable transmission | **42** | Exact OEM type, actual fault, donor control/calibration, cooler condition | Saab WIS complete-unit removal involves **engine beam, subframe fixtures and lift**; obtain true shop/DIY-equipment quote or walk |

The numbers above are **source-derived applicable production *configuration groups***, not a fleet size, vehicle-failure count, frequency or percentage.

### Major source distinctions

**Early B205/B235 engine:** Saab US/CA [TSB 210-2554 ed.3](https://saabwisonline.com/9-5-9600/2000/2-engine/basic-engine-4-cylinder-petrol/bulletins-si-mi/210-2554-ed-3-noise-from-the-timing-chain-and-oil-sludge-in-the-engine) checks symptom-specific oil pressure, pickup and bearing damage and requires short-block replacement when bearing damage is found. The special-policy text is historic, **not proof of active coverage in 2026**.

**MY2002–04 original 9-5 five-speed:** Saab [TSB 440-2497](https://saabwisonline.com/9-5-9600/2003/4-transmission/automatic-transmission/bulletins-si-mi/440-2497-general-fault-diagnosis-for-automatic-transmission) distinguishes valve housing, servo cover, software, speed sensor and adaptation faults from certain conditions where gearbox replacement is necessary. The TSB must not be projected to all later-year FA57 cars.

**Early 9-3 five-speed coolant ingress:** Saab [TA440-0702](https://saabwisonline.com/9-3-9440/2005/4-transmission/automatic-transmission/5-speed-fa-57/bulletins-si-mi/ta440-0702-coolant-in-atf-oil) applies M03–M05 sedans up to a specified production VIN and directs complete gearbox replacement once coolant contamination is confirmed. Its **original hot-fluid/open-flame contamination method is not an instruction to repeat unsafely**; request a professional closed-system test.

**9-3 AF40 ATF:** Saab [TA440-0902](https://saabwisonline.com/9-3-9440/2006/4-transmission/automatic-transmission/6-speed-af-40/bulletins-si-mi/ta440-0902-atf-oil-check-on-af40-6-speed-aut) explains a temperature/engine-running Tech2 fluid level procedure, not a lifetime reliability verdict.

**Original 9-5 structural mount:** [Saab MY2006 rear captive-nut replacement](https://saabwisonline.com/9-5-9600/2006/8-body/body/adjustment-replacement/nut-piece-rear-subframe) is a fastener-service procedure and does **not** make a corroded floor, rail or mount safe. A project such as an **2008 9-5 wagon with reported rear-subframe rust and a seller-attributed blocked catalyst** needs independent structural and engine/exhaust diagnosis; neither claim is a verified repair estimate.

**Complete automatic replacement:** The [MY2007 original 9-5 gearbox removal procedure](https://saabwisonline.com/9-5-9600/2007/4-transmission/automatic-transmission/adjustment-replacement/complete-automatic-transmission) specifies engine support and special subframe/lift equipment. Merely having a source-compatible used gearbox is not sufficient to price a DIY swap.

## Missing inputs before a real purchase recommendation

**Evidence we still need per actual car:** complete VIN decoded against original market/MY/engine/AT; title/status; recorded mileage and maintenance history; safe underbody floor/rail/subframe/brake/fuel photographs and preferably lift inspection; safe engine oil pressure/compression/leakdown and cooling condition if indicated; TCM/ECM DTCs and gearbox fluid assessment; current VIN-specific parts supply; realistic labor/tool/rust repair estimates; towing/storage/registration budget. Actual fault frequency, repair success rates and durability gains remain unmeasured.

**For the research programme:** Expand these source-scoped feasibility branches to remaining engine families **B204L, B284L, B308E and 2011 A20NFT/LHU** with manufacturer failure-mechanism documentation and real parts/access evidence, rather than assigning favourable or unfavourable scores because fewer problems have been documented.

This work does **not** update the repository's original 40-domain inventory census or advance Phase 0 Gate A/B/C to completion.

## Reproduction

```sh
python3 tools/build_us_feasibility_coverage.py --check
python3 -m unittest discover -s tests -v
python3 tools/validate.py
python3 tools/phase0_audit.py --check
```

To regenerate the crosswalk after changing a scenario or production entry: run `python3 tools/build_us_feasibility_coverage.py` and review the diff before committing.
