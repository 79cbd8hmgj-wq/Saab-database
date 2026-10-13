# U.S. Saab automatic-transmission families — factory workshop crosscheck (2026-10-13)

**Scope:** U.S. Saab 9-3 and 9-5, model years 1998–2011 inclusive, only the **110 previously normalized compiled-production groups** with automatic, FWD and nonconvertible bodies. Canada and manual/XWD/convertible cars are outside this analysis. This source overlay **does not change** the compiled production data, parts database, or eligibility rules.

The [machine-readable family-evidence overlay](../data/vehicle-catalogue/us-automatic-gearbox-evidence.json) is generated deterministically from the [production matrix](../data/vehicle-catalogue/us-production-normalized.json) and the source-scoped rules in [`tools/annotate_us_automatic_gearboxes.py`](../tools/annotate_us_automatic_gearboxes.py).

## Saab WIS-sourced factory identities

| U.S. model/platform | Compiled AT years | WIS family identity | Production groups annotated | Evidence scope |
| --- | --- | --- | ---: | --- |
| Original 9-3, 9400 | 1999–2002 | **AF20 or AF22** four-speed; example type `FA44` | 11 | Original Saab WIS **MY2001** names both families, **not** which individual engine/VIN received AF20 versus AF22. Do not designate every unit FA44. |
| Original 9-5, 9600 | 1999–2001 | **AF30** four-speed; example type `FA47`, `50-40LE` identifier | 22 | WIS **MY2000** describes AF30. Extension to adjacent compiled four-speed production years is **provisional platform/year inference**. |
| Original 9-5, 9600 | 2002–2009 | **FA57** five-speed | 42 | Original Saab WIS **MY2008** states that FA57 was fitted from **MY2002**. No year-specific version, fluid grade or complete assembly is approved from this. |
| Second-gen 9-3, 9440 | 2003–2011 | **FA57** five-speed | 28 | WIS **MY2006** says 9-3 FA57 designation began **MY2003**, adapted to B207 engines. |
| Second-gen 9-3, 9440 | 2006–2008 | **AF40 / Aisin TF-80SC** six-speed | 6 | WIS **MY2006** explicitly identifies the six-speed as AF40 / TF-80SC. US compiled groups here are FWD B284L Aero 2006–08. |
| Second-gen 9-5, 650 (WIS 9650) | 2011 | **AF40** six-speed | 1 | Saab 2011 9-5 WIS identifies the AF40 casing and defines VIN position 7 **A** as six-speed automatic FWD. Specific U.S. Turbo4 individual case-tag/part-number still needs VIN and physical confirmation. |

**Evidence-status census:** **99** groups have a Saab-WIS-backed *platform-family* attribution, while **11** original 9-3 automatic groups still have an unresolved AF20-versus-AF22 individual identity. **Zero** of the 110 groups have a physical VIN or case-tag match. All interchange/durability approval flags remain **false**. Platform-family attribution is **not** complete vehicle-specific gearbox verification.

### Why matching model names are not interchange permission

- **9-3 FA57 ≠ 9-5 FA57 drop-in proof.** The 9-3 WIS FA57 pages identify B207-specific control-module/engine coding; the original 9-5 workshop family label alone does not establish bellhousing, mounts, torque converter, ratios, electronics, immobilizer/programming or VIN-parts application.
- An `AF40` designation names a gearbox family; even `TF-80SC` does not certify complete donor interchange.
- A transmitted gear count `5AT` is not a Saab type label, OEM part number, or factory calibration.
- **The 2011 NG 9-5 650/9650 WIS names AF40**, but this must not be treated as a 9-3 AF40 interchange approval. Confirm the Turbo4's VIN (gearbox character A for six-speed FWD) and its actual AF40 case plate before selecting any fluid, control module, parts or replacement gearbox.

## Important avoid-an-engine-or-transmission-rebuild diagnostic avenues

