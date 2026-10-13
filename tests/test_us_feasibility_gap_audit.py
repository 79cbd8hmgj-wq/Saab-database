"""Gap-denominator audit tests: missing research is not a failed vehicle."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from audit_us_feasibility_gaps import build, PROD, FEAS, COVER, GEAR, OUT


class USFeasibilityGapAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.prod, cls.feas, cls.cov, cls.gear = (
            json.loads(x.read_text(encoding="utf-8"))
            for x in (PROD, FEAS, COVER, GEAR)
        )
        cls.audit = json.loads(OUT.read_text(encoding="utf-8"))

    def test_exactly_reproducible_from_already_merged_us_sources(self):
        self.assertEqual(build(self.prod, self.feas, self.cov, self.gear),
                         self.audit)
        self.assertEqual(self.audit["markets"], ["US"])
        self.assertEqual(self.audit["production_configuration_denominator"], 110)
        self.assertEqual(self.audit["scenario_denominator"], 18)
        self.assertEqual(len(self.audit["configurations"]), 110)
        ids = [x["production_configuration_id"] for x in self.audit["configurations"]]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(set(ids), {x["id"] for x in self.prod["configurations"]})

    def test_completeness_denominators_and_unassessed_family_identification(self):
        m = self.audit["missing"]
        self.assertEqual(m["missing_engine_core_repair_scenario"]["configuration_count"], 7)
        self.assertEqual(m["missing_transmission_repair_scenario"]["configuration_count"], 19)
        self.assertEqual(m["missing_structural_repair_scenario"]["configuration_count"], 12)
        self.assertEqual(m["missing_both_engine_and_transmission_scenarios"]["configuration_count"], 1)
        e = {
            (x["platform"], x["family_or_engine"]): x["unreviewed_configurations"]
            for x in self.audit["grouped_missing_research"]["engine_core"]
        }
        self.assertEqual(e, {
            ("9440", "B284L"): 6,
            ("650", "2.0T"): 1,
        })
        t = {
            (x["platform"], x["family_or_engine"]): x["unreviewed_configurations"]
            for x in self.audit["grouped_missing_research"]["transmission"]
        }
        self.assertEqual(t, {
            ("9440", "FA57"): 18,
            ("650", "AF40"): 1,
        })

    def test_absence_of_research_does_not_certify_health(self):
        for x in self.audit["configurations"]:
            self.assertTrue(x["general_safety_screen_present"])
            self.assertFalse(x["vehicle_VIN_or_condition_verified"])
            self.assertFalse(x["repair_price_or_rate_established"])
            self.assertEqual(
                x["neither_engine_nor_transmission_scenario"],
                not x["engine_core_failure_and_repair_scenario_present"] and
                not x["transmission_failure_and_repair_scenario_present"])
        self.assertFalse(self.audit["all_factory_vehicle_VINs_verified"])
        self.assertFalse(self.audit["all_priced_repair_options_verified"])
        self.assertTrue(self.audit["phase0_gates_unchanged"])

    def test_uncovered_original_93_and_new_95_structure_not_assumed_safe(self):
        body_gaps = [x for x in self.audit["configurations"]
                     if not x["structural_repair_scenario_present"]]
        self.assertEqual({x["platform"] for x in body_gaps}, {"9400", "650"})
        self.assertEqual(len(body_gaps), 12)
        self.assertTrue(all(x["general_safety_screen_present"] for x in body_gaps))

if __name__ == "__main__":
    unittest.main()
