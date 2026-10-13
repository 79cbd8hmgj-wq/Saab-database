"""Check that 9-5 part-sourcing correction does not approve donor conversions."""
import json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class OG95SharedElectrics(unittest.TestCase):
 def test_candidates_unapproved(self):
  d=json.loads((ROOT/'data/datasets/og95-shared-electrics-countercheck.json').read_text())
  self.assertEqual(len(d['parts']),2)
  for p in d['parts']:
   self.assertEqual(p['applicability']['platforms'],['9-5-9600'])
   self.assertEqual(p['evidence_status'],'supplier_claim')
   for field in ('fitment_approved','vehicle_verified','durability_validated'):
    self.assertFalse(p['interchange_candidate'][field])
 def test_alternator_not_a0319(self):
  d=json.loads((ROOT/'data/datasets/og95-shared-electrics-countercheck.json').read_text())
  self.assertTrue(any('A0319' in x['title'] for x in d['issues']))
  self.assertTrue(any(x['part_number']=='A0219' for x in d['parts']))
