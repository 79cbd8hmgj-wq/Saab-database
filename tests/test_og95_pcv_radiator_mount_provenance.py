"""Factory/campaign/merchant provenance on OG9-5 PCV, radiator and mounts."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from database import load_datasets, validate_datasets, filter_records

class OG95PCVRadiatorMountProvenanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.datasets=load_datasets()
        cls.d=next(x for x in cls.datasets if x["domain"]=="og95_pcv_radiator_mount_provenance")

    def fact(self,predicate):
        rows=[r for r in self.d["facts"] if r["predicate"]==predicate]
        self.assertEqual(len(rows),1,predicate)
        return rows[0]

    def test_integrity_counts_and_sources(self):
        self.assertEqual(validate_datasets(self.datasets),[])
        self.assertEqual(tuple(len(self.d[k]) for k in
            ("sources","facts","issues","parts","gaps")),(16,31,3,8,9))
        self.assertTrue(all(s["retrieval"]=="full_text" for s in self.d["sources"]))

    def test_csp_cannot_be_applied_to_all_range(self):
        a=self.fact("csp15433_scope")["value"]
        b=self.fact("csp15435_scope")["value"]
        self.assertEqual(a["transmission"],"manual")
        self.assertNotEqual(a["vin_range_inclusive"][1],b["vin_range_inclusive"][1])
        self.assertTrue(a["not_all_in_range"])
        self.assertTrue(b["not_all_in_range"])
        self.assertEqual(self.fact("csp15433_oil_trap_part")["value"],"55 558 696")
        self.assertEqual(self.fact("csp15435_market")["value"],"all markets")

    def test_early_engine_case_stays_inside_15433(self):
        x=self.fact("csp15433_early_engine_hose")
        self.assertEqual(x["value"]["hose"],"59 61 610")
        self.assertEqual(x["applicability"]["transmission_codes"],["manual"])
        self.assertTrue(any("US/CA" in r["notes"] for r in self.d["facts"]))

    def test_radiator_manual_and_auto_parts_are_not_interchanged(self):
        expected={"5193370":"manual","5193388":"automatic","32019619":"manual","32019620":"automatic"}
        for p in self.d["parts"]:
            self.assertEqual(p["evidence_status"],"supplier_claim")
            self.assertEqual(p["review_status"],"needs_vehicle_verification")
            self.assertEqual(p["relationships"],[])
            if p["part_number"] in expected:
                self.assertEqual(p["applicability"]["transmission_codes"],[expected[p["part_number"]]])
        self.assertEqual(self.fact("retailer_radiator_gearbox_split")["evidence_status"],"supplier_claim")
        self.assertEqual(self.fact("automatic_radiator_transmission_cooler_lines")["applicability"]["transmission_codes"],["automatic"])

    def test_mount_torque_boundary_is_not_part_swap(self):
        left=self.fact("left_mount_centre_nut_vin_cutover")["value"]
        arm=self.fact("front_torque_arm_vin_cutover")["value"]
        self.assertEqual((left["up_to_inclusive"],left["from_inclusive"]),("73514478","73514479"))
        self.assertEqual((left["torque_up_to_Nm"],left["torque_from_Nm"]),(84,74))
        self.assertEqual((arm["bracket_screws_before_Nm"],arm["bracket_screws_after_Nm"]),(47,38))
        self.assertIn("NOT",self.d["issues"][2]["limits"][0])
        self.assertEqual(self.fact("left_mount_manual_vs_auto_fasteners")["value"]["automatic_Nm"],84)

    def test_unsafe_misapplication_prohibited(self):
        x=self.fact("V6_engine_mount_category_caution")
        self.assertEqual(x["evidence_status"],"supplier_claim")
        self.assertEqual(x["value"]["listed_variant"],"B308E")
        self.assertIn("DO NOT",x["notes"])
        no_2009_csp={r["id"] for r in filter_records(self.datasets,platform="9-5-9600",year=2009)}
        self.assertNotIn(self.fact("csp15433_scope")["id"],no_2009_csp)
        self.assertFalse(self.d["parts"][0]["relationships"])

if __name__=="__main__":
    unittest.main()
