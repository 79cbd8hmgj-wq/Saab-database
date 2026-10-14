# First comparative component observations — October 14, 2026

The [observation ledger](../../data/tier-research/observations.json) now contains two ignition-module revision records and three separately scoped failure **case records** linked to **two engineering failure mechanisms**. This is the first evidence batch, **not comparable coverage or a model ranking**. Existing factory sources are reused with their IDs; the new [regulator dataset](../../data/datasets/tier-component-factory-revision-20261014.json) adds two NHTSA-hosted originals.

| Research subject | Distinction preserved | Still required |
| --- | --- | --- |
| 2000–02 B205/B235 9-3 (9400)/9-5 IDM | Four-cylinder serial-gated remedy | Installed module, campaign history, current OE chain |
| 2001–03 B308 9-5 IDM | Separate V6 scope/chassis restriction | V6-specific hardware and current repair evidence |
| Early 9-3 (9440) FA57 cooler sealing | Diagnostic advice versus narrower campaign | Cooler identity, contamination assessment, coupling applicability |

## Deduplicated mechanism identity and scope

The original 9-3/9-5 B205/B235 and B308 ignition-module cases are separate `failure_modes` records because original module hardware, years, remediation and consequences differ. Both link to the **same** `mechanism-idm-igbt-overload`; they are not two independent engineering defect types. The FA57 cooler-nipple seal problem links to a separate `mechanism-fa57-cooler-connection-seal`. Case counts, independent engineering-mechanism counts, affected campaign populations, and actual measured failure events are different quantities. **No frequency denominator exists.**

The [original TA440-0702 factory technical advice](https://saabwisonline.com/9-3-9440/2005/4-transmission/automatic-transmission/5-speed-fa-57/bulletins-si-mi/ta440-0702-coolant-in-atf-oil) says **up to VIN below** and lists three distinct **exclusive** upper bounds:

| Factory line | VIN suffix must be strictly below | Scope restriction |
| --- | --- | --- |
| 9-3SS | `51002378` | SS line; specific engine code not stated |
| 9-3SS TiD | `51000001` | Distinct diesel SS line; do not impute to a U.S. B207 petrol car |
| 9-3CV | `56001058` | Convertible line; specific engine code not stated |

Each now has an independent record in `configuration_scope.groups`, retaining the market, model-year and FA57 gearbox limits. The flat `body_styles` and `vin_ranges` fields are an **index union**, never a direct body/engine eligibility map. Engine codes are intentionally blank because this technical advice does not list them. Matching a particular VIN, factory variant and market requires manual verification; these records cannot justify an auto-generated applicability approval. The separate MI260-2634 campaign remains a *narrower* document and must not be substituted for the all-market technical advice.

## Original revision evidence

[GM's September 2005 report](https://static.nhtsa.gov/odi/rcl/2005/RCDNN-05V399-5581.PDF) identifies QP3 module changes. The ledger stores module manufacturing dates, **not vehicle-year cutovers**. Only pages 1–2 were inspected; the population attachment was not extracted.

The November [factory serial criteria](https://saabwisonline.com/9-5-9600/2000/2-engine/trionic-t7-lev-4-cyl-b235e-r/bulletins-si-mi/248-2611-utg-3-check-replacement-of-ignition-discharge-module) and December [2006 GM reissue](https://static.nhtsa.gov/odi/rcl/2006/RCMN-06V410-7676.pdf) remain service references. The reissue permits 55559955 as well as 55562588 for the four-cylinder recall. Historical authorization does not establish today's supersession, availability or lifespan.

The [06V410 acknowledgement](https://static.nhtsa.gov/odi/rcl/2006/RCAK-06V410-7245.pdf) reports 5,078 potentially affected vehicles, **not confirmed failures**. Its contradictory notification dates remain a retrieval limitation.

## Repair path matters

An IDM campaign is a component inspection/replacement path; it does not itself require engine rebuilding. This does not diagnose an unknown nonrunning car. Severe misfire requires separate damage assessment.

[TA440-0702](https://saabwisonline.com/9-3-9440/2005/4-transmission/automatic-transmission/5-speed-fa-57/bulletins-si-mi/ta440-0702-coolant-in-atf-oil) prescribes complete transmission replacement after confirmed coolant contamination. A connection kit cannot be represented as a cure for an already contaminated gearbox. Its historical open-flame fluid test is not reproduced as DIY instructions.

## Remaining comparison work

Failure frequency, complete installed costs and confirmed U.S. fulfilment remain unestablished. The unchanged 110-row audit measures legacy research leads, not this ledger's critical-system completeness, and grants no tiers. Next batches should cover other critical systems, then exact OE service chains and balanced dated offers. Original installed numbers stay unknown where only service replacements are named.
