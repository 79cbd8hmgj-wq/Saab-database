"""Conservative MY2006/08 B235R oil/PCV sources; no unsupported extrapolation."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from database import load_datasets, validate_datasets, filter_records

class B235ROilAndPCVTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.datasets=load_datasets()
        cls.domain=next(x for x in cls.datasets if x["domain"]=="b235r_oil_pcv_2006_2008")
        cls.facts=cls.domain["facts"]

    def find(self, predicate):
        found=[x for x in self.facts if x["predicate"]==predicate]
        self.assertEqual(len(found),1,predicate)
        return found[0]

    def test_counts_and_provenance(self):
        self.assertEqual(validate_datasets(self.datasets),[])
        self.assertEqual(tuple(len(self.domain[k]) for k in
            ("sources","facts","issues","parts","gaps")),(17,31,2,7,9))
        self.assertEqual(self.domain["sources"][5]["retrieval"],"search_excerpt")
        self.assertEqual(self.domain["sources"][6]["retrieval"],"metadata_only")

    def test_2006_hot_pressure_is_not_inferred_2008(self):
        r=self.find("oil_pressure_minimum_test")
        self.assertEqual(r["applicability"]["model_years"],[2006])
        self.assertEqual(r["value"]["minimum_bar"],2.5)
        self.assertEqual(r["value"]["oil_temperature_C"],105)
        self.assertEqual(r["value"]["test_grade"],"10W-30")
        self.assertEqual(self.find("oil_warning_switch_band")["value"]["maximum"],0.55)
        self.assertFalse(any(x["predicate"]=="oil_pressure_minimum_test"
            and 2008 in x["applicability"].get("model_years",[]) for x in self.facts))
        self.assertTrue(any("MY2008" in gap["title"] for gap in self.domain["gaps"]))

    def test_2008_owner_market_is_not_unproven_engine_code(self):
        f=self.find("MY2008_USCA_2_3_turbo_change_fill")
        self.assertEqual(f["value"],4)
        self.assertEqual(f["applicability"]["markets"],["US","CA"])
        self.assertNotIn("engine_codes",f["applicability"])
        self.assertEqual(self.find("MY2008_USCA_short_trip_service_interval")["value"]["additional_interval_miles"],5000)

    def test_no_wrong_b235r_drain_plug_transfer(self):
        f=self.find("MY2008_B205E_B235E_service_page_scope")
        self.assertEqual(f["applicability"]["engine_codes"],["B205E","B235E"])
        self.assertIn("not B235R",f["value"])
        self.assertFalse(any(x["predicate"]=="oil_drain_plug_torque_for_B235R" for x in self.facts))

    def test_engine_code_and_special_sump(self):
        f=self.find("engine_version_code_letters")
        self.assertEqual(f["value"]["R"],"high-pressure turbo with charge air cooler stage 2")
        self.assertIn("Y062148-",self.find("MY2007_B235R_manual_sump_notched_boundary")["value"])
        t=self.find("MY2007_B235R_manual_sump_torque_references")["value"]
        self.assertEqual(t["sump_Nm"],22)
        self.assertEqual(t["gearbox_joint_Nm"],47)
        self.assertEqual(self.find("MY2008_B235R_manual_sump_dedicated_procedure")["applicability"]["transmission_codes"],["manual"])

    def test_parts_are_supplier_claims_without_approved_supersessions(self):
        self.assertEqual({p["part_number"] for p in self.domain["parts"]},
            {"55558696","32019651","55355330","5955927","5961610","55557709","213452433"})
        for p in self.domain["parts"]:
            self.assertEqual(p["evidence_status"],"supplier_claim")
            self.assertEqual(p["review_status"],"needs_vehicle_verification")
            self.assertEqual(p["relationships"],[])
        text=self.find("PCV_supplier_separator_conflicting_crossreference")["notes"]
        self.assertIn("Do not promote",text)

    def test_2006_year_scope_and_no_vehicle_condition_claim(self):
        ids_2005={x["id"] for x in filter_records(self.datasets,platform="9-5-9600",year=2005)}
        self.assertNotIn(self.find("oil_pressure_minimum_test")["id"],ids_2005)
        self.assertNotIn("2008",str(self.find("oil_pressure_minimum_test")["applicability"]["model_years"]))

if __name__ == "__main__":
    unittest.main()
