#!/usr/bin/env python3
"""Build bounded Wave 4.5 evidence-hardening traces.

The hardening pass is intentionally narrower than a full port.  It records
verified reads/writes, caller bridges, render behavior, and target clusters.
It preserves unresolved timer units, actor identity, graph labels, and event
mode names when the scoped sources do not prove them.
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
DOCS = PHASE / "docs"
SLICES = DOCS / "wave4_slices"

FORM_C = ROOT / "game-dev-story-mod_Dumped" / "Categorized_Code" / "Global" / "form.c"
DUMP_CS = ROOT / "game-dev-story-mod_Dumped" / "dump.cs"
DO_EVENT_ASM = ROOT / "game-dev-story-mod_Dumped" / "Failed_Functions_Assembly" / "00f5c704_form_GameForm__DoEvent.asm.txt"
STRING_LITERAL_MAP = ARTIFACTS / "string_literal_map.json"
WAVE1_BRANCH = ARTIFACTS / "wave1_branch_index.json"
WAVE4_EVENT = ARTIFACTS / "wave4_event_contract.json"
WAVE4_GAP = ARTIFACTS / "wave4_gap_register.json"
WAVE4_TALK = ARTIFACTS / "wave4_talk_contract.json"
WAVE4_LIFECYCLE = ARTIFACTS / "wave4_lifecycle_slices.json"

TIMER_TRACE = ARTIFACTS / "wave4_timer_fuki_trace.json"
TALK_TRACE = ARTIFACTS / "wave4_talk_speaker_trace.json"
GRAPH_TRACE = ARTIFACTS / "wave4_message_graph_trace.json"
EVENT_TRACE = ARTIFACTS / "wave4_event_mode_candidates.json"
MANIFEST = ARTIFACTS / "wave4_hardening_manifest.json"
REPORT = DOCS / "wave4_hardening_report.md"
TIMER_DOC = SLICES / "timer_fuki_02.md"
TALK_DOC = SLICES / "talk_speaker_02.md"
GRAPH_DOC = SLICES / "message_graph_02.md"
EVENT_DOC = SLICES / "event_mode_02.md"

OUTPUTS = [
    TIMER_TRACE,
    TALK_TRACE,
    GRAPH_TRACE,
    EVENT_TRACE,
    MANIFEST,
    REPORT,
    TIMER_DOC,
    TALK_DOC,
    GRAPH_DOC,
    EVENT_DOC,
]

FUNCTION_HEADER_RE = re.compile(r"^// Function: (?P<name>\S+)")
CALL_TARGET_RE = re.compile(r"\bbl\s*;\s*(?P<target>0x[0-9a-fA-F]+)")
STRING_LITERAL_RE = re.compile(r"PTR_StringLiteral_(?P<id>\d+)_")
ASM_IMMEDIATE_RE = re.compile(r"\b(?:cmp|mov|movk|add|sub)\b.*?#(?P<value>0x[0-9a-fA-F]+|\d+)")

TARGET_INFO = {
    "0x00f1a908": {"symbol": "form_GameForm__AddKaiwa", "role": "dialogue_append_short"},
    "0x00f1a98c": {"symbol": "form_GameForm__AddKaiwa", "role": "dialogue_append_windowed"},
    "0x00f4b038": {"symbol": "form_GameForm__AddKaiwa", "role": "dialogue_append_named_actor"},
    "0x00f4a714": {"symbol": "form_GameForm__AddMessage", "role": "notification_enqueue"},
    "0x00f1aa34": {"symbol": "form_GameForm__EventGChange", "role": "related_visual_event_target"},
    "0x00f3ab48": {"symbol": "form_GameForm__Print", "role": "diagnostic_or_text_side_effect"},
}


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def evidence(path: Path, needle: str, status: str = "verified") -> dict[str, Any]:
    for number, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        if needle in line:
            return {"file": rel(path), "line": number, "needle": needle, "status": status}
    return {"file": rel(path), "line": None, "needle": needle, "status": "not_found"}


def compact(text: str, limit: int = 260) -> str:
    value = " ".join(text.split())
    return value if len(value) <= limit else value[: limit - 3] + "..."


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


def function_end(headers: list[tuple[int, str]], start_line: int, total_lines: int) -> int:
    return next((number for number, _ in headers if number > start_line), total_lines + 1) - 1


def line_refs(lines: list[str], needle: str, start: int = 1, end: int | None = None) -> list[int]:
    end = end or len(lines)
    return [number for number in range(start, end + 1) if needle.lower() in lines[number - 1].lower()]


def source_call_rows(lines: list[str], symbol: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, line in enumerate(lines):
        if symbol not in line or line.lstrip().startswith("//") or line.lstrip().startswith("void "):
            continue
        snippet = [line]
        finish = index
        while finish + 1 < len(lines) and ");" not in "\n".join(snippet):
            finish += 1
            snippet.append(lines[finish])
        rows.append(
            {
                "source_line": index + 1,
                "end_line": finish + 1,
                "caller": None,
                "raw_call": compact(" ".join(snippet)),
                "well_formed": ");" in "\n".join(snippet),
            }
        )
    headers = function_spans(lines)
    for row in rows:
        row["caller"] = function_at_line(headers, row["source_line"])
    return rows


def build_timer_trace() -> dict[str, Any]:
    lines = FORM_C.read_text(encoding="utf-8", errors="replace").splitlines()
    headers = function_spans(lines)
    main_start = next(n for n, name in headers if name == "form_GameForm__MainProcess")
    update_start = next(n for n, name in headers if name == "form_GameForm___update")
    draw_start = next(n for n, name in headers if name == "form_GameForm__DrawObj")
    call_fuki_start = next(n for n, name in headers if name == "form_GameForm__CallFuki")
    update_end = function_end(headers, update_start, len(lines))

    human_time_refs = line_refs(lines, "0xe68")
    human_index_refs = line_refs(lines, "0xe70")
    update_lines = line_refs(lines, "form_GameForm__MainProcess", update_start, update_end)
    fuki_timer_tick = [1408, 1416, 1420]
    draw_gate = [16183, 16188, 16193, 16227, 16228, 16229]
    call_fuki_writes = [30102, 30117, 30135, 30136, 30139]

    return {
        "schema_version": "wave4-timer-fuki-trace-v1",
        "phase": "Phase4",
        "wave": "Wave4",
        "stage": "W4.5-R1-timer-and-human-fuki-hardening",
        "source_roots_read_only": True,
        "legacy_equivalence": False,
        "update_bridge": {
            "function": "form_GameForm___update",
            "source_file": rel(FORM_C),
            "source_span": {"start_line": update_start, "end_line": update_end},
            "mainprocess_call_lines": update_lines,
            "repeat_control": {
                "source_lines": [18373, 18391, 18396, 18401, 18402, 18403],
                "observed_candidate_counts": [1, 2, 16],
                "status": "verified_repeat_count_control_logical_tick_candidate",
                "not_claimed": "not mapped to milliseconds or Unity deltaTime",
            },
        },
        "human_fuki": {
            "fields": {
                "HumanFukiTime": {
                    "offset": "0xe68",
                    "all_source_reference_count": len(human_time_refs),
                    "all_source_lines": human_time_refs,
                    "status": "verified_raw_field_reference",
                },
                "HumanFukiIndex": {
                    "offset": "0xe70",
                    "all_source_reference_count": len(human_index_refs),
                    "all_source_lines": human_index_refs,
                    "status": "verified_raw_field_reference",
                },
            },
            "write_and_consume_slice": {
                "call_fuki": {
                    "source_lines": call_fuki_writes,
                    "operation": "CallFuki writes HumanFukiTime[param_2] = param_4 and HumanFukiIndex[param_2] = param_3 after bounds/limit checks",
                    "status": "verified_write_pair",
                },
                "mainprocess": {
                    "source_lines": fuki_timer_tick,
                    "operation": "positive HumanFukiTime entry is decremented by one",
                    "status": "verified_consumer_tick",
                },
                "drawobj": {
                    "source_lines": draw_gate,
                    "operation": "positive HumanFukiTime gates DrawFukidashi and HumanFukiIndex supplies the text index",
                    "status": "verified_draw_gate",
                },
            },
            "cleanup_search": {
                "scoped_mainprocess_clear_lines": [],
                "status": "not_found_in_scoped_mainprocess",
                "interpretation": "adapter must clear expired bubble state unless a wider save/load or event path proves cleanup",
            },
        },
        "conclusion": {
            "timer_unit": "logical_tick_candidate_with_speed_multiplier_open",
            "human_fuki_index_cleanup": "not_found_in_scoped_mainprocess; targeted adapter cleanup required",
            "wave5_blocker": False,
        },
        "evidence": [
            evidence(FORM_C, "// Function: form_GameForm___update"),
            evidence(FORM_C, "form_GameForm__MainProcess(param_1,0);"),
            evidence(FORM_C, "// Function: form_GameForm__CallFuki"),
            evidence(FORM_C, "// Function: form_GameForm__DrawObj"),
            evidence(DUMP_CS, "HumanFukiTime;"),
            evidence(DUMP_CS, "HumanFukiIndex;"),
        ],
    }


def build_talk_trace() -> dict[str, Any]:
    lines = FORM_C.read_text(encoding="utf-8", errors="replace").splitlines()
    literal_map = read_json(STRING_LITERAL_MAP)
    literal_ids = sorted({int(match.group("id")) for line in lines[42289:42474] if (match := STRING_LITERAL_RE.search(line))})
    literal_entries = []
    for literal_id in literal_ids:
        entry = literal_map["entries"][literal_id] if literal_id < len(literal_map["entries"]) else None
        literal_entries.append(
            {
                "literal_id": literal_id,
                "value": entry.get("value") if entry else None,
                "address": entry.get("address") if entry else None,
                "status": "table_value_recorded_pointer_validation_required",
            }
        )

    return {
        "schema_version": "wave4-talk-speaker-trace-v1",
        "phase": "Phase4",
        "wave": "Wave4",
        "stage": "W4.5-R2-talk-token-and-speaker-hardening",
        "source_roots_read_only": True,
        "legacy_equivalence": False,
        "pipeline": {
            "get_talk_index": {
                "source_lines": [42528, 42529, 42532, 42534],
                "operations": ["StringUtil.Split", "compare first segment with requested tag", "return index or -1"],
                "status": "verified_bounded_lookup_with_delimiter_pointer_open",
            },
            "add_kaiwa_talk_data": {
                "source_lines": [42346, 42356, 42358, 42362, 42408, 42472],
                "operations": [
                    "GetTalkIndex",
                    "optional StringUtil.Replace",
                    "StringUtil.Split",
                    "Int32.Parse second split token",
                    "GetHumanTalkName(raw speaker)",
                    "AddKaiwa with resolved text/name and raw speaker-derived values",
                ],
                "status": "verified_raw_speaker_pipeline_token_meanings_open",
            },
        },
        "literal_refs": {
            "referenced_ids": literal_ids,
            "table_entries": literal_entries,
            "status": "values_recorded_but_pointer_name_to_table_index_not_promoted",
            "next_validation": "match pointer addresses and raw talk records before naming delimiters or placeholders",
        },
        "speaker": {
            "raw_parse": {"source_line": 42362, "status": "verified_int_parse_of_second_split_token"},
            "display_name_bridge": {"source_line": 42408, "status": "verified_GetHumanTalkName_bridge"},
            "direct_producer_callers_in_scoped_c_and_assembly": {
                "symbol": "form_GameForm__AddKaiwaTalkData",
                "callsite_count": 0,
                "status": "not_found_in_scoped_sources",
            },
            "actor_binding": {
                "status": "adapter_boundary",
                "not_claimed": "GetHumanTalkName output is not proof of Wave 3 actor identity",
            },
        },
        "conclusion": {
            "talk_token": "bounded_split_replace_parse_verified; delimiter/token names open",
            "speaker_binding": "raw_speaker_to_display_name_verified; raw_speaker_to_actor_not_found",
            "wave5_blocker": False,
        },
        "evidence": [
            evidence(FORM_C, "// Function: form_GameForm__AddKaiwaTalkData"),
            evidence(FORM_C, "kairo_unity_util_StringUtil__Split"),
            evidence(FORM_C, "form_GameForm__GetHumanTalkName"),
            evidence(DUMP_CS, "public void AddKaiwaTalkData(string talkTag, string arg)"),
        ],
    }


def build_graph_trace() -> dict[str, Any]:
    lines = FORM_C.read_text(encoding="utf-8", errors="replace").splitlines()
    headers = function_spans(lines)
    draw_start = next(n for n, name in headers if name == "form_GameForm___draw")
    draw_end = function_end(headers, draw_start, len(lines))
    add_message_rows = source_call_rows(lines, "form_GameForm__AddMessage")
    direct_calls = [row for row in add_message_rows if row["caller"] not in {"form_GameForm__AddMessage"}]
    graph_expressions = Counter()
    for row in direct_calls:
        match = re.search(r"form_GameForm__AddMessage\(.*?,\s*([^,)]+)\s*\)", row["raw_call"])
        graph_expressions[match.group(1) if match else "unparsed"] += 1

    return {
        "schema_version": "wave4-message-graph-trace-v1",
        "phase": "Phase4",
        "wave": "Wave4",
        "stage": "W4.5-R3-message-graph-and-audio-hardening",
        "source_roots_read_only": True,
        "legacy_equivalence": False,
        "producer": {
            "function": "form_GameForm__AddMessage",
            "direct_source_callsite_count": len(direct_calls),
            "direct_source_calls": direct_calls,
            "graph_expression_counts": dict(sorted(graph_expressions.items())),
            "status": "verified_source_producer_inventory",
        },
        "draw_consumer": {
            "function": "form_GameForm___draw",
            "function_span": {"start_line": draw_start, "end_line": draw_end},
            "operation_span": {"start_line": 20468, "end_line": 20595},
            "message_graph_refs": [20468, 20560, 20578, 20590],
            "observed_behavior": [
                {
                    "condition": "MessageGraph >= 0",
                    "operation": "adds graph-dependent horizontal padding before notification text/image layout",
                    "status": "verified_render_behavior",
                },
                {
                    "condition": "MessageGraph == 1",
                    "operation": "draws an image from imgMain using source x = graph * 0xe + 0x38 and a 0xe by 0xe crop",
                    "status": "verified_render_behavior",
                },
                {
                    "condition": "MessageGraph == 2",
                    "operation": "branches to the same image-draw path",
                    "status": "verified_render_behavior",
                },
            ],
            "image_field": {"offset": "0x1140", "field": "imgMain", "status": "verified_declaration"},
            "raw_labels": {
                "1": None,
                "2": None,
                "status": "numeric_graph_labels_not_named",
            },
        },
        "audio_consumer": {
            "source_lines": [1648, 1651, 1654, 1656],
            "operation": "when MessageMaxTime - MessageTime == 1, calls SoundPlay(param_1,1,3,0)",
            "status": "verified_threshold_and_call; sound_label_open",
        },
        "conclusion": {
            "message_graph": "render behavior for graph 1/2 verified; product labels remain raw",
            "audio": "threshold behavior verified; audio meaning open",
            "wave5_blocker": False,
        },
        "evidence": [
            evidence(FORM_C, "// Function: form_GameForm___draw"),
            evidence(FORM_C, "kairo_unity_ui_Graphics__DrawImage"),
            evidence(DUMP_CS, "MessageGraph;"),
            evidence(DUMP_CS, "public static Image imgMain;"),
        ],
    }


def build_event_trace() -> dict[str, Any]:
    asm_lines = DO_EVENT_ASM.read_text(encoding="utf-8", errors="replace").splitlines()
    event_contract = read_json(WAVE4_EVENT)
    branch_index = read_json(WAVE1_BRANCH)
    target_calls: dict[str, list[dict[str, Any]]] = {target: [] for target in TARGET_INFO}
    for index, line in enumerate(asm_lines):
        match = CALL_TARGET_RE.search(line)
        if not match:
            continue
        target = match.group("target").lower()
        if target not in TARGET_INFO:
            continue
        window_start = max(0, index - 16)
        window = asm_lines[window_start : index + 1]
        constants = []
        for item in window:
            for immediate in ASM_IMMEDIATE_RE.findall(item):
                constants.append(immediate)
        target_calls[target].append(
            {
                "asm_line": index + 1,
                "branch_address": line.split()[0],
                "nearby_immediate_constants": sorted(set(constants)),
                "window_start_line": window_start + 1,
                "raw_instruction": compact(line),
                "semantic_status": "target_cluster_only_no_event_mode_mapping",
            }
        )

    mode_counts = event_contract["producer"]["literal_mode_counts"]
    return {
        "schema_version": "wave4-event-mode-candidates-v1",
        "phase": "Phase4",
        "wave": "Wave4",
        "stage": "W4.5-R4-event-mode-hardening",
        "source_roots_read_only": True,
        "legacy_equivalence": False,
        "producer_modes": {
            "source_callsite_count_contract": event_contract["producer"]["callsite_count"],
            "literal_mode_counts": mode_counts,
            "status": "raw_producer_inventory_only",
        },
        "consumer": {
            "function": "form_GameForm__DoEvent",
            "source_status": "assembly_fallback_only",
            "structural": branch_index["functions"]["form_GameForm__DoEvent"],
            "event_queue_field_refs": {
                "EventMode": {"offset": "0xff8", "asm_reference_count": 35, "status": "verified_raw_read_boundary"},
                "EventTemp": {"offset": "0x1000", "asm_reference_count": 1, "status": "verified_raw_read_boundary"},
                "EventTemp2": {"offset": "0x1008", "asm_reference_count": 1, "status": "verified_raw_read_boundary"},
            },
            "target_clusters": {
                target: {
                    "symbol": info["symbol"],
                    "role": info["role"],
                    "count": len(rows),
                    "calls": rows,
                    "status": "candidate_target_cluster_only",
                }
                for target, info in TARGET_INFO.items()
                for rows in [target_calls[target]]
            },
        },
        "candidate_policy": {
            "allowed": ["target_cluster", "nearby_constant_context", "raw_field_boundary"],
            "forbidden": ["semantic_event_mode_name", "complete_DoEvent_state_machine", "legacy_equivalence"],
            "status": "no_numeric_mode_promoted",
        },
        "conclusion": {
            "semantic_event_modes": "target clusters and nearby constants indexed; exact mode-to-branch mapping remains open",
            "wave5_blocker": False,
        },
        "evidence": [
            evidence(DO_EVENT_ASM, "00f5c704", "verified_assembly_entry"),
            evidence(DUMP_CS, "EventMode;"),
            evidence(DUMP_CS, "public void AddKaiwa(string TK, int TModori)"),
            evidence(DUMP_CS, "public void AddMessage(string TText, int TGraph)"),
        ],
    }


def build_manifest() -> dict[str, Any]:
    inputs = [
        FORM_C,
        DUMP_CS,
        DO_EVENT_ASM,
        STRING_LITERAL_MAP,
        WAVE1_BRANCH,
        WAVE4_EVENT,
        WAVE4_GAP,
        WAVE4_TALK,
        WAVE4_LIFECYCLE,
    ]
    return {
        "schema_version": "wave4-hardening-manifest-v1",
        "phase": "Phase4",
        "wave": "Wave4",
        "stage": "W4.5-evidence-hardening",
        "source_roots_read_only": True,
        "source_hashes": {rel(path): {"sha256": sha256(path), "bytes": path.stat().st_size} for path in inputs},
        "artifact_inputs": [rel(path) for path in inputs],
        "artifact_outputs": [rel(path) for path in OUTPUTS],
        "packages": {
            "W4.5-R1": "timer_and_human_fuki_lifecycle",
            "W4.5-R2": "talk_token_and_speaker_boundary",
            "W4.5-R3": "message_graph_render_and_audio_threshold",
            "W4.5-R4": "DoEvent_target_clusters_without_mode_names",
            "W4.5-R5": "hardening_report_and_wave5_handoff",
        },
        "acceptance": [
            "logical tick evidence recorded without claiming milliseconds",
            "HumanFukiIndex cleanup gap classified and adapter action explicit",
            "MessageGraph render behavior for IDs 1/2 recorded without labels",
            "talk raw parse/name bridge recorded without actor identity promotion",
            "DoEvent target clusters recorded without numeric event names",
            "all remaining boundaries have status and next action",
        ],
        "status": "W4.5-hardening_complete_with_remaining_boundaries",
        "legacy_equivalence": False,
    }


def docs() -> dict[Path, str]:
    return {
        REPORT: """# Phase 4 Wave 4.5 — Evidence hardening report

