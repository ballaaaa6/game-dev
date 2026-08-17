"""Build AM-3 selector usage and data-field semantic matrices."""

from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "knowledge/fixtures/accepted"
RUNTIME_EVIDENCE = ROOT / "knowledge/fixtures/accepted/runtime"

COVERAGE_PATH = EVIDENCE / "asset_metadata_coverage.json"
TAXONOMY_PATH = EVIDENCE / "asset_family_taxonomy.json"
NATIVE_CATALOG_PATH = RUNTIME_EVIDENCE / "native_content_catalog.json"
NATIVE_REGISTRY_PATH = EVIDENCE / "native_content_registry.json"
SELECTOR_CONTRACT_PATH = EVIDENCE / "asset_selector_contract.json"

SELECTOR_MATRIX_PATH = EVIDENCE / "asset_selector_usage_matrix.json"
FIELD_MATRIX_PATH = EVIDENCE / "data_field_semantics_matrix.json"
CONTRACT_PATH = RUNTIME_EVIDENCE / "asset_selector_usage_contract.json"
REPORT_PATH = ROOT / "docs/reports/social-dev_asset_selector_usage.md"

KNOWN_CONTROLS = {
    ("RoomData", "objMap_"): ("scene_topology_control", "non_asset_control", "closed_native_control"),
    ("RoomData", "objDir_"): ("scene_direction_control", "non_asset_control", "closed_native_control"),
    ("FurnitureData", "passMap_"): ("placement_collision_control", "non_asset_control", "closed_native_control"),
    ("RoomData", "floor_"): ("mapchip_topology_variant_control", "non_asset_control", "closed_native_control"),
    ("FurnitureData", "iconU_"): ("texture_uv_control", "non_asset_control", "source_field_semantics"),
    ("FurnitureData", "iconV_"): ("texture_uv_control", "non_asset_control", "source_field_semantics"),
}

FIELD_PROFILES = {
    ("FurnitureData", "seb_"): {
        "semantic_role": "furniture_primary_animation_selector",
        "asset_disposition": "direct_selector",
        "selector_kind": "seb",
        "call_contract": "furniture_primary_animation",
        "sentinel_policy": "nonnegative_requires_resolution; -1 is not present in the closed FurnitureData seb_ rows",
    },
    ("FurnitureData", "subSeb_"): {
        "semantic_role": "furniture_secondary_animation_selector",
        "asset_disposition": "direct_selector",
        "selector_kind": "seb",
        "call_contract": "furniture_secondary_animation",
        "sentinel_policy": "-1 means absent_by_sentinel; nonnegative values require resolution",
    },
    ("FurnitureData", "img_"): {
        "semantic_role": "furniture_direct_image_selector",
        "asset_disposition": "direct_selector",
        "selector_kind": "img",
        "call_contract": "furniture_direct_image",
        "sentinel_policy": "-1 means absent_by_sentinel; nonnegative values require resolution",
    },
    ("StaffData", "img_"): {
        "semantic_role": "staff_human_image_selector",
        "asset_disposition": "direct_selector",
        "selector_kind": "img",
        "call_contract": "staff_human_image",
        "sentinel_policy": "nonnegative requires resolution; all closed StaffData rows resolve",
    },
    ("HelperData", "img_"): {
        "semantic_role": "helper_image_selector",
        "asset_disposition": "direct_selector",
        "selector_kind": "img",
        "call_contract": "helper_image",
        "sentinel_policy": "-1 may be absent; human-scope values require an explicit helper selector-scope contract",
    },
    ("RoomData", "floorImgId_"): {
        "semantic_role": "room_floor_indirect_selector",
        "asset_disposition": "indirect_selector",
        "selector_kind": "img",
        "call_contract": "room_floor_image_indirection",
        "sentinel_policy": "nonnegative value indexes Room.FLOOR_IMAGE_ID_ARRAY; no silent direct-id interpretation",
    },
    ("RoomData", "wallImgId_"): {
        "semantic_role": "room_wall_image_selector",
        "asset_disposition": "direct_selector",
        "selector_kind": "img",
        "call_contract": "room_wall_image",
        "sentinel_policy": "nonnegative requires resolution",
    },
    ("RoomData", "doorImgId_"): {
        "semantic_role": "room_door_image_selector",
        "asset_disposition": "direct_selector",
        "selector_kind": "img",
        "call_contract": "room_door_image",
        "sentinel_policy": "nonnegative requires resolution",
    },
}


