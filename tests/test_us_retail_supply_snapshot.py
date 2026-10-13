"""Dated retail observations cannot be mistaken for real-time supply or an approved swap."""
import json,unittest
from pathlib import Path
PATH=Path(__file__).resolve().parents[1]/"data/datasets/us-retail-parts-supply-snapshot.json"
class USRetailObservations(unittest.TestCase):
 def test_source_bounds_and_no_approved_parts(self):
  data=json.loads(PATH.read_text(encoding="utf-8"))
  self.assertEqual(data["domain"],"us_retail_parts_supply_snapshot")
  self.assertEqual(data["parts"],[])
  self.assertGreaterEqual(len(data["sources"]),6)
  for fact in data["facts"]:
   self.assertEqual(fact["evidence_status"],"supplier_claim")
   self.assertEqual(fact["review_status"],"needs_vehicle_verification")
  self.assertTrue(all(s["accessed_at"]=="2026-10-13" for s in data["sources"]))
 def test_price_and_unavailable_are_separate(self):
  d=json.loads(PATH.read_text(encoding="utf-8"))
  f={(x["subject"],x["predicate"]):x["value"] for x in d["facts"]}
  self.assertEqual(f[("retail:eSaabParts:32020290","quoted_price")],91.74)
  self.assertEqual(f[("retail:eSaabParts:32020290","quoted_stock_text")],"Currently Unavailable")
  self.assertEqual(f[("retail:eSaabParts:32101497","quoted_price")],194.99)
 def test_not_a_same_system_model_price_comparison(self):
  d=json.loads(PATH.read_text(encoding="utf-8"))
  g=" ".join(x["reason"] for x in d["gaps"])
  self.assertIn("different",g.lower())
  self.assertIn("VIN",g)
