"""Exhaustive but explicitly non-adjudicating crosswalk of Saab research evidence."""
from __future__ import annotations
import copy
import json
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"tools"))
from database import load_datasets
from build_system_evidence_index import build, check_policy, route

def read(rel):
    return json.loads((ROOT/rel).read_text(encoding="utf8"))

class SystemResearchIndexTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.datasets=load_datasets()
        cls.policy=read("data/audits/system-evidence-routing-policy-20261014.json")
        cls.method=read("data/tier-research/methodology.json")
        cls.taxonomy=read("data/audits/legacy-issue-taxonomy-20261014.json")
        cls.ledger=read("data/tier-research/observations.json")
        cls.census=read("data/phase0-coverage-snapshot.json")
        cls.report=build(cls.datasets,cls.policy,cls.method,cls.taxonomy,cls.ledger,cls.census)
        cls.by_id={x["id"]:x for x in cls.report["records"]}

    def test_all_records_are_included_with_unchanged_provenance(self):
        saved={x["id"]:(k,d["domain"],x)
               for d in self.datasets
               for k in ("facts","issues","parts","gaps")
               for x in d[k]}
        self.assertEqual(len(saved),1101+92+89+284)
        self.assertEqual(len(self.by_id),len(saved))
        self.assertEqual(set(self.by_id),set(saved))
        self.assertEqual(self.report["tracked_systems"],16)
        for record in self.report["records"]:
            kind,domain,original=saved[record["id"]]
            self.assertEqual((record["kind"],record["domain"]),(kind,domain))
            self.assertEqual(record["original_source_ids"],original["source_ids"])
            self.assertEqual(record["original_applicability"],original.get("applicability"))
            if kind != "gaps":
                self.assertTrue(record["original_source_urls"])
            self.assertEqual(record["no_source_is_unanswered_research_question"],
                             kind == "gaps" and not bool(original["source_ids"]))
            self.assertFalse(record["source_overlap_proves_same_root_cause"])
            self.assertFalse(record["source_overlap_proves_same_vehicle_scope"])
            self.assertFalse(record["eligible_for_model_rating_from_this_index"])

    def test_validated_system_ids_or_explicit_unrouted(self):
        ids=set(self.report["systems"])
        self.assertEqual(ids,{x["id"] for x in self.method["system_inventory"]})
        for rec in self.report["records"]:
            self.assertTrue(set(rec["system_ids_for_discovery"]).issubset(ids))
            self.assertEqual(rec["cross_cutting_or_unresolved_system"],
                             not bool(rec["system_ids_for_discovery"]))
            self.assertEqual(rec["primary_navigation_system"],
                             (rec["system_ids_for_discovery"] or [None])[0])
            self.assertEqual(rec["review_status"],"not_manually_adjudicated")
            self.assertNotIn("certified",rec["routing_basis"])
        self.assertEqual(sum(self.report["record_routes"].values()),len(self.by_id))

    def test_specific_examples_not_misrepresented(self):
        cases={
          "corrections-part-001":"engine_core_oil_pcv",
          "gmwp-part-001":"cooling_heat",
          "cross-part-001":"steering_suspension",
          "as-p001":"charging_starting_wiring",
          "mountbrake-part-001":"body_corrosion_mounts",
          "repl-part-001":"turbo_intake_boost",
          "corrections-issue-016":"restraints_safety",
          "corrections-issue-011":"engine_timing_valvetrain",
          "corrections-issue-006":"cooling_heat",
          "hydbrake-issue-001":"brakes_hydraulics",
          "rustgate-issue-001":"body_corrosion_mounts",
          "og95wire-fact-001":"charging_starting_wiring",
          "wp6-fact-002":"fuel_emissions_exhaust",
        }
        for name,system in cases.items():
            self.assertIn(system,self.by_id[name]["system_ids_for_discovery"],name)
        fa=self.by_id["corrections-issue-006"]
        self.assertEqual(fa["claim_type"],"factory_documented_mechanism")
        self.assertEqual(fa["canonical_mechanism_id"],
                         "mechanism-fa57-cooler-connection-seal")
        self.assertFalse(fa["eligible_for_model_rating_from_this_index"])
        suspected=self.by_id["corrections-issue-012"]
        self.assertEqual(suspected["claim_type"],"suspected_factory_mechanism")
        self.assertEqual(self.by_id["hcdiag-issue-003"]["claim_type"],"diagnostic_nonunique")

    def test_parts_and_gaps_cannot_assert_fitment_or_approval(self):
        for p in (r for r in self.report["records"] if r["kind"]=="parts"):
            self.assertFalse(p["live_US_fulfilment_verified_by_this_index"])
            self.assertFalse(p["supersession_is_verified_by_this_index"])
            self.assertIn("not_VIN_approved",p["claim_type"])
        for g in (r for r in self.report["records"] if r["kind"]=="gaps"):
            self.assertFalse(g["resolved_by_this_index"])
        self.assertEqual(self.report["input_technical_counts"]["facts"],1101)
        self.assertEqual(self.report["input_technical_counts"]["issues"],92)
        self.assertEqual(self.report["input_technical_counts"]["parts"],89)
        self.assertEqual(self.report["input_technical_counts"]["gaps"],284)

    def test_system_counts_are_overlapping_navigation_not_completeness(self):
        for system in self.report["systems"].values():
            for label in ("factory_documented_claims_coverage_certified",
                          "original_component_lifetime_coverage_certified",
                          "exact_US_parts_fulfilment_certified",
                          "complete_US_repair_cost_certified",
                          "population_failure_rate_available_from_this_index"):
                self.assertFalse(system[label])
        self.assertGreaterEqual(sum(sum(s["candidate_records_by_type"].values())
                                   for s in self.report["systems"].values()),
                                len(self.report["records"]) -
                                self.report["unrouted_cross_cutting_records"])

    def test_scope_and_policy_fail_closed_when_new_domain_added(self):
        p=copy.deepcopy(self.policy)
        p["domain_context_defaults"].pop("corrections")
        with self.assertRaisesRegex(ValueError,"Dataset domain"):
            check_policy(p,self.method,self.datasets)
        p=copy.deepcopy(self.policy)
        p["match_rules"].pop("cooling_heat")
        with self.assertRaisesRegex(ValueError,"exact 16"):
            check_policy(p,self.method,self.datasets)
        p=copy.deepcopy(self.policy)
        p["match_rules"]["fuel_emissions_exhaust"]=["[bad"]
        with self.assertRaisesRegex(ValueError,"Invalid route"):
            check_policy(p,self.method,self.datasets)

    def test_source_id_aliases_are_context_only_not_new_faults(self):
        fa=self.by_id["corrections-issue-006"]
        self.assertIn("hcdiag-issue-003",
                      fa["same_source_document_issue_ids_navigation_only"])
        self.assertFalse(fa["source_overlap_proves_same_root_cause"])
        self.assertEqual(self.by_id["tier-fact-001"]["kind"],"facts")
        self.assertFalse(self.by_id["tier-fact-001"]["eligible_for_model_rating_from_this_index"])

if __name__=="__main__":
    unittest.main()
