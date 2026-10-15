"""Evidence safeguards for the MY2011 US Turbo4 component expansion."""
import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('ng95_check', ROOT / 'tools/check_ng95_components.py')
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class NG95ComponentEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(checker.DATA.read_text(encoding='utf-8'))
        cls.parts = {c['catalogue_service_part_number']: c for c in cls.data['component_inventory']}

    def test_valid_scoped_register_and_reproducible_report(self):
        self.assertEqual(checker.validate(self.data), [])
        self.assertEqual(checker.render(self.data), checker.REPORT.read_text(encoding='utf-8'))

    def test_bad_source_and_misrouted_component_are_rejected(self):
        d = copy.deepcopy(self.data)
        d['component_inventory'][0]['evidence_source_ids'] = ['invented-source']
        d['inventory_systems'][0]['component_ids'].pop()
        errors = checker.validate(d)
        self.assertTrue(any('unknown source' in e for e in errors))
        self.assertTrue(any('assigned exactly once' in e for e in errors))

    def test_no_unproved_factory_identity_approval_or_life_claim(self):
        for p in self.data['component_inventory']:
            self.assertIsNone(p['factory_installed_part_number'])
            self.assertIsNone(p['official_supersession_history'])
            self.assertFalse(p['vin_fitment_approved'])
            self.assertFalse(p['physical_vehicle_verified'])
            self.assertIsNone(p['failure_research']['failure_frequency'])
        self.assertTrue(all(not x['durability_validated'] for x in self.data['interchange_assessments']))
        self.assertTrue(all(not x['verified_practical_durability_gain'] for x in self.data['modernization_candidates']))

    def test_supplier_candidate_cannot_be_silently_promoted(self):
        d = copy.deepcopy(self.data)
        candidate = next(x for x in d['interchange_assessments'] if x['category'] == 'C')
        candidate['category'] = 'A'
        self.assertTrue(any('A/B promotion' in e for e in checker.validate(d)))
        candidate['category'] = 'C'
        candidate['approved_drop_in'] = True
        self.assertTrue(any('cannot silently approve' in e for e in checker.validate(d)))

    def test_false_delivery_and_all_in_cost_claims_are_rejected(self):
        d = copy.deepcopy(self.data)
        d['current_supply_observations'][0]['deliverable_inventory_confirmed'] = True
        d['repair_economics'][0]['all_in_repair_cost_usd'] = 200
        errors = checker.validate(d)
        self.assertTrue(any('delivery claim' in e for e in errors))
        self.assertTrue(any('all-in cost' in e for e in errors))

    def test_bad_cost_arithmetic_rejected_and_unknowns_not_zeroed(self):
        d = copy.deepcopy(self.data)
        d['repair_economics'][0]['known_part_lines'][0]['extended_price_usd'] += 1
        self.assertTrue(any('line arithmetic' in e for e in checker.validate(d)))
        for job in self.data['repair_economics']:
            for key in ['shipping_usd', 'tax_usd', 'core_charges_usd', 'specialized_tools_usd',
                        'programming_or_calibration_usd', 'published_labor_time_hours',
                        'independent_specialist_labor_usd', 'towing_or_transportation_usd',
                        'all_in_repair_cost_usd']:
                self.assertIsNone(job[key])

    def test_generation_and_configuration_boundaries_survive(self):
        self.assertIn('AF40-6 II', self.parts['55570649']['production_applicability']['source_restrictions'])
        self.assertIn('without XWD', self.parts['55570649']['production_applicability']['source_restrictions'])
        self.assertNotIn('55570650', self.parts)
        self.assertNotIn('13322172', self.parts)
        self.assertIn('FWD', self.parts['13312096']['production_applicability']['source_restrictions'])
        self.assertIn('120 A', self.parts['13502591']['production_applicability']['source_restrictions'])
        self.assertIn('140 A', self.parts['13502590']['production_applicability']['source_restrictions'])
        self.assertIn('rear', self.parts['13219164']['description'].lower())
        self.assertEqual(self.parts['09186677']['catalogue_service_part_number'], '09186677')

    def test_original_cold_valve_and_pump_provenance_not_discarded(self):
        original = {x['id']: x for x in self.data['facts']}
        self.assertIn('ng95-2011-conflict-pump', original)
        self.assertIn('ng95-2011-coldvalve', original)
        resolved = {x['id']: x for x in self.data['source_conflict_resolutions']}
        self.assertEqual(resolved['ng95-resolution-pump']['original_fact_id'], 'ng95-2011-conflict-pump')
        self.assertEqual(self.parts['12630084']['existing_canonical_part_id'], 'gmwp-part-001')

    def test_primary_kit_does_not_masquerade_as_balance_drive(self):
        contents = {x['part_number'] for x in self.parts['12635447']['kit_contents']}
        self.assertIn('24461834', contents)
        self.assertIn('12608580', contents)
        self.assertNotIn('12635427', contents)
        self.assertNotIn('90537300', contents)
        self.assertEqual(self.data['atf_purchase_options']['job_quantity_litres'], None)

    def test_market_scope_and_missing_as_built_evidence_rejected(self):
        d = copy.deepcopy(self.data)
        d['active_research_scope']['markets'].append('EU')
        d['component_inventory'][0]['factory_installed_part_number'] = 'invented'
        errors = checker.validate(d)
        self.assertIn('target market/year widened', errors)
        self.assertTrue(any('factory-installed identity' in e for e in errors))


    def test_bosch_alternative_is_manufacturer_reference_not_original_supplier_proof(self):
        a = next(x for x in self.data['interchange_assessments'] if x['id'] == 'ng95-interchange-bosch-pump')
        self.assertEqual(a['category'], 'C')
        self.assertEqual(a['manufacturer_sku'], '66814')
        self.assertFalse(a['approved_drop_in'])
        self.assertIsNone(self.parts['12658478']['original_supplier'])
        o = next(x for x in self.data['current_supply_observations'] if x['id'] == 'ng95-supply-bosch66814')
        self.assertEqual(o['displayed_unit_price'], 288.29)
        self.assertEqual(o['seller_sku'], '12658478-14')
        self.assertEqual(o['price_basis'], 'retrieved_retail_page_no_checkout')
        self.assertFalse(o['deliverable_inventory_confirmed'])

    def test_inspection_template_preserves_unknowns_and_evidence_classes(self):
        path = ROOT / self.data['inspection_framework']['template_path']
        t = json.loads(path.read_text(encoding='utf-8'))
        self.assertEqual(t['scope'], self.data['active_research_scope'])
        self.assertEqual(t['stages'], self.data['inspection_framework']['stages'])
        self.assertEqual(t['disposition'], 'HOLD')
        self.assertIsNone(t['essential_repair_total_usd'])
        self.assertIsNone(t['private_vin_record_reference'])
        self.assertEqual(t['measured_tests'], [])
        self.assertEqual(t['seller_claims'], [])
        self.assertFalse(t['published_personal_data'])
        self.assertEqual(len(t['stages']), 10)
        self.assertTrue(all(x['result'] is None for x in t['stages']))

    def test_invented_inspection_result_is_rejected(self):
        d = copy.deepcopy(self.data)
        d['inspection_framework']['stages'][0]['result'] = 'healthy'
        self.assertTrue(any('invented inspection result' in e for e in checker.validate(d)))


if __name__ == '__main__':
    unittest.main()