def stable_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def field_key(source_type: str | None, field: str | None) -> str:
    return f"{source_type or 'unknown'}.{field or 'unknown'}"


def classify_unrelated_field(source_type: str, field: str, field_type: str | None, consumer_count: int) -> dict[str, Any]:
    control = KNOWN_CONTROLS.get((source_type, field))
    if control:
        role, disposition, evidence_status = control
        return {"semantic_role": role, "asset_disposition": disposition, "semantic_status": evidence_status, "selector_scope_status": "not_applicable"}
    if field.isupper():
        return {"semantic_role": "constant_or_enum", "asset_disposition": "non_asset_constant_or_enum", "semantic_status": "closed_structural_non_asset", "selector_scope_status": "not_applicable"}
    lowered = field.lower()
    if field in {"iconU_", "iconV_"} or lowered.endswith("rate_") or "effect" in lowered:
        return {"semantic_role": "gameplay_or_texture_control", "asset_disposition": "non_asset_control", "semantic_status": "closed_structural_non_asset", "selector_scope_status": "not_applicable"}
    if any(token in lowered for token in ("img", "image", "icon", "texture", "sprite", "banner", "background")):
        return {"semantic_role": "visual_selector_candidate", "asset_disposition": "candidate_selector_without_relation", "semantic_status": "selector_scope_or_consumer_contract_needed", "selector_scope_status": "not_closed"}
    if consumer_count:
        return {"semantic_role": "consumer_data_or_control", "asset_disposition": "non_asset_or_semantic_deferred", "semantic_status": "consumer_semantics_needed", "selector_scope_status": "not_applicable"}
    return {"semantic_role": "data_only_or_control_candidate", "asset_disposition": "non_asset_or_semantic_deferred", "semantic_status": "field_not_selector_bearing_in_current_graph", "selector_scope_status": "not_applicable"}


