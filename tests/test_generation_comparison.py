import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('comparison', ROOT / 'tools/check_generation_comparison.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class GenerationComparisonTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(module.DATA.read_text())

    def test_sources_and_report(self):
        self.assertEqual(module.render(self.data), module.REPORT.read_text())

    def test_broken_cross_dossier_source_is_rejected(self):
        self.data['comparisons'][0]['evidence_refs'].append('ng:invented')
        with self.assertRaises(AssertionError):
            module.validate(self.data)

    def test_listing_cannot_become_delivered_inventory(self):
        self.data['supply_observations'][0]['deliverable_inventory_confirmed'] = True
        with self.assertRaises(AssertionError):
            module.validate(self.data)

    def test_part_price_cannot_become_installed_quote(self):
        self.data['supply_observations'][0]['installed_cost'] = 100
        with self.assertRaises(AssertionError):
            module.validate(self.data)

    def test_unknowns_cannot_be_silently_removed(self):
        self.data['comparisons'][0]['remaining_unknown'] = ''
        with self.assertRaises(AssertionError):
            module.validate(self.data)
