"""Build the complete source SEB inventory and the Floor00 subset contract.

The source ZIP is immutable evidence.  This builder reads it, decodes every
SEB with :mod:`seb_codec`, and records unsupported members instead of silently
falling back to the old single-layer parser.  The generated inventory belongs
under ``knowledge/fixtures/accepted``; the smaller Floor00 contract belongs
under ``knowledge/fixtures/accepted/runtime``.
"""

from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path
from typing import Any

from seb_codec import SebDecodeError, decode_seb


ROOT = Path(__file__).resolve().parents[2]
ZIP_PATH = ROOT / "sources/raw/Social_Dev_Story_v2.5.1_ASSETS_ONLY_WITH_ASSEMBLY_GUIDE.zip"
KNOWLEDGE_OUTPUT = ROOT / "knowledge/fixtures/accepted/seb_catalog.json"
RUNTIME_OUTPUT = ROOT / "knowledge/fixtures/accepted/runtime/floor00_seb_contract.json"
DEFAULT_MAP_PATH = ROOT / "knowledge/fixtures/accepted/runtime/default_map_chip_contract.json"
NATIVE_SCENE_PATH = ROOT / "knowledge/fixtures/accepted/runtime/native_scene_assembly_contract.json"
ROOM_ASSETS_PATH = ROOT / "knowledge/fixtures/accepted/runtime/room_scene_asset_manifest.json"
DISPLAY_MANIFEST_PATH = ROOT / "knowledge/fixtures/accepted/runtime/display_asset_manifest.json"

ARCHIVE_PREFIX = "Social_Dev_Story_v2.5.1_ASSETS_ONLY/"


def stable_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def normalized_member(member: str) -> str:
    value = member.replace("\\", "/")
    if value.startswith(ARCHIVE_PREFIX):
        return value[len(ARCHIVE_PREFIX) :]
    return value


def archive_sha256() -> str:
    return sha256_bytes(ZIP_PATH.read_bytes())


def probe_header(raw: bytes) -> dict[str, int] | None:
    if len(raw) < 8:
        return None
    return {
        "word_0": int.from_bytes(raw[0:2], "big"),
        "word_1": int.from_bytes(raw[2:4], "big"),
        "word_2": int.from_bytes(raw[4:6], "big"),
        "word_3": int.from_bytes(raw[6:8], "big"),
    }


def make_member_entry(member: str, raw: bytes) -> dict[str, Any]:
    normalized = normalized_member(member)
    entry: dict[str, Any] = {
        "member": normalized,
        "archive_member": member,
        "pack": normalized.split("/", 1)[0] if "/" in normalized else None,
        "bytes": len(raw),
        "sha256": sha256_bytes(raw),
        "header_probe": probe_header(raw),
    }
    try:
        decoded = decode_seb(raw, normalized)
    except (SebDecodeError, ValueError) as error:
        entry.update(
            {
                "status": "unsupported",
                "unsupported_reason": str(error),
            }
        )
    else:
        entry.update(
            {
                "status": "pass",
                "decode": decoded,
            }
        )
    return entry


def _add_member(result: set[str], member: str | None) -> None:
    if not member:
        return
    normalized = normalized_member(member)
    if "/" not in normalized and normalized.lower().endswith(".seb"):
        normalized = f"01_GAME_PACKS/chip/{normalized}"
    if normalized.lower().endswith(".seb"):
        result.add(normalized)


