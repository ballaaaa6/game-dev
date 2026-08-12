#!/usr/bin/env python3
"""Build the Wave 3 C0 actor evidence register and bounded function map.

This is an evidence-index builder, not a web runtime implementation.  It reads
the frozen dump/source roots and existing Wave 0--2 artifacts, records actor
field/function provenance, and preserves unresolved movement/state semantics.
Source roots are never written by this script.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
PHASE = ROOT / "Phases" / "Phase4"
ARTIFACTS = PHASE / "artifacts"
DUMP = ROOT / "game-dev-story-mod_Dumped"
FORM_C = DUMP / "Categorized_Code" / "Global" / "form.c"
DUMP_CS = DUMP / "dump.cs"
SCRIPT_JSON = DUMP / "script.json"
FUNCTION_INVENTORY = ARTIFACTS / "function_inventory.json"
CALL_GRAPH = ARTIFACTS / "office_runtime_call_graph.json"
WAVE1_BRANCH_INDEX = ARTIFACTS / "wave1_branch_index.json"
WAVE1_SLICES = ARTIFACTS / "wave1_slices.json"
WAVE2_MANIFEST = ARTIFACTS / "wave2_build_manifest.json"
WAVE2_GAPS = ARTIFACTS / "wave2_gap_register.json"
WAVE2_MOVEMENT = ARTIFACTS / "wave2_wave3_movement_interface.json"


ACTOR_FUNCTIONS = [
    {
        "symbol": "form_GameForm__AddSyain",
        "area": "identity",
        "role": "employee table insertion and employee-facing source record",
        "priority": "P0",
        "semantic_status": "bounded_provenance_only",
    },
    {
        "symbol": "form_GameForm__CallSyain",
        "area": "identity_spawn",
        "role": "actor slot allocation, object binding, and initial Human* writes",
        "priority": "P0",
        "semantic_status": "bounded_provenance_only",
    },
    {
        "symbol": "form_GameForm__NextTarget",
        "area": "target_position",
        "role": "copy target arrays into actor position arrays by index",
        "priority": "P0",
        "semantic_status": "field_flow_verified_space_open",
    },
    {
        "symbol": "form_GameForm__AddTarget",
        "area": "target_position",
        "role": "target array producer",
        "priority": "P0",
        "semantic_status": "bounded_provenance_only",
    },
    {
        "symbol": "form_GameForm__MainProcess",
        "area": "actor_tick",
        "role": "large lifecycle/tick function; only actor-touching branches are in scope",
        "priority": "P1",
        "semantic_status": "bounded_slice_required",
    },
    {
        "symbol": "form_GameForm__DoEvent",
        "area": "actor_tick_lifecycle",
        "role": "event lifecycle function; current source is assembly fallback only",
        "priority": "P1",
        "semantic_status": "assembly_fallback_bounded_slice_required",
    },
    {
        "symbol": "form_GameForm__DrawHuman",
        "area": "animation_render",
        "role": "TFace/TBody/TMode renderer entry; two recovered C definitions exist",
        "priority": "P0",
        "semantic_status": "composition_contract_verified_semantic_state_open",
    },
    {
        "symbol": "form_GameForm__DrawObj",
        "area": "scene_render",
        "role": "object dispatch boundary that calls DrawHuman",
        "priority": "P0",
        "semantic_status": "dispatch_verified_depth_open",
    },
    {
        "symbol": "form_GameForm__CallHikkosi",
        "area": "scene_actor_bridge",
        "role": "room initialization caller that reaches CallSyain/AddTarget",
        "priority": "P1",
        "semantic_status": "bounded_scene_dependency_only",
    },
    {
        "symbol": "form_GameForm__ProcessEvent",
        "area": "event_boundary",
        "role": "input/event boundary; no actor state claim from this C0 index",
        "priority": "P1",
        "semantic_status": "scope_boundary_only",
    },
]


FIELD_GROUPS = {
    "identity_binding": [
        "HumanEnabled",
        "HumanObjec",
        "HumanSyain",
        "HumanSyurui",
        "HumanVisitor",
    ],
    "position": [
        "HumanX",
        "HumanY",
        "HumanPX",
        "HumanPY",
    ],
    "target_points": [
        "TargetX",
        "TargetY",
        "HumanNowPoint",
        "HumanGoalPoint",
    ],
    "state_timing": [
        "HumanMode",
        "HumanTime",
        "HumanStop",
        "HumanWalkLong",
        "HumanSitChair",
        "HumanReaction",
        "HumanWait",
        "HumanState",
        "HumanAnime",
    ],
    "composition": [
        "HumanFaceG",
        "HumanBodyG",
        "HumanDegree",
        "HumanFukiIndex",
        "HumanFukiTime",
    ],
    "interaction_relations": [
        "HumanMeetMode",
        "HumanMeetSyain",
        "HumanRequestMax",
        "HumanBallTime",
        "HumanBallMode",
        "HumanBallIndex",
        "HumanBallNumber",
        "HumanDevProcess",
        "DeskSyain",
        "DeskObjec",
        "ChairMainObjec",
        "ChairSubObjec",
        "PCObjec",
        "DeskZahyou",
    ],
}

CONTROLLED_STATUSES = [
    "verified",
    "recoverable",
    "conflicting_evidence",
    "extraction_missing",
    "not_found_in_scoped_functions",
    "web_adapter_decision",
    "out_of_scope",
]


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_hashes(paths: list[Path]) -> dict[str, dict[str, Any]]:
    return {
        rel(path): {"sha256": sha256(path), "bytes": path.stat().st_size}
        for path in paths
    }


def line_of(text: str, needle: str, occurrence: int = 1) -> int | None:
    matches = list(re.finditer(re.escape(needle), text))
    if not matches:
        return None
    index = min(max(occurrence - 1, 0), len(matches) - 1)
    return text.count("\n", 0, matches[index].start()) + 1


def source_ref(path: Path, text: str, needle: str, occurrence: int = 1) -> dict[str, Any]:
    return {"file": rel(path), "line": line_of(text, needle, occurrence), "needle": needle}


def all_function_spans(text: str, symbol: str) -> list[dict[str, Any]]:
    lines = text.splitlines()
    header = f"// Function: {symbol}"
    starts = [index for index, line in enumerate(lines) if line.strip() == header]
    spans: list[dict[str, Any]] = []
    for occurrence, start in enumerate(starts, 1):
        end = len(lines)
        for index in range(start + 1, len(lines)):
            if lines[index].startswith("// Function:"):
                end = index
                break
        address = None
        for line in lines[start : min(start + 4, end)]:
            match = re.search(r"// Address:\s*(0x[0-9a-fA-F]+)", line)
            if match:
                address = match.group(1)
                break
        spans.append(
            {
                "symbol": symbol,
                "occurrence": occurrence,
                "status": "recovered_c_function",
                "line_start": start + 1,
                "line_end": end,
                "line_count": end - start,
                "address": address,
                "source": rel(FORM_C),
            }
        )
    return spans


def parse_gameform_fields(names: set[str]) -> dict[str, dict[str, Any]]:
    fields: dict[str, dict[str, Any]] = {}
    for line_number, line in enumerate(read_text(DUMP_CS).splitlines(), 1):
        if "// 0x" not in line:
            continue
        for name in names:
            pattern = rf"\b{re.escape(name)}\s*;\s*//\s*(0x[0-9A-Fa-f]+)\b"
            match = re.search(pattern, line)
            if not match or name in fields:
                continue
            declaration = line.strip().split("//", 1)[0].strip()
            fields[name] = {
                "name": name,
                "declaration": declaration,
                "offset": match.group(1).lower(),
                "source": rel(DUMP_CS),
                "line": line_number,
                "status": "verified_dump_field_declaration",
            }
    missing = sorted(names - set(fields))
    if missing:
        raise RuntimeError("missing expected GameForm fields: " + ", ".join(missing))
    return fields


def constrained_offset_references(
    form_lines: list[str], spans: list[dict[str, Any]], offset: str, limit: int = 8
) -> list[dict[str, Any]]:
    token = offset.lower()
    refs: list[dict[str, Any]] = []
    for span in spans:
        local_lines = form_lines[span["line_start"] - 1 : span["line_end"]]
        for local_index, line in enumerate(local_lines):
            if re.search(rf"\b{re.escape(token)}\b", line.lower()):
                refs.append(
                    {
                        "file": rel(FORM_C),
                        "line": span["line_start"] + local_index,
                        "function": span["symbol"],
                        "function_occurrence": span["occurrence"],
                        "needle": token,
                    }
                )
                if len(refs) >= limit:
                    return refs
    return refs


def build_field_map(
    fields: dict[str, dict[str, Any]],
    form_text: str,
    function_spans: list[dict[str, Any]],
) -> dict[str, Any]:
    form_lines = form_text.splitlines()
    field_map: dict[str, Any] = {}
    for group, names in FIELD_GROUPS.items():
        for name in names:
            field = dict(fields[name])
            refs = constrained_offset_references(form_lines, function_spans, field["offset"])
            functions = Counter(ref["function"] for ref in refs)
            field.update(
                {
                    "group": group,
                    "semantic_status": "field_declared_offset_references_only",
                    "offset_reference_count_in_scoped_functions": len(refs),
                    "offset_reference_functions": dict(sorted(functions.items())),
                    "offset_reference_samples": refs,
                    "semantic_policy": "do_not_assign Agent meaning from field name or offset alone",
                }
            )
            field_map[name] = field
    return field_map


def inventory_lookup(inventory: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {row["symbol"]: row for row in inventory.get("shortlist", [])}


def relevant_edges(call_graph: dict[str, Any], symbols: set[str]) -> list[dict[str, Any]]:
    edges = []
    for edge in call_graph.get("edges", []):
        if edge.get("caller") in symbols or edge.get("callee") in symbols:
            edges.append(edge)
    return sorted(edges, key=lambda row: (row.get("caller", ""), row.get("callee", "")))


def build_actor_function_map(
    form_text: str,
    inventory: dict[str, Any],
    call_graph: dict[str, Any],
    field_map: dict[str, Any],
) -> dict[str, Any]:
    lookup = inventory_lookup(inventory)
    spans = all_function_spans(form_text, "")
    del spans
    selected_symbols = {row["symbol"] for row in ACTOR_FUNCTIONS}
    all_c_defs = {
        symbol: all_function_spans(form_text, symbol) for symbol in selected_symbols
    }
    function_rows: list[dict[str, Any]] = []
    for spec in ACTOR_FUNCTIONS:
        symbol = spec["symbol"]
        inventory_row = lookup.get(symbol, {})
        c_defs = all_c_defs[symbol]
        row = {
            **spec,
            "source_status": inventory_row.get("source_status", "not_in_wave0_shortlist"),
            "dump_methods": inventory_row.get("dump_methods", []),
            "script_methods": inventory_row.get("script_methods", []),
            "c_definitions": c_defs,
            "assembly_fallback": inventory_row.get("assembly_fallback"),
            "assembly_call_targets": inventory_row.get("assembly_call_targets"),
            "inventory_reason": inventory_row.get("reason"),
            "evidence_policy": "C0 records provenance and bounded scope; it does not close actor semantics",
        }
        function_rows.append(row)

    return {
        "schema_version": "wave3-actor-function-map-v1",
        "phase": "Phase4",
        "wave": "Wave3",
        "stage": "W3-C0-actor-evidence-register",
        "source_roots_read_only": True,
        "address_namespace": {
            "export_to_raw_delta": "-0x100000",
            "status": "inherited_verified_wave1_wave2",
        },
        "scope": {
            "function_count": len(function_rows),
            "functions": function_rows,
            "field_groups": {
                group: names for group, names in FIELD_GROUPS.items()
            },
            "field_map": field_map,
        },
        "call_graph_edges": relevant_edges(call_graph, selected_symbols),
        "boundaries": [
            {
                "boundary_id": "actor_spawn",
                "functions": ["form_GameForm__AddSyain", "form_GameForm__CallSyain"],
                "status": "ready_for_bounded_c1_trace",
                "next_action": "trace source employee fields and initial Human* writes",
            },
            {
                "boundary_id": "actor_target",
                "functions": ["form_GameForm__AddTarget", "form_GameForm__NextTarget"],
                "status": "field_flow_ready_space_semantics_open",
                "next_action": "separate target point, current position, previous position, and coordinate spaces",
            },
            {
                "boundary_id": "actor_tick",
                "functions": ["form_GameForm__MainProcess", "form_GameForm__DoEvent"],
                "status": "bounded_slice_required",
                "next_action": "slice only branches that read/write actor state, position, target, or timer",
            },
            {
                "boundary_id": "actor_draw",
                "functions": ["form_GameForm__DrawObj", "form_GameForm__DrawHuman"],
                "status": "dispatch_and_composition_boundary_ready",
                "next_action": "map actor selectors to draw command without semantic animation claim",
            },
        ],
        "summary": {
            "function_count": len(function_rows),
            "function_with_recovered_c": sum(bool(row["c_definitions"]) for row in function_rows),
            "function_assembly_fallback_only": sum(
                row["source_status"] == "assembly_fallback_only" for row in function_rows
            ),
            "field_count": len(field_map),
            "call_graph_edge_count": len(relevant_edges(call_graph, selected_symbols)),
            "semantic_status": "actor_provenance_indexed_semantic_state_movement_open",
        },
    }


def build_gap_register(
    field_map: dict[str, Any],
    actor_map: dict[str, Any],
    wave2_gaps: dict[str, Any],
    movement_interface: dict[str, Any],
) -> dict[str, Any]:
    def field_evidence(names: list[str]) -> list[dict[str, Any]]:
        return [
            {
                "file": field_map[name]["source"],
                "line": field_map[name]["line"],
                "needle": f"{name}; // {field_map[name]['offset']}",
            }
            for name in names
        ]

    function_rows = {row["symbol"]: row for row in actor_map["scope"]["functions"]}
    gaps = [
        {
            "id": "W3-GAP-001",
            "area": "actor_field_provenance",
            "status": "recoverable",
            "impact": "field declarations and offset references are indexed, but semantic roles still need bounded traces",
            "evidence": field_evidence(["HumanX", "HumanY", "HumanMode", "HumanFaceG", "HumanBodyG"]),
            "next_action": "use W3-C1/W3-C2 slices to classify producer/consumer behavior",
        },
        {
            "id": "W3-GAP-002",
            "area": "actor_spawn",
            "status": "recoverable",
            "impact": "CallSyain has recovered C and direct AddObjec/NextTarget calls, but employee-to-actor semantics are not closed",
            "evidence": [
                {"file": rel(FORM_C), "line": function_rows["form_GameForm__CallSyain"]["c_definitions"][0]["line_start"], "needle": "// Function: form_GameForm__CallSyain"},
                {"file": rel(FORM_C), "line": line_of(read_text(FORM_C), "form_GameForm__AddObjec", 1), "needle": "form_GameForm__AddObjec"},
            ],
            "next_action": "build W3-C1 spawn contract from bounded CallSyain writes",
        },
        {
            "id": "W3-GAP-003",
            "area": "target_position_space",
            "status": "recoverable",
            "impact": "AddTarget/NextTarget field flow is present, but point/pixel/world coordinate meaning is open",
            "evidence": [
                {"file": rel(FORM_C), "line": function_rows["form_GameForm__AddTarget"]["c_definitions"][0]["line_start"], "needle": "// Function: form_GameForm__AddTarget"},
                {"file": rel(FORM_C), "line": function_rows["form_GameForm__NextTarget"]["c_definitions"][0]["line_start"], "needle": "// Function: form_GameForm__NextTarget"},
            ],
            "next_action": "compare target/current/previous arrays in W3-C3 without assigning world semantics prematurely",
        },
        {
            "id": "W3-GAP-004",
            "area": "actor_tick_state_timer",
            "status": "recoverable",
            "impact": "MainProcess is recovered C but very large; DoEvent remains assembly fallback only",
            "evidence": [
                {"file": rel(FORM_C), "line": function_rows["form_GameForm__MainProcess"]["c_definitions"][0]["line_start"], "needle": "// Function: form_GameForm__MainProcess"},
                {"file": rel(WAVE1_BRANCH_INDEX), "line": None, "needle": "form_GameForm__DoEvent"},
            ],
            "next_action": "create bounded actor-touching slices; do not translate either full function",
        },
        {
            "id": "W3-GAP-005",
            "area": "semantic_animation",
            "status": "recoverable",
            "impact": "DrawHuman composition boundary is available, but state/mode/timing/direction mapping is not closed",
            "evidence": [
                {"file": rel(FORM_C), "line": function_rows["form_GameForm__DrawHuman"]["c_definitions"][0]["line_start"], "needle": "// Function: form_GameForm__DrawHuman"},
                {"file": "Phases/Phase2/artifacts/animation_manifest.json", "line": None, "needle": "verified_semantic_animations"},
            ],
            "next_action": "keep mode_id, animation_id, semantic state, direction, and timer as separate namespaces",
        },
        {
            "id": "W3-GAP-006",
            "area": "seat_occupancy",
            "status": "not_found_in_scoped_functions",
            "impact": "Wave 2 traced chair/desk relations but did not find a legacy occupancy producer",
            "evidence": [
                {"file": rel(WAVE2_GAPS), "line": None, "needle": "seat occupancy"},
                {"file": rel(WAVE2_MOVEMENT), "line": None, "needle": "seat occupancy must be an explicit relation/state owned by Wave 3"},
            ],
            "next_action": "use explicit Wave 2 seat adapter and label it non-legacy until a producer is found",
        },
        {
            "id": "W3-GAP-007",
            "area": "collision_walkable",
            "status": "not_found_in_scoped_functions",
            "impact": "No legacy collision or walkable producer is available in the scoped Wave 2 scene functions",
            "evidence": [
                {"file": rel(WAVE2_MOVEMENT), "line": None, "needle": "require an explicit collision provider"},
                {"file": rel(WAVE2_MOVEMENT), "line": None, "needle": "inject a walk graph/grid as adapter data"},
            ],
            "next_action": "inject adapter providers in W3-C3 fixtures; never infer geometry from sprites",
        },
        {
            "id": "W3-GAP-008",
            "area": "legacy_lifecycle_boundary",
            "status": "out_of_scope",
            "impact": "dialogue, business lifecycle, and full DoEvent behavior are not required to build the C0 provenance index",
            "evidence": [
                {"file": "Phases/Phase4/docs/wave3_plan.md", "line": None, "needle": "ไม่อยู่ใน Wave 3"},
            ],
            "next_action": "revisit only when a Wave 3 fixture proves a concrete dependency",
        },
    ]
    return {
        "schema_version": "wave3-gap-register-v1",
        "phase": "Phase4",
        "wave": "Wave3",
        "stage": "W3-C0-actor-evidence-register",
        "source_roots_read_only": True,
        "controlled_statuses": CONTROLLED_STATUSES,
        "gaps": gaps,
        "inherited_wave2_interface": {
            "status": movement_interface["status"],
            "seat": movement_interface["seat"],
            "collision": movement_interface["collision"],
            "walkable": movement_interface["walkable"],
        },
        "summary": {
            "gap_count": len(gaps),
            "unclassified_unknown_count": 0,
            "status_counts": dict(Counter(row["status"] for row in gaps)),
            "current_wave3_gate": "w3_c0_baseline_ready_for_bounded_spawn_and_state_slices",
            "status": "W3-C0-built_actor_provenance_indexed_semantics_open",
        },
    }


def build_manifest(
    field_map: dict[str, Any],
    actor_map: dict[str, Any],
    gap_register: dict[str, Any],
) -> dict[str, Any]:
    source_files = [
        FORM_C,
        DUMP_CS,
        SCRIPT_JSON,
        FUNCTION_INVENTORY,
        CALL_GRAPH,
        WAVE1_BRANCH_INDEX,
        WAVE1_SLICES,
        WAVE2_MANIFEST,
        WAVE2_GAPS,
        WAVE2_MOVEMENT,
    ]
    return {
        "schema_version": "wave3-c0-build-manifest-v1",
        "phase": "Phase4",
        "wave": "Wave3",
        "stage": "W3-C0-actor-evidence-register",
        "source_roots_read_only": True,
        "address_namespace": {
            "export_to_raw_delta": "-0x100000",
            "status": "verified_inherited_from_wave1_wave2",
        },
        "source_hashes": source_hashes(source_files),
        "artifact_inputs": [
            rel(FUNCTION_INVENTORY),
            rel(CALL_GRAPH),
            rel(WAVE1_BRANCH_INDEX),
            rel(WAVE1_SLICES),
            rel(WAVE2_MANIFEST),
            rel(WAVE2_GAPS),
            rel(WAVE2_MOVEMENT),
        ],
        "artifact_outputs": [
            "Phases/Phase4/artifacts/wave3_actor_function_map.json",
            "Phases/Phase4/artifacts/wave3_gap_register.json",
            "Phases/Phase4/artifacts/wave3_build_manifest.json",
            "Phases/Phase4/docs/wave3_slices/actor_spawn_01.md",
            "Phases/Phase4/docs/wave3_slices/actor_tick_01.md",
        ],
        "artifact_summary": {
            "actor_function_count": actor_map["summary"]["function_count"],
            "recovered_c_function_count": actor_map["summary"]["function_with_recovered_c"],
            "assembly_fallback_only_count": actor_map["summary"]["function_assembly_fallback_only"],
            "actor_field_count": len(field_map),
            "call_graph_edge_count": actor_map["summary"]["call_graph_edge_count"],
            "gap_count": gap_register["summary"]["gap_count"],
            "unclassified_unknown_count": gap_register["summary"]["unclassified_unknown_count"],
        },
        "status": "W3-C0-baseline-built_ready_for_bounded_actor_slices",
    }


def build() -> dict[Path, Any]:
    required = [
        FORM_C,
        DUMP_CS,
        SCRIPT_JSON,
        FUNCTION_INVENTORY,
        CALL_GRAPH,
        WAVE1_BRANCH_INDEX,
        WAVE1_SLICES,
        WAVE2_MANIFEST,
        WAVE2_GAPS,
        WAVE2_MOVEMENT,
    ]
    missing = [rel(path) for path in required if not path.is_file()]
    if missing:
        raise RuntimeError("missing W3-C0 inputs: " + ", ".join(missing))

    form_text = read_text(FORM_C)
    inventory = load_json(FUNCTION_INVENTORY)
    call_graph = load_json(CALL_GRAPH)
    wave2_gaps = load_json(WAVE2_GAPS)
    movement_interface = load_json(WAVE2_MOVEMENT)
    all_field_names = {name for names in FIELD_GROUPS.values() for name in names}
    fields = parse_gameform_fields(all_field_names)
    all_spans: list[dict[str, Any]] = []
    for spec in ACTOR_FUNCTIONS:
        all_spans.extend(all_function_spans(form_text, spec["symbol"]))
    field_map = build_field_map(fields, form_text, all_spans)
    actor_map = build_actor_function_map(form_text, inventory, call_graph, field_map)
    gap_register = build_gap_register(field_map, actor_map, wave2_gaps, movement_interface)
    manifest = build_manifest(field_map, actor_map, gap_register)
    return {
        ARTIFACTS / "wave3_actor_function_map.json": actor_map,
        ARTIFACTS / "wave3_gap_register.json": gap_register,
        ARTIFACTS / "wave3_build_manifest.json": manifest,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="build in memory and compare with existing artifacts")
    args = parser.parse_args()
    outputs = build()
    if args.check:
        mismatches = []
        for path, expected in outputs.items():
            if not path.is_file() or load_json(path) != expected:
                mismatches.append(rel(path))
        if mismatches:
            raise SystemExit("artifact mismatch: " + ", ".join(mismatches))
        return
    for path, value in outputs.items():
        write_json(path, value)
    print(json.dumps({"outputs": [rel(path) for path in outputs], "status": "built"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
