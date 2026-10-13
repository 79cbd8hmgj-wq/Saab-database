# Official Saab WebEPC access and subframe part-identity conflicts

Research date: 2026-10-12. Structured dataset: [epc-provenance.json](../../data/datasets/epc-provenance.json). This source-validation pass records **10 sources, 12 findings, 2 restricted part entries, and 5 gaps**. Nothing in this research authorizes a physical subframe substitution or purchase.

## A factory-backed verification route exists, but its actual VIN results remain inaccessible

[Saab Parts / Hedin's official subscription page](https://saabparts.com/saab-subscription-services) identifies the **Saab WebEPC** as the manufacturer-backed catalogue with VIN/build-data filtering, illustrated assembly diagrams, applicability comments and Saab-approved substitutions for no-longer-serviced articles. Its **WebWIS** similarly advertises factory technical repair procedures, bulletins, electrical diagrams and service documentation.

These are **paid subscription products**; the public site lists day, month and year terms. No account, subscription or VIN-specific paid catalogue view was accessed for this research. Therefore:

- WebEPC's **published capabilities** may be stored as official factual metadata, but individual vehicle fitment and supersession claims must stay unverified until their actual entries are consulted.
- WIS repair procedures and parts catalogue supersession history answer different questions. A correct tightening torque does not establish that replacement frame A is interchangeable with original frame B.
- A retailer labeling a part “Genuine Saab” or including a manufacturer's logo does not transform its own cross-reference table into a factory-authored EPC result.
- Copyright, license terms and access restrictions must be respected; a future researcher should record citations and original summaries rather than redistributing entire catalogues or scraping restricted services without permission.

## Independent retailers agree on some number associations—but not their meaning

[The eSaabParts 32022623 product entry](https://www.esaabparts.com/saab/parts/32022623?ss=12825111) lists 12825111 and 12762720 among *superseded numbers*, and explicitly restricts the replacement to FWD **4D/5D** rather than CV. It cautions that some MY2005 vehicles may require a newer engine mount. A second retailer, [R&D Car Parts](https://www.rendcarparts.com/parts-for-saab-car/12762720-12825111-24401110-32022623/RD24401110), includes 12762720, 12825111, 24401110 and 32022623 as OE references for its complete-frame **merchant SKU RD24401110**. A third [aftermarket support-frame listing](https://plenty.parts/parts/klokkerholm/body/klokkerholm-5078004-support-frame-subframe-t3595659) groups 12762720 and 12825111.

This improves confidence that **12762720 is related in aftermarket cataloguing** to the later FWD 9-3 subframe family. But R&D lists an undirected group of references, whereas eSaabParts describes supersession. No manufacturer-authored item-by-item chain, changeover notice or fitted-car approval has yet been retrieved.

### Significant part-category collision: unprefixed 24401110

| Source | Meaning assigned to 24401110 |
| --- | --- |
| [eSaabParts 13247173](https://www.esaabparts.com/saab/parts/13247173) | **Old Saab part number of the front 4D/5D subframe bushing** (catalogue diagram item 2) |
| [Saab Parts Counter 13247173](https://www.saabpartscounter.com/oem-parts/saab-subframe-bushing-13247173) | Predecessor of **front subframe bushing** 13247173 |
| [Skandix 13247173](https://www.skandix.de/en/spare-parts/suspension-steering/axle-mounting/bushing/bushing-suspension-front-axle-subframe-front/1040617/) | Original-equipment reference for **front subframe bushing**, quantity two |
| [R&D complete-frame SKU RD24401110](https://www.rendcarparts.com/parts-for-saab-car/12762720-12825111-24401110-32022623/RD24401110) | The retailer's proprietary **RD-prefixed SKU** describes a whole subframe and includes bare **24401110** in its OE frame references |
| [R&D separate bushing SKU RD13247173A](https://www.rendcarparts.com/en/product-list/product-list?cat1=1&cat2=1381&cat3=1380&page=1) | The same retailer **also** lists bare 24401110 as a reference for an actual bushing |

**Current interpretation:** the more consistently supported unprefixed **Saab 24401110** identity is an earlier **front bushing**, while **RD24401110** is a **different, retailer-prefixed product SKU** that is being used for a complete subframe. R&D's bare 24401110 frame reference may be a catalogue-entry error, a mixed search/reference family, or a distinct historically reused identifier; we cannot choose among those explanations from the accessible evidence. **Do not assert 24401110 is a complete factory subframe or that a bushing number is a full-frame replacement.**

The ambiguity is isolated in the new dataset's separate `part:24401110` and `supplier_sku:RD24401110` records. Their evidence status remains **supplier_claim** and **needs_vehicle_verification**. Similar number overlap elsewhere must not be automatically combined by a future cross-reference tool.

## Factory service data is a distinct dependency

[MY2005 B207 engine mount service](https://saabwisonline.com/9-3-9440/2005/2-engine/4-cylinder-petrol/basic-engine/adjustment-replacement/engine-mounting-right) explicitly requires positioning of the engine pad and bracket to avoid unwanted contact. [MY2005 powertrain refitting](https://saabwisonline.com/9-3-9440/2005/2-engine/4-cylinder-petrol/basic-engine/adjustment-replacement/fitting-the-power-train) also specifies body alignment reference holes and centering jigs. Neither procedure alone provides a late-type 2005 retrofit mount parts kit for front subframe 32022623.

Until official WebEPC/WebWIS data is consulted, the remaining research blocks are:
1. Part category of **24401110** and reason for the R&D cross-category reference.
2. Exact manufacturer-revision/supersession order for **12762720 → 12825111 → 32022623**, or whatever direction and scope the original records actually give.
3. VIN/engine/gearbox/body-style applicability and **MY2005 engine-mount conversion hardware**.
4. Full **PI 08-01 (2007)** bulletin referenced by an early 9-3 frame listing.
5. Usage rights for any permitted future incorporation of official EPC/WIS information.

## Verification checklist for eventual authorized catalogue access

For a real or representative VIN, manually record separately:

| Field | Required observation |
| --- | --- |
| Vehicle identity | Model/platform, model year, **full VIN used for lookup**, market, build/chassis code |
| Configuration | Engine, gearbox, FWD/XWD, body style, equipment restrictions |
| Original part | Exact part number and **assembly category**, drawing position and build limit |
| Replacements | Each directed supersession and its conditions, not just a comma-separated reference list |
| Hardware dependencies | Engine mount/bracket, bushings, bolts, alignment tools, reuse/new-fastener rules |
| Publication | EPC revision/date, source locator and retrieval date; preserve copied content restrictions |
| Outstanding restrictions | Any unknown should block a claim of approved exact fitment |

Do not store arbitrary third-party VINs in a public repository. The complete factory fitment will remain a **research target**, rather than a completed fact, until the official entry has actually been examined and a compatible vehicle identified.
