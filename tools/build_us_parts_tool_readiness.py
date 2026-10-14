#!/usr/bin/env python3
"""Rebuild conservative Saab US parts/tools/quote research applicability.

A factory workshop example for MY2006 is a *lead* on MY2003 or MY2011.
Neither a matched model year nor an FA57/AF40 family name approves part fit.
"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROD = ROOT / "data/vehicle-catalogue/us-production-normalized.json"
PLAN = ROOT / "data/vehicle-catalogue/us-parts-tool-readiness.json"
OUT = ROOT / "data/audits/us-parts-tool-readiness-coverage.json"

def applies(config, packet):
    match = packet["match"]
    return (
        config["platform"] == match["platform"]
        and config["automatic_gears"] in match["automatic_gears"]
        and match["model_year_range"][0] <= config["model_year"]
        <= match["model_year_range"][1]
        and ("engine_codes" not in match
             or config["engine_code"] in match["engine_codes"])
    )

def build(production, plans):
    if production.get("markets") != ["US"] or plans["scope"]["market"] != "US":
        raise ValueError("This index covers compiled US candidates only")
    srcs = {x["id"]: x for x in plans["source_records"]}
    if len(srcs) != len(plans["source_records"]):
        raise ValueError("Duplicate readiness source IDs")
    packet_ids = [x["id"] for x in plans["job_packets"]]
    if len(packet_ids) != len(set(packet_ids)):
        raise ValueError("Duplicate job packet ID")
    for packet in plans["job_packets"]:
        years = packet["match"]["model_year_range"]
        if len(years) != 2 or years[0] > years[1]:
            raise ValueError("Invalid application model-year range " + packet["id"])
        for sid in packet["evidence_source_ids"]:
            if sid not in srcs or srcs[sid]["platform"] != packet["match"]["platform"]:
                raise ValueError("Missing or cross-platform WIS source in " + packet["id"])
        if (packet["estimate_usd"] is not None
                or packet["required_shop_labor_hours"] is not None
                or not packet["required_tools_or_capabilities"]
                or not packet["vin_rpo_case_gates"]):
            raise ValueError("Unsupported price or omitted safeguards " + packet["id"])
        # A historical parts-store display is not a current installed quote.
        if "historical_advertised_part_price_usd" in packet:
            if not packet.get("historical_observed_date") or not packet.get("retail_source_ids"):
                raise ValueError("Dated retail evidence incomplete " + packet["id"])
    if any(plans["guardrails"].values()):
        raise ValueError("A false part, VIN or budget approval was promoted")

    rows = []
    for c in production["configurations"]:
        if c["market"] != "US" or c["drivetrain"] != "FWD":
            raise ValueError("Out-of-scope compiled production entry " + c["id"])
        leads = []
        for packet in plans["job_packets"]:
            if not applies(c, packet):
                continue
            status = (
                "source_model_year_matched_still_VIN_unverified"
                if c["model_year"] == packet["factory_example_year"]
                else "adjacent_year_research_lead_not_repair_approval")
            leads.append({
                "job_id": packet["id"],
                "evidence_year": packet["factory_example_year"],
                "source_applicability_state": status,
                "vin_and_part_fitment_confirmed": False,
                "special_tool_access_confirmed": False,
                "shop_quote_obtained": False,
            })
        rows.append({
            "production_configuration_id": c["id"],
            "platform": c["platform"],
            "model_year": c["model_year"],
            "body_style": c["body_style"],
            "engine_code": c["engine_code"],
            "automatic_gears": c["automatic_gears"],
            "job_readiness_leads": leads,
            "actual_vehicle_inspected": False,
            "repair_authorized": False,
        })
    counts = []
    for packet in plans["job_packets"]:
        matching = [lead for row in rows for lead in row["job_readiness_leads"]
                    if lead["job_id"] == packet["id"]]
        counts.append({
            "job_id": packet["id"],
            "matching_production_configuration_groups": len(matching),
            "matching_model_year_source_examples": sum(
                m["source_applicability_state"] ==
                "source_model_year_matched_still_VIN_unverified" for m in matching),
            "physical_vins_verified": 0,
            "part_fitment_approved": 0,
            "current_install_cost_quotes": 0,
        })
        if not matching:
            raise ValueError("Unmatched job packet " + packet["id"])
    return {
        "schema_version": "1.0.0",
        "source_production": "data/vehicle-catalogue/us-production-normalized.json",
        "source_job_packets": "data/vehicle-catalogue/us-parts-tool-readiness.json",
        "denominator_source_compiled_us_automatic_fwd_groups": len(rows),
        "interpretation": "Counts are research job leads for normalized configurations, not actual vehicles or confirmed repair application; example-year matches do not verify VIN or donor interchange.",
        "job_coverage": counts,
        "production_groups": rows,
        "no_parts_fitment_approved": True,
        "no_actual_vehicle_verified": True,
        "no_installed_repair_prices": True,
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    production = json.loads(PROD.read_text(encoding="utf-8"))
    plans = json.loads(PLAN.read_text(encoding="utf-8"))
    result = json.dumps(build(production, plans), indent=2, ensure_ascii=False) + "\n"
    if args.check:
        if not OUT.exists() or OUT.read_text(encoding="utf-8") != result:
            raise SystemExit("Parts/tool research index stale or inconsistent")
        print("Source-scoped parts/tool job index matches 110 US groups.")
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(result, encoding="utf-8")
        print("Generated source-scoped parts/tool research index.")

if __name__ == "__main__":
    main()
