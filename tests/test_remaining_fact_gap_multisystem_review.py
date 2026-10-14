"""Review the last source-scoped multiple-system fact/gap assignments without rewriting technical evidence."""
from __future__ import annotations

import copy
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from database import load_datasets
from build_system_evidence_index import build, check_policy


def read(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


class RemainingSystemReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.datasets=load_datasets()
        cls.policy=read("data/audits/system-evidence-routing-policy-20261014.json")
        cls.method=read("data/tier-research/methodology.json")
        cls.index=build(cls.datasets,cls.policy,cls.method,
                        read("data/audits/legacy-issue-taxonomy-20261014.json"),
                        read("data/tier-research/observations.json"),
                        read("data/phase0-coverage-snapshot.json"))
        cls.rows={r["id"]:r for r in cls.index["records"]}

    def test_all_176_facts_and_49_open_gaps_added_to_original_review_register(self):
        registry=self.policy["explicit_fact_gap_routes"]
        facts=sum(x["kind"]=="facts" for x in registry.values())
        gaps=sum(x["kind"]=="gaps" for x in registry.values())
        self.assertEqual((facts,gaps),(337,80))
        self.assertEqual(len(registry),417)
        self.assertEqual(self.index["reviewed_fact_gap_navigation_routes"],{"facts":337,"gaps":80})
        self.assertEqual(self.index["remaining_unreviewed_ambiguous_record_count"],0)
        self.assertEqual(self.index["input_technical_counts"],
                         {"facts":1107,"issues":92,"parts":89,"gaps":284})
        for id_,decision in registry.items():
            original=self.rows[id_]
            self.assertEqual(original["kind"],decision["kind"])
            self.assertEqual(original["system_ids_for_discovery"],decision["system_ids"])
            self.assertTrue(decision["original_record_sha256"])
            self.assertTrue(decision["reason"])
            self.assertEqual(original["routing_basis"],
                             "curated_explicit_fact_gap_navigation")
            self.assertFalse(original["eligible_for_model_rating_from_this_index"])
            if decision["kind"]=="gaps":
                self.assertFalse(original["resolved_by_this_index"])

    def test_incidental_model_engine_codes_not_crosscounted_as_failures(self):
        expected={
            "afdiag-fact-001":["turbo_intake_boost"],
            "b235rev-fact-025":["engine_core_oil_pcv"],
            "ng93-fact-043":["cooling_heat"],
            "ng93-fact-039":["brakes_hydraulics"],
            "og95-fact-065":[],
            "og95t7-fact-024":["ecu_immobilizer_security"],
            "gate5-gap-003":["ecu_immobilizer_security"],
            "rrtriage-gap-007":["transmission_driveline"],
            "og95years-gap-006":[],
            "simulation-gap-002":[],
        }
        for id_,systems in expected.items():
            row=self.rows[id_]
            self.assertEqual(row["system_ids_for_discovery"],systems,id_)
        self.assertTrue(self.rows["og95-fact-065"]["cross_cutting_or_unresolved_system"])
        self.assertFalse(self.rows["og95-fact-065"]["eligible_for_model_rating_from_this_index"])

    def test_real_component_interfaces_remain_multisystem(self):
        expected={
            "hcdiag-fact-029":{"cooling_heat","transmission_driveline"},
            "maint-fact-044":{"cooling_heat","transmission_driveline"},
            "afdiag-fact-005":{"transmission_driveline","charging_starting_wiring"},
            "og95t7-fact-003":{"ecu_immobilizer_security","charging_starting_wiring"},
            "og95wire-fact-021":{"cooling_heat","charging_starting_wiring"},
            "ng93structure-fact-027":{"body_corrosion_mounts","charging_starting_wiring","restraints_safety"},
            "early9three-fact-016":{"brakes_hydraulics","fuel_emissions_exhaust"},
            "parts95-gap-008":{"cooling_heat","body_corrosion_mounts","engine_core_oil_pcv"},
            "simulation-gap-003":{"engine_core_oil_pcv","fuel_emissions_exhaust"},
        }
        for id_,systems in expected.items():
            row=self.rows[id_]
            self.assertEqual(set(row["system_ids_for_discovery"]),systems,id_)
            self.assertTrue(row["possible_multiple_systems"],id_)
            self.assertFalse(row["eligible_for_model_rating_from_this_index"])

    def test_source_digest_blocks_stale_interpretations(self):
        datasets=copy.deepcopy(self.datasets)
        record=next(x for d in datasets for x in d["gaps"]
                    if x["id"]=="parts95-gap-008")
        record["missing_inputs"].append("Unsupported new assertion")
        with self.assertRaisesRegex(ValueError,"Stale fact/gap navigation review"):
            check_policy(self.policy,self.method,datasets)

    def test_no_remaining_hidden_review_queue(self):
        result=subprocess.run(
            [sys.executable,"tools/build_system_evidence_index.py",
             "--review","--review-unreviewed-only","--review-limit","0"],
            cwd=ROOT,text=True,capture_output=True,check=True)
        data=json.loads(result.stdout)
        self.assertEqual(data["review_candidates_total"],0)
        self.assertEqual(data["review_records"],[])
        self.assertFalse(data["truncated"])

    def test_original_claim_context_option_does_not_assert_factory_proof(self):
        result=subprocess.run(
            [sys.executable,"tools/build_system_evidence_index.py",
             "--review","--review-kind","facts","--review-limit","2",
             "--review-context"],
            cwd=ROOT,text=True,capture_output=True,check=True)
        data=json.loads(result.stdout)
        self.assertEqual(data["review_records_printed"],2)
        self.assertTrue(all("original_record_sha256" in x and "record_context" in x
                            for x in data["review_records"]))
        self.assertTrue(data["truncated"])


if __name__=="__main__":
    unittest.main()
