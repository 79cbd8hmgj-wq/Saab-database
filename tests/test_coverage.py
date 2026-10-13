"""Regression tests for the conservative research coverage census."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from coverage import census, explicitly_applies_to_year, markdown_report


def fixture():
    return [{
        "domain": "synthetic", "sources": [{"id": "s", "url": "https://example.org", "retrieval": "full_text"}],
        "facts": [{
            "id": "f", "evidence_status": "documented",
            "applicability": {"platforms": ["9-5-9600", "9-3-9440"], "model_years": [2005, 2006],
                "groups": [
                    {"platforms": ["9-5-9600"], "model_years": [2005]},
                    {"platforms": ["9-3-9440"], "model_years": [2006]},
                ]},
        }],
        "issues": [{"evidence_status": "documented", "applicability": {"platforms": ["9-5-9600"]}}],
        "parts": [], "gaps": [{}],
    }]


class CoverageTests(unittest.TestCase):
    def test_grouped_scope_does_not_invent_model_year_pair(self):
        record = fixture()[0]["facts"][0]
        self.assertTrue(explicitly_applies_to_year(record, "9-5-9600", 2005))
        self.assertFalse(explicitly_applies_to_year(record, "9-5-9600", 2006))
        self.assertTrue(explicitly_applies_to_year(record, "9-3-9440", 2006))

    def test_missing_year_is_not_automatically_applicable(self):
        issue = fixture()[0]["issues"][0]
        self.assertFalse(explicitly_applies_to_year(issue, "9-5-9600", 2005))

    def test_counts_and_plain_language_warning(self):
        report = census(fixture())
        self.assertEqual(report["counts"]["facts"], 1)
        self.assertEqual(report["counts"]["issues"], 1)
        self.assertEqual(report["explicit_scope_counts"]["model_years"], 1)
        self.assertEqual(report["platform_year"]["9-5-9600"]["2006"]["facts"], 0)
        self.assertEqual(report["platform_year"]["9-3-9440"]["2006"]["facts"], 1)
        self.assertIn("not", markdown_report(report).lower())


if __name__ == "__main__":
    unittest.main()
