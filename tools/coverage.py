#!/usr/bin/env python3
"""Reproducible record-count census; not a vehicle completeness or fitment score."""

from __future__ import annotations

import argparse
import json
from collections import Counter

from database import load_datasets, validate_datasets

KINDS = ("facts", "issues", "parts")
SCOPE_FIELDS = (
    "platforms", "model_years", "markets", "engine_codes",
    "transmission_codes", "body_styles", "vin_ranges",
)
TARGETS = {"9-5-9600": range(1998, 2010), "9-3-9440": range(2003, 2012)}


def scopes(record: dict) -> list[dict]:
    scope = record.get("applicability") or {}
    return scope.get("groups", [scope])


def explicitly_applies_to_year(record: dict, platform: str, year: int) -> bool:
    """Require platform and year together in one group; never expand unions."""
    return any(
        platform in group.get("platforms", [])
        and year in group.get("model_years", [])
        for group in scopes(record)
    )


def census(datasets: list[dict]) -> dict:
    records = [r for d in datasets for k in KINDS for r in d[k]]
    sources = [s for d in datasets for s in d["sources"]]
    return {
        "meaning": "Explicit record counts, not completeness, reliability or fitment ratings",
        "domains": [d["domain"] for d in datasets],
        "counts": {
            "sources": len(sources),
            **{kind: sum(len(d[kind]) for d in datasets) for kind in KINDS},
            "gaps": sum(len(d["gaps"]) for d in datasets),
        },
        "unique_source_urls": len({s["url"] for s in sources}),
        "retrieval": dict(sorted(Counter(s["retrieval"] for s in sources).items())),
        "evidence": dict(sorted(Counter(r["evidence_status"] for r in records).items())),
        "explicit_scope_counts": {
            field: sum(bool(r.get("applicability", {}).get(field)) for r in records)
            for field in SCOPE_FIELDS
        },
        "platform_year": {
            platform: {
                str(year): {
                    kind: sum(
                        explicitly_applies_to_year(r, platform, year)
                        for d in datasets for r in d[kind]
                    )
                    for kind in KINDS
                }
                for year in years
            }
            for platform, years in TARGETS.items()
        },
    }


def markdown_report(report: dict) -> str:
    counts = report["counts"]
    lines = [
        "# Saab research record census",
        "",
        f"Source records: {counts['sources']}; facts: {counts['facts']}; "
        f"issues: {counts['issues']}; parts: {counts['parts']}; gaps: {counts['gaps']}.",
        "", "Scope field | Records with explicit field | Total technical/issue/part records",
        "--- | ---: | ---:",
    ]
    total = sum(counts[k] for k in KINDS)
    for field, n in report["explicit_scope_counts"].items():
        lines.append(f"{field} | {n} | {total}")
    lines.extend(["", "The following counts require explicit, jointly applicable platform and model year.",
                  "Unspecified years are omitted, **not** assumed to be uncovered.", ""])
    for platform, years in report["platform_year"].items():
        lines.extend([f"## {platform}", "", "Model year | Facts | Issues | Parts", "--- | ---: | ---: | ---:"])
        for year, values in years.items():
            lines.append(f"{year} | {values['facts']} | {values['issues']} | {values['parts']}")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    args = parser.parse_args()
    try:
        datasets = load_datasets()
        errors = validate_datasets(datasets)
    except (OSError, ValueError) as exc:
        parser.exit(1, f"Cannot load Saab datasets: {exc}\n")
    if errors:
        parser.exit(1, "Dataset validation failed:\n" + "\n".join(errors) + "\n")
    report = census(datasets)
    print(json.dumps(report, indent=2) if args.format == "json" else markdown_report(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
