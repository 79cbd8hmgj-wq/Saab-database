"""Gate A structural inspection boundaries and official New York DMV criteria."""
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"tools"))
from database import load_datasets,validate_datasets,filter_records

class StructuralCorrosionGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.all=load_datasets()
        cls.d=next(d for d in cls.all if d["domain"]=="priority_structural_corrosion_inspection")

    def f(self,predicate):
        rows=[r for r in self.d["facts"] if r["predicate"]==predicate]
        self.assertEqual(len(rows),1,predicate)
        return rows[0]

    def test_source_integrity(self):
        self.assertEqual(validate_datasets(self.all),[])
        self.assertEqual([len(self.d[k]) for k in ("sources","facts","issues","parts","gaps")],
                         [14,21,3,0,8])
        self.assertTrue(all(f["evidence_status"]=="documented" for f in self.d["facts"]))

    def test_wagon_specific_2006_body_repair_not_2008_approval(self):
        x=self.f("wagon_rear_floor_approved_section_method")
        self.assertEqual(x["applicability"]["model_years"],[2006])
        self.assertEqual(x["applicability"]["body_styles"],["5D"])
        self.assertEqual(x["value"]["cut_from_crossmember_mm"],50)
        self.assertIn("NOT",x["notes"])
        self.assertNotIn(x["id"],{r["id"] for r in filter_records(
            self.all,platform="9-5-9600",year=2008)})
        self.assertTrue(any("MY2008" in g["title"] for g in self.d["gaps"]))

    def test_mount_nut_and_frame_are_not_interchange_approval(self):
        n=self.f("rear_subframe_mount_nut_floor_access")["value"]
        self.assertEqual(n["hole_saw_mm"],35)
        self.assertEqual(n["closing_plug_historic"],"43 33 498")
        s=self.f("rear_frame_member_partial_repair_cut_boundary")["value"]
        self.assertIn("illustrated marking",s)
        self.assertEqual(self.d["parts"],[])
        self.assertIn("not a procedure",self.f("rear_subframe_mount_nut_floor_access")["notes"])

    def test_lifting_forbidden_not_optional(self):
        self.assertEqual(self.f("OG95_rear_axle_spare_well_lifting_forbidden")["value"],
                         ["rear axle","spare wheel well"])
        self.assertIn("professional",self.f("OG95_rear_axle_spare_well_lifting_forbidden")["notes"])

    def test_CV_reinforcement_not_sedan(self):
        cv=self.f("NG93_convertible_extra_rear_chassis_reinforcement")
        self.assertEqual(cv["applicability"]["body_styles"],["CV"])
        self.assertEqual(cv["applicability"]["model_years"],[2006])
        self.assertIn("structural",self.f("NG93_CV_inner_sill_multiple_panels_reinforcement")["notes"])

    def test_NY_regulatory_scope_not_Saab_factory_corrosion_gauge(self):
        ny=self.f("NYS_chassis_frame_inspection_criteria")
        self.assertEqual(ny["applicability"]["markets"],["NY, USA"])
        self.assertIn("severe rust at suspension attachment points",ny["value"]["look_for"])
        self.assertIn("dripping or pooling",self.f("NYS_brake_fuel_inspection_criteria")["value"]["fuel"])
        self.assertEqual(self.d["sources"][11]["source_type"],"technical_reference")
        self.assertFalse(any("mm" in k for k in ny["value"]))

    def test_fuel_brake_line_route_required(self):
        x=self.f("NG93_B207_fuel_lines_brake_pipes_front_subframe_share_route")
        self.assertEqual(x["applicability"]["model_years"],[2006])
        self.assertEqual(x["applicability"]["engine_codes"],["B207"])
        self.assertTrue(any("fuel/brake" in g["title"].lower() for g in self.d["gaps"]))

if __name__=="__main__":
    unittest.main()
