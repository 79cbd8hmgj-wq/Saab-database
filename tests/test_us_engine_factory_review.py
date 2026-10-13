"""US Saab engine identity / no-rebuild screening evidence-integrity tests.

These checks protect the source scope; they do not certify actual vehicle VINs,
engine serial numbers, parts interchange or fault prevalence.
"""
import json
from pathlib import Path
import unittest
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
PRODUCTION = ROOT / "data/vehicle-catalogue/us-production-normalized.json"
ENGINE = ROOT / "data/vehicle-catalogue/us-engine-factory-review.json"


class USEngineFactoryReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.production = json.loads(PRODUCTION.read_text(encoding="utf-8"))
        cls.data = json.loads(ENGINE.read_text(encoding="utf-8"))
        cls.records = {x["id"]: x for x in cls.production["configurations"]}
        cls.source_map = {x["id"]: x for x in cls.data["source_records"]}
        cls.topic_map = {x["id"]: x for x in cls.data["screening_topics"]}

    def test_110_us_configuration_ids_match_exactly(self):
        reviews = self.data["engine_reviews"]
        ids = [x["production_id"] for x in reviews]
        self.assertEqual(len(reviews), 110)
        self.assertEqual(len(set(ids)), len(ids))
        self.assertEqual(set(ids), set(self.records))
        self.assertEqual(self.data["market_priority"], "US")
        self.assertFalse(self.data["canadian_records_modified"])
        self.assertEqual(self.data["production_source"],
                         "data/vehicle-catalogue/us-production-normalized.json")

    def test_no_promotion_of_unconfirmed_engine_fitness(self):
        for review in self.data["engine_reviews"]:
            with self.subTest(id=review["production_id"]):
                item = self.records[review["production_id"]]
                for key in ("model", "model_year", "platform", "body_style"):
                    self.assertEqual(item[key], review[key])
                self.assertEqual(item["engine_label"], review["engine_source_label"])
                self.assertEqual(item["engine_code"], review["engine_source_code"])
                self.assertFalse(review["candidate_model_year_original_vin_checked"])
                self.assertFalse(review["physical_engine_stamping_checked"])
                self.assertFalse(review["parts_interchange_approved"])
                self.assertFalse(review["engine_reliability_ranked"])
                self.assertIn(review["evidence_level"],
                              {"factory_platform_code_correlated_not_car_verified",
                               "factory_year_vin_code_correlated_not_car_verified"})
                self.assertTrue(review["source_ids"])
                for sid in review["source_ids"]:
                    self.assertIn(sid, self.source_map)
                    self.assertEqual(self.source_map[sid]["platform"], item["platform"])
                for tid in review["diagnostic_topic_ids"]:
                    self.assertIn(tid, self.topic_map)

    def test_factory_engine_code_families_follow_actual_source(self):
        counts = Counter((x["platform"], x["saab_wis_engine_family_candidate"])
                         for x in self.data["engine_reviews"])
        self.assertEqual(counts, Counter({
            ("9400", "B204L"): 4, ("9400", "B205L"): 4,
            ("9400", "B205R"): 3, ("9440", "B207L"): 3,
            ("9440", "B207R"): 25, ("9440", "B284L"): 6,
            ("9600", "B235E"): 15, ("9600", "B235L"): 4,
            ("9600", "B235R"): 32, ("9600", "B308E"): 13,
            ("650", "A20NFT/LHU"): 1,
        }))

    def test_sourced_usca_sludge_bulletin_scope_is_precise(self):
        affected = {
            x["production_id"] for x in self.data["engine_reviews"]
            if "us-eng-screen-sludge-bearing" in x["diagnostic_topic_ids"]
        }
        expected = {
            x["id"] for x in self.records.values()
            if ((x["platform"] == "9400" and x["model_year"] in range(1999, 2004)
                 and x["engine_code"] in ("B205L", "B205R"))
                or (x["platform"] == "9600" and x["model_year"] in range(1998, 2004)
                    and x["engine_code"] in ("B235E", "B235L", "B235R")))
        }
        self.assertEqual(affected, expected)
        self.assertNotIn("engine-tsb-pcv-allmarkets-2102417",
                         self.data["engine_reviews"][0]["source_ids"])
        for x in self.data["engine_reviews"]:
            if x["engine_source_code"] in ("B204L", "B207L", "B207R", "B284L", "B308E") or x["model_year"] >= 2004:
                self.assertNotIn("us-eng-screen-sludge-bearing", x["diagnostic_topic_ids"])
        topic = self.topic_map["us-eng-screen-sludge-bearing"]
        self.assertEqual(topic["source_ids"], ["engine-tsb-usca-sludge-2102554"])
        self.assertIn("hcdiag-issue-001", topic["existing_repo_issues"])

    def test_factory_2011_ng95_code_is_candidate_until_vin_seen(self):
        a = [x for x in self.data["engine_reviews"] if x["platform"] == "650"]
        self.assertEqual(len(a), 1)
        self.assertEqual(a[0]["engine_source_label"], "2.0T")
        self.assertIsNone(a[0]["engine_source_code"])
        self.assertEqual(a[0]["saab_wis_engine_family_candidate"], "A20NFT/LHU")
        self.assertFalse(a[0]["candidate_model_year_original_vin_checked"])
        self.assertEqual(a[0]["source_ids"], ["engine-wis-9650-2011-vin"])
        self.assertTrue(any("BioPower" in x for x in [
            self.source_map["engine-wis-9650-2011-vin"]["notes"]]))

    def test_research_topics_are_bounded_without_unproven_failures(self):
        self.assertEqual(len(self.data["screening_topics"]), 6)
        self.assertEqual(len(self.data["source_records"]), 17)
        self.assertEqual(len(self.topic_map), 6)
        self.assertEqual(len(self.source_map), 17)
        for topic in self.data["screening_topics"]:
            self.assertTrue(topic["source_ids"])
            self.assertTrue(topic["recommended_evidence"])
            self.assertTrue(topic["not_claimed"])
            self.assertTrue(topic["decision_rule"])
            for sid in topic["source_ids"]:
                self.assertIn(sid, self.source_map)
        self.assertIn("no_original_candidate_VINs_checked", self.data["factory_certification"])


if __name__ == "__main__":
    unittest.main()
