#!/usr/bin/env python3
"""Audit gaps in U.S. Saab repair-feasibility coverage without scoring reliability.

Uses the existing, merged 110-group production universe, 14 scenario matrix,
and source-scoped WIS gearbox overlay. Counts are distinct *configurations*,
never failure events, inspected VINs, cost estimates or available vehicles.
"""
import argparse
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROD = ROOT / "data/vehicle-catalogue/us-production-normalized.json"
FEAS = ROOT / "data/vehicle-catalogue/us-repair-replace-feasibility.json"
COVER = ROOT / "data/vehicle-catalogue/us-feasibility-coverage.json"
GEAR = ROOT / "data/vehicle-catalogue/us-automatic-gearbox-evidence.json"
OUT = ROOT / "data/audits/us-feasibility-powertrain-gaps.json"

def build(production, feasibility, coverage, gearboxes):
    configs = {c["id"]: c for c in production["configurations"]}
    scenarios = {s["id"]: s for s in feasibility["scenarios"]}
    gearbox = {x["production_configuration_id"]: x
               for x in gearboxes["annotations"]}
    rows = coverage["production_group_reviews"]
    if production.get("markets") != ["US"] or coverage.get("market") != "US":
        raise ValueError("This research audit is U.S.-only")
    if len(configs) != 110 or len(rows) != 110 or len(gearbox) != 110:
        raise ValueError("Unreconciled source or coverage denominator")
    if set(configs) != {x["production_id"] for x in rows} or set(configs) != set(gearbox):
        raise ValueError("Production, scenario coverage and gearbox IDs disagree")
    out = []
    for row in rows:
        p = configs[row["production_id"]]
        linked = [scenarios[x["scenario_id"]] for x in row["scenario_links"]]
        engine_core = any(s["system"] == "engine" for s in linked)
        transmission = any(s["system"] == "transmission" for s in linked)
        chassis = any(s["system"] == "structure" for s in linked)
        safety = any(s["system"] == "safety" for s in linked)
        out.append({
            "production_configuration_id": row["production_id"],
            "model_year": p["model_year"],
            "model": p["model"],
            "platform": p["platform"],
            "trim": p["trim"],
            "body_style": p["body_style"],
            "engine_label": p["engine_label"],
            "engine_code": p["engine_code"],
            "automatic_gears": p["automatic_gears"],
            "workshop_gearbox_family": gearbox[p["id"]]["gearbox_family"],
            "applicable_scenario_ids": [s["id"] for s in linked],
            "engine_core_failure_and_repair_scenario_present": engine_core,
            "transmission_failure_and_repair_scenario_present": transmission,
            "structural_repair_scenario_present": chassis,
            "general_safety_screen_present": safety,
            "neither_engine_nor_transmission_scenario": not engine_core and not transmission,
            "vehicle_VIN_or_condition_verified": False,
            "repair_price_or_rate_established": False,
        })
    if not all(x["general_safety_screen_present"] for x in out):
        raise ValueError("Lost mandatory general brake/fuel screening")
    dimensions = {
        "missing_engine_core_repair_scenario": "engine_core_failure_and_repair_scenario_present",
        "missing_transmission_repair_scenario": "transmission_failure_and_repair_scenario_present",
        "missing_structural_repair_scenario": "structural_repair_scenario_present",
        "missing_both_engine_and_transmission_scenarios": "neither_engine_nor_transmission_scenario",
    }
    missing = {}
    for name, flag in dimensions.items():
        subset = [x for x in out if (x[flag] if name.startswith("missing_both")
                                    else not x[flag])]
        missing[name] = {
            "configuration_count": len(subset),
            "production_configuration_ids": [x["production_configuration_id"] for x in subset],
        }
    grouped = {}
    for name, keyname, subset_name in [
        ("engine_core", "engine_code", "missing_engine_core_repair_scenario"),
        ("transmission", "workshop_gearbox_family", "missing_transmission_repair_scenario"),
    ]:
        subset = set(missing[subset_name]["production_configuration_ids"])
        counts = defaultdict(lambda: {"count": 0, "years": set()})
        for x in out:
            if x["production_configuration_id"] not in subset:
                continue
            family = x[keyname] or x["engine_label"]
            key = (x["platform"], family, x["automatic_gears"]) if name == "transmission" else (x["platform"], family)
            counts[key]["count"] += 1
            counts[key]["years"].add(x["model_year"])
        grouped[name] = [
            {"platform": k[0], "family_or_engine": k[1],
             "automatic_gears": k[2] if name == "transmission" else None,
             "unreviewed_configurations": v["count"],
             "years": sorted(v["years"])}
            for k, v in sorted(counts.items())
        ]
    return {
        "schema_version": "1.0.0",
        "purpose": "Research completeness audit; not a vehicle condition, frequency, cost or reliability ranking",
        "markets": ["US"],
        "input_paths": [
            "data/vehicle-catalogue/us-production-normalized.json",
            "data/vehicle-catalogue/us-repair-replace-feasibility.json",
            "data/vehicle-catalogue/us-feasibility-coverage.json",
            "data/vehicle-catalogue/us-automatic-gearbox-evidence.json",
        ],
        "production_configuration_denominator": len(out),
        "scenario_denominator": len(scenarios),
        "counts_are": "configuration groups in compiled US production table, NOT inspected cars, produced units or failed systems",
        "missing": missing,
        "grouped_missing_research": grouped,
        "configurations": out,
        "all_factory_vehicle_VINs_verified": False,
        "all_priced_repair_options_verified": False,
        "phase0_gates_unchanged": True,
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    values = [json.loads(p.read_text(encoding="utf-8"))
              for p in (PROD, FEAS, COVER, GEAR)]
    result = json.dumps(build(*values), indent=2, ensure_ascii=False) + "\n"
    if args.check:
        if not OUT.exists() or OUT.read_text(encoding="utf-8") != result:
            raise SystemExit("Gap audit is stale; regenerate from current scenario/production sources")
        print("U.S. powertrain repair-coverage gap audit reproducible.")
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(result, encoding="utf-8")
        print("Generated U.S. powertrain repair-coverage gap audit.")

if __name__ == "__main__":
    main()
