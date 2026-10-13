# Reproducible United States Saab production catalogue

**Scope:** Original United States-market **Saab 9-3 and 9-5**, **1998–2011 model years**, **factory automatic**, **FWD**, **nonconvertible** sedan, hatchback or wagon. Canadian records remain in the existing North American catalogue and are **not a prerequisite** to this U.S. research.

## Source and limitations

The four eSaabParts [U.S. production tables](https://www.esaabparts.com/saab/production/) cover Saab **9-3 9400 (1999–2003)**, **9-3 9440 (2003–2011)**, **9-5 9600 (1999–2009)** and **9-5 650 (2010–2011)**. They are **third-party compiled production tables**, not factory VIN certificates, factory sales-option approvals, or vehicle reliability records. These tables list paint-level rows with production counts, sometimes very small. We must not call their grand totals numbers of eligible automatic cars.

The importer at `tools/us_production_import.py` uses Python standard-library HTML parsing and maps each paint-level source row to exactly one combination of **model, platform, year, trim, body, transmission, drive and engine**. It then sums `Produced` values **only within that key**, and exports a distinct U.S. candidate row per observed combination. The labels and source-reported counts remain unverified against original manufacturer VIN data. Source-reported groups of 12 or fewer units carry an explicit low-volume manual-review flag.

Filters are deliberately strict: it **rejects all manual cars, convertibles and AWD/XWD**; accepts only recognizable four-, five- and six-speed automatic labels; keeps original 9-3 **9400** five-doors as **hatchbacks** and second-generation 9-3 **9440** and 9-5 **9600** five-doors as **wagons**; does not infer engine codes for the second-generation 9-5 shorthand `2.0T`/`2.8T`; and has no way to turn blank/unknown combinations into supposed factory cars.

## Reproduce

Run the full normalization online (makes four outbound HTTPS requests):

```sh
python3 tools/us_production_import.py --fetch \
  --require-total-reconciliation \
  --output data/vehicle-catalogue/us-production-normalized.json
```

Alternatively, save each HTML table with its original filename and run offline:

```sh
python3 tools/us_production_import.py --html-dir ./saved-esaab-tables \
  --require-total-reconciliation \
  --output data/vehicle-catalogue/us-production-normalized.json
```

The `--require-total-reconciliation` mode checks whether each table's displayed all-model `Total US Production` equals the sum of its extracted **paint rows, including excluded vehicles**. A mismatch fails closed instead of silently publishing incorrect totals. **This is a parser-consistency test, not manufacturer verification.**

The companion offline unit tests run with:

```sh
python3 -m unittest tests.test_us_production_import -v
python3 -m unittest discover -s tests -v
python3 tools/validate.py
python3 tools/phase0_audit.py --check
```

A one-shot branch workflow in `.github/workflows/us-production-import.yml` generates and tests the snapshot from the live tables. The JSON under `data/vehicle-catalogue/` is separate from `data/datasets/`, so neither existing fact counts nor Phase 0 research gates are artificially inflated.

## Acceptance conditions before declaring U.S. catalogue complete

1. All four input tables parse and source **all-vehicle paint-count sums** reconcile (without counting prohibited vehicles as eligible).
2. Every retained row has **US, automatic, FWD, nonconvertible** proof in the compiled register, with a year/platform/trim/engine/body and an immutable source URL. Low-volume or anomalous trim/engine combinations remain subject to OEM verification.
3. The official original Saab model-year US sales and VIN documents are checked independently against each unusual combination, and model/year absences are not inferred merely from absent third-party rows.
4. Original engine and **physical automatic transmission family** codes are verified separately before any fitment or durability recommendation; e.g. `5AT` is not a transmission serial/type designation.
5. This source-derived matrix is reconciled against `north-america-1998-2011.json` to avoid double-counting overlapping original research records. Existing Canada research must remain untouched.
6. No reliability, engine/transmission rebuild avoidance, affordability or interchange claims follow automatically from production count alone.

**Gate status unchanged:** Phase 0 Gate A remains partial; Gates B/C remain unmet until the separate failure, safety, repair and parts criteria are satisfied.
