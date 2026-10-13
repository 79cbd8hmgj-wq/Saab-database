# Cross-manufacturer OEM service SKU — GM / Saab B207 water pump 12630084

Research date **2026-10-13**. Priority vehicle **2005–06 9-3 (9440), B207**, not the original 2008 9-5 B235. This extends the earlier FAG/Opel aftermarket wheel-hub pilot with a **different evidence class**: two current manufacturer-support channels listing **the same part number**.

## Primary finding: both official channels list 12630084

- [GM Genuine Parts Chevrolet official product](https://parts.chevrolet.com/product/gm-genuine-parts-engine-water-pump-kit-12630084) identifies **12630084** as a GM OE replacement water-pump kit, with a **gear-driven** pump, four mounting holes, gasket/seal included and no mounting hardware. These are GM catalogue attributes, not measured original Saab component specifications.
- [Saab Parts / Hedin official webshop](https://webshop-fi.saabparts.com/productdetail/saabparts/12630084) independently sells **Saab Original 12630084** for **9-3 MY2003–14 B207**, and newer **9-5 MY2010–11 A20NFT/NHT**, with **sprocket and gasket included**. **Do not extrapolate to first-generation 9-5 (9600) MY2008 B235E/R.**
- The same number in both official sales channels is stronger evidence than a third-party cross-reference and establishes **dual-channel service SKU identity**. It still does not establish that a previously installed GM junkyard donor, old Opel variant or every boxed kit revision is the exact VIN-appropriate physical assembly. Accordingly, this is a *documented identical-number service option*, **not an approved installed donor conversion**.

## Important catalog conflict and actual mechanical difficulty

GM's product-specific attributes say **Water Pump Drive Type: Gear**, but its generic marketing paragraph mentions being **driven by a serpentine belt**. The [Saab original B207 coolant-pump procedure](https://saabwisonline.com/9-3-9440/2004/2-engine/4-cylinder-petrol/cooling-system/adjustment-replacement/coolant-pump) confirms the pump's timing-cover/balancer-shaft pinion and requires special **coolant pump holder 83 96 103**, new seals and careful timing-drive work. The GM generic belt-installation story must not guide a Saab B207 repair. Never open or handle a hot pressurized cooling system, and never improvise the drive gear procedure.

## Opel Z20NET historical number evidence is weaker

An [independently mirrored Opel Vectra C EPC table](https://nemigaparts.com/cat_spares/epc/opel/z02/f/19/) names Z20NET pump **93172718** with NLS recommendation **93178602**, also separate **93181118** and **93195308** entries. A [Saab retailer](https://www.saabpartscounter.com/oem-parts/saab-water-pump-12630084) lists these among 12630084 predecessor references. **Neither is the original authenticated VIN-based Saab/Opel WebEPC directed chain**. This is not enough to approve a used Vectra donor water pump or assert every predecessor number was identical.

## Decisions and missing verification

| Question | Current disposition |
| --- | --- |
| Exact GM Genuine and Saab Original numbered service SKU both 12630084 | **Documented by both official channels** |
| MY2005–06 B207 Saab 9-3 part installed from GM dealer without VIN check | **Not yet vehicle verified** |
| Original Opel Z20NET pump interchangeable as a donor | **Unverified** |
| Correct B207 removal/installation procedure | **Saab factory gear-driven pump sequence required** |
| Cheaper or longer-lasting than Saab-labelled part | **Unknown; no price or comparative life test** |

The machine-readable [dataset](../../data/datasets/cross-manufacturer-gm-saab-b207-water-pump.json) and [candidate-matrix entry](../../data/interchange-candidates/phase0.json) keep `approved_drop_in`, `approved_oem_donor`, `vehicle_tested`, `cost_advantage_verified` and `independently_tested_reliability_improvement` set to **false**, while preserving distinct confidence in **current SKU identity**. Future work should retrieve a real VIN-filtered Saab EPC application and compare physical boxed kits, then investigate selected older Opel/GM OE predecessors and actual cost outcomes.
