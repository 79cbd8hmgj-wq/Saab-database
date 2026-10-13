"""Factory WIS transmission-family research overlay safety and reproducibility tests."""
import json
import sys
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from annotate_us_automatic_gearboxes import build, PRODUCTION, OUTPUT


class USGearboxEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.production = json.loads(PRODUCTION.read_text(encoding="utf-8"))
        cls.committed = json.loads(OUTPUT.read_text(encoding="utf-8"))

    def test_full_overlay_matches_reproducible_generator(self):
        self.assertEqual(build(self.production), self.committed)

    def test_every_us_source_group_annotated_exactly_once(self):
        original = {x["id"]: x for x in self.production["configurations"]}
        rows = self.committed["annotations"]
        self.assertEqual(len(original), 110)
        self.assertEqual(len(rows), 110)
        self.assertEqual(
            set(original), {x["production_configuration_id"] for x in rows}
        )
        self.assertEqual(len(rows),
                         len({x["production_configuration_id"] for x in rows}))
        for item in rows:
            with self.subTest(id=item["production_configuration_id"]):
                prod = original[item["production_configuration_id"]]
                for field in ("model", "platform", "model_year", "engine_code"):
                    self.assertEqual(item[field], prod[field])
                self.assertEqual(item["gear_count"], prod["automatic_gears"])
                self.assertFalse(item["vehicle_vin_verified"])
                self.assertFalse(item["oem_interchange_approved"])
                self.assertFalse(item["durability_improvement_proven"])

    def test_documentation_status_by_platform_and_gears(self):
        counts = Counter((x["platform"], x["gear_count"], x["gearbox_family"])
                         for x in self.committed["annotations"])
        self.assertEqual(counts, Counter({
            ("9400", 4, "AF20 / AF22"): 11,
            ("9600", 4, "AF30"): 22,
            ("9600", 5, "FA57"): 42,
            ("9440", 5, "FA57"): 28,
            ("9440", 6, "AF40 / TF-80SC"): 6,
            ("650", 6, None): 1,
        }))
        states = Counter(x["evidence_state"] for x in self.committed["annotations"])
        self.assertEqual(states["factory_family_platform_supported"], 98)
        self.assertEqual(states["alternative_families_not_vehicle_resolved"], 11)
        self.assertEqual(states["factory_family_unresolved"], 1)

    def test_source_ids_and_diagnostic_claims_are_scoped(self):
        ids = {s["id"] for s in self.committed["research_sources"]}
        self.assertEqual(len(ids), 8)
        for item in self.committed["annotations"]:
            self.assertTrue(set(item["source_ids"]) <= ids)
            self.assertEqual(bool(item["source_ids"]),
                             item["evidence_state"] != "factory_family_unresolved")
        for caution in self.committed["diagnostic_cautions"]:
            self.assertTrue(caution["source_ids"])
            self.assertTrue(set(caution["source_ids"]) <= ids)
        self.assertEqual(len(self.committed["diagnostic_cautions"]), 4)

    def test_false_interchange_inference_rejected(self):
        items = self.committed["annotations"]
        for platform in ("9600", "9440"):
            fa57 = [x for x in items if x["platform"] == platform
                    and x["gearbox_family"] == "FA57"]
            self.assertTrue(fa57)
            self.assertTrue(all(not x["oem_interchange_approved"] for x in fa57))
        self.assertTrue(any(c["id"] == "at-risk-fa57-interchange"
                            for c in self.committed["diagnostic_cautions"]))

    def test_rare_and_ng95_remain_unverified(self):
        ng = [x for x in self.committed["annotations"]
              if x["platform"] == "650"]
        self.assertEqual(len(ng), 1)
        self.assertIsNone(ng[0]["gearbox_family"])
        self.assertEqual(ng[0]["source_ids"], [])
        original = {x["id"]: x for x in self.production["configurations"]}
        rare = {x["production_configuration_id"] for x in self.committed["annotations"]
                if original[x["production_configuration_id"]]["low_volume_manual_review"]}
        self.assertEqual(len(rare), 5)
        self.assertTrue(all(
            not x["vehicle_vin_verified"]
            for x in self.committed["annotations"]
            if x["production_configuration_id"] in rare
        ))


if __name__ == "__main__":
    unittest.main()