def build_usage_and_fields() -> tuple[dict[str, Any], dict[str, Any]]:
    coverage = load_json(COVERAGE_PATH)
    taxonomy = load_json(TAXONOMY_PATH)
    catalog = load_json(NATIVE_CATALOG_PATH)
    registry = load_json(NATIVE_REGISTRY_PATH)
    selector_contract = load_json(SELECTOR_CONTRACT_PATH)
    taxonomy_by_asset = {item["asset_id"]: item for item in taxonomy["assets"]}
    namespace_to_type = {
        item.get("native_namespace", "").removeprefix("data:"): item.get("element_type")
        for item in registry.get("data_types", [])
    }

    consumer_by_field: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for edge in catalog["connections"]["consumer"]:
        if edge.get("from", "").startswith("field:"):
            consumer_by_field[edge["from"][len("field:") :]].append(edge)
    lifecycle_by_field: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for edge in catalog["connections"]["lifecycle"]:
        if edge.get("from", "").startswith("field:"):
            lifecycle_by_field[edge["from"][len("field:") :]].append(edge)

    relations_by_selector: dict[str, list[dict[str, Any]]] = defaultdict(list)
    relations_by_field: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for relation in registry["data_selector_relations"]:
        selector = relation.get("to")
        namespace = relation.get("from", "").split(":")[1] if relation.get("from", "").startswith("data:") else None
        key = field_key(namespace_to_type.get(namespace, namespace), relation.get("field"))
        relations_by_field[key].append(relation)
        if selector:
            relations_by_selector[selector].append(relation)

    field_rows = []
    for field in coverage["data_fields"]:
        source_type = field["source_type"]
        name = field["field"]
        key = field_key(source_type, name)
        relations = relations_by_field.get(key, [])
        profile = FIELD_PROFILES.get((source_type, name))
        if profile:
            semantics = {**profile, "semantic_status": "closed_selector_field_contract", "selector_scope_status": "resolved_or_explicit_gap"}
        else:
            semantics = classify_unrelated_field(source_type, name, field.get("field_type"), field["consumer_edge_count"])
        values = [item.get("native_value") for item in relations]
        target_assets = sorted({item.get("target_asset_id") for item in relations if item.get("target_asset_id")})
        statuses = dict(sorted(Counter(item.get("status", "unknown") for item in relations).items()))
        field_rows.append(
            {
                **field,
                "field_key": key,
                **semantics,
                "relation_count": len(relations),
                "relation_statuses": statuses,
                "native_value_min": min(values) if values else None,
                "native_value_max": max(values) if values else None,
                "sentinel_value_count": sum(1 for value in values if value == -1),
                "target_asset_count": len(target_assets),
                "target_assets_sample": target_assets[:20],
                "consumer_methods": sorted({edge.get("source", {}).get("method") for edge in consumer_by_field.get(name, []) if edge.get("source", {}).get("method")}),
                "lifecycle_phases": sorted({edge.get("phase") for edge in lifecycle_by_field.get(name, []) if edge.get("phase")}),
                "consumer_evidence_count": len(consumer_by_field.get(name, [])),
                "lifecycle_evidence_count": len(lifecycle_by_field.get(name, [])),
                "runtime_call_ready": bool(
                    profile
                    and semantics["semantic_status"] == "closed_selector_field_contract"
                    and not statuses.get("selector_scope_unresolved")
                ),
            }
        )

    selector_rows = []
    selector_usage_counts: Counter[str] = Counter()
    for selector in coverage["selectors"]:
        selector_key = selector["selector_key"]
        relations = relations_by_selector.get(selector_key, [])
        target = selector.get("target_asset_id")
        family = taxonomy_by_asset.get(target, {}) if target else {}
        fields = sorted(
            {
                field_key(
                    namespace_to_type.get(item.get("from", "").split(":")[1]) if item.get("from", "").startswith("data:") else None,
                    item.get("field"),
                )
                for item in relations
            }
        )
        consumers = []
        lifecycle_phases = set()
        for item in relations:
            source_field = item.get("field")
            consumers.extend(consumer_by_field.get(source_field, []))
            lifecycle_phases.update(edge.get("phase") for edge in lifecycle_by_field.get(source_field, []) if edge.get("phase"))
        if selector["coverage_status"] == "unresolved_selector":
            usage_status = "unresolved_identity"
        elif selector["data_relation_count"] == 0:
            usage_status = "resolved_unreferenced_by_closed_data_relations"
        elif target and selector["coverage_status"] == "resolved_target_runtime_referenced":
            usage_status = "resolved_runtime_referenced"
        else:
            usage_status = "resolved_data_referenced_not_runtime_promoted"
        selector_usage_counts[usage_status] += 1
        selector_rows.append(
            {
                **selector,
                "target_family_id": family.get("family_id"),
                "target_subfamily_id": family.get("subfamily_id"),
                "target_lineage": family.get("lineage"),
                "data_relation_count": len(relations),
                "data_fields": fields,
                "native_values": sorted({item.get("native_value") for item in relations}),
                "consumer_methods": sorted({edge.get("source", {}).get("method") for edge in consumers if edge.get("source", {}).get("method")}),
                "consumer_targets": sorted({edge.get("to") for edge in consumers}),
                "lifecycle_phases": sorted(lifecycle_phases),
                "usage_status": usage_status,
                "selector_call_contract": (
                    "no_call_unresolved_identity"
                    if usage_status == "unresolved_identity"
                    else "resolve_selector_then_resolve_target_asset_then_apply_family_composition_policy"
                ),
                "negative_value_policy": "not_applicable_to_selector_row",
            }
        )

    field_counts = Counter(item["semantic_status"] for item in field_rows)
    direct_selector_fields = [item for item in field_rows if item["asset_disposition"] in {"direct_selector", "indirect_selector"}]
    selector_field_contracts = []
    for field in sorted(direct_selector_fields, key=lambda item: item["field_key"]):
        selector_field_contracts.append(
            {
                "field_key": field["field_key"],
                "semantic_role": field["semantic_role"],
                "asset_disposition": field["asset_disposition"],
                "selector_kind": field.get("selector_kind"),
                "call_contract": field.get("call_contract"),
                "sentinel_policy": field.get("sentinel_policy"),
                "consumer_methods": field["consumer_methods"],
                "lifecycle_phases": field["lifecycle_phases"],
                "relation_statuses": field["relation_statuses"],
                "runtime_call_ready": field["runtime_call_ready"],
            }
        )

    field_payload = {
        "schema_version": "social-dev-data-field-semantics-matrix-v1",
        "package": "social-dev",
        "status": "pass",
        "semantic_status": "field_dispositions_explicit_selector_contracts_partial",
        "coverage_ref": {"path": "knowledge/fixtures/accepted/asset_metadata_coverage.json", "content_hash": coverage["determinism"]["content_hash"]},
        "selector_contract_ref": {"path": "knowledge/fixtures/accepted/asset_selector_contract.json", "schema_version": selector_contract["schema_version"]},
        "counts": {
            "fields": len(field_rows),
            "selector_bearing_fields": len(direct_selector_fields),
            "field_semantic_statuses": dict(sorted(field_counts.items())),
            "fields_with_consumer_evidence": sum(1 for item in field_rows if item["consumer_evidence_count"]),
            "fields_with_deferred_selector_scope": sum(1 for item in field_rows if item["selector_scope_status"] == "not_closed"),
        },
        "field_semantics": field_rows,
        "selector_field_contracts": selector_field_contracts,
        "policy": {
            "no_selector_relation_is_not_treated_as_asset_absence": True,
            "candidate_visual_fields_remain_explicit_until_scope_is_proven": True,
            "negative_values_are_preserved_as_sentinels": True,
            "room_floor_indirection_is_not_flattened_to_a_direct_id": True,
        },
    }
    field_payload["determinism"] = {"algorithm": "stable-json-sha256 excluding determinism.content_hash", "content_hash": sha256_bytes(stable_json(field_payload).encode("utf-8"))}

    selector_payload = {
        "schema_version": "social-dev-asset-selector-usage-matrix-v1",
        "package": "social-dev",
        "status": "pass",
        "semantic_status": "selector_usage_contract_partial_runtime_approval_separate",
        "coverage_ref": {"path": "knowledge/fixtures/accepted/asset_metadata_coverage.json", "content_hash": coverage["determinism"]["content_hash"]},
        "taxonomy_ref": {"path": "knowledge/fixtures/accepted/asset_family_taxonomy.json", "content_hash": taxonomy["determinism"]["content_hash"]},
        "counts": {"selectors": len(selector_rows), "usage_statuses": dict(sorted(selector_usage_counts.items())), "selectors_with_data_relations": sum(1 for item in selector_rows if item["data_relation_count"]), "selectors_with_consumer_methods": sum(1 for item in selector_rows if item["consumer_methods"]), "unresolved_selectors": sum(1 for item in selector_rows if item["usage_status"] == "unresolved_identity")},
        "selectors": selector_rows,
        "call_policy": {
            "lookup_key": "resource_scope + selector_kind + selector_id",
            "target_identity": "target_asset_id",
            "composition_boundary": "selector resolution does not itself authorize drawing; family composition and geometry gates remain required",
            "unresolved_behavior": "return explicit unresolved status; do not guess filename or numeric id",
        },
    }
    selector_payload["determinism"] = {"algorithm": "stable-json-sha256 excluding determinism.content_hash", "content_hash": sha256_bytes(stable_json(selector_payload).encode("utf-8"))}
    return selector_payload, field_payload


