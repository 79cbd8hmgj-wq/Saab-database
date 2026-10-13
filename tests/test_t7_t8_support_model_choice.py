"""T7 cassette and T8 ECM are different repairs; keep service conditions visible."""
import json
import unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
D=json.loads((R/'data/datasets/t7-t8-repair-support-model-choice.json').read_text(encoding='utf-8'))
M=json.loads((R/'data/model-selection/interchange-evidence-20261013.json').read_text(encoding='utf-8'))
class T7T8SupportTests(unittest.TestCase):
 def test_dont_duplicate_existing_cassette_part(self):
  self.assertEqual(len(D['parts']),0)
  self.assertEqual(len(D['sources']),6)
 def test_vendor_cloning_condition_is_not_guarantee(self):
  f={x['predicate']:x for x in D['facts']}
  self.assertEqual(f['specialist_clone_requires_original_communication']['value'],True)
  self.assertEqual(f['specialist_clone_requires_original_communication']['evidence_status'],'supplier_claim')
  self.assertEqual(f['factory_service_requires_extended_diagnosis']['evidence_status'],'documented')
 def test_model_remains_open(self):
  self.assertEqual(M['model_recommendation'],'not_yet_rankable')
  self.assertTrue(all('repair_support' in p for p in M['candidates']))
