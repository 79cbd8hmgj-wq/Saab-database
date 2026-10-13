#!/usr/bin/env python3
"""Map sourced repair/replace scenarios to eligible US Saab production configurations.

This is an applicability *research index*; it is not evidence any specific
vehicle has a fault, evidence of fault prevalence, cost, or parts fitment.
Only standard library is needed.
"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRODUCTION = ROOT / "data/vehicle-catalogue/us-production-normalized.json"
SCENARIOS = ROOT / "data/vehicle-catalogue/us-repair-replace-feasibility.json"
OUTPUT = ROOT / "data/vehicle-catalogue/us-feasibility-coverage.json"


def scenario_applies(group, scenario):
    filt = scenario["applicability"]
    if group["platform"] not in filt["platforms"]:
        return False
    if "engine_codes" in filt and group["engine_code"] not in filt["engine_codes"]:
        return False
    if "automatic_gears" in filt and group["automatic_gears"] not in filt["automatic_gears"]:
        return False
    yrange = filt.get("model_year_range_by_platform", {}).get(group["platform"])
    if yrange is not None and not (yrange[0] <= group["model_year"] <= yrange[1]):
        return False
    if "body_styles" in filt and group["body_style"] not in filt["body_styles"]:
        return False
    return True


def build(production, matrix):
    if production["markets"] != ["US"] or matrix["market"] != "US":
        raise ValueError("Coverage must be restricted to the US vehicle population")
    source_by_id = {s["id"]: s for s in matrix["source_records"]}
    if len(source_by_id) != len(matrix["source_records"]):
        raise ValueError("Duplicate evidence source ID")
    scenario_ids = set()
    for s in matrix["scenarios"]:
        if s["id"] in scenario_ids:
            raise ValueError("Duplicate scenario ID: " + s["id"])
        scenario_ids.add(s["id"])
        if not s["evidence_source_ids"] or any(ref not in source_by_id for ref in s["evidence_source_ids"]):
            raise ValueError("Missing source link in " + s["id"])
        if s["price_estimate_usd"] is not None or s["labor_hours_estimate"] is not None:
            raise ValueError("Unverified numeric repair cost or labor estimate: " + s["id"])
        if any((s["part_interchange_approved"], s["rate_of_failure_established"], s["individual_vehicle_inspected"])):
            raise ValueError("Unsupported approval in " + s["id"])
        f = s["applicability"]
        if not f["platforms"] or any(p not in ("9400", "9440", "9600", "650") for p in f["platforms"]):
            raise ValueError("Invalid platform scope: " + s["id"])
        for key, r in f.get("model_year_range_by_platform", {}).items():
            if key not in f["platforms"] or not (len(r) == 2 and 1998 <= r[0] <= r[1] <= 2011):
                raise ValueError("Invalid year range in " + s["id"])
    associations = []
    count_by_scenario = {s["id"]: 0 for s in matrix["scenarios"]}
    ids = set()
    for v in production["configurations"]:
        if v["id"] in ids:
            raise ValueError("Duplicate production configuration")
        ids.add(v["id"])
        if v["market"] != "US" or v["drivetrain"] != "FWD" or v["automatic_gears"] not in (4, 5, 6) or v["body_code"] == "CV":
            raise ValueError("Out-of-scope production group")
        matches = []
        for s in matrix["scenarios"]:
            if scenario_applies(v, s):
                matches.append({
                    "scenario_id": s["id"],
                    "applicability_status": "scope_match_only_not_fault_diagnosis",
                    "additional_vehicle_vin_gate": s["applicability"].get("vin_gate"),
                    "actual_fault_confirmed": False,
                    "replacement_authorized": False,
                })
                count_by_scenario[s["id"]] += 1
        associations.append({
            "production_id": v["id"],
            "model": v["model"], "platform": v["platform"],
            "model_year": v["model_year"], "engine_code": v["engine_code"],
            "automatic_gears": v["automatic_gears"], "body_style": v["body_style"],
            "scenario_links": matches,
            "individual_vehicle_inspection_completed": False,
            "price_or_kit_confirmed": False,
        })
    if any(n == 0 for n in count_by_scenario.values()):
        raise ValueError("At least one scenario scope has no actual eligible US production groups")
    return {
        "schema_version": "1.0.0",
        "source_production_catalogue": "data/vehicle-catalogue/us-production-normalized.json",
        "source_feasibility_scenarios": "data/vehicle-catalogue/us-repair-replace-feasibility.json",
        "meaning": "Applicability crosswalk, not observed failure cases or verified parts or price scores",
        "market": "US",
        "counts": {
            "production_groups": len(associations),
            "source_linked_scenarios": len(matrix["scenarios"]),
            "matching_links_by_scenario": count_by_scenario,
            "individual_vehicles_inspected": 0,
            "failure_rates_quantified": 0,
            "repair_prices_verified": 0,
            "parts_interchanges_approved": 0,
        },
        "production_group_reviews": associations,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    production = json.loads(PRODUCTION.read_text(encoding="utf-8"))
    matrix = json.loads(SCENARIOS.read_text(encoding="utf-8"))
    text = json.dumps(build(production, matrix), indent=2, ensure_ascii=False) + "\n"
    if args.check:
        if not OUTPUT.exists() or OUTPUT.read_text(encoding="utf-8") != text:
            raise SystemExit("Outdated feasibility scope crosswalk: run without --check")
        print("US repair/replace feasibility coverage is current and source-scoped.")
    else:
        OUTPUT.write_text(text, encoding="utf-8")
        print("Wrote US repair/replace feasibility coverage.")


if __name__ == "__main__":
    main()
