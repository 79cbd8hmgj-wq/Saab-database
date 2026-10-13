"""Manufacturer original US year/VIN facts and conditional 9-3 service-kit scope."""
import json
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"tools"))
from database import load_datasets,validate_datasets,filter_records

class OriginalSaabUSManufacturerProvenanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.all=load_datasets()
        cls.d=next(x for x in cls.all if x["domain"]=="official_us_vin_and_service_kit_provenance")
        cls.template=json.loads((ROOT/"data"/"inspection-templates"/"oem-replacement-verification.json").read_text(encoding="utf-8"))

    def f(self,predicate):
        xs=[x for x in self.d["facts"] if x["predicate"]==predicate]
        self.assertEqual(len(xs),1,predicate)
        return xs[0]

    def test_all_scope_and_sources_and_counts(self):
        self.assertEqual(validate_datasets(self.all),[])
        self.assertEqual(tuple(len(self.d[k]) for k in ("sources","facts","issues","parts","gaps")),(7,15,3,2,6))
        self.assertTrue(all(x["evidence_status"]=="documented" for x in self.d["parts"]))
        self.assertTrue(all(x["review_status"]=="needs_vehicle_verification" for x in self.d["parts"]))

    def test_official_US_2004_2007_year_codes_preserved(self):
        for year,digit in [(2004,"4"),(2005,"5"),(2006,"6"),(2007,"7")]:
            row=self.f(f"US_original_{year}_VIN_engine_gear")
            self.assertEqual(row["value"]["MY_code"],digit)
            self.assertEqual(row["applicability"]["model_years"],[year])
            self.assertEqual(row["applicability"]["markets"],["US"])
        y2005=self.f("US_original_2005_VIN_engine_gear")["value"]
        self.assertEqual(y2005["9-5_engine_8"]["G"],"B235R")
        self.assertEqual(y2005["9-3_engine_8"]["Y"],"B207R")
        self.assertEqual(y2005["gearbox_7"]["9"],"5AT")

    def test_2006_no_unlisted_engine_inferred_and_not_2008(self):
        y2006=self.f("US_original_2006_VIN_engine_gear")
        self.assertEqual(y2006["value"]["gearbox_7"]["1"],"6AT")
        self.assertNotIn("S",y2006["value"]["engine_8_listed"])
        self.assertEqual(y2006["applicability"]["model_years"],[2006])
        self.assertNotIn(y2006["id"],{x["id"] for x in filter_records(self.all,platform="9-3-9440",year=2008)})
        missing=self.f("US_original_pdf_missing_MY2008_2009_VIN_complete")["value"]
        self.assertEqual(missing["missing_in_this_compilation"],[2008,2009])

    def test_factory_example_year_2005_is_wrong_but_table_is_five(self):
        x=self.f("US_original_2005_example_modelyear_contradiction")["value"]
        self.assertEqual((x["2005_page_tenth_code_table"],x["example_tenth_character"]),("5","4"))

    def test_official_ism_kit_is_not_direct_interchange(self):
        old=next(x for x in self.d["parts"] if x["part_number"]=="12801010")
        kit=next(x for x in self.d["parts"] if x["part_number"]=="32021815")
        self.assertEqual(old["relationships"][0]["type"],"replaced_by_service_kit")
        self.assertEqual(old["relationships"][0]["part_number"],kit["part_number"])
        self.assertIn("NOT drop-in",old["relationships"][0]["conditions"])
        self.assertIn("black",kit["requirements"][0])
        self.assertEqual(old["applicability"]["platforms"],["9-3-9440"])
        self.assertEqual(self.f("official_93_2003_11_ISM_replacement_kit")["value"]["type"],"conditional service/rebuild kit rather than complete swap")

    def test_production_cutoff_torque_is_not_part_number(self):
        d=self.f("og95_2008_left_engine_mount_VIN_cutover_nut")
        self.assertEqual(d["value"]["through_printed_VIN"],"73514478")
        self.assertEqual(d["value"]["from_printed_VIN"],"73514479")
        self.assertIn("not entire 17-digit",d["notes"])
        self.assertEqual(d["applicability"]["model_years"],[2008])

    def test_blank_template_no_vehicle_approval(self):
        self.assertIsNone(self.template["vehicle_identity"])
        self.assertEqual(self.template["replacement_proposals"],[])
        self.assertIn("conditional_service_kit_documented",self.template["allowed_decisions"])
        self.assertNotIn("universal_direct_fit",self.template["allowed_decisions"])
        self.assertTrue(all(field["default"] is None for field in self.template["required_fields"]))
        self.assertGreaterEqual(len(self.template["required_fields"]),10)

if __name__=="__main__":
    unittest.main()
