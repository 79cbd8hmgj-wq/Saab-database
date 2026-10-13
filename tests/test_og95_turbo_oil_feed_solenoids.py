"""Year-scoped Saab 9-5 turbo lubrication and FA57 solenoid separation."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1] / "tools"))
from database import load_datasets, validate_datasets, filter_records

class OG95TurboAndSolenoidTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.datasets=load_datasets()
        cls.d=next(x for x in cls.datasets if x["domain"]=="og95_turbo_oil_feed_solenoids")
    def fact(self,predicate,year):
        found=[x for x in self.d["facts"] if x["predicate"]==predicate and x["applicability"].get("model_years")==[year]]
        self.assertEqual(len(found),1,(predicate,year))
        return found[0]
    def test_schema_source_counts(self):
        self.assertEqual(validate_datasets(self.datasets),[])
        self.assertEqual(tuple(len(self.d[k]) for k in ("sources","facts","issues","parts","gaps")),(14,39,3,0,9))
        self.assertEqual([s["retrieval"] for s in self.d["sources"][-3:]],["metadata_only","full_text","search_excerpt"])
    def test_turbo_yearly_installation_pre_oil_and_lines(self):
        for year in (2005,2006,2008):
            v=self.fact("turbo_bearing_pre_oil_before_start",year)
            self.assertIn("bearing",v["value"]["oil_fill"])
            self.assertEqual(v["applicability"]["engine_codes"],["4-cylinder petrol"])
            oil=self.fact("turbo_oil_inlet_seal_renewal",year)["value"]
            self.assertEqual(oil["turbo_banjo_Nm"],20)
            self.assertEqual(oil["oil_filter_adapter_Nm"],25)
            self.assertEqual(self.fact("turbo_oil_return_joint_spec",year)["value"]["turbo_M6_Nm"],14)
            self.assertEqual(self.fact("turbo_front_exhaust_bellows_protection",year)["value"]["max_from_neutral_deg"],5)
    def test_2008_extra_fastener_is_engine_number_not_vin(self):
        row=self.fact("MY2008_heatshield_nut_engine_serial_torque",2008)["value"]
        self.assertEqual((row["through_engine_no"],row["from_engine_no"]),(7011078,7011079))
        self.assertEqual((row["torque_through_Nm"],row["torque_from_Nm"]),(20,21))
    def test_shift_valve_vs_pressure_valve_no_mixing(self):
        for year in (2007,2008,2009):
            shift=self.fact("FA57_S1_S5_shift_coil_20C_ohm",year)["value"]
            self.assertEqual(shift["S1"],[11,16])
            self.assertEqual(shift["S5"],[11,16])
            state=self.fact("FA57_S1_S5_zero_current_state",year)["value"]
            self.assertEqual(state["open"],["S1","S2","S4"])
            self.assertEqual(state["closed"],["S3","S5"])
        self.assertEqual(self.fact("MY2008_FA57_SLT_SLS_20C_descriptive_ohm",2008)["value"]["SLS"],[5.1,5.5])
        self.assertEqual(self.fact("MY2007_FA57_SLT_SLS_20C_data_ohm",2007)["value"]["SLS"],[5.0,5.6])
    def test_pressure_open_circuit_and_tcm_pins(self):
        f=self.fact("MY2008_FA57_SLT_SLS_lose_drive_effect",2008)["value"]
        self.assertEqual(f["open_circuit"],"maximum hydraulic system pressure")
        self.assertEqual(f["SLT_DTC"],"P0748")
        self.assertEqual(f["SLS_DTC"],"P0785")
        b=self.fact("MY2008_FA57_SLT_SLS_drive_wiring",2008)["value"]
        self.assertEqual(b["PWM_Hz"],300)
        self.assertEqual(b["SLT_signal_TCM_B_pin"],35)
    def test_early_bulletins_restricted_and_oil_grade_not_transferred(self):
        a=self.fact("bulletin_4402181_wrong_platform_for_9_5",1998)
        self.assertEqual(a["applicability"]["platforms"],["9-3-9400"])
        b=self.fact("bulletin_4402182_original_9_5_scope",1998)
        self.assertEqual(b["applicability"]["model_years"],[1998,1999])
        self.assertEqual(b["applicability"]["markets"],["non-US/CA"])
        self.assertIn("Saab 3309",b["notes"])
        records={r["id"] for r in filter_records(self.datasets,platform="9-5-9600",year=2008)}
        self.assertNotIn(b["id"],records)
        self.assertNotIn(a["id"],records)
    def test_no_numeric_turbo_shaft_play_claim(self):
        v=self.fact("MY2008_turbo_shaft_numeric_unknown",2008)["value"]
        self.assertIsNone(v["shaft_axial_max_mm"])
        self.assertIsNone(v["shaft_radial_max_mm"])
        self.assertTrue(any("shaft" in gap["title"].lower() for gap in self.d["gaps"]))

if __name__=="__main__":
    unittest.main()
