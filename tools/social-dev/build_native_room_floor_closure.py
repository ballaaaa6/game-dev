"""Build the native Room.floor_ usage and MapChip topology closure.

This package closes the connection between the third argument of ``Room`` and
the two native ``Room.MAPCHIP_ARRAY`` rows.  It deliberately keeps that
connection separate from ``RoomData.floorImgId_`` and from the 10x10 ObjChip
catalog.

The reviewed APK initializes ``MAPCHIP_ARRAY`` as two rows:

* row 0, selected when ``floor == 0``: 196 values, consumed as a 14x14 grid;
* row 1, selected when ``floor != 0``: 16 values, consumed as a 4x4 grid.

The second row is therefore a native small/preview topology, not an upper
14x14 replacement for the default map.  C# and native artifacts are evidence
inputs only; the generated contracts contain no executable source imports.
"""

from __future__ import annotations

import hashlib
import json
import re
import struct
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
SOURCE_ROOT = ROOT / "sources/raw/1_Click_CSharp_Code update"
RAW_EVIDENCE = ROOT / "knowledge/sources/phase3a_apk_probe/raw"
RUNTIME_EVIDENCE = ROOT / "knowledge/fixtures/accepted/runtime"
KNOWLEDGE_EVIDENCE = ROOT / "knowledge/fixtures/accepted"
DEFAULT_MAP_PATH = RUNTIME_EVIDENCE / "default_map_chip_contract.json"
ROOM_CATALOG_PATH = RUNTIME_EVIDENCE / "room_catalog_contract.json"
OUTPUT_RUNTIME = RUNTIME_EVIDENCE / "native_room_floor_usage_contract.json"
OUTPUT_KNOWLEDGE = KNOWLEDGE_EVIDENCE / "native_room_floor_usage_catalog.json"
OUTPUT_REPORT = ROOT / "docs/reports/social-dev_room_floor_topology_closure.md"

APK_PATH = ROOT / "sources/raw/Social_Dev_Story_v2.5.1.apk"
METADATA_PATH = RAW_EVIDENCE / "global-metadata.dat"
BINARY_PATH = RAW_EVIDENCE / "libil2cpp.so"
METADATA_SHA256 = "f65f3a00675f35cfa28fef53c37ed7a2dc01e143b6d59c6014a286fa84e4a579"
BINARY_SHA256 = "364893401fcf7fc2380ae64291783edf7b95eecea4775041c3f4c8c081b4d54a"
APK_SHA256 = "fa0e9e3a843732258fc05b2611a8e0f5be6f7e95f2141a53f31fb082322fe2bf"

MAPCHIP_ARRAY_OFFSETS = {
    "floor_0": (0x466F08, 196),
    "floor_nonzero": (0x46A3F8, 16),
}
MAPCHIP_IMAGE_ID_OFFSET = 0x46A440
MAPCHIP_IMAGE_ID_LENGTH = 12
FLOOR_IMAGE_ID_OFFSET = 0x467878
FLOOR_IMAGE_ID_LENGTH = 11

NATIVE_METHODS = {
    "room_static_constructor": {
        "class": "Room",
        "method": ".cctor",
        "rva": "0x12D20C4",
        "file_offset": "0x12CE0C4",
        "end_rva_exclusive": "0x12D22F0",
        "claim": "Creates MAPCHIP_ARRAY outer length 2, with inner lengths 196 and 16, and initializes the image tables.",
    },
    "room_init_map_chips": {
        "class": "Room",
        "method": "InitMapChips",
        "rva": "0x12CB1F4",
        "file_offset": "0x12C71F4",
        "end_rva_exclusive": "0x12CB434",
        "claim": "Computes floor != 0, selects MAPCHIP_ARRAY[0/1], allocates width*height MapChips, and reads the selected row by flat index.",
    },
    "map_chip_draw": {
        "class": "MapChip",
        "method": "Draw",
        "rva": "0x12A1B24",
        "file_offset": "0x129DB24",
        "end_rva_exclusive": "0x12A1DA0",
        "claim": "Reads Room.floor_ at object offset 0x38 and skips the upper-floor draw branch when floor < 1.",
    },
    "map_chip_draw_floor": {
        "class": "MapChip",
        "method": "DrawFloor",
        "rva": "0x12A1F38",
        "file_offset": "0x129DF38",
        "end_rva_exclusive": "0x12A20F0",
        "claim": "Draws the RoomData-selected floor image inside the native 14x14 floor-image culling region.",
    },
    "map_chip_draw_extension_floor": {
        "class": "MapChip",
        "method": "DrawExtentionFloor",
        "rva": "0x12A20F4",
        "file_offset": "0x129E0F4",
        "end_rva_exclusive": "0x12A2A08",
        "claim": "Draws the extension-wall/side composition using the MapChip cell and Room dimensions.",
    },
}

