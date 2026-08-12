#!/usr/bin/env python3
"""Build the bounded Phase 4 Wave 4 dialogue/lifecycle contracts.

The builder only reads extraction/source roots and writes generated artifacts below
``Phases/Phase4``.  It records evidence boundaries; it does not claim that raw
event, mode, timer, locale, or speaker IDs have full legacy semantics.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[3]
PHASE = ROOT / "Phases" / "Phase4"
ARTIFACTS = PHASE / "artifacts"
DOCS = PHASE / "docs"
SLICES = DOCS / "wave4_slices"
LOCALE_DIR = ROOT / "game-dev-story-mod_Sprites" / "language"

FORM_C = ROOT / "game-dev-story-mod_Dumped" / "Categorized_Code" / "Global" / "form.c"
MAIN_C = ROOT / "game-dev-story-mod_Dumped" / "Categorized_Code" / "Global" / "main.c"
KAIRO_C = ROOT / "game-dev-story-mod_Dumped" / "Categorized_Code" / "Global" / "kairo.c"
DUMP_CS = ROOT / "game-dev-story-mod_Dumped" / "dump.cs"
DO_EVENT_ASM = ROOT / "game-dev-story-mod_Dumped" / "Failed_Functions_Assembly" / "00f5c704_form_GameForm__DoEvent.asm.txt"
PHASE3_DOC = ROOT / "Phases" / "Phase3" / "docs" / "kairosoft_language_system.md"
WAVE1_BRANCH = ARTIFACTS / "wave1_branch_index.json"
WAVE3_C7 = ARTIFACTS / "wave3_c7_build_manifest.json"
WAVE3_SPAWN = ARTIFACTS / "wave3_spawn_fixture.json"
WAVE3_E2E = ARTIFACTS / "wave3_actor_e2e_fixture.json"

OUTPUTS = [
    ARTIFACTS / "wave4_build_manifest.json",
    ARTIFACTS / "wave4_gap_register.json",
    ARTIFACTS / "wave4_locale_contract.json",
    ARTIFACTS / "wave4_locale_fixture.json",
    ARTIFACTS / "wave4_talk_contract.json",
    ARTIFACTS / "wave4_talk_fixture.json",
    ARTIFACTS / "wave4_bubble_contract.json",
    ARTIFACTS / "wave4_bubble_fixture.json",
    ARTIFACTS / "wave4_event_contract.json",
    ARTIFACTS / "wave4_event_fixture.json",
    ARTIFACTS / "wave4_notification_contract.json",
    ARTIFACTS / "wave4_notification_fixture.json",
    ARTIFACTS / "wave4_actor_dialogue_fixture.json",
    DOCS / "wave4_plan.md",
    SLICES / "language_lookup_01.md",
    SLICES / "talk_data_01.md",
    SLICES / "bubble_lifecycle_01.md",
    SLICES / "event_dispatch_01.md",
    SLICES / "message_bridge_01.md",
]

PLACEHOLDER_RE = re.compile(r"<\d+>")
EVENT_CALL_RE = re.compile(r"form_GameForm__AddEvent\((?P<args>.*?)\);", re.DOTALL)


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


def source_line(path: Path, needle: str) -> int | None:
    for number, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        if needle in line:
            return number
    return None


def evidence(path: Path, needle: str, status: str = "verified") -> dict[str, Any]:
    return {"file": rel(path), "line": source_line(path, needle), "needle": needle, "status": status}


def required_paths() -> list[Path]:
    return [
        FORM_C,
        MAIN_C,
        KAIRO_C,
        DUMP_CS,
        DO_EVENT_ASM,
        PHASE3_DOC,
        WAVE1_BRANCH,
        WAVE3_C7,
        WAVE3_SPAWN,
        WAVE3_E2E,
        *sorted(LOCALE_DIR.glob("GameDevStory_*.csv")),
    ]


def split_call_args(value: str) -> list[str]:
    result: list[str] = []
    current: list[str] = []
    depth = 0
    for char in value:
        if char in "([{":
            depth += 1
        elif char in ")]}":
            depth = max(0, depth - 1)
        if char == "," and depth == 0:
            result.append("".join(current).strip())
            current = []
        else:
            current.append(char)
    if current:
        result.append("".join(current).strip())
    return result


def parse_locale(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    text = raw.decode("utf-8-sig")
    metadata: dict[str, str] = {}
    entries: dict[str, str] = {}
    duplicate_ids: list[str] = []
    empty_ids: list[str] = []
    placeholder_ids: dict[str, list[str]] = {}
    reader = csv.reader(io.StringIO(text))
    for row_number, row in enumerate(reader, 1):
        if not row:
            continue
        key = row[0].strip()
        if key.startswith("@"):
            metadata[key[1:]] = row[1] if len(row) > 1 else ""
            continue
        if not key.startswith("#"):
            continue
        value = row[1] if len(row) > 1 else ""
        if key in entries:
            duplicate_ids.append(key)
        entries[key] = value
        if not value:
            empty_ids.append(key)
        tokens = sorted(set(PLACEHOLDER_RE.findall(value)))
        if tokens:
            placeholder_ids[key] = tokens

    suffix = path.stem.rsplit("_", 1)[-1]
    return {
        "file": rel(path),
        "file_suffix": suffix,
        "metadata": metadata,
        "record_count": len(entries),
        "duplicate_ids": sorted(set(duplicate_ids)),
        "empty_ids": sorted(set(empty_ids)),
        "placeholder_record_count": len(placeholder_ids),
        "placeholder_examples": [
            {"id": key, "tokens": placeholder_ids[key]}
            for key in sorted(placeholder_ids)[:8]
        ],
        "bom": raw.startswith(b"\xef\xbb\xbf"),
        "utf8_strict": True,
        "sha256": sha256(path),
        "bytes": len(raw),
        "_entries": entries,
    }


def build_locale_contract(locales: list[dict[str, Any]]) -> tuple[dict[str, Any], dict[str, Any]]:
    all_ids = sorted({key for locale in locales for key in locale["_entries"]})
    locale_entries = {locale["file"]: dict(locale["_entries"]) for locale in locales}
    locale_rows = []
    for locale in locales:
        entries = locale_entries[locale["file"]]
        missing = sorted(set(all_ids) - set(entries))
        locale_rows.append(
            {
                **{key: value for key, value in locale.items() if key != "_entries"},
                "missing_from_union_count": len(missing),
                "missing_from_union_examples": missing[:8],
            }
        )

    placeholder_example: dict[str, Any] | None = None
    for locale in locales:
        for key, value in locale_entries[locale["file"]].items():
            tokens = sorted(set(PLACEHOLDER_RE.findall(value)))
            if tokens:
                placeholder_example = {
                    "locale": locale["metadata"].get("language", locale["file_suffix"]),
                    "id": key,
                    "tokens": tokens,
                    "text_length": len(value),
                }
                break
        if placeholder_example:
            break

    contract = {
        "schema_version": "wave4-locale-contract-v1",
        "phase": "Phase4",
        "wave": "Wave4",
        "stage": "W4-C1-language-locale-contract",
        "source_roots_read_only": True,
        "source_policy": "CSV is source-of-truth; no text is inferred or translated by this builder",
        "locale_count": len(locale_rows),
        "union_record_count": len(all_ids),
        "locales": locale_rows,
        "runtime_contract": {
            "lookup_input": ["id", "requested_locale", "args"],
            "lookup_output": ["text", "resolved_locale", "placeholder_tokens", "status", "source_file"],
            "fallback_policy": "configured_default_locale",
            "default_locale": "th",
            "default_locale_status": "web_adapter_decision_not_legacy_fact",
            "english_source_status": "not_present_in_current_language_directory",
            "placeholder_policy": "preserve_tokens_and_validate_args_before_substitution",
            "empty_result_policy": "return_explicit_missing_or_empty_status",
        },
        "evidence": [
            evidence(PHASE3_DOC, "มี 12 ภาษา"),
            evidence(PHASE3_DOC, "GameDevStory_EN.csv"),
            evidence(KAIRO_C, "kairo_unity_util_Language__SetTextTable"),
            evidence(KAIRO_C, "kairo_unity_util_Language__TranslateText"),
            evidence(KAIRO_C, "kairo_unity_util_Language___translateText2"),
        ],
        "summary": {
            "duplicate_id_count": sum(len(row["duplicate_ids"]) for row in locale_rows),
            "empty_id_count": sum(len(row["empty_ids"]) for row in locale_rows),
            "bom_failures": sum(not row["bom"] for row in locale_rows),
            "strict_utf8_failures": sum(not row["utf8_strict"] for row in locale_rows),
            "placeholder_example": placeholder_example,
            "status": "contract_ready_with_fallback_and_token_semantics_explicit",
        },
    }

    sample_ids = [key for key in ("#00000", "#00001", "#00002") if key in all_ids]
    fixture = {
        "schema_version": "wave4-locale-fixture-v1",
        "phase": "Phase4",
        "wave": "Wave4",
        "stage": "W4-C1-language-fixture",
        "source_roots_read_only": True,
        "fixture_scope": "deterministic lookup contract; not a full translation of all gameplay text",
        "source_contract": "Phases/Phase4/artifacts/wave4_locale_contract.json",
        "cases": [
            {
                "id": "existing_record_samples",
                "input": {"ids": sample_ids, "requested_locale": "th", "args": []},
                "expected": {"status": "csv_record_present", "source_namespace": "language_id"},
            },
            {
                "id": "placeholder_validation",
                "input": {"example": placeholder_example or "no_placeholder_found"},
                "expected": {"status": "preserve_and_validate_tokens"},
            },
            {
                "id": "missing_id",
                "input": {"id": "#__missing__", "requested_locale": "th", "args": []},
                "expected": {"status": "missing_key", "text": None},
            },
            {
                "id": "locale_fallback",
                "input": {"id": sample_ids[0] if sample_ids else "#00000", "requested_locale": "en", "args": []},
                "expected": {
                    "status": "fallback_required",
                    "fallback_locale": "th",
                    "legacy_equivalence": False,
                },
            },
        ],
        "status": "ready_for_runtime_lookup_adapter",
    }
    return contract, fixture


def build_talk_contract() -> tuple[dict[str, Any], dict[str, Any]]:
    functions = [
        {
            "symbol": "main_AppData__GetTalkTexts",
            "source_status": "categorized_c",
            "bounded_behavior": "resolve talk index, replace optional argument, split raw record, normalize data segments and concatenate output",
            "semantic_status": "verified_bounded_behavior_token_meanings_open",
            "evidence": [evidence(MAIN_C, "// Function: main_AppData__GetTalkTexts")],
        },
        {
            "symbol": "form_GameForm__GetTalkIndex",
            "source_status": "categorized_c",
            "bounded_behavior": "scan AppData talk table, split each record, compare its first segment to the requested tag, return index or -1",
            "semantic_status": "verified_bounded_behavior",
            "evidence": [evidence(FORM_C, "// Function: form_GameForm__GetTalkIndex")],
        },
        {
            "symbol": "form_GameForm__AddKaiwaTalkData",
            "source_status": "categorized_c",
            "bounded_behavior": "resolve talk data, parse the second split token as a raw speaker/chara value, resolve speaker name and forward to AddKaiwa",
            "semantic_status": "verified_bounded_behavior_raw_speaker_namespace",
            "evidence": [evidence(FORM_C, "// Function: form_GameForm__AddKaiwaTalkData")],
        },
        {
            "symbol": "form_GameForm__GetHumanTalkName",
            "source_status": "categorized_c",
            "bounded_behavior": "default values index KaiwaHumanSetName; four negative raw IDs use localized special-name branches",
            "semantic_status": "verified_raw_branch_special_labels_not_promoted",
            "evidence": [evidence(FORM_C, "// Function: form_GameForm__GetHumanTalkName")],
        },
        {
            "symbol": "form_GameForm__AddKaiwa",
            "source_status": "categorized_c",
            "bounded_behavior": "reset dialogue state, split/wrap text into KaiwaLine storage and update bounded dialogue fields",
            "semantic_status": "verified_bounded_storage_layout_timing_open",
            "evidence": [evidence(FORM_C, "// Function: form_GameForm__AddKaiwa")],
        },
    ]
    fields = []
    for name in [
        "KaiwaHumanSetName",
        "KaiwaHumanSetFaceG",
        "KaiwaHumanSetBodyG",
        "KaiwaMax",
        "KaiwaTime",
        "KaiwaPage",
        "KaiwaName",
        "KaiwaLine",
    ]:
        fields.append({"field": name, "evidence": evidence(DUMP_CS, f"{name};"), "status": "verified_declaration"})

    contract = {
        "schema_version": "wave4-talk-contract-v1",
        "phase": "Phase4",
        "wave": "Wave4",
        "stage": "W4-C2-talk-index-and-dialogue-contract",
        "source_roots_read_only": True,
        "namespaces": {
            "talk_tag": "source record lookup key; not a language ID",
            "talk_index": "zero-based runtime table index returned by GetTalkIndex",
            "language_id": "CSV/text-table ID namespace",
            "raw_speaker_id": "value parsed by AddKaiwaTalkData and passed to GetHumanTalkName",
            "actor_id": "stable web adapter identity from Wave 3; not a recovered legacy field",
        },
        "functions": functions,
        "fields": fields,
        "special_raw_speaker_ids": {
            "values": [-5, -4, -3, -2],
            "status": "verified_branch_values_labels_not_decoded",
            "policy": "keep raw IDs until localized literal mapping is independently verified",
        },
        "runtime_contract": {
            "resolve_talk": ["talk_tag", "args", "locale"],
            "resolve_talk_output": ["talk_index", "raw_segments", "formatted_text", "raw_speaker_id", "status"],
            "speaker_binding": "raw_speaker_id_to_actor_id_is_adapter_boundary_until_producer_evidence_exists",
            "line_storage": "KaiwaLine",
            "timing_status": "unknown",
            "legacy_equivalence": False,
        },
        "evidence": [
            evidence(FORM_C, "form_GameForm__GetTalkIndex"),
            evidence(MAIN_C, "form_GameForm__GetTalkIndex"),
            evidence(FORM_C, "form_GameForm__GetHumanTalkName"),
            evidence(DUMP_CS, "public void AddKaiwaTalkData(string talkTag, string arg)"),
            evidence(DUMP_CS, "public static string[] KaiwaLine"),
        ],
        "status": "bounded_talk_contract_ready_semantic_token_and_timing_gaps_open",
    }
    fixture = {
        "schema_version": "wave4-talk-fixture-v1",
        "phase": "Phase4",
        "wave": "Wave4",
        "stage": "W4-C2-talk-fixture",
        "source_roots_read_only": True,
        "fixture_scope": "neutral algorithm fixture; no invented production talk tag",
        "source_contract": "Phases/Phase4/artifacts/wave4_talk_contract.json",
        "cases": [
            {
                "id": "tag_scan_hit",
                "input": {"raw_records": [["fixture.tag", "2", "line-a", "line-b"]], "tag": "fixture.tag"},
                "expected": {"talk_index": 0, "raw_speaker_id": 2, "segments": ["line-a", "line-b"], "status": "neutral_contract"},
            },
            {
                "id": "tag_scan_miss",
                "input": {"raw_records": [["fixture.tag", "2", "line-a"]], "tag": "missing.tag"},
                "expected": {"talk_index": -1, "status": "not_found"},
            },
            {
                "id": "special_raw_speaker",
                "input": {"raw_speaker_id": -2},
                "expected": {"status": "localized_special_branch_required", "semantic_label": None},
            },
            {
                "id": "actor_binding",
                "input": {"raw_speaker_id": 2, "actor_id": "adapter.actor.0"},
                "expected": {"status": "adapter_binding_only", "legacy_equivalence": False},
            },
        ],
        "status": "ready_for_bubble_and_actor_dialogue_integration",
    }
    return contract, fixture


def build_bubble_contract() -> tuple[dict[str, Any], dict[str, Any]]:
    fields = []
    for name in ["fukiList", "FukiMax", "FukiCX", "FukiCY", "FukiWX", "HumanFukiTime", "HumanFukiIndex"]:
        fields.append({"field": name, "evidence": evidence(DUMP_CS, f"{name};"), "status": "verified_declaration"})

    contract = {
        "schema_version": "wave4-bubble-contract-v1",
        "phase": "Phase4",
        "wave": "Wave4",
        "stage": "W4-C3-fukidashi-bubble-contract",
        "source_roots_read_only": True,
        "fields": fields,
        "functions": [
            {
                "symbol": "form_GameForm__AddFuki",
                "bounded_behavior": "write TCX/TCY/TWX into FukiCX/FukiCY/FukiWX at FukiMax and increment FukiMax",
                "status": "verified_bounded_write",
                "evidence": [evidence(FORM_C, "// Function: form_GameForm__AddFuki")],
            },
            {
                "symbol": "form_GameForm__CallFuki",
                "bounded_behavior": "apply bounded time/index values to HumanFukiTime/HumanFukiIndex after active-human and limit checks",
                "status": "verified_bounded_write_timer_semantics_open",
                "evidence": [evidence(FORM_C, "// Function: form_GameForm__CallFuki")],
            },
            {
                "symbol": "form_GameForm__DrawFukidashi",
                "bounded_behavior": "read fukiList by index, translate with Language.LT, trim, construct Balloon and draw at supplied coordinates",
                "status": "verified_bounded_draw_contract",
                "evidence": [evidence(FORM_C, "// Function: form_GameForm__DrawFukidashi")],
            },
        ],
        "runtime_contract": {
            "bubble_record": ["bubble_id", "actor_id", "text_or_talk_ref", "position", "expires_at", "status"],
            "raw_mapping": {"index": "HumanFukiIndex", "time": "HumanFukiTime"},
            "ui_boundary": "Balloon and TextLayout are contract-only; browser rendering is an adapter",
            "expiry_unit": "unknown_until_MainProcess_consumer_trace",
            "legacy_equivalence": False,
        },
        "evidence": [
            evidence(FORM_C, "form_GameForm__DrawObj"),
            evidence(FORM_C, "form_GameForm__DrawFukidashi"),
            evidence(KAIRO_C, "kairo_unity_util_Language__LT"),
        ],
        "status": "bubble_storage_and_draw_boundary_ready_expiry_semantics_open",
    }
    fixture = {
        "schema_version": "wave4-bubble-fixture-v1",
        "phase": "Phase4",
        "wave": "Wave4",
        "stage": "W4-C3-bubble-fixture",
        "source_roots_read_only": True,
        "fixture_scope": "deterministic adapter clock with raw field provenance kept separate",
        "source_contract": "Phases/Phase4/artifacts/wave4_bubble_contract.json",
        "adapter_clock": {"frame_ms": 100, "legacy_timing_status": "unknown"},
        "cases": [
            {
                "id": "attach_and_draw",
                "input": {"actor_id": "adapter.actor.0", "fuki_index": 0, "fuki_time": 3, "position": [100, 200]},
                "expected": {"status": "draw_command_ready", "raw_fields": {"HumanFukiIndex": 0, "HumanFukiTime": 3}, "legacy_equivalence": False},
            },
            {
                "id": "expire",
                "input": {"actor_id": "adapter.actor.0", "clock_ticks": 3},
                "expected": {"status": "adapter_expired", "legacy_timer_equivalence": False},
            },
            {
                "id": "missing_text",
                "input": {"actor_id": "adapter.actor.0", "fuki_index": 999},
                "expected": {"status": "explicit_missing_bubble_text", "silent_empty_fallback": False},
            },
        ],
        "status": "ready_for_actor_dialogue_composition",
    }
    return contract, fixture


def build_event_contract() -> tuple[dict[str, Any], dict[str, Any]]:
    form_text = FORM_C.read_text(encoding="utf-8", errors="replace")
    producers = []
    for match in EVENT_CALL_RE.finditer(form_text):
        line = form_text.count("\n", 0, match.start()) + 1
        args = split_call_args(" ".join(match.group("args").split()))
        user_args = args[1:] if len(args) >= 4 else args
        mode = user_args[0] if user_args else None
        temp = user_args[1] if len(user_args) > 1 else None
        temp2 = user_args[2] if len(user_args) > 2 else None
        producers.append(
            {
                "source_line": line,
                "caller_file": rel(FORM_C),
                "mode_expression": mode,
                "temp_expression": temp,
                "temp2_expression": temp2,
                "raw_call": "form_GameForm__AddEvent(" + " ".join(match.group("args").split()) + ");",
                "semantic_status": "raw_producer_only",
            }
        )
    literal_modes = Counter(row["mode_expression"] for row in producers if row["mode_expression"] is not None)
    branch_index = read_json(WAVE1_BRANCH)
    do_event = branch_index["functions"]["form_GameForm__DoEvent"]

    contract = {
        "schema_version": "wave4-event-contract-v1",
        "phase": "Phase4",
        "wave": "Wave4",
        "stage": "W4-C4-event-and-lifecycle-bridge",
        "source_roots_read_only": True,
        "queue_fields": [
            {"field": "EventMode", "evidence": evidence(DUMP_CS, "EventMode;"), "status": "verified_declaration"},
            {"field": "EventTemp", "evidence": evidence(DUMP_CS, "EventTemp;"), "status": "verified_declaration"},
            {"field": "EventTemp2", "evidence": evidence(DUMP_CS, "EventTemp2;"), "status": "verified_declaration"},
            {"field": "EventMax", "evidence": evidence(DUMP_CS, "EventMax;"), "status": "verified_declaration"},
        ],
        "producer": {
            "function": "form_GameForm__AddEvent",
            "bounded_behavior": "scan EventMode for first zero slot and write mode/temp/temp2 into parallel arrays",
            "status": "verified_bounded_queue_write",
            "evidence": [evidence(FORM_C, "// Function: form_GameForm__AddEvent")],
            "callsite_count": len(producers),
            "literal_mode_counts": dict(sorted(literal_modes.items())),
        },
        "consumer": {
            "function": "form_GameForm__DoEvent",
            "source_status": "assembly_fallback_only",
            "instruction_count": do_event["instruction_count"],
            "branch_count": do_event["branch_count"],
            "basic_block_count": do_event["basic_block_count"],
            "status": "structural_branch_index_only",
            "semantic_policy": "slice_only_branches_that_touch_dialogue_bubble_message_or_actor_lifecycle",
            "known_call_targets": do_event["calls_by_target"],
            "evidence": [evidence(DO_EVENT_ASM, "00f5c704", "verified_assembly_entry")],
        },
        "related_functions": [
            {"symbol": "form_GameForm__MainProcess", "status": "bounded_slice_required"},
            {"symbol": "form_GameForm__AddKaiwa", "status": "W4-C2"},
            {"symbol": "form_GameForm__AddMessage", "status": "W4-C6"},
            {"symbol": "form_GameForm__CallFuki", "status": "W4-C3"},
        ],
        "semantic_status": "event_modes_not_named_without_consumer_evidence",
        "legacy_equivalence": False,
        "evidence": [
            evidence(FORM_C, "form_GameForm__AddEvent"),
            evidence(DUMP_CS, "internal static int[] EventMode"),
            evidence(DO_EVENT_ASM, "00f5c704"),
        ],
        "status": "producer_index_ready_consumer_semantics_open",
    }
    fixture = {
        "schema_version": "wave4-event-fixture-v1",
        "phase": "Phase4",
        "wave": "Wave4",
        "stage": "W4-C4-event-fixture",
        "source_roots_read_only": True,
        "fixture_scope": "queue contract; no semantic label is assigned to numeric event mode",
        "source_contract": "Phases/Phase4/artifacts/wave4_event_contract.json",
        "cases": [
            {
                "id": "first_free_slot",
                "input": {"mode": "raw_mode_0xe", "temp": 4, "temp2": 0, "queue": [0, 0, 0]},
                "expected": {"slot": 0, "fields": {"EventMode": "raw_mode_0xe", "EventTemp": 4, "EventTemp2": 0}, "status": "queue_write_contract"},
            },
            {
                "id": "preserve_raw_mode",
                "input": {"mode_expression": "uVar22", "temp_expression": "uVar41", "temp2_expression": "0"},
                "expected": {"semantic_label": None, "status": "raw_expression_only"},
            },
            {
                "id": "full_queue",
                "input": {"queue_state": "all_slots_nonzero"},
                "expected": {"status": "bounded_no_free_slot_path_requires_consumer_trace"},
            },
        ],
        "status": "ready_for_bounded_DoEvent_dialogue_slices",
    }
    return contract, fixture


def build_notification_contract() -> tuple[dict[str, Any], dict[str, Any]]:
    fields = []
    for name in ["MessageText", "MessageTime", "MessageMaxTime", "MessageGraph"]:
        fields.append({"field": name, "evidence": evidence(DUMP_CS, f"{name};"), "status": "verified_declaration"})
    contract = {
        "schema_version": "wave4-notification-contract-v1",
        "phase": "Phase4",
        "wave": "Wave4",
        "stage": "W4-C6-message-notification-bridge",
        "source_roots_read_only": True,
        "fields": fields,
        "function": {
            "symbol": "form_GameForm__AddMessage",
            "overloads": [
                {"signature": "AddMessage(string TText)", "default_graph": -1},
                {"signature": "AddMessage(string TText, int TGraph)", "graph_argument": "TGraph"},
            ],
            "bounded_behavior": "scan MessageTime for first zero slot, write MessageText, set MessageTime and MessageMaxTime to 0x60, then write MessageGraph",
            "status": "verified_bounded_queue_write",
            "evidence": [evidence(FORM_C, "// Function: form_GameForm__AddMessage")],
        },
        "runtime_contract": {
            "notification_record": ["message_id", "text_or_text_ref", "graph_id", "created_at", "expires_at", "status"],
            "default_lifetime_raw": 96,
            "default_lifetime_unit": "unknown",
            "graph_semantics": "raw_graph_id_not_decoded",
            "office_event_mapping": "adapter-only until source event consumer is traced",
            "legacy_equivalence": False,
        },
        "not_in_scope": [
            "sales/ranking/news gameplay notifications",
            "inferring graph meaning from numeric value",
            "claiming raw 0x60 is milliseconds",
        ],
        "evidence": [
            evidence(FORM_C, "form_GameForm__AddMessage"),
            evidence(DUMP_CS, "internal static string[] MessageText"),
            evidence(DUMP_CS, "internal static int[] MessageMaxTime"),
        ],
        "status": "bounded_message_storage_and_partial_graph_render_ready_ttl_labels_audio_open",
    }
    fixture = {
        "schema_version": "wave4-notification-fixture-v1",
        "phase": "Phase4",
        "wave": "Wave4",
        "stage": "W4-C6-message-notification-fixture",
        "source_roots_read_only": True,
        "fixture_scope": "bounded queue fixture; time unit remains unknown",
        "source_contract": "Phases/Phase4/artifacts/wave4_notification_contract.json",
        "cases": [
            {
                "id": "default_graph",
                "input": {"text": "fixture.message", "graph_id": -1, "queue": [0, 0]},
                "expected": {"slot": 0, "MessageTime": 96, "MessageMaxTime": 96, "MessageGraph": -1, "status": "queue_write_contract"},
            },
            {
                "id": "explicit_graph",
                "input": {"text": "fixture.message", "graph_id": 2, "queue": [1, 0]},
                "expected": {"slot": 1, "MessageTime": 96, "MessageMaxTime": 96, "MessageGraph": 2, "graph_semantics": None},
            },
            {
                "id": "ttl_policy",
                "input": {"raw_lifetime": 96, "clock_unit": "configured_adapter_unit"},
                "expected": {"status": "adapter_policy_required", "legacy_unit": None, "legacy_equivalence": False},
            },
        ],
        "status": "ready_for_bounded_consumer_trace",
    }
    return contract, fixture


def build_actor_dialogue_fixture() -> dict[str, Any]:
    spawn = read_json(WAVE3_SPAWN)
    e2e = read_json(WAVE3_E2E)
    return {
        "schema_version": "wave4-actor-dialogue-fixture-v1",
        "phase": "Phase4",
        "wave": "Wave4",
        "stage": "W4-C5-actor-dialogue-composition",
        "source_roots_read_only": True,
        "fixture_scope": "single actor dialogue-to-bubble adapter boundary; not legacy runtime equivalence",
        "inputs": {
            "spawn_fixture": rel(WAVE3_SPAWN),
            "wave3_e2e_fixture": rel(WAVE3_E2E),
            "talk_fixture": "Phases/Phase4/artifacts/wave4_talk_fixture.json",
            "bubble_fixture": "Phases/Phase4/artifacts/wave4_bubble_fixture.json",
        },
        "actor": {
            "actor_id": "adapter.actor.0",
            "employee_id": spawn["input"]["employee_record"]["employee_id"],
            "identity_policy": "Wave3 stable web adapter ID",
        },
        "trace": [
            {"tick": 0, "event": "spawn", "actor_id": "adapter.actor.0", "provenance": rel(WAVE3_SPAWN)},
            {"tick": 0, "event": "dialogue_request", "talk_tag": "fixture.tag", "raw_speaker_id": 2, "status": "adapter_input"},
            {"tick": 0, "event": "talk_lookup", "status": "contract_fixture", "provenance": "Phases/Phase4/artifacts/wave4_talk_fixture.json"},
            {"tick": 0, "event": "bubble_attach", "raw_fields": {"HumanFukiIndex": 0, "HumanFukiTime": 3}, "legacy_equivalence": False},
            {"tick": 0, "event": "bubble_draw", "status": "draw_command_ready", "legacy_equivalence": False},
            {"tick": 3, "event": "bubble_expire", "status": "adapter_expired", "legacy_timer_equivalence": False},
        ],
        "not_claimed": [
            "talking is not a recovered HumanMode semantic",
            "raw speaker IDs are not public actor IDs",
            "bubble expiry unit is not verified legacy timing",
            "DoEvent has not been translated as a whole",
        ],
        "wave3_e2e_status": e2e["status"],
        "legacy_equivalence": False,
        "status": "adapter_dialogue_trace_ready_semantic_lifecycle_open",
    }


def build_gap_register() -> dict[str, Any]:
    return {
        "schema_version": "wave4-gap-register-v1",
        "phase": "Phase4",
        "wave": "Wave4",
        "stage": "W4-C0-through-C7-with-W4.5-hardening",
        "source_roots_read_only": True,
        "controlled_statuses": [
            "verified",
            "recoverable",
            "conflicting_evidence",
            "not_found_in_scoped_functions",
            "web_adapter_decision",
            "out_of_scope",
        ],
        "gaps": [
            {
                "id": "W4-GAP-001",
                "area": "locale_fallback",
                "status": "web_adapter_decision",
                "impact": "English CSV is absent and fallback locale must be configured explicitly",
                "next_action": "make Phase 3/runtime locale fallback configurable and test it",
                "evidence": [evidence(PHASE3_DOC, "GameDevStory_EN.csv")],
            },
            {
                "id": "W4-GAP-002",
                "area": "talk_token_semantics",
                "status": "recoverable",
                "impact": "split/replace/parse pipeline is verified and referenced literal table values are recorded, but pointer provenance and user-facing token meanings are not fully decoded",
                "next_action": "match StringLiteral pointer addresses against raw talk records before naming delimiters or placeholders",
                "evidence": [evidence(MAIN_C, "kairo_unity_util_StringUtil__Split")],
            },
            {
                "id": "W4-GAP-003",
                "area": "speaker_binding",
                "status": "not_found_in_scoped_functions",
                "impact": "raw speaker/chara IDs are parsed and passed through GetHumanTalkName, but no direct AddKaiwaTalkData caller to Wave 3 actor reference was found in scoped C/assembly",
                "next_action": "keep raw speaker-to-actor mapping as an explicit adapter boundary; reopen only when a producer caller is in scope",
                "evidence": [evidence(FORM_C, "form_GameForm__GetHumanTalkName")],
            },
            {
                "id": "W4-GAP-004",
                "area": "bubble_expiry",
                "status": "recoverable",
                "impact": "MainProcess decrements HumanFukiTime and DrawObj gates on a positive value; update repeat counts support a logical-tick candidate, but timer unit and zero-time HumanFukiIndex cleanup remain open",
                "next_action": "use adapter logical ticks and explicit expired-state cleanup; reopen only if legacy timing fidelity is required",
                "evidence": [evidence(FORM_C, "form_GameForm__CallFuki")],
            },
            {
                "id": "W4-GAP-005",
                "area": "DoEvent_dialogue_lifecycle",
                "status": "recoverable",
                "impact": "DoEvent is assembly-only and has a large unresolved branch space",
                "next_action": "use W4.5 target clusters as the Phase 5 map and reopen only when a concrete event-mode semantic is required",
                "evidence": [evidence(DO_EVENT_ASM, "00f5c704", "verified_assembly_entry")],
            },
            {
                "id": "W4-GAP-006",
                "area": "semantic_talking_state",
                "status": "not_found_in_scoped_functions",
                "impact": "Wave 3 mode 8/9 remains probable only; Wave 4 must not promote talking semantics",
                "next_action": "reopen only with actor state-to-dialogue timing/consumer evidence",
                "evidence": [evidence(FORM_C, "form_GameForm__AddKaiwa")],
            },
            {
                "id": "W4-GAP-007",
                "area": "message_graph_and_ttl",
                "status": "recoverable",
                "impact": "AddMessage writes, MainProcess decrement/compaction, and MessageGraph render behavior for IDs 1/2 are verified, but timer unit, graph labels, and audio policy are not closed",
                "next_action": "keep raw graph IDs with the verified render adapter; classify labels/audio only when a concrete notification UI dependency requires it",
                "evidence": [evidence(FORM_C, "form_GameForm__AddMessage")],
            },
        ],
        "summary": {
            "gap_count": 7,
            "unclassified_unknown_count": 0,
            "legacy_equivalence": False,
            "status": "controlled_open_gaps_ready_for_phase5_targeted_traces",
        },
    }


def build_manifest(paths: list[Path], outputs: list[Path], status: str) -> dict[str, Any]:
    return {
        "schema_version": "wave4-build-manifest-v1",
        "phase": "Phase4",
        "wave": "Wave4",
        "stage": "W4-C0-through-C6-dialogue-lifecycle-contracts_with_C7_separate_closure_manifest",
        "source_roots_read_only": True,
        "source_hashes": {rel(path): {"sha256": sha256(path), "bytes": path.stat().st_size} for path in paths},
        "artifact_inputs": [rel(path) for path in paths],
        "artifact_outputs": [rel(path) for path in outputs],
        "packages": {
            "W4-C0": "baseline_manifest_and_gap_register",
            "W4-C1": "locale_contract_and_fixture",
            "W4-C2": "talk_contract_and_fixture",
            "W4-C3": "bubble_contract_and_fixture",
            "W4-C4": "event_producer_contract_and_fixture",
            "W4-C5": "actor_dialogue_composition_fixture",
            "W4-C6": "message_notification_bridge_contract_ready_consumer_slice_open",
            "W4-C7": "bounded_consumer_slices_and_separate_closure_manifest",
        },
        "status": "W4-C0-C6-contracts_built_with_C7_closure_separate_manifest",
        "legacy_equivalence": False,
    }


def markdown_slices() -> dict[Path, str]:
    return {
        DOCS / "wave4_plan.md": """# Phase 4 Wave 4 — Dialogue, text, bubble และ lifecycle bridge

