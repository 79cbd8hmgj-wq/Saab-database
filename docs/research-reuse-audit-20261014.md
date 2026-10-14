# Whole-repository research reuse audit — 2026-10-14

**Conclusion: Stop discovering factory defects already represented in the database. Reconcile and link the existing evidence before another collection PR.**

This is an **entire-dataset structural and research-overlap audit**, not a page-by-page recertification of every original Saab document. The reproducible analyzer is [tools/audit_research_reuse.py](../tools/audit_research_reuse.py); [CI and its regression suite](../tests/test_research_reuse_audit.py) run it. No vehicle tiers, reliability rates, new defects, VIN-fitment approvals or model preferences are introduced.

## 1. Existing material

| Database quantity | Count | Interpretation |
| --- | ---: | --- |
| Dataset domains | **42** | Research topics; not 42 independent technical studies |
| Stored source records / distinct exact source URLs | **562 / 494** | Domain-specific citations; many repeated documents |
| Technical facts | **1,101** | Specifications and observations, not defect count |
| Issue records | **92** | Selected faults, service/diagnostic cases, campaigns, not all known Saab factory issues |
| Part records / open research gaps | **89 / 284** | Sources and questions, not approved interchanges or unique missing faults |
| Source-derived U.S. automatic/FWD/nonconvertible configuration groups | **110** | Not the full U.S./Canadian Saab family |
| New tier-ledger case records / engineering mechanisms | **3 / 2** | No implication these were newly discovered |
| Tier-ledger quantified failure studies, fulfilled part offers and complete repair quotes | **0 / 0 / 0** | Existing older retail price snapshots are not verified fulfilled repair offers |

The older [research overview](research-overview.md), [corrections domain](../data/datasets/corrections.json), [high-cost powertrain diagnostics](../data/datasets/high-cost-powertrain-diagnostics.json), and [Phase 0 gap audit](phase0-gap-audit-2026-10-13.md) contain relevant information that predates the tier-ledger work. The [current coverage audit](coverage-audit.md) measures *stored record counts*, not factory bulletin completeness.

## 2. Proven re-research in PR #67

| Tier failure case | Already present in | What was actually new |
| --- | --- | --- |
| Four-cylinder IDM electrical overload | **corrections-issue-004** | Structured four-cylinder revision/case record; new regulator details |
| B308 V6 IDM electrical overload | **corrections-issue-004**, with separate V6 scope in the original Saab bulletin | Structured separate engine cohort and revision details |
| FA57 cooler-seal coolant ingress | **corrections-issue-006** and **hcdiag-issue-003** | Reorganized the existing technical advice into a tier case |

The FA57 original bulletin TA440-0702 is cited under **corrections-src-004**, **hcdiag-src-014**, and **maint-src-013**: **three different source IDs referring to the same manufacturer document URL**. Requiring identical source IDs for detecting prior work therefore gives false negatives.

**corrections-issue-005** is related but **not a duplicate**: that record covers the narrower coolant-coupling campaign, while TA440-0702 gives the distinct technical-advice population and diagnostic context. Never collapse campaign eligibility into all-market technical-advice applicability.

PR #67 did add useful structured QP3 component-revision details. The problem is that it failed to show source and legacy-issue lineage before claiming to populate the first failure records.

## 3. Quantified cross-dataset overlaps

| Potential repeat class | Measured | Editorial interpretation |
| --- | ---: | --- |
| Reused exact source URL clusters | **53** | **68** more source records than distinct URLs |
| Cross-domain issue clusters sharing an original source URL | **18** | Review for a common mechanism versus different findings from one bulletin |
| Same subject + predicate + value fact clusters | **76** | Many can be intentional year-specific repetitions; **not automatic duplicates** |
| Repeated exact part-number clusters | **5** | Different catalog claims or assembly contexts may need separate records |
| Normalized identical-title gap clusters | **2** | Existing workstream blockers repeated under different IDs |
| Normalized identical-title issue clusters | **0** | Different wording still permits semantic overlap |
| Dataset domains with no issues array entries | **14** | Specifications, sources and part research can exist without issue classifications |

Selected **source reuse clusters** demonstrating the navigation problem:

- Saab Parts subscription/EPC access page: **5 IDs** in five domains. This is **not five VIN-specific EPC confirmations**.
- Saab 9-5 MY2009 engine lubrication specification: **4 IDs** across maintenance, OG9-5 specification, high-cost diagnostics and nonrunning screening.
- Saab TA440-0702 FA57 cooler contamination: **3 IDs**, used in three domains.
- Saab NG9-3 subframe service, OG9-5 radiator procedure, OG9-5 coolant pressure/temperature limits, and 2008 turbo tech data: each appears in **three** source domains.
- Retailer listings for PCV kit **21341200** and radiator **32019620** each appear in **three** source domains. Repeated listings are not independent current stock.

**Repeated part numbers with prior records:**

| Part number | Existing records |
| --- | --- |
| 21341200 | corrections-part-022; pcv-supply-part-002 |
| 32021815 | corrections-part-016; gate5-part-002 |
| 55558696 | b235rev-part-001; corrections-part-007 |
| 55561200 | corrections-part-001; pcv-supply-part-001 |
| 5961610 | b235rev-part-005; corrections-part-008 |

