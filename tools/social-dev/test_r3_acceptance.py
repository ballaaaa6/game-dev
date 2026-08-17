"""Validate the tracked R3 acceptance package and its closure gates."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


TOKEN = "PASS_R3_WHOLE_GAME_CFG_REPAIR_CLOSED"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate R3 acceptance artifacts")
    parser.add_argument("--package", default="knowledge/brain/acceptance/r3-whole-game-cfg-repair")
    args = parser.parse_args()
    package = Path(args.package)
    required = {
        "r3-source-gate.json",
        "r3-canonical-prework.json",
        "r3-identity-recovery-summary.json",
        "r3-cfg-family-summary.json",
        "r3-transformer-summary.json",
        "r3-batch-summary.json",
        "r3-negative-fixture-validation.json",
        "r3-provenance-manifest.json",
        "r3-method-status-summary.json",
        "r3-graph-delta.json",
        "r3-validation.json",
        "r3-final-decision.json",
        "R3_WHOLE_GAME_CFG_REPAIR_REPORT.md",
    }
    missing = sorted(name for name in required if not (package / name).exists())
    if missing:
        raise AssertionError(f"missing acceptance files: {missing}")

    source_gate = read_json(package / "r3-source-gate.json")
    canonical = read_json(package / "r3-canonical-prework.json")
    identity = read_json(package / "r3-identity-recovery-summary.json")
    transformer = read_json(package / "r3-transformer-summary.json")
    batch = read_json(package / "r3-batch-summary.json")
    negative = read_json(package / "r3-negative-fixture-validation.json")
    statuses = read_json(package / "r3-method-status-summary.json")
    graph = read_json(package / "r3-graph-delta.json")
    validation = read_json(package / "r3-validation.json")
    decision = read_json(package / "r3-final-decision.json")
    checks = {
        "source_gate": source_gate["status"] == "PASS",
        "canonical_universe": canonical["canonical_method_count"] == 10827 and canonical["canonical_queue_count"] == 10827 and canonical["canonical_target_types"] == 641,
        "identity_blockers": identity["blocked_identity_start"] == 2634 and sum(identity["root_cause_counts"].values()) == 2634,
        "identity_accounted": identity["resolved_total"] + identity["unresolved_total"] == 2634,
        "cfg_evidence": canonical["r3_active_cfg_count"] == 2856 and canonical["evidence_bundle_count"] == 2856,
        "negative_fixtures": negative["status"] == "PASS" and negative["fixture_count"] == 5 and negative["rejected_count"] == 5,
        "transformers": transformer["status"] == "PASS" and transformer["planned_eligible_count"] == 0 and transformer["accepted_repair_count"] == 0,
        "batch_no_write": batch["status"] == "PASS" and batch["repaired_count"] == 0 and not batch["files_changed"],
        "status_universe": statuses["status"] == "PASS" and statuses["method_count"] == 10827 and statuses["unique_method_ids"] == 10827,
        "graph_zero": graph["status"] == "PASS" and all(value == 0 for value in graph["graph_delta"].values()),
        "validation": validation["status"] == "PASS" and not validation["failed_checks"],
        "decision": decision["status"] == "PASS" and decision["acceptance_token"] == TOKEN and decision["stop_after_r3"],
    }
    if not all(checks.values()):
        raise AssertionError(f"failed R3 acceptance checks: {[key for key, value in checks.items() if not value]}")
    print(json.dumps({
        "status": "PASS",
        "acceptance_token": TOKEN,
        "methods": statuses["method_count"],
        "active_cfg": canonical["r3_active_cfg_count"],
        "identity_resolved": identity["resolved_total"],
        "identity_unresolved": identity["unresolved_total"],
        "negative_rejected": negative["rejected_count"],
        "r3_repaired": transformer["accepted_repair_count"],
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
