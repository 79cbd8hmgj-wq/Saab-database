# U.S. Saab OEM parts and tooling readiness — October 14, 2026

**Purpose:** Extend the [24 conditional repair scenarios](us-repair-vs-replace-feasibility.md) and [110 source-derived U.S. automatic/FWD configurations](../data/vehicle-catalogue/us-production-normalized.json) to the practical question: **What physical identity, part evidence, special tools and quotes would we need to undertake a repair without an engine or gearbox rebuild?**

Nine [VIN/tool/parts job packets](../data/vehicle-catalogue/us-parts-tool-readiness.json) use **14 specific manufacturer/dated-retailer source URLs**. The [reproducible 110-row crosswalk](../data/audits/us-parts-tool-readiness-coverage.json) distinguishes **exact workshop-example model-year matches** from **other-year research leads**. Neither type approves individual-car repairs, donor interchange, current stock, a reliable used vehicle or installed job prices. Canadian records remain unchanged.

## Verified procedural and identification distinctions

| Repair category | Factory or dated-supplier finding | Part/order boundary |
| --- | --- | --- |
| Original 9-3 **AF20/AF22** (four-speed) | Saab MY2001 [gearbox code](https://saabwisonline.com/9-3-9400/2001/4-transmission/automatic-transmission/technical-data/type-designation-gearbox) describes AF20/AF22 and an illustrative **FA44** serialized adaptation code. Its [automatic gearbox removal](https://saabwisonline.com/9-3-9400/2001/4-transmission/automatic-transmission/adjustment-replacement/automatic-gearbox-assembly) requires **83 94 850 lifting beam**, **83 94 793 subframe trolley**, **87 92 608 gearbox holder** and **87 92 277 converter restraint**. | This is substantial lift/subframe work, not a basic driveway swap; MY2001 FA44 example must not be assigned to all MY1999–02 B204/B205 automatics without the real case label |
| Original 9-5 **AF30** (four-speed) | MY2000 [Saab AF30/FA47 type designation](https://saabwisonline.com/9-5-9600/2000/4-transmission/automatic-transmission/technical-data/type-designation) contains engine-adaptation and serialized type details | Family name/four speeds alone cannot certify a donor gearbox, torque converter or TCM |
| Original 9-5 **FA57** (five-speed) | MY2008 [FA57 C01-type tag](https://saabwisonline.com/9-5-9600/2008/4-transmission/automatic-transmission/technical-data/type-designation) contains engine adaptation, revision and production serial | The second-generation 9-3 FA57 uses different adaptation identifiers |
| Second-generation 9-3 **FA57** | MY2006 [FA57 1 01 and TCM letter table](https://saabwisonline.com/9-3-9440/2006/4-transmission/automatic-transmission/5-speed-fa-57/technical-data/type-designations) describes B207E/L/R engine adaptations | Full actual case and TCM identification, original EPC fitment and programming are needed before donor selection |
| 9-3 **FA57 oil level** | MY2006 [manufacturer check](https://saabwisonline.com/9-3-9440/2006/4-transmission/automatic-transmission/5-speed-fa-57/adjustment-replacement/checking-the-transmission-fluid-level) uses **Tech2 TCM at 80°C**, a specific dipstick O-ring instruction and **87 92 822 filler funnel** | Do not use AF40's fluid-level procedure or diagnose a nonrunning car by unsupported fluid guesses |
| B284L 9-3 **AF40 oil level/pressure** | Saab [TA440-0902](https://saabwisonline.com/9-3-9440/2006/4-transmission/automatic-transmission/6-speed-af-40/bulletins-si-mi/ta440-0902-atf-oil-check-on-af40-6-speed-aut) requires **Tech2 at 70–80°C**, a level vehicle and a running-engine procedure. MY2006 [pressure check](https://saabwisonline.com/9-3-9440/2006/4-transmission/automatic-transmission/6-speed-af-40/adjustment-replacement/oil-pressure-check-b284) names special pressure equipment **87 92 301** and **87 91 600** | Full-load/pressure tests are not appropriate on an uninspected nonrunner; exact model-year/type procedure and trained operator required |
| **2008 9-5 B235** left/right engine mounts | Saab original [left](https://saabwisonline.com/9-5-9600/2008/2-engine/basic-engine-4-cylinder-petrol/adjustment-replacement/engine-mounting-left) and [right](https://saabwisonline.com/9-5-9600/2008/2-engine/basic-engine-4-cylinder-petrol/adjustment-replacement/engine-mounting-and-engine-pad-rh) procedures use **83 94 850 engine lifting beam**. Left-mount fastening specification differs at VIN **73514478/73514479** | Mount SKU differences are **not** established by the tightening difference; need real VIN and safe engine support |
| **2011 new 9-5 Turbo4** | Factory [MY2011 VIN table](https://saabwisonline.com/9-5-9650/2011/0-general/general/technical-description/vehicle-engine-and-transmission-id-and-vin-location-derivative-and-usage): position 7 **A = FWD 6AT**; position 8 **Z = A20NFT/LHU 2.0T**, **R = BioPower**. The 9650 WIS also specifies [AF40 gearbox identification](https://saabwisonline.com/9-5-9650/2011/4-transmission/automatic-transmission/technical-description/transmission-identification-information) | Original production register's `2.0T` alone does not prove the exact actual engine/case; another model's AF40 is not a donor approval |
| **2008 9-5 automatic radiator** | Existing [dated retail survey](research/us-retail-parts-supply-snapshot.md) recorded Nissens **32019620** at **$211.98 on Oct. 13, 2026** | This is neither current inventory nor an installed quote nor OEM VIN-approved fitment; a manual radiator must not be presumed equivalent |

**Safety:** WIS procedures assume appropriate mechanical condition and trained access. Never run an oil-starved, seized, hydrolocked or structurally unsafe nonrunner to generate fluid temperatures or transmission pressure readings. Never attempt transmission stall testing as a substitute for identifying a fault.

## How much job-planning research is present?

| Job packet | Matching source-derived U.S. groups | Same model-year as factory/supplier example |
| --- | ---: | ---: |
| Original 9-3 AF20/AF22 gearbox tag + removal tooling | 11 | 3 |
| Original 9-5 AF30 gearbox tag | 22 | 7 |
| Original 9-5 FA57 gearbox tag | 42 | 4 |
| Second-generation 9-3 FA57 gearbox/TCM | 28 | 2 |
| Second-generation 9-3 FA57 temperature/level | 28 | 2 |
| B284L 9-3 AF40 oil-level/pressure tooling | 6 | 2 |
| 2008 9-5 B235 mounts | 4 | 4 |
| 2011 9-5 Turbo4 factory engine/AF40 identity | 1 | 1 |
| 2008 9-5 automatic radiator source | 4 | 4 |

The groups overlap across job types. **All 110 of 110** source-derived U.S. production groups now have at least one job-planning *research lead*, including **11 original 9-3 four-speed groups** with a dedicated AF20/AF22 case-label and removal-tool packet. Their individual AF20 versus AF22 identity, parts interchange and actual repair cost remain unresolved. This is *not* a replacement for the already complete baseline engine/transmission/structural diagnostic coverage.

## Required proof before any parts purchase

1. Real original VIN, model year/market/body, original engine and *installed* gearbox full case tag and TCM ID. Keep full VIN/title and seller identity **out of the public repository**.
2. Actual fault established with year-specific diagnostic evidence: external component, control/programming fault, mechanical internal damage, or structural integrity problem. A source-matched scenario does not mean the fault happened.
3. OEM WebEPC VIN-filtered **part number and supersession**, converter/TCM or radiator connection variants, correct side/mounting and all one-use bolts, hoses, seals or coolant/ATF.
4. Required OEM tool IDs and safe access, whether Tech2/TIS or specialist programming is available, structurally sound lift points and professional help if equipment is beyond DIY.
5. **Dated total repair quote:** part availability and delivery, tax, core and shipping, small hardware/fluids, towing, tools, any outside labor and a hidden-damage allowance. Historical retailer displays cannot supply a future all-in price.
6. If internal engine bearings, complete gearsets/shafts or load-bearing body metal are substantially damaged, treat the job as a **separately budgeted complete powertrain replacement or walk-away** consistent with the project's no-internal-rebuild goal.

## Integrity and limits

Data: [nine job plans](../data/vehicle-catalogue/us-parts-tool-readiness.json), [110-group research crosswalk](../data/audits/us-parts-tool-readiness-coverage.json), and generator [`tools/build_us_parts_tool_readiness.py`](../tools/build_us_parts_tool_readiness.py). Run:

```sh
python3 tools/build_us_parts_tool_readiness.py --check
python3 -m unittest discover -s tests -v
python3 tools/validate.py
python3 tools/phase0_audit.py --check
```

Original manufacturer sources identify tools and procedures **for the cited model year**, not verified parts availability, exact donor fitment or comparative failure prevalence. Every VIN, donor-part approval, shop-equipment possession, verified all-in repair budget and reliability ranking is **unknown/unapproved**. Phase 0 Gate A partial, Gates B/C unmet; no Canadian catalogue or previously researched parts dataset is modified.
