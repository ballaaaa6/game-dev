"""Validate the content-addressed Phase 3C visual gate v2 evidence."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "knowledge/fixtures/accepted"
PACKAGE_PATH = EVIDENCE / "phase3c_visual_gate_v2.json"
RUNTIME_PATH = ROOT / "knowledge/fixtures/accepted/runtime/phase3c_visual_gate_v2_contract.json"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_visual_gate_package() -> None:
    package = read_json(PACKAGE_PATH)
    runtime = read_json(RUNTIME_PATH)
    assert package == runtime
    assert package["status"] == "pass_structural_pending_native_composition"
    assert package["semantic_status"] == "deterministic_asset_frame_overlay_gate"
    assert package["browser_fixture"]["canvas"] == {"width": 980, "height": 600}
    assert package["browser_fixture"]["console"] == {"errors": 0, "warnings": 0}
    assert package["checks"]["render_pass_order"]["status"] == "pass"
    assert package["checks"]["flicker_regression"]["status"] == "pass"
    assert package["checks"]["no_invented_furniture"]["status"] == "pass"
    assert package["browser_fixture"]["room17"]["raw_overlay"]["cells"] == 100
    assert package["browser_fixture"]["room17"]["raw_overlay"]["door_cells"] == [[8, 3]]
    assert package["browser_fixture"]["room17"]["native_composition"] == "blocked_by_evidence"

    for frame in package["browser_fixture"]["room0"]["frames"]:
        assert frame["frame_checks"] == {
            "checked": 51,
            "total": 51,
            "missing_assets": [],
            "out_of_bounds": [],
        }
        assert frame["furniture_render"]["approved_asset_draws"] == 7
        assert frame["furniture_render"]["fallbacks"] == 0
        screenshot = ROOT / frame["screenshot"]["path"]
        assert screenshot.is_file()
        assert hashlib.sha256(screenshot.read_bytes()).hexdigest() == frame["screenshot"]["sha256"]

    room17 = package["browser_fixture"]["room17"]
    screenshot = ROOT / room17["screenshot"]["path"]
    assert screenshot.is_file()
    assert hashlib.sha256(screenshot.read_bytes()).hexdigest() == room17["screenshot"]["sha256"]


if __name__ == "__main__":
    test_visual_gate_package()
    print("phase3c_visual_gate_v2_test_passed frames=3 overlay_cells=100")
