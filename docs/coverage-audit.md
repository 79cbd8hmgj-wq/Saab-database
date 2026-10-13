# Phase 0 research coverage audit

Audit date: 2026-10-12. Repository baseline: `4895cffd450c7e295133d246fbef17309ef9a057`. This is an audit of *stored records*, not an independent recertification of the linked technical sources. The objective is to deepen documentation before attempting a car-ranking tool, interchange approval, reliability model, or vehicle simulator.

## Baseline inventory

| Measure | Count | Interpretation |
| --- | ---: | --- |
| Research domains | 7 | OG 9-5, NG 9-3, their body/chassis supplements, corrections, replacements, simulation resources |
| Sources / unique source URLs | 128 / 127 | Repeated URL is not an independent corroborating source |
| Factual records | 269 | Includes specifications and source-scoped research/resource facts |
| Issue records | 20 | Selected corrections; not a complete failure or recall census |
| Part records | 31 | Small sample of specific parts; not an electronic parts catalogue |
| Explicit research gaps | 51 | Not a count of all missing subjects |
| Source retrieval: full / partial / excerpt / metadata | 120 / 3 / 3 / 2 | Retrieval depth; not evidence-quality certification |
| Evidence: documented / supplier claim / inference | 289 / 28 / 3 | Across 320 facts, issues and parts; not failure-rate evidence |

The 320 records have the following explicitly populated top-level applicability fields. An absent field is **unknown**, not evidence of universal compatibility. Some omissions reflect the limits of the cited document rather than missing transcription.

| Applicability field | Records with explicit scope | Out of |
| --- | ---: | ---: |
| Platform | 286 | 320 |
| Model year(s) | 222 | 320 |
| Engine code(s) | 121 | 320 |
| Market(s) | 79 | 320 |
| Transmission code(s) | 28 | 320 |
| Body style(s) | 35 | 320 |
| VIN restriction(s) | 8 | 320 |

These percentages should **not** be combined into a completeness score: a broadly applicable fact may legitimately lack a narrower engine/year scope, and a year label in a WIS URL does not itself establish all applications.

## Explicit platform/model-year record counts

The tables below count a fact, issue or part **only if platform and year are explicitly paired within the same applicability group**. No unknown years are assigned to adjacent years. Records may be repeated in multiple rows because one documented fact may apply to multiple years. These are records, not unique pieces of confirmed equipment per car.

### Original-generation 9-5 (`9-5-9600`)

| Year | Facts | Issues | Parts |
| ---: | ---: | ---: | ---: |
| 1998 | 3 | 1 | 7 |
| 1999 | 3 | 1 | 10 |
| 2000 | 8 | 2 | 13 |
| 2001 | 4 | 2 | 13 |
| 2002 | 5 | 2 | 13 |
| 2003 | 5 | 1 | 11 |
| 2004 | 25 | 2 | 7 |
| 2005 | 97 | 2 | 7 |
| 2006 | 5 | 1 | 4 |
| 2007 | 5 | 1 | 4 |
| 2008 | 2 | 1 | 4 |
| 2009 | 27 | 1 | 4 |

**Priority finding:** MY2006–2008 are conspicuously underrepresented among year-scoped facts despite being central to our purchasing shortlist. MY2005 WIS documentation accounts for much of the OG 9-5 specification work. General facts must not be propagated to MY2006–2008 without actual applicability evidence.

### Second-generation 9-3 (`9-3-9440`)

| Year | Facts | Issues | Parts |
| ---: | ---: | ---: | ---: |
| 2003 | 9 | 12 | 9 |
| 2004 | 8 | 13 | 9 |
| 2005 | 14 | 7 | 6 |
| 2006 | 21 | 7 | 7 |
| 2007 | 7 | 7 | 7 |
| 2008 | 5 | 7 | 7 |
| 2009 | 5 | 7 | 7 |
| 2010 | 5 | 8 | 7 |
| 2011 | 9 | 8 | 6 |

A further **64 9-3 facts explicitly identify the platform but do not specify model years**. They may be useful as engineering context but cannot automatically pass a strict year-specific search. Issue counts in early years reflect campaign research, not proof that those cars fail more often.

## System-level qualitative matrix

