"""Original 9-5 cooling-service year scope and separate oil-cooler VIN boundary."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from database import load_datasets, validate_datasets, filter_records

class OG95CoolingServiceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.datasets=load_datasets()
        cls.d=next(x for x in cls.datasets if x["domain"]=="og95_cooling_service_2006_2009")

    def fact(self,name,year=None):
        rows=[x for x in self.d["facts"] if x["predicate"]==name
              and (year is None or x["applicability"]["model_years"]==[year])]
        if year is None:
            self.assertEqual(len(rows),1,name)
        else:
            self.assertEqual(len(rows),1,(name,year))
        return rows[0]

    def test_source_integrity_and_counts(self):
        self.assertEqual(validate_datasets(self.datasets),[])
        self.assertEqual(tuple(len(self.d[k]) for k in
            ("sources","facts","issues","parts","gaps")),(15,30,3,0,9))
        self.assertTrue(all(x["retrieval"]=="full_text" for x in self.d["sources"]))

    def test_coolant_interval_only_independent_years(self):
        for year in (2007,2008):
            x=self.fact("maximum_coolant_change_interval_years",year)
            self.assertEqual(x["value"],3)
            self.assertEqual(self.fact("coolant_full_system_capacity_L",year)["value"],7.4)
            self.assertIn("4-cylinder petrol",x["applicability"]["engine_codes"])
        self.assertFalse(any(x["predicate"]=="maximum_coolant_change_interval_years"
            and 2009 in x["applicability"]["model_years"] for x in self.d["facts"]))

    def test_engine_oil_cooler_vin_cutover_distinct_from_mount(self):
        for year in (2006,2007):
            a=self.fact("oil_cooler_union_vin_torque",year)["value"]
            self.assertEqual((a["last_low_group_suffix"],a["first_high_group_suffix"]),
                             ("73514907","73514908"))
            self.assertEqual((a["low_group_torque_Nm"],a["high_group_torque_Nm"]),(10,8))
            b=self.fact("cooler_hose_joint_o_ring_handling",year)["value"]
            self.assertEqual(b["grease"],"Gleitmo 805")
            self.assertEqual(b["historical_grease_part"],"30 06 442")
        for year in (2005,2007):
            m=self.fact("mount_nut_2007chassis_vin_torque",year)["value"]
            self.assertEqual((m["last_84Nm_suffix"],m["first_74Nm_suffix"]),
                             ("73514478","73514479"))
        self.assertNotEqual(a["last_low_group_suffix"],m["last_84Nm_suffix"])

    def test_no_year_directory_implies_2005_change(self):
        x=self.fact("mount_nut_2007chassis_vin_torque",2005)
        self.assertIn("NOT proof of change in MY2005",x["notes"])
        self.assertIn("2006",self.fact("oil_cooler_union_vin_torque",2006)["notes"])
        self.assertEqual(self.d["issues"][1]["applicability"]["model_years"],[2005,2007])

    def test_transmission_cooler_and_engine_oil_cooler_separate(self):
        x=self.fact("cooling_diagram_auto_only_oil_cooler")["value"]
        self.assertEqual(x["label"],"Oil cooler (aut. only)")
        self.assertEqual(self.fact("automatic_radiator_line_service")["applicability"]["transmission_codes"],["automatic"])
        self.assertIn("separate from", self.fact("cooler_hose_joint_o_ring_handling",2006)["notes"].lower())

    def test_modern_fluid_and_no_2009_coolant_interval(self):
        x=self.fact("mixture_and_corrosion_guidance")
        self.assertEqual(x["value"]["freeze_protection_minimum_C"],-30)
        self.assertIn("2026",x["notes"])
        self.assertEqual(x["applicability"]["model_years"],[2009])

    def test_2008_thermostat_pressure_and_pump(self):
        self.assertEqual(self.fact("thermostat_regulated_open_temp")["value"]["nominal_C"],89)
        self.assertEqual(self.fact("coolant_pressure_relief_kPa")["value"]["max"],150)
        self.assertEqual(self.fact("thermostat_vent_and_housing_torque")["value"]["housing_Nm"],22)
        self.assertEqual(self.fact("fan_count_according_to_AC")["value"]["without_AC"],1)

if __name__=="__main__":
    unittest.main()
