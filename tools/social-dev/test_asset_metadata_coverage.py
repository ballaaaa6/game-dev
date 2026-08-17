"""Deterministic checks for the AM-1 asset metadata coverage matrix."""

from __future__ import annotations

import json

import build_asset_metadata_coverage as builder


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def main() -> int:
    coverage = load(builder.COVERAGE_PATH)
    orphan = load(builder.ORPHAN_PATH)
    contract = load(builder.CONTRACT_PATH)
    rebuilt, rebuilt_orphan = builder.build_payload()
    rebuilt_contract = builder.build_contract_payload(rebuilt, rebuilt_orphan)

    assert coverage["schema_version"] == "social-dev-asset-metadata-coverage-v1"
    assert coverage["status"] == "pass"
    assert coverage["semantic_status"] == "coverage_matrix_not_runtime_approval"
    assert coverage["determinism"]["content_hash"] == rebuilt["determinism"]["content_hash"]
    assert orphan["determinism"]["content_hash"] == rebuilt_orphan["determinism"]["content_hash"]
    assert contract["determinism"]["content_hash"] == rebuilt_contract["determinism"]["content_hash"]

    counts = coverage["counts"]
    assert counts["indexed_assets"] == 3542
    assert counts["native_assets"] == 3542
    assert counts["selectors"] == 3192
    assert counts["data_selector_relations"] == 523
    assert counts["consumer_edges"] == 250
    assert counts["lifecycle_edges"] == 43
    assert counts["runtime_manifest_entries"] == 197
    assert counts["display_gate_entries"] == 18
    assert counts["data_fields"] == 1063
    assert counts["relations_explicit_absent_sentinel"] == 88
    assert counts["relations_selector_scope_unresolved"] == 11
    assert counts["relation_coverage_statuses"]["resolved_to_indexed_asset"] == 424
    assert counts["asset_statuses"].get("indexed_not_in_native_catalog", 0) == 0
    assert counts["selector_coverage_statuses"]["unresolved_selector"] == 1

    assert len(coverage["assets"]) == counts["indexed_assets"]
    assert len({row["asset_id"] for row in coverage["assets"]}) == counts["indexed_assets"]
    assert len(coverage["selectors"]) == counts["selectors"]
    assert len(coverage["data_fields"]) == counts["data_fields"]
    assert len(coverage["data_selector_relations"]) == counts["data_selector_relations"]
    assert len(coverage["consumer_edges"]) == counts["consumer_edges"]
    assert len(coverage["runtime_manifest_entries"]) == counts["runtime_manifest_entries"]

    unresolved = orphan["selector_gaps"]["unresolved"]
    assert len(unresolved) == 1
    assert unresolved[0]["raw_line"] == "bg.seb"
    assert len(orphan["asset_gaps"]["indexed_not_in_native_catalog"]) == 0
    assert len(orphan["runtime_reference_gaps"]) == 0
    assert contract["acceptance"]["indexed_assets_are_traceable"] is True
    assert contract["acceptance"]["unresolved_selector_count_is_explicit"] is True

    print("asset_metadata_coverage_test_passed " f"assets={counts['indexed_assets']} " f"selectors={counts['selectors']} " f"fields={counts['data_fields']} " f"runtime_entries={counts['runtime_manifest_entries']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
