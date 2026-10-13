# Phase 0 — cross-manufacturer replacement pilot: GM/Opel, Fiat, aftermarket

**Evidence date: 2026-10-13. Gate C NOT MET.** This research is explicitly about *non-Saab-labelled parts*, not a complete original Saab parts catalogue. Priority: North American second-gen **9-3 (9440) MY2005–06 B207 FWD** and original **9-5 (9600) MY2006–09 B235**. **No donor part has been installed, bench-tested, or validated for a specific Saab.**

## Four questions kept separate

- **Shared OEM identity:** factory Saab and donor manufacturer document exactly the same OE assembly and revision. **Not yet established.**
- **Shared aftermarket SKU:** one supplier markets its one SKU for both Saab and Opel/Fiat/Cadillac cars. **Found in wheel hubs; catalogue-level only.**
- **Saab-specific aftermarket direct replacement:** a different company makes a radiator/PCV part **for Saab**. **Found but cannot be described as a GM donor part.**
- **Engineered adaptation:** a non-matching donor is deliberately modified to meet interfaces and durability. **No validated conversion or design.**

Each new `parts[*].interchange_candidate` object stores `strategy`, original Saab reference numbers, donor marque claims, mandatory proof and three always-false approval/vehicle/durability flags. `aftermarket_reference` edges are *catalogue leads* (not OE manufacturer substitutions). Supplier entries are `supplier_claim`, with `needs_vehicle_verification`. No stock, price, reliability gain, or legal approval is asserted.

## 1. Strongest new cross-manufacturer research lead: 9-3 front hub

