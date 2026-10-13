#!/usr/bin/env python3
"""Reproducible Phase 0 coverage snapshot; record counts are NOT vehicle readiness scores."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from coverage import KINDS, SCOPE_FIELDS, census, scopes
from database import ROOT, load_datasets, validate_datasets

SNAPSHOT = ROOT / "data" / "phase0-coverage-snapshot.json"
AUDIT_DOC = ROOT / "docs" / "coverage-audit.md"
BEGIN = "<!-- BEGIN AUTO-GENERATED PHASE0 CENSUS -->"
END = "<!-- END AUTO-GENERATED PHASE0 CENSUS -->"


def build_snapshot(datasets: list[dict]) -> dict:
    """Derive all numeric census results directly from the checked-in records."""
    totals = census(datasets)
    records = [r for d in datasets for kind in KINDS for r in d[kind]]
    parts = [p for d in datasets for p in d["parts"]]
    return {
        "schema_version": "1.0.0",
        "meaning": "Record coverage and evidence provenance, NOT completeness, fitment, or reliability",
        "counts": totals["counts"],
        "unique_source_urls": totals["unique_source_urls"],
        "retrieval_statuses": totals["retrieval"],
        "evidence_statuses": totals["evidence"],
        "explicit_scope_counts": {
            field: sum(
                any(bool(scope.get(field)) for scope in scopes(record))
                for record in records
            )
            for field in SCOPE_FIELDS
        },
        "platform_year": totals["platform_year"],
        "domain_counts": {
            d["domain"]: {
                key: len(d[key]) for key in ("sources", "facts", "issues", "parts", "gaps")
            }
            for d in sorted(datasets, key=lambda dataset: dataset["domain"])
        },
        "parts_provenance": {
            "total": len(parts),
            "with_relationships": sum(bool(p["relationships"]) for p in parts),
            "supplier_claim": sum(p["evidence_status"] == "supplier_claim" for p in parts),
            "needs_vehicle_verification": sum(
                p.get("review_status") == "needs_vehicle_verification" for p in parts
            ),
        },
    }


def render_census(snapshot: dict) -> str:
    """Produce the only count-bearing part of the human-readable audit."""
    counts = snapshot["counts"]
    lines = [
        BEGIN,
        "## Current database snapshot (automatically verified)",
        "",
        "| Measure | Current records |",
        "| --- | ---: |",
        f"| Research domains | {len(snapshot['domain_counts'])} |",
        f"| Source records | {counts['sources']} |",
        f"| Unique source URLs | {snapshot['unique_source_urls']} |",
        f"| Technical facts | {counts['facts']} |",
        f"| Diagnostic/correction issues | {counts['issues']} |",
        f"| Part records | {counts['parts']} |",
        f"| Explicit open research gaps | {counts['gaps']} |",
        "",
        "A repeated URL is not independent corroboration. These are stored record counts,",
        "**not** estimates of system completeness, part fitment confidence, failure rates,",
        "or the probability that an individual vehicle is repairable.",
        "",
        "### Source retrieval and evidence",
        "",
        "| Source retrieval | Records |",
        "| --- | ---: |",
    ]
    for label in ("full_text", "partial", "search_excerpt", "metadata_only"):
        lines.append(f"| `{label}` | {snapshot['retrieval_statuses'].get(label, 0)} |")
    lines.extend(["", "| Technical evidence | Facts + issues + parts |", "| --- | ---: |"])
    for label in ("documented", "supplier_claim", "inference"):
        lines.append(f"| `{label}` | {snapshot['evidence_statuses'].get(label, 0)} |")
    lines.extend([
        "",
        "### Explicit application dimensions",
        "",
        "A record may legitimately lack a dimension when its source is general. Missing",
        "dimensions are **unknown**, never a blanket approval. Grouped applicability",
        "is counted from individual groups, not from a misleading top-level union.",
        "",
        "| Scope field explicitly present | Records out of facts + issues + parts |",
        "| --- | ---: |",
    ])
    denom = sum(counts[k] for k in KINDS)
    for label in SCOPE_FIELDS:
        lines.append(f"| `{label}` | {snapshot['explicit_scope_counts'][label]} / {denom} |")
    lines.extend([
        "",
        "### Factory-source record coverage by original Saab model year",
        "",
        "Only facts/issues/parts with the **same applicability group** specifying both",
        "platform and year are counted. Repeated records can appear in more than one",
        "model-year row. Year-path names do not prove a given production revision.",
    ])
    for platform, caption in (
        ("9-5-9600", "Original 9-5, platform 9600"),
        ("9-3-9440", "Second-generation 9-3, platform 9440"),
    ):
        lines.extend([
            "",
            f"#### {caption}",
            "",
            "| Model year | Facts | Issues | Parts |",
            "| ---: | ---: | ---: | ---: |",
        ])
        for year, row in snapshot["platform_year"][platform].items():
            lines.append(
                f"| {year} | {row['facts']} | {row['issues']} | {row['parts']} |"
            )
    p = snapshot["parts_provenance"]
    lines.extend([
        "",
        "### Parts evidence does not equal approved interchange",
        "",
        "| Part-record metric | Count |",
        "| --- | ---: |",
        f"| Records in research database | {p['total']} |",
        f"| Have at least one recorded part relationship | {p['with_relationships']} |",
        f"| Supported as a supplier claim | {p['supplier_claim']} |",
        f"| Explicitly marked as needing vehicle verification | {p['needs_vehicle_verification']} |",
        "",
        "A relationship can be an aftermarket cross-reference, kit contents, or a",
        "conditional supersession. Its existence does **not** make the replacement",
        "VIN-approved, bidirectional, or suitable for a safety-critical repair.",
        "",
        "### Distribution of recorded evidence by research domain",
        "",
        "| Dataset domain | Sources | Facts | Issues | Parts | Gaps |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ])
    for name, row in snapshot["domain_counts"].items():
        lines.append(
            f"| `{name}` | {row['sources']} | {row['facts']} | {row['issues']} | "
            f"{row['parts']} | {row['gaps']} |"
        )
    lines.extend(["", END])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--format", choices=("json", "markdown"), default="markdown")
    parser.add_argument("--check", action="store_true",
                        help="fail if snapshot or embedded audit census is stale")
    args = parser.parse_args()
    datasets = load_datasets()
    errors = validate_datasets(datasets)
    if errors:
        parser.exit(1, "Invalid datasets:\n" + "\n".join(errors) + "\n")
    fresh = build_snapshot(datasets)
    if args.check:
        try:
            stored = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
            audit = AUDIT_DOC.read_text(encoding="utf-8")
        except (OSError, ValueError) as exc:
            parser.exit(1, f"Missing/invalid Phase 0 audit files: {exc}\n")
        if fresh != stored:
            parser.exit(1, "STALE snapshot: regenerate data/phase0-coverage-snapshot.json\n")
        block = render_census(fresh)
        if audit.count(BEGIN) != 1 or audit.count(END) != 1 or block not in audit:
            parser.exit(1, "STALE audit census: regenerate docs/coverage-audit.md\n")
        print("PASS: live Phase 0 snapshot and human-readable census agree.")
        return 0
    print(json.dumps(fresh, indent=2) if args.format == "json" else render_census(fresh))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
