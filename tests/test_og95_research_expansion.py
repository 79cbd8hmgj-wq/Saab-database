"""Regression checks for the Phase 0 OG 9-5 structural/year-specific research."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from database import filter_records, load_datasets, validate_datasets


class ExpansionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.datasets = load_datasets()

    def test_all_research_records_validate(self):
        self.assertEqual(validate_datasets(self.datasets), [])

    def test_2006_2008_us_owner_specs_remain_separate(self):
        rows = filter_records(
            self.datasets, platform="9-5-9600", year=2008, market="US"
        )
        ids = {r["id"] for r in rows}
        self.assertIn("og95years-fact-012", ids)
        self.assertNotIn("og95years-fact-001", ids)

    def test_generic_wis_rating_not_marked_us(self):
        rows = filter_records(
            self.datasets, platform="9-5-9600", year=2008, market="US"
        )
        self.assertNotIn("og95years-fact-023", {r["id"] for r in rows})

    def test_2006_turbo_marketing_label_not_assumed_b235r(self):
        rows = filter_records(
            self.datasets, platform="9-5-9600", year=2006, engine="B235R"
        )
        self.assertNotIn("og95years-fact-001", {r["id"] for r in rows})

    def test_body_repair_cannot_expand_to_unknown_year(self):
        rows = filter_records(
            self.datasets, platform="9-5-9600", year=2008
        )
        self.assertNotIn("og95structure-fact-003", {r["id"] for r in rows})
        rows_2006 = filter_records(
            self.datasets, platform="9-5-9600", year=2006
        )
        self.assertIn("og95structure-fact-003", {r["id"] for r in rows_2006})


if __name__ == "__main__":
    unittest.main()
