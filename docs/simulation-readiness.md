# From documents to a replacement simulator

The repository currently supports source lookup, configuration boundaries,
replacement candidate screening and a missing-input inventory. It has not run a
Saab performance, thermal or fatigue model. Structural validation of the database
does not validate a numerical vehicle model.

## Questions and required evidence

| Question | Available starting evidence | Still required for a defensible answer |
| --- | --- | --- |
| Does a part belong to the documented application? | Factory/catalogue IDs, scoped supersessions, VIN/serial restrictions | Actual vehicle and installed-part identity, exact current application and interfaces; software/security requirements for modules |
| Is an alternative hose or bracket suitable? | Illustrative supplier material/pressure/temperature envelopes | Exact SKU compound/alloy, dimensions, fluid/vacuum/pressure under heat, routing, clamp/fastener loads, aging and vibration evidence |
| What RPM corresponds to a given speed? | Scoped overall gearbox ratios and factory wheel/tire options | Installed gearbox, measured loaded rolling radius and slip; independent RPM/speed validation |
| How does a powertrain change affect acceleration? | Peak factory output, scoped weight ranges, ECU signal semantics | Measured torque-speed-load map, actual test mass, inertia, losses, road load, traction, shifts and converter behavior |
| Will an ECU location run cooler? | Factory wiring dependencies and seller mounting/temperature claims | Thermal geometry and material properties, case/junction temperatures, airflow, heat soak, harness/ground characteristics, water exposure and measured before/after traces |
| Will a component last longer? | Selected documented failure mechanisms and corrections | Representative load/thermal spectra, material/process/aging distributions, failure-mode tests and appropriate durability/fleet evidence |

Wheelbase, track and body dimensions are useful context. They do not substitute for
suspension hard points, spring/damper rates, compliance, tire coefficients, test
mass or measured center of gravity. A catalogue turbo number does not supply a
compressor map. Diagnostic torque calculated from air mass is not an independent
dynamometer measurement.

## Smallest useful model sequence

1. **Identify and screen:** join source-scoped specifications, correction history
   and component identities for a real vehicle. Leave unresolved mappings open.
2. **Validate simple calculations:** start with gearing and steady-state electrical
   or flow checks when sufficient inputs exist. Keep original units and conditions.
3. **Calibrate one subsystem:** obtain a suitable thermal, road-load or component
   dataset and parameterize only the subsystem being evaluated.
4. **Compare alternatives:** use the same boundary conditions and record uncertainty,
   residuals and the operating range in which the comparison was tested.
5. **Investigate durability:** add failure-mode-specific aging/load evidence. Do not
   extrapolate a temperature change directly into years of life without a supported
   physical model and validation.

This sequence is a planning recommendation. The repository's query tool searches
records; it does not implement these engineering models.

## Replacement record needed for each candidate

| Field group | Required content |
| --- | --- |
| Identity/application | Manufacturer, exact part/SKU/revision, vehicle/engine/gearbox/VIN conditions, source and retrieval date |
| Physical interfaces | Drawings or measured dimensions, connectors, mounting, clearances, hose/fitting ends and tolerance stack |
| Functional envelope | Material/chemical compatibility, pressure/vacuum/temperature/load limits, electrical and protocol requirements |
| Dependencies | Accompanying parts, calibration or pairing requirements, ground paths, cooling/airflow and related sensors/actuators |
| Evidence | Manufacturer specification versus supplier claim versus measured result, test conditions and uncertainties |
| Model/validation | Versioned equations/software and parameter set, declared assumptions, validation data, residuals and tested range |
| Decision | Supported application, unresolved questions, required changes and the evidence needed to accept the substitute |

Use [the vehicle template](../templates/vehicle-instance.json) when vehicle data
becomes available. Future measurements should retain timestamp, instrument,
calibration, unit, uncertainty, operating conditions and raw-data provenance. A
factory nominal value remains a specification rather than a measurement of that
vehicle. Keep vehicle data, supplier envelopes and model parameters distinct.

## Resources and gaps

The [simulation resource report](research/simulation.md) identifies diagnostic
semantics, read-only acquisition leads and modeling references. The corresponding
[JSON](../data/datasets/simulation.json) contains the missing inputs. Software
license terms are recorded individually: public source availability alone is not
permission to reuse every project or bundled asset.

The [replacement report](research/replacements.md) documents the currently located
turbo/pipe and ECU-mounting candidates. Their findings are candidate evidence, not
proof of cross-year fitment or Toyota-equivalent dependability.
