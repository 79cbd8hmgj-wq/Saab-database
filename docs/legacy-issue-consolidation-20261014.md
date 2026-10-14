# Consolidation of the 92 preexisting Saab issue records — October 14, 2026

**Result:** All **92** existing source-scoped issue records now have a stable, explicitly reviewed primary role. Source-document provenance, original engine/year/market/VIN applicability and known limitations remain in the original datasets, not rewritten here.

This is **not** the complete Saab factory defect or recall population, **not** an observed reliability comparison and **not** a tier list. The legacy records include defects, diagnostics, parts ordering restrictions, source-version mistakes and purchase-screening questions. Reusing all of them is necessary before searching for *new* Saab failure bulletins.

Source manifest: [legacy issue taxonomy](../data/audits/legacy-issue-taxonomy-20261014.json). Reproducible catalogue: [build_legacy_issue_index.py](../tools/build_legacy_issue_index.py). This builds a source-linked view directly from **all 42 existing datasets** and the [current tier ledger](../data/tier-research/observations.json).

**Further crosswalk:** [All existing research records across sixteen systems](system-evidence-crosswalk-20261014.md) are now indexed, including the 1,101 original facts, 89 part records and 284 gaps. Source document co-citations are useful lookup links, not independent fault diagnoses or part fitment approval.

## 1. Every issue counted once without inflating defects

| Reviewed record category | Legacy records | Does NOT mean |
| --- | ---: | --- |
| Specific original factory-documented failure mechanism | **12** | Twelve failures per car or twelve measured epidemic faults |
| Manufacturer/regulator safety campaign and campaign implementation | **8** | Eight independent safety root causes or completed/failed recall repairs |
| Factory-origin **suspected** design failure | **1** | Confirmed defective component |
| Symptom-driven diagnostic and repair differential | **32** | Unique original design defects |
| Parts identity, compatibility, service-kit or architecture restriction | **16** | Verified physical interchange or current stock |
| Maintenance or service procedure/handling requirement | **8** | Manufacturer defect or preventive reliability proof |
| Source, bulletin, market or specification inconsistency | **11** | A defective factory-installed vehicle component |
| Rust/body/underbody or jurisdictional inspection safety case | **3** | Factory-wide defect or structurally certified car |
| Evidence or recall-lookup verification gate | **1** | A factory engineering failure |
| **Total, each legacy issue exactly once** | **92** | A manufacturer-wide defect count |

The **21** entries in the first three categories are conservatively linked to **19 engineering/safety mechanism identities**: **12** factory-documented component types, **6** underlying campaign hazards/nonconformances, and **1** still-*suspected* casting-porosity hypothesis. The difference between eight campaign records and six campaign mechanisms is particularly important: three Takata-related records represent *one general inflator-rupture hazard*, not three independent engineering defects. Their affected markets, vehicle bodies, regions and service implementations remain **different**.

There are **17** additional conserved mechanism identities **not yet linked to the new tier ledger**, rather than only the two mechanisms currently displayed by that ledger. These 17 are preexisting evidence **leads**, not 17 newly discovered factory problems. They also do not mean that we have located every known Saab issue.

## 2. Source-backed manufacturer defects already present

The twelve distinct source-scoped **factory mechanism** identities already recorded are:

| Existing mechanism group | Legacy record | Key boundary |
| --- | --- | --- |
| Early 9-3 (9400) PCV flow insufficiency | pcv-supply-issue-001 | Early B205/B235 years; separate renovation bulletin |
| 9-5 B235 manual oil trap / high oil consumption correction | corrections-issue-002 | Specific MY2004–05/VIN/manual conditions |
| 9-5 B205/B235 ventilation hose detachment | corrections-issue-003 | Specific throttle-body hose and production cohort |
| Trionic 7 IDM electrical overload | corrections-issue-004 | Four-cylinder and B308 must retain separate serial, engine and campaign applicability |
| Early NG9-3 auto cooler quick-coupler O-ring displacement | corrections-issue-005 | Narrow program scope, distinct from TA440-0702 |
| NG9-3 FA57 cooler-nipple seal and coolant-contaminated ATF | corrections-issue-006 | Separate Sport Sedan/TiD/CV cutoffs in original technical advice |
| Early NG9-3 CIM remote software defect | corrections-issue-007 | Not a generic key/ISM issue |
| Early NG9-3 faulty key/remote acceptance | corrections-issue-008 | Not proof all CIM faults need module replacement |
| Early NG9-3 ISM detector material defect | corrections-issue-009 | Not all START BLOCKED messages |
| B207 intake-valve face/seat wear | corrections-issue-011 | Original engine/model-year split must be retained |
| NG9-3 front spring corrosion/fracture | corrections-issue-014 | Special coverage climate/region and model constraints |
| NG9-3 right-hand A-pillar seam water entry | corrections-issue-015 | Specific sealed seam location, not all interior dampness |

