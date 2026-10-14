"""17-case B207/FA57 buyer engineering dossier, not reliability grades."""
import json
import unittest
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
DOSSIER = ROOT / "data/engineering-dossiers/ng93-b207-purchase-engineering-20261014.json"
DATASETS = ROOT / "data/datasets"
LEDGER = ROOT / "data/tier-research/observations.json"
DOC = ROOT / "docs/research/ng93-b207-complete-purchase-dossier-20261014.md"

class B207EngineeringBuyerBatchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = json.loads(DOSSIER.read_text(encoding="utf-8"))
        cls.rows = {r["id"]: r for r in cls.d["cases"]}
        cls.existing_ids = set()
        for path in DATASETS.glob("*.json"):
            data = json.loads(path.read_text(encoding="utf-8"))
            for key in ("facts", "issues", "parts", "gaps"):
                cls.existing_ids.update(x["id"] for x in data[key])
        ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
        cls.existing_ids.update(x["id"] for x in ledger["failure_modes"])
        cls.report = DOC.read_text(encoding="utf-8")

    def test_delivers_usable_case_by_case_purchase_and_repair_batch(self):
        required = {"B207-01","B207-02","B207-03","B207-04","B207-05",
                    "T8-01","T8-02","KEY-01","KEY-02","FA57-01","FA57-02",
                    "CHASSIS-01","CHASSIS-02","CONFIG-01","BRAKE-01",
                    "SAFETY-01","BODY-01"}
        self.assertEqual(set(self.rows),required)
        self.assertEqual(len(self.d["cases"]),len(self.rows))
        valid_decisions = set(self.d["dispositions"])
        for case in self.d["cases"]:
            for key in ("system","concern","applies","failure","corrective_path",
                        "repair_class","improvement_status","cost_basis"):
                self.assertIsInstance(case[key],str)
                self.assertTrue(case[key].strip(),(case["id"],key))
            self.assertIn(case["purchase_decision"],valid_decisions)
            self.assertGreaterEqual(len(case["buyer_checks"]),2)
            self.assertTrue(all(s.strip() for s in case["buyer_checks"]))
            self.assertGreater(len(case["unresolved"]),0)
            self.assertGreater(len(case["sources"]),0)

    def test_prior_facts_issues_and_parts_resolve_to_saved_research(self):
        for case in self.d["cases"]:
            self.assertTrue(case["prior_ids"],case["id"])
            for id_ in case["prior_ids"]:
                self.assertIn(id_,self.existing_ids,(case["id"],id_))

    def test_sources_are_identifiable_and_not_placeholder_links(self):
        for case in self.d["cases"]:
            for uri in case["sources"]:
                parts = urlparse(uri)
                self.assertEqual(parts.scheme,"https",(case["id"],uri))
                self.assertIn(".",parts.netloc,(case["id"],uri))
                self.assertNotIn("example.com",uri)
                self.assertNotIn("/basic-engine/adjustment-replacement/",uri,
                                 "generic WIS directory must not masquerade as PCV procedure")

    def test_expensive_fails_distinguished_from_software_and_ordinary_service(self):
        for id_ in ("B207-01","B207-02","FA57-01","CHASSIS-02"):
            self.assertEqual(self.rows[id_]["purchase_decision"],
                             "avoid_major_unpriced_work")
        for id_ in ("T8-01","KEY-01","KEY-02"):
            self.assertTrue(self.rows[id_]["buyer_checks"])
        self.assertIn("Tech2",self.rows["T8-01"]["corrective_path"])
        self.assertIn("replace",self.rows["FA57-01"]["corrective_path"].lower())
        self.assertNotIn("T7 PCV renovation kit",self.rows["B207-05"]["corrective_path"])

    def test_critical_factory_and_market_boundaries_remain_visible(self):
        early=self.rows["FA57-01"]["applies"]
        self.assertIn("51002378",early)
        self.assertIn("56001058",early)
        self.assertIn("non-US",early)
        self.assertIn("2007",self.rows["B207-01"]["applies"])
        self.assertIn("2009",self.rows["B207-01"]["applies"])
        self.assertIn("2003 old-generation convertible",
                      self.rows["CONFIG-01"]["applies"])
        self.assertIn("New York",self.rows["CHASSIS-01"]["applies"])
        self.assertIn("31007202",self.rows["KEY-01"]["corrective_path"])
        self.assertIn("46011570",self.rows["KEY-01"]["corrective_path"])

    def test_prices_are_partial_quotes_never_total_repairs(self):
        valve=self.rows["B207-01"]["cost_basis"]
        self.assertIn("314.48",valve)
        self.assertIn("363.92",valve)
        self.assertIn("102.24",valve)
        self.assertIn("unpriced",valve)
        clone=self.rows["T8-02"]["cost_basis"]
        self.assertIn("89.99",clone)
        self.assertIn("donor",clone)
        self.assertIn("unquoted",self.rows["FA57-01"]["cost_basis"].lower())
        self.assertIn("€155",self.rows["B207-03"]["cost_basis"])

    def test_zero_rankings_no_factory_failure_rates_claimed(self):
        evidence=self.d["evidence_method"]
        self.assertTrue(evidence["no_year_is_universally_safe"])
        self.assertTrue(evidence["no_factory_failure_denominators_established"])
        self.assertTrue(evidence["no_verified_model_ranking_or_tier"])
        self.assertIn("6-speed",evidence["completeness"])
        self.assertIn("not",self.d["status"])

    def test_report_is_comprehensive_and_traces_to_structured_dataset(self):
        self.assertIn("../../data/engineering-dossiers/ng93-b207-purchase-engineering-20261014.json",
                      self.report)
        for label in ("B207 intake","Trionic 8","ISM","FA57","Front spring",
                      "A-pillar","Brake","water pump","Buyer checklist",
                      "Repair cost","2003–2011"):
            self.assertIn(label.lower(),self.report.lower())
        self.assertIn("Not quoted",self.report)

if __name__=="__main__":
    unittest.main()
