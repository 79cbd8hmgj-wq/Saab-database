# Original 9-5 MY2004–09 PCV, radiator and engine-mount provenance

**Research date: 2026-10-12.** This is a Phase 0 **source-scoped engineering database increment**. It does not approve a supplier part for any actual car, guarantee durability, establish an original manufacturer supersession or run a simulator. Read the exact source, vehicle engine and full VIN/repair history before taking mechanical action.

## 1. Two Saab PCV campaigns must remain separate

| Factory bulletin | Market, years, engine/transmission | Chassis range printed | Selection caveat | Corrective work |
| --- | --- | --- | --- | --- |
| [210-2496 / CSP15433](https://saabwisonline.com/9-5-9600/2005/2-engine/basic-engine-4-cylinder-petrol/bulletins-si-mi/210-2496-replacing-the-oil-trap) | Market "see separate list", MY2004–05 **B235 manual** | 43000003–53502479 | **Not all in range** | Oil trap **55 558 696**, related hose and hose retention steps |
| [210-2508 / CSP15435](https://saabwisonline.com/9-5-9600/2005/2-engine/basic-engine-4-cylinder-petrol/bulletins-si-mi/210-2508-securing-the-crankcase-ventilation-hose) | All markets, MY2004–05 **B205/B235**, no manual-only restriction | 43000003–53502893 | **Not all in range** | Ventilation hose tie **79 71 864** and hose clip **90 490 543** |

The 15433 bulletin addresses high oil consumption/low-load high-rpm driving, plus the MY2004 crankcase ventilation configuration. Its early engine case **4 000 000–4 017 590** uses additional hose **59 61 610**; a factory repair document has more force for *that repair/engine range* than a retailer's generic 2004–2009 compatibility headline. CSP15435 primarily secures a throttle-body ventilation hose that can detach. These are **different** programs with different inclusion boundaries; neither applies merely because the car is a 2004/05 B235. Modification plates A1 and A2 are distinguished and described for **non-US/Canada** markets; US/CA repair completion requires actual service history, not an assumed sticker rule.

The [MY2008 Trionic 7 diagram](https://saabwisonline.com/9-5-9600/2008/2-engine/trionic-t7-4-cyl/technical-description/system-diagram-intake-turbo-exhaust-4-cyl) independently shows oil trap as callout 12 and PCV check valves as 13, **but the diagram provides no authorised part number, modern kit compatibility, or proof of failed engine bearings**.

## 2. Radiators: gearbox-dependent interface backed by WIS

The [MY2006 petrol radiator procedure](https://saabwisonline.com/9-5-9600/2006/2-engine/cooling-system/adjustment-replacement/radiator-4-cyl) specifically calls for removal/refit of transmission oil cooler connections **on automatic cars**, plus ATF level checking. That supports a **real functional interface difference**, not a guessed catalogue rule.

Independent [eSaabParts radiator assembly diagram](https://www.esaabparts.com/viewparts.php?section=314395285) claims 2002–09 4-cyl variants:

| Application in supplier catalogue | Claimed Saab-number reference | Vendor part SKU |
| --- | --- | --- |
| Manual radiator | **5193370** | **32019619** Nissens |
| Automatic radiator | **5193388** | **32019620** Nissens |

The merchant calls its Nissens SKU the "latest part number" and the Saab reference a "superseded part number." **This is a supplier product cross-reference, not evidence of an official Saab manufacturer supersession or an OE-approved Nissens design**. Both are recorded with supplier-level evidence and empty validated interchange relationships.

Additional candidate radiator system identifiers from the same retailer: upper hose **5193362** (Orio-labelled merchant SKU 33457832), lower hose **4899449** (Orio-labelled SKU 32022572), and differing callout-44 radiator screws **92153150** for 2005–06 versus **11900355** for 2007–09. Even if the catalogue puts them in one diagram, these are distinct components with separate vehicle checks.

**Safe diagnostics:** [MY2008 Saab WIS cooling pressure test](https://saabwisonline.com/9-5-9600/2008/2-engine/cooling-system/adjustment-replacement/cooling-system-pressure-testing) uses factory adaptor 30 05 451/tester 30 05 477 and says to pressurize the system to **over 1 bar**, then look for pressure loss. This does **not** establish a do-it-yourself pressure target for an unknown hot or damaged car; the factory specifically warns about burns from pressurised coolant. [MY2008 radiator-fan procedure](https://saabwisonline.com/9-5-9600/2008/2-engine/cooling-system/adjustment-replacement/radiator-fan-4-cyl) calls for unplugging fan connectors before contact, and includes different automatic line routing on the fan cowling.

Do **not** transpose the **9-3 FA57 coolant-in-ATF advisory** to these original 9-5 radiators. Transmission family and cooling layout differ; a particular original 9-5 must be examined, not diagnosed from another platform's bulletin.

## 3. Engine mounts: a real WIS VIN-bound service change, not a part supersession

The [MY2008 WIS LH engine mounting](https://saabwisonline.com/9-5-9600/2008/2-engine/basic-engine-4-cylinder-petrol/adjustment-replacement/engine-mounting-left) differentiates manual and automatic mounting fastener torques (47 Nm vs 84 Nm), requires center-aligned mounting pad bolt position, and makes the **central nut**:
- up to VIN **73514478** inclusive: **84 Nm**;
- from VIN **73514479** inclusive: **74 Nm**.

The separately documented [MY2008 front torque arm](https://saabwisonline.com/9-5-9600/2008/2-engine/basic-engine-4-cylinder-petrol/adjustment-replacement/front-torque-arm) switches **gearbox bracket screw** torque from **47 Nm to 38 Nm** at the same boundary, while listing separate torque-plus-angle fasteners for the subframe and arm. Same cutover does **not** establish which parts may be swapped. Never apply these torque values to different joints.

The [MY2007 RH mounting](https://saabwisonline.com/9-5-9600/2007/2-engine/basic-engine-4-cylinder-petrol/adjustment-replacement/engine-mounting-and-engine-pad-rh) describes engine load support and neutral alignment after installation. [MY2009 rear mounting](https://saabwisonline.com/9-5-9600/2009/2-engine/basic-engine-4-cylinder-petrol/adjustment-replacement/engine-mounting-rear) distinguishes the manual gearbox's shift-linkage stay. Neither supplies a verified four-cylinder OEM mount number in our current record.

**False-positive supplier warning:** A retailer page for **5235544** says **B308E automatic** (a different engine), and its "Engine Mounts (2002–2009)" diagram shows **1998–2003** in its year selector. This mismatch is recorded as an explicit vendor metadata conflict, **not** a recommended mount for any B235 9-5.

## 4. Essential missing evidence before recommending actual parts or durability modifications

- VIN-filtered original manufacturer [Saab WebEPC](https://saabparts.com/saab-subscription-services) outputs with affected build, engine, gearbox, part description, supersession direction and actual component fitment.
- Campaign 15433 and 15435 selected-vehicle status and proof of work.
- Actual physical OEM or OE-stamped radiator, PCV hoses and original mount variants on a specific donor/project car.
- 2007–09 individual petrol radiator oil cooler fittings/lines and module gearbox identification.
- Controlled measured improvement in oil longevity, thermal performance or mount life for any aftermarket product. A parts catalogue is not reliability validation.

**Implication for project-car screening:** Record gearbox type, year, market, last eight VIN characters, engine code/stamping, campaign paperwork, PCV service, leak/ATF observations and mount/radiator condition. This makes DIY repair planning more accurate without alleging that every original part was designed badly, or that replacing it with an aftermarket part automatically creates Toyota-level reliability.
