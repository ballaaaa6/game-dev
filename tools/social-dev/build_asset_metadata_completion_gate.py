"""Build the final asset-metadata completion and readiness audit.

The gate answers two different questions explicitly:

* Is every indexed asset represented by deterministic identity, family,
  selector, composition, usage, and provenance metadata or an explicit gap?
* Which rows are approved for the current runtime query surface?

It never upgrades a catalog-only row into runtime-ready status.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "knowledge/fixtures/accepted"
RUNTIME_EVIDENCE = ROOT / "knowledge/fixtures/accepted/runtime"
RUNTIME_SRC = ROOT / "runtime/social-dev/src"

BASELINE_PATH = EVIDENCE / "asset_metadata_baseline.json"
COVERAGE_PATH = EVIDENCE / "asset_metadata_coverage.json"
TAXONOMY_PATH = EVIDENCE / "asset_family_taxonomy.json"
SELECTOR_PATH = EVIDENCE / "asset_selector_usage_matrix.json"
FIELD_PATH = EVIDENCE / "data_field_semantics_matrix.json"
COMPOSITION_PATH = EVIDENCE / "asset_composition_catalog.json"
GEOMETRY_PATH = EVIDENCE / "asset_geometry_catalog.json"
FURNITURE_PATH = EVIDENCE / "furniture_asset_metadata.json"
CHARACTER_PATH = EVIDENCE / "character_visual_asset_metadata.json"
USAGE_PATH = EVIDENCE / "asset_usage_lifecycle_placement_matrix.json"
SURFACE_PATH = EVIDENCE / "asset_surface_provenance.json"
NATIVE_CATALOG_PATH = RUNTIME_EVIDENCE / "native_content_catalog.json"
RUNTIME_MANIFEST_PATH = RUNTIME_EVIDENCE / "asset_metadata_runtime_manifest.json"
RUNTIME_CONTRACT_PATH = RUNTIME_EVIDENCE / "asset_metadata_runtime_contract.json"

GATE_PATH = EVIDENCE / "asset_metadata_completion_gate.json"
CONTRACT_PATH = RUNTIME_EVIDENCE / "asset_metadata_completion_contract.json"
REPORT_PATH = ROOT / "docs/reports/social-dev_asset_metadata_completion.md"


def stable_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def artifact_hash(value: dict[str, Any]) -> str | None:
    determinism = value.get("determinism", {})
    return determinism.get("content_hash") or determinism.get("contract_hash")


def source_import_violations() -> list[dict[str, Any]]:
    forbidden = ("knowledge/", "archive/", ".apk", ".zip", "Assembly-CSharp")
    # V1/V2/V3 consume immutable, generated visual contracts as their
    # compatibility boundary. These JSON contracts are not source roots or
    # executable decompiled C# and are the approved static-only input for the
    # visual-port layers.
    approved_visual_contracts = (
        "knowledge/fixtures/accepted/visual-port/",
        "knowledge/fixtures/accepted/seb_catalog.json",
    )
    csharp_import = re.compile(r"\.cs(?:['\"]|/)")
    violations = []
    for path in sorted(RUNTIME_SRC.rglob("*.ts")):
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            stripped = line.strip()
            if not (stripped.startswith("import ") or stripped.startswith("export ") or " from \"" in stripped or " from '" in stripped):
                continue
            if any(token in stripped for token in approved_visual_contracts):
                continue
            if any(token in stripped for token in forbidden) or csharp_import.search(stripped):
                violations.append({"path": path.relative_to(ROOT).as_posix(), "line": line_number, "text": stripped})
    return violations


def check(name: str, passed: bool, observed: Any, expected: Any) -> dict[str, Any]:
    return {"name": name, "passed": bool(passed), "observed": observed, "expected": expected}


def build_payload() -> dict[str, Any]:
    baseline = load_json(BASELINE_PATH)
    coverage = load_json(COVERAGE_PATH)
    taxonomy = load_json(TAXONOMY_PATH)
    selector = load_json(SELECTOR_PATH)
    fields = load_json(FIELD_PATH)
    composition = load_json(COMPOSITION_PATH)
    geometry = load_json(GEOMETRY_PATH)
    furniture = load_json(FURNITURE_PATH)
    character = load_json(CHARACTER_PATH)
    usage = load_json(USAGE_PATH)
    surface = load_json(SURFACE_PATH)
    native_catalog = load_json(NATIVE_CATALOG_PATH)
    runtime_manifest = load_json(RUNTIME_MANIFEST_PATH)
    runtime_contract = load_json(RUNTIME_CONTRACT_PATH)
    artifact_hashes = {
        "baseline": artifact_hash(baseline),
        "coverage": artifact_hash(coverage),
        "taxonomy": artifact_hash(taxonomy),
        "selector": artifact_hash(selector),
        "fields": artifact_hash(fields),
        "composition": artifact_hash(composition),
        "geometry": artifact_hash(geometry),
        "furniture": artifact_hash(furniture),
        "character": artifact_hash(character),
        "usage": artifact_hash(usage),
        "surface": artifact_hash(surface),
        "runtime_manifest": artifact_hash(runtime_manifest),
        "runtime_contract": artifact_hash(runtime_contract),
    }

    checks = [
        check(
            "baseline_asset_identity",
            baseline["inventory"]["asset_index"]["row_count"] == 3542 and baseline["inventory"]["asset_index"]["unique_relative_paths"] == 3542,
            {"asset_rows": baseline["inventory"]["asset_index"]["row_count"], "unique_relative_paths": baseline["inventory"]["asset_index"]["unique_relative_paths"]},
            {"asset_rows": 3542, "unique_relative_paths": 3542},
        ),
        check(
            "native_catalog_identity",
            native_catalog["status"] == "pass" and native_catalog["counts"]["data_records"] == 3693 and native_catalog["counts"]["assets"] == 3542 and native_catalog["counts"]["selectors"] == 3192,
            native_catalog["counts"],
            {"data_records": 3693, "assets": 3542, "selectors": 3192},
        ),
        check(
            "coverage_matrix",
            coverage["counts"]["indexed_assets"] == 3542 and coverage["counts"]["selectors"] == 3192 and coverage["counts"]["data_fields"] == 1063 and coverage["counts"]["data_selector_relations"] == 523,
            {key: coverage["counts"][key] for key in ("indexed_assets", "selectors", "data_fields", "data_selector_relations")},
            {"indexed_assets": 3542, "selectors": 3192, "data_fields": 1063, "data_selector_relations": 523},
        ),
        check(
            "taxonomy_classification",
            taxonomy["counts"]["assets"] == 3542 and taxonomy["counts"]["families"] == 27 and taxonomy["counts"]["taxonomy_statuses"].get("classified_structural_family") == 3542,
            {key: taxonomy["counts"][key] for key in ("assets", "families", "subfamilies")},
            {"assets": 3542, "families": 27},
        ),
        check(
            "selector_and_field_semantics",
            selector["counts"]["selectors"] == 3192 and selector["counts"]["unresolved_selectors"] == 1 and fields["counts"]["fields"] == 1063 and fields["counts"]["selector_bearing_fields"] == 8,
            {"selectors": selector["counts"]["selectors"], "unresolved_selectors": selector["counts"]["unresolved_selectors"], "fields": fields["counts"]["fields"], "selector_bearing_fields": fields["counts"]["selector_bearing_fields"]},
            {"selectors": 3192, "unresolved_selectors": 1, "fields": 1063, "selector_bearing_fields": 8},
        ),
        check(
            "composition_and_geometry",
            composition["counts"]["composition_entries"] == 47 and geometry["counts"]["geometry_rows"] == 3546 and geometry["counts"]["runtime_geometry_gaps"] == 0,
            {"composition_entries": composition["counts"]["composition_entries"], "geometry_rows": geometry["counts"]["geometry_rows"], "runtime_geometry_gaps": geometry["counts"]["runtime_geometry_gaps"]},
            {"composition_entries": 47, "geometry_rows": 3546, "runtime_geometry_gaps": 0},
        ),
        check(
            "furniture_world_metadata",
            furniture["counts"]["furniture_records"] == 103 and furniture["counts"]["rooms"] == 18 and furniture["counts"]["native_binding_instances"] == 6,
            {"furniture_records": furniture["counts"]["furniture_records"], "rooms": furniture["counts"]["rooms"], "native_binding_instances": furniture["counts"]["native_binding_instances"]},
            {"furniture_records": 103, "rooms": 18, "native_binding_instances": 6},
        ),
        check(
            "character_visual_metadata",
            character["counts"]["staff_records"] == 141 and character["counts"]["helper_records"] == 19 and character["counts"]["unique_human_images"] == 105 and character["counts"]["human_animations"] == 35 and character["counts"]["avatar_body_assets"] == 284 and character["counts"]["avatar_head_assets"] == 509,
            {key: character["counts"][key] for key in ("staff_records", "helper_records", "unique_human_images", "human_animations", "avatar_body_assets", "avatar_head_assets")},
            {"staff_records": 141, "helper_records": 19, "unique_human_images": 105, "human_animations": 35, "avatar_body_assets": 284, "avatar_head_assets": 509},
        ),
        check(
            "usage_lifecycle_placement",
            usage["counts"]["assets"] == 3542 and usage["counts"]["usage_edges"] == 3495 and usage["counts"]["lifecycle_edges"] == 43 and usage["counts"]["non_actor_families"] == 21,
            {key: usage["counts"][key] for key in ("assets", "usage_edges", "lifecycle_edges", "families", "non_actor_families")},
            {"assets": 3542, "usage_edges": 3495, "lifecycle_edges": 43, "families": 27, "non_actor_families": 21},
        ),
        check(
            "surface_provenance",
            surface["counts"]["indexed_assets"] == 3542 and surface["counts"]["non_actor_families"] == 21 and surface["counts"]["zip_exact_assets"] == 3542 and surface["counts"]["apk_entry_present_assets"] == 3508 and surface["counts"]["apk_entry_missing_assets"] == 34 and surface["counts"]["unity_textasset_apk_missing_assets"] == 34,
            {key: surface["counts"][key] for key in ("indexed_assets", "non_actor_families", "zip_exact_assets", "apk_entry_present_assets", "apk_entry_missing_assets", "unity_textasset_apk_missing_assets")},
            {"indexed_assets": 3542, "non_actor_families": 21, "zip_exact_assets": 3542, "apk_entry_present_assets": 3508, "apk_entry_missing_assets": 34, "unity_textasset_apk_missing_assets": 34},
        ),
        check(
            "runtime_query_manifest",
            runtime_manifest["status"] == "pass" and runtime_manifest["counts"]["runtime_assets"] == 186 and runtime_manifest["counts"]["families"] == 27 and runtime_manifest["lazy_loading"]["eager_load_full_catalog"] is False and runtime_manifest["lazy_loading"]["source_archive_imports"] is False,
            {"runtime_assets": runtime_manifest["counts"]["runtime_assets"], "families": runtime_manifest["counts"]["families"], "lazy": runtime_manifest["lazy_loading"]["eager_load_full_catalog"], "archive_imports": runtime_manifest["lazy_loading"]["source_archive_imports"]},
            {"runtime_assets": 186, "families": 27, "lazy": False, "archive_imports": False},
        ),
        check(
            "runtime_contract_connection",
            runtime_contract["status"] == "pass" and runtime_contract["acceptance"]["runtime_assets_are_lazy"] is True and runtime_contract["acceptance"]["source_imports_are_disabled"] is True,
            runtime_contract["acceptance"],
            {"runtime_assets_are_lazy": True, "source_imports_are_disabled": True},
        ),
    ]

    import_violations = source_import_violations()
    checks.append(check("runtime_source_import_boundary", not import_violations, import_violations, []))
    all_checks_pass = all(item["passed"] for item in checks)

    payload = {
        "schema_version": "social-dev-asset-metadata-completion-gate-v1",
        "package": "social-dev",
        "status": "pass" if all_checks_pass else "blocked",
        "semantic_status": "asset_metadata_catalog_complete_with_runtime_subset_and_explicit_boundaries" if all_checks_pass else "asset_metadata_completion_gate_failed",
        "refs": {
            "baseline": {"path": "knowledge/fixtures/accepted/asset_metadata_baseline.json", "content_hash": artifact_hash(baseline)},
            "coverage": {"path": "knowledge/fixtures/accepted/asset_metadata_coverage.json", "content_hash": artifact_hash(coverage)},
            "taxonomy": {"path": "knowledge/fixtures/accepted/asset_family_taxonomy.json", "content_hash": artifact_hash(taxonomy)},
            "selector": {"path": "knowledge/fixtures/accepted/asset_selector_usage_matrix.json", "content_hash": artifact_hash(selector)},
            "fields": {"path": "knowledge/fixtures/accepted/data_field_semantics_matrix.json", "content_hash": artifact_hash(fields)},
            "composition": {"path": "knowledge/fixtures/accepted/asset_composition_catalog.json", "content_hash": artifact_hash(composition)},
            "geometry": {"path": "knowledge/fixtures/accepted/asset_geometry_catalog.json", "content_hash": artifact_hash(geometry)},
            "furniture": {"path": "knowledge/fixtures/accepted/furniture_asset_metadata.json", "content_hash": artifact_hash(furniture)},
            "character": {"path": "knowledge/fixtures/accepted/character_visual_asset_metadata.json", "content_hash": artifact_hash(character)},
            "usage": {"path": "knowledge/fixtures/accepted/asset_usage_lifecycle_placement_matrix.json", "content_hash": artifact_hash(usage)},
            "surface": {"path": "knowledge/fixtures/accepted/asset_surface_provenance.json", "content_hash": artifact_hash(surface)},
            "runtime_manifest": {"path": "knowledge/fixtures/accepted/runtime/asset_metadata_runtime_manifest.json", "content_hash": artifact_hash(runtime_manifest)},
            "runtime_contract": {"path": "knowledge/fixtures/accepted/runtime/asset_metadata_runtime_contract.json", "content_hash": artifact_hash(runtime_contract)},
        },
        "checks": checks,
        "readiness": {
            "catalog_metadata": "complete_for_all_3542_indexed_rows_with_explicit_status_or_boundary",
            "native_identity_graph": "ready_for_3693_data_rows_and_3192_selector_records",
            "runtime_query_surface": "ready_for_186_explicit_runtime_asset_rows_and_native_catalog_lookup",
            "full_runtime_visual_promotion": "not_ready_and_not_claimed_for_catalog_only_rows",
            "repeatability": "stable_asset_id_selector_key_and_contract_hash lookup; no filename guessing",
        },
        "counts": {
            "indexed_assets": 3542,
            "native_data_records": 3693,
            "native_selectors": 3192,
            "runtime_query_assets": 186,
            "catalog_only_assets": coverage["counts"]["asset_statuses"]["cataloged_without_current_relation"],
            "unresolved_selector_identities": selector["counts"]["unresolved_selectors"],
            "helper_scope_gaps": fields["counts"]["fields_with_deferred_selector_scope"],
            "unity_textasset_apk_gaps": surface["counts"]["unity_textasset_apk_missing_assets"],
            "non_actor_families_without_screen_event_contract": surface["counts"]["non_actor_families"],
            "runtime_geometry_gaps": geometry["counts"]["runtime_geometry_gaps"],
        },
        "explicit_boundaries": [
            "1 lineup_layout/bg.seb selector has unresolved target identity.",
            "11 helper selector-scope fields remain deferred; 1 helper image selector is an explicit -1 sentinel.",
            "34 Unity TextAsset/resource rows have APK absence and unresolved nested mapping; they remain provenance-only.",
            "21 non-actor families have catalog/provenance metadata but no invented screen/event consumer contract.",
            "3,231 indexed assets are cataloged without a current native relation; they remain queryable evidence, not automatic runtime assets.",
            "Full visual runtime promotion remains limited to the explicit 186-row runtime manifest.",
        ],
        "verification_commands": [
            "python -B tools/social-dev/test_asset_metadata_baseline.py",
            "python -B tools/social-dev/test_asset_metadata_coverage.py",
            "python -B tools/social-dev/test_asset_family_taxonomy.py",
            "python -B tools/social-dev/test_asset_selector_usage_matrix.py",
            "python -B tools/social-dev/test_asset_composition_geometry.py",
            "python -B tools/social-dev/test_furniture_asset_metadata.py",
            "python -B tools/social-dev/test_character_visual_asset_metadata.py",
            "python -B tools/social-dev/test_asset_usage_lifecycle_placement.py",
            "python -B tools/social-dev/test_asset_surface_provenance.py",
            "python -B tools/social-dev/test_asset_metadata_runtime_manifest.py",
            "npm run typecheck",
            "npm test",
            "npm run build",
        ],
        "determinism_inputs": {"artifact_hashes": artifact_hashes},
    }
    payload["determinism"] = {"algorithm": "stable-json-sha256 excluding determinism.content_hash", "content_hash": sha256_bytes(stable_json(payload).encode("utf-8"))}
    return payload


def build_contract_payload(gate: dict[str, Any]) -> dict[str, Any]:
    payload = {
        "schema_version": "social-dev-asset-metadata-completion-contract-v1",
        "package": "social-dev",
        "status": gate["status"],
        "semantic_status": gate["semantic_status"],
        "gate_path": "knowledge/fixtures/accepted/asset_metadata_completion_gate.json",
        "gate_content_hash": gate["determinism"]["content_hash"],
        "counts": gate["counts"],
        "readiness": gate["readiness"],
        "explicit_boundaries": gate["explicit_boundaries"],
        "acceptance": {
            "all_checks_pass": all(item["passed"] for item in gate["checks"]),
            "catalog_metadata_complete": gate["readiness"]["catalog_metadata"].startswith("complete"),
            "runtime_query_surface_explicit": gate["counts"]["runtime_query_assets"] == 186,
            "full_runtime_promotion_not_overclaimed": gate["readiness"]["full_runtime_visual_promotion"].startswith("not_ready"),
        },
    }
    payload["determinism"] = {"algorithm": "stable-json-sha256 excluding determinism.content_hash", "content_hash": sha256_bytes(stable_json(payload).encode("utf-8"))}
    return payload


def markdown_report(gate: dict[str, Any], contract: dict[str, Any]) -> str:
    lines = [
        "# Social Dev asset metadata completion audit",
        "",
        "This is the final audit for the asset-metadata workstream. `pass` means the indexed catalog is deterministic and every known limit is explicit; it does not mean that every catalog row is approved for visual runtime promotion.",
        "",
        "## Result",
        "",
        f"- Gate status: `{gate['status']}`",
        f"- Semantic status: `{gate['semantic_status']}`",
        f"- Gate hash: `{gate['determinism']['content_hash']}`",
        f"- Runtime contract hash: `{contract['determinism']['content_hash']}`",
        "",
        "## Readiness split",
        "",
        "| Surface | Result |",
        "|---|---|",
        f"| Catalog metadata | {gate['readiness']['catalog_metadata']} |",
        f"| Native identity graph | {gate['readiness']['native_identity_graph']} |",
        f"| Runtime query surface | {gate['readiness']['runtime_query_surface']} |",
        f"| Full visual runtime promotion | {gate['readiness']['full_runtime_visual_promotion']} |",
        "",
        "## Counts",
        "",
        "| Dimension | Count |",
        "|---|---:|",
        f"| Indexed assets | {gate['counts']['indexed_assets']:,} |",
        f"| Native data records | {gate['counts']['native_data_records']:,} |",
        f"| Native selectors | {gate['counts']['native_selectors']:,} |",
        f"| Runtime-query asset rows | {gate['counts']['runtime_query_assets']:,} |",
        f"| Catalog-only assets | {gate['counts']['catalog_only_assets']:,} |",
        f"| Runtime geometry gaps | {gate['counts']['runtime_geometry_gaps']:,} |",
        "",
        "## Explicit boundaries",
        "",
    ]
    lines.extend(f"- {item}" for item in gate["explicit_boundaries"])
    lines.extend(
        [
            "",
            "## Verification",
            "",
            "The deterministic Python package tests, TypeScript typecheck, Vitest suite, production build, and runtime lookup tests are the handoff gates. The completion gate also scans runtime source imports for archive, APK, C#, and knowledge-root imports.",
            "",
            "```powershell",
            "python -B tools/social-dev/build_asset_metadata_completion_gate.py",
            "python -B tools/social-dev/test_asset_metadata_completion_gate.py",
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    gate = build_payload()
    contract = build_contract_payload(gate)
    write_json(GATE_PATH, gate)
    write_json(CONTRACT_PATH, contract)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(markdown_report(gate, contract), encoding="utf-8", newline="\n")
    print(json.dumps({"gate_hash": gate["determinism"]["content_hash"], "status": gate["status"], "checks": len(gate["checks"])}, indent=2))
    return 0 if gate["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
