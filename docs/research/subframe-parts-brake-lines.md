# OEM subframe assemblies, fasteners and brake-line research

Research date: 2026-10-12. See [structured records](../../data/datasets/subframe-parts-brake-lines.json).

## Evidence boundary

This pass records **17 source entries, 16 factory-procedure facts, 15 catalogue parts and 9 explicit gaps**. Factory WIS entries were checked for repair context, torque and line safety; eSaabParts is a parts retailer reporting its own product applications and supersessions, **not manufacturer-approved universal interchange**. No currently installed part, VIN, physical fit, structural condition or present purchase availability has been verified. Listing years and model/year directory navigation can be broader than applicability established by a specific component. Part records retain `supplier_claim`.

## Assembly distinctions (retailer/catalogue statements only)

| Part number | Catalogued role | Restriction or dependency |
| --- | --- | --- |
| [32022623](https://www.esaabparts.com/saab/parts/32022623?ss=12825111) | Replacement NG9-3 front subframe for FWD 4D/5D; retailer marks 12825111 as predecessor | Not CV or XWD. MY2005 may need the later front engine mount. One supplier view also names 12762720 as predecessor; that mapping requires independent confirmation. |
| [12825111](https://www.esaabparts.com/viewparts.php?section=582948118) | Listed original-type FWD 4D/5D front frame | Retailer shows superseded by 32022623, but engine and chassis-specific fit still need confirmation |
| [12825112](https://www.esaabparts.com/saab/parts/12825112) | NG9-3 CV front frame | Separate convertible listing; not a 4D/5D interchange |
| [12777984](https://www.esaabparts.com/viewparts.php?section=582948118) | NG9-3 front frame, XWD | All-wheel-drive application, not FWD B207 replacement |
| [12761536](https://www.esaabparts.com/saab/parts/12761536) | NG9-3 rear frame, FWD 4D/5D, MY2006–2011 | Excludes unverified CV/XWD applications |
| [12831642](https://www.esaabparts.com/saab/parts/12831642) | NG9-3 CV rear subframe | Exact convertible year/engine/option boundaries remain to be established |
| [12765948](https://www.esaabparts.com/saab/parts/12765948) | OG9-5 front subframe, MY2006–2009 | More specific engine/gearbox/body identity and associated hardware are required |
| [32019861](https://www.esaabparts.com/saab/parts/32019861) | OG9-5 catalogued subframe/strut bolt | Seller lists 11095961, 4597985 and 4940219 as superseded. No basis to label it every subframe bolt or presume fastener reuse |

The [NG9-3 front-floor diagram](https://www.esaabparts.com/viewparts.php?section=582948118) also lists separate 4D/5D and CV front/rear bushings. Convertible bushing catalog text calls them solid rather than rubber, with an additional special CV rear bushing **12759331 only for cars without a front axle stay**. The early MY2003–2004 sedan frame **24401525** refers to PI 08-01 2007; that bulletin is still needed. The current 2005-on replacement frame must not be assigned to a MY2003–2004 car merely because both use platform 9440.

## Documented factory fastener and installation constraints

- [MY2006 B207 9-3 front subframe](https://saabwisonline.com/9-3-9440/2006/7-suspension-wheels/front-suspension/adjustment-replacement/subframe-b207) separates main-to-body **75 Nm plus 135°**, rear stay **90 Nm plus 45°**, and front/rear suspension arm bush-to-subframe **65 Nm plus 135°** joints. It calls for centring tools and a four-wheel alignment after subframe replacement. **Do not confuse these fastener locations** or treat old hardware as automatically reusable.
- [MY2006 OG9-5 petrol front subframe](https://saabwisonline.com/9-5-9600/2006/7-suspension-wheels/front-suspension/adjustment-replacement/subframe-petrol-engines) specifies **100 Nm plus 45°** for its subframe bolts, while warning that the middle bolts differ in washer and head size. A 9-3 B207 fastener specification cannot be applied to an OG 9-5.
- [MY2006 OG9-5 rear support arm](https://saabwisonline.com/9-5-9600/2006/7-suspension-wheels/rear-suspension/adjustment-replacement/support-arm) uses **90 Nm plus 60°** for the rear suspension support arm attachment and stresses preservation of transverse-link bolt protective sleeves because they protect the fuel tank/filler in collisions. This rear support arm should not be conflated with the NG9-3 separate rear subframe part 12761536.

These are narrowly documented workshop specifications, not complete step-by-step repair instructions. Joint geometry, actual hardware identity, single-use status and suspension loading must be confirmed before working.

## Brake lines: sourced condition and routing clues

[MY2008 OG9-5 brake-line instructions](https://saabwisonline.com/9-5-9600/2008/5-brakes/footbrake-system/adjustment-replacement/brake-lines) explicitly require body-clipped brake lines to be free of *any visible corrosion or pitting* and fittings to be inspected for leakage/damage. Factory line removal/installation specifies a flare-nut wrench, no bending of installed lines, **15 Nm** connection torque in that procedure, hydraulic bleeding and leak verification. [A separate 9-5 brake joint table](https://saabwisonline.com/9-5-9600/2008/5-brakes/brake-discs-and-pads/technical-data/tightening-torques) identifies different torques for other joints, including **16 Nm** for rear brake-pipe nipples; a torque value must always be tied to its named joint.

NG9-3 MY2006 factory pages establish several **partial routing anchor points**, not a complete underbody map:

- [Master cylinder](https://saabwisonline.com/9-3-9440/2006/5-brakes/footbrake-system/adjustment-replacement/master-cylinder): master-cylinder pipe connections and fluid/bleeding steps; 16 Nm for that connection.
- [TCS/ESP unit](https://saabwisonline.com/9-3-9440/2006/5-brakes/tcs-esp/adjustment-replacement/control-module-tcs-382-esp-671-b207-b284-rhd-z18xe-z19): brake pipes clipped along the MacPherson strut tower during module servicing.
- [Rear disc](https://saabwisonline.com/9-3-9440/2006/5-brakes/footbrake-system/adjustment-replacement/brake-disc-rear): support the caliper without damaging the nearby rigid brake pipe.
- [Rear subframe](https://saabwisonline.com/9-3-9440/2006/7-suspension-wheels/rear-suspension/adjustment-replacement/subframe): careful separation of brake equipment, cables and other suspension attachments.

**Still missing:** complete LH/RH hard-line circuit diagrams, exact clips/unions and line lengths, material/flare specs, pre-bent assemblies by VIN, fuel line protection, hidden mounting-corrosion assessments and approved fastener renewals. Do not assume universal pipe routing or bend/fabricate hydraulic lines solely from this report.

## Research significance

A replacement subframe becomes a plausible *candidate* once its exact platform, driveline, body style and version are known; purchasing or installing one additionally requires the actual vehicle VIN, installed mounting parts, frame geometry, corrosion at captive nuts/body points, correct bushings and fasteners, alignment and system checks.

This is an evidence-gathering milestone, not a parts substitution simulator, not a reliability prediction, and not a safety certificate for a car with subframe rust.
