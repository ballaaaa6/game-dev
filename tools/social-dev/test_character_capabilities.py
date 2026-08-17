from __future__ import annotations

import json
from pathlib import Path

import build_character_capabilities as builder


ROOT = builder.ROOT
EVIDENCE = ROOT / "knowledge/fixtures/accepted"
RUNTIME_EVIDENCE = ROOT / "knowledge/fixtures/accepted/runtime"


def load(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def without_dynamic(value):
    if isinstance(value, dict):
        return {
            key: without_dynamic(item)
            for key, item in value.items()
            if key not in {"generated_at_utc", "content_hash", "contract_hash"}
        }
    if isinstance(value, list):
        return [without_dynamic(item) for item in value]
    return value


def main() -> int:
    fixture = load(EVIDENCE / "character_capability_fixture.json")
    validation = load(EVIDENCE / "character_capability_validation.json")
    contract = load(RUNTIME_EVIDENCE / "character_capability_contract.json")
    rebuilt_fixture, rebuilt_contract, rebuilt_validation = builder.build_package()

    assert fixture["schema_version"] == "social-dev-character-capability-fixture-v1"
    assert contract["schema_version"] == "social-dev-character-capability-v1"
    assert fixture["status"] == contract["status"] == validation["status"] == "pass"
    assert contract["semantic_status"] == "approved_for_runtime_contract"
    assert validation["failed_checks"] == []
    assert validation["counts"]["passed_checks"] == validation["counts"]["checks"]
    assert validation["counts"]["profiles"] == 4
    assert validation["counts"]["staff_bindings"] == 141
    assert validation["counts"]["helper_bindings"] == 19
    assert validation["counts"]["human_seb_selectors"] == 35
    assert validation["counts"]["human_native_actions"] == 16
    assert validation["counts"]["human_native_action_selectors"] == 35

    profiles = {profile["id"]: profile for profile in contract["profiles"]}
    human = profiles["human-staff-v1"]
    assert set(human["actions"]["wait"]["selector_by_direction"]) == {"right", "left", "up", "down"}
    assert set(human["actions"]["move"]["selector_by_direction"]) == {"right", "left", "up", "down"}
    assert set(human["actions"]["typing"]["selector_by_direction"]) == {"right", "left", "up", "down"}
    assert human["actions"]["talk"]["source_action"] == "typing"
    assert human["actions"]["fly_away"]["status"] == "deferred"
    assert human["frame_composition"]["binary_decoder"] == "multilayer_seb_decoder_v1"
    assert human["native_actions"]["banzai"]["selector_by_direction"]["right"]["selector_id"] == 19
    assert human["native_actions"]["head"]["selector"]["selector_id"] == 100
    assert {item["profile_ref"] for item in contract["bindings"]["staff"]} == {"human-staff-v1"}
    assert [item["source_id"] for item in contract["bindings"]["staff"]] == list(range(141))
    assert [item["source_id"] for item in contract["bindings"]["helpers"]] == list(range(19))
    assert profiles["helper-record-v1"]["behavior"]["status"] == "not_promoted_as_staff_lifecycle"
    assert profiles["avatar-v1"]["composition"]["parts"] == ["body", "head"]
    assert contract["runtime_policy"]["instance_creation"] == "lazy_on_spawn_or_scene_use"
    assert contract["runtime_policy"]["asset_loading"] == "lazy_selector_cache_not_eager_full_catalog"

    assert without_dynamic(fixture) == without_dynamic(rebuilt_fixture)
    assert without_dynamic(contract) == without_dynamic(rebuilt_contract)
    assert without_dynamic(validation) == without_dynamic(rebuilt_validation)

    print(
        "character_capabilities_test_passed "
        f"profiles={validation['counts']['profiles']} "
        f"staff={validation['counts']['staff_bindings']} "
        f"helpers={validation['counts']['helper_bindings']} "
        f"selectors={validation['counts']['human_seb_selectors']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
