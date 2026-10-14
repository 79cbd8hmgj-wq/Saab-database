#!/usr/bin/env python3
"""Adjudicate *existing* overlapping part-number and research-gap records.

The result is a non-destructive source-and-scope cross-reference, not a
manufacturer interchange directive, corrected supplier claim, or closed gap.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

from audit_research_reuse import build as audit_reuse, text_key
from database import ROOT, load_datasets, validate_datasets

REGISTER_PATH = ROOT / "data/audits/part-gap-overlap-review-20261014.json"
SNAPSHOT_PATH = ROOT / "data/phase0-coverage-snapshot.json"
LEDGER_PATH = ROOT / "data/tier-research/observations.json"


def normalize_part_number(value: str) -> str:
    return value.strip().casefold()


def build(datasets: list[dict], register: dict) -> dict:
    errors=validate_datasets(datasets)
    if errors:
        raise ValueError("Invalid original research: "+"; ".join(errors[:4]))
    parts={p["id"]:p for d in datasets for p in d["parts"]}
    gaps={g["id"]:g for d in datasets for g in d["gaps"]}
    source={s["id"]:s for d in datasets for s in d["sources"]}
    part_groups=defaultdict(list)
    for part in parts.values():
        part_groups[normalize_part_number(part["part_number"])].append(part["id"])
    repeated_parts={n:sorted(ids) for n,ids in part_groups.items() if len(ids)>1}
    gap_groups=defaultdict(list)
    for gap in gaps.values():
        gap_groups[text_key(gap["title"])].append(gap["id"])
    repeated_gap_sets=sorted(
        tuple(sorted(ids)) for ids in gap_groups.values() if len(ids)>1
    )
    reviewed_parts={entry["part_number"].strip().casefold():entry
                    for entry in register["parts"]}
    if len(reviewed_parts)!=len(register["parts"]):
        raise ValueError("Repeated or duplicate curated part group number")
    if set(reviewed_parts)!=set(repeated_parts):
        raise ValueError("Unreviewed/stale exact part-number overlaps: missing="
                         +str(sorted(set(repeated_parts)-set(reviewed_parts)))
                         +" stale="+str(sorted(set(reviewed_parts)-set(repeated_parts))))
    reviewed_gaps={entry["id"]:entry for entry in register["research_blockers"]}
    if len(reviewed_gaps)!=len(register["research_blockers"]):
        raise ValueError("Duplicate canonical blocker id")
    if sorted(tuple(sorted(x["record_ids"])) for x in register["research_blockers"])!=repeated_gap_sets:
        raise ValueError("Unreviewed/stale exact-title gap groups")
    used=set()
    part_rows=[]
    for num,record in sorted(reviewed_parts.items()):
        ids=sorted(record["record_ids"])
        if ids!=repeated_parts[num]:
            raise ValueError("Part review record IDs drift for "+num)
        for id_ in ids:
            if id_ not in parts:
                raise ValueError("Missing part "+id_)
            if id_ in used:
                raise ValueError("Part appears in multiple groups "+id_)
            used.add(id_)
        if (not record["nonmergeable"] or record["factory_proof_of_cross_platform_VIN_fitment"]
            or not record["claim_review"] or not record["keep_distinct_reason"]
            or not record["unresolved"] or not record["relationship"]):
            raise ValueError("Part review improperly asserts unrestricted interchange: "+num)
        origins=[
            {
                "record_id":id_,
                "original_part_number":parts[id_]["part_number"],
                "original_applicability":parts[id_]["applicability"],
                "original_evidence_status":parts[id_]["evidence_status"],
                "original_requirements":parts[id_]["requirements"],
                "original_relationships":parts[id_]["relationships"],
                "original_source_ids":parts[id_]["source_ids"],
                "original_urls":sorted({source[s]["url"] for s in parts[id_]["source_ids"]})
            } for id_ in ids
        ]
        part_rows.append({**record,"source_specific_original_claims":origins})
    gap_rows=[]
    for entry in sorted(register["research_blockers"],key=lambda e:e["id"]):
        ids=sorted(entry["record_ids"])
        if any(x not in gaps for x in ids):
            raise ValueError("Missing original blocker record")
        if (entry["state"]!="open_not_resolved" or not entry["remaining_work"]
            or not entry["do_not_close_until"] or not entry["claim_review"]):
            raise ValueError("Source blockers cannot be automatically closed")
        gap_rows.append({
            **entry,
            "original_gap_records":[
                {"record_id":x,"title":gaps[x]["title"],
                 "reason":gaps[x]["reason"],"missing_inputs":gaps[x]["missing_inputs"],
                 "original_source_ids":gaps[x]["source_ids"],
                 "original_urls":sorted({source[s]["url"] for s in gaps[x]["source_ids"]})}
                for x in ids
            ]
        })
    if not (register["policy"]["all_original_part_and_gap_records_remain"]
            and register["policy"]["source_specific_applicability_not_collapsed"]
            and register["policy"]["same_gap_title_not_closed"]
            and register["policy"]["same_number_not_global_OE_supersession"]):
        raise ValueError("Missing strict evidence preservation rules")
    return {
        "schema_version":register["schema_version"],
        "meaning":"Manual claim-to-claim distinctions for exact-number/title repetitions; all original records remain authoritative, no new fitted cars or source facts.",
        "stats":{"original_parts":len(parts),"original_gaps":len(gaps),
                 "repeated_part_number_groups_reviewed":len(part_rows),
                 "repeated_gap_title_groups_reviewed":len(gap_rows),
                 "original_part_records_cross_referenced":sum(len(x["record_ids"]) for x in part_rows),
                 "original_gap_records_cross_referenced":sum(len(x["record_ids"]) for x in gap_rows),
                 "duplicate_part_numbers_unreviewed":0,
                 "identical_gap_titles_unreviewed":0},
        "part_claim_groups":part_rows,
        "open_shared_research_blockers":gap_rows,
        "parts_by_original_id":{
            id_:{"part_number":p["part_number"],
                 "related_part_record_ids":[x for x in
                    reviewed_parts[normalize_part_number(p["part_number"])]["record_ids"]
                    if x!=id_],
                 "review_relationship":reviewed_parts[normalize_part_number(p["part_number"])]["relationship"],
                 "still_needs_VIN_supplier_validation":True}
            for id_,p in parts.items()
            if normalize_part_number(p["part_number"]) in reviewed_parts
        },
        "gaps_by_original_id":{
            id_:{"canonical_open_blocker_id":entry["id"],
                 "related_gap_ids":[x for x in entry["record_ids"] if x!=id_],
                 "resolved":False}
            for entry in register["research_blockers"]
            for id_ in entry["record_ids"]
        }
    }


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check",action="store_true",
                        help="Fail if new duplicate groups are not manually adjudicated")
    parser.add_argument("--summary",action="store_true",help="Show the exact overlap decisions")
    parser.add_argument("--output",type=Path,help="Export full original scope and citations")
    args=parser.parse_args()
    report=build(load_datasets(),json.loads(REGISTER_PATH.read_text(encoding="utf-8")))
    if args.output:
        args.output.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",
                               encoding="utf-8")
        print("Saved",args.output)
    if args.summary:
        print(json.dumps({
            "stats":report["stats"],
            "part_overlap": [
                {"part_number":x["part_number"],"records":x["record_ids"],
                 "relationship":x["relationship"],"scope_conflict":x["source_scope_conflict"],
                 "unresolved":x["unresolved"]}
                for x in report["part_claim_groups"]],
            "still_open_shared_research_blockers":[
                {"id":x["id"],"records":x["record_ids"],"state":x["state"]}
                for x in report["open_shared_research_blockers"]]
        },indent=2,ensure_ascii=False))
    if args.check:
        print("PASS: five repeated part-number groups and two repeated gap-title groups "
              "have source-preserving reviewed cross-references; no gaps closed or "
              "supersession/fitment inferred")
    if not any([args.check,args.summary,args.output]):
        parser.print_help()
    return 0

if __name__=="__main__":
    sys.exit(main())
