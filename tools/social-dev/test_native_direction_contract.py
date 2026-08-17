"""Validate the closed native ObjChip direction mapping."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "knowledge/fixtures/accepted/runtime/native_direction_contract.json"


def main() -> int:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    assert contract["status"] == "pass"
    assert contract["semantic_status"] == "approved_for_runtime_contract"
    assert contract["direction_semantics_status"] == "closed_native_vector_mapping"
    assert contract["raw_domain"] == [0, 1, 2, 3]
    assert contract["raw_values"] == {
        "0": {"label": "DIRECTION_RIGHT", "vector": [0, 1], "reverse": 1},
        "1": {"label": "DIRECTION_LEFT", "vector": [0, -1], "reverse": 0},
        "2": {"label": "DIRECTION_UP", "vector": [1, 0], "reverse": 3},
        "3": {"label": "DIRECTION_DOWN", "vector": [-1, 0], "reverse": 2},
    }
    trace = contract["native_trace"]
    assert trace["binary_evidence_status"] == "reviewed_native_disassembly"
    assert trace["vector_rva"] == "0x12C4754"
    assert trace["reverse_rva"] == "0x12C47D4"
    assert trace["static_constructor_rva"] == "0x12C59DC"
    assert trace["reverse_table"] == [1, 0, 3, 2]
    assert trace["static_vectors"] == [[0, 1], [0, -1], [1, 0], [-1, 0]]
    assert contract["runtime_policy"]["expose_native_label_and_vector"] is True
    assert contract["runtime_policy"]["rotation_is_allowed"] is False
    print("native_direction_contract_test_passed domain=4 vectors=4 reverse_table=1,0,3,2")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
