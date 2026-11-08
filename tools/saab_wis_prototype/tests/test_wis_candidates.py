import json
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import wis_candidates as c

URL = 'https://saabwisonline.com/9-5-9600/2008/2-engine/basic-engine-4-cylinder-petrol/technical-data/general-data/'
HTML = '''<html><head><title>General data</title></head><body><main><h1>General data</h1>
<h2>Technical data</h2><table><tr><th>Specification</th><th>Value</th></tr>
<tr><td>Thermostat opening temperature</td><td>89 ± 2 °C</td></tr>
<tr><td>Expansion tank pressure</td><td>140–150 kPa</td></tr>
<tr><td>Unrelated note</td><td>See diagnostic procedure</td></tr>
</table><p>Applicable chassis: verify before use.</p></main></body></html>'''

class CandidateTests(unittest.TestCase):
    def test_extracts_only_labeled_numeric_table_rows(self):
        result = c.extract_candidates(HTML, URL)
        self.assertEqual(len(result['candidates']), 2)
        self.assertEqual(result['candidates'][0]['subject'], 'Thermostat opening temperature')
        self.assertEqual(result['candidates'][0]['raw_value'], '89 ± 2 °C')
        self.assertEqual(result['candidates'][0]['unit'], '°C')
        self.assertEqual(result['candidates'][0]['locator'], 'Technical data / table 1 / row 2')
        self.assertEqual(result['candidates'][1]['unit'], 'kPa')
        self.assertEqual(result['candidates'][0]['review_status'], 'needs_vehicle_verification')
        self.assertEqual(result['candidates'][0]['applicability_hint']['model_year'], 2008)
        self.assertNotIn('evidence_status', result['candidates'][0])

    def test_ambiguous_and_header_rows_not_promoted(self):
        html = '<h1>X</h1><table><tr><td>Opening</td><td>Closed</td></tr><tr><td>Oil</td><td>5W-30</td></tr><tr><td>Range</td><td>1 to 3</td></tr></table>'
        result = c.extract_candidates(html, URL)
        self.assertEqual(result['candidates'], [])
        self.assertGreaterEqual(result['skipped_rows'], 3)

    def test_rejects_other_host_and_invalid_scope(self):
        with self.assertRaises(ValueError):
            c.extract_candidates(HTML, 'https://example.com/9-5-9600/2008/')
        with self.assertRaises(ValueError):
            c.extract_candidates(HTML, 'https://saabwisonline.com/9-5-9600/not-a-year/')

    def test_deterministic_id_and_duplicates(self):
        first = c.extract_candidates(HTML, URL)
        again = c.extract_candidates(HTML, URL)
        self.assertEqual(first['candidates'], again['candidates'])
        repeated = HTML.replace('</table>', '<tr><td>Thermostat opening temperature</td><td>89 ± 2 °C</td></tr></table>')
        self.assertEqual(len(c.extract_candidates(repeated, URL)['candidates']), 2)

    def test_existing_url_marked_for_reconciliation(self):
        result = c.extract_candidates(HTML, URL, known_source_urls={URL})
        self.assertTrue(result['source_already_recorded'])
        self.assertEqual(result['candidates'][0]['promotion'], 'review_only')

    def test_write_review_file_does_not_replace_existing(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'review.json'
            path.write_text('existing')
            with self.assertRaises(FileExistsError):
                c.write_review(path, c.extract_candidates(HTML, URL))
            self.assertEqual(path.read_text(), 'existing')

if __name__ == '__main__': unittest.main()
