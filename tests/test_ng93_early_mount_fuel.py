"""Regression tests for factory-vs-catalogue scope and MY2003–05 NG9-3 evidence."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from database import load_datasets, validate_datasets


class EarlyNG93MountAndFuelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.datasets = load_datasets()
        cls.domain = next(d for d in cls.datasets if d["domain"] == "ng93_early_mount_fuel")
        cls.facts = {x["id"]: x for x in cls.domain["facts"]}
        cls.parts = {x["part_number"]: x for x in cls.domain["parts"]}

    def test_integrity_and_counts(self):
        self.assertEqual(validate_datasets(self.datasets), [])
        self.assertEqual(len(self.domain["sources"]), 15)
        self.assertEqual(len(self.domain["facts"]), 20)
        self.assertEqual(len(self.domain["parts"]), 5)
        self.assertEqual(len(self.domain["gaps"]), 7)

    def test_chassis_suffix_boundaries_not_turned_into_crossfit(self):
        old = self.parts["12831387"]
        new = self.parts["12805522"]
        self.assertEqual(old["applicability"]["vin_ranges"][0]["end"], "56000012")
        self.assertEqual(new["applicability"]["vin_ranges"][0]["start"], "56000013")
        self.assertEqual(old["applicability"]["body_styles"], ["CV"])
        self.assertEqual(new["applicability"]["body_styles"], ["CV"])
        self.assertEqual(old["relationships"], [])
        self.assertEqual(new["relationships"], [])
        self.assertEqual(new["applicability"]["engine_codes"], ["B284", "B207R", "B207E", "B207L"])

    def test_supplier_only_supersession_is_not_factory_verified(self):
        candidate = self.parts["12762720"]
        self.assertEqual(candidate["evidence_status"], "supplier_claim")
        self.assertEqual(candidate["review_status"], "needs_vehicle_verification")
        self.assertEqual(candidate["relationships"][0]["part_number"], "32022623")
        self.assertIn("omits it", candidate["relationships"][0]["conditions"].lower())

    def test_factory_fuel_inspections_are_exactly_year_scoped(self):
        a = self.facts["early9three-fact-010"]
        b = self.facts["early9three-fact-012"]
        self.assertEqual(a["applicability"]["model_years"], [2004])
        self.assertEqual(b["applicability"]["model_years"], [2005])
        self.assertEqual(a["evidence_status"], "documented")
        self.assertEqual(b["evidence_status"], "documented")

    def test_b207_specific_mounting_not_extended_to_z18xe(self):
        row = self.facts["early9three-fact-004"]
        self.assertEqual(row["applicability"]["engine_codes"], ["B207"])
        self.assertEqual(row["applicability"]["model_years"], [2005])
        other = self.facts["early9three-fact-017"]
        self.assertEqual(other["applicability"]["engine_codes"], ["Z18XE"])
        self.assertEqual(other["applicability"]["model_years"], [2004])

    def test_early_catalogue_exceptions_do_not_claim_order_fit(self):
        for p in self.domain["parts"]:
            self.assertEqual(p["evidence_status"], "supplier_claim")
            self.assertEqual(p["review_status"], "needs_vehicle_verification")
        self.assertTrue(any("PI 08-01" in g["title"] for g in self.domain["gaps"]))


if __name__ == "__main__":
    unittest.main()
