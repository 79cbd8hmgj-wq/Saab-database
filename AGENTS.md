# Working with the Saab database

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
