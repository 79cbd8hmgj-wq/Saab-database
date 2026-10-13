"""Regression checks for cautious US Saab repair-versus-replace feasibility.

The matrix describes which diagnostic *questions* to ask. It does not predict
fault incidence, assert an individual VIN/campaign, certify parts or quote cost.
"""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from build_us_repair_feasibility_coverage import build, applies

PROD = ROOT / "data/vehicle-catalogue/us-production-normalized.json"
FEAS = ROOT / "data/vehicle-catalogue/us-repair-replace-feasibility.json"
COVER = ROOT / "data/vehicle-catalogue/us-repair-feasibility-coverage.json"

class FeasibilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.prod = json.loads(PROD.read_text(encoding="utf-8"))
        cls.feas = json.loads(FEAS.read_text(encoding="utf-8"))
        cls.cover = json.loads(COVER.read_text(encoding="utf-8"))
        cls.scenarios = {x["id"]: x for x in cls.feas["scenarios"]}

    def test_source_references_resolve_to_existing_source_file(self):
        self.assertEqual(len(self.scenarios), 14)
        all_known = {}
        for source_file in set(x["source_file"] for x in self.feas["source_records"]):
            data = json.loads((ROOT / source_file).read_text(encoding="utf-8"))
            collection = "research_sources" if "research_sources" in data else "source_records" if "source_records" in data else "sources"
            for src in data[collection]:
                all_known[src["id"]] = src
        refs = {x["id"]: x for x in self.feas["source_records"]}
        self.assertEqual(len(refs), 37)
        for ref in refs.values():
            with self.subTest(source=ref["id"]):
                self.assertIn(ref["id"], all_known)
                self.assertEqual(ref["url"], all_known[ref["id"]]["url"])
                self.assertTrue(ref["url"].startswith("https://"))
        for scenario in self.scenarios.values():
            for sid in scenario["evidence_source_ids"]:
                self.assertIn(sid, refs)

    def test_missing_price_and_no_false_approvals(self):
        for scenario in self.scenarios.values():
            with self.subTest(id=scenario["id"]):
                self.assertIsNone(scenario["price_estimate_usd"])
                self.assertIsNone(scenario["labor_hours_estimate"])
                self.assertFalse(scenario["part_interchange_approved"])
                self.assertFalse(scenario["rate_of_failure_established"])
                self.assertFalse(scenario["individual_vehicle_inspected"])
                self.assertTrue(scenario["inspection_and_diagnosis"]["next_evidence"])
                self.assertTrue(scenario["repair_options"])
                self.assertTrue(scenario["evidence_limits"])
                self.assertTrue(scenario["unknowns"])
                self.assertIn("when_testing_unavailable", scenario["conditional_purchase_decision"])
        self.assertEqual(self.feas["market"], "US")
        self.assertEqual(self.feas["candidate_scope"]["drivetrain"], "FWD")

    def test_precise_bulletin_scope_no_implied_incidence(self):
        rule = self.scenarios["us-feas-001"]
        self.assertEqual(rule["applicability"]["model_year_range_by_platform"]["9600"],
                         [1998, 2003])
        self.assertEqual(rule["applicability"]["model_year_range_by_platform"]["9400"],
                         [1999, 2003])
        self.assertEqual(rule["evidence_source_ids"][0], "hcdiag-src-001")
        prod = self.prod["configurations"]
        caught = [x for x in prod if applies(rule, x)]
        self.assertEqual(len(caught), 28)
        self.assertFalse(any(x["engine_code"] in ("B204L", "B207L", "B207R",
                                                  "B284L", "B308E")
                             for x in caught))
        self.assertFalse(any(x["model_year"] > 2003 for x in caught))

    def test_coolant_ATF_requires_individual_vin(self):
        rule = self.scenarios["us-feas-004"]
        self.assertIn("51002378", rule["applicability"]["vin_gate"])
        affected = [x for x in self.prod["configurations"] if applies(rule, x)]
        self.assertEqual(len(affected), 10)
        coverage = [
            x for row in self.cover["model_groups"]
            for x in row["applicable_research_checks"]
            if x["scenario_id"] == rule["id"]]
        self.assertEqual(len(coverage), 10)
        self.assertTrue(all(x["screen_status"] == "VIN_condition_unresolved"
                            for x in coverage))
        self.assertTrue(all(not x["fault_diagnosed"] for x in coverage))

    def test_all_110_groups_reproducible_and_not_failing(self):
        self.assertEqual(build(self.prod, self.feas), self.cover)
        self.assertEqual(len(self.cover["model_groups"]), 110)
        self.assertEqual(
            {x["production_configuration_id"] for x in self.cover["model_groups"]},
            {x["id"] for x in self.prod["configurations"]})
        for row in self.cover["model_groups"]:
            self.assertFalse(row["factory_vehicle_VIN_seen"])
            self.assertFalse(row["individual_mechanical_condition_verified"])
            self.assertFalse(row["repair_budget_verified"])
            for screening in row["applicable_research_checks"]:
                self.assertIn(screening["scenario_id"], self.scenarios)
                self.assertFalse(screening["fault_diagnosed"])
                self.assertFalse(screening["actual_symptom_reported"])
                self.assertFalse(screening["vehicle_repair_approved"])
        for row in self.cover["scenario_coverage"]:
            self.assertEqual(row["actual_confirmed_faults"], 0)
            self.assertEqual(row["cars_inspected"], 0)

    def test_full_safety_screen_but_powertrain_gaps_remain(self):
        model_groups = self.cover["model_groups"]
        self.assertTrue(all(
            any(x["scenario_id"] == "us-feas-013" for x in g["applicable_research_checks"])
            for g in model_groups))
        missing = [g for g in model_groups if not g["has_powertrain_specific_research"]]
        self.assertEqual(len(missing), 14)
        self.assertEqual(
            {(x["platform"], x["engine_code"]) for x in missing},
            {("9400", "B204L"), ("9600", "B308E"), ("650", None)})
        self.assertTrue(any(x["name"].startswith("Original 9-5 rear subframe")
                            for x in self.feas["scenarios"]))

if __name__ == "__main__":
    unittest.main()
