"""US Saab VIN/tool/cost readiness evidence and crosswalk regression tests."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from build_us_parts_tool_readiness import build, PROD, PLAN, OUT


class USPartsToolReadinessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.prod = json.loads(PROD.read_text(encoding="utf-8"))
        cls.plans = json.loads(PLAN.read_text(encoding="utf-8"))
        cls.cover = json.loads(OUT.read_text(encoding="utf-8"))

    def test_reproducible_110_groups_and_year_specific_provenance(self):
        self.assertEqual(build(self.prod, self.plans), self.cover)
        self.assertEqual(self.cover["denominator_source_compiled_us_automatic_fwd_groups"], 110)
        self.assertEqual(len(self.cover["production_groups"]), 110)
        self.assertEqual(len(self.plans["job_packets"]), 8)
        self.assertEqual(len(self.plans["source_records"]), 11)
        self.assertEqual(len({x["id"] for x in self.plans["source_records"]}), 11)
        self.assertEqual(
            [j["matching_production_configuration_groups"]
             for j in self.cover["job_coverage"]],
            [22, 42, 28, 28, 6, 4, 1, 4]
        )
        self.assertEqual(
            [j["matching_model_year_source_examples"]
             for j in self.cover["job_coverage"]],
            [7, 4, 2, 2, 2, 4, 1, 4]
        )
        self.assertEqual(sum(bool(r["job_readiness_leads"]) for r in
                             self.cover["production_groups"]), 99)
        ids = {x["id"] for x in self.prod["configurations"]}
        self.assertEqual({r["production_configuration_id"] for r
                          in self.cover["production_groups"]}, ids)

    def test_no_vehicle_or_part_approval_from_group_match(self):
        self.assertTrue(self.cover["no_parts_fitment_approved"])
        self.assertTrue(self.cover["no_actual_vehicle_verified"])
        self.assertTrue(self.cover["no_installed_repair_prices"])
        for r in self.cover["production_groups"]:
            self.assertFalse(r["actual_vehicle_inspected"])
            self.assertFalse(r["repair_authorized"])
            for lead in r["job_readiness_leads"]:
                self.assertIn(lead["source_applicability_state"], (
                    "source_model_year_matched_still_VIN_unverified",
                    "adjacent_year_research_lead_not_repair_approval",
                ))
                self.assertFalse(lead["vin_and_part_fitment_confirmed"])
                self.assertFalse(lead["special_tool_access_confirmed"])
                self.assertFalse(lead["shop_quote_obtained"])
                packet = next(x for x in self.plans["job_packets"]
                              if x["id"] == lead["job_id"])
                self.assertEqual(
                    lead["source_applicability_state"] ==
                    "source_model_year_matched_still_VIN_unverified",
                    r["model_year"] == packet["factory_example_year"])

    def test_no_unsupported_donor_interchange_or_exact_price(self):
        self.assertFalse(any(self.plans["guardrails"].values()))
        for p in self.plans["job_packets"]:
            self.assertIsNone(p["estimate_usd"])
            self.assertIsNone(p["required_shop_labor_hours"])
            self.assertTrue(p["inspection_evidence"])
            self.assertTrue(p["required_tools_or_capabilities"])
            self.assertTrue(p["vin_rpo_case_gates"])
        byid = {p["id"]: p for p in self.plans["job_packets"]}
        self.assertIn("not drop-in proof",
                      byid["part-ready-002"]["source_specific_fact"])
        self.assertIn("does not approve 9-3 AF40 donor interchange",
                      " ".join(byid["part-ready-007"]["vin_rpo_case_gates"]))
        self.assertIn("73514478/73514479",
                      byid["part-ready-006"]["source_specific_fact"])
        self.assertIn("83 94 850",
                      " ".join(byid["part-ready-006"]["required_tools_or_capabilities"]))

    def test_historical_retail_price_is_not_a_live_quote(self):
        p = next(x for x in self.plans["job_packets"] if x["id"] == "part-ready-008")
        self.assertEqual(p["candidate_parts_or_numbers"], ["32019620"])
        self.assertEqual(p["historical_advertised_part_price_usd"], 211.98)
        self.assertEqual(p["historical_observed_date"], "2026-10-13")
        self.assertEqual(p["retail_source_ids"], ["usparts-src-004"])
        retail = json.loads((ROOT / "data/datasets/us-retail-parts-supply-snapshot.json")
                            .read_text(encoding="utf-8"))
        matching = next(x for x in retail["sources"] if x["id"] == "usparts-src-004")
        self.assertIn("32019620", matching["url"])
        self.assertIsNone(p["estimate_usd"])
        self.assertTrue(all(z["current_install_cost_quotes"] == 0
                            for z in self.cover["job_coverage"]))

    def test_unknown_vin_case_and_quote_are_rejected(self):
        bad = json.loads(json.dumps(self.plans))
        bad["guardrails"]["oem_replacement_part_fitment_approved"] = True
        with self.assertRaises(ValueError):
            build(self.prod, bad)
        bad = json.loads(json.dumps(self.plans))
        bad["job_packets"][0]["estimate_usd"] = 1500
        with self.assertRaises(ValueError):
            build(self.prod, bad)
        bad = json.loads(json.dumps(self.plans))
        bad["job_packets"][0]["evidence_source_ids"] = [
            "ready-wis-9650-2011-af40"]
        with self.assertRaises(ValueError):
            build(self.prod, bad)

if __name__ == "__main__":
    unittest.main()
