"""Boundary checks for provenance and conservative applicability filtering."""

import copy
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from database import filter_records, load_datasets, validate_datasets


def fixture():
    return {
        "schema_version": "1.0.0", "domain": "test_fixture",
        "sources": [{
            "id": "test-source", "title": "Synthetic validation fixture",
            "url": "https://example.org/fixture", "publisher": "Test fixture",
            "source_type": "technical_reference", "accessed_at": "2026-10-12",
            "retrieval": "full_text", "notes": "Not real vehicle information.",
        }],
        "facts": [{
            "id": "test-fact", "subject": "test:quantity", "category": "fixture",
            "predicate": "illustrative_quantity", "value": 7.1, "unit": "L",
            "applicability": {"platforms": ["test-platform"], "model_years": [2006], "markets": ["US"]},
            "source_ids": ["test-source"], "evidence_status": "documented",
            "locator": "Synthetic fixture", "notes": "Not a Saab specification.",
        }],
        "issues": [], "parts": [], "gaps": [],
    }


class ProvenanceTests(unittest.TestCase):
    def test_valid_source_chain_is_accepted(self):
        self.assertEqual(validate_datasets([fixture()]), [])

    def test_missing_reference_fails(self):
        dataset = fixture()
        dataset["facts"][0]["source_ids"] = ["missing-source"]
        self.assertTrue(any("unresolved source" in message for message in validate_datasets([dataset])))

    def test_technical_finding_without_source_fails(self):
        dataset = fixture()
        dataset["facts"][0]["source_ids"] = []
        self.assertTrue(any("require a source" in message for message in validate_datasets([dataset])))

    def test_cross_domain_duplicate_id_fails(self):
        first = fixture()
        second = copy.deepcopy(first)
        second["domain"] = "another_fixture"
        self.assertTrue(any("duplicate id" in message for message in validate_datasets([first, second])))

    def test_unitless_number_fails(self):
        dataset = fixture()
        dataset["facts"][0]["unit"] = None
        self.assertTrue(any("explicit unit" in message for message in validate_datasets([dataset])))

    def test_nonfinite_quantity_is_rejected(self):
        dataset = fixture()
        dataset["facts"][0]["value"] = {"pressure": float("nan")}
        self.assertTrue(any("nonfinite" in message for message in validate_datasets([dataset])))

    def test_nonstandard_json_number_is_rejected_on_load(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            directory = root / "data" / "datasets"
            directory.mkdir(parents=True)
            (directory / "invalid.json").write_text('{"quantity": NaN}', encoding="utf-8")
            with self.assertRaises(ValueError):
                load_datasets(root)

    def test_invalid_retrieval_label_fails(self):
        dataset = fixture()
        dataset["sources"][0]["retrieval"] = "probably"
        self.assertTrue(any("retrieval" in message for message in validate_datasets([dataset])))

    def test_part_number_type_preserves_identifiers(self):
        dataset = fixture()
        dataset["parts"] = [{
            "id": "test-part", "part_number": 123, "title": "Synthetic part",
            "applicability": {}, "relationships": [], "requirements": [],
            "source_ids": ["test-source"], "evidence_status": "documented", "notes": "Fixture only.",
        }]
        self.assertTrue(any("part_number" in message for message in validate_datasets([dataset])))


class ApplicabilityTests(unittest.TestCase):
    def test_missing_engine_is_not_universal_fitment(self):
        self.assertEqual(filter_records([fixture()], engine="B235R"), [])

    def test_unknown_scope_can_be_explicitly_included(self):
        self.assertEqual(len(filter_records([fixture()], engine="B235R", include_unknown=True)), 1)

    def test_wrong_year_is_excluded(self):
        self.assertEqual(filter_records([fixture()], year=2007), [])

    def test_wrong_market_is_excluded(self):
        self.assertEqual(filter_records([fixture()], market="EU"), [])

    def test_explicit_scope_matches_without_case_dependency(self):
        self.assertEqual(len(filter_records([fixture()], platform="TEST-PLATFORM", year=2006, market="us")), 1)

    def test_partial_engine_name_is_not_automatically_a_variant(self):
        dataset = fixture()
        dataset["facts"][0]["applicability"]["engine_codes"] = ["B207"]
        self.assertEqual(filter_records([dataset], engine="B207R"), [])

    def test_inference_status_is_retained_in_results(self):
        dataset = fixture()
        dataset["facts"][0]["evidence_status"] = "inference"
        self.assertEqual(filter_records([dataset])[0]["evidence_status"], "inference")

    def test_grouped_platform_and_year_are_not_a_cartesian_product(self):
        dataset = fixture()
        dataset["facts"][0]["applicability"] = {
            "platforms": ["older", "newer"], "model_years": [2006, 2011],
            "groups": [
                {"platforms": ["older"], "model_years": [2006]},
                {"platforms": ["newer"], "model_years": [2011]},
            ],
        }
        self.assertEqual(filter_records([dataset], platform="newer", year=2006), [])
        self.assertEqual(len(filter_records([dataset], platform="newer", year=2011)), 1)

    def test_unknown_is_checked_inside_each_group(self):
        dataset = fixture()
        dataset["facts"][0]["applicability"] = {
            "platforms": ["older", "newer"], "model_years": [2006, 2011],
            "groups": [
                {"platforms": ["older"], "model_years": [2006]},
                {"platforms": ["newer"]},
            ],
        }
        self.assertEqual(filter_records([dataset], platform="newer", year=2006), [])
        self.assertEqual(len(filter_records([dataset], platform="newer", year=2006, include_unknown=True)), 1)

    def test_malformed_group_is_rejected(self):
        dataset = fixture()
        dataset["facts"][0]["applicability"]["groups"] = ["not a scope"]
        self.assertTrue(any("groups" in message for message in validate_datasets([dataset])))

    def test_known_group_does_not_hide_malformed_nested_year(self):
        dataset = fixture()
        dataset["facts"][0]["applicability"]["groups"] = [{"model_years": ["2006"]}]
        self.assertTrue(any("model_years" in message for message in validate_datasets([dataset])))


class ResearchBoundaryTests(unittest.TestCase):
    """Keep documented production boundaries intact as records are extended."""

    @classmethod
    def setUpClass(cls):
        cls.datasets = load_datasets()

    def test_intake_valve_advisory_does_not_cross_platform_engine_year(self):
        matches = filter_records(self.datasets, platform="9-5-9650", year=2007, engine="B207R")
        self.assertNotIn("corrections-fact-006", {row["id"] for row in matches})
        matches = filter_records(self.datasets, kind="issues", platform="9-5-9650", year=2011, engine="A20NFT")
        self.assertIn("corrections-issue-011", {row["id"] for row in matches})

    def test_early_pcv_bulletin_retains_variant_restriction(self):
        wrong = filter_records(self.datasets, kind="parts", platform="9-3-9440", year=2003, engine="B207")
        self.assertTrue({"corrections-part-017", "corrections-part-018", "corrections-part-019"}.isdisjoint({row["id"] for row in wrong}))
        correct = filter_records(self.datasets, kind="parts", platform="9-3-9440", year=2003, engine="B207R")
        self.assertIn("corrections-part-017", {row["id"] for row in correct})

    def test_chassis_sources_use_queryable_platform_identity(self):
        for platform, domain in (("9-5-9600", "og95_body"), ("9-3-9440", "ng93_body")):
            expected = {row["id"] for dataset in self.datasets if dataset["domain"] == domain for row in dataset["facts"]}
            actual = {row["id"] for row in filter_records(self.datasets, platform=platform) if row["domain"] == domain}
            self.assertTrue(expected)
            self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
