"""Guard factory market and engine boundaries, ATF thermal protection and turbo shaft uncertainty."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from database import load_datasets, validate_datasets, filter_records

class ATFThermalAndTurboBulletinTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.datasets=load_datasets()
        cls.d=next(x for x in cls.datasets if x["domain"]=="og95_atf_thermal_turbo_bulletin")
        cls.correction=next(x for x in cls.datasets if x["domain"]=="repair_vs_replace_troubleshooting")
    def fact(self,pred):
        x=[r for r in self.d["facts"] if r["predicate"]==pred]
        self.assertEqual(len(x),1,pred)
        return x[0]
    def test_sources_counts_structure_and_retrieval(self):
        self.assertEqual(validate_datasets(self.datasets),[])
        self.assertEqual(tuple(len(self.d[k]) for k in
            ("sources","facts","issues","parts","gaps")),(14,28,3,2,9))
        self.assertEqual(sum(s["retrieval"]=="metadata_only" for s in self.d["sources"]),2)
        self.assertEqual(sum(s["retrieval"]=="search_excerpt" for s in self.d["sources"]),1)
    def test_original_wastegate_bulletin_is_not_US_B235R_or_2007_campaign(self):
        f=self.fact("291_2317_factory_scope")
        self.assertEqual(f["applicability"]["markets"],["non-US/CA"])
        self.assertEqual(f["applicability"]["engine_codes"],["B205E","B235E"])
        self.assertNotIn("model_years",f["applicability"])
        self.assertEqual(f["value"]["date"],"2002-01")
        self.assertEqual(self.fact("291_2317_factory_clip_o_ring")["value"]["clip"],"91 85 497")
        old=next(x for x in self.correction["facts"] if x["predicate"]=="underboost_rattle_wastegate_clip")
        self.assertEqual(old["applicability"]["markets"],["non-US/CA"])
        self.assertNotIn("B235R",old["applicability"]["engine_codes"])
        self.assertNotIn("model_years",old["applicability"])
        self.assertTrue(all(p["relationships"]==[] for p in self.d["parts"]))
        self.assertTrue(all(p["review_status"]=="needs_vehicle_verification" for p in self.d["parts"]))
    def test_temperature_DTC_and_protective_programs_distinct(self):
        x=self.fact("MY2008_atf_sensor_DTCs")["value"]
        self.assertEqual(set(x),{"P0711","P0712","P0713"})
        self.assertEqual(self.fact("MY2008_ATF_hot_program_1")["value"]["activation_C"],128)
        self.assertEqual(self.fact("MY2008_ATF_hot_program_2")["value"]["activation_C"],135)
        self.assertEqual(self.fact("MY2008_ATF_torque_limit")["value"]["threshold_C"],145)
        critical=self.fact("MY2008_ATF_P0218_trigger")
        self.assertEqual(critical["value"]["above_C"],155)
        self.assertEqual(critical["value"]["lasting_seconds_more_than"],10)
        self.assertEqual(critical["applicability"]["model_years"],[2008])
    def test_ATF_NTC_and_output_input_checks(self):
        self.assertEqual(self.fact("MY2008_atf_sensor_resistance_map")["value"]["at_C_80_ohms"],125)
        self.assertEqual(self.fact("MY2008_atf_NTC_wiring")["value"]["TCM_pin_positive"],"21B")
        self.assertEqual(self.fact("MY2008_P0705_range_switch")["applicability"]["model_years"],[2008])
        self.assertEqual(self.fact("MY2009_P0722_output_sensor")["applicability"]["model_years"],[2009])
        self.assertEqual(self.fact("MY2009_P0722_output_sensor")["value"]["condition"].count("200 rpm"),1)
        self.assertIn("requested_field",self.fact("MY2009_TCC_current_vs_requested_slip")["value"])
    def test_turbo_shaft_numeric_spec_remains_gap(self):
        f=self.fact("MY2008_turbo_shaft_data_index_unreadable")
        self.assertFalse(f["value"]["numeric_axial_radial_limits_recovered"])
        self.assertEqual(self.d["sources"][9]["retrieval"],"metadata_only")
        self.assertTrue(any("shaft" in g["title"].lower() for g in self.d["gaps"]))
    def test_no_Diy_stall_test_or_indiscriminate_reset(self):
        f=self.fact("MY2005_factory_stall_test_not_Diy")
        self.assertEqual(f["value"]["stall_max_seconds_in_table"],5)
        self.assertIn("NOT",f["notes"])
        x=self.fact("MY2006_TCMAfterReplacementReset")
        self.assertEqual(x["value"]["listed_triggers"],["gearbox replacement","throttle-housing replacement","TCM replacement"])
    def test_2009_banjo_torque_not_engine_oil_cooler(self):
        x=self.fact("MY2009_cooler_and_gearbox_banjo_torques")["value"]
        self.assertEqual((x["radiator_cooler_banjo_Nm"],x["gearbox_banjo_Nm"],x["gearbox_fluid_drain_plug_Nm"]),(27,24,40))
        self.assertEqual(self.fact("MY2008_T7_wastegate_PWM")["value"]["pwm_frequency_Hz"],32)
        self.assertEqual(self.fact("MY2008_T7_wastegate_PWM")["value"]["TCM_PIN"],"Trionic pin 13, not TCM")
if __name__ == "__main__":
    unittest.main()
