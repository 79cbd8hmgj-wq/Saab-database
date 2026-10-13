"""Regressions for manufacturer access vs retailer catalogue part identity."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from database import load_datasets, validate_datasets


class EPCProvenanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.datasets = load_datasets()
        cls.domain = next(d for d in cls.datasets if d["domain"] == "epc_provenance")
        cls.parts = {p["part_number"]: p for p in cls.domain["parts"]}
        cls.facts = {f["predicate"]: f for f in cls.domain["facts"]}

    def test_cross_dataset_integrity(self):
        self.assertEqual(validate_datasets(self.datasets), [])
        self.assertEqual(len(self.domain["sources"]), 10)
        self.assertEqual(len(self.domain["facts"]), 12)
        self.assertEqual(len(self.domain["parts"]), 2)
        self.assertEqual(len(self.domain["gaps"]), 5)

    def test_webepc_capability_is_not_a_retrieved_vin_record(self):
        fact = self.facts["vin_or_build_data_filtering_available"]
        self.assertEqual(fact["evidence_status"], "documented")
        self.assertTrue(fact["value"])
        self.assertEqual(fact["source_ids"], ["epcverify-src-001"])
        self.assertIn("not a successful VIN query", fact["notes"])

    def test_bushing_oe_number_not_the_complete_frame_merchant_sku(self):
        bushing = self.parts["24401110"]
        frame = self.parts["RD24401110"]
        self.assertNotEqual(bushing["part_number"], frame["part_number"])
        self.assertIn("BUSHING", bushing["relationships"][0]["conditions"])
        self.assertIn("merchant", frame["requirements"][0])
        self.assertEqual(bushing["relationships"][0]["part_number"], "13247173")
        self.assertEqual(frame["relationships"][0]["part_number"], "32022623")

    def test_neither_supplier_part_has_verified_interchange_status(self):
        for item in self.parts.values():
            self.assertEqual(item["evidence_status"], "supplier_claim")
            self.assertEqual(item["review_status"], "needs_vehicle_verification")

    def test_12762720_reference_is_not_promoted_to_oem(self):
        item = self.facts["independent_merchant_grouping"]
        self.assertEqual(item["evidence_status"], "supplier_claim")
        self.assertEqual(item["review_status"], "needs_vehicle_verification")
        self.assertIn("not official", item["notes"].replace("not official authorized", "not official"))

    def test_2005_engine_mount_factory_scope(self):
        item = self.facts["wisl_engine_pad_alignment_required"]
        self.assertEqual(item["applicability"]["engine_codes"], ["B207"])
        self.assertEqual(item["applicability"]["model_years"], [2005])
        self.assertEqual(item["evidence_status"], "documented")

    def test_research_gaps_include_original_epc_and_conflicting_identity(self):
        titles = " ".join(g["title"] for g in self.domain["gaps"]).lower()
        self.assertIn("24401110", titles)
        self.assertIn("12762720", titles)
        self.assertIn("vin", titles)


if __name__ == "__main__":
    unittest.main()
