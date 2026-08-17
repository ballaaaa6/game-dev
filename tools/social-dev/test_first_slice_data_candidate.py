"""Validate the first-slice data candidate and its provenance boundary."""

from __future__ import annotations

import json

from build_first_slice_data_candidate import DEFAULT_OUTPUT, build_candidate


def main() -> int:
    candidate, validation = build_candidate(DEFAULT_OUTPUT)
    if validation["status"] != "pass":
        raise AssertionError(f"validation failed: {validation['failed_checks']}")
    if candidate["semantic_status"] != "pending_review":
        raise AssertionError("candidate must remain pending_review")
    if validation["counts"] != {
        "types": 5,
        "selected_records": 22,
        "missing_records": 0,
        "links": 6,
        "review_items": 5,
    }:
        raise AssertionError(f"unexpected counts: {validation['counts']}")
    if candidate["selection"]["furniture"]["name_evidence"]["Japanese"][-1] != "ペンタブデスク":
        raise AssertionError("Japanese furniture name must come from evidence")
    if candidate["selection"]["room_state_status"] != "unverified":
        raise AssertionError("room placement must remain unverified")
    if candidate["selection"]["skill"]["ids"] != [1]:
        raise AssertionError("loader-aware first-slice skill candidate must be SkillData(1)")

    for name in ("first_slice_data_candidate.json", "first_slice_data_validation.json"):
        with (DEFAULT_OUTPUT / name).open("r", encoding="utf-8") as handle:
            json.load(handle)

    print(
        "first_slice_data_test_passed "
        f"types={validation['counts']['types']} "
        f"records={validation['counts']['selected_records']} "
        f"missing={validation['counts']['missing_records']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
