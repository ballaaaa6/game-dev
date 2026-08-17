"""Offline I1 assignment-adapter acceptance.

This validator checks the evidence package, product/living boundary, required
scenarios, and focused runtime test. It does not start a server or access the
network.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "knowledge/fixtures/accepted/i1-assignment-adapter"
PRODUCT = ROOT / "runtime/social-dev/src/product/assignment"


def load_json(relative: str) -> dict:
    path = ROOT / relative
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def check(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    failures: list[str] = []
    checks = 0

    required_json = [
        "checkpoint-ledger.json",
        "baseline.json",
        "source-reverification.json",
        "i0-hash-lock.json",
        "original-work-regime-matrix.json",
        "original-development-start-chain.json",
        "original-development-assignment-payload.json",
        "original-development-completion-chain.json",
        "update-develop-native-map.json",
        "update-develop-state-machine.json",
        "develop-hp-interaction.json",
        "develop-interruption-contract.json",
        "assignment-bridge-decision.json",
        "product-task-model.json",
        "agent-binding-contract.json",
        "assignment-command-contract.json",
        "assignment-event-contract.json",
        "task-lifecycle-contract.json",
        "backend-execution-policy-boundary.json",
        "living-interruption-product-state-contract.json",
        "multi-agent-conflict-contract.json",
        "dashboard-read-model-contract.json",
        "scenario-results.json",
        "deterministic-replay.json",
        "implementation-manifest.json",
        "validation.json",
        "unknowns.json",
    ]
    required_reports = [
        "I1_ORIGINAL_WORK_REGIMES.md",
        "I1_ORIGINAL_DEVELOPMENT_ASSIGNMENT.md",
        "I1_UPDATE_DEVELOP_NATIVE_CLOSURE.md",
        "I1_ASSIGNMENT_BRIDGE_DECISION.md",
        "I1_PRODUCT_TASK_MODEL.md",
        "I1_ASSIGNMENT_ADAPTER.md",
        "I1_LIVING_INTERRUPTION_POLICY.md",
        "I1_DASHBOARD_READ_MODEL.md",
        "I1_SCENARIO_ACCEPTANCE.md",
        "I1_FINAL_HANDOFF.md",
    ]
    required_product = ["types.ts", "commands.ts", "events.ts", "adapter.ts", "bridge.ts", "read-model.ts", "snapshot.ts", "index.ts"]

    for name in required_json:
        checks += 1
        check((EVIDENCE / name).is_file(), f"missing evidence: {name}", failures)
    for name in required_reports:
        checks += 1
        check((ROOT / "docs/Phases/Runtime" / name).is_file(), f"missing report: {name}", failures)
    for name in required_product:
        checks += 1
        check((PRODUCT / name).is_file(), f"missing product implementation: {name}", failures)

    baseline = load_json("knowledge/fixtures/accepted/i1-assignment-adapter/baseline.json")
    source = load_json("knowledge/fixtures/accepted/i1-assignment-adapter/source-reverification.json")
    lock = load_json("knowledge/fixtures/accepted/i1-assignment-adapter/i0-hash-lock.json")
    matrix = load_json("knowledge/fixtures/accepted/i1-assignment-adapter/original-work-regime-matrix.json")
    native = load_json("knowledge/fixtures/accepted/i1-assignment-adapter/update-develop-native-map.json")
    bridge = load_json("knowledge/fixtures/accepted/i1-assignment-adapter/assignment-bridge-decision.json")
    model = load_json("knowledge/fixtures/accepted/i1-assignment-adapter/product-task-model.json")
    command_contract = load_json("knowledge/fixtures/accepted/i1-assignment-adapter/assignment-command-contract.json")
    validation = load_json("knowledge/fixtures/accepted/i1-assignment-adapter/validation.json")
    scenarios = load_json("knowledge/fixtures/accepted/i1-assignment-adapter/scenario-results.json")

    checks += 4
    check(baseline["status"] == "PASS_I1_0_BASELINE", "I1.0 baseline failed", failures)
    check(source["status"] == "PASS_I1_SOURCE_TARGETS_REVERIFIED", "source re-verification failed", failures)
    check(bridge["selected_bridge"] == "PRODUCT_TASK_OVERLAY_WITH_BASELINE_LIVING", "bridge selection is not exactly Bridge C", failures)
    check(validation["status"] == "PASS_I1_12_FULL_ACCEPTANCE" and validation["remaining_blockers"] == 0, "validation is not closed", failures)

    expected_source_hashes = {
        "apk": "FA0E9E3A843732258FC05B2611A8E0F5BE6F7E95F2141A53F31FB082322FE2BF",
        "libil2cpp": "364893401FCF7FC2380AE64291783EDF7B95EECEA4775041C3F4C8C081B4D54A",
        "metadata": "F65F3A00675F35CFA28FEF53C37ED7A2DC01E143B6D59C6014A286FA84E4A579",
        "dump": "4487CBA6916E159AFEFEC2CD1A9ECF0D12D05B2D76126E7099A5D35323967EB2",
        "csharp_rar": "A50A442491E422C20699A9CA4266E794D215BFF29248D3EDD24C41F42A57F903",
    }
    for key, expected in expected_source_hashes.items():
        checks += 1
        check(source["pinned_sources"][key]["sha256"].upper() == expected, f"source hash mismatch: {key}", failures)

    checks += 3
    check(lock["roots"]["runtime/social-dev/src/core/living"]["manifest_sha256"] == "086883b3a2250d61333c438dabbef674038ab438f2d1f599b70b600fd0d618fd", "I0 living manifest mismatch", failures)
    check(lock["roots"]["knowledge/fixtures/accepted/i0-living-runtime"]["manifest_sha256"] == "f2e462f2365532bc5345852b645727a25b7d0e15d6cad0b266c28b87b1e7f2c2", "I0 evidence manifest mismatch", failures)
    check(lock["roots"]["knowledge/fixtures/accepted/runtime-contract-freeze"]["manifest_sha256"] == "040e32a1eabc7ec51233b47e070825989c2279b909c43eba3adc170161ae4613", "R0 manifest mismatch", failures)

    checks += 7
    check({entry["id"] for entry in matrix["regimes"]} == {"BASELINE_NO_PROJECT", "PLANNING_ACTIVE", "DEVELOP_ACTIVE", "POST_DEVELOP_BASELINE"}, "work regime matrix incomplete", failures)
    check(native["native_method"]["rva"] == "0x12D3D48", "UpdateDevelop RVA mismatch", failures)
    check(native["native_method"]["develop_state_offset"] == "0x188", "developState offset mismatch", failures)
    check(len(native["states"]) == 10 and {row["id"] for row in native["states"]} == set(range(10)), "native 0..9 map incomplete", failures)
    check(source["native_targets"]["Staff.Update"]["state_field_offset"] == "0x70", "Staff.Update state offset missing", failures)
    check(source["native_targets"]["Staff.Update"]["state12_call"] == "bl 0x12D3D48 at 0x12D301C", "Staff.Update state12 dispatch mismatch", failures)
    check(source["native_targets"]["Staff.ChangeState"]["rva"] == "0x12D3CDC", "Staff.ChangeState writer missing", failures)

    living_text = "\n".join(path.read_text(encoding="utf-8") for path in (ROOT / "runtime/social-dev/src/core/living").glob("*.ts"))
    product_text = "\n".join(path.read_text(encoding="utf-8") for path in PRODUCT.glob("*.ts"))
    product_mutator_text = "\n".join((PRODUCT / name).read_text(encoding="utf-8") for name in ["adapter.ts", "bridge.ts"])
    checks += 6
    check("externalAgentId" not in living_text and "externalTaskId" not in living_text, "product IDs leaked into LivingStaff semantics", failures)
    check("TaskStatus" in model["entities"] and "StaffState" not in model["entities"]["TaskStatus"], "task status is not separated", failures)
    check("externalProgress" in model["entities"]["TaskRecord"], "external progress boundary missing", failures)
    check(not re.search(r"\.(?:state|hp|route|x|y|moveMode|deskId|equipmentId)\s*=(?!=)", product_mutator_text), "product layer contains a raw living field assignment", failures)
    check(all(field not in Path(PRODUCT / "types.ts").read_text(encoding="utf-8") for field in ["walkFrame", "talkTarget", "equipmentTarget", "homeCommand", "animationFrame"]), "forbidden raw command field leaked", failures)
    check("queue" not in product_text.lower() and "fairness" not in product_text.lower(), "scheduler policy leaked into product implementation", failures)

    checks += 3
    check(set(command_contract["commands"][i]["type"] for i in range(7)) == {"bind_agent", "unbind_agent", "assign_task", "start_task", "complete_task", "fail_task", "cancel_task"}, "required command set incomplete", failures)
    check("ACTIVE_TASK_CONFLICT" in load_json("knowledge/fixtures/accepted/i1-assignment-adapter/multi-agent-conflict-contract.json")["rules"][4], "active conflict code missing", failures)
    check("PRODUCT_POLICY_PENDING_AFTER_I1" == load_json("knowledge/fixtures/accepted/i1-assignment-adapter/backend-execution-policy-boundary.json")["status"], "backend policy boundary missing", failures)

    checks += 1
    scenario_ids = [scenario["id"] for scenario in scenarios["scenarios"]]
    check(scenario_ids == [f"A{i}" for i in range(1, 13)] and all(scenario["status"] == "PASS" for scenario in scenarios["scenarios"]), "A1-A12 scenario results incomplete", failures)
    for scenario_id in scenario_ids:
        checks += 1
        trace = EVIDENCE / "transition-traces" / f"{scenario_id}.jsonl"
        check(trace.is_file() and trace.read_text(encoding="utf-8").strip(), f"missing trace: {scenario_id}", failures)
        if trace.is_file():
            for line in trace.read_text(encoding="utf-8").splitlines():
                try:
                    check(json.loads(line)["scenarioId"] == scenario_id, f"trace scenario mismatch: {scenario_id}", failures)
                except (json.JSONDecodeError, KeyError):
                    failures.append(f"invalid trace JSON: {scenario_id}")

    checks += 2
    diff = subprocess.run(["git", "diff", "--check"], cwd=ROOT, capture_output=True, text=True)
    check(diff.returncode == 0, "git diff --check failed", failures)
    npm = "npm.cmd" if os.name == "nt" else "npm"
    focused = subprocess.run([npm, "test", "--", "--run", "tests/i1-assignment-adapter.test.ts"], cwd=ROOT / "runtime/social-dev", capture_output=True, text=True)
    check(focused.returncode == 0, "focused I1 Vitest failed", failures)

    if failures:
        print("FAIL_I1_ASSIGNMENT_ADAPTER")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"PASS_I1_ASSIGNMENT_ADAPTER_NO_TASK_RUNNING_LIFECYCLE_CLOSED checks={checks} scenarios=12")
    return 0


if __name__ == "__main__":
    sys.exit(main())
