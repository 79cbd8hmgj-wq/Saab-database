# Replacement candidates and electrical dependencies

Research date: 2026-10-12. Eight source records, ten findings, five part records and
three gaps were added. Catalogue applications and aftermarket temperature claims
carry `supplier_claim`; factory functional descriptions carry `documented`.

## B235R turbo and intake applications

The eSaabParts diagram identifies separate MY2000–2005 and MY2006–2009 B235R turbo
rows. Individual listings supply superseded numbers; intake pipes also have
year-specific rows. The database retains those boundaries. The generic switch-
diagram year range on an individual product page is not used to expand a narrower
engine-specific application.

This is not a complete conversion bill of materials. Turbo identity, maps,
wastegate, plumbing, connected interfaces and calibration remain unresolved for
an earlier-to-later conversion. Availability and prices are not recorded as
permanent specifications.

## T8 heat-protection candidates

RBM's KIT89.3 and KM-tronics' relocation product were found in first-party seller
pages. Their claimed temperatures, mounting descriptions and ground provisions
are preserved in JSON. No independent thermal or life testing was found in those
pages. RBM's model-year title conflicts with its description; KM-tronics does not
publish a complete application matrix or exact SKU. Neither product is designated
an approved substitute here.

The missing evidence includes ambient/load/heat-soak traces, case-versus-junction
temperature, harness/ground behavior, vibration and water exposure. The colder
mounting claim alone does not demonstrate a longer-lived ECU.

## Factory dependencies

The MY2004 T7 descriptions show why ignition changes cannot be evaluated solely
by spark output: combustion and knock feedback also pass through the discharge
module and spark-plug gaps. The module warning and correct-plug requirement are
preserved without resolving the separate plug-table conflict.

The MY2011 NG9-3 bus overview supports the need for communication and immobiliser
messages before starting, and for sound module power/ground. Its later examples
mix MIU and CIM names, so the database does not infer a module-programming or
security-transfer procedure from that page. Exact replacement instructions remain
a gap.

Sources and locators are in [replacements.json](../../data/datasets/replacements.json)
and the [source index](../source-index.md).