def build_contract_payload(selector_matrix: dict[str, Any], field_matrix: dict[str, Any]) -> dict[str, Any]:
    payload = {
        "schema_version": "social-dev-asset-selector-usage-contract-v1",
        "package": "social-dev",
        "status": "pass",
        "semantic_status": "selector_usage_contract_not_full_runtime_approval",
        "selector_matrix": {"path": "knowledge/fixtures/accepted/asset_selector_usage_matrix.json", "content_hash": selector_matrix["determinism"]["content_hash"]},
        "field_matrix": {"path": "knowledge/fixtures/accepted/data_field_semantics_matrix.json", "content_hash": field_matrix["determinism"]["content_hash"]},
        "counts": {"selectors": selector_matrix["counts"]["selectors"], "fields": field_matrix["counts"]["fields"], "selector_bearing_fields": field_matrix["counts"]["selector_bearing_fields"], "unresolved_selectors": selector_matrix["counts"]["unresolved_selectors"], "deferred_selector_scope_fields": field_matrix["counts"]["fields_with_deferred_selector_scope"]},
        "acceptance": {
            "every_selector_has_lookup_identity": all(item["resource_scope"] and item["selector_kind"] is not None for item in selector_matrix["selectors"] if item["usage_status"] != "unresolved_identity"),
            "every_field_has_explicit_disposition": all(item["asset_disposition"] for item in field_matrix["field_semantics"]),
            "every_selector_has_explicit_unresolved_or_call_policy": all(item["selector_call_contract"] for item in selector_matrix["selectors"]),
            "sentinel_policy_is_preserved": any(item["sentinel_value_count"] for item in field_matrix["field_semantics"]),
            "runtime_promotion_is_not_inferred": True,
        },
        "runtime_policy": {"may_be_used_for_lookup": True, "may_be_used_to_draw_without_composition_gate": False, "next_gate": "asset_composition_geometry_catalog"},
    }
    payload["determinism"] = {"algorithm": "stable-json-sha256 excluding determinism.content_hash", "content_hash": sha256_bytes(stable_json(payload).encode("utf-8"))}
    return payload


