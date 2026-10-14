"""Detect repeated research and prevent an old finding from being relabelled new."""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from audit_research_reuse import build, text_key
from database import load_datasets


class ExistingResearchReuseAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.datasets = load_datasets()
        cls.ledger = json.loads((ROOT / "data/tier-research/observations.json").read_text())
        cls.census = json.loads((ROOT / "data/phase0-coverage-snapshot.json").read_text())
        cls.audit = build(cls.datasets, cls.ledger, cls.census)

    def test_canonical_census_still_matches_all_datasets(self):
        counts=self.audit["census"]
        self.assertEqual(counts["domains"], len(cls_datasets := self.datasets))
        self.assertEqual(counts["sources"], self.census["counts"]["sources"])
        self.assertEqual(counts["facts"], self.census["counts"]["facts"])
        self.assertEqual(counts["issues"], self.census["counts"]["issues"])
        self.assertEqual(counts["parts"], self.census["counts"]["parts"])
        self.assertEqual(counts["gaps"], self.census["counts"]["gaps"])
        self.assertEqual(counts["unique_exact_source_urls"], self.census["unique_source_urls"])
        self.assertEqual(counts["source_record_reuse_excess"],
                         counts["sources"]-counts["unique_exact_source_urls"])
        self.assertEqual(len(self.audit["existing_issue_catalogue"]),counts["issues"])
        self.assertEqual(len(self.audit["domain_evidence_inventory"]), len(cls_datasets))

    def test_case_to_legacy_issue_reuse_not_reinvention(self):
        bridges=self.audit["already_researched_tier_issue_bridges"]
        pairs={(x["tier_case_id"], x["preexisting_issue_id"]) for x in bridges}
        self.assertEqual(pairs, {
            ("tier-failure-idm-four-cylinder","corrections-issue-004"),
            ("tier-failure-idm-b308","corrections-issue-004"),
            ("tier-failure-ng93-coolant-in-atf","corrections-issue-006"),
            ("tier-failure-ng93-coolant-in-atf","hcdiag-issue-003"),
        })
        for record in bridges:
            self.assertEqual(record["relationship"],"same_mechanism_family")
            self.assertTrue(record["supporting_shared_original_urls"])
        related=self.audit["related_distinct_scope_campaigns"]
        self.assertEqual({(r["tier_case_id"], r["preexisting_issue_id"]) for r in related},
            {("tier-failure-ng93-coolant-in-atf","corrections-issue-005")})
        self.assertTrue(all("not_equivalent_scope" in r["relationship"] for r in related))

    def test_duplicate_candidates_are_not_authoritative_engineering_duplicates(self):
        self.assertGreater(self.audit["census"]["source_record_reuse_excess"],0)
        self.assertTrue(all(x["n_records"]>1 for x in self.audit["source_url_reuse_groups"]))
        self.assertTrue(all(len(x["record_ids"])>1 for x in
                            self.audit["issue_shared_source_cross_domain_review_groups"]))
        warnings=" ".join(self.audit["method_warnings"])
        self.assertIn("not proof of equal root cause",warnings)
        self.assertIn("not the number of unique factory design faults",warnings)
        self.assertIn("not independently corroborated",warnings)
        self.assertIn("not verified parts",warnings)

    def test_tier_is_unrated_without_frequency_studies_or_current_market_quotes(self):
        counts=self.audit["census"]
        self.assertEqual(counts["tier_cohort_cases"],len(self.ledger["failure_modes"]))
        self.assertEqual(counts["tier_engineering_mechanisms"],len(self.ledger["failure_mechanisms"]))
        self.assertEqual(counts["independent_failure_frequency_studies_in_tier_ledger"],0)
        self.assertEqual(counts["tier_verified_parts_market_offers"],0)
        self.assertEqual(counts["tier_complete_repair_cost_observations"],0)
        self.assertNotIn("rank", str(self.audit.get("tier_grade","")))
        self.assertNotIn("ranking_score",self.audit)

    def test_title_normalization_is_conservative(self):
        self.assertEqual(text_key("Ignition--Module /  Overload  "),
                         "ignition module overload")
        self.assertNotEqual(text_key("Ignition-module overload"),
                            text_key("Coolant in transmission"))


if __name__ == "__main__":
    unittest.main()