[PFI manufacturer-origin wheel-bearing interchange table](https://7000765.fs1.hubspotusercontent-na1.net/hubfs/7000765/Knowledge%20Base/PFI/PFI%20Automotive%20Bearings.pdf) maps **PHU3191** to **Saab 9-3 MY2003–11, Opel/Vauxhall Vectra C and Signum, Fiat Croma 2005–11 and Cadillac BLS 2006–10**, among its OE reference strings (Saab `12799815`, `93175327`, `93186387`; SKF `VKBA3620`; FAG `713644090`). The original [Saab MY2004 hub/bearing explanation](https://saabwisonline.com/9-3-9440/2004/7-suspension-wheels/front-suspension/technical-description/front-assembly) confirms the bearing and hub form a factory-preloaded unit with integrated wheel-speed sensing. The [MY2006 hub installation](https://saabwisonline.com/9-3-9440/2006/7-suspension-wheels/front-suspension/adjustment-replacement/wheel-hub-front) uses a sensor cable, three hub bolts and a **new centre nut** after removal.

**Assessment: worthwhile catalogue-level shared-platform SKU, not a verified Opel junkyard donor.** Next retrieve actual donor and Saab factory EPC entries, hub-to-knuckle geometry, spline dimensions, sealing, ABS signal and connector and service kits; confirm the true installed part on a real car. The broad MY2003–11 cataloguing should not be expanded to arbitrary AWD/XWD donor, side, or suspension variant.

### Stronger manufacturer-origin follow-up: FAG 713 6440 90

The [original Schaeffler/FAG product listing](https://vehiclelifetimesolutions.schaeffler.com/en/catalog/auto-parts/axle-mounting-steering-wheels/wheel-hub-mounting/wheel-hub/wheel-bearing-kit/p-TA-654-7136440900) gives a **137 mm outer diameter and integrated ABS sensor**, and labels **SAAB 93171495, 93175327, 93186387**, corresponding GM references and Opel 1603143/1603243/1603294 as **Interchangeable** for the FAG aftermarket kit. Crucially, its **FIAT 51748680** and **OPEL/VAUXHALL 12796081** use the weaker separate label **Reference corresponds to a component**. We preserve these separate categories and do not overstate a Fiat used donor match. [MY2006 original Saab front sensor](https://saabwisonline.com/9-3-9440/2006/5-brakes/tcs-esp/adjustment-replacement/front-wheel-speed-sensor-298fl-fr) independently confirms the hub-integrated ABS architecture. [TecAlliance-using merchant application](https://motostacja.com/p/38090.html) maps the broader vehicles but warns dates of overall models are not part-specific fitment, so every candidate still needs a VIN and interface check.

**Disposition:** FAG is a stronger direct manufacturer aftermarket cross-brand lead than a reseller-only claim. It does not establish a safe used original GM/Opel/Fiat hub transplant, a verified improvement to reliability, US stock, or a reduction in repair cost.

## 2. 9-3 front brake pads: a promising common OE number, but brake-level trap

[Saab Parts' North American brake-pad PDF](https://saabparts.com/us/wp-content/uploads/sites/10/2022/02/BrakePadsRetail.pdf) indexes **93188111** for the **9-3 15-inch front brake system** (the PDF row was accessible via search excerpt, not fully read). [eSaabParts' specific part](https://www.esaabparts.com/saab/parts/93188111) gives **285/302 mm AA/AB** and a chassis suffix limitation. [Spareto OE number cross](https://spareto.com/oe/93188111) lists **93188111** under Saab and Opel/GM and catalogue alternatives **Delphi LP1723**, **Bosch 0 986 494 044** and ATE. These are *merchant/OE-number associations*, not official Saab-Opel interchange certificates or performance testing. Original [Saab MY2006 brake-option plate documentation](https://saabwisonline.com/9-3-9440/2006/5-brakes/footbrake-system/technical-data/vin-plate-brake-caliper-and-brake-discs) maps positions **7–10** to front/rear rotor and caliper codes; first retrieve actual plate and rotor size. **Never treat 93188111 as fitting the 314mm AC or 345mm AD front-brake families.**

## 3. Original 9-5: non-Saab supplier is different from a GM donor

The currently recorded [Nissens automatic radiator `32019620` catalogued to Saab `5193388`](https://www.esaabparts.com/saab/parts/32019620) is a **Saab-specific aftermarket radiator option**. The [Saab factory radiator procedure](https://saabwisonline.com/9-5-9600/2006/2-engine/cooling-system/adjustment-replacement/radiator-4-cyl) has gearbox oil-cooler connections on automatic cars. Neither source documents an Opel radiator swap. The existing [ProParts PCV kit `21341200` associated with `55561200`](https://www.esaabparts.com/saab/parts/21341200?ss=55561200) is shown by its merchant under *earlier* 9-5/old 9-3 diagrams. **It is not approved for a 2008 B235R merely because the engine family resembles earlier Saabs.** Exact later-year PCV routing and serial revisions remain open.

## Approval criteria and research sequence

1. **Provenance:** identify exact original Saab VIN-filtered OE component, position/side, model-year build boundaries, and matching complete donor OE number.
2. **Cross-maker evidence:** seek original manufacturer catalogues/authoritative part-maker data with precise vehicle **year, axle, powertrain, brake option and revisions**; record conflicts without averaging them.
3. **Mechanical and functional equivalence:** dimensions, seals, material/pressure and thermal envelope, fasteners, electrical sensor/protocol signals, service calibrations and related components. Safety-critical hardware needs further independent verification.
4. **Availability economics:** dated United States stock/price *per SKU* including any extra hardware, programming and fitment labor. Do not treat cheaper sticker price as cheaper installed repair.
5. **Real reliability:** compare representative failures and valid load tests of actual installed alternatives. Without evidence, durability remains **unknown**, not improved.

## Pilot exit status

- **Shared-platform hub SKU candidate:** identified, unverified for vehicle.
- **Shared Saab/Opel front-pad OE-number reference:** documented in merchant cross; unverified for installed brake option.
- **Non-Saab brand Saab-specific radiator and early PCV lead:** already recorded, **not** cross-platform donor approval.
- **No documented Toyota-equivalent durability improvement, GM donor vehicle verified plug-and-play interchange, or legal aftermarket conversion.**

The next priority should be first-party Opel/GM component identities and application drawing for the **9-3 front hub** before widening this to other chassis/systems. The B235 engine architecture cannot be assumed identical to an Opel application just because Saab belonged to GM.
