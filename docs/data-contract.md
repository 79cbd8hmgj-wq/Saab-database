# Data contract

Schema version: `1.0.0`.

Each file under `data/datasets/` is a self-contained research domain with these
arrays: `sources`, `facts`, `issues`, `parts`, and `gaps`. IDs are unique across the
repository. Duplicate URLs can appear under different source IDs where research
domains record the same document; provenance is not discarded during integration.

## Sources

Required fields: `id`, `title`, `url`, `publisher`, `source_type`, `accessed_at`,
`retrieval`, and `notes`.

Source types are `factory_manual`, `factory_bulletin`, `factory_press_release`,
`supplier_catalog`, `manufacturer_datasheet`, `open_source_project`,
`technical_reference`, and `regulator_record`. The project resource type is a
category of reference, not a guarantee that its license is open source.

`accessed_at` is an ISO date for research retrieval, not the document publication
date. Publication/revision information belongs in the source notes or a separate
explicit field when available.

## Facts

Required fields: `id`, `subject`, `category`, `predicate`, `value`, `unit`,
`applicability`, `source_ids`, `evidence_status`, `locator`, and `notes`.

`value` may be a JSON number, string, boolean, array, or object. `unit` is null for
non-quantity descriptions; numeric quantities should identify the unit or
dimensionless convention. `locator` describes the table, page, heading, or row.

Subjects identify the entity rather than a particular owner, for example
`engine:B235R`, `gearbox:FA57`, or `profile:og95-us-2006-2009`.

Applicability can include string arrays `platforms`, `markets`, `engine_codes`,
`transmission_codes`, and `body_styles`; an integer array `model_years`; and a
`vin_ranges` array of objects preserving source notation and restrictions.
Omitted fields are unknown. An explicit `all`/`global` marker means the source
itself supports a broad scope, not that an author forgot to select one.

When a record combines different model/year/engine pairings, use `groups`, a
nonempty array of complete scope objects. The flat arrays are then an index union;
the query evaluates the separate groups and never takes a Cartesian product of
the union fields. A field omitted within a group stays unknown even if a flat
union field exists above it. Nested groups are not supported. Registration-history
regions and VIN/serial restrictions are retained for interpretation, not automated
eligibility decisions.

Optional `review_status` can be `source_scoped`, `provisional`, or
`needs_vehicle_verification`. Use it to clarify a conflict or unresolved
application without changing what the source actually states.

## Issues

Required fields: `id`, `title`, `applicability`, `cause`, `symptoms`,
`diagnosis_summary`, `correction_summary`, `source_ids`, `evidence_status`, and
`limits`.

These are concise source summaries. They are not complete step-by-step repair
instructions and cannot replace the linked factory procedure.

## Parts

Required fields: `id`, `part_number`, `title`, `applicability`, `relationships`,
`requirements`, `source_ids`, `evidence_status`, and `notes`.

Part numbers are strings, preserving leading zeroes, punctuation, and suffixes.
Relationship entries contain `type`, `part_number`, and `conditions`.
`supersedes` and `superseded_by` retain their direction. A catalogue relationship
does not by itself prove a reverse substitution or cross-platform fit.
`aftermarket_reference` identifies a supplier cross-reference without calling it
an OEM supersession. `contains` identifies kit contents and does not instruct the
reader to purchase those components separately. `requires` describes an explicitly
stated accompanying part or prerequisite.

### Conditional manufacturer parts-service kits

`replaced_by_service_kit` records a **directed manufacturer support workflow**
from an earlier serviced part to an official kit, while
`kit_for_earlier_part` connects the kit back to the **earlier serviced item**
for catalogue discovery. Neither type is a drop-in complete-assembly fitment
claim or a reverse supersession. Record every required salvaged component,
conditions under which the old component is NOT reusable, option/VIN scope and
the specific service-document page.

A manufacturer-hosted owner-service bulletin may provide a documented
**conditional kit repair process** without proving a live stock status or an
individual VIN-approved WebEPC successor. Do not change those claims to
`supersedes` until the exact official WebEPC relationship, direction and
applicability are independently retrieved.

## Gaps

Required fields: `id`, `title`, `missing_inputs`, `reason`, and `source_ids`.

Gaps can represent missing factory parameters, source conflicts, unverified
replacement data, unsupported applicability, or needed measurements/validation.
An empty source list is permitted for a clearly identified research requirement;
it cannot be used to support a claimed technical specification.

## Validation limits

The validator checks structure, identifiers, references, dates, units, and
applicability representation. Passing validation does not prove the underlying
engineering claim. Source review, vehicle identification, and appropriate testing
remain separate checks.

## Cross-manufacturer interchange candidates (research-only)

The separate `data/interchange-candidates/phase0.json` matrix preserves manufacturer,
exact aftermarket SKU, *candidate* donor brands and the difference between
manufacturer-labelled `Interchangeable` and weaker `Reference corresponds to a
component` catalogue relationships. It also distinguishes the **research scope**
(e.g., priority MY2005–06 B207 Saab 9-3) from **verified fitment**. Neither a
common aftermarket SKU nor a shared platform name proves that actual original
Opel/GM/Fiat donor assemblies are identical, VIN-approved, or durable on Saab.

Each candidate must explicitly record the physical and electrical unknowns,
OEM/factory application verification, installation dependencies, and **separate**
flags for verified drop-in, original donor, physical vehicle test, availability,
price benefit and reliability improvement. False flags are meaningful: do not
mark an option approved from a supplier cross-reference alone. Source IDs must
resolve to stored provenance; tests reject accidental status promotion of early
catalogue candidates. Any claim of validated fitment or durability requires
stronger supporting test and application evidence beyond structure validation.


### Additional source-scoped supplier candidate records

The companion `cross_manufacturer_interchange_pilot` dataset optionally uses `parts[*].interchange_candidate` with `strategy`, `donor_makes`, `saab_reference_numbers`, three booleans (`fitment_approved`, `vehicle_verified`, `durability_validated`) and `verification_required`. This supplementary catalogue evidence is **not a second approved-parts matrix**. All pilot booleans are false, review state is `needs_vehicle_verification` and evidence is `supplier_claim`. Product cross-reference direction is `aftermarket_reference`, never an inferred manufacturer supersession. A future reconciliation with the dedicated `data/interchange-candidates/phase0.json` schema should deduplicate by manufacturer SKU and provenance, not combine unrelated Opel OE numbers.
