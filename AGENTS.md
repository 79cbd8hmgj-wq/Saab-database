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
