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

    def test_shared_ignition_failure_mechanism_has_separate_cohort_cases(self):
        ledger=read_json(ROOT/"data/tier-research/observations.json")
        mechanisms={r["id"]:r for r in ledger["failure_mechanisms"]}
        cases={r["id"]:r for r in ledger["failure_modes"]}
        self.assertEqual(len(mechanisms),2)
        self.assertEqual(len(cases),3)
        self.assertEqual(set(ledger["minimum_record_contract"]["failure_mechanisms"]),
                         set(("id","description","category","factory_failure_mechanism",
                              "source_ids","related_case_ids","scope_note","frequency_status")))
        for case in cases.values():
            self.assertIn(case["mechanism_id"],mechanisms)
        for mechanism in mechanisms.values():
            self.assertEqual(mechanism["frequency_status"],"unknown")
            self.assertEqual(set(mechanism["related_case_ids"]),
                             {k for k,v in cases.items() if v["mechanism_id"]==mechanism["id"]})
        four=cases["tier-failure-idm-four-cylinder"]
        six=cases["tier-failure-idm-b308"]
        coolant=cases["tier-failure-ng93-coolant-in-atf"]
        self.assertEqual(four["mechanism_id"],six["mechanism_id"])
        self.assertNotEqual(four["mechanism_id"],coolant["mechanism_id"])
        self.assertNotEqual(four["configuration_scope"],six["configuration_scope"])
        self.assertNotEqual(four["factory_correction"],"")
        self.assertEqual(len(ledger["fleet_failure_frequency_studies"]),0)

    def test_fa57_original_bulletin_has_exact_exclusive_variant_boundaries(self):
        ledger=read_json(ROOT/"data/tier-research/observations.json")
        fa=next(r for r in ledger["failure_modes"]
                if r["id"]=="tier-failure-ng93-coolant-in-atf")
        self.assertTrue(fa["configuration_scope"]["manual_scope_resolution_required"])
        self.assertEqual(fa["population_frequency_status"],"unknown")
        groups=fa["configuration_scope"]["groups"]
        self.assertEqual(len(groups),3)
        expected={
            "ta440-0702-ss": ("SS","9-3SS","51002378"),
            "ta440-0702-ss-tid": ("SS","9-3SS TiD","51000001"),
            "ta440-0702-cv": ("CV","9-3CV","56001058"),
        }
        self.assertEqual({g["group_id"] for g in groups},set(expected))
        for group in groups:
            body,line,limit=expected[group["group_id"]]
            self.assertEqual(group["platforms"],["9-3-9440"])
            self.assertEqual(group["model_years"],[2003,2004,2005])
            self.assertEqual(group["transmission_codes"],["FA57"])
            self.assertEqual(group["markets"],["all"])
            self.assertEqual(group["body_styles"],[body])
            self.assertTrue(group["manual_scope_resolution_required"])
            self.assertEqual(group["engine_codes"],[])
            self.assertEqual(len(group["vin_ranges"]),1)
            bound=group["vin_ranges"][0]
            self.assertEqual(bound["end"],limit)
            self.assertEqual(bound["source_line"],line)
            self.assertTrue(bound["upper_bound_exclusive"])
            self.assertIn("STRICTLY BELOW",bound["format"])
        self.assertIn("TiD_diesel",groups[1]["engine_variant_category"])
        self.assertNotIn("B207",str(groups))
        top_level={v["source_line"]:v["end"] for v in fa["configuration_scope"]["vin_ranges"]}
        self.assertEqual(top_level,{"9-3SS":"51002378","9-3SS TiD":"51000001","9-3CV":"56001058"})
        self.assertTrue(all(x["upper_bound_exclusive"]
                            for x in fa["configuration_scope"]["vin_ranges"]))

    def test_recall_population_is_not_a_measured_failure_rate(self):
        d=read_json(ROOT/"data/datasets/tier-component-factory-revision-20261014.json")
        facts={x["id"]:x for x in d["facts"]}
        claim=facts["tier-fact-001"]
        self.assertEqual(claim["subject"],"campaign:06V410")
        self.assertEqual(claim["predicate"],"potential_units_affected_not_verified_failures")
        self.assertEqual(claim["value"],5078)
        self.assertEqual(claim["unit"],"vehicles in recall population")
        self.assertIn("neither failed cars nor at-risk exposure",claim["notes"])
        ledger=read_json(ROOT/"data/tier-research/observations.json")
        self.assertEqual(ledger["fleet_failure_frequency_studies"],[])
        self.assertEqual(ledger["parts_market_offers"],[])
        self.assertEqual(ledger["complete_repair_cost_observations"],[])

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
