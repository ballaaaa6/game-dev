#!/usr/bin/env python3
"""Collect bounded source evidence for the remaining Phase 4 gaps.

This is an inventory scan, not a semantic translator.  Counts and nearby
source lines are recorded so that a later slice can be selected from evidence
without treating a symbol occurrence as proof of its meaning.
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

FORM_C = ROOT / "game-dev-story-mod_Dumped" / "Categorized_Code" / "Global" / "form.c"
METHOD_C = ROOT / "game-dev-story-mod_Dumped" / "Categorized_Code" / "Global" / "Method.c"
DUMP_CS = ROOT / "game-dev-story-mod_Dumped" / "dump.cs"
SCRIPT_JSON = ROOT / "game-dev-story-mod_Dumped" / "script.json"
NEWGAME_ASM = ROOT / "game-dev-story-mod_Dumped" / "Failed_Functions_Assembly" / "00f265b8_form_GameForm__NewGamePara.asm.txt"
DOEVENT_ASM = ROOT / "game-dev-story-mod_Dumped" / "Failed_Functions_Assembly" / "00f5c704_form_GameForm__DoEvent.asm.txt"

TRANSLATION = ARTIFACTS / "translation_coverage.json"
BRANCH_INDEX = ARTIFACTS / "wave1_branch_index.json"
ASSET_AUDIT = ARTIFACTS / "wave1_asset_gap_audit.json"
ANIMATION_CONTRACT = ARTIFACTS / "wave3_actor_animation_contract.json"
EVENT_MODES = ARTIFACTS / "wave4_event_mode_candidates.json"
ROOM_CALLER = ROOT / "Phases" / "Phase5" / "artifacts" / "wave5_8_room_caller_contract.json"
PRODUCER = ROOT / "Phases" / "Phase5" / "artifacts" / "wave5_9_object_producer_contract.json"
OUTPUT = ARTIFACTS / "targeted_gap_scan.json"

SAMPLE_LIMIT = 16
FUNCTION_HEADER_RE = re.compile(r"^// Function: (?P<name>\S+)")
DRAW_HUMAN_RE = re.compile(r"form_GameForm__DrawHuman\s*\(")

ACTOR_FIELDS = [
    "TargetX",
    "TargetY",
    "HumanX",
    "HumanY",
    "HumanPX",
    "HumanPY",
    "HumanMode",
    "HumanState",
    "HumanAnime",
    "HumanWait",
    "HumanTime",
    "HumanFukiTime",
    "HumanFukiIndex",
]

OBJECT_FIELDS = [
    "ObjecX",
    "ObjecY",
    "ObjecZX",
    "ObjecZY",
    "ObjecCX",
    "ObjecCY",
    "ObjecWX",
    "ObjecWY",
    "ObjecSY",
    "ObjecUpDown",
]

ROOM_PATTERNS = [
    "floor0.seb",
    "floor1.seb",
    "floor2.seb",
    "SetOrigin",
    "DepthMethod",
    "DrawObj",
    "RenderGameScreen",
    "OnTouchCamera",
    "Camera",
    "camera",
]

EVENT_PATTERNS = [
    "NewGamePara",
    "DoEvent",
    "AddKaiwa",
    "AddKaiwaTalkData",
    "AddMessage",
    "EventGChange",
    "Print",
]


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8", errors="replace").splitlines()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def compact(value: str, limit: int = 260) -> str:
    text = " ".join(value.strip().split())
    return text if len(text) <= limit else text[: limit - 3] + "..."


def function_spans(lines: list[str]) -> list[tuple[int, str]]:
    return [
        (number, match.group("name"))
        for number, line in enumerate(lines, 1)
        if (match := FUNCTION_HEADER_RE.match(line))
    ]


def function_at_line(headers: list[tuple[int, str]], line_number: int) -> str | None:
    current = None
    for number, name in headers:
        if number > line_number:
            break
        current = name
    return current


def line_occurrences(path: Path, pattern: str, *, regex: bool = False, limit: int = SAMPLE_LIMIT) -> dict[str, Any]:
    lines = read_lines(path)
    matcher = re.compile(pattern) if regex else None
    rows = []
    total = 0
    headers = function_spans(lines)
    for number, line in enumerate(lines, 1):
        hit = bool(matcher.search(line)) if matcher else pattern in line
        if not hit:
            continue
        total += 1
        if len(rows) < limit:
            rows.append(
                {
                    "line": number,
                    "function": function_at_line(headers, number),
                    "text": compact(line),
                }
            )
    return {"count": total, "sample": rows}


def source_inventory(paths: list[Path], patterns: list[str]) -> dict[str, Any]:
    result = {}
    for path in paths:
        result[rel(path)] = {
            pattern: line_occurrences(path, pattern)
            for pattern in patterns
        }
    return result


def source_call_rows(path: Path, symbol: str) -> list[dict[str, Any]]:
    lines = read_lines(path)
    headers = function_spans(lines)
    rows = []
    for index, line in enumerate(lines):
        if symbol not in line or line.lstrip().startswith("//"):
            continue
        if re.search(rf"\b(?:void|undefined\w*|long|int)\s+{re.escape(symbol)}\b", line):
            continue
        snippet = [line]
        finish = index
        while finish + 1 < len(lines) and ");" not in "\n".join(snippet):
            finish += 1
            snippet.append(lines[finish])
        raw = " ".join(snippet)
        rows.append(
            {
                "source_line": index + 1,
                "end_line": finish + 1,
                "caller": function_at_line(headers, index + 1),
                "raw_call": compact(raw),
                "well_formed": ");" in raw,
            }
        )
    return [row for row in rows if row["caller"] != symbol]


def split_arguments(value: str) -> list[str]:
    arguments = []
    current = []
    depth = 0
    for char in value:
        if char in "([{":
            depth += 1
        elif char in ")]}":
            depth = max(0, depth - 1)
        if char == "," and depth == 0:
            arguments.append("".join(current).strip())
            current = []
        else:
            current.append(char)
    if current:
        arguments.append("".join(current).strip())
    return arguments


def drawhuman_selector_scan() -> dict[str, Any]:
    rows = source_call_rows(FORM_C, "form_GameForm__DrawHuman")
    selector_rows = []
    variable_driven = 0
    direct_40 = []
    direct_41 = []
    for row in rows:
        raw = row["raw_call"]
        match = re.search(r"form_GameForm__DrawHuman\s*\(", raw)
        if not match:
            continue
        args_text = raw[match.end() :]
        args_text = args_text.split(")", 1)[0]
        args = split_arguments(args_text)
        if len(args) < 7:
            continue
        # Recovered DrawHuman uses param_5 as imgFace and param_6 as imgBody:
        # the callee indexes GameForm+0x1150 with param_5 and +0x1158 with
        # param_6.  Keep the names explicit here because call sites often use
        # both selectors as literals.
        tface = args[4]
        tbody = args[5]
        if re.search(r"(?:^|\W)(?:40|0x28)(?:$|\W)", tface):
            direct_40.append({"source_line": row["source_line"], "caller": row["caller"], "tface_expression": tface, "raw_call": raw})
        elif re.search(r"(?:^|\W)(?:41|0x29)(?:$|\W)", tface):
            direct_41.append({"source_line": row["source_line"], "caller": row["caller"], "tface_expression": tface, "raw_call": raw})
        else:
            variable_driven += 1
        selector_rows.append(
            {
                "source_line": row["source_line"],
                "caller": row["caller"],
                "tbody_expression": tbody,
                "tface_expression": tface,
                "tmode_expression": args[6],
                "raw_call": raw,
            }
        )
    return {
        "source_file": rel(FORM_C),
        "symbol_reference_count": len(rows),
        "parsed_callsite_count": len(selector_rows),
        "unparsed_symbol_reference_count": len(rows) - len(selector_rows),
        "variable_driven_tface_count": variable_driven,
        "literal_tface_40_callsite_count": len(direct_40),
        "literal_tface_41_callsite_count": len(direct_41),
        "literal_tface_40_calls": direct_40[:SAMPLE_LIMIT],
        "literal_tface_41_calls": direct_41[:SAMPLE_LIMIT],
        "selector_sample": selector_rows[:SAMPLE_LIMIT],
        "asset_boundary": {
            "current_face_family": "face_0.png..face_35.png",
            "status": "TFace=40/41 remains unresolved; no alternate namespace promoted by this scan",
        },
    }


def uncovered_function_scan() -> list[dict[str, Any]]:
    translation = read_json(TRANSLATION)
    units = {row["symbol"]: row for row in translation["units"]}
    branch = read_json(BRANCH_INDEX)["functions"]
    targets = [
        "form_GameForm__NewGamePara",
        "form_GameForm__DoEvent",
        "kairo_unity_util_JarInflater__GetInputStream",
        "form_GameForm__GameScreenLayout",
        "form_GameForm__RenderGameScreen",
    ]
    rows = []
    source_paths = [FORM_C, METHOD_C, DUMP_CS, SCRIPT_JSON, NEWGAME_ASM, DOEVENT_ASM]
    for symbol in targets:
        unit = units[symbol]
        row: dict[str, Any] = {
            "symbol": symbol,
            "priority": unit.get("priority"),
            "source_status": unit.get("source_status"),
            "translation_evidence_ready": unit.get("evidence_ready"),
            "source_counts": {},
        }
        for path in source_paths:
            if symbol in path.read_text(encoding="utf-8", errors="replace"):
                row["source_counts"][rel(path)] = line_occurrences(path, symbol)["count"]
        if symbol in branch:
            structural = branch[symbol]
            row["assembly_structure"] = {
                "file": structural["file"],
                "instruction_count": structural["instruction_count"],
                "branch_count": structural["branch_count"],
                "basic_block_count": structural["basic_block_count"],
                "top_call_targets": structural["calls_by_target"][:12],
                "status": structural["status"],
            }
        rows.append(row)
    return rows


def field_scan(paths: list[Path], fields: list[str]) -> dict[str, Any]:
    result = {}
    for field in fields:
        per_file = {}
        total = 0
        for path in paths:
            hit = line_occurrences(path, field)
            per_file[rel(path)] = hit
            total += hit["count"]
        result[field] = {"total_count": total, "by_file": per_file}
    return result


def event_call_scan() -> dict[str, Any]:
    rows = {}
    for symbol in ["form_GameForm__AddKaiwa", "form_GameForm__AddKaiwaTalkData", "form_GameForm__AddMessage", "form_GameForm__EventGChange", "form_GameForm__Print"]:
        calls = source_call_rows(FORM_C, symbol)
        rows[symbol] = {
            "direct_source_callsite_count": len(calls),
            "sample": calls[:SAMPLE_LIMIT],
        }
    event_modes = read_json(EVENT_MODES)
    return {
        "source_file": rel(FORM_C),
        "calls": rows,
        "doevent_target_cluster_status": event_modes["conclusion"],
        "policy": event_modes["candidate_policy"],
    }


def build() -> dict[str, Any]:
    source_paths = [FORM_C, METHOD_C, DUMP_CS, SCRIPT_JSON, NEWGAME_ASM, DOEVENT_ASM]
    required = [
        *source_paths,
        TRANSLATION,
        BRANCH_INDEX,
        ASSET_AUDIT,
        ANIMATION_CONTRACT,
        EVENT_MODES,
        ROOM_CALLER,
        PRODUCER,
    ]
    missing = [rel(path) for path in required if not path.is_file()]
    if missing:
        raise RuntimeError("missing targeted scan inputs: " + ", ".join(missing))

    source_hashes = {
        rel(path): {"sha256": sha256(path), "bytes": path.stat().st_size}
        for path in source_paths
    }
    field_paths = [FORM_C, METHOD_C, DUMP_CS]
    room_scan = source_inventory([FORM_C, METHOD_C, NEWGAME_ASM, DOEVENT_ASM], ROOM_PATTERNS)
    direct_seb_count = sum(room_scan[rel(path)]["floor0.seb"]["count"] for path in [FORM_C, METHOD_C, NEWGAME_ASM, DOEVENT_ASM])

    return {
        "schema_version": "phase4-targeted-gap-scan-v1",
        "phase": "Phase4",
        "wave_scope": ["Wave0", "Wave1", "Wave2", "Wave3", "Wave4", "Wave5"],
        "source_roots_read_only": True,
        "legacy_equivalence": False,
        "status": "evidence_collected_open_semantics",
        "source_hashes": source_hashes,
        "scopes": {
            "function_availability": "translation coverage plus branch index for the five Wave0 uncovered/assembly-only units",
            "tface": "parsed DrawHuman call arguments from recovered form.c",
            "actor_and_object_fields": "symbol occurrence inventory in recovered C and dump.cs",
            "room_seb": "bounded C/Method/assembly occurrence inventory; no binary reconstruction",
            "event": "direct recovered-C producer calls plus existing DoEvent target-cluster policy",
        },
        "wave0_uncovered_functions": uncovered_function_scan(),
        "tface_scan": drawhuman_selector_scan(),
        "actor_field_scan": field_scan(field_paths, ACTOR_FIELDS),
        "object_field_scan": field_scan(field_paths, OBJECT_FIELDS),
        "room_seb_scan": {
            "by_file": room_scan,
            "direct_floor0_seb_occurrence_count_in_scoped_sources": direct_seb_count,
            "camera_symbol_interpretation": "occurrence inventory only; Camera/camera names do not prove a transform producer",
            "known_later_contracts": {
                "room_caller": {
                    "status": read_json(ROOM_CALLER)["status"],
                    "seb_caller_inventory": read_json(ROOM_CALLER)["seb_caller_inventory"],
                    "room_placement": read_json(ROOM_CALLER)["room_placement"],
                },
                "object_producer": {
                    "direct_floor0_seb_drawobj_callsite_count": read_json(PRODUCER)["seb_mapping"]["direct_floor0_seb_drawobj_callsite_count"],
                    "literal_floor0_seb_count_in_c_sources": read_json(PRODUCER)["seb_mapping"]["literal_floor0_seb_count_in_c_sources"],
                    "named_camera_symbol_reference_count_in_c": read_json(PRODUCER)["camera_transform_boundary"]["named_camera_symbol_reference_count_in_c"],
                },
            },
        },
        "event_touch_scan": event_call_scan(),
        "conclusions": [
            {
                "gap_key": "newgamepara_branch_semantics",
                "status": "evidence_collected_not_closed",
                "finding": "assembly structural metadata is available, but this scan does not assign initialization/reset/exit semantics",
                "next_action": "slice high-value branch clusters using caller/field context",
            },
            {
                "gap_key": "doevent_dispatch_lifecycle",
                "status": "evidence_collected_not_closed",
                "finding": "DoEvent remains assembly fallback; recovered-C producer calls and existing target clusters do not establish mode-to-branch mapping",
                "next_action": "trace only clusters reaching dialogue/message/event-change helpers",
            },
            {
                "gap_key": "tface_40_41_namespace",
                "status": "unresolved",
                "finding": "face asset family remains 0..35 while 40/41 need an alternate namespace or missing extraction; no safe promotion found",
                "next_action": "trace producer values/callers and preserve missing face layer",
            },
            {
                "gap_key": "universal_room_transform",
                "status": "evidence_collected_not_closed",
                "finding": "field and render symbol references exist, but a universal camera/world/isometric/pivot transform is not proven",
                "next_action": "search producer-side transform inputs or close as extraction-unavailable",
            },
            {
                "gap_key": "seb_room_caller_mapping",
                "status": "evidence_collected_not_closed",
                "finding": f"scoped source scan has {direct_seb_count} literal floor0.seb occurrences; local SEB consumer evidence does not identify the room caller",
                "next_action": "look for wider LoadSeb/resource caller or alternate asset extraction",
            },
        ],
        "artifact_inputs": [rel(path) for path in required if path.is_file()],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="compare generated output with the checked-in artifact")
    args = parser.parse_args()
    value = build()
    if args.check:
        if not OUTPUT.is_file():
            raise SystemExit(f"missing generated artifact: {rel(OUTPUT)}")
        actual = read_json(OUTPUT)
        if actual != value:
            raise SystemExit(f"artifact mismatch: {rel(OUTPUT)}")
        print(json.dumps({"status": "check_pass", "output": rel(OUTPUT)}, ensure_ascii=False))
        return
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "built", "output": rel(OUTPUT)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
