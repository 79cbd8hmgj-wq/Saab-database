# 9-5 petrol cooling service and oil-cooler VIN boundaries, MY2006–09

**Research date:** October 12, 2026. Source-backed database expansion, not a parts fitment approval or DIY procedure substitute. **Do not treat 2005/06 WIS mirrored later VIN cutovers as proof of hardware changing in that model year.**

## Factory-supported coolant service

The separately retrieved [MY2007](https://saabwisonline.com/9-5-9600/2007/2-engine/cooling-system/adjustment-replacement/coolant-changing) and [MY2008](https://saabwisonline.com/9-5-9600/2008/2-engine/cooling-system/adjustment-replacement/coolant-changing) 4-cylinder petrol WIS coolant change pages both state a maximum **three-year** change interval and **7.4 L** full cooling system volume. The corresponding diesel capacity is **7.5 L** and is **not** entered as petrol. 7.4 L is not necessarily the amount exiting the radiator during a partial drain. Coolant fills must begin with the engine cold; fill to MAX, not above. The original procedure bleeds with A/C or ACC switched off, runs to the fan cycle, then rechecks coolant level and hose condition. Do not run a non-running/overheating vehicle to satisfy a checklist.

The [MY2007 factory fill/bleed procedure](https://saabwisonline.com/9-5-9600/2007/2-engine/cooling-system/adjustment-replacement/filling-and-bleeding-the-cooling-system) names **400 131 389** (1 L) and **400 131 397** (4 L) as historical Saab genuine coolant supply numbers and specifies equal coolant/water portions. [MY2009 coolant mixture service](https://saabwisonline.com/9-5-9600/2009/2-engine/cooling-system/service/coolant-mixture-and-freezing-point) gives ethylene-glycol based 50/50 Saab Original coolant with water, says protection must withstand at least **−30°C**, notes local weather can demand lower freeze protection, and warns against mixing different types. No currently sold coolant or modern replacement is approved based solely on these old numbers.

[MY2008 technical pressure/temperature limits](https://saabwisonline.com/9-5-9600/2008/2-engine/cooling-system/technical-data/temperature-pressure-limits) gives petrol thermostat opening **89 ± 2°C**, expansion-tank pressure-valve opening **140–150 kPa**, nominal system boiling temp **131°C at 1.4 bar** and a gauge red-zone temperature of **129 ± 2.5°C**. These are four separate functional quantities and must not be confused with fan-switch or oil-cooler thermostat control. The existing database preserves the documented disagreement between fan activation numbers on different pages rather than using this source to choose one as the 'real' temperature.

[MY2006 cooling-system overview](https://saabwisonline.com/9-5-9600/2006/2-engine/cooling-system/technical-description/system-overview-4-cyl) describes an accessory-belt-driven water pump on the engine's right side, thermostat left, pressurized cross-flow radiator and **one radiator fan motor without A/C; two with A/C**. Petrol only: don't import 2008 diesel cooling system specifics.

## Distinguish the TWO types of oil cooler

The [MY2008 4-cylinder petrol coolant-system diagram](https://saabwisonline.com/9-5-9600/2008/2-engine/cooling-system/technical-description/cooling-system-diagram-4-cyl) explicitly labels **oil cooler (automatic only), item 9**: that is the **automatic transmission fluid** cooling circuit. Meanwhile [MY2006](https://saabwisonline.com/9-5-9600/2006/2-engine/cooling-system/adjustment-replacement/engine-oil-cooler-4-cyl) and [MY2007](https://saabwisonline.com/9-5-9600/2007/2-engine/cooling-system/adjustment-replacement/engine-oil-cooler-4-cyl) have a separate **engine-oil cooler** service procedure attached to the charge-air cooler. These are not interchangeable components or fluid paths.

The engine oil-cooler WIS describes **O-rings at the pipe junctions**; check each for shape/damage and replace if necessary; the original factory procedure uses **Gleitmo 805**, historical product reference **30 06 442**, and pre-fills the engine oil cooler with the recommended engine oil. Service notes caution against damaging the sealing seat. It specifies:

| Joint | WIS years independently read | Factory torque |
|---|---|---|
| Engine-oil cooler oil-pipe nut **up to VIN suffix 73514907** | MY2006 and MY2007 | **10 Nm** |
| Same nut **from VIN suffix 73514908** | MY2006 and MY2007 | **8 Nm** |
| Charge-air cooler to engine-oil cooler bracket | MY2006 and MY2007 | **8 Nm** |

**Critical source-quality warning:** The MY2006 page already includes a VIN cutover with a 7-prefix. This does not indicate that a 2006 car definitely contains later hardware, and it is **not** evidence that different hose part numbers superseded one another at model-year introduction. Confirm the exact complete VIN, installed cooler hardware and genuine Saab EPC before service. The earlier [MY2008 engine-mount and torque-arm audit](og95-pcv-radiator-mount-provenance.md) records a *different* VIN breakpoint at **73514478/73514479**, which is a different joint. Do not combine them.

Likewise the factory [MY2005 left-mount](https://saabwisonline.com/9-5-9600/2005/2-engine/basic-engine-4-cylinder-petrol/adjustment-replacement/engine-mounting-left) and [MY2007 left-mount](https://saabwisonline.com/9-5-9600/2007/2-engine/basic-engine-4-cylinder-petrol/adjustment-replacement/engine-mounting-left) pages both include that future VIN boundary, with **84 Nm** through 73514478 and **74 Nm** from 73514479. This cross-directory repetition argues for keeping **year of the webpage separate from applicability of the particular cutover**, until an original PI/TSB or EPC build history resolves it.

## Service procedures that matter for reliability and DIY safety

- [MY2007 4-cyl thermostat](https://saabwisonline.com/9-5-9600/2007/2-engine/cooling-system/adjustment-replacement/thermostat-4-cyl): upper vent hole/`TOP` orientation and **22 Nm** thermostat housing fastening. Maintain/clean the ground connection at the coolant pipe bracket. This is a local housing torque, not the engine oil-cooler nut.
- [MY2006 radiator](https://saabwisonline.com/9-5-9600/2006/2-engine/cooling-system/adjustment-replacement/radiator-4-cyl): additional **automatic transmission oil cooler** line disconnection/refit and fluid-level check. Transmission fluid lines demand attention but the existence of this line is not proof of any NG 9-3 FA57 contamination defect.
- [MY2009 coolant drain/refill](https://saabwisonline.com/9-5-9600/2009/2-engine/cooling-system/adjustment-replacement/coolant-4-cyl) confirms radiator drain cock, AC/ACC off, and run-until-fan cycle for a serviceable motor.
- [MY2006 leak-pressure procedure](https://saabwisonline.com/9-5-9600/2006/2-engine/cooling-system/adjustment-replacement/cooling-system-pressure-testing) instructs pressure **over 1 bar** with Saab adapter **30 05 451** and tester **30 05 477**, looking for pressure decay. Never open or pressurize a hot cooling circuit: burns/steam are dangerous. Pressure loss is not by itself a definitive diagnosis of which component has failed.

## Unresolved validation gates

1. Official manufacturer VIN-filtered OE parts and supersession data for radiator variants, engine-oil cooler sealing O-rings and pipe fittings, expansion cap, thermostat and mounts are still missing.
2. Specific MY2007–09 factory petrol radiator removal links were not independently readable in this retrieval session. They remain explicit gaps; only the verified 2006 source is used for the gearbox-fluid cooler line procedure.
3. The source-date and production-version relationships behind both 73514478/73514479 mount and 73514907/73514908 engine oil-cooler cutovers are unknown.
4. The 2007–08 coolant service pages do not establish a three-year interval for every other model year, market or engine.
5. No lifetime statistics, quantified failure risk or tested improvement from changing hoses, coolant, radiator or mounts are asserted.

The objective remains to make a defensible purchase/maintenance specification for one actual Saab, **before** building a simulator or approving modernization changes.
