"""P0 high-cost repair triage keeps source scope, test conditions and hazards distinct."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from database import load_datasets, validate_datasets, filter_records

class HighCostPowertrainDiagnosticsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.all = load_datasets()
        cls.d = next(x for x in cls.all if x["domain"] == "high_cost_powertrain_diagnostics")
        cls.facts = {f["predicate"]: [] for f in cls.d["facts"]}
        for f in cls.d["facts"]: cls.facts[f["predicate"]].append(f)

    def test_structure_and_research_counts(self):
        self.assertEqual(validate_datasets(self.all), [])
        self.assertEqual(len(self.d["sources"]), 17)
        self.assertEqual(len(self.d["issues"]), 3)
        self.assertEqual(len(self.d["parts"]), 2)
        self.assertEqual(len(self.d["gaps"]), 9)
        self.assertEqual(self.d["sources"][11]["retrieval"], "search_excerpt")

    def test_us_canadian_bulletin_not_later_cars(self):
        rec = self.facts["service_bulletin_scope"][0]
        self.assertEqual(rec["value"]["number"], "210-2554 ed.3")
        self.assertEqual(rec["applicability"]["model_years"], list(range(1998, 2004)))
        self.assertEqual(rec["applicability"]["markets"], ["US", "CA"])
        self.assertEqual({x["id"] for x in filter_records(self.all, platform="9-5-9600", year=2008)}
                         & {x["id"] for x in self.d["facts"] if x["subject"].startswith("B205/B235")},set())

    def test_later_oil_table_not_early_threshold(self):
        recs = self.facts["minimum_oil_pressure_conditions"]
        self.assertEqual({r["applicability"]["model_years"][0] for r in recs}, {2005,2009})
        for r in recs:
            self.assertEqual(r["value"]["minimum_bar"], 2.5)
            self.assertEqual(r["value"]["oil_temp_C"], 105)
            self.assertEqual(r["value"]["test_oil"], "10W-30")

    def test_advisory_grouped_scope_no_B284(self):
        x=self.facts["cold_start_symptom_pattern"][0]
        g=x["applicability"]["groups"]
        self.assertEqual(g[0]["engine_codes"], ["B207R"])
        self.assertEqual(g[0]["model_years"], [2007,2008])
        self.assertEqual(g[1]["model_years"], [2009,2010,2011])
        self.assertFalse(any("B284" in t.get("engine_codes",[]) for t in g))
        self.assertEqual(g[2]["platforms"], ["9-5-9650"])

    def test_explicitly_no_automatic_valve_interchange(self):
        self.assertTrue(all(p["review_status"]=="needs_vehicle_verification" for p in self.d["parts"]))
        self.assertTrue(all(not p["relationships"] for p in self.d["parts"]))
        self.assertEqual({p["part_number"] for p in self.d["parts"]},{"55192156","12786696"})

    def test_FA57_not_AF40_and_separate_dipstick_methods(self):
        x=self.facts["technical_advice_population"][0]
        self.assertEqual(x["applicability"]["transmission_codes"],["FA57"])
        self.assertEqual(x["value"]["CV_VIN_suffix_below"],"56001058")
        self.assertNotEqual(self.facts["level_minmax_difference"][0]["value"],
                            self.facts["fluid_change_procedure_minmax_difference"][0]["value"])
        self.assertEqual(self.facts["fluid_level_test_conditions"][0]["value"]["TCM_temp_C"],80)

    def test_unsafe_sample_heat_not_recommended_as_DIY(self):
        q=next(i for i in self.d["issues"] if "FA57" in i["title"])
        self.assertIn("DO NOT",q["diagnosis_summary"])
        self.assertIn("qualified shop",q["diagnosis_summary"])

if __name__ == "__main__":
    unittest.main()
