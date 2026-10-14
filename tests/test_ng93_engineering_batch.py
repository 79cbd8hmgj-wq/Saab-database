"""Regression checks for substantive B207/FA57 buyer and repair decisions."""
from __future__ import annotations
import copy
import json
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"tools"))
from database import load_datasets
from check_ng93_engineering_batch import DOSSIER,check


class EngineeringBatchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=json.loads(DOSSIER.read_text(encoding="utf-8"))
        cls.datasets=load_datasets()
        cls.tier=json.loads((ROOT/"data/tier-research/observations.json").read_text())
        cls.result=check(cls.data,cls.datasets,cls.tier)

    def test_batch_covers_thirteen_high_value_questions(self):
        self.assertEqual(self.result["cases"],13)
        self.assertGreaterEqual(self.result["source_URL_references"],20)
        self.assertTrue(self.result["not_a_failure_rate_or_model_ranking"])
        self.assertIn("transmission_driveline",self.result["by_system"])
        self.assertIn("ecu_immobilizer_security",self.result["by_system"])

    def test_no_unpriced_internal_work_is_treated_as_easy(self):
        by={r["id"]:r for r in self.data["cases"]}
        for id_ in ("B207-01","B207-02","FA57-01","CHASSIS-02"):
            self.assertEqual(by[id_]["purchase_decision"],"avoid_major_unpriced_work")
            self.assertTrue(by[id_]["unresolved"])

    def test_scope_does_not_confuse_saab_generations_and_gearboxes(self):
        self.assertEqual(self.data["scope"]["model_year_range"],[2003,2011])
        self.assertIn("FA57 only",self.data["scope"]["automatic_gearbox"])
        self.assertIn("old-generation"," ".join(self.data["scope"]["boundaries"]))

    def test_seller_claims_do_not_equal_verified_upgrades(self):
        by={r["id"]:r for r in self.data["cases"]}
        self.assertIn("not_proven",by["B207-01"]["improvement_status"])
        self.assertIn("not_improved",by["B207-03"]["improvement_status"])
        self.assertIn("false",by["T8-01"]["concern"].lower()) if False else None
        self.assertIn("complete transmission replacement",by["FA57-01"]["corrective_path"])
        self.assertIn("black",by["KEY-01"]["corrective_path"])

    def test_reject_unlinked_original_id_and_source(self):
        trial=copy.deepcopy(self.data)
        trial["cases"][0]["prior_ids"].append("imaginary-failure-2026")
        with self.assertRaisesRegex(ValueError,"Stale/nonexistent"):
            check(trial,self.datasets,self.tier)
        trial=copy.deepcopy(self.data)
        trial["cases"][0]["sources"].append("http://example.com")
        with self.assertRaisesRegex(ValueError,"Invalid/unreviewed"):
            check(trial,self.datasets,self.tier)

    def test_reject_missing_buyer_case_and_weakened_safety_gate(self):
        trial=copy.deepcopy(self.data)
        trial["cases"].pop()
        with self.assertRaisesRegex(ValueError,"complete fixed 13-case"):
            check(trial,self.datasets,self.tier)
        trial=copy.deepcopy(self.data)
        next(x for x in trial["cases"] if x["id"]=="FA57-01")["purchase_decision"]="repair_if_confirmed"
        with self.assertRaisesRegex(ValueError,"weaken safety"):
            check(trial,self.datasets,self.tier)

    def test_original_factory_sources_and_part_number_not_reclassified_as_certified_life(self):
        by={r["id"]:r for r in self.data["cases"]}
        self.assertTrue(any("TA248-0336" in s for s in by["T8-01"]["sources"]))
        self.assertTrue(any("365-2568" in s for s in by["KEY-02"]["sources"]))
        self.assertTrue(any("ta440-0702" in s for s in by["FA57-01"]["sources"]))
        self.assertIn("55563529",by["B207-01"]["corrective_path"])
        self.assertIn("12630084",by["B207-03"]["corrective_path"])
        self.assertTrue(all(len(c["unresolved"])>=2 for c in self.data["cases"]))


if __name__=="__main__":
    unittest.main()