อัปเดต: 2026-08-11

สถานะ: **W4-C0 ถึง W4-C7 ปิดรอบแบบ `complete_with_known_limitations`**

Wave 4 ใช้ Wave 3 actor handoff เป็น input และคง `legacy_equivalence=false` สำหรับ
ทุก adapter fixture. ไม่แปล `DoEvent` หรือ `MainProcess` ทั้งฟังก์ชัน และไม่ตั้งชื่อ
raw event/mode/speaker จากการเดา.

## Packages

- W4-C0: baseline/hash/gap register
- W4-C1: CSV locale contract และ fallback/token fixture
- W4-C2: talk index, talk text, speaker และ `KaiwaLine` contract
- W4-C3: `Fuki*`, `HumanFuki*`, `DrawFukidashi` contract
- W4-C4: `AddEvent` producer และ bounded `DoEvent` consumer boundary
- W4-C5: actor → talk → bubble deterministic adapter trace
- W4-C6: `AddMessage` notification bridge — bounded producer/consumer/compaction slice
- W4-C7: closure/handoff — bounded consumer slices, manifest และ Phase 5 handoff เสร็จ
- W4.5: evidence hardening — logical timer candidate, HumanFuki cleanup boundary,
  talk/speaker pipeline, MessageGraph render behavior และ DoEvent target clusters

