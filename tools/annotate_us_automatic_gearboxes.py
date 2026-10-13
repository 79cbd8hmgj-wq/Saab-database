#!/usr/bin/env python3
"""Overlay Saab WIS transmission-family *research evidence* on US production groups.

Never equate a platform family designation with a VIN-approved replacement,
and never turn a gear count into an invented factory gearbox code.
"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRODUCTION = ROOT / "data/vehicle-catalogue/us-production-normalized.json"
OUTPUT = ROOT / "data/vehicle-catalogue/us-automatic-gearbox-evidence.json"

SOURCES = [
    {"id": "wis-9400-2001-automatic-type", "title": "9-3 9400 MY2001 type designation, gearbox",
     "url": "https://saabwisonline.com/9-3-9400/2001/4-transmission/automatic-transmission/technical-data/type-designation-gearbox",
     "publisher": "Saab WIS, mirrored", "source_model_year": 2001,
     "scope_note": "Factory WIS identifies AF20 and AF22 four-speed families; FA44 is an example type code, not a universal application."},
    {"id": "wis-9600-2000-af30", "title": "9-5 9600 MY2000 automatic AF30 / FA47",
     "url": "https://saabwisonline.com/9-5-9600/2000/4-transmission/automatic-transmission/technical-data/type-designation",
     "publisher": "Saab WIS, mirrored", "source_model_year": 2000,
     "scope_note": "WIS identifies AF30 4-speed, factory type designation example FA47 and gearbox model 50-40LE. Source is MY2000."},
    {"id": "wis-9600-2008-fa57", "title": "9-5 9600 MY2008 FA57 type designation",
     "url": "https://saabwisonline.com/9-5-9600/2008/4-transmission/automatic-transmission/technical-data/type-designation",
     "publisher": "Saab WIS, mirrored", "source_model_year": 2008,
     "scope_note": "WIS states original 9-5 automatic from MY2002 has FA57 designation; not a 9-3 interchange permission."},
    {"id": "wis-9440-2006-fa57", "title": "9-3 9440 MY2006 FA57 type designations",
     "url": "https://saabwisonline.com/9-3-9440/2006/4-transmission/automatic-transmission/5-speed-fa-57/technical-data/type-designations",
     "publisher": "Saab WIS, mirrored", "source_model_year": 2006,
     "scope_note": "WIS says 9-3 9440 B207 automatic from MY2003 uses FA57; TCM engine adaptation codes differ."},
    {"id": "wis-9440-2006-af40", "title": "9-3 9440 MY2006 AF40 six-speed type designations",
     "url": "https://saabwisonline.com/9-3-9440/2006/4-transmission/automatic-transmission/6-speed-af-40/technical-data/type-designations",
     "publisher": "Saab WIS, mirrored", "source_model_year": 2006,
     "scope_note": "WIS designates six-speed as AF40 / Aisin TF-80SC; cannot assume identical boxed assemblies for other cars."},
    {"id": "wis-9440-af40-low-atf", "title": "TA440-0902 AF40 ATF level technical advice",
     "url": "https://saabwisonline.com/9-3-9440/2006/4-transmission/automatic-transmission/6-speed-af-40/bulletins-si-mi/ta440-0902-atf-oil-check-on-af40-6-speed-aut",
     "publisher": "Saab technical advice mirrored by WIS", "source_model_year": 2006,
     "scope_note": "January 2009 bulletin: low ATF can produce delayed shifts; use original fluid/temperature procedures and Tech2. Not automatic proof of a failed transmission."},
    {"id": "wis-9440-fa57-adaptation", "title": "9-3 9440 FA57 adaptation reset procedure",
     "url": "https://saabwisonline.com/9-3-9440/2006/4-transmission/automatic-transmission/5-speed-fa-57/adjustment-replacement/adaptation-resetting",
     "publisher": "Saab WIS, mirrored", "source_model_year": 2006,
     "scope_note": "Saab requires Tech2 reset/re-adaptation after certain transmission, TCM or software changes. Never reset as a substitute for fault diagnosis."},
    {"id": "wis-9600-fa57-solenoids", "title": "9-5 9600 FA57 2004 hydraulic pressure solenoids",
     "url": "https://saabwisonline.com/9-5-9600/2004/4-transmission/automatic-transmission/technical-description/solenoid-valves-sls-and-slt-for-system-pressure",
     "publisher": "Saab WIS, mirrored", "source_model_year": 2004,
     "scope_note": "P0748 (SLT) and P0785 (SLS) documented limp-home faults; diagnosis required before deciding on transmission replacement."},
]

RULES = {
    ("9400", 4): {"designation": "AF20 / AF22", "state": "alternative_families_not_vehicle_resolved",
                  "source": "wis-9400-2001-automatic-type", "identity_notes": "FA44 example appears in MY2001 factory type-code description; AF20 vs AF22 not assigned to individual groups."},
    ("9600", 4): {"designation": "AF30", "state": "factory_family_platform_supported",
                  "source": "wis-9600-2000-af30", "identity_notes": "WIS 2000 AF30; FA47 type example. Extend to 1999 and 2001 compiled 4AT era provisionally, not certified on each year/VIN."},
    ("9600", 5): {"designation": "FA57", "state": "factory_family_platform_supported",
                  "source": "wis-9600-2008-fa57", "identity_notes": "WIS MY2008 states from MY2002 original 9-5 uses FA57; exact variant and part number unknown."},
    ("9440", 5): {"designation": "FA57", "state": "factory_family_platform_supported",
                  "source": "wis-9440-2006-fa57", "identity_notes": "WIS says 9440 FA57 from MY2003 for B207. No cross-platform fitment proof."},
    ("9440", 6): {"designation": "AF40 / TF-80SC", "state": "factory_family_platform_supported",
                  "source": "wis-9440-2006-af40", "identity_notes": "WIS six-speed AF40 / Aisin TF-80SC; current US candidate subset is 2006–2008 FWD B284L, not all Saab six-speeds."},
    ("650", 6): {"designation": None, "state": "factory_family_unresolved",
                 "source": None, "identity_notes": "2011 new 9-5 Turbo4 FWD 6AT confirmed in register, but factory physical transmission family still needs a direct manufacturer citation."},
}
CAUTIONS = [
    {"id": "at-risk-fa57-interchange",
     "claim": "FA57 label exists on both original 9-5 9600 and 9-3 9440.",
     "decision": "Do NOT claim interchangeability, identical application calibration, donor compatibility or fluid spec across platforms.",
     "source_ids": ["wis-9600-2008-fa57", "wis-9440-2006-fa57"]},
    {"id": "at-screen-af40-low-atf",
     "claim": "Saab technical advice connects low AF40 ATF level to delayed gear engagement/shift.",
     "decision": "Before classifying a delayed-shift AF40 vehicle as needing a rebuild, obtain Tech2 readings and professional fluid-level/temperature assessment to the exact WIS procedure.",
     "source_ids": ["wis-9440-af40-low-atf"]},
    {"id": "at-screen-9440-fa57-tcm-adaptation",
     "claim": "Saab WIS instructs Tech2 adaptation after transmission, TCM or software changes for 9440 FA57.",
     "decision": "Investigate calibration/adaptation history and codes before diagnosing internal gearbox failure. Do not claim all hard shifts are adaptive.",
     "source_ids": ["wis-9440-fa57-adaptation"]},
    {"id": "at-screen-9600-fa57-solenoids",
     "claim": "2004 WIS links SLT/SLS pressure solenoid faults to P0748/P0785 and limp-home.",
     "decision": "Read transmission DTCs, wiring and solenoid fault procedures before declaring the entire gearbox damaged.",
     "source_ids": ["wis-9600-fa57-solenoids"]},
]


def build(production):
    if production.get("markets") != ["US"]:
        raise ValueError("Only the separately normalized US production catalogue may be annotated")
    known_ids = {s["id"] for s in SOURCES}
    groups = []
    for item in production["configurations"]:
        if item["market"] != "US" or item["drivetrain"] != "FWD" or item["automatic_gears"] not in (4, 5, 6):
            raise ValueError("Ineligible US production input " + item["id"])
        key = (item["platform"], item["automatic_gears"])
        if key not in RULES:
            raise ValueError("Unreviewed factory platform/gear combination: " + str(key))
        rule = RULES[key]
        sid = [rule["source"]] if rule["source"] else []
        if not set(sid).issubset(known_ids):
            raise ValueError("Unknown evidence source")
        groups.append({
            "production_configuration_id": item["id"],
            "model_year": item["model_year"],
            "model": item["model"],
            "platform": item["platform"],
            "engine_code": item["engine_code"],
            "gear_count": item["automatic_gears"],
            "gearbox_family": rule["designation"],
            "evidence_state": rule["state"],
            "source_ids": sid,
            "identity_notes": rule["identity_notes"],
            "vehicle_vin_verified": False,
            "oem_interchange_approved": False,
            "durability_improvement_proven": False,
        })
    return {
        "schema_version": "1.0.0",
        "purpose": "Source-scoped Saab factory automatic family identification overlay on independently compiled US production groups; not original VIN validation or interchange approval.",
        "source_production_catalogue": "data/vehicle-catalogue/us-production-normalized.json",
        "research_sources": SOURCES,
        "diagnostic_cautions": CAUTIONS,
        "annotations": groups,
        "research_status": "factory_family_research_partial; exact model-year variants/VIN, parts and 650 gearbox unresolved",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    production = json.loads(PRODUCTION.read_text(encoding="utf-8"))
    generated = json.dumps(build(production), indent=2, ensure_ascii=False) + "\n"
    if args.check:
        if not OUTPUT.exists() or OUTPUT.read_text(encoding="utf-8") != generated:
            raise SystemExit("Factory gearbox evidence overlay stale: rerun annotator")
        print("Factory gearbox evidence overlay matches source production snapshot.")
    else:
        OUTPUT.write_text(generated, encoding="utf-8")
        print("Generated US factory family evidence overlay.")


if __name__ == "__main__":
    main()
