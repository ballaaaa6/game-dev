"""Standalone acceptance checks for the R1 whole-corpus index package."""

from __future__ import annotations

import json
import sys
from pathlib import Path

TOOLS_ROOT = Path(__file__).resolve().parent
ROOT = TOOLS_ROOT.parents[1]
sys.path.insert(0, str(TOOLS_ROOT))

from build_r1_whole_corpus_index import (  # noqa: E402
    DEFAULT_OUT,
    EXPECTED_HASHES,
    OWNERSHIPS,
    load_json,
    load_jsonl,
    validate_local_artifacts,
)


def main() -> int:
    result = validate_local_artifacts(DEFAULT_OUT)
    if result.get("status") != "PASS":
        print(json.dumps(result, sort_keys=True, indent=2))
        return 1
    gate = load_json(DEFAULT_OUT / "source-gate.json")
    assert gate["status"] == "PASS"
    assert all(row["match"] for row in gate["pinned_inputs"].values())
    assert {
        key: row["observed_sha256"]
        for key, row in gate["pinned_inputs"].items()
    } == EXPECTED_HASHES
    assert {
        row["ownership"]
        for row in load_jsonl(DEFAULT_OUT / "type-catalog.jsonl")
    }.issubset(set(OWNERSHIPS))
    assert {
        row["method_id"]
        for row in load_jsonl(DEFAULT_OUT / "method-catalog.jsonl")
    } == {
        row["method_id"]
        for row in load_jsonl(DEFAULT_OUT / "repair-queue.jsonl")
    }
    assert load_json(DEFAULT_OUT / "core-nine-validation.json")["pass"] is True
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
