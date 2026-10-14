#!/usr/bin/env python3
"""Build a lossless reuse-first crosswalk for *all* legacy issue records.

Curated taxonomy identifies actual factory mechanisms separately from diagnosis,
recall scope, source/version errors and parts/market applicability. Related fact,
part and gap links are original-document *leads*, not proven identical claims.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

from database import ROOT, load_datasets, validate_datasets

TAXONOMY = ROOT / "data/audits/legacy-issue-taxonomy-20261014.json"
LEDGER = ROOT / "data/tier-research/observations.json"


def validate_taxonomy(datasets: list[dict], taxonomy: dict, ledger: dict) -> None:
    """Fail closed when a newly added source-scoped issue has no human-reviewed role."""
    errors = validate_datasets(datasets)
    if errors:
        raise ValueError("Source database invalid: " + "; ".join(errors[:3]))
    issue_by_id = {x["id"]: x for d in datasets for x in d["issues"]}
    classes = taxonomy["assignments"]
    if set(classes) != set(taxonomy["categories"]):
        raise ValueError("Categories do not match role assignments")
    assigned = [issue for items in classes.values() for issue in items]
    if len(assigned) != len(set(assigned)):
        raise ValueError("Issue assigned multiple competing primary roles")
    if set(assigned) != set(issue_by_id):
        raise ValueError("Unclassified/retired issues: missing="
                         + str(sorted(set(issue_by_id) - set(assigned)))
                         + " stale=" + str(sorted(set(assigned) - set(issue_by_id))))
    mechanisms = taxonomy["mechanism_clusters"]
    ids = [m["id"] for m in mechanisms]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate canonical mechanism IDs")
    source_by_id = {s["id"]: s for d in datasets for s in d["sources"]}
    eligible = (set(classes["factory_documented_mechanism"])
                | set(classes["factory_safety_campaign"])
                | set(classes["suspected_factory_mechanism"]))
    mapped = [id_ for mechanism in mechanisms for id_ in mechanism["issue_ids"]]
    if set(mapped) != eligible or len(mapped) != len(set(mapped)):
        raise ValueError("Documented/suspected causes must have exactly one reviewed mechanism identity; non-defect cases must not.")
    role_of = {id_: kind for kind, entries in classes.items() for id_ in entries}
    for mechanism in mechanisms:
        if not mechanism.get("scope_note"):
            raise ValueError("Mechanism without cohort/scope caution: " + mechanism["id"])
        roles = {role_of[id_] for id_ in mechanism["issue_ids"]}
        if mechanism["state"] == "suspected_not_confirmed":
            if roles != {"suspected_factory_mechanism"}:
                raise ValueError("Suspected defect upgraded to confirmed status")
        elif mechanism["state"] == "campaign_documented":
            if roles != {"factory_safety_campaign"}:
                raise ValueError("Campaign reinterpreted as proven engineering failure rate")
        elif mechanism["state"] == "factory_documented":
            if roles != {"factory_documented_mechanism"}:
                raise ValueError("Documented component mechanism uses a non-defect case")
        else:
            raise ValueError("Unknown evidence strength: " + mechanism["state"])
        for id_ in mechanism["issue_ids"]:
            x = issue_by_id[id_]
            original_types = {source_by_id[s]["source_type"] for s in x["source_ids"]}
            if not original_types & {"factory_bulletin", "factory_manual",
                                     "regulator_record"}:
                raise ValueError("Mechanism lacks factory/regulator record: " + id_)
    for group in taxonomy["related_existing_issue_links"]:
        if len(set(group["ids"])) != len(group["ids"]) or len(group["ids"]) < 2:
            raise ValueError("Invalid explicit related-issue group")
        if not set(group["ids"]).issubset(issue_by_id):
            raise ValueError("Related issue refers to nonexistent record")
        if not group.get("note"):
            raise ValueError("Related issues require reviewer explanation")
    relevant = {m["id"] for m in mechanisms}
    observed = {m["id"] for m in ledger["failure_mechanisms"]}
    if not observed.issubset(relevant):
        raise ValueError("Tier ledger mechanism missing from curated legacy map")
    for m in ledger["failure_mechanisms"]:
        if m["id"] not in relevant:
            raise ValueError("Tier mechanism not reconciled")
    if len(ledger["fleet_failure_frequency_studies"]) != 0:
        # Review quantitative references separately rather than ignoring updates.
        raise ValueError("Population failure studies changed; reassess crosswalk")


def build(datasets: list[dict], taxonomy: dict, ledger: dict) -> dict:
    validate_taxonomy(datasets, taxonomy, ledger)
    source_by_id = {x["id"]: x for d in datasets for x in d["sources"]}
    kind_by_id = {x["id"]: (kind, d["domain"], x)
                  for d in datasets for kind in ("facts", "issues", "parts", "gaps")
                  for x in d[kind]}
    role = {id_: classification for classification, ids in
            taxonomy["assignments"].items() for id_ in ids}
    mechanism_by_issue = {id_: m["id"] for m in taxonomy["mechanism_clusters"]
                          for id_ in m["issue_ids"]}
    tier_by_mechanism = defaultdict(list)
    for case in ledger["failure_modes"]:
        tier_by_mechanism[case["mechanism_id"]].append(case["id"])

    # Preserve original source IDs while enabling joins across duplicate document IDs.
    source_url_index = defaultdict(set)
    for sid, source in source_by_id.items():
        source_url_index[source["url"]].add(sid)
    record_urls = {}
    context_for_url = defaultdict(list)
    for id_, (kind, domain, record) in kind_by_id.items():
        urls = {source_by_id[s]["url"] for s in record["source_ids"]}
        record_urls[id_] = urls
        for url in urls:
            context_for_url[url].append((id_, kind, domain))

    explicit_groups = defaultdict(list)
    for group in taxonomy["related_existing_issue_links"]:
        for id_ in group["ids"]:
            explicit_groups[id_].append({
                "relationship": group["type"],
                "other_issue_ids": sorted(set(group["ids"]) - {id_}),
                "reviewer_note": group["note"]
            })

    inventory = []
    for d in sorted(datasets, key=lambda x: x["domain"]):
        for issue in d["issues"]:
            urls = record_urls[issue["id"]]
            associated = defaultdict(set)
            # This is a navigation join, not independent factual corroboration.
            for url in urls:
                for id_, kind, domain in context_for_url[url]:
                    if id_ != issue["id"]:
                        associated[kind].add(id_)
            records = {
                name: sorted(associated[name])
                for name in ("facts", "issues", "parts", "gaps")
            }
            m_id = mechanism_by_issue.get(issue["id"])
            inventory.append({
                "issue_id": issue["id"], "domain": d["domain"],
                "title": issue["title"], "record_type": role[issue["id"]],
                "canonical_mechanism_id": m_id,
                "tier_case_ids": sorted(tier_by_mechanism.get(m_id, [])),
                "original_cause": issue["cause"],
                "original_applicability": issue["applicability"],
                "original_source_ids": issue["source_ids"],
                "original_source_urls": sorted(urls),
                "original_evidence_status": issue["evidence_status"],
                "source_url_sharing_context_record_ids": records,
                "source_sharing_is_independent_corroboration": False,
                "explicitly_reviewed_issue_relationships":
                    explicit_groups[issue["id"]]
            })

    return {
        "schema_version": "1.0.0",
        "source_taxonomy_path": "data/audits/legacy-issue-taxonomy-20261014.json",
        "semantics": ("Exhaustive *saved issue* catalogue and curated type/mechanism map. "
                      "Not an exhaustive Saab factory-defect corpus; source-URL joins "
                      "are research navigation only, not independent corroboration, "
                      "same-root proof, valid fitment or quantified risk."),
        "counts": {
            "legacy_issues": len(inventory),
            "record_classifications": dict(sorted(Counter(x["record_type"] for x in inventory).items())),
            "curated_engineering_mechanism_clusters": len(taxonomy["mechanism_clusters"]),
            "mechanism_cluster_states": dict(sorted(
                Counter(m["state"] for m in taxonomy["mechanism_clusters"]).items())),
            "issues_with_curated_mechanism": sum(bool(x["canonical_mechanism_id"]) for x in inventory),
            "original_source_url_overlap_issue_pairs": sum(
                len(x["source_url_sharing_context_record_ids"]["issues"]) for x in inventory) // 2,
            "existing_tier_cases": len(ledger["failure_modes"]),
            "existing_tier_mechanisms": len(ledger["failure_mechanisms"]),
        },
        "factory_mechanisms": [
            {**m, "existing_tier_case_ids": sorted(tier_by_mechanism.get(m["id"], []))}
            for m in taxonomy["mechanism_clusters"]
        ],
        "existing_issue_records": sorted(inventory, key=lambda x: x["issue_id"]),
        "research_pr_acceptance_rule": (
            "Before adding a new factory defect, use this crosswalk to identify legacy issue, "
            "source URL and mechanism; document exact vehicle/revision applicability and "
            "what genuinely new source, production boundary, observation or repair evidence "
            "was gained. Never relabel a preexisting issue as a newly discovered defect.")
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="Validate complete classification, original source traceability and tier references")
    parser.add_argument("--summary", action="store_true",
                        help="Show role counts, mechanism clusters and tier crosswalk")
    parser.add_argument("--find", metavar="TEXT", help="Search issue title, id, cause, source IDs/URLs and mechanism")
    parser.add_argument("--output", type=Path, help="Write full lossless index to JSON")
    args = parser.parse_args()
    datasets = load_datasets()
    audit = build(datasets, json.loads(TAXONOMY.read_text(encoding="utf-8")),
                  json.loads(LEDGER.read_text(encoding="utf-8")))
    if args.output:
        args.output.write_text(json.dumps(audit, indent=2, ensure_ascii=False) + "\n",
                               encoding="utf-8")
        print("Wrote", args.output)
    if args.summary:
        print(json.dumps({
            "counts": audit["counts"],
            "factory_mechanisms": audit["factory_mechanisms"],
        }, indent=2))
    if args.find:
        term = re.sub(r"\s+", " ", args.find.strip().lower())
        found = [
            item for item in audit["existing_issue_records"]
            if term in json.dumps({
                k: v for k, v in item.items()
                if k not in {"source_url_sharing_context_record_ids"}
            }, ensure_ascii=False).lower()
        ]
        print(json.dumps({"query": args.find, "matched_issues": len(found),
                          "records": found}, indent=2, ensure_ascii=False))
    if args.check:
        print("PASS: all saved issues classified with source URL traceability; "
              "documented/suspected mechanism links and tier crosswalk consistent")
    if not any((args.summary, args.find, args.output, args.check)):
        parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
