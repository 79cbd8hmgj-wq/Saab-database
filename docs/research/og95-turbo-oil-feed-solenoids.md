# Original 9-5: turbo installation/oil-feed preservation and FA57 solenoid differentiation

**Evidence reviewed 2026-10-12.** This is an engineering **research dataset**, not a simulator, VIN-level parts approval, a measured failure-rate study, or an instruction to dismantle/operate a damaged vehicle. Original Saab WIS year directories and bulletin population boundaries are preserved.

## 1. Turbo repair: correct installation can prevent a second failure

Separately reviewed original **9-5 4-cylinder petrol** Saab factory service procedures for [MY2005](https://saabwisonline.com/9-5-9600/2005/2-engine/turbocharger-system/adjustment-replacement/turbo-4-cyl), [MY2006](https://saabwisonline.com/9-5-9600/2006/2-engine/turbocharger-system/adjustment-replacement/turbo-4-cyl) and [MY2008](https://saabwisonline.com/9-5-9600/2008/2-engine/turbocharger-system/adjustment-replacement/turbo-4-cyl) all explicitly require **filling the turbo bearing housing oil inlet with oil and turning the compressor by hand** before the first startup after fitting. This is a replacement *prerequisite*, not proof a vehicle needs another turbo.

For these independently read year-specific procedures, Saab lists:

| Service joint | Factory torque (2005, 2006, 2008 petrol 4-cyl turbo installation) |
| --- | --- |
| Turbo **oil-feed** banjo | **20 Nm**, with new copper seals |
| Oil-feed pipe at **oil-filter adapter** | **25 Nm**, with new copper seals |
| Turbo **oil return** M6 bolts | **14 Nm** |
| Turbo **coolant** banjo | **25 Nm**, with new copper seals |
| Turbo coolant connection at pump | **20 Nm**, with new copper seals |
| Charge-air hose to turbo | **8 Nm** |
| Front exhaust flex bellow while removing unit | **do not bend more than 5°** from neutral |

*Each number applies to its specifically named joint. It is not an oil-pressure acceptance test, coolant drain-plug torque, engine-oil-cooler fitting or automatic-transmission cooler banjo.*

The procedures also require keeping dirt out of the compressor plumbing, thoroughly **cleaning charge-air hose contact surfaces and adjoining pipes**, and replacing rusty/damaged clamps before securing. MY2006 and MY2008 pages separately describe work around a **260-hp wastegate-box** installation; they do not authorize replacing a lower-output engine, its control module or wastegate with the 260-hp hardware.

The separate original [MY2004 factory turbo lubrication explanation](https://saabwisonline.com/9-5-9600/2004/2-engine/turbocharger-system/technical-description/lubrication-cooling-4-cyl) shows the turbo's high-speed floating journal bearings require oil from the engine oil-filter adapter via a dedicated feed pipe, returning to the **engine sump**. Water cooling and after-shutdown **thermosiphon circulation** reduce oil coking risk. Its qualitative wording is not a quantitative test of feed pressure, turbine wear or service-life improvement. The [MY2005 oil-filter adapter procedure](https://saabwisonline.com/9-5-9600/2005/2-engine/basic-engine-4-cylinder-petrol/adjustment-replacement/oil-filter-adapter-housing) separately requires replacing the adapter-housing O-ring; it must **not be confused with banjo copper washers**.

**Remaining high-cost uncertainty:** [MY2008 Saab turbo technical-data directory](https://saabwisonline.com/9-5-9600/2008/2-engine/turbocharger-system/technical-data/) lists a shaft-play page, but its axial/radial numeric limits were **not independently retrievable**. They are stored as `null`, not guessed from another turbo. Before calling a used B235R turbo good or bad, we still need exact hardware/type, original mechanical acceptance limits, oil pressure and feed/return condition and direct inspection.

## 2. MY2007–09 five-speed 9-5 automatic: shift valves versus pressure valves

The factory [2007](https://saabwisonline.com/9-5-9600/2007/4-transmission/automatic-transmission/technical-data/gearshift-solenoid-valve-s1-s2-s3-s4-and-s5), [2008](https://saabwisonline.com/9-5-9600/2008/4-transmission/automatic-transmission/technical-data/gearshift-solenoid-valve-s1-s2-s3-s4-and-s5), and [2009](https://saabwisonline.com/9-5-9600/2009/4-transmission/automatic-transmission/technical-data/gearshift-solenoid-valve-s1-s2-s3-s4-and-s5) **gearshift solenoid S1–S5** tables independently state all five **11–16 Ω at 20°C**. S1, S2 and S4 are **open at zero current**; S3 and S5 are **closed at zero current**.

They are not the same circuits as the 300 Hz modulated **SLS/SLT hydraulic-pressure regulators**. Factory documents must retain their *original year and section type*:

| Factory source | Coil type | Winding resistance at 20°C |
| --- | --- | --- |
| MY2007 9-5 transmission **technical-data table** | SLS/SLT pressure control | **5.0–5.6 Ω** |
| MY2008 9-5 transmission **technical description** | SLS/SLT pressure control | **normally 5.1–5.5 Ω** |
| MY2007, 2008 and 2009 **technical-data table** | S1–S5 gear selection | **11–16 Ω** |

The small difference between MY2007 table and MY2008 narrative may reflect rounding/spec presentation or a real revision; **we do not claim which** without a controlled Saab specification/revision record. Neither value is a safe substitute for the other coil class.

[MY2008 pressure-control description](https://saabwisonline.com/9-5-9600/2008/4-transmission/automatic-transmission/technical-description/solenoid-valves-sls-and-slt-for-system-pressure) specifies SLS **TCM connector B pins 26/36**, SLT **B pins 35/15**, **300 Hz PWM**, and an unusual failure behavior: **open-circuit/zero-current leads to maximum hydraulic system pressure**, a plausible reason a car may **shift hard without the complete gearbox being mechanically ruined**. The same document associates **P0748 with SLT** and **P0785 with SLS** and limp-home mode. This is a diagnostic fork, not a presumption every solenoid with correct resistance is functioning hydraulically. Factory 2007 resistance data: [SLS/SLT technical data](https://saabwisonline.com/9-5-9600/2007/4-transmission/automatic-transmission/technical-data/solenoid-valves-pressure-regulation-slt-and-sls).

A separate MY2007 lock-up **SLU** valve page was only present in search-index form: we record its lower confidence and do **not** generalize it to later years. Physical gearbox/TCM ID, installed connectors, ATF condition, cold/warm symptoms and current module diagnostics remain necessary before approving any solenoid or valve-body repair.

## 3. Two similar "common faults" bulletins for completely different cars

Saab issued similarly named original technical bulletins in **February 2000**, both excluding US/Canada:

- [**440-2181**](https://saabwisonline.com/9-3-9400/1998/4-transmission/automatic-transmission/bulletins-si-mi/440-2181-common-faults-on-automatic-transmissions): **MY1998–99 9-3 (9400)** with automatic transmission, **not** 9-5.
- [**440-2182**](https://saabwisonline.com/9-5-9600/1998/4-transmission/automatic-transmission/bulletins-si-mi/440-2182-common-faults-on-automatic-transmissions): **MY1998–99 9-5 (9600)** with automatic transmission, not MY2005–09 FA57.

Both old documents name historic **Dexron III** and associated early-transmission procedures; **this does not apply to the separately verified Saab 3309 oil on MY2005 FA57**. The 9-5 bulletin mentions a possible falsely triggered overheating display caused by grounding at **G41S, G41P and G43**, but again **only within its original 1998–99 non-US/CA population**. Never infer that those grounding-point labels explain a 2008 9-5 transmission warning.

## 4. Specific unresolved research, before calling a Saab "repairable"

1. MY2007 and MY2009 petrol turbo installation text must be read independently. The 2005, 2006 and 2008 specifications are recorded separately and do not establish other years.
2. Turbine/shaft exact acceptance values, genuine OE feed/return seals and independent turbo oil delivery and drainage test criteria remain unresolved; current facts cannot identify bearing damage on a non-running car.
3. Current VIN-filtered original Saab WebEPC solenoid, valve-body and turbo replacement parts have not been retrieved.
4. Exact MY2007 versus MY2008 SLS/SLT winding band discrepancy remains an explicit gap, not an inferred new component design.
5. MY2008–09 lock-up valve SLU data and authorized Tech2 electrical and hydraulic checks require original model-specific information.
6. The later-year automatic's real repair cost, risk of internal damage and remaining life still depend on actual fluid condition, TCM data, qualified examination and any donor swap history.

These additions advance **mechanical triage and parts provenance**, not premature construction of a reliability simulator.
