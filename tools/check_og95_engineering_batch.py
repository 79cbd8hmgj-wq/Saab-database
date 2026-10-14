#!/usr/bin/env python3
"""Validate the 20-case OG 9-5 buyer dossier's structure and existing source links.

This is not verification of factory engineering truth, real VIN fitment or lifespan.
"""
from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/engineering-dossiers/og95-b205-b235-purchase-engineering-20261014.json"
REPORT = ROOT / "docs/research/og95-b205-b235-complete-purchase-dossier-20261014.md"
WORKSHEET = ROOT / "docs/research/og95-b205-b235-buyer-inspection-worksheet-20261014.md"
REQUIRED = {"id", "system", "concern", "applies", "failure", "purchase_decision",
            "buyer_checks", "corrective_path", "repair_class", "improvement_status",
            "cost_basis", "unresolved", "prior_ids", "sources"}

def validate() -> int:
    doc = json.loads(DATA.read_text(encoding="utf-8"))
    cases = doc["cases"]
    assert len(cases) == 20, "Expected 20 independently reviewed cases"
    assert [c["id"] for c in cases] == [f"O95-{i:02d}" for i in range(1, 21)]
    assert doc["scope"]["platform"] == "9-5-9600"
    assert "B205" in doc["scope"]["engine_family"] and "B235" in doc["scope"]["engine_family"]
    assert set(doc["scope"]["markets"]) >= {"US", "CA"}
    report = REPORT.read_text(encoding="utf-8")
    worksheet = WORKSHEET.read_text(encoding="utf-8")
    valid_old_ids = set()
    for f in (ROOT / "data/datasets").glob("*.json"):
        dataset = json.loads(f.read_text(encoding="utf-8"))
        for category in ("sources", "facts", "issues", "parts", "gaps"):
            valid_old_ids.update(x["id"] for x in dataset.get(category, []))
    for c in cases:
        assert set(c) == REQUIRED, f"Bad record shape: {c['id']}"
        assert all(isinstance(c[k], str) and c[k].strip()
                   for k in ("system", "concern", "applies", "failure", "purchase_decision",
                             "corrective_path", "repair_class", "improvement_status", "cost_basis"))
        assert len(c["buyer_checks"]) >= 2 and len(c["unresolved"]) >= 2 and len(c["sources"]) >= 1
        for old_id in c["prior_ids"]:
            assert old_id in valid_old_ids, f"Unresolved old ID: {c['id']} {old_id}"
        for src in c["sources"]:
            u = urlsplit(src)
            assert u.scheme == "https" and u.netloc, f"Invalid source URL: {c['id']} {src}"
        assert c["id"] in report, f"Report missing {c['id']}"
    for phrase in ("VIN", "subframe", "transmission", "cost"):
        assert phrase.lower() in worksheet.lower(), f"Worksheet missing: {phrase}"
    assert "failure rate" in report.lower()
    assert all(key in doc["buyer_protocol"] for key in
               ("before_travel", "on_site_if_safe", "never_drive_without_professional_clearance", "final_document"))
    print("PASS: 20 original 9-5 buyer/repair cases, report, worksheet, source URLs and original IDs checked.")
    print("This does NOT prove engineering accuracy, measured failure rates or authorized part fitment.")
    return 0

if __name__ == "__main__":
    raise SystemExit(validate())
