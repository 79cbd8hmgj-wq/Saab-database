#!/usr/bin/env python3
"""Search research records without treating unspecified applicability as fitment."""

import argparse
import json
import sys

from database import KINDS, filter_records, inventory, load_datasets, validate_datasets


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--summary", action="store_true")
    parser.add_argument("--kind", choices=KINDS, default="facts")
    parser.add_argument("--text")
    parser.add_argument("--category")
    parser.add_argument("--platform")
    parser.add_argument("--engine")
    parser.add_argument("--year", type=int)
    parser.add_argument("--market")
    parser.add_argument("--include-unknown", action="store_true")
    args = parser.parse_args()
    try:
        datasets = load_datasets()
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 1
    errors = validate_datasets(datasets)
    if errors:
        print("Database failed validation; run python3 tools/validate.py", file=sys.stderr)
        return 1
    result = inventory(datasets) if args.summary else filter_records(
        datasets, kind=args.kind, text=args.text, category=args.category,
        platform=args.platform, engine=args.engine, year=args.year,
        market=args.market, include_unknown=args.include_unknown,
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
