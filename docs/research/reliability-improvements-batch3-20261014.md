# Reliability improvement evidence register — batch 3

Scope: original Saab 9-5 (9600) B205/B235 and second-generation Saab 9-3 (9440) B207 FWD. Excludes second-generation 9-5 (9650), B308E, B284 and XWD pending their own analysis.

This register reuses existing repository research. **No candidate below is proven to have longer service life than the original part.** Factory corrections, normal service replacements and reliability upgrades must not be conflated.

| ID | Vehicle / system | Candidate or correction | Evidence level | Remaining verification |
| --- | --- | --- | --- | --- |
| RI-01 | Early original 9-5 B205/B235 PCV | Saab 55561200 renovation kit in relevant bulletin scope | Factory-documented intervention | Year/engine applicability, actual installed kit, present supply; does not reverse bearing damage |
| RI-02 | Original 9-5 Trionic 7 ignition | Genuine Saab black cassette 32022255 | Identified genuine service part | VIN fitment, stock, revision, fault diagnosis, comparative life |
| RI-03 | Original 9-5 B235 automatic radiator | Nissens 32019620 listing | Supplier-listed service alternative | VIN/ATF fitting confirmation, delivery, leak-life comparison |
| RI-04 | 9-3 B207 water pump | Saab/GM-number 12630084; separate HEPU 32020290 listing | Supplier-listed candidates | Exact B207 configuration, gear/seal kit, actual HEPU availability, longevity |
| RI-05 | Early 9-3 FA57 automatic cooler | Factory TA440-0702 seal/cooler correction | Factory-documented limited chassis range | VIN and contamination testing; coolant in ATF may mean gearbox replacement |
| RI-06 | Original 9-5 starter | Bosch reman 32101497, OE-reference 5194758 | Supplier-listed remanufactured service part | OE match, gearbox configuration, core/warranty and installed cost |

## Practical ordering

1. **Reject or price high-consequence existing damage first:** oil-pressure/bearing symptoms, internal gearbox slip, coolant-contaminated ATF, structural mounting rust, severe overheating.
2. **Verify exact factory correction eligibility** by VIN, chassis and transmission identity, rather than general model year.
3. **Validate component interchange** from original EPC and full installation bill; a shared GM number or aftermarket catalog listing is not automatic fitment proof.
4. **Look for comparative reliability evidence** (revision change, design mechanism, test results or defensible field data) before calling a replacement an upgrade.
5. **Check parts supply and total cost** including seals, programming, tools, fluid, labor and possible donor-component risk.

## Source documents already present in repository

- [Original 9-5 20-case engineering dossier](og95-b205-b235-complete-purchase-dossier-20261014.md)
- [9-3 B207 17-case engineering dossier](ng93-b207-complete-purchase-dossier-20261014.md)
- [U.S. retail parts supply snapshot](us-retail-parts-supply-snapshot.md)
- [B207 cross-manufacturer water pump investigation](cross-manufacturer-gm-saab-b207-water-pump.md)

## Interpretation limits

The early 9-3 FA57 cooler bulletin must **not** be transferred to original 9-5 automatics. The original 9-5 PCV kit must **not** be prescribed for B207. Neither a genuine part number nor a supplier listing establishes longer lifespan, VIN approval or current stock. This document records six prioritized leads, not six verified upgrades.


## Follow-up primary-source verification (2026-10-14)

### RI-01: Early original 9-5 oil-sludge / PCV decision