These are *diagnostic options to investigate*, **not claims that all rough shifts are cheap or fixable**.

1. **9-3 9440 AF40 six-speed:** Saab's **TA440-0902** (January 2009) lists **low automatic-transmission fluid** as a cause of delayed shifting and requires a controlled fluid-temperature/Tech2 test. A delayed shift warrants diagnosis before declaring the gearbox unrepairable. Do not improvise oil level or fluid grade.
2. **9-3 9440 FA57 five-speed:** Saab WIS documents **Tech2 adaptation/reset after transmission, TCM or software service**. Old adaptation data can require handling after such work, but resetting codes does not replace mechanical diagnosis.
3. **Original 9-5 9600 FA57 five-speed:** Saab WIS describes valve-body **SLT/SLS pressure-control solenoid** faults, including **P0748 and P0785** limp-home codes. Read fault codes and perform electrical/hydraulic checks before interpreting limp-home as a destroyed transmission.

Original factory procedures and exact affected VIN/year/engine application must be consulted for a physical car; only equipment suited to the procedure and appropriate expertise should be used.

## Source inventory and limitations

The JSON overlay preserves **10 Saab workshop/bulletin URLs**, original cited *model year*, all **110** matching production record IDs, field-level status and **5** caution entries.

| WIS source area | Direct source |
| --- | --- |
| 9-3 9400 / MY2001 four-speed family | https://saabwisonline.com/9-3-9400/2001/4-transmission/automatic-transmission/technical-data/type-designation-gearbox |
| 9-5 9600 / MY2000 AF30 | https://saabwisonline.com/9-5-9600/2000/4-transmission/automatic-transmission/technical-data/type-designation |
| 9-5 9600 / MY2008 FA57 | https://saabwisonline.com/9-5-9600/2008/4-transmission/automatic-transmission/technical-data/type-designation |
| 9-3 9440 / MY2006 FA57 | https://saabwisonline.com/9-3-9440/2006/4-transmission/automatic-transmission/5-speed-fa-57/technical-data/type-designations |
| 9-3 9440 / MY2006 AF40 / TF-80SC | https://saabwisonline.com/9-3-9440/2006/4-transmission/automatic-transmission/6-speed-af-40/technical-data/type-designations |
| 9-5 9650 / MY2011 AF40 transmission case ID | https://saabwisonline.com/9-5-9650/2011/4-transmission/automatic-transmission/technical-description/transmission-identification-information |
| 9-5 9650 / MY2011 VIN code A = FWD 6AT | https://saabwisonline.com/9-5-9650/2011/0-general/general/technical-description/vehicle-engine-and-transmission-id-and-vin-location-derivative-and-usage |

All referenced workshop information is manufacturer-origin **mirrored** WIS. A year directory may carry later-revised service data; each factory-year range remains subject to original edition/VIN confirmation. No sourced comparative transmission failure rate, lifetime, rebuild cost, or reliability ranking has been established.

## Reproducibility and next verification gate

```sh
python3 tools/annotate_us_automatic_gearboxes.py --check
python3 -m unittest discover -s tests -v
python3 tools/validate.py
python3 tools/phase0_audit.py --check
```

To refresh the overlay after production data or evidence rules change: `python3 tools/annotate_us_automatic_gearboxes.py`, review the changed JSON and rerun the above checks.

**Next manufacturer-review actions:** (a) physically assign AF20 versus AF22 where original 9-3 option/VIN/build pages support it; (b) reconcile the manufacturer 9-5 9650 AF40 case-code and 2011 Turbo4 FWD automatic VIN character with exact original U.S. assembly documentation; (c) obtain exact 9600/9440 factory box/case identifiers for each engine/year before any interchange claims; (d) expand nonrebuild diagnostic issues and replace-versus-repair exposure with documented evidence; (e) resolve five low-volume production anomalies against manufacturer VIN documents. **Phase 0 Gate A still partial; B/C unmet.**
