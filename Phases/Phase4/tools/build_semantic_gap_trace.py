#!/usr/bin/env python3
"""Build the next bounded Phase 4 evidence slice.

The two remaining Wave 0 assembly-only functions are indexed here only at
the branch/call/field boundary that can be supported by the recovered
assembly.  The TFace section joins that trace to the existing DrawHuman
inventory and records where the literal selectors occur.  It deliberately
does not promote numeric modes, asset namespaces, or actor semantics.
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
DUMP_CS = ROOT / "game-dev-story-mod_Dumped" / "dump.cs"
NEWGAME_ASM = ROOT / "game-dev-story-mod_Dumped" / "Failed_Functions_Assembly" / "00f265b8_form_GameForm__NewGamePara.asm.txt"
DOEVENT_ASM = ROOT / "game-dev-story-mod_Dumped" / "Failed_Functions_Assembly" / "00f5c704_form_GameForm__DoEvent.asm.txt"
TARGETED_SCAN = ARTIFACTS / "targeted_gap_scan.json"
ANIMATION_CONTRACT = ARTIFACTS / "wave3_actor_animation_contract.json"
EVENT_MODES = ARTIFACTS / "wave4_event_mode_candidates.json"
BRANCH_INDEX = ARTIFACTS / "wave1_branch_index.json"
OUTPUT = ARTIFACTS / "semantic_gap_trace.json"

BRANCH_MNEMONICS = {
    "b", "b.eq", "b.ne", "b.cs", "b.cc", "b.mi", "b.pl", "b.vs", "b.vc",
    "b.hi", "b.ls", "b.ge", "b.lt", "b.gt", "b.le", "cbz", "cbnz", "tbz", "tbnz", "ret",
}
HEX_RE = re.compile(r"0x[0-9a-fA-F]+")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def compact(text: str, limit: int = 280) -> str:
    value = " ".join(text.strip().split())
    return value if len(value) <= limit else value[: limit - 3] + "..."


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_assembly(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_number, raw in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        if ";" not in raw:
            continue
        left, operands = raw.split(";", 1)
        tokens = left.split()
        if len(tokens) < 2 or not re.fullmatch(r"[0-9a-fA-F]+", tokens[0]):
            continue
        mnemonic = tokens[-1].lower()
        rows.append(
            {
                "address": f"0x{int(tokens[0], 16):08x}",
                "line": line_number,
                "mnemonic": mnemonic,
                "operands": compact(operands),
                "raw": compact(raw),
            }
        )
    return rows


def target(row: dict[str, Any]) -> str | None:
    match = HEX_RE.search(row["operands"])
    return f"0x{int(match.group(0), 16):08x}" if match else None


def calls(rows: list[dict[str, Any]], destination: str) -> list[dict[str, Any]]:
    expected = destination.lower()
    return [row for row in rows if row["mnemonic"] == "bl" and target(row) == expected]


def instruction(rows: list[dict[str, Any]], address: str) -> dict[str, Any]:
    expected = address.lower()
    for row in rows:
        if row["address"] == expected:
            return dict(row)
    raise ValueError(f"assembly instruction not found: {address}")


def evidence(rows: list[dict[str, Any]], address: str, *, expected_target: str | None = None) -> dict[str, Any]:
    row = instruction(rows, address)
    result = {
        "address": row["address"],
        "line": row["line"],
        "mnemonic": row["mnemonic"],
        "operands": row["operands"],
        "raw": row["raw"],
    }
    if expected_target is not None:
        actual = target(row)
        if actual != expected_target.lower():
            raise ValueError(f"unexpected target at {address}: {actual} != {expected_target}")
        result["target"] = actual
    return result


def structural(rows: list[dict[str, Any]], branch_index: dict[str, Any], symbol: str) -> dict[str, Any]:
    indexed = branch_index["functions"][symbol]
    branch_count = sum(row["mnemonic"] == "bl" or row["mnemonic"] in BRANCH_MNEMONICS for row in rows)
    if len(rows) != indexed["instruction_count"] or branch_count != indexed["branch_count"]:
        raise ValueError(f"assembly parser drift for {symbol}")
    return {
        "file": rel(Path(indexed["file"] if Path(indexed["file"]).is_absolute() else ROOT / indexed["file"])),
        "entry": indexed["entry"],
        "end": indexed["end"],
        "instruction_count": len(rows),
        "branch_count": branch_count,
        "basic_block_count": indexed["basic_block_count"],
        "parser_status": "verified_against_wave1_branch_index",
    }


def offset_refs(rows: list[dict[str, Any]], offsets: dict[str, str]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for field, offset in offsets.items():
        needle = offset.lower()
        result[field] = {
            "offset": offset,
            "reference_count": sum(f"#{needle}" in row["raw"].lower() for row in rows),
            "status": "verified_named_field",
        }
    return result


def object_setup(rows: list[dict[str, Any]]) -> dict[str, Any]:
    add_calls = calls(rows, "0x00f33b54")
    writebacks = []
    for call in add_calls:
        index = next(index for index, row in enumerate(rows) if row["address"] == call["address"])
        nearby = rows[index : index + 14]
        writebacks.append(
            {
                "call_address": call["address"],
                "returned_w0_writeback": any(
                    row["mnemonic"] == "str" and row["operands"].startswith("w0,") for row in nearby[1:]
                ),
            }
        )
    offsets = {
        "DeskObjec": "0x458",
        "ChairMainObjec": "0x460",
        "ChairSubObjec": "0x468",
        "PCObjec": "0x470",
        "ObjecPoint": "0x308",
        "ObjecIndex": "0x290",
    }
    return {
        "call_target": "0x00f33b54",
        "call_count": len(add_calls),
        "first_call": add_calls[0]["address"],
        "last_call": add_calls[-1]["address"],
        "array_field_refs": offset_refs(rows, offsets),
        "returned_w0_writeback_count": sum(row["returned_w0_writeback"] for row in writebacks),
        "returned_w0_writeback_all_calls": all(row["returned_w0_writeback"] for row in writebacks),
        "sample_calls": [
            {"address": row["address"], "line": row["line"], "raw": row["raw"]}
            for row in (add_calls[:2] + add_calls[-2:])
        ],
        "status": "verified_bounded_repeated_object_setup",
    }


def newgame_trace(rows: list[dict[str, Any]], branch_index: dict[str, Any]) -> dict[str, Any]:
    calls_by_target = Counter(target(row) for row in rows if row["mnemonic"] == "bl")
    terminal = [
        evidence(rows, "0x00f33b4c", expected_target="0x00db0dec"),
        evidence(rows, "0x00f33b50", expected_target="0x00db0de4"),
    ]
    return {
        "source_status": "assembly_fallback_only",
        "structural": structural(rows, branch_index, "form_GameForm__NewGamePara"),
        "clusters": [
            {
                "cluster_id": "NGP-INIT-GUARD",
                "classification": "static_initialization_guard",
                "evidence": [evidence(rows, "0x00f265e8")],
                "observations": [
                    "entry guard branches to 0x00f27e24 when the static guard is set",
                    "the following region contains repeated helper initialization calls",
                ],
                "status": "verified_structural_only",
                "not_claimed": ["full initialization semantics", "meaning of unresolved helper 0x00db0cc0"],
            },
            {
                "cluster_id": "NGP-OBJECT-CONSTRUCTION",
                "classification": "repeated_AddObjec_setup",
                "object_setup": object_setup(rows),
                "status": "verified_bounded",
                "not_claimed": ["universal placement semantics", "complete NewGamePara lifecycle"],
            },
            {
                "cluster_id": "NGP-HELPER-HEAVY",
                "classification": "unresolved_helper_cluster",
                "call_target": "0x00db0cc0",
                "call_count": calls_by_target["0x00db0cc0"],
                "status": "unresolved_helper",
                "not_claimed": ["helper meaning"],
            },
            {
                "cluster_id": "NGP-TERMINAL-BOUNDARY",
                "classification": "terminal_guard_or_exception_epilogue",
                "evidence": terminal,
                "status": "verified_terminal_boundary_only",
                "not_claimed": ["cleanup semantics"],
            },
        ],
        "conclusions": [
            "NewGamePara has a repeated AddObjec setup region with nearby object-array bounds/write-back evidence",
            "the static guard and terminal helper targets are bounded, but their higher-level meaning remains open",
            "no full initialization/reset lifecycle is promoted from assembly structure alone",
        ],
    }


def producer_call(rows: list[dict[str, Any]], address: str, destination: str, symbol: str) -> dict[str, Any]:
    row = evidence(rows, address, expected_target=destination)
    row["symbol"] = symbol
    return row


def doevent_trace(rows: list[dict[str, Any]], branch_index: dict[str, Any], event_modes: dict[str, Any]) -> dict[str, Any]:
    fields = offset_refs(
        rows,
        {
            "KikakuMode": "0x870",
            "KikakuZyuchu": "0x878",
            "KikakuPara": "0x8a8",
            "AnkenName": "0x910",
            "EventMode": "0xff8",
            "EventTemp": "0x1000",
            "EventTemp2": "0x1008",
            "KaiwaNextAction": "0x260",
        },
    )
    mode_clusters = [
        {
            "cluster_id": "DE-KIKAKU-5-DIALOGUE",
            "classification": "KikakuMode_value_branch_to_dialogue",
            "comparison_value": 5,
            "comparison": evidence(rows, "0x00f5d418"),
            "branch": evidence(rows, "0x00f5d41c", expected_target="0x00f5d4d4"),
            "producer_calls": [
                producer_call(rows, "0x00f5d448", "0x00f83b80", "MyFormBase.LT"),
                producer_call(rows, "0x00f5d4b0", "0x018ecc5c", "StringUtil.Replace"),
                producer_call(rows, "0x00f5d4c0", "0x00f1a908", "form_GameForm__AddKaiwa"),
            ],
        },
        {
            "cluster_id": "DE-KIKAKU-7-DIALOGUE",
            "classification": "KikakuMode_value_branch_to_dialogue",
            "comparison_value": 7,
            "comparison": evidence(rows, "0x00f5d4f0"),
            "branch": evidence(rows, "0x00f5d4f4", expected_target="0x00f5d558"),
            "producer_calls": [
                producer_call(rows, "0x00f5d520", "0x00f83b80", "MyFormBase.LT"),
                producer_call(rows, "0x00f5d530", "0x00f1a908", "form_GameForm__AddKaiwa"),
            ],
        },
        {
            "cluster_id": "DE-KIKAKU-8-DIALOGUE",
            "classification": "KikakuMode_value_branch_to_dialogue",
            "comparison_value": 8,
            "comparison": evidence(rows, "0x00f5d574"),
            "branch": evidence(rows, "0x00f5d578", expected_target="0x00f5f124"),
            "producer_calls": [
                producer_call(rows, "0x00f5d5a4", "0x00f83b80", "MyFormBase.LT"),
                producer_call(rows, "0x00f5d5b4", "0x00f1a908", "form_GameForm__AddKaiwa"),
            ],
            "next_action_write": [
                evidence(rows, "0x00f5d5d4"),
                evidence(rows, "0x00f5d5d8"),
            ],
        },
        {
            "cluster_id": "DE-EVENTMODE-2",
            "classification": "EventMode_indexed_dispatch",
            "eventmode_load": evidence(rows, "0x00f5d5f4"),
            "comparison_value": 2,
            "comparison": evidence(rows, "0x00f5d614"),
            "branch": evidence(rows, "0x00f5d618", expected_target="0x00f5f1fc"),
            "status": "verified_dispatch_boundary",
            "semantic_mode_name": None,
        },
    ]
    target_inventory = {}
    for address, value in event_modes["consumer"]["target_clusters"].items():
        target_inventory[address] = {
            "symbol": value["symbol"],
            "role": value["role"],
            "count": value["count"],
            "status": value["status"],
        }
    return {
        "source_status": "assembly_fallback_only",
        "structural": structural(rows, branch_index, "form_GameForm__DoEvent"),
        "field_boundaries": fields,
        "clusters": mode_clusters,
        "target_inventory": target_inventory,
        "terminal_boundary": {
            "classification": "terminal_guard_or_exception_boundary",
            "evidence": [
                evidence(rows, "0x00f6ba04", expected_target="0x00db0dec"),
                evidence(rows, "0x00f6ba08", expected_target="0x00db0de4"),
            ],
            "status": "verified_boundary_only",
        },
        "conclusions": [
            "KikakuMode values 5, 7, and 8 reach bounded LT/Replace/AddKaiwa clusters",
            "EventMode indexed dispatch and comparison value 2 are verified, but the numeric event meaning is unnamed",
            "the full DoEvent state machine and lifecycle semantics remain open",
        ],
    }


def tface_trace(targeted: dict[str, Any], animation: dict[str, Any]) -> dict[str, Any]:
    scan = targeted["tface_scan"]
    literal_calls = scan["literal_tface_40_calls"] + scan["literal_tface_41_calls"]
    literal_calls.sort(key=lambda row: row["source_line"])
    actor_callers = {
        "form_GameForm__AddSyain",
        "form_GameForm__CallSyain",
        "form_GameForm__LoadGameData",
        "form_GameForm__SaveGameData",
        "form_GameForm__MainProcess",
        "form_GameForm__DrawObj",
    }
    actor_scope_hits = [row for row in literal_calls if row["caller"] in actor_callers]
    selector_namespaces = [
        {
            "selector": "HumanFaceG",
            "offset": "0xf30",
            "producer_or_consumer_functions": ["form_GameForm__CallSyain", "form_GameForm__MainProcess", "form_GameForm__DrawObj"],
            "evidence_lines": [16316, 27594, 27604, 7764],
            "status": "dynamic_field_flow_no_literal_40_41_producer",
        },
        {
            "selector": "HumanBodyG",
            "offset": "0xf38",
            "producer_or_consumer_functions": ["form_GameForm__CallSyain", "form_GameForm__MainProcess", "form_GameForm__DrawObj"],
            "evidence_lines": [16319, 27602, 7777],
            "status": "dynamic_field_flow_no_literal_40_41_producer",
        },
        {
            "selector": "HumanDexFaceG",
            "offset": "0x3f8",
            "producer_or_consumer_functions": ["form_GameForm___draw"],
            "evidence_lines": [19676, 19687],
            "status": "preview_dynamic_selector_flow_not_office_actor_producer",
        },
        {
            "selector": "SyainFaceG",
            "offset": "0x5b8",
            "producer_or_consumer_functions": ["form_GameForm__AddSyain", "form_GameForm__CallSyain", "form_GameForm__LoadGameData", "form_GameForm__SaveGameData"],
            "evidence_lines": [27061, 27591, 35399, 39888],
            "status": "stored_dynamic_face_source_no_literal_40_41_producer",
        },
    ]
    source_rows = []
    for row in literal_calls:
        source_rows.append(
            {
                "source_line": row["source_line"],
                "caller": row["caller"],
                "tface": 40 if row["tface_expression"] == "0x28" else 41,
                "raw_call": row["raw_call"],
                "classification": "literal_direct_non_actor_dynamic_callsite",
            }
        )
    return {
        "literal_hits": source_rows,
        "classification_counts": {
            "literal_direct_non_actor_dynamic_callsite": len(literal_calls),
            "actor_dynamic_or_unknown_literal_producer": len(actor_scope_hits),
        },
        "direct_literal_producer_search": {
            "actor_producer_scope_callers": sorted(actor_callers),
            "literal_40_or_41_hits_in_scoped_actor_producers": len(actor_scope_hits),
            "status": "not_found_in_scoped_actor_producers" if not actor_scope_hits else "found_and_requires_followup",
        },
        "selector_namespaces": selector_namespaces,
        "existing_selector_policy": [
            namespace for namespace in animation["selector_namespaces"]
            if namespace["namespace"] in {"legacy_draw_selector", "actor_selector_source", "raw_actor_state"}
        ],
        "conclusion": "TFace 40/41 hits are fixed literal DrawHuman callsites in screen/panel/preview code; actor draw paths remain field/array driven, with no direct 40/41 producer found in the scoped actor functions. The asset/index-space gap remains unresolved.",
    }


def build() -> dict[str, Any]:
    newgame_rows = parse_assembly(NEWGAME_ASM)
    doevent_rows = parse_assembly(DOEVENT_ASM)
    branch_index = read_json(BRANCH_INDEX)
    targeted = read_json(TARGETED_SCAN)
    animation = read_json(ANIMATION_CONTRACT)
    event_modes = read_json(EVENT_MODES)
    source_paths = [FORM_C, DUMP_CS, NEWGAME_ASM, DOEVENT_ASM, TARGETED_SCAN, ANIMATION_CONTRACT, EVENT_MODES, BRANCH_INDEX]
    return {
        "schema_version": "phase4-semantic-gap-trace-v1",
        "phase": "Phase4",
        "waves": ["Wave0", "Wave1", "Wave3", "Wave4"],
        "source_roots_read_only": True,
        "legacy_equivalence": False,
        "status": "bounded_branch_and_selector_trace_open",
        "source_hashes": {
            rel(path): {"sha256": sha256(path), "bytes": path.stat().st_size}
            for path in source_paths
        },
        "newgamepara": newgame_trace(newgame_rows, branch_index),
        "doevent": doevent_trace(doevent_rows, branch_index, event_modes),
        "tface_producer_trace": tface_trace(targeted, animation),
        "next_recoverable_slices": [
            "trace AddObjec parameter constants to each object family without promoting world/depth semantics",
            "trace DoEvent field writes around the bounded mode clusters before naming any numeric mode",
            "find an extracted asset/index namespace or preserve TFace 40/41 as unresolved",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="rebuild in memory and compare with the committed artifact")
    args = parser.parse_args()
    value = build()
    rendered = json.dumps(value, ensure_ascii=False, indent=2) + "\n"
    if args.check:
        current = OUTPUT.read_text(encoding="utf-8")
        if current != rendered:
            print(f"artifact drift: {OUTPUT}")
            return 1
        print("semantic gap trace: OK")
        return 0
    OUTPUT.write_text(rendered, encoding="utf-8")
    print(f"wrote {OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
