"""Regression tests built on trimmed structure excerpts of GENUINE SaabWISOnline pages."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import wis_candidates as c
import wis_indexer as w

FIX = Path(__file__).resolve().parent / 'fixtures'
TORQUE_URL = 'https://saabwisonline.com/9-5-9600/2008/2-engine/cooling-system/technical-data/tightening-torques'
LIST_URL = 'https://saabwisonline.com/9-5-9600/2008/2-engine/cooling-system/technical-data/'


def torque_result():
    return c.extract_candidates((FIX / 'wis_real_tightening_torques_excerpt.html').read_text(encoding='utf-8'), TORQUE_URL)


class RealTorqueTable(unittest.TestCase):
    def test_colspan_label_rows_and_four_cell_restricted_rows_all_extracted(self):
        subjects = [x['subject'] for x in torque_result()['candidates']]
        self.assertEqual(len(subjects), 5)
        self.assertIn('Radiator fan', subjects)

    def test_both_engine_number_revisions_are_kept_separately(self):
        res = {x['subject']: x for x in torque_result()['candidates']}
        early = next(v for k, v in res.items() if 'up to and including' in k)
        late = next(v for k, v in res.items() if 'from and including' in k)
        self.assertEqual((early['raw_value'], early['alternate_display_value']), ('20', '14.7 lbf ft'))
        self.assertEqual((late['raw_value'], late['alternate_display_value']), ('21', '15.4 lbf ft'))
        self.assertEqual(early['applicability_restrictions']['engine_number'],
                         [{'relation': 'up_to_and_including', 'boundary': '7011078', 'source_text': 'up to and including engine no. 7011078'}])
        self.assertEqual(late['applicability_restrictions']['engine_number'][0]['relation'], 'from_and_including')
        self.assertNotEqual(early['candidate_id'], late['candidate_id'])

    def test_units_not_converted_and_original_text_preserved(self):
        rec = next(x for x in torque_result()['candidates'] if x['subject'] == 'Coolant pump, 4-cyl.')
        self.assertEqual((rec['raw_value'], rec['unit']), ('22', 'Nm'))
        self.assertEqual(rec['alternate_display_value'], '16.2 lbf ft')
        self.assertEqual(rec['configuration_tokens'], ['4-cyl'])
        self.assertEqual(rec['info_class'], 'A')

    def test_locator_counts_the_real_page_banner_table_first(self):
        # Genuine pages open with a 1-row title-banner table, so the data table is table 2.
        rec = next(x for x in torque_result()['candidates'] if x['subject'] == 'Radiator fan')
        self.assertEqual(rec['locator'], 'Tightening torques / table 2 / row 2')
        self.assertEqual(torque_result()['tables_examined'], 2)

    def test_restricted_candidates_are_class_c_needing_verification(self):
        rec = next(x for x in torque_result()['candidates'] if 'up to and including' in x['subject'])
        self.assertEqual(rec['info_class'], 'C')
        self.assertEqual(rec['review_status'], 'needs_vehicle_verification')
        self.assertEqual(rec['promotion'], 'review_only')

    def test_chrome_ad_script_text_never_becomes_content(self):
        r = torque_result()
        self.assertNotIn('adsbygoogle', str(r))

    def test_unrestricted_row_is_not_claimed_for_all_engines(self):
        rec = next(x for x in torque_result()['candidates'] if x['subject'] == 'Radiator fan')
        self.assertEqual(rec['applicability_restrictions']['engine_number'], [])
        self.assertIn('Year path is not verified vehicle applicability', rec['warnings'])


class SpanAndShapeHandling(unittest.TestCase):
    HDR = '<tr><td colspan="2"></td><td>Torque (Nm)</td><td>Torque (lbf ft)</td></tr>'

    def run_table(self, body):
        return c.extract_candidates('<h1>T</h1><table>' + self.HDR + body + '</table>', TORQUE_URL)

    def test_rowspan_label_is_not_duplicated_into_value_columns(self):
        r = self.run_table('<tr><td rowspan="2" colspan="2">Pump</td><td>22</td><td>16.2</td></tr><tr><td>10</td><td>7.4</td></tr>')
        self.assertEqual([x['subject'] for x in r['candidates']], ['Pump', 'Pump'])
        self.assertEqual([x['raw_value'] for x in r['candidates']], ['22', '10'])
        self.assertTrue(all('inherited_label_from_rowspan' in x['warnings'] or x['locator'].endswith('row 2') for x in r['candidates']))
        self.assertIn('inherited_label_from_rowspan', r['candidates'][1]['warnings'])

    def test_extra_trailing_column_makes_row_review_required(self):
        r = self.run_table('<tr><td colspan="2">Pump</td><td>22</td><td>16.2</td><td>see note</td></tr>')
        self.assertEqual(r['candidates'], [])
        self.assertEqual(r['review_required'][0]['reason'], 'unexpected_extra_columns')

    def test_missing_value_cell_is_review_required_not_dropped_silently(self):
        r = self.run_table('<tr><td colspan="2">Pump</td><td></td><td>16.2</td></tr>')
        self.assertEqual(r['candidates'], [])
        self.assertEqual(r['review_required'][0]['reason'], 'missing_or_non_numeric_value')
        self.assertEqual(r['review_required'][0]['raw_cells'][-1], '16.2')

    def test_multistage_angle_procedure_preserved_verbatim_not_reduced(self):
        r = self.run_table('<tr><td colspan="2">Head bolt</td><td>40 60 Tighten a further 90°</td><td>30 44 90°</td></tr>')
        self.assertEqual(r['candidates'], [])
        rr = r['review_required'][0]
        self.assertEqual(rr['reason'], 'multistage_or_angle_procedure')
        self.assertEqual(rr['info_class'], 'B')
        self.assertIn('40 60 Tighten a further 90°', rr['raw_cells'])

    def test_chassis_restriction_preserved_not_expanded_to_vin(self):
        r = self.run_table('<tr><td colspan="2">Bracket (from chassis no. 1234567)</td><td>8</td><td>5.9</td></tr>')
        rec = r['candidates'][0]
        self.assertEqual(rec['applicability_restrictions']['chassis_number'][0]['boundary'], '1234567')
        self.assertNotIn('vin', str(rec['applicability_restrictions']).lower().replace('chassis', ''))

    def test_comma_decimal_and_inconsistent_unit_pair(self):
        ok = self.run_table('<tr><td colspan="2">A</td><td>8</td><td>5,9</td></tr>')
        self.assertEqual(len(ok['candidates']), 1)
        bad = self.run_table('<tr><td colspan="2">B</td><td>8</td><td>9.9</td></tr>')
        self.assertEqual(bad['candidates'], [])
        self.assertEqual(bad['review_required'][0]['reason'], 'nm_lbfft_inconsistent')

    def test_malformed_unclosed_table_does_not_crash_or_invent(self):
        r = c.extract_candidates('<h1>T</h1><table><tr><td>Pump<td>22', TORQUE_URL)
        self.assertEqual(r['candidates'], [])

    def test_nested_table_does_not_corrupt_outer(self):
        html = '<h1>T</h1><table>' + self.HDR + '<tr><td colspan="2">Pump <table><tr><td>x</td></tr></table></td><td>22</td><td>16.2</td></tr></table>'
        r = c.extract_candidates(html, TORQUE_URL)
        self.assertEqual(r['candidates'][0]['raw_value'], '22')


class ListingPage(unittest.TestCase):
    def setUp(self):
        self.html = (FIX / 'wis_real_listing_excerpt.html').read_text(encoding='utf-8')

    def test_children_have_kind_and_breadcrumbs_excluded(self):
        d = w.parse_page(self.html, LIST_URL, '/9-5-9600/2008/')
        kinds = {x['url']: x['kind'] for x in d['child_links']}
        self.assertEqual(kinds, {
            LIST_URL + 'coolant': 'document',
            LIST_URL + 'tightening-torques': 'document',
            LIST_URL + 'sub-folder': 'folder'})

    def test_site_chrome_images_not_counted(self):
        d = w.parse_page(self.html, LIST_URL, '/9-5-9600/2008/')
        self.assertEqual(d['image_count'], 0)

    def test_listing_page_produces_no_candidates(self):
        self.assertEqual(c.extract_candidates(self.html, LIST_URL)['candidates'], [])


if __name__ == '__main__':
    unittest.main()
