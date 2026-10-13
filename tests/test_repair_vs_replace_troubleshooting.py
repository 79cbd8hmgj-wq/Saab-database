"""Factory source-scoped repair-vs-replace distinctions for Saab original 9-5."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from database import load_datasets, validate_datasets, filter_records

class RepairVsReplaceTriageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.datasets=load_datasets()
        cls.d=next(x for x in cls.datasets if x["domain"]=="repair_vs_replace_troubleshooting")

    def f(self,predicate):
        rs=[x for x in self.d["facts"] if x["predicate"]==predicate]
        self.assertEqual(len(rs),1,predicate)
        return rs[0]

    def test_source_scoped_and_counts(self):
        self.assertEqual(validate_datasets(self.datasets),[])
        self.assertEqual(tuple(len(self.d[k]) for k in
            ("sources","facts","issues","parts","gaps")),(17,31,4,0,9))
        self.assertEqual(sum(s["retrieval"]=="search_excerpt" for s in self.d["sources"]),2)
        self.assertTrue(all(x["evidence_status"]=="documented" for x in self.d["facts"]))

    def test_turbo_activation_not_actual_maximum_boost(self):
        gt=self.f("B205E_B235E_basic_actuator_start_bar")
        b235=self.f("B235R_basic_actuator_start_bar")
        self.assertEqual((gt["value"],b235["value"]),(0.4,0.45))
        self.assertEqual(b235["applicability"]["engine_codes"],["B235R"])
        self.assertEqual(gt["applicability"]["engine_codes"],["B205E","B235E"])
        self.assertIn("not",gt["notes"].lower())
        self.assertEqual(self.f("charge_air_pressure_test_at_1_bar")["applicability"]["model_years"],[2005])
        self.assertIn("P1105",self.f("underboost_rattle_wastegate_clip")["value"]["symptoms"][-1])

    def test_early_gearbox_bulletin_does_not_cover_2007(self):
        x=self.f("440_2497_affected_years")
        self.assertEqual(x["applicability"]["model_years"],[2002,2003,2004])
        self.assertEqual(self.f("440_2497_P_D_N_D_valve_housing")["applicability"]["model_years"],[2002,2003])
        later={r["id"] for r in filter_records(self.datasets,platform="9-5-9600",year=2007)}
        self.assertNotIn(x["id"],later)
        self.assertNotIn(self.f("440_2497_2003_2004_gearbox_exception")["id"],later)

    def test_2007_dipstick_variants_preserved(self):
        for p in ("2007_fa57_with_dipstick_80C","2007_fa57_without_dipstick_80C"):
            self.assertEqual(self.f(p)["value"]["TCM_fluid_C"],80)
            self.assertEqual(self.f(p)["value"]["MIN_MAX_delta_L"],0.5)
        self.assertEqual(self.f("2007_fa57_without_dipstick_80C")["value"]["tool"],"DT-47653")
        self.assertEqual(self.f("2005_fa57_full_capacity")["value"],7)
        self.assertEqual(self.f("2005_fa57_original_ATF")["value"]["name"],"Saab 3309")
        self.assertIn("converter",self.f("2005_fa57_full_capacity")["notes"])

    def test_electrical_DTC_not_assumed_mechanical(self):
        self.assertEqual(self.f("2007_fa57_P0748_solenoid_circuit")["value"]["code"],"P0748")
        self.assertEqual(self.f("2007_fa57_P0722_output_signal")["value"]["code"],"P0722")
        self.assertEqual(self.f("2006_fa57_P0730_wrong_ratio")["applicability"]["model_years"],[2006])
        self.assertIn("solenoid",self.f("2006_fa57_P0730_wrong_ratio")["notes"])

    def test_overheat_distinction_and_no_part_swaps(self):
        self.assertEqual(self.d["parts"],[])
        self.assertEqual(self.f("2008_cooling_temp_pressure_distinctions")["value"]["thermostat_open_C"],89)
        self.assertTrue(any("not" in r["limits"][0].lower() for r in self.d["issues"]))
        self.assertEqual(self.f("2007_replacement_fa57_contaminated_circuit_flush")["applicability"]["model_years"],[2007])

if __name__=="__main__":
    unittest.main()
