# Saab numerical simulation and measurement resource map

Research date: 2026-10-12. Scope: read-only resources for OG 9-5 B235/Trionic 7 and NG 9-3 B207/Trionic 8. No model was run, no vehicle was connected, no software was executed, and no firmware was obtained or changed. The accompanying JSON distinguishes documented information, manufacturer claims, and engineering inferences. Hose examples describe material/application limits and do not establish Saab fitment.

## What can already be collected

Factory-derived WIS pages explain available diagnostic quantities and their meaning. The MY2000 9-5 B235E/R page separates sensor-derived airmass from calculated airmass and converts airmass into reported torque/power. It also identifies transmission and traction-control torque limits. The MY2007 9-3 Tech 2 page confirms graphical read-value display, with engine speed, airmass/combustion and coolant temperature examples. These pages provide signal semantics; they are not full engine geometry, experimental engine maps or fatigue databases. They are factory content republished by Saab WIS Online; their publication chain should be kept visible.

T7Suite and T8Suite have first-party project documentation for interfaces and real-time viewing. Trionic CAN Flasher documents ECU information retrieval. Treat ECU software identity as a separate configuration attribute: engine name and model year alone do not prove that the calibration installed in a particular vehicle is stock or matches a model. Capture software identifiers, hardware identifiers and file hashes when lawfully supplied in future read-only work. This pass does not contain ECU binaries or installation/flash instructions.

## Project availability and reuse

| Resource | Verified finding | Limit |
| --- | --- | --- |
| [TuningSuites](https://github.com/mattiasclaesson/TuningSuites) | Public; master; not archived; repository LICENSE is Apache-2.0; API pushed_at 2025-07-03 | Repo license does not automatically cover third-party dependencies, bundled firmware or factory manuals. |
| [Trionic CAN Flasher](https://github.com/mattiasclaesson/Trionic) | Public; master; not archived; API pushed_at 2025-07-03 | GitHub license metadata null; inspected root listing has no LICENSE. Reuse terms remain unresolved. |
| [txlogger](https://github.com/roffe/txlogger) | Public; master; not archived; API pushed_at 2026-10-10; README names T7 OG9-5 and T8 NG9-3 | LICENSE.md is a custom PUSU-1.0 document; GitHub reports NOASSERTION. Do not label it Apache/MIT or assume permissive reuse. |

These are observations at retrieval time, not maintenance/support guarantees or endorsements. txlogger's own documentation distinguishes binary-based output estimates from acceleration-based street-dyno results. Its cam display uses a modelled lobe shape, so the rendered curve cannot become a measured cam profile. Community software is useful for acquisition and interpretation, but an estimator is not an independently validated Saab physics model.

## Compatibility evidence available now

| Item | Evidence usable in the database | Validation still needed |
| --- | --- | --- |
| OBDLink SX | Manufacturer USB/OBD protocol and electrical envelope, plus TxSuite interface listing | Actual ECU/protocol/software pairing, attainable per-channel sample rate, missing frames, timestamps and sensor scaling |
| LAWICEL CANUSB | Manufacturer CAN interface information and throughput caveats | Driver/platform compatibility, actual request-response timing and acquisition integrity |
| Gates 24826 silicone coolant hose | SKU-specific temperature/working-pressure values and exclusion of fuel/oil service | Saab diameter, routing, bend radius, fittings, clamp suitability, coolant chemistry and hot pressure derating |
| Gates GB PCV/EEC hose family | Nitrile construction and service exclusions; fuel/PCV-oriented rather than coolant use | Exact SKU, pressure/vacuum under heat, oil mist/blow-by compatibility, wall thickness and retention |

High temperature rating alone cannot establish a better replacement. The whole assembly must satisfy fluid, pressure, vacuum, geometry, permeation and fastening requirements. The retrieved US PCV family page contains different service text from the GB page; use the clear GB family limits for screening and obtain an exact SKU datasheet before specifying a part. No universal silicone-for-PCV recommendation is supported.

## Data availability versus numerical model readiness

| Analysis | Obtainable baseline | Missing inputs | Required validation |
| --- | --- | --- | --- |
| RPM versus speed/gearing | Exact-model factory ratios and tire size can be sought in WIS/specification sources | Installed gearbox/final drive, measured loaded radius, clutch or converter slip | Compare steady-state logged RPM/speed for each gear; check independent speed reference |
| Acceleration/tractive effort | Factory peak output and curb mass; diagnostic traces | Measured torque-speed-load map, vehicle test mass, rotational inertias, losses, road load, tire grip and shift strategy | Instrumented acceleration/coastdown or chassis/engine dynamometer data; hold-out conditions |
| Fuel consumption/emissions | Existing diagnostic fuel/air signals | Calibrated full operating maps, nonfiring loss map, fuel properties, exhaust/emissions data | Gravimetric or traceable fuel-flow measurement and appropriate emissions measurements |
| Boost/turbo/injector change | ECU request/limit maps may be inspectable | Compressor/turbine maps, wastegate characteristics, intercooler loss/effectiveness, flow bench and injector characterization | Independent pressure/temperature/lambda/EGT and fuel-pressure measurements over transients |
| Cooling/heat soak | Factory thermostat/fan logic may be found | Coolant/oil flow, heat rejection, thermal masses, radiator UA/geometry, airflow, contact conductance | Steady and transient temperatures/flows across ambient/load conditions; sensor lag characterization |
| ECU relocation/electrical stress | Wiring diagrams, connector and adapter limits | Harness impedance, ground topology, ECU temperatures, heat paths and thermal cycling | Voltage-drop/EMC/thermal measurements and representative durability testing |
| Hose or bracket replacement | Supplier envelope and measured interfaces | Exact compound/alloy, geometry, aging, clamp loads, vibration, chemical exposure | Hot pressure/vacuum cycles, leak/retention tests, abrasion and endurance tests |
| Structural fatigue/lifetime | Repair dimensions and some material leads | Manufacturing process, residual stress, material S-N/strain-life scatter, load spectra, defects/corrosion and failure history | Coupon/component tests, mesh/convergence checks and representative fleet or endurance evidence |

MathWorks documents how calibrated engine lookup tables and radiator/tire models need application-specific measurements. Its reference engine maps originate in 1.5 L reference engines, not B235/B207. Default coefficients, example radiator dimensions and example fluids must never be stored as Saab parameters. COMSOL documents material/testing dependence and statistical scatter in fatigue inputs; a deterministic stress plot cannot establish a failure probability or remaining service life.

## Suggested next dataset structure

Keep vehicle identity, factory specifications, supplier envelopes, ECU calibration descriptions, measured traces and model inputs as separate records joined by explicit applicability. Each numerical input should carry units, source/test ID, uncertainty, temperature/fuel/ambient conditions and whether it is measured, estimated or assumed. Version the model and its parameter set; record the tested operating range and validation residuals. Before/after comparisons should use controlled conditions and independent measurements where possible, with uncertainty bands rather than a single unqualified improvement percentage.

The JSON gaps are the implementation checklist. Factory maxima and service diagnostics support initial screening. Specific performance gains, ECU durability improvements and high-fidelity reliability predictions remain unproven until the missing measurements and validation exist.