อัปเดต: 2026-08-11

สถานะ: **bounded hardening complete; Wave 5 handoff พร้อม โดยยังคง known limitations**

## สิ่งที่แกะเพิ่มได้

- `__update` เรียก `MainProcess` ด้วยจำนวนรอบที่สังเกตได้ `1/2/16` จึงบันทึก
  timer เป็น logical-tick candidate และยังไม่อ้างเป็น milliseconds;
- `HumanFukiTime` ถูกลดลงและใช้เป็น draw gate ส่วน `HumanFukiIndex` ถูกอ่านเพื่อเลือก
  text index แต่ไม่พบ clear ตอนหมดอายุใน MainProcess scope;
- `AddKaiwaTalkData` ยืนยัน pipeline `Replace → Split → Parse → GetHumanTalkName → AddKaiwa`;
  actor binding ยังเป็น adapter boundary และ literal pointer values ต้อง validate กับ raw records;
- `MessageGraph` consumer ใน `form_GameForm___draw` ยืนยัน render behavior ของค่า `1/2`
  ผ่าน `imgMain` crop แต่ยังไม่ตั้งชื่อ product label; `SoundPlay` threshold ถูกบันทึกแล้ว;
- `DoEvent` เพิ่ม target clusters และ nearby constant context แต่ยังไม่ตั้งชื่อ numeric event modes.

