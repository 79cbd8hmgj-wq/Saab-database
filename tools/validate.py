#!/usr/bin/env python3
"""Validate the integrated research database; does not certify engineering claims."""

import json
import sys

from database import inventory, load_datasets, validate_datasets


def main() -> int:
    try:
        datasets = load_datasets()
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 1
    errors = validate_datasets(datasets)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        print(f"FAILED: {len(errors)} structural errors", file=sys.stderr)
        return 1
    print(json.dumps(inventory(datasets), indent=2))
    print("PASS: structure and references are valid; technical source review is separate.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
