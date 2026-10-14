# Saab component reliability and parts-availability evidence — before any tier list

**Status: research framework only. No ranked models, preliminary winner, grades, weights, invented failure rates, or model elimination.** Date: 2026-10-14.

This research should eventually support a **high-confidence, reproducible comparison of Saab configurations**, not a predetermined "best Saab" narrative. The neutral [machine-readable protocol](../data/tier-research/methodology.json), [blank original-component and repair record](../data/tier-research/component-evidence-template.json), and [110-group U.S. crosswalk](../data/tier-research/us-110-evidence-readiness.json) are the initial inputs.

## Comparison unit, universe, and fairness

"2008 Saab 9-5" is not a sufficient unit: body, original engine and engine revision, gearbox and gearbox adaptation, market/emissions rules, factory drivetrain, build/VIN boundaries, and original installed options may change both defect exposure and parts sourcing.

The **110 source-derived groups** already stored in the repo are U.S., original 9-3 / 9-5, automatic, FWD, nonconvertible, model years 1998–2011. They **do not represent all production, current surviving vehicles, or all variants**, and the factory accuracy of the third-party compiled group list remains unverified. In particular manual gearboxes, AWD/XWD, convertibles, original 9-2X/9-7X/9-4X, original Canada-only options and other-market Saabs are **not evaluated** by this crosswalk. Existing personal shopping restrictions should not silently become a rule that a completely unresearched model is mechanically inferior. Any broader tier-comparison scope must be explicitly defined **before** claims of fair coverage.

The existing higher-density 9-5 B235 / 9-3 B207 work is a **research pilot, not a model ranking or preferred ownership shortlist**. It cannot win simply by having more factory documents.

## Four independent dimensions: never substitute one for another

| Dimension | Evidence to collect | What is not evidence |
| --- | --- | --- |
| **Original factory component reliability** | Installed original part and revision; dated defect mechanism, affected build range, original and later countermeasure; independent observed failure exposure where possible | A TSB means the part fails in every vehicle; anecdote counts are population probability |
| **Real replacement availability** | VIN/build-scoped OE number; official direction of supersession; separately labeled third-party compatible SKU; dated U.S. actual fulfilment, seller diversity, delivery delay, tax/core/warranty and end-of-life supply | A historical e-commerce page proves stock today; an aftermarket catalogue reference proves original-OE donor interchange |
| **Documented model-specific failures** | Exact engine/gearbox/body/build; diagnostic signs; factory or regulator findings; likelihood only if statistically supported; safety, stranding, repair/repeat severity and whether a production fix exists | Count of recall notices or web complaints equals recurrence rate |
| **Repairability and true cost** | Real factory tools and software, DIY safety/access feasibility, what can be replaced without internal engine/gearbox rebuilding, full parts+fluids+tools+labor+shipping+towing+programming cost | Price of one component or an original warranty labor allowance is a complete 2026 repair quote |

The sixteen explicit subsystems in the JSON method apply to every comparable configuration. Corrosion should also be **body style and climate adjusted**, rather than an independent motor or gearbox defect assumption. Maintenance history and vehicle mileage are covariates, not punishments applied to one specific model.

## A defensible failure-rate standard

1. **Denominator:** the actual at-risk vehicle/component population with the same production hardware and time interval. Cumulative original production is *not* current in-service exposure.
2. **Event definition:** distinguish one recurring repair, a second owner description of the same event, a different failure of the same system, and independent vehicles. Distinguish an alleged fault from a diagnostically verified one.
3. **Exposure:** calendar years, odometer, annual driving, climate/road salt, driving and service practices, service-bulletin revision date, warranty coverage and retirement/scrap time.
4. **Ascertainment:** recall campaigns, dedicated specialist repair shops, online forums and NHTSA ODI complaints recruit very different samples. Each creates selection bias. Account for censoring and survivor bias where individual cohort data exist.
5. **Uncertainty:** retain sample size, original source, calculation, confidence interval or caveats; if denominator and measurement are unavailable, store **frequency: null**, never zero or an invented high/medium/low numerical risk.

Failure *mechanism* is useful even without frequency. It can inform inspection and preventable repairs, but it must **not** turn into an unfounded percentage or severity-adjusted rank.

## Official external sources with distinct roles

