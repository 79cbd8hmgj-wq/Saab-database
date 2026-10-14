#!/usr/bin/env python3
"""Inventory existing Saab evidence and reuse leads without re-research or ranking.

This is a reproducible cross-dataset structural/reuse audit. A shared source,
repeated title or matching subject/predicate is a REVIEW CANDIDATE, not proof
two engineering findings are identical.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

from database import ROOT, load_datasets, validate_datasets

LEDGER = ROOT / "data/tier-research/observations.json"
CURRENT_CENSUS = ROOT / "data/phase0-coverage-snapshot.json"
LEGACY_BRIDGES = {
    "tier-failure-idm-four-cylinder": [
        "corrections-issue-004"
    ],
    "tier-failure-idm-b308": [
        "corrections-issue-004"
    ],
    "tier-failure-ng93-coolant-in-atf": [
        "corrections-issue-006", "hcdiag-issue-003"
    ],
}
RELATED_BUT_DISTINCT = {
    "tier-failure-ng93-coolant-in-atf": [
        "corrections-issue-005"
    ]
}


def text_key(value: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^\w ]", " ", value.casefold())).strip()


def entries_map(datasets: list[dict], kind: str) -> dict[str, dict]:
    return {r["id"]: {**r, "_domain": d["domain"]}
            for d in datasets for r in d[kind]}


def collapse_groups(groups: dict[str, list[dict]], *, show_singletons: bool = False) -> list[dict]:
    rows = [
        {"key": key, "record_ids": sorted({r["id"] for r in recs}),
         "domains": sorted({r["_domain"] for r in recs}),
         "n_records": len(recs)}
        for key, recs in groups.items()
        if show_singletons or len({r["id"] for r in recs}) > 1
    ]
    return sorted(rows, key=lambda r: (-r["n_records"], r["key"]))


def build(datasets: list[dict], ledger: dict, census: dict) -> dict[str, Any]:
    errors = validate_datasets(datasets)
    if errors:
        raise ValueError("Cannot audit invalid datasets: " + "; ".join(errors[:4]))
    sources = entries_map(datasets, "sources")
    facts = entries_map(datasets, "facts")
    issues = entries_map(datasets, "issues")
    parts = entries_map(datasets, "parts")
    gaps = entries_map(datasets, "gaps")
    source_url_by_id = {k: x["url"] for k, x in sources.items()}
    by_source = defaultdict(list)
    for src in sources.values():
        # Exact URL; don't collapse distinct manufacturer revision or query strings.
        by_source[src["url"]].append(src)
    source_clusters = collapse_groups(by_source)
    title_groups = defaultdict(list)
    for issue in issues.values():
        title_groups[text_key(issue["title"])].append(issue)
    issue_title_groups = collapse_groups(title_groups)

    gap_groups = defaultdict(list)
    for gap in gaps.values():
        gap_groups[text_key(gap["title"])].append(gap)
    gap_title_groups = collapse_groups(gap_groups)

    part_groups = defaultdict(list)
    for part in parts.values():
        part_groups[part["part_number"].strip().casefold()].append(part)
    part_number_groups = collapse_groups(part_groups)

    fact_groups = defaultdict(list)
    for fact in facts.values():
        key = json.dumps([fact["subject"], fact["predicate"], fact["value"]],
                         sort_keys=True, ensure_ascii=False, separators=(",", ":"))
        fact_groups[key].append(fact)
    fact_semantic_review = collapse_groups(fact_groups)

    issue_source_groups = defaultdict(list)
    for issue in issues.values():
        for s_id in issue["source_ids"]:
            issue_source_groups[source_url_by_id[s_id]].append(issue)
    cross_issue_shared_originals = [
        row for row in collapse_groups(issue_source_groups)
        if len(row["domains"]) > 1
    ]
    known_issue_ids = set(issues)
    tier_cases = {r["id"]: r for r in ledger["failure_modes"]}
    if set(tier_cases) != set(LEGACY_BRIDGES):
        raise ValueError("Tier case inventory changed: manually review legacy issue links")
    bridge_rows = []
    for case, originals in sorted(LEGACY_BRIDGES.items()):
        record = tier_cases[case]
        for original in originals:
            if original not in known_issue_ids:
                raise ValueError("Stale link to historical issue: " + original)
            issue = issues[original]
            source_match = sorted(
                set(record["source_ids"]) & set(issue["source_ids"])
            )
            shared_urls = sorted(
                {source_url_by_id[s] for s in record["source_ids"]}
                & {source_url_by_id[s] for s in issue["source_ids"]}
            )
            if not shared_urls:
                raise ValueError("Expected shared original document URL missing: " + case + "/" + original)
            bridge_rows.append({
                "tier_case_id": case, "preexisting_issue_id": original,
                "preexisting_dataset": issue["_domain"], "relationship": "same_mechanism_family",
                "supporting_shared_source_ids": source_match,
                "supporting_shared_original_urls": shared_urls,
                "mechanism_id": record["mechanism_id"],
                "note": "Reuse candidate; does not prove same vehicle application, incidence or repair."
            })
    related_rows = []
    for case, older_ids in RELATED_BUT_DISTINCT.items():
        for old in older_ids:
            if old not in issues:
                raise ValueError("Missing linked but distinct historical issue")
            related_rows.append({
                "tier_case_id": case, "preexisting_issue_id": old,
                "relationship": "related_factory_campaign_not_equivalent_scope",
                "preexisting_dataset": issues[old]["_domain"],
                "note": "Campaign population and technical-advice diagnosis must remain separate."
            })
    original_counts = census["counts"]
    actual_counts = {
        "sources": len(sources), "facts": len(facts), "issues": len(issues),
        "parts": len(parts), "gaps": len(gaps)
    }
    if actual_counts != original_counts:
        raise ValueError("Dataset totals disagree with canonical Phase 0 census")
    if len(by_source) != census["unique_source_urls"]:
        raise ValueError("Exact source URL count disagrees with canonical Phase 0 census")
    domain_rows = sorted(
        [{
            "domain": d["domain"],
            "sources": len(d["sources"]), "facts": len(d["facts"]),
            "issues": len(d["issues"]), "parts": len(d["parts"]),
            "gaps": len(d["gaps"])
        } for d in datasets],
        key=lambda row: row["domain"]
    )
    return {
        "schema_version": "1.0.0",
        "meaning": "Deduplication *review leads* and existing evidence discovery; NOT engineering defect counts, unique failure rates, OEM approvals or tier scores.",
        "scope": "All data/datasets/*.json + existing tier ledger, with canonical count checks; does not inspect every primary document or prove complete Saab recall/failure coverage.",
        "census": {
            "domains": len(datasets),
            **actual_counts,
            "unique_exact_source_urls": len(by_source),
            "source_record_reuse_excess": len(sources) - len(by_source),
            "source_urls_reused": len(source_clusters),
            "dataset_domains_without_issue_records": sum(r["issues"] == 0 for r in domain_rows),
            "tier_cohort_cases": len(tier_cases),
            "tier_engineering_mechanisms": len(ledger["failure_mechanisms"]),
            "legacy_issue_links_for_tier_cases": len(bridge_rows),
            "independent_failure_frequency_studies_in_tier_ledger":
                len(ledger["fleet_failure_frequency_studies"]),
            "tier_verified_parts_market_offers": len(ledger["parts_market_offers"]),
            "tier_complete_repair_cost_observations": len(
                ledger["complete_repair_cost_observations"]),
            "repeated_exact_issue_title_groups": len(issue_title_groups),
            "repeated_exact_gap_title_groups": len(gap_title_groups),
            "repeated_part_number_groups": len(part_number_groups),
            "same_subject_predicate_value_fact_groups": len(fact_semantic_review),
            "cross_domain_shared_source_issue_clusters": len(cross_issue_shared_originals)
        },
        "already_researched_tier_issue_bridges": bridge_rows,
        "related_distinct_scope_campaigns": related_rows,
        "source_url_reuse_groups": source_clusters,
        "issue_shared_source_cross_domain_review_groups": cross_issue_shared_originals,
        "fact_same_subject_predicate_value_review_groups": fact_semantic_review,
        "exact_issue_title_review_groups": issue_title_groups,
        "exact_gap_title_review_groups": gap_title_groups,
        "repeated_part_number_review_groups": part_number_groups,
        "domain_evidence_inventory": domain_rows,
        "existing_issue_catalogue": [{
            "id": id_, "domain": row["_domain"], "title": row["title"],
            "source_ids": row["source_ids"],
            "original_source_urls": sorted(set(source_url_by_id[s] for s in row["source_ids"]))
        } for id_, row in sorted(issues.items())],
        "method_warnings": [
            "42 datasets are research topics and some re-use the same source; they are not 42 independent engineering studies.",
            "A source re-used across domains is not independently corroborated and need not mean duplicate findings.",
            "92 issue records are source-scoped summaries, not the number of unique factory design faults.",
            "Identical fact values can be correct for multiple VIN scopes; inspect applicability before merging records.",
            "Overlapping issue source URLs are only review leads, not proof of equal root cause or identical affected population.",
            "284 gaps are research tasks, potentially related or overlapping; do not treat as distinct missing factory defects.",
            "Existing 110-group automatic FWD US feasibility links are research coverage leads, not verified parts, inspection, or durability.",
            "No model/part priority, tier or reliability percentage follows from this audit."
        ]
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path,
                        help="Write comprehensive JSON report to this path.")
    parser.add_argument("--summary", action="store_true",
                        help="Print compact counts, existing tier issue bridges and domain list.")
    args = parser.parse_args()
    audit = build(load_datasets(), json.loads(LEDGER.read_text(encoding="utf-8")),
                  json.loads(CURRENT_CENSUS.read_text(encoding="utf-8")))
    if args.output:
        args.output.write_text(json.dumps(audit, indent=2, ensure_ascii=False) + "\n",
                               encoding="utf-8")
        print("Wrote", args.output)
    if args.summary or not args.output:
        print(json.dumps({
            "census": audit["census"],
            "tier_to_existing_issues": audit["already_researched_tier_issue_bridges"],
            "related_but_distinct": audit["related_distinct_scope_campaigns"],
            "top_source_reuse": audit["source_url_reuse_groups"][:12],
            "top_cross_domain_issue_overlap": audit["issue_shared_source_cross_domain_review_groups"][:10],
            "fact_reuse_examples": audit["fact_same_subject_predicate_value_review_groups"][:8],
            "exact_issue_title_review_groups": audit["exact_issue_title_review_groups"][:8],
            "exact_gap_title_review_groups": audit["exact_gap_title_review_groups"][:8],
            "repeated_part_number_review_groups": audit["repeated_part_number_review_groups"][:8],
            "domain_evidence_inventory": audit["domain_evidence_inventory"]
        }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
