"""Validate the mandatory R3 negative-repair fixtures.

The fixtures are intentionally adversarial source edits from the user-provided
R3 pack.  This validator is a semantic-gate sentinel: it must reject the
edits before any source mutation is considered.  It does not claim that a
textual diff is a substitute for Roslyn binding or IL/data-flow evidence.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_changed_hunks(diff_text: str) -> list[dict[str, Any]]:
    """Return each unified-diff file section with its hunk text."""

    sections: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    for line in diff_text.splitlines():
        if line.startswith("--- "):
            if current is not None:
                sections.append(current)
            current = {"old": line[4:], "new": "", "hunks": []}
        elif line.startswith("+++ ") and current is not None:
            current["new"] = line[4:]
        elif line.startswith("@@ ") and current is not None:
            current["hunks"].append([line])
        elif current is not None and current["hunks"]:
            current["hunks"][-1].append(line)
    if current is not None:
        sections.append(current)
    return sections


def section_body(section: dict[str, Any]) -> str:
    return "\n".join(line for hunk in section["hunks"] for line in hunk)


def validate_fixture(fixture: dict[str, Any], section: dict[str, Any]) -> dict[str, Any]:
    body = section_body(section)
    failures = set(fixture["failure_modes"])
    reasons: list[str] = []

    if "DECLARATION_RENAMED_BUT_OLD_IDENTIFIER_CONSUMER_REMAINS" in failures:
        if re.search(r"^-\s*object\s+obj\s*=\s*0;", body, re.MULTILINE) and re.search(
            r"(?:^|\n)[+ ](?!-).*\bobj\b", body
        ):
            reasons.append("ORPHAN_OR_RENAMED_IDENTIFIER")
        else:
            reasons.append("IDENTIFIER_BINDING_NOT_PROVEN")

    if "DECLARING_TYPE_INFERRED_AS_LOCAL_TYPE_WITHOUT_PROOF" in failures:
        declaring_type = re.escape(fixture["declaring_type"])
        if re.search(rf"^\+\s*{declaring_type}\s+localTarget\s*=\s*0;", body, re.MULTILINE):
            reasons.append("LOCAL_TYPE_GUESSED_FROM_DECLARING_TYPE")
        else:
            reasons.append("LOCAL_TYPE_EVIDENCE_MISSING")

    if "UNPROVEN_INVARIANT_GENERIC_CAST_REMOVAL" in failures:
        if "-\t\t\tList<object>.Enumerator enumerator3 = ((List<object>)(object)tasks_).GetEnumerator();" in body and \
                "+\t\t\tList<object>.Enumerator enumerator3 = ((List<object>)tasks_).GetEnumerator();" in body:
            reasons.append("UNPROVEN_INVARIANT_GENERIC_CONVERSION")
        else:
            reasons.append("GENERIC_CONVERSION_EVIDENCE_MISSING")

    # These fixtures contain no binding, data-flow, or type-system proof.  A
    # syntax-only parse or a visually improved graph is never sufficient.
    reasons.append("SEMANTIC_PROOF_REQUIRED")
    return {
        "method_id": fixture["method_id"],
        "declaring_type": fixture["declaring_type"],
        "method_name": fixture["method_name"],
        "status": "REJECT",
        "failure_modes": fixture["failure_modes"],
        "reject_reasons": sorted(set(reasons)),
        "semantic_proof_present": False,
    }


def validate(fixtures_path: Path, diff_path: Path) -> dict[str, Any]:
    payload = read_json(fixtures_path)
    fixtures = payload.get("fixtures", [])
    sections = parse_changed_hunks(diff_path.read_text(encoding="utf-8"))
    if payload.get("canonical_status") != "REJECT_ALL_SOURCE_CHANGES":
        raise AssertionError("negative fixture pack does not require rejection")
    if len(fixtures) != 5 or len(sections) != 4:
        raise AssertionError(f"expected 5 fixtures and 4 diff sections, got {len(fixtures)} and {len(sections)}")

    section_by_type = {
        section["new"].split("\t", 1)[0].split("/")[-1].split("\\")[-1]: section
        for section in sections
    }
    results: list[dict[str, Any]] = []
    for fixture in fixtures:
        file_name = fixture["declaring_type"].split(".")[-1] + ".cs"
        section = section_by_type.get(file_name)
        if section is None:
            raise AssertionError(f"no diff section for {fixture['method_id']}: {file_name}")
        results.append(validate_fixture(fixture, section))

    rejected = [row for row in results if row["status"] == "REJECT"]
    if len(rejected) != 5:
        raise AssertionError(f"expected 5 rejected fixtures, got {len(rejected)}")
    if any("SEMANTIC_PROOF_REQUIRED" not in row["reject_reasons"] for row in results):
        raise AssertionError("every negative fixture must require semantic proof")
    return {
        "schema_version": "r3-negative-fixture-validation-v1",
        "status": "PASS",
        "fixture_count": len(fixtures),
        "diff_section_count": len(sections),
        "rejected_count": len(rejected),
        "syntax_only_is_rejected": True,
        "source_mutation_performed": False,
        "results": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate R3 negative CFG-repair fixtures")
    parser.add_argument("--fixtures", default="tools/social-dev/r3_negative_repair_fixtures.json")
    parser.add_argument("--diff", default="tools/social-dev/r3_negative_repair_fixtures.diff")
    parser.add_argument("--out")
    args = parser.parse_args()
    result = validate(Path(args.fixtures), Path(args.diff))
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
