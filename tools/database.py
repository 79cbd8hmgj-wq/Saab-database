"""Read and structurally validate source-scoped research records."""

from __future__ import annotations

import json
import math
from collections import Counter
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
KINDS = ("sources", "facts", "issues", "parts", "gaps")
SOURCE_TYPES = {
    "factory_manual", "factory_bulletin", "factory_press_release",
    "supplier_catalog", "manufacturer_datasheet", "open_source_project",
    "technical_reference", "regulator_record",
}
RETRIEVAL_TYPES = {"full_text", "search_excerpt", "partial", "metadata_only"}
EVIDENCE_TYPES = {"documented", "supplier_claim", "inference"}
REVIEW_TYPES = {"source_scoped", "provisional", "needs_vehicle_verification"}
REQUIRED = {
    "sources": {
        "id", "title", "url", "publisher", "source_type", "accessed_at",
        "retrieval", "notes",
    },
    "facts": {
        "id", "subject", "category", "predicate", "value", "unit",
        "applicability", "source_ids", "evidence_status", "locator", "notes",
    },
    "issues": {
        "id", "title", "applicability", "cause", "symptoms",
        "diagnosis_summary", "correction_summary", "source_ids",
        "evidence_status", "limits",
    },
    "parts": {
        "id", "part_number", "title", "applicability", "relationships",
        "requirements", "source_ids", "evidence_status", "notes",
    },
    "gaps": {"id", "title", "missing_inputs", "reason", "source_ids"},
}


def _reject_json_constant(value: str) -> None:
    raise ValueError(f"Nonstandard JSON numeric constant: {value}")


def load_datasets(root: Path = ROOT) -> list[dict]:
    paths = sorted((root / "data" / "datasets").glob("*.json"))
    if not paths:
        raise ValueError("No datasets found under data/datasets/")
    datasets = []
    for path in paths:
        try:
            dataset = json.loads(path.read_text(encoding="utf-8"), parse_constant=_reject_json_constant)
        except (OSError, ValueError) as exc:
            raise ValueError(f"{path}: {exc}") from exc
        if not isinstance(dataset, dict):
            raise ValueError(f"{path}: dataset must be an object")
        datasets.append(dataset)
    return datasets


def _string_array(value: object) -> bool:
    return isinstance(value, list) and all(
        isinstance(item, str) and item.strip() for item in value
    )


def _contains_nonfinite(value: object) -> bool:
    if isinstance(value, float):
        return not math.isfinite(value)
    if isinstance(value, dict):
        return any(_contains_nonfinite(item) for item in value.values())
    if isinstance(value, list):
        return any(_contains_nonfinite(item) for item in value)
    return False


def _validate_scope(scope: object, location: str, errors: list[str]) -> None:
    if not isinstance(scope, dict):
        errors.append(f"{location}: applicability must be an object")
        return
    for field in (
        "platforms", "markets", "engine_codes", "transmission_codes", "body_styles",
    ):
        if field in scope and not _string_array(scope[field]):
            errors.append(f"{location}: {field} must be a string array")
    years = scope.get("model_years")
    if years is not None and (
        not isinstance(years, list)
        or not all(type(year) is int and 1950 <= year <= 2100 for year in years)
    ):
        errors.append(f"{location}: invalid model_years")
    ranges = scope.get("vin_ranges")
    if ranges is not None and (
        not isinstance(ranges, list) or not all(isinstance(item, dict) for item in ranges)
    ):
        errors.append(f"{location}: vin_ranges must preserve object notation")
    if "groups" in scope:
        groups = scope["groups"]
        if not isinstance(groups, list) or not groups:
            errors.append(f"{location}: groups must be a nonempty array of scope objects")
        else:
            for index, group in enumerate(groups):
                if not isinstance(group, dict):
                    errors.append(f"{location}.groups[{index}]: expected a scope object")
                elif "groups" in group:
                    errors.append(f"{location}.groups[{index}]: nested groups are not supported")
                else:
                    _validate_scope(group, f"{location}.groups[{index}]", errors)


