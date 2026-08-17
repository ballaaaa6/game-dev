"""Independent I0 contract, source-boundary, and runtime acceptance gate."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
I0 = ROOT / "knowledge/fixtures/accepted/i0-living-runtime"
RUNTIME = ROOT / "runtime/social-dev"


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def run(command: list[str], cwd: Path, failures: list[str], label: str) -> str:
    if command and command[0] in {"npx", "npm"}:
        command = [f"{command[0]}.cmd", *command[1:]]
    result = subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=False)
    if result.returncode != 0:
        failures.append(f"{label}: exit={result.returncode}\n{result.stdout}\n{result.stderr}")
    return result.stdout + result.stderr


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--static-only", action="store_true")
    parser.add_argument("--skip-toolchain", action="store_true")
    args = parser.parse_args()
    failures: list[str] = []

    catalog_path = ROOT / "knowledge/fixtures/accepted/runtime/i0-runtime-catalog.json"
    source_path = I0 / "source-reverification.json"
    lock_path = I0 / "r0-contract-hash-lock.json"
    scenario_path = I0 / "scenario-results.json"
    check(catalog_path.exists(), "missing generated I0 runtime catalog", failures)
    check(source_path.exists(), "missing source reverification", failures)
    check(lock_path.exists(), "missing R0 hash lock", failures)
    check(scenario_path.exists(), "missing scenario results", failures)
    if failures:
        print("FAIL_I0_ACCEPTANCE\n" + "\n".join(failures))
        return 1

    catalog = read_json(catalog_path)
    source = read_json(source_path)
    lock = read_json(lock_path)
    scenarios = read_json(scenario_path)
    check(catalog.get("status") == "pass", "catalog status is not pass", failures)
    check(catalog.get("semantic_status") == "approved_for_i0_runtime_catalog", "catalog semantic status drift", failures)
    check(catalog.get("counts") == {"StaffData": 141, "JobData": 30, "SkillData": 36, "FurnitureData": 103, "RoomData": 18}, "catalog counts drift", failures)
    check([len(catalog["data"][key]) for key in ("staff", "jobs", "skills", "furniture")] == [141, 30, 36, 103], "catalog record arrays drift", failures)
    check([fixture["id"] for fixture in catalog.get("scenario_fixtures", [])] == [f"S{index}" for index in range(1, 11)], "fixture sequence drift", failures)
    staff0 = next((record for record in catalog["data"]["staff"] if record["id"] == 0), None)
    furniture18 = next((record for record in catalog["data"]["furniture"] if record["id"] == 18), None)
    check(staff0 is not None and staff0["fields"].get("jobId_") == 4 and staff0["fields"].get("skill_") == 1, "StaffData:0 job/skill relation drift", failures)
    check(furniture18 is not None and furniture18.get("type") == 1 and furniture18.get("recovery") == 10, "FurnitureData:18 recovery relation drift", failures)
    hp_fixture = next((fixture for fixture in catalog["derived_parameters"]["staff_max_hp_fixtures"] if fixture["staff_id"] == 0), None)
    check(hp_fixture is not None and hp_fixture.get("expected_max_hp") == 108, "Staff:0 neutral max HP fixture drift", failures)

    expected_sources = {
        "apk": "fa0e9e3a843732258fc05b2611a8e0f5be6f7e95f2141a53f31fb082322fe2bf",
        "libil2cpp": "364893401fcf7fc2380ae64291783edf7b95eecea4775041c3f4c8c081b4d54a",
        "metadata": "f65f3a00675f35cfa28fef53c37ed7a2dc01e143b6d59c6014a286fa84e4a579",
        "dump": "4487cba6916e159afefec2cd1a9ecf0d12d05b2d76126e7099a5d35323967eb2",
        "csharp_rar": "a50a442491e422c20699a9ca4266e794d215bff29248d3edd24c41f42a57f903",
    }
    check(source.get("all_match") is True and source.get("observed") == expected_sources, "pinned source identity mismatch", failures)

    for entry in lock.get("entries", []):
        path = ROOT / entry["path"]
        check(path.exists(), f"R0 hash-lock path missing: {entry['path']}", failures)
        if path.exists():
            check(sha256(path) == entry["sha256"], f"R0 contract mutated: {entry['path']}", failures)
    check(lock.get("status") == "PASS_PRE_I0_IMMUTABLE_LOCK", "R0 lock status drift", failures)

    living_sources = list((RUNTIME / "src/core/living").glob("*.ts"))
    check(bool(living_sources), "living runtime module directory is empty", failures)
    combined_source = "\n".join(path.read_text(encoding="utf-8") for path in living_sources)
    check("Math.random" not in combined_source, "living runtime uses Math.random", failures)
    check("knowledge/" not in combined_source.replace("knowledge/", ""), "living runtime imports a knowledge source root", failures)
    check("scenarioId" not in (RUNTIME / "src/core/living/runtime.ts").read_text(encoding="utf-8"), "production runtime branches on scenario id", failures)
    check("TRACE_ROUTE_START_TICK" not in (RUNTIME / "src/core/simulation.ts").read_text(encoding="utf-8"), "legacy fixed trace constants remain in simulation owner", failures)

    scenario_results = scenarios.get("results", [])
    check(scenarios.get("scenario_count") == 10, "scenario count is not 10", failures)
    check(all(result.get("status") == "PASS" for result in scenario_results), "one or more S1-S10 scenarios failed", failures)
    for index in range(1, 11):
        trace_path = I0 / "transition-traces" / f"S{index}.jsonl"
        check(trace_path.exists(), f"missing transition trace S{index}", failures)
        if trace_path.exists():
            lines = [line for line in trace_path.read_text(encoding="utf-8").splitlines() if line.strip()]
            check(bool(lines), f"empty transition trace S{index}", failures)
            for line in lines:
                try:
                    json.loads(line)
                except json.JSONDecodeError:
                    failures.append(f"invalid JSONL transition trace S{index}")
                    break

    spotchecks = read_json(I0 / "native-implementation-spotchecks.json")
    check(spotchecks.get("status") == "PASS_REVALIDATED_PINNED_NATIVE_TARGETS", "native spotcheck status is not closed", failures)
    check(len(spotchecks.get("checks", [])) >= 10 and all(item.get("status") == "PASS" for item in spotchecks.get("checks", [])), "native spotcheck coverage incomplete", failures)
    manifest = read_json(I0 / "implementation-manifest.json")
    for module in manifest.get("modules", []):
        check((ROOT / module).exists(), f"implementation manifest module missing: {module}", failures)

    if not args.static_only:
        run(["npx", "--no-install", "vite-node", "tools/social-dev/run_i0_scenarios.ts"], ROOT, failures, "scenario runtime")
    if not args.skip_toolchain:
        run(["npm", "run", "typecheck"], RUNTIME, failures, "typecheck")
        run(["npm", "test", "--", "--run", "tests/i0-living-runtime.test.ts", "tests/simulation.test.ts"], RUNTIME, failures, "focused vitest")

    if failures:
        print("FAIL_I0_ACCEPTANCE")
        print("\n".join(failures))
        return 1
    print("PASS_I0_ORIGINAL_LIVING_CORE_RUNTIME_IMPLEMENTED_S1_S10_CLOSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
