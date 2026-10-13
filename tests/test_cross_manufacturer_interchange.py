"""Guard non-Saab interchange candidates against accidental 'approved fit' promotion."""
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'/'datasets'/'cross-manufacturer-interchange-pilot.json'

class InterchangeResearchGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.records=json.loads(DATA.read_text(encoding='utf-8'))

    def test_supplier_leads_are_not_approved_replacements(self):
        self.assertGreaterEqual(len(self.records['parts']),3)
        allowed={'shared_platform_aftermarket_sku','cross_catalogue_aftermarket_reference','shared_oe_reference_aftermarket_sku'}
        for p in self.records['parts']:
            with self.subTest(part=p['part_number']):
                c=p['interchange_candidate']
                self.assertIn(c['strategy'],allowed)
                self.assertEqual(p['evidence_status'],'supplier_claim')
                self.assertEqual(p['review_status'],'needs_vehicle_verification')
                self.assertFalse(c['fitment_approved'])
                self.assertFalse(c['vehicle_verified'])
                self.assertFalse(c['durability_validated'])
                self.assertTrue(c['verification_required'])
                self.assertTrue(c['saab_reference_numbers'])
                self.assertTrue(p['source_ids'])
                self.assertTrue(all(x['type']=='aftermarket_reference' for x in p['relationships']))

    def test_excluded_2008_95_pcv_is_not_promoted(self):
        older=next(f for f in self.records['facts'] if f['predicate']=='retailer_older_model_pcv_kit_application')
        self.assertNotIn(2008,older['applicability']['model_years'])
        self.assertIn('1998',older['value']['listed_9_5_years'])

    def test_brake_option_and_hub_stay_unverified(self):
        for p in self.records['parts']:
            self.assertEqual(p['applicability']['platforms'],['9-3-9440'])
            self.assertEqual(p['applicability']['model_years'],[2005,2006])
        g=' '.join(' '.join(x['missing_inputs']) for x in self.records['gaps'])
        self.assertIn('ABS',g)
        self.assertIn('brake',g.lower())
