"""Offline contract tests for the US production-register importer."""
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from us_production_import import SOURCE_SPECS, read_table, build_snapshot, gearbox_gears


def html_table(rows, total):
    header = "<p>Total US Production #: " + str(total) + "</p>"
    return header + "<table><tbody>" + "".join(
        "<tr>" + "".join("<td>" + str(v) + "</td>" for v in row) + "</tr>"
        for row in rows
    ) + "</tbody></table>"


class ProductionImporterTests(unittest.TestCase):
    def test_automatic_gear_labels_only(self):
        self.assertEqual(gearbox_gears("4AT"), 4)
        self.assertEqual(gearbox_gears("5AT"), 5)
        self.assertEqual(gearbox_gears("AT 6-Spd"), 6)
        self.assertIsNone(gearbox_gears("6MT"))
        self.assertIsNone(gearbox_gears("MT 6-Spd"))

    def test_9400_groups_paint_rows_and_rejects_manual_convertibles(self):
        html = html_table([
            ("1999", "Base", "3D", "4AT", "B204L", "BLACK 170", 2),
            ("1999", "Base", "3D", "4AT", "B204L", "SILVER 268", 3),
            ("1999", "Base", "3D", "5MT", "B204L", "BLACK 170", 9),
            ("1999", "Base", "CV", "4AT", "B204L", "BLACK 170", 20),
        ], 34)
        result = read_table(html, SOURCE_SPECS[0])
        self.assertEqual(len(result["candidates"]), 1)
        item = result["candidates"][0]
        self.assertEqual(item["engine_code"], "B204L")
        self.assertEqual(item["body_style"], "3-door hatchback")
        self.assertEqual(item["reported_production_count"], 5)
        self.assertEqual(item["paint_row_count"], 2)
        self.assertTrue(result["source"]["all_vehicle_total_reconciles"])
        self.assertEqual(result["source"]["excluded_reported_vehicle_counts"],
                         {"manual": 9, "convertible": 20, "awd": 0})

    def test_9440_fwd_auto_only(self):
        html = html_table([
            ("2003", "Arc", "4D", "FWD", "5AT", "B207R", "BLACK", 3),
            ("2003", "Arc", "4D", "AWD", "5AT", "B207R", "BLACK", 7),
            ("2003", "Arc", "CV", "FWD", "5AT", "B207R", "BLUE", 4),
        ], 14)
        result = read_table(html, SOURCE_SPECS[1])
        self.assertEqual(len(result["candidates"]), 1)
        self.assertEqual(result["candidates"][0]["reported_production_count"], 3)
        self.assertEqual(result["source"]["excluded_reported_vehicle_counts"]["awd"], 7)

    def test_9440_sportcombi_five_door_maps_to_wagon(self):
        html = html_table([
            ("2008", "2.0T", "5D", "FWD", "5AT", "B207R", "BLACK", 4),
            ("2008", "2.0T", "4D", "FWD", "5AT", "B207R", "BLACK", 6),
        ], 10)
        result = read_table(html, SOURCE_SPECS[1])
        body_by_code = {x["body_code"]: x["body_style"] for x in result["candidates"]}
        self.assertEqual(body_by_code["5D"], "wagon")
        self.assertEqual(body_by_code["4D"], "sedan")

    def test_650_compiled_2010_xwd_and_2011_turbo4(self):
        html = html_table([
            ("2010", "Aero", "AT 6-Spd", "AWD", "2.8T", "JET BLACK", 55),
            ("2011", "Turbo4", "AT 6-Spd", "FWD", "2.0T", "JET BLACK", 40),
            ("2011", "Turbo4", "MT 6-Spd", "FWD", "2.0T", "JET BLACK", 6),
        ], 101)
        result = read_table(html, SOURCE_SPECS[3])
        self.assertEqual(len(result["candidates"]), 1)
        item = result["candidates"][0]
        self.assertEqual(item["model_year"], 2011)
        self.assertEqual(item["body_style"], "sedan")
        self.assertEqual(item["automatic_gears"], 6)
        self.assertIsNone(item["engine_code"])
        self.assertEqual(item["engine_label"], "2.0T")
        self.assertEqual(item["reported_production_count"], 40)

    def test_9600_5at_sedan_and_wagon_are_distinct(self):
        html = html_table([
            ("2005", "Arc", "4D", "5AT", "B235L", "RED", 12),
            ("2005", "Arc", "5D", "5AT", "B235L", "RED", 6),
        ], 18)
        result = read_table(html, SOURCE_SPECS[2])
        self.assertEqual(len(result["candidates"]), 2)
        self.assertEqual({x["body_style"] for x in result["candidates"]},
                         {"sedan", "wagon"})

    def test_reject_unknown_bad_source_shape_instead_of_fabricating(self):
        with self.assertRaises(ValueError):
            read_table(html_table([
                ("2008", "Aero", "4D", "AT", "B284L", "RED", 10),
            ], 10), SOURCE_SPECS[1])
        with self.assertRaises(ValueError):
            read_table("<html>Access Denied</html>", SOURCE_SPECS[0])

    def test_complete_fixture_build_stays_research_only(self):
        raws = {
            SOURCE_SPECS[0][2]: html_table(
                [("1999", "Base", "5D", "4AT", "B204L", "RED", 3)], 3),
            SOURCE_SPECS[1][2]: html_table(
                [("2003", "Arc", "4D", "FWD", "5AT", "B207R", "RED", 5)], 5),
            SOURCE_SPECS[2][2]: html_table(
                [("2005", "Arc", "4D", "5AT", "B235L", "RED", 7)], 7),
            SOURCE_SPECS[3][2]: html_table(
                [("2011", "Turbo4", "AT 6-Spd", "FWD", "2.0T", "RED", 9)], 9),
        }
        d = build_snapshot(raws)
        self.assertEqual(len(d["configurations"]), 4)
        self.assertEqual(len(d["year_model_screening"]), 28)
        self.assertTrue(all(not r["factory_exhaustiveness_certified"]
                            for r in d["year_model_screening"]))
        self.assertEqual(d["markets"], ["US"])
        self.assertTrue(all(x["requires_vehicle_verification"]
                            for x in d["configurations"]))


if __name__ == "__main__":
    unittest.main()
