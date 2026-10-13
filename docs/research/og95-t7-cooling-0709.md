# MY2007–2009 original Saab 9-5: Trionic T7 and petrol cooling systems

Research date: 2026-10-12. Structured evidence: [`og95-t7-cooling-0709.json`](../../data/datasets/og95-t7-cooling-0709.json). This source-scoped expansion has **28 factory-authored service references, 72 facts, 3 diagnostic issue records, and 7 unresolved gaps**. The goal is accurate knowledge for eventual reliable-car screening, **not** changing Saab's thermal calibration or treating all models as identical.

## Trionic T7 MY2007–09: independently corroborated year readings

For each of [MY2007](https://saabwisonline.com/9-5-9600/2007/2-engine/trionic-t7-4-cyl/technical-description/control-module-power-supply), [MY2008](https://saabwisonline.com/9-5-9600/2008/2-engine/trionic-t7-4-cyl/technical-description/control-module-power-supply), and [MY2009](https://saabwisonline.com/9-5-9600/2009/2-engine/trionic-t7-4-cyl/technical-description/control-module-power-supply), the four-cylinder Trionic T7 WIS pages identify three distinct ECU power arrangements:

| Named factory function | Feed / fuse / pin |
| --- | --- |
| Retained +30 (ECU memory) | Maxifuse 2 → fuse 17 → ECU pin 23 |
| Switched +15 | Fuse 27 → ECU pin 43 |
| Main relay supplies throttle motor | Relay contact 87 → fuse 14 → ECU pin 1 |

Loss of +30 or +15 can cause no start and no ECU communication; absence of main-relay feed can provoke P1640. These are **MY directory evidence records**, not proof an individual harness or fuse box remains unaltered. The [5V supply pages for MY2007](https://saabwisonline.com/9-5-9600/2007/2-engine/trionic-t7-4-cyl/technical-description/5v-supply), [MY2008](https://saabwisonline.com/9-5-9600/2008/2-engine/trionic-t7-4-cyl/technical-description/5v-supply), and [MY2009](https://saabwisonline.com/9-5-9600/2009/2-engine/trionic-t7-4-cyl/technical-description/5v-supply) independently identify ECU pins 69/46, an internally coupled supply in the throttle body, and limp-home if this bus is shorted by sensor or wiring trouble.

Separate factory [crankshaft sensor 2007](https://saabwisonline.com/9-5-9600/2007/2-engine/trionic-t7-4-cyl/technical-data/crankshaft-position-sensor-345), [2008](https://saabwisonline.com/9-5-9600/2008/2-engine/trionic-t7-4-cyl/technical-data/crankshaft-position-sensor-345), and [2009](https://saabwisonline.com/9-5-9600/2009/2-engine/trionic-t7-4-cyl/technical-data/crankshaft-position-sensor-345) data repeat the **860±90 Ω at 20°C** and 0.4–1.3 mm non-adjustable gap. The reading does *not* establish a failed crank sensor on a specific nonrunning car or rule out intermittent hot faults.

For each of 2007/08/09, the [coolant temperature sensor description, MY2008](https://saabwisonline.com/9-5-9600/2008/2-engine/trionic-t7-4-cyl/technical-description/coolant-temperature-sensor) explicitly establishes NTC sensor 202 at the left-hand cylinder head, ECU pins 39 (5V through internal 1kΩ resistor) and 22 (return), DTCs P0116/P0117/P0118/P0119 and **substitute-temperature behavior up to 90°C** if its signal fails. The [MY2007](https://saabwisonline.com/9-5-9600/2007/2-engine/trionic-t7-4-cyl/technical-data/coolant-temperature-sensor-202) and [MY2009](https://saabwisonline.com/9-5-9600/2009/2-engine/trionic-t7-4-cyl/technical-data/coolant-temperature-sensor-202) resistance tables independently state **2.1–2.9 kΩ at 20°C**. A substitute ECU coolant value is **not a measured physical temperature**.

## Cooling circuit and component conditions

MY2008 factory [cooling-circuit flow description](https://saabwisonline.com/9-5-9600/2008/2-engine/cooling-system/technical-description/coolant-4-cyl) explains that the closed thermostat allows a block/head/heater bypass path. As it opens, radiator flow develops; when fully open, it closes the lower bypass passage to direct flow through the radiator. **Do not infer full opening occurs at the initial thermostat opening temperature.**

MY2008 [technical limits](https://saabwisonline.com/9-5-9600/2008/2-engine/cooling-system/technical-data/temperature-pressure-limits) include:

| Parameter | Factory WIS value | Context |
| --- | --- | --- |
| Thermostat begins opening | **89 ± 2°C** | Initial opening, not full-stroke |
| Expansion-tank cap relief valve | **140–150 kPa** | Cap opening, **not** a 1-bar test pressure |
| Petrol fan low on/high on, technical data | **100±2°C / 113±2°C** | Summary rounded/toleranced |
| Petrol fan low off/high off | **96±1°C / 109±1°C** | Cooling hysteresis |
| Coolant boiling point | **131°C at stated 1.4 bar** | Factory table; mixture, pressure reference and operating environment require care |

The **detailed fan page instead says 99°C low-on**, and its introduction says 100°C. All values are retained with source locator and an explicit discrepancy gap. This is not a recommendation to reprogram any fan. For real diagnosis, observe *rising/falling* temperature, A/C state and actual coolant sensor validity.

The [thermostat service guide](https://saabwisonline.com/9-5-9600/2008/2-engine/cooling-system/adjustment-replacement/thermostat-4-cyl) requires the **TOP** vent marking upward and gives **22 Nm** for the housing; it also instructs reinstalling/protecting a ground connection nearby. The [coolant-pump service guide](https://saabwisonline.com/9-5-9600/2008/2-engine/cooling-system/adjustment-replacement/coolant-pump-4-cyl) is a more substantial procedure involving belt, turbo inlet, power steering pump and coolant pipes. It notes that *very slight* shaft-seal seep lubricates the pump, which is not authority to ignore sustained coolant loss.

MY2007 and MY2008 separate WIS [coolant change](https://saabwisonline.com/9-5-9600/2008/2-engine/cooling-system/adjustment-replacement/coolant-changing) pages specify a **maximum three-year interval** and nominal **7.4 L system volume** for four-cylinder petrol, distinct from volume of every individual service refill. Filling/bleeding is done cold, with the cap tightly secured; venting and confirmation follow the factory procedure. A [MY2008 pressure test](https://saabwisonline.com/9-5-9600/2008/2-engine/cooling-system/adjustment-replacement/cooling-system-pressure-testing) calls for original Saab tester 30 05 477 and adapter 30 05 451, pressurization **above 1 bar**, and inspection for a pressure drop and leaks. **Neither a leak test nor the relief-valve rating should be treated as an arbitrary safe overpressure instruction.**

## Petrol radiator fans are controlled by DICE, not diesel ECM/UEC

The [MY2007](https://saabwisonline.com/9-5-9600/2007/2-engine/cooling-system/technical-description/radiator-fans-4-cyl), [MY2008](https://saabwisonline.com/9-5-9600/2008/2-engine/cooling-system/technical-description/radiator-fans-4-cyl) and [MY2009](https://saabwisonline.com/9-5-9600/2009/2-engine/cooling-system/technical-description/radiator-fans-4-cyl) **petrol** descriptions state:

- A non-A/C car uses one fan with low/high-speed relay/resistor control; an A/C-equipped car uses **two fans**, with three relays **155, 81, 396**, switched between series (low) and parallel (high) operation.
- DICE receives coolant temperature from **Trionic**; for A/C-equipped cars it also uses A/C pressure, speed (MIU), ambient temperature (SID) and compressor status.
- The detailed hysteresis is low **99°C on / 96°C off**, high **113°C on / 109°C off**. The same page's overview calls low-on 100°C. The MY2008 technical-data table lists 100±2°C.
- If coolant temperature is absent/out of range, DICE can start low fan operation after **five seconds** as a protective measure. This may be a sensor, harness, Trionic or bus issue, **not necessarily a bad fan**.
- Hot ignition-off operation is possible: the source discusses thresholds around **103°C and 107°C**, states only low speed is enabled with key off, and gives a maximum of about **3.5 minutes** depending on recent state. A running fan after switch-off is therefore not automatically a failure.
- High fan speed can be delayed after key-on; the document also imposes conditions for fan speed transitions and A/C pressures.

This is **not** the four-speed dual-fan ECU/UEC arrangement described under the separate [diesel cooling system](https://saabwisonline.com/9-5-9600/2008/2-engine/cooling-system-diesel/technical-description/detailed-description-radiator-fans). No diesel control data has been imported into the petrol dataset.

## DIY maintenance-screening significance, without unsupported conclusions

Factory descriptions identify distinct testable systems: coolant retention, cap pressure, pump circulation, thermostat behavior, sensor validity, DICE-to-relay output and fan motor paths. These are suitable for a **screening evidence checklist** on a mechanically neglected example, but no service bulletin or fleet denominator here establishes a common defect ranking. Rust at radiator support/wiring and physical part identity need actual inspections; a repair procedure alone cannot establish costs or economic salvageability.

## Remaining research limits

Seven dataset gaps cover exact year/option wiring and ground diagrams, 99-versus-100°C source discrepancy, actual thermal measurements and pressure testing, independently checked 2007/09 cooling tables, detailed DTC/fan diagnostic trees, petrol-versus-diesel system boundaries, and historical failure/replacement evidence. No replacement-part ordering, coolant thermodynamic simulation or fan reprogramming work is included.
