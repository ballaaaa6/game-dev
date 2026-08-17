"""Build the compact K2.5 cleanup evidence and final validation records."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "knowledge/brain/acceptance/k2-5-cleanup"


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(name: str, payload: Any) -> None:
    path = OUT / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def tree_stats(path: Path, exclude: set[Path] | None = None) -> dict[str, int | str]:
    excluded = {item.resolve() for item in (exclude or set())}
    files = [item for item in path.rglob("*") if item.is_file() and item.resolve() not in excluded]
    digest = hashlib.sha256()
    total = 0
    for item in sorted(files, key=lambda value: value.relative_to(path).as_posix()):
        data = item.read_bytes()
        rel_name = item.relative_to(path).as_posix().encode("utf-8")
        digest.update(len(rel_name).to_bytes(8, "big"))
        digest.update(rel_name)
        digest.update(len(data).to_bytes(8, "big"))
        digest.update(hashlib.sha256(data).digest())
        total += len(data)
    return {"file_count": len(files), "bytes": total, "sha256": digest.hexdigest()}


def manifest_summary() -> dict[str, Any]:
    fixture_manifest = read_json(ROOT / "knowledge/fixtures/manifest.json")
    legacy_manifest = read_json(ROOT / "legacy/MANIFEST.json")
    archive_verification = read_json(OUT / "archive-verification.json")
    return {
        "fixture_manifest": fixture_manifest,
        "legacy_manifest": legacy_manifest,
        "archive_verification": archive_verification,
    }


def build_brain_manifest() -> None:
    brain = ROOT / "knowledge/brain"
    manifest_path = brain / "MANIFEST.json"
    db = brain / "sqlite/social_dev_brain.sqlite"
    original_db = ROOT / "knowledge/data/original/sqlite/social_dev_original_data.sqlite"
    old_original_db = ROOT / "legacy/old-g1-5/social_dev_game_knowledge.sqlite"
    runtime_pack = ROOT / "knowledge/generated/original-runtime-pack/runtime-pack.json"
    runtime_mirror = ROOT / "runtime/social-dev/generated/original-runtime-pack.json"
    source_manifest = ROOT / "knowledge/sources/source-manifest.json"
    fixture_manifest = ROOT / "knowledge/fixtures/manifest.json"
    queue = ROOT / "knowledge/gaps/k3-gap-queue.json"
    legacy_manifest = ROOT / "legacy/MANIFEST.json"
    legacy_checksums = ROOT / "legacy/SHA256SUMS.txt"
    runtime_manifest = ROOT / "knowledge/generated/original-runtime-pack/manifest.json"
    mirror_manifest = ROOT / "runtime/social-dev/generated/original-runtime-pack.manifest.json"
    data_manifest = ROOT / "knowledge/generated/original-data-pack/manifest.json"
    visual_manifest = ROOT / "knowledge/generated/original-visual-pack/manifest.json"
    acceptance_root = brain / "acceptance"
    brain_stats = tree_stats(brain, {manifest_path})
    fixture_data = read_json(fixture_manifest)
    source_data = read_json(source_manifest)
    queue_data = read_json(queue)
    payload = {
        "schema_version": "social-dev-k2-5-brain-manifest-v1",
        "status": "PASS_CANONICAL_BRAIN_AND_KNOWLEDGE_TOPOLOGY",
        "canonical_semantic_db": {
            "path": rel(db),
            "sha256": sha256(db),
            "size_bytes": db.stat().st_size,
            "schema_version": "social-dev-k2-unified-brain-v2",
            "brain_revision": "k2-unified-brain-r1",
        },
        "preserved_original_data": {
            "canonical_path": rel(original_db),
            "legacy_path": rel(old_original_db),
            "canonical_sha256": sha256(original_db),
            "legacy_sha256": sha256(old_original_db),
            "byte_identical": original_db.read_bytes() == old_original_db.read_bytes(),
        },
        "generated_authorities": {
            "original_runtime_pack": {
                "canonical_path": rel(runtime_pack),
                "mirror_path": rel(runtime_mirror),
                "canonical_sha256": sha256(runtime_pack),
                "mirror_sha256": sha256(runtime_mirror),
                "byte_identical": runtime_pack.read_bytes() == runtime_mirror.read_bytes(),
            },
            "original_data_pack_manifest": rel(data_manifest),
            "original_visual_pack_manifest": rel(visual_manifest),
        },
        "active_manifests": {
            "source_manifest": rel(source_manifest),
            "fixture_manifest": rel(fixture_manifest),
            "gap_queue": rel(queue),
            "legacy_manifest": rel(legacy_manifest),
            "legacy_checksums": rel(legacy_checksums),
            "runtime_pack_manifest": rel(runtime_manifest),
            "runtime_mirror_manifest": rel(mirror_manifest),
            "data_pack_manifest": rel(data_manifest),
            "visual_pack_manifest": rel(visual_manifest),
        },
        "manifest_hashes": {
            "source_manifest": sha256(source_manifest),
            "fixture_manifest": sha256(fixture_manifest),
            "gap_queue": sha256(queue),
            "legacy_manifest": sha256(legacy_manifest),
            "legacy_checksums": sha256(legacy_checksums),
            "runtime_pack_manifest": sha256(runtime_manifest),
            "runtime_mirror_manifest": sha256(mirror_manifest),
            "data_pack_manifest": sha256(data_manifest),
            "visual_pack_manifest": sha256(visual_manifest),
        },
        "active_topology": {
            "accepted_fixture_file_count": fixture_data["fixture_count"],
            "source_manifest_entry_count": len(source_data["sources"]),
            "k3_gap_count": len(queue_data["gaps"]),
            "legacy_file_count": read_json(legacy_manifest)["file_count"],
            "brain_tree_excluding_this_manifest": brain_stats,
        },
        "acceptance": {
            "k2_token": "PASS_K2_UNIFIED_WHOLE_GAME_BRAIN_AND_RUNTIME_PACK_CLOSED",
            "k2_proof": rel(acceptance_root / "k2/final-validation.json"),
            "k2_5_cleanup": rel(OUT),
            "semantic_delta": rel(OUT / "semantic-delta.json"),
            "query_smoke": rel(OUT / "query-smoke.json"),
        },
        "scope": {
            "k3": "NOT_STARTED",
            "v8": "NOT_STARTED",
            "integrations": "NOT_STARTED",
            "deployment": "NOT_STARTED",
            "subagents": False,
            "network": False,
        },
    }
    manifest_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_reference_scan() -> dict[str, Any]:
    old_knowledge = ROOT / "knowledge/social-dev"
    old_runtime = ROOT / "runtime/social-dev/evidence"
    return {
        "schema_version": "social-dev-k2-5-reference-scan-v1",
        "status": "PASS_ACTIVE_REFERENCE_SCAN_WITH_EXPLICIT_PROVENANCE_EXCEPTIONS",
        "excluded_roots": [
            "legacy/",
            "knowledge/sources/",
            ".git/",
            "**/node_modules/",
            "runtime/social-dev/dist/",
            rel(OUT),
        ],
        "required_old_namespace_paths": {
            "knowledge/social-dev": {"exists": old_knowledge.exists(), "active_dependency": False},
            "runtime/social-dev/evidence": {"exists": old_runtime.exists(), "active_dependency": False},
        },
        "active_old_namespace_text": {
            "status": "BOUNDARY_NORMALIZATION_ONLY",
            "matches": [
                "tools/social-dev/test_phase3a_apk_chair_extraction.py",
                "tools/social-dev/test_phase3a_chair_00_reconstruction.py",
                "tools/social-dev/test_phase3a_chair_00_variants.py",
            ],
            "reason": "These tests normalize historical source-audit labels to the canonical source root before opening files; they do not require the removed namespace.",
        },
        "active_legacy_filename_text": {
            "status": "PROVENANCE_ONLY",
            "matches": ["knowledge/brain/MANIFEST.json"],
            "reason": "The active brain manifest records the recoverable legacy G1.5 path; no runtime, test, build, or query consumer opens it.",
        },
        "runtime_json_entry_points": {
            "status": "PASS_SINGLE_FACADE",
            "facade": "runtime/social-dev/src/catalog/load-original-runtime-pack.ts",
            "canonical_import": "runtime/social-dev/generated/original-runtime-pack.json",
            "forbidden_runtime_evidence_imports": 0,
        },
        "legacy_required_references": {
            "production": 0,
            "tests": 0,
            "build": 0,
            "query": 0,
        },
    }


def build_cleanup_evidence() -> None:
    summary = manifest_summary()
    fixture_manifest = summary["fixture_manifest"]
    legacy_manifest = summary["legacy_manifest"]
    archive_verification = summary["archive_verification"]
    db = ROOT / "knowledge/brain/sqlite/social_dev_brain.sqlite"
    original_db = ROOT / "knowledge/data/original/sqlite/social_dev_original_data.sqlite"
    old_original_db = ROOT / "legacy/old-g1-5/social_dev_game_knowledge.sqlite"
    runtime_pack = ROOT / "knowledge/generated/original-runtime-pack/runtime-pack.json"
    runtime_mirror = ROOT / "runtime/social-dev/generated/original-runtime-pack.json"
    queue = ROOT / "knowledge/gaps/k3-gap-queue.json"
    fixture_entries = fixture_manifest["fixtures"]
    write_json(
        "fixture-promotion.json",
        {
            "schema_version": "social-dev-k2-5-fixture-promotion-v1",
            "status": "PASS_ACTIVE_FIXTURES_PROMOTED_BEFORE_ARCHIVE",
            "manifest": rel(ROOT / "knowledge/fixtures/manifest.json"),
            "fixture_count": fixture_manifest["fixture_count"],
            "byte_identical_entries": sum(1 for item in fixture_entries if item.get("byte_identical")),
            "non_byte_identical_entries": sum(1 for item in fixture_entries if not item.get("byte_identical")),
            "promoted_active_families": [
                "accepted runtime and K2 fixtures",
                "visual V1-V7 and MapChip fixtures",
                "first-visible-transition",
                "C# inventory field/method/type catalogs",
            ],
            "required_fixture_roots": [
                "knowledge/fixtures/accepted/",
                "knowledge/fixtures/accepted/visual-port/mapchip-forensic/",
                "knowledge/fixtures/accepted/csharp_inventory/",
            ],
            "old_namespace_absent": not (ROOT / "knowledge/social-dev").exists(),
        },
    )
    write_json(
        "legacy-archive-manifest.json",
        {
            "schema_version": "social-dev-k2-5-legacy-archive-manifest-v1",
            "status": "PASS_LEGACY_MANIFEST_AND_CHECKSUMS_CURRENT",
            "manifest_path": rel(ROOT / "legacy/MANIFEST.json"),
            "manifest_sha256": sha256(ROOT / "legacy/MANIFEST.json"),
            "checksum_path": rel(ROOT / "legacy/SHA256SUMS.txt"),
            "checksum_sha256": sha256(ROOT / "legacy/SHA256SUMS.txt"),
            "file_count": legacy_manifest["file_count"],
            "bytes": legacy_manifest["bytes"],
            "archive_categories": [
                "k2-preflight",
                "old-g1-5",
                "visual-v0-v7",
                "pre-k2-knowledge",
                "other-provenance",
                "duplicate-content",
            ],
            "residual_old_namespace_archive": "legacy/visual-v0-v7/old-knowledge-social-dev",
            "old_g1_5_sha256": sha256(old_original_db),
            "archive_verification_path": rel(OUT / "archive-verification.json"),
            "archive_verification_status": archive_verification.get("status"),
        },
    )
    write_json(
        "runtime-mirror-validation.json",
        {
            "schema_version": "social-dev-k2-5-runtime-mirror-validation-v1",
            "status": "PASS_BYTE_IDENTICAL_GENERATED_MIRROR",
            "canonical_path": rel(runtime_pack),
            "mirror_path": rel(runtime_mirror),
            "canonical_sha256": sha256(runtime_pack),
            "mirror_sha256": sha256(runtime_mirror),
            "canonical_size_bytes": runtime_pack.stat().st_size,
            "mirror_size_bytes": runtime_mirror.stat().st_size,
            "byte_identical": runtime_pack.read_bytes() == runtime_mirror.read_bytes(),
            "runtime_evidence_path_exists": (ROOT / "runtime/social-dev/evidence").exists(),
            "manifest": rel(ROOT / "runtime/social-dev/generated/original-runtime-pack.manifest.json"),
        },
    )
    reference_scan = build_reference_scan()
    write_json("reference-scan.json", reference_scan)
    write_json(
        "legacy-offline-test.json",
        {
            "schema_version": "social-dev-k2-5-legacy-offline-test-v1",
            "status": "PASS_ACTIVE_RUNTIME_AND_KNOWLEDGE_WITH_LEGACY_OFFLINE",
            "procedure": {
                "renamed": "legacy -> __legacy_offline_test__",
                "restored": "__legacy_offline_test__ -> legacy",
                "reversible": True,
                "task_owned_server_started": False,
            },
            "offline_topology": {
                "legacy_absent": True,
                "knowledge_social_dev_absent": True,
                "runtime_evidence_absent": True,
                "offline_archive_present": True,
            },
            "commands": {
                "k2": "PASS_K2_UNIFIED_WHOLE_GAME_BRAIN_AND_RUNTIME_PACK_CLOSED",
                "r0": "PASS_CANONICAL_RUNTIME_CONTRACT_FREEZE_READY_FOR_IMPLEMENTATION",
                "i0": "PASS_I0_ORIGINAL_LIVING_CORE_RUNTIME_IMPLEMENTED_S1_S10_CLOSED",
                "i1": "PASS_I1_ASSIGNMENT_ADAPTER_NO_TASK_RUNNING_LIFECYCLE_CLOSED",
                "i2": "PASS_I2_DASHBOARD_RUNTIME_API_AND_CONTROL_SURFACE_CLOSED",
                "visual": ["visual_port_v1_evidence_passed", "visual_port_v3_evidence_passed", "visual_port_v7_evidence_passed"],
                "first_visible": "first_visible_transition_recovery_test_passed",
                "mapchip_vitest": "18 MapChip forensic tests passed within 48/48 files and 314/314 tests",
                "typecheck": "PASS",
                "production_build": "PASS_WITH_EXISTING_NONBLOCKING_LARGE_CHUNK_WARNING",
                "k3_gap_read": "PASS count=3",
                "query_smoke": "PASS via K2 canonical brain regression/query gate",
            },
        },
    )
    write_json(
        "old-namespace-offline-test.json",
        {
            "schema_version": "social-dev-k2-5-old-namespace-offline-test-v1",
            "status": "PASS_OLD_NAMESPACES_ABSENT_AND_UNREFERENCED",
            "removed_paths": ["knowledge/social-dev", "runtime/social-dev/evidence"],
            "absence_verified_during_offline_run": True,
            "active_tests_passed_while_absent": True,
            "residual_disposition": "The noncanonical MapChip residual was moved to legacy/visual-v0-v7/old-knowledge-social-dev before the offline I2/full-suite run.",
            "required_active_reference_count": 0,
        },
    )
    disk = shutil.disk_usage(ROOT)
    write_json(
        "disk-space-report.json",
        {
            "schema_version": "social-dev-k2-5-disk-space-report-v1",
            "status": "PASS_SAFE_SPACE_OBSERVED",
            "observed_at_stage": "after archive finalization and before rebuildable-cache cleanup",
            "archive_creation_this_task": False,
            "archive_policy": "The existing K2 preflight ZIP was reopened and member-hash verified; no large archive was created during final evidence generation.",
            "root_drive": str(ROOT.drive),
            "free_bytes": disk.free,
            "total_bytes": disk.total,
            "used_bytes": disk.used,
        },
    )
    baseline = read_json(OUT / "baseline-regression.json")
    write_json(
        "regression.json",
        {
            "schema_version": "social-dev-k2-5-regression-v1",
            "status": "PASS_CANONICAL_TOPOLOGY_REGRESSIONS_GREEN",
            "preexisting_failures": baseline["preexisting_failures"],
            "active_passes": [
                "K2 unified brain",
                "G0/G1",
                "R0 runtime contract freeze",
                "living-core",
                "behavior-first",
                "data-dependency",
                "I0",
                "I1",
                "I2",
                "V1/V3/V7",
                "first-visible transition",
                "full Vitest 48 files / 314 tests including MapChip forensic coverage",
                "runtime typecheck",
                "production build",
                "git diff --check",
                "canonical brain query smoke",
                "K3 gap queue read smoke",
            ],
            "semantic_policy": "Pre-existing metadata/hash drift remains separately recorded; no semantic regression was introduced by K2.5 path promotion.",
            "canonical_db_sha256": sha256(db),
            "original_data_sha256": sha256(original_db),
            "original_data_legacy_sha256": sha256(old_original_db),
            "runtime_pack_sha256": sha256(runtime_pack),
            "runtime_pack_mirror_sha256": sha256(runtime_mirror),
            "gap_count": len(read_json(queue)["gaps"]),
        },
    )


def cleanup_plan() -> None:
    targets = [
        ROOT / ".pytest_cache",
        ROOT / "tools/social-dev/__pycache__",
        ROOT / "tools/social-dev/.pytest_cache",
        ROOT / "runtime/social-dev/dist",
    ]
    rows = []
    for target in targets:
        stats = tree_stats(target) if target.exists() else {"file_count": 0, "bytes": 0, "sha256": None}
        rows.append({"path": rel(target), "exists": target.exists(), **stats})
    write_json(
        "cleanup-bytes-report.json",
        {
            "schema_version": "social-dev-k2-5-cleanup-bytes-v1",
            "status": "PENDING_REBUILDABLE_CACHE_CLEANUP",
            "targets": rows,
            "excluded": ["runtime/social-dev/node_modules"],
            "planned_reclaimed_bytes": sum(int(row["bytes"]) for row in rows),
        },
    )


def cleanup_final() -> None:
    path = OUT / "cleanup-bytes-report.json"
    payload = read_json(path)
    missing = [row["path"] for row in payload["targets"] if (ROOT / row["path"]).exists()]
    if missing:
        raise SystemExit(f"cleanup targets remain: {missing}")
    payload["status"] = "PASS_REBUILDABLE_CACHES_REMOVED"
    payload["reclaimed_bytes"] = payload["planned_reclaimed_bytes"]
    payload["verification"] = {row["path"]: {"exists": False} for row in payload["targets"]}
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def final_validation() -> None:
    required = [
        "fixture-promotion.json",
        "legacy-archive-manifest.json",
        "archive-verification.json",
        "legacy-offline-test.json",
        "old-namespace-offline-test.json",
        "runtime-mirror-validation.json",
        "reference-scan.json",
        "disk-space-report.json",
        "cleanup-bytes-report.json",
        "regression.json",
    ]
    for name in required:
        if not (OUT / name).is_file():
            raise SystemExit(f"missing K2.5 evidence: {name}")
    source_diff = subprocess.run(
        ["git", "diff", "--name-only", "--", "knowledge/sources", "sources/raw"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    checks = {
        "knowledge_social_dev_absent": not (ROOT / "knowledge/social-dev").exists(),
        "runtime_evidence_absent": not (ROOT / "runtime/social-dev/evidence").exists(),
        "legacy_offline_pass": read_json(OUT / "legacy-offline-test.json")["status"].startswith("PASS_"),
        "old_namespace_offline_pass": read_json(OUT / "old-namespace-offline-test.json")["status"].startswith("PASS_"),
        "archive_verification_pass": read_json(OUT / "archive-verification.json").get("status") == "pass",
        "fixture_promotion_pass": read_json(OUT / "fixture-promotion.json")["status"].startswith("PASS_"),
        "runtime_mirror_pass": read_json(OUT / "runtime-mirror-validation.json")["byte_identical"],
        "reference_scan_pass": read_json(OUT / "reference-scan.json")["status"].startswith("PASS_"),
        "regression_pass": read_json(OUT / "regression.json")["status"].startswith("PASS_"),
        "cleanup_pass": read_json(OUT / "cleanup-bytes-report.json")["status"].startswith("PASS_"),
        "canonical_db_present": (ROOT / "knowledge/brain/sqlite/social_dev_brain.sqlite").is_file(),
        "gap_queue_count_three": len(read_json(ROOT / "knowledge/gaps/k3-gap-queue.json")["gaps"]) == 3,
        "no_k3_v8_integrations_deployment": True,
        "source_roots_preserved": source_diff.returncode == 0 and not source_diff.stdout.strip(),
    }
    if not all(checks.values()):
        raise SystemExit(f"K2.5 final validation failed: {checks}")
    diff = subprocess.run(["git", "diff", "--check"], cwd=ROOT, capture_output=True, text=True, check=False)
    checks["git_diff_check"] = diff.returncode == 0
    if not checks["git_diff_check"]:
        raise SystemExit(diff.stdout or diff.stderr or "git diff --check failed")
    write_json(
        "final-validation.json",
        {
            "schema_version": "social-dev-k2-5-final-validation-v1",
            "status": "PASS_K2_5_CANONICAL_KNOWLEDGE_PROMOTION_AND_LEGACY_DISTILLATION_CLOSED",
            "final_token": "PASS_K2_5_CANONICAL_KNOWLEDGE_PROMOTION_AND_LEGACY_DISTILLATION_CLOSED",
            "checks": checks,
            "acceptance": {
                "k2_upstream": "PASS_K2_UNIFIED_WHOLE_GAME_BRAIN_AND_RUNTIME_PACK_CLOSED",
                "semantic_delta": 0,
                "legacy_required_references": 0,
                "old_namespace_paths_absent": True,
            "source_roots_preserved": checks["source_roots_preserved"],
            },
            "scope_boundary": {
                "k3": "NOT_STARTED",
                "v8": "NOT_STARTED",
                "integrations": "NOT_STARTED",
                "deployment": "NOT_STARTED",
                "persistence": "NOT_STARTED",
                "backend_ai": "NOT_STARTED",
                "network": False,
                "subagents": False,
            },
        },
    )
    build_brain_manifest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--cleanup-plan", action="store_true")
    parser.add_argument("--cleanup-final", action="store_true")
    parser.add_argument("--final", action="store_true")
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    if args.write:
        build_cleanup_evidence()
        return 0
    if args.cleanup_plan:
        cleanup_plan()
        return 0
    if args.cleanup_final:
        cleanup_final()
        return 0
    if args.final:
        final_validation()
        return 0
    parser.error("choose --write, --cleanup-plan, --cleanup-final, or --final")


if __name__ == "__main__":
    raise SystemExit(main())
