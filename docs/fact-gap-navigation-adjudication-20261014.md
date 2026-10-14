# Cross-cutting fact and gap navigation review — October 14, 2026

This continues [PR #72's consolidation](part-gap-overlap-adjudication-20261014.md).
All **161 facts and 31 gaps** that were cross-cutting/unrouted after that PR have
been reviewed against their saved values, notes, source IDs and applicability.
No external source was newly retrieved or recertified. No original technical
dataset was edited, no gap was closed, and no new defect was collected.

The [routing policy](../data/audits/system-evidence-routing-policy-20261014.json)
contains each original record ID, kind, reviewed system list, reason and digest
in `explicit_fact_gap_routes`. It is the machine-readable review register.
Original source IDs, scopes, units and evidence statuses remain authoritative.

| Review outcome | Facts | Gaps | Total |
| --- | ---: | ---: | ---: |
| Reviewed from PR #72's cross-cutting queue | 161 | 31 | 192 |
| Given physical-system navigation | 97 | 13 | 110 |
| Deliberately retained as cross-cutting | 64 | 18 | 82 |

Together with five previously reviewed source/recall-lookup issue cases, the
index now retains **87 cross-cutting records**, down from 197. All 87 have a
manual navigation decision; a deliberate empty route is not an unfinished
physical-component assignment.

## Saved information made easier to find

| Existing records reviewed | Navigation decision | Boundary preserved |
| --- | --- | --- |
| `corrections-fact-003` | PCV/lubrication | Additional-hose serial range and manual-gearbox scope remain; the 5961610 seller conflict remains open |
| `prebuy-fact-020`, `prebuy-fact-021` | Transmission and electrical sensing | Input-speed diagnostics do not prove a failed gearbox; no seller-lot stress test is approved |
| `t7cool-fact-037`, `043`, `049` | Cooling | Stored DICE fan references concern their petrol/year context, not diesel or all DICE functions |
| `wp7-fact-018` through `026` | Occupant safety/campaigns | A-pillar trim, airbags and belts retain separate market/year/body and registration restrictions |
| `usparts-fact-001` through `011` | Cooling, ignition or starting according to the SKU | Historical retailer prices and stock displays stay supplier claims, not verified current supply or repair totals |
| `turbsol-gap-006`, `turbsol-gap-007` | Transmission | Solenoid identity and resistance-presentation questions are still unresolved |

Engine output and geometry specifications now have engine-core search routes.
That does not turn peak power into internal durability evidence. Oil refill,
cooler-inclusive volume, warning thresholds and lubricant approvals keep their
different definitions and year/market limitations.

## Why some records should stay cross-cutting

VIN tables and vehicle identities concern the whole configuration. WebEPC
feature descriptions identify an access path, not a retrieved manufacturer part
chain. Generic software/adapter limits and simulation requirements are not
specifications of an installed Saab assembly. Mixed-SKU fulfilment questions
and general source-version/licensing questions likewise lack one physical target.

Examples include `gate5-fact-004`, `vinfit-fact-006`, `epcverify-fact-001`,
`simulation-fact-019`, `gateac-gap-001`, `vinfit-gap-006` and `usparts-gap-002`.
Their empty route lists are now explained, rather than silently assigned from
incidental engine names or technical words.

## Real overlap remains

Multi-system membership increased from **244 to 255**. Eleven newly reviewed
entries legitimately link multiple systems, such as gearbox sensing and wiring,
or TCM-to-engine torque control. The count is overlapping navigation, **not** a
count of distinct defects, failures, research gaps or completed systems.

The remaining unreviewed ambiguous queue contains **176 facts and 49 gaps**,
all currently multi-system proposals. This batch reviewed the complete
cross-cutting queue; it did not adjudicate those 225 existing multi-system routes
or declare factory-document coverage complete.

## Repeatable review and safeguards

```sh
python3 tools/build_system_evidence_index.py --check --summary
python3 tools/build_system_evidence_index.py --system transmission_driveline --find prebuy-fact-020
python3 tools/build_system_evidence_index.py --find gateac-gap-001

# Keep deliberate reviewed cross-cutting/multi-system decisions out of the next queue.
python3 tools/build_system_evidence_index.py --review --review-kind facts --review-unreviewed-only --review-limit 0
python3 tools/build_system_evidence_index.py --review --review-kind gaps --review-unreviewed-only --review-limit 0
```

CI rejects reviews of nonexistent records, incorrect kinds, unknown/duplicate
system IDs, blank reasons or changed original records whose reviews were not
refreshed. The digest detects edits to the saved record, not whether its original
engineering claim is true. A full `--review` still includes reviewed overlapping
and cross-cutting entries for audit inspection; the new option only filters the
work queue.

**Follow-up completed:** [The October 14 multi-system review](multisystem-fact-gap-route-review-20261014.md) has now reviewed those **176 facts and 49 gaps**, leaving **no identified unreviewed navigation candidates**, but does not externally verify or close any original technical question.

The next consolidation pass should compare the still-open named missing inputs
against source-linked facts already saved in other domains, rather than redoing
the now-reviewed navigation routes.
The 1,101 facts, 92 issues, 89 parts and 284 open gaps are unchanged. Failure
frequency, VIN-approved replacements, current fulfilment, complete repair costs
and model tiers gain no approval from this navigation review.
