#!/usr/bin/env python3
"""Rebuild a U.S.-market automatic/FWD Saab production-candidate snapshot.

Input: the four eSaabParts *compiled* U.S. production tables. These are
third-party production research, not original Saab VIN/build certificates.
Color rows are grouped by (platform, year, trim, body, drive, transmission,
engine); manual, convertible, XWD/AWD and non-US rows are never admitted.

No external Python packages required. Network access is used only with --fetch.
"""
from __future__ import annotations

import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.request import Request, urlopen

SOURCE_SPECS = (
    ("9400", "9-3", "9-3_1999_2003.php", "na-cat-usprod-9400",
     ("year", "trim", "body", "trans", "engine", "color", "count")),
    ("9440", "9-3", "9-3_2003_2011.php", "na-cat-usprod-9440",
     ("year", "trim", "body", "drive", "trans", "engine", "color", "count")),
    ("9600", "9-5", "9-5_1999_2009.php", "na-cat-usprod-9600",
     ("year", "trim", "body", "trans", "engine", "color", "count")),
    ("650", "9-5", "9-5_2010_2011.php", "na-cat-usprod-650",
     ("year", "trim", "trans", "drive", "engine", "color", "count")),
)
URL_ROOT = "https://www.esaabparts.com/saab/production/data/"
BODY = {"3D": "3-door hatchback", "5D": "5-door hatchback", "4D": "sedan"}
YEAR_RE = re.compile(r"^(?:19|20)\d\d$")
AT_RE = (re.compile(r"^([456])AT$", re.I),
         re.compile(r"^AT\s+([456])\s*-?\s*Spd$", re.I))
ENGINE_CODE_RE = re.compile(r"^B\d{3}[A-Z]$", re.I)
TOTAL_RE = re.compile(r"Total\s+US\s+Production\s*#:\s*([\d,]+)", re.I)


