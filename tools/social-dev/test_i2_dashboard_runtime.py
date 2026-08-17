"""Run the I2 dashboard integration, evidence, and regression closure checks."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RUNTIME = ROOT / "runtime/social-dev"
EVIDENCE = ROOT / "knowledge/fixtures/accepted/i2-dashboard-runtime"


def run(command: list[str], cwd: Path) -> dict[str, object]:
    executable_command = list(command)
    if sys.platform.startswith("win") and executable_command and executable_command[0] in {"npm", "npx"}:
        executable_command[0] = f"{executable_command[0]}.cmd"
    completed = subprocess.run(executable_command, cwd=cwd, capture_output=True, text=True, timeout=300, check=False)
    output = (completed.stdout + completed.stderr).strip()
    return {"command": " ".join(command), "cwd": cwd.relative_to(ROOT).as_posix(), "status": "PASS" if completed.returncode == 0 else "FAIL", "returncode": completed.returncode, "output_tail": output[-1200:]}


def read_json(name: str) -> object:
    return json.loads((EVIDENCE / name).read_text(encoding="utf-8"))


def main() -> int:
    command_results: list[dict[str, object]] = []

    command_results.append(run(["python", "tools/social-dev/test_i1_assignment_adapter.py"], ROOT))
    command_results.append(run(["python", "tools/social-dev/test_i0_living_runtime.py"], ROOT))
    command_results.append(run(["python", "tools/social-dev/test_runtime_contract_freeze.py"], ROOT))
    command_results.append(run(["python", "tools/social-dev/test_game_knowledge_g0_g1.py"], ROOT))
    command_results.append(run(["python", "tools/social-dev/test_behavior_first_forensics.py"], ROOT))
    command_results.append(run(["python", "tools/social-dev/test_data_dependency_forensics.py"], ROOT))
    command_results.append(run(["python", "tools/social-dev/test_living_core_final_closure.py"], ROOT))
    command_results.append(run(["npx", "vitest", "run", "tests/i2-dashboard-runtime.test.ts"], RUNTIME))
    command_results.append(run(["npx", "vite-node", "../../tools/social-dev/run_i2_dashboard_scenarios.ts"], RUNTIME))

    scenario_results_path = EVIDENCE / "scenario-results.json"
    scenario_results = read_json("scenario-results.json") if scenario_results_path.exists() else {}
    if isinstance(scenario_results, dict) and scenario_results.get("status") == "PASS":
        scenario_check = {"name": "D1-D14 scenario runner", "status": "PASS", "observed": "14/14 PASS"}
    else:
        scenario_check = {"name": "D1-D14 scenario runner", "status": "FAIL", "observed": scenario_results}

    command_results.append(run(["npm", "test", "--", "--run"], RUNTIME))
    command_results.append(run(["npm", "run", "typecheck"], RUNTIME))
    command_results.append(run(["npm", "run", "build"], RUNTIME))
    command_results.append(run(["git", "diff", "--check"], ROOT))

    # Build all JSON contracts/reports after the scenario runner has produced its traces.
    command_results.append(run([sys.executable, "tools/social-dev/build_i2_dashboard_runtime_evidence.py"], ROOT))

    app_runtime = (RUNTIME / "src/app/runtime.ts").read_text(encoding="utf-8")
    dashboard_runtime = (RUNTIME / "src/product/dashboard/runtime.ts").read_text(encoding="utf-8")
    dashboard_ui = (RUNTIME / "src/product/dashboard/ui.ts").read_text(encoding="utf-8")
    living_types = (RUNTIME / "src/core/living/types.ts").read_text(encoding="utf-8")
    source_files = list((RUNTIME / "src").rglob("*.ts"))
    source_text = "\n".join(path.read_text(encoding="utf-8") for path in source_files)

    static_checks = [
        {"name": "production imports no legacy simulation", "status": "PASS" if "../core/simulation" not in app_runtime and "stepSimulation" not in app_runtime else "FAIL"},
        {"name": "one production LivingRuntime construction", "status": "PASS" if len(re.findall(r"\bcreateLivingRuntime\s*\(", app_runtime)) == 1 else "FAIL"},
        {"name": "one production scheduler interval", "status": "PASS" if app_runtime.count("window.setInterval") == 1 else "FAIL"},
        {"name": "DashboardRuntime owns AssignmentAdapter", "status": "PASS" if "createAssignmentAdapter" in dashboard_runtime and "public readonly assignmentAdapter" in dashboard_runtime else "FAIL"},
        {"name": "DashboardRuntime does not clone LivingRuntime", "status": "PASS" if "fromSnapshot" not in dashboard_runtime and "new LivingRuntime" not in dashboard_runtime else "FAIL"},
        {"name": "no product fields in LivingStaff", "status": "PASS" if not re.search(r"externalAgentId|externalTaskId|productStatus|taskProgress", living_types) else "FAIL"},
        {"name": "no browser storage", "status": "PASS" if not re.search(r"localStorage|sessionStorage|indexedDB|indexedDB", source_text, re.IGNORECASE) else "FAIL"},
        {"name": "no raw gameplay controls", "status": "PASS" if not re.search(r'button\("(?:Go Home|Talk|Use Printer|Move|Rest|Heal|Use Equipment)"', dashboard_ui) else "FAIL"},
        {"name": "typed facade API present", "status": "PASS" if all(name in dashboard_runtime for name in ["bindAgent", "unbindAgent", "assignTask", "startTask", "updateTaskProgress", "completeTask", "failTask", "cancelTask", "getSnapshot", "getEvents", "subscribe"]) else "FAIL"},
    ]

    required_files = [
        "checkpoint-ledger.json", "baseline.json", "source-reverification.json", "upstream-hash-lock.json", "current-web-runtime-integration-map.json", "original-app-lifecycle-boundary.json", "dashboard-runtime-contract.json", "dashboard-app-update-contract.json", "scheduler-integration-contract.json", "dashboard-bootstrap-contract.json", "dashboard-api-contract.json", "dashboard-snapshot-contract.json", "dashboard-subscription-contract.json", "dashboard-ui-contract.json", "dashboard-error-contract.json", "persistence-boundary.json", "backend-execution-policy-boundary.json", "browser-smoke-result.json", "scenario-results.json", "deterministic-replay.json", "implementation-manifest.json", "validation.json", "unknowns.json",
    ]
    evidence_checks = [{"name": "required evidence file set", "status": "PASS" if all((EVIDENCE / name).exists() for name in required_files) else "FAIL", "observed": len([name for name in required_files if (EVIDENCE / name).exists()])}]
    traces = sorted((EVIDENCE / "transition-traces").glob("D*.jsonl"))
    evidence_checks.append({"name": "D1-D14 transition traces", "status": "PASS" if {path.stem for path in traces} == {f"D{index}" for index in range(1, 15)} else "FAIL", "observed": [path.stem for path in traces]})

    browser = read_json("browser-smoke-result.json") if (EVIDENCE / "browser-smoke-result.json").exists() else {}
    browser_check = {"name": "browser smoke", "status": "PASS" if isinstance(browser, dict) and browser.get("status") == "PASS_PRODUCT_UI_SMOKE_ONLY" else "FAIL", "observed": browser}

    all_checks = command_results + [scenario_check] + static_checks + evidence_checks + [browser_check]
    passed = all(result.get("status") == "PASS" for result in all_checks)
    validation = {
        "schema": "i2-validation-v1",
        "status": "PASS_I2_DASHBOARD_RUNTIME_API_AND_CONTROL_SURFACE_CLOSED" if passed else "FAIL_I2_VALIDATION",
        "commands": command_results,
        "static_checks": static_checks,
        "evidence_checks": evidence_checks,
        "scenario_check": scenario_check,
        "browser_check": browser_check,
        "server_lifecycle": "reused pre-existing healthy Vite process; no task-owned long-running process",
    }
    (EVIDENCE / "validation.json").write_text(json.dumps(validation, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("PASS_I2_DASHBOARD_RUNTIME_API_AND_CONTROL_SURFACE_CLOSED" if passed else "FAIL_I2_VALIDATION")
    for result in all_checks:
        if result.get("status") != "PASS":
            print(json.dumps(result, ensure_ascii=False))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