## Source policy

CSV, `dump.cs`, categorized C, assembly fallback และ Wave 3 artifacts เป็น read-only
source-of-truth. Generated output อยู่ใต้ `Phases/Phase4/`.

## Closure evidence

ดู `artifacts/wave4_lifecycle_slices.json` และ `docs/wave4_closure_report.md` สำหรับ
MainProcess/DrawObj consumer ranges, DoEvent target map และ notification compaction.

## Open gaps

ดู `artifacts/wave4_gap_register.json`; ข้อสำคัญคือ English fallback, talk token
semantics, raw speaker-to-actor binding, bubble timer cleanup, `DoEvent` branch semantics,
talking state และ message graph/audio labels.
""",
        SLICES / "language_lookup_01.md": """# W4-C1 — Language lookup slice

หลักฐานหลัก: `Phases/Phase3/docs/kairosoft_language_system.md`, language CSV 12 ไฟล์,
`Language.SetTextTable`, `MakeTextTable`, `TranslateText`, `_translateText2`.

สิ่งที่ยืนยันใน bounded scope:

- CSV มี metadata และ language IDs เดิม
- current extraction ไม่มี English CSV
- runtime มี text-table setup, translation และ cache boundary
- placeholder ต้องถูกเก็บเป็น token และตรวจ argument ก่อนแทนค่า

