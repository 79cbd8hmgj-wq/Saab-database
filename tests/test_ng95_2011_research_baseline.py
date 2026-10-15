"""Regression checks for the independent MY2011 new-generation Saab 9-5 baseline."""

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/engineering-dossiers/ng95-2011-purchase-reliability-20261015.json"
REPORT = ROOT / "docs/research/ng95-2011-purchase-reliability-baseline-20261015.md"


class NG95BaselineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(DATA.read_text(encoding="utf-8"))

    def test_source_ids_are_unique_and_all_links_resolve(self):
        sources = self.data["source_records"]
        ids = [record["id"] for record in sources]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertGreaterEqual(len(ids), 15)
        self.assertTrue(all(record["url"].startswith("https://") for record in sources))
        known = set(ids)
        for fact in self.data["facts"]:
            self.assertTrue(fact["evidence_source_ids"])
            self.assertTrue(set(fact["evidence_source_ids"]) <= known)
        for case in self.data["investigation_cases"]:
            self.assertTrue(case["evidence_source_ids"])
            self.assertTrue(set(case["evidence_source_ids"]) <= known)
        for observation in self.data["supplier_observations"]:
            self.assertIn(observation["source_id"], known)

    def test_scope_does_not_merge_original_9_5_or_v6_xwd(self):
        d = self.data
        self.assertEqual(d["platform"], "650")
        self.assertEqual(d["wis_platform"], "9650")
        self.assertEqual(d["target_scope"]["model_years"], [2011])
        self.assertEqual(d["target_scope"]["drive"], "FWD")
        self.assertIn("A20NFT", d["target_scope"]["engine"])
        self.assertIn("AF40", d["target_scope"]["transmission"])
        self.assertTrue(any("V6" in x and "XWD" in x for x in d["other_2011_us_variants_not_covered_by_turbo4_diagnostics"]))

    def test_no_unsourced_reliability_or_part_approval(self):
        d = self.data
        self.assertIsNone(d["known_failure_rates"])
        self.assertEqual(d["confirmed_candidate_inspections"], 0)
        self.assertEqual(d["confirmed_vin_approved_replacements"], 0)
        self.assertEqual(d["verified_all_in_repair_quotes"], 0)
        self.assertTrue(all(not item["incidence_established"] for item in d["investigation_cases"]))
        self.assertTrue(all(not item["vin_fitment_approved"] and not item["live_delivery_confirmed"]
                            for item in d["supplier_observations"]))

    def test_advisory_and_cooling_conflict_both_preserved(self):
        facts = {fact["id"]: fact for fact in self.data["facts"]}
        self.assertIn("ng95-2011-coldvalve", facts)
        self.assertIn("ng95-2011-conflict-pump", facts)
        self.assertTrue(REPORT.is_file())
        prose = REPORT.read_text(encoding="utf-8")
        self.assertIn("GNE/FWD", prose)
        self.assertIn("55563529", prose)
        self.assertIn("70–80°C", prose)


if __name__ == "__main__":
    unittest.main()
