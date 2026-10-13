# High-cost fault triage: turbo underboost, FA57 shifting, overheating (original 9-5)

Research date **2026-10-12**.

**Scope correction (factory bulletin reviewed later):** The turbo/wastegate retaining clip example is based on Saab **bulletin 291-2317, January 2002, non-US/Canada, B205E/B235E only**. Its presence in a 2007 WIS mirror folder does not establish that the campaign applies to a 2007 model-year car or US/Canada B235R. See [the corrected turbo bulletin and ATF temperature report](og95-atf-thermal-turbo-bulletin.md). Database scope: original 9-5 (9600) petrol four-cylinder and five-speed automatic, with model-year limits **per source**. This is not a simulator, failure-probability model, repair authorization, or parts-fitment approval. Never test-drive a smoking/knocking/overheating car to force a diagnostic reading.

## Decision logic for inexpensive project cars

| Seller symptom | Lower-cost cause to rule out first | Factory evidence | When serious damage remains a possibility |
| --- | --- | --- | --- |
| Weak turbo boost, rattle, possibly P1105 | **Non-US/CA B205E/B235E only** for 2002 wastegate clip bulletin; other cars still need independent hose/diaphragm/boost diagnosis | [2007-indexed fault symptom](https://saabwisonline.com/9-5-9600/2007/2-engine/turbocharger-system/fault-diagnosis-fault-symptoms/low-engine-power-output-little-movement-on-the-turbo-pressure-gauge-and-rattling-from-the-turbocharger) (indexed **excerpt only**); [bypass valve test](https://saabwisonline.com/9-5-9600/2007/2-engine/turbocharger-system/adjustment-replacement/checking-the-charge-air-bypass-valve-4-cyl) | Actual shaft or compressor damage, severe oil-smoke source, no oil feed; requires independent tests |
| MY2002–03 hard shift, delayed P-D, 2–3 flare | B4 servo cover, faulty/slow valve body, TCM software/adaptation, fluid quality, speed sensor or wiring depending on symptom | [TSB 440-2497](https://saabwisonline.com/9-5-9600/2003/4-transmission/automatic-transmission/bulletins-si-mi/440-2497-general-fault-diagnosis-for-automatic-transmission) | Continued slipping/internal hydraulic faults after factory diagnostic sequence |
| MY2007 CHECK GEARBOX / limp-home | P0748 solenoid electrical circuit, P0722 missing output speed signal, poor ATF condition, wrong gearbox/TCM ID | [P0748](https://saabwisonline.com/9-5-9600/2007/4-transmission/automatic-transmission/fault-diagnosis-diagnostic-trouble-codes/p0748), [P0722](https://saabwisonline.com/9-5-9600/2007/4-transmission/automatic-transmission/fault-diagnosis-diagnostic-trouble-codes/p0722) | Verified clutch slip/internal contamination/failed mechanical checks |
| Coolant loss/temperature rising | Hose, cap, thermostat, grounding near sensor, fans/circuit, radiator leak or improper bleed | [2008 limits](https://saabwisonline.com/9-5-9600/2008/2-engine/cooling-system/technical-data/temperature-pressure-limits); [2007 thermostat service](https://saabwisonline.com/9-5-9600/2007/2-engine/cooling-system/adjustment-replacement/thermostat-4-cyl) | Warped head, compromised head gasket, piston/bearing damage from a genuine severe overheat |

This is a **diagnostic-order guide**. The existence of an inexpensive possible fault does not mean the car actually has that fault, that repairs are affordable, or that an engine/transmission is intact.

## 1. Turbocharger: the first-movement boost test is not maximum boost

The [2007-indexed Saab boost actuator adjustment procedure](https://saabwisonline.com/9-5-9600/2007/2-engine/turbocharger-system/adjustment-replacement/checking-and-adjusting-basic-charging-pressure) specifies the pressure at which the **wastegate actuator rod just begins to move** using a pressure pump:

- Garrett GT17 on B205E / B235E: **0.40 bar**;
- Mitsubishi unit on B235R: **0.45 bar**;
- mechanical pushrod pre-tension **2 mm**, with locknut torques split by **engine serial 7011078/7011079** (20 / 21 Nm).

These are **bench-style actuator test readings**, not peak manifold boost, ECU desired boost or a do-it-yourself tuning recommendation. The 2007 [charge-air bypass diaphragm procedure](https://saabwisonline.com/9-5-9600/2007/2-engine/turbocharger-system/adjustment-replacement/checking-the-charge-air-bypass-valve-4-cyl) requires testing whether the valve holds vacuum, then pressure. A damaged diaphragm won't build vacuum. Neither defect proves the turbo shaft itself is ruined.

The independently retrieved [MY2005 charge-air leak test](https://saabwisonline.com/9-5-9600/2005/2-engine/turbocharger-system/adjustment-replacement/test-pressurization-of-the-charge-air-cooler-and-pressure-pipes-4-cyl) describes an **isolated and capped pressure test around 1 bar** with a leak threshold of **more than 0.1 bar loss in 30 seconds**. It explicitly warns against excess pressure damaging hoses and connections. This number is entered for **MY2005 only**. A 2007 car needs its own verified test procedure before anyone treats it as universal.

**Critical:** the wastegate clip case is a January 2002 non-US/CA B205E/B235E bulletin even though it appears under a MY2007 path. No direct US/CA B235R approval was found.

The [2007 T7 turbo/ECU replacement checklist](https://saabwisonline.com/9-5-9600/2007/2-engine/trionic-t7-4-cyl/fault-diagnosis-general/checklist-for-changing-turbocharger-and-engine-control-module) calls for recording diagnostic data and engine/ECU software IDs. We have **search-result excerpt only** for this and for the clip-loss fault page, so neither is marked as fully re-opened evidence.

## 2. MY2002–04 automatic bulletin is narrowly applicable

Saab [TSB 440-2497, dated October 2004](https://saabwisonline.com/9-5-9600/2003/4-transmission/automatic-transmission/bulletins-si-mi/440-2497-general-fault-diagnosis-for-automatic-transmission) applies to **MY2002–04 five-speed automatic OG9-5, all markets**. Its symptom rows frequently only cover **MY2002–03**. The factory specifically distinguishes:

- Hard 2→3 shifts under limited acceleration: inspect **B4 servo cover** first, then perform appropriate adaptation.
- Delayed/hard P→D and N→D: modified valve housing **5449780** is a bulletin-specific candidate for **MY2002–03**.
- 3→2 deceleration hesitation: TCM software/compatibility check.
- Lock-up slipping: ATF amount and quality, flow through cooler hoses, DTC and fault recurrence **before** replacement.
- Very hard D/R engagement: check cold ATF temperature reading vs real ambient and inspect wiring/connector.
- Some MY2003 cars may actually have the **MY2004 gearbox** fitted. Identify physical gearbox and TCM software rather than relying on the VIN's model year alone.

This bulletin **does not document those repairs as universal MY2005–09 solutions**, and it does **not** establish a priced or VIN-approved replacement part for a later car. No vehicle repair should proceed based on 5449780 alone.

## 3. MY2007 automatic: electrical DTC, fluid access and internal wear are distinct

Saab provides two factory MY2007 9-5 ATF level procedures: [one with dipstick](https://saabwisonline.com/9-5-9600/2007/4-transmission/automatic-transmission/adjustment-replacement/automatic-transmission-fluid-level) and [one with sealed access and gauge DT-47653](https://saabwisonline.com/9-5-9600/2007/4-transmission/automatic-transmission/adjustment-replacement/automatic-transmission-transmission-fluid-level-without-dipstick). Both specify engine **idling**, TCM readout at **80°C**, and **0.5 L** between MIN/MAX. We do **not** know which hardware corresponds to an actual VIN: that remains a gap.

[MY2005 automatic full fluid capacity](https://saabwisonline.com/9-5-9600/2005/4-transmission/automatic-transmission/technical-data/weight-fluid-capacity-and-grade-of-fluid) is **7.0 L including torque converter and cooler**, historical **Saab 3309** fluid (87 92 731). That is **not** the amount drained in a simple service. The [2005 factory change procedure](https://saabwisonline.com/9-5-9600/2005/4-transmission/automatic-transmission/adjustment-replacement/changing-the-automatic-transmission-fluid) uses specialized line-exchange equipment and follows with TCM-temperature level checking; it should not be reinterpreted as an improvised unrestricted DIY flush. Do not confuse this OG9-5 7.0 L number with early NG9-3 FA57 **7.2 L**.

[MY2007 P0748](https://saabwisonline.com/9-5-9600/2007/4-transmission/automatic-transmission/fault-diagnosis-diagnostic-trouble-codes/p0748) indicates pressure solenoid current outside electrical limits, and [MY2007 P0722](https://saabwisonline.com/9-5-9600/2007/4-transmission/automatic-transmission/fault-diagnosis-diagnostic-trouble-codes/p0722) records a missing output-speed sensor signal. Both may cause limp-home and warrant sensor/connector/TCM live-value testing rather than an immediate transmission rebuild. The separate [MY2006 P0730 description](https://saabwisonline.com/9-5-9600/2006/4-transmission/automatic-transmission/fault-diagnosis-diagnostic-trouble-codes/p0730) names a faulty ratio resembling third gear even when fourth/fifth expected, and mentions S3 solenoid diagnostic help. It is **not proof of harmless electrical failure**: ratio errors can accompany real hydraulic/mechanical damage.

Saab [2007 gearbox replacement WIS](https://saabwisonline.com/9-5-9600/2007/4-transmission/automatic-transmission/adjustment-replacement/complete-automatic-transmission) requires contaminated-circuit flushing before starting a newly installed transmission. Fluid contamination can transfer damage to a replacement. This is a **replacement prerequisite**, not a reason to buy a replacement before diagnosing the existing one.

## 4. Cooling: do not confuse external and internal damage

Saab's [MY2008 petrol temperature/pressure data](https://saabwisonline.com/9-5-9600/2008/2-engine/cooling-system/technical-data/temperature-pressure-limits) distinguishes nominal thermostat opening **89°C**, expansion tank relief valve **140–150 kPa**, and gauge red-zone **129°C**. None by itself proves a warped cylinder head or confirms the engine is healthy. The [MY2007 thermostat procedure](https://saabwisonline.com/9-5-9600/2007/2-engine/cooling-system/adjustment-replacement/thermostat-4-cyl) describes top vent orientation, sealing surface and adjacent ground cable plus 22 Nm housing joint torque. Actual severe overheating needs stopping the engine, cold-safe leak/pressure testing, and possibly professional combustion-gas/compression or leak-down testing.

**Non-running purchase limitation:** Without documented history, physical corrosion inspection, a running test and relevant mechanical/electrical data, the database cannot declare a $1,200 Saab an inexpensive repair, nor verify turbo, automatic or head-gasket condition. It also cannot infer that a clogged catalytic converter is isolated from exhaust or engine faults.

## Open research gates

Full-text recovery of the turbo-clip symptom/ECU checklist; turbo shaft/shaft-oil limits; later-year FA57 TSB coverage and module fitment; dipstick hardware VIN boundary; presently approved Saab 3309 substitutes; actual overheating damage examination; and controlled failure rates or cost estimates. These remain explicit gaps. The next priority is assessing the **actual** candidates with these diagnostic criteria, not building a simulation algorithm.
