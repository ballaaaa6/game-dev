"""Regression checks for the accepted T1.0 full-body generation pilot."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ACCEPTANCE = ROOT / "knowledge" / "brain" / "acceptance" / "t1-0-full-body-generation-pivot-pilot"


def read_json(name: str) -> dict:
    return json.loads((ACCEPTANCE / name).read_text(encoding="utf-8"))


def test_final_decision_is_go() -> None:
    decision = read_json("final-decision.json")

    assert decision["decision"] == "GO"
    assert decision["go_token"] == "PASS_T1_0_FULL_BODY_GENERATION_PIVOT_PILOT_GO"
    assert all(decision["gates"].values())
    assert decision["source_mutation"] is False
    assert decision["next_authorized_phase"] == "T1_FULL_BODY_GENERATION"


def test_canonical_500_cohort_shape_and_manifest() -> None:
    composition = read_json("cohort-composition.json")
    summary = read_json("representation-summary.json")
    manifest = json.loads((ACCEPTANCE / "sample-manifest.json").read_text(encoding="utf-8"))

    expected = {
        "BASELINE_READABLE": 75,
        "CFG_DEFERRED": 175,
        "NATIVE_DEFERRED": 175,
        "IDENTITY_MECHANICAL_SOURCE_LIMITED": 50,
        "EXTREME_COMPLEXITY": 25,
    }
    assert composition["cohort_counts"] == expected
    assert sum(expected.values()) == 500
    assert composition["selection_scan"]["canonical_rows"] == 10827
    assert composition["selection_scan"]["canonical_types"] == 641
    assert composition["overall_ownership"] == {"GAME_FIRST_PARTY": 249, "KAIRO_ENGINE": 251}
    assert composition["extreme_min_instructions"] == 1888
    assert composition["extreme_max_instructions"] == 8693
    assert summary["representation_coverage"] == {"emitted": 500, "missing": 0, "total": 500}
    assert summary["method_identity_coverage"] == 500
    assert summary["provenance_coverage"] == 500
    assert len(manifest) == 500
    assert len({row["method_id"] for row in manifest}) == 500
    assert {row["cohort"] for row in manifest} == set(expected)


def test_native_instruction_conservation_and_fact_accounting() -> None:
    conservation = read_json("instruction-conservation.json")
    facts = conservation["native_facts"]

    assert conservation["all_native_ranges_accounted"] is True
    assert conservation["omitted_operation_count"] == 0
    assert facts["total_decoded_instructions"] == 117876
    assert facts["total_represented_instructions"] == 117876
    assert facts["total_omitted_instructions"] == 0
    assert facts["total_extra_ir_operations"] == 0
    assert facts["resolved_direct_calls"] == 3873
    assert facts["resolved_field_accesses"] == 16658
    assert facts["branch_targets"] == 18500


def test_sidecar_compile_replay_and_negative_fixture_gates() -> None:
    compile_result = read_json("sidecar-compile.json")
    replay = read_json("deterministic-replay.json")
    negatives = read_json("false-positive-audit.json")
    source_gate = read_json("source-gate.json")

    assert compile_result["parse_pass"] is True
    assert compile_result["compile_pass"] is True
    assert compile_result["parse_error_count"] == 0
    assert compile_result["compile_error_count"] == 0
    assert compile_result["sidecar_method_source_count"] == 500
    assert replay["deterministic"] is True
    assert replay["byte_identical"] is True
    assert negatives["pass"] is True
    assert negatives["negative_fixtures_rejected"] is True
    assert negatives["false_positive_count"] == 0
    assert source_gate["status"] == "PASS"
    assert all(item["matches"] for name, item in source_gate["hashes"].items() if name != "source_tree")


def test_hosted_ir_contract_exposes_replayable_method_body() -> None:
    contract = (ROOT / "tools" / "social-dev" / "t1_twin_native_ir_contract.cs").read_text(encoding="utf-8")

    assert "public sealed class TwinNativeIrMethod" in contract
    assert "public List<TwinIrOp> Operations" in contract
    assert "public string SourceBody { get; set; }" in contract
    assert "public string GeneratedHighLevelCSharp { get; set; }" in contract
    assert "public string OpaqueEvidenceReference { get; set; }" in contract
    assert "public string Limitation { get; set; }" in contract
