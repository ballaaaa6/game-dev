"""Validate the complete Phase 0–1C pre-runtime closure package."""

from __future__ import annotations

import json
from pathlib import Path

import build_pre_runtime_closure as builder


ROOT = builder.ROOT


def load(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def main() -> int:
    package = builder.build_package()

    matrix = load(ROOT / "knowledge/fixtures/accepted/semantic_review_closure.json")
    closure = load(ROOT / "knowledge/fixtures/accepted/runtime/pre_runtime_closure_contract.json")
    load_contract = load(ROOT / "knowledge/fixtures/accepted/load_contract_closure.json")
    data_contract = load(ROOT / "knowledge/fixtures/accepted/runtime/data_contract.json")
    entity_contract = load(ROOT / "knowledge/fixtures/accepted/runtime/entity_contract.json")
    save_contract = load(ROOT / "knowledge/fixtures/accepted/runtime/save_contract.json")
    supersession = load(ROOT / "knowledge/fixtures/accepted/phase1_supersession.json")

    assert closure["status"] == "pass"
    assert closure["semantic_status"] == "closed_before_runtime"
    assert closure["blocking_review_items"] == []
    assert closure["open_items"] == []
    assert matrix["status"] == "pass"
    assert matrix["semantic_status"] == "closed_before_runtime"
    assert matrix["counts"]["total_items"] == 21
    assert matrix["counts"]["closed_items"] == 21
    assert matrix["counts"]["open_items"] == 0
    assert matrix["counts"]["pending_review_items"] == 0
    assert matrix["counts"]["blocking_items_remaining"] == 0
    assert all(item["closure_status"] == "closed" for item in matrix["items"])
    assert all(item["final_status"] in builder.ALLOWED_FINAL_STATUSES for item in matrix["items"])

    assert load_contract["status"] == "pass"
    assert load_contract["semantic_status"] == "closed_for_display_slice"
    assert len(load_contract["first_slice_mappings"]) == 5
    assert all(item["status"] == "verified" for item in load_contract["first_slice_mappings"])
    assert load_contract["exceptions"]["missing_loaders"]
    assert load_contract["exceptions"]["count_mismatches"]
    assert load_contract["open_blocking_items"] == []

    for contract in (data_contract, entity_contract, save_contract):
        assert contract["status"] == "pass"
        assert contract["semantic_status"] == "approved_for_runtime_contract"
        assert contract["open_blocking_items"] == []

    assert supersession["status"] == "pass"
    assert supersession["semantic_status"] == "closed_by_authority"
    assert len(supersession["replacement_matrix"]) == 3
    assert all(item["final_status"] == "verified" for item in supersession["replacement_matrix"])

    phase0_ids = {item["id"] for item in matrix["items"] if item["phase"] == "Phase 0"}
    assert phase0_ids == {
        "loader-column-semantic",
        "decompiler-body-repair",
        "player-appdata-split",
        "asset-selector-promotion",
        "semantic-state-labels",
        "first-slice-selection",
    }
    phase1c_ids = {item["id"] for item in matrix["items"] if item["phase"] == "Phase 1C"}
    assert phase1c_ids == {"passmap-and-standing-semantics", "route-goal-filter", "asset-selector-carryover"}

    for relative, expected in package.items():
        path = ROOT / relative
        assert path.is_file(), f"missing generated closure artifact: {path}"
        actual = load(path)
        assert builder.without_dynamic(actual) == builder.without_dynamic(expected)

    assert not (ROOT / "runtime/social-dev/core").exists()
    assert not (ROOT / "runtime/social-dev/renderer").exists()

    print(
        "pre_runtime_closure_test_passed "
        f"items={matrix['counts']['total_items']} "
        f"verified={matrix['counts']['final_statuses']['verified']} "
        f"deferred={matrix['counts']['final_statuses']['deferred']} "
        f"quarantine={matrix['counts']['final_statuses']['quarantine']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
