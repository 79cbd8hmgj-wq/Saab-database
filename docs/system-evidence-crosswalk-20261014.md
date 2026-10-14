# Saab evidence crosswalk across sixteen systems — October 14, 2026

## Purpose and evidence boundary

This reconciles **all existing research records**, not new manufacturer findings. It joins the **1,101 facts, 92 issue records, 89 parts, and 284 research gaps** from the repository's **42 source-scoped datasets** to the existing [16-system vocabulary](../data/tier-research/methodology.json). The [prior 92-issue curation](legacy-issue-consolidation-20261014.md) remains the only human-reviewed **defect-versus-diagnosis/campaign** classification and the definitive original source record.

**The system assignments are discovery/navigation only.** They do not certify complete subsystem documentation, genuine defect frequency, original-component durability, current stock, engineer-approved VIN fitment, actual repair costs, or model ranking. Document count and parts count cannot be converted to these outcomes.

The [record-routing policy](../data/audits/system-evidence-routing-policy-20261014.json) contains sixteen topic-recognition groups and explicit domain-context fallbacks. The source-preserving [index generator](../tools/build_system_evidence_index.py) cross-links any existing original issue, fact, part, and gap by original **document URL**, not just by the domain-specific source ID. The same citation is **not independent corroboration** and is not proof that two different records describe the same failure mechanism.

### Actual indexing result

| Record category | Preserved | How used |
| --- | ---: | --- |
| Original technical facts | **1,101** | Search as specifications, diagnostic references, service/bulletin statements, supplier observations or source identity as originally marked |
| Existing classified issues | **92** | Retain primary role and original mechanism ID where human-curated |
| Existing parts | **89** | All 89 have **explicit, reviewed navigation-system assignments**; original OE/supplier part relationship and fitment claims remain unchanged |
| Unresolved gap records | **284** | Unclosed requirements; no inferred solution or retroactive source |
| **Total indexed records** | **1,566** | No factual research record replaced or copied as a new defect |

Every one of the 1,566 records has a traceable, lossless navigation entry, including original domain, ID, original source IDs and URLs when supplied, original applicability when present, and original evidence status. Original records remain in their respective research datasets. **An uncited gap can legitimately name evidence still needed; it must not be promoted into an uncited technical claim.**

Routes by verification state:

| Routing treatment | Records | What it proves |
| --- | ---: | --- |
| Explicit part-by-part system curation | **89** | Reviewed which physical system to **search** for each part; not inspected fitment or reliability |
| Keyword-matched topic | **1,135** | Searchable lead requiring engineering and exact-scope review |
| Research-domain context only | **143** | Lower-confidence context lead; no specific part/model scope approved |
| Cross-cutting / not unambiguously attributable | **199** | Retained for search and manual adjudication, not artificially counted toward a system |
| **All routes** | **1,566** | Complete **indexing**, not complete knowledge |

Of the 199 cross-cutting/unrouted records, **161 are facts, 31 are gaps, 7 are issue cases**. **250** records have more than one credible candidate system, so the per-system numbers below deliberately **overlap** and should **not** be summed as independent observations. Cross-cutting VIN identity, WebEPC access, source inconsistencies, general diagnostic/simulation requirements and multi-system outcomes may legitimately lack a single subsystem.

## Sixteen-system discovery inventory

These counts are **topic-index matches**, not validated coverage, independently observed fault events, real stock checks, or numbers of factory-documented failures. Original model-year/body/engine/gearbox/VIN restrictions require opening each linked source record.

| Subsystem | Facts | Issues | Parts | Gaps |
| --- | ---: | ---: | ---: | ---: |
| Engine core, lubrication, PCV/sludge | 191 | 20 | 26 | 45 |
| Timing drive, valve train, intake valves | 11 | 2 | 3 | 2 |
| Turbo, oil feed, intake and boost | 50 | 6 | 6 | 19 |
| Transmission and driveline | 139 | 16 | 0 | 52 |
| Body corrosion, mounting and subframes | 105 | 7 | 22 | 46 |
| Brakes and hydraulics | 58 | 6 | 1 | 20 |
| Cooling, radiators and heat exchangers | 142 | 11 | 10 | 29 |
| Fuel, emissions, exhaust and EVAP | 62 | 7 | 0 | 22 |
| ECUs, immobilizers, ignition, programming | 91 | 14 | 7 | 21 |
| Charging, starting, wiring and grounds | 85 | 9 | 5 | 12 |
| Steering, suspension and wheel hubs | 43 | 4 | 6 | 10 |
| HVAC, defrost and water ingress | 3 | 2 | 0 | 0 |
| Safety restraints and campaigns | 1 | 7 | 3 | 2 |
| Interior instruments, comfort and locks | 0 | 0 | 0 | 0 |
| Exterior body, glass and lighting | 38 | 0 | 0 | 7 |
| Maintenance, consumables and service | 103 | 5 | 0 | 23 |

