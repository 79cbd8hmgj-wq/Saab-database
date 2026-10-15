# 2011 US Turbo4 FWD automatic: component and repair expansion

Research date: 2026-10-15. **Incomplete; no scoring, purchase approval or verified donor swap.**

This expands the [existing PR #82 dossier](../../data/engineering-dossiers/ng95-2011-purchase-reliability-20261015.json), retains its original facts/cases/supplier observations, and preserves the unmerged follow-up `94b2d4046445f539afd936580adf91811042c695`. Open PRs #80/#81 explicitly exclude 9650; their catalogue and scoring work is not target coverage.

Only MY2011 US Turbo4/Turbo4 Premium A20NFT/LHU FWD factory AF40 automatic production sedans are targets. Historical V6/XWD backlog text stays in the original document for provenance and is outside this active research. European/other GM applications are component leads only.

## What the identifiers establish

The register contains **141 curated component identities**, organized under 19 systems. A service number from a merchant diagram is not an original installed part number. Those fields, original supplier, revision, factory supersessions and VIN approval remain explicitly unknown where unsupported. BorgWarner is identified by the factory LHU turbo description; its exact assembly number/revision remains unknown. No complete as-built component inventory has been verified.

Existing evidence reused: `gmwp-part-001`, `hcdiag-issue-002`, `corrections-issue-011`, `corrections-issue-016`, `corrections-issue-020`, the six PR82 facts and eight investigation cases. New service findings are repair requirements, not new claims of common factory defects.

## Consequential factory findings

- **ng95-service-pump** — Pump service requires EN-44602 to retain the sprocket/chain. Incorrect handling can over-stress the timing drive and cause noise/damage. Balance timing errors can cause vibration. [pump-service](https://saabwisonline.com/9-5-9650/2011/2-engine/cooling-system/adjustment-replacement/water-pump-replacement-lhu-a20nft), [balance-timing](https://saabwisonline.com/9-5-9650/2011/2-engine/basic-engine-2-0-l-petrol/adjustment-replacement/balance-shaft-to-engine-timing-ldk-lhu)
- **ng95-service-chain** — Chain installation requires actuator locking, correct timed links, new actuator bolts and tensioner reset/release. A replacement-kit number alone is not a complete repair procedure. [chain-install](https://saabwisonline.com/9-5-9650/2011/2-engine/basic-engine-2-0-l-petrol/adjustment-replacement/camshaft-timing-chain-sprocket-and-tensioner-installation-ldk-lhu), [tensioner-service](https://saabwisonline.com/9-5-9650/2011/2-engine/basic-engine-2-0-l-petrol/adjustment-replacement/timing-chain-tensioner-replacement-lhu-a20nft)
- **ng95-service-head** — Head installation requires new main head bolts, specified sequence/angle tightening and no added gasket sealing material. This does not establish a revised valve metallurgy or guaranteed cure. [head-install](https://saabwisonline.com/9-5-9650/2011/2-engine/basic-engine-2-0-l-petrol/adjustment-replacement/cylinder-head-installation-ldk-lhu)
- **ng95-service-rail** — Rail removal discards the high-pressure pipe; installation uses a new pipe. Injector extraction may need specified tools. Bare-pump pricing excludes these possible job dependencies. [rail-service](https://saabwisonline.com/9-5-9650/2011/2-engine/engine-management-and-fuel-system-2-0-l-petrol/adjustment-replacement/fuel-injection-fuel-rail-assembly-replacement)
- **ng95-service-tcm** — TCM replacement calls for SPS, adaptation reset and selector learning in neutral. Stable power and the module-specific programming path matter; current 2026 tool/subscription/security access remains unverified. [tcm-service](https://saabwisonline.com/9-5-9650/2011/4-transmission/automatic-transmission/adjustment-replacement/transmission-control-module-replacement), [sps](https://saabwisonline.com/9-5-9650/2011/3-electrical-system/bus-and-diagnostics-communication/adjustment-replacement/service-programming-system-sps)
- **ng95-service-turbo** — Factory 2.0T description identifies oil feed/return and coolant cooling, and requires synthetic oil for high-temperature performance. It does not measure turbo failure frequency or prove an aftermarket oil-line upgrade. [turbo-description](https://saabwisonline.com/9-5-9650/2011/2-engine/engine-management-and-fuel-system-2-0-l-petrol/technical-description/turbocharger-system-description)

The inherited cold-valve advisory remains a manufacturer-described possible mechanism, not a measured failure rate. A truly cold compression/leakdown evaluation remains necessary. A new valve part number or a seller claiming a rebuilt head does not prove a material improvement or a healthy engine. The manufacturer PDF redirect could not be refreshed during this batch; the original saved provenance remains intact.

## Contradictions and scope controls

- **ng95-resolution-pump** — The specific LHU pump removal and balance timing procedures identify a chain-driven pump; the generic belt-driven wording does not govern this engine. Original contradictory text retained. [pump-service](https://saabwisonline.com/9-5-9650/2011/2-engine/cooling-system/adjustment-replacement/water-pump-replacement-lhu-a20nft), [balance-timing](https://saabwisonline.com/9-5-9650/2011/2-engine/basic-engine-2-0-l-petrol/adjustment-replacement/balance-shaft-to-engine-timing-ldk-lhu), [ng95-2011-src-08](https://saabwisonline.com/9-5-9650/2011/2-engine/cooling-system/technical-description/cooling-system-description-and-operation)
- **ng95-resolution-af40-table** — General-specification table explicitly names AF40-6 AWD/MXE; do not transfer its ratios, mass or torque limits to FWD. Use separate AW1 material table for fluid specification. [awd-table](https://saabwisonline.com/9-5-9650/2011/4-transmission/automatic-transmission/technical-data/transmission-general-specifications), [fluid](https://saabwisonline.com/9-5-9650/2011/4-transmission/automatic-transmission/technical-data/adhesives-fluids-lubricants-and-sealers)
- **ng95-resolution-airbag** — Initial 2016 report names 2010-2011 9-5; 2017 revision Vehicle 3 and defect text name 2006-2009. Do not assign 16V063 to all 2011 Turbo4s from the older report, or call any car recall-free. [recall-initial](https://static.nhtsa.gov/odi/rcl/2016/RCLRPT-16V063-5196.PDF), [recall-revised](https://static.nhtsa.gov/odi/rcl/2016/RCLRPT-16V063-3035.PDF)

The revised airbag filing changes the documented population; it does not prove that any actual car has no open campaigns. The live NHTSA model API request failed, so no complete recall/TSB census or zero-recall claim is made.

## Interchange assessments

| Assessment | Class | Finding / remaining boundary |
| --- | --- | --- |
| pump | D | Official Saab identifies 12630084 for A20NFT/NHT and kit contents; GM offers same service identifier. Reused finding is strengthened by LHU drive procedure. [official-pump](https://webshop-fi.saabparts.com/productdetail/saabparts/12630084), [gm-pump](https://parts.chevrolet.com/product/gm-genuine-parts-engine-water-pump-kit-12630084) |
| aw1 | C | AISIN lists ATF-0WS against GM AW-1/19256039. Factory 9650 material table requires AW1. Separate ATF-0T4/3309 recommendation must not be conflated. [aisin](https://aisinaftermarket.com/assets/blog/post/455de84b8e71bdff7c2da1dec1e069bb.pdf), [fluid](https://saabwisonline.com/9-5-9650/2011/4-transmission/automatic-transmission/technical-data/adhesives-fluids-lubricants-and-sealers) |
| valve | D | Same current numbered service offering; not proof of as-built supplier, revised wear resistance or a complete common cylinder head. [gm-valve](https://parts.gmparts.com/product/gm-genuine-parts-engine-intake-valve-55563529), [head](https://www.esaabparts.com/viewparts.php?searchpart=1&section=61938747) |
| 6t | E | Reject the inherited 6T40/6T45 controller/valve-body swap claim for the target Aisin AF40. Shared GM affiliation and six forward gears do not establish hardware or software equivalence. [ng95-2011-src-10](https://saabwisonline.com/9-5-9650/2011/4-transmission/automatic-transmission/technical-description/transmission-identification-information), [transmission](https://www.esaabparts.com/viewparts.php?searchpart=1&section=64167132), [tcm](https://www.esaabparts.com/viewparts.php?searchpart=1&section=624919812), [valvebody](https://www.esaabparts.com/viewparts.php?searchpart=1&section=641677851) |
| cap | D | 13502353 overlap retained; alleged GM successor is not established as Saab-approved. [radiator](https://www.esaabparts.com/viewparts.php?searchpart=1&section=61383145), [cap-gm](https://www.gmpartsgiant.com/parts/gm-cap-13502353.html) |
| arm | E | 13219164 is the REAR lower arm in the target FWD diagram. The inherited front-arm paragraph cannot establish a front replacement using this reference. Rejection is of that claimed mapping; independent APCA8564 fitment remains unassessed. [rear](https://www.esaabparts.com/viewparts.php?searchpart=1&section=671529702) |
| hub | D | Saab merchant diagrams use 13502785 at front and FWD rear and offer FAG under merchant SKU 102230. Original manufacturer SKU, ABS encoder interfaces and cross-brand donor identity remain unverified. [front-hub](https://www.esaabparts.com/viewparts.php?searchpart=1&section=673108713), [rear](https://www.esaabparts.com/viewparts.php?searchpart=1&section=671529702) |

A = identical original supplier/number/revision/interfaces; B = approved directed OEM supersession; C = named aftermarket manufacturer cross-reference; D = engineering/number candidate; E = rejected claimed mapping. **No A or B approval is established.** AISIN fluid is C, not proof that a Toyota-labelled bottle or any other Aisin transmission part fits.

## US supply observations

Exact-product public storefront responses were read on 2026-10-15 without placing orders. Stock and lead times are seller assertions. Destination shipping, tax, core charges and deliverability are unknown. The three earlier baseline observations are retained separately.

| Service / seller SKU | Description | Displayed USD | Seller availability |
| --- | --- | ---: | --- |
| [12630084](https://www.esaabparts.com/saab/parts/12630084) | Chain-driven coolant pump | $159.50 | In Stock: 10 Available |
| [12658478](https://www.esaabparts.com/saab/parts/12658478) | High-pressure direct-injection pump | $901.17 | Available from Sweden — estimated delivery 3–4 weeks |
| [12679099](https://www.esaabparts.com/saab/parts/12679099) | Intake camshaft actuator solenoid | $63.60 | In Stock: 3 Available |
| [12679100](https://www.esaabparts.com/saab/parts/12679100) | Exhaust camshaft actuator solenoid | $63.60 | In Stock: 6 Available |
| [12775748](https://www.esaabparts.com/saab/parts/12775748) | US LH halogen headlamp | $301.82 | Currently Unavailable |
| [13241729](https://www.esaabparts.com/saab/parts/13241729) | Automatic-transmission radiator | $613.70 | Currently Unavailable |
| [13312096](https://www.esaabparts.com/saab/parts/13312096) | Left transmission mount | $100.20 | In Stock: 7 Available |
| [13320976](https://www.esaabparts.com/saab/parts/13320976) | Taillamp bulb socket | $23.14 | Currently Unavailable |
| [13502353](https://www.esaabparts.com/saab/parts/13502353) | Expansion-tank cap | $13.89 | In Stock: 4 Available |
| [55574324](https://www.esaabparts.com/saab/parts/55574324) | AF40-II transmission controller | $1718.57 | In Stock: 1 Available |
| [90537379](https://www.esaabparts.com/saab/parts/90537379) | Pump-to-thermostat pipe O-ring | $3.98 | In Stock: 20+ Available |
| [93165147](https://www.esaabparts.com/saab/parts/93165147) | AW1 automatic-transmission fluid | $81.98 | In Stock: 20+ Available |
| [9995147](https://www.esaabparts.com/saab/parts/9995147) | AISIN AW1 fluid alternative | $14.99 | In Stock: 7 Available |
| [9997379](https://www.esaabparts.com/saab/parts/9997379) | Viton O-ring alternative | $4.49 | In Stock: 20+ Available |
| [12635447](https://www.esaabparts.com/saab/parts/12635447) | Primary timing service kit | $92.50 | In Stock: 20+ Available |

The current kit response is $92.50 versus an indexed $99.99; controller 55574324 now displays one available versus the cached backorder; exhaust solenoid 12679100 now displays $63.60 versus cached $53.12. Both observations remain in the data. A catalog price on an unavailable radiator/headlamp is not a purchasable restoration budget.

General [seller warranty terms](https://www.esaabparts.com/warranty_and_returns.php) say most eligible OEM parts receive 24 months/24,000 miles subject to conditions. Aftermarket parts have no warranty through the seller; manufacturer coverage needs verification. Socket 13320976 explicitly has no warranty. A/C warranty conditions require qualified installation, and compressor claims require additional component/service evidence. Verify exact eligibility and return exceptions before purchase.

## Repair economics and DIY boundaries

Subtotals below include only the observed line items. **They are not complete repair estimates or guaranteed minimum costs.** Every job separately retains unknown additional parts, fluids, shipping, tax, core, tools, programming, specialist labor, towing and contingency. No invented labor hours or installed quotes are provided.

| Repair | Observed parts subtotal | Practical decision |
| --- | ---: | --- |
| LHU coolant-pump replacement | $167.46 | External assembly service possible if engine and balance drive healthy; not an engine rebuild |
| Primary timing kit, without balance drive | $92.50 | Potential preventative/repair service before damage; confirmed bent valves or bearing damage exceeds simple chain replacement |
| DI high-pressure pump only | $901.17 | External pump is replaceable; no promise that pump alone fixes no-start |
| AF40-II controller only | $1718.57 | External electronic repair possible; confirmed slipping/contamination/internal damage still requires separate transmission decision |
| FWD automatic left transmission mount | $100.20 | External assembly; inspect all mounts and case/body anchors first |
| LHU intake and exhaust VVT solenoids | $127.20 | External components; fault code alone does not prove mechanical timing is healthy |
| 2.0T automatic radiator, presently unavailable listing | $613.70 | Replacement technically plausible but unavailable seller offer cannot fund an executable restoration plan |
| Confirmed cold intake-valve sealing damage | Unknown | STOP for confirmed repair outside project objective; a priced complete head and labor route is needed before reconsidering |
| Confirmed AF40-II internal failure | Unknown | Complete external assembly replacement may avoid rebuilding but delivered unit/labor/warranty unknown; economically unresolved |
| Missing US LH halogen headlamp | $301.82 | Current unavailable listing is a restoration blocker until an actual lawful deliverable alternative is quoted |

The coolant-pump subtotal includes the pump and two standard pipe O-rings, conditional on renewing them. Verify boxed contents to avoid duplicate purchases. The primary timing kit omits the balance-chain/tensioner and gears; new actuator bolts and other disturbed seals/fluids/tools are not priced. AW1 service quantity is still unknown; the AISIN container volume has not been verified, so no per-litre saving or total ATF-service price is asserted.

## Reliability improvements: evidence level

- **factory_supported_service_practice** — Use proper sprocket retention/timing tools, new specified one-time parts and stable programming power; address underlying diagnosis before fitting assemblies. [pump-service](https://saabwisonline.com/9-5-9650/2011/2-engine/cooling-system/adjustment-replacement/water-pump-replacement-lhu-a20nft), [chain-install](https://saabwisonline.com/9-5-9650/2011/2-engine/basic-engine-2-0-l-petrol/adjustment-replacement/camshaft-timing-chain-sprocket-and-tensioner-installation-ldk-lhu), [rail-service](https://saabwisonline.com/9-5-9650/2011/2-engine/engine-management-and-fuel-system-2-0-l-petrol/adjustment-replacement/fuel-injection-fuel-rail-assembly-replacement), [sps](https://saabwisonline.com/9-5-9650/2011/3-electrical-system/bus-and-diagnostics-communication/adjustment-replacement/service-programming-system-sps)
- **supplier_material_claim_only** — Evaluate ESAABKITS 9997379 Viton replacement for 90537379; compound grade, geometry and long-term coolant aging data remain needed. [pump](https://www.esaabparts.com/viewparts.php?searchpart=1&section=613839948)
- **supplier_design_claim_only** — Evaluate merchant 9998522 guide-bolt alternative only after torque, thread engagement, material and failure-mode review; a harder bolt is not automatically a validated improvement. [timing](https://www.esaabparts.com/viewparts.php?searchpart=1&section=6193588)
- **supplier_repair_candidate_only** — Seller offers LED/socket and third-brake-light repairs; verify US photometry, warning diagnostics, thermal behavior and lawful application before fitting. Seller short-life claim is not measured incidence. [lamps](https://www.esaabparts.com/viewparts.php?searchpart=1&section=624311872), [socket](https://www.esaabparts.com/saab/parts/13320976)

No candidate has independent durability-test evidence or a verified lifespan gain. No tuning, emissions defeat, safety-system bypass or generic preventive replacement interval is proposed.

## Component identities and option restrictions

All rows inherit the strict active research scope. Restrictions below are the source-specific conditions; a conditional catalogue row is not proof that its equipment was offered on either US target trim. Original installed numbers, revisions and official supersessions need factory/physical verification.

### 01. Engine core / head / valvetrain

| Service number | Component | Source restriction / evidence |
| --- | --- | --- |
| 12626382 | Cylinder head assembly with valves | 650 four-cylinder catalogue; exact original US VIN/options not verified [head](https://www.esaabparts.com/viewparts.php?searchpart=1&section=61938747) |
| 12589335 | Intake camshaft | 650 four-cylinder catalogue; exact original US VIN/options not verified [head](https://www.esaabparts.com/viewparts.php?searchpart=1&section=61938747) |
| 12629743 | Exhaust camshaft | 650 four-cylinder catalogue; exact original US VIN/options not verified [head](https://www.esaabparts.com/viewparts.php?searchpart=1&section=61938747) |
| 12597371 | Exhaust valve | 650 four-cylinder catalogue; exact original US VIN/options not verified [head](https://www.esaabparts.com/viewparts.php?searchpart=1&section=61938747) |
| 55563529 | Intake valve | 650 four-cylinder catalogue; exact original US VIN/options not verified [head](https://www.esaabparts.com/viewparts.php?searchpart=1&section=61938747), [gm-valve](https://parts.gmparts.com/product/gm-genuine-parts-engine-intake-valve-55563529) |
| 90537241 | Valve stem seal | 650 four-cylinder catalogue; exact original US VIN/options not verified [head](https://www.esaabparts.com/viewparts.php?searchpart=1&section=61938747) |
| 90537032 | Valve spring | 650 four-cylinder catalogue; exact original US VIN/options not verified [head](https://www.esaabparts.com/viewparts.php?searchpart=1&section=61938747) |
| 90537243 | Valve spring retainer | 650 four-cylinder catalogue; exact original US VIN/options not verified [head](https://www.esaabparts.com/viewparts.php?searchpart=1&section=61938747) |
| 90354648 | Valve keepers | 650 four-cylinder catalogue; exact original US VIN/options not verified [head](https://www.esaabparts.com/viewparts.php?searchpart=1&section=61938747) |
| 12656486 | Rocker arm | 650 four-cylinder catalogue; exact original US VIN/options not verified [head](https://www.esaabparts.com/viewparts.php?searchpart=1&section=61938747) |
| 9194698 | Hydraulic valve lifter | 650 four-cylinder catalogue; exact original US VIN/options not verified [head](https://www.esaabparts.com/viewparts.php?searchpart=1&section=61938747) |
| 12589346 | Cylinder-head gasket | 650 four-cylinder catalogue; exact original US VIN/options not verified [head](https://www.esaabparts.com/viewparts.php?searchpart=1&section=61938747) |
| 90537691 | Main cylinder-head bolt | 650 four-cylinder catalogue; exact original US VIN/options not verified [head](https://www.esaabparts.com/viewparts.php?searchpart=1&section=61938747) |
| 12605217 | Camshaft cover | 650 four-cylinder catalogue; exact original US VIN/options not verified [head](https://www.esaabparts.com/viewparts.php?searchpart=1&section=61938747) |
| 12605173 | Camshaft-cover seal | 650 four-cylinder catalogue; exact original US VIN/options not verified [head](https://www.esaabparts.com/viewparts.php?searchpart=1&section=61938747) |
| 12679099 | Intake camshaft actuator solenoid | 650 four-cylinder catalogue; exact original US VIN/options not verified [head](https://www.esaabparts.com/viewparts.php?searchpart=1&section=61938747) |
| 12679100 | Exhaust camshaft actuator solenoid | 650 four-cylinder catalogue; exact original US VIN/options not verified [head](https://www.esaabparts.com/viewparts.php?searchpart=1&section=61938747) |

**Still required:** block casting and assembly; pistons and rings; crankshaft and bearings; connecting rods; head as-built number/material; valve material and revisions.

### 02. Timing / balance shafts

| Service number | Component | Source restriction / evidence |
| --- | --- | --- |
| 24461834 | Primary timing chain | 650 four-cylinder catalogue; exact original US VIN/options not verified [timing](https://www.esaabparts.com/viewparts.php?searchpart=1&section=6193588) |
| 13104978 | Primary chain guide | 650 four-cylinder catalogue; exact original US VIN/options not verified [timing](https://www.esaabparts.com/viewparts.php?searchpart=1&section=6193588) |
| 24449448 | Primary chain guide | 650 four-cylinder catalogue; exact original US VIN/options not verified [timing](https://www.esaabparts.com/viewparts.php?searchpart=1&section=6193588) |
| 12588387 | Upper primary chain guide | 650 four-cylinder catalogue; exact original US VIN/options not verified [timing](https://www.esaabparts.com/viewparts.php?searchpart=1&section=6193588) |
| 12608580 | Primary timing tensioner | 650 four-cylinder catalogue; exact original US VIN/options not verified [timing](https://www.esaabparts.com/viewparts.php?searchpart=1&section=6193588) |
| 12577163 | Timing-chain oil nozzle | 650 four-cylinder catalogue; exact original US VIN/options not verified [timing](https://www.esaabparts.com/viewparts.php?searchpart=1&section=6193588) |
| 11588522 | Chain-guide screw | 650 four-cylinder catalogue; exact original US VIN/options not verified [timing](https://www.esaabparts.com/viewparts.php?searchpart=1&section=6193588) |
| 11516425 | Chain-guide screw | 650 four-cylinder catalogue; exact original US VIN/options not verified [timing](https://www.esaabparts.com/viewparts.php?searchpart=1&section=6193588) |
| 11518828 | Upper-guide screw | 650 four-cylinder catalogue; exact original US VIN/options not verified [timing](https://www.esaabparts.com/viewparts.php?searchpart=1&section=6193588) |
| 12635427 | Balance-shaft drive chain | 650 four-cylinder catalogue; exact original US VIN/options not verified [timing](https://www.esaabparts.com/viewparts.php?searchpart=1&section=6193588) |
| 90537300 | Balance-chain tensioner | 650 four-cylinder catalogue; exact original US VIN/options not verified [timing](https://www.esaabparts.com/viewparts.php?searchpart=1&section=6193588) |
| 90537369 | Lower left balance-chain guide | 650 four-cylinder catalogue; exact original US VIN/options not verified [timing](https://www.esaabparts.com/viewparts.php?searchpart=1&section=6193588) |
| 90537299 | Right balance-chain guide | 650 four-cylinder catalogue; exact original US VIN/options not verified [timing](https://www.esaabparts.com/viewparts.php?searchpart=1&section=6193588) |
| 90537336 | Upper balance-chain guide | 650 four-cylinder catalogue; exact original US VIN/options not verified [timing](https://www.esaabparts.com/viewparts.php?searchpart=1&section=6193588) |
| 24424758 | Lower primary-chain gear | 650 four-cylinder catalogue; exact original US VIN/options not verified [timing](https://www.esaabparts.com/viewparts.php?searchpart=1&section=6193588) |
| 24424855 | Crankshaft drive key | 650 four-cylinder catalogue; exact original US VIN/options not verified [timing](https://www.esaabparts.com/viewparts.php?searchpart=1&section=6193588) |
| 12642713 | Balance drive gear | 650 four-cylinder catalogue; exact original US VIN/options not verified [timing](https://www.esaabparts.com/viewparts.php?searchpart=1&section=6193588) |
| 12578515 | Intake camshaft gear | 650 four-cylinder catalogue; exact original US VIN/options not verified [timing](https://www.esaabparts.com/viewparts.php?searchpart=1&section=6193588) |
| 12621505 | Exhaust camshaft gear | 650 four-cylinder catalogue; exact original US VIN/options not verified [timing](https://www.esaabparts.com/viewparts.php?searchpart=1&section=6193588) |
| 11588844 | Camshaft gear bolts | 650 four-cylinder catalogue; exact original US VIN/options not verified [timing](https://www.esaabparts.com/viewparts.php?searchpart=1&section=6193588) |
| 12587216 | Left balance shaft | 650 four-cylinder catalogue; exact original US VIN/options not verified [timing](https://www.esaabparts.com/viewparts.php?searchpart=1&section=6193588) |
| 12587215 | Right balance shaft | 650 four-cylinder catalogue; exact original US VIN/options not verified [timing](https://www.esaabparts.com/viewparts.php?searchpart=1&section=6193588) |
| 12581395 | Balance shaft bearing | 650 four-cylinder catalogue; exact original US VIN/options not verified [timing](https://www.esaabparts.com/viewparts.php?searchpart=1&section=6193588) |
| 55561057 | Timing-guide access plug | 650 four-cylinder catalogue; exact original US VIN/options not verified [timing](https://www.esaabparts.com/viewparts.php?searchpart=1&section=6193588) |
| 12635447 | Primary timing service kit | 650 four-cylinder catalogue; exact original US VIN/options not verified [kit](https://www.esaabparts.com/saab/parts/12635447) |

**Still required:** factory revision chronology; balance-bearing complete application; wear measurements and service limits.

### 03. Oil / PCV / oil cooling

| Service number | Component | Source restriction / evidence |
| --- | --- | --- |
| 12637040 | Front cover / oil pump housing | 650 four-cylinder catalogue; exact original US VIN/options not verified [oil-pump](https://www.esaabparts.com/viewparts.php?searchpart=1&section=61931828) |
| 24434093 | Oil pump kit | 650 four-cylinder catalogue; exact original US VIN/options not verified [oil-pump](https://www.esaabparts.com/viewparts.php?searchpart=1&section=61931828) |
| 25193519 | Front crankshaft seal | 650 four-cylinder catalogue; exact original US VIN/options not verified [oil-pump](https://www.esaabparts.com/viewparts.php?searchpart=1&section=61931828) |
| 24435052 | Timing-cover gasket | 650 four-cylinder catalogue; exact original US VIN/options not verified [oil-pump](https://www.esaabparts.com/viewparts.php?searchpart=1&section=61931828) |
| 12606566 | PCV hose | 650 four-cylinder catalogue; exact original US VIN/options not verified [head](https://www.esaabparts.com/viewparts.php?searchpart=1&section=61938747) |
| 12625448 | PCV pipe | 650 four-cylinder catalogue; exact original US VIN/options not verified [head](https://www.esaabparts.com/viewparts.php?searchpart=1&section=61938747) |

**Still required:** pickup and strainer; oil filter and housing; oil cooler and seals; oil-pressure sensor; PCV integrated passages/check valves.

### 04. Turbo / intake / charge air

| Service number | Component | Source restriction / evidence |
| --- | --- | --- |
| 12654315 | Turbocharger oil-feed pipe | A20NFT; distinguish A20NHT return plumbing [turbo](https://www.esaabparts.com/viewparts.php?searchpart=1&section=611817732) |
| 12611119 | Turbo oil-feed seal | A20NFT; distinguish A20NHT return plumbing [turbo](https://www.esaabparts.com/viewparts.php?searchpart=1&section=611817732) |
| 12626643 | Turbo oil-return hose | A20NFT; distinguish A20NHT return plumbing [turbo](https://www.esaabparts.com/viewparts.php?searchpart=1&section=611817732) |
| 12589435 | Turbo oil-return gasket | A20NFT; distinguish A20NHT return plumbing [turbo](https://www.esaabparts.com/viewparts.php?searchpart=1&section=611817732) |
| 12612816 | Turbo oil-return O-ring | A20NFT; distinguish A20NHT return plumbing [turbo](https://www.esaabparts.com/viewparts.php?searchpart=1&section=611817732) |
| 12626640 | Turbo coolant return pipe | A20NFT; distinguish A20NHT return plumbing [turbo](https://www.esaabparts.com/viewparts.php?searchpart=1&section=611817732) |
| Unknown | Original-design dual-scroll turbocharger assembly | Factory 2011 9650 2.0L petrol/LHU description; fitted number/revision and donor application unverified [turbo-description](https://saabwisonline.com/9-5-9650/2011/2-engine/engine-management-and-fuel-system-2-0-l-petrol/technical-description/turbocharger-system-description) |

**Still required:** turbo complete original ID and maker; wastegate and bypass calibration; intercooler; boost ducts/clamps; air filter and MAF/MAP.

### 05. Fuel / DI / EVAP / emissions

| Service number | Component | Source restriction / evidence |
| --- | --- | --- |
| 12658478 | High-pressure direct-injection pump | 650 four-cylinder catalogue; exact original US VIN/options not verified [injection](https://www.esaabparts.com/viewparts.php?searchpart=1&section=614174632) |
| 12590679 | High-pressure pump tappet | 650 four-cylinder catalogue; exact original US VIN/options not verified [injection](https://www.esaabparts.com/viewparts.php?searchpart=1&section=614174632) |
| 12615401 | High-pressure pump-to-rail pipe | 650 four-cylinder catalogue; exact original US VIN/options not verified [injection](https://www.esaabparts.com/viewparts.php?searchpart=1&section=614174632) |
| 12621643 | Fuel rail assembly | 650 four-cylinder catalogue; exact original US VIN/options not verified [injection](https://www.esaabparts.com/viewparts.php?searchpart=1&section=614174632) |
| 12636111 | Direct injector | 650 four-cylinder catalogue; exact original US VIN/options not verified [injection](https://www.esaabparts.com/viewparts.php?searchpart=1&section=614174632) |
| 12633374 | Injector service kit | 650 four-cylinder catalogue; exact original US VIN/options not verified [injection](https://www.esaabparts.com/viewparts.php?searchpart=1&section=614174632) |
| 13578363 | In-tank fuel pump | FWD; CA/MX/US emissions row; original emissions label still required [tank](https://www.esaabparts.com/viewparts.php?searchpart=1&section=614175493) |
| 20791901 | Fuel-pump flow control module | 2011 A20NFT fuel-flow row; programming verification required [tank](https://www.esaabparts.com/viewparts.php?searchpart=1&section=614175493) |
| 13238457 | EVAP canister | FWD; US/CA/MX emissions row [tank](https://www.esaabparts.com/viewparts.php?searchpart=1&section=614175493) |
| 22865590 | EVAP canister solenoid | Included in applicable canister diagram; emissions label required [tank](https://www.esaabparts.com/viewparts.php?searchpart=1&section=614175493) |
| 22682111 | Fuel-pump seal | FWD pump service; verify package contents [tank](https://www.esaabparts.com/viewparts.php?searchpart=1&section=614175493) |

**Still required:** pump and injector original suppliers; injector seal installation; fuel-pressure sensor calibration; purge plumbing; US certification-specific catalyst and oxygen sensors.

### 06. Cooling

| Service number | Component | Source restriction / evidence |
| --- | --- | --- |
| 12630084 | Chain-driven coolant pump | 650 four-cylinder catalogue; exact original US VIN/options not verified [pump](https://www.esaabparts.com/viewparts.php?searchpart=1&section=613839948), [official-pump](https://webshop-fi.saabparts.com/productdetail/saabparts/12630084), [gm-pump](https://parts.chevrolet.com/product/gm-genuine-parts-engine-water-pump-kit-12630084) |
| 90537379 | Pump-to-thermostat pipe O-ring | 650 four-cylinder catalogue; exact original US VIN/options not verified [pump](https://www.esaabparts.com/viewparts.php?searchpart=1&section=613839948) |
| 12592401 | Pump outlet pipe | 650 four-cylinder catalogue; exact original US VIN/options not verified [pump](https://www.esaabparts.com/viewparts.php?searchpart=1&section=613839948) |
| 12605853 | Thermostat housing | 650 four-cylinder catalogue; exact original US VIN/options not verified [pump](https://www.esaabparts.com/viewparts.php?searchpart=1&section=613839948) |
| 13241729 | Automatic-transmission radiator | 2.0T AT row; manual radiator 13241728 is not approved [radiator](https://www.esaabparts.com/viewparts.php?searchpart=1&section=61383145) |
| 22953219 | Coolant expansion tank | 2.0T; predecessor 13220123 seller relationship [radiator](https://www.esaabparts.com/viewparts.php?searchpart=1&section=61383145) |
| 13271444 | Coolant-level sensor | Listed as included with expansion tank [radiator](https://www.esaabparts.com/viewparts.php?searchpart=1&section=61383145) |
| 13502353 | Expansion-tank cap | 2.0T diagram; pressure specification and GM successor unverified [radiator](https://www.esaabparts.com/viewparts.php?searchpart=1&section=61383145) |
| 13220131 | Radiator inlet hose | 2.0T; check physical fittings [radiator](https://www.esaabparts.com/viewparts.php?searchpart=1&section=61383145) |
| 13220126 | Radiator outlet hose | 2.0T; check physical fittings [radiator](https://www.esaabparts.com/viewparts.php?searchpart=1&section=61383145) |

**Still required:** thermostat exact LHU temperature specification; fan motors/relays/resistor; all coolant hoses; build-cutoff lower radiator supports; official cap rating.

### 07. AF40 automatic / controls / cooling

| Service number | Component | Source restriction / evidence |
| --- | --- | --- |
| 55570649 | Complete AF40-II automatic | 2011 A20NFT; AF40-6 II without XWD [transmission](https://www.esaabparts.com/viewparts.php?searchpart=1&section=64167132) |
| 55577380 | AF40-II torque converter | 2011 A20NFT AF40-6 II [converter](https://www.esaabparts.com/viewparts.php?searchpart=1&section=641671335) |
| 55574324 | AF40-II transmission controller | 2011 AF40-6 II; not interchangeable with AF40 first generation by assumption [tcm](https://www.esaabparts.com/viewparts.php?searchpart=1&section=624919812) |
| 55577385 | AF40-II valve housing | 2011 AF40-6 II [valvebody](https://www.esaabparts.com/viewparts.php?searchpart=1&section=641677851) |
| 55578637 | AF40-II solenoid | 2011 AF40-6 II; position/type mapping not yet verified [valvebody](https://www.esaabparts.com/viewparts.php?searchpart=1&section=641677851) |
| 55578638 | AF40-II solenoid | 2011 AF40-6 II; position/type mapping not yet verified [valvebody](https://www.esaabparts.com/viewparts.php?searchpart=1&section=641677851) |
| 55577386 | AF40-II internal harness | 2011 AF40-6 II [valvebody](https://www.esaabparts.com/viewparts.php?searchpart=1&section=641677851) |
| 22953353 | Automatic oil-cooler line | Automatic; seller successor of 13220158 [cooler-lines](https://www.esaabparts.com/viewparts.php?searchpart=1&section=641679837) |
| 93183012 | Automatic cooler sealing ring | Automatic; seller successor of 24221233 [cooler-lines](https://www.esaabparts.com/viewparts.php?searchpart=1&section=641679837) |

**Still required:** AF40-II fitted case/code and differential; FWD ratios/final drive; clutch/internal mechanical coverage; cooler contamination diagnosis; fluid service quantity; replacement adaptation details.

### 08. Axles / CV / powertrain mounts

| Service number | Component | Source restriction / evidence |
| --- | --- | --- |
| 22796269 | Front driveshaft assembly | 2011 A20NFT automatic, STANDARD front strut [axles](https://www.esaabparts.com/viewparts.php?searchpart=1&section=643828207) |
| 13292197 | Front driveshaft assembly | 2011 A20NFT automatic, PERFORMANCE front strut; eligible target option not established [axles](https://www.esaabparts.com/viewparts.php?searchpart=1&section=643828207) |
| 13233952 | Intermediate shaft | 2.0T automatic; confirm fitted shaft and FWD housing [axles](https://www.esaabparts.com/viewparts.php?searchpart=1&section=643828207) |
| 09186677 | Automatic output sealing ring | Automatic without XWD; leading zero preserved [axles](https://www.esaabparts.com/viewparts.php?searchpart=1&section=643828207) |
| 13227769 | Front engine mount | 2011 2.0T automatic FWD; XWD mount 13322172 is excluded [mounts](https://www.esaabparts.com/viewparts.php?searchpart=1&section=611809163) |
| 22744337 | Right engine mount | 2011 2.0T automatic FWD; XWD mount 13322172 is excluded [mounts](https://www.esaabparts.com/viewparts.php?searchpart=1&section=611809163) |
| 13312096 | Left transmission mount | 2011 2.0T automatic FWD; XWD mount 13322172 is excluded [mounts](https://www.esaabparts.com/viewparts.php?searchpart=1&section=611809163) |
| 13228303 | Rear engine mount | 2011 2.0T automatic FWD; XWD mount 13322172 is excluded [mounts](https://www.esaabparts.com/viewparts.php?searchpart=1&section=611809163) |

**Still required:** actual standard front suspension verification; CV boot and joint complete kit contents; intermediate-bearing service; mount supplier and fastener renewal.

### 09. Steering / suspension / subframes / hubs

| Service number | Component | Source restriction / evidence |
| --- | --- | --- |
| 13309277 | Hydraulic power-steering pump | 650 four-cylinder catalogue; exact original US VIN/options not verified [steering](https://www.esaabparts.com/viewparts.php?searchpart=1&section=664542998) |
| 22755964 | 2011 power-steering reservoir | 650 four-cylinder catalogue; exact original US VIN/options not verified [steering](https://www.esaabparts.com/viewparts.php?searchpart=1&section=664542998) |
| 22755965 | 2011 steering reservoir cap | 650 four-cylinder catalogue; exact original US VIN/options not verified [steering](https://www.esaabparts.com/viewparts.php?searchpart=1&section=664542998) |
| 13311248 | Steering pressure hose | 650 four-cylinder catalogue; exact original US VIN/options not verified [steering](https://www.esaabparts.com/viewparts.php?searchpart=1&section=664542998) |
| 13336906 | FWD rear suspension support | FWD rear suspension; never relabel 13219164 a front arm [rear](https://www.esaabparts.com/viewparts.php?searchpart=1&section=671529702) |
| 13219164 | Rear lower control arm | FWD rear suspension; never relabel 13219164 a front arm [rear](https://www.esaabparts.com/viewparts.php?searchpart=1&section=671529702) |
| 13219171 | Rear additional lower control arm | FWD rear suspension; never relabel 13219164 a front arm [rear](https://www.esaabparts.com/viewparts.php?searchpart=1&section=671529702) |
| 13502785 | Wheel hub/bearing assembly | Merchant front hub and FWD rear hub diagrams use same number; installed ABS interface and original factory application unverified [front-hub](https://www.esaabparts.com/viewparts.php?searchpart=1&section=673108713), [rear](https://www.esaabparts.com/viewparts.php?searchpart=1&section=671529702) |

**Still required:** steering rack option; front subframe and body mount locations; springs/dampers/bushings per chassis code; FWD rear alignment specifications; corrosion repair boundaries.

### 10. Brakes / ABS / stability / parking brake

| Service number | Component | Source restriction / evidence |
| --- | --- | --- |
| 20997680 | ABS hydraulic modulator | 2011 A20NFT; WITHOUT stop/go adaptive cruise [abs](https://www.esaabparts.com/viewparts.php?searchpart=1&section=654968142) |
| 22758235 | ABS electronic controller | 2011 WITHOUT stop/go adaptive cruise [abs](https://www.esaabparts.com/viewparts.php?searchpart=1&section=654968142) |
| 13237753 | Front brake-pad kit | CA/MX/US 17-inch brake noise/dust performance row; verify option code and rotor [front-brake](https://www.esaabparts.com/viewparts.php?searchpart=1&section=653264747) |
| 13579150 | Front brake rotor | AG brake code, 321 mm; target option not established [front-brake](https://www.esaabparts.com/viewparts.php?searchpart=1&section=653264747) |
| 20978663 | Rear brake-pad kit | 2011 CA/MX/US 17-inch noise/dust performance row [rear-brake](https://www.esaabparts.com/viewparts.php?searchpart=1&section=65326285) |
| 13502199 | Rear brake rotor | BE code; verify caliper and option [rear-brake](https://www.esaabparts.com/viewparts.php?searchpart=1&section=65326285) |
| 13505410 | Electric parking-brake unit | 2011 row; module-specific setup required [epb](https://www.esaabparts.com/viewparts.php?searchpart=1&section=653264969) |
| 20918018 | Parking-brake cable | 4-link rear suspension; verify target configuration [epb](https://www.esaabparts.com/viewparts.php?searchpart=1&section=653264969) |

**Still required:** as-built brake code; all hydraulic lines and hoses; master cylinder/booster/vacuum; ABS hydraulic bleed/setup; parking brake service-release/relearn.

### 11. Starting / charging / battery / distribution

| Service number | Component | Source restriction / evidence |
| --- | --- | --- |
| 13502591 | Automatic alternator 120A | AT 120 A; actual fitted amperage/pulley/charging control required [alternator](https://www.esaabparts.com/viewparts.php?searchpart=1&section=623179216) |
| 13502590 | Automatic alternator 140A | AT 140 A; not an assumed upgrade from 120 A [alternator](https://www.esaabparts.com/viewparts.php?searchpart=1&section=623179216) |

**Still required:** starter exact number and supplier; battery current sensor and battery spec; fuse/relay centers; all primary grounds; alternator original rating/protocol.

### 12. ECM / immobilizer / networks

| Service number | Component | Source restriction / evidence |
| --- | --- | --- |
| 12651993 | A20NFT engine controller service successor | Retailer maps 12650256 to 12651993; software/emissions/VIN dependencies unresolved [ecm](https://www.esaabparts.com/viewparts.php?searchpart=1&section=624917385) |

**Still required:** BCM and immobilizer original labels; CAN topology/termination; LHU ECM calibration/security; 2026 authorized programming service availability.

### 13. Body controls / harnesses / sensors

| Service number | Component | Source restriction / evidence |
| --- | --- | --- |
| 13578646 | Keyless entry module successor | 2011 keyless module; retailer predecessor 13577129 [security](https://www.esaabparts.com/viewparts.php?searchpart=1&section=62548443) |
| 25849809 | 2011 315MHz transmitter without remote start | US frequency row; no remote start; pairing required [security](https://www.esaabparts.com/viewparts.php?searchpart=1&section=62548443) |
| 25849810 | 2011 315MHz transmitter with remote start | US frequency row; remote start; pairing required [security](https://www.esaabparts.com/viewparts.php?searchpart=1&section=62548443) |

**Still required:** body harness complete equipment matrix; BCM number; keyless module vendor and pairing restrictions; door/latch/window controls; water-ingress paths.

### 14. HVAC / defrost

| Service number | Component | Source restriction / evidence |
| --- | --- | --- |
| 13262836 | 2.0T air-conditioning compressor | 650 four-cylinder catalogue; exact original US VIN/options not verified [ac](https://www.esaabparts.com/viewparts.php?searchpart=1&section=610495231) |
| 13263279 | HVAC blower motor | 650 four-cylinder catalogue; exact original US VIN/options not verified [hvac](https://www.esaabparts.com/viewparts.php?searchpart=1&section=610409347) |
| 13503201 | Blower motor regulator | 650 four-cylinder catalogue; exact original US VIN/options not verified [hvac](https://www.esaabparts.com/viewparts.php?searchpart=1&section=610409347) |
| 13263329 | Heater heat-exchanger kit | 650 four-cylinder catalogue; exact original US VIN/options not verified [hvac](https://www.esaabparts.com/viewparts.php?searchpart=1&section=610409347) |
| 13339087 | A/C evaporator kit | 650 four-cylinder catalogue; exact original US VIN/options not verified [hvac](https://www.esaabparts.com/viewparts.php?searchpart=1&section=610409347) |

**Still required:** condenser and hoses; refrigerant/oil exact charges; ACC panel/module options; actuator calibration; labor and dash-removal boundaries.

### 15. Restraints / safety

| Service number | Component | Source restriction / evidence |
| --- | --- | --- |
| 13578321 | 2011 restraint sensing/diagnostic module | Without rear-seat safety package; verify original option [srs](https://www.esaabparts.com/viewparts.php?searchpart=1&section=692477903) |
| 13578323 | 2011 restraint sensing/diagnostic module | With rear-seat safety package; target equipment unverified [srs](https://www.esaabparts.com/viewparts.php?searchpart=1&section=692477903) |
| 13502340 | Front impact sensor | US/CA/MX row; matching restraint calibration required [srs](https://www.esaabparts.com/viewparts.php?searchpart=1&section=692477903) |
| 12821592 | Passenger-presence repair kit | RH comfort seat with heater/PPS; exact seat required [pps](https://www.esaabparts.com/viewparts.php?searchpart=1&section=69249036) |
| 12825768 | 2011 passenger-presence repair kit | Sport/heated seat without ventilation or manual cushion extension; equipment unverified [pps](https://www.esaabparts.com/viewparts.php?searchpart=1&section=69249036) |

**Still required:** seatbelt and pretensioner numbers; original airbag maker/label; current VIN-specific campaigns; PPS calibration; repair rules after crash or water damage.

### 16. Exterior lighting

| Service number | Component | Source restriction / evidence |
| --- | --- | --- |
| 12776357 | Left US outer taillamp | US/CA/MX left [lamps](https://www.esaabparts.com/viewparts.php?searchpart=1&section=624311872) |
| 12776358 | Right US outer taillamp | US/CA/MX right [lamps](https://www.esaabparts.com/viewparts.php?searchpart=1&section=624311872) |
| 13320976 | Taillamp bulb socket | Seller explicitly no warranty; design claim not factory finding [lamps](https://www.esaabparts.com/viewparts.php?searchpart=1&section=624311872) |
| 32022126 | High-mounted stop lamp | Sedan; repair kit separately offered [lamps](https://www.esaabparts.com/viewparts.php?searchpart=1&section=624311872) |

**Still required:** US halogen versus xenon eligibility; adaptive lamp module/setup; Saab-specific lamp repair/donor supply; US-compliant replacement photometry.

### 17. Body / structure / glass / seals

| Service number | Component | Source restriction / evidence |
| --- | --- | --- |
| 12827530 | Rain-sensor windshield | No HUD, no traffic camera [glass](https://www.esaabparts.com/viewparts.php?searchpart=1&section=683802931) |
| 12827531 | Rain-sensor windshield | No HUD, with traffic camera; original US option verification outstanding [glass](https://www.esaabparts.com/viewparts.php?searchpart=1&section=683802931) |
| 12827533 | Rain-sensor windshield | HUD, no traffic camera [glass](https://www.esaabparts.com/viewparts.php?searchpart=1&section=683802931) |
| 12827534 | Rain-sensor windshield | HUD and traffic camera; original US option verification outstanding [glass](https://www.esaabparts.com/viewparts.php?searchpart=1&section=683802931) |
| 12776403 | Front door seal | 650 four-cylinder catalogue; exact original US VIN/options not verified [seals](https://www.esaabparts.com/viewparts.php?searchpart=1&section=68855355) |
| 12776402 | Rear door seal | 650 four-cylinder catalogue; exact original US VIN/options not verified [seals](https://www.esaabparts.com/viewparts.php?searchpart=1&section=68855355) |

**Still required:** bumper original trim/options; structural panels and joining/protection rules; windshield actual US options and supply; door/trunk seals and water testing.

### 18. Interior / instruments / infotainment

| Service number | Component | Source restriction / evidence |
| --- | --- | --- |
| 12825271 | 2011 mph monochrome instrument cluster | 2011 A20NFT mph; programming/odometer/configuration not approved [instruments](https://www.esaabparts.com/viewparts.php?searchpart=1&section=691393985) |
| 12827040 | 2011 mph color instrument cluster | 2011 A20NFT mph; no assumed plug-and-play upgrade [instruments](https://www.esaabparts.com/viewparts.php?searchpart=1&section=691393985) |

**Still required:** radio/navigation/amplifier original numbers; all interior controls; cluster VIN/odometer and security rules; display repair and parts supply.

### 19. Consumables / fasteners / tools

| Service number | Component | Source restriction / evidence |
| --- | --- | --- |
| 12638824 | 2011 ignition coil | 650 four-cylinder catalogue; exact original US VIN/options not verified [coil](https://www.esaabparts.com/viewparts.php?searchpart=1&section=622589802) |
| 12620540 | Spark plug | 650 four-cylinder catalogue; exact original US VIN/options not verified [coil](https://www.esaabparts.com/viewparts.php?searchpart=1&section=622589802) |
| 13271191 | Activated-carbon cabin filter | 650 four-cylinder catalogue; exact original US VIN/options not verified [hvac](https://www.esaabparts.com/viewparts.php?searchpart=1&section=610409347) |
| 93165147 | AW1 automatic-transmission fluid | AF40; retailer 1 L container; no Dexron VI or 3309 substitution approval [fluid](https://saabwisonline.com/9-5-9650/2011/4-transmission/automatic-transmission/technical-data/adhesives-fluids-lubricants-and-sealers), [aw1-listing](https://www.esaabparts.com/saab/parts/93165147) |

**Still required:** engine oil and full filter/fluids schedule; factory ATF quantity by job; bolt renewal and sealant matrix; tool purchase/rental prices; lift/support and torque data.

## Separate coverage states

| Area | State | Basis |
| --- | --- | --- |
| component_inventory_completeness | partial | 19-system required inventory plus curated service identities; block internals, harnesses and many option assemblies remain open |
| factory_identification_confidence | partial | LHU factory architecture/procedures and official current pump SKU; no as-built VIN-filtered catalogue for a real car |
| failure_mechanism_research | partial | Existing cold-valve advisory reused; service checks do not prove fleet prevalence |
| original_supplier_identification | partial | BorgWarner named by 2.0L factory description; most tier-one suppliers and fitted labels unknown |
| factory_supersession_verification | unresolved | Directed retailer claims retained; no target VIN-directed official supersession chain retrieved |
| cross_brand_interchange_validation | partial | Official common service SKU and AISIN fluid cross-reference; no category A/B donor approval |
| current_US_replacement_availability | partial | 15 exact-product displayed observations; no physical stock/delivery confirmations |
| repair_procedure_coverage | partial | Pump/timing/head/rail/TCM/hydraulic service evidence; complete job procedure trees still needed |
| DIY_feasibility | partial | Tool/dependency-aware project judgments; no actual vehicle measurements or published labor times |
| actual_repair_cost_evidence | partial | Observed part subtotals only; no verified installed quotes |
| remaining_safety_critical_gaps | unresolved | Structural mounts, braking/ABS option/bleed, restraint/campaign scope and immobilizer support require vehicle and primary evidence |

No system is claimed complete and no search is marked exhausted. Counts measure saved records, not the proportion of the vehicle verified. No failure-frequency denominator is available.

## Prioritized remaining work

1. **Original US VIN/build/options and all fitted labels** — Factory US MY2011 VIN bulletin plus actual title/build/VIN labels, engine/case/module/trim evidence; WIS Z versus salvage R discrepancy preserved.
2. **Cold intake sealing and exact revised valve/head repair** — Full manufacturer advisory and factory VIN-part path, material/revision proof, genuinely cold raw cylinder measurements; no claim that later number proves cure.
3. **Lubrication, pickup/PCV and timing complete inventory** — VIN-filtered drawings plus exact oil-pressure test conditions, pump/PCV architecture, all timing/seal/bolt dependencies and available job basket.
4. **AF40-II original tag and economically available assembly** — FWD case/controller/converter/valvebody mapping, actual used/reman written warranty and delivered quote, fluid job quantities and adaptation support.
5. **Cooling and turbo complete original identity** — LHU thermostat/cap/fan specs, BorgWarner fitted number, catalogue supersessions and oil/coolant/charge-air service checks.
6. **Structure, brakes and restraint safety** — Factory structure/repair/lifting data, actual corrosion inspection, brake option and ABS setup, seat/PPS/SDM labels, full recall history and completion.
7. **Current authorized module/keys support** — Successful supported Saab service path/quote for exact ECM/BCM/TCM/key pairing; hardware/calibration/security restrictions; no generic GM programming promise.
8. **Full fuel/emissions component mapping** — US emissions label-specific catalyst/EVAP/sensors/injectors; manufacturer-approved replacement and installation seal/pipe requirements.
9. **Rare lighting/body/glass restoration blockers** — Actual deliverable US legal lamp/glass/trim quotes, correct HUD/options and freight terms; used condition and return rights documented.
10. **Chassis, steering, axles, HVAC and interior inventory** — Chassis-option-specific assembly rows and manufacturer labels, all hardware/procedures and repair alternatives; no platform-wide swaps.
11. **A/B interchange approval and real supplier identities** — Exact manufacturer part/revision, interfaces, operating/calibration requirements and directed OEM supersession; manufacturer evidence before category promotion.
12. **Complete US repair economics and maintenance evidence** — Published exact-configuration labor times or written specialist quote, tools/programming/tax/shipping/core/towing, verified package contents and factory US schedule.

Use the [existing detailed lot worksheet](ng95-2011-turbo4-lot-inspection-worksheet-20261015.md) and its added component/diagnostic decision sequence before evaluating a real vehicle. Unknown faults remain HOLD; confirmed work outside the objective remains STOP. FINALIST is a request for further inspection and pricing.

## Reproduction

`python3 tools/check_ng95_components.py --check --summary` checks source references, hierarchy, scope boundaries, price arithmetic and generated-report consistency. `python3 tools/check_ng95_components.py --write-report` regenerates this document from the existing dossier. Passing checks does not validate mechanical fitment or turn a listing into stock.
