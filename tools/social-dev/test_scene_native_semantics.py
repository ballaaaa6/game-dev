"""Contract checks for the Phase 1D native scene-semantics evidence."""

from __future__ import annotations

import json
from pathlib import Path

import scene_native_semantics_facts as facts


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "knowledge/fixtures/accepted"


def load(name: str) -> dict:
    with (EVIDENCE / name).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def main() -> int:
    package = load("scene_native_semantics.json")
    validation = load("scene_native_semantics_validation.json")
    assert validation["status"] == "pass"
    assert validation["failed_checks"] == []
    assert validation["counts"]["native_methods"] == 14
    assert validation["counts"]["claims"] == 7
    assert validation["counts"]["closed_contract_gates"] == 5

    methods = {item["id"]: item for item in package["native_method_manifest"]}
    assert methods["room-init-obj-chips"]["rva_hex"] == "0x12CB448"
    assert methods["objchip-standing-positions"]["rva_hex"] == "0x12C4868"
    assert methods["objchip-is-passable"]["rva_hex"] == "0x12C4AB8"
    assert methods["astar-add-neighbor"]["rva_hex"] == "0x110F248"

    claims = {item["id"]: item for item in package["claims"]}
    assert claims["objmap-to-objchip-type"]["promotable_to_contract"] is True
    assert claims["standing-positions"]["contract"]["order"][0] == {
        "index": 0,
        "x": "baseX + 34",
        "y": "baseY + 25",
    }
    assert claims["neighbor-policy"]["contract"]["connectivity"] == 4
    assert claims["neighbor-policy"]["contract"]["corners_included"] is False
    assert claims["passmap-consumer"]["contract"]["window"]["rows"] == 3
    assert claims["passmap-consumer"]["contract"]["boolean_semantics"] == facts.PASSMAP_CONSUMER["boolean_semantics"]

    fixture = package["fixture"]["record"]
    assert fixture["id"] == 0
    assert fixture["type_candidate"] == 4
    assert fixture["passMap_non_empty"] is True
    assert package["route"]["status"] == "blocked_on_fixture_semantics"
    assert package["route"]["no_path_emitted"] is True
    assert "passmap_boolean_normalization" in package["route"]["remaining_gates"]
    assert "route_goal_filter" in package["route"]["remaining_gates"]
    print(
        "scene_native_semantics_test_passed "
        f"methods={validation['counts']['native_methods']} "
        f"closed={validation['counts']['closed_contract_gates']} "
        f"fixture={fixture['id']} "
        f"route={package['route']['status']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
