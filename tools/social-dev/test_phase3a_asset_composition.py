"""Deterministic checks for the Phase 3A source audit and quarantine closure."""

from __future__ import annotations

import json
from pathlib import Path

import build_phase3a_asset_composition as builder


ROOT = builder.ROOT
EVIDENCE = ROOT / "knowledge/fixtures/accepted"
RUNTIME = ROOT / "runtime/social-dev"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def without_dynamic(value):
    if isinstance(value, dict):
        return {
            key: without_dynamic(item)
            for key, item in value.items()
            if key not in {"generated_at_utc", "content_hash"}
        }
    if isinstance(value, list):
        return [without_dynamic(item) for item in value]
    return value


def main() -> int:
    audit_path = EVIDENCE / "phase3a_asset_composition_source_audit.json"
    closure_path = EVIDENCE / "phase3a_asset_composition_closure.json"
    gate_path = EVIDENCE / "display_asset_gate.json"
    manifest_path = ROOT / "knowledge/fixtures/accepted/runtime/display_asset_manifest.json"
    audit = load(audit_path)
    closure = load(closure_path)
    gate = load(gate_path)
    manifest = load(manifest_path)
    rebuilt_audit, rebuilt_closure = builder.build_package()

    assert audit["schema_version"] == "social-dev-phase3a-source-audit-v1"
    assert audit["status"] == "approved"
    assert audit["target"] == "furniture:2"
    assert audit["chair_00"]["opt"]["sha256"] == "5cf124773282b1693210853c6fb04a35426a55d04b08cccb61daa4b8f7454f0a"
    assert audit["chair_00"]["opt"]["size_bytes"] == 63
    assert audit["chair_00"]["opt"]["partial_tail_bytes"] == 0
    assert audit["chair_00"]["opt"]["expected_record_count"] == 3
    assert audit["chair_00"]["opt"]["cells"][0]["piece_count"] == 1
    assert [cell["piece_count"] for cell in audit["chair_00"]["opt"]["cells"]] == [1, 2, 1]
    assert audit["chair_00"]["reconstruction"]["status"] == "pass"
    assert audit["chair_00"]["reconstruction"]["issues"] == []
    assert not audit["alternate_search"]["derived_chair_00_matches"]
    assert audit["alternate_search"]["filename_level_matches"] == [
        "01_GAME_PACKS/chip/chair_00.opt",
        "01_GAME_PACKS/chip/chair_00.png",
        "01_GAME_PACKS/chip/chair_00.seb",
    ]
    assert all(item["status"] == "pass" for item in audit["findings"] if item["code"] in {"source_members_hash_exact", "selector_chain_resolved"})
    version_comparison = audit["source_archives"]["apk"]["chair_version_comparison"]
    assert version_comparison["versions"] == ["2.4.9", "2.5.0", "2.5.1"]
    assert version_comparison["all_three_chip_plaintexts_exact"] is True
    assert version_comparison["all_three_selected_triplets_exact"] is True
    assert version_comparison["all_15_outputs_match_reference_zip_in_each_version"] is True
    assert any(item["code"] == "apk_three_version_chair_assets_exact" and item["status"] == "pass" for item in audit["findings"])

    assert closure["status"] == "approved"
    assert closure["semantic_status"] == "closed_for_phase3a_with_runtime_promotion"
    assert closure["reason_code"] == "chair_00_opt_variable_piece_reconstruction_verified"
    assert closure["runtime_policy"] == {
        "promote_chair_00": True,
        "promote_furniture_2": True,
        "phase3c_may_render_furniture_2": True,
    }
    assert closure["gate_ref"]["content_hash"] == gate["determinism"]["content_hash"]
    assert closure["manifest_ref"]["content_hash"] == manifest["determinism"]["content_hash"]

    assert without_dynamic(audit) == without_dynamic(rebuilt_audit)
    assert without_dynamic(closure) == without_dynamic(rebuilt_closure)
    assert all((RUNTIME / "assets/display-slice-01/01_GAME_PACKS/chip" / f"chair_00.{extension}").is_file() for extension in ("png", "opt", "seb"))
    assert not list(RUNTIME.rglob("*.cs"))

    print(
        "phase3a_asset_composition_test_passed "
        f"status={closure['status']} "
        f"audit_hash={audit['determinism']['content_hash']} "
        f"gate_hash={gate['determinism']['content_hash']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
