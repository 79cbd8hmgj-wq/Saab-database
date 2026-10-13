# Saab lot visit — quick field guide (October 16, 2026)

**Purpose:** In-person *evidence collection* at a lot with multiple stored/nonrunning Saabs. Target original **U.S.-market 1998–2011 Saab 9-3 and 9-5**, **factory automatic**, **FWD**, **sedan/hatch/wagon**. No manuals, convertibles or AWD/XWD. Canadian cars may be recorded separately but are not this visit's research priority.

**Most important rule:** We are **not** buying an unseen engine/transmission rebuild or a body-structural restoration disguised as an easy DIY fix. The first visit should leave us with a SHORTLIST, not pressure to make an offer. Every "easy fix" claim remains **seller-reported, unverified** until supported by a measurement or relevant invoice.

This is a condensed field companion to the existing [nonrunning purchase protocol](research/priority-nonrunning-purchase-screen.md), [safety/structure report](research/priority-structural-corrosion-inspection.md), [factory vehicle identity gates](research/priority-vehicle-identity-gates.md), and [U.S. repair-vs-replace matrix](us-repair-vs-replace-feasibility.md). It does not replace a qualified inspection or allow unsafe diagnostics.

## Before arriving

- Ask the seller **how many cars are accessible**, whether there are **keys**, whether titles exist, whether any are **running/rolling**, and whether they can point out the *least rusty and most complete* first. Ask permission to photograph VIN labels, engine bays and the externally visible underbody.
- Arrange to inspect **in daylight**. If arriving after dark, prioritize collecting IDs and scheduling a second **daylight/lift** visit; do not judge serious underside corrosion by a phone flash alone.
- Bring **charged phone, power bank, strong flashlight/headlamp, work gloves, inspection mirror, a rag, notepad or offline notes**, sturdy shoes; a read-only OBD scanner is optional but **may not reach Saab-specific TCM/body data**. A Tech2 technician would be later, not required for this first inventory pass.
- Arrange **transport/towing**, title checking and inspection cost expectations separately. Do not bring purchase cash as the primary way to make a rushed decision. Never store a full actual VIN, seller's phone/address, title photograph, plate number or private messages in this public GitHub repo.

## Pass 1 — every car: ~2 minutes

Assign a simple private visit ID **S01, S02...** immediately. Record:

| Field | What to write or photograph |
| --- | --- |
| Identity | Exterior model/trim, seller's stated model year, sedan/hatch/wagon, automatic gear selector, FWD/possibly XWD. **Do not infer exact engine from the badge.** Privately photo full 17-character VIN and title year; note only `VIN privately captured: yes/no` in any public template. |
| Access & legal | One working key? Can doors/hood open? Seller has **original signed title / lawful transfer paperwork**? Title branded or lien? Any vehicle hard to access safely? |
| Why parked | Seller's **exact words**, *date last ran and last moved*, cause they think stopped it, diagnosis performed by whom/invoice, reason it hasn't been fixed. |
| Rust safety | Visible **sills/jack regions**, rocker pinch welds, rear wheel arches and wheelhouse, rear/front suspension mount regions **where visible without crawling underneath**, obvious brake/fuel lines and engine subframe. Note whether severe corrosion is suspected, not a professional ruling of safety. |
| Engine/driveline | Presence/completeness of engine/gearbox, wiring intact, fluids **only by safe cold passive observation**, visible leaks, broken timing/drive components, missing turbo/exhaust assemblies, evidence of fire/collision or flood. |
| Baseline image set | Front three-quarter, side, rear three-quarter, dashboard/odometer, engine bay, safely visible rust/lifting zones. Privately also capture VIN/door-label photos. |
| Offer facts | Seller asking price, whether negotiable, whether it must be removed by tow, tires rolling/steering access, whether spare parts or second donor included. |

**Pass-1 outcome:** `STOP` (major hazard or excluded configuration), `HOLD` (worth a deeper look but too many unknowns), or `FINALIST` (appears within scope, structurally promising from ground level, records/keys accessible). This is an evidence triage, **not a reliability score**.

## Pass 2 — finalists only: 5–10 minutes, passive checks

