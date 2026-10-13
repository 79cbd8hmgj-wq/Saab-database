"""Saab 9-5 turbo oil and FA57 solenoid evidence, cross-year and source-scope guardrails."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from database import load_datasets, validate_datasets, filter_records

class TurboOilSolenoidTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.datasets=load_datasets()
        cls.d=next(x for x in cls.datasets if x["domain"]=="og95_turbo_oil_fa57_solenoid_provenance")

    def fact(self,name,year=None):
        vals=[x for x in self.d["facts"] if x["predicate"]==name and
            (year is None or x["applicability"]["model_years"]==[year])]
        self.assertEqual(len(vals),1,(name,year))
        return vals[0]

    def test_counts_and_source_validity(self):
        self.assertEqual(validate_datasets(self.datasets),[])
        self.assertEqual(tuple(len(self.d[k]) for k in
            ("sources","facts","issues","parts","gaps")),(15,27,3,0,9))
        self.assertEqual(sum(x["retrieval"]=="metadata_only" for x in self.d["sources"]),2)

    def test_turbo_oil_priming_only_2005_2006(self):
        for year in [2005,2006]:
            f=self.fact("turbo_bearing_housing_prime_before_start",year)
            self.assertEqual(f["value"]["fill_port"],"turbo oil inlet")
            self.assertEqual(f["applicability"]["engine_codes"],["4-cylinder petrol"])
        self.assertEqual(self.fact("turbo_oil_pipe_to_turbo_banjo_Nm")["value"],20)
        self.assertEqual(self.fact("turbo_oil_pipe_adapter_banjo_Nm")["value"],25)
        self.assertEqual(self.fact("turbo_oil_return_M6_bolts_Nm")["value"],14)

    def test_pressure_solenoid_not_gearshift_solenoid(self):
        vals=self.fact("S1_to_S5_resistance_20C_ohm")["value"]
        self.assertEqual({tuple(v) for v in vals.values()},{(11,16)})
        v=self.fact("SLS_SLT_2007_tech_table_ohm_range_20C")
        u=self.fact("SLS_SLT_2008_description_resistance_20C")
        self.assertEqual((v["value"]["min"],v["value"]["max"]),(5.0,5.6))
        self.assertEqual((u["value"]["min"],u["value"]["max"]),(5.1,5.5))
        self.assertEqual(v["applicability"]["model_years"],[2007])
        self.assertEqual(u["applicability"]["model_years"],[2008])

    def test_inverse_pressure_and_dtc_map(self):
        x=self.fact("SLS_SLT_inverse_current_pressure_logic")["value"]
        self.assertEqual(x["open_circuit_effect"],"maximum commanded hydraulic pressure")
        self.assertEqual(self.fact("SLS_SLT_DTC_distinctions")["value"]["P0785"],"SLS pressure regulation electrical current anomaly")
        self.assertEqual(self.fact("SLS_SLT_PWM_ground_and_pins")["value"]["frequency_Hz"],300)

    def test_TCM_specific_and_electrical_safe(self):
        f=self.fact("TCM_engine_specific_programming_required")
        self.assertEqual(f["applicability"]["model_years"],[2007])
        self.assertIn("B235E/R",f["value"]["variants"])
        self.assertIn("Never",self.fact("TCM_resistance_meter_safety")["value"])
        self.assertTrue(any("SPS" in s for s in self.fact("TCM_control_module_before_replacement_checks")["value"]))

    def test_misfiled_bulletin_not_recommended_for_9_5(self):
        f=self.fact("misfiled_100_2512_not_OG95")
        self.assertEqual(f["value"]["printed_cars_affected"],"Saab 9-3 M98-99 automatic")
        self.assertEqual(f["value"]["printed_fluid"],"Dexron III")
        self.assertIn("DO NOT",f["notes"])
        self.assertEqual(self.d["issues"][2]["applicability"]["model_years"],[2007])

    def test_no_invented_turbo_shaft_spec(self):
        for year in (2006,2008):
            f=self.fact("turbo_shaft_spec_%s_index_only" % year)
            self.assertIsNone(f["value"]["radial_mm"])
            self.assertIsNone(f["value"]["axial_mm"])
            self.assertEqual(f["value"]["document_retrieval"],"metadata_only")
        self.assertEqual(self.d["parts"],[])

if __name__ == "__main__":
    unittest.main()