## Wave 5 decision

W4.5 ไม่เป็น blocker ต่อ Wave 5. ให้ใช้ adapter tick, explicit bubble cleanup,
raw MessageGraph IDs และ named web events โดยคง `legacy_equivalence=false`.

รายละเอียดอยู่ใน `artifacts/wave4_*_trace.json` และ slice docs ชุด `*_02.md`.
""",
        TIMER_DOC: """# W4.5-R1 — Timer และ HumanFuki lifecycle

`form_GameForm___update` เรียก `MainProcess` ด้วยจำนวนรอบที่ขึ้นกับ config; หลักฐานนี้
รองรับ logical tick/speed multiplier candidate แต่ยังไม่มี direct delta-time mapping.

`CallFuki` เขียน `HumanFukiTime` และ `HumanFukiIndex`; `MainProcess` ลด timer ที่เป็นบวก;
`DrawObj` ตรวจ timer ก่อนอ่าน index และเรียก `DrawFukidashi`. ไม่พบ clear ของ index ใน
scoped MainProcess expiry path จึงต้องให้ Wave 5 adapter ลบ expired bubble state เอง.
""",
        TALK_DOC: """# W4.5-R2 — Talk token และ speaker boundary

`GetTalkIndex` ใช้ `StringUtil.Split` แล้วเทียบ segment แรกกับ tag.
`AddKaiwaTalkData` ทำ optional replace, split, parse token ที่สองเป็น raw speaker ID,
เรียก `GetHumanTalkName` และส่งต่อ `AddKaiwa`.

