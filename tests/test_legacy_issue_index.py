"""Ensure every preexisting research issue is reusable without inventing factory defects."""
from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from database import load_datasets
from build_legacy_issue_index import build, validate_taxonomy

def read(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


class LegacyIssueIndexTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.datasets=load_datasets()
        cls.tax=read("data/audits/legacy-issue-taxonomy-20261014.json")
        cls.ledger=read("data/tier-research/observations.json")
        cls.index=build(cls.datasets,cls.tax,cls.ledger)

    def test_exhaustive_issue_lineage_and_categories(self):
        all_ids={x["id"] for d in self.datasets for x in d["issues"]}
        rows=self.index["existing_issue_records"]
        self.assertEqual(len(all_ids),92)
        self.assertEqual({r["issue_id"] for r in rows},all_ids)
        self.assertEqual(sum(self.index["counts"]["record_classifications"].values()),92)
        self.assertEqual(set(self.tax["categories"]),
                         set(self.index["counts"]["record_classifications"]))
        self.assertTrue(all(r["original_source_ids"] and r["original_source_urls"]
                            and isinstance(r["original_applicability"],dict)
                            for r in rows))
        self.assertTrue(all(not r["source_sharing_is_independent_corroboration"]
                            for r in rows))

    def test_only_source_documented_cases_have_mechanism_ids(self):
        index=self.index
        m=index["factory_mechanisms"]
        self.assertEqual(len(m),19)
        self.assertEqual(index["counts"]["issues_with_curated_mechanism"],21)
        relevant={"factory_documented_mechanism","factory_safety_campaign",
                  "suspected_factory_mechanism"}
        rows=index["existing_issue_records"]
        for x in rows:
            self.assertEqual(bool(x["canonical_mechanism_id"]),x["record_type"] in relevant)
        suspected=next(x for x in rows if x["issue_id"]=="corrections-issue-012")
        self.assertEqual(suspected["record_type"],"suspected_factory_mechanism")
        self.assertEqual(next(x for x in m if x["id"]==suspected["canonical_mechanism_id"])["state"],
                         "suspected_not_confirmed")

    def test_existing_tier_cases_not_re_discovered_and_cohorts_separate(self):
        ix={x["issue_id"]:x for x in self.index["existing_issue_records"]}
        ignition=ix["corrections-issue-004"]
        self.assertEqual(ignition["canonical_mechanism_id"],"mechanism-idm-igbt-overload")
        self.assertEqual(len(ignition["tier_case_ids"]),2)
        fa=ix["corrections-issue-006"]
        self.assertEqual(fa["canonical_mechanism_id"],"mechanism-fa57-cooler-connection-seal")
        self.assertEqual(fa["tier_case_ids"],["tier-failure-ng93-coolant-in-atf"])
        related=ix["corrections-issue-005"]
        self.assertNotEqual(fa["canonical_mechanism_id"],related["canonical_mechanism_id"])
        self.assertEqual(related["record_type"],"factory_documented_mechanism")
        self.assertEqual(ix["hcdiag-issue-003"]["record_type"],"diagnostic_nonunique")
        self.assertIsNone(ix["hcdiag-issue-003"]["canonical_mechanism_id"])
        self.assertIn("corrections-issue-006",
                      ix["hcdiag-issue-003"]["source_url_sharing_context_record_ids"]["issues"])

    def test_multiple_recall_records_one_hazard_without_merging_recall_scopes(self):
        ix={x["issue_id"]:x for x in self.index["existing_issue_records"]}
        ids=["corrections-issue-016","corrections-issue-020","wp7-issue-004"]
        mechanisms={ix[id_]["canonical_mechanism_id"] for id_ in ids}
        self.assertEqual(mechanisms,{"mechanism-takata-driver-airbag-inflator-rupture"})
        self.assertEqual(len({json.dumps(ix[id_]["original_applicability"],sort_keys=True)
                              for id_ in ids}),3)
        for id_ in ids:
            self.assertEqual(ix[id_]["record_type"],"factory_safety_campaign")

    def test_no_automatic_promotion_of_research_scenarios_into_defects(self):
        ix={x["issue_id"]:x for x in self.index["existing_issue_records"]}
        for id_ in ("nrscreen-issue-001","wp6-issue-001",
                    "og95t7-issue-004","rrtriage-issue-003","gateac-issue-001",
                    "hydbrake-issue-001","as-i001"):
            self.assertIsNone(ix[id_]["canonical_mechanism_id"])
        self.assertNotIn("failure_rate",json.dumps(self.index["counts"]))
        self.assertEqual(self.index["counts"]["existing_tier_cases"],3)

    def test_new_issue_requires_explicit_curated_reconciliation(self):
        modified=copy.deepcopy(self.tax)
        modified["assignments"]["diagnostic_nonunique"].remove("hcdiag-issue-003")
        with self.assertRaisesRegex(ValueError,"Unclassified/retired"):
            validate_taxonomy(self.datasets,modified,self.ledger)
        modified=copy.deepcopy(self.tax)
        modified["assignments"]["factory_documented_mechanism"].append("hcdiag-issue-003")
        with self.assertRaisesRegex(ValueError,"multiple"):
            validate_taxonomy(self.datasets,modified,self.ledger)
        modified=copy.deepcopy(self.tax)
        modified["mechanism_clusters"]=[
            m for m in modified["mechanism_clusters"]
            if m["id"]!="mechanism-fa57-cooler-connection-seal"]
        with self.assertRaisesRegex(ValueError,"exactly one"):
            validate_taxonomy(self.datasets,modified,self.ledger)


if __name__=="__main__":
    unittest.main()