def validate_datasets(datasets: list[dict]) -> list[str]:
    errors: list[str] = []
    seen_ids: set[str] = set()
    source_ids: set[str] = set()
    records: list[tuple[str, dict, str]] = []
    domains: set[str] = set()

    for index, dataset in enumerate(datasets):
        label = f"dataset[{index}]"
        if not isinstance(dataset, dict):
            errors.append(f"{label}: expected an object")
            continue
        if dataset.get("schema_version") != "1.0.0":
            errors.append(f"{label}: unsupported schema_version")
        domain = dataset.get("domain")
        if not isinstance(domain, str) or not domain.strip():
            errors.append(f"{label}: missing domain")
        elif domain in domains:
            errors.append(f"{label}: duplicate domain {domain}")
        else:
            domains.add(domain)
            label = domain

        for kind in KINDS:
            entries = dataset.get(kind)
            if not isinstance(entries, list):
                errors.append(f"{label}.{kind}: expected an array")
                continue
            for position, record in enumerate(entries):
                location = f"{label}.{kind}[{position}]"
                if not isinstance(record, dict):
                    errors.append(f"{location}: expected an object")
                    continue
                missing = REQUIRED[kind] - record.keys()
                if missing:
                    errors.append(f"{location}: missing {', '.join(sorted(missing))}")
                identifier = record.get("id")
                if not isinstance(identifier, str) or not identifier.strip():
                    errors.append(f"{location}: invalid id")
                elif identifier in seen_ids:
                    errors.append(f"{location}: duplicate id {identifier}")
                else:
                    seen_ids.add(identifier)
                    location = identifier
                    if kind == "sources":
                        source_ids.add(identifier)
                records.append((kind, record, location))

    for kind, record, location in records:
        if _contains_nonfinite(record):
            errors.append(f"{location}: nonfinite numeric value")
        if kind == "sources":
            parsed = urlparse(str(record.get("url", "")))
            if parsed.scheme not in {"http", "https"} or not parsed.netloc:
                errors.append(f"{location}: invalid source URL")
            if record.get("source_type") not in SOURCE_TYPES:
                errors.append(f"{location}: invalid source_type")
            if record.get("retrieval") not in RETRIEVAL_TYPES:
                errors.append(f"{location}: invalid retrieval status")
            try:
                stamp = record.get("accessed_at")
                if not isinstance(stamp, str) or date.fromisoformat(stamp).isoformat() != stamp:
                    raise ValueError("not an ISO date")
            except (TypeError, ValueError):
                errors.append(f"{location}: invalid accessed_at date")
            for field in ("title", "publisher"):
                if not isinstance(record.get(field), str) or not record[field].strip():
                    errors.append(f"{location}: empty {field}")
            continue

        references = record.get("source_ids")
        if not _string_array(references):
            errors.append(f"{location}: source_ids must be a string array")
        else:
            if kind != "gaps" and not references:
                errors.append(f"{location}: technical findings require a source")
            for reference in references:
                if reference not in source_ids:
                    errors.append(f"{location}: unresolved source {reference}")
            if len(references) != len(set(references)):
                errors.append(f"{location}: duplicate source reference")

        if kind in {"facts", "issues", "parts"}:
            if record.get("evidence_status") not in EVIDENCE_TYPES:
                errors.append(f"{location}: invalid evidence_status")
            review = record.get("review_status")
            if review is not None and review not in REVIEW_TYPES:
                errors.append(f"{location}: invalid review_status")
            _validate_scope(record.get("applicability"), location, errors)

        if kind == "facts":
            for field in ("subject", "category", "predicate", "locator"):
                if not isinstance(record.get(field), str) or not record[field].strip():
                    errors.append(f"{location}: empty {field}")
            unit = record.get("unit")
            if unit is not None and (not isinstance(unit, str) or not unit.strip()):
                errors.append(f"{location}: invalid unit")
            if type(record.get("value")) in {int, float} and unit is None:
                errors.append(f"{location}: numeric values need an explicit unit/convention")
        elif kind == "issues":
            for field in ("symptoms", "limits"):
                if not _string_array(record.get(field)):
                    errors.append(f"{location}: {field} must be a string array")
        elif kind == "parts":
            if not isinstance(record.get("part_number"), str) or not record["part_number"].strip():
                errors.append(f"{location}: part_number must preserve a string")
            if not _string_array(record.get("requirements")):
                errors.append(f"{location}: requirements must be a string array")
            relationships = record.get("relationships")
            if not isinstance(relationships, list):
                errors.append(f"{location}: relationships must be an array")
            else:
                for relationship in relationships:
                    if not isinstance(relationship, dict) or not {
                        "type", "part_number", "conditions",
                    } <= relationship.keys():
                        errors.append(f"{location}: incomplete part relationship")
                    elif not isinstance(relationship["part_number"], str):
                        errors.append(f"{location}: relationship part_number must be a string")
        elif kind == "gaps" and not _string_array(record.get("missing_inputs")):
            errors.append(f"{location}: missing_inputs must be a string array")

    return errors


def inventory(datasets: list[dict]) -> dict:
    counts = {kind: sum(len(dataset.get(kind, [])) for dataset in datasets) for kind in KINDS}
    sources = [source for dataset in datasets for source in dataset.get("sources", [])]
    statuses = Counter(
        record.get("evidence_status", "unspecified")
        for dataset in datasets
        for kind in ("facts", "issues", "parts")
        for record in dataset.get(kind, [])
    )
    return {
        "schema_version": "1.0.0",
        "domains": [dataset["domain"] for dataset in datasets],
        "counts": counts,
        "unique_source_urls": len({source["url"] for source in sources}),
        "retrieval_statuses": dict(sorted(Counter(source["retrieval"] for source in sources).items())),
        "evidence_statuses": dict(sorted(statuses.items())),
    }


def matches_scope(record: dict, field: str, target: str | int | None, include_unknown: bool) -> bool:
    if target is None:
        return True
    values = record.get("applicability", {}).get(field)
    if not values:
        return include_unknown
    if field == "model_years":
        return target in values
    normalized = {str(value).casefold() for value in values}
    return str(target).casefold() in normalized or bool(normalized & {"all", "global"})


def filter_records(
    datasets: list[dict], *, kind: str = "facts", text: str | None = None,
    category: str | None = None, platform: str | None = None, engine: str | None = None,
    year: int | None = None, market: str | None = None, include_unknown: bool = False,
) -> list[dict]:
    records = []
    for dataset in datasets:
        for record in dataset.get(kind, []):
            if text and text.casefold() not in json.dumps(record, ensure_ascii=False).casefold():
                continue
            if category and record.get("category", "").casefold() != category.casefold():
                continue
            scope = record.get("applicability", {})
            groups = scope.get("groups", [scope])
            if not any(all((
                matches_scope({"applicability": group}, "platforms", platform, include_unknown),
                matches_scope({"applicability": group}, "engine_codes", engine, include_unknown),
                matches_scope({"applicability": group}, "model_years", year, include_unknown),
                matches_scope({"applicability": group}, "markets", market, include_unknown),
            )) for group in groups):
                continue
            records.append({"domain": dataset["domain"], **record})
    return records
