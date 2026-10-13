"""Audit index is grounded in real Phase 0 gap records and never promotes decisions."""
import json
import unittest
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
REG=BASE/'data'/'audits'/'phase0-gap-register-20261013.json'
class Phase0GapRegisterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.audit=json.loads(REG.read_text(encoding='utf-8'))
        cls.gaps=set()
        for path in (BASE/'data'/'datasets').glob('*.json'):
            dataset=json.loads(path.read_text(encoding='utf-8'))
            cls.gaps.update(g['id'] for g in dataset['gaps'])

    def test_every_link_to_existing_gap_is_real(self):
        rows=self.audit['blockers']
        self.assertEqual(len(rows),len({r['id'] for r in rows}))
        self.assertGreaterEqual(len(rows),15)
        for row in rows:
            with self.subTest(id=row['id']):
                self.assertEqual(row['review_status'],'open')
                self.assertTrue(row['decision_blocked'])
                self.assertTrue(row['exit_evidence'])
                self.assertTrue(set(row['linked_gap_ids']) <= self.gaps)
                if row['coverage_state']=='new_coverage_question':
                    self.assertEqual(row['linked_gap_ids'],[])
                else:
                    self.assertTrue(row['linked_gap_ids'])

    def test_not_an_approved_model_ranking(self):
        self.assertIn('Gate B',self.audit['decision'])
        self.assertNotIn('approved',self.audit['decision'].lower())
        self.assertTrue(any(r['id']=='P0-U01' for r in self.audit['blockers']))
        self.assertTrue(any(r['id']=='P1-U02' for r in self.audit['blockers']))
        self.assertTrue(any(r['needs_specific_vehicle_data'] for r in self.audit['blockers']))
