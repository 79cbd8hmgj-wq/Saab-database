# North American Saab automatic-FWD model catalogue — first verified batch (2026-10-13)

**Scope:** Saab 9-3 and 9-5, MY1998–2011 inclusive, original US/Canadian market only, **factory automatic only**, **FWD only**, **nonconvertibles**. European-only models, manual-only variants, XWD/AWD and 9-3X are not eligible. This is the first **partial** research batch; it does not claim exhaustive model-year or trim completeness.

The machine-readable companion [initial NA model-year screening and evidence records](../data/vehicle-catalogue/north-america-1998-2011.json) contains **28 model/year screening rows**, **11 sourced example configurations**, **15 source references** and **5 source-grounded exclusions/cautions**. Screening rows with missing evidence remain `unassessed`; there is no invented availability or reliability score. US and Canada are checked separately.

## Confirmed candidate examples (NOT a complete trim list)

| Market | MY | Platform | Body | Engine offering | Factory automatic | Evidence |
|---|---:|---|---|---|---|---|
| US | 1999 | 9-3 9400 | 3-door hatch | 2.0L 185-hp turbo | 4-speed | Initial MY1999 US announcement + historical trim list (gearbox/year secondary corroboration) |
| US | 1999 | 9-5 9600 | Sedan | 2.3L 170-hp turbo | 4-speed | Saab Cars USA MY1999 manufacturer press |
| US | 1999 | 9-5 9600 | Sedan | 3.0L 200-hp V6 turbo | 4-speed | Saab Cars USA MY1999 manufacturer press |
| US | 1999 | 9-5 9600 | Wagon | 3.0L V6 turbo | 4-speed | Saab US wagon launch + period US trim reference |
| US | 2000 | 9-5 9600 | Aero sedan | 2.3L 230-hp turbo | 4-speed | Saab Cars USA MY2000 manufacturer press |
| US | 2000 | 9-3 9400 | SE five-door | 2.0L 205-hp turbo | 4-speed | Saab Cars USA MY2000 manufacturer press + US trim catalogue |
| US | 2002 | 9-3 9400 | SE five-door | B205R 2.0L turbo | 4-speed | Saab M2002 US product overview |
| US | 2003 | 9-3 9440 | Linear/Arc sedans | 2.0L turbo 175/210 hp | 5-speed | Historical 2003 US configuration reference, awaiting direct Saab brochure corroboration |
| US | 2011 | 9-5 650 | Turbo4 sedan | 2.0L 220-hp turbo | 6-speed | US MY2011 trim listing + period launch analysis |
| Canada | 2011 | 9-5 650 | Turbo4 sedan | 2.0L turbo | 6-speed | Canadian 2011 model specification/price listing |

## Verified pitfalls / exclusions

- **1998 U.S. MY:** Saab's U.S. distributor launched both nameplates in spring 1998 as **MY1999**, not MY1998 (source `na-cat-s01`). Whether a distinct 1998 **Canadian** model-year entry exists remains unanswered.
- **2002 U.S. Viggen:** B235R Viggen was manual-only according to Saab's US/CA product overview. Do not mistake its FWD body for an eligible automatic (`na-cat-s06`).
- **2003 U.S. 9-3:** the new nonconvertible sedan is 9440; the carried-over 9400 is convertible, which is excluded (`na-cat-s07`).
- **2010 U.S. new 9-5:** the launch Aero was a **2.8L V6 six-speed automatic XWD**, ineligible under FWD-only criteria. A US MY2010 FWD offering is not established in inspected launch sources; Canada needs independent assessment (`na-cat-s09`, `na-cat-s10`).
- **2011 U.S./Canada 9-5:** a Turbo4 **FWD six-speed automatic** does qualify, despite AWD being available on other 9-5 trims (`na-cat-s11`, `na-cat-s12`).

## Remaining acceptance work

1. Obtain factory US/Canada year-specific sales guides for every remaining model/year (separate Canadian equipment tables rather than copying US availability).
2. Convert each year into complete **engine + transmission code + body + FWD + market** combinations, with factory sales source citation and VIN constraints.
3. Verify 1999–2002 9400 subtrims; 2003–2011 9440 sedans and SportCombis; 1999–2009 9600 sedans/wagons; MY2010/2011 650 regional equipment and emissions.
4. Mark manual-only or XWD-only packages excluded even if model/year has another eligible trim.
5. Then connect eligible vehicle identities to the existing source-scoped failure, rust, parts, maintenance, and high-cost DIY-repair data. Do not rank on source count.

**Existing technical dataset census is unchanged:** no source, fact, issue or part entry is falsely added to `data/datasets/` by this separate catalogue. Phase 0 remains Gate A partial; B/C unmet.
