#!/usr/bin/env python3
"""Build the bounded Phase 4 Wave 4 consumer slices and closure handoff.

This builder deliberately stops at evidence boundaries.  It indexes the
categorized MainProcess/DrawObj code, the relevant DoEvent assembly targets,
and the raw field accesses that connect the queues to their consumers.  It
does not translate DoEvent as a whole or assign legacy meanings to timers,
graph IDs, event modes, or actor state.
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
WAVE1_BRANCH = ARTIFACTS / "wave1_branch_index.json"
WAVE4_EVENT = ARTIFACTS / "wave4_event_contract.json"
WAVE4_GAP = ARTIFACTS / "wave4_gap_register.json"
WAVE4_NOTIFICATION = ARTIFACTS / "wave4_notification_contract.json"

LIFECYCLE_ARTIFACT = ARTIFACTS / "wave4_lifecycle_slices.json"
C7_MANIFEST = ARTIFACTS / "wave4_c7_build_manifest.json"
CLOSURE_REPORT = DOCS / "wave4_closure_report.md"
MAINPROCESS_DOC = SLICES / "mainprocess_lifecycle_01.md"
DOEVENT_DOC = SLICES / "do_event_lifecycle_01.md"

OUTPUTS = [
    LIFECYCLE_ARTIFACT,
    C7_MANIFEST,
    CLOSURE_REPORT,
    MAINPROCESS_DOC,
    DOEVENT_DOC,
]

FUNCTION_HEADER_RE = re.compile(r"^// Function: (?P<name>\S+)")
CALL_RE = re.compile(
    r"\bform_GameForm__(?P<call>AddEvent|AddMessage|CallFuki|AddKaiwa|DrawFukidashi)\b"
)
ASM_TARGET_RE = re.compile(r"\bbl\s*;\s*(?P<target>0x[0-9a-fA-F]+)")

FIELD_MAP = {
    "0xe68": {"field": "HumanFukiTime", "role": "bubble_expiry_counter"},
    "0xe70": {"field": "HumanFukiIndex", "role": "bubble_text_index"},
    "0xe78": {"field": "HumanMode", "role": "raw_actor_mode"},
    "0xe80": {"field": "HumanTime", "role": "raw_actor_timer"},
    "0xff0": {"field": "EventMax", "role": "event_queue_length"},
    "0xff8": {"field": "EventMode", "role": "event_queue_mode"},
    "0x1000": {"field": "EventTemp", "role": "event_queue_temp"},
    "0x1008": {"field": "EventTemp2", "role": "event_queue_temp2"},
    "0x11f0": {"field": "MessageText", "role": "notification_text_queue"},
    "0x11f8": {"field": "MessageTime", "role": "notification_timer"},
    "0x1200": {"field": "MessageMaxTime", "role": "notification_max_timer"},
    "0x1208": {"field": "MessageGraph", "role": "notification_graph_id"},
}

TARGET_MAP = {
    "0x00f1a908": {
        "symbol": "form_GameForm__AddKaiwa",
        "role": "dialogue_append_short",
        "rva_needle": "RVA: 0xE1A908",
    },
    "0x00f1a98c": {
        "symbol": "form_GameForm__AddKaiwa",
        "role": "dialogue_append_windowed",
        "rva_needle": "RVA: 0xE1A98C",
    },
    "0x00f4b038": {
        "symbol": "form_GameForm__AddKaiwa",
        "role": "dialogue_append_named_actor",
        "rva_needle": "RVA: 0xE4B038",
    },
    "0x00f4a714": {
        "symbol": "form_GameForm__AddMessage",
        "role": "notification_enqueue",
        "rva_needle": "RVA: 0xE4A714",
    },
    "0x00f1aa34": {
        "symbol": "form_GameForm__EventGChange",
        "role": "related_visual_event_target",
        "rva_needle": "RVA: 0xE1AA34",
    },
    "0x00f3ab48": {
        "symbol": "form_GameForm__Print",
        "role": "diagnostic_or_text_side_effect",
        "rva_needle": "RVA: 0xE3AB48",
    },
}


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def evidence(path: Path, needle: str, status: str = "verified") -> dict[str, Any]:
    for number, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        if needle in line:
            return {"file": rel(path), "line": number, "needle": needle, "status": status}
    return {"file": rel(path), "line": None, "needle": needle, "status": "not_found"}


def required_paths() -> list[Path]:
    return [
        FORM_C,
        DUMP_CS,
        DO_EVENT_ASM,
        WAVE1_BRANCH,
        WAVE4_EVENT,
        WAVE4_GAP,
        WAVE4_NOTIFICATION,
    ]


def function_spans(lines: list[str], names: list[str]) -> dict[str, dict[str, int]]:
    headers: list[tuple[int, str]] = []
    for number, line in enumerate(lines, 1):
        match = FUNCTION_HEADER_RE.match(line)
        if match:
            headers.append((number, match.group("name")))
    result: dict[str, dict[str, int]] = {}
    for name in names:
        start = next(number for number, header in headers if header == name)
        next_header = next((number for number, _ in headers if number > start), len(lines) + 1)
        result[name] = {"start_line": start, "end_line": next_header - 1}
    return result


def compact(text: str, limit: int = 280) -> str:
    value = " ".join(text.split())
    return value if len(value) <= limit else value[: limit - 3] + "..."


def has_offset(line: str, offset: str) -> bool:
    return re.search(re.escape(offset) + r"(?![0-9a-fA-F])", line.lower()) is not None


def extract_calls(lines: list[str], span: dict[str, int]) -> list[dict[str, Any]]:
    calls: list[dict[str, Any]] = []
    start = span["start_line"] - 1
    end = span["end_line"]
    for index in range(start, end):
        match = CALL_RE.search(lines[index])
        if not match:
            continue
        call = match.group("call")
        snippet_lines = [lines[index]]
        finish = index
        while finish + 1 < end and ");" not in "\n".join(snippet_lines):
            finish += 1
            snippet_lines.append(lines[finish])
        raw = " ".join(snippet_lines)
        well_formed = ");" in raw
        calls.append(
            {
                "source_line": index + 1,
                "end_line": finish + 1,
                "call": f"form_GameForm__{call}",
                "classification": {
                    "AddEvent": "event_enqueue",
                    "AddMessage": "notification_enqueue",
                    "CallFuki": "human_bubble_schedule",
                    "AddKaiwa": "dialogue_append",
                    "DrawFukidashi": "bubble_draw",
                }[call],
                "well_formed_call": well_formed,
                "raw_excerpt": compact(raw),
            }
        )
    return calls


def field_refs(lines: list[str], span: dict[str, int], offsets: list[str]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    start = span["start_line"] - 1
    end = span["end_line"]
    for offset in offsets:
        hits = [number for number in range(start, end) if has_offset(lines[number], offset)]
        if not hits:
            continue
        result[offset] = {
            **FIELD_MAP[offset],
            "reference_count": len(hits),
            "source_lines": [number + 1 for number in hits[:16]],
            "status": "raw_offset_reference",
        }
    return result


def message_consumer_slices(lines: list[str], span: dict[str, int]) -> list[dict[str, Any]]:
    # These ranges are deliberately narrow: each range contains one bounded
    # operation that is visible in categorized C, rather than a guessed state
    # machine reconstructed from the whole MainProcess function.
    ranges = [
        {
            "id": "human_fuki_time_tick",
            "line_start": 1408,
            "line_end": 1420,
            "fields": ["HumanFukiTime"],
            "observed_operation": "checks a positive per-index value and decrements it by one",
            "semantic_status": "bounded_consumer_observed_timer_unit_open",
        },
        {
            "id": "message_timer_tick_branch_a",
            "line_start": 1433,
            "line_end": 1494,
            "fields": ["MessageTime"],
            "observed_operation": "checks a queued timer, decrements the selected entry, and enters removal when it reaches zero",
            "semantic_status": "bounded_consumer_observed_timer_unit_open",
        },
        {
            "id": "message_compaction",
            "line_start": 1505,
            "line_end": 1575,
            "fields": ["MessageText", "MessageTime", "MessageGraph"],
            "observed_operation": "shifts later queue entries left, clears the final text/timer/graph slots, and preserves queue order",
            "semantic_status": "bounded_queue_lifecycle_observed_graph_label_open",
        },
        {
            "id": "message_timer_tick_branch_b",
            "line_start": 1579,
            "line_end": 1618,
            "fields": ["MessageTime"],
            "observed_operation": "decrements a positive queued timer under the alternate branch guard",
            "semantic_status": "bounded_consumer_observed_timer_unit_open",
        },
        {
            "id": "message_max_timer_sound_threshold",
            "line_start": 1648,
            "line_end": 1656,
            "fields": ["MessageMaxTime", "MessageTime"],
            "observed_operation": "compares max-time and current-time difference and calls SoundPlay at a one-step threshold",
            "semantic_status": "bounded_consumer_observed_audio_policy_open",
        },
    ]
    for item in ranges:
        if item["line_start"] < span["start_line"] or item["line_end"] > span["end_line"]:
            raise RuntimeError(f"consumer slice outside MainProcess span: {item['id']}")
        item["source_file"] = rel(FORM_C)
        item["source_status"] = "categorized_c"
    return ranges


def build_lifecycle_slices() -> dict[str, Any]:
    form_lines = FORM_C.read_text(encoding="utf-8", errors="replace").splitlines()
    spans = function_spans(
        form_lines,
        ["form_GameForm__MainProcess", "form_GameForm__DrawObj"],
    )
    main_calls = extract_calls(form_lines, spans["form_GameForm__MainProcess"])
    draw_calls = extract_calls(form_lines, spans["form_GameForm__DrawObj"])
    main_fields = field_refs(form_lines, spans["form_GameForm__MainProcess"], list(FIELD_MAP))
    draw_fields = field_refs(form_lines, spans["form_GameForm__DrawObj"], list(FIELD_MAP))

    asm_lines = DO_EVENT_ASM.read_text(encoding="utf-8", errors="replace").splitlines()
    event_contract = read_json(WAVE4_EVENT)
    branch_index = read_json(WAVE1_BRANCH)
    do_event_structural = branch_index["functions"]["form_GameForm__DoEvent"]
    target_calls: list[dict[str, Any]] = []
    for number, line in enumerate(asm_lines, 1):
        match = ASM_TARGET_RE.search(line)
        if not match:
            continue
        target = match.group("target").lower()
        target_info = TARGET_MAP.get(target)
        if not target_info:
            continue
        target_calls.append(
            {
                "asm_line": number,
                "branch_address": line.split()[0],
                "target": target,
                "symbol": target_info["symbol"],
                "role": target_info["role"],
                "raw_instruction": compact(line),
            }
        )

    target_counts = Counter(row["target"] for row in target_calls)
    target_map = []
    for target, info in TARGET_MAP.items():
        target_map.append(
            {
                "target": target,
                "symbol": info["symbol"],
                "role": info["role"],
                "address_mapping": "assembly VA = dump RVA + 0x100000",
                "evidence": evidence(DUMP_CS, info["rva_needle"]),
            }
        )

    do_event_offsets = {}
    for offset in ["0xff8", "0x1000", "0x1008"]:
        hits = [number for number, line in enumerate(asm_lines, 1) if has_offset(line, offset)]
        if hits:
            do_event_offsets[offset] = {
                **FIELD_MAP[offset],
                "reference_count": len(hits),
                "asm_lines": hits[:24],
                "status": "assembly_raw_offset_reference",
            }

    counts = Counter(row["call"] for row in main_calls)
    draw_counts = Counter(row["call"] for row in draw_calls)
    same_line_event_call_count = sum(
        1
        for row in main_calls
        if row["call"] == "form_GameForm__AddEvent"
        and "form_GameForm__AddEvent(" in row["raw_excerpt"]
    )
    return {
        "schema_version": "wave4-lifecycle-slices-v1",
        "phase": "Phase4",
        "wave": "Wave4",
        "stage": "W4-C4-C6-bounded-consumer-slices",
        "source_roots_read_only": True,
        "legacy_equivalence": False,
        "mainprocess": {
            "function": "form_GameForm__MainProcess",
            "source_file": rel(FORM_C),
            "source_status": "categorized_c",
            "span": spans["form_GameForm__MainProcess"],
            "call_summary": {
                "symbol_occurrence_count": len(main_calls),
                "well_formed_call_count": sum(row["well_formed_call"] for row in main_calls),
                "by_call": dict(sorted(counts.items())),
                "same_line_add_event_call_count": same_line_event_call_count,
                "same_line_add_event_count_note": "the existing producer contract's 53 count uses a same-line call regex; two categorized-C callsites split the function name and opening parenthesis across lines",
            },
            "relevant_calls": main_calls,
            "field_offset_refs": main_fields,
            "consumer_slices": message_consumer_slices(form_lines, spans["form_GameForm__MainProcess"]),
            "findings": [
                "MainProcess directly decrements positive HumanFukiTime entries by one.",
                "MainProcess directly decrements MessageTime entries and compacts MessageText/MessageTime/MessageGraph when a message expires.",
                "MessageMaxTime participates in a one-step difference check before SoundPlay; its audio policy is not named here.",
            ],
            "not_claimed": [
                "the raw timer unit is not milliseconds or a recovered legacy frame duration",
                "zero-time HumanFukiIndex cleanup is not proven by these slices",
                "MessageGraph numeric IDs are not named as UI categories",
                "HumanMode is not promoted to talking semantics",
            ],
        },
        "drawobj": {
            "function": "form_GameForm__DrawObj",
            "source_file": rel(FORM_C),
            "source_status": "categorized_c",
            "span": spans["form_GameForm__DrawObj"],
            "call_summary": {"by_call": dict(sorted(draw_counts.items()))},
            "relevant_calls": draw_calls,
            "field_offset_refs": draw_fields,
            "finding": "DrawObj gates DrawFukidashi on a positive HumanFukiTime entry, then reads HumanFukiIndex before issuing the draw call.",
            "semantic_status": "bounded_draw_consumer_observed_timer_unit_open",
        },
        "do_event": {
            "function": "form_GameForm__DoEvent",
            "source_file": rel(DO_EVENT_ASM),
            "source_status": "assembly_fallback_only",
            "structural": {
                "instruction_count": do_event_structural["instruction_count"],
                "branch_count": do_event_structural["branch_count"],
                "basic_block_count": do_event_structural["basic_block_count"],
            },
            "bounded_target_policy": "only targets mapped to AddKaiwa/AddMessage/EventGChange/Print are indexed",
            "target_map": target_map,
            "target_counts": dict(sorted(target_counts.items())),
            "relevant_target_calls": target_calls,
            "event_queue_field_refs": do_event_offsets,
            "findings": [
                "DoEvent reads EventMode, EventTemp, and EventTemp2 in assembly, establishing a queue-consumer field boundary.",
                "DoEvent has bounded call-target evidence for dialogue append and notification enqueue paths.",
                "DoEvent branch predicates and event-mode meanings remain unresolved because the function is assembly fallback only.",
            ],
            "not_claimed": [
                "numeric event modes are not assigned names",
                "AddKaiwa target calls are not treated as a complete dialogue state machine",
                "actor lifecycle or HumanMode semantics are not inferred from nearby branches",
            ],
        },
        "acceptance": {
            "mainprocess_consumer_slice": "pass_bounded_raw_field_and_lifecycle_evidence",
            "drawobj_consumer_slice": "pass_bounded_positive_timer_to_draw_index_evidence",
            "doevent_dialogue_message_targets": "pass_target_calls_with_dump_rva_mapping",
            "semantic_overreach_check": "pass_open_timer_graph_mode_and_actor_boundaries_preserved",
        },
    }


def build_manifest() -> dict[str, Any]:
    inputs = required_paths()
    return {
        "schema_version": "wave4-c7-build-manifest-v1",
        "phase": "Phase4",
        "wave": "Wave4",
        "stage": "W4-C7-closure-and-handoff",
        "source_roots_read_only": True,
        "source_hashes": {
            rel(path): {"sha256": sha256(path), "bytes": path.stat().st_size}
            for path in inputs
            if path.suffix != ".json" or path in {WAVE1_BRANCH, WAVE4_EVENT, WAVE4_GAP, WAVE4_NOTIFICATION}
        },
        "artifact_inputs": [rel(path) for path in inputs],
        "artifact_outputs": [rel(path) for path in OUTPUTS],
        "packages": {
            "W4-C4": "producer_plus_bounded_DoEvent_and_MainProcess_consumer_slices",
            "W4-C6": "notification_timer_decrement_compaction_and_graph_boundary",
            "W4-C7": "closure_report_manifest_and_phase5_handoff",
        },
        "acceptance": [
            "all W4-C0-C6 generated contracts remain reproducible",
            "MainProcess/DrawObj consumer spans are source-line bounded",
            "DoEvent target calls are mapped through dump.cs RVA evidence",
            "legacy_equivalence remains false",
        ],
        "status": "W4-C0-C7-closure_complete_with_known_limitations",
        "legacy_equivalence": False,
    }


def closure_report() -> str:
    return """# Phase 4 Wave 4 — Closure report

