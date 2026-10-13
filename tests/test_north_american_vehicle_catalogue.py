"""Regression checks for the incremental North American automatic/FWD candidate catalogue.

This is a catalogue consistency test, not certification of factory fitment.
"""
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CATALOGUE = ROOT / "data/vehicle-catalogue/north-america-1998-2011.json"
SCOPE = ROOT / "data/audits/candidate-scope-1998-2011.json"


class NorthAmericanVehicleCatalogueTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalogue = json.loads(CATALOGUE.read_text(encoding="utf-8"))
        cls.scope = json.loads(SCOPE.read_text(encoding="utf-8"))
        cls.sources = {s["id"]: s for s in cls.catalogue["source_records"]}
        cls.examples = cls.catalogue["documented_configuration_examples"]
        cls.rows = cls.catalogue["model_year_screening"]

    def test_complete_screening_denominator_without_claiming_complete_research(self):
        expected = {(model, year) for model in ("9-3", "9-5") for year in range(1998, 2012)}
        observed = [(r["model"], r["model_year"]) for r in self.rows]
        self.assertEqual(len(observed), 28)
        self.assertEqual(set(observed), expected)
        self.assertEqual(len(observed), len(set(observed)))
        self.assertTrue(all(r["coverage_complete"] is False for r in self.rows))

    def test_scope_matches_decision_file(self):
        self.assertEqual(set(self.scope["eligible_markets"]), {"US", "CA"})
        self.assertEqual(self.catalogue["rules"]["markets"], ["US", "CA"])
        self.assertEqual(self.catalogue["rules"]["drive"], "FWD")
        self.assertEqual(self.catalogue["rules"]["transmission"], "factory automatic")
        self.assertIn("convertible", self.catalogue["rules"]["body_excluded"])

    def test_examples_only_include_qualified_market_configuration(self):
        ids = [r["id"] for r in self.examples]
        self.assertEqual(len(ids), len(set(ids)))
        source_ids = [s["id"] for s in self.catalogue["source_records"]]
        self.assertEqual(len(source_ids), len(set(source_ids)))
        for item in self.examples:
            with self.subTest(id=item["id"]):
                self.assertIn(item["model"], {"9-3", "9-5"})
                self.assertGreaterEqual(item["model_year"], 1998)
                self.assertLessEqual(item["model_year"], 2011)
                self.assertIn(item["platform"], {"9400", "9440", "9600", "650"})
                self.assertEqual(item["drivetrain"], "FWD")
                self.assertNotIn("convertible", item["body_style"].lower())
                self.assertGreater(item["automatic_gears"], 0)
                self.assertTrue(item["market_evidence"])
                self.assertTrue(item["source_ids"])
                self.assertIsNone(item["transmission_code"])  # no gearbox-code guessing in first batch
                for market in item["market_evidence"]:
                    self.assertIn(market, ("US", "CA"))
                    self.assertTrue(any(market in self.sources[sid]["market_scope"] for sid in item["source_ids"]))
                for source_id in item["source_ids"]:
                    self.assertIn(source_id, self.sources)

    def test_all_sampled_configurations_link_from_screening_row(self):
        for item in self.examples:
            rows = [r for r in self.rows if r["model"] == item["model"] and r["model_year"] == item["model_year"]]
            self.assertEqual(len(rows), 1)
            self.assertIn(item["id"], rows[0]["documented_configuration_ids"])
            for market in item["market_evidence"]:
                key = "us_status" if market == "US" else "canada_status"
                self.assertEqual(rows[0][key], "at_least_one_candidate_documented")

    def test_restricted_launches_and_manual_only_packages_not_promoted(self):
        self.assertFalse(any(r["model_year"] == 1998 and "US" in r["market_evidence"] for r in self.examples))
        self.assertFalse(any(r["model"] == "9-5" and r["model_year"] == 2010 and "US" in r["market_evidence"] for r in self.examples))
        self.assertFalse(any("viggen" in r["engine_label"].lower() for r in self.examples))
        excluded_ids = [e["id"] for e in self.catalogue["explicit_exclusions"]]
        self.assertEqual(len(excluded_ids), len(set(excluded_ids)))
        for excluded in self.catalogue["explicit_exclusions"]:
            with self.subTest(id=excluded["id"]):
                self.assertIn(excluded["market"], ("US", "CA"))
                self.assertTrue(excluded["source_ids"])
                for source_id in excluded["source_ids"]:
                    self.assertIn(source_id, self.sources)


    def test_year_specific_trims_and_engines_never_collapse_across_generations(self):
        by_id = {item["id"]: item for item in self.examples}
        self.assertIn("2.8L", by_id["na-2008-93-aero-sedan-at"]["engine_label"])
        self.assertIn("2.0L", by_id["na-2010-93-aero-sedan-at"]["engine_label"])
        self.assertIn("2.0L", by_id["na-2011-93-aero-sedan-at"]["engine_label"])
        self.assertEqual(by_id["na-2002-95-arc-sedan-at"]["engine_code"], "B308E")
        self.assertIn("V6", by_id["na-2002-95-arc-sedan-at"]["engine_label"])
        self.assertIn("I4", by_id["na-2004-95-arc-sedan-at"]["engine_label"])
        for yr in (2004, 2005):
            self.assertFalse(any(
                x["model"] == "9-5" and x["model_year"] == yr and
                x["body_style"] == "sedan" and
                "linear" in x["id"]
                for x in self.examples
            ))

    def test_conflicting_canadian_turbo_x_not_promoted_to_fwd(self):
        self.assertFalse(any("turbo-x" in x["id"].lower() for x in self.examples))
        source_ids = {s["id"] for s in self.catalogue["source_records"]}
        self.assertTrue({"na-cat-s34", "na-cat-s35"}.issubset(source_ids))
        exclusions = {x["id"]: x for x in self.catalogue["explicit_exclusions"]}
        self.assertIn("na-ex-11", exclusions)
        self.assertEqual(exclusions["na-ex-11"]["market"], "CA")
        self.assertTrue(all(
            x["model_year"] != 2010 or x["model"] != "9-5" or
            "US" not in x["market_evidence"]
            for x in self.examples
        ))

    def test_canadian_eligibility_not_inferred_from_us_facts(self):
        for item in self.examples:
            for market in item["market_evidence"]:
                self.assertTrue(any(
                    market in self.sources[source_id]["market_scope"]
                    for source_id in item["source_ids"]
                ))
        for row in self.rows:
            if row["canada_status"] == "unassessed":
                self.assertFalse(any(
                    "CA" in item["market_evidence"]
                    for item in self.examples
                    if item["model"] == row["model"] and item["model_year"] == row["model_year"]
                ))



    def test_2009_us_aero_xwd_is_not_2008_fwd_aero(self):
        by_id = {item["id"]: item for item in self.examples}
        self.assertIn("na-2008-93-aero-sedan-at", by_id)
        self.assertIn("na-2009-93-20t-sedan-at-us", by_id)
        self.assertIn("na-2009-93-20t-wagon-at-us", by_id)
        self.assertFalse(any(
            item["model"] == "9-3" and item["model_year"] == 2009 and
            "US" in item["market_evidence"] and "aero" in item["id"].lower()
            for item in self.examples
        ))
        excluded = {x["id"] for x in self.catalogue["explicit_exclusions"]}
        self.assertIn("na-ex-14", excluded)
        self.assertIn("na-ex-15", excluded)

    def test_us_and_canada_model_year_progress_independent(self):
        for row in self.rows:
            for market, status_key in (("US", "us_status"), ("CA", "canada_status")):
                matched = [
                    x for x in self.examples
                    if x["model"] == row["model"] and x["model_year"] == row["model_year"]
                    and market in x["market_evidence"]
                ]
                self.assertEqual(
                    row[status_key] == "at_least_one_candidate_documented",
                    bool(matched)
                )
        # This is intentional: partial country-specific coverage is not completeness.
        self.assertLess(
            sum(row["canada_status"] == "at_least_one_candidate_documented" for row in self.rows),
            len(self.rows)
        )
        self.assertTrue(all(row["coverage_complete"] is False for row in self.rows))


    def test_canadian_2009_aero_automatic_fwd_requires_factory_proof(self):
        # The 2009 CA editorial overview combines FWD Aero and an Aero AT
        # option, but exact CA FWD Aero trim pages show manual gearbox.
        # Do not construct an unproven FWD automatic via cross-product.
        self.assertFalse(any(
            x["model"] == "9-3" and x["model_year"] == 2009
            and "CA" in x["market_evidence"]
            and "aero" in x["id"].lower()
            for x in self.examples
        ))
        exclusions = {x["id"]: x for x in self.catalogue["explicit_exclusions"]}
        self.assertIn("na-ex-16", exclusions)
        self.assertEqual(exclusions["na-ex-16"]["market"], "CA")
        self.assertTrue(
            {"na-cat-s62", "na-cat-s63", "na-cat-s64"}.issubset(
                set(exclusions["na-ex-16"]["source_ids"])
            )
        )

    def test_canadian_2003_sedan_excludes_outgoing_9400_convertible(self):
        included = [
            x for x in self.examples
            if x["model"] == "9-3" and x["model_year"] == 2003
            and "CA" in x["market_evidence"]
        ]
        self.assertEqual(
            {x["id"] for x in included},
            {"na-2003-93-linear-sedan-at-ca", "na-2003-93-arc-sedan-at-ca"}
        )
        self.assertTrue(all(x["platform"] == "9440" for x in included))
        self.assertTrue(all(x["body_style"] == "sedan" for x in included))



if __name__ == "__main__":
    unittest.main()