สิ่งที่ยังไม่ปิด: ความหมาย token เฉพาะเกม, fallback แบบ legacy และการเลือกข้อความ
สำหรับ dashboard ทั้งหมด.
""",
        SLICES / "talk_data_01.md": """# W4-C2 — Talk data slice

เส้นทางที่ตรวจ: `GetTalkIndex → GetTalkTexts → AddKaiwaTalkData → GetHumanTalkName
→ AddKaiwa`.

`GetTalkIndex` มี bounded scan/split/compare และคืน `-1` เมื่อไม่พบ tag.
`AddKaiwaTalkData` parse raw speaker/chara value แล้วส่งต่อชื่อและข้อความให้
`AddKaiwa`. ชื่อ special speaker IDs ยังไม่ promote เป็น semantic label.

Fixture ใช้ `fixture.tag` เป็น neutral record และไม่อ้างว่าเป็น production talk tag.
""",
        SLICES / "bubble_lifecycle_01.md": """# W4-C3 — Fukidashi bubble slice

`AddFuki` ยืนยันการเขียน `FukiCX/FukiCY/FukiWX` และเพิ่ม `FukiMax`.
`CallFuki` ยืนยัน bounded writes ไปยัง `HumanFukiIndex/HumanFukiTime` หลัง limit
checks. `DrawFukidashi` อ่าน `fukiList`, เรียก `Language.LT`, trim และส่งเข้า
`Balloon.Draw`.