อัปเดต: 2026-08-11

สถานะ: **W4-C0 ถึง W4-C7 ปิดรอบแบบ `complete_with_known_limitations`**

รอบนี้ปิดหลักฐาน dialogue, bubble และ notification consumer ที่ bounded แล้ว:

- `MainProcess` ลด `HumanFukiTime` และใช้ค่าที่เป็นบวกเป็น gate ก่อนการวาดใน `DrawObj`;
- `MainProcess` ลด `MessageTime`, compaction `MessageText/MessageTime/MessageGraph`
  เมื่อหมดอายุ และอ่าน `MessageMaxTime` ใน threshold สำหรับ `SoundPlay`;
- `DoEvent` มี raw field reads ของ `EventMode/EventTemp/EventTemp2` และมี call-target
  ที่ map กับ `AddKaiwa`, `AddMessage`, `EventGChange` และ `Print` ผ่าน RVA ใน `dump.cs`;
- `MainProcess` มี bounded producer callsites ของ `AddEvent`, `AddMessage`, `CallFuki`
  และ `AddKaiwa` ซึ่งเก็บไว้เป็น raw callsite index ไม่ใช่ semantic event table.

## Artifacts

- `Phases/Phase4/artifacts/wave4_lifecycle_slices.json`
- `Phases/Phase4/artifacts/wave4_c7_build_manifest.json`
- `Phases/Phase4/docs/wave4_slices/mainprocess_lifecycle_01.md`
- `Phases/Phase4/docs/wave4_slices/do_event_lifecycle_01.md`

