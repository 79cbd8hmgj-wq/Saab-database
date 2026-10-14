"""Reviewed routes preserve source records and never close research gaps."""
import copy
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from database import load_datasets
from build_system_evidence_index import build, check_policy


def read(path):
    return json.loads((ROOT / path).read_text())


class FactGapNavigationReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.datasets = load_datasets()
        cls.policy = read("data/audits/system-evidence-routing-policy-20261014.json")
        cls.method = read("data/tier-research/methodology.json")
        cls.report = build(cls.datasets, cls.policy, cls.method,
                           read("data/audits/legacy-issue-taxonomy-20261014.json"),
                           read("data/tier-research/observations.json"),
                           read("data/phase0-coverage-snapshot.json"))
        cls.rows = {r["id"]: r for r in cls.report["records"]}

    def test_all_legacy_cross_cutting_and_multisystem_fact_gap_candidates_reviewed(self):
        reviews = self.policy["explicit_fact_gap_routes"]
        self.assertEqual(sum(r["kind"] == "facts" for r in reviews.values()), 337)
        self.assertEqual(sum(r["kind"] == "gaps" for r in reviews.values()), 80)
        for id_, review in reviews.items():
            row = self.rows[id_]
            self.assertEqual(row["system_ids_for_discovery"], review["system_ids"])
            self.assertEqual(row["routing_basis"], "curated_explicit_fact_gap_navigation")
            self.assertEqual(row["manual_navigation_review"], review)
            self.assertFalse(row["eligible_for_model_rating_from_this_index"])
            if row["kind"] == "gaps":
                self.assertFalse(row["resolved_by_this_index"])

    def test_vin_and_catalogue_access_remain_cross_cutting(self):
        for id_ in ("gate5-fact-004", "vinfit-fact-006", "epcverify-fact-001",
                    "gateac-gap-001", "vinfit-gap-006", "usparts-gap-002"):
            self.assertEqual(self.rows[id_]["system_ids_for_discovery"], [], id_)
            self.assertTrue(self.rows[id_]["manual_navigation_review"]["reason"])

    def test_concrete_saved_specs_remedies_and_quotes_are_retrievable(self):
        expected = {"corrections-fact-003": "engine_core_oil_pcv",
                    "prebuy-fact-020": "transmission_driveline",
                    "wp7-fact-021": "restraints_safety",
                    "usparts-fact-001": "cooling_heat",
                    "usparts-fact-009": "charging_starting_wiring",
                    "turbsol-gap-007": "transmission_driveline"}
        for id_, system in expected.items():
            self.assertIn(system, self.rows[id_]["system_ids_for_discovery"])
        self.assertEqual(self.rows["usparts-fact-001"]["original_evidence_status"],
                         "supplier_claim")

    def test_review_rejects_wrong_kind_unknown_system_or_blank_reason(self):
        for field, value in (("kind", "parts"), ("system_ids", ["fake-system"]),
                             ("system_ids", ["cooling_heat", "cooling_heat"]),
                             ("reason", "")):
            policy = copy.deepcopy(self.policy)
            policy["explicit_fact_gap_routes"]["usparts-fact-001"][field] = value
            with self.assertRaises(ValueError):
                check_policy(policy, self.method, self.datasets)

    def test_modified_original_record_requires_review_refresh(self):
        datasets = copy.deepcopy(self.datasets)
        record = next(r for d in datasets for r in d["facts"]
                      if r["id"] == "usparts-fact-001")
        record["value"] = 0
        with self.assertRaisesRegex(ValueError, "Stale fact/gap navigation review"):
            check_policy(self.policy, self.method, datasets)

    def test_review_must_reference_an_existing_record(self):
        policy = copy.deepcopy(self.policy)
        policy["explicit_fact_gap_routes"]["missing-fact"] = copy.deepcopy(
            policy["explicit_fact_gap_routes"]["usparts-fact-001"])
        with self.assertRaises(ValueError):
            check_policy(policy, self.method, self.datasets)

    def test_unreviewed_cli_queue_excludes_deliberate_cross_cutting_decisions(self):
        result = subprocess.run(
            [sys.executable, "tools/build_system_evidence_index.py", "--review",
             "--review-unreviewed-only", "--review-limit", "0"],
            cwd=ROOT, text=True, capture_output=True, check=True)
        queue = json.loads(result.stdout)
        expected = {r["id"] for r in self.report["records"]
                    if r["review_status"] == "not_manually_adjudicated"
                    and (r["cross_cutting_or_unresolved_system"]
                         or r["possible_multiple_systems"])}
        self.assertEqual({r["id"] for r in queue["review_records"]}, expected)
        self.assertFalse(queue["truncated"])
        self.assertTrue(queue["unreviewed_only"])
        self.assertNotIn("gateac-gap-001", expected)


if __name__ == "__main__":
    unittest.main()
