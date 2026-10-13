# OG 9-5 MY2007–09 wiring, ground and supply-location research

Date: 2026-10-12. Scope: original-generation 9-5 (9600). These are factory-authored Saab WIS *location and textual wiring references*, not a working circuit simulator, a diagnosis of a specific car, or approved replacement parts.

## Factory ground paths, independently listed by model year

| Ground identity | Source-backed factory locator |
| --- | --- |
| G2 | Left structural member behind headlamp; battery body ground (16 mm² feed) |
| G25 | Gearbox; battery engine/gearbox ground (25 mm² feed) |
| G2 ↔ G25 | Redundant 10 mm² gearbox-to-body lead in factory description |
| G7 | Intake manifold side near cylinder 4 |
| G30 | Front engine-bay side panel ahead of left wheel housing |
| G40 / G42 | Left and right knee-member locations in cabin |
| G41P / G41S | Separate central/left knee-member screws; names must not be conflated |

Documented independently in [2007](https://saabwisonline.com/9-5-9600/2007/3-electrical-system/wiring-harness/technical-description/grounding-points), [2008](https://saabwisonline.com/9-5-9600/2008/3-electrical-system/wiring-harness/technical-description/grounding-points) and [2009](https://saabwisonline.com/9-5-9600/2009/3-electrical-system/wiring-harness/technical-description/grounding-points). The numbers are conductor *cross-sectional areas*, not cable part numbers or acceptable voltage drop. System wiring may use different grounding points in LHD versus RHD versions.

## Supply distribution and start-state distinction

The [MY2007](https://saabwisonline.com/9-5-9600/2007/3-electrical-system/wiring-harness/technical-description/system-overview) and [MY2008](https://saabwisonline.com/9-5-9600/2008/3-electrical-system/wiring-harness/technical-description/system-overview) wiring system overviews list engine bay power centers 501 (maxi-fuses), 342a (fuses) and 342b (relay board); 342a and 342b are integrated. Dashboard distribution uses 22a/22b. The factory describes +15 as retained in ON and START, but +54 is shed in START; this is deliberate to relieve consumers while starting. It explicitly cautions that direct battery distribution to the starter, generator and some fuse/relay feeds is unfused.

The [MY2009 +54 wiring-component table](https://saabwisonline.com/9-5-9600/2009/3-electrical-system/wiring-harness/wiring-diagram/power-supply-54) locates ignition relay 21 in the dashboard relay board, switch 20 in the floor console and H43-1 below the left A-pillar. The [MY2009 +30 partial source](https://saabwisonline.com/9-5-9600/2009/3-electrical-system/wiring-harness/wiring-diagram/power-supply-30-part-1-2) was reviewed as a search excerpt only, so no MY2009 electrical switching logic is extrapolated from it.

## Petrol cooling fans: three independently checked model years

| Component | MY2007, MY2008 and MY2009 petrol wiring diagrams |
| --- | --- |
| 81 | LH fan high-speed relay, engine-bay relay board |
| 155 | Two-fan low-speed relay, engine-bay relay board |
| 396 | RH fan high-speed relay, engine-bay fuse box |
| 628 | DICE; LHD above dashboard relay box / RHD behind it |
| 202 | Coolant sensor, left side of cylinder head |
| J3 | Splice approx. 100 mm from G30 branch toward fan |
| G30, G40, G42 | Ground points named on diagram's component list |

Original links: [2007](https://saabwisonline.com/9-5-9600/2007/2-engine/cooling-system/wiring-diagram/radiator-fans-petrol), [2008](https://saabwisonline.com/9-5-9600/2008/2-engine/cooling-system/wiring-diagram/radiator-fans-petrol), [2009](https://saabwisonline.com/9-5-9600/2009/2-engine/cooling-system/wiring-diagram/radiator-fans-petrol). A component listed in a multi-variant drawing need not be fitted to every car. Two-fan A/C and one-fan no-A/C distinctions are preserved from earlier cooling research. These are *component lists*, not complete graphical pin-to-pin redrawings.

## MY2007/08 T7 harness evidence

MY2007 and MY2008 [Trionic 7 sheet 2 of 4](https://saabwisonline.com/9-5-9600/2007/3-electrical-system/wiring-harness/wiring-diagram/trionic-t7-engine-management-system-4-cyl-part-2-4) / [corresponding MY2008 sheet](https://saabwisonline.com/9-5-9600/2008/3-electrical-system/wiring-harness/wiring-diagram/trionic-t7-engine-management-system-4-cyl-part-2-4) independently locate crank sensor 345 beneath the exhaust manifold, MAF 205 behind the RH headlamp, coolant sensor 202 at LH cylinder head, intake air/charge-air assembly 688, engine-bay side grey H24-1 and black H24-2 connectors, and white H43-1 under LH A-pillar. Crimp distances J15/J21/J22 are approximate harness landmarks.

The [MY2009 T7 sheet 4 of 4](https://saabwisonline.com/9-5-9600/2009/3-electrical-system/wiring-harness/wiring-diagram/trionic-t7-engine-management-system-4-cyl-part-4-4) identifies relay 102 for fuel pump, relay 229 for engine management, pre/post-catalyst O2 sensors 592Fa/592Ra, and relevant splices. It is *not* the missing MY2009 sheet 2 of 4 and therefore cannot justify copying MY2007 sensor locations into MY2009.

## Limits and next evidence collection

1. WIS web pages expose component locator tables; their drawn wiring graphics have **not** been transcribed into complete connectivity, fusing, pin contacts, wire colors or current ratings. All remain research gaps.
2. Conductor cross sections alone cannot establish original cable construction, electrical acceptability, replacement fitment or measured ground integrity.
3. Engine family, market, handedness and equipment applicability must be verified before circuit testing or part ordering; diesel EDC16 and petrol T7 are different systems.
4. Symptoms in issue records represent testable hypotheses, **not** observed fleet incidence or a known fault on a specific Saab.
5. Do not bridge unfused supplies, bypass relays, alter coolant thresholds or replace an electronic module solely from these locators.

Next: obtain source-complete four-sheet T7 schematics and exact fuse, relay and connector tables, with pictures/terminal numbering, then manufacturer WebEPC cable and harness identifiers.
