# Existing part-number and research-blocker adjudication — 2026-10-14

**Scope:** Consolidation of previously saved research, not a new Saab factory defect search. The [whole repository audit](research-reuse-audit-20261014.md) found five part numbers with two original part records apiece and two identical-title gap pairs. This review preserves all **89 parts**, **284 gaps**, **92 issues**, and their original source citations and applicability.

The reviewed [claim relationship register](../data/audits/part-gap-overlap-review-20261014.json) records distinct source assertions for each exact repeated number. [The validator](../tools/check_part_gap_reconciliation.py) dynamically checks original records and fails CI if future exact number/title overlaps appear without review. This does **not** decide current US parts orderability, original component failure probability, interchange approval or installed replacement costs.

## Five part-number relationships reviewed

| Same number | Original record IDs | Findings and remaining caution |
| --- | --- | --- |
| **55561200** | `corrections-part-001`, `pcv-supply-part-001` | Same Saab factory PCV renovation kit identity, but separate 9-5 sludge and earlier 9-3 PCV/leak bulletin applications. Each has installation and conditional hose instructions; no universal retrofit, current stock or complete-kit identity is inferred |
| **21341200** | `corrections-part-022`, `pcv-supply-part-002` | Same Pro Parts Sweden aftermarket PCV kit reference over different advertised 9-3/9-5 model scopes. Supplier cross-reference to Saab **55561200 is not a manufacturer-directed OE supersession**. PPS **21341200C** is a distinct more complete kit, not the same SKU |
| **32021815** | `corrections-part-016`, `gate5-part-002` | Same Saab Parts ignition-switch service **kit** for former **12801010**. Requires a functioning/reused black sliding mechanism from the old switch or intact donor. **Not** a fully interchangeable complete original switch assembly |
| **55558696** | `corrections-part-007`, `b235rev-part-001` | Original **CSP15433** selective 2004–05 9-5 B235 **manual** oil-trap campaign versus broader seller catalogue and disputed later **12755243** cross-reference. Preserve original engine, VIN and gearbox restrictions |
| **5961610** | `corrections-part-008`, `b235rev-part-005` | **Material conflict:** Saab CSP15433 conditional additional hose references engine serial **4000000–4017590**; a seller catalogue says **4017591 onward** and lists later 9-5 years. Those cannot be flattened into one universal fitment recommendation |

The last item is particularly important. A matching numeric identifier does not prove that the listed service condition, installed assembly, PCV routing, or supplier interpretation is the same. The factory campaign's conditional instruction and the seller's broader display remain separate **claims**. Only vehicle identity and original manufacturer parts/service verification can resolve their applicability.

Original records were not overwritten. The dynamic output includes each record's original platform/year/engine/gearbox scope, requirements, declared source strength, product relationships and original citation URLs.

## Two shared, still-open research blockers

| Canonical navigation blocker | Both original gap IDs | What remains genuinely missing |
| --- | --- | --- |
| Original **US MY2008–09 9-5** complete VIN source plus Canadian cross-check | `gateac-gap-001`, `vinfit-gap-001` | Dated manufacturer-issued 2008–09 VIN-position tables and country/equipment decoding. Previously recovered US 2004–07 tables do not solve this; a 2010-code table in an earlier WIS folder must not be substituted |
| **Canadian MY2006 9-3** option/VIN interpretation and real car build verification | `gateac-gap-002`, `vinfit-gap-003` | Canadian original equipment mapping and actual physical engine/gearbox build confirmation. The retrieved Saab USA 2006 table does not establish Canadian equipment or an individual VIN's installed components |

These are *one open question referenced in two research domains*, not four independent information deficiencies. All four original gap records remain open until their specified evidence is collected. The canonical blocker IDs are navigational aliases, not retroactive gap closures.

## Review of issue-system routing

[PR #71's system index](system-evidence-crosswalk-20261014.md) originally marked **25 issues** as possibly multi-system and **7** as cross-cutting/unrouted. Their titles, original issue type, and stored causal descriptions have been reviewed for **navigation only**. The system-policy now includes **32 explicit issue routes**, distinct from the earlier **89 explicit part routes**.

Examples of corrected false positives:

- **B235 alternator descriptions** now route to charging and starting, rather than engine internals merely because the engine designation appears in a part name.
- **A 9-5 severe-duty oil service interval** stays in maintenance, not turbo failure research because the marketing engine name includes “Turbo.”
- **START BLOCKED/steering-lock electronics** belong to electrical security and starting supply; a warning-message phrase does not establish a steering/suspension failure.
- **Coolant-in-ATF** remains legitimately cross-system (cooling plus automatic transmission).
- **SID service-reset versus actual service history** is a maintenance/instrumentation question, not a diagnosed electronic engine defect.

**Five reviewed issue records deliberately have no physical-system assignment**: `gate5-issue-001`, `gateac-issue-001`, `vinfit-issue-001` (source/VIN table quality), `usparts-issue-001` (retailer stock display inconsistency), and `wp7-issue-001` (historical recall lookup limits). Those are essential research controls, **not known component failures**.

Following this review, the source-backed master index contains **197 cross-cutting/unrouted records** and **244 records with multiple candidate systems** (down from 199 and 250). The remaining counts include **automated fact/gap topic matches**, not 197 unrecorded Saab faults. Those still need later source and applicability checks before system-specific reliability claims.

## Repeatable queries and ongoing safeguards

```sh
# Read claims for the duplicate product numbers and the two shared, open blockers
python3 tools/check_part_gap_reconciliation.py --check --summary
python3 tools/check_part_gap_reconciliation.py --output /tmp/saab-reconciled-overlaps.json

# Original provenance, review links and current system taxonomy
python3 tools/build_system_evidence_index.py --find 5961610
python3 tools/build_system_evidence_index.py --find 32021815
python3 tools/build_system_evidence_index.py --find gateac-gap-001

# Show all remaining routes (without the earlier silent first-250 cap)
python3 tools/build_system_evidence_index.py --review --review-kind facts --review-limit 0
python3 tools/build_system_evidence_index.py --review --review-kind gaps --review-limit 0
```

CI rejects a newly repeated exact part-number group or gap-title group without a reviewed disposition; it also rejects new parts lacking reviewed system assignments and retains all 92 historical issue classifications. The master system index now links the reviewed same-number part records and shared-open-gap blocker IDs directly to their original stored entries.

**Next engineering audit milestone:** adjudicate the remaining ambiguous facts/gaps against the source and individual configuration; then compare the resulting documented manufacturer component/part revision coverage against a defined factory bulletin/recall population. No Saab model tier follows from these counts.
