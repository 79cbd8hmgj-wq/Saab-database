"""Phase 0 nonrunning inspection protocol keeps market and safety limits explicit."""
import json
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"tools"))
from database import load_datasets,validate_datasets,filter_records

class NonrunningPurchaseGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.all=load_datasets()
        cls.d=next(x for x in cls.all if x["domain"]=="priority_nonrunning_purchase_screen")
        cls.sheet=json.loads((ROOT/"data"/"inspection-templates"/"nonrunning-phase0.json").read_text())

    def fact(self,pred):
        rows=[r for r in self.d["facts"] if r["predicate"]==pred]
        self.assertEqual(len(rows),1,pred)
        return rows[0]

    def test_record_structure(self):
        self.assertEqual(validate_datasets(self.all),[])
        self.assertEqual(tuple(len(self.d[k]) for k in ("sources","facts","issues","parts","gaps")),(13,20,4,0,8))
        self.assertEqual(self.d["parts"],[])
        self.assertEqual(sum(s["retrieval"]=="search_excerpt" for s in self.d["sources"]),3)

    def test_US_CA_is_sales_market_not_build_location(self):
        scope=self.sheet["market_scope"]
        self.assertEqual(scope["target_sales_markets"],["US","CA"])
        self.assertTrue(scope["manufacturing_country_is_not_market"])
        self.assertIn("not US/CA",scope["excluded_market_bulletin"])

    def test_nonUS_2004_bulletin_not_2008_US_approval(self):
        b=self.fact("nov2004_TSB2482506_market_scope")
        self.assertEqual(b["applicability"]["markets"],["non-US/CA"])
        self.assertNotIn("model_years",b["applicability"])
        self.assertEqual(b["value"]["date"],"2004-11")
        self.assertEqual(b["value"]["WIS_folder_year"],2008)
        self.assertFalse(self.fact("MY2007_enhanced_IDM_requires_software_feature")["value"]["current2026_access_verified"])

    def test_catalyst_pass_fail_cannot_be_assumed_on_nonrunner(self):
        q=self.fact("Tech2_quick_check_three_results")["value"]
        self.assertEqual(q["coolant_threshold_C"],60)
        self.assertIn("High back pressure",q["statuses"])
        self.assertEqual(self.fact("Tech2_indirect_backpressure_MAF_MAP")["value"]["method"],
                         "uses MAF and MAP values for backpressure estimation")
        self.assertIn("US/CA",self.d["issues"][0]["limits"][0])
        self.assertIn("RUNNING",self.d["issues"][0]["limits"][0])
        self.assertEqual(self.sheet["vehicle_results"],None)

    def test_2007_pressure_protocol_not_2005_or_diy(self):
        b=self.fact("MY2007_controlled_intake_test_limit")
        self.assertEqual(b["value"]["upper_pressure_bar"],0.6)
        self.assertEqual(b["applicability"]["model_years"],[2007])
        self.assertIn("not",b["notes"].lower())

    def test_engine_pressure_sender_not_mechanical_acceptance(self):
        p=self.fact("MY2009_oil_pressure_documented_test_only")["value"]
        self.assertEqual((p["rpm"],p["oil_temperature_C"],p["minimum_bar"]),(2000,105,2.5))
        sender=self.fact("MY2009_lamp_threshold_not_bearing_proof")["value"]
        self.assertEqual(sender["switch_on_below_bar_min"],0.3)
        self.assertLess(sender["switch_on_below_bar_max"],p["minimum_bar"])

    def test_B207_factory_minimum_is_compression_not_cold_start_guarantee(self):
        f=self.fact("MY2006_B207_compression_12_4_bar")
        self.assertEqual(f["applicability"]["platforms"],["9-3-9440"])
        self.assertEqual(f["applicability"]["model_years"],[2006])
        self.assertEqual(f["value"]["minimum_bar"],12.4)

    def test_template_requires_unknown_and_prohibits_invented_pass(self):
        self.assertEqual(self.sheet["template_version"],"1.0.0")
        self.assertIn("unknown",self.sheet["allowed_evidence_statuses"])
        self.assertNotIn("pass",self.sheet["allowed_evidence_statuses"])
        ids=[x["id"] for x in self.sheet["fields"]]
        self.assertEqual(len(ids),len(set(ids)))
        self.assertGreaterEqual(len(ids),12)
        self.assertTrue(all(x["default_status"]=="unknown" for x in self.sheet["fields"]))
        self.assertTrue(all(x["stage"] in ("A","B","C","D","E") for x in self.sheet["fields"]))
        self.assertTrue(all(x["requires"] for x in self.sheet["fields"]))
        self.assertTrue(all(x["stop_if"] is not None for x in self.sheet["fields"]))
        self.assertIn("no full-throttle transmission stall test",self.sheet["prohibited_shortcuts"])
        self.assertIn("no catalyst bypass/removal as a diagnostic shortcut",self.sheet["prohibited_shortcuts"])

if __name__=="__main__":
    unittest.main()
