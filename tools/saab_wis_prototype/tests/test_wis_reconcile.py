"""Stage 4: no-write comparison with actual Saab Database dataset shape."""
import json
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from wis_reconcile import reconcile, load_repo_index, write_reconciliation

URL = 'https://saabwisonline.com/9-5-9600/2008/2-engine/cooling-system/technical-data/tightening-torques'

def candidate(subject='Thermostat housing, 4-cyl.', value='22'):
    return {'candidate_id':'wis-review-a','source_url': URL,'subject':subject, 'raw_value':value,'unit':'Nm',
            'locator':'Tightening torques / table 1 / row 2','applicability_hint':{'platform_path':'9-5-9600','model_year':2008},
            'promotion':'review_only'}

class ReconcileTests(unittest.TestCase):
    def test_loads_only_datasets_and_identifies_reused_source_urls(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); (root/'data/datasets').mkdir(parents=True)
            (root/'data/datasets/x.json').write_text(json.dumps({'sources':[{'id':'old-1','url':URL}], 'facts':[], 'issues':[], 'parts':[], 'gaps':[]}))
            (root/'data/datasets/y.json').write_text(json.dumps({'sources':[{'id':'old-2','url':URL+'/' }], 'facts':[], 'issues':[], 'parts':[], 'gaps':[]}))
            urls, facts=load_repo_index(root)
            self.assertEqual(len(urls[URL]),2)
            self.assertEqual(facts,[])

    def test_matching_source_is_not_claimed_new_and_never_auto_promoted(self):
        sources={URL:[{'id':'s1','path':'data/datasets/foo.json'}]}
        result=reconcile({'candidates':[candidate()]},sources,[])
        rec=result['results'][0]
        self.assertEqual(rec['source_status'],'already_indexed')
        self.assertEqual(rec['possible_fact_matches'],[])
        self.assertEqual(rec['decision'],'manual_review')
        self.assertEqual(result['writes_to_repository'],False)

    def test_existing_fact_is_a_possible_match_not_verified_equivalence(self):
        facts=[{'id':'f1','subject':'Thermostat housing, 4-cyl.', 'value':22, 'unit':'Nm', 'source_ids':['s1'], 'path':'data/datasets/foo.json'}]
        result=reconcile({'candidates':[candidate()]},{URL:[{'id':'s1','path':'foo'}]},facts)
        self.assertEqual(result['results'][0]['possible_fact_matches'],['f1'])
        self.assertEqual(result['results'][0]['decision'],'manual_review')

    def test_same_subject_different_value_flagged_as_potential_conflict(self):
        facts=[{'id':'f2','subject':'Thermostat housing, 4-cyl.', 'value':30, 'unit':'Nm', 'source_ids':['s1']}]
        result=reconcile({'candidates':[candidate()]},{URL:[{'id':'s1'}]},facts)
        self.assertEqual(result['results'][0]['potential_conflicts'],['f2'])

    def test_output_will_not_overwrite_previous_review(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'review.json'; p.write_text('original')
            with self.assertRaises(FileExistsError): write_reconciliation(p, {'results':[]})
            self.assertEqual(p.read_text(),'original')

if __name__=='__main__': unittest.main()
