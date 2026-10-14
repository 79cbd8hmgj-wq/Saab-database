# Saab tier-list evidence standard — no model ranking yet

**Research milestone:** October 14, 2026. **Status:** NOT RANKABLE.

## The question this project will eventually answer

For each *actual* Saab generation/model-year/powertrain/gearbox/drivetrain/body/market/build combination, how reliable were the **original installed components**, what serious failure mechanisms are documented, and how expensive and obtainable is a durable repair **today**?

The final output may be a tiered comparison **only after a shared evidence standard and comparison universe are agreed**. It must not treat plentiful documentation, an inexpensive part, a famous failure, or thousands of production cars as proof of good/bad reliability.

## Four independent research pillars

| Pillar | What it measures | What it must not pretend |
| --- | --- | --- |
| **Factory component reliability** | Original OE revision and materials/design, known factory defect or weakness, recurrence, conditions/age/mileage, revised factory solution | A service bulletin is not a fleet failure rate; current aftermarket quality is not original reliability |
| **Known failure burden** | Exact fault mechanism, platform/engine/gearbox/build scope, symptom-test differential, stranding/safety/catastrophic consequence and feasible prevention | Forum mentions, complaint counts and recalls aren't equivalent to how frequently a problem occurs |
| **Current parts availability** | Correct OE part, directed Saab supersession, supplier-referenced aftermarket substitute, U.S. delivered inventory, suppliers, lead time, programming/tools and cost | Multiple listings do not prove current stock, OEM approval, physical interchange or durability |
| **Repair economics** | DIY feasibility vs qualified shop, complete parts/hardware/fluids/tools, labor, core/shipping/tax/towing, and rust/powertrain write-off thresholds | Factory warranty-operation time or cheapest listing is not an all-in repair quote |

The [blank component evidence intake](../data/tier-research/component-evidence-template.json) holds original installed-part revision, precise cohort and failure mechanism, properly denominated risk (or explicit unknown), OEM versus aftermarket replacement proof, dated supply observations, and separately costed DIY/specialist work. No example VIN, defect frequency, verified cost or fitment is fabricated. The [initial observation ledger](../data/tier-research/observations.json) now holds source-scoped ignition-module revisions and three failure mechanisms; see the [first batch review](research/component-defects-first-ledger-20261014.md). This is incomplete research, not comparable system coverage or a ranking.

The machine-readable standard: [`data/tier-research/methodology.json`](../data/tier-research/methodology.json). Separate typed observation categories: [`data/tier-research/observations.json`](../data/tier-research/observations.json).

## Why the current 110 are not an adequate tier-list universe

[U.S. production normalization](../data/vehicle-catalogue/us-production-normalized.json) identifies **110 source-compiled** production groups, but they are specifically **original 9-3/9-5 U.S., FWD, automatic, nonconvertible** rows. They exclude US/CA manual, AWD/XWD, convertibles and potentially different models (9-2X, 9-7X, 9-4X), as well as Canadian-only variants. Existing [candidate eligibility](../data/audits/candidate-scope-1998-2011.json) is a real prior research boundary and is **not changed by this methodology**. Decide the eventual tier-list universe explicitly before an across-the-brand ranking. Cars excluded from the 110-row baseline are **not less reliable**; they are outside the current denominator.

The baseline [U.S. feasibility audit](../data/vehicle-catalogue/us-feasibility-coverage.json) and [parts/tool research crosswalk](../data/audits/us-parts-tool-readiness-coverage.json) cover all 110 with one or more **research leads**, but the former explicitly reports **0 measured population failure rates, 0 actual inspected cars, 0 verified repair prices and 0 approved part interchanges**. This is **not** zero failing Saabs, zero available parts or complete evidence for the mechanisms. It is a gap in *comparable* quantitative/market verification.

[Reproducible 110-row tier readiness audit](../data/audits/tier-research-readiness.json) records existing scenario and job-plan **link counts only for tracking**. The counts are not failures, successes or scoring variables. Every cohort's original factory part lifespan, exact 2026 supplier delivery and installed repair economics are unestablished. Source-rich years must not be given preferred status by research density.

## Standard system inventory for equal comparison

The methodology lists **16 systems**, including **13 designated critical** for catastrophic cost, safety, immobilization or essential service. The same template applies to each eligible cohort:

- Engine oil / PCV / timing / valves; turbo, intake and charge air; gearbox/driveline; engine cooling / ATF heat exchanger
- Body corrosion, structural attachments, brakes and safety restraints; steering and suspension
- Fuel and exhaust/emissions; ECU/immobilizer, ignition, charging, starting, body wiring
- HVAC and water intrusion; interior controls; body panels, lights and seals; routine scheduled service and consumables

