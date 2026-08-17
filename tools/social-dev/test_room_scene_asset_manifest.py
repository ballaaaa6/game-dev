"""Deterministic checks for the all-room selector PNG promotion boundary."""

from __future__ import annotations

import json
from pathlib import Path

import build_room_scene_asset_manifest as builder


ROOT = builder.ROOT


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def without_dynamic(value):
    if isinstance(value, dict):
        return {
            key: without_dynamic(item)
            for key, item in value.items()
            if key not in {"generated_at_utc", "content_hash"}
        }
    if isinstance(value, list):
        return [without_dynamic(item) for item in value]
    return value


def main() -> int:
    path = ROOT / "knowledge/fixtures/accepted/runtime/room_scene_asset_manifest.json"
    manifest = load(path)
    rebuilt = builder.build()
    assert manifest["status"] == "pass"
    assert manifest["semantic_status"] == "approved_for_runtime_contract"
    assert manifest["counts"] == {
        "rooms": 18,
        "unique_selector_pngs": 23,
        "floor_pngs": 10,
        "wall_pngs": 7,
        "door_pngs": 6,
    }
    assert len(manifest["rooms"]) == 18
    assert all(set(room["assets"]) == {"floor", "wall", "door"} for room in manifest["rooms"])
    assert manifest["runtime_policy"]["native_coordinate_composition_not_implied"] is True
    for asset in manifest["assets"]:
        runtime_path = ROOT / "runtime/social-dev" / asset["runtime_path"]
        assert runtime_path.is_file(), runtime_path
        assert builder.sha256(runtime_path.read_bytes()) == asset["sha256"]
    assert without_dynamic(manifest) == without_dynamic(rebuilt)
    assert not list((ROOT / "runtime/social-dev").rglob("*.cs"))
    print(
        "room_scene_asset_manifest_test_passed "
        f"rooms={manifest['counts']['rooms']} assets={manifest['counts']['unique_selector_pngs']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
