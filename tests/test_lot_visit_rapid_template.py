"""Lot-visit worksheet remains blank, privacy-safe and outside false Phase 0 approvals."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "data/inspection-templates/lot-rapid-20261016.json"
DETAILED = ROOT / "data/inspection-templates/nonrunning-phase0.json"

class LotVisitWorksheetTests(unittest.TestCase):
    def test_blank_2026_visit_does_not_claim_an_inspected_vehicle(self):
        data = json.loads(TEMPLATE.read_text(encoding="utf-8"))
        original = json.loads(DETAILED.read_text(encoding="utf-8"))
        self.assertEqual(data["scheduled_visit_date"], "2026-10-16")
        self.assertEqual(data["project_scope"]["original_market_priority"], "US")
        self.assertEqual(data["project_scope"]["transmission"], "factory automatic")
        self.assertEqual(data["project_scope"]["drivetrain"], "FWD")
        self.assertEqual(data["record"]["status"], "not_inspected")
        self.assertEqual(data["record"]["visit_disposition"], "unassessed")
        self.assertFalse(data["record"]["mechanical_condition_confirmed"])
        self.assertFalse(data["record"]["exact_vin_specific_parts_verified"])
        self.assertFalse(data["record"]["price_and_repair_budget_verified"])
        self.assertEqual(original["vehicle_results"], None)
        self.assertIn("no full-throttle transmission stall test",
                      original["prohibited_shortcuts"])

    def test_privacy_and_vin_not_prepopulated(self):
        data = json.loads(TEMPLATE.read_text(encoding="utf-8"))
        template = data["record"]
        self.assertTrue("Keep privately" in data["privacy"]["full_vin"])
        self.assertEqual(template["lot_index"], "S__")
        self.assertIsNone(template["first_pass"]["seller_stated_model_year"])
        self.assertIsNone(template["first_pass"]["odometer_as_displayed"])
        self.assertFalse(template["first_pass"]["vin_privately_photographed"])
        self.assertFalse(template["first_pass"]["seller_provided_diagnostic_invoice"])
        self.assertEqual(template["first_pass"]["asking_price_usd"], None)
        self.assertEqual(template["second_pass_if_safe"]["diagnostic_codes_read_only"], None)
        for s in ("stop_excluded_or_major_hazard", "hold_proof_required",
                  "finalist_requires_inspection"):
            self.assertIn(s, data["enumerations"]["visit_disposition"])

    def test_live_intake_never_treats_seller_diagnosis_as_fact(self):
        data = json.loads(TEMPLATE.read_text(encoding="utf-8"))
        self.assertTrue(any("Seller claims" in x for x in data["safety_stops"]))
        self.assertTrue(any("Never crawl" in x for x in data["safety_stops"]))
        self.assertIn("A partial", data["gate_status"])

if __name__ == "__main__":
    unittest.main()