The **one suspected** source-origin defect, **corrections-issue-012**, records an engineering **hypothesis** about B207 block casting porosity when coolant loss is otherwise unexplained. It must not be promoted to confirmed porosity without testing and factory evidence.

The six distinct documented campaign hazard/nonconformance identities include the Takata driver inflator, later NG9-3 fuel pump, two *separately described* sedan belt-cable campaigns, MY2008 OG9-5 occupant-impact A-pillar compliance, and NG9-3 convertible belt-retractor cable. An original campaign describes risk and eligibility; it **does not measure how many cars actually failed**.

**Excluded from factory-defect counting:** the original B205/B235 sludge bulletin can list *multiple causes* rather than one verified failed original part; cold-compression diagnostic cases can identify the B207 valve-wear risk but do not independently prove a mechanical defect on a vehicle; service torque errors, aftermarket cross-brand catalogue discrepancies, uncertain seller catalyst claims and WIS mirror year mismatches are important research records, **not separate endemic Saab failures**.

## 3. Explicitly recorded cross-research relationships

- **T7 electrical overload:** one mechanism, multiple affected 4-cylinder and B308 *cohorts*. Existing tier cases both reuse corrections-issue-004; neither can be evaluated from model year alone.
- **FA57 coolant contamination:** corrections-issue-006, hcdiag-issue-003 and maint-issue-002 refer to the same original manufacturer technical advice, stored under different source IDs. **corrections-issue-005** is a separate narrower cooler O-ring campaign—related, not an identical bulletin population.
- **B207 valve wear:** corrections-issue-011 contains the factory failure mechanism while hcdiag-issue-002 adds a diagnostic interpretation. A 2006 compression-screening scenario is **not** silently assigned to that later production advisory.
- **Takata:** corrections-issue-016, corrections-issue-020 and wp7-issue-004 share a hazard identity, but manufacturer service, original regulator report and market/registration history can be different.
- **9-5 left engine mount:** gate5-issue-003, parts95-issue-003 and coolsvc-issue-002 share a factory VIN torque cutover context, not proof of three separate defective mounts.
- **Source year conflict:** gateac-issue-001 and vinfit-issue-001 document mislabeled original/MY2010 information within different WIS-year mirrors; this is a research provenance trap, **not a car failure**.
- **Ignition diagnosis:** og95t7-issue-004 concerns *wiring and power/feedback* and must not be merged as if every ignition fault resulted from the recalled IDM overload.

Every automatically joined fact/part/gap ID in the generated catalogue means **the same original document URL is cited somewhere in the database**. It does **not** necessarily establish the same technical statement, warranty service revision, failure mechanism or installed assembly. The generator retains explicit reviewer relationship notes separately.

## 4. How to use the complete existing evidence rather than repeat it

To generate a lossless view of all 92 issues, including original source IDs, URLs, applicability and matching source-citation navigation for facts, parts and gaps:

```sh
python3 tools/build_legacy_issue_index.py --check --summary
python3 tools/build_legacy_issue_index.py --find "FA57"
python3 tools/build_legacy_issue_index.py --find "corrections-issue-011"
python3 tools/build_legacy_issue_index.py --find "ignition"
python3 tools/build_legacy_issue_index.py --output /tmp/saab-legacy-issue-index.json
```

Use the existing [all-dataset reuse audit](research-reuse-audit-20261014.md) for URL overlap, fact and part-number collisions. The new 92-issue catalogue and the original 562 source records are complementary.

**New-research rule:** Before a new defect PR is opened, require an explicit citation check against this index and original Saab/regulator bulletin numbers, and state whether a claimed advance is (a) a **different component/root cause**, (b) a **newly verified affected cohort or revision**, (c) **previously unknown sourcing or repair proof**, or (d) **new regulator/factory evidence**. Don't record an existing issue a second time solely because a different research package requires it.

## 5. What is and is not complete

- **Now reconciled:** all **92 records** from the *existing issue arrays* at this revision; all 21 defect/campaign/suspected records mapped to canonical mechanism IDs; two tier mechanism IDs reconciled without duplicating prior research; original source URLs preserved, including cross-domain aliases.
- **Not yet reconciled as a component-failure study:** individual technical claims in the **1,101 facts**, all **89** part records and **284** gap records. They are discoverable through citation links, **not reviewed as proof of equivalent mechanisms or closed gaps**.
- **Not established:** manufacturer-wide original Saab TSB/recall denominator and exhaustive source retrieval; equal coverage across every platform/engine/year/market/body; measured fleet durability, 2026 VIN-appropriate delivered parts fulfillment, or complete installed repair economics.

**Next actual research task:** assign existing fact, issue, part and gap evidence to the 16 subsystem classes **by exact cohort and evidence type**, then review the five repeated part-number groups and open research gaps before conducting an outside missing-bulletin sweep. This is consolidation, not a model tiering or new PR of isolated failures.

The CI gate fails if new saved issues are added without manual primary category, or if a specific defect/campaign gets a speculative or missing mechanism identity. Full factory/source engineering review remains separate from passing automated tests.
