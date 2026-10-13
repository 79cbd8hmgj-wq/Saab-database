# Saab 9-5 factory turbo returns: bulletin 291-2494 and FA57 MY2005–09 diagnosis

**Evidence date:** October 12, 2026. This is a research-only database supplement for the Saab original 9-5 (9600), not a working replacement simulator or a claim that any particular project Saab has a healthy turbo/gearbox.

## 1. The important November 2004 turbo bulletin

Original factory bulletin [**291-2494: Reduced performance and diagnostic trouble codes for the turbo control valve**](https://saabwisonline.com/9-5-9600/1998/2-engine/turbocharger-system/bulletins-si-mi/291-2494-reduced-performance-and-diagnostic-trouble-codes-for-the-turbo-control-valve) says:

- **Issue date November 2004**; **all markets**; includes **original 9-5 M98-** and separately both generations of 9-3. The `/1998/` workshop mirror directory is **not** the publication date.
- Saab investigated returned turbos and often found the real fault in **bypass diaphragm, wastegate, or boost-control function**, not the turbocharger.
- Factory pre-replacement checklist records vehicle/engine/transmission, actual DTCs, control-module VIN/part/hardware/software/programming date, and the customer's symptom.
- For petrol engines it separately tests **wastegate actuator and lever leakage**, **bypass valve membrane vacuum/pressure holding**, and **charge-air hoses/intercooler pressurization**. The proper pressure test value and procedure must be obtained from the matching engine/year WIS page, not guessed.
- The bulletin gives **different vacuum-circuit tests for engines with a vacuum pump (at least 0.7 bar) and without one (at least 0.4 bar)**. You must establish which circuit is present rather than apply both to a B235.
- Inspect for abnormal turbo oil leakage, compressor wheel damage, and shaft movement only **after** the external faults are assessed. Replacement is Saab's last diagnostic branch if earlier checks do not identify the problem.

### Important: the shaft-play sentence is not a usable engineering tolerance

The bulletin describes small shaft movement using a phrase equivalent to **“axial (up/down, about 1–2 mm)”** and contrasts it with “no radial play.” That is **internally inconsistent terminology**: up/down would conventionally describe radial rather than axial direction in a shaft. It is an all-model turbo diagnostic checklist, **not a calibrated GT17 or Mitsubishi TD04HL-15T shaft-play data table**. We record its existence and ambiguity, but the dataset deliberately stores `usable_numeric_axial_mm: null` and `usable_numeric_radial_mm: null`. **Do not put 1–2 mm into a micrometer limit, warranty pass/fail test, or used-turbo purchase decision.**

We separately confirmed that the factory [MY2006 turbo technical data](https://saabwisonline.com/9-5-9600/2006/2-engine/turbocharger-system/technical-data/) and [MY2008 turbo technical data](https://saabwisonline.com/9-5-9600/2008/2-engine/turbocharger-system/technical-data/) indices contain a **Turbo shaft play** entry, but the actual numerical pages could not be opened. This is an explicit unresolved high-priority gap. The previous specific non-US/CA B205E/B235E **January 2002 bulletin 291-2317** on a retaining clip is **different**; it does not authorize a clip retrofit for every US/CA B235R.

## 2. Distinguish MY2005 and MY2009 five-speed automatic adaptation

The separate [MY2005 adaptation procedure](https://saabwisonline.com/9-5-9600/2005/4-transmission/automatic-transmission/adjustment-replacement/adaptation-resetting) and [MY2009 procedure](https://saabwisonline.com/9-5-9600/2009/4-transmission/automatic-transmission/adjustment-replacement/adaptation-resetting) agree on important points:

| Factory statement | Meaning for DIY project-car screening |
| --- | --- |
| Reset old learned shift adaptation **after transmission, TCM or software replacement/update** | Not a generic remedy for rough shifting on unknown used car |
| Adaptation uses working ATF temperature **65–110°C** | This is a **shift adaptation** temperature window, not the 80°C **fluid level** check condition from other WIS pages |
| Use **Tech 2** to zero learned adaptation and perform an instructed full workflow | Do not assume a disconnected battery or random clearing of codes is equivalent |
| **Do not warm the gearbox using a stall test** | Explicit factory prohibition; do not run a full-throttle brake-stall test to prepare adaptation |
| Record outcome and check that actual shifting quality improves | Successful adaptation is not proof that internal clutches are unworn |

The [MY2007 TCM description](https://saabwisonline.com/9-5-9600/2007/4-transmission/automatic-transmission/technical-description/control-module) specifies **engine-code-specific programming** for B205E, B235E/R, D223L and B308E, an unprogrammed new service unit requiring **Tech 2/SPS**, and nonvolatile learned shift corrections that allow smooth shifts even as a gearbox wears. **A TCM housing that fits is not an approved interchange**. A battery disconnect does not erase learned wear history or make the car mechanically sound.

## 3. Missing sensor signal is different from confirmed ratio error

- [MY2005 **P0717**](https://saabwisonline.com/9-5-9600/2005/4-transmission/automatic-transmission/fault-diagnosis-diagnostic-trouble-codes/p0717): The **input speed sensor** has no signal while the output shaft signal is available. The TCM can estimate input speed from output speed. A year-correct diagnostic check compares input RPM with engine RPM when the selector is in **P/N**. This requires sensor/harness assessment, not automatic complete gearbox replacement.
- [MY2009 **P0735**](https://saabwisonline.com/9-5-9600/2009/4-transmission/automatic-transmission/fault-diagnosis-diagnostic-trouble-codes/p0735): In fifth gear and documented temperature/load conditions, the **actual ratio deviates by more than 20%** from the expected ratio. That is a genuine functional ratio discrepancy, but the page does not independently identify whether it is clutch, hydraulic pressure, command, sensor or other damage. Mechanical repair cost cannot be decided from this code alone.
- [MY2009 TCM Read Values](https://saabwisonline.com/9-5-9600/2009/4-transmission/automatic-transmission/fault-diagnosis-general/menu-read-values) includes input/output shaft speeds, requested/current converter lock-up slip and more. A nonzero actual torque-converter slip value does **not** automatically equal failure if the controller requested slipping lock-up.
- [MY2007 automatic Differential Protection System](https://saabwisonline.com/9-5-9600/2007/4-transmission/automatic-transmission/technical-description/differential-protection-system-dps) limits engine torque in substantial wheelspin below 80 km/h, using front-right wheel speed vs TCM output. This is an **engine control protective response**, not a standard gearbox wear symptom or identical to TCS.
- The original [MY2008 no-dipstick ATF level procedure](https://saabwisonline.com/9-5-9600/2008/4-transmission/automatic-transmission/adjustment-replacement/automatic-transmission-transmission-fluid-level-without-dipstick) uses **80°C** and special gauge **DT-47653**; this is separate from adaptation. A real car must be identified to know its level access variant.

## 4. A test recorded for expert interpretation, not for buyer use

The [MY2006 factory stall-speed page](https://saabwisonline.com/9-5-9600/2006/4-transmission/automatic-transmission/fault-diagnosis-fault-symptoms/checking-the-stalling-speed) lists **2,250–2,450 rpm** for the listed petrol engine variants under a special **full-throttle loaded D/R test**, no longer than **five seconds**, with at least **one minute** between tests. Its symptom table suggests problems involving low engine torque or converter failure when too slow, and several potentially internal hydraulic and clutch causes when too fast. The engine and transmission must already be working within normal requirements.

**This is not a used-lot diagnostic procedure we recommend.** Brake-stall testing imposes severe heat and torque loads on an unknown transmission, can move a vehicle, and can worsen damage. The later source expressly **forbids using a stall test to warm the transmission for adaptation**. Keep the values in technical research for qualified specialists, not a clickable DIY purchase checklist or simulator result.

## 5. What remains missing

- Authentic year/turbo-specific **axial and radial shaft play acceptance** with corrected axis definition and measurement condition for B235R TD04 and B235E Garrett variants.
- Manufacturer WebEPC parts, original turbo and gearbox hardware identities, repair supersessions, and usable present-day Tech 2/SPS/software support.
- Later individual model-year code definitions between MY2005 and MY2009; cross-year differences cannot be resolved by applying one year’s DTC wording universally.
- Physical VIN, engine and gearbox serial, fluid samples, actual scan measurements, boost leaks, turbo compressor contact and safe corrosion examination for any particular candidate.
- Real prices and labor/damage estimates, plus validated field data on failure frequency. Record counts are **not** a completeness or reliability score.

**Purpose:** make the source-backed differential diagnosis sufficiently accurate to avoid buying engines or transmissions for small control faults, while still rejecting a used Saab that has proven expensive internal damage.
