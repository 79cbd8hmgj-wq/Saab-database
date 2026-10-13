"""First Gate A/C identity worksheets distinguish exact original Saab assemblies."""
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT / "tools"))
from database import load_datasets, validate_datasets, filter_records

class PrioritySaabIdentityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.all=load_datasets()
        cls.d=next(d for d in cls.all if d["domain"]=="priority_vehicle_identity_gates")

    def f(self,predicate):
        xs=[f for f in self.d["facts"] if f["predicate"]==predicate]
        self.assertEqual(len(xs),1,predicate)
        return xs[0]

    def test_count_and_source_chain(self):
        self.assertEqual(validate_datasets(self.all),[])
        self.assertEqual(tuple(len(self.d[k]) for k in ("sources","facts","issues","parts","gaps")),(13,15,2,0,6))
        self.assertEqual(self.d["parts"],[])
        self.assertTrue(all(f["evidence_status"]=="documented" for f in self.d["facts"]))

    def test_2009_95_mirror_page_is_2010_not_2009_decoder(self):
        x=self.f("MY2009_WIS_VIN_table_is_2010")
        self.assertEqual(x["value"]["year_printed"],2010)
        self.assertEqual(x["applicability"]["model_years"],[2009])
        self.assertIn("cannot independently validate",x["notes"])
        self.assertIn("VIN",self.d["issues"][0]["title"])

    def test_2005_93_vin_cannot_be_used_as_2006(self):
        v=self.f("MY2005_9440_body_transmission_positions")
        self.assertEqual(v["applicability"]["model_years"],[2005])
        self.assertEqual(v["value"]["position_7"]["1"],"6-speed automatic")
        self.assertEqual(v["value"]["position_7"]["9"],"5-speed automatic")
        matches=filter_records(self.all,platform="9-3-9440",year=2006)
        self.assertNotIn(v["id"],{r["id"] for r in matches})

    def test_2006_93_fa57_af40_and_f40_never_collapsed(self):
        five=self.f("MY2006_9440_FA57_B207_engine_adaptation")["value"]
        six=self.f("MY2006_9440_AF40_type_independent_of_FA57")["value"]
        m=self.f("MY2006_9440_6MT_F40_distinct_family")["value"]
        self.assertIn("FA57",five["gearbox"])
        self.assertIn("AF40",six["gearbox"])
        self.assertEqual(m["gearbox"],"F40 manual six speed")
        self.assertEqual(m["dry_volume_L"],2.4)
        self.assertEqual(m["replacement_volume_L"],2.2)
        self.assertEqual(self.f("MY2006_9440_AF40_AW1_separate_fluid")["value"]["factory_fluid"],
                         "AW-1 or Saab 93 165 147")

    def test_suspension_codes_are_not_sided_part_approval(self):
        a=self.f("MY2005_suspension_assembly_code_plate")["value"]
        b=self.f("MY2006_suspension_plate_uses_EPC_and_side")["value"]
        self.assertEqual(len(a["positions"]),6)
        self.assertEqual(a["select_parts_from"],"Saab EPC")
        self.assertIn("different part numbers",b["front_strut_note"])

    def test_no_VIN_approved_replacement_claim(self):
        epc=self.f("WebEPC_VIN_OE_SUPERSESSION_gate")["value"]
        self.assertFalse(epc["actual_cars_queried"])
        self.assertTrue(any("VIN" in g["title"] for g in self.d["gaps"]))
        self.assertEqual(len(self.d["parts"]),0)

if __name__=="__main__":
    unittest.main()
