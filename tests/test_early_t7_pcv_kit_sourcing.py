"""Original Saab early 9-3 PCV bulletin and 2026 supplier data remain separate."""
import json
import unittest
from pathlib import Path

P=Path(__file__).resolve().parents[1]/"data/datasets/early-t7-pcv-kit-factory-and-sourcing-20261014.json"

class EarlyT7PCVSourcingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d=json.loads(P.read_text(encoding="utf-8"))

    def test_factory_9400_bulletin_is_complaint_conditioned(self):
        d=self.d
        self.assertEqual(d["domain"],"early_t7_pcv_kit_factory_and_sourcing_20261014")
        src=next(x for x in d["sources"] if x["id"]=="pcv-supply-src-001")
        self.assertIn("55561200_93.pdf",src["url"])
        scope=d["issues"][0]["applicability"]
        self.assertEqual(scope["platforms"],["9-3-9400"])
        self.assertEqual(scope["engine_codes"],["B205","B235"])
        self.assertEqual(scope["model_years"],list(range(1999,2004)))
        self.assertTrue(any("not all" in x.lower() for x in d["issues"][0]["limits"]))
        kit=next(x for x in d["facts"] if x["predicate"]=="factory_renovation_kit_contents")
        self.assertEqual(kit["evidence_status"],"documented")
        self.assertIn("oil trap",kit["value"])
        hours=next(x for x in d["facts"] if x["predicate"]=="historic_warranty_labor_operation_time")
        self.assertEqual((hours["value"],hours["unit"]),(0.9,"h"))
        self.assertIn("NOT 2026",hours["notes"])

    def test_aftermarket_is_never_presented_as_oem_supersession(self):
        d=self.d
        p={x["part_number"]:x for x in d["parts"]}
        self.assertEqual(set(p),{"55561200","21341200","21341200C"})
        self.assertEqual(p["21341200"]["evidence_status"],"supplier_claim")
        for part in p.values():
            self.assertEqual(part["review_status"],"needs_vehicle_verification")
            self.assertTrue(part["requirements"])
            for r in part["relationships"]:
                self.assertIn(r["type"],("aftermarket_reference","contains"))
                self.assertNotIn(r["type"],("supersedes","superseded_by","replaced_by_service_kit"))
        self.assertEqual(
            [r["part_number"] for r in p["21341200C"]["relationships"]],
            ["21341200","23340445","23349973","23340463"]
        )
        self.assertTrue(any("directed" in g["title"].lower()
                            for g in d["gaps"]))

    def test_supplier_years_are_grouped_and_exclude_newer_engines(self):
        d=self.d
        p=next(x for x in d["parts"] if x["part_number"]=="21341200")
        groups=p["applicability"]["groups"]
        self.assertEqual(groups[0]["platforms"],["9-3-9400"])
        self.assertEqual(groups[0]["model_years"],[2000,2001,2002])
        self.assertEqual(groups[1]["platforms"],["9-5-9600"])
        self.assertEqual(groups[1]["model_years"],list(range(1998,2004)))
        self.assertNotIn("B207",p["applicability"]["engine_codes"])

    def test_cached_price_and_unavailable_kit_not_real_stock(self):
        d=self.d
        f={(x["subject"],x["predicate"]):x["value"] for x in d["facts"]}
        self.assertEqual(f[("retail:eSaabParts:21341200","quoted_price")],72.5)
        self.assertEqual(f[("retail:FCP:21341200","quoted_price")],79.99)
        self.assertEqual(f[("retail:eSaabParts:55554444","quoted_stock_text")],
                         "Currently Unavailable")
        self.assertEqual(f[("retail:RAndD:Genuine55561200","quoted_stock_text")],
                         "Discontinued")
        for fact in d["facts"]:
            if fact["predicate"] in ("quoted_price","quoted_stock_text"):
                self.assertEqual(fact["evidence_status"],"supplier_claim")
                self.assertEqual(fact["review_status"],"needs_vehicle_verification")
        self.assertTrue(any("55554444" in g["reason"] for g in d["gaps"]))

if __name__=="__main__":
    unittest.main()
