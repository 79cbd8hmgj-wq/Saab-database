#!/usr/bin/env python3
"""Audit tier-list evidence readiness for existing U.S. Saab cohorts; never rank.

Research crosswalks are evidence *leads*, not confirmed vehicle failures, live
parts inventory, authorized fitment, or comparable failure probabilities.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRODUCTION = ROOT / "data/vehicle-catalogue/us-production-normalized.json"
FEASIBILITY = ROOT / "data/vehicle-catalogue/us-feasibility-coverage.json"
PARTS_TOOLS = ROOT / "data/audits/us-parts-tool-readiness-coverage.json"
PROTOCOL = ROOT / "data/tier-research/methodology.json"
OUT = ROOT / "data/audits/tier-research-readiness.json"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _index(items: list[dict], key: str, name: str) -> dict[str, dict]:
    indexed = {row[key]: row for row in items}
    if len(indexed) != len(items):
        raise ValueError(f"{name}: duplicate {key}")
    return indexed


def build(production: dict, feasibility: dict, part_tools: dict,
          protocol: dict) -> dict:
    if protocol.get("status") != "research_protocol_no_tier_assignments":
        raise ValueError("Methodology must not contain preassigned rankings")
    dims = {x["id"] for x in protocol["dimensions"]}
    if dims != {"factory_component_reliability", "parts_supply",
                "known_failure_burden", "repairability_economics"}:
        raise ValueError("Missing required separate comparison dimensions")
    if not protocol["system_inventory"] or not all(
        "critical" in system for system in protocol["system_inventory"]
    ):
        raise ValueError("System inventory not explicit")
    prod = _index(production["configurations"], "id", "production")
    feas = _index(feasibility["production_group_reviews"], "production_id",
                  "feasibility")
    part = _index(part_tools["production_groups"],
                  "production_configuration_id", "parts/tool")
    if set(prod) != set(feas) or set(prod) != set(part):
        raise ValueError("Configuration sets differ: cannot audit scope fairly")
    if (feasibility["counts"]["failure_rates_quantified"] != 0 or
            feasibility["counts"]["repair_prices_verified"] != 0 or
            feasibility["counts"]["parts_interchanges_approved"] != 0 or
            feasibility["counts"]["individual_vehicles_inspected"] != 0):
        raise ValueError("Measured evidence now exists: explicitly update tier audit")
    if not (part_tools["no_parts_fitment_approved"] and
            part_tools["no_actual_vehicle_verified"] and
            part_tools["no_installed_repair_prices"]):
        raise ValueError("Parts/tool proof changed: explicitly update tier audit")

    rows = []
    for id_, p in sorted(prod.items(),
                         key=lambda item: (item[1]["platform"],
                                           item[1]["model_year"], item[0])):
        f, t = feas[id_], part[id_]
        for field in ("platform", "model_year", "body_style", "engine_code",
                      "automatic_gears"):
            if p[field] != f[field] or p[field] != t[field]:
                raise ValueError(f"{id_}: contradictory {field}")
        if (p["market"], p["drivetrain"]) != ("US", "FWD"):
            raise ValueError(f"{id_}: unsupported scope")
        if not f["scenario_links"] or not t["job_readiness_leads"]:
            raise ValueError(f"{id_}: existing research leads missing")
        if f["individual_vehicle_inspection_completed"] or f["price_or_kit_confirmed"]:
            raise ValueError(f"{id_}: vehicle evidence now changed")
        if t["actual_vehicle_inspected"] or t["repair_authorized"]:
            raise ValueError(f"{id_}: repair approval now changed")
        if any(x["actual_fault_confirmed"] or x["replacement_authorized"]
               for x in f["scenario_links"]):
            raise ValueError(f"{id_}: scenario is no longer research-only")
        if any(x["vin_and_part_fitment_confirmed"] or
               x["special_tool_access_confirmed"] or
               x["shop_quote_obtained"]
               for x in t["job_readiness_leads"]):
            raise ValueError(f"{id_}: parts lead is no longer research-only")
        rows.append({
            "production_configuration_id": id_,
            "market": p["market"],
            "model": p["model"], "platform": p["platform"],
            "model_year": p["model_year"],
            "engine_code": p["engine_code"],
            "transmission": p["transmission"],
            "gearbox_case_identified": p["transmission_code"] is not None,
            "body_style": p["body_style"], "drivetrain": p["drivetrain"],
            "existing_source_scoped_leads": {
                "diagnostic_repair_scenarios": len(f["scenario_links"]),
                "parts_and_tool_job_plans": len(t["job_readiness_leads"]),
                "interpretation": "Applicability leads; counts MUST NOT be used as rankings or number of observed failures."
            },
            "tier_comparison_evidence": {
                "factory_component_reliability": "no_population_failure_rate_or_same_revision_lifetime_measurement",
                "parts_supply": "no_vehicle_specific_approved_interchange_or_verified_delivered_quote",
                "known_failure_burden": "documented_mechanism_leads_not_population_incidence",
                "repairability_economics": "no_current_total_repair_price_or_tested_DIY_access"
            },
            "rankable": False,
            "tier": None,
            "confidence_grade": None,
            "unresolved": [
                "Exact original VIN/build and installed components",
                "Failure-frequency denominators, age/mileage/exposure and maintenance",
                "Original versus factory-revised part condition and population risk",
                "Per-critical-system matched failure-mechanism and diagnostic coverage",
                "VIN-verified OEM successor and alternative fitment",
                "2026 U.S. supplier availability, delivery, and complete repair quotes",
                "Inspection of actual vehicle and structural safety"
            ]
        })
    if len(rows) != 110:
        raise ValueError("Scope changed: review eligibility and ranking denominator")
    return {
        "schema_version": "1.0.0",
        "as_of": protocol["as_of"],
        "status": "not_rankable_no_tiers_or_scores",
        "scope": "Only 110 source-compiled US automatic FWD nonconvertible 9-3/9-5 groups; exclusions are NOT negatives",
        "source_files": [
            str(PRODUCTION.relative_to(ROOT)),
            str(FEASIBILITY.relative_to(ROOT)),
            str(PARTS_TOOLS.relative_to(ROOT)),
            str(PROTOCOL.relative_to(ROOT))
        ],
        "comparison_pillars": sorted(dims),
        "summary": {
            "source_reported_production_configuration_groups": len(rows),
            "groups_with_existing_diagnostic_leads": sum(
                bool(r["existing_source_scoped_leads"]["diagnostic_repair_scenarios"])
                for r in rows
            ),
            "groups_with_existing_parts_tool_leads": sum(
                bool(r["existing_source_scoped_leads"]["parts_and_tool_job_plans"])
                for r in rows
            ),
            "groups_with_usable_population_failure_frequency": 0,
            "groups_with_exact_VIN_approved_parts_and_confirmed_US_supply": 0,
            "groups_with_all_in_repair_costs": 0,
            "groups_rankable": 0,
            "critical_systems_to_assess_symmetrically": sum(
                bool(x["critical"]) for x in protocol["system_inventory"]
            ),
            "ranked_models": 0
        },
        "note": "Unknown means not established by this evidence crosswalk, not zero failures or unavailable parts. Scenario/job lead counts must not become scores.",
        "configuration_rows": rows
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        result = build(read_json(PRODUCTION), read_json(FEASIBILITY),
                       read_json(PARTS_TOOLS), read_json(PROTOCOL))
        text = json.dumps(result, indent=2) + "\n"
        if args.check:
            if OUT.read_text(encoding="utf-8") != text:
                parser.exit(1, "STALE tier evidence audit; regenerate after reviewing evidence scope\n")
            print("PASS: all scoped configurations represented, no unsupported tier assignments")
        else:
            OUT.write_text(text, encoding="utf-8")
            print(f"Updated {OUT}")
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(1, f"Tier readiness audit failed: {exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