A low-value cosmetic failure and a seized original engine cannot be collapsed into one unweighted 'known issues' counter. Repeat repairs must not be counted as independent defective vehicles. A documented factory revision can improve later production without retroactively eliminating early-original issues.

## Evidence acquisition — source strength and outcome distinction

1. **Original Saab material:** WIS, technical service bulletins, revision/VIN boundaries, EPC part number chains, inspections, material specifications. Supports actual design and diagnostic procedures, usually **not event frequency**.
2. **U.S. NHTSA ODI complaints and investigations:** [official NHTSA data/API](https://www.nhtsa.gov/nhtsa-datasets-and-apis). Useful for finding patterns and checking safety investigations, not an unbiased per-vehicle failure rate: people self-select into filing complaints; powertrain/part revision and fleet exposure usually aren't known.
3. **NHTSA recalls and manufacturer campaigns:** same [official data/API](https://www.nhtsa.gov/nhtsa-datasets-and-apis). Use population, VIN/manufacturing range, failure hypothesis and prescribed corrective action; record actual vehicle completion separately.
4. **UK DVSA MOT inspection microdata:** [official anonymized testing dataset](https://open.data.dvsa.gov.uk/mot-anonymised/index.html) includes make/model, odometer, failures and test dates. Offers **inspection defect observations among surviving, UK-tested vehicles**, not U.S. road-salt or Saab powertrain lifetime failure probabilities. Normalize/cohort stratify by age, mileage, year, region when supported, retests and inspection regime; inspect test counts before conclusions.
5. **NHTSA manufacturer-supplied VIN identity:** [vPIC](https://vpic.nhtsa.dot.gov/api/). Helps confirm factory identity on applicable years; doesn't know a used car's installed engine, gearbox, corrosion or service history.
6. **Saab Parts/Hedin and present U.S. sellers:** [factory parts subscription](https://saabparts.com/saab-subscription-services) for VIN-filtered OE part chain when accessible, and dated merchant-specific *deliverable* offers, warranty, case deposit and lead times. Current online listings may be cached or out of stock, and compatible aftermarket brands can have different durability.

Community forums and specialist mechanics are useful for **candidate fault discovery and diagnostic detail**, but not self-validating prevalence. Seek original supplier or factory evidence and independent corroboration of repeat-failure mechanisms. Avoid conflating an enthusiast's difficulty ordering rare body trim with critical repair parts supply.

## What a real reliability estimate requires

A percentage would require **verified unique failure events / eligible in-service units or relevant exposure**, exact build/revision and failure definition, age/mileage/operating environment, maintenance/repair history, survivor and reporting bias, uncertainty, and a specified observation time window. Production totals in the normalized catalogue provide *historical manufacturing context*, **not the denominator of cars still at risk now**.

Where such a study is unavailable, the database can honestly say **factory-documented serious mechanism with unknown incidence**, and later support an explicitly uncertainty-limited *qualitative* tier. Do not manufacture a precise reliability percentage, lifetime prediction or Toyota comparison from owner anecdotes, NHTSA complaint counts or repair bulletins.

## Evidence exit criteria before ranking

The model list and eligible body/transmission/drivetrain combinations must be explicit; each has comparable critical-system source/search outcomes. Each major original factory failure has proper year/build/revision boundaries and differentiating tests. Part replacement evidence must separate documented OE-directed supersession, an untested supplier cross-reference, and a measured approved donor or engineered replacement. Dated in-market pricing must be real deliverability with repair cost components. Quantitative risk remains unknown unless a real denominator study exists.

When there is sufficient source parity, we can define **severity, supply risk, original-design weakness, ease of replacement and cost** as separate assessments, disclose certainty levels, and only then agree the weighting and tier cutoffs. Unsupported configurations should be **unrated due to missing evidence**, never assigned a low tier by default.

## Repeatability and guardrails

```bash
python3 tools/build_tier_readiness.py --check
python3 -m unittest discover -s tests -p 'test_tier_readiness.py' -v
python3 -m unittest discover -s tests -v
python3 tools/phase0_audit.py --check
```

The unranked audit regenerates from existing source-limited 110-configuration production, scenario, parts/tool and methodology files. If new genuine failure-rate, parts approval or vehicle inspection data appears in those sources, the generator fails until reviewed and intentionally redesigned for that stronger evidence—rather than silently promoting a questionable score.

**Next data collection work, not model priority:** complete the same original-component revision, failure-mechanism and market-supply worksheet for all critical systems across eligible configurations; import/normalize NHTSA complaints and DVSA inspection evidence with denominators and provenance; obtain manufacturer part chain and balanced real U.S. offers. Keep unmeasured rates and costs unknown.