### How to interpret underrepresentation

The **zero** transmission, fuel/exhaust, HVAC, interior and other-system parts here means **none of the current 89 part records were assigned to that physical system**; it does **not** mean the parts are unobtainable. Historical fault and procedure references already exist in several of those categories. For example, the NG9-3 FA57 coolant-in-ATF factory advice has an actual recorded failure mechanism and diagnosis in the old issues, despite the transmission part category having zero inventory records. Conversely a large B235 specification count cannot establish greater reliability or enough original installed-part revision analysis.

Interior/comfort electronics has no *explicitly system-attributable* topic matches in this first index. This might represent research omission or insufficient record metadata/routing. We should review related immobilizer, key, body, and wiring records and fetch original comfort-system material **only after checking those records**. Do **not** conclude interior electronics are safe, problematic, or absent.

The engine intake-valve group has **11** topic-matched facts and **two** issue records, but the factory B207 valve-wear bulletin is an established defect *mechanism*, while related compression-test facts describe diagnosis and service procedures. They are different evidence types. A source in an engine subsection does not establish model-year applicability to another B207 variant.

### What the 89 explicit part assignments corrected

A source-title-based route had mistakenly placed **12801010 / 32021815 ignition-switch module service-kit** records under maintenance rather than electronic immobilizer/security. Alternators with "B235" in their descriptions also risked spurious "engine core" system assignment; PCV hoses lacking "PCV" in the title were incorrectly left cross-cutting. All 89 current parts have now been assigned to an appropriate **search system explicitly**. Their existing source/part relationship qualifiers remain exactly as before; **this is not physical fitment approval or a current orderability check**.

### Unresolved gaps stay unresolved

The generator labels gaps as needing specific VIN/measurements, primary OE documentation, market/repair-economics checks, or other validation **for navigation**, but never marks one complete. In particular, the 284 gap records may duplicate workstreams or include tasks outside a particular physical system. The two repeated-title gaps and five duplicate part-number families found in [the repository reuse audit](research-reuse-audit-20261014.md) still require careful source-specific reconciliation rather than deletion.

## Repeatable use

```sh
# Rebuild an index from the original datasets; fail if any current record lacks a valid route entry.
python3 tools/build_system_evidence_index.py --check --summary

# Search original facts, issues, parts, gaps and original source URLs.
python3 tools/build_system_evidence_index.py --find "PCV"
python3 tools/build_system_evidence_index.py --find "55561200"
python3 tools/build_system_evidence_index.py --system transmission_driveline --find "FA57"

# Investigate overlapping/cross-cutting matches; export complete machine-readable records when needed.
python3 tools/build_system_evidence_index.py --review
python3 tools/build_system_evidence_index.py --output /tmp/saab-system-evidence.json
```

The index is derived on demand from stored authoritative research records: **we intentionally did not check a second 1,566-record copy into the repository**, which would rapidly become stale or create another duplicate-data workflow. New part records must be manually routed to a system; new datasets or changed system definitions must be explicitly reviewed by CI.

## What still needs source-level reconciliation

This completes the **initial full-inventory and source-preserving system crosswalk**, not factory-defect research completeness. The necessary follow-up is to examine the 199 cross-cutting records and 250 multi-system candidates, and then reconcile actual part number/version/applicability links and meaningful gap closures against the existing 19 mechanism groups and sixteen systems. That review must distinguish system specs, original manufacturer defect mechanisms, factory corrective revisions, observed failure events, parts supply and complete repair economics.

Only after validating what evidence is **truly missing**, should future PRs retrieve newly found original Saab/regulator bulletins or new market data. **No tier ranking or model preference is justified by these topic counts.**