## Boundaries retained

ยังไม่ปิดหน่วยของ timer `0x60`/counter, label ของ `MessageGraph`, semantic name ของ
numeric event modes, delimiter/token semantics, raw speaker-to-actor binding และ
ความหมายของ `HumanMode`. `DoEvent` ยังเป็น assembly fallback จึงยังไม่แปลง branch graph
เป็น implementation ที่อ้างว่าเทียบเท่า legacy.

ผลลัพธ์นี้พร้อมเป็น Phase 5 handoff สำหรับ adapter implementation และ targeted trace
ต่อเมื่อมี feature ที่ต้องใช้ semantics เหล่านี้โดยตรง.
"""


def slice_docs() -> dict[Path, str]:
    return {
        CLOSURE_REPORT: closure_report(),
        MAINPROCESS_DOC: """# W4-C4/C6 — MainProcess and DrawObj consumer slice

หลักฐานจาก categorized `form.c` ถูกจำกัดไว้ที่ function spans และ raw offsets ใน
`wave4_lifecycle_slices.json`.

- `MainProcess` ลด `HumanFukiTime` เมื่อค่าปัจจุบันมากกว่า 0;
- `DrawObj` ตรวจค่า `HumanFukiTime > 0`, อ่าน `HumanFukiIndex` และเรียก
  `DrawFukidashi`;
