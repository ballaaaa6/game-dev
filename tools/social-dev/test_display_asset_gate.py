"""Deterministic checks for the bounded Social Dev display asset gate."""

from __future__ import annotations

import json
from pathlib import Path

import build_display_asset_gate as builder


ROOT = builder.ROOT
EVIDENCE = ROOT / "knowledge/fixtures/accepted"
RUNTIME_EVIDENCE = ROOT / "knowledge/fixtures/accepted/runtime"


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
    gate_path = EVIDENCE / "display_asset_gate.json"
    manifest_path = RUNTIME_EVIDENCE / "display_asset_manifest.json"
    gate = load(gate_path)
    manifest = load(manifest_path)
    rebuilt_gate, rebuilt_manifest, validation = builder.build_package()

    assert gate["schema_version"] == "social-dev-display-asset-gate-v1"
    assert gate["status"] == "pass"
    assert gate["semantic_status"] == "approved_for_runtime_subset"
    assert gate["phase3a"] == {
        "target": "furniture:2",
        "status": "approved",
        "reason_code": "chair_00_opt_variable_piece_reconstruction_verified",
        "runtime_promotion": "approved",
    }
    assert gate["counts"] == {
        "entries": 18,
        "approved": 18,
        "blocked": 0,
        "by_status": {"approved_for_runtime_subset": 18},
        "promoted_binary_assets": 34,
    }
    assert validation["status"] == "pass"
    assert validation["failed_checks"] == []
    assert validation["counts"]["passed_checks"] == validation["counts"]["checks"] == 10

    entries = {entry["id"]: entry for entry in gate["entries"]}
    assert all(entries[f"actor-sprite:{source_id}"]["status"] == "approved_for_runtime_subset" for source_id in range(5))
    assert entries["human-animation:wait:direction-0"]["source"]["selector_id"] == 10
    assert entries["human-animation:typing:direction-0"]["source"]["selector_id"] == 23
    assert entries["object-frame:furniture:0"]["status"] == "approved_for_runtime_subset"
    assert entries["object-frame:furniture:0"]["source"]["composition_issues"] == []
    assert entries["object-frame:furniture:0"]["source"]["records"][0]["source_asset_member"] == "big_base00.png"
    assert entries["object-frame:furniture:1"]["status"] == "approved_for_runtime_subset"
    assert all(record["source_status"] == "pass_opt_logical" for record in entries["object-frame:furniture:1"]["source"]["records"])
    assert entries["object-frame:furniture:1"]["source"]["source_compositions"][0]["opt_status"] == "pass"
    assert entries["object-frame:furniture:2"]["status"] == "approved_for_runtime_subset"
    assert entries["object-frame:furniture:2"]["source"]["phase3a_closure"]["status"] == "approved"
    assert entries["object-frame:furniture:2"]["source"]["sub_composition"]["source_compositions"][0]["opt_status"] == "pass"
    assert entries["object-frame:furniture:5"]["status"] == "approved_for_runtime_subset"
    assert entries["object-frame:furniture:5"]["source"]["sub_composition"]["filename"] == "chair_02.seb"
    assert entries["object-frame:furniture:5"]["source"]["sub_composition"]["source_compositions"][0]["opt_status"] == "pass"
    assert entries["native-initial-frame:furniture:3"]["source"]["display_mode"] == "native_selector_composition"
    assert entries["native-initial-frame:furniture:3"]["source"]["img_selector_id"] == 148
    assert entries["native-initial-frame:furniture:12"]["source"]["display_mode"] == "native_type1_direct_img"
    assert entries["native-initial-frame:furniture:12"]["source"]["records"][0]["source_status"] == "pass_native_img_asset"
    assert entries["native-initial-frame:furniture:26"]["source"]["records"][0]["source_asset_member"] == "01_GAME_PACKS/chip/old_printer.png"
    assert entries["native-initial-frame:furniture:56"]["source"]["records"][0]["source_asset_member"] == "01_GAME_PACKS/chip/calendar.png"
    assert entries["scene:room:0/floor"]["status"] == "approved_for_runtime_subset"
    assert entries["scene:room:0/floor"]["filename"] == "floor_09.png"
    assert entries["scene:room:0/floor"]["image_id"] == 5
    assert entries["scene:room:0/floor"]["fallback_selector_id"] == 85
    assert entries["scene:room:0/floor"]["source_resolution_status"] == "unresolved"
    assert entries["scene:room:0/wall"]["filename"] == "wall_00.png"
    assert entries["scene:room:0/wall"]["status"] == "approved_for_runtime_subset"
    assert entries["scene:room:0/wall"]["native_coordinate_composition"]["status"] == "verified_native_coordinate_composition"
    assert entries["scene:room:0/door"]["filename"] == "door_01.png"
    assert entries["scene:room:0/door"]["status"] == "approved_for_runtime_subset"
    assert entries["scene:room:0/door"]["native_coordinate_composition"]["cell"] == [8, 4]

    assert manifest["status"] == "pass"
    assert manifest["semantic_status"] == "approved_for_runtime_subset"
    assert manifest["scope"] == "actor-frame-subset-proven-chip-compositions-native-wall-door-composition-and-explicit-floor-fallback"
    assert manifest["phase3a"] == {
        "target": "furniture:2",
        "status": "approved",
        "reason_code": "chair_00_opt_variable_piece_reconstruction_verified",
        "runtime_promotion": "approved",
        "closure_path": "knowledge/fixtures/accepted/phase3a_asset_composition_closure.json",
    }
    assert set(asset["asset_member"] for asset in manifest["assets"]) == {
        "01_GAME_PACKS/chip/big_base00.png",
        "01_GAME_PACKS/chip/big_base00.seb",
        "01_GAME_PACKS/chip/chair_02.opt",
        "01_GAME_PACKS/chip/chair_02.png",
        "01_GAME_PACKS/chip/chair_02.seb",
        "01_GAME_PACKS/chip/chair_00.opt",
        "01_GAME_PACKS/chip/chair_00.png",
        "01_GAME_PACKS/chip/chair_00.seb",
        "01_GAME_PACKS/chip/desk_00.opt",
        "01_GAME_PACKS/chip/desk_00.png",
        "01_GAME_PACKS/chip/desk_00.seb",
        "01_GAME_PACKS/chip/floor_09.png",
        "01_GAME_PACKS/chip/door_02.opt",
        "01_GAME_PACKS/chip/door_02.png",
        "01_GAME_PACKS/chip/door_03.seb",
        "01_GAME_PACKS/human/chara86.png",
        "01_GAME_PACKS/human/chara87.png",
        "01_GAME_PACKS/human/chara88.png",
        "01_GAME_PACKS/human/chara89.png",
        "01_GAME_PACKS/human/chara90.png",
        "01_GAME_PACKS/human/typing_right.seb",
        "01_GAME_PACKS/human/wait_right.seb",
        "01_GAME_PACKS/chip/wall_00.png",
        "01_GAME_PACKS/chip/wall_00.seb",
        "01_GAME_PACKS/chip/door_01.png",
        "01_GAME_PACKS/chip/door_02.seb",
        "01_GAME_PACKS/chip/equip.seb",
        "01_GAME_PACKS/chip/garbage_can.png",
        "01_GAME_PACKS/chip/old_printer.png",
        "01_GAME_PACKS/chip/calendar.png",
        "02_DERIVED_READY_IMAGES/opt_reconstructed/chip/chair_00.png",
        "02_DERIVED_READY_IMAGES/opt_reconstructed/chip/chair_02.png",
        "02_DERIVED_READY_IMAGES/opt_reconstructed/chip/desk_00.png",
        "02_DERIVED_READY_IMAGES/opt_reconstructed/chip/door_02.png",
    }
    assert any("desk_00.opt" in asset["asset_member"] for asset in manifest["assets"])
    assert any("door_03.seb" in asset["asset_member"] for asset in manifest["assets"])
    assert len(manifest["actors"]) == 5
    assert sorted(manifest["native_initial_objects"]) == ["furniture:12", "furniture:26", "furniture:3", "furniture:56"]
    assert [actor["image_selector_id"] for actor in manifest["actors"]] == [86, 87, 88, 89, 90]
    assert all(actor["animations"]["wait"]["records"][0]["source_status"] == "pass" for actor in manifest["actors"])
    assert all(actor["animations"]["typing"]["records"][0]["source_status"] == "pass" for actor in manifest["actors"])

    for asset in manifest["assets"]:
        path = ROOT / "runtime/social-dev" / asset["runtime_path"]
        assert path.is_file(), path
        assert path.read_bytes() and builder.sha256_file(path) == asset["sha256"]

    assert without_dynamic(gate) == without_dynamic(rebuilt_gate)
    assert without_dynamic(manifest) == without_dynamic(rebuilt_manifest)
    assert (ROOT / "runtime/social-dev/assets/display-slice-01/01_GAME_PACKS/chip/desk_00.png").exists()
    assert (ROOT / "runtime/social-dev/assets/display-slice-01/01_GAME_PACKS/chip/floor_09.png").exists()
    assert (ROOT / "runtime/social-dev/assets/display-slice-01/01_GAME_PACKS/chip/chair_00.png").exists()
    assert not list((ROOT / "runtime/social-dev").rglob("*.cs"))

    print(
        "display_asset_gate_test_passed "
        f"checks={validation['counts']['passed_checks']} "
        f"approved={gate['counts']['approved']} "
        f"blocked={gate['counts']['blocked']} "
        f"promoted={gate['counts']['promoted_binary_assets']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
