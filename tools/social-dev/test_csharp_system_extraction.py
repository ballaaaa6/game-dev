"""Validate the generated Social Dev Phase 0 extraction artifacts."""

from __future__ import annotations

import json
from pathlib import Path

from build_csharp_system_extraction import DEFAULT_OUTPUT, build_artifacts


EXPECTED_FILES = {
    "csharp_system_inventory.json",
    "csharp_dependency_graph.json",
    "csharp_source_slice_manifest.json",
    "csharp_semantic_review_queue.json",
    "csharp_extraction_validation.json",
}


def main() -> int:
    artifacts = build_artifacts(DEFAULT_OUTPUT)
    validation = artifacts["csharp_extraction_validation.json"]
    if validation["status"] != "pass":
        raise AssertionError(f"validation failed: {validation['failed_checks']}")
    if validation["semantic_status"] != "pending_review":
        raise AssertionError("semantic status must remain pending_review")
    if validation["counts"] != {
        "types": 82,
        "fields": 3430,
        "methods": 1685,
        "systems": 11,
        "dependency_edges": 14,
        "source_slices": 7,
        "review_items": 6,
    }:
        raise AssertionError(f"unexpected counts: {validation['counts']}")

    for name in EXPECTED_FILES:
        path = DEFAULT_OUTPUT / name
        if not path.is_file():
            raise AssertionError(f"missing artifact: {path}")
        with path.open("r", encoding="utf-8") as handle:
            json.load(handle)

    slices = artifacts["csharp_source_slice_manifest.json"]["slices"]
    unresolved = {
        item["id"]: {
            "types": item["missing_types"],
            "methods": item["missing_methods"],
            "fields": item["missing_fields"],
            "constants": item["missing_constants"],
        }
        for item in slices
        if any(
            item[key]
            for key in (
                "missing_types",
                "missing_methods",
                "missing_fields",
                "missing_constants",
            )
        )
    }
    if unresolved:
        raise AssertionError(f"unresolved source slice references: {unresolved}")

    print(
        "phase0_extraction_test_passed "
        f"types={validation['counts']['types']} "
        f"fields={validation['counts']['fields']} "
        f"methods={validation['counts']['methods']} "
        f"slices={validation['counts']['source_slices']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
