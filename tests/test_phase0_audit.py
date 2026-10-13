"""Fail CI when the whole-project Phase 0 census becomes stale or unsafely broad."""
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT / "tools"))
from database import load_datasets, validate_datasets
from phase0_audit import (
    BEGIN, END, build_snapshot, render_census,
)


class WholeProjectPhase0AuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.datasets=load_datasets()
        cls.snapshot=json.loads(
            (ROOT / "data" / "phase0-coverage-snapshot.json").read_text(encoding="utf-8")
        )
        cls.audit=(ROOT / "docs" / "coverage-audit.md").read_text(encoding="utf-8")

    def test_all_26_domains_and_scope_counts_match_checked_in_records(self):
        self.assertEqual(validate_datasets(self.datasets),[])
        actual=build_snapshot(self.datasets)
        differences={}
        for key in actual:
            if actual[key]!=self.snapshot.get(key):
                if isinstance(actual[key],dict):
                    a=actual[key]; b=self.snapshot.get(key,{})
                    differences[key]={
                        k:{"actual":v,"stored":b.get(k)}
                        for k,v in a.items() if v!=b.get(k)
                    }
                else:
                    differences[key]={"actual":actual[key],"stored":self.snapshot.get(key)}
        self.assertEqual(differences,{})

    def test_human_audit_has_exactly_one_current_generated_census(self):
        self.assertEqual(self.audit.count(BEGIN),1)
        self.assertEqual(self.audit.count(END),1)
        self.assertIn(render_census(self.snapshot),self.audit)
        self.assertIn("These are stored record counts",self.audit)

    def test_inventory_and_source_index_match_real_deduplication(self):
        saved=json.loads((ROOT / "data" / "inventory.json").read_text(encoding="utf-8"))
        index=(ROOT / "docs" / "source-index.md").read_text(encoding="utf-8")
        for k in ("counts","unique_source_urls","retrieval_statuses","evidence_statuses"):
            self.assertEqual(saved[k],self.snapshot[k],k)
        header=(
            f"There are {self.snapshot['counts']['sources']} source records with "
            f"{self.snapshot['unique_source_urls']} distinct" + "\nURLs."
        )
        self.assertIn(header,index)

    def test_no_unearned_vehicle_or_parts_approval(self):
        self.assertIn("Gate A = partial", (ROOT / "docs" / "gap-closure-plan.md").read_text(encoding="utf-8"))
        self.assertIn("Gate B = not met", (ROOT / "docs" / "gap-closure-plan.md").read_text(encoding="utf-8"))
        self.assertIn("Gate C = not met", (ROOT / "docs" / "gap-closure-plan.md").read_text(encoding="utf-8"))
        self.assertIn("NOT completeness, fitment, or reliability",self.snapshot["meaning"])
        self.assertLess(self.snapshot["parts_provenance"]["with_relationships"],
                        self.snapshot["parts_provenance"]["total"])
        self.assertEqual(self.snapshot["counts"]["facts"] + self.snapshot["counts"]["issues"]+
                         self.snapshot["counts"]["parts"],1007)

    def test_no_cross_year_data_leakage_for_grouped_applications(self):
        synthetic=[{"domain":"test_scope",
            "sources":[],
            "facts":[{"evidence_status":"documented",
                "applicability":{"platforms":["9-5-9600","9-3-9440"],"model_years":[2005,2006],
                  "groups":[
                    {"platforms":["9-5-9600"],"model_years":[2005]},
                    {"platforms":["9-3-9440"],"model_years":[2006]}
                  ]}}],
            "issues":[],"parts":[],"gaps":[]}]
        snapshot=build_snapshot(synthetic)
        self.assertEqual(snapshot["platform_year"]["9-5-9600"]["2005"]["facts"],1)
        self.assertEqual(snapshot["platform_year"]["9-5-9600"]["2006"]["facts"],0)
        self.assertEqual(snapshot["platform_year"]["9-3-9440"]["2006"]["facts"],1)
        self.assertEqual(snapshot["explicit_scope_counts"]["model_years"],1)

if __name__=="__main__":
    unittest.main()
