# Phase 0 Gate A/B — brakes, hydraulics and hardware identification

**Research date: 2026-10-13.** Source-focused analysis of the original Saab 9-5 (9600), especially 2006–2009 B235, and second-generation 9-3 (9440) 2005–2006 B207. These are *workshop information records*, not a real-car safety assessment, current OEM fitment authorization or diagnosis from a seller's photograph.

**Milestone outcome:** Saab's 9-3 brake assembly classification can now be read from the VIN chassis-option row; OG9-5 brake chart discrepancies and a dangerous 2008 brake caliper torque disagreement have been isolated. Existing serious corrosion/no-driving rules still apply. Gate A remains **partial**; Gate B **not met**; Gate C **not met**.

## 1. Original 9-3 (9440) brake level and chassis-option plate

The [MY2006 Saab VIN-plate brake-options page](https://saabwisonline.com/9-3-9440/2006/5-brakes/footbrake-system/technical-data/vin-plate-brake-caliper-and-brake-discs) assigns positions **7 front disc, 8 rear disc, 9 front caliper, 10 rear caliper** on the *bottom option row* of the actual vehicle VIN plate. Saab explicitly refers these classification codes to the EPC. If codes are lost, the historic dealer process involved importer/PIP/PAC; we have **not** established whether that assistance remains operational today. The plate is not itself a part number; an installed swapped caliper might not match it.

Independently verified [MY2006 brake rotor](https://saabwisonline.com/9-3-9440/2006/5-brakes/footbrake-system/technical-data/brake-discs) and [caliper](https://saabwisonline.com/9-3-9440/2006/5-brakes/footbrake-system/technical-data/brake-caliper) tables give:

| Saab 9-3 2006 brake level | Front rotor new | Front caliper / piston | Rear rotor new | Rear caliper / piston |
| --- | --- | --- | --- | --- |
| **1** | **285 × 25 mm**, ventilated, min **22 mm** | **FNG 57 / 57 mm** | **278 × 12 mm**, solid, min **10 mm** | **FNC 38 / 38 mm** |
| **2** | **302 × 28 mm**, ventilated, min **25 mm** | **FNG 60 / 60 mm** | **292 × 20 mm**, ventilated, min **18 mm** | **FNC 40 / 40 mm** |
| **3** | **314 × 28 mm**, ventilated, min **25 mm** | **FNRG 60 / 60 mm** | **292 × 20 mm**, ventilated, min **18 mm** | **FNC 40 / 40 mm** |
| **4** | **302 × 28 mm**, ventilated, min **25 mm** | **FNG 60 / 60 mm** | **278 × 12 mm**, solid, min **10 mm** | **FNC 38 / 38 mm** |

Each front rotor type in this WIS page has fitted lateral runout **≤0.08 mm** and rotor thickness variation **≤0.015 mm**. These are measurement acceptance tolerances *after correct assembly*, not evidence that a rusty hub is mechanically sound.

The [MY2006 9-3 front rotor procedure](https://saabwisonline.com/9-3-9440/2006/5-brakes/footbrake-system/adjustment-replacement/front-brake-disc) makes a clear fastener distinction: **front carrier-to-knuckle bolt 210 Nm +30° with specified threadlocker**, whereas the **small rotor locking screw is 7 Nm**. The [rear carrier procedure](https://saabwisonline.com/9-3-9440/2006/5-brakes/footbrake-system/adjustment-replacement/brake-caliper-holder-rear) gives **rear carrier bolt 130 Nm +45°**, but sliding **guide pin 28 Nm** and a screw-in rear piston adapter. These are *different components*, not competing numbers for the same bolt.

The MY2006 9-3 has separate front hydraulic body/pad procedures for **brake level 3 vs 1/2/4**; for 1/2/4 its inner pad arrow must follow the rotor's forward rotation. Enlarging a rotor without OEM-verified caliper, carrier, wheel/hub and hose compatibility is **not** a ready-to-install “upgrade.”

## 2. Original 9-5 (9600) brake configuration: a genuine unresolved data conflict

The [MY2009 WIS brake-configuration chart](https://saabwisonline.com/9-5-9600/2009/5-brakes/brake-discs-and-pads/technical-data/brake-configurations) includes M01–M09 rows and nominal **B1/B2/B3** combinations:

| Printed chart classification | Front disc (diameter × new thickness) | Rear disc (diameter × new thickness) |
| --- | --- | --- |
| **B1** | **288 × 25 mm** | **286 × 10 mm** |
| **B2** | **308 × 25 mm** | **300 × 20 mm** |
| **B3** | **308 × 25 mm** | **286 × 10 mm** |

However the separate [MY2006 9-5 front-rotor technical-data page](https://saabwisonline.com/9-5-9600/2006/5-brakes/brake-discs-and-pads/technical-data/brake-disc-front-wheel) reports **standard 285 ×25 mm** and **“heavily laden” 308 ×28 mm**, with **22 mm minimum thickness on both** despite the nominal heavy disc being 28 mm thick when new. These figures are **not reconcilable simply from the available pages**: they might represent different equipment, carried-forward source revisions, chart transcription, or a real change, none of which is yet proven.

**Safety rule:** Do not automatically decide that a 2008 9-5 Aero has B2 rotors, select one contradictory dimension as “the correct Saab spec,” combine 308 mm diameter with arbitrary disc thickness, or buy rotors by trim alone. Obtain the **actual installed disc dimensions, caliper and holder**, an original manufacturer VIN-filtered EPC application, and competent confirmation of a conflicting source.

## 3. Important 2008 9-5 front caliper **torque conflict**

The [MY2008 front disc replacement instructions](https://saabwisonline.com/9-5-9600/2008/5-brakes/brake-discs-and-pads/adjustment-replacement/brake-disc-front-wheel) contain a likely copy/paste error: the instructions say **4 Nm** for the small disc locking screw and also **4 Nm for the front caliper retaining bolts**. The [separate MY2008 brake fastening table](https://saabwisonline.com/9-5-9600/2008/5-brakes/brake-discs-and-pads/technical-data/tightening-torques) states:

| Joint as identified by factory | Dedicated table torque |
| --- | --- |
| Front caliper carrier/retaining bolts | **140 Nm +45°** (manufacturer specifies thread locking compound) |
| Front hydraulic body guide pins | **28 Nm** |
| Front small disc locking screw | **4 Nm** |
| Rear caliper retaining bolts | **80 Nm** |
| Rear caliper guide pins | **28 Nm** |
| Rear small disc locking screw | **10 Nm** |
| Rear hydraulic brake-pipe nipple | **16 Nm** |

**Never use the replacement-prose 4 Nm for the front caliper retaining bolts.** The conflict must be presented to the technician with both exact URLs and fastener identification; this analysis does not silently “correct” the factory page or authorize torqueing an unverified modified component. The torque table is stronger joint-specific evidence, yet this is a safety-critical discrepancy worth original Saab revision research.

## 4. Parking brake and hydraulic routing: 9-5 versus 9-3

- **Original 9-5 MY2006:** A separate rear **shoe-and-cable** parking brake operates inside the rear disc arrangement. [Saab says adjust shoes before the handbrake cable](https://saabwisonline.com/9-5-9600/2006/5-brakes/handbrake/adjustment-replacement/adjusting-the-handbrake-cable); lever should lock wheels at the **second to third notch** after adjustment. [Cable replacement](https://saabwisonline.com/9-5-9600/2006/5-brakes/handbrake/adjustment-replacement/handbrake-cable) interacts with the rear exhaust joint, shielding, cable equalizer and fuel tank straps.
- **Second-generation 9-3 MY2006:** The [parking brake acts on mechanical levers integrated into the **rear hydraulic calipers**](https://saabwisonline.com/9-3-9440/2006/5-brakes/handbrake/technical-description/handbrake), pressing rear *service* brake pads against the disc. This is **not** the 9-5 parking shoe mechanism. The [rear holder procedure](https://saabwisonline.com/9-3-9440/2006/5-brakes/footbrake-system/adjustment-replacement/brake-caliper-holder-rear) requires a compatible piston wind-back tool, not an assumed push-only piston.
- [MY2006 9-3 flexible brake hoses](https://saabwisonline.com/9-3-9440/2006/5-brakes/footbrake-system/adjustment-replacement/brake-hose) must not twist or rub any component through steering/suspension travel, with new caliper seals and **system bleeding and leak checks** after being opened.
- [MY2006 9-5 hose inspection](https://saabwisonline.com/9-5-9600/2006/5-brakes/footbrake-system/adjustment-replacement/brake-hoses) treats corrosion, pitting or damage to body-clipped rigid pipes as unacceptable. This is a critical purchase-screen checkpoint on a rust-belt Saab even if the line is not dripping.

### Actual vehicle information required before parts or road testing

Request *privately* a VIN, model/build, bottom chassis option row, full photos of installed front and rear calipers including casting/type, front and rear rotor **diameter plus measured thickness**, pad lining, hub condition, all visible hardlines/retaining clips and flexible hose sweep. Record any hydraulically wet connections, soft pedal, stuck parking-brake lever or unequal brake operation. A professional evaluation is needed whenever braking, lifting or suspension integrity is uncertain.

**No-driving / specialist branch:** cracked/chafed/leaking lines or hoses; structurally rusted line brackets/pickups; insufficient pad/disc thickness on actual correctly identified setup; improperly mounted caliper/carrier; uncertain thread engagement or conflicting torque application. The existing [Gate A structural-corrosion map](priority-structural-corrosion-inspection.md) and NY safety inspection criteria remain mandatory. Do not test-drive just to see if a defective brake “works.”

## Remaining blockers and next research objective

Exact manufacturer WebEPC OE disc, pad, caliper, holder, side, hose and hardline SKUs **are not verified**. The 9-5 specification and torque contradictions remain recorded gaps rather than artificially resolved. Source-year/MY2006 and model/year chart scopes require checking for **MY2004–09 9-5 and MY2005–06 9-3**, including modified cars and US/CA variants. ABS/ESP service bleed procedures, module codes, hydraulic unit air entry and approved current consumables also need year-specific WIS work.

The next Phase 0 package in [the closure plan](../gap-closure-plan.md) is **work package 4: non-running engine/transmission/catalyst high-cost exclusion**, not simulator programming or automatic parts approval.
