"""Model comparison must not elevate shared catalogue leads into approved donor parts."""
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
D=json.loads((ROOT/'data/datasets/cross-manufacturer-electrics-model-choice.json').read_text(encoding='utf-8'))
M=json.loads((ROOT/'data/model-selection/interchange-evidence-20261013.json').read_text(encoding='utf-8'))
class ModelPartsComparisonTests(unittest.TestCase):
    def test_unverified_candidates(self):
        self.assertEqual(len(D['parts']),3)
        for p in D['parts']:
            self.assertEqual(p['evidence_status'],'supplier_claim')
            self.assertEqual(p['review_status'],'needs_vehicle_verification')
            for flag in ('fitment_approved','vehicle_verified','durability_validated'):
                self.assertFalse(p['interchange_candidate'][flag])
    def test_different_9_3_9_5_alternators(self):
        parts={p['part_number']:p for p in D['parts']}
        self.assertEqual(parts['A0047']['applicability']['platforms'],['9-3-9440'])
        self.assertEqual(parts['A0319']['applicability']['platforms'],['9-5-9600'])
        f={(x['subject'],x['predicate']):x['value'] for x in D['facts']}
        self.assertEqual(f[('charging_start:A0047','pulley_grooves')],5)
        self.assertEqual(f[('charging_start:A0319','pulley_grooves')],6)
    def test_no_model_rank_from_catalogue_counts(self):
        self.assertEqual(M['model_recommendation'],'not_yet_rankable')
        self.assertEqual(len(M['candidates']),2)
        self.assertTrue(all(x['unresolved'] for x in M['candidates']))
