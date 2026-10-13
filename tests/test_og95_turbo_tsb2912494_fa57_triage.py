"""Factory bulletin date/shaft-play ambiguity and FA57 year-scoped triage."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from database import load_datasets, validate_datasets, filter_records

class SaabTurboBulletinFa57Triage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.all=load_datasets()
        cls.ds=next(d for d in cls.all if d["domain"]=="og95_turbo_tsb_2912494_fa57_triage")

    def find(self, pred, year=None):
        a=[f for f in self.ds["facts"] if f["predicate"]==pred and
           (year is None or f["applicability"].get("model_years")==[year])]
        self.assertEqual(len(a),1,(pred,year))
        return a[0]

    def test_records_and_sources_validate(self):
        self.assertEqual(validate_datasets(self.all),[])
        self.assertEqual([len(self.ds[k]) for k in ("sources","facts","issues","parts","gaps")],
                         [13,31,3,0,9])
        self.assertEqual(sum(s["retrieval"]=="metadata_only" for s in self.ds["sources"]),2)

    def test_bulletin_publication_date_not_mirrored_1998_directory(self):
        f=self.find("turbo_tsb_2912494_header")
        self.assertEqual(f["value"]["published"],"2004-11")
        self.assertEqual(f["value"]["market"],"all")
        self.assertNotIn("model_years",f["applicability"])
        self.assertEqual(f["applicability"]["platforms"],["9-5-9600"])

    def test_ambiguous_turbo_play_not_approved_numeric_limit(self):
        shaft=self.find("turbo_tsb_shaft_wording_not_dimensional_spec")["value"]
        self.assertTrue(shaft["internally_inconsistent_axes"])
        self.assertFalse(shaft["calibrated_tolerance_verified"])
        self.assertIsNone(shaft["usable_numeric_axial_mm"])
        self.assertIsNone(shaft["usable_numeric_radial_mm"])
        self.assertIn("DO NOT",self.find("turbo_tsb_shaft_wording_not_dimensional_spec")["notes"])
        missing=self.find("turbo_2006_and_2008_shaft_page_only")["value"]
        self.assertFalse(missing["MY2006_numeric_verified"])
        self.assertFalse(missing["MY2008_numeric_verified"])

    def test_vacuum_with_and_without_pump_not_equivalent(self):
        x=self.find("turbo_tsb_vacuum_circuit_divergent_tests")["value"]
        self.assertEqual(x["with_vacuum_pump"]["min_vacuum_bar"],0.7)
        self.assertEqual(x["without_vacuum_pump"]["min_vacuum_bar"],0.4)

    def test_adaptation_is_after_service_never_stall_warming(self):
        for year in (2005,2009):
            a=self.find("fa57_adaptation_trigger",year)["value"]
            self.assertIn("TCM software replaced/updated",a)
            self.assertEqual(self.find("fa57_adaptation_working_temp_C",year)["value"],{"minimum":65,"maximum":110})
            self.assertIs(self.find("fa57_adaptation_no_stall_heating",year)["value"],True)
        self.assertEqual(self.find("fa57_2008_no_dipstick_level_condition")["value"]["TCM_ATF_temperature_C"],80)

    def test_missing_sensor_is_not_ratio_slip(self):
        self.assertEqual(self.find("fa57_2005_P0717_condition")["value"]["dtc"],"P0717")
        self.assertEqual(self.find("fa57_2005_P0717_condition")["value"]["fallback"],"TCM estimates input speed from output shaft signal")
        self.assertEqual(self.find("fa57_2009_P0735_ratio_error")["value"]["ratio_deviation_more_than_percent"],20)
        self.assertEqual(self.find("fa57_2009_P0735_ratio_error")["applicability"]["model_years"],[2009])

    def test_high_load_stall_not_diy(self):
        x=self.find("fa57_2006_stall_test_listed_but_unsafe")
        self.assertEqual(x["value"]["max_seconds"],5)
        self.assertIn("NEVER",x["notes"])
        self.assertNotIn(x["id"], {r["id"] for r in filter_records(
            self.all,platform="9-5-9600",year=2008)})

    def test_TC_specific_code_and_DPS(self):
        tcm=self.find("fa57_2007_engine_specific_TCM")["value"]
        self.assertEqual(tcm["programming"],"engine-specific by Tech 2/SPS")
        self.assertEqual(self.find("fa57_2007_DPS_conditions")["value"]["vehicle_speed_below_kmh"],80)
        self.assertEqual(self.find("fa57_2007_DPS_conditions")["value"]["front_right_vs_TCM_output_difference_exceeds_kmh"],15)

if __name__=="__main__":
    unittest.main()
