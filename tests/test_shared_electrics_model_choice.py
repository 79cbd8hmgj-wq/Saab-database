"""Prevent arbitrary reliability or OE donor fitment inference from parts catalogue matches."""
import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class SharedElectricitySafety(unittest.TestCase):
 def test_parts_remain_unapproved(self):
  d=json.loads((ROOT/'data/datasets/cross-manufacturer-electrics-model-choice.json').read_text())
  self.assertEqual(len(d['parts']),3)
  for p in d['parts']:
   self.assertEqual(p['review_status'],'needs_vehicle_verification')
   self.assertEqual(p['evidence_status'],'supplier_claim')
   for field in ('fitment_approved','vehicle_verified','durability_validated'):
    self.assertFalse(p['interchange_candidate'][field])
 def test_distinct_electrical_families(self):
  d=json.loads((ROOT/'data/datasets/cross-manufacturer-electrics-model-choice.json').read_text())
  ps={p['part_number']:p for p in d['parts']}
  self.assertEqual(ps['A0047']['applicability']['platforms'],['9-3-9440'])
  self.assertEqual(ps['A0319']['applicability']['platforms'],['9-5-9600'])
 def test_no_claim_to_rank_models(self):
  m=json.loads((ROOT/'data/model-selection/interchange-evidence-20261013.json').read_text())
  self.assertEqual(m['decision'],'insufficient_evidence_to_rank')
  self.assertTrue(all(p['unresolved'] for p in m['profiles']))