- [NHTSA Datasets and APIs](https://www.nhtsa.gov/nhtsa-datasets-and-apis): U.S. ODI consumer complaint descriptions/IDs, investigations, original manufacturer service-bulletin and recall sources. Useful for discovering allegations and proven safety campaigns; **complaint counts alone cannot establish model failure rates**. The public complaint API groups by make/model/model-year, usually **not factory engine, transmission or part revision**, so decoded configuration attribution needs independent support.
- [UK DVSA anonymised MOT data](https://open.data.dvsa.gov.uk/mot-anonymised/index.html): actual test outcomes, make/model, odometer and reasons for failure. Potentially informative on aged brake, steering, suspension, corrosion and lighting among **vehicles surviving to inspection**. Do not transfer UK climate, engines, inspected survivor rates or test-regime definitions directly to North American powertrain failure probabilities. Test definitions changed in 2018.
- [Saab Parts / Hedin subscription tools](https://saabparts.com/saab-subscription-services): original WebEPC VIN/build selection, factory supersession and restrictions, WebWIS instructions, TIS2WEB programming. Official access can be **paid**. A supplier's statement that a SKU "supersedes" another is not a Saab-authorized direction unless manufacturer records confirm it.
- Independently dated U.S. supplier listings: exact SKU, manufacturer label, warehouse confirmation, promised lead time, tax/shipping/core/warranty. A listing remains a **claim**, not a fulfilled order or demonstrated durability. Track at least one competing seller where possible; multiple listings from the same supply chain are not independent stock.
- Matched warranty/fleet or verified workshop repair records when accessible: can quantify failures only when unit exposure and event definition are known. Otherwise use as case studies, never inferred fleet rates.

**No new NHTSA case extraction, UK MOT Saab sample, actual supplier order, or VIN-filtered EPC result is claimed in this PR.** These are research-access paths, not imported failure data.

## Why the new crosswalk deliberately contains empty answers

The existing U.S. feasibility audit reports **110/110 with at least one linked scenario**, but **zero quantified failure rates, zero verified repair prices and zero approved interchange parts**. The existing parts/tool audit reports **110/110 job research leads**, **not** 110 fully verified repairs.

Our generated 110-group table preserves the existing IDs and source leads and sets **all four comparative dimensions to \`not_audited_for_comparable_population_and_part_evidence\`**. This does *not* deny that the broader repo has useful factory research. It says research leads have not been quality-audited into a comparable **tier input**.

This status must not be algorithmically promoted by adding records. There are no provisional numeric ratings.

## Evidence capture standard for every problem or component

Record in [component-evidence-template.json](../data/tier-research/component-evidence-template.json):

1. Production cohort: original platform, model year, model, market, engine, gearbox, body, serial cutover and source.
2. Failure: original part/revision, mechanism, symptoms, confirmed test, affected population, engineering correction and whether recurrence is possible after repair.
3. Evidence quality: source URL/document/page/retrieval date, primary vs secondary, independent corroboration, complaint/warranty/inspection data classification, confidence limitations.
4. Frequency: measured events, at-risk denominator, exposure and selection methodology—or **null**.
5. Replacement: original OE and directed WebEPC chain; manufacturer, brand, aftermarket and cross-brand claims **kept separate**; dimensions/connectors/firmware/safety hardware; VIN/case approval.
6. Supply: date, merchant, country/warehouse, exact variant, stock interpretation, delivered quote, competing suppliers and likely discontinuation; no future stock assumptions.
7. Repair: safe access/tools/software/competency, preventive action versus replacement of an already damaged component; complete realistic DIY and specialist cost with uncertainty.
8. Conflicts and gaps: inconsistent sources stay distinct, with exact missing proof to resolve.

## Research exit conditions — not numerical thresholds

A tier decision becomes worth discussing only when the comparison universe has been accepted; the same key systems and common-failure questions have been searched for **all comparable cohorts**; missing facts are transparent; the known dangerous/expensive cases have a documented diagnostic and repair/avoidance pathway; the essential replacement options have credible US delivered availability and fitment; original component revisions are accounted for; and any frequency claim includes exposure and a defensible denominator.

If representative quantitative failure-frequency evidence remains unavailable, the final output may be a **well-sourced qualitative ownership/repairability tier with explicit confidence**, but it must *not* pretend to be a highly accurate statistical durability ranking. The choice between partial qualitative tiers and further research comes later, not in this phase.

## Run and extend

\`\`\`sh
python3 tools/build_tier_evidence_readiness.py --check
python3 -m unittest discover -s tests -v
python3 tools/validate.py
python3 tools/phase0_audit.py --check
\`\`\`

The crosswalk generator only reads existing production, repair scenario, parts/tool audits and the neutral protocol; it does **not** change the Phase 0 research evidence census, vehicle eligibility rules, source datasets, scoring settings or factory parts claims. Add a new research cohort when its basic source-backed identity is established, and adjust the generator with explicit review. Never silently expand the denominator.
