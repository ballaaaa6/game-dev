"""Verify the native Room.floor_ and MapChip topology closure package."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))

import build_native_room_floor_closure as builder  # noqa: E402


def read_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    evidence, runtime, report = builder.build_contract()
    evidence_on_disk = read_json(builder.OUTPUT_KNOWLEDGE)
    runtime_on_disk = read_json(builder.OUTPUT_RUNTIME)
    report_on_disk = builder.OUTPUT_REPORT.read_text(encoding="utf-8")

    assert evidence == evidence_on_disk, "knowledge catalog is not reproducible"
    assert runtime == runtime_on_disk, "runtime contract is not reproducible"
    assert report == report_on_disk, "closure report is not reproducible"

    variants = evidence["native_static_arrays"]["MAPCHIP_ARRAY"]["variants"]
    assert evidence["native_static_arrays"]["MAPCHIP_ARRAY"]["outer_length"] == 2
    assert variants["floor_0"]["length"] == 196
    assert (variants["floor_0"]["width"], variants["floor_0"]["height"]) == (14, 14)
    assert variants["floor_nonzero"]["length"] == 16
    assert (variants["floor_nonzero"]["width"], variants["floor_nonzero"]["height"]) == (4, 4)
    assert variants["floor_nonzero"]["rows"] == [[1, 1, 1, 1]] * 4
    assert evidence["native_artifacts"]["method_evidence"]["map_chip_draw"]["file_offset"] == "0x129DB24"
    assert evidence["native_artifacts"]["method_evidence"]["map_chip_draw_floor"]["file_offset"] == "0x129DF38"
    assert evidence["native_artifacts"]["method_evidence"]["map_chip_draw_extension_floor"]["file_offset"] == "0x129E0F4"

    calls = evidence["room_constructor_callsites"]
    assert len(calls) == 8
    assert any(call["usage_role"] == "main_map_bootstrap" and call["arguments"]["width"] == 14 for call in calls)
    assert any(call["usage_role"] == "persistent_player_room" and call["arguments"]["floor"] == 0 for call in calls)
    assert sum(call["usage_role"] == "addition_floor_preview" for call in calls) == 6
    assert all(
        not (call["arguments"]["floor"] not in (None, 0) and (call["arguments"]["width"], call["arguments"]["height"]) == (14, 14))
        for call in calls
    )

    assert evidence["coverage"]["roomdata_catalog_rows"] == [f"room:{index}" for index in range(18)]
    assert evidence["coverage"]["status"] == "closed_explicit_native_dimension_policy"
    assert runtime["topology_selection"]["variants"] == {
        variant_id: {
            "native_index": variants[variant_id]["native_index"],
            "floor_predicate": variants[variant_id]["floor_predicate"],
            "width": variants[variant_id]["width"],
            "height": variants[variant_id]["height"],
            "length": variants[variant_id]["length"],
            "rows": variants[variant_id]["rows"],
            "status": variants[variant_id]["status"],
        }
        for variant_id in ("floor_0", "floor_nonzero")
    }
    assert runtime["runtime_policy"]["mapchip_never_inferred_from_objchip"] is True
    assert runtime["runtime_policy"]["unsupported_dimension_combinations_are_rejected"] is True
    assert runtime["source_evidence"]["source_policy"].startswith("C# and native artifacts are evidence only")

    print(
        "native_room_floor_closure_pass "
        f"calls={len(calls)} roomdata={runtime['roomdata_catalog']['room_count']} "
        f"floor0={variants['floor_0']['width']}x{variants['floor_0']['height']} "
        f"nonzero={variants['floor_nonzero']['width']}x{variants['floor_nonzero']['height']}"
    )


if __name__ == "__main__":
    main()
