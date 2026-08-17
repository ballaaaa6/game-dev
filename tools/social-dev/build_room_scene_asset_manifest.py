"""Promote the exact room selector PNGs used by every verified RoomData row."""

from __future__ import annotations

import hashlib
import io
import json
import zipfile
from pathlib import Path
from typing import Any

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
ROOM_CATALOG = ROOT / "knowledge/fixtures/accepted/room_catalog_full.json"
ASSET_INDEX = ROOT / "knowledge/sources/asset_guide_20260813/00_INDEX/ASSET_INDEX.json"
ZIP_PATH = ROOT / "sources/raw/Social_Dev_Story_v2.5.1_ASSETS_ONLY_WITH_ASSEMBLY_GUIDE.zip"
OUTPUT = ROOT / "knowledge/fixtures/accepted/runtime/room_scene_asset_manifest.json"
ASSET_ROOT = ROOT / "runtime/social-dev/assets/room-scene"
ARCHIVE_PREFIX = "Social_Dev_Story_v2.5.1_ASSETS_ONLY/"


def stable_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def content_hash(value: Any) -> str:
    return sha256(stable_json(value).encode("utf-8"))


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def image_dimensions(raw: bytes, member: str) -> tuple[int, int, str]:
    try:
        with Image.open(io.BytesIO(raw)) as image:
            image.load()
            return image.width, image.height, image.mode
    except Exception as error:
        raise ValueError(f"Cannot decode room selector PNG {member}: {error}") from error


def build() -> dict[str, Any]:
    catalog = load(ROOM_CATALOG)
    index = {str(item["relative_path"]).replace("\\", "/"): item for item in load(ASSET_INDEX)}
    roles = ("floor", "wall", "door")
    filenames_by_role: dict[str, set[str]] = {role: set() for role in roles}
    for room in catalog["rooms"]:
        for role in roles:
            filename = room["selectors"][role].get("target_filename")
            if not filename:
                raise ValueError(f"Room {room['room_key']} has no {role} target filename")
            filenames_by_role[role].add(str(filename))

    descriptors: dict[str, dict[str, Any]] = {}
    with zipfile.ZipFile(ZIP_PATH) as archive:
        for role in roles:
            for filename in sorted(filenames_by_role[role]):
                member = f"01_GAME_PACKS/chip/{filename}"
                index_entry = index.get(member)
                if index_entry is None:
                    raise ValueError(f"Asset index is missing room selector {member}")
                raw = archive.read(ARCHIVE_PREFIX + member)
                actual_hash = sha256(raw)
                if actual_hash != str(index_entry["sha256"]).lower():
                    raise ValueError(f"Room selector hash drift for {member}")
                width, height, mode = image_dimensions(raw, member)
                runtime_path = f"assets/room-scene/{member}"
                destination = ROOT / "runtime/social-dev" / runtime_path
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(raw)
                if sha256(destination.read_bytes()) != actual_hash:
                    raise ValueError(f"Promoted room selector hash drift for {destination}")
                descriptors[filename] = {
                    "asset_id": f"asset:{member}",
                    "asset_member": member,
                    "runtime_path": runtime_path,
                    "kind": "room_selector_asset",
                    "pack": "chip",
                    "semantic_role": f"RoomData {role} selector PNG",
                    "original_name": filename,
                    "extension": ".png",
                    "bytes": len(raw),
                    "sha256": actual_hash,
                    "width": width,
                    "height": height,
                    "mode": mode,
                }

    rooms: list[dict[str, Any]] = []
    for room in catalog["rooms"]:
        bindings: dict[str, dict[str, Any]] = {}
        for role in roles:
            selector = room["selectors"][role]
            filename = str(selector["target_filename"])
            descriptor = descriptors[filename]
            bindings[role] = {
                "raw_selector_id": selector["native_id"],
                "native_selector_id": selector.get("native_selector_id"),
                "filename": filename,
                "asset_id": descriptor["asset_id"],
                "runtime_status": "pass_promoted_room_selector_asset",
                "source_status": selector["status"],
            }
        rooms.append({"room_key": room["room_key"], "assets": bindings})

    body = {
        "schema_version": "social-dev-room-scene-asset-manifest-v1",
        "package": "social-dev-room-scene-assets",
        "status": "pass",
        "semantic_status": "approved_for_runtime_contract",
        "catalog_ref": {
            "path": "knowledge/fixtures/accepted/room_catalog_full.json",
            "content_hash": catalog["content_hash"],
        },
        "scope": "all exact RoomData floor/wall/door selector PNGs",
        "assets": [descriptors[filename] for filename in sorted(descriptors)],
        "rooms": rooms,
        "counts": {
            "rooms": len(rooms),
            "unique_selector_pngs": len(descriptors),
            "floor_pngs": len(filenames_by_role["floor"]),
            "wall_pngs": len(filenames_by_role["wall"]),
            "door_pngs": len(filenames_by_role["door"]),
        },
        "runtime_policy": {
            "source_code_imports": False,
            "archive_imports": False,
            "exact_selector_identity_preserved": True,
            "native_coordinate_composition_not_implied": True,
        },
    }
    return {**body, "determinism": {"algorithm": "stable-json-sha256", "content_hash": content_hash(body)}}


def main() -> None:
    result = build()
    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": result["status"], "rooms": result["counts"]["rooms"], "assets": result["counts"]["unique_selector_pngs"], "content_hash": result["determinism"]["content_hash"]}))


if __name__ == "__main__":
    main()
