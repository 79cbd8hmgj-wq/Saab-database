# VIN, gearbox and module provenance — original 9-5 and NG 9-3

**Research date:** October 12, 2026. **Phase:** original manufacturer-source coverage, before simulator or part interchange approval. Original workshop documents (Saab WIS mirrored online) and official Saab Parts subscription description are distinguished from a verified VIN-specific WebEPC result.

## The critical trap: year folders do not necessarily contain that year's decoder

The [MY2007 9-5 VIN WIS page](https://saabwisonline.com/9-5-9600/2007/0-general/general/technical-data/vin-vehicle-identification-number) is filed under **2007**, but its own position-10 table reads **A = 2010**, along with later-looking 5-door-only and K/L trim fields. Therefore **do not decode a 2007 Saab 9-5 using that mirror table**. Independently [the MY2005 9-5 VIN page](https://saabwisonline.com/9-5-9600/2005/0-general/general/technical-data/vin-vehicle-identification-number) explicitly stops its model-year mappings at **4 = 2004**. It is inadequate proof of MY2005 VIN-code applicability.

Even the [MY2005 9-3 VIN page](https://saabwisonline.com/9-3-9440/2005/0-general/general/technical-data/vin-vehicle-identification-number) prints an example whose tenth character is **3**, although its separate year table says **5 = 2005**. The *table* is not permission to ignore the contradictory example without documenting it. These facts concern **retrieved source reliability**, not a claim that a real car is misidentified. A future real VIN should be cross-checked against an independently dated manufacturer guide and the actual body-stamped VIN.

## Year-scoped MY2005 and MY2008 9-3 (9440) VIN evidence

| Field | MY2005 WIS | MY2008 WIS |
| --- | --- | --- |
| Position 4 | F = 9-3 | F = 9-3 |
| Position 6, body | 4=4-door; 7=convertible | 4=4-door; **5=5-door**; 7=convertible |
| Position 7, gearbox | 1=6-speed auto; 5=5MT; 6=6MT; 9=5-speed auto | Same broad options plus AWD 6AT (2) and AWD 6MT (7), explicitly FWD for others |
| Position 8, B207 | Marketing designations 1.8t (F), 2.0t (S), 2.0 Turbo (Y) | **F=B207E; S=B207L; Y=B207R**, explicitly named |
| Position 10, model year | **5=2005** (contradicts page example) | **8=2008** |

Sources: [2005](https://saabwisonline.com/9-3-9440/2005/0-general/general/technical-data/vin-vehicle-identification-number), [2008](https://saabwisonline.com/9-3-9440/2008/0-general/general/technical-data/vin-vehicle-identification-number). MY2008 engine-code labels are not automatically assigned to MY2005 without a separately checked MY2005 code source. No arbitrary VIN examples or guessed checksum results are inserted.

For the 9-5, the [MY2006 WIS plates and labels](https://saabwisonline.com/9-5-9600/2006/0-general/general/technical-data/plates-and-labels) names six separate evidence points: windshield VIN, body-stamped VIN, VIN plate, engine number, gearbox number and body/trim identification label. Recording the actual component stamp separately is crucial when inspecting a used or non-running car, especially if it may have received replacement drivetrain parts.

## FA57 automatic does not mean approved cross-platform replacement

Both factory manuals say **FA57**, yet identify the installed boxes using substantially different adaptation schemes:

| Factor | OG 9-5 MY2007 | NG 9-3 MY2005 |
| --- | --- | --- |
| Factory type-code example | `FA57 C01 97CV00101` | `FA57 1 01 03CV12345` |
| Engine/vehicle adaptation code | **C** | **1** (B207E/L/R) |
| Transmission family | 5-speed FWD automatic | 5-speed FWD automatic |
| TCM engine-code table (independent MY2005 document) | E=D223L; F=B205E; G=B235E; **H=B235R**; I=B308E | J=B207L; **K=B207R**; L=B207E |
| Fitment conclusion | **Not approved for exchange from these sources** | **Not approved for exchange from these sources** |

References: [9-5 FA57 identifier](https://saabwisonline.com/9-5-9600/2007/4-transmission/automatic-transmission/technical-data/type-designation), [9-3 FA57 identifier](https://saabwisonline.com/9-3-9440/2005/4-transmission/automatic-transmission/5-speed-fa-57/technical-data/type-designations), [9-5 TCM codes](https://saabwisonline.com/9-5-9600/2005/4-transmission/automatic-transmission/technical-data/control-module), [9-3 TCM codes](https://saabwisonline.com/9-3-9440/2005/4-transmission/automatic-transmission/5-speed-fa-57/technical-data/type-designations). Both FA57 documents use month codes A,B,C,D,E,F,G,H,J,K,L,M; the **I** code is omitted. Examples show manufacture dates; these are **not real car measurements** or VIN model-year positions.

A different [MY2005 9-3 AF40 six-speed automatic](https://saabwisonline.com/9-3-9440/2005/4-transmission/automatic-transmission/6-speed-af-40/technical-data/type-designations) is documented as Aisin TF-80SC / GM AF40; do not conflate with FA57. The [MY2005 9-3 FA57 TCM reference](https://saabwisonline.com/9-3-9440/2005/4-transmission/automatic-transmission/5-speed-fa-57/technical-description/tcm-fa-57-502a) separately names G33T and pins; those pins are *not* transferable to another transmission application.

## Manual gearbox source warnings

The [9-5 MY2006 manual type-code page](https://saabwisonline.com/9-5-9600/2006/4-transmission/manual-gearbox/technical-data/type-designation) prints `FM55 B01 A12345` as an example yet labels the 'first group' `FM57`. The [9-3 MY2005 manual page](https://saabwisonline.com/9-3-9440/2005/4-transmission/manual-gearbox/5-speed/technical-data/type-designation) has an inconsistent description of three/four groups and a conflicting second-group example/development line. These remain named research gaps, **not corrected from assumption**.

## Manufacturer source that is needed for proper part substitution

[Official Saab WebEPC](https://saabparts.com/saab-subscription-services) states that it uses a VIN or vehicle-build data to hide nonapplicable parts, displays assembly diagrams, records fitment comments and offers approved NLS supersession chains. The repository has **not** accessed actual paid VIN/part results, so this establishes *capability*, not any approved part relationship.

[MY2007 9-3 TIS2000 SPS](https://saabwisonline.com/9-3-9440/2007/0-general/tis-2000/technical-description/service-programming-system) requires confirming the displayed VIN, engine and transmission variant when reviewing an ECU program, and displays hardware and software numbers. These are identification steps, **not approval to flash or pair donor modules**.

## On-lot vehicle-identification evidence checklist

1. Photograph/read **complete 17-character VIN**, compare windshield, body stamping, official paperwork (never record a made-up VIN). Preserve model year and actual body style.
2. Locate and record original **engine stamping/version and serial number**, **gearbox stamped type/adaptation/development/production serial**, and any visible replacement markings separately.
3. Verify **market**, transmission identity, actual manual/automatic equipment, body variant and any relevant **VIN/chassis suffix** as a string, not an unrestricted integer comparison.
4. Record transmission control/engine control module **hardware and software IDs** through manufacturer-approved read-only diagnostics if available; do not attempt firmware swaps.
5. Use official **VIN-filtered WebEPC** for original article ID, build split, any one-way supersession, needed bolts/seals and applicability comments **before ordering**, and retain unresolved fields in `templates/vehicle-instance.json`.
6. Only then examine donor-car replacement options and physical measurements. No full source-supported interchange approval exists in this batch.

Outstanding tasks: independently correct model-year 9-5 VIN code guides, real installed-label photographs, genuine WebEPC VIN-bound part lists and manufacturer supersessions, firmware pairing rules, and exact 2005/2006 engine/transmission mappings. No simulator, quantitative durability model or VIN decoding software has been introduced.
