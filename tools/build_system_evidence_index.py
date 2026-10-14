#!/usr/bin/env python3
"""Reuse-first, source-linked system navigation for ALL existing Saab evidence.

No new engineering findings. A keyword/domain match is a research routing
proposal and MUST NOT become model coverage, OE fitment, real stock, failure
incidence, or a vehicle recommendation.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urlparse

from database import ROOT, load_datasets, validate_datasets
from build_legacy_issue_index import validate_taxonomy

POLICY_PATH = ROOT / "data/audits/system-evidence-routing-policy-20261014.json"
ISSUE_TAXONOMY_PATH = ROOT / "data/audits/legacy-issue-taxonomy-20261014.json"
METHOD_PATH = ROOT / "data/tier-research/methodology.json"
LEDGER_PATH = ROOT / "data/tier-research/observations.json"
CENSUS_PATH = ROOT / "data/phase0-coverage-snapshot.json"
KINDS = ("facts", "issues", "parts", "gaps")
GENERIC_SUBJECTS = (
    "saab original 9-5 9600", "saab original 9-5",
    "saab original 9-3", "saab original", "9-5 original 9600",
)


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def check_policy(policy: dict, methodology: dict, datasets: list[dict]) -> None:
    systems = {s["id"] for s in methodology["system_inventory"]}
    if len(methodology["system_inventory"]) != 16:
        raise ValueError("Unexpected system vocabulary; review routing explicitly.")
    if set(policy["match_rules"]) != systems:
        raise ValueError("Routing policy not aligned with exact 16 system IDs")
    if set(policy["domain_context_defaults"]) != {d["domain"] for d in datasets}:
        raise ValueError("Dataset domain added/removed without routing policy review")
    for domain, entries in policy["domain_context_defaults"].items():
        if len(entries) != len(set(entries)) or set(entries) - systems:
            raise ValueError("Invalid domain system fallback: " + domain)
    for system, expressions in policy["match_rules"].items():
        if not expressions:
            raise ValueError("System has no semantic cues: " + system)
        for expression in expressions:
            try:
                re.compile(expression, re.I)
            except re.error as error:
                raise ValueError(f"Invalid route rule for {system}: {expression}") from error
    originals = {r["id"]: kind for d in datasets for kind in KINDS for r in d[kind]}
    curated = policy.get("explicit_record_routes", {})
    for id_, value in curated.items():
        if id_ not in originals or not isinstance(value, list) or not value or (
            set(value) - systems
        ):
            raise ValueError("Invalid curated system override: " + id_)
    expected_parts = {id_ for id_, kind in originals.items() if kind == "parts"}
    if set(curated) != expected_parts:
        raise ValueError(
            "Curated system routes must correspond to all and only existing part IDs; "
            + "new or unreviewed parts=" + str(sorted(expected_parts - set(curated)))
            + "; obsolete or non-part overrides=" + str(sorted(set(curated) - expected_parts))
        )


def topic_fields(kind: str, record: dict) -> list[tuple[str, str, int]]:
    """Only use stated record metadata, not full value/body or source publisher."""
    if kind == "facts":
        raw = [
            ("predicate", record.get("predicate"), 5),
            ("category", record.get("category"), 3),
            ("subject", record.get("subject"), 2),
        ]
    elif kind == "parts":
        raw = [("title", record.get("title"), 6),
               ("subject", record.get("part_number"), 1)]
    elif kind == "issues":
        raw = [("title", record.get("title"), 6),
               ("cause", record.get("cause"), 2)]
    elif kind == "gaps":
        raw = [("title", record.get("title"), 6),
               ("missing_inputs", " ".join(str(x) for x in record.get("missing_inputs", [])), 1)]
    else:
        raise ValueError("Unexpected dataset kind " + kind)
    return [(name, str(value), weight) for name, value, weight in raw if value]


def route(kind: str, record: dict, domain: str, policy: dict) -> dict:
    fields = topic_fields(kind, record)
    subject = str(record.get("subject", "")).casefold()
    ignore_subject = (
        subject in GENERIC_SUBJECTS
        or any(re.search(expr, subject) for expr in policy["ignore_generic_subject_patterns"])
    )
    scores: dict[str, int] = defaultdict(int)
    matched: dict[str, set[str]] = defaultdict(set)
    for system, expressions in policy["match_rules"].items():
        compiled = [re.compile(expr, flags=re.I) for expr in expressions]
        for field, value, weight in fields:
            if field == "subject" and ignore_subject:
                continue
            matching = {r.pattern for r in compiled if r.search(value)}
            if matching:
                scores[system] += weight * min(len(matching), 3)
                matched[system].update(field + ":" + x for x in sorted(matching))

    overrides = policy.get("explicit_record_routes", {})
    manual = overrides.get(record["id"])
    if manual is not None:
        candidates = list(manual)
        route_basis = "curated_explicit_record"
        review = "source_scope_and_engineering_still_required"
    elif scores:
        high = max(scores.values())
        # Keep all systems with at least 50% of top evidentiary topic score.
        candidates = sorted((s for s, n in scores.items() if n * 2 >= high),
                            key=lambda s: (-scores[s], s))
        route_basis = "keyword_topic_navigation_only"
        review = "not_manually_adjudicated"
    else:
        candidates = list(policy["domain_context_defaults"][domain])
        route_basis = "domain_context_navigation_only" if candidates else "cross_cutting_unrouted"
        review = "not_manually_adjudicated"
    if not set(candidates).issubset(policy["match_rules"]):
        raise ValueError("Unknown assigned system id")
    return {
        "system_ids_for_discovery": candidates,
        "primary_navigation_system": candidates[0] if candidates else None,
        "routing_basis": route_basis,
        "review_status": review,
        "cross_cutting_or_unresolved_system": not bool(candidates),
        "possible_multiple_systems": len(candidates) > 1,
        # Show actual matched fields, so the reviewer can correct an ambiguous route.
        "matched_topic_fields": sorted(
            {token.split(":", 1)[0] for s in candidates for token in matched.get(s, ())}
        ) if manual is None else [],
    }


def fact_use(record: dict, sources: list[dict]) -> str:
    fields = (str(record.get("subject", "")) + " "
              + str(record.get("predicate", "")) + " "
              + str(record.get("category", ""))).lower()
    category = str(record.get("category", "")).lower()
    if category in {"source_quality", "source_scope", "vin_code",
                    "identity", "vehicle_identity", "software_provenance"}:
        return "source_identity_or_provenance"
    if "us_retail_quote_snapshot" in fields or category in {
        "parts_candidate", "replacement_sourcing", "catalog_interchange", "interchange",
        "shared_oem_service_sku", "parts_fitment"
    }:
        return "parts_catalogue_or_historical_market_observation"
    if "factory_correction" in fields or "campaign" in fields or "bulletin" in fields:
        return "factory_campaign_or_advisory_reference_not_failure_frequency"
    if "simulation" in fields or "diagnostic_resources" in fields:
        return "simulation_or_tooling_resource"
    if "diagnos" in fields or "dtc" in fields or "fault" in fields:
        return "diagnostic_reference_not_confirmed_vehicle_fault"
    if "maintenance" in fields or "service" in fields or "fluid" in fields:
        return "service_schedule_or_procedure_reference"
    return "specification_or_component_description_not_failure_rate"


def gap_kind(record: dict) -> str:
    t = (record["title"] + " " + " ".join(str(x) for x in record["missing_inputs"])).lower()
    if any(k in t for k in ("actual vin", "selected vehicle", "actual car", "real car",
                           "installed component", "physical confirmation", "inspect",
                           "measured", "roadworthy", "readout", "real vehicle")):
        return "needs_specific_vehicle_or_measurement"
    if any(k in t for k in ("stock", "price", "quote", "shipping", "deliver", "cost",
                           "available", "warranty")):
        return "market_and_repair_economics_unverified"
    if any(k in t for k in ("supersession", "webepc", "original oe", "original saab",
                           "factory bulletin", "vin application", "saab original",
                           "manufacturer", "original part")):
        return "primary_OE_documentation_needed"
    return "additional_evidence_or_validation_needed"


def build(datasets: list[dict], policy: dict, method: dict,
          taxonomy: dict, ledger: dict, census: dict) -> dict:
    errors = validate_datasets(datasets)
    if errors:
        raise ValueError("Invalid research data: " + "; ".join(errors[:3]))
    validate_taxonomy(datasets, taxonomy, ledger)
    check_policy(policy, method, datasets)
    known_counts = {
        "sources": sum(len(d["sources"]) for d in datasets),
        **{k: sum(len(d[k]) for d in datasets) for k in KINDS}
    }
    if known_counts != census["counts"]:
        raise ValueError("Original dataset count drift from reproducible census")
    source = {s["id"]: s for d in datasets for s in d["sources"]}
    evidence_urls: dict[str, set[str]] = defaultdict(set)
    shared_url_issue_ids: dict[str, set[str]] = defaultdict(set)
    for d in datasets:
        for kind in KINDS:
            for r in d[kind]:
                urls = {source[s]["url"] for s in r["source_ids"]}
                evidence_urls[r["id"]] = urls
                if kind == "issues":
                    for url in urls:
                        shared_url_issue_ids[url].add(r["id"])

    issue_role = {id_: role for role, ids in taxonomy["assignments"].items()
                  for id_ in ids}
    issue_mechanism = {id_: m["id"] for m in taxonomy["mechanism_clusters"]
                       for id_ in m["issue_ids"]}
    records = []
    systems = {s["id"]: s for s in method["system_inventory"]}
    for d in sorted(datasets, key=lambda x: x["domain"]):
        for kind in KINDS:
            for record in d[kind]:
                details = route(kind, record, d["domain"], policy)
                urls = evidence_urls[record["id"]]
                # Context shared across different URL aliases; not evidence that
                # a topic belongs to the same defect or original build revision.
                colocated_issues = sorted(set().union(
                    *(shared_url_issue_ids[url] for url in urls)
                ) - ({record["id"]} if kind == "issues" else set()))
                record_id = record["id"]
                out = {
                    "id": record_id, "kind": kind, "domain": d["domain"],
                    **details,
                    "original_source_ids": list(record["source_ids"]),
                    "original_source_urls": sorted(urls),
                    "no_source_is_unanswered_research_question":
                        kind == "gaps" and not bool(urls),
                    "original_applicability": record.get("applicability"),
                    "original_evidence_status": record.get("evidence_status"),
                    "same_source_document_issue_ids_navigation_only": colocated_issues,
                    "source_overlap_proves_same_root_cause": False,
                    "source_overlap_proves_same_vehicle_scope": False,
                    "eligible_for_model_rating_from_this_index": False,
                }
                if kind == "facts":
                    out.update({
                        "subject": record["subject"],
                        "category": record["category"],
                        "predicate": record["predicate"],
                        "claim_type": fact_use(record, [source[s] for s in record["source_ids"]]),
                    })
                elif kind == "parts":
                    out.update({
                        "part_number": record["part_number"],
                        "title": record["title"],
                        "claim_type": "parts_identity_or_supplier_reference_not_VIN_approved",
                        "supersession_is_verified_by_this_index": False,
                        "live_US_fulfilment_verified_by_this_index": False,
                    })
                elif kind == "gaps":
                    out.update({
                        "title": record["title"],
                        "claim_type": gap_kind(record),
                        "resolved_by_this_index": False,
                    })
                elif kind == "issues":
                    out.update({
                        "title": record["title"],
                        "claim_type": issue_role[record_id],
                        "canonical_mechanism_id": issue_mechanism.get(record_id),
                    })
                records.append(out)

    by_system: dict[str, dict] = {}
    for s in method["system_inventory"]:
        id_ = s["id"]
        members = [r for r in records if id_ in r["system_ids_for_discovery"]]
        by_system[id_] = {
            "system_id": id_, "system_name": s["name"],
            "is_tier_critical_system": s["critical"],
            "candidate_records_by_type": {
                k: sum(r["kind"] == k for r in members) for k in KINDS
            },
            "proposed_cross_system_membership": sum(r["possible_multiple_systems"] for r in members),
            "curated_factory_documented_issue_ids": sorted(
                r["id"] for r in members
                if r["kind"] == "issues" and r["claim_type"] == "factory_documented_mechanism"
            ),
            "factory_documented_claims_coverage_certified": False,
            "original_component_lifetime_coverage_certified": False,
            "exact_US_parts_fulfilment_certified": False,
            "complete_US_repair_cost_certified": False,
            "population_failure_rate_available_from_this_index": False,
        }
    routing = Counter(r["routing_basis"] for r in records)
    return {
        "schema_version": "1.0.0",
        "meaning": ("Exhaustive navigation through existing source-backed Saab records; "
                    "system matches are not adjudicated completeness, verified engineering "
                    "defect frequency, approved parts or tier grades."),
        "input_dataset_count": len(datasets),
        "input_technical_counts": {k: known_counts[k] for k in KINDS},
        "tracked_systems": len(by_system),
        "record_routes": dict(sorted(routing.items())),
        "unrouted_cross_cutting_records": sum(r["cross_cutting_or_unresolved_system"]
                                              for r in records),
        "records_with_multiple_candidate_systems": sum(r["possible_multiple_systems"]
                                                       for r in records),
        "explicitly_curated_system_routes": sum(
            r["routing_basis"] == "curated_explicit_record" for r in records),
        "systems": by_system,
        "records": sorted(records, key=lambda r: (r["kind"], r["id"])),
        "all_records_reconciled_to_a_traceable_entry": True,
        "no_total_coverage_percent_or_tier_ranking": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="Reconcile all stored records to source-linked route entries")
    parser.add_argument("--summary", action="store_true",
                        help="System-by-kind rollup and unclassified route overview")
    parser.add_argument("--find", metavar="QUERY",
                        help="Find original subject, title, part number, predicate, id, and source URL")
    parser.add_argument("--system", help="Filter by exact system id from methodology")
    parser.add_argument("--output", type=Path, help="Export source-linked full research index")
    parser.add_argument("--review", action="store_true",
                        help="Print navigation-only cross-cutting and multi-system routing candidates")
    args = parser.parse_args()
    index = build(
        load_datasets(), load(POLICY_PATH), load(METHOD_PATH),
        load(ISSUE_TAXONOMY_PATH), load(LEDGER_PATH), load(CENSUS_PATH))
    if args.output:
        args.output.write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n",
                               encoding="utf-8")
        print("Exported", args.output)
    if args.summary:
        print(json.dumps({
            "dataset_count": index["input_dataset_count"],
            "record_counts": index["input_technical_counts"],
            "systems": index["tracked_systems"],
            "routes": index["record_routes"],
            "cross_cutting_or_unrouted": index["unrouted_cross_cutting_records"],
            "multi_system_records": index["records_with_multiple_candidate_systems"],
            "system_rollup": {k: v["candidate_records_by_type"]
                              for k, v in index["systems"].items()},
            "cross_cutting_by_kind": dict(Counter(
                x["kind"] for x in index["records"]
                if x["cross_cutting_or_unresolved_system"])),
            "cross_cutting_by_domain": dict(Counter(
                x["domain"] for x in index["records"]
                if x["cross_cutting_or_unresolved_system"])),
        }, indent=2, ensure_ascii=False))
    if args.review:
        print(json.dumps({
            "review_records": [
                {k: x.get(k) for k in ("id", "kind", "domain",
                    "title", "subject", "predicate", "primary_navigation_system",
                    "system_ids_for_discovery", "routing_basis")}
                for x in index["records"]
                if x["cross_cutting_or_unresolved_system"]
                    or x["possible_multiple_systems"]
            ][:250],
            "showing_first_250": True,
        }, indent=2, ensure_ascii=False))
    if args.find or args.system:
        if args.system and args.system not in index["systems"]:
            raise SystemExit("Unknown system id: " + args.system)
        term = (args.find or "").casefold()
        rows = [x for x in index["records"]
                if (not args.system or args.system in x["system_ids_for_discovery"])
                and (not term or term in " ".join(map(str, (
                    x["id"], x.get("title", ""), x.get("subject", ""),
                    x.get("predicate", ""), x.get("part_number", ""),
                    " ".join(x["original_source_urls"])
                ))).casefold())]
        print(json.dumps({"matched_count": len(rows), "records": rows},
                         indent=2, ensure_ascii=False))
    if args.check:
        print("PASS: every original fact, issue, part and gap has a sourced, "
              "non-grading navigation record across 16 system categories "
              "or explicitly marked cross-cutting/unresolved.")
    if not any((args.output, args.check, args.find, args.summary, args.review, args.system)):
        parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
