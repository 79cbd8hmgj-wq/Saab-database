#!/usr/bin/env python3
"""Validate decision completeness of the 9440 B207/FA57 engineering dossier.

Separate decision support from factory failure incidence, universal OEM fitment,
model scores or proved longevity. This checks structure and existing-ID reuse,
not the external technical truth of each linked manufacturer document.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

from database import ROOT, load_datasets, validate_datasets

DOSSIER = ROOT / "data/engineering-dossiers/ng93-b207-purchase-engineering-20261014.json"
REPORT = ROOT / "docs/research/ng93-b207-powertrain-engineering-batch-20261014.md"
WORKSHEET = ROOT / "docs/research/ng93-b207-2003-2011-buyer-inspection-worksheet.md"
VALID_DISPOSITIONS = {
    "avoid_major_unpriced_work", "inspect_before_negotiation",
    "repair_if_confirmed", "source_scope_only",
}
EXPECTED_IDS = {
    "B207-01", "B207-02", "B207-03", "B207-04", "B207-05",
    "T8-01", "T8-02", "KEY-01", "KEY-02", "FA57-01", "FA57-02",
    "CHASSIS-01", "CHASSIS-02"
}
NECESSARY_FIELDS = {
    "id","system","concern","applies","failure","purchase_decision",
    "buyer_checks","corrective_path","repair_class","improvement_status",
    "cost_basis","unresolved","prior_ids","sources"
}


def check(dossier: dict, datasets: list[dict], tier: dict) -> dict:
    original_errors=validate_datasets(datasets)
    if original_errors:
        raise ValueError("Existing technical data validation failed")
    existing_ids={r["id"] for d in datasets
                  for kind in ("sources","facts","issues","parts","gaps") for r in d[kind]}
    existing_ids.update(x["id"] for x in tier["failure_modes"])
    cases=dossier["cases"]
    actual_ids=[x.get("id") for x in cases]
    if set(actual_ids)!=EXPECTED_IDS or len(actual_ids)!=len(set(actual_ids)):
        raise ValueError("Dossier must review the complete fixed 13-case powertrain/safety scope")
    if dossier["scope"]["model_year_range"]!=[2003,2011] or dossier["scope"]["engine_family"].find("B207")<0:
        raise ValueError("Wrong platform/engine scope")
    if not {"US","CA"}<=set(dossier["scope"]["markets"]):
        raise ValueError("Must preserve US/CA market restrictions")
    if not any("old-generation" in x for x in dossier["scope"]["boundaries"]):
        raise ValueError("Must distinguish the 2003 OG 9-3 convertible")
    for c in cases:
        if set(c)!=NECESSARY_FIELDS:
            raise ValueError("Missing/extra decision field "+c["id"])
        if c["purchase_decision"] not in VALID_DISPOSITIONS:
            raise ValueError("Unknown repair/buying decision "+c["id"])
        for field in ("system","concern","applies","failure","corrective_path",
                      "repair_class","improvement_status","cost_basis"):
            if not isinstance(c[field],str) or len(c[field].strip())<15:
                raise ValueError("Empty substantive case text "+c["id"]+" "+field)
        for field in ("buyer_checks","unresolved","sources"):
            if not isinstance(c[field],list) or len(c[field]) < (2 if field!="sources" else 1):
                raise ValueError("Missing buyer/uncertainty/source evidence "+c["id"]+" "+field)
        if not all(x.strip() and len(x)>=20 for x in c["buyer_checks"]):
            raise ValueError("Buyer tests cannot be labels only: "+c["id"])
        if not all(x.strip() and len(x)>=20 for x in c["unresolved"]):
            raise ValueError("Unknowns must be explicit: "+c["id"])
        for source_url in c["sources"]:
            p=urlparse(source_url)
            if p.scheme!="https" or not p.netloc or p.netloc not in {
                "saabwisonline.com","www.engineprofessional.com","www.fcpeuro.com",
                "saabparts.com","parts.gmparts.com","webshop-fi.saabparts.com",
                "parts.chevrolet.com","www.esaabparts.com","velectronix.com",
                "www.modernclassicsaab.com"
            }:
                raise ValueError("Invalid/unreviewed external citation "+c["id"]+" "+source_url)
        for old in c["prior_ids"]:
            if old not in existing_ids:
                raise ValueError("Stale/nonexistent original cross-reference "+c["id"]+": "+old)
    for id_ in ("B207-01","B207-02","FA57-01","CHASSIS-02"):
        if next(x for x in cases if x["id"]==id_)["purchase_decision"]!="avoid_major_unpriced_work":
            raise ValueError("Cannot silently weaken safety/internal rebuild buying gate: "+id_)
    for id_ in ("B207-01","B207-03","T8-02","FA57-01"):
        claim=next(x for x in cases if x["id"]==id_)["improvement_status"]
        if "proven_permanent" in claim or "guaranteed" in claim:
            raise ValueError("Do not assert unverified longevity/permanent upgrade")
    for wanted in ("engine_timing_valvetrain","cooling_heat","turbo_intake_boost",
                   "ecu_immobilizer_security","transmission_driveline",
                   "steering_suspension","body_corrosion_mounts"):
        if wanted not in {x["system"] for x in cases}:
            raise ValueError("Missing entire vehicle subsystem "+wanted)
    if not {"before_travel","on_site_if_safe","never_drive_without_professional_clearance",
            "final_document"}==set(dossier["buyer_protocol"]):
        raise ValueError("Incomplete buyer decision workflow")
    for name,items in dossier["buyer_protocol"].items():
        if len(items)<3:
            raise ValueError("Too few buyer decision checks "+name)
    if not REPORT.is_file() or not WORKSHEET.is_file():
        raise ValueError("Both readable report and practical worksheet required")
    r=REPORT.read_text(encoding="utf-8")
    w=WORKSHEET.read_text(encoding="utf-8")
    if any(x["id"] not in r for x in cases):
        raise ValueError("Not all decision cases in readable report")
    for required in ("55563529","12630084","32021815","TA248-0336",
                     "TA440-0702","365-2568","731-2726"):
        if required not in r:
            raise ValueError("Major primary document or service part missing in narrative")
    if not all(x in w for x in ("VIN","compression","CIM","FA57","subframe","total","Total")):
        raise ValueError("Worksheet not a practical buying/repair test")
    if not any("no factory" in x.lower() or "no saab model" in x.lower()
               for x in dossier["limits"]):
        raise ValueError("No safe failure-frequency/model-ranking evidence boundary")
    return {
        "cases":len(cases),
        "by_system":dict(Counter(x["system"] for x in cases)),
        "buying_disposition":dict(Counter(x["purchase_decision"] for x in cases)),
        "source_URL_references":len({url for c in cases for url in c["sources"]}),
        "case_original_reference_links":sum(len(c["prior_ids"]) for c in cases),
        "documents":["docs/research/ng93-b207-powertrain-engineering-batch-20261014.md",
                     "docs/research/ng93-b207-2003-2011-buyer-inspection-worksheet.md"],
        "not_a_failure_rate_or_model_ranking":True,
    }


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check",action="store_true")
    parser.add_argument("--summary",action="store_true")
    args=parser.parse_args()
    report=check(
        json.loads(DOSSIER.read_text(encoding="utf-8")),
        load_datasets(),
        json.loads((ROOT/"data/tier-research/observations.json").read_text(encoding="utf-8"))
    )
    if args.summary:
        print(json.dumps(report,indent=2))
    if args.check:
        print("PASS: complete 13-case B207/FA57 decision dossier, documented buyer gates, "
              "existing source links, worksheet, and no false reliability rankings.")
    if not args.check and not args.summary:
        parser.print_help()
    return 0


if __name__=="__main__":
    raise SystemExit(main())
