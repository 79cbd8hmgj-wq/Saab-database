# Trionic 7 versus Trionic 8 service support: repair-path evidence

Research date **2026-10-13**, US/Canada priority MY2005–06 Saab 9-3 9440 B207 (Trionic 8) versus 2008 original Saab 9-5 9600 B235 (Trionic 7). These are **different components and failure modes**. No quantified fleet frequency, lifecycle durability or tested car was supplied.

## 9-5 T7: genuine ignition discharge cassette remains a serviceable component

[Official Saab Parts / Hedin product listing](https://saabparts.com/product/HP32022255) shows genuine ignition cassette **32022255** as an ongoing stocked item on its Swedish market support site, with foreign-currency pricing; this does **not** establish current local US inventory or fitment of any real VIN. The original [MY2008 Saab WIS cassette removal/installation](https://saabwisonline.com/9-5-9600/2008/2-engine/trionic-t7-4-cyl/adjustment-replacement/ignition-discharge-module) prescribes *extended ignition-discharge diagnosis first*, then a ten-pin connector/four screws, sealing treatment and exact factory procedures. The cassette is **not** the full Trionic 7 engine-control module. This service path may be mechanically more straightforward than T8 ECM security/memory programming, but it does not establish a lower failure rate or total repair expense without actual system faults and invoices.

## 9-3 T8: specialist cloning service is available but not a simple donor swap

[Velectronix T8 cloning service](https://velectronix.com/products/2003-2011-saab-9-3-2-0l-ecm-clone-programming-service) lists **$89.99** (observed 2026-10-13), requires both customer original and replacement ECUs, **and explicitly requires original ECU to communicate**. The vendor's warranty is for programming, not the module hardware. A separate [Modern Classic Saab service](https://www.modernclassicsaab.com/products/p/trionic-8-t8-cloning-service) lists **$75** for customer-supplied original and donor, with seller-noted FWD and XWD donor restrictions; not a complete fitted replacement cost or an official Saab interchange authorization. Costs, active availability, required software and actual ECU-data recoverability must be confirmed anew when shopping.

Factory [MY2006 Trionic 8 ECM architecture](https://saabwisonline.com/9-3-9440/2006/2-engine/4-cylinder-petrol/engine-management-system-trionic-t8/technical-description/control-module-trionic-4-cyl-petrol-589) has two processors controlling torque/fuel/ignition and ESD/short-circuit warnings. [Saab's MY2006 original component location](https://saabwisonline.com/9-3-9440/2006/2-engine/4-cylinder-petrol/engine-management-system-trionic-t8/location-of-components/control-module-trionic-b207-switch-b-589b) places this ECU at the engine front. This supports a hypothesis of thermal exposure; it does **not** provide quantified failures or independent proof that relocating the ECU extends life.

## What changes in the model decision

1. Both candidate Saab platforms retain service paths for significant electronics faults: a Saab Original T7 cassette is currently listed, and independent T8 ECU cloning services exist. Neither platform should be rejected solely on an unsupported claim that its electronics are impossible to repair.
2. **T7 ignition cassette replacement and T8 ECM replacement are not like-for-like faults.** The former cassette is a separate ignition unit with a factory mechanical removal procedure; the latter involves calibration and immobilizer data and might require a readable original unit. Compare T7 ECM versus T8 ECM separately when those are the actual failed components.
3. One vendor's cheap programming-only quote must **not** be compared with the price of a whole genuine ignition cassette as if both supplied a working replacement with labor. Include donor unit, shipping, diagnosis, downtime, warranty and tools.
4. The provisional B207 parts-commonality lead remains **insufficient to rank model dependability**. Real transmission/engine condition and structural corrosion are primary inexpensive-project screening factors.

Structured [dataset](../../data/datasets/t7-t8-repair-support-model-choice.json) and [qualitative decision map](../../data/model-selection/interchange-evidence-20261013.json) preserve these differences without fabricating failure probabilities.
