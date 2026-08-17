"""Validate the deterministic all-room native assembly gate."""

from __future__ import annotations

import json
from pathlib import Path

import build_phase3d_all_room_assembly_gate as builder


ROOT = builder.ROOT
EVIDENCE = ROOT / "knowledge/fixtures/accepted/phase3d_all_room_assembly_gate.json"
RUNTIME = ROOT / "knowledge/fixtures/accepted/runtime/phase3d_all_room_assembly_gate_contract.json"


def main() -> int:
    evidence = json.loads(EVIDENCE.read_text(encoding="utf-8"))
    runtime = json.loads(RUNTIME.read_text(encoding="utf-8"))
    rebuilt = builder.build_payload()
    assert evidence == runtime
    assert evidence["status"] == "pass"
    assert evidence["semantic_status"] == "approved_for_runtime_composition"
    assert evidence["determinism"]["content_hash"] == rebuilt["determinism"]["content_hash"]
    assert len(evidence["rooms"]) == 18
    assert [room["room_key"] for room in evidence["rooms"]] == [f"room:{index}" for index in range(18)]
    assert all(room["grid"] == [10, 10] and room["objchip_cells"] == 100 for room in evidence["rooms"])
    assert all(room["map_variant"] == "floor_0" for room in evidence["rooms"])
    assert all(room["wall_cells"] > 0 and room["door_cells"] == 1 for room in evidence["rooms"])
    assert evidence["checks"]["native_content_catalog"]["records"] == 3693
    assert evidence["checks"]["native_content_catalog"]["assets"] == 3542
    assert evidence["checks"]["native_content_catalog"]["selectors"] == 3192
    assert evidence["checks"]["wall_door_composition"]["walls"] == 18
    assert evidence["checks"]["wall_door_composition"]["doors"] == 18
    assert evidence["runtime_trace_policy"]["silent_unresolved_fallbacks"] is False
    assert evidence["browser_smoke"]["status"] == "pass"
    assert evidence["browser_smoke"]["assertions"] == {
        "rooms_checked": 18,
        "rooms_gate_pass": 18,
        "rooms_with_zero_unresolved": 18,
        "rooms_with_zero_console_errors": 18,
        "rooms_with_zero_console_warnings": 18,
        "wall_door_draws_observed": 18,
        "furniture_fallbacks_observed": 0,
    }
    assert len(evidence["browser_smoke"]["rooms"]) == 18
    assert all(room["gate_status"] == "pass" for room in evidence["browser_smoke"]["rooms"])
    assert all(room["asset_status"] == "ready" for room in evidence["browser_smoke"]["rooms"])
    assert all(room["unresolved"] == [] for room in evidence["browser_smoke"]["rooms"])
    assert all(room["trace"]["wall_door_draws"] == 16 for room in evidence["browser_smoke"]["rooms"])
    assert evidence["browser_smoke"]["rooms"][17]["raw_overlay_cells"] == 100
    assert not evidence.get("open_items")
    assert not evidence.get("blockers")
    print(f"phase3d_all_room_assembly_gate_test_passed rooms={len(evidence['rooms'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