Key: **Partial** = relevant sourced records exist but not a comprehensive subsystem inventory; **Conflicting** = important applicability or quantity conflict remains open; **Unresearched** = no adequate dedicated coverage found for the named subsystem in this seven-dataset pass. These are analyst classifications, not machine-produced coverage percentages. A few isolated mentions do not amount to a complete system description.

| Vehicle system | OG 9-5 | NG 9-3 | Most important missing evidence |
| --- | --- | --- | --- |
| VIN, trim, production and powertrain identity | Partial | Partial | Full US/CA build-year / option / chassis mappings and production changes |
| Engine internals, specifications, controls | Partial | Partial | Component-level service limits, procedures, revisions |
| Oil, lubrication, PCV | Partial | Partial | Complete service/correction matrix and inspection thresholds |
| Cooling, coolant and plumbing | Partial | Conflicting | Year/gearbox-specific capacities, coolant routing, hose IDs, revisions |
| Fuel, turbo and charge-air systems | Partial | Partial | Complete assembly drawings, flow envelopes, diagnostic procedures |
| Gearboxes, driveline and clutch | Partial | Conflicting | Exact installation mapping, refill methods, internal failure diagnostics |
| Brake system | Conflicting | Unresearched | Rotor/caliper/carrier fitment, hydraulics, lines, wear limits |
| Steering and suspension | Partial | Partial | Chassis-option codes, fasteners, bushings, detailed service limits |
| Wheels and tires | Partial | Conflicting | Confirmed PCD/bore, rated loads, approved wheel variations |
| Body structure and corrosion | Unresearched | Unresearched | Subframes, jacking points, mounts, sills, corrosion assessment, repairs |
| Electrical wiring and modules | Partial | Partial | Wiring/pinouts, grounds, power distribution, bus/security dependencies |
| HVAC and passenger comfort systems | Unresearched | Unresearched | HVAC hardware, climate electronics, failure and service procedures |
| Exhaust, catalyst and evaporative systems | Unresearched | Unresearched | Assemblies, sensors, emissions applicability and diagnostics |
| Occupant safety and campaigns | Partial | Partial | Full recall/TSB inventory and vehicle-specific completion confirmation |
| OEM parts and supersessions | Partial | Partial | EPC-level assembly coverage, boundaries and verified manufacturer relations |
| Maintenance and tests | Partial | Partial | Complete scheduled/severe service; measurable inspection/test limits |

There are already specific references to spring corrosion, water intrusion, ignition dependencies and recalls. **Unresearched structural corrosion** means the database lacks a systematic structural corrosion reference—not that rust was never mentioned anywhere.

## Research priorities and acceptance criteria

See [the research backlog](research-backlog.md). The immediate priority is **structural condition and model-year-specific mechanical coverage**, followed by brake/drivetrain verification and the exact identity/parts links needed to inspect affordable, non-running Saabs without gambling on engine or transmission rebuilds.

A high-quality new record must preserve: original publisher and retrieval strength; exact source locator; supported model/year/market/engine/gearbox/body/VIN scope; original units and test conditions; distinction between factory data, supplier claims and inference; any conflicting readings; and explicit unresolved inputs.

### Known methodology and code limitations

- `tools/query.py` currently filters platform, engine, year and market, not transmission, body style, VIN, or registration history. **Do not use its results alone as a fitment decision.**
- Applicability-group unions are for indexing only. `tools/coverage.py` counts a platform/year pair only when the same group explicitly names both.
- The validator checks integrity of recorded structure and references, not technical truth or correctness of engineering models.
- None of the source records establishes fleet failure rates or Toyota-equivalent reliability. Vehicle-specific condition, measured oil/cooling performance, structural inspection and service history are separate future inputs.
- This audit introduces no fabricated specifications, prices, inspection results, interchange claims or simulator predictions.

## Reproduce this census

Run on Python 3.10+ from the repository root:

```sh
python3 tools/validate.py
python3 -m unittest discover -s tests -v
python3 tools/coverage.py --format markdown
python3 tools/coverage.py --format json
```

The script generates the counts from the checked-out JSON datasets. The qualitative matrix and backlog require source-aware review; they are not inferred from category names alone. Update this audit when a research milestone changes material coverage or resolves conflicts.
