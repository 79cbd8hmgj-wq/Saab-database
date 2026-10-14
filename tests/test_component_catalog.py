import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import component_catalog as catalog


class ComponentCatalogGuards(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = catalog.build()

    def test_source_groups_never_become_cross_product(self):
        scope = {"platforms": ["9-3-9440", "9-5-9600"],
                 "engine_codes": ["B207R", "B235R"],
                 "groups": [{"platforms": ["9-3-9440"], "engine_codes": ["B207R"]},
                            {"platforms": ["9-5-9600"], "engine_codes": ["B235R"]}]}
        self.assertEqual([(x["platforms"], x["engine_codes"]) for x in catalog.project_scope(scope)],
                         [(["9-3-9440"], ["B207R"]), (["9-5-9600"], ["B235R"])])

    def test_unknown_does_not_become_all(self):
        self.assertEqual(catalog.project_scope({}), [])
        self.assertNotIn("model_years", catalog.project_scope({"platforms": ["9-3-9440"]})[0])

    def test_exclusions_and_wrong_engines(self):
        for scope in ({"platforms": ["9-3-9400"]},
                      {"platforms": ["9-3-9440"], "engine_codes": ["B284"]},
                      {"platforms": ["9-5-9600"], "model_years": [2010]},
                      {"platforms": ["9-3-9440"], "drivetrain": "XWD"}):
            self.assertEqual(catalog.project_scope(scope), [])

    def test_candidate_cannot_be_promoted(self):
        c = copy.deepcopy(self.catalog)
        edge = next(r for r in c["interchanges"] if r["category"] == "E")
        edge["donor_approved"] = True
        self.assertTrue(any("marked approved" in e for e in catalog.validate(c)))

    def test_pump_screw_quarantine(self):
        c = copy.deepcopy(self.catalog)
        edge = copy.deepcopy(c["interchanges"][0])
        edge.update(id="int:bad:pump-screw", from_component_id="cmp:saab_service:93166829:water_pump",
                    to_component_id="cmp:saab_service:92151823:structural_fasteners", category="E")
        c["interchanges"].append(edge)
        self.assertTrue(any("pump-to-screw" in e for e in catalog.validate(c)))

    def test_unknown_complete_cost_is_not_zero_or_sticker_price(self):
        c = copy.deepcopy(self.catalog)
        c["repair_scenarios"][0]["complete_professional_total"] = 59.96
        self.assertTrue(any("Incomplete repair" in e for e in catalog.validate(c)))

    def test_missing_provenance_and_currency_rejected(self):
        c = copy.deepcopy(self.catalog)
        c["supplier_offerings"][0]["currency"] = "dollars"
        c["components"][0]["source_ids"] = ["nonexistent-source"]
        errors = catalog.validate(c)
        self.assertTrue(any("currency" in e for e in errors))
        self.assertTrue(any("provenance" in e for e in errors))

    def test_reviewed_evidence_change_requires_reconciliation(self):
        c = copy.deepcopy(self.catalog)
        c["research_reuse_index"][0]["original_sha256"] = "unreviewed"
        self.assertTrue(any("Unexplained change" in e for e in catalog.validate(c)))


if __name__ == "__main__":
    unittest.main()
