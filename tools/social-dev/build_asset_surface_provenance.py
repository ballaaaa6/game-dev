"""Build the explicit surface-family and source-provenance closure package.

Track X/A covers the catalog families that are not actor or world-placement
records: UI, event/effect, localization, configuration, data, system, and
platform surfaces.  The package closes what the current evidence proves and
keeps screen/event consumer gaps as named boundaries instead of inferring
usage from filenames.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "knowledge/fixtures/accepted"
RUNTIME_EVIDENCE = ROOT / "knowledge/fixtures/accepted/runtime"

TAXONOMY_PATH = EVIDENCE / "asset_family_taxonomy.json"
USAGE_PATH = EVIDENCE / "asset_usage_lifecycle_placement_matrix.json"
SELECTOR_PATH = EVIDENCE / "asset_selector_usage_matrix.json"
VALIDATION_PATH = EVIDENCE / "asset_validation_gate.json"
BINARY_INVENTORY_PATH = EVIDENCE / "asset_binary_inventory.json"

SURFACE_PATH = EVIDENCE / "asset_surface_provenance.json"
CONTRACT_PATH = RUNTIME_EVIDENCE / "asset_surface_provenance_contract.json"
REPORT_PATH = ROOT / "docs/reports/social-dev_asset_surface_provenance.md"


def stable_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def boundary_for_family(family_id: str) -> tuple[str, str, str]:
    if family_id.startswith("ui."):
        return (
            "ui_surface_cataloged_no_closed_screen_consumer_contract",
            "catalog_only_until_screen_consumer_contract",
            "Screen route, render call, layer order, and timing must be supplied before runtime promotion.",
        )
    if family_id in {"effect.visual", "event.visual"}:
        return (
            "event_visual_cataloged_no_closed_event_consumer_contract",
            "catalog_only_until_event_consumer_contract",
            "Event trigger, consumer, timing, and placement must be supplied before runtime promotion.",
        )
    if family_id == "text.localization":
        return (
            "localization_cataloged_no_closed_text_consumer_contract",
            "catalog_only_until_text_consumer_contract",
            "Locale selection and text consumer mapping remain source/data evidence, not inferred from filenames.",
        )
    if family_id in {"config.connection", "data.table", "data.unity_textasset", "system.game", "platform.android"}:
        return (
            "support_family_cataloged_provenance_only",
            "provenance_only_until_runtime_consumer_contract",
            "The payload is retained for identity/provenance and is not promoted as a drawable runtime asset.",
        )
    if family_id.startswith("character."):
        return (
            "character_family_closed_by_track_h",
            "use_character_metadata_contract",
            "Character visual promotion is governed by the human/helper/avatar capability contracts.",
        )
    if family_id.startswith("world."):
        return (
            "world_family_closed_by_track_w_and_scene_contracts",
            "use_world_and_scene_contracts",
            "World placement and composition are governed by furniture, room, and native scene contracts.",
        )
    return (
        "catalog_boundary_explicit",
        "catalog_only_until_consumer_contract",
        "No runtime promotion is permitted without an explicit consumer contract.",
    )


def build_payload() -> dict[str, Any]:
    taxonomy = load_json(TAXONOMY_PATH)
    usage = load_json(USAGE_PATH)
    selectors = load_json(SELECTOR_PATH)
    validation = load_json(VALIDATION_PATH)
    binary_inventory = load_json(BINARY_INVENTORY_PATH)

    taxonomy_by_family: dict[str, list[dict[str, Any]]] = {}
    for row in taxonomy["assets"]:
        taxonomy_by_family.setdefault(row["family_id"], []).append(row)
    usage_by_family = {row["family_id"]: row for row in usage["families"]}
    non_actor_ids = {row["family_id"] for row in usage["non_actor_families"]}
    validation_by_path = {row["relative_path"]: row for row in validation["rows"]}

    family_rows = []
    for family in taxonomy["families"]:
        family_id = family["family_id"]
        rows = taxonomy_by_family[family_id]
        usage_row = usage_by_family[family_id]
        boundary_status, promotion_policy, boundary_reason = boundary_for_family(family_id)
        zip_statuses = Counter()
        apk_statuses = Counter()
        for row in rows:
            source = validation_by_path.get(row["relative_path"])
            if source:
                zip_statuses[source.get("zip_status", "missing_validation_row")] += 1
                apk_statuses[source.get("apk_source_status", "missing_validation_row")] += 1
            else:
                zip_statuses["missing_validation_row"] += 1
                apk_statuses["missing_validation_row"] += 1
        family_rows.append(
            {
                "family_id": family_id,
                "category": family["category"],
                "purpose": family["purpose"],
                "asset_count": family["row_count"],
                "non_actor_surface": family_id in non_actor_ids,
                "boundary_status": boundary_status,
                "promotion_policy": promotion_policy,
                "boundary_reason": boundary_reason,
                "runtime_referenced_count": family["runtime_referenced_count"],
                "selector_target_asset_count": sum(1 for row in usage["assets"] if row["family_id"] == family_id and row["selector_keys"]),
                "data_relation_count": sum(row["data_relation_count"] for row in usage["assets"] if row["family_id"] == family_id),
                "usage_statuses": usage_row["usage_statuses"],
                "lifecycle_statuses": usage_row["lifecycle_statuses"],
                "placement_statuses": usage_row["placement_statuses"],
                "runtime_query_statuses": usage_row["runtime_query_statuses"],
                "source_statuses": {
                    "zip": dict(sorted(zip_statuses.items())),
                    "apk": dict(sorted(apk_statuses.items())),
                },
                "runtime_policy": "do_not_promote_without_screen_or_event_consumer_contract" if family_id in non_actor_ids else promotion_policy,
            }
        )

    unity_rows = [row for row in taxonomy["assets"] if row["family_id"] == "data.unity_textasset"]
    unity_paths = sorted(row["relative_path"] for row in unity_rows)
    unity_validation_rows = [validation_by_path[path] for path in unity_paths if path in validation_by_path]
    unity_apk_missing = sorted(row["relative_path"] for row in unity_validation_rows if row.get("apk_source_status") == "apk_entry_missing")

    unresolved_selectors = [
        {
            "selector_key": row.get("selector_key"),
            "resource_scope": row.get("resource_scope"),
            "selector_kind": row.get("selector_kind"),
            "selector_id": row.get("selector_id"),
            "source_file": row.get("source_file"),
            "source_row": row.get("source_row"),
            "raw_line": row.get("raw_line"),
            "status": row.get("status"),
            "coverage_status": row.get("coverage_status"),
        }
        for row in selectors["selectors"]
        if row.get("status") == "unresolved_target"
    ]

    binary_sources = {}
    for name, archive in sorted(binary_inventory.get("archives", {}).items()):
        binary_sources[name] = {
            "path": archive.get("path"),
            "bytes": archive.get("bytes"),
            "sha256": archive.get("sha256"),
            "members": archive.get("members"),
            "total_uncompressed_bytes": archive.get("total_uncompressed_bytes"),
            "top_level_groups": archive.get("top_level_groups", {}),
        }

    family_rows = sorted(family_rows, key=lambda row: row["family_id"])
    non_actor_assets = sum(row["asset_count"] for row in family_rows if row["non_actor_surface"])
    apk_statuses = Counter(row.get("apk_source_status", "missing_validation_row") for row in validation["rows"])
    zip_statuses = Counter(row.get("zip_status", "missing_validation_row") for row in validation["rows"])
    roundtrip_exact = int(validation.get("roundtrip_exact_counts", {}).get("True", 0))

    payload = {
        "schema_version": "social-dev-asset-surface-provenance-v1",
        "package": "social-dev",
        "status": "pass",
        "semantic_status": "surface_provenance_boundary_closed_with_explicit_runtime_promotion_gates",
        "refs": {
            "taxonomy": {"path": "knowledge/fixtures/accepted/asset_family_taxonomy.json", "content_hash": taxonomy["determinism"]["content_hash"]},
            "usage_matrix": {"path": "knowledge/fixtures/accepted/asset_usage_lifecycle_placement_matrix.json", "content_hash": usage["determinism"]["content_hash"]},
            "selector_matrix": {"path": "knowledge/fixtures/accepted/asset_selector_usage_matrix.json", "content_hash": selectors["determinism"]["content_hash"]},
            "asset_validation_gate": {"path": "knowledge/fixtures/accepted/asset_validation_gate.json", "content_hash": sha256_bytes(stable_json(validation).encode("utf-8"))},
            "binary_inventory": {"path": "knowledge/fixtures/accepted/asset_binary_inventory.json", "content_hash": sha256_bytes(stable_json(binary_inventory).encode("utf-8"))},
        },
        "counts": {
            "indexed_assets": len(taxonomy["assets"]),
            "families": len(family_rows),
            "non_actor_families": len(non_actor_ids),
            "non_actor_assets": non_actor_assets,
            "zip_exact_assets": zip_statuses.get("zip_exact", 0),
            "apk_entry_present_assets": apk_statuses.get("apk_entry_present", 0),
            "apk_entry_missing_assets": apk_statuses.get("apk_entry_missing", 0),
            "pack_roundtrip_exact_rows": roundtrip_exact,
            "unity_textasset_assets": len(unity_rows),
            "unity_textasset_apk_missing_assets": len(unity_apk_missing),
            "unresolved_selectors": len(unresolved_selectors),
        },
        "families": family_rows,
        "source_provenance": {
            "asset_validation_status": validation.get("status"),
            "asset_validation": {
                "asset_index_count": validation.get("asset_index_count"),
                "pack_source_map_count": validation.get("pack_source_map_count"),
                "zip_status_counts": validation.get("zip_status_counts", {}),
                "apk_source_status_counts": validation.get("apk_source_status_counts", {}),
                "roundtrip_exact_counts": validation.get("roundtrip_exact_counts", {}),
                "source_fingerprint": validation.get("source_fingerprint", {}),
            },
            "binary_sources": binary_sources,
            "unity_textasset_boundary": {
                "asset_count": len(unity_rows),
                "asset_ids": sorted(row["asset_id"] for row in unity_rows),
                "relative_paths": unity_paths,
                "apk_entry_missing_count": len(unity_apk_missing),
                "apk_entry_missing_paths": unity_apk_missing,
                "status": "source_hash_or_nested_unity_mapping_not_closed",
                "runtime_policy": "retain_as_provenance_only; do_not_promote_or_decode_by_guessing",
            },
            "selector_identity_boundary": {
                "unresolved_count": len(unresolved_selectors),
                "rows": unresolved_selectors,
                "runtime_policy": "return_explicit_unresolved_identity; do_not_guess_filename_or_selector_id",
            },
            "identity_policy": "ZIP-relative identity, source hashes, APK presence, and nested Unity provenance are recorded independently; one source status never upgrades another.",
        },
        "closure": {
            "all_indexed_assets_have_structural_family": len(taxonomy["assets"]) == 3542 and all(row["family_id"] for row in taxonomy["assets"]),
            "all_non_actor_families_have_explicit_boundary": len(non_actor_ids) == 21 and all(row["boundary_status"] for row in family_rows if row["non_actor_surface"]),
            "zip_identity_closed": validation.get("asset_index_count") == 3542 and validation.get("zip_status_counts", {}).get("zip_exact") == 3542,
            "apk_presence_classified": validation.get("apk_source_status_counts", {}).get("apk_entry_present") == 3508 and validation.get("apk_source_status_counts", {}).get("apk_entry_missing") == 34,
            "pack_roundtrip_evidence_closed": validation.get("pack_source_map_count") == 25 and validation.get("roundtrip_exact_counts", {}).get("True") == 25,
            "unity_textasset_gap_explicit": len(unity_rows) == 34 and len(unity_apk_missing) == 34,
            "unresolved_selector_gap_explicit": len(unresolved_selectors) == 1,
            "runtime_promotion_requires_consumer_contract": all(row["runtime_policy"] == "do_not_promote_without_screen_or_event_consumer_contract" for row in family_rows if row["non_actor_surface"]),
        },
        "open_boundaries": [
            "21 non-actor families have complete catalog/provenance boundaries but no invented screen or event consumer contract.",
            "34 Unity TextAsset/resource rows are retained with APK absence and unresolved nested mapping; they are not runtime-promoted.",
            "1 lineup_layout/bg.seb selector has unresolved target identity and returns an explicit unresolved status.",
        ],
        "runtime_policy": {
            "source_archive_imports": False,
            "source_code_imports": False,
            "screen_event_usage_inference": False,
            "filename_identity_inference": False,
            "catalog_and_provenance_lookup_allowed": True,
        },
    }
    payload["determinism"] = {"algorithm": "stable-json-sha256 excluding determinism.content_hash", "content_hash": sha256_bytes(stable_json(payload).encode("utf-8"))}
    return payload


def build_contract_payload(surface: dict[str, Any]) -> dict[str, Any]:
    payload = {
        "schema_version": "social-dev-asset-surface-provenance-contract-v1",
        "package": "social-dev",
        "status": "pass",
        "semantic_status": "approved_for_provenance_boundary_and_catalog_query",
        "surface_path": "knowledge/fixtures/accepted/asset_surface_provenance.json",
        "surface_content_hash": surface["determinism"]["content_hash"],
        "counts": surface["counts"],
        "acceptance": surface["closure"],
        "runtime_policy": surface["runtime_policy"],
        "query_surface": ["family_id", "asset_id", "relative_path", "selector_key", "source_hash", "apk_presence_status"],
    }
    payload["determinism"] = {"algorithm": "stable-json-sha256 excluding determinism.content_hash", "content_hash": sha256_bytes(stable_json(payload).encode("utf-8"))}
    return payload


def markdown_report(surface: dict[str, Any], contract: dict[str, Any]) -> str:
    lines = [
        "# Social Dev asset surface and provenance closure",
        "",
        "Track X/A closes the metadata boundary for UI, event/effect, localization, configuration, data, system, and platform families. It records what the source package proves and refuses to invent screen/event call sites from filenames.",
        "",
        "## Identity",
        "",
        f"- Surface package hash: `{surface['determinism']['content_hash']}`",
        f"- Runtime contract hash: `{contract['determinism']['content_hash']}`",
        "",
        "## Counts",
        "",
        "| Dimension | Count |",
        "|---|---:|",
        f"| Indexed assets | {surface['counts']['indexed_assets']:,} |",
        f"| Structural families | {surface['counts']['families']:,} |",
        f"| Non-actor families with explicit boundary | {surface['counts']['non_actor_families']:,} |",
        f"| Non-actor assets | {surface['counts']['non_actor_assets']:,} |",
        f"| ZIP-exact assets | {surface['counts']['zip_exact_assets']:,} |",
        f"| APK entries present | {surface['counts']['apk_entry_present_assets']:,} |",
        f"| APK entries missing | {surface['counts']['apk_entry_missing_assets']:,} |",
        f"| Exact pack round-trips | {surface['counts']['pack_roundtrip_exact_rows']:,} |",
        f"| Unity TextAsset rows | {surface['counts']['unity_textasset_assets']:,} |",
        f"| Unity TextAsset rows with APK gap | {surface['counts']['unity_textasset_apk_missing_assets']:,} |",
        f"| Unresolved selector identities | {surface['counts']['unresolved_selectors']:,} |",
        "",
        "## Surface policy",
        "",
        "| Family boundary | Rows | Runtime policy |",
        "|---|---:|---|",
    ]
    for family in surface["families"]:
        if not family["non_actor_surface"]:
            continue
        lines.append(f"| `{family['family_id']}` — {family['boundary_status']} | {family['asset_count']:,} | `{family['promotion_policy']}` |")
    lines.extend(
        [
            "",
            "## Explicit gaps",
            "",
            "- The 34 Unity TextAsset/resource rows are retained by asset ID and ZIP-relative path, but their APK entry/nested Unity mapping is not closed. They remain provenance-only.",
            "- `lineup_layout/bg.seb` remains one unresolved selector identity. The runtime must return an unresolved status rather than guess a filename or selector ID.",
            "- The 21 non-actor families are cataloged and traceable, but screen/event consumer timing, layer order, and placement are not fabricated. A future screen contract can promote a family deliberately.",
            "",
            "## Verification",
            "",
            "```powershell",
            "python -B tools/social-dev/build_asset_surface_provenance.py",
            "python -B tools/social-dev/test_asset_surface_provenance.py",
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    surface = build_payload()
    contract = build_contract_payload(surface)
    write_json(SURFACE_PATH, surface)
    write_json(CONTRACT_PATH, contract)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(markdown_report(surface, contract), encoding="utf-8", newline="\n")
    print(json.dumps({"surface_hash": surface["determinism"]["content_hash"], "assets": surface["counts"]["indexed_assets"], "non_actor_families": surface["counts"]["non_actor_families"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
