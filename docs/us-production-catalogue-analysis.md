# U.S. Saab production-normalized automatic/FWD catalogue: first complete register pass

**Candidate policy:** Saab 9-3 / 9-5, U.S. original market, MY1998–2011, factory automatic transmission, **front-wheel drive**, and **no convertibles**. Canada remains recorded in the separate North American research catalogue and was not modified.

This report summarizes the automatically generated [U.S. source-derived production matrix](../data/vehicle-catalogue/us-production-normalized.json), built by `tools/us_production_import.py` from the four live [eSaabParts compiled U.S. production tables](https://www.esaabparts.com/saab/production/). **Complete here means all paint rows of all four *third-party compiled* tables have been processed; it does not mean original manufacturer production/option data have been exhaustively certified.**

## Count and source-data reconciliation

| Platform | Saab | Compiled source all-vehicle count | Distinct eligible configuration groups | Source-reported eligible automatic FWD units |
|---|---|---:|---:|---:|
| 9400 | 9-3 original hatch | 94,266 | 11 | 35,597 |
| 9440 | 9-3 Sport Sedan / SportCombi | 159,444 | 34 | 99,247 |
| 9600 | Original 9-5 sedan / SportCombi | 120,454 | 64 | 103,833 |
| 650 | New 9-5 sedan | 3,419 | 1 | 1,981 |
| **Total** | | **377,583** | **110** | **240,658** |

All four published **unfiltered** source totals reconcile exactly with the sum of parsed paint rows (375 / 1,226 / 964 / 51 source paint rows, respectively). **The 240,658 figure is not the number of cars on the road or for sale today.** It is a sum of units *reported* in historical third-party tables for qualifying groups, and not independently verified against manufacturer VIN data.

### Year-by-year source-derived configuration groups

| US MY | 9-3 qualifying groups | 9-5 qualifying groups | Significant distinctions |
|---|---:|---:|---|
| 1998 | 0 | 0 | Both U.S. nameplates started as model-year 1999 |
| 1999 | 4 | 8 | Original 9-3 B204L 4AT and 9-5 B235E/B308E 4AT |
| 2000 | 3 | 7 | Original 9-3 B205L/B205R; 9-5 Aero 4AT |
| 2001 | 3 | 7 | Original 9-3 B205 family and 9-5 four-speed autos |
| 2002 | 1 | 6 | 9-3 SE hatch 4AT only; 9-5 switches to 5AT family |
| 2003 | 3 | 6 | New 9440 9-3 nonconvertible sedans with 5AT; 9400 continues only as excluded convertible |
| 2004 | 3 | 5 | 9-5 Arc B235L turbo I4, not previous Arc V6 |
| 2005 | 4 | 5 | Very small 9-3 Vector B207R automatic count deserves VIN review |
| 2006 | 4 | 4 | 9-3 Aero B284L V6 6AT / 2.0T B207R 5AT; 9-5 B235R 5AT |
| 2007 | 6 | 6 | Sixtieth Anniversary U.S. trims separately recorded |
| 2008 | 4 | 4 | 9-3 2.0T FWD 5AT and Aero V6 FWD 6AT |
| 2009 | 2 | 6 | U.S. nonconvertible 9-3 Aero XWD excluded; 9-5 Griffin B235R auto recorded |
| 2010 | 4 | 0 | U.S. 9-3 Aero FWD B207R 5AT; new 9-5 launch XWD excluded |
| 2011 | 4 | 1 | 9-3 2.0T/Aero FWD B207R 5AT; new 9-5 Turbo4 2.0T FWD 6AT |

The exact list of **110** normalized rows, engine codes where printed and source-reported production counts is in the linked JSON. Color choices have been collapsed within each year/model/platform/trim/body/engine/automatic/drivetrain key, avoiding duplicate configurations.

## Manual-review candidates

The source includes these particularly low-volume entries (12 or fewer reported units); they are **not** dismissed or silently promoted to fully factory-verified builds:

| MY | Saab configuration in compiled register | Units reported |
|---|---|---:|
| 1999 | 9-3 SE 3-door hatch, B204L 4AT | 3 |
| 2005 | 9-3 Vector sedan, B207R 5AT | 4 |
| 1999 | 9-5 SE wagon, B235E 4AT | 9 |
| 1999 | 9-5 Standard sedan, B308E 4AT | 12 |
| 2001 | 9-5 Standard sedan, B308E 4AT | 1 |

These deserve an original Saab VIN/build-source check. Low production counts may reflect rare cars, unusual designation mapping, special vehicles or data errors; they do **not** independently prove fitment, durability or current market supply. The generated JSON labels such groups `low_volume_manual_review: true`.

## Exact scope limits and next research decision

- This **compiled-register pass is complete and reproducible**, but **factory model-year completeness is not certified**. Registries can omit, misidentify, or miscount vehicles. A missing group is not conclusive proof Saab never produced one.
- The 9-5 650 U.S. table calls all qualifying 2011 FWD automatic cars `Turbo4`. Manufacturer equipment materials distinguish Turbo4 and Turbo4 Premium; the source does **not** support splitting its 1,981 vehicles by those factory trim sublevels.
- Original 9-3 9400 five-door is a **hatchback**. 9-3 9440 and 9-5 9600 five-door are **SportCombi/wagon** models. A five-door body code is not a sufficient body-style identifier.
- Automatic `4AT`/`5AT`/`6AT` describes the gearbox *gear count only*. It is **not the factory transmission family, control-module ID, option code, replacement interchange, VIN range or service procedure**.
- Neither production volume nor U.S. trim prevalence establishes comparative reliability, DIY cost, rust status, parts lifetime, or worthiness of an unseen car.
- Existing `data/vehicle-catalogue/north-america-1998-2011.json` has 77 U.S. research examples; its applicable model/year/platform/body/automatic records structurally match at least one of these production groups, **but only 20 have source-populated engine codes**. This is useful reconciliation, not independent manufacturer certification. No Canada records were altered.

**Next gate within Phase 0:** Cross-check these 110 source-derived groups against *original U.S. Saab factory model-year sales, VIN and gearbox specification documents*, resolve low-volume anomalies, map physical automatic transmission families, and only then compare catastrophic engine/transmission risks. The current Phase 0 gates remain A partial, B/C unmet.