**Duplicated research blocker titles:**

| Open blocker | Existing IDs |
| --- | --- |
| Canadian MY2006 9-3 VIN/option mapping and original build verification | gateac-gap-002 and vinfit-gap-003 |
| U.S. MY2008–09 9-5 VIN codes plus Canada cross-check | gateac-gap-001 and vinfit-gap-001 |

These are **overlap leads**, not commands to delete data. Parts may carry different manufacturer/supplier claims and applicability. Repeated fact values may legitimately describe separate original model years or test conditions. The manufacturer source, original scope and uncertainty must survive editorial reconciliation.

## 4. Unfinished comprehension, despite the large record count

Substantial documentation is already stored for both original and later 9-3/9-5 platforms: oil/PCV/sludge, turbos, cooling, fuel/EVAP, T7/T8 and key/security modules, legacy/FA57/AF40 drivetrains, steering/suspension and subframes, brake hydraulics, recalls, VIN tables, parts and cross-brand sourcing, diagnostic tooling and DIY/nonrunning screening. It would be wasteful to re-query all of these from scratch.

However, this is **not a complete manufacturer TSB/campaign inventory** for all North American Saab years, engines, gearboxes, bodies, production revisions or all models. In particular:

- The **92 issue records** do not form a canonical, de-duplicated **factory defect mechanism index**.
- The **1,101 facts and 89 parts** have not been source-adjudicated into the [16 comparable tier research systems](../data/tier-research/methodology.json).
- The **284 gaps** are tasks and unknowns, some duplicated; they are not an exact number of missing factory failures.
- The 110-group automatic/FWD reference captures **research leads**, not the complete Saab market, field reliability, individual-VIN interchange or delivered total repair costs.
- The [three-entry tier ledger](../data/tier-research/observations.json) underrepresents the technical mechanisms already discussed elsewhere.
- The validator and tests check structural contracts and selected known contradictions. **Neither a green test run nor the label “full_text” independently proves every technical claim.** An externally verified, exact-population factory bulletin and recall coverage denominator is missing.

A claim such as “we have researched all Saab factory issues” would be unsupported. Equally, a claim such as “we only have three documented problems” would be false.

## 5. Documentation and workflow consistency

The audit scanned **64 Markdown files** and **247 local relative links** and found **zero broken local links**. This checks navigation, not whether an old recommendation is current.

It identified two documentation-drift cases:
1. The top of [coverage-audit.md](coverage-audit.md) previously called itself a **41-domain** refresh despite the current **42-domain** table; corrected in this audit PR.
2. [research-overview.md](research-overview.md) contains an older **provisional car-priority section**. This is now labelled as historical research context in the older file; it is **not a current ranking**, and the user has requested no early ranking.

The huge [source index](source-index.md) successfully tracks source retrieval but does not yet tell a researcher whether a newly proposed problem is **already in another data domain**.

## 6. Concrete reuse-first corrective plan

**First: consolidate access, not erase original records.** Generate the complete 92-issue index from the audit script and manually match the older problem records to canonical engineering failure-mechanism IDs and exact original platform/year/engine/gearbox/body/serial subgroups. Retain all source references and distinguish complaint, recall, technical advice, original design revision and specific repair event. The current three tier cases now have explicit tested bridges to prior records.

**Second: reconcile repeat parts and blockers.** Review the five repeated part-number sets and two repeated blocker-title sets before adding more versions. Preserve directed manufacturer supersession versus supplier catalog references, conditional kit contents and unverified donor claims.

**Third: inventory actual completeness.** Assign the existing documents, issues, facts, parts and gaps to all 16 tier system categories and each agreed market/configuration cohort; label **known design mechanism, source-only lead, validated replacement, observed supply/cost, missing source, needs actual VIN/measurement**. Do not invent numerical percent completeness.

**Fourth: search only proven gaps.** Once existing material is indexed, use manufacturer bulletins, regulator campaigns and real replacement offers to find specific missing evidence. A future PR must identify the *existing source URLs/IDs and issue IDs searched*, what is demonstrably **new** (new source, stronger access, production revision, application exception, repair pathway, or closed gap), and what is deliberately reused. More record count is not a research success by itself.

**Finally: maintain no-ranking policy.** Do not introduce Saab model tiers until original component durability, defect severity and probability where measurable, VIN-gated parts availability, and practical DIY/shop repair cost have been compared on a sufficiently symmetric basis.

### Repeatable command

Run **python3 tools/audit_research_reuse.py --summary** for all-dataset counts, overlap examples and full domain counts. Run **python3 tools/audit_research_reuse.py --output /tmp/saab-reuse-audit.json** to export the complete 92-issue catalogue plus all URL/fact/part/gap overlap clusters. CI also runs this script and its tests on subsequent work.

**Audit boundary:** This is the comprehensive *repository inventory, overlap and workflow audit*, **not** a claimed exhaustive external Saab service bulletin audit. The latter should follow the source-reconciliation work, not precede it.
