"""Factory-vs-supplier evidence and configuration boundary tests for mounting research."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from database import filter_records, inventory, load_datasets, validate_datasets


class SubframePartsAndBrakeLinesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = load_datasets()
        cls.domain = next(d for d in cls.data if d["domain"] == "subframe_parts_brake_lines")
        cls.parts = {p["part_number"]: p for p in cls.domain["parts"]}
        cls.facts = {f["id"]: f for f in cls.domain["facts"]}

    def test_data_and_inventory(self):
        self.assertEqual(validate_datasets(self.data), [])
        self.assertEqual(len(self.domain["sources"]), 17)
        self.assertEqual(len(self.domain["parts"]), 15)
        self.assertEqual(len(self.domain["facts"]), 16)
        self.assertEqual(len(self.domain["gaps"]), 9)
        summary = inventory(self.data)
        self.assertEqual(summary["counts"]["sources"], 185)
        self.assertEqual(summary["counts"]["facts"], 356)
        self.assertEqual(summary["counts"]["parts"], 48)
        self.assertEqual(summary["counts"]["gaps"], 79)

    def test_catalogue_parts_never_claim_factory_approval(self):
        for part in self.domain["parts"]:
            self.assertEqual(part["evidence_status"], "supplier_claim")
            self.assertEqual(part["review_status"], "needs_vehicle_verification")

    def test_fwd_sedan_wagon_subframe_excludes_convertible(self):
        item = self.parts["32022623"]
        self.assertEqual(item["applicability"]["body_styles"], ["4D", "5D"])
        self.assertNotIn("CV", item["applicability"]["body_styles"])
        self.assertEqual(item["relationships"][0]["type"], "supersedes")
        self.assertEqual(item["relationships"][0]["part_number"], "12825111")
        self.assertIn("engine mount", " ".join(item["requirements"]).lower())

    def test_convertible_rear_special_bushing_is_conditional(self):
        item = self.parts["12759331"]
        self.assertEqual(item["applicability"]["body_styles"], ["CV"])
        self.assertIn("without front axle stay", " ".join(item["requirements"]).lower())

    def test_early_chassis_stays_separate(self):
        early = self.parts["24401525"]
        self.assertEqual(early["applicability"]["model_years"], [2003, 2004])
        self.assertFalse(any(r["part_number"] == "32022623" for r in early["relationships"]))

    def test_factory_torques_remain_distinct_from_catalogue(self):
        fwd = self.facts["mountbrake-fact-001"]
        og95 = self.facts["mountbrake-fact-005"]
        self.assertEqual(fwd["value"], "75 Nm plus 135 degrees")
        self.assertEqual(og95["value"], "100 Nm plus 45 degrees")
        self.assertNotEqual(fwd["applicability"]["platforms"], og95["applicability"]["platforms"])
        self.assertEqual(fwd["evidence_status"], "documented")

    def test_brake_line_source_year_remains_scope_limited(self):
        rows = filter_records(self.data, platform="9-5-9600", year=2008)
        self.assertIn("mountbrake-fact-009", {r["id"] for r in rows})
        rows = filter_records(self.data, platform="9-5-9600", year=2005)
        self.assertNotIn("mountbrake-fact-009", {r["id"] for r in rows})


if __name__ == "__main__":
    unittest.main()
