#!/usr/bin/env python3
"""Build a screening *applicability* index, not a failure prediction.

The source-derived Saab production catalogue establishes real U.S. model groups.
The feasibility scenarios record what to CHECK if a fault or symptom is present.
Matching them is never evidence that the fault exists on a particular car.
"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRODUCTION_PATH = ROOT / "data/vehicle-catalogue/us-production-normalized.json"
FEASIBILITY_PATH = ROOT / "data/vehicle-catalogue/us-repair-replace-feasibility.json"
OUT = ROOT / "data/vehicle-catalogue/us-repair-feasibility-coverage.json"

def applies(scenario, item):
    constraints = scenario["applicability"]
    if item["platform"] not in constraints["platforms"]:
        return False
    if "engine_codes" in constraints and item["engine_code"] not in constraints["engine_codes"]:
        return False
    if "automatic_gears" in constraints and item["automatic_gears"] not in constraints["automatic_gears"]:
        return False
    year_span = constraints.get("model_year_range_by_platform", {}).get(item["platform"])
    if year_span and not year_span[0] <= item["model_year"] <= year_span[1]:
        return False
    return True

def build(production, feasibility):
    if production.get("markets") != ["US"] or feasibility.get("market") != "US":
        raise ValueError("Only US factory-automatic/FWD production may be indexed")
    scenarios = feasibility["scenarios"]
    ids = [s["id"] for s in scenarios]
    if len(set(ids)) != len(ids):
        raise ValueError("Duplicate feasibility scenario IDs")
    out_rows = []
    for item in production["configurations"]:
        if (item["market"], item["drivetrain"]) != ("US", "FWD") or item["automatic_gears"] not in (4, 5, 6):
            raise ValueError("Ineligible model group: " + item["id"])
        matching = [s for s in scenarios if applies(s, item)]
        entries = [{
            "scenario_id": s["id"],
            "screen_status": (
                "VIN_condition_unresolved" if s["applicability"].get("vin_gate")
                else "generic_all_vehicle_safety_inspection" if s["system"] == "safety"
                else "platform_model_year_applicability_only"
            ),
            "actual_symptom_reported": False,
            "fault_diagnosed": False,
            "vehicle_repair_approved": False,
        } for s in matching]
        out_rows.append({
            "production_configuration_id": item["id"],
            "model": item["model"],
            "model_year": item["model_year"],
            "platform": item["platform"],
            "engine_code": item["engine_code"],
            "automatic_gears": item["automatic_gears"],
            "applicable_research_checks": entries,
            "has_powertrain_specific_research": any(
                s["system"] in ("engine", "transmission") for s in matching
            ),
            "factory_vehicle_VIN_seen": False,
            "individual_mechanical_condition_verified": False,
            "repair_budget_verified": False,
        })
    counts = [{
        "scenario_id": s["id"],
        "candidate_groups_to_check": sum(
            any(m["scenario_id"] == s["id"] for m in row["applicable_research_checks"])
            for row in out_rows
        ),
        "actual_confirmed_faults": 0,
        "cars_inspected": 0,
    } for s in scenarios]
    return {
        "schema_version": "1.0.0",
        "title": "US Saab factory automatic FWD model-group repair research applicability",
        "provenance": {
            "production": "data/vehicle-catalogue/us-production-normalized.json",
            "feasibility": "data/vehicle-catalogue/us-repair-replace-feasibility.json",
        },
        "scope_note": "Every count is a distinct source-derived MODEL CONFIGURATION, not a faulty vehicle, vehicle population, durability score, or diagnosed problem. Unknowns are not failed systems.",
        "scenario_coverage": counts,
        "model_groups": out_rows,
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    production = json.loads(PRODUCTION_PATH.read_text(encoding="utf-8"))
    feasibility = json.loads(FEASIBILITY_PATH.read_text(encoding="utf-8"))
    payload = json.dumps(build(production, feasibility), indent=2, ensure_ascii=False) + "\n"
    if args.check:
        if not OUT.exists() or OUT.read_text(encoding="utf-8") != payload:
            raise SystemExit("US repair-feasibility coverage index is stale")
        print("US repair feasibility coverage is reproducible.")
    else:
        OUT.write_text(payload, encoding="utf-8")
        print("Generated research-application index for 110 US Saab model groups.")

if __name__ == "__main__":
    main()
