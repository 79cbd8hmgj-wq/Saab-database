"""Factory VIN/gearbox document consistency and strict platform scopes."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1] / "tools"))
from database import load_datasets, validate_datasets, filter_records

class VINGearboxProvenanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.all=load_datasets()
        cls.d=next(x for x in cls.all if x["domain"]=="vin_gearbox_provenance")
        cls.facts=cls.d["facts"]

    def record(self,predicate,subject):
        matches=[x for x in self.facts if x["predicate"]==predicate and x["subject"]==subject]
        self.assertEqual(len(matches),1,(predicate,subject))
        return matches[0]

    def test_counts_and_provenance(self):
        self.assertEqual(validate_datasets(self.all),[])
        self.assertEqual(tuple(len(self.d[k]) for k in ("sources","facts","issues","parts","gaps")),
                         (14,29,2,0,9))
        self.assertTrue(all(x["retrieval"]=="full_text" for x in self.d["sources"]))
        self.assertTrue(all(x["source_ids"] for x in self.facts))

    def test_cross_year_95_vin_mirror_mismatch_not_used(self):
        x=self.record("VIN_year_page_mismatch","VIN:9600:2007-directory")
        self.assertEqual(x["value"]["directory_model_year"],2007)
        self.assertEqual(x["value"]["VIN_year_mapping"],2010)
        self.assertEqual(x["category"],"source_quality")
        self.assertIn("Reject",x["notes"])
        x=self.record("VIN_stale_year_list","VIN:9600:2005-directory")
        self.assertEqual(x["value"]["latest_year_shown"],2004)
        self.assertIn("Reject",x["notes"])

    def test_2005_93_example_is_not_an_actual_vehicle(self):
        q=self.record("VIN_example_conflict","VIN:9440:2005")
        self.assertEqual(q["value"]["illustrative_row_year_character"],"3")
        self.assertEqual(q["value"]["table_year_character"],"5")

    def test_2008_93_B207_mapping_does_not_spread_to_2005(self):
        q=self.record("VIN_B207_engine_position_8","VIN:9440:2008")
        self.assertEqual(q["value"],{"F":"B207E","S":"B207L","Y":"B207R"})
        self.assertEqual(q["applicability"]["model_years"],[2008])
        q05=self.record("VIN_engine_marketing_position_8","VIN:9440:2005")
        self.assertEqual(q05["value"]["Y"],"2.0 Turbo")
        self.assertNotIn("B207R",q05["value"].values())
        self.assertEqual(self.record("VIN_body_position_6","VIN:9440:2008")["value"]["5"],"5-door")

    def test_FA57_adaptation_codes_and_tcm_are_not_equal(self):
        og=self.record("FA57_gearbox_type_example","Gearbox:9600:FA57")
        ng=self.record("FA57_gearbox_type_example","Gearbox:9440:FA57")
        self.assertEqual(og["value"]["group2_adaptation"],"C")
        self.assertTrue(ng["value"]["adaptation"].startswith("1"))
        self.assertNotEqual(og["applicability"]["platforms"],ng["applicability"]["platforms"])
        tcmo=self.record("tcm_engine_letter_mapping","TCM:9600:FA57")["value"]
        tcmn=self.record("tcm_engine_letter_mapping","TCM:9440:FA57")["value"]
        self.assertEqual(tcmo["H"],"B235R")
        self.assertEqual(tcmn["K"],"B207R")
        self.assertFalse(set(tcmo)&set(tcmn))

    def test_manual_source_discrepancy_not_silently_resolved(self):
        q=self.record("manual_type_example_and_source_discrepancy","Gearbox:9600:manual")
        self.assertEqual(q["value"]["example"].split()[0],"FM55")
        self.assertEqual(q["value"]["first_group_heading"],"FM57")
        self.assertEqual(q["category"],"source_quality")

    def test_no_part_approval_from_webepc_feature_listing(self):
        self.assertEqual(self.d["parts"],[])
        q=self.record("vin_filtered_part_evidence_required","Factory:Saab-WebEPC")
        self.assertEqual(q["applicability"],{})
        self.assertIn("No actual VIN",q["notes"])
        self.assertTrue(any("Manufacturer original WebEPC" in gap["title"] for gap in self.d["gaps"]))

    def test_platform_group_identity_not_cross_applied(self):
        g=next(x for x in self.d["issues"] if "Shared FA57" in x["title"])
        self.assertEqual(len(g["applicability"]["groups"]),2)
        self.assertEqual({x["platforms"][0] for x in g["applicability"]["groups"]},
                         {"9-5-9600","9-3-9440"})
        self.assertNotIn(g["id"],{r["id"] for r in filter_records(
            self.all,kind="issues",platform="9-3-9440",year=2007)})
        self.assertIn(g["id"],{r["id"] for r in filter_records(
            self.all,kind="issues",platform="9-3-9440",year=2005)})
        self.assertIn(g["id"],{r["id"] for r in filter_records(
            self.all,kind="issues",platform="9-5-9600",year=2007)})

if __name__=="__main__":
    unittest.main()
