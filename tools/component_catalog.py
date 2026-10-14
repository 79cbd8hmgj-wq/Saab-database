#!/usr/bin/env python3
"""Build/query a conservative, normalized catalogue without rewriting evidence.

Assembly research targets and product identities are separate denominators.
Application claims are never expanded into a year/engine/gearbox Cartesian product.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

from database import ROOT, load_datasets, validate_datasets
from build_system_evidence_index import route

DIR = ROOT / "data/component-catalog"
OUTPUT = DIR / "catalog.json"
DATE = "2026-10-14"
FAMILIES = {"9-3-9440": (2003, 2011, {"B207", "B207E", "B207L", "B207R"}),
            "9-5-9600": (1998, 2009, {"B205", "B205E", "B205L", "B205R",
                                      "B235", "B235E", "B235L", "B235R"})}


def read(path):
    return json.loads(Path(path).read_text())


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                    separators=(",", ":")).encode()).hexdigest()


def identity(namespace, number, assembly):
    return "cmp:" + namespace + ":" + "".join(number.split()).lower() + ":" + assembly


def project_scope(scope):
    """Return only explicit eligible groups; omitted dimensions stay unknown.

    No platform evidence yields no approved/claimed target application. A reuse
    record still survives in the context index with its original scope.
    """
    result = []
    for group in scope.get("groups", [scope]):
        for platform in group.get("platforms", []):
            if platform not in FAMILIES:
                continue
            lo, hi, engines = FAMILIES[platform]
            if group.get("drivetrain") == "XWD" or group.get("drivetrains") == ["XWD"]:
                continue
            selected = copy.deepcopy(group)
            selected["platforms"] = [platform]
            if "model_years" in group:
                selected["model_years"] = [y for y in group["model_years"] if lo <= y <= hi]
                if not selected["model_years"]:
                    continue
            if "engine_codes" in group:
                selected["engine_codes"] = [e for e in group["engine_codes"] if e in engines]
                if not selected["engine_codes"]:
                    continue
            result.append(selected)
    return result


def build():
    datasets = load_datasets()
    errors = validate_datasets(datasets)
    if errors:
        raise ValueError("Legacy validation failed: " + str(errors))
    inventory = read(DIR / "inventory.json")
    curation = read(DIR / "curation.json")["legacy_part_routes"]
    policy = read(ROOT / "data/audits/system-evidence-routing-policy-20261014.json")
    records = {r["id"]: r for d in datasets for k in ("facts", "issues", "parts", "gaps") for r in d[k]}
    parts = {p["id"]: p for d in datasets for p in d["parts"]}
    if set(curation) != set(parts):
        raise ValueError("Every legacy part must have a reviewed namespace/assembly route")
    sources = {s["id"]: copy.deepcopy(s) for d in datasets for s in d["sources"]}
    components, applications, numbers, relations = {}, [], [], []
    part_component = {}
    excluded = {"mountbrake-part-004": "XWD front subframe explicitly excluded",
                "pcv-supply-part-001": "9400-only factory kit application; retained original evidence"}
    for id_, p in sorted(parts.items()):
        if id_ in excluded:
            continue
        mapping = curation[id_]
        groups = project_scope(p["applicability"])
        # Non-target explicit scopes stay out; unscoped research survives as a candidate.
        if p["applicability"].get("platforms") and not groups:
            excluded[id_] = "No eligible explicitly scoped application"
            continue
        key = identity(mapping["number_namespace"], p["part_number"], mapping["assembly_id"])
        part_component[id_] = key
        if key not in components:
            components[key] = dict(id=key, assembly_id=mapping["assembly_id"], name=p["title"],
                number_namespace=mapping["number_namespace"], part_number=p["part_number"],
                marketed_brand=mapping["marketed_brand"], original_oem_manufacturer=None,
                original_installed_identity_verified=False, service_identity_status="source_claim",
                source_ids=[], legacy_record_ids=[], notes=[])
        c = components[key]
        c["legacy_record_ids"].append(id_)
        c["source_ids"] = sorted(set(c["source_ids"] + p["source_ids"]))
        c["notes"].append({"record_id": id_, "evidence_status": p["evidence_status"],
                           "review_status": p.get("review_status"), "notes": p["notes"]})
        for n, group in enumerate(groups):
            # Manually adjudicated, contradictory engine cutoffs stay separate
            # and machine readable; the untouched original claim remains raw_scope.
            if id_ == "corrections-part-008":
                group["production_restrictions"] = [dict(kind="engine_serial", operator="inclusive_range",
                    minimum="4000000", maximum="4017590", source_id="corrections-src-002")]
            elif id_ == "b235rev-part-005":
                group["production_restrictions"] = [dict(kind="engine_serial", operator="from",
                    value="4017591", source_id="b235rev-src-014")]
            applications.append(dict(id=f"app:{id_}:{n}", component_id=key,
                scope=group, raw_scope=p["applicability"], status=p["evidence_status"],
                source_ids=p["source_ids"], conditions=p["requirements"], vin_approved=False,
                legacy_record_id=id_, legacy_sha256=digest(p)))
        for n, rel in enumerate(p["relationships"]):
            relations.append(dict(id=f"pnrel:{id_}:{n}", component_id=key,
                claim=rel, source_ids=p["source_ids"], status="unadjudicated_source_claim",
                approved=False, legacy_record_id=id_))
    batches = [read(p) for p in sorted(DIR.glob("research-batch-*.json"))]
    interchanges, specifications, offerings, conflicts, procedures, repairs, gearboxes = [], [], [], [], [], [], []
    for batch in batches:
        for s in batch["sources"]:
            if s["id"] in sources:
                raise ValueError("Duplicate source identity: " + s["id"])
            sources[s["id"]] = s
        for c in batch["components"]:
            if c["id"] in components:
                raise ValueError("Duplicate new product identity: " + c["id"])
            components[c["id"]] = c
        applications.extend(batch["applications"])
        interchanges.extend(batch["interchanges"])
        specifications.extend(batch["specifications"])
        offerings.extend(batch["supplier_offerings"])
        conflicts.extend(batch["conflicts"])
        procedures.extend(batch["procedures"])
        repairs.extend(batch["repair_scenarios"])
        gearboxes.extend(batch.get("gearbox_families", []))
    # Explicitly verified dual-channel SERVICE SKU, not an original installed donor.
    pump = part_component.get("gmwp-part-001")
    if pump:
        gm = identity("gm_service", "12630084", "water_pump")
        components[gm] = dict(id=gm, assembly_id="water_pump", name="GM Genuine pump service SKU",
            number_namespace="gm_service", part_number="12630084", marketed_brand="GM Genuine",
            original_oem_manufacturer=None, original_installed_identity_verified=False,
            service_identity_status="dual_official_channel_sku", source_ids=["gmwp-src-001"],
            legacy_record_ids=[], notes=["Original Chevrolet donor vehicle/VIN application remains unknown."])
        interchanges.append(dict(id="int:12630084:dual-official-service-sku",
            from_component_id=pump, to_component_id=gm, category="A",
            relationship="same_current_service_sku", identity_basis="dual_official_channel_exact_number",
            source_ids=["gmwp-src-001", "gmwp-src-002"],
            conditions=["Identity restricted to the current service number; verify Saab VIN, sprocket and gasket contents."],
            fitment_approved=False, donor_approved=False, reliability_improvement_proven=False))
    old_switch = part_component.get("gate5-part-001")
    kit = part_component.get("gate5-part-002")
    if old_switch and kit:
        interchanges.append(dict(id="int:ism:conditional-service-kit", from_component_id=old_switch,
            to_component_id=kit, category="B", relationship="manufacturer_conditional_repair_kit",
            identity_basis="manufacturer_repair_instructions", source_ids=parts["gate5-part-002"]["source_ids"],
            conditions=["Reuse serviceable original black sliding mechanism; kit is not a complete replacement switch."],
            fitment_approved=False, donor_approved=False, reliability_improvement_proven=False))
    # Preserve historical offerings as observations, not present-day confirmed inventory.
    fact_offers = defaultdict(dict)
    for d in datasets:
        for f in d["facts"]:
            if f["predicate"] not in {"quoted_price", "quoted_stock_text"}:
                continue
            if not project_scope(f["applicability"]):
                continue
            fact_offers[f["subject"]][f["predicate"]] = f
    extra_routes = {"32020290": ("esaabparts_sku", "water_pump", "Aftermarket pump service candidate"),
                    "32101497": ("esaabparts_sku", "starter", "Remanufactured starter service candidate"),
                    "5194758": ("saab_service", "gearbox_mounts", "Mount service reference")}
    for subject, fields in sorted(fact_offers.items()):
        pn = subject.split(":")[-1]
        matched = [c["id"] for c in components.values() if c["part_number"] == pn]
        fs = list(fields.values())
        if not matched and pn in extra_routes:
            ns, assembly, name = extra_routes[pn]
            key = identity(ns, pn, assembly)
            components[key] = dict(id=key, assembly_id=assembly, name=name, number_namespace=ns,
                part_number=pn, marketed_brand=None, original_oem_manufacturer=None,
                original_installed_identity_verified=False, service_identity_status="supplier_claim",
                source_ids=sorted({s for f in fs for s in f["source_ids"]}), legacy_record_ids=[], notes=[])
            matched = [key]
            for n, scope in enumerate(project_scope(fs[0]["applicability"])):
                applications.append(dict(id=f"app:offering:{pn}:{n}", component_id=key, scope=scope,
                    raw_scope=fs[0]["applicability"], status="supplier_claim", source_ids=fs[0]["source_ids"],
                    conditions=["Verify exact VIN and supplier product identity"], vin_approved=False))
        if len(matched) != 1:
            continue  # Ambiguous namespace is not silently resolved by a retail quote.
        price = fields.get("quoted_price")
        stock = fields.get("quoted_stock_text")
        sid = sorted({s for f in fs for s in f["source_ids"]})
        offerings.append(dict(id="offer:legacy:" + digest(subject)[:12], component_id=matched[0],
            supplier=subject.split(":")[1], condition="not_established", region="US_research_context",
            canadian_fulfillment_verified=False, observed_at=max(sources[s]["accessed_at"] for s in sid),
            observation_status="legacy_snapshot_not_rechecked", price=price["value"] if price else None,
            currency=price["unit"] if price else None, stock_text=stock["value"] if stock else None,
            price_basis="legacy_source_scoped_observation", shipping=None, core_charge=None, warranty=None,
            tax=None, checkout_verified=False, source_ids=sid, legacy_record_ids=[f["id"] for f in fs]))
    # Complete reuse index: link every original finding, including excluded context.
    reuse, failures, gaps, claims = [], [], [], []
    for d in datasets:
        path = next(p for p in (ROOT / "data/datasets").glob("*.json") if read(p)["domain"] == d["domain"])
        for kind in ("facts", "issues", "parts", "gaps"):
            for r in d[kind]:
                systems = route(kind, r, d["domain"], policy)["system_ids_for_discovery"]
                cid = part_component.get(r["id"])
                reuse.append(dict(id=r["id"], kind=kind, path=str(path.relative_to(ROOT)),
                    source_ids=r["source_ids"], original_sha256=digest(r), raw_scope=r.get("applicability"),
                    target_scope_groups=project_scope(r.get("applicability", {})),
                    component_ids=[cid] if cid else [], system_ids_navigation_only=systems,
                    verification_meaning="context_link_not_fitment", excluded_reason=excluded.get(r["id"])))
                if kind == "issues":
                    failures.append(dict(id=r["id"], scope=r["applicability"], source_ids=r["source_ids"],
                        mechanism=r["cause"], diagnosis=r["diagnosis_summary"], correction=r["correction_summary"],
                        evidence_status=r["evidence_status"], limits=r["limits"], system_ids=systems,
                        record_role=next((role for role, ids in read(ROOT / "data/audits/legacy-issue-taxonomy-20261014.json")["assignments"].items() if r["id"] in ids), None),
                        failure_rate=None, comparative_durability_verified=False))
                elif kind == "gaps":
                    gaps.append(dict(id=r["id"], title=r["title"], missing_inputs=r["missing_inputs"],
                        reason=r["reason"], source_ids=r["source_ids"], system_ids=systems, status="unresolved_legacy_question"))
                elif kind == "facts":
                    claims.append(dict(id=r["id"], subject=r["subject"], property=r["predicate"],
                        value=r["value"], unit=r["unit"], scope=r["applicability"], source_ids=r["source_ids"],
                        locator=r["locator"], evidence_status=r["evidence_status"], system_ids=systems,
                        verification_meaning="original_source_scope_only"))
    for f in failures:
        f["target_scope_groups"] = project_scope(f["scope"])
        f["application_role"] = "source_scope_context_not_confirmed_target_vehicle_fault"
    for g in gaps:
        g["target_scope_groups"] = project_scope(records[g["id"]].get("applicability", {}))
    for p in sorted((ROOT / "data/engineering-dossiers").glob("*purchase-engineering-*.json")):
        dossier = read(p)
        for c in dossier["cases"]:
            sid = []
            for url in c["sources"]:
                found = [s["id"] for s in sources.values() if s["url"] == url]
                if not found:
                    id_ = "dossier-src:" + digest(url)[:16]
                    sources[id_] = dict(id=id_, url=url, title="Existing dossier cited source", publisher="See original dossier",
                        source_type="inherited_dossier_reference", accessed_at=dossier["date"],
                        retrieval="metadata_only", notes="Inherited citation; not re-retrieved for this catalog import.")
                    found = [id_]
                sid.extend(found)
            repairs.append(dict(id="repair:case:" + c["id"], dossier_case_id=c["id"],
                original_case_path=str(p.relative_to(ROOT)), original_sha256=digest(c),
                source_ids=sorted(set(sid)), component_ids=sorted({part_component[x] for x in c["prior_ids"] if x in part_component}),
                system_id=c["system"], scope_description=c["applies"], diagnosis=c["failure"],
                target_platform=dossier["scope"]["platform"],
                corrective_path=c["corrective_path"], improvement_status=c["improvement_status"],
                diy_feasibility=c["repair_class"], professional_feasibility="vehicle_specific_quote_needed",
                exceeds_no_engine_transmission_rebuild_goal=c["purchase_decision"] == "avoid_major_unpriced_work",
                original_cost_basis=c["cost_basis"], parts_bill=[], currency=None, labor_hours=None,
                labor_rate=None, complete_parts_total=None, complete_diy_total=None, complete_professional_total=None,
                estimate_status="inherited_engineering_case_full_cost_unestablished", missing_cost_inputs=c["unresolved"],
                prior_record_ids=c["prior_ids"]))
    production = read(ROOT / "data/vehicle-catalogue/us-production-normalized.json")
    configurations = [c for c in production["configurations"] if ("9-" + c["model"].split("-")[-1] + "-" + c["platform"]) in FAMILIES
        and c["engine_code"] in FAMILIES["9-" + c["model"].split("-")[-1] + "-" + c["platform"]][2]
        and FAMILIES["9-" + c["model"].split("-")[-1] + "-" + c["platform"]][0] <= c["model_year"] <= FAMILIES["9-" + c["model"].split("-")[-1] + "-" + c["platform"]][1]]
    for s in production["sources"]:
        sources[s["id"]] = dict(s, title="Compiled US production", publisher="eSaabParts",
            accessed_at=DATE, retrieval="inherited_normalized_register", notes=production["limit"])
    # A part number is namespace-specific. Repeated claims remain separate applications.
    for c in sorted(components.values(), key=lambda c: c["id"]):
        numbers.append(dict(id="pn:" + c["id"], component_id=c["id"], namespace=c["number_namespace"],
                            value=c["part_number"], source_ids=c["source_ids"]))
    manufacturers = []
    for name in sorted({c["marketed_brand"] for c in components.values() if c["marketed_brand"]}):
        members = [c for c in components.values() if c["marketed_brand"] == name]
        manufacturers.append(dict(id="maker:" + re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-"),
            name=name, role="marketed_product_brand_not_original_vehicle_supplier_certification",
            component_ids=[c["id"] for c in members], source_ids=sorted({s for c in members for s in c["source_ids"]})))
    catalogue = dict(schema_version="1.0", as_of=DATE, exhaustive=False, scoring_allowed=False,
        systems=read(ROOT / "data/tier-research/methodology.json")["system_inventory"],
        subsystems=[dict(id=s, system_id=s.split(".")[0]) for s in sorted({a["subsystem_id"] for a in inventory["assemblies"]})],
        assembly_inventory=inventory["assemblies"], components=sorted(components.values(), key=lambda c: c["id"]),
        applications=applications, part_numbers=numbers, part_number_relationships=relations,
        interchanges=interchanges, specifications=specifications, evidence_claims=claims,
        gearbox_families=gearboxes, manufacturers=manufacturers,
        fastener_specification_contract=inventory["fastener_specification_contract"],
        reliability_register=failures, supplier_offerings=offerings, repair_procedures=procedures,
        repair_scenarios=repairs, evidence_sources=sorted(sources.values(), key=lambda s: s["id"]),
        verification_gaps=gaps, unresolved_contradictions=conflicts, research_reuse_index=reuse,
        vehicle_configurations=configurations, configuration_limits="US automatic nonconvertible subset only; manual, convertible, MY1998 US and Canada enumeration incomplete. No fitment certified by trim/year alone.",
        excluded_part_claims=excluded)
    return catalogue


def validate(catalogue):
    errors = []
    tables = [k for k, v in catalogue.items() if isinstance(v, list) and all(isinstance(r, dict) for r in v)]
    for name in tables:
        values = catalogue[name]
        ids = [r.get("id") for r in values]
        if None in ids or len(ids) != len(set(ids)):
            errors.append(name + ": missing/duplicate identities")
    components = {c["id"]: c for c in catalogue["components"]}
    sources = {s["id"]: s for s in catalogue["evidence_sources"]}
    assemblies = {a["id"] for a in catalogue["assembly_inventory"]}
    identities = [(c["number_namespace"], "".join(c["part_number"].split()).lower(), c["assembly_id"]) for c in components.values()]
    if len(identities) != len(set(identities)):
        errors.append("Duplicate component identities")
    for c in components.values():
        if c["assembly_id"] not in assemblies:
            errors.append("Unknown assembly: " + c["id"])
        if c["id"] != identity(c["number_namespace"], c["part_number"], c["assembly_id"]):
            errors.append("Unstable component identity: " + c["id"])
        if not c["source_ids"]:
            errors.append("Unsourced component identity: " + c["id"])
    for name in tables:
        for r in catalogue[name]:
            if "source_ids" in r and set(r["source_ids"]) - sources.keys():
                errors.append("Missing provenance: " + r["id"])
            for field in ("component_id", "from_component_id", "to_component_id"):
                if field in r and r[field] not in components:
                    errors.append("Dangling component link: " + r["id"])
            if set(r.get("component_ids", [])) - components.keys():
                errors.append("Dangling component list: " + r["id"])
    for a in catalogue["applications"]:
        if not a.get("source_ids"):
            errors.append("Unsourced application: " + a["id"])
        if a.get("application_role") == "donor_research_context":
            if a.get("vin_approved"):
                errors.append("Donor context promoted to target fitment")
            continue
        for g in a["scope"].get("groups", [a["scope"]]):
            for p in g.get("platforms", []):
                if p not in FAMILIES:
                    errors.append("Excluded platform application: " + a["id"])
                    continue
                lo, hi, engines = FAMILIES[p]
                if any(not lo <= y <= hi for y in g.get("model_years", [])):
                    errors.append("Model year outside assignment: " + a["id"])
                if set(g.get("engine_codes", [])) - engines:
                    errors.append("Invalid engine/platform combination: " + a["id"])
            if a.get("vin_approved") and not g.get("transmission_codes"):
                errors.append("VIN approval without transmission verification: " + a["id"])
    for r in catalogue["interchanges"]:
        if r["category"] not in "ABCDE" or len(r["category"]) != 1:
            errors.append("Invalid interchange classification")
        if not r["source_ids"] or not r["conditions"]:
            errors.append("Unexplained interchange: " + r["id"])
        if r["category"] in "DE" and (r["fitment_approved"] or r["donor_approved"]):
            errors.append("Unverified/modification lead marked approved: " + r["id"])
        if r["category"] == "A" and r["identity_basis"] not in {"dual_official_channel_exact_number", "manufacturer_oe_information_exact_number"}:
            errors.append("Unauthenticated category A: " + r["id"])
        if r["category"] == "B" and r["identity_basis"] != "manufacturer_repair_instructions":
            errors.append("Unapproved category B basis: " + r["id"])
        if r["category"] == "C" and not r.get("independent_fitment_proof_ids"):
            errors.append("Category C without independent fitment proof")
        if r["fitment_approved"] and not r.get("application_ids"):
            errors.append("Approved fitment without application evidence")
        if r["reliability_improvement_proven"] and not r.get("comparative_evidence_ids"):
            errors.append("Durability upgrade without comparative evidence")
        left, right = components[r["from_component_id"]], components[r["to_component_id"]]
        if left["assembly_id"] != right["assembly_id"] and r["category"] != "B":
            errors.append("Cross-category interchange: " + r["id"])
        if "92151823" in {left["part_number"], right["part_number"]} and "water_pump" in {left["assembly_id"], right["assembly_id"]}:
            errors.append("Quarantined pump-to-screw relationship escaped")
    for o in catalogue["supplier_offerings"]:
        if o["price"] is not None and (type(o["price"]) not in (int, float) or o["price"] < 0 or o["currency"] not in {"USD", "CAD", "EUR", "GBP"}):
            errors.append("Invalid price/currency: " + o["id"])
        try:
            date.fromisoformat(o["observed_at"])
        except (ValueError, TypeError):
            errors.append("Undated offering")
    for gb in catalogue["gearbox_families"]:
        if gb["platform"] not in FAMILIES or gb["assembly_id"] not in assemblies:
            errors.append("Invalid gearbox platform/assembly")
        if gb["production_application_verified"] and not gb.get("application_proof_ids"):
            errors.append("Gearbox example promoted to production application")
    # Active supersessions require exact endpoints, no category crossing, one
    # successor per adjudicated cohort, and no cycles. Raw disputed claims stay inactive.
    graph = defaultdict(set)
    by_cohort = defaultdict(set)
    for rel in catalogue["part_number_relationships"]:
        if not rel["approved"]:
            continue
        left = rel.get("from_component_id")
        right = rel.get("to_component_id")
        if left not in components or right not in components or not rel.get("application_ids"):
            errors.append("Approved supersession lacks endpoint/cohort proof")
            continue
        if components[left]["assembly_id"] != components[right]["assembly_id"]:
            errors.append("Approved cross-category supersession")
        graph[left].add(right)
        for cohort in rel["application_ids"]:
            by_cohort[(left, cohort)].add(right)
    if any(len(v) > 1 for v in by_cohort.values()):
        errors.append("Contradictory active supersessions")
    def cycle(node, active, done):
        if node in active:
            return True
        if node in done:
            return False
        active.add(node)
        if any(cycle(n, active, done) for n in graph.get(node, [])):
            return True
        active.remove(node)
        done.add(node)
        return False
    done = set()
    if any(cycle(n, set(), done) for n in list(graph)):
        errors.append("Cyclic active supersessions")
    originals = {r["id"]: r for d in load_datasets() for k in ("facts", "issues", "parts", "gaps") for r in d[k]}
    for r in catalogue["research_reuse_index"]:
        if r["id"] not in originals or digest(originals[r["id"]]) != r["original_sha256"]:
            errors.append("Unexplained change to reviewed legacy evidence: " + r["id"])
    for r in catalogue["repair_scenarios"]:
        totals = [r.get(k) for k in ("complete_parts_total", "complete_diy_total", "complete_professional_total")]
        if any(v is not None for v in totals) and (r["missing_cost_inputs"] or not r.get("currency")):
            errors.append("Incomplete repair presented as total cost: " + r["id"])
        currencies = {p["currency"] for p in r["parts_bill"] if p.get("currency")}
        if currencies and currencies != {r["currency"]}:
            errors.append("Mixed repair currencies without conversion: " + r["id"])
    # Conflicting measured/specification claims cannot be hidden by selecting one.
    specs = defaultdict(list)
    for s in catalogue["specifications"]:
        specs[(s["component_id"], s["property"], digest(s.get("scope")))].append(s)
    for rows in specs.values():
        if len({digest((s["value"], s["unit"])) for s in rows}) > 1 and not all(s.get("conflict_id") for s in rows):
            errors.append("Conflicting specifications without contradiction linkage")
    return errors


def coverage(c):
    apps = defaultdict(set)
    for a in c["applications"]:
        for p in a["scope"].get("platforms", []):
            if p in FAMILIES:
                apps[a["component_id"]].add(p)
    rows = []
    for p in FAMILIES:
        for system in c["systems"]:
            assemblies = {a["id"] for a in c["assembly_inventory"] if a["system_id"] == system["id"] and p[-4:] in a["research_targets"]}
            parts = [x for x in c["components"] if x["assembly_id"] in assemblies and p in apps[x["id"]]]
            known = {x["assembly_id"] for x in parts}
            part_ids = {x["id"] for x in parts}
            approved = {a["component_id"] for a in c["applications"] if a.get("vin_approved") and p in a["scope"].get("platforms", [])}
            rows.append(dict(platform=p, system_id=system["id"], inventory_serviceable_groups=len(assemblies),
                identified_product_records=len(parts), serviceable_groups_with_product_claims=len(known),
                verified_original_installed_identities=sum(x["original_installed_identity_verified"] for x in parts),
                verified_vin_replacements=len({a["component_id"] for a in c["applications"] if a.get("vin_approved") and p in a["scope"].get("platforms", []) and a["component_id"] in {x["id"] for x in parts}}),
                factory_specified_component_identities=len({a["component_id"] for a in c["applications"] if a.get("factory_specification_verified") and a["component_id"] in part_ids and p in a["scope"].get("platforms", [])}),
                manufacturer_documented_service_applications=len({a["component_id"] for a in c["applications"] if a.get("manufacturer_application_verified") and a["component_id"] in part_ids and p in a["scope"].get("platforms", [])}),
                verified_cross_brand_vin_alternatives=len({r["to_component_id"] for r in c["interchanges"] if r["donor_approved"] and r["fitment_approved"] and r["from_component_id"] in part_ids and r["to_component_id"] in approved}),
                components_with_complete_repair_costs=len({x for r in c["repair_scenarios"] if r["complete_professional_total"] is not None for x in r["component_ids"] if x in {p["id"] for p in parts}}),
                product_records_with_fitment_or_sourcing_gaps=len(parts),
                remaining_assembly_groups=sorted(assemblies-known)))
    return dict(as_of=DATE, whole_vehicle_universe_established=False, completeness_percentage=None,
        denominator_policy="Inventory serviceable groups are research slots; products count namespace/number/category identities. A group can contain many products. Neither is an exhaustive factory component universe.",
        counts={k:len(c[k]) for k in ("assembly_inventory", "components", "applications", "interchanges", "supplier_offerings", "repair_scenarios", "gearbox_families", "vehicle_configurations", "research_reuse_index")},
        platform_system_rows=rows, scoring_allowed=False,
        readiness_reason="No configuration has a fully verified original BOM, regional replacement package and complete repair economics. Failure rates and comparative upgrade durability are not established.")


def readiness(c):
    return dict(as_of=DATE, scoring_allowed=False, configurations=[dict(
        id="readiness:" + x["id"], configuration_id=x["id"], platform=x["platform"],
        model_year=x["model_year"], engine_code=x["engine_code"],
        reliability="insufficient_evidence", parts_availability="insufficient_evidence",
        repair_economics="insufficient_evidence", overall="unranked",
        blockers=["Factory original-component and revision identities incomplete",
                  "Gearbox tag/application and software calibration not certified",
                  "Regional per-application replacement/stock packages incomplete",
                  "Complete DIY/shop repair costs absent",
                  "No validated population failure incidence or comparative durability"])
        for x in c["vehicle_configurations"]], excluded_from_current_enumeration=[
            "Canadian configurations", "Manual gearbox configurations",
            "9440 convertibles", "MY1998 US 9600 production rows"],
        enumeration_is_not_brandwide_vehicle_universe=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--component", help="Part number, identity or name substring")
    parser.add_argument("--platform", choices=FAMILIES)
    args = parser.parse_args()
    c = build()
    errors = validate(c)
    if errors:
        raise SystemExit("\n".join(errors))
    output = json.dumps(c, ensure_ascii=False, indent=2) + "\n"
    summary = json.dumps(coverage(c), ensure_ascii=False, indent=2) + "\n"
    ready = json.dumps(readiness(c), ensure_ascii=False, indent=2) + "\n"
    if args.check:
        expected = {OUTPUT: output, DIR / "coverage.json": summary, DIR / "readiness.json": ready}
        if any(not path.exists() or path.read_text() != value for path, value in expected.items()):
            raise SystemExit("Generated component catalogue/coverage drift: run --write")
        print("PASS: catalogue reproducible; foreign keys, provenance, scope and evidence guards valid")
    elif args.write:
        OUTPUT.write_text(output)
        (DIR / "coverage.json").write_text(summary)
        (DIR / "readiness.json").write_text(ready)
        print(json.dumps(coverage(c)["counts"], indent=2))
    elif args.component or args.platform:
        ids = {a["component_id"] for a in c["applications"] if not args.platform or args.platform in a["scope"].get("platforms", [])}
        selected = [x for x in c["components"] if (not args.platform or x["id"] in ids) and (not args.component or args.component.lower() in json.dumps(x).lower())]
        chosen = {x["id"] for x in selected}
        print(json.dumps(dict(components=selected,
            gearbox_families=[g for g in c["gearbox_families"] if (not args.platform or args.platform == g["platform"]) and (not args.component or args.component.lower() in json.dumps(g).lower())],
            applications=[a for a in c["applications"] if a["component_id"] in chosen],
            interchanges=[r for r in c["interchanges"] if r["from_component_id"] in chosen or r["to_component_id"] in chosen],
            offerings=[o for o in c["supplier_offerings"] if o["component_id"] in chosen]), indent=2))
    else:
        print(summary)


if __name__ == "__main__":
    main()