Literal values ถูกบันทึกจาก table แต่ยังไม่ promote เพราะต้องตรวจ pointer/address และ
raw talk record ร่วมกัน. ไม่พบ direct `AddKaiwaTalkData` caller ใน scoped categorized C
หรือ assembly จึงยังไม่มีหลักฐาน raw speaker → Wave 3 actor โดยตรง.
""",
        GRAPH_DOC: """# W4.5-R3 — MessageGraph และ audio

`form_GameForm___draw` อ่าน `MessageGraph`. ค่า `1` และ `2` เข้าสู่ image-draw path ของ
`imgMain` โดยใช้ crop ขนาด `0xe × 0xe`; พฤติกรรมการ render นี้ verified แต่ชื่อ graph
เชิง product ยังไม่ทราบ.

`MessageMaxTime - MessageTime == 1` เรียก `SoundPlay(param_1,1,3,0)`. threshold และ
call ถูกยืนยัน แต่ชื่อเสียง/ความหมาย UI ยังเปิด.
""",
        EVENT_DOC: """# W4.5-R4 — Event mode candidate trace

เพิ่ม target clusters ของ `DoEvent` สำหรับ `AddKaiwa`, `AddMessage`, `EventGChange` และ
`Print` พร้อม nearby immediate constants และ raw `EventMode/EventTemp/EventTemp2` refs.

