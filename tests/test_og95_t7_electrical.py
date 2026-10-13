"""Trionic T7 factory diagnostic provenance and exact model-year restrictions."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from database import load_datasets, validate_datasets, filter_records


class OG95Trionic7ElectricalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.datasets = load_datasets()
        cls.domain = next(x for x in cls.datasets if x["domain"] == "og95_t7_electrical")
        cls.facts = {x["predicate"] + ":" + str(x["applicability"]["model_years"][0]): x
                     for x in cls.domain["facts"]}

    def test_provenance_and_domain_counts(self):
        self.assertEqual(validate_datasets(self.datasets), [])
        self.assertEqual(len(self.domain["sources"]), 22)
        self.assertEqual(len(self.domain["facts"]), 43)
        self.assertEqual(len(self.domain["issues"]), 4)
        self.assertEqual(len(self.domain["parts"]), 0)
        self.assertEqual(len(self.domain["gaps"]), 7)

    def test_supply_and_ground_are_distinct(self):
        batt = self.facts["battery_memory_supply:2006"]
        switched = self.facts["ignition_switched_supply:2006"]
        ground = self.facts["power_ground_G7_ecu_pins:2006"]
        self.assertEqual(batt["value"], {"maxifuse": 2, "fuse": 17, "pin": 23})
        self.assertEqual(switched["value"], {"fuse": 27, "pin": 43})
        self.assertEqual(ground["value"], [25, 47, 62])
        self.assertEqual(batt["source_ids"], ["og95t7-src-002"])
        self.assertEqual(ground["source_ids"], ["og95t7-src-004"])

    def test_cps_is_an_essential_not_a_synthetic_substitute(self):
        cps = self.facts["resistance_at_20C:2006"]
        self.assertEqual(cps["unit"], "ohm")
        self.assertEqual(cps["value"], {"nominal": 860, "tolerance": 90})
        self.assertFalse(self.facts["cps_has_substitute_value:2006"]["value"])
        self.assertEqual(self.facts["cranking_signal_fault:2006"]["value"], "P0337")
        self.assertEqual(self.facts["running_position_loss:2006"]["value"], "P0336")

    def test_ignition_feedback_and_no_red_module_substitution(self):
        self.assertEqual(self.facts["combustion_feedback_pins:2006"]["value"], [53, 6])
        self.assertTrue(self.facts["incompatible_red_idm:2006"]["value"])
        self.assertEqual(self.facts["incompatible_red_idm:2006"]["source_ids"], ["og95t7-src-009"])

    def test_security_pairing_not_approved_as_free_interchange(self):
        security = self.facts["missing_immobilizer_permission:2006"]
        self.assertEqual(security["value"], "P1460")
        related = next(x for x in self.domain["issues"] if "TWICE" in x["title"])
        self.assertIn("programming", related["correction_summary"])
        self.assertTrue(any("Security-coding" in limit for limit in related["limits"]))

    def test_independent_source_years_are_not_automatically_expanded(self):
        rows_2007 = filter_records(self.datasets, platform="9-5-9600", year=2007)
        codes07 = {x["id"] for x in rows_2007}
        self.assertIn("og95t7-fact-037", codes07)
        self.assertNotIn("og95t7-fact-038", codes07)
        self.assertNotIn("og95t7-fact-012", codes07)
        rows_2009 = filter_records(self.datasets, platform="9-5-9600", year=2009)
        codes09 = {x["id"] for x in rows_2009}
        self.assertIn("og95t7-fact-039", codes09)
        self.assertNotIn("og95t7-fact-011", codes09)

    def test_temperature_location_dispute_kept_as_gap(self):
        titles = " ".join(g["title"] for g in self.domain["gaps"]).lower()
        self.assertIn("iat", titles)
        self.assertIn("cassette", titles)
        self.assertEqual(self.facts["resistance_at_20C:2006"]["subject"], "sensor:iat:T7")


if __name__ == "__main__":
    unittest.main()
