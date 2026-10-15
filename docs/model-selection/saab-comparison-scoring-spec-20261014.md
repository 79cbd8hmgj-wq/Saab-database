# Saab configuration comparison model v0.1

Purpose: compare purchase candidates by reliability, parts sourcing (including cross-brand OEM), and complete repair cost. Scope initially original 9-5 (9600) B205/B235 and 9-3 (9440) B207 FWD. Exclude 9-5 (9650).

## Unit of comparison

Use model generation + model year + body + engine code + transmission code + drive configuration + market. Preserve exact VIN/chassis for individual offers. Do not average FA57 risk into every 9-3 or transfer B235 PCV to B207.

## Dimensions (proposed weights, not measured scores)

Reliability 40%; parts availability 30%; repair economics 30%. Publish each independently, then an optional weighted overall score **only when minimum evidence is met**.

Reliability components: frequency/exposure where supported, severity, preventative correction availability, consequence of failure, and durability after correction. Unknown fleet frequency stays null; never fabricate a failure probability.

Parts components: genuine Saab supply, aftermarket supply, verified cross-brand OEM identity, exact donor interchange, geographic availability, fulfillment and lead time. Distinguish official same-number SKU from untested donor conversion; a supplier catalog cross-reference alone is not fitment approval.

Economics components: diagnostic cost, parts, shipping/tax, seals/fluids, specialty tools, machine shop, programming, outsourced labor, towing, collateral damage and contingency. Separate DIY cash spend from professional installed total. Report intervals and assumptions, not invented single totals.

## Evidence and missing-data rules

Each metric stores value, evidence source, observation date, fitment scope, confidence, and status (verified, supplier_claim, hypothesis, unknown). Store unknown as null, not zero or average. Never award a high score for absence of reported failures. For a composite, require sufficient coverage of high-consequence powertrain, structural, braking, electronics and cooling systems. Otherwise publish dimension-level evidence and 'not rankable'.

## Repair scenario structure

Each vehicle configuration has issue scenarios with: failure mode, severity, probability estimate if defensible, inspection test, preventative action, replacement part options (Saab / aftermarket / cross-brand OEM / donor), interchange approval, labor hours source, required tools, full cost components, and post-repair residual risk. Separate one-time baseline restoration budget from expected annual repairs and worst-case major repair exposure.

## Initial comparison cases

- 9-3 (9440) B207 FWD, gearbox-specific: intake-valve cold compression loss; T8 ECM; gear-driven pump 12630084; early FA57 cooler only if chassis/gearbox eligible.
- Original 9-5 (9600) B205/B235: early PCV/sludge only within bulletin scope; T7 cassette 32022255; automatic radiator 32019620 only if applicable; starter 32101497; body-side rear subframe anchor corrosion on SportCombi.

## Required outputs

1. Side-by-side comparison with three separate dimension scores and evidence completeness.
2. Component-by-component Saab / GM / Opel / other OEM cross-reference matrix, marking verified identity versus speculative interchange.
3. Baseline restoration estimate, routine maintenance estimate and catastrophic repair exposure as distinct values.
4. Individual listing worksheet that overrides configuration defaults with observed condition, VIN, seller price and quotes.
5. Explainable ranking: every score must trace to sourced issue records and cost assumptions.

Existing source research: docs/research/ng93-b207-complete-purchase-dossier-20261014.md; docs/research/og95-b205-b235-complete-purchase-dossier-20261014.md; docs/research/us-retail-parts-supply-snapshot.md; docs/research/cross-manufacturer-gm-saab-b207-water-pump.md.
