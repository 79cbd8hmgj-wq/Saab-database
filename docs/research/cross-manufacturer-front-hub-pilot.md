# Phase 0 — cross-manufacturer interchange pilot (front 9-3 wheel hub)

Research date **2026-10-13**. First dedicated cross-manufacturer candidate workstream for priority US/Canadian **MY2005–06 9-3 (9440), B207**. **This project does not assert that any donor GM/Opel/Fiat hub can safely replace an actual Saab hub yet.**

## First direct manufacturer evidence

[Schaeffler's own FAG 713 6440 90 product entry](https://vehiclelifetimesolutions.schaeffler.com/en/catalog/auto-parts/axle-mounting-steering-wheels/wheel-hub-mounting/wheel-hub/wheel-bearing-kit/p-TA-654-7136440900) describes **137 mm outer diameter, integrated ABS sensor** and lists **SAAB 93171495 / 93175327 / 93186387** as *Interchangeable* catalogue OE numbers. The same FAG replacement also lists **GM** equivalents **93171495 / 93175327 / 93186387**, plus **Opel 1603143 / 1603243 / 1603294** and others. Importantly, its **FIAT 51748680** and **Opel/Vauxhall 12796081** are in a different category: *Reference corresponds to a component*; these must **not** be reinterpreted as confirmed identical OE assemblies.

An independent aftermarket [TecAlliance-based retailer application page](https://motostacja.com/p/38090.html) also groups **9-3, Vectra C/Signum and Fiat Croma** under this FAG SKU, but warns overall model production years are not part-specific fitment and a VIN/variant check is necessary. No genuine Saab factory or GM/Opel VIN-filtered part-line lookup was obtained.

## Factory architecture and safe replacement dependency

Original Saab [MY2006 wheel hub service](https://saabwisonline.com/9-3-9440/2006/7-suspension-wheels/front-suspension/adjustment-replacement/wheel-hub-front) documents a three-bolt front hub and speed-sensor connector, and expressly requires replacing the hub-center nut if removed. [MY2006 TCS/ESP front sensor](https://saabwisonline.com/9-3-9440/2006/5-brakes/tcs-esp/adjustment-replacement/front-wheel-speed-sensor-298fl-fr) confirms the sensor is **integrated into the wheel hub**. Neither Saab page names a FAG replacement or confirms that the Opel vehicle's original assembly has the same electrical/physical fit.

## Candidate decision record

Machine-readable [candidate matrix](../../data/interchange-candidates/phase0.json) indexes the specific supplier product, Saab and cross-brand catalogue-number statuses, evidence sources, vehicle research scope and the blocked verification gates. It records **not approved for a specific VIN**, **unverified used-GM/Opel donor**, **no proven lower cost**, and **no demonstrated reliability gain**. Those are different dimensions and should never be conflated.

| Claim | Current evidence | Disposition |
| --- | --- | --- |
| A FAG aftermarket kit is catalogued against Saab and Opel/GM OE reference families | Original Schaeffler product listing | **Supplier-supported catalogue candidate** |
| The 2006 Saab 9-3 front speed sensor is hub-integrated | Original Saab WIS | **Factory-documented architecture** |
| A specific used donor Opel/Fiat OE hub is a direct fit to a MY2005/06 B207 US Saab | No VIN-specific OE source or physical/electrical verification | **Unapproved** |
| FAG product improves service life compared with an original Saab hub | No comparative durability test found | **Unproven** |
| It is cheaper or locally available | No verified current US quote/stock | **Unknown** |

## Next cross-manufacturer targets

1. **Complete this pilot** with authenticated original GM/Opel and Saab WebEPC VIN-by-VIN hub identities plus spline, wheel mounting, ABS signal and fastener verification; **do not** assume an aftermarket common part means all donor assemblies are identical.
2. **Cooling/PCV**: investigate direct manufacturer aftermarket products and true alternate-OEM applications only when actual part/engine/gearbox data exists. Existing Nissens and ProParts catalogue claims remain supplier claims, not OEM manufacturer-approved interchange.
3. **Brakes**: use original 9-3 VIN brake-level/option row to segregate rotor/caliper/pad variants before any shared GM pad/bearing recommendations. Do not resolve the original 9-5 brake-carrier torque discrepancy from catalogue fitment.
4. **Electronics**: check connectors, sensor characteristics, protocols, power/ground and authorized module pairing before comparing same-looking GM modules.

This is a bounded source-evidence **research increment**, not part-purchasing advice or a calibrated reliability simulator.
