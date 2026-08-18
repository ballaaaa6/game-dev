#!/usr/bin/env python3
"""Validate the named T3 adversarial regression cases against the materialized acceptance."""

from __future__ import annotations

import argparse
import collections
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EXPECTED_TIERS = {"EXISTING_READABLE": 2481, "GENERATED_LOW": 8291, "DECLARATION_ONLY": 50, "SOURCE_LIMITED_STUB": 5}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def run(root: Path) -> dict[str, Any]:
    acceptance = root / "knowledge" / "brain" / "acceptance" / "t3-source-like-uplift"
    artifacts = root / "artifacts" / "t3-source-like-uplift" / "waves" / "final"
    fixture = load(root / "tools" / "social-dev" / "t3_negative_regression_cases.json")
    profile = load(acceptance / "full-corpus-profile.json")
    manifest = load(artifacts / "methods" / "method-identity-manifest.json")
    compile_summary = load(acceptance / "compile-summary.json")
    final_compile = compile_summary["final"]
    replay = load(acceptance / "deterministic-replay.json")
    tiers = collections.Counter(row.get("representation_tier") for row in manifest)
    promoted = [row for row in manifest if row.get("promotion_status") == "PROMOTED"]
    ledger_rows = [json.loads(line) for line in (acceptance / "promotion-ledger.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    profile_ids = {row.get("method_id") for row in profile}
    manifest_ids = {row.get("method_id") for row in manifest}
    source_files = sorted(artifacts.rglob("*.cs"))
    source_text = "\n".join(path.read_text(encoding="utf-8") for path in source_files)
    canonical = load(acceptance / "canonical-universe.json")
    checks = {
        "INVALID_CTOR_EMISSION": not any(".ctor(" in line or ".cctor(" in line for line in source_text.splitlines() if "TwinCanonicalMethod" not in line),
        "INVALID_COMPILER_GENERATED_IDENTIFIER": not any(re.search(r"\b(?:class|struct|interface|enum)\s+<", line) for line in source_text.splitlines()),
        "SUMMARY_COMPILE_WITHOUT_ARTIFACT_COMPILE": bool(final_compile.get("parse_pass") and final_compile.get("compile_pass") and final_compile.get("parse_error_count") == 0 and final_compile.get("compile_error_count") == 0 and Path(final_compile.get("project_root", "")).exists()),
        "METHOD_ID_LABEL_WITHOUT_T1_HASH_LINK": len(manifest) == 10827 and all(row.get("representation_hash") and row.get("t1_shard") is not None and row.get("t1_segment_count") is not None and row.get("exact_t1_linkage") is True for row in manifest),
        "NOOP_DISPATCH_RUNTIME": all(row.get("body_policy") == "SOURCE_LIKE_EXACT" and row.get("semantic_tier") == "SOURCE_LIKE_EXACT" for row in promoted),
        "TYPE_SURFACE_COUNT_DRIFT": canonical.get("type_count") == 641 and compile_summary.get("final_generation", {}).get("canonical_type_count") == 641,
        "FIELD_SURFACE_MISSING": canonical.get("field_count") == 10251,
        "TIER_COLLAPSE": dict(tiers) == EXPECTED_TIERS,
        "FALSE_READABLE_REINJECTION_PASS": all(row.get("t1_representation_tier") != "EXISTING_READABLE" or row.get("promotion_status") != "PROMOTED" or row.get("promotion_rule") == "EXACT_SOURCE_BODY_COMPILE_PROVEN" for row in manifest),
        "REPORT_ARITHMETIC_DRIFT": sum(int(row.get("t1_operation_count") or 0) for row in profile) == 988046 and len(profile) == 10827 and len(manifest) == 10827,
        "SHARED_NATIVE_BODY_IDENTITY_COLLAPSE": len(profile_ids) == 10827 and profile_ids == manifest_ids,
        "WRONG_RVA_NATIVE_SLICE": all(row.get("native_fingerprints", {}).get("native_start") and row.get("t1_segments") is not None for row in profile if row.get("t1_representation_tier") not in {"DECLARATION_ONLY", "SOURCE_LIMITED_STUB"}),
        "PLACEHOLDER_SEMANTIC_PROMOTION": all(row.get("promotion_rule") and row.get("semantic_tier") == "SOURCE_LIKE_EXACT" for row in promoted),
        "OPERATION_TRUNCATION": all(int(row.get("t1_accounting", {}).get("omitted_operation_count") or 0) == 0 for row in profile),
        "PROMOTION_PROVENANCE_LOSS": len(ledger_rows) == len({row.get("method_id") for row in ledger_rows}) and all(row.get("ownership") and row.get("declaring_type") and row.get("t1_representation_hash") and row.get("t1_shard") is not None and row.get("t1_segments") is not None and (row.get("source_body_hash") or row.get("native_operation_fingerprint")) for row in ledger_rows),
        "HIDDEN_COMPILE_REGRESSION": replay.get("status") == "PASS" and replay.get("source_tree_sha256_equal") is True and replay.get("compile_pass_a") is True and replay.get("compile_pass_b") is True,
    }
    fixture_ids = [case["id"] for case in fixture.get("cases", [])]
    case_results = [{"id": case_id, "pass": bool(checks.get(case_id))} for case_id in fixture_ids]
    return {
        "schema_version": "t3-negative-regression-validation-v2",
        "fixture": "tools/social-dev/t3_negative_regression_cases.json",
        "case_count": len(case_results),
        "case_results": case_results,
        "checks": checks,
        "status": "PASS" if len(case_results) == 16 and all(item["pass"] for item in case_results) else "FAIL",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    result = run(args.root.resolve())
    out = args.out or (args.root.resolve() / "knowledge" / "brain" / "acceptance" / "t3-source-like-uplift" / "negative-regression-validation.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