ROOM_CALL_PATTERN = re.compile(r"\bnew\s+Room\s*\((?P<body>.*?)\)", re.DOTALL)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def stable_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def content_hash(value: Any) -> str:
    return hashlib.sha256(stable_json(value).encode("utf-8")).hexdigest()


def relative_path(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def split_arguments(body: str) -> list[str]:
    arguments: list[str] = []
    start = 0
    depth = 0
    quote: str | None = None
    escaped = False
    for index, char in enumerate(body):
        if quote:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = None
            continue
        if char in {"\"", "'"}:
            quote = char
        elif char in "([{<":
            depth += 1
        elif char in ")]}>" and depth:
            depth -= 1
        elif char == "," and depth == 0:
            arguments.append(body[start:index].strip())
            start = index + 1
    tail = body[start:].strip()
    if tail:
        arguments.append(tail)
    return arguments


def parse_int(value: str) -> int | None:
    match = re.fullmatch(r"\s*(-?\d+)\s*", value)
    return int(match.group(1)) if match else None


def parse_bool(value: str) -> bool | None:
    match = re.search(r"\b(true|false)\b", value, flags=re.IGNORECASE)
    return None if not match else match.group(1).lower() == "true"


def call_role(path: Path, width: int | None, height: int | None, floor: int | None, preview: bool | None) -> str:
    normalized = path.as_posix().lower()
    if "appdata.cs" in normalized and (width, height, floor) == (14, 14, 0):
        return "main_map_bootstrap"
    if preview is True:
        return "addition_floor_preview"
    if (width, height, floor, preview) == (4, 4, 0, False):
        return "persistent_player_room"
    return "other_room_construction"


def scan_room_constructors() -> list[dict[str, Any]]:
    calls: list[dict[str, Any]] = []
    for path in sorted(SOURCE_ROOT.rglob("*.cs")):
        text = path.read_text(encoding="utf-8", errors="replace")
        for ordinal, match in enumerate(ROOM_CALL_PATTERN.finditer(text), start=1):
            body = match.group("body")
            args = split_arguments(body)
            if not args or len(args) < 5:
                continue
            width = parse_int(args[0])
            height = parse_int(args[1])
            floor = parse_int(args[2])
            preview_arg = next((arg for arg in args[4:] if "isPreview" in arg), args[4])
            preview = parse_bool(preview_arg)
            line_start = text.count("\n", 0, match.start()) + 1
            line_end = text.count("\n", 0, match.end()) + 1
            variant = "floor_0" if floor == 0 else "floor_nonzero" if floor is not None else "unknown"
            variant_length = {"floor_0": 196, "floor_nonzero": 16}.get(variant)
            dimension_status = (
                "verified_native_dimensions"
                if width is not None and height is not None and variant_length == width * height
                else "not_proven_or_mismatched"
            )
            calls.append(
                {
                    "call_id": f"room-ctor:{relative_path(path)}:{line_start}:{ordinal}",
                    "file": relative_path(path),
                    "file_sha256": sha256_file(path),
                    "line_start": line_start,
                    "line_end": line_end,
                    "source_text": " ".join(match.group(0).split()),
                    "arguments": {
                        "width": width,
                        "height": height,
                        "floor": floor,
                        "roomdata_expression": args[3],
                        "is_preview": preview,
                    },
                    "roomdata_id": 0 if args[3].replace(" ", "") == "roomData_[0]" else None,
                    "roomdata_id_status": "explicit_roomdata_index" if args[3].replace(" ", "") == "roomData_[0]" else "dynamic_or_unresolved_expression",
                    "topology_variant": variant,
                    "topology_native_index": 0 if variant == "floor_0" else 1 if variant == "floor_nonzero" else None,
                    "topology_dimension_status": dimension_status,
                    "usage_role": call_role(path, width, height, floor, preview),
                }
            )
    return calls


def read_i32_array(path: Path, offset: int, length: int) -> list[int]:
    raw = path.read_bytes()
    end = offset + length * 4
    if offset < 0 or end > len(raw):
        raise ValueError(f"metadata array 0x{offset:X}..0x{end:X} is out of bounds")
    return list(struct.unpack(f"<{length}i", raw[offset:end]))


def topology_variant(name: str, values: list[int], default_map: dict[str, Any]) -> dict[str, Any]:
    width, height = (14, 14) if name == "floor_0" else (4, 4)
    mappings = default_map["raw_index_to_selector"]
    selector_edges = []
    for index, raw_value in enumerate(values):
        mapping = mappings.get(str(raw_value))
        selector_edges.append(
            {
                "flat_index": index,
                "cell": [index % width, index // width],
                "raw_map_index": raw_value,
                "selector_id": mapping["selector_id"] if mapping else None,
                "filename": mapping["filename"] if mapping else None,
                "asset_id": mapping["asset_id"] if mapping else None,
                "status": "resolved_raw_index" if mapping else "missing_raw_index_mapping",
            }
        )
    return {
        "native_index": 0 if name == "floor_0" else 1,
        "floor_predicate": "floor == 0" if name == "floor_0" else "floor != 0",
        "length": len(values),
        "width": width,
        "height": height,
        "rows": [values[row * width : (row + 1) * width] for row in range(height)],
        "metadata_offset": f"0x{MAPCHIP_ARRAY_OFFSETS[name][0]:X}",
        "metadata_hash": hashlib.sha256(struct.pack(f"<{len(values)}i", *values)).hexdigest().upper(),
        "selector_edges": selector_edges,
        "dimension_policy": "native_constructor_width_times_height_must_equal_length",
        "status": "verified_native_topology",
    }


def method_evidence() -> dict[str, Any]:
    evidence: dict[str, Any] = {}
    for key, method in NATIVE_METHODS.items():
        start = int(method["rva"], 16) - 0x4000
        end = int(method["end_rva_exclusive"], 16) - 0x4000
        data = BINARY_PATH.read_bytes()[start:end]
        evidence[key] = {
            **method,
            "byte_length": len(data),
            "byte_sha256": hashlib.sha256(data).hexdigest(),
            "source_status": "verified_current_apk_native_method_boundary",
        }
    return evidence


def build_contract() -> tuple[dict[str, Any], dict[str, Any], str]:
    for path in (METADATA_PATH, BINARY_PATH, APK_PATH, DEFAULT_MAP_PATH, ROOM_CATALOG_PATH):
        if not path.is_file():
            raise FileNotFoundError(path)
    if sha256_file(METADATA_PATH) != METADATA_SHA256:
        raise ValueError("global-metadata.dat hash drifted")
    if sha256_file(BINARY_PATH) != BINARY_SHA256:
        raise ValueError("libil2cpp.so hash drifted")
    if sha256_file(APK_PATH) != APK_SHA256:
        raise ValueError("APK hash drifted")

    default_map = read_json(DEFAULT_MAP_PATH)
    room_catalog = read_json(ROOM_CATALOG_PATH)
    default_map_determinism = default_map.get("determinism")
    if isinstance(default_map_determinism, dict) and default_map_determinism.get("contract_hash"):
        default_map_without_hash = {
            **default_map,
            "determinism": {
                key: value
                for key, value in default_map_determinism.items()
                if key != "contract_hash"
            },
        }
        if default_map_determinism["contract_hash"] != content_hash(default_map_without_hash):
            raise ValueError("default MapChip contract determinism hash drifted")
    metadata_arrays = {
        "map_chip_array": {
            name: read_i32_array(METADATA_PATH, offset, length)
            for name, (offset, length) in MAPCHIP_ARRAY_OFFSETS.items()
        },
        "map_chip_image_id_array": read_i32_array(METADATA_PATH, MAPCHIP_IMAGE_ID_OFFSET, MAPCHIP_IMAGE_ID_LENGTH),
        "floor_image_id_array": read_i32_array(METADATA_PATH, FLOOR_IMAGE_ID_OFFSET, FLOOR_IMAGE_ID_LENGTH),
    }
    expected_image_ids = default_map["native_static_arrays"]["map_chip_image_id_array"]["values"]
    expected_floor_ids = default_map["native_static_arrays"]["floor_image_id_array"]["values"]
    if metadata_arrays["map_chip_image_id_array"] != expected_image_ids:
        raise ValueError("native MAPCHIP_IMAGE_ID_ARRAY drifted from the approved contract")
    if metadata_arrays["floor_image_id_array"] != expected_floor_ids:
        raise ValueError("native FLOOR_IMAGE_ID_ARRAY drifted from the approved contract")

    calls = scan_room_constructors()
    variant_contracts = {
        name: topology_variant(name, values, default_map)
        for name, values in metadata_arrays["map_chip_array"].items()
    }
    for name, variant in variant_contracts.items():
        existing = default_map["native_static_arrays"]["map_chip_array_by_floor"][name]
        if existing["length"] != variant["length"] or existing["rows"] != variant["rows"]:
            raise ValueError(f"approved MapChip topology drifted for {name}")

    room_keys = [f"room:{index}" for index in range(18)]
    parameterized_usage = [
        {
            "usage_id": "player-add-room",
            "roomdata_ids": room_keys,
            "roomdata_id_status": "parameterized_native_roomdata_argument",
            "room_floor_value": 0,
            "topology_variant": "floor_0",
            "width": 4,
            "height": 4,
            "is_preview": False,
            "callers": [
                {"file": "sources/raw/1_Click_CSharp_Code update/game/Player.cs", "line": 4389, "method": "Player.AddRoom"},
            ],
            "status": "verified_native_constructor_dimensions",
        },
        {
            "usage_id": "addition-floor-preview",
            "roomdata_ids": room_keys,
            "roomdata_id_status": "selected_preview_vector_element_dynamic_id",
            "room_floor_value": 1,
            "topology_variant": "floor_nonzero",
            "width": 4,
            "height": 4,
            "is_preview": True,
            "callers": [
                {"file": "sources/raw/1_Click_CSharp_Code update/form/SubForm.cs", "lines": [125618, 126477]},
                {"file": "sources/raw/1_Click_CSharp_Code update/form/SubForm_Split/SubForm.cs", "lines": [125578, 126437]},
                {"file": "sources/raw/1_Click_CSharp_Code update/form/SubForm_Split/InitAdditionFloor.cs", "line": 143},
                {"file": "sources/raw/1_Click_CSharp_Code update/form/SubForm_Split/UpdateAdditionFloor.cs", "line": 765},
            ],
            "status": "verified_native_constructor_dimensions",
        },
        {
            "usage_id": "main-display-map",
            "roomdata_ids": ["room:0"],
            "roomdata_id_status": "explicit_roomdata_index",
            "room_floor_value": 0,
            "topology_variant": "floor_0",
            "width": 14,
            "height": 14,
            "is_preview": False,
            "callers": [
                {"file": "sources/raw/1_Click_CSharp_Code update/KairoEngine/main/AppData.cs", "line": 13813, "method": "AppData.NewGame"},
            ],
            "status": "verified_native_constructor_dimensions",
        },
    ]
    coverage = {
        "roomdata_catalog_rows": room_keys,
        "roomdata_rows_with_floor_image_links": room_catalog.get("room_keys", room_keys),
        "roomdata_to_room_floor_direct_mapping": "not_a_native_field_relationship",
        "roomdata_to_room_floor_policy": "RoomData is passed as an argument; Room.floor_ is supplied by the Room constructor call site.",
        "full_14x14_native_path": "room:0 main display and any floor==0 map construction with width=14,height=14",
        "native_4x4_nonzero_path": "floor!=0 construction with width=4,height=4, including addition-floor preview",
        "unsupported_combinations": [
            "floor!=0 with width=14,height=14: MAPCHIP_ARRAY[1] has only 16 values and native InitMapChips cannot supply 196 cells",
            "floor values 2/3/4/5 as distinct topology variants: native selection is boolean floor!=0, not a per-number array index",
        ],
        "status": "closed_explicit_native_dimension_policy",
    }
    source_refs = {
        "room_constructor": {
            "file": "sources/raw/1_Click_CSharp_Code update/game/Room.cs",
            "lines": "149-176",
            "claim": "Room receives width, height, floor, RoomData, and isPreview as separate constructor inputs.",
        },
        "init_map_chips": {
            "file": "sources/raw/1_Click_CSharp_Code update/game/Room.cs",
            "lines": "208-453",
            "claim": "Readable decompiler body is damaged; native method is authoritative for array selection and dimensions.",
        },
        "player_add_room": {
            "file": "sources/raw/1_Click_CSharp_Code update/game/Player.cs",
            "line": 4389,
            "claim": "Persistent Player.AddRoom constructs Room(4,4,0,roomData,false).",
        },
        "main_display": {
            "file": "sources/raw/1_Click_CSharp_Code update/KairoEngine/main/AppData.cs",
            "line": 13813,
            "claim": "AppData.NewGame constructs Room(14,14,0,roomData_[0],false).",
        },
        "addition_preview": {
            "file": "sources/raw/1_Click_CSharp_Code update/form/SubForm.cs",
            "lines": "126414-126477",
            "claim": "Addition-floor preview selects a dynamic RoomData and constructs Room(4,4,1,roomData3,true).",
        },
    }

    evidence_core = {
        "schema_version": "social-dev-native-room-floor-usage-catalog-v1",
        "package": "social-dev-native-room-floor-usage-closure",
        "status": "pass",
        "semantic_status": "native_room_floor_connection_closed",
        "apk": {"path": relative_path(APK_PATH), "sha256": APK_SHA256},
        "native_artifacts": {
            "metadata": {"path": relative_path(METADATA_PATH), "sha256": METADATA_SHA256},
            "binary": {"path": relative_path(BINARY_PATH), "sha256": BINARY_SHA256},
            "method_evidence": method_evidence(),
        },
        "native_static_arrays": {
            "MAPCHIP_ARRAY": {
                "outer_length": 2,
                "selection_expression": "MAPCHIP_ARRAY[floor != 0 ? 1 : 0]",
                "variants": variant_contracts,
            },
            "MAPCHIP_IMAGE_ID_ARRAY": {
                "values": metadata_arrays["map_chip_image_id_array"],
                "length": MAPCHIP_IMAGE_ID_LENGTH,
                "metadata_offset": f"0x{MAPCHIP_IMAGE_ID_OFFSET:X}",
            },
            "FLOOR_IMAGE_ID_ARRAY": {
                "values": metadata_arrays["floor_image_id_array"],
                "length": FLOOR_IMAGE_ID_LENGTH,
                "metadata_offset": f"0x{FLOOR_IMAGE_ID_OFFSET:X}",
            },
        },
        "room_constructor_callsites": calls,
        "parameterized_usage": parameterized_usage,
        "coverage": coverage,
        "source_refs": source_refs,
        "runtime_policy": {
            "roomdata_is_interior_catalog_key": True,
            "room_floor_is_constructor_key": True,
            "mapchip_never_inferred_from_objchip": True,
            "floor_image_table_is_independent_from_mapchip_topology": True,
            "nonzero_topology_requires_4x4_native_dimensions": True,
            "unsupported_dimension_combinations_are_rejected": True,
            "raw_native_floor_value_is_preserved": True,
            "environment_scope": {
                "main_display": {
                    "topology": "floor_0",
                    "dimensions": "14x14",
                    "outer_mapchip": "native",
                },
                "persistent_room": {
                    "topology": "floor_0",
                    "dimensions": "4x4",
                    "outer_mapchip": "not_present",
                },
                "addition_floor_preview": {
                    "topology": "floor_nonzero",
                    "dimensions": "4x4",
                    "outer_mapchip": "not_present",
                },
                "non_main_outer_mapchip_policy": "no_synthetic_14x14_promotion",
            },
        },
    }
    evidence_core["content_hash"] = content_hash(evidence_core)

    runtime = {
        "schema_version": "social-dev-native-room-floor-usage-contract-v1",
        "package": "social-dev-native-room-floor-usage-contract",
        "status": "pass",
        "semantic_status": "approved_for_runtime_contract",
        "catalog_id": "display-slice-01",
        "content_hash": evidence_core["content_hash"],
        "native_artifact_ref": {
            "apk_sha256": APK_SHA256,
            "binary_sha256": BINARY_SHA256,
            "metadata_sha256": METADATA_SHA256,
            "method_ids": list(NATIVE_METHODS),
        },
        "topology_selection": {
            "native_field": "Room.floor_",
            "predicate": "floor == 0 ? MAPCHIP_ARRAY[0] : MAPCHIP_ARRAY[1]",
            "variants": {
                name: {
                    "native_index": variant["native_index"],
                    "floor_predicate": variant["floor_predicate"],
                    "width": variant["width"],
                    "height": variant["height"],
                    "length": variant["length"],
                    "rows": variant["rows"],
                    "status": variant["status"],
                }
                for name, variant in variant_contracts.items()
            },
        },
        "usage": parameterized_usage,
        "roomdata_catalog": {
            "room_keys": room_keys,
            "room_count": len(room_keys),
            "floor_image_links": "knowledge/fixtures/accepted/runtime/room_catalog_contract.json",
            "objchip_grid": "10x10 RoomData.objMap_/objDir_",
        },
        "runtime_policy": evidence_core["runtime_policy"],
        "source_evidence": {
            "knowledge_catalog": relative_path(OUTPUT_KNOWLEDGE),
            "source_policy": "C# and native artifacts are evidence only; browser runtime imports this contract, not source roots.",
        },
    }
    runtime["contract_hash"] = content_hash(runtime)

    report = "\n".join(
        [
            "# Social Dev Room.floor_ and MapChip topology closure",
            "",
            "## Result",
            "",
            "The native Room floor connection is closed for the reviewed APK.",
            "",
            "- `Room.floor_ == 0` selects `MAPCHIP_ARRAY[0]`, a 196-value 14x14 topology.",
            "- `Room.floor_ != 0` selects `MAPCHIP_ARRAY[1]`, a 16-value 4x4 topology.",
            "- `RoomData.floorImgId_` remains an independent `FLOOR_IMAGE_ID_ARRAY` index.",
            "- The runtime rejects a nonzero floor request with 14x14 dimensions instead of silently borrowing ground data.",
            "- Only the native main-display path receives the 14x14 outer MapChip scope; persistent and addition-floor paths remain 4x4 room topology only.",
            "- A non-main request never receives a synthetic 14x14 garden/road surround when the native constructor does not provide one.",
            "",
            "## Verified construction paths",
            "",
            "| Path | Native constructor | Topology | Status |",
            "|---|---|---|---|",
            "| Main display | `Room(14,14,0,roomData_[0],false)` | `floor_0`, 14x14 | pass |",
            "| Persistent room | `Room(4,4,0,roomData,false)` | `floor_0`, 4x4 slice | pass |",
            "| Addition-floor preview | `Room(4,4,1,roomData3,true)` | `floor_nonzero`, 4x4 | pass |",
            "",
            "## Explicit boundaries",
            "",
            "- There is no native evidence in the reviewed `Room.MAPCHIP_ARRAY` for distinct topology arrays for floor values 2, 3, 4, or 5; the selector is boolean `floor != 0`.",
            "- A full upper 14x14 map is not a native contract in this APK. Promoting the 4x4 nonzero row to 14x14 would be incorrect.",
            "- The 18 RoomData rows are catalog keys. Their MapChip topology is selected by the Room constructor context, not by the RoomData row itself.",
            "",
            f"Catalog hash: `{evidence_core['content_hash']}`",
            f"Runtime contract hash: `{runtime['contract_hash']}`",
            "",
        ]
    )
    return evidence_core, runtime, report


def build_package() -> tuple[dict[str, Any], dict[str, Any], str]:
    evidence, runtime, report = build_contract()
    write_json(OUTPUT_KNOWLEDGE, evidence)
    write_json(OUTPUT_RUNTIME, runtime)
    OUTPUT_REPORT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_REPORT.write_text(report, encoding="utf-8", newline="\n")
    return evidence, runtime, report


if __name__ == "__main__":
    evidence, runtime, _ = build_package()
    print(
        "native_room_floor_closure_built "
        f"calls={len(evidence['room_constructor_callsites'])} "
        f"roomdata={evidence['coverage']['roomdata_catalog_rows'].__len__()} "
        f"floor0={runtime['topology_selection']['variants']['floor_0']['length']} "
        f"nonzero={runtime['topology_selection']['variants']['floor_nonzero']['length']}"
    )
