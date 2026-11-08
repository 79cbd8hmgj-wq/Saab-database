# SaabWISOnline importer — Stage 4 handoff

Status: **offline-tested research prototype; no live site extraction or authorization verified.**

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