from __future__ import annotations

import json
from pathlib import Path

import build_character_metadata as builder


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
    fixture = load(EVIDENCE / "character_metadata_fixture.json")
    validation = load(EVIDENCE / "character_metadata_validation.json")
    contract = load(RUNTIME_EVIDENCE / "character_metadata_contract.json")
    rebuilt_fixture, rebuilt_contract, rebuilt_validation = builder.build_package()

    assert fixture["schema_version"] == "social-dev-character-metadata-fixture-v1"
    assert contract["schema_version"] == "social-dev-character-metadata-v1"
    assert fixture["status"] == contract["status"] == validation["status"] == "pass"
    assert contract["semantic_status"] == "approved_for_runtime_contract"
    assert validation["failed_checks"] == []
    assert validation["counts"]["passed_checks"] == validation["counts"]["checks"]
    assert validation["counts"]["staff_records"] == 141
    assert validation["counts"]["helper_records"] == 19
    assert validation["counts"]["job_records"] == 30
    assert validation["counts"]["skill_records"] == 36
    assert validation["counts"]["staff_image_selectors_resolved"] == 141
    assert validation["counts"]["unique_staff_image_selectors"] == 105

    assert [item["source_identity"]["source_id"] for item in contract["staff"]] == list(range(141))
    assert [item["source_identity"]["source_id"] for item in contract["helpers"]] == list(range(19))
    assert [item["source_identity"]["source_id"] for item in contract["jobs"]] == list(range(30))
    assert [item["source_identity"]["source_id"] for item in contract["skills"]] == list(range(36))
    assert all(item["render"]["image_selector"]["resolution_status"] == "resolved" for item in contract["staff"])
    assert {item["render"]["capability_profile_ref"] for item in contract["staff"]} == {"human-staff-v1"}
    assert {item["render"]["behavior_profile_ref"] for item in contract["staff"]} == {"staff-living-scene-v1"}
    assert {item["render"]["capability_profile_ref"] for item in contract["helpers"]} == {"helper-record-v1"}
    assert all(item["relations"]["job_ref"]["source_id"] in range(30) for item in contract["staff"])
    assert all(item["relations"]["skill_ref"]["source_id"] in range(36) for item in contract["staff"])
    assert all("level" not in item["source_fields"] and "position" not in item["source_fields"] for item in contract["staff"])
    assert contract["staff"][0]["source_fields"]["rank_"] == 5
    assert "provenance_ref" not in contract["staff"][0]
    assert contract["runtime_state_boundary"]["mutable_actor_state_owner"] == "ActorState"
    assert contract["staff"][114]["name"]["values"]["English"] == "Bearington Bearington"
    assert contract["helpers"][2]["name"]["values"]["English"] == "Kairobot"

    assert without_dynamic(fixture) == without_dynamic(rebuilt_fixture)
    assert without_dynamic(contract) == without_dynamic(rebuilt_contract)
    assert without_dynamic(validation) == without_dynamic(rebuilt_validation)

    print(
        "character_metadata_test_passed "
        f"staff={validation['counts']['staff_records']} "
        f"helpers={validation['counts']['helper_records']} "
        f"jobs={validation['counts']['job_records']} "
        f"skills={validation['counts']['skill_records']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