def floor00_member_refs() -> dict[str, list[str]]:
    """Collect SEB references from the verified Floor00 contracts/manifests."""

    default_map = load_json(DEFAULT_MAP_PATH)
    native_scene = load_json(NATIVE_SCENE_PATH)
    room_assets = load_json(ROOM_ASSETS_PATH)
    display_manifest = load_json(DISPLAY_MANIFEST_PATH)

    explicit: set[str] = set()
    related: set[str] = set()

    extension = default_map.get("extension_wall", {})
    _add_member(explicit, f"01_GAME_PACKS/chip/{extension.get('seb_filename')}")

    wall_door = native_scene.get("wall_door_composition", {})
    _add_member(explicit, wall_door.get("wall", {}).get("seb_filename"))
    _add_member(explicit, wall_door.get("door", {}).get("seb_filename"))

    for room in room_assets.get("rooms", []):
        if room.get("room_key") != "room:0":
            continue
        for role in ("wall", "door"):
            filename = room.get("assets", {}).get(role, {}).get("filename")
            _add_member(explicit, f"01_GAME_PACKS/chip/{filename}")

    for item in display_manifest.get("native_initial_objects", {}).values():
        _add_member(explicit, item.get("seb_asset_member"))
        _add_member(explicit, item.get("sub_composition", {}).get("asset_member") if item.get("sub_composition") else None)

    for actor in display_manifest.get("actors", []):
        for animation in actor.get("animations", {}).values():
            _add_member(explicit, f"01_GAME_PACKS/human/{animation.get('filename')}" )

    # These are shipped sibling definitions that the contracts identify as
    # the source variants for the room's wall/door and under-floor rendering.
    # They remain related until a native call site promotes them to a draw.
    for member in (
        "01_GAME_PACKS/chip/wall_01.seb",
        "01_GAME_PACKS/chip/wall_01_new.seb",
        "01_GAME_PACKS/chip/door_02.seb",
        "01_GAME_PACKS/chip/door_03.seb",
        "01_GAME_PACKS/chip/under_floor.seb",
        "01_GAME_PACKS/game/under_floor00.seb",
    ):
        _add_member(related, member)

    return {
        "explicit_contract_refs": sorted(explicit),
        "related_variant_refs": sorted(related - explicit),
    }