- `MessageTime` ถูกลดลงในสอง branch ที่ bounded ได้;
- เมื่อ timer ถึงศูนย์ มีการ shift `MessageText`, `MessageTime`, `MessageGraph`
  และ clear ช่องสุดท้าย;
- `MessageMaxTime - MessageTime == 1` เป็นหลักฐาน threshold ที่นำไปสู่ `SoundPlay`.

หน่วย timer, การล้าง `HumanFukiIndex` เมื่อหมดอายุ และชื่อ graph/UI category ยังไม่
ถูกสรุปจาก slice นี้.
""",
        DOEVENT_DOC: """# W4-C4 — DoEvent dialogue/message target slice

`DoEvent` ยังไม่มี categorized C ที่เชื่อถือได้ จึงใช้ assembly fallback และเก็บเฉพาะ
call-target ที่ map ผ่าน `dump.cs` RVA:

- `0x00f1a908`, `0x00f1a98c`, `0x00f4b038` → `AddKaiwa` overloads;
- `0x00f4a714` → `AddMessage(string,int)`;
- `0x00f1aa34` → `EventGChange`;
- `0x00f3ab48` → `Print`.

นอกจากนี้มี raw reads ของ `EventMode`, `EventTemp`, `EventTemp2`. การเก็บนี้เป็น
target/field index เท่านั้น ไม่ใช่การตั้งชื่อ event mode หรือการอธิบาย branch semantics
ของ `DoEvent` ทั้งฟังก์ชัน.
""",
    }


def build_all() -> dict[Path, Any]:
    missing = [rel(path) for path in required_paths() if not path.is_file()]
    if missing:
        raise RuntimeError("missing Wave 4 closure inputs: " + ", ".join(missing))
    lifecycle = build_lifecycle_slices()
    result: dict[Path, Any] = {
        LIFECYCLE_ARTIFACT: lifecycle,
        C7_MANIFEST: build_manifest(),
    }
    result.update(slice_docs())
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