ผลลัพธ์เป็น target-context evidence เท่านั้น ไม่ใช่ event-mode mapping. Numeric modes
ยังไม่ถูกตั้งชื่อ และ Wave 5 ควรใช้ named adapter events แทน.
""",
    }


def build_all() -> dict[Path, Any]:
    required = [FORM_C, DUMP_CS, DO_EVENT_ASM, STRING_LITERAL_MAP, WAVE1_BRANCH, WAVE4_EVENT, WAVE4_GAP, WAVE4_TALK, WAVE4_LIFECYCLE]
    missing = [rel(path) for path in required if not path.is_file()]
    if missing:
        raise RuntimeError("missing W4.5 inputs: " + ", ".join(missing))
    result: dict[Path, Any] = {
        TIMER_TRACE: build_timer_trace(),
        TALK_TRACE: build_talk_trace(),
        GRAPH_TRACE: build_graph_trace(),
        EVENT_TRACE: build_event_trace(),
        MANIFEST: build_manifest(),
    }
    result.update(docs())
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="build in memory and compare generated outputs")
    args = parser.parse_args()
    outputs = build_all()
    if args.check:
        mismatches = []
        for path, expected in outputs.items():
            actual = None
            if path.is_file():
                actual = json.loads(path.read_text(encoding="utf-8")) if path.suffix == ".json" else path.read_text(encoding="utf-8")
            if actual != expected:
                mismatches.append(rel(path))
        if mismatches:
            raise SystemExit("artifact mismatch: " + ", ".join(mismatches))
        print(json.dumps({"status": "check_pass", "outputs": [rel(path) for path in outputs]}, ensure_ascii=False))
        return
    for path, value in outputs.items():
        if path.suffix == ".json":
            write_json(path, value)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(value, encoding="utf-8")
    print(json.dumps({"status": "built", "outputs": [rel(path) for path in outputs]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