- Photograph underhood engine label and gearbox case plate **only if safely reachable without dismantling**; record expected Saab model/engine/AT family and unresolved physical identity. Compare to the [110 U.S. production groups](../data/vehicle-catalogue/us-production-normalized.json) afterwards.
- Get close photographs of **rear subframe/member and its BODY anchors**, rear floor/longitudinal rails, wheelhouse and brake/fuel line corrosion **from safe external angles**. For a 9-5 SportCombi, visible rear frame rust does **not** establish that the floor/captive nuts are sound.
- Observe whether **fluids show obvious cross-contamination** (only when cold and safely accessible), air intake/wiring cut or missing, radiator damaged, electrical/fuel leaks apparent. Do not open a hot pressurized reservoir or disconnect fuel lines.
- Ask seller for proof of diagnosis for: **"just a cat," "just a sensor," "needs a head gasket," "bad transmission," "just a battery."** Record what was tested, codes, date, mileage and who made the assessment. Treat vague answers as **UNKNOWN**, not as factual diagnoses.
- If power is safely available **with permission**, record an existing scan readout and freeze frames without clearing/resetting modules. **Do not jump-start, crank, rev, stall-test the gearbox, or road-test a stored/nonrunner merely to see what happens.** A competent mechanical check must first clear seizure/hydrolock/oil starvation and fuel/brake/structural hazards.

### Three outcome labels

| Label | Meaning | Next step |
| --- | --- | --- |
| **STOP / OUTSIDE DIY OBJECTIVE** | Unsafe body/suspension anchors or severely corroded load-bearing shell; fuel/brake safety failure; confirmed major bearing damage, nonrepairable gearbox, or forced internal engine/trans rebuild. Also manuals, convertibles or AWD/XWD excluded from our intended build. | Do not start, drive or crawl under. Walk away **unless** an independent professional repair estimate supports deliberate structural/complete powertrain replacement outside the original DIY goal. |
| **HOLD — NEEDS PROOF** | Unverified engine/no-start, seller's "clogged cat," unclear FA57 shifts, incomplete VIN/title, no key, no safe underside view, or no diagnostic invoice. | Collect evidence and price quotes. Request later lift/specialist assessment and qualified compression/oil-pressure/TCM diagnosis **only when safe**. |
| **FINALIST — FURTHER EVALUATION** | In-scope factory identity, apparently sound visible body/anchors (not full proof), intact components and a plausible externally repairable fault **backed by evidence**. | Arrange exact-VIN parts/market checks, sound-structure lift inspection, and documented mechanical inspection. **No automatic purchase authorization.** |

## Prior known seller claim: 2008 9-5 wagon, rear-subframe rust + "clogged cat"

These are **two separate unverified problems**. On site:
1. **Rust:** Is damage confined to a removable rear subframe, or are the captive nuts, rear floor, wheelhouses or longitudinal members/thin load-bearing mounting steel affected? If uncertain, classify **STOP/HOLD**, **no unsafe lifting**; seek a structural shop opinion.
2. **"Clogged cat":** Ask how restriction was measured, **which stage/assembly** was checked, whether the engine runs/misfires/smokes/burns oil, and whether there is an estimate. A P0420 code or seller statement **does not** prove a physically blocked converter, and a restriction may be a consequence of an upstream engine issue.
3. **Financial:** A $1,200 asking price cannot be considered cheap until towing, engine/TCM diagnostics, safe structure, emissions-correct parts and any professional repairs are priced. The car may still be useful as a parts donor **if lawful and economically sensible**, but don't assume its structural or emissions condition qualifies as a running project.

## Immediate post-visit workflow

Create an **individual private copy** of [the quick intake template](../data/inspection-templates/lot-rapid-20261016.json) for each car. Keep full VIN/title and seller contact in **private notes**, not the public repository. Then send a few photos and observations per car, ordered by provisional promise.

We'll match the privately supplied VIN evidence (if provided in a private conversation) to the **factory identity guide**, check that car's exact engine/gearbox against U.S. catalogue rows, identify factory-bulletin and parts gaps, and prioritize which vehicles deserve a qualified inspection. The result may be **no safe purchases**; that is an acceptable outcome.

**No source-backed price ceilings, year-by-year reliability rankings, or repair guarantees are implied.** Phase 0 A remains partial and B/C remain unmet until car-specific evidence appears.
