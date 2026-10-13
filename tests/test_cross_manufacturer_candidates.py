"""Cross-manufacturer evidence gates; a catalogue cross-reference is not fitted-car approval."""

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "data" / "interchange-candidates" / "phase0.json"
DATASETS = ROOT / "data" / "datasets"

class CrossManufacturerCandidateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.matrix = json.loads(MATRIX.read_text(encoding="utf-8"))
        cls.sources = set()
        cls.parts = set()
        for path in sorted(DATASETS.glob("*.json")):
            dataset = json.loads(path.read_text(encoding="utf-8"))
            cls.sources.update(s["id"] for s in dataset["sources"])
            cls.parts.update(p["id"] for p in dataset["parts"])

    def test_matrix_has_unique_candidates_with_referenced_sources(self):
        self.assertEqual(self.matrix["schema_version"], "1.0.0")
        candidates = self.matrix["candidates"]
        self.assertTrue(candidates)
        self.assertEqual(len(candidates), len({c["id"] for c in candidates}))
        for c in candidates:
            self.assertTrue(c["references"])
            self.assertTrue(set(c["references"]) <= self.sources)
            self.assertTrue(c["candidate"]["manufacturer"])
            self.assertTrue(c["candidate"]["sku"])

    def test_candidate_does_not_conflate_part_with_verified_donor(self):
        for c in self.matrix["candidates"]:
            self.assertIn(c["readiness"], {"catalog_candidate_unverified", "vehicle_verified", "validated_installation"})
            if c["readiness"] == "catalog_candidate_unverified":
                for field in ["approved_drop_in", "approved_oem_donor", "vehicle_tested", "cost_advantage_verified", "stock_verified", "independently_tested_reliability_improvement"]:
                    self.assertIs(c[field], False, (c["id"], field))
                self.assertIs(c["needs_vehicle_verification"], True)
                self.assertTrue(c["unknowns"])
            self.assertTrue(c["engineering_risk"])

    def test_catalog_reference_only_not_promoted_to_interchangeable(self):
        for c in self.matrix["candidates"]:
            support = c["interchange_support"]
            interchangeable = set(support["manufacturer_labeled_interchangeable"])
            reference_only = set(support["manufacturer_labeled_reference_only"])
            self.assertFalse(interchangeable & reference_only)
            self.assertTrue(support["applicability_caveat"])
            self.assertNotEqual(c["candidate"]["type"], "confirmed_original_equipment_donor")

if __name__ == "__main__":
    unittest.main()
