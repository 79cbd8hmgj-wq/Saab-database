# Original 9-5 turbo oil lines, FA57 solenoid diagnosis and misfiled bulletin safety

**Research date: 2026-10-12.** Phase 0 research-only: original factory-source documentation, **not** a simulator, repair instructions for unqualified users, a substitute turbo acceptance test, 2026 parts approval, or a determination that a particular non-running car is sound.

## Turbocharger: oil-feed and bearing priming are hard manufacturer prerequisites

Separately retrieved Saab WIS turbocharger removal/refit procedures for [MY2005](https://saabwisonline.com/9-5-9600/2005/2-engine/turbocharger-system/adjustment-replacement/turbo-4-cyl) and [MY2006](https://saabwisonline.com/9-5-9600/2006/2-engine/turbocharger-system/adjustment-replacement/turbo-4-cyl) independently state that the **turbo bearing housing must contain oil before the engine is first started**. The original service procedure fills the turbo oil inlet with engine oil and rotates the compressor wheel by hand repeatedly before installation. Turbo feed is through the engine's oil-filter adapter; oil drains by the turbo return pipe to the cylinder block. A replacement turbo without lubrication is at risk of new bearing damage even when its hardware is otherwise serviceable.

MY2006 [factory turbocharger tightening-torque table](https://saabwisonline.com/9-5-9600/2006/2-engine/turbocharger-system/technical-data/tightening-torques) (only use when the actual vehicle year, engine and joint match):

| Joint in original MY2006 four-cylinder WIS | Torque | Critical distinction |
| --- | ---: | --- |
| Turbo **oil feed at turbo** banjo | 20 Nm | New copper washers |
| Turbo **oil feed at filter adapter** banjo | 25 Nm | Different end of same pipe |
| Turbo **oil return** two M6 bolts | 14 Nm | Return flow path, not automatic transmission pipe |
| Turbo **coolant pipe** banjo at turbo | 25 Nm | Coolant circuit, not engine oil |
| Turbo/intake-pipe V-band clamp | 3 Nm | Different from outlet hose clamp |
| Charge-air hose clip | 8 Nm | Clean hose interior and coupling surfaces before reinstalling |

The factory procedure emphasizes new copper sealing washers at oil/coolant unions and clean pressurized charge-air hose connections; an aftermarket parts bundle does not prove correct joint geometry. The independently retrieved [MY2009 oil-filter adapter housing procedure](https://saabwisonline.com/9-5-9600/2009/2-engine/basic-engine-4-cylinder-petrol/adjustment-replacement/oil-filter-adapter-housing) requires a new *adapter O-ring* and Loctite 518 at that housing. **The adapter housing O-ring is not the turbo banjo's copper washer**, and its application must remain MY2009-scoped.

**Remaining mechanical barrier:** The [MY2006](https://saabwisonline.com/9-5-9600/2006/2-engine/turbocharger-system/technical-data/) and [MY2008](https://saabwisonline.com/9-5-9600/2008/2-engine/turbocharger-system/technical-data/) turbo technical-data directories both list a page called *Turbo shaft play*. However the numerical factory pages could not be retrieved. **No axial/radial tolerance is stated or approved**; do not take shaft-play figures from a 9-3 B207, diesel turbo, another compressor family or unverified community discussion and assume they apply to a B235R TD04/GT17.

The [MY2009 bypass-valve diaphragm test](https://saabwisonline.com/9-5-9600/2009/2-engine/turbocharger-system/adjustment-replacement/checking-the-charge-air-bypass-valve-4-cyl) is a separately independently sourced check: use factory vacuum/pressure pump 30 14 883, verify the diaphragm holds vacuum, then pressure. It can help isolate a manageable bypass-valve fault *before* condemning the turbo's bearings, but a successful result does not confirm the bearings, lubrication or exhaust.

## The FA57 automatic's solenoid families are electrically different

[MY2008 WIS S1–S5 technical data](https://saabwisonline.com/9-5-9600/2008/4-transmission/automatic-transmission/technical-data/gearshift-solenoid-valve-s1-s2-s3-s4-and-s5) lists **each of S1, S2, S3, S4, S5 = 11–16 Ω at 20°C**. Factory default when unenergized: **S1/S2/S4 open**; **S3/S5 closed**.

Separate pressure-regulating valves **SLT** (line pressure) and **SLS** (clutch pressure) are controlled at **300 Hz**, with very different coil readings:
- [MY2007 WIS technical data](https://saabwisonline.com/9-5-9600/2007/4-transmission/automatic-transmission/technical-data/solenoid-valves-pressure-regulation-slt-and-sls): **5.0–5.6 Ω at 20°C**.
- [MY2008 WIS technical description](https://saabwisonline.com/9-5-9600/2008/4-transmission/automatic-transmission/technical-description/solenoid-valves-sls-and-slt-for-system-pressure): nominal **5.1–5.5 Ω at 20°C**.
- **These two independently sourced limits are preserved separately**. The technical-description number and technical-data table can differ; we must not silently select one threshold as valid for every year or invent a revision date.
- MY2008 TCM connector B: SLS output **26B / ground 36B**; SLT **35B / ground 15B**. Factory documentation notes that higher solenoid current (~1A) produces **lower line pressure**, while an open circuit yields **maximum system pressure** and may cause harsh shifts.
- [MY2008 P0785](https://saabwisonline.com/9-5-9600/2008/4-transmission/automatic-transmission/fault-diagnosis-diagnostic-trouble-codes/p0785) identifies **SLS** abnormal current, fluid above 20°C and battery voltage 11–16V, triggering CHECK GEARBOX/limp home; MY2008 functional description independently associates **P0748 with SLT**.

Therefore a **harsh shift may be related to hydraulic pressure-command loss without establishing clutch wear**. Conversely, electrically acceptable solenoid resistance doesn't prove hydraulic pressure, valve operation or good clutch packs. Resistances require powered-down circuitry, correct connector/year, and suitably qualified diagnosis.

## Control modules: engine coding and programming are not optional

[Saab MY2007 TCM description](https://saabwisonline.com/9-5-9600/2007/4-transmission/automatic-transmission/technical-description/control-module) expressly says the module is **programmed for the engine type** (B205E, B235E/R, D223L or B308E) and an unprogrammed factory replacement requires **Tech2/SPS** plus resetting adaptation where specified. Do not swap an unrelated used TCM simply because its connectors fit. Learned shift adaptation and DTCs are stored independently of battery removal.

The independent [MY2007 before-changing-a-module checklist](https://saabwisonline.com/9-5-9600/2007/4-transmission/automatic-transmission/fault-diagnosis-general/before-changing-a-control-module) begins with power, grounds and sensor/plausibility testing; it warns about unnecessary SPS flashing and electrostatic damage. No evidence is presented here that a present-day SPS subscription/programming key will work on a particular car. The [electrical-test page](https://saabwisonline.com/9-5-9600/2007/4-transmission/automatic-transmission/fault-diagnosis-general/testing-for-open-short-circuits) prohibits using resistance mode on semiconductors such as the TCM and requires disconnecting supply when measuring passive resistance.

## Critical misfiled service bulletin: **not** a 9-5 FA57 ATF approval

Original Saab [bulletin 100-2512 edition 3](https://saabwisonline.com/9-5-9600/2007/1-service/saab-service-eu/bulletins-si-mi/100-2512-utg-3-common-faults-on-automatic-transmissions) is stored in a **2007 Saab 9-5** service directory, but its internal **Cars affected** line says **Saab 9-3 M98–99 with automatic transmission**, market **SE/NO**, date May 2006. It includes **Dexron III** in its parts section for *that car*. **Do not use this bulletin as evidence that MY2005–09 9-5 FA57s accept Dexron III.** The prior dataset's historic 9-5 FA57 Saab 3309 fluid evidence remains separately year-scoped.

This is another example where a WIS directory path is not sufficient to prove an original bulletin's model-year, car or market applicability.

## What remains unresolved

1. Original factory numbers and measuring procedure for **turbo shaft axial/radial free play**, separately for GT17/B235E and Mitsubishi TD04/B235R, especially 2005–09.
2. VIN-specific turbo oil-feed/return parts and genuine seals; independently verify installed engine/charger, oil pressure and oil-cooling condition.
3. MY2008 original *technical-data* SLS/SLT table (separate source from MY2008 descriptive document), and year-specific 2005/06/09 solenoid specifications.
4. Actual TCM and gearbox hardware, wiring and supported legitimate SPS option before ordering components.
5. Individual vehicle noise, fluid contamination, gearbox speed/slip measurements and repair cost: there is no sourced 2026 cost benchmark or statistical reliability/repair probability.

The emphasis remains **prevent irreversible damage from wrong part/fluid/repair assumptions** while gaining enough original evidence to choose Saabs that do not require engine or transmission rebuilds.
