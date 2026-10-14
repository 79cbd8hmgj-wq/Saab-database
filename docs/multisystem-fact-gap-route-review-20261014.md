# Review of remaining multi-system fact and gap references — October 14, 2026

This follows the [cross-cutting 161-fact and 31-gap review](fact-gap-navigation-adjudication-20261014.md) and the [32-issue/89-part navigation review](part-gap-overlap-adjudication-20261014.md).

**Scope: source-preserving classification, not new engineering research.** All **225 previously unreviewed multi-system entries**—**176 facts** and **49 still-open gaps**—were assessed against their saved subject/title, predicate, original value or missing inputs, and stated topic/source context. The [routing policy](../data/audits/system-evidence-routing-policy-20261014.json) contains an individual record ID, explicitly selected physical systems or empty cross-cutting route, a written justification and SHA-256 digest of the unchanged original record. The digest detects stale navigation decisions after data edits; it does **not** prove the technical claim true.

No existing source-scoped technical dataset, manufacturer bulletin, original applicability, part identity, supplier price, or original gap was changed.

## 1. Measured review outcomes

| Previously unreviewed multi-system candidates | Facts | Open gaps | Total |
| --- | ---: | ---: | ---: |
| Original queue at PR #73 close | **176** | **49** | **225** |
| Narrowed to one physical-system navigation route | 89 | 10 | **99** |
| Retained as genuinely cross-system or related-system navigation | 85 | 29 | **114** |
| Reclassified as legitimate *cross-cutting*, not a specific physical component | 2 | 10 | **12** |
| Original proposed system list changed by review | 106 | 27 | **133** |

The other **92** candidate records retain their overlapping routes after checking original context. Keeping two related systems does not assert there are two failed components or independent factory defects.

**Current total of all 1,566 original evidence records:**

- **417 fact/gap decisions** were expressly reviewed across PRs #73–74 (**337 facts, 80 gaps**).
- The previously reviewed **32 issue** and **89 part** route decisions remain intact.
- **99** cross-cutting entries are now *deliberately* identified (**66 facts, 28 gaps, five source/recall-provenance issues**), compared with 87 after PR #73.
- **144** records retain more than one related-system route, down from 255 after PR #73.
- **Zero previously identified ambiguous candidates remain unreviewed** in the navigation work queue. This is **not** evidence that all Saab factory component defects are discovered, that all observations are externally verified, or that any of the 284 open research gaps are resolved.

The 16-system source catalogue still contains **1,101 facts, 92 issue records, 89 parts and 284 gaps**. System-specific record counts remain *overlapping topic references*, not engineering-quality scores.

## 2. Spurious multiple-system matches corrected

A number of the original automatic routes reflected incidental engine identifiers, unrelated keywords, or generic descriptions:

| Original fact/gap | Curated navigation | Why the second/third match was misleading |
| --- | --- | --- |
| `afdiag-fact-001` through `004` | Turbocharging | Bulletin 291-2317 describes a specific wastegate/bypass repair, not a B205/B235 internal engine failure; original **non-US/CA** scope is still binding |
| `b235rev-fact-025`, `029` | PCV/lubrication | Oil-trap hoses and their supplier engine-serial restrictions are not timing drive or independent turbo faults |
| `ng93-fact-043`, `045`–`050` | Cooling/heat | Coolant capacity, radiator cap, boiling limits, fan stage and afterrun values are not original B207 oil-system durability observations |
| `ng93-fact-039`, `040` | Brakes | Brake rotor diameter and thickness values aren't body exterior/glazing specifications |
| `ng93body-fact-022`, `023` | Steering/suspension | Hydraulic steering pump specification is not an original B207 engine-core failure |
| `og95-fact-058`–`060` | Turbocharging | Actual GT17/TD04 actuator pressure belongs to turbo control; B205/B235 text identifies the original engine variant only |
| `og95-fact-065` | Cross-cutting | Market engine/option code `B3` is a vehicle-identity observation, not brake-system evidence despite a substring match |
| `prebuy-gap-001` | Turbocharging | Missing turbo shaft-play acceptance is a turbo measurement gap, not an exterior body dimension |
| `og95years-gap-006`, `simulation-gap-002` | Cross-cutting | Requests for broad manufacturer documentation and timestamped data acquisition span components; treating them as confirmed subsystem problems is not justified |
| `gate5-gap-003` | ECU/immobilizer | Exact ignition-switch repair-kit VIN exclusions concern security hardware, not general scheduled maintenance; gap stays open |

