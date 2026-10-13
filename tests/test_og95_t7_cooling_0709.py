"""Source-scoped MY2007–09 9-5 petrol cooling and T7 regression tests."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from database import load_datasets, validate_datasets, filter_records


class OG95T7CoolingYearTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.datasets = load_datasets()
        cls.dataset = next(x for x in cls.datasets if x["domain"] == "og95_t7_cooling_0709")
        cls.facts = cls.dataset["facts"]

    def find(self, predicate, year):
        matches = [x for x in self.facts if x["predicate"] == predicate
                   and x["applicability"]["model_years"] == [year]]
        self.assertEqual(len(matches), 1, f"{predicate} for MY{year}")
        return matches[0]

    def test_schema_and_fixed_domain_counts(self):
        self.assertEqual(validate_datasets(self.datasets), [])
        self.assertEqual(len(self.dataset["sources"]), 28)
        self.assertEqual(len(self.facts), 72)
        self.assertEqual(len(self.dataset["issues"]), 3)
        self.assertEqual(len(self.dataset["gaps"]), 7)

    def test_power_circuits_verified_independently_by_year(self):
        for year in [2007, 2008, 2009]:
            x = self.find("battery_30_supply_path", year)
            self.assertEqual(x["value"]["fuse"], 17)
            self.assertEqual(x["value"]["ecu_pin"], 23)
            self.assertEqual(self.find("ignition_15_supply_path", year)["value"]["ecu_pin"], 43)
            self.assertEqual(self.find("shared_5V_supply_pins", year)["value"], [69, 46])
        self.assertEqual(len({self.find("battery_30_supply_path", y)["source_ids"][0]
                              for y in [2007, 2008, 2009]}), 3)

    def test_cps_resistance_and_coolant_sensor_are_not_same_measurement(self):
        for year in [2007, 2008, 2009]:
            x = self.find("cps_resistance_20C", year)
            self.assertEqual(x["value"], {"nominal": 860, "tolerance": 90})
            self.assertEqual(x["unit"], "ohm")
        self.assertEqual(self.find("coolant_sensor_resistance_20C", 2007)["unit"], "kOhm")
        self.assertEqual(self.find("coolant_sensor_resistance_20C", 2009)["unit"], "kOhm")
        self.assertFalse(any(f["predicate"] == "coolant_sensor_resistance_20C"
                             and 2008 in f["applicability"]["model_years"] for f in self.facts))

    def test_fan_threshold_discrepancy_is_retained(self):
        summary = self.find("fan_switch_temperature_overview", 2008)["value"]
        detailed = self.find("fan_coolant_hysteresis", 2008)["value"]
        self.assertEqual(summary["low_on"], 100)
        self.assertEqual(detailed["low_on"], 99)
        self.assertEqual(summary["high_on"], detailed["high_on"])
        self.assertTrue(any("99 versus 100" in gap["title"] for gap in self.dataset["gaps"]))

    def test_ac_variants_and_missing_signal_failsafe_by_year(self):
        for year in [2007, 2008, 2009]:
            self.assertEqual(self.find("fan_control_module", year)["value"], "DICE")
            counts = self.find("fan_count_by_air_conditioning", year)["value"]
            self.assertEqual(counts, {"without_AC": 1, "with_AC": 2})
            fallback = self.find("missing_coolant_temperature_fan_behavior", year)["value"]
            self.assertEqual(fallback, {"speed": "low", "delay_seconds": 5})

    def test_pressure_test_not_misread_as_cap_relief_pressure(self):
        valve = self.find("cap_pressure_valve_opening", 2008)
        tested = self.find("static_leak_test_above", 2008)
        self.assertEqual(valve["unit"], "kPa")
        self.assertEqual(tested["unit"], "bar")
        self.assertNotEqual(valve["source_ids"], tested["source_ids"])

    def test_no_pseudoglobal_applicability(self):
        x = self.find("thermostat_opening_temperature", 2008)
        self.assertEqual(x["applicability"]["model_years"], [2008])
        ids_2007 = {r["id"] for r in filter_records(
            self.datasets, platform="9-5-9600", year=2007)}
        self.assertNotIn(x["id"], ids_2007)
        for row in self.facts:
            self.assertEqual(row["applicability"]["platforms"], ["9-5-9600"])
            self.assertEqual(len(row["applicability"]["model_years"]), 1)


if __name__ == "__main__":
    unittest.main()
