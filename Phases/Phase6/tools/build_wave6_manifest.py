"""Build the deterministic Wave 6 source/artifact manifest."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
PHASE6 = ROOT / "Phases" / "Phase6"
OUTPUT = PHASE6 / "artifacts" / "wave6_build_manifest.json"

FILES = [
    "Phases/Phase5/runtime/runtime.js",
    "Phases/Phase5/runtime/app.js",
    "Phases/Phase5/runtime/index.html",
    "Phases/Phase5/runtime/style.css",
    "Phases/Phase6/runtime/task_system.js",
    "Phases/Phase6/runtime/task_storage.js",
    "Phases/Phase6/runtime/task_repository.js",
    "Phases/Phase6/tests/test_wave6_task_system.js",
    "Phases/Phase6/tests/test_wave6_contract.py",
    "Phases/Phase6/tools/build_wave6_manifest.py",
    "Phases/Phase6/artifacts/wave6_task_contract.json",
    "Phases/Phase6/artifacts/wave6_assignment_rules.json",
    "Phases/Phase6/artifacts/wave6_event_catalog.json",
    "Phases/Phase6/artifacts/wave6_notification_contract.json",
    "Phases/Phase6/artifacts/wave6_queue_fixture.json",
    "Phases/Phase6/artifacts/wave6_interaction_report.json",
    "Phases/Phase6/artifacts/wave6_gap_register.json",
    "Phases/Phase6/artifacts/wave6_repository_contract.json",
    "Phases/Phase6/artifacts/wave6_permission_policy.json",
    "Phases/Phase6/artifacts/wave6_migration_fixture.json",
    "Phases/Phase6/docs/wave6_plan.md",
    "Phases/Phase6/docs/wave6_runtime_architecture.md",
    "Phases/Phase6/docs/wave6_closure_report.md",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build() -> dict:
    records = []
    for relative in FILES:
        path = ROOT / relative
        records.append({
            "path": relative.replace("\\", "/"),
            "exists": path.is_file(),
            "sha256": sha256(path) if path.is_file() else "",
            "bytes": path.stat().st_size if path.is_file() else 0,
        })
    return {
        "schema_version": "wave6-build-manifest-v1",
        "phase": "Phase6",
        "wave": "Wave6",
        "stage": "W6-C0..C7+W6.1-task-system-dashboard-hardening",
        "status": "complete_with_known_limitations",
        "legacy_equivalence": False,
        "source_roots_read_only": True,
        "files": records,
    }


if __name__ == "__main__":
    OUTPUT.write_text(json.dumps(build(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}")
