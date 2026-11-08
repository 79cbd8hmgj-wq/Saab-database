"""Distinct genuine-page structures found in the 2008 9-5 cooling-system pilot (one test group each)."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import wis_candidates as c

FIX = Path(__file__).resolve().parent / 'fixtures'
BASE = 'https://saabwisonline.com/9-5-9600/2008/2-engine/cooling-system/'


def load(name, doc):
    return c.extract_candidates((FIX / name).read_text(encoding='utf-8'), BASE + doc)


class TemperatureLimits(unittest.TestCase):
    def setUp(self):
        self.r = load('wis_real_unit_value_excerpt.html', 'technical-data/temperature-pressure-limits')
        self.by = {x['subject']: x for x in self.r['candidates']}

    def test_dual_unit_cell_keeps_primary_unit_and_alternate_without_converting(self):
        x = self.by['Thermostat, opening temperature']
        self.assertEqual((x['raw_value'], x['unit'], x['alternate_display_value']), ('89 ± 2', '°C', '192 ± 4 °F'))
        self.assertEqual((x['source_value_text'], x['source_unit_text']), ('89 ± 2 (192 ± 4)', '°C (°F)'))
        self.assertEqual(x['info_class'], 'A')

    def test_range_kept_verbatim(self):
        x = self.by['Expansion tank pressure valve, opening pressure']
        self.assertEqual((x['raw_value'], x['unit'], x['alternate_display_value'] if 'alternate_display_value' in x else None), ('140 - 150', 'kPa', None))

    def test_compound_two_measure_cell_not_interpreted(self):
        self.assertNotIn('System boiling point', self.by)
        rr = next(x for x in self.r['review_required'] if x['raw_cells'][0] == 'System boiling point')
        self.assertEqual(rr['reason'], 'multi_measure_cell')
        self.assertIn('131 (268) 1.4', rr['raw_cells'])

    def test_group_header_and_multiline_pairing_flagged_as_interpretation(self):
        x = self.by['Radiator fan, coolant temperature / turn-on, high speed']
        self.assertEqual((x['raw_value'], x['group_context'], x['info_class']), ('113 ± 2', '4 cyl.', 'B'))
        self.assertIn('paired_by_multiline_alignment', x['warnings'])
        self.assertIn('group_context_inferred_from_preceding_header_row', x['warnings'])
        self.assertIn('4-cyl', x['configuration_tokens'])
        self.assertTrue(x['locator'].endswith('/ line 2'))

    def test_blank_label_continuation_row_uses_previous_label_with_warning(self):
        x = self.by['Radiator fan, coolant temperature / turn-off, low speed']
        self.assertEqual(x['raw_value'], '96 ± 1')
        self.assertIn('label_continued_from_previous_row', x['warnings'])

    def test_rows_before_group_header_get_no_group(self):
        self.assertNotIn('group_context', self.by['Thermostat, opening temperature'])
        self.assertEqual(len(self.r['candidates']), 6)   # thermostat, expansion valve, 4 fan lines


class FanMotor(unittest.TestCase):
    def setUp(self):
        self.r = load('wis_real_fan_motor_excerpt.html', 'technical-data/radiator-fan-motor')

    def test_identical_rows_under_different_group_headers_are_distinct_candidates(self):
        power = [x for x in self.r['candidates'] if x['subject'] == 'Power supply']
        self.assertEqual(sorted(x['group_context'] for x in power),
                         ['Radiator fan motor, left-hand (37LH)', 'Radiator fan motor, right-hand (37RH)'])
        self.assertEqual(len({x['candidate_id'] for x in power}), 2)

    def test_condition_text_is_preserved_separately_from_subject(self):
        x = next(x for x in self.r['candidates'] if x['subject'].startswith('Resistance'))
        self.assertEqual(x['subject'], 'Resistance, low speed resistor (367)')
        self.assertEqual(x['explicit_conditions'], ['For cars with one radiator fan'])
        self.assertEqual((x['raw_value'], x['unit']), ('0.33 ± 10 %', 'Ohm'))

    def test_same_subject_different_conditions_is_not_an_internal_conflict(self):
        self.assertEqual(self.r['internal_conflicts'], [])


class TextValue(unittest.TestCase):
    def test_text_specification_preserved_as_review_not_numeric_candidate(self):
        r = load('wis_real_coolant_excerpt.html', 'technical-data/coolant')
        self.assertEqual([x['subject'] for x in r['candidates']], ['Volume, 4-cyl.'])
        self.assertEqual(r['candidates'][0]['unit'], 'L')
        rr = r['review_required'][0]
        self.assertEqual((rr['reason'], rr['info_class']), ('text_value_no_unit', 'A'))
        self.assertIn('Saab Original Coolant (50% water)', rr['raw_cells'])


class OtherStructures(unittest.TestCase):
    def setUp(self):
        self.r = load('wis_real_other_structures_excerpt.html', 'fault-diagnosis-diagnostic-trouble-codes/diagnostic-trouble-code-table')

    def test_each_structure_is_classified_not_called_unsupported(self):
        tc = self.r['table_classes']
        for kind in ('dtc_table', 'applicability_matrix', 'procedure_step', 'note_box', 'bullet_item'):
            self.assertEqual(tc.get(kind), 1, kind)
        self.assertEqual(tc.get('banner'), 1)

    def test_dtc_rows_recorded_verbatim_without_inference(self):
        d = self.r['diagnostic_records']
        self.assertEqual([(x['code'], x['description_verbatim']) for x in d], [('B1100', 'Radiator fan low speed function faulty.')])
        self.assertEqual(d[0]['promotion'], 'review_only')

    def test_unrecognised_text_table_is_reported_unsupported_and_yields_nothing(self):
        self.assertEqual(self.r['candidates'], [])
        self.assertEqual([t['reason'] for t in self.r['unsupported_tables']], ['no_recognized_specification_columns'])


if __name__ == '__main__':
    unittest.main()
