# U.S. Saab factory engine identity and no-rebuild screening — Phase 0

**Research date: 2026-10-13.** This crosschecks **all 110 distinct U.S. source-derived automatic/FWD/nonconvertible Saab 9-3 and 9-5 production groups** from [the normalized register](../data/vehicle-catalogue/us-production-normalized.json) against original Saab manufacturer workshop identity and diagnostic documentation. Original Saab WIS is mirrored at SaabWISOnline; production counts originate separately with eSaabParts. The [machine-readable evidence crosswalk](../data/vehicle-catalogue/us-engine-factory-review.json) is **NOT 110 individually inspected VINs**, an approved engine/interchange or a fault-frequency survey. Existing Canadian research and source-scoped technical datasets remain unchanged.

## Engine family and production-group denominator

| Platform | Original U.S. eligible recorded family | Groups | Factory source alignment |
| --- | --- | ---: | --- |
| 9-3 9400 (1999–2002 hatch) | **B204L** turbo inline-four | 4 | Saab WIS 1999 B204 turbo system, WIS MY2000 engine/VIN code `N` |
| 9-3 9400 | **B205L** turbo inline-four | 4 | MY2000 original 9-3 VIN code `H` and MY2001 B205 power specification |
| 9-3 9400 | **B205R** turbo inline-four | 3 | MY2000 original 9-3 VIN code `K` and MY2001 B205R power specification |
| 9-3 9440 (MY2003–11) | **B207L** 2.0L turbo inline-four | 3 | MY2004 9-3 WIS technical data; MY2008 VIN code `S` |
| 9-3 9440 | **B207R** 2.0L turbo inline-four | 25 | MY2004 9-3 WIS technical data; MY2008 VIN code `Y` |
| 9-3 9440 | **B284L** 2.8L turbo V6 | 6 | MY2006 factory engine-number pattern, MY2008 VIN code `U` |
| 9-5 9600 (MY1999–09) | **B235E** 2.3L turbo inline-four | 15 | MY2000 WIS B235 engine systems; MY2004 VIN code `E` |
| 9-5 9600 | **B235L** 2.3L turbo inline-four | 4 | MY2004 factory technical data, VIN code `A`; do not assume it existed as a 1999 U.S. option |
| 9-5 9600 | **B235R** 2.3L turbo inline-four | 32 | MY2000 factory engine systems; MY2004 VIN code `G` |
| 9-5 9600 | **B308E** 3.0L turbo V6 | 13 | MY2000 Saab WIS V6 engine-management section. Do not carry it into MY2004 Arc, which has B235L |
| 9-5 650 / WIS 9650 (MY2011) | **2.0T** compiled source label → factory candidate **A20NFT/LHU** | 1 | Saab MY2011 VIN pos8 `Z` for A20NFT/LHU gasoline 2.0T, `R` for BioPower 2.0T; pos7 `A` FWD six-speed AT. The U.S. compiled register does not give VIN position 8; **no individual engine variant is certified**. |
| **Total** | | **110** | Family/name corroboration only; **0 actual vehicles VIN/stamping verified** |

### Why these details matter

**Engine code ≠ trim/year.** A 2002 original 9-5 Arc automatic uses B308E V6, while a 2004 Arc automatic is B235L four-cylinder. Similarly, the 2008 9-3 Aero FWD uses B284L V6 while eligible 2010–2011 Aero FWD groups use B207R turbo inline-four. The actual generation, market, powertrain code, and physical VIN need to agree before looking up service components. Workshop engine-code lists by themselves are not approval of any individual seller's description or a parts-donor assembly.

**Original Saab VIN character locations** that can be used *after receiving the actual vehicle VIN*:
- 9-3 9400 MY2000: position 7 `8` = 4-speed AT; position 8 `N` = B204L, `H` = B205L, `K` = B205R. Exact model-year VIN chart is required for other years.
- 9-3 9440 MY2008: position 6 `4` = sedan or `5` = five-door; position 7 `9` = 5AT/FWD or `1` = 6AT/FWD; position 8 `S` = B207L, `Y` = B207R, `U` = B284L. This **2008** chart must not be automatically projected to other model years.
- 9-5 9600 MY2004: position 6 `4` = sedan or `5` = wagon; position 7 `9` = 5AT; position 8 `A` = B235L, `E` = B235E, `G` = B235R. Use an actual **2004** VIN, not the production-register engine name alone.
- New 9-5 WIS 9650 MY2011: position 7 `A` = 6AT/FWD; position 8 `Z` = A20NFT/LHU 2.0T or `R` = A20NFT/LHU BioPower; model-year position 10 `B`. The compiled 2011 US Turbo4 row itself only says `2.0T`.

**These mappings identify engine families; they are not anti-theft key, ECU programming, complete powertrain interchange, market-version, or current inspection certificates.**

## Engine rebuild avoidance: connect factory evidence to pre-purchase tests

