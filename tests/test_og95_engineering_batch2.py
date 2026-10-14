#!/usr/bin/env python3
"""Contract test for the derived OG 9-5 engineering buying dossier, not factory-claim certification."""
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
REGISTER=ROOT/"data/engineering-dossiers/og95-b205-b235-purchase-engineering-20261014.json"
REPORT=ROOT/"docs/research/og95-b205-b235-complete-purchase-dossier-20261014.md"
WORKSHEET=ROOT/"docs/research/og95-b205-b235-buyer-inspection-worksheet-20261014.md"

class TestOg95Batch2(unittest.TestCase):
    def test_usable_case_contract_and_crosslinks(self):
        d=json.loads(REGISTER.read_text())
        cases=d["cases"]
        self.assertEqual(len(cases),20)
        self.assertEqual(len({x["id"] for x in cases}),len(cases))
        self.assertEqual(d["scope"]["platform"],"9-5-9600")
        self.assertEqual(d["scope"]["markets"],["US","CA"])
        self.assertIn("B205/B235",d["scope"]["engine_family"])
        ids={x["id"] for x in cases}
        self.assertIn("O95-16",ids)
        source_index=set()
        for path in (ROOT/"data/datasets").glob("*.json"):
            data=json.loads(path.read_text())
            for kind in ("sources","facts","issues","parts","gaps"):
                source_index.update(x["id"] for x in data[kind])
        report=REPORT.read_text()
        worksheet=WORKSHEET.read_text()
        for x in cases:
            with self.subTest(case=x["id"]):
                self.assertIn(x["id"],report)
                self.assertIn(x["purchase_decision"],d["dispositions"])
                self.assertGreaterEqual(len(x["buyer_checks"]),2)
                self.assertGreaterEqual(len(x["unresolved"]),2)
                self.assertTrue(x["prior_ids"])
                self.assertTrue(set(x["prior_ids"]) <= source_index)
                self.assertTrue(x["sources"])
                self.assertTrue(all(s.startswith("https://") for s in x["sources"]))
                for k in ("applies","failure","corrective_path","cost_basis","improvement_status","repair_class"):
                    self.assertGreater(len(x[k]),18)
        for token in ("subframe","VIN","coolant","FA57","Total installed","catalytic","AF30"):
            self.assertIn(token.lower(),worksheet.lower())
        for token in ("55561200","55558696","32022255","32019620","O95-18","B308E"):
            self.assertIn(token,report)
        self.assertTrue(any("No factory" in x for x in d["limits"]))

if __name__=="__main__":
    unittest.main()
