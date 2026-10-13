# Saab database

A source-backed research database for Saab specifications, factory corrections,
parts relationships, and the information needed to evaluate replacements.

The first research pass focuses on the original-generation 9-5 (9600) and
second-generation 9-3 (9440), especially US/Canadian four-cylinder configurations.
It also records boundaries that matter when comparing adjacent model years,
engines, and platforms.

## Start here

- [Research overview](docs/research-overview.md): scope, coverage, model-selection
  reasoning, and the limits of the initial research.
- [Evidence policy](docs/evidence-policy.md): what a recorded finding actually
  establishes.
- [Data contract](docs/data-contract.md): dataset fields and applicability rules.
- [Simulation readiness](docs/simulation-readiness.md): what can be evaluated from
  documents and what still needs measurements or engineering data.
- [Research reports](docs/research/): detailed notes from the individual research
  domains, including contradictions and gaps.
- [Original 9-5 Trionic 7 electrical diagnosis](docs/research/og95-t7-electrical.md):
  factory ECU supplies and grounds, crank/ignition diagnosis, and TWICE immobilizer requirements.
- [Official Saab EPC access and cross-reference conflicts](docs/research/saab-epc-provenance.md):
  manufacturer VIN workflow, bushing/subframe identifier collision, and research restrictions.
- [Early 9-3 mount and petrol fuel research](docs/research/ng93-early-mount-fuel.md):
  2003–2005 factory revisions, convertible chassis suffix boundaries, and fuel-line safety.
- [Subframe and brake-line parts research](docs/research/subframe-parts-brake-lines.md):
  documented OEM assembly candidates, installation limits, and hydraulic safety.
- [9-3 structural research](docs/research/ng93-structure.md): corrosion-protection scope,
  body repair rules and specific subframe/convertible differences.
- [9-5 structural research](docs/research/og95-structure.md): factory repair boundaries,
  rust and inspection-relevant mounting areas.
- [9-5 2006–2008 source supplement](docs/research/og95-2006-2008.md):
  North American specifications, WIS conflicts and source limits.
- [Datasets](data/datasets/): structured JSON with source IDs and original links.

As of October 12, 2026 the database contains **232 source records, 431 factual
records, 24 issue records, 55 part records, and 98 explicit gaps** across fourteen
research domains. This is not a completeness score.
See [the source index](docs/source-index.md) and [machine-readable inventory](data/inventory.json).

## What this contains

- Engine, lubrication, cooling, drivetrain, chassis, and electrical specifications
  where primary documents support them.
- Factory bulletins/campaigns with model, engine, VIN, and component restrictions.
- Useful part numbers and documented supersession relationships.
- References to diagnostic and ECU-analysis resources, with reuse/license notes.
- Explicit missing-input records for fitment, thermal, structural, performance,
  and durability evaluation.

Each finding is scoped to its evidence. A catalogued part is not automatically a
verified substitute for a particular installed part. A supplier's thermal claim is
not a measured lifetime improvement. A model-selection preference is not a
statistical reliability ranking.

## Inspect and validate

The tools use Python's standard library and require Python 3.10 or newer.

```sh
python3 tools/validate.py
python3 -m unittest discover -s tests -v
python3 tools/query.py --summary
python3 tools/query.py --engine B235R --category cooling
python3 tools/query.py --platform 9-3-9440 --year 2006
python3 tools/query.py --text "intake valve" --kind issues
```

Query filters help find source-scoped records. They do not issue a fitment approval.
Unspecified applicability is treated as unknown, not as universal compatibility.
By default an applicability filter excludes records lacking that field; use
`--include-unknown` to inspect those records too.
Engine-code filters are exact: a family-level `B207` entry is not silently expanded
to `B207R`. Search by platform/year or text as well when exploring family-scoped
records. VIN, component serial, registration-history, and installed-hardware
conditions still require interpretation of the full record and source.

## Add a particular car later

Use [the vehicle-instance template](templates/vehicle-instance.json) to record
identity, installed components, observations, and measurements. The template has
no invented vehicle data. Do not treat factory nominal specifications as measured
condition on an individual car.

## Source material and reuse

This repository contains original summaries, extracted factual records, and links.
Original manuals, catalogues, manufacturer documentation, and referenced software
retain their own rights and licensing terms. No third-party license is extended to
the entire repository. Referenced software is not vendored or executed by this
database.
