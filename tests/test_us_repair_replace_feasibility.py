"""Safeguards for US Saab conditional repair-vs-replace research coverage."""
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from build_us_feasibility_coverage import build, scenario_applies, OUTPUT, PRODUCTION, SCENARIOS


class USFeasibilityMatrixTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.prod = json.loads(PRODUCTION.read_text(encoding="utf-8"))
        cls.data = json.loads(SCENARIOS.read_text(encoding="utf-8"))
        cls.coverage = json.loads(OUTPUT.read_text(encoding="utf-8"))

    def test_exactly_reproducible_110_candidates(self):
        self.assertEqual(build(self.prod, self.data), self.coverage)
        self.assertEqual(self.coverage["market"], "US")
        self.assertEqual(len(self.prod["configurations"]), 110)
        self.assertEqual(len(self.coverage["production_group_reviews"]), 110)
        ids = [x["production_id"] for x in self.coverage["production_group_reviews"]]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(set(ids), {x["id"] for x in self.prod["configurations"]})

    def test_scenarios_are_evidence_scoped_and_no_fake_prices(self):
        items = self.data["scenarios"]
        self.assertEqual(len(items), 22)
        source_ids = {s["id"] for s in self.data["source_records"]}
        self.assertEqual(len(source_ids), len(self.data["source_records"]))
        self.assertEqual(len(items), len({s["id"] for s in items}))
        for s in items:
            with self.subTest(id=s["id"]):
                self.assertTrue(s["evidence_source_ids"])
                self.assertTrue(set(s["evidence_source_ids"]) <= source_ids)
                self.assertIsNone(s["price_estimate_usd"])
                self.assertIsNone(s["labor_hours_estimate"])
                self.assertFalse(s["part_interchange_approved"])
                self.assertFalse(s["rate_of_failure_established"])
                self.assertFalse(s["individual_vehicle_inspected"])
                self.assertTrue(s["inspection_and_diagnosis"]["next_evidence"])
                self.assertTrue(s["repair_options"])
                self.assertTrue(s["evidence_limits"])
                self.assertTrue(s["unknowns"])
                self.assertTrue(s["conditional_purchase_decision"])

    def test_scope_only_not_fault_counts_or_approvals(self):
        counts = self.coverage["counts"]
        self.assertEqual(counts["production_groups"], 110)
        self.assertEqual(counts["source_linked_scenarios"], 22)
        for key in ("individual_vehicles_inspected", "failure_rates_quantified",
                    "repair_prices_verified", "parts_interchanges_approved"):
            self.assertEqual(counts[key], 0)
        for group in self.coverage["production_group_reviews"]:
            self.assertFalse(group["individual_vehicle_inspection_completed"])
            self.assertFalse(group["price_or_kit_confirmed"])
            for m in group["scenario_links"]:
                self.assertEqual(m["applicability_status"],
                                 "scope_match_only_not_fault_diagnosis")
                self.assertFalse(m["actual_fault_confirmed"])
                self.assertFalse(m["replacement_authorized"])

    def test_sludge_covered_only_by_factory_early_year_engine_scope(self):
        targets = [x for x in self.coverage["production_group_reviews"]
                   if "us-feas-001" in [s["scenario_id"] for s in x["scenario_links"]]]
        self.assertEqual(len(targets), 28)
        for x in targets:
            self.assertIn(x["platform"], ("9400", "9600"))
            self.assertIn(x["engine_code"],
                          ("B205L", "B205R", "B235E", "B235L", "B235R"))
            self.assertLessEqual(x["model_year"], 2003)
            self.assertNotEqual(x["engine_code"], "B204L")
        for x in self.coverage["production_group_reviews"]:
            if x["platform"] == "650" or x["platform"] == "9440":
                self.assertNotIn("us-feas-001",
                                 [s["scenario_id"] for s in x["scenario_links"]])

    def test_fa57_early_93_coolant_requires_actual_vin(self):
        items = [x for x in self.coverage["production_group_reviews"]
                 for s in x["scenario_links"] if s["scenario_id"] == "us-feas-004"]
        self.assertEqual(len(items), 10)
        self.assertTrue(all(x["platform"] == "9440" and
                            2003 <= x["model_year"] <= 2005 and
                            x["automatic_gears"] == 5 for x in items))
        for x in self.coverage["production_group_reviews"]:
            for link in x["scenario_links"]:
                if link["scenario_id"] == "us-feas-004":
                    self.assertIn("51002378", link["additional_vehicle_vin_gate"])

    def test_family_and_year_specific_specialist_cases(self):
        counts = self.coverage["counts"]["matching_links_by_scenario"]
        self.assertEqual(counts["us-feas-005"], 17)
        self.assertEqual(counts["us-feas-006"], 6)
        self.assertEqual(counts["us-feas-007"], 6)
        self.assertEqual(counts["us-feas-011"], 64)
        self.assertEqual(counts["us-feas-012"], 34)
        self.assertEqual(counts["us-feas-013"], 110)
        self.assertEqual(counts["us-feas-014"], 42)
        # A year-specific WIS page never becomes a universal diagnosis.
        for x in self.coverage["production_group_reviews"]:
            ids = [s["scenario_id"] for s in x["scenario_links"]]
            if "us-feas-006" in ids:
                self.assertEqual((x["platform"], x["model_year"]),
                                 ("9600", 2007))
            if "us-feas-007" in ids:
                self.assertEqual(x["platform"], "9440")
                self.assertEqual(x["automatic_gears"], 6)

    def test_legacy_original_four_speed_and_mechanical_screens(self):
        counts = self.coverage["counts"]["matching_links_by_scenario"]
        self.assertEqual(
            [counts[f"us-feas-{i:03d}"] for i in (15, 16, 17, 18)],
            [4, 13, 11, 22])
        expected = {
            "us-feas-015": ("9400", "engine", "B204L"),
            "us-feas-016": ("9600", "engine", "B308E"),
            "us-feas-017": ("9400", "transmission", None),
            "us-feas-018": ("9600", "transmission", None),
        }
        prod_by_id = {x["id"]: x for x in self.prod["configurations"]}
        scenarios = {x["id"]: x for x in self.data["scenarios"]}
        for sid, (platform, system, engine) in expected.items():
            with self.subTest(sid=sid):
                self.assertEqual(scenarios[sid]["system"], system)
                matches = [prod_by_id[x["production_id"]]
                           for x in self.coverage["production_group_reviews"]
                           if sid in [link["scenario_id"] for link in x["scenario_links"]]]
                self.assertTrue(matches)
                self.assertTrue(all(x["platform"] == platform for x in matches))
                if engine:
                    self.assertTrue(all(x["engine_code"] == engine for x in matches))
                if system == "transmission":
                    self.assertTrue(all(x["automatic_gears"] == 4 for x in matches))
                self.assertFalse(scenarios[sid]["rate_of_failure_established"])
                self.assertIsNone(scenarios[sid]["price_estimate_usd"])

    def test_b284_lhu_late_fa57_and_new_95_af40_are_research_not_approvals(self):
        expected = {
            "us-feas-019": (6, "9440", "engine", "B284L", None),
            "us-feas-020": (1, "650", "engine", None, 6),
            "us-feas-021": (18, "9440", "transmission", None, 5),
            "us-feas-022": (1, "650", "transmission", None, 6),
        }
        counts = self.coverage["counts"]["matching_links_by_scenario"]
        sc = {x["id"]: x for x in self.data["scenarios"]}
        for sid, (n, platform, system, engine, gears) in expected.items():
            with self.subTest(sid=sid):
                self.assertEqual(counts[sid], n)
                self.assertEqual(sc[sid]["system"], system)
                self.assertFalse(sc[sid]["individual_vehicle_inspected"])
                self.assertFalse(sc[sid]["rate_of_failure_established"])
                self.assertFalse(sc[sid]["part_interchange_approved"])
                self.assertIsNone(sc[sid]["price_estimate_usd"])
                rows = [x for x in self.coverage["production_group_reviews"]
                        if sid in {v["scenario_id"] for v in x["scenario_links"]}]
                self.assertEqual(len(rows), n)
                self.assertTrue(all(x["platform"] == platform for x in rows))
                if engine is not None:
                    self.assertTrue(all(x["engine_code"] == engine for x in rows))
                if gears is not None:
                    self.assertTrue(all(x["automatic_gears"] == gears for x in rows))
        self.assertIn("factory_engine_VIN_required", sc["us-feas-020"]["applicability"])
        self.assertIn("factory_vin_gate", sc["us-feas-022"]["applicability"])
        self.assertTrue(all(not x["individual_vehicle_inspection_completed"]
                            for x in self.coverage["production_group_reviews"]))

    def test_refuse_source_free_or_price_populated_claim(self):
        bad = json.loads(json.dumps(self.data))
        bad["scenarios"][0]["price_estimate_usd"] = 500
        with self.assertRaises(ValueError):
            build(self.prod, bad)
        bad = json.loads(json.dumps(self.data))
        bad["scenarios"][0]["evidence_source_ids"] = ["fabricated"]
        with self.assertRaises(ValueError):
            build(self.prod, bad)
        bad = json.loads(json.dumps(self.data))
        bad["scenarios"][0]["part_interchange_approved"] = True
        with self.assertRaises(ValueError):
            build(self.prod, bad)

    def test_existing_canadian_records_not_imported(self):
        self.assertEqual(self.data["market"], "US")
        self.assertTrue(all(x["model"] in ("9-3", "9-5")
                            for x in self.coverage["production_group_reviews"]))


if __name__ == "__main__":
    unittest.main()
