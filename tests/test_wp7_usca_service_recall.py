"""Regression tests for source-scoped US/Canada service/recall work package 7."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/datasets/priority-usca-service-recall-baseline-wp7.json"


class SourceScopedUSCAServiceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(DATA.read_text(encoding="utf-8"))
        cls.facts = {f["predicate"]: f for f in cls.data["facts"]}

    def test_historical_nhtsa_lookup_is_never_a_full_recall_clearance(self):
        self.assertIs(self.facts["vin_lookup_excludes_more_than_15_year_old_recalls"]["value"], True)
        self.assertIs(self.facts["vin_lookup_excludes_completed_recall_repairs"]["value"], True)
        self.assertIs(self.facts["vin_lookup_does_not_show_non_safety_service_campaigns"]["value"], True)
        self.assertEqual(self.data["issues"][0]["id"], "wp7-issue-001")

    def test_2008_9_5_usca_schedule_is_not_universal(self):
        for key in ("brake_fluid_change_interval", "automatic_transmission_fluid_change_interval", "spark_plug_change_interval"):
            scope = self.facts[key]["applicability"]
            self.assertEqual(scope["platforms"], ["9-5-9600"])
            self.assertEqual(scope["model_years"], [2008])
            self.assertEqual(scope["markets"], ["US", "CA"])
        self.assertIn("automatic", self.facts["automatic_transmission_fluid_change_interval"]["applicability"]["transmission_codes"])

    def test_2006_9_3_is_only_a_service_classification_not_an_interval(self):
        record = self.facts["intermediate_vs_main_service_types"]
        self.assertEqual(record["applicability"]["platforms"], ["9-3-9440"])
        self.assertEqual(record["applicability"]["model_years"], [2006])
        self.assertIsInstance(record["value"], dict)
        self.assertNotIn("miles", record["value"])
        self.assertTrue(any("US/Canada 2005-06" in g["title"] for g in self.data["gaps"]))


if __name__ == "__main__":
    unittest.main()
