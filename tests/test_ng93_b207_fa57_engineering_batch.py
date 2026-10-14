"""Regression contract for the B207/FA57 engineering buyer dossier.

Tests ensure the decision artifact remains source/vehicle-scoped; they do not
purport to test the external documents or predict real failure frequency.
"""
from __future__ import annotations
import json
import unittest
from pathlib import Path
from urllib.parse import urlparse

ROOT=Path(__file__).resolve().parents[1]
MATRIX=ROOT/"data/engineering-batches/ng93-b207-fa57-buyer-decision-matrix-20261014.json"
REPORT=ROOT/"docs/engineering/ng93-b207-fa57-buy-repair-improve-20261014.md"

class B207FA57EngineeringBatchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw=MATRIX.read_text(encoding="utf-8")
        cls.data=json.loads(cls.raw)
        cls.cases={item["id"]:item for item in cls.data["cases"]}
        cls.report=REPORT.read_text(encoding="utf-8")

    def test_15_material_engineering_decisions_not_only_index_routes(self):
        self.assertEqual(len(self.cases),15)
        self.assertEqual(len(self.cases),len(self.data["cases"]))
        self.assertTrue(self.data["scope"]["not_a_model_reliability_rating"])
        self.assertEqual(self.data["stats"]["engineering_decisions"],len(self.cases))
        self.assertEqual(self.data["stats"]["fleet_failure_denominators"],0)
        self.assertEqual(self.data["stats"]["vehicles_vin_tested"],0)
        self.assertEqual(self.data["stats"]["all_in_repairs_priced"],0)

    def test_original_primary_sources_and_reuse_links_are_explicit(self):
        for row in self.data["cases"]:
            with self.subTest(case=row["id"]):
                for key in ("system","applicability","factory_issue",
                            "repair","repair_scope","price_evidence",
                            "improvement_evidence","purchase_rule"):
                    self.assertTrue(row[key].strip(),(row["id"],key))
                self.assertTrue(row["buyer_tests"])
                self.assertTrue(row["sources"])
                self.assertTrue(row["original_links"])
                for url in row["sources"]:
                    parsed=urlparse(url)
                    self.assertEqual(parsed.scheme,"https")
                    self.assertTrue(parsed.netloc)
                for link in row["original_links"]:
                    self.assertTrue((ROOT/link).is_file(),link)

    def test_cold_valve_wear_does_not_create_immune_year_or_full_repair_quote(self):
        row=self.cases["engine-valve-sealing"]
        self.assertIn("2007",row["applicability"])
        self.assertIn("2009",row["applicability"])
        self.assertIn("55563529",row["repair"])
        self.assertIn("no verified",row["improvement_evidence"].casefold())
        self.assertIn("excludes",row["price_evidence"])

    def test_coolant_transmission_branch_must_retain_cutoffs_and_full_replacement(self):
        row=self.cases["early-fa57-coolant-atf"]
        for s in ("51002378","56001058","51000001"):
            self.assertIn(s,row["applicability"])
        self.assertIn("complete gearbox",row["repair"].casefold())
        self.assertIn("Confirmed coolant",row["purchase_rule"])
        self.assertIn("not all autos", " ".join(self.data["decision_rules"]["scope_guards"]))

    def test_ecm_software_warning_distinct_from_hardware_and_cloning_quote(self):
        sw=self.cases["t8-early-false-p0606"]
        hardware=self.cases["t8-ecu-replacement"]
        self.assertIn("TA248-0336",sw["sources"][0].upper())
        self.assertIn("software",sw["factory_issue"].casefold())
        self.assertIn("real fault",sw["purchase_rule"].casefold())
        self.assertIn("communicative original",hardware["repair"].casefold())
        self.assertIn("programming-only",hardware["price_evidence"])
        self.assertNotEqual(sw["kind"],hardware["kind"])

    def test_ism_and_key_security_keep_distinct_diagnostics(self):
        keys=self.cases["cim-remote-scl-key-loss"]
        ism=self.cases["ism-key-catch-detector"]
        self.assertIn("365-2568",keys["sources"][0])
        self.assertIn("41033108",ism["applicability"])
        self.assertIn("41063613",keys["applicability"])
        self.assertIn("CIM replacement",keys["repair"])
        self.assertIn("reusable",ism["repair"])
        self.assertIn("unavailable",ism["price_evidence"])

    def test_not_painting_all_repairs_as_diy_or_all_codes_as_proven_failure(self):
        categories={r["kind"] for r in self.data["cases"]}
        self.assertIn("factory_supported_fault",categories)
        self.assertIn("diagnostic_gate",categories)
        self.assertIn("configuration_and_safety_gate",categories)
        for case in ("engine-valve-sealing","early-fa57-coolant-atf",
                     "front-springs-structure","brakes-lines-abs"):
            self.assertIn(case,self.cases)
        self.assertIn("not a B207",self.cases["turbo-boost-chargeair"]["purchase_rule"].casefold())
        self.assertIn("gear-driven",self.cases["b207-water-pump"]["factory_issue"])

    def test_readable_document_contains_material_decisions(self):
        self.assertGreater(len(self.report),16000)
        for key in ("TA248-0336","365-2568","TA440-0702","55563529",
                    "12630084","32021815","15917","Saab 3309",
                    "no full installed repair quote","cold compression"):
            self.assertIn(key.casefold(),self.report.casefold())
        self.assertIn("original installed",self.report)
        self.assertIn("not a claim",self.report.casefold())

if __name__=="__main__":
    unittest.main()
