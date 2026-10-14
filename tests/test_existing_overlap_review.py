"""Preserve contradictory original Saab service and seller claims on shared part IDs."""
from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"tools"))
from database import load_datasets
from check_part_gap_reconciliation import build
from build_system_evidence_index import build as build_system

def read(path):
    return json.loads((ROOT/path).read_text(encoding="utf-8"))

class SaabExistingPartGapOverlapTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.datasets=load_datasets()
        cls.register=read("data/audits/part-gap-overlap-review-20261014.json")
        cls.report=build(cls.datasets,cls.register)

    def test_all_and_only_actual_exact_part_and_gap_overlap_groups_are_reviewed(self):
        stats=self.report["stats"]
        self.assertEqual(stats["original_parts"],89)
        self.assertEqual(stats["original_gaps"],284)
        self.assertEqual(stats["repeated_part_number_groups_reviewed"],5)
        self.assertEqual(stats["original_part_records_cross_referenced"],10)
        self.assertEqual(stats["repeated_gap_title_groups_reviewed"],2)
        self.assertEqual(stats["original_gap_records_cross_referenced"],4)
        self.assertEqual(stats["duplicate_part_numbers_unreviewed"],0)
        self.assertEqual(stats["identical_gap_titles_unreviewed"],0)
        self.assertEqual(set(self.report["parts_by_original_id"]),{
            "corrections-part-001","pcv-supply-part-001",
            "corrections-part-022","pcv-supply-part-002",
            "corrections-part-016","gate5-part-002",
            "b235rev-part-001","corrections-part-007",
            "b235rev-part-005","corrections-part-008"
        })
        self.assertEqual(set(self.report["gaps_by_original_id"]),{
            "gateac-gap-001","vinfit-gap-001","gateac-gap-002","vinfit-gap-003"
        })

    def test_original_document_claims_kept_with_scope_and_type(self):
        for p in self.report["part_claim_groups"]:
            self.assertTrue(p["nonmergeable"])
            self.assertFalse(p["factory_proof_of_cross_platform_VIN_fitment"])
            self.assertTrue(p["unresolved"])
            self.assertEqual(len(p["source_specific_original_claims"]),2)
            for original in p["source_specific_original_claims"]:
                self.assertEqual(original["original_part_number"],p["part_number"])
                self.assertTrue(original["original_source_ids"])
                self.assertTrue(original["original_urls"])
                self.assertIsInstance(original["original_applicability"],dict)
                self.assertIsInstance(original["original_relationships"],list)
                self.assertIsInstance(original["original_requirements"],list)

    def test_serial_boundary_conflict_never_flattened_to_one_hose_fitment(self):
        row=next(x for x in self.report["part_claim_groups"] if x["part_number"]=="5961610")
        self.assertTrue(row["source_scope_conflict"])
        factory=next(x for x in row["source_specific_original_claims"]
                     if x["record_id"]=="corrections-part-008")
        seller=next(x for x in row["source_specific_original_claims"]
                    if x["record_id"]=="b235rev-part-005")
        self.assertEqual(factory["original_evidence_status"],"documented")
        self.assertEqual(seller["original_evidence_status"],"supplier_claim")
        self.assertTrue(any("4000000–4017590" in x for x in factory["original_requirements"]))
        self.assertTrue(any("4017591" in x for x in
                            [seller["original_applicability"].get("model_years",""),
                             row["claim_review"],row["keep_distinct_reason"]]
                            if isinstance(x,str)))
        self.assertFalse(row["factory_proof_of_cross_platform_VIN_fitment"])

    def test_kit_for_old_switch_is_not_an_unconditional_supersession(self):
        row=next(x for x in self.report["part_claim_groups"] if x["part_number"]=="32021815")
        self.assertEqual(len(row["record_ids"]),2)
        self.assertTrue(all(x["original_relationships"] for x in row["source_specific_original_claims"]))
        self.assertIn("black lower sliding mechanism",row["claim_review"])
        self.assertIn("NOT a complete drop-in",row["claim_review"])
        self.assertFalse(row["factory_proof_of_cross_platform_VIN_fitment"])

    def test_older_pcvs_keep_factory_scope_and_supplier_only_cross_reference(self):
        x=next(r for r in self.report["part_claim_groups"] if r["part_number"]=="55561200")
        self.assertTrue(x["confirmed_same_factory_part_number"])
        platforms={z for o in x["source_specific_original_claims"]
                   for z in o["original_applicability"]["platforms"]}
        self.assertEqual(platforms,{"9-3-9400","9-5-9600"})
        y=next(r for r in self.report["part_claim_groups"] if r["part_number"]=="21341200")
        self.assertFalse(y["confirmed_same_factory_part_number"])
        self.assertIn("NOT",y["claim_review"] if "NOT" in y["claim_review"] else y["claim_review"].upper())
        self.assertIn("21341200C",y["claim_review"])

    def test_both_gap_pairs_remain_open_and_preserve_primary_source_context(self):
        blockers=self.report["open_shared_research_blockers"]
        self.assertEqual(len(blockers),2)
        for block in blockers:
            self.assertEqual(block["state"],"open_not_resolved")
            self.assertEqual(len(block["original_gap_records"]),2)
            self.assertTrue(block["remaining_work"])
            self.assertTrue(block["do_not_close_until"])
            for ref in block["original_gap_records"]:
                self.assertIsInstance(ref["missing_inputs"],list)
                self.assertTrue(ref["reason"])
        self.assertTrue(all(not x["resolved"] for x in self.report["gaps_by_original_id"].values()))

    def test_new_part_number_or_gap_overlap_must_be_manually_reconciled(self):
        mutated=copy.deepcopy(self.register)
        mutated["parts"].pop()
        with self.assertRaisesRegex(ValueError,"Unreviewed/stale"):
            build(self.datasets,mutated)
        mutated=copy.deepcopy(self.register)
        mutated["research_blockers"].pop()
        with self.assertRaisesRegex(ValueError,"Unreviewed/stale"):
            build(self.datasets,mutated)
        mutated=copy.deepcopy(self.register)
        mutated["research_blockers"][0]["state"]="resolved"
        with self.assertRaisesRegex(ValueError,"cannot be automatically closed"):
            build(self.datasets,mutated)
        mutated=copy.deepcopy(self.register)
        mutated["parts"][0]["factory_proof_of_cross_platform_VIN_fitment"]=True
        with self.assertRaisesRegex(ValueError,"unrestricted interchange"):
            build(self.datasets,mutated)

    def test_system_index_exposes_part_and_gap_aliases_without_using_them_to_rank(self):
        index=build_system(
            self.datasets,
            read("data/audits/system-evidence-routing-policy-20261014.json"),
            read("data/tier-research/methodology.json"),
            read("data/audits/legacy-issue-taxonomy-20261014.json"),
            read("data/tier-research/observations.json"),
            read("data/phase0-coverage-snapshot.json")
        )
        by_id={r["id"]:r for r in index["records"]}
        self.assertEqual(index["manually_reconciled_exact_part_groups"],5)
        self.assertEqual(index["manually_reconciled_shared_gap_blockers"],2)
        self.assertEqual(
            by_id["corrections-part-008"]["reviewed_same_number_part_claims"]["related_part_record_ids"],
            ["b235rev-part-005"])
        self.assertEqual(
            by_id["vinfit-gap-001"]["reviewed_shared_open_gap_blocker"]["canonical_open_blocker_id"],
            "blocker-us-my2008-09-og95-vin-tables")
        self.assertFalse(by_id["vinfit-gap-001"]["reviewed_shared_open_gap_blocker"]["resolved"])
        self.assertFalse(by_id["corrections-part-008"]["eligible_for_model_rating_from_this_index"])
        self.assertIsNone(by_id["corrections-issue-006"]["reviewed_same_number_part_claims"])

if __name__=="__main__":
    unittest.main()
