"""Prevent unsafe Saab brake fastener and cross-platform hardware claims."""
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"tools"))
from database import load_datasets, validate_datasets, filter_records

class BrakeHydraulicGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.datasets=load_datasets()
        cls.d=next(x for x in cls.datasets if x["domain"]=="priority_brake_hydraulic_safety")

    def fact(self,predicate):
        rows=[x for x in self.d["facts"] if x["predicate"]==predicate]
        self.assertEqual(len(rows),1,predicate)
        return rows[0]

    def test_source_integrity(self):
        self.assertEqual(validate_datasets(self.datasets),[])
        self.assertEqual(tuple(len(self.d[k]) for k in ("sources","facts","issues","parts","gaps")),(19,25,4,0,8))
        self.assertEqual(self.d["parts"],[])
        self.assertTrue(any("torque" in g["title"] for g in self.d["gaps"]))

    def test_four_93_levels_are_complete_and_not_same_assemblies(self):
        levels=[self.fact(f"MY2006_NG93_level{n}_rotor_caliper_matrix")["value"]
                for n in range(1,5)]
        self.assertEqual([v["front_diameter_mm"] for v in levels],[285,302,314,302])
        self.assertEqual([v["rear_diameter_mm"] for v in levels],[278,292,292,278])
        self.assertEqual([v["front_caliper"] for v in levels],["FNG57","FNG60","FNRG60","FNG60"])
        self.assertEqual([v["rear_piston_mm"] for v in levels],[38,40,40,38])
        self.assertEqual(self.fact("MY2006_NG93_VINplate_brake_slots")["value"]["10"],
                         "rear caliper option")

    def test_95_front_bolt_4Nm_conflict_is_explicitly_blocked(self):
        v=self.fact("MY2008_OG95_front_carrier_unsafe_torque_conflict")["value"]
        self.assertEqual(v["disc_procedure_caliper_bolt_Nm"],4)
        self.assertEqual(v["dedicated_torque_table_caliper_bolt"],"140 Nm +45 degrees")
        self.assertEqual(v["dedicated_torque_table_rotor_lock_screw_Nm"],4)
        self.assertIn("SAFETY CONFLICT",v["status"])
        self.assertIn("Do not use 4 Nm",self.fact("MY2008_OG95_front_carrier_unsafe_torque_conflict")["notes"])

    def test_95_rotor_285_vs_288_conflict_remains_open(self):
        chart=self.fact("OG95_B1_B2_B3_printed_brake_configurations")["value"]
        detail=self.fact("MY2006_OG95_front_rotor_alt_standard")["value"]
        self.assertEqual(chart["B1"]["front_d_mm"],288)
        self.assertEqual(detail["standard_diameter_mm"],285)
        self.assertEqual(chart["B2"]["front_new_mm"],25)
        self.assertEqual(detail["heavy_new_thickness_mm"],28)
        self.assertTrue(any("B1/B2/B3" in g["title"] for g in self.d["gaps"]))

    def test_93_handbrake_not_95_shoes(self):
        ng=self.fact("MY2006_NG93_integrated_parking_caliper")
        og=self.fact("MY2006_OG95_park_shoes_first")["value"]
        self.assertEqual(ng["applicability"]["platforms"],["9-3-9440"])
        self.assertEqual(og["parking_brake_type"],"separate rear drum-in-hat shoes plus cables")
        self.assertIn("not OG9-5",ng["value"])

    def test_hose_and_carrier_are_different_fasteners(self):
        f=self.fact("MY2006_NG93_flex_hose_clearance_bleeding")["value"]
        self.assertEqual(f["hardline_connector_Nm"],15)
        self.assertEqual(f["hose_to_caliper_banjo_Nm"],40)
        self.assertTrue(f["requires_bleeding_and_leak_test"])
        rear=self.fact("MY2006_NG93_rear_carrier_fastener_vs_guide_pin")["value"]
        self.assertEqual(rear["guide_pins_Nm"],28)
        self.assertIn("130 Nm",rear["carrier_bolts"])

    def test_no_95_2009_omnibus_table_assumed_2006(self):
        f=self.fact("OG95_B1_B2_B3_printed_brake_configurations")
        self.assertEqual(f["applicability"]["model_years"],[2009])
        self.assertNotIn(f["id"],{r["id"] for r in filter_records(
            self.datasets,platform="9-5-9600",year=2006)})
        self.assertEqual(self.fact("MY2006_OG95_front_rotor_alt_standard")["applicability"]["model_years"],[2006])

if __name__=="__main__":
    unittest.main()
