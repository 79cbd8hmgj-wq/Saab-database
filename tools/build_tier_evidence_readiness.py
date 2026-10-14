#!/usr/bin/env python3
"""Build neutral Saab tier-evidence readiness crosswalk; NEVER calculate a tier."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRODUCTION = ROOT / "data/vehicle-catalogue/us-production-normalized.json"
SCENARIOS = ROOT / "data/vehicle-catalogue/us-feasibility-coverage.json"
TOOLS = ROOT / "data/audits/us-parts-tool-readiness-coverage.json"
METHOD = ROOT / "data/tier-research/methodology.json"
OUTPUT = ROOT / "data/tier-research/us-110-evidence-readiness.json"

BLOCKERS = (
    "comparable_component_failure_frequency_with_valid_at_risk_denominator",
    "original_part_revision_and_factory_countermeasure_chain",
    "VIN_or_build_approved_OEM_part_and_directed_supersession",
    "timestamped_exact_SKU_US_deliverability_and_supplier_diversity",
    "full_parts_tools_programming_labor_total_cost",
    "symmetric_critical_system_assessment_with_missingness_recorded",
)

def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))

def build(production: dict, feasibility: dict, tooling: dict, method: dict) -> dict:
    if method["status"] != "research_protocol_no_tier_assignments":
        raise ValueError("Tier grades are outside the current research protocol")
    if {x["id"] for x in method["dimensions"]} != {
        "factory_component_reliability", "parts_supply",
        "known_failure_burden", "repairability_economics",
    }:
        raise ValueError("Four independent research dimensions must remain present")
    if len(method["system_inventory"]) != 16:
        raise ValueError("Review explicit subsystem inventory before changing baseline")
    counts = feasibility["counts"]
    if any(counts[k] != 0 for k in (
        "failure_rates_quantified", "repair_prices_verified",
        "parts_interchanges_approved", "individual_vehicles_inspected",
    )):
        raise ValueError("New approvals or measurements require a reviewed readiness method")
    if not (tooling["no_parts_fitment_approved"] and
            tooling["no_actual_vehicle_verified"] and
            tooling["no_installed_repair_prices"]):
        raise ValueError("Parts/tool readiness changed: revisit assumptions")
    configs = production["configurations"]
    feasibility_by_id = {x["production_id"]: x for x in feasibility["production_group_reviews"]}
    tools_by_id = {x["production_configuration_id"]: x for x in tooling["production_groups"]}
    keys = [x["id"] for x in configs]
    if not keys or len(keys) != len(set(keys)):
        raise ValueError("Empty or duplicate production configurations")
    if set(keys) != set(feasibility_by_id) or set(keys) != set(tools_by_id):
        raise ValueError("Existing linked research denominator changed")
    rows = []
    for config in configs:
        key = config["id"]
        f = feasibility_by_id[key]
        t = tools_by_id[key]
        if (f["platform"] != config["platform"] or
            f["model_year"] != config["model_year"] or
            f["engine_code"] != config["engine_code"] or
            t["platform"] != config["platform"] or
            t["model_year"] != config["model_year"] or
            t["engine_code"] != config["engine_code"]):
            raise ValueError("Conflicting original configuration identifiers: " + key)
        if (f["individual_vehicle_inspection_completed"] or
            f["price_or_kit_confirmed"] or t["actual_vehicle_inspected"] or
            t["repair_authorized"]):
            raise ValueError("Actual vehicle now documented: source-specific review required")
        if any(x["actual_fault_confirmed"] or x["replacement_authorized"]
               for x in f["scenario_links"]):
            raise ValueError("Known actual fault/approval cannot be silently skipped")
        if any(x["vin_and_part_fitment_confirmed"] or
               x["special_tool_access_confirmed"] or x["shop_quote_obtained"]
               for x in t["job_readiness_leads"]):
            raise ValueError("New individual-car job evidence needs explicit review")

        rows.append({
            "production_configuration_id": key,
            "factory_applicability_approved": False,
            "identity_from_unverified_compiled_US_production": {
                "model": config["model"],
                "platform": config["platform"],
                "model_year": config["model_year"],
                "engine_code": config["engine_code"],
                "body_style": config["body_style"],
                "drivetrain": config["drivetrain"],
                "reported_automatic_gear_count": config["automatic_gears"],
                "reported_gearbox_case_code": config["transmission_code"],
            },
            "existing_diagnostic_scenario_leads": sorted(
                x["scenario_id"] for x in f["scenario_links"]),
            "existing_parts_tool_job_leads": sorted(
                x["job_id"] for x in t["job_readiness_leads"]),
            "dimension_assessments": {
                x["id"]: "not_audited_for_comparable_population_and_part_evidence"
                for x in method["dimensions"]
            },
            "documented_failure_rate": None,
            "verified_US_parts_availability": None,
            "VIN_approved_replacement_matrix": None,
            "full_repair_cost_USD": None,
            "tier": None,
            "ranking": None,
            "not_rankable": True,
        })
    return {
        "schema_version": "1.0.0",
        "as_of": method["as_of"],
        "meaning": "Research lead presence only, NOT completed subsystem analysis, verified parts, measured failure rate, or a model-quality score.",
        "universe": "Existing compiled US automatic/FWD/nonconvertible Saab 9-3/9-5 1998-2011 records ONLY, not all Saab models or US+Canada.",
        "source_files": [
            str(p.relative_to(ROOT)) for p in (PRODUCTION, SCENARIOS, TOOLS, METHOD)
        ],
        "denominator": len(rows),
        "number_with_research_scenario_leads": sum(
            bool(x["existing_diagnostic_scenario_leads"]) for x in rows),
        "number_with_parts_tool_job_leads": sum(
            bool(x["existing_parts_tool_job_leads"]) for x in rows),
        "number_with_quantified_failure_rate": 0,
        "number_with_VIN_approved_replacements": 0,
        "number_with_full_repair_quotes": 0,
        "number_ranked": 0,
        "shared_unresolved_requirements": list(BLOCKERS),
        "records": rows,
    }

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    fresh = build(load(PRODUCTION), load(SCENARIOS), load(TOOLS), load(METHOD))
    if args.check:
        if load(OUTPUT) != fresh:
            parser.exit(1, "STALE tier-research crosswalk; regenerate from tool\n")
        print(f"PASS: {fresh['denominator']} groups; no fabricated tier or reliability estimates")
    else:
        OUTPUT.write_text(json.dumps(fresh, indent=2) + "\n", encoding="utf-8")
        print(f"Wrote {OUTPUT} ({fresh['denominator']} source-derived groups)")

if __name__ == "__main__":
    main()