These are organization fixes based on what the *saved records already say*. Neither an engine code in a source title nor a maintenance procedure by itself establishes a component defect.

## 3. Genuine cross-system interfaces retained

- **`hcdiag-fact-029` / `030`, `maint-fact-043` / `044`:** Factory FA57 coolant-in-ATF diagnosis involves the **cooler/engine cooling interface and automatic gearbox**. The original Saab 9-3 SS, SS TiD and convertible VIN cutoffs remain separate and exclusive. Confirmation requires vehicle-specific diagnosis; no failure frequency is implied.
- **`afdiag-fact-005` and `turbsol-fact-031`:** Gearbox TCM sensor or solenoid circuitry involves **transmission and electrical wiring**. Fault-code electrical paths do not alone prove internal gearbox failure.
- **`og95wire-fact-021` / `022`:** Cooling fan relays/grounds and harness branch positions legitimately span **cooling plus wiring**.
- **`ng93structure-fact-027`:** Body repair requires original structural, **restraint safety** and electrical grounding precautions; navigation includes all three without claiming these systems share a defect.
- **`early9three-fact-016` and `rustgate-gap-004`:** Brake/fuel pipes and underbody route/clip corrosion controls legitimately intersect, but prevalence and physical condition are unknown.
- **`parts95-gap-008`:** The unresolved replacement-durability question spans **radiator, structural mount and PCV** alternatives. No supplier's aftermarket material or kit has achieved an independently verified Toyota-equivalent service life.
- **`simulation-gap-003`:** Engine brake-torque/BSFC **dynamometer terminology** refers to engine output and fuel flow, **not** the vehicle's brake friction hardware. The gap remains unmeasured.

All route decisions leave manufacturer production revisions, market applicability, full VIN, actual installed part identity, quote fulfillment, and DIY/shop labor *separate gates*.

## 4. What remains unresolved

Although the navigation ambiguity queue is now fully assessed, **284 stored gaps remain open**, including disputed PCV hose `5961610` engine-serial application, original US/CAN VIN mappings, OEM-directed replacement supersessions, actual part stock and shipping, comprehensive factory bulletin coverage, quantified owner-fleet failures, and complete high-severity repair cost scenarios.

The repository's 110 automatic/FWD/nonconvertible U.S. candidate groups are **not the full Saab comparison universe**, and their existence does not prove production defects or individual-vehicle service history.

The next justified consolidation step is to **compare the saved 284 gap questions against the saved 1,101 facts and 562 source records**, distinguishing unchanged/open, already partially answered, actually solved but never closed, genuinely missing primary factory material, and vehicle-instance-only requirements. That is substantially more useful than generating another batch of repeated faults.

## 5. Reproducible audit commands

```sh
python3 tools/build_system_evidence_index.py --check --summary

# This should return 0 currently unreviewed ambiguous candidates.
python3 tools/build_system_evidence_index.py --review --review-unreviewed-only --review-limit 0

# Audit original saved source context and hash for reviewed records.
python3 tools/build_system_evidence_index.py --review --review-kind facts --review-context --review-limit 0
python3 tools/build_system_evidence_index.py --review --review-kind gaps --review-context --review-limit 0

# Export all source-linked research records without duplicating original content in the repository.
python3 tools/build_system_evidence_index.py --output /tmp/saab-system-evidence.json
```

CI verifies all existing source records and regression contracts, digest alignment, all-part routing, the 92-issue taxonomy, the five repeated part claims, two *still-open* shared VIN research blockers, and the unchanged unranked tier methodology. A green workflow is structural validation, **not a fresh technical audit of each external source**.

**No reliability tiers, vehicle priorities, model scores or invented failure rates are warranted by these index counts.**
