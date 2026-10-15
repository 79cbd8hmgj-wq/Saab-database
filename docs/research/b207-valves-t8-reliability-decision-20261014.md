# B207 intake valves and Trionic 8: reliability decisions

Research continuation: 2026-10-14. Applies to 9-3 (9440) B207 FWD. Does not apply to second-generation 9-5.

## Intake valve failure

Existing repository evidence identifies cold intake-valve face erosion/cupping and loss of cold compression. A warm idle does not exclude it.

- Saab Parts advisory distinguishes 2007-08 B207R from 2009-11 update: https://saabparts.com/us/wp-content/uploads/sites/10/2023/05/Hard-Starting-Cold-With-Engine-Stall-Misfire-and-Low-Compression-Starts-and-Runs-Normally-When-Hot-07-11-9-3-11-9-5.pdf
- AERA note describes face erosion and head-off eight-valve repair: https://www.engineprofessional.com/TB/TB011117-1.pdf
- GM Genuine Parts 55563529 provides a documented genuine service number: https://parts.gmparts.com/product/gm-genuine-parts-engine-intake-valve-55563529
- Earlier seller snapshots: eight genuine valves $314.48 to $363.92; eight TRW candidates $102.24. Neither amount includes diagnosis, head work, tools, gaskets, machine shop, labor or other damage.
- Unknown: original fitted valve metallurgy, complete VIN cutoff, controlled comparative lifetime of genuine versus TRW.
- Buying rule: ask for overnight-cold start and appropriately performed cold compression/leak-down if symptoms; documented prior repair should show installed valves and post-repair test. Do not prophylactically remove a healthy head on present evidence.

## Trionic 8 ECU and false fault reports

- Saab WIS technical advice TA248-0336 documents false P0606 detection in a defined diagnostic circumstance; not every P0606 is false: https://saabwisonline.com/9-3-9440/2005/2-engine/4-cylinder-petrol/engine-management-system-trionic-t8/bulletins-si-mi/ta248-0336-false-detection-of-dtc-p0606-00
- Saab WIS MY2006 T8 architecture and engine-front ECU location: https://saabwisonline.com/9-3-9440/2006/2-engine/4-cylinder-petrol/engine-management-system-trionic-t8/technical-description/control-module-trionic-4-cyl-petrol-589 and https://saabwisonline.com/9-3-9440/2006/2-engine/4-cylinder-petrol/engine-management-system-trionic-t8/location-of-components/control-module-trionic-b207-switch-b-589b
- Existing specialist vendor observations: programming-only $75-$89.99; donor required and at least one vendor requires communicating original ECU. Those prices are not complete installed replacements.
- Engine-front location makes thermal stress a plausible investigation target but **does not demonstrate that relocation extends service life**. Any relocation proposal must address harness strain, shielding, water ingress, grounds, electromagnetic effects and service access, plus actual comparative outcome data.
- Buying rule: obtain Saab-capable diagnostics, power/ground and software verification, and confirm original ECU data recoverability before valuing a non-running car as an inexpensive ECM repair.

## Engineering ranking

| Concern | Severity when established | Preventative improvement established? | Buyer action |
| --- | --- | --- | --- |
| Cold intake-valve compression loss | High, internal head repair | No proven no-failure retrofit | Cold test; require completed repair evidence or full head quote |
| T8 ECU no-communication | Potentially high due to security/programming | No proven heat-relocation lifetime improvement | Check electrical supply and clone viability; quote donor plus specialist |
| P0606 alone | Diagnosis-dependent | Factory software diagnostic path | Follow factory fault differential before replacing ECU |

These findings reuse existing technical documents rather than creating duplicate defect identities. The appropriate labels are factory diagnostic pathway, genuine repair part and specialist recovery service—not proven reliability upgrade.