class RowParser(HTMLParser):
    """Extract all table rows without assuming fixed CSS or JS dependencies."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.rows: list[list[str]] = []
        self._row: list[str] | None = None
        self._cell: list[str] | None = None

    def handle_starttag(self, tag, attrs):
        if tag == "tr":
            self._row = []
        elif tag in ("th", "td") and self._row is not None:
            self._cell = []

    def handle_data(self, data):
        if self._cell is not None:
            self._cell.append(data)

    def handle_endtag(self, tag):
        if tag in ("th", "td") and self._cell is not None:
            if self._row is not None:
                self._row.append(" ".join(" ".join(self._cell).split()))
            self._cell = None
        elif tag == "tr" and self._row is not None:
            if self._row:
                self.rows.append(self._row)
            self._row = None


def gearbox_gears(label: str) -> int | None:
    for regex in AT_RE:
        match = regex.fullmatch(label.strip())
        if match:
            return int(match.group(1))
    return None


def read_table(html: str, spec: tuple) -> dict:
    platform, model, filename, source_id, fields = spec
    parser = RowParser()
    parser.feed(html)
    parsed = []
    for row in parser.rows:
        if not row or not YEAR_RE.fullmatch(row[0]):
            continue
        if len(row) != len(fields):
            raise ValueError(f"{filename}: year row has {len(row)} fields; expected {len(fields)}: {row}")
        item = dict(zip(fields, row))
        if not item["count"].replace(",", "").isdigit():
            raise ValueError(f"{filename}: invalid count: {item}")
        item["count"] = int(item["count"].replace(",", ""))
        item["year"] = int(item["year"])
        parsed.append(item)
    if not parsed:
        raise ValueError(f"{filename}: found no production rows; check source HTML or access restrictions")

    grouped = {}
    filtered_counts = {"manual": 0, "convertible": 0, "awd": 0}
    for item in parsed:
        trans = item["trans"]
        gears = gearbox_gears(trans)
        if gears is None:
            if re.fullmatch(r"(?:[456]MT|MT\s+[456]\s*-?\s*Spd)", trans, re.I):
                filtered_counts["manual"] += item["count"]
                continue
            raise ValueError(f"{filename}: unknown transmission code {trans!r}")
        raw_body = item.get("body", "4D")
        if raw_body == "CV":
            filtered_counts["convertible"] += item["count"]
            continue
        if raw_body not in BODY:
            raise ValueError(f"{filename}: unknown body code {raw_body!r}")
        drive = item.get("drive", "FWD").upper()
        if drive in ("AWD", "XWD", "4WD"):
            filtered_counts["awd"] += item["count"]
            continue
        if drive != "FWD":
            raise ValueError(f"{filename}: unknown drivetrain {drive!r}")
        year = item["year"]
        if not 1998 <= year <= 2011:
            raise ValueError(f"{filename}: year out of candidate scope: {year}")
        normalized_body = "wagon" if platform in ("9440", "9600") and raw_body == "5D" else BODY[raw_body]
        key = (year, item["trim"], raw_body, drive, trans, item["engine"])
        if key not in grouped:
            canonical = "|".join(map(str, (platform, *key)))
            suffix = hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:12]
            engine = item["engine"]
            grouped[key] = {
                "id": f"usprod-{platform}-{year}-{suffix}",
                "market": "US", "model": model, "platform": platform,
                "model_year": year, "trim": item["trim"],
                "body_code": raw_body, "body_style": normalized_body,
                "drivetrain": "FWD", "transmission": trans,
                "automatic_gears": gears, "transmission_code": None,
                "engine_code": engine if ENGINE_CODE_RE.fullmatch(engine) else None,
                "engine_label": engine,
                "reported_production_count": 0,
                "paint_row_count": 0,
                "requires_vehicle_verification": True,
                "source_ids": [source_id],
                "evidence_status": "third_party_compiled_US_production",
            }
        grouped[key]["reported_production_count"] += item["count"]
        grouped[key]["paint_row_count"] += 1

    full_count = sum(item["count"] for item in parsed)
    plain_text = " ".join(re.sub(r"<[^>]+>", " ", html).split())
    match = TOTAL_RE.search(plain_text)
    declared = int(match.group(1).replace(",", "")) if match else None
    return {
        "source": {"id": source_id, "url": URL_ROOT + filename,
                   "platform": platform, "model": model,
                   "source_type": "third_party_compiled_production_register",
                   "input_sha256": hashlib.sha256(html.encode("utf-8")).hexdigest(),
                   "parsed_paint_rows": len(parsed),
                   "total_from_paint_rows": full_count,
                   "published_all_vehicle_total": declared,
                   "all_vehicle_total_reconciles": declared == full_count if declared is not None else None,
                   "excluded_reported_vehicle_counts": filtered_counts},
        "candidates": sorted(grouped.values(),
                             key=lambda v: (v["model_year"], v["trim"],
                                            v["body_code"], v["engine_label"],
                                            v["transmission"]))
    }


def build_snapshot(raw_html_by_filename: dict[str, str]) -> dict:
    sources = []
    candidates = []
    for spec in SOURCE_SPECS:
        filename = spec[2]
        if filename not in raw_html_by_filename:
            raise ValueError(f"Missing input for {filename}")
        result = read_table(raw_html_by_filename[filename], spec)
        sources.append(result["source"])
        candidates.extend(result["candidates"])
    seen = set()
    for candidate in candidates:
        if candidate["id"] in seen:
            raise ValueError("Duplicate normalized ID: " + candidate["id"])
        seen.add(candidate["id"])
    by_year = []
    for model in ("9-3", "9-5"):
        for year in range(1998, 2012):
            matching = [x for x in candidates if x["model"] == model
                        and x["model_year"] == year]
            by_year.append({
                "model": model, "model_year": year,
                "normalized_US_automatic_FWD_nonconvertible_groups": len(matching),
                "compiled_production_count_for_eligible_groups": sum(
                    x["reported_production_count"] for x in matching),
                "register_status": "observed_matching_production_rows" if matching
                                   else "no_matching_rows_in_compiled_register",
                "factory_exhaustiveness_certified": False,
            })
    return {
        "schema_version": "1.0.0",
        "catalogue_kind": "US compiled production normalized color rows",
        "markets": ["US"], "years": [1998, 2011],
        "eligible": {"models": ["9-3", "9-5"], "transmission": "automatic",
                     "drivetrain": "FWD",
                     "body_styles": ["sedan", "3-door hatchback",
                                     "5-door hatchback", "wagon"]},
        "limit": "Third-party compiled production. Counts are source-reported, not independently VIN-certified. Zero matching rows does not prove zero factory sales. Original parts and gearbox codes are not established by shorthand AT labels.",
        "sources": sources,
        "year_model_screening": by_year,
        "configurations": sorted(candidates,
                                 key=lambda v: (v["model"], v["model_year"],
                                                v["platform"], v["trim"],
                                                v["body_code"], v["engine_label"],
                                                v["transmission"])),
    }


def fetch_html(filename: str) -> str:
    req = Request(URL_ROOT + filename, headers={
        "User-Agent": "Mozilla/5.0 (compatible; SaabResearchCatalog/1.0)",
        "Accept": "text/html"})
    with urlopen(req, timeout=35) as response:
        return response.read().decode("utf-8", errors="replace")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--fetch", action="store_true",
                       help="Download live US compiled production tables")
    group.add_argument("--html-dir", type=Path,
                       help="Use saved HTML files instead of the network")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--require-total-reconciliation", action="store_true")
    args = parser.parse_args()
    raw = {spec[2]: fetch_html(spec[2]) if args.fetch else
           (args.html_dir / spec[2]).read_text(encoding="utf-8")
           for spec in SOURCE_SPECS}
    snapshot = build_snapshot(raw)
    if args.require_total_reconciliation:
        mismatches = [x["id"] for x in snapshot["sources"]
                      if x["all_vehicle_total_reconciles"] is not True]
        if mismatches:
            raise SystemExit("Source population totals did not reconcile: " +
                             ", ".join(mismatches))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(snapshot, indent=2, ensure_ascii=False) +
                           "\n", encoding="utf-8")
    print(f"Normalized {len(snapshot['configurations'])} US automatic/FWD "
          f"nonconvertible production groups from {len(snapshot['sources'])} "
          "compiled US tables.")
    for source in snapshot["sources"]:
        print(f"{source['platform']}: {source['parsed_paint_rows']} color rows, "
              f"source count reconciliation={source['all_vehicle_total_reconciles']}")


if __name__ == "__main__":
    main()
