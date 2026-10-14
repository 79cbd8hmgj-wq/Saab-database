"""A source-rich Saab configuration is not automatically a good or bad Saab."""
from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from build_tier_evidence_readiness import build, PRODUCTION, SCENARIOS, TOOLS, METHOD, OUTPUT

def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))

class NeutralTierResearchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.production = load(PRODUCTION)
        cls.feasibility = load(SCENARIOS)
        cls.tooling = load(TOOLS)
        cls.methodology = load(METHOD)
        cls.snapshot = load(OUTPUT)

    def test_reproducible_snapshot_uses_real_existing_110_row_denominator(self):
        self.assertEqual(
            build(self.production, self.feasibility, self.tooling, self.methodology),
            self.snapshot,
        )
        self.assertEqual(self.snapshot["denominator"], 110)
        self.assertEqual(self.snapshot["number_with_research_scenario_leads"], 110)
        self.assertEqual(self.snapshot["number_with_parts_tool_job_leads"], 110)
        self.assertEqual(len(self.snapshot["records"]), 110)
        ids = [r["production_configuration_id"] for r in self.snapshot["records"]]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual({c["id"] for c in self.production["configurations"]}, set(ids))
        self.assertIn("not all Saab models", self.snapshot["universe"])

    def test_all_comparability_statuses_are_unassessed_not_failure_rates(self):
        self.assertEqual(self.methodology["status"], "research_protocol_no_tier_assignments")
        expected = {d["id"] for d in self.methodology["dimensions"]}
        self.assertEqual(len(expected), 4)
        self.assertEqual(len(self.methodology["system_inventory"]), 16)
        self.assertEqual(self.snapshot["number_ranked"], 0)
        self.assertEqual(self.snapshot["number_with_quantified_failure_rate"], 0)
        self.assertEqual(self.snapshot["number_with_full_repair_quotes"], 0)
        self.assertEqual(self.snapshot["number_with_VIN_approved_replacements"], 0)
        self.assertEqual(len(self.snapshot["shared_unresolved_requirements"]), 6)
        for row in self.snapshot["records"]:
            self.assertEqual(set(row["dimension_assessments"]), expected)
            self.assertTrue(all(
                value == "not_audited_for_comparable_population_and_part_evidence"
                for value in row["dimension_assessments"].values()))
            self.assertTrue(row["not_rankable"])
            self.assertFalse(row["factory_applicability_approved"])
            for key in (
                "tier", "ranking", "documented_failure_rate", "verified_US_parts_availability",
                "VIN_approved_replacement_matrix", "full_repair_cost_USD",
            ):
                self.assertIsNone(row[key])

    def test_research_leads_are_not_measured_faults_or_approved_replacements(self):
        source_scenarios = {
            r["production_id"]: sorted(s["scenario_id"] for s in r["scenario_links"])
            for r in self.feasibility["production_group_reviews"]
        }
        for row in self.snapshot["records"]:
            self.assertEqual(
                row["existing_diagnostic_scenario_leads"],
                source_scenarios[row["production_configuration_id"]],
            )
            self.assertTrue(row["existing_parts_tool_job_leads"])
            self.assertEqual(
                row["identity_from_unverified_compiled_US_production"]["drivetrain"], "FWD")
            self.assertIn(row["identity_from_unverified_compiled_US_production"]["reported_automatic_gear_count"], (4,5,6))

    def test_new_population_risk_evidence_needs_explicit_methodology_review(self):
        bad = copy.deepcopy(self.feasibility)
        bad["counts"]["failure_rates_quantified"] = 1
        with self.assertRaisesRegex(ValueError,"reviewed readiness method"):
            build(self.production, bad, self.tooling, self.methodology)
        bad = copy.deepcopy(self.tooling)
        bad["no_parts_fitment_approved"] = False
        with self.assertRaisesRegex(ValueError,"revisit assumptions"):
            build(self.production, self.feasibility, bad, self.methodology)
        bad = copy.deepcopy(self.feasibility)
        bad["production_group_reviews"][0]["scenario_links"][0]["actual_fault_confirmed"] = True
        with self.assertRaisesRegex(ValueError,"actual fault"):
            build(self.production, bad, self.tooling, self.methodology)

    def test_no_year_or_engine_shortcuts_and_unknown_not_zero(self):
        bad = copy.deepcopy(self.tooling)
        bad["production_groups"][0]["engine_code"] = "UNVERIFIED"
        with self.assertRaisesRegex(ValueError,"Conflicting"):
            build(self.production, self.feasibility, bad, self.methodology)
        bad = copy.deepcopy(self.production)
        bad["configurations"] = bad["configurations"][:-1]
        with self.assertRaisesRegex(ValueError,"denominator changed"):
            build(bad, self.feasibility, self.tooling, self.methodology)

    def test_source_ratings_do_not_confuse_repair_publicity_with_prevalence(self):
        m=self.methodology
        self.assertIn("denominator", m["quantitative_observation_requirements"])
        self.assertTrue(m["quantitative_observation_requirements"]["no_unsupported_percentages"])
        for kind in ("factory_source", "owner_complaint", "inspection_statistic", "warranty_or_fleet", "supplier_catalogue"):
            self.assertIn(kind,m["evidence_classes"])
        source_ids={s["id"] for s in m["source_pipeline"]}
        self.assertIn("src-nhtsa-complaints",source_ids)
        self.assertIn("src-dvsa-mot",source_ids)
        self.assertIn("src-saab-epc",source_ids)
        self.assertIsNone(self.snapshot["records"][0]["documented_failure_rate"])

if __name__ == "__main__":
    unittest.main()
