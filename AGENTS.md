# Working with the Saab database

## Complete engineering buying/repair batches



This repository records technical evidence for Saab specifications, replacement
analysis, and reliability-oriented model selection. It is not a calibrated vehicle
simulator or a source of verified failure probabilities.

- Read `README.md`, `docs/evidence-policy.md`, and `docs/data-contract.md` before
  changing records.
- Keep sources, applicability, units, and evidence status attached to every finding.
- Prefer original manufacturer/regulator documents. A mirror of an original
  document must identify the original publisher and its retrieval limitations.
- A year in a WIS URL is not by itself proof of model-year, engine, or market
  applicability. WIS pages can contain later revisions.
- Do not convert a supplier listing into verified fitment, physical stock, or
  demonstrated durability. Do not infer ECU/software compatibility from a plug
  that fits.
- Preserve contradictory source values as separate records and describe the
  missing information needed to resolve them.
- Do not silently equate RON with US AKI/AON, SAE hp with PS/EEC power, or service
  refill quantities with dry-fill quantities.
- Keep paraphrased findings and links here; do not add full third-party manuals,
  proprietary ECU binaries, or unlicensed copied datasets.
- Do not invent vehicle-instance values, VINs, inspection results, or calibration
  measurements.
- Run `python3 tools/validate.py` and `python3 -m unittest discover -s tests -v`
  after changing the data or validation tools. Inspect the full result.

## Completed engineering buyer dossiers

The first major buyer-focused batch is
[NG 9-3 B207/FA57 engineering batch 1](docs/research/ng93-b207-complete-purchase-dossier-20261014.md),
with [17 independent purchase/repair decisions](data/engineering-dossiers/ng93-b207-purchase-engineering-20261014.json).
New *engineering batches* should deliver complete buyer-useful evidence for a defined vehicle and
component family, including original factory fault/correction, exact application,
source-supported replacement, repair difficulty, parts/labor economics, inspection gates,
and explicit unresolved uncertainties. Avoid repeatedly replacing substantive work
with another record routing or gap counting audit. Preserve original issue IDs and
cross-link previously sourced records before researching new claims. A cost for
bare parts or ECU programming is **not** an all-in repair quote. A WIS repair
procedure or parts listing does not itself prove a common factory defect or
longer service life. Keep VIN/country/body/gearbox and safety scopes separate.

## Reuse-first requirement for research changes

Before adding a factory fault, component revision, part substitution, price observation,
or new gap, consult the [whole-repository reuse audit](docs/research-reuse-audit-20261014.md)
and run `python3 tools/audit_research_reuse.py --summary`.
Run `python3 tools/build_legacy_issue_index.py --check` and
`python3 tools/build_legacy_issue_index.py --find 'topic'` before recording an issue.
**Every saved issue must appear exactly once in the [reviewed legacy issue taxonomy](data/audits/legacy-issue-taxonomy-20261014.json).**
Never label a diagnostic, source conflict or part fitment warning as a documented
factory design mechanism; primary Saab/regulator documentation and scope required.
Search all existing datasets by original **source URL/bulletin number**, fault root cause,
source/issue/part/gap ID, and exact platform, market, model year, engine, body,
transmission and applicable VIN/serial scope.

A newly opened research PR must list the existing records reviewed, distinguish
what is genuinely new from evidence reused, and explicitly link prior issue IDs.
New comparison-ledger records must not be presented as newly discovered factory
failures when a matching original source or legacy issue already exists.

Do not automatically merge records based on shared URLs, part numbers, symptoms
or similarly worded gap titles. Different populations, factory corrections, test
conditions and campaign/TSB scopes can legitimately cite one document.
Keep existing source IDs stable and correct references rather than discarding provenance.
Update audit tests if the original ledger cohort list changes; no premature ranking.

## Reviewed part and research-blocker overlap

Run `python3 tools/check_part_gap_reconciliation.py --check --summary` before adding
a potentially duplicate part identity or repeating an unresolved source/VIN blocker.
Read [the overlap adjudication](docs/part-gap-overlap-adjudication-20261014.md).
Five same-number part groups retain separate factory/supplier original claims,
and two shared research gaps remain **open**. A matching number does not permit
broadening engine-number, market, transmission or VIN fitment; e.g., part 5961610
has conflicting original campaign and retailer engine-number conditions.
The system index records 32 additional manually reviewed issue navigation routes;
source quality and recall lookup cases may legitimately have **no physical system**.
When reviewing more ambiguous fact/gap routes, use `--review --review-kind gaps --review-limit 0`
or `--review --review-kind facts --review-limit 0` to avoid truncated review.
Read [the fact/gap navigation adjudication](docs/fact-gap-navigation-adjudication-20261014.md).
Add `--review-unreviewed-only` for the remaining work queue; deliberately reviewed
cross-cutting records must not be rediscovered as missing physical-system evidence.
Explicit fact/gap decisions carry original-record digests; review again when the
saved source-scoped record changes rather than merely refreshing its hash.

## Completed overlapping fact/gap navigation review

See [the final 225-record route review](docs/multisystem-fact-gap-route-review-20261014.md).
All previously flagged cross-cutting/multi-system fact and gap records have explicit
source-context navigation decisions with original-record SHA-256 digests. Run
`python3 tools/build_system_evidence_index.py --review --review-unreviewed-only --review-limit 0`
to confirm no **currently flagged** ambiguous routing is awaiting review.
A zero navigation queue does **not** close the 284 evidence gaps or certify
factory recall/TSB completeness, component life, original replacement compatibility,
manufacturer-directed OE supersessions or real parts purchase options. New
fact/gap claims and changed original records require fresh review before upgrading
their source status. Actual engine codes in unrelated titles are not extra faults.

## Sixteen-system evidence retrieval

Run `python3 tools/build_system_evidence_index.py --check --summary` before
beginning a new subsystem investigation. For a known part, source URL or issue,
use `--find 'part or subject'` or `--system engine_core_oil_pcv`.
Read the [system crosswalk](docs/system-evidence-crosswalk-20261014.md).
Every existing part record is assigned explicitly to a *navigation system* in
`data/audits/system-evidence-routing-policy-20261014.json`, and CI refuses new
unrouted parts. That assignment is **not** OEM approval or proof of stock.
Keyword/domain matches remain tentative; cross-cutting facts and gaps may have no
system ID without being research errors. Reuse sources and original applicability;
never count same-document references as independent evidence or model reliability.

## Engineering-first delivery: full decision batch, not index cleanup

For US/Canada NG9-3 B207 powertrain research consult the [single completed 17-case
purchase and repair dossier](docs/research/ng93-b207-complete-purchase-dossier-20261014.md),
the [buyer worksheet](docs/research/ng93-b207-2003-2011-buyer-inspection-worksheet.md)
and the [source-linked decision register](data/engineering-dossiers/ng93-b207-purchase-engineering-20261014.json)
**before** researching a previously documented factory bulletin again.
Run `python3 tools/check_ng93_engineering_batch.py --check --summary` when
changing this dossier. Future batches should be scoped by real vehicle/engine/
gearbox configuration and cover major faults, factory revisions, original
parts, current proven options, DIY complexity, full-economics blockers and
specific buyer tests **in one usable delivery**. A source-supported replacement
path alone is not a measured reliability improvement or factory defect frequency.
Do not recast historical supplier stock and price displays as current delivered
quotes. Keep high-cost engine/head/gearbox decisions distinct from repairable
software, sensors and hoses. Do not silently shift the dossier into the original
research dataset census; it is a derived purchasing-analysis product with direct
factory/source URLs and legacy identifiers, not a replacement for original facts.