def build_catalog() -> tuple[dict[str, Any], dict[str, Any]]:
    refs = floor00_member_refs()
    entries: list[dict[str, Any]] = []
    with zipfile.ZipFile(ZIP_PATH) as archive:
        members = sorted(
            member
            for member in archive.namelist()
            if member.startswith(ARCHIVE_PREFIX)
            and member.lower().endswith(".seb")
        )
        for member in members:
            entries.append(make_member_entry(member, archive.read(member)))

    by_member = {entry["member"]: entry for entry in entries}
    statuses = {status: sum(entry["status"] == status for entry in entries) for status in ("pass", "unsupported")}
    unsupported = [
        {
            "member": entry["member"],
            "bytes": entry["bytes"],
            "sha256": entry["sha256"],
            "header_probe": entry["header_probe"],
            "reason": entry["unsupported_reason"],
        }
        for entry in entries
        if entry["status"] != "pass"
    ]

    floor00_entries: list[dict[str, Any]] = []
    missing_refs: list[str] = []
    for member in refs["explicit_contract_refs"] + refs["related_variant_refs"]:
        entry = by_member.get(member)
        if entry is None:
            missing_refs.append(member)
        else:
            floor00_entries.append(entry)

    default_map = load_json(DEFAULT_MAP_PATH)
    native_scene = load_json(NATIVE_SCENE_PATH)
    room_assets = load_json(ROOM_ASSETS_PATH)
    floor00_default_map = {
        "catalog_id": default_map.get("catalog_id"),
        "scene_ref": default_map.get("scene_ref"),
        "room": default_map.get("room"),
        "native_static_arrays": default_map.get("native_static_arrays"),
        "raw_index_to_selector": default_map.get("raw_index_to_selector"),
        "floor_selector_remap": default_map.get("floor_selector_remap"),
        "extension_wall": default_map.get("extension_wall"),
        "draw_contract": default_map.get("draw_contract"),
        "source_assets": default_map.get("source_assets"),
        "native_wall_door_composition": native_scene.get("wall_door_composition"),
        "room0_asset_resolution": next(
            (room for room in room_assets.get("rooms", []) if room.get("room_key") == "room:0"),
            None,
        ),
    }

    catalog: dict[str, Any] = {
        "schema_version": "social-dev-seb-catalog-v1",
        "package": "Social_Dev_Story_v2.5.1_ASSETS_ONLY",
        "status": "pass" if not missing_refs else "blocked_by_missing_reference",
        "semantic_status": "complete_layered_decode_with_explicit_unsupported_members",
        "source": {
            "zip_path": str(ZIP_PATH.relative_to(ROOT)).replace("\\", "/"),
            "zip_sha256": archive_sha256(),
            "archive_prefix": ARCHIVE_PREFIX,
            "decoder": "tools/social-dev/seb_codec.py",
            "grammar": "seb-layered-v1",
        },
        "counts": {
            "seb_total": len(entries),
            "decoded_pass": statuses["pass"],
            "unsupported": statuses["unsupported"],
            "floor00_explicit_refs": len(refs["explicit_contract_refs"]),
            "floor00_related_refs": len(refs["related_variant_refs"]),
            "floor00_missing_refs": len(missing_refs),
        },
        "unsupported": unsupported,
        "floor00": {
            "explicit_contract_refs": refs["explicit_contract_refs"],
            "related_variant_refs": refs["related_variant_refs"],
            "missing_refs": missing_refs,
            "default_map_metadata": floor00_default_map,
            "assets": floor00_entries,
        },
        "assets": entries,
    }
    content_hash = sha256_bytes(stable_json(catalog).encode("utf-8"))
    catalog["determinism"] = {
        "algorithm": "sha256(canonical_json_without_content_hash)",
        "content_hash": content_hash,
    }

    runtime_contract = {
        "schema_version": "social-dev-floor00-seb-contract-v1",
        "package": "floor00-seb-default-map-composition",
        "status": catalog["status"],
        "semantic_status": "complete_layered_decode_with_explicit_unsupported_members",
        "catalog_id": "floor00-seb-default-map-composition",
        "source_catalog": "knowledge/fixtures/accepted/seb_catalog.json",
        "source_zip_sha256": catalog["source"]["zip_sha256"],
        "decoder": catalog["source"]["decoder"],
        "counts": {
            "explicit_assets": len(refs["explicit_contract_refs"]),
            "related_assets": len(refs["related_variant_refs"]),
            "unsupported_source_sebs": len(unsupported),
        },
        "unsupported_source_sebs": unsupported,
        "default_map_metadata": floor00_default_map,
        "explicit_assets": [
            {
                "member": entry["member"],
                "bytes": entry["bytes"],
                "sha256": entry["sha256"],
                "status": entry["status"],
                "decode": entry.get("decode"),
                "unsupported_reason": entry.get("unsupported_reason"),
            }
            for entry in floor00_entries
            if entry["member"] in refs["explicit_contract_refs"]
        ],
        "related_variant_assets": [
            {
                "member": entry["member"],
                "bytes": entry["bytes"],
                "sha256": entry["sha256"],
                "status": entry["status"],
                "decode": entry.get("decode"),
                "unsupported_reason": entry.get("unsupported_reason"),
            }
            for entry in floor00_entries
            if entry["member"] in refs["related_variant_refs"]
        ],
    }
    runtime_contract["determinism"] = {
        "algorithm": "sha256(canonical_json_without_content_hash)",
        "content_hash": sha256_bytes(stable_json(runtime_contract).encode("utf-8")),
    }
    return catalog, runtime_contract


def write_outputs() -> None:
    catalog, runtime_contract = build_catalog()
    KNOWLEDGE_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    RUNTIME_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    KNOWLEDGE_OUTPUT.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    RUNTIME_OUTPUT.write_text(json.dumps(runtime_contract, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "catalog": str(KNOWLEDGE_OUTPUT.relative_to(ROOT)).replace("\\", "/"),
                "runtime_contract": str(RUNTIME_OUTPUT.relative_to(ROOT)).replace("\\", "/"),
                "counts": catalog["counts"],
                "unsupported": catalog["unsupported"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    write_outputs()
