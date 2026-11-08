# SaabWISOnline importer — Stage 4 handoff

Status: **Stage 5 - validated against genuine 2008 9-5 cooling-system HTML (62 documents); not production-ready; bulk-collection permission not established.**

This development branch is intentionally separate from canonical datasets. Do not merge as a production WIS importer until real HTML and access policy have been verified.

## Existing prototype

Four development stages were completed in the ChatGPT Saab Project Car conversation on 2026-11-08. The original Stage 4 package is `saab_wis_indexer_stage4.zip` and includes:

- `wis_indexer.py`: bounded read-only document navigation indexer
- `wis_candidates.py`: conservative numeric and torque specification candidates
- `wis_reconcile.py`: duplicate source and possible fact/conflict matching
- `tests/test_wis_indexer.py`, `test_wis_candidates.py`, `test_wis_stage3.py`, `test_wis_reconcile.py`
- `examples/synthetic.html`: synthetic example only

The full local test suite previously ran as `python3 -m unittest discover -s tests -v`, with 22 tests passing. These are offline tests; there was no real SaabWISOnline HTML end-to-end test.

## Source-of-truth rules

Follow `docs/data-contract.md` and `docs/evidence-policy.md`. Existing `data/datasets/*.json` remain untouched. Never automatically promote parser output to `documented` factory facts. Preserve year, market, engine, gearbox, and chassis/VIN limitations exactly.

## Next work (Claude/local execution only after site access review)

1. Inspect website robots rules and terms; request publisher approval for sustained collection if needed.
2. Retrieve a small, permitted set of real HTML documents from 2008 Saab 9-5.
3. Check the existing prototype against raw HTML rather than reconstructed fixtures.
4. Fix parsers under tests; produce review-only JSON and a documented failure report.
5. Reconcile against existing sources/facts; prevent duplicate or contradictory import.
6. No automatic broad crawl or canonical dataset modifications.

## Integration note

This handoff file records verified development scope; **the three Stage 4 Python modules and all four original test files have been transferred to this branch**. The exact original ZIP remains available in the ChatGPT conversation. Real SaabWISOnline HTML and end-to-end website verification are still outstanding.

The active research database remains on `main`.
## Stage 5 outcome (2026-11-08)

- Original 22 tests reproduced on the transferred code: 22/22 pass. Now 95 tests (original 22 unchanged).
- Genuine pages were fetched (robots permits; 73 requests at 3 s spacing, all HTTP 200 after directory redirects). The Stage 4 extractor had real defects on them:
  - **Silent wrong data**: engine-number-bounded torque rows (4 cells) were dropped, leaving only the "from engine no. 7011079" value (21 Nm) and losing the "up to and including 7011078" value (20 Nm). Fixed by a column-grid model; both revisions are kept separately with boundaries preserved.
  - Missing documents answer 302 to the parent directory and would have been indexed as the parent. Fixed (`soft_404_redirect`).
  - Redirects were followed before validation; reconciliation never matched real facts (entity subjects, object values, null units). Fixed.
- Pilot (`tools/saab_wis_prototype/pilot/2008-9-5-cooling-system-summary.json`, counts only): 11 listing pages, 62 documents retrieved and parsed, 32 review-only candidates from 4 pages (tightening torques 16, fan motor 8, temperature/pressure limits 7, coolant 1; info class A 18 / B 12 / C 2), 7 candidates on already-cited sources (2 possible duplicates of existing facts, 0 conflicts, 5 unmatched although the source has existing facts), 12 review-required rows, 8 documents with partly unsupported structure, 0 errors.
- **Coverage is not claimed**: the inventory comes from navigation listings only; the sitemap host is outside the allowed scope.

## Next technical milestone

Obtain written permission (or terms) from the SaabWISOnline operators, then run the pipeline for the 2008 9-5 `2-engine/basic-engine-4-cylinder-petrol` subtree, where most existing repository sources live. Priorities there: cross-check existing facts' stated values against the new candidates, extend the `label | unit | value` reader to compound cells (`°C (°F) bar`) with explicit multi-measure fields, parse procedure-step/torque sequences (multistage angles) as ordered records, and add an independent inventory source (the sitemap) so a coverage statement becomes possible.
