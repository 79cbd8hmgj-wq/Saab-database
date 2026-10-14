"""Tier-list research must not become premature Saab model rankings."""
import copy
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"tools"))
from build_tier_readiness import build, read_json, PRODUCTION, FEASIBILITY, PARTS_TOOLS, PROTOCOL, OUT

class TierReadinessResearchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.p=read_json(PRODUCTION)
        cls.f=read_json(FEASIBILITY)
        cls.t=read_json(PARTS_TOOLS)
        cls.m=read_json(PROTOCOL)
        cls.result=build(cls.p,cls.f,cls.t,cls.m)

    def test_generated_audit_reproducible_and_unranked(self):
        self.assertEqual(self.result,read_json(OUT))
        self.assertEqual(len(self.result["configuration_rows"]),110)
        self.assertEqual(self.result["summary"]["ranked_models"],0)
        self.assertEqual(self.result["summary"]["groups_rankable"],0)
        self.assertTrue(all(x["tier"] is None and not x["rankable"] and
                            x["confidence_grade"] is None
                            for x in self.result["configuration_rows"]))

    def test_identical_cohort_denominator_not_selective(self):
        ids={x["id"] for x in self.p["configurations"]}
        rows=self.result["configuration_rows"]
        self.assertEqual({x["production_configuration_id"] for x in rows},ids)
        self.assertEqual(len(ids),110)
        self.assertEqual(self.result["summary"]["groups_with_existing_diagnostic_leads"],110)
        self.assertEqual(self.result["summary"]["groups_with_existing_parts_tool_leads"],110)
        self.assertTrue(all(x["market"]=="US" and x["drivetrain"]=="FWD" for x in rows))
        self.assertTrue(all("nonconvertible" in self.result["scope"] for x in [0]))

    def test_frequency_parts_and_total_costs_not_inferred_from_leads(self):
        for row in self.result["configuration_rows"]:
            axes=row["tier_comparison_evidence"]
            self.assertEqual(set(axes),{
                "factory_component_reliability","parts_supply",
                "known_failure_burden","repairability_economics"})
            self.assertTrue(all(isinstance(x,str) and x for x in axes.values()))
            self.assertIn("not_population_incidence",axes["known_failure_burden"])
            self.assertIn("no_vehicle_specific",axes["parts_supply"])
            self.assertTrue(row["unresolved"])
        for key in ("groups_with_usable_population_failure_frequency",
                    "groups_with_exact_VIN_approved_parts_and_confirmed_US_supply",
                    "groups_with_all_in_repair_costs"):
            self.assertEqual(self.result["summary"][key],0)

    def test_separate_durability_supply_failure_and_cost_evidence_standards(self):
        m=self.m
        self.assertEqual(len(m["dimensions"]),4)
        self.assertGreaterEqual(len(m["system_inventory"]),14)
        self.assertTrue(all(x["required_fields"] for x in m["dimensions"]))
        self.assertIn("src-dvsa-mot",{x["id"] for x in m["source_pipeline"]})
        self.assertIn("src-nhtsa-complaints",{x["id"] for x in m["source_pipeline"]})
        self.assertTrue(m["quantitative_observation_requirements"]["no_unsupported_percentages"])
        self.assertEqual(m["readiness_requirements"]["weighting"][:8],"Not set.")
        self.assertIn("9-2X",m["boundaries"]["candidate_policy"])
        self.assertEqual(m["status"],"research_protocol_no_tier_assignments")

    def test_dont_silently_extend_or_promote_scope(self):
        invalid=copy.deepcopy(self.p)
        invalid["configurations"].pop()
        with self.assertRaises(ValueError):
            build(invalid,self.f,self.t,self.m)
        invalid=copy.deepcopy(self.f)
        invalid["counts"]["failure_rates_quantified"]=1
        with self.assertRaises(ValueError):
            build(self.p,invalid,self.t,self.m)
        invalid=copy.deepcopy(self.t)
        invalid["production_groups"][0]["job_readiness_leads"][0]["vin_and_part_fitment_confirmed"]=True
        with self.assertRaises(ValueError):
            build(self.p,self.f,invalid,self.m)
        invalid=copy.deepcopy(self.m)
        invalid["dimensions"].pop()
        with self.assertRaises(ValueError):
            build(self.p,self.f,self.t,invalid)

    def test_new_special_tool_verification_cannot_be_ignored(self):
        invalid=copy.deepcopy(self.t)
        invalid["production_groups"][0]["job_readiness_leads"][0]["special_tool_access_confirmed"]=True
        with self.assertRaises(ValueError):
            build(self.p,self.f,invalid,self.m)

    def test_component_evidence_intake_is_blank_without_hidden_ratings(self):
        intake=read_json(ROOT/"data/tier-research/component-evidence-template.json")
        self.assertEqual(intake["record_state"],"blank_research_template_no_vehicle_or_part_assertions")
        self.assertIsNone(intake["original_component"]["factory_part_number"])
        self.assertEqual(intake["failure_evidence"],[])
        self.assertEqual(intake["replacement_candidates"],[])
        self.assertEqual(intake["supply_observations"],[])
        self.assertIsNone(intake["quantitative_risk"]["computed_rate"])
        self.assertIsNone(intake["repairability"]["verified_total_usd"])
        self.assertFalse(intake["assessed_in_comparable_cohort"])
        self.assertFalse((ROOT/"tools/build_tier_evidence_readiness.py").exists())
        self.assertFalse((ROOT/"data/tier-research/us-110-evidence-readiness.json").exists())
        self.assertFalse((ROOT/"tests/test_tier_evidence_readiness.py").exists())

    def test_initial_observations_do_not_fabricate_rates_or_costs(self):
        observations=read_json(ROOT/"data/tier-research/observations.json")
        for field in ("fleet_failure_frequency_studies","parts_market_offers",
                      "complete_repair_cost_observations"):
            self.assertEqual(observations[field],[])
        self.assertIn("not_a_zero_failure_assertion",observations["interpretation"])

    def test_observation_contract_and_provenance(self):
        observations=read_json(ROOT/"data/tier-research/observations.json")
        datasets=[read_json(p) for p in (ROOT/"data/datasets").glob("*.json")]
        sources={s["id"] for d in datasets for s in d["sources"]}
        systems={s["id"] for s in self.m["system_inventory"]}
        ids=[]
        for category, required in observations["minimum_record_contract"].items():
            for record in observations[category]:
                self.assertTrue(set(required).issubset(record),record.get("id"))
                if "source_ids" in required:
                    self.assertTrue(record["source_ids"])
                    self.assertTrue(set(record["source_ids"]).issubset(sources))
                ids.append(record["id"])
                if category=="failure_modes":
                    self.assertIn(record["system_id"],systems)
                    self.assertEqual(record["population_frequency_status"],"unknown")
        self.assertEqual(len(ids),len(set(ids)))

    def test_recalled_ignition_cohorts_remain_separate(self):
        observations=read_json(ROOT/"data/tier-research/observations.json")
        modes={r["id"]:r for r in observations["failure_modes"]}
        four=modes["tier-failure-idm-four-cylinder"]
        six=modes["tier-failure-idm-b308"]
        self.assertEqual(four["configuration_scope"]["model_years"],[2000,2001,2002])
        self.assertNotIn("B308",four["configuration_scope"]["engine_codes"])
        self.assertEqual(six["configuration_scope"]["platforms"],["9-5-9600"])
        self.assertEqual(six["configuration_scope"]["engine_codes"],["B308"])
        self.assertNotIn("9-3-9440",four["configuration_scope"]["platforms"])

    def test_component_revision_date_is_not_vehicle_year_or_original_part(self):
        revisions=read_json(ROOT/"data/tier-research/observations.json")["original_part_revisions"]
        expected={"tier-revision-idm-four-cylinder":"2002-07-04",
                  "tier-revision-idm-b308":"2003-01-07"}
        for revision in revisions:
            self.assertIsNone(revision["original_part_number"])
            self.assertEqual(revision["revision_or_countermeasure"]["component_manufacturing_introduction_date"],expected[revision["id"]])
            self.assertIn("not a vehicle model-year cutover",revision["effective_original_build_scope"])

if __name__=="__main__":
    unittest.main()