def markdown_report(selector: dict[str, Any], fields: dict[str, Any], contract: dict[str, Any]) -> str:
    lines = [
        "# Social Dev selector usage and data-field semantics",
        "",
        "AM-3 converts selector IDs and data fields into explicit lookup/call contracts. It preserves native IDs, `-1` sentinels, unresolved helper scope, and the Room floor indirection instead of flattening them into guessed asset names.",
        "",
        "## Identity",
        "",
        f"- Selector matrix hash: `{selector['determinism']['content_hash']}`",
        f"- Field matrix hash: `{fields['determinism']['content_hash']}`",
        f"- Contract hash: `{contract['determinism']['content_hash']}`",
        "",
        "## Counts",
        "",
        "| Dimension | Count |",
        "|---|---:|",
        f"| Selectors | {selector['counts']['selectors']:,} |",
        f"| Selectors with data relations | {selector['counts']['selectors_with_data_relations']:,} |",
        f"| Selectors with consumer methods | {selector['counts']['selectors_with_consumer_methods']:,} |",
        f"| Unresolved selectors | {selector['counts']['unresolved_selectors']:,} |",
        f"| Data fields | {fields['counts']['fields']:,} |",
        f"| Selector-bearing fields | {fields['counts']['selector_bearing_fields']:,} |",
        f"| Fields with consumer evidence | {fields['counts']['fields_with_consumer_evidence']:,} |",
        f"| Fields with deferred selector scope | {fields['counts']['fields_with_deferred_selector_scope']:,} |",
        "",
        "## Closed field contracts",
        "",
        "| Field | Role | Disposition | Call contract | Sentinel/indirection policy |",
        "|---|---|---|---|---|",
    ]
    for item in fields["selector_field_contracts"]:
        lines.append(f"| `{item['field_key']}` | {item['semantic_role']} | `{item['asset_disposition']}` | `{item['call_contract']}` | {item['sentinel_policy']} |")
    lines.extend(
        [
            "",
            "## Usage statuses",
            "",
            "| Status | Count |",
            "|---|---:|",
        ]
    )
    for status, count in selector["counts"]["usage_statuses"].items():
        lines.append(f"| `{status}` | {count:,} |")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- Selector lookup is now deterministic by `(resource_scope, selector_kind, selector_id)`.",
            "- Selector lookup does not authorize drawing; composition/frame/geometry remains AM-4.",
            "- Fields without a current selector relation have an explicit disposition, including candidate visual fields whose selector scope remains open.",
            "",
            "```powershell",
            "python -B tools/social-dev/build_asset_selector_usage_matrix.py",
            "python -B tools/social-dev/test_asset_selector_usage_matrix.py",
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    selector_matrix, field_matrix = build_usage_and_fields()
    contract = build_contract_payload(selector_matrix, field_matrix)
    write_json(SELECTOR_MATRIX_PATH, selector_matrix)
    write_json(FIELD_MATRIX_PATH, field_matrix)
    write_json(CONTRACT_PATH, contract)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(markdown_report(selector_matrix, field_matrix, contract), encoding="utf-8", newline="\n")
    print(json.dumps({"selector_matrix_hash": selector_matrix["determinism"]["content_hash"], "field_matrix_hash": field_matrix["determinism"]["content_hash"], "selectors": selector_matrix["counts"]["selectors"], "fields": field_matrix["counts"]["fields"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
