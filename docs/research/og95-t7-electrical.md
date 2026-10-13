# Original Saab 9-5 Trionic 7: electrical supply, engine sensors and no-start diagnostics

Research date: 2026-10-12. New structured source data in [`og95-t7-electrical.json`](../../data/datasets/og95-t7-electrical.json) comprises **22 factory WIS source records, 43 facts, four symptom-oriented issue records, and seven research gaps**. This pass concentrates on the original-generation 9-5 **Trionic T7 four-cylinder** system, especially the model-year 2006 workshop documentation, with separately reviewed MY2007, MY2008 and MY2009 electrical pages. It does **not** cover V6, diesel, NG9-5 or NG9-3, and it is not a measured failure-rate study.

## Engine ECU, relay supplies and grounds

[MY2006 T7 control module](https://saabwisonline.com/9-5-9600/2006/2-engine/trionic-t7-4-cyl/technical-description/control-module) identifies a **70-pin ECU** and nominal powered operating range **8–16 V**. Its stored adaptations and trouble codes depend on the retained +30 feed; unnecessary disconnection can erase useful evidence. The source explicitly states that this ECU substitutes for various failed sensor readings **except crankshaft position**.

The [MY2006 ECU supply page](https://saabwisonline.com/9-5-9600/2006/2-engine/trionic-t7-4-cyl/technical-description/control-module-power-supply) documents distinct feeds:

| Circuit | MY2006 factory source path | Consequence named by WIS |
| --- | --- | --- |
| Retained battery +30 / memory | Maxifuse 2 → fuse 17 → ECU pin 23 | Missing ECU supply can produce no-start and no diagnostic communication |
| Switched ignition +15 | Fuse 27 → ECU pin 43 | Enables the ECU; absence can prevent starting/diagnostic contact |
| Main-relay throttle supply | Relay terminal 87 → fuse 14 → ECU pin 1 | Failure can give P1640, closed throttle, engine stop |

These paths are **MY2006 4-cylinder T7** source readings, with the +30/+15/main-relay path independently located in the [MY2009 source](https://saabwisonline.com/9-5-9600/2009/2-engine/trionic-t7-4-cyl/technical-description/control-module-power-supply). A particular car still needs a wiring and physical-fuse verification.

[MY2006 grounds](https://saabwisonline.com/9-5-9600/2006/2-engine/trionic-t7-4-cyl/technical-description/ground) distinguish **power ground G7** for ECU pins **25, 47, 62**, MAF and ignition cassette; *sensor returns* on ECU pins **22 and 70**; and an oxygen-sensor reference return on **pin 58**. Loss of G7 or total sensor ground can inhibit starting; oxygen reference return loss can yield P0134. The G7/pin layout was separately retrieved from [MY2007](https://saabwisonline.com/9-5-9600/2007/2-engine/trionic-t7-4-cyl/technical-description/ground) and [MY2008](https://saabwisonline.com/9-5-9600/2008/2-engine/trionic-t7-4-cyl/technical-description/ground) WIS pages. There is **no basis** to equate a no-communication condition immediately with an internally dead ECU.

[MY2006 shared 5V supply](https://saabwisonline.com/9-5-9600/2006/2-engine/trionic-t7-4-cyl/technical-description/5v-supply) identifies ECU pins **69 and 46**, internally coupled through the throttle body and used by multiple pressure and pedal/throttle sensors. A short in a sensor or the harness can cause throttle limp-home; the throttle assembly is not automatically the failed component.

## Crankshaft signal: hard no-start dependency

The [MY2006 crankshaft sensor operation](https://saabwisonline.com/9-5-9600/2006/2-engine/trionic-t7-4-cyl/technical-description/crankshaft-position-sensor) and [technical data](https://saabwisonline.com/9-5-9600/2006/2-engine/trionic-t7-4-cyl/technical-data/crankshaft-position-sensor-345) describe an inductive sensor reading a **60-2 tooth pattern (58 present ribs)** and entering T7 at pins **17/18**. Factory test resistance is **860 ±90 Ω at 20°C**; nominal nonadjustable sensor-to-ring gap is **0.4–1.3 mm**. WIS associates P0337 with missing signal during cranking and P0336 with lost position during operation, and states that **there is no substitute crankshaft-position signal**.

These values and DTCs support specific troubleshooting, **not** the conclusion that every stalled 9-5 needs a new crank sensor. Signal waveform, sensor temperature, connector condition and harness continuity still matter; a room-temperature resistance check alone cannot exclude a hot intermittent failure.

## Ignition discharge module is not a generic four-coil bank

The [MY2006 IDM description](https://saabwisonline.com/9-5-9600/2006/2-engine/trionic-t7-4-cyl/technical-description/ignition-discharge-module) and [data page](https://saabwisonline.com/9-5-9600/2006/2-engine/trionic-t7-4-cyl/technical-data/ignition-discharge-module-346) describe **four coils**, firing order **1-3-4-2**, high-energy ignition and combustion ionization feedback. ECU pins **53 and 6** receive combustion signals used for synchronization and knock/misfire analysis. The cassette depends on G7 and main-relay power; P1310 can indicate missing supply. The factory material states **red ignition discharge modules must not be used** in this Trionic 7 four-cylinder context and references TK3.4D on T7 LEV.

Do not replace this with an ordinary four-coil arrangement simply because spark plugs can fire. Equally, misfire or synchronization codes do not prove a cassette itself is faulty. Correct black-cassette OEM identity and exact hardware/VIN fitment remain research gaps.

## Relays, air-measurement and mechanical throttle fallback

The [main relay](https://saabwisonline.com/9-5-9600/2006/2-engine/trionic-t7-4-cyl/technical-description/main-relay) is held energized for approximately **10 seconds after key-off** to allow throttle adaptation. The [fuel pump relay](https://saabwisonline.com/9-5-9600/2006/2-engine/trionic-t7-4-cyl/technical-description/fuel-pump-relay) commands approximately **one second of pump operation when the key is switched on**; that brief prime is not a pump-delivery specification.

The [MAF](https://saabwisonline.com/9-5-9600/2006/2-engine/trionic-t7-4-cyl/technical-description/mass-air-flow-sensor) outputs frequency pulses to ECU pin **65**, not a generic linear 0–5 V analog output. WIS links a low-frequency MAF code P0102 to causes including a significant air leak between MAF and throttle as well as possible sensor failure; substitute air-pressure/temperature calculations are used after certain MAF diagnoses.

The [pedal sensor](https://saabwisonline.com/9-5-9600/2006/2-engine/trionic-t7-4-cyl/technical-description/pedal-position-sensor) contains two opposing potentiometers in the throttle body, actuated by the accelerator cable. The [throttle control](https://saabwisonline.com/9-5-9600/2006/2-engine/trionic-t7-4-cyl/technical-description/throttle-control) contains a mechanical limp-home arrangement. Do **not** force the solenoid, bypass protection or undertake reset procedures without full WIS diagnostics.

Factory [coolant](https://saabwisonline.com/9-5-9600/2006/2-engine/trionic-t7-4-cyl/technical-data/coolant-temperature-sensor-202) and [intake-temperature](https://saabwisonline.com/9-5-9600/2006/2-engine/trionic-t7-4-cyl/technical-data/intake-air-temperature-sensor-407) sensor tables both report **2.1–2.9 kΩ at 20°C**, but the ECU bias resistor/nominal signal voltages differ. The **IAT page contradicts itself on physical location** (combined charge-air sensor vs intake-manifold text). That contradiction remains an explicit gap; it must not become a made-up parts-location diagram.

## TWICE, DICE, MIU, TCM and immobilizer dependencies

The [T7 bus list](https://saabwisonline.com/9-5-9600/2006/2-engine/trionic-t7-4-cyl/technical-description/bus-messages-trionic-t7) and [TWICE bus list](https://saabwisonline.com/9-5-9600/2006/3-electrical-system/bus-and-diagnostics-communication/technical-description/bus-messages-twice) document authorization and information exchanged among T7, TWICE, DICE, MIU and optional TCM/ESP; diagnostic requests travel via DICE. The [fuel shut-off description](https://saabwisonline.com/9-5-9600/2006/2-engine/trionic-t7-4-cyl/technical-description/fuel-shut-off) says **P1460** may be generated when TWICE authorization is missing or codes were not programmed after a control-module replacement. The separately checked [MY2005 T7 replacement procedure](https://saabwisonline.com/9-5-9600/2005/2-engine/trionic-t7-4-cyl/adjustment-replacement/control-module) explicitly uses Tech 2/TWICE for immobilizer reprogramming, but its steps must not be assumed unchanged for every later hardware/software revision.

**Conclusion for candidate nonrunning cars:** An authorized diagnostic sequence should establish ECU communication, power/grounds, crank synchronization, main relay/fuel-pump control, IDM power and correct immobilizer authorization *before* deciding an engine, ECU or cassette must be replaced. This is an evidence-based inspection prioritization, not an official full repair flowchart and not a claim any failure mode is statistically common.

## Open work

Seven dataset gaps remain: complete factory electrical diagrams and G7 physical location; independent MY2007–09 sensor/relay document coverage; IDM part/VIN restrictions; year-specific immobilizer/ECU replacement procedures; the inconsistent IAT location; full P0336/P0337/P1310/P1460 DTC enable/diagnostic trees; and fleet evidence of actual electrical failure frequency and cost. No simulation, failure-rate model, flash programming or unauthorized security bypass was introduced.