[Saab bulletin 210-2554 ed.3, June 2006](https://saabwisonline.com/9-5-9600/2000/2-engine/basic-engine-4-cylinder-petrol/bulletins-si-mi/210-2554-ed-3-noise-from-the-timing-chain-and-oil-sludge-in-the-engine) specifies **US/CA MY1998–2003 B205/B235** and also **old 9-3 (9400) MY1999–2003**. The latter is not the B207 9440.

- Bulletin is **symptom-triggered**: chain rattle, unusual whine/rumble/knock or oil pressure warning; it expressly says no further bulletin diagnosis absent those symptoms. That does not prohibit normal purchase inspection.
- For symptoms, Saab directs oil level, mechanical pressure, timing-chain and sump/bearing assessment. Chain tensioner extension **over 15 mm** triggers timing/balance chain replacement, but first evaluate lower-end damage.
- Saab directs bearing inspection of cylinders 1 and 4 after sump removal; if bearings damaged, **short-block replacement**, not PCV-only repair.
- Sump cleanup specifies pickup **91 86 156** (Canadian reference 55557225) and O-ring **91 38 009** (Canadian reference 30544347). Factory PCV renovation kit **55 561 200** is part of the final correction, with condition-dependent hoses.
- Saab recommends full-synthetic compliant oil and shorter oil-change intervals following correction. Do not generalize bulletin symptom pathway to every asymptomatic car or claim the PCV kit restores a damaged engine.
- **Disposition:** documented factory corrective pathway, **not proven lifetime upgrade**. Prioritize engine damage exclusion over kit purchase.

### RI-05: Early 9-3 FA57 automatic cooler — purchase disqualifier

[Saab technical advice TA440-0702, January 2007](https://saabwisonline.com/9-3-9440/2005/4-transmission/automatic-transmission/5-speed-fa-57/bulletins-si-mi/ta440-0702-coolant-in-atf-oil) applies to **9-3 SS/CV MY2003–2005**, below chassis **51002378 (SS)** and **56001058 (CV)**, with a separate diesel SS threshold **51000001**. Its stated cause is inadequate sealing between cooler-line nipples and the cooler.

- Symptoms include gearbox warning, TCM **P0715 00 / P0720 00**, poor shifting and noise; absence of these does not establish fluid purity.
- **Confirmed coolant contamination**: Saab instructs complete transmission replacement, cooler connection rework under service campaign **15446 / MI 260-2634 ed.2**, cleaning/flush and TCM adaptation. A seal-only fix is **not** a remedy for an already contaminated transmission.
- Bulletin describes heating an ATF sample with a flame as a detection method. **Do not instruct DIY flame-heating ATF**; request a professional transmission-fluid contamination test instead.
- **Disposition:** chassis-limited factory-documented failure mechanism, potentially uneconomic on a low-price project. Do not transfer it to the original 9-5 or all 9-3 gearboxes.

### RI-04: B207 water pump — strong shared-SKU identity, difficult DIY

[Saab Parts original listing](https://webshop-fi.saabparts.com/productdetail/saabparts/12630084) identifies **12630084** for **9-3 B207 MY2003–14**, with sprocket and gasket included. [GM Genuine Parts](https://parts.chevrolet.com/product/gm-genuine-parts-engine-water-pump-kit-12630084) independently lists **GM 12630084 / ACDelco 251-751** and **gear-driven** pump specifications. The GM page's generic *serpentine-belt-driven* marketing description conflicts with its own product-specific drive-type field; **use the Saab-specific procedure**, not the generic marketing text.

[Saab WIS coolant pump removal/fitting](https://saabwisonline.com/9-3-9440/2004/2-engine/4-cylinder-petrol/cooling-system/adjustment-replacement/coolant-pump) requires special holder **83 96 103** to secure the balancer-shaft pinion, extensive exhaust/turbo and wheel-well access, seals and precise gear installation. This is **not a simple conventional external pump swap**. The identical official service SKU does not prove a used donor interchange, a lower total cost or improved longevity.

**Disposition:** confirmed two-channel genuine service-part identity; **DIY complexity elevated**, fitment/boxed content and comparative life still require vehicle-level confirmation.

### New purchasing logic

1. **Early 9-5 with oil pressure lamp, low rumble or lower-end knock:** do not spend money on PCV kit before qualified damage assessment; pass if major engine work exceeds budget.
2. **Early 9-3 FA57 with coolant in ATF:** treat as transmission-replacement economics, not a preventative cooler seal bill.
3. **9-3 B207 needing water pump:** verify 12630084 and required tool, access, seals and labor before valuing the car. Shared GM/Saab SKU helps supply, not necessarily DIY cost.
4. **No proof of comparative failure rates or longer life** has been added; none of RI-01, RI-04, RI-05 should be relabeled a proven durability upgrade.