Six research topics, defined in the JSON crosswalk, describe **what evidence might distinguish an external repair from unacceptable internal damage**. They complement the existing `high-cost-powertrain-diagnostics` and `priority-nonrunning-purchase-screen` datasets; they do not duplicate those technical records or claim fleet rates.

### 1. Early B205/B235 sludge, chain noise, low oil pressure and bearing damage (US/CA bulletin)

Saab U.S./Canadian technical service bulletin **210-2554 edition 3 (June 2006)** covers **original 9-5 MY1998–2003 B205/B235** and **original 9-3 9400 MY1999–2003 B205/B235**. It explicitly distinguishes low oil level/sensor problems, clogged oil pickup symptoms and timing/balancer chain service from **bearing damage**, for which the manufacturer directs short-block replacement. In our **eligible** U.S. production matrix, **28 groups** are affected by this *engine/year applicability*; this count is **not 28 failure cases**.

- **Requires verification:** history of PCV updates/engine oil, engine symptoms, qualified controlled mechanical oil pressure when appropriate, sump/pickup/bearing inspection if diagnostic evidence warrants. Use Saab's exact procedure; a warning lamp or lower-end knock is not permission to keep running an engine with possible oil starvation.
- **Do not claim:** all B205/B235 engines failed, 1999 B204L is covered, the special warranty still exists, all MY2004+ B235s had the same bulletin applicability, or replacing PCV restores damaged bearings.
- **For this DIY project:** documented internal bearing damage or an engine that cannot be safely assessed is a **high-risk, typically reject/price-for-complete-engine-replacement** scenario, whereas a PCV hose or properly isolated chain service is a separate repair decision.

The related all-market Saab **210-2417 ed.4** documents crankcase ventilation limited flow and a service kit for 9-5 MY1998–2003 B205/B235 with oil leakage. This does **not** establish that a seller's car received that kit or that oil sludge never occurred.

### 2. B207 9-3 9440 cold-misfire and compression investigation

The repo already has B207 cold-start valve-sealing research (`hcdiag-issue-002`) and a nonrunning low-compression screen (`nrscreen-issue-003`). Original **MY2006** WIS specifies minimum compression and the MY2005 workshop has compression, oil-pressure and timing/balance-chain check procedures. Match the **actual car/year/engine** before using a numerical compression threshold: a 2006 WIS figure is not an unsupervised cold-test acceptance for every 2003–2011 B207. Distinguish ignition, fuel and ECU faults from real cylinder sealing damage; a cold start misfire **alone** cannot price a cylinder-head job.

### 3. B284L 9-3 Aero V6 architecture is not a proven failure rate

Saab MY2006 WIS describes a 2.8L turbo V6 with **chain-driven camshafts** and variable cam phasing. It does **not** quantify timing-chain failures or prove every used V6 needs a chain kit. Verify actual engine number, stored faults, start/run noises and applicable original repair procedure. The technical/database coverage for B284 remains thinner than B207/B235; **unassessed is not unreliable**.

### 4. New 9-5 2011 2.0T engine: separate A20NFT/LHU generation

Saab MY2011 WIS includes a **special-tool timing-chain check** (EN-49212), plus independent mechanical diagnostic paths for lower/upper noise, compression, coolant/oil consumption and turbo oil starvation. These procedures establish ways to investigate a symptom **without** assuming this engine shares the B207/B235 fault profile. The actual Turbo4 VIN and engine identification must precede parts sourcing. No frequency or replacement cost is established.

### 5. Original 9-5 B308E V6: avoid four-cylinder fault transposition

B308E appears in original 9-5 factory 2000 WIS but is **not** covered by the B205/B235-specific sludge bulletin. A prospective B308E must have its own original-year V6 diagnostics and real-world repair estimate before being accepted or rejected.

## Still unclosed, despite completing this evidence crosswalk

- No actual candidate VIN, photographed engine number, transmission case label, service history, hot oil pressure, crank/compression results, leakdown, cooling pressure test, fault snapshot or specialist estimate exists yet.
- A factory workshop page for one model year does **not** prove every recorded color-level production group is legitimate or shares every later engineering revision. The five source-reported ultra-low-volume production groups remain pending original build verification.
- Actual **engine/transmission replacement** costs, credible DIY hours, tools, and evidence of improved longevity remain unknown. This is a readiness and diagnostic evidence map, **not** a purchase ranking.
- Phase 0 Gate A remains partial; B/C unmet. The 554 sources, 1,086 facts, 91 issues, 86 parts and 280 source-dataset gaps are *not modified or artificially increased* by this separate vehicle-research overlay.

## Source retrieval / reproducibility

The JSON dataset records **17 exact factory-source links** with original model-year/market scope, **110 engine reviews**, and **six diagnostic/research topics**, preserving unsupported claims as separate forbidden conclusions. Run:

```sh
python3 tools/validate.py
python3 -m unittest discover -s tests -v
python3 tools/phase0_audit.py --check
```

After this PR the most useful next step is to produce a **VIN decoding and field-inspection checklist** for real U.S. Saab sellers, followed by source-backed failure/cost screening for the eleven engines before we assign any preference among cars.
