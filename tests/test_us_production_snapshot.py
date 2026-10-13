"""Checked-in US production snapshot scope and evidence integrity regression tests.

A third-party production compilation is NOT a factory VIN or reliability certificate.
"""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PRODUCTION = ROOT / "data/vehicle-catalogue/us-production-normalized.json"
EXISTING = ROOT / "data/vehicle-catalogue/north-america-1998-2011.json"


class USProductionSnapshotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(PRODUCTION.read_text(encoding="utf-8"))
        cls.previous = json.loads(EXISTING.read_text(encoding="utf-8"))

    def test_source_counts_and_immutable_individual_source_provenance(self):
        data = self.data
        self.assertEqual(data["markets"], ["US"])
        self.assertEqual(len(data["sources"]), 4)
        byid = {s["id"]: s for s in data["sources"]}
        self.assertEqual(set(byid), {
            "na-cat-usprod-9400", "na-cat-usprod-9440",
            "na-cat-usprod-9600", "na-cat-usprod-650"})
        self.assertTrue(all(
            s["all_vehicle_total_reconciles"] is True
            and s["parsed_paint_rows"] > 0
            and s["published_all_vehicle_total"] == s["total_from_paint_rows"]
            and s["input_sha256"] and s["url"].startswith("https://")
            for s in data["sources"]
        ))
        self.assertTrue(all(
            len(x["source_ids"]) == 1 and x["source_ids"][0] in byid
            and x["requires_vehicle_verification"] is True
            and x["evidence_status"] == "third_party_compiled_US_production"
            for x in data["configurations"]
        ))

    def test_normalized_groups_only_eligible_and_unambiguous(self):
        items = self.data["configurations"]
        ids = [x["id"] for x in items]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertGreater(len(items), 100)
        for x in items:
            with self.subTest(id=x["id"]):
                self.assertEqual(x["market"], "US")
                self.assertIn(x["model"], ("9-3", "9-5"))
                self.assertIn(x["platform"], ("9400", "9440", "9600", "650"))
                self.assertGreaterEqual(x["model_year"], 1998)
                self.assertLessEqual(x["model_year"], 2011)
                self.assertEqual(x["drivetrain"], "FWD")
                self.assertIn(x["automatic_gears"], (4, 5, 6))
                self.assertIsNone(x["transmission_code"])  # manufacturer code unknown
                self.assertNotIn(x["body_code"], ("CV",))
                self.assertIn(x["body_style"], (
                    "sedan", "3-door hatchback", "5-door hatchback", "wagon"))
                self.assertGreater(x["reported_production_count"], 0)
                self.assertGreater(x["paint_row_count"], 0)
                self.assertEqual(x["low_volume_manual_review"],
                                 x["reported_production_count"] <= 12)
                if x["platform"] == "9400" and x["body_code"] == "5D":
                    self.assertEqual(x["body_style"], "5-door hatchback")
                if x["platform"] in ("9440", "9600") and x["body_code"] == "5D":
                    self.assertEqual(x["body_style"], "wagon")

    def test_model_year_rollup_recomputes_exactly(self):
        rows = self.data["year_model_screening"]
        self.assertEqual(len(rows), 28)
        for row in rows:
            matching = [x for x in self.data["configurations"]
                        if x["model"] == row["model"]
                        and x["model_year"] == row["model_year"]]
            self.assertEqual(
                row["normalized_US_automatic_FWD_nonconvertible_groups"],
                len(matching))
            self.assertEqual(
                row["compiled_production_count_for_eligible_groups"],
                sum(x["reported_production_count"] for x in matching))
            self.assertFalse(row["factory_exhaustiveness_certified"])
            self.assertEqual(
                row["register_status"] == "observed_matching_production_rows",
                bool(matching))

    def test_2003_platform_break_2010_ng95_xwd_absence_and_2011_fwd(self):
        items = self.data["configurations"]
        self.assertFalse(any(
            x["model"] == "9-3" and x["model_year"] == 2003
            and x["platform"] == "9400" for x in items))
        self.assertFalse(any(
            x["model"] == "9-5" and x["model_year"] == 2010 for x in items))
        self.assertTrue(any(
            x["model"] == "9-5" and x["model_year"] == 2011
            and x["platform"] == "650" and x["trim"] == "Turbo4"
            and x["automatic_gears"] == 6 for x in items))

    def test_prior_canadian_research_remains_separate(self):
        old = self.previous
        self.assertEqual(set(old["rules"]["markets"]), {"US", "CA"})
        self.assertTrue(any(
            "CA" in x["market_evidence"] for x in old["documented_configuration_examples"]))
        self.assertTrue(all(
            x["market"] == "US" for x in self.data["configurations"]))

    def test_legacy_us_candidates_have_at_least_one_matching_group(self):
        # Match on model-year/platform/body/automatic gears; add engine-code
        # match only when the old pilot actually documented it.
        old = [x for x in self.previous["documented_configuration_examples"]
               if "US" in x["market_evidence"]]
        for candidate in old:
            with self.subTest(id=candidate["id"]):
                self.assertTrue(any(
                    x["model"] == candidate["model"]
                    and x["platform"] == candidate["platform"]
                    and x["model_year"] == candidate["model_year"]
                    and x["body_style"] == candidate["body_style"]
                    and x["automatic_gears"] == candidate["automatic_gears"]
                    and (candidate["engine_code"] is None
                         or x["engine_code"] == candidate["engine_code"])
                    for x in self.data["configurations"]
                ), candidate["id"])


if __name__ == "__main__":
    unittest.main()
