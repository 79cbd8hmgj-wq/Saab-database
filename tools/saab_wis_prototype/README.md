# SaabWISOnline extraction prototype (Stage 4)

This is a **read-only, unverified site integration prototype**. It is not an authoritative service manual, complete parts catalog, or fitment approval. The Python modules require no third-party dependencies.

## Modules

- `wis_indexer.py`: a bounded metadata indexer for a specific Saab model and model year, with fail-closed robots.txt check, same-host URLs, max-page limit and request delay.
- `wis_candidates.py`: offline HTML table parser for numeric specification **review candidates**, with units, source URL and locator. Three-column Nm/lbf-ft torque tables support simple numeric rows; ambiguous rows are skipped.
- `wis_reconcile.py`: offline comparison of candidate rows against the repository's existing `data/datasets/*.json`, identifying existing source URLs, possible matches and possible numeric conflicts.

All generated candidates remain `review_only`; a page's model-year path is never treated as exact VIN applicability.

## Run tests

From repository root:

```bash
python3 -m unittest discover -s tools/saab_wis_prototype/tests -v
```

Previously the source package passed 22 offline tests. The GitHub copy still needs CI verification.

## Offline extraction (using authorized, locally obtained HTML)

```bash
python3 tools/saab_wis_prototype/wis_candidates.py \
  --html-file saved-wis-page.html \
  --source-url 'https://saabwisonline.com/9-5-9600/2008/2-engine/cooling-system/technical-data/tightening-torques' \
  --output wis-review.json

python3 tools/saab_wis_prototype/wis_reconcile.py \
  --repo-root . \
  --review-file wis-review.json \
  --output wis-reconciliation.json
```

Output filenames must not already exist; review writers refuse overwrites.

## Limited indexing

**Do not run a live collection** until the site's permissions, robots.txt availability, and load expectations have been reviewed. If authorized, use a small page limit:

```bash
python3 tools/saab_wis_prototype/wis_indexer.py \
  --start 'https://saabwisonline.com/9-5-9600/2008/2-engine/basic-engine-4-cylinder-petrol/technical-data/' \
  --max-pages 5 --delay 3 \
  --output wis-manifest.json
```

The indexer captures metadata and link fingerprints, not full copyrighted page text. Be aware that `robots.txt` is not itself copyright or bulk-scraping permission.

## Known limitations

- No actual raw HTML from the site was available for development.
- Synthetic fixtures demonstrate parser behavior, not live correctness.
- Site terms, crawl permission and rights to redistribute text/diagrams remain unverified.
- The parser doesn't reliably interpret merged table cells, complex procedure structures, wiring diagrams, or image-only information.
- Database facts, applicability rules, and supplier interchange claims are never automatically changed.
- Integration must comply with `docs/data-contract.md` and `docs/evidence-policy.md`.

## Next

1. Audit access and obtain a small number of authorized real HTML samples.
2. Add regression fixtures and tests for those exact structures without republishing copyrighted full documents.
3. Run tests against the repository and inspect candidate review JSON.
4. Only then evaluate a larger indexing pilot and a supervised import process.

See `docs/saab-wis-indexer-stage4-handoff.md` for history and scope.
