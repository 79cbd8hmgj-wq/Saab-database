# B235 2004–2009 oil / PCV and FA57 identity research

**Research date:** October 12, 2026. **Scope:** Saab original 9-5 9600 four-cylinder petrol and Saab 9-3 9440 early automatic FA57 identification. This is evidence and diagnostic preparation only, not parts interchange, retrofit advice, engine repair authorization or a working reliability simulator.

## 2004–2009 B235: what is confirmed

1. Saab MY2004 [petrol crankcase-ventilation design](https://saabwisonline.com/9-5-9600/2004/2-engine/exhaust-emission-control-system/technical-description/crankcase-ventilation-4-cyl) describes an external oil trap on the engine block, an oil return into the sump, a one-way path toward the throttle body when manifold pressure is negative, and an alternative path into the turbo inlet under boost when the check valve closes.
2. MY2007 and MY2009 [factory PCV descriptions](https://saabwisonline.com/9-5-9600/2007/2-engine/exhaust-emission-control-system/technical-description/crankcase-ventilation-4-cyl) / [MY2009 source](https://saabwisonline.com/9-5-9600/2009/2-engine/exhaust-emission-control-system/technical-description/crankcase-ventilation-4-cyl) independently document these same *functional descriptions* and name DTCs P1181/P0171/P1171/P0507/P0101/P0300/P0455 as possible leakage outcomes. **They repeat “This model year has a new system.” That wording must not be read as evidence of an additional redesign in 2007 and 2009.** Part revisions need original EPC verification. The mere presence of a listed DTC cannot establish a faulty oil trap.
3. MY2006 [oil-trap coupling inspection](https://saabwisonline.com/9-5-9600/2006/2-engine/exhaust-emission-control-system/adjustment-replacement/inspection-of-crankcase-ventilation-hoses) checks that oil-trap hose connectors are secure and intact. Its [check-valve hose procedure](https://saabwisonline.com/9-5-9600/2006/2-engine/exhaust-emission-control-system/adjustment-replacement/hose-with-check-valve-for-crankcase-ventilation) confirms an accessible hose/clip and a dedicated external oil-trap connection. Neither proves the condition of engine bearings or identifies a universal retrofit kit.

## Petrol oil service values: avoid a dangerous assumption

| Documented fact | MY2007 | MY2009 | Limits |
| --- | --- | --- | --- |
| Total lubrication volume including oil cooler/filter | 5.4 L | 5.4 L | **Not** an ordinary oil-change refill |
| Oil-change service refill incl. filter | 4.0 L | 4.0 L | Confirm level at MAX after service |
| Difference between dipstick MIN/MAX | 1.0 L | 1.0 L | Not a required top-off amount |
| Warm minimum mechanical oil pressure | 2.5 bar at 2000 rpm | 2.5 bar at 2000 rpm | 105±2°C oil, specified **10W-30** test oil |
| Oil warning switch threshold | 0.3–0.55 bar | 0.3–0.55 bar | A silent warning lamp is **not** proof of acceptable running pressure |
| Pressure-reducing valve | 3.8 bar | 3.8 bar | Different from test-pressure and warning-threshold values |
| Oil-cooler thermostat | 105±2°C | 105±2°C | Not the coolant thermostat |

Source [MY2007](https://saabwisonline.com/9-5-9600/2007/2-engine/basic-engine-4-cylinder-petrol/technical-data/lubricating-system) and [MY2009](https://saabwisonline.com/9-5-9600/2009/2-engine/basic-engine-4-cylinder-petrol/technical-data/lubricating-system). These are year-scoped technical-data tables; unresolved MY2006 and 2008 tables are not filled by interpolation.

Individual [MY2006](https://saabwisonline.com/9-5-9600/2006/2-engine/basic-engine-4-cylinder-petrol/service/engine-oil-and-oil-filter), [MY2008](https://saabwisonline.com/9-5-9600/2008/2-engine/basic-engine-4-cylinder-petrol/service/engine-oil-and-oil-filter) and [MY2009](https://saabwisonline.com/9-5-9600/2009/2-engine/basic-engine-4-cylinder-petrol/service/engine-oil-and-oil-filter) oil/filter service pages give **B205E/B235E** a 4.0 L service refill, 25 Nm oil drain plug, and level check 2–5 minutes after switching off a warm engine. The text of those service pages **does not list B235R**, so no B235R drain torque or service procedure is automatically expanded from that narrower passage.

The 2009 [EU service oil-quality reference](https://saabwisonline.com/9-5-9600/2009/1-service/saab-service-eu/service/recommended-oil-quality) lists historical petrol B235E/L/R GM-LL-A-025 with 0W-30, 0W-40, 5W-30 and 5W-40, warns against additives, and explicitly associates short city trips with extra fuel/condensation in the oil. **This is historical EU guidance, not proof that a 2026 bottle meets the superseded approval or that it is approved for US/CA use.** No custom “Toyota reliability” oil interval is invented.

## FA57 gearbox / TCM identities are not a VIN lookup

[MY2005 type designations](https://saabwisonline.com/9-3-9440/2005/4-transmission/automatic-transmission/5-speed-fa-57/technical-data/type-designations) gives factory example `FA57 1 01 03CV12345`. It encodes gearbox architecture, a B207E/L/R adaptation category, development and gearbox manufacture. Month code deliberately uses **J for September** and excludes I. The TCM identifier independently uses **J=B207L, K=B207R, L=B207E** in its engine-character position. These data are *identification clues*, not replacement compatibility or module programming approval.

The separate [TA440-0702](https://saabwisonline.com/9-3-9440/2005/4-transmission/automatic-transmission/5-speed-fa-57/bulletins-si-mi/ta440-0702-coolant-in-atf-oil) limits its concern to Saab 9-3 MY2003–05 SS before suffix **51002378**, convertibles before **56001058**, and a separately scoped diesel subset. Its narrower campaign 15446 must not be assumed from this advisory alone. Confirm actual vehicle VIN, gearbox type, cooling and repair history before screening. If contamination is suspected, consult qualified transmission service using safe methods; the technical advice describes hazardous open-flame heating of ATF that **must not be presented as a DIY test**.

## Practical buying research, not repair assumptions

For a low-cost 9-5, ask for precise engine code, oil pressure measurements made at documented test conditions, existing oil-change records and PCV repairs. A steady warning lamp, lack of a warning lamp, or seller claim of a “new PCV” does not prove internal condition. For an early 9-3 automatic, record body configuration, chassis suffix and stamped transmission identity separately; fluid appearance and history do not rule out hidden contamination.

## Unresolved research

- 2004/05 and 2006/08 hot oil-pressure testing documentation still needs individual year resolution.
- Specific B235R service instructions and later PCV EPC revision/fitment chains remain incomplete.
- Replacement oil approvals, present-day equivalents and severe-duty intervals remain vehicle/market-specific.
- FA57 TCM calibration, VIN applicability, campaign-15446 status and safe contamination test criteria need manufacturer/qualified diagnostics.
- Neither published WIS specifications nor dataset record counts are failure rates, evidence of a “Toyota-equivalent” lifespan, or proof that a non-running car is mechanically sound.
