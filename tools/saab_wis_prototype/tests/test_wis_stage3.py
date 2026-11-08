"""Stage 3 regression coverage for WIS-style torque tables and safe review."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from wis_candidates import extract_candidates

URL = 'https://saabwisonline.com/9-5-9600/2008/2-engine/cooling-system/technical-data/tightening-torques'

# Reconstructed HTML representing the *table shape* shown in publicly rendered WIS.
# Not an actual HTML download; values below are fixture inputs.
HTML = '''<h1>Tightening torques</h1><table>
<tr><th></th><th>Torque (Nm)</th><th>Torque (lbf ft)</th></tr>
<tr><td>Thermostat housing, 4-cyl.</td><td>22</td><td>16.2</td></tr>
<tr><td>Heat shield (up to and including engine no. 7011078)</td><td></td><td>14.7</td></tr>
<tr><td>Heat shield (from and including engine no. 7011079)</td><td>21</td><td>15.4</td></tr>
<tr><td>Cylinder head, multi-stage</td><td>40 60 Tighten a further 90°</td><td>30 44 90°</td></tr>
</table>'''

class Stage3Tests(unittest.TestCase):
    def test_column_header_units_generate_review_candidate(self):
        result = extract_candidates(HTML, URL)
        rec = next(x for x in result['candidates'] if x['subject'] == 'Thermostat housing, 4-cyl.')
        self.assertEqual(rec['raw_value'], '22')
        self.assertEqual(rec['unit'], 'Nm')
        self.assertEqual(rec['alternate_display_value'], '16.2 lbf ft')
        self.assertEqual(rec['locator'], 'Tightening torques / table 1 / row 2')
        self.assertEqual(rec['promotion'], 'review_only')

    def test_partial_or_multistage_rows_not_automatically_interpreted(self):
        result = extract_candidates(HTML, URL)
        subjects = [x['subject'] for x in result['candidates']]
        self.assertNotIn('Heat shield (up to and including engine no. 7011078)', subjects)
        self.assertNotIn('Cylinder head, multi-stage', subjects)
        self.assertGreaterEqual(result['skipped_rows'], 2)

    def test_revision_restriction_kept_without_expanding_application(self):
        result = extract_candidates(HTML, URL)
        rec = next(x for x in result['candidates'] if x['subject'].startswith('Heat shield (from'))
        self.assertIn('7011079', rec['subject'])
        self.assertIn('engine no. 7011079', rec['applicability_note'])
        self.assertEqual(rec['review_status'], 'needs_vehicle_verification')

    def test_conflicting_units_table_is_not_promoted(self):
        html = '<h1>Tightening torques</h1><table><tr><th>Item</th><th>Torque (Nm)</th><th>Torque (lbf ft)</th></tr><tr><td>Pump</td><td>22</td><td>999</td></tr></table>'
        result = extract_candidates(html, URL)
        self.assertEqual(result['candidates'], [])

    def test_three_column_other_table_does_not_create_candidates(self):
        html = '<h1>Electrical</h1><table><tr><th>Item</th><th>Resistance (ohm)</th><th>Condition</th></tr><tr><td>Sensor</td><td>100</td><td>Cold</td></tr></table>'
        result = extract_candidates(html, URL)
        self.assertEqual(result['candidates'], [])

if __name__ == '__main__': unittest.main()
