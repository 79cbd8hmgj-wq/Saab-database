"""Reconciliation against the REAL dataset fact shape (entity subjects, object values, null units)."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from wis_reconcile import reconcile

URL = 'https://saabwisonline.com/9-5-9600/2008/2-engine/cooling-system/technical-data/temperature-pressure-limits'
SRC = {URL: [{'id': 's1', 'url': URL}]}


def cand(label='Thermostat, opening temperature', value='89', unit='°C', restr=None):
    return {'candidate_id': 'c', 'source_url': URL, 'subject': label, 'raw_value': value, 'unit': unit,
            'applicability_restrictions': restr or {'engine_number': [], 'chassis_number': []}}


def fact(fid, locator, value, unit, sources=('s1',), subject='thermostat:9-5-petrol4'):
    return {'id': fid, 'subject': subject, 'predicate': 'p', 'value': value, 'unit': unit, 'locator': locator,
            'source_ids': list(sources), 'applicability': {}}


class RealShape(unittest.TestCase):
    def test_object_value_with_matching_nominal_is_possible_duplicate_not_equivalence(self):
        r = reconcile({'candidates': [cand()]}, SRC, [fact('f1', 'Thermostat, opening temperature', {'nominal': 89, 'tolerance': 2}, '°C')])
        rec = r['results'][0]
        self.assertEqual(rec['possible_fact_matches'], ['f1'])
        self.assertEqual(rec['decision'], 'manual_review')
        self.assertEqual(rec['match_details'][0]['label_match'], 'exact')

    def test_object_value_without_match_is_potential_conflict(self):
        r = reconcile({'candidates': [cand(value='95')]}, SRC, [fact('f1', 'Thermostat, opening temperature', {'nominal': 89, 'tolerance': 2}, '°C')])
        self.assertEqual(r['results'][0]['potential_conflicts'], ['f1'])

    def test_null_unit_fact_is_flagged_not_silently_equated(self):
        r = reconcile({'candidates': [cand()]}, SRC, [fact('f1', 'Thermostat, opening temperature', {'nominal_C': 89}, None)])
        d = r['results'][0]['match_details'][0]
        self.assertEqual(d['unit_status'], 'fact_unit_unstated')
        self.assertIn('existing_fact_unit_not_stated_as_unit_field', d['caveats'])

    def test_different_stated_unit_not_compared(self):
        r = reconcile({'candidates': [cand()]}, SRC, [fact('f1', 'Thermostat, opening temperature', 89, '°F')])
        self.assertEqual(r['results'][0]['possible_fact_matches'], [])
        self.assertEqual(r['results'][0]['potential_conflicts'], [])

    def test_unrelated_label_same_number_not_matched(self):
        r = reconcile({'candidates': [cand()]}, SRC, [fact('f1', 'Washer fluid pump', 89, '°C', subject='pump:x')])
        self.assertEqual(r['results'][0]['possible_fact_matches'], [])

    def test_other_source_same_label_is_overlap_only(self):
        r = reconcile({'candidates': [cand()]}, SRC, [fact('f9', 'Thermostat, opening temperature', 70, '°C', sources=('other',))])
        rec = r['results'][0]
        self.assertEqual(rec['cross_source_label_overlaps'], ['f9'])
        self.assertEqual((rec['possible_fact_matches'], rec['potential_conflicts']), ([], []))

    def test_engine_boundary_caveat_attached(self):
        c = cand(restr={'engine_number': [{'relation': 'from_and_including', 'boundary': '7011079', 'source_text': 'x'}], 'chassis_number': []})
        r = reconcile({'candidates': [c]}, SRC, [fact('f1', 'Thermostat, opening temperature', 89, '°C')])
        self.assertTrue(any('engine_or_chassis_boundary' in x for x in r['results'][0]['match_details'][0]['caveats']))

    def test_exact_vs_normalised_url_reported(self):
        r = reconcile({'candidates': [cand()]}, {URL: [{'id': 's1', 'url': URL + '/'}]}, [])
        self.assertEqual(r['results'][0]['source_match'], 'normalized_url')
        r = reconcile({'candidates': [cand()]}, SRC, [])
        self.assertEqual(r['results'][0]['source_match'], 'exact_url')

    def test_printed_tolerance_and_range_values_compare_against_object_facts(self):
        facts = [fact('f1', 'Thermostat, opening temperature', {'nominal': 89, 'tolerance': 2}, '°C'),
                 fact('f2', 'Expansion tank pressure valve, opening pressure', {'min': 140, 'max': 150}, 'kPa', subject='tank:x')]
        r = reconcile({'candidates': [cand(value='89 ± 2'), cand('Expansion tank pressure valve, opening pressure', '140 - 150', 'kPa')]}, SRC, facts)
        self.assertEqual([x['possible_fact_matches'] for x in r['results']], [['f1'], ['f2']])
        r = reconcile({'candidates': [cand(value='91 ± 2')]}, SRC, facts[:1])
        self.assertEqual(r['results'][0]['potential_conflicts'], ['f1'])


if __name__ == '__main__':
    unittest.main()
