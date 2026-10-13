# Phase 0 Gate A/C — vehicle identity and component provenance

**Research date:** 2026-10-13. Scope: original 9-5 (9600), especially **US/Canada MY2004–09 B235**, and second-generation 9-3 (9440), especially **US/Canada MY2005–06 B207 FWD**. This is the first work package in [the gate-closure plan](../gap-closure-plan.md).

**Verdict: identity evidence improved, Gate A and C are still NOT passed.** No real VIN, factory WebEPC per-VIN part result or inspected drivetrain was obtained. The worksheets are intended to prevent unsafe year/trim-based assumptions, not decode an absent VIN into an invented car.

## 1. Original 9-5, MY2004–09 B235 — identification worksheet

| Required field | Where evidence comes from | What we currently know or do not know |
| --- | --- | --- |
| Full 17-character VIN, model-year position, title versus stamped VIN | VIN visible at windscreen and stamped on body; original [MY2006 Saab plates and labels](https://saabwisonline.com/9-5-9600/2006/0-general/general/technical-data/plates-and-labels) | **No candidate VIN provided.** Independently confirm an authoritative model-year-correct decoder. |
| Engine type (B235E versus B235R) and **engine serial** | Original Saab engine stamp/tag, engine records; physical condition | Cannot infer actual engine from seller's 'Aero' listing, trim badge, or unverified WIS VIN legend. |
| Gearbox family and exact **stamped type string** | Physical gearbox; [MY2008 9-5 5-speed manual type guide](https://saabwisonline.com/9-5-9600/2008/4-transmission/manual-gearbox/technical-data/type-designation) and [MY2009 9-5 FA57 type guide](https://saabwisonline.com/9-5-9600/2009/4-transmission/automatic-transmission/technical-data/type-designation) | FM55/FM57 manual and FA57 5AT are distinct families. Original gearbox factory type uses adaptation and development codes beyond name. Sample code/year in WIS can represent historical demonstration, not the actual car. |
| TCM/ECU software and configuration | Factory read-only Tech 2 when safe and available; physical modules/labels | Unknown until car is scanned; housing/tag similarity does not prove software/immobilizer compatibility. |
| Body style, market and build-specific options | Physical 4D/5D, VIN build record, manufacturer catalogue | Restricts radiator, subframe, suspension, exhaust and other assemblies. Don't generalize from year alone. |
| Original OEM part and supersession | [Official Saab WebEPC](https://saabparts.com/saab-subscription-services) **filtered by the actual VIN/build** | Subscription advertised; **no paid/VIN result accessed**. Every replacement approval remains pending. |

### Critical year-source failures to guard against

The [9-5 WIS folder labelled MY2009](https://saabwisonline.com/9-5-9600/2009/0-general/general/technical-data/vin-vehicle-identification-number) prints **A=2010** at the tenth VIN position, uses 5-door-only, and lists gearbox codes C/P. **That is not proof that MY2009 American/Canadian cars use that table**. This repeats the existing warning for WIS 2007 containing MY2010 and MY2005 containing a year mapping ending at 2004. The file-folder name is not the revision or effective model year. A genuine 2008–09 VIN must be resolved using a properly validated original model-year source or official WebEPC, not a mirrored folder.

The [MY2008 manual transmission type page](https://saabwisonline.com/9-5-9600/2008/4-transmission/manual-gearbox/technical-data/type-designation) prints the example **FM55 B01 A12345** but labels another explanatory subsection **FM57**. We preserve both as written rather than converting FM55 into FM57. The [MY2009 FA57 page](https://saabwisonline.com/9-5-9600/2009/4-transmission/automatic-transmission/technical-data/type-designation) uses a sample **FA57 C01 97CV00101** whose production marker indicates 1997; the **sample** cannot be interpreted as the build date of the model-year 2009 vehicle. A swapped gearbox is possible and must be confirmed physically.

### Real-car fields to complete

- VIN photographed from dash and body stamping (keep private), title year and build label.
- Engine code/serial, **gearbox complete stamping**, manual/automatic and gearbox development adaptation.
- TCM/ECU hardware/software where safely readable; modification/repair history.
- 4D sedan versus 5D SportCombi, market/emissions configuration, chassis/body modifications.
- Manufacturer WebEPC screenshot/record with original OE part number, part category, direction of supersession, VIN restrictions, accompanying hardware and source observation date.

**Unresolved blocker:** MY2005–09 original 9-5 year-specific complete VIN position tables remain unverified in the mirrored sources; do not mark this worksheet 'VIN-validated' merely because physical VIN characters are available.

## 2. Second-generation 9-3, MY2005–06 B207 — identification worksheet

| Required field | Factory statement | Stop condition / remaining proof |
| --- | --- | --- |
| VIN, body and transmission marketing codes for **MY2005** | [MY2005 Saab VIN table](https://saabwisonline.com/9-3-9440/2005/0-general/general/technical-data/vin-vehicle-identification-number): position 4=F; position 6 4=4D, 7=convertible; position 7 1=6AT, 5=5MT, 6=6MT, 9=5AT; position 10 5=2005 | **Only 2005 table.** It prints an example with tenth VIN character 3, a source inconsistency; do not use the example as evidence the car is MY2005. The matching **2006** decoder has not been recovered. |
| Installed five-speed **FA57** automatic | [MY2006 FA57 physical designation](https://saabwisonline.com/9-3-9440/2006/4-transmission/automatic-transmission/5-speed-fa-57/technical-data/type-designations) says adaptation code 1 for B207E/L/R; TCM engine letters J=B207L, K=B207R, L=B207E | Photograph full gearbox stamping and record TCM hardware/software; family name alone doesn't approve 9-5 or 9-3 donor interchange. |
| Installed six-speed **AF40** automatic | [MY2006 AF40 type guide](https://saabwisonline.com/9-3-9440/2006/4-transmission/automatic-transmission/6-speed-af-40/technical-data/type-designations) uses example TF-80SC AF40 PD, separate GM part-number example **13106944** | The **2006-folder text calls it MY2005**: presence of the page is not proof that every MY2006 US/CA B207 could be fitted with AF40. Verify per VIN/build. Historical number is not a replacement authorization. |
| Which automatic transmission fluid? | [MY2006 AF40 description](https://saabwisonline.com/9-3-9440/2006/4-transmission/automatic-transmission/6-speed-af-40/technical-description/brief-description-of-the-gearbox): AW-1 / Saab **93 165 147** for 6AT AF40 and no dipstick | Never import original 9-5 FA57 Saab 3309 fluid specification or its 80°C dipstick procedure into AF40. Confirm installed hardware first. |
| Installed five-speed manual | [MY2006 five-speed manual legend](https://saabwisonline.com/9-3-9440/2006/4-transmission/manual-gearbox/5-speed/technical-data/type-designation) uses FM57 B05 sample but inconsistent explanations | Preserve actual stamping; source has borrowed 9-5 code and inconsistent group labels. Do not order a donor by FM57/marketing year alone. |
| Installed six-speed manual | [MY2006 six-speed F40 gearbox specification](https://saabwisonline.com/9-3-9440/2006/4-transmission/manual-gearbox/6-speed/technical-data/gearbox) names F40 and differentiates **2.4 L dry**, **2.2 L replacement** | F40 is not FA57, AF40 or FM55; dry and refill capacities have different meanings. |
| Suspension/steering chassis option and **left/right strut part** | [MY2005 front](https://saabwisonline.com/9-3-9440/2005/7-suspension-wheels/front-suspension/technical-data/vin-plate-springs-and-shock-absorbers) and [MY2006 rear](https://saabwisonline.com/9-3-9440/2006/7-suspension-wheels/rear-suspension/technical-data/vin-plate-springs-and-shock-absorbers) say bottom of VIN plate gives six spring/bar/damper option codes | Codes are for Saab EPC lookup and can be the **same class on left/right even while Saab part numbers differ**. No automatic part substitution from the code alone. |

### Chassis code-position lookup (both independently documented years)

| Position on option row | System |
| ---: | --- |
| 1 | Front springs |
| 2 | Rear springs |
| 3 | Front anti-roll bar |
| 4 | Rear anti-roll bar |
| 5 | Front strut insert — physically sided part |
| 6 | Rear shock absorber |

When the code row or VIN/build records are missing, parts selection must remain pending a verified manufacturer EPC reconstruction, rather than choosing arbitrary 'Aero' or 'Linear' suspension based on trim.

### Real-car fields to complete

- VIN, title year, market, **confirmed MY2006 primary-source decoding if relevant**, 4D/5D/CV actual body.
- B207 variant (not inferred solely from marketing '2.0T'), physical engine/gearbox/TCM and history of swaps.
- FA57 versus AF40 versus 5MT versus F40, full gearbox and calibration code.
- Chassis-option row photograph, each spring/bar/strut code, component side.
- Genuine WebEPC number, applicability note and original directed supersession before ordering.

## 3. Part-interchange decision boundary

| Evidence available | Allowed conclusion | Not allowed |
| --- | --- | --- |
| Factory VIN/gearbox type description | Identifies possible installed equipment classes / where to check physical tags | A donor gearbox or ECU is compatible |
| Factory suspension chassis-option code | Identifies original component **classification** to retrieve in WebEPC | Left/right struts share a replacement SKU |
| Supplier retailer cross-reference | Candidate to verify independently | Original Saab manufacturer supersession |
| Official Saab WebEPC VIN-filtered entry with date | Supports documented OEM part applicability and directed replacement in stated conditions | Automatic reverse interchange, mechanical safety or software pairing on a swapped car |
| No physical VIN, part stamp or official manufacturer fitment | **Evidence insufficient** | Arbitrary compatibility, purchase or a repairability guarantee |

**Actual advancement:** We can reliably tell a 9-3 owner which identifiers distinguish gearbox families and suspension parts, and we have identified another misfiled original 9-5 VIN page. However, no primary-source evidence closes the full **MY2004–09 9-5 VIN/build** blocker or the **MY2006 9-3 VIN** blocker; we have not touched a paid catalogue or inspected a real car. Gate A remains **partial**, Gate C remains **not met**.

**Next work package:** [Structural rust and safety inventory](../gap-closure-plan.md) (Gate A), including sedan/wagon/convertible distinctions, inspected subframe suspension pickup locations, brake/fuel pipes, and structural-vs-cosmetic boundaries. Research may proceed without an individual VIN, but inspection/fitment certification cannot.
