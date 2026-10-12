"""Phase 0 regression tests: source and year boundaries for NG 9-3 body research."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from database import load_datasets, filter_records, validate_datasets, inventory


class NG93StructureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.datasets = load_datasets()
        cls.domain = next(d for d in cls.datasets if d["domain"] == "ng93_structure")

    def test_integrated_records_have_valid_provenance(self):
        self.assertEqual(validate_datasets(self.datasets), [])
        self.assertEqual(len(self.domain["sources"]), 21)
        self.assertEqual(len(self.domain["facts"]), 30)

    def test_main_body_facts_do_not_spread_to_other_platform_or_year(self):
        for year, platform in ((2005, "9-3-9440"), (2006, "9-5-9600")):
            rows = filter_records(self.datasets, platform=platform, year=year)
            self.assertNotIn("ng93structure-fact-004", {r["id"] for r in rows})
        rows = filter_records(self.datasets, platform="9-3-9440", year=2006)
        self.assertIn("ng93structure-fact-004", {r["id"] for r in rows})

    def test_historical_lift_guidance_stays_year_2004(self):
        rows_2004 = filter_records(self.datasets, platform="9-3-9440", year=2004)
        rows_2006 = filter_records(self.datasets, platform="9-3-9440", year=2006)
        self.assertIn("ng93structure-fact-023", {r["id"] for r in rows_2004})
        self.assertNotIn("ng93structure-fact-023", {r["id"] for r in rows_2006})

    def test_convertible_and_b207_scope_is_preserved(self):
        r = next(x for x in self.domain["facts"] if x["id"] == "ng93structure-fact-016")
        self.assertEqual(r["applicability"]["engine_codes"], ["B207"])
        self.assertEqual(r["applicability"]["body_styles"], ["CV"])
        self.assertEqual(r["unit"], "Nm")
        self.assertEqual(r["value"], 50)

    def test_rear_chassis_fasteners_are_not_subframe_fasteners(self):
        rear_cv = next(x for x in self.domain["facts"] if x["id"] == "ng93structure-fact-014")
        rear_subframe = next(x for x in self.domain["facts"] if x["id"] == "ng93structure-fact-021")
        self.assertNotEqual(rear_cv["subject"], rear_subframe["subject"])
        self.assertEqual(rear_cv["value"], rear_subframe["value"])
        self.assertNotEqual(rear_cv["source_ids"], rear_subframe["source_ids"])

    def test_source_boundaries_and_inventory(self):
        report = inventory(self.datasets)
        self.assertEqual(report["counts"]["sources"], 168)
        self.assertEqual(report["counts"]["facts"], 340)
        self.assertEqual(report["counts"]["parts"], 33)
        self.assertEqual(report["counts"]["gaps"], 70)


if __name__ == "__main__":
    unittest.main()
