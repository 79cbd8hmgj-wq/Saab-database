"""MY2004–09 B235 lubrication and 9-3 FA57 identification boundaries."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from database import load_datasets, validate_datasets, filter_records

class B235MaintenanceFA57IdentityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.datasets = load_datasets()
        cls.d = next(x for x in cls.datasets if x["domain"] == "b235_maintenance_fa57_identity")
        cls.facts = cls.d["facts"]

    def row(self, predicate, year):
        a = [f for f in self.facts if f["predicate"] == predicate
             and f["applicability"].get("model_years") == [year]]
        self.assertEqual(len(a), 1, (predicate, year))
        return a[0]

    def test_all_sources_and_inventory(self):
        self.assertEqual(validate_datasets(self.datasets), [])
        self.assertEqual(tuple(len(self.d[k]) for k in
                         ("sources", "facts", "issues", "parts", "gaps")), (13, 44, 2, 0, 9))
        self.assertEqual(len({r["id"] for k in
             ("sources","facts","issues","parts","gaps") for r in self.d[k]}), 68)

    def test_repeated_pcv_wording_not_a_2009_new_hardware_claim(self):
        for year in (2004, 2007, 2009):
            x = self.row("pcv_external_oil_trap_location", year)
            self.assertIn("NOT a new revision", x["notes"])
            self.assertEqual(self.row("pcv_leak_possible_DTCs", year)["value"][0], "P1181")
        self.assertNotIn(2008, [r["applicability"]["model_years"][0]
            for r in self.facts if r["predicate"] == "pcv_low_load_flow"])

    def test_pressure_and_warning_distinct(self):
        for year in (2007, 2009):
            v=self.row("oil_pressure_test_2000_rpm", year)["value"]
            self.assertEqual((v["minimum_bar"],v["rpm"],v["oil_temperature_C"],
                              v["test_grade"]), (2.5,2000,105,"10W-30"))
            self.assertEqual(self.row("low_oil_warning_switch_band_bar",year)["value"]["max"],0.55)
            self.assertEqual(self.row("oil_total_and_service_fill_litres",year)["value"]["service_refill_including_filter"],4.0)
        self.assertFalse(any(f["predicate"] == "oil_pressure_test_2000_rpm"
          and f["applicability"].get("model_years") == [2008] for f in self.facts))

    def test_restricted_service_page_engines(self):
        for year in (2006,2008,2009):
            f=self.row("oil_drain_plug_torque_nm",year)
            self.assertEqual(f["value"],25)
            self.assertEqual(f["applicability"]["engine_codes"],["B205E","B235E"])
            self.assertNotIn("B235R",f["applicability"]["engine_codes"])

    def test_eu_oil_is_not_usca_approval(self):
        f=self.row("historical_gm_ll_a_025_oil",2009)
        self.assertEqual(f["applicability"]["markets"],["EU"])
        self.assertIn("2026",f["notes"])

    def test_fa57_code_cannot_become_vin_approval(self):
        x=self.row("fa57_code_groups",2005)
        self.assertEqual(x["applicability"]["transmission_codes"],["FA57"])
        self.assertIn("not a real serial",x["notes"])
        self.assertEqual(self.row("fa57_manufacture_month_encoding",2005)["value"]["J"],"Sep")
        self.assertEqual(self.row("fa57_tcm_engine_character_map",2005)["value"]["K"],"B207R")
        ta=self.facts[-2]
        self.assertEqual(ta["predicate"],"ta440_0702_body_chassis_limits")
        self.assertEqual(len(ta["applicability"]["groups"]),2)
        self.assertTrue(all(g["transmission_codes"]==["FA57"] for g in ta["applicability"]["groups"]))
        self.assertTrue(all(g["vin_ranges"][0]["comparison"]=="below" for g in ta["applicability"]["groups"]))

    def test_no_scope_leak_into_2003_9_5(self):
        y03={x["id"] for x in filter_records(self.datasets,platform="9-5-9600",year=2003)}
        self.assertFalse(y03 & {r["id"] for r in self.facts})
        self.assertIn("open-flame", self.d["issues"][1]["limits"][2])

if __name__ == "__main__":
    unittest.main()
