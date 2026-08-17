"""Deterministic checks for the AM-0 asset metadata baseline."""

from __future__ import annotations

import json

import build_asset_metadata_baseline as builder


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def main() -> int:
    baseline = load(builder.BASELINE_PATH)
    contract = load(builder.CONTRACT_PATH)
    rebuilt = builder.build_payload()
    rebuilt_contract = builder.build_contract_payload(rebuilt)

    assert baseline["schema_version"] == "social-dev-asset-metadata-baseline-v1"
    assert baseline["status"] == "pass"
    assert baseline["semantic_status"] == "evidence_baseline_not_runtime_approval"
    assert baseline["determinism"]["content_hash"] == rebuilt["determinism"]["content_hash"]
    assert baseline["inputs"]["input_hash"] == rebuilt["inputs"]["input_hash"]

    index = baseline["inventory"]["asset_index"]
    assert index["row_count"] == 3542
    assert index["unique_relative_paths"] == 3542
    assert index["duplicate_relative_paths"] == []
    assert index["rows_with_sha256"] == 3542
    assert index["by_kind"]["original_pack_asset"] == 2826
    assert index["by_pack"]["__ungrouped__"] == 112

    native = baseline["native_catalog"]
    assert native["counts"]["assets"] == 3542
    assert native["counts"]["selectors"] == 3192
    assert native["counts"]["data_records"] == 3693
    assert native["selector_status"]["resolved"] == 3191
    assert native["selector_status"]["unresolved_target"] == 1
    assert native["data_record_status"]["verified_reader_order"] == 281
    assert native["data_record_status"]["not_mapped"] == 3412
    assert native["unresolved_selector_samples"][0]["raw_line"] == "bg.seb"

    contract_counts = contract["counts"]
    assert contract["schema_version"] == "social-dev-asset-metadata-baseline-contract-v1"
    assert contract["status"] == "pass"
    assert contract["semantic_status"] == "baseline_contract_not_runtime_catalog"
    assert contract["baseline_content_hash"] == baseline["determinism"]["content_hash"]
    assert contract["determinism"]["content_hash"] == rebuilt_contract["determinism"]["content_hash"]
    assert contract_counts["indexed_assets"] == 3542
    assert contract_counts["native_data_rows"] == 3693
    assert contract_counts["native_selectors"] == 3192
    assert contract_counts["runtime_approved_display_assets"] == 34
    assert contract_counts["room_count"] == 18
    assert contract_counts["staff_count"] == 141
    assert contract_counts["helper_count"] == 19

    assert len(baseline["inputs"]["files"]) == len(builder.INPUT_PATHS)
    assert all(item["path"] and item["sha256"] for item in baseline["inputs"]["files"])
    assert len(baseline["known_exceptions"]) >= 5
    assert len(baseline["verification_commands"]) == 10

    print(
        "asset_metadata_baseline_test_passed "
        f"indexed_assets={index['row_count']} "
        f"native_assets={native['counts']['assets']} "
        f"selectors={native['counts']['selectors']} "
        f"data_rows={native['counts']['data_records']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
