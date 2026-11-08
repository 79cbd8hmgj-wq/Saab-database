# SaabWISOnline extraction prototype (Stage 5)

This is a **read-only, unverified site integration prototype**. It is not an authoritative service manual, complete parts catalog, or fitment approval. The Python modules require no third-party dependencies.

## Modules

- `wis_indexer.py`: fail-closed robots check, same-host URL canonicalisation, per-hop redirect validation, **soft-404 detection** (the site answers a missing document with a 302 to its parent directory), retry/backoff with `Retry-After`, duplicate-content and slash-variant handling, refuse-overwrite output, `--dry-run`.
- `wis_candidates.py`: grid-based (colspan/rowspan) table reader. Extracts review-only candidates from Nm/lbf-ft torque tables and `label | unit | value` tables; classifies DTC tables, applicability matrices, procedure steps, notes and bullets; everything else is preserved as `review_required` or `unsupported_tables`. Records carry `info_class` A/B/C, engine/chassis boundaries exactly as printed, and original value/unit text.
- `wis_reconcile.py`: no-write comparison with `data/datasets/*.json` using the real fact shape (entity subjects, object values, null units, locator labels). Reports possible duplicates, potential conflicts and cross-source overlaps; never decides equivalence.
- `wis_pipeline.py`: checkpointed pilot (collect -> offline extract -> reconcile -> report). Resumable, bounded, never writes inside `data/`, `docs/` or `tests/`, never claims coverage.

All candidates stay `review_only`. A model-year path is never treated as engine, market or VIN applicability.

## Tests

```bash
python3 -m unittest discover -s tools/saab_wis_prototype/tests -v
```

Fixtures in `tests/fixtures/*_excerpt.html` are **trimmed structure excerpts** of genuine pages (a few rows each, styling and site chrome removed, original URL in the header comment). They are not copies of the manuals. `examples/synthetic.html` and the Stage 3 table HTML remain synthetic.

## Controlled pilot (needs network access to saabwisonline.com)

```bash
python3 tools/saab_wis_prototype/wis_pipeline.py --dry-run --state-dir /path/outside/repo/wis-state
python3 tools/saab_wis_prototype/wis_pipeline.py --state-dir /path/outside/repo/wis-state --max-pages 80 --delay 3
python3 tools/saab_wis_prototype/wis_pipeline.py --state-dir ... --resume ...     # after an interruption
python3 tools/saab_wis_prototype/wis_pipeline.py --state-dir ... --analyse-only --run-name v2   # offline re-analysis
```

Raw cached HTML lives only in `--state-dir` and must not be committed. Output files are never overwritten. The counts-only result of the 2026-11-08 run is `pilot/2008-9-5-cooling-system-summary.json`.

## Offline extraction of a single locally saved page

```bash
python3 tools/saab_wis_prototype/wis_candidates.py --html-file page.html --source-url '<wis url>' --output review.json
python3 tools/saab_wis_prototype/wis_reconcile.py --repo-root . --review-file review.json --output reconciliation.json
```

## Access findings (2026-11-08)

- `robots.txt`: `User-agent: *`, `Disallow: /docs2`, `Allow: /`; the sitemap named there is on another host (`v2.saabwisonline.com`) and was **not** collected.
- Pages are static HTML (`text/html`, Apache). Directory URLs 301 to a trailing-slash form; documents have no slash; missing documents 302 to the parent directory.
- No collection or redistribution terms were found on the pages examined (home, listings, documents; footer carries a donation/membership notice). **Absence of a published prohibition is not permission to republish.** Contact the site operators before any larger collection or any republication of text or diagrams.
- Shared hosting-side limits are unknown; the pilot used one request every 3 s and 73 requests in total.

## Known limitations

- Only the 2008 9-5 cooling-system subtree has been exercised against live HTML. Other systems, platforms and years are untested.
- Procedures, wiring diagrams, images, special-tool matrices and symptom pages are *classified*, not extracted.
- A listing-page inventory is not an independent inventory; coverage is never claimed.
- Group-header and multi-line pairing are interpretations (`info_class` B); engine/chassis boundaries and fitment need human verification (`info_class` C).
- Reconciliation labels are token heuristics; **no match does not mean new** (see `candidates_unmatched_but_source_has_existing_facts`).
- Database facts, applicability rules and supplier interchange claims are never changed automatically.
- Integration must comply with `docs/data-contract.md` and `docs/evidence-policy.md`.

## Next

See the "Next technical milestone" in `docs/saab-wis-indexer-stage4-handoff.md`.
