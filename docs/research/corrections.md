# Factory corrections and parts research

Initial pass completed on 2026-10-12: 27 sources, 9 facts, 20 issues, 26 parts, 7 gaps. Records are in [corrections.json](../../data/datasets/corrections.json).

## Use and limitations

The records distinguish factory technical advice, customer satisfaction campaigns, special coverage, and safety recalls. They establish mechanisms and prescribed remedies; they do not estimate failure prevalence or rank cars statistically. Historical warranty/coverage language is not a promise of free repair today.

Applicability arrays for grouped advisories are index unions. Explicit `groups` retain correlated model/year/engine pairings. Generic “manual” and “automatic” values indicate transmission type where an exact gearbox code was not stated. An eight-character VIN value is a chassis suffix, not a complete VIN.

Sources 26 and 27 are search-excerpt-only. The remaining bulletins/PDFs were opened; campaign 15446 is split across two partial-page sources. Part supersession lists are flat supplier mappings; aftermarket mappings are explicitly labeled supplier_claim. No supplier stock, prices, durability improvement, or cross-platform interchange assurance was imported.

Individual VIN, market, repair invoices, engine serial, and inspection results remain necessary. This is a selected campaign set, not a complete recall inventory.

## Source subjects

| Subject | Source ID |
|---|---|
| Early sludge/PCV | corrections-src-001 |
| 2004–05 oil trap | corrections-src-002 |
| Hose retention | corrections-src-003 |
| IDM serial ranges | corrections-src-005 |
| ATF coolant diagnosis | corrections-src-004 |
| Cooler campaign VIN/date | corrections-src-021, 022 |
| Intake valves, revised official PDF | corrections-src-010 |
| ISM replacement kit | corrections-src-011 |
| B207 coolant/casting PI | corrections-src-012 |
| CIM/ISM item-specific corrections | corrections-src-007 |
| No-start voltage diagnostic advisory | corrections-src-009 |
| Springs special coverage | corrections-src-008 |
| Driver airbag repair | corrections-src-024 |

All direct URLs are retained in corrections.json. SaabParts official PDFs now resolve through /wp-content/uploads/1/ rather than the old /sites/10/ paths. The [source index](../source-index.md) provides direct links and retrieval statuses.

## Distinct airbag applications

The 16V-063 Part 573 report names NG9-3 MY2003–2011 and NG9-5 MY2010–2011. The separate 15043-03 implementation bulletin names NG9-3 MY2006–2011 and OG9-5 MY2006–2009 with current/prior registration-region conditions. These scopes remain separate in issues 016 and 020; part 024 follows the latter bulletin. Neither record is a current VIN recall clearance.

## Quality checks

All source references resolve to local source IDs. IDs are unique within arrays. Every issue/part/fact has evidence status and applicability. Sources 26/27 and related records flag excerpt limits. Mechanical, electrical and software remedies remain separate, including the ISM kit's salvageable-housing requirement.
