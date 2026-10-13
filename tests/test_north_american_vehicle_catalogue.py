"""Regression checks for the incremental North American automatic/FWD candidate catalogue.

This is a catalogue consistency test, not certification of factory fitment.
"""
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CATALOGUE = ROOT / "data/vehicle-catalogue/north-america-1998-2011.json"
SCOPE = ROOT / "data/audits/candidate-scope-1998-2011.json"


class NorthAmericanVehicleCatalogueTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalogue = json.loads(CATALOGUE.read_text(encoding="utf-8"))
        cls.scope = json.loads(SCOPE.read_text(encoding="utf-8"))
        cls.sources = {s["id"]: s for s in cls.catalogue["source_records"]}
        cls.examples = cls.catalogue["documented_configuration_examples"]
        cls.rows = cls.catalogue["model_year_screening"]

    def test_complete_screening_denominator_without_claiming_complete_research(self):
        expected = {(model, year) for model in ("9-3", "9-5") for year in range(1998, 2012)}
        observed = [(r["model"], r["model_year"]) for r in self.rows]
        self.assertEqual(len(observed), 28)
        self.assertEqual(set(observed), expected)
        self.assertEqual(len(observed), len(set(observed)))
        self.assertTrue(all(r["coverage_complete"] is False for r in self.rows))

    def test_scope_matches_decision_file(self):
        self.assertEqual(set(self.scope["eligible_markets"]), {"US", "CA"})
        self.assertEqual(self.catalogue["rules"]["markets"], ["US", "CA"])
        self.assertEqual(self.catalogue["rules"]["drive"], "FWD")
        self.assertEqual(self.catalogue["rules"]["transmission"], "factory automatic")
        self.assertIn("convertible", self.catalogue["rules"]["body_excluded"])

    def test_examples_only_include_qualified_market_configuration(self):
        ids = [r["id"] for r in self.examples]
        self.assertEqual(len(ids), len(set(ids)))
        source_ids = [s["id"] for s in self.catalogue["source_records"]]
        self.assertEqual(len(source_ids), len(set(source_ids)))
        for item in self.examples:
            with self.subTest(id=item["id"]):
                self.assertIn(item["model"], {"9-3", "9-5"})
                self.assertGreaterEqual(item["model_year"], 1998)
                self.assertLessEqual(item["model_year"], 2011)
                self.assertIn(item["platform"], {"9400", "9440", "9600", "650"})
                self.assertEqual(item["drivetrain"], "FWD")
                self.assertNotIn("convertible", item["body_style"].lower())
                self.assertGreater(item["automatic_gears"], 0)
                self.assertTrue(item["market_evidence"])
                self.assertTrue(item["source_ids"])
                self.assertIsNone(item["transmission_code"])  # no gearbox-code guessing in first batch
                for market in item["market_evidence"]:
                    self.assertIn(market, ("US", "CA"))
                    self.assertTrue(any(market in self.sources[sid]["market_scope"] for sid in item["source_ids"]))
                for source_id in item["source_ids"]:
                    self.assertIn(source_id, self.sources)

    def test_all_sampled_configurations_link_from_screening_row(self):
        for item in self.examples:
            rows = [r for r in self.rows if r["model"] == item["model"] and r["model_year"] == item["model_year"]]
            self.assertEqual(len(rows), 1)
            self.assertIn(item["id"], rows[0]["documented_configuration_ids"])
            for market in item["market_evidence"]:
                key = "us_status" if market == "US" else "canada_status"
                self.assertEqual(rows[0][key], "at_least_one_candidate_documented")

    def test_restricted_launches_and_manual_only_packages_not_promoted(self):
        self.assertFalse(any(r["model_year"] == 1998 and "US" in r["market_evidence"] for r in self.examples))
        self.assertFalse(any(r["model"] == "9-5" and r["model_year"] == 2010 and "US" in r["market_evidence"] for r in self.examples))
        self.assertFalse(any("viggen" in r["engine_label"].lower() for r in self.examples))
        excluded_ids = [e["id"] for e in self.catalogue["explicit_exclusions"]]
        self.assertEqual(len(excluded_ids), len(set(excluded_ids)))
        for excluded in self.catalogue["explicit_exclusions"]:
            with self.subTest(id=excluded["id"]):
                self.assertIn(excluded["market"], ("US", "CA"))
                self.assertTrue(excluded["source_ids"])
                for source_id in excluded["source_ids"]:
                    self.assertIn(source_id, self.sources)


if __name__ == "__main__":
    unittest.main()
