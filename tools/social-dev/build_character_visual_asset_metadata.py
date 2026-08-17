"""Build the Track H human/helper/avatar visual asset metadata catalog."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "knowledge/fixtures/accepted"
RUNTIME_EVIDENCE = ROOT / "knowledge/fixtures/accepted/runtime"

CHARACTER_METADATA_PATH = RUNTIME_EVIDENCE / "character_metadata_contract.json"
CHARACTER_CAPABILITY_PATH = RUNTIME_EVIDENCE / "character_capability_contract.json"
CHARACTER_ASSET_PATH = RUNTIME_EVIDENCE / "character_asset_manifest.json"
TAXONOMY_PATH = EVIDENCE / "asset_family_taxonomy.json"
GEOMETRY_PATH = EVIDENCE / "asset_geometry_catalog.json"
SELECTOR_MATRIX_PATH = EVIDENCE / "asset_selector_usage_matrix.json"

CATALOG_PATH = EVIDENCE / "character_visual_asset_metadata.json"
CONTRACT_PATH = RUNTIME_EVIDENCE / "character_visual_asset_metadata_contract.json"
REPORT_PATH = ROOT / "docs/reports/social-dev_character_visual_asset_metadata.md"


def stable_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def package_rows(taxonomy: dict[str, Any], family_id: str) -> list[dict[str, Any]]:
    return [
        {
            "asset_id": item["asset_id"],
            "relative_path": item["relative_path"],
            "kind": item["kind"],
            "extension": item["extension"],
            "subfamily_id": item["subfamily_id"],
            "lineage": item["lineage"],
            "coverage_status": item["coverage_status"],
            "runtime_families": item["runtime_families"],
            "geometry_status": item["geometry_status"],
        }
        for item in taxonomy["assets"]
        if item["family_id"] == family_id
    ]


def build_payload() -> dict[str, Any]:
    metadata = load_json(CHARACTER_METADATA_PATH)
    capability = load_json(CHARACTER_CAPABILITY_PATH)
    asset_manifest = load_json(CHARACTER_ASSET_PATH)
    taxonomy = load_json(TAXONOMY_PATH)
    geometry = load_json(GEOMETRY_PATH)
    selector_matrix = load_json(SELECTOR_MATRIX_PATH)
    geometry_by_asset = {item["asset_id"]: item for item in geometry["assets"]}
    selector_by_key = {item["selector_key"]: item for item in selector_matrix["selectors"] if item.get("selector_key")}

    staff = []
    for item in metadata["staff"]:
        selector = item.get("render", {}).get("image_selector", {})
        asset = selector.get("asset", {})
        asset_id = asset.get("asset_id")
        staff.append(
            {
                "record_id": item["id"],
                "source_id": item.get("source_identity", {}).get("source_id"),
                "name": item.get("name"),
                "source_fields": item.get("source_fields"),
                "relations": item.get("relations"),
                "capability_profile_ref": item.get("render", {}).get("capability_profile_ref"),
                "image_selector": {
                    "selector_key": selector.get("reference"),
                    "selector_id": selector.get("id"),
                    "asset_id": asset_id,
                    "resolution_status": selector.get("resolution_status"),
                    "geometry_status": geometry_by_asset.get(asset_id, {}).get("geometry_status") if asset_id else None,
                },
                "runtime_status": "human_image_binding_ready" if selector.get("resolution_status") == "resolved" else "human_image_binding_gap",
            }
        )

    helpers = []
    for item in metadata["helpers"]:
        render = item.get("render", {})
        image = render.get("image_selector", {})
        big_image = render.get("big_image_selector", {})
        image_ref = image.get("reference")
        image_asset = image.get("asset", {}).get("asset_id") if image.get("asset") else None
        helper_row = {
            "record_id": item["id"],
            "source_id": item.get("source_identity", {}).get("source_id"),
            "name": item.get("name"),
            "description": item.get("description"),
            "source_fields": item.get("source_fields"),
            "capability_profile_ref": render.get("capability_profile_ref"),
            "image_selector": {
                "selector_key": image_ref,
                "selector_id": image.get("id"),
                "asset_id": image_asset,
                "resolution_status": image.get("resolution_status"),
                "catalog_selector_status": selector_by_key.get(image_ref, {}).get("status") if image_ref else None,
                "geometry_status": geometry_by_asset.get(image_asset, {}).get("geometry_status") if image_asset else None,
            },
            "big_image_selector": {
                "selector_id": big_image.get("id"),
                "resolution_status": big_image.get("resolution_status"),
                "status": big_image.get("status"),
            },
            "runtime_status": "helper_image_ready" if image.get("resolution_status") == "resolved" else "helper_image_deferred_or_absent",
        }
        helpers.append(helper_row)

    def profile_summary(profile: dict[str, Any]) -> dict[str, Any]:
        actions = profile.get("actions", {})
        return {
            "profile_id": profile.get("profile_id"),
            "family": profile.get("family"),
            "record_kind": profile.get("record_kind"),
            "action_count": len(actions),
            "action_statuses": dict(sorted(Counter(item.get("status", "unknown") for item in actions.values()).items())),
            "selector_ready_action_count": sum(1 for item in actions.values() if item.get("status") in {"selector_ready", "native_selector_ready", "fallback_ready"}),
            "actions": {
                name: {"status": item.get("status"), "semantic_status": item.get("semantic_status"), "source_action": item.get("source_action"), "fallback_action": item.get("fallback_action")}
                for name, item in sorted(actions.items())
            },
        }

    profiles = [profile_summary(item) for item in capability.get("profiles", [])]
    human_images = [
        {
            "asset_id": item.get("asset_id"),
            "selector_id": item.get("selector_id"),
            "filename": item.get("filename"),
            "runtime_sha256": item.get("runtime_sha256"),
            "geometry_status": geometry_by_asset.get(item.get("asset_id"), {}).get("geometry_status"),
            "status": item.get("status"),
        }
        for item in asset_manifest.get("images", [])
    ]
    human_animations = [
        {
            "asset_id": item.get("asset_id"),
            "selector_id": item.get("selector_id"),
            "filename": item.get("filename"),
            "frame_bound": item.get("header", {}).get("frame_bound"),
            "layer_count": item.get("header", {}).get("layer_count"),
            "record_count": item.get("header", {}).get("record_count"),
            "geometry_status": geometry_by_asset.get(item.get("asset_id"), {}).get("geometry_status"),
            "status": item.get("status"),
        }
        for item in asset_manifest.get("animations", [])
    ]

    packages = []
    for family_id, role, status in [
        ("character.staff.human", "human StaffData visuals and native action SEBs", "approved_for_runtime_catalog"),
        ("character.helper", "HelperData visual package", "metadata_closed_visual_resolution_partial"),
        ("character.avatar.body", "Avatar body/pose parts", "family_catalog_only_no_runtime_binding"),
        ("character.avatar.head", "Avatar head/face parts", "family_catalog_only_no_runtime_binding"),
        ("event.visual", "Event visual package reserved for event-only actor scope", "event_only_catalog_boundary"),
    ]:
        rows = package_rows(taxonomy, family_id)
        packages.append(
            {
                "family_id": family_id,
                "role": role,
                "status": status,
                "asset_count": len(rows),
                "extension_counts": dict(sorted(Counter(item["extension"] for item in rows).items())),
                "asset_rows": rows,
            }
        )

    helper_image_statuses = Counter(item["image_selector"]["resolution_status"] for item in helpers)
    helper_big_statuses = Counter(item["big_image_selector"]["resolution_status"] for item in helpers)
    payload = {
        "schema_version": "social-dev-character-visual-asset-metadata-v1",
        "package": "social-dev",
        "status": "pass",
        "semantic_status": "human_visual_closed_helper_partial_avatar_catalog_boundary",
        "refs": {
            "character_metadata": {"path": "knowledge/fixtures/accepted/runtime/character_metadata_contract.json", "contract_hash": metadata["determinism"]["contract_hash"]},
            "character_capability": {"path": "knowledge/fixtures/accepted/runtime/character_capability_contract.json", "contract_hash": capability["determinism"]["contract_hash"]},
            "character_asset_manifest": {"path": "knowledge/fixtures/accepted/runtime/character_asset_manifest.json", "contract_hash": asset_manifest["determinism"]["contract_hash"]},
            "taxonomy": {"path": "knowledge/fixtures/accepted/asset_family_taxonomy.json", "content_hash": taxonomy["determinism"]["content_hash"]},
            "geometry": {"path": "knowledge/fixtures/accepted/asset_geometry_catalog.json", "content_hash": geometry["determinism"]["content_hash"]},
        },
        "counts": {
            "staff_records": len(staff),
            "staff_image_bindings": sum(1 for item in staff if item["image_selector"]["resolution_status"] == "resolved"),
            "unique_human_images": len(human_images),
            "human_animations": len(human_animations),
            "helper_records": len(helpers),
            "helper_image_statuses": dict(sorted(helper_image_statuses.items())),
            "helper_big_image_statuses": dict(sorted(helper_big_statuses.items())),
            "avatar_body_assets": next(item["asset_count"] for item in packages if item["family_id"] == "character.avatar.body"),
            "avatar_head_assets": next(item["asset_count"] for item in packages if item["family_id"] == "character.avatar.head"),
            "event_visual_assets": next(item["asset_count"] for item in packages if item["family_id"] == "event.visual"),
        },
        "staff": staff,
        "helpers": helpers,
        "human_visuals": {"images": human_images, "animations": human_animations, "runtime_policy": asset_manifest.get("runtime_policy")},
        "capability_profiles": profiles,
        "packages": packages,
        "gaps": [
            {"id": "helper.img.selector_scope", "status": "deferred", "count": helper_image_statuses.get("deferred", 0), "detail": "Helper img_ values 130–140 retain source selector references but require scope/asset resolution."},
            {"id": "helper.bigImg.runtime_promotion", "status": "not_promoted", "count": helper_big_statuses.get("not_promoted", 0), "detail": "Helper bigImg_ selectors are preserved as metadata but no full big-image runtime package is promoted."},
            {"id": "avatar.body.binding", "status": "catalog_only", "count": next(item["asset_count"] for item in packages if item["family_id"] == "character.avatar.body"), "detail": "Avatar body assets are indexed and family-classified; no AvatarData binding contract is active."},
            {"id": "avatar.head.binding", "status": "catalog_only", "count": next(item["asset_count"] for item in packages if item["family_id"] == "character.avatar.head"), "detail": "Avatar head assets are indexed and family-classified; no AvatarData binding contract is active."},
            {"id": "event.actor.scope", "status": "reserved", "count": next(item["asset_count"] for item in packages if item["family_id"] == "event.visual"), "detail": "Event visuals remain separate from the human StaffData runtime profile."},
        ],
        "policy": {
            "staff_lookup": "staff:<native_id> -> image_selector -> human asset id; action lookup uses capability profile and native SEB selector.",
            "helper_lookup": "helper:<native_id> -> image_selector/big_image_selector; unresolved/deferred statuses are returned, not guessed.",
            "avatar_lookup": "No active AvatarData binding; use family asset IDs only until an avatar composition contract closes.",
            "event_lookup": "No active event actor binding; keep event package separate from human/helper actor state.",
        },
    }
    payload["determinism"] = {"algorithm": "stable-json-sha256 excluding determinism.content_hash", "content_hash": sha256_bytes(stable_json(payload).encode("utf-8"))}
    return payload


def build_contract_payload(catalog: dict[str, Any]) -> dict[str, Any]:
    payload = {
        "schema_version": "social-dev-character-visual-asset-metadata-contract-v1",
        "package": "social-dev",
        "status": "pass",
        "semantic_status": "character_visual_metadata_contract_not_full_family_runtime_approval",
        "catalog_path": "knowledge/fixtures/accepted/character_visual_asset_metadata.json",
        "catalog_content_hash": catalog["determinism"]["content_hash"],
        "counts": catalog["counts"],
        "acceptance": {
            "all_staff_records_bound": catalog["counts"]["staff_records"] == 141 and catalog["counts"]["staff_image_bindings"] == 141,
            "human_images_closed": catalog["counts"]["unique_human_images"] == 105,
            "human_animations_closed": catalog["counts"]["human_animations"] == 35,
            "helper_metadata_complete": catalog["counts"]["helper_records"] == 19,
            "helper_visual_gap_explicit": catalog["counts"]["helper_image_statuses"].get("deferred", 0) == 11,
            "avatar_boundary_explicit": catalog["counts"]["avatar_body_assets"] == 284 and catalog["counts"]["avatar_head_assets"] == 509,
            "event_boundary_explicit": True,
        },
        "runtime_policy": {"human_lookup": True, "helper_metadata_lookup": True, "helper_pixel_lookup": False, "avatar_pixel_lookup": False, "event_actor_lookup": False, "next_gate": "usage_lifecycle_placement_runtime_query_contract"},
    }
    payload["determinism"] = {"algorithm": "stable-json-sha256 excluding determinism.content_hash", "content_hash": sha256_bytes(stable_json(payload).encode("utf-8"))}
    return payload


def markdown_report(catalog: dict[str, Any], contract: dict[str, Any]) -> str:
    lines = [
        "# Social Dev character visual asset metadata",
        "",
        "Track H separates the complete human StaffData visual package from partial HelperData visuals and catalog-only Avatar/Event families.",
        "",
        "## Identity",
        "",
        f"- Catalog hash: `{catalog['determinism']['content_hash']}`",
        f"- Contract hash: `{contract['determinism']['content_hash']}`",
        "",
        "## Counts",
        "",
        "| Scope | Count |",
        "|---|---:|",
        f"| StaffData records | {catalog['counts']['staff_records']:,} |",
        f"| Staff image bindings | {catalog['counts']['staff_image_bindings']:,} |",
        f"| Human image assets | {catalog['counts']['unique_human_images']:,} |",
        f"| Human SEB animations | {catalog['counts']['human_animations']:,} |",
        f"| HelperData records | {catalog['counts']['helper_records']:,} |",
        f"| Avatar body asset rows | {catalog['counts']['avatar_body_assets']:,} |",
        f"| Avatar head asset rows | {catalog['counts']['avatar_head_assets']:,} |",
        f"| Event visual asset rows | {catalog['counts']['event_visual_assets']:,} |",
        "",
        "## Helper status",
        "",
        f"- `img_`: `{catalog['counts']['helper_image_statuses']}`.",
        f"- `bigImg_`: `{catalog['counts']['helper_big_image_statuses']}`.",
        "- The 11 helper scope-deferred image references and the unpromoted big-image package remain explicit.",
        "",
        "## Boundary",
        "",
        "- Human StaffData is ready for lazy image/frame lookup and capability-driven action selection.",
        "- HelperData is metadata-ready but not fully pixel-ready.",
        "- Avatar body/head and event visuals are cataloged and classified, but no runtime actor composition is inferred.",
        "",
        "```powershell",
        "python -B tools/social-dev/build_character_visual_asset_metadata.py",
        "python -B tools/social-dev/test_character_visual_asset_metadata.py",
        "```",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    catalog = build_payload()
    contract = build_contract_payload(catalog)
    write_json(CATALOG_PATH, catalog)
    write_json(CONTRACT_PATH, contract)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(markdown_report(catalog, contract), encoding="utf-8", newline="\n")
    print(json.dumps({"catalog_hash": catalog["determinism"]["content_hash"], "staff": catalog["counts"]["staff_records"], "helpers": catalog["counts"]["helper_records"], "human_images": catalog["counts"]["unique_human_images"], "human_animations": catalog["counts"]["human_animations"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
