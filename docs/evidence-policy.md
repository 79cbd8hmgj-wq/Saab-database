# Evidence policy

## Three evidence statuses

| Status | Meaning | Does not establish |
| --- | --- | --- |
| `documented` | The named source directly states the finding. | That it applies to every car in a broad year range, or that an individual car is healthy. |
| `supplier_claim` | A manufacturer/supplier makes the stated product or performance claim. | Independent validation, live stock, or a measured durability improvement. |
| `inference` | A reasoned interpretation or project judgment uses the cited sources. | A factory-approved substitution or a measured outcome. |

Evidence status describes the basis of the claim, not a numerical probability of
correctness or failure. A faithfully recorded specification can still have
unresolved vehicle applicability.

## Retrieval strength

- `full_text`: the relevant document/page text was retrieved and inspected.
- `partial`: only part of the document or relevant page was available.
- `search_excerpt`: the finding was available in an indexed search excerpt; the
  source is retained, but full-document review remains outstanding.
- `metadata_only`: only identity, catalogue metadata, or an external resource's
  description was available. Do not derive undisclosed technical specifications
  from it.

An original Saab document hosted by a third party remains a factory-authored
document. The hosting site is not represented as the original publisher. A forum
reproduction is weaker retrieval provenance and should be labeled as such rather
than silently substituting for the original.

## Applicability is a contract

An explicit engine code, chassis/VIN boundary, body style, gearbox code, market,
or component serial number can change a finding's applicability. Unknown scope
must stay unknown. Factory US manuals and generic European WIS tables may use
different ratings and conventions. The year path in WIS is organizational evidence,
not a guarantee that the table is a frozen copy of that year's production data.

Capture the source's labels. Keep VIN fragments as fragments; do not expand an
eight-character chassis suffix into an invented full VIN. Never compare VIN ranges
lexicographically as though every market and body style shared one numeric sequence.

## Quantities and units

Retain the original unit and definition. Record oil drain/refill and total-system
capacity separately. Distinguish gearbox case codes from marketing names. Preserve
wheel diameter, disc diameter, and disc thickness as separate quantities. Identify
reference temperature, engine speed, load, or test condition when a specification
depends on them.

Conversions may be added only as separate calculated records with the input,
formula, and rounding assumptions. They must not replace an original value or
resolve a disputed specification by appearance alone.

## Contradictions

Store conflicting source statements separately, identify their source and scope,
and create a gap record. Resolving the contradiction requires stronger application
information or a measurement, not majority voting across copied websites.

## Reliability and simulation

Documented failure mechanisms and factory corrections support risk-based analysis.
They do not supply fleet failure rates, mileage-to-failure predictions, or a claim
that a model matches Toyota's long-term dependability. Diagnostic logs may contain
ECU-calculated quantities rather than independent measurements.

Every numerical model needs explicit parameters, assumptions, operating conditions,
and verification against appropriate observations. A generic model is not a
Saab-calibrated model. Fitment, brake/suspension adequacy, fatigue strength, and
durability each require evidence appropriate to that question.
