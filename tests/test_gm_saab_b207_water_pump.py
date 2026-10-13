"""Protect sourced GM/Saab water-pump SKU identity from unsupported fitted-VIN claims."""
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT / "data" / "datasets" / "cross-manufacturer-gm-saab-b207-water-pump.json"
MATRIX=ROOT / "data" / "interchange-candidates" / "phase0.json"
class GenuineGMSaabWaterPumpTests(unittest.TestCase):
    def test_dual_official_part_number_is_not_a_donor_approval(self):
        d=json.loads(DATA.read_text(encoding="utf-8"))
        assert len(d["sources"])>=3
        p=d["parts"][0]
        self.assertEqual(p["part_number"],"12630084")
        self.assertEqual(p["evidence_status"],"documented")
        self.assertEqual(p["review_status"],"needs_vehicle_verification")
        self.assertFalse(p["interchange_candidate"]["fitment_approved"])
        self.assertFalse(p["interchange_candidate"]["vehicle_verified"])
        self.assertFalse(p["interchange_candidate"]["durability_validated"])
        self.assertEqual(p["applicability"]["platforms"],["9-3-9440"])
        self.assertNotIn("9-5-9600",p["applicability"]["platforms"])
    def test_candidate_matrix_retains_identity_without_promoting_approval(self):
        m=json.loads(MATRIX.read_text(encoding="utf-8"))
        c=next((c for c in m["candidates"] if c["id"]=="xmake-002"),None)
        self.assertIsNotNone(c)
        self.assertEqual(c["candidate"]["sku"],"12630084")
        self.assertEqual(c["readiness"],"catalog_candidate_unverified")
        for k in ["approved_drop_in","approved_oem_donor","vehicle_tested","cost_advantage_verified","stock_verified","independently_tested_reliability_improvement"]:
            self.assertFalse(c[k])
        self.assertEqual(c["interchange_support"]["manufacturer_labeled_interchangeable"],[])
    def test_gm_copy_conflict_is_recorded(self):
        d=json.loads(DATA.read_text(encoding="utf-8"))
        self.assertEqual(len(d["issues"]),1)
        self.assertIn("belt",d["issues"][0]["title"].lower())
        self.assertTrue(any("2008" in gap.get("reason","") or "B207" in gap["title"] or "B207" in gap["reason"] for gap in d["gaps"]))

if __name__=="__main__":
    unittest.main()
