"""Year-scoped 9-5 power and grounding source regression tests."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from database import filter_records, load_datasets, validate_datasets

class GroundPowerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.datasets = load_datasets()
        cls.domain = next(d for d in cls.datasets if d["domain"] == "og95_ground_power_0709")
        cls.facts = cls.domain["facts"]

    def f(self, year, pred):
        found = [f for f in self.facts
                 if f["predicate"] == pred and f["applicability"]["model_years"] == [year]]
        self.assertEqual(len(found), 1, (year, pred))
        return found[0]

    def test_source_integrity_and_counts(self):
        self.assertEqual(validate_datasets(self.datasets), [])
        for kind, count in [("sources", 13), ("facts", 44), ("issues", 2),
                            ("parts", 0), ("gaps", 6)]:
            self.assertEqual(len(self.domain[kind]), count)
        self.assertEqual(self.domain["sources"][11]["retrieval"], "search_excerpt")
        self.assertTrue(all(i["evidence_status"] == "inference"
                            for i in self.domain["issues"]))

    def test_each_year_has_independent_ground_source(self):
        source_ids = set()
        for year in (2007, 2008, 2009):
            x = self.f(year, "battery_ground_cable_sizes")
            self.assertEqual(x["value"]["battery_to_gearbox_G25_mm2"], 25)
            self.assertEqual(x["value"]["battery_to_chassis_G2_mm2"], 16)
            self.assertEqual(x["value"]["redundant_gearbox_to_chassis_mm2"], 10)
            self.assertIn("No approved", x["notes"])
            source_ids.add(x["source_ids"][0])
        self.assertEqual(len(source_ids), 3)

    def test_ignition_states_do_not_expand_into_2009(self):
        for year in (2007, 2008):
            x = self.f(year, "ignition_feed_states")["value"]
            self.assertEqual(x["plus_15"], "energized in ON and START")
            self.assertEqual(x["plus_54"], "energized in ON but cut in START")
        self.assertFalse(any(f["predicate"] == "ignition_feed_states"
                             and f["applicability"]["model_years"] == [2009] for f in self.facts))

    def test_petrol_fan_years_and_ground_references(self):
        for year in (2007, 2008, 2009):
            relay = self.f(year, "petrol_fan_relay_component_locations")
            self.assertEqual(set(relay["value"]), {"81", "155", "396"})
            self.assertIn("petrol", relay["notes"].lower())
            self.assertEqual(self.f(year, "fan_diagram_ground_refs")["value"],
                             ["G30", "G40", "G42"])

    def test_t7_harness_locations_not_assumed_for_2009(self):
        for year in (2007, 2008):
            self.assertIn("H24-2", self.f(year, "t7_bulkhead_connectors")["value"])
            self.assertIn("407_intake_air_temperature",
                          self.f(year, "t7_engine_sensor_locations")["value"])
        self.assertFalse(any(f["predicate"] == "t7_engine_sensor_locations"
                             and f["applicability"]["model_years"] == [2009] for f in self.facts))
        self.assertEqual(self.f(2009, "t7_2009_oxygen_sensor_locations")["value"]["592Fa"],
                         "heated oxygen sensor before catalytic converter")

    def test_no_scope_leakage_into_2006(self):
        got = {f["id"] for f in filter_records(
            self.datasets, platform="9-5-9600", year=2006)}
        for f in self.facts:
            self.assertEqual(f["applicability"]["platforms"], ["9-5-9600"])
            self.assertEqual(len(f["applicability"]["model_years"]), 1)
            self.assertNotIn(f["id"], got)

if __name__ == "__main__":
    unittest.main()
