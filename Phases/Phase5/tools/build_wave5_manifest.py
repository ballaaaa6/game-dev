"""Build the Phase 5 source/artifact manifest without touching frozen roots."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--output", type=Path, default=Path("Phases/Phase5/artifacts/wave5_build_manifest.json"))
    args = parser.parse_args()
    paths = [
        Path("Phases/Phase4/artifacts/wave2_minimum_scene_fixture.json"),
        Path("Phases/Phase4/artifacts/wave2_furniture_contract.json"),
        Path("Phases/Phase4/artifacts/wave2_draw_order_contract.json"),
        Path("Phases/Phase4/artifacts/wave2_wave3_movement_interface.json"),
        Path("Phases/Phase4/artifacts/wave3_actor_e2e_fixture.json"),
        Path("Phases/Phase4/artifacts/wave4_locale_contract.json"),
        Path("Phases/Phase4/artifacts/wave4_talk_contract.json"),
        Path("Phases/Phase4/artifacts/wave4_bubble_contract.json"),
        Path("Phases/Phase4/artifacts/wave4_notification_contract.json"),
        Path("Phases/Phase4/artifacts/wave4_event_contract.json"),
        Path("Phases/Phase2/artifacts/bodyface_analysis.json"),
        Path("game-dev-story-mod_Sprites/office/floor0.png"),
        Path("game-dev-story-mod_Sprites/office/floor0.seb"),
        Path("game-dev-story-mod_Sprites/office/reception_000.png"),
        Path("game-dev-story-mod_Sprites/office/desk_000.png"),
        Path("game-dev-story-mod_Sprites/office/chair_000.png"),
        Path("Phases/Phase5/runtime/runtime.js"),
        Path("Phases/Phase5/runtime/app.js"),
        Path("Phases/Phase5/runtime/data/room_manifest.json"),
        Path("Phases/Phase5/artifacts/wave5_1_furniture_manifest.json"),
        Path("Phases/Phase5/artifacts/wave5_1_transform_depth_contract.json"),
        Path("Phases/Phase5/artifacts/wave5_1_timer_contract.json"),
        Path("Phases/Phase5/artifacts/wave5_1_animation_policy.json"),
        Path("Phases/Phase5/artifacts/wave5_1_selector_gap_contract.json"),
        Path("Phases/Phase5/artifacts/wave5_1_event_mode_policy.json"),
        Path("Phases/Phase5/artifacts/wave5_2_furniture_mapping_contract.json"),
        Path("Phases/Phase5/artifacts/wave5_2_furniture_draw_fixture.json"),
        Path("Phases/Phase5/artifacts/wave5_3_numeric_crop_placement_contract.json"),
        Path("Phases/Phase5/artifacts/wave5_4_img_list_loader_bridge.json"),
        Path("Phases/Phase5/artifacts/wave5_5_img_list_alignment.json"),
        Path("Phases/Phase5/artifacts/wave5_6_floorparts_seb_contract.json"),
        Path("Phases/Phase5/artifacts/wave5_7_seb_consumer_contract.json"),
        Path("Phases/Phase5/artifacts/wave5_8_room_caller_contract.json"),
        Path("Phases/Phase5/artifacts/wave5_9_object_producer_contract.json"),
    ]
    files = []
    for relative in paths:
        absolute = args.root / relative
        files.append({
            "path": relative.as_posix(),
            "exists": absolute.is_file(),
            "sha256": sha256(absolute) if absolute.is_file() else None,
        })
    artifact = {
        "schema_version": "wave5-build-manifest-v1",
        "phase": "Phase5",
        "wave": "Wave5",
        "stage": "C0-through-C8-W5.1-B-through-G-W5.2-furniture-mapping-W5.3-numeric-crop-placement-W5.4-loader-bridge-W5.5-exact-img-list-alignment-W5.6-floorparts-seb-structural-trace-W5.7-seb-consumer-crop-placement-trace-W5.8-room-caller-screen-placement-trace-and-W5.9-object-producer-camera-seb-mapping-trace-with-known-limitations",
        "source_roots_read_only": True,
        "legacy_equivalence": False,
        "files": files,
        "runtime_host": "Phases/Phase5/runtime",
        "status": "complete_with_known_limitations",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(artifact, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "file_count": len(files)}))


if __name__ == "__main__":
    main()
