# Phase 0 Gate C — manufacturer-channel US VIN and conditional service-kit provenance

**Evidence date:** 2026-10-13. This package advances **work package 5: original manufacturer replacement identity and supersession evidence**, while closing parts of work package 1. The target cars are **US/Canadian-market original 9-5 (9600), MY2004–09 B235**, and **US/Canadian-market 9-3 (9440), MY2005–06 B207**. **The original Saab USA bulletins document US specification; equivalent Canadian build particulars still require independent confirmation.**

**Critical distinction:** Vehicle assembly plant (Sweden/Austria), destination sales market (US/Canada), original factory VIN codes, actual installed engine/gearbox, Saab WebEPC approved part application, a supplier's cross-reference and an official **service kit** are different kinds of evidence. The repo does not merge them into a single “fits” field.

## Manufacturer-sourced VIN discovery

[Saab Parts USA's owner-reference directory](https://saabparts.us/reference-library/) publicly hosts a [13-page compilation of original Saab Automobile VIN sheets](https://saabparts.us/wp-content/uploads/1/2023/05/VIN-breakdown-for-1999-2011-9-3-9-5.pdf). The **original Saab Automobile AB/America bulletin sheets**, *not WIS model-year directory names*, identify the following original US-market code definitions:

| Original bulletin page (PDF page zero-index) | Model year and position 10 | Position 4 model | Position 7 gearbox | Position 8 original engine codes mentioned | Important limits |
| --- | --- | --- | --- | --- | --- |
| 2004 (p7) | `4` | E=9-5; F=9-3 | 5=5MT; 6=6MT; 9=5AT (listed) | 9-5 E=B235E, A=B235L, G=B235R; 9-3 S=B207L, Y=B207R | Original source-specific marketing/engine grouping; production and donor fitment need verification |
| 2005 (p8) | `5` | E=9-5; F=9-3 | 5=5MT; 6=6MT; 9=5AT | 9-5 E=B235E, A=B235L, G=B235R; 9-3 S=B207L, Y=B207R | **Printed example VIN has prior-year digit 4**, while the **2005 code table correctly says 5**. Document sample inconsistency, never treat sample as real vehicle. |
| 2006 (p9) | `6` | E=9-5; F=9-3 | 1=6AT; 5=5MT; 6=6MT; 9=5AT | Document lists U=B284L (9-3 V6), Y=B207R (9-3), G=B235R (9-5) | This shorter original **USA** table is not evidence that other engines could not exist in Canada/other markets. |
| 2007 (p10) | `7` | E=9-5; F=9-3 | 1=6AT; 5=5MT; 6=6MT; 9=5AT | Document lists U=B284L (9-3 V6), Y=B207R (9-3), G=B235R (9-5) | Year/year engine row exists, yet any individual drivetrain might have been swapped. |

All these factory tables also include **position 6** 4=sedan, 5=five-door/wagon, 7=convertible (when that vehicle body type is in the car line), **position 9** check digit, **position 11** 1=9-3 Trollhättan, 3=9-5 Trollhättan, 6=9-3 convertible Graz, and **positions 12–17** serial.

**What this actually closes:** Original official USA definitions for **9-5 MY2004–07**, and **9-3 MY2005–06**. Earlier copies in SaabWISOnline's `/2005/`, `/2007/` and `/2009/` directories could be misleading: one 9-5 WIS page says MY2010 despite being in 2009 directory; original 2005 examples sometimes display previous-year codes. The dated Saab USA sheets establish the target model years independently. Those contradictions remain preserved in the history as **source-quality evidence**, not silently rewritten.

**What remains open:** The published 13-page collection *jumps from 2007 to 2011*. It does **not contain individual 2008 and 2009 US-market year sheets**. The unrelated 2011 9-5 is **NG 9-5**, not a source for first-generation 2008–09 engine/gearbox/year tables. This research does not verify an authentic Canadian-specific model-year code table or decode a specific buyer VIN. We do **not** fill missing 2008–09 mappings from generic Wikipedia or guesses.

## Real original Saab 9-3 replacement: service kit is conditional, not a complete donor module

Saab Parts USA hosts the official [MY2003–11 9-3 ignition switch module (ISM) instructions](https://saabparts.us/wp-content/uploads/1/2023/06/Saab-93-2003_11-Ignition-Switch-Module-ISM-32021815-Kit-Saabparts-Reference-Library-version.pdf):

| Earlier module | Official service offering | What the parts relationship **actually** means |
| --- | --- | --- |
| **12801010** | **32021815** | Manufacturer service-channel says 12801010 “now kit 32021815”; the repair requires reusing the intact **old black sliding/rotating mechanism**. The kit is not a self-contained direct plug-in complete switch. |

The original lower mechanism must be undamaged, clean and free-moving. The official procedure also identifies a **key retaining tab** that must be properly seated to prevent the key jumping out, and correct orientation of the new plunger/spring and contacts. An irreparably broken old black assembly needs another suitable switch, not just the kit.

The database therefore records the original module and kit as **two manufacturer-documented part records** with an explicit **conditional `replaced_by_service_kit`** relation, not a universal `superseded_by` or a bidirectional physical interchange. Neither stock, current delivery, exact VIN application nor compatibility with a swapped security system was proven. A safety-/anti-theft-related service procedure must be followed properly, and we should not claim a generic non-jailbroken tool or spare key can substitute for Saab service access.

## Other factory/official constraints relevant to future replacement approvals

The [official Saab Parts USA lost-key guide](https://saabparts.com/us/wp-content/uploads/sites/10/2023/09/What-happens-if-I-lose-all-the-keys-to-my-Saab-Sept-2023.pdf) says the **early original 9-5 separate key/remote** (MY1999–02) is no longer available and was superseded to the integrated later style. However, **Tech 2 pairing**, original TWICE theft module status and possession of a working key are crucial. For all keys lost, that original guide describes **TWICE replacement plus two new keys**, illustrating why a physical/seller-described supersession is not a guaranteed working repair. It names no particular key SKU; none has been inferred.

The separate [MY2008 original 9-5 left engine mounting WIS](https://saabwisonline.com/9-5-9600/2008/2-engine/basic-engine-4-cylinder-petrol/adjustment-replacement/engine-mounting-left) distinguishes **47 Nm manual versus 84 Nm automatic mounting joint**, and requires a **centre mounting nut 84 Nm through printed chassis ID 73514478, 74 Nm from 73514479**. The printed numbers are **not entire 17-character VINs**, and a torque revision is **not** an OEM part number or proof that a new mount replaces an earlier mount. This is an example of an original production-restriction **that still needs the exact actual VIN and bolt** before use.

## Which authoritative supplier tools are available?

- [Official Saab WebEPC](https://saabparts.com/saab-subscription-services) advertises paid VIN/build filters, OE exploded drawings, specific application comments and **approved forward supersessions for no-longer-serviced parts**. **No paid subscriber query or specific vehicle records were accessed in this package.** A true kit/assembly/bolt-on substitution still requires the original filtered result.
- [Saab Parts USA's MySaabCar](https://saabparts.com/us/) advertises a vehicle VIN decoder and original equipment list. It requires owner account interaction; **none was performed**.
- Historical retailer references in `epc-provenance` and `subframe-parts-brake-lines` still do **not** prove manufacturer approval for 24401110, 13247173, 12825111, 32022623 or any actual 9-3 subframe/frame bushing interchange. No existing `supplier_claim` has been promoted or rewritten.

## What to capture when an actual project Saab appears

The [manufacturer replacement verification template](../../data/inspection-templates/oem-replacement-verification.json) is an empty, gated evidence form (not a simulated car). It requires the **actual VIN/build and installed original component ID**, function/position/side, manufacturer original numbered part, the **exact official WebEPC illustration and application note**, any forward directional NLS chain with source/conditions, accompanying hardware/geometry/seals/firmware/security and final after-install tests. It distinguishes **drop-in original**, **conditional service kit/rebuild**, **aftermarket claim awaiting proof** and **unknown**. A printed generic Saab model-year row or a vendor supersession is not enough to approve the original part.

## Remaining Phase 0 readiness status

**Gate A remains partially met**, although original 2005/06 identity documents are now source-backed and candidate year codes can be checked. **Gate B remains unmet**, and **Gate C is not yet met**: one conditional service-kit precedent does not replace a complete manufacturer VIN-filtered parts matrix for radiators, rear subframes, steering, brakes, transmission/TCM or electronics.

**Next blocker:** Recover missing genuine **US/Canadian MY2008/09 VIN definitions** and obtain actual licensed WebEPC results when a VIN/vehicle candidate and user-approved access are available; then move through the most critical original components. While waiting, the separate emissions/exhaust **work package 6** is researchable without a specific VIN.