Timer unit และ expiry consumer ยังต้อง trace ใน `MainProcess/DrawObj`; fixture จึงใช้
deterministic adapter clock และติดป้าย non-legacy.
""",
        SLICES / "event_dispatch_01.md": """# W4-C4 — Event dispatch slice

`AddEvent` scan first-free slot แล้วเขียน `EventMode/EventTemp/EventTemp2`.
Callsite inventory เก็บ raw mode expressions และไม่ตั้งชื่อ semantic event.

`DoEvent` ยังเป็น assembly fallback ขนาดใหญ่; งานถัดไปคือ slice เฉพาะ branch ที่แตะ
`AddKaiwa`, `AddMessage`, `CallFuki` หรือ actor lifecycle.
""",
        SLICES / "message_bridge_01.md": """# W4-C6 — Message bridge slice

`AddMessage` scan `MessageTime` หา slot ว่าง แล้วเขียน `MessageText`, ตั้ง
`MessageTime`/`MessageMaxTime` เป็น raw value `0x60` และเขียน `MessageGraph`.

ค่า `0x60` ยังไม่ถูกตีความเป็น milliseconds และ `MessageGraph` ยังเป็น raw ID.
Notification ที่ map เข้ากับ dashboard ต้องใช้ adapter contract จนกว่าจะ trace
consumer และ lifecycle event ที่แน่นอนได้.
""",
    }


def build_all() -> dict[Path, Any]:
    missing = [rel(path) for path in required_paths() if not path.is_file()]
    if missing:
        raise RuntimeError("missing Wave 4 inputs: " + ", ".join(missing))
    locales = [parse_locale(path) for path in sorted(LOCALE_DIR.glob("GameDevStory_*.csv"))]
    locale_contract, locale_fixture = build_locale_contract(locales)
    talk_contract, talk_fixture = build_talk_contract()
    bubble_contract, bubble_fixture = build_bubble_contract()
    event_contract, event_fixture = build_event_contract()
    notification_contract, notification_fixture = build_notification_contract()
    actor_fixture = build_actor_dialogue_fixture()
    gap_register = build_gap_register()
    paths = required_paths()
    outputs = [path for path in OUTPUTS if path.suffix == ".json"]
    manifest = build_manifest(paths, OUTPUTS, "W4-C0-C6-contracts-built_with_C7_open")
    result: dict[Path, Any] = {
        ARTIFACTS / "wave4_build_manifest.json": manifest,
        ARTIFACTS / "wave4_gap_register.json": gap_register,
        ARTIFACTS / "wave4_locale_contract.json": locale_contract,
        ARTIFACTS / "wave4_locale_fixture.json": locale_fixture,
        ARTIFACTS / "wave4_talk_contract.json": talk_contract,
        ARTIFACTS / "wave4_talk_fixture.json": talk_fixture,
        ARTIFACTS / "wave4_bubble_contract.json": bubble_contract,
        ARTIFACTS / "wave4_bubble_fixture.json": bubble_fixture,
        ARTIFACTS / "wave4_event_contract.json": event_contract,
        ARTIFACTS / "wave4_event_fixture.json": event_fixture,
        ARTIFACTS / "wave4_notification_contract.json": notification_contract,
        ARTIFACTS / "wave4_notification_fixture.json": notification_fixture,
        ARTIFACTS / "wave4_actor_dialogue_fixture.json": actor_fixture,
    }
    result.update(markdown_slices())
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="build in memory and compare generated outputs")
    args = parser.parse_args()
    outputs = build_all()
    if args.check:
        mismatches = []
        for path, expected in outputs.items():
            if path.suffix == ".json":
                actual = json.loads(path.read_text(encoding="utf-8")) if path.is_file() else None
            else:
                actual = path.read_text(encoding="utf-8") if path.is_file() else None
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
