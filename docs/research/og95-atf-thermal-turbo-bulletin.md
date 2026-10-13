# Original 9-5: ATF thermal diagnostics and wastegate-bulletin scope correction

**Research date:** 2026-10-12. Phase 0 factory evidence. This report expands original Saab 9-5 MY2005–09 automatic-transmission diagnostic provenance and corrects an earlier turbo-clip bulletin overgeneralization. It does **not** provide car-specific replacement authorization, a repair cost estimate, a reliability failure probability, or a simulator.

## Critical correction: WIS mirror directory year is NOT a bulletin effective year

Factory [bulletin 291-2317](https://saabwisonline.com/9-5-9600/2007/2-engine/turbocharger-system/bulletins-si-mi/291-2317-low-output-and-rattling-from-turbocharger), stored in the **MY2007** WIS mirror directory, was actually dated **January 2002**. It explicitly says **Market: not US/CA** and lists **9-5 B205E and B235E**, not B235R. Saab describes a disconnected wastegate actuator rod retaining clip as a possible cause of low power, little turbo gauge motion, rattle and P1105. In its narrow scope the bulletin's historical service items are:

| Factory bulletin service item | Number | Limit |
| --- | --- | --- |
| Stainless actuator retaining clip | **91 85 497** | Specific restricted bulletin; not proven universal OEM retrofit |
| Bypass pipe O-ring | **79 87 415** | Used in same bulletin procedure only |

The bulletin also prints parenthetical `CA: ...` number variants, **despite its non-US/CA market statement**; that ambiguous notation is not a basis to infer Canadian-market authorization. The original fact and issue in `repair-vs-replace-troubleshooting.json` have been narrowed to the factory engine and market scope. No car has been inspected. The symptom should still prompt diagnosis of other boost problems, but must not be presented as a US-market B235R clip fix.

## MY2008 automatic transmission: sensor faults versus real overheating

[Saab WIS MY2008 ATF temperature sensor](https://saabwisonline.com/9-5-9600/2008/4-transmission/automatic-transmission/technical-description/transmission-fluid-temperature-sensor) specifies a **5 V**, **1 kΩ** TCM bias at **TCM connector B pin 21**, with return **B pin 31**, using a negative-temperature-coefficient (NTC) sensor mounted in the valve housing. It documents approximate resistances at **20°C: 900 Ω; 40°C: 400 Ω; 80°C: 125 Ω; 100°C: 75 Ω**, with **±10%** tolerance. These are controlled sensor reference data, not proof of ATF oil level or hydraulic pressure.

The factory distinguishes electrical plausibility codes **P0711** (temperature fails to change as expected early in driving), **P0712** (short to B−) and **P0713** (short to B+ or open circuit) from a true thermal warning. The MY2008 temperature-control description sets the following *protective triggers*, **not safe operating targets**:

| TCM behaviour | Temperature |
| --- | --- |
| HOT program 1, torque-converter lock-up in 4th gear | **128°C**; disables below **120°C** |
| HOT program 2, lock-up in 3rd gear | **135°C**; disables below **130°C** |
| Engine torque reduction | **145°C**, limits engine torque to **200 Nm** |
| P0218 and SID transmission-overheating warning | **Over 155°C for more than 10 seconds** |

There is no general suggestion to intentionally heat a transmission to any of these temperatures; doing so could cause damage or loss of mobility. P0218 is a potentially severe condition needing **immediate safe assessment**. P0711/12/13 can instead indicate a temperature-signal/circuit problem. Both branches should be confirmed using live TCM data, original unit identity, level and fluid condition, and qualified diagnosis. A fault code alone never proves an automatic is either healthy or ready for replacement.

## Independently documented MY2008–09 electrical and TCM diagnostics

- [MY2008 P0705](https://saabwisonline.com/9-5-9600/2008/4-transmission/automatic-transmission/fault-diagnosis-diagnostic-trouble-codes/p0705) is an invalid combination of transmission range-selector switch contacts, potentially causing CHECK GEARBOX and limp-home. The factory calls for reading switch ON/OFF statuses; it is **not** standalone proof of internal clutch wear.
- [MY2009 P0722](https://saabwisonline.com/9-5-9600/2009/4-transmission/automatic-transmission/fault-diagnosis-diagnostic-trouble-codes/p0722) means the calculated output RPM should exceed **200 rpm** but the output sensor provides no signal. Saab says no adaptation in that fault state and describes readout/wiring tests. This is distinct from a confirmed slipping gear ratio.
- The [MY2009 automatic TCM read-values menu](https://saabwisonline.com/9-5-9600/2009/4-transmission/automatic-transmission/fault-diagnosis-general/menu-read-values) exposes **input speed, output speed, gear engaged, gearbox fluid temperature, selector position, requested and actual torque-converter clutch slip, and HOT shift programs**. Only compare actual converter slip to **requested** slip when the controller is regulating; nonzero slip in isolation is not a full diagnosis.
- The [MY2005 gearbox replacement checklist](https://saabwisonline.com/9-5-9600/2005/4-transmission/automatic-transmission/adjustment-replacement/checklist-complete-before-changing-gearbox) requires VIN, actual gearbox and TCM identification, mileage, cold/hot symptoms, gear transition, fluid history, DTC and software/adaptation details. It was a *warranty/dealer-era* checklist, **not present-day warranty eligibility**.
- The [MY2005 control-connector test document](https://saabwisonline.com/9-5-9600/2005/4-transmission/automatic-transmission/technical-data/test-readings-control-module-connections) explicitly orders **TCM supply and ground before sensors, bus input and actuator tests**. It warns that a measured input does not prove an actuator works. Its temperature sensor examples are 3.4 V at 20°C, 0.7 V at 100°C, with ±10% conditions.
- [MY2006 Tech 2 Activate menu](https://saabwisonline.com/9-5-9600/2006/4-transmission/automatic-transmission/fault-diagnosis-general/activate-menu) names S1–S5 actuation and 300 Hz PWM/current solenoids SLT/SLS/SLU. It explicitly warns that the adaptation reset is required after **gearbox/TCM/throttle housing replacement**; indiscriminately erasing adaptation can damage a transmission. These commands are for appropriately trained service staff in safeguarded conditions, not a buyer's project-car test.
- The [MY2009 gearbox torque page](https://saabwisonline.com/9-5-9600/2009/4-transmission/automatic-transmission/technical-data/tightening-torques) lists automatic oil-cooler banjo **27 Nm**, gearbox banjo **24 Nm**, transmission drain plug **40 Nm**. Distinguish every joint from the separate engine-oil-cooler union documented at 8/10 Nm in previous research.

## Turbocharger mechanical-condition acceptance remains unverified

The [MY2008 factory turbo technical-data index](https://saabwisonline.com/9-5-9600/2008/2-engine/turbocharger-system/technical-data/) **lists** a 'Turbo shaft play' page, but repeated attempts to retrieve the numeric page failed. Therefore **no radial or axial shaft-play number is entered**. Don't borrow a GT17 or B207 turbo tolerance from another engine or treat a whistle as proof of turbo failure.

[MY2008 Trionic T7 turbo control](https://saabwisonline.com/9-5-9600/2008/2-engine/trionic-t7-4-cyl/technical-description/turbo-control) shows pneumatic wastegate control by an electrical solenoid at **32 Hz PWM**, supplied by +15 and grounded by **Trionic ECU pin 13**, with control compensating for air-mass demand, ambient barometric pressure and intake temperature. **This is an ECU pin, not a TCM pin.** Underboost is not necessarily an internal turbocharger fault. Yet only tested compressor/turbine damage, correct shaft-play tolerances, oil feed/return function and documented fault conditions can justify a mechanical condition determination.

## What remains blocked

- No readable year-correct original factory axial/radial shaft-play numbers for GT17 versus B235R TD04; current index is metadata only.
- No VIN-filtered Saab WebEPC supersession for clip 9185497, O-ring 7987415 or 2005–09 speed/range/temperature sensors.
- We have MY2008 temperature protection documentation, not an independently repeated 2005–07 or MY2009 version of every threshold.
- No actual car observations, controlled ATF lab results, safe hydraulic tests or current repair labor/parts quotes.
- The [MY2005 hydraulic/stall-test settings](https://saabwisonline.com/9-5-9600/2005/4-transmission/automatic-transmission/technical-data/settings) mention a **five-second maximum** for an engine-loaded stall test. **Do not run this test on an unknown cheap/non-running Saab**; serious drivetrain stress and movement can result.

**Practical value:** The next individual used Saab can be logged against its VIN/TCM/gearbox identity, live ATF temperature and sensor codes, turbo wastegate and hose condition, and genuine mechanical evidence. This reduces unjustified major-replacement assumptions without pretending a cheap candidate is automatically repairable.
