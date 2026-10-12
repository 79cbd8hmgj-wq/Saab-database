# Initial research and model-selection case

Research date: 2026-10-12. The objective is dependable daily use with practical
replacement options and as much DIY ownership as appropriate. The working target
is Toyota-like dependability. That is an objective for the project; the available
Saab documents do not demonstrate that outcome or supply comparable fleet failure
rates. No particular vehicle has been selected or inspected.

## Coverage

| Dataset | Coverage | Important boundary |
| --- | --- | --- |
| [OG9-5 specifications](../data/datasets/og95.json) | B235 geometry, output, ignition, oil/cooling, fuel delivery, gearboxes, brakes and service | Mostly MY2004/2005/2009 source snapshots; no blanket interpolation to intervening years |
| [OG9-5 body/chassis](../data/datasets/og95-body.json) | Sedan/wagon dimensions and weights, wheels, suspension and steering | MY2009 generic WIS dimensions conflict with the North American manual |
| [NG9-3 specifications](../data/datasets/ng93.json) | B207 geometry, fluids, output, transmissions, brakes, cooling and US identity | WIS year directories contain later revisions; MY11.5 engine-family change matters |
| [NG9-3 body/chassis](../data/datasets/ng93-body.json) | MY2006 US/CA dimensions, scoped weight ranges, wheels and chassis architecture | Early manual has missing SportCombi weights and ambiguous dimensions |
| [Factory corrections and parts](../data/datasets/corrections.json) | Selected PCV, ignition, cooler, valve, casting, electrical, spring, water-ingress and recall records | VIN/serial/market restrictions remain necessary; this is not a complete recall inventory |
| [Replacement candidates](../data/datasets/replacements.json) | B235R turbo/pipe catalogue distinctions, T8 heat-protection claims, electrical dependencies | Supplier application is not verified interchange or proven improvement |
| [Simulation resources](../data/datasets/simulation.json) | Diagnostic semantics, acquisition tools, software licenses, material envelopes and modelling inputs | No measured vehicle model, firmware dataset or life prediction is supplied |

The [source index](source-index.md) links every source record and shows retrieval
strength. JSON findings retain stable IDs, source locators, units and applicability.
The [individual reports](research/) explain source conflicts in more detail.

## Provisional cars to research first

This is a project preference based on documented mechanisms and the current
research scope. It is an inference, not an observed reliability ranking. A sound
individual car can change the ordering. Budget, market, transmission preference,
body requirements and actual available cars remain unknown.

| Priority | Candidate configuration | Basis for investigating it | What the evidence still needs |
| --- | --- | --- | --- |
| First OG9-5 search | MY2006–2009 original-generation 9-5, 2.3 petrol; confirm B235R for the North American 2.3T profile | Factory documentation identifies a MY2004 PCV redesign; the catalogue separates later B235R turbo/pipe applications from MY2000–2005. This makes later cars a useful starting profile. | Exact market/engine/gearbox, oil and cooling history, condition and correction completion. Later years alone do not demonstrate a healthy engine or longer life. |
| Second OG9-5 search | MY2004–2005 original-generation 9-5 four-cylinder | Shares the documented redesigned PCV architecture, with explicit correction evidence available for certain oil-trap and hose applications. | Narrow manual-transmission/VIN conditions for the oil-trap campaign, hose campaign completion, exact ignition/brake application and individual condition. |
| Main NG9-3 alternative | MY2006 9-3 2.0 turbo, FWD; confirm B207 engine and gearbox | Provides a specific B207/FWD target for the database. The cold-compression advisory identifies later MY2007–2011 groups, while several early cooler/key advisories name earlier production groups. | An advisory's scope is not proof that MY2006 cannot suffer similar faults. Confirm actual casting, valve, cooling, electrical and drivetrain condition, plus applicable campaigns. |
| Additional NG9-3 candidate | MY2005 9-3 2.0 turbo, FWD | Well represented by the retrieved owner manual and factory identity sheets. Can be compared using the same B207 dependency model. | Check exact VIN against cooler and early electrical advice; resolve gearbox/fluid ambiguity before selecting replacement parts. |

Selection basis: `og95-fact-074`, `repl-fact-001`, `corrections-issue-002/003`,
`corrections-issue-005/006/007/008/009/011/012`, and the US identity records in
`ng93.json`. Their original links are in their dataset sources. There is no basis
here to claim that all other Saab engines, transmissions or drivetrains are poor
choices; they have not received equivalent coverage.

The project should favor a viable engine and transmission because the stated
ownership goal does not include rebuilding either. Factory bulletins about cold
compression loss, coolant-contaminated ATF or suspected casting porosity identify
possible major-work scenarios. A bolt-on accessory or routine service cannot be
assumed to reverse existing internal damage. No inspection work is required from
the user at this research stage.

## Findings that change replacement decisions

- T7 ignition hardware also provides combustion/knock feedback. A substitute must
  preserve those functions, and the plug application conflict remains open.
- Oil service refill, complete-system capacity and dry gearbox capacity are
  different quantities. Conflicting NG9-3 coolant and six-speed figures remain
  separate, with their source/configuration context.
- Overall transmission ratios already include final drive. Multiplying the final
  drive again would give an incorrect RPM/speed model.
- OG9-5 brake-table discrepancies prevent automatic rotor ordering. Brake level,
  caliper/carrier identity and actual dimensions are missing discriminators.
- Aftermarket cross-references remain distinct from OEM supersessions. Kit contents
  remain distinct from parts that must be purchased separately.
- The Takata report and the separate 15043-03 repair bulletin have different
  platform/year/registration scopes. They are separate records, not one enlarged
  recall application.
- ECU mounting changes have plausible thermal questions to investigate, but seller
  temperature claims do not establish reduced failure probability or useful life.

## Research still open

The structured `gaps` arrays contain the detailed backlog. Highest-value next
information is a vehicle's identity and installed components, complete current
application/supersession evidence, resolved source conflicts, actual calibration
identity and measured condition. Numerical simulation additionally needs measured
loads, geometry, material properties and validation traces. These are not filled
with generic estimates simply to make a model run.

Additional primary research can extend adjacent years, full wiring/pinouts,
connector ratings, hose assemblies, corrosion/structure, supplier drawings,
production revisions and current part availability. Supplier prices and stock were
not stored as durable specifications. No arbitrary replacement interval or
probability-of-failure curve was inferred from a bulletin.
