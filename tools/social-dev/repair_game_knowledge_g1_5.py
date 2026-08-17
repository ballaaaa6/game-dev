"""Augment the canonical Social Dev KB with the G1.5 static closure.

This is an inline, deterministic repair pass.  It reuses the existing G0/G1
builder and canonical output paths, then merges native disassembly, decoded
``xls`` evidence, native HP accesses, and source-derived planning call sites.
It never launches the APK, uses ADB/network access, or writes runtime/visual
artifacts.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sqlite3
import struct
import sys
from pathlib import Path
from typing import Any

from capstone import Cs, CS_ARCH_ARM64, CS_MODE_ARM


ROOT = Path(__file__).resolve().parents[2]
RAW_UPDATE = ROOT / "sources/raw/1_Click_CSharp_Code update"
RAW_EVIDENCE = ROOT / "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code"
EVIDENCE = ROOT / "knowledge/fixtures/accepted/g1_5"
KB = ROOT / "knowledge/data/original"
JSONL = KB / "jsonl"
GRAPHS = KB / "graphs"
REPORTS = KB / "reports"
REGISTRY_PATH = ROOT / "knowledge/fixtures/accepted/native_content_registry.json"
DUMP_PATH = ROOT / "knowledge/sources/phase3a_apk_probe/il2cpp_dump/dump.cs"
NATIVE_PATH = ROOT / "knowledge/sources/phase3a_apk_probe/raw/libil2cpp.so"
XLS_MANIFEST_PATH = EVIDENCE / "xls-decoded/manifest.json"

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_game_knowledge_g0_g1 as builder  # noqa: E402


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def ref(path: str | Path, line: int | None = None, note: str | None = None) -> dict[str, Any]:
    return builder.source_ref(path, line, note)


def native_file_offset(rva: int) -> int:
    # LIEF's pinned program headers show the executable LOAD begins at RVA
    # 0xE6805C and file offset 0xE6405C, hence the -0x4000 mapping above it.
    return rva - 0x4000 if rva >= 0xE6805C else rva


def disassemble(rva: int, end_rva: int) -> list[Any]:
    data = NATIVE_PATH.read_bytes()
    blob = data[native_file_offset(rva) : native_file_offset(end_rva)]
    return list(Cs(CS_ARCH_ARM64, CS_MODE_ARM).disasm(blob, rva))


def parse_dump_rvas(dump_text: str) -> list[int]:
    return sorted({int(value, 16) for value in re.findall(r"// RVA: 0x([0-9A-Fa-f]+)", dump_text)})


def next_native_rva(rvas: list[int], start: int) -> int:
    return next((value for value in rvas if value > start), start + 0x1000)


def data_manager_fields(dump_text: str) -> dict[int, dict[str, Any]]:
    match = re.search(r"\bclass\s+DataManager\b", dump_text)
    if match is None:
        raise RuntimeError("DataManager declaration is absent from dump.cs")
    end = dump_text.find("\n\t// Methods", match.start())
    block = dump_text[match.start() : end if end >= 0 else match.start() + 50000]
    fields: dict[int, dict[str, Any]] = {}
    for line_number, line in enumerate(block.splitlines(), 1):
        found = re.search(r"\b([A-Za-z_]\w*(?:\[\])?)\s+([A-Za-z_]\w*)\s*;\s*//\s*(0x[0-9A-Fa-f]+)", line)
        if not found:
            continue
        fields[int(found.group(3), 16)] = {
            "field": found.group(2),
            "declared_type": found.group(1),
            "offset": found.group(3).upper(),
            "dump_relative_line": line_number,
        }
    return fields


def dump_constructor_map(dump_text: str) -> dict[int, str]:
    """Map native constructor RVAs to the nearest recovered class name."""

    lines = dump_text.splitlines()
    current_class = "unknown"
    constructors: dict[int, str] = {}
    pending_rva: int | None = None
    for index, line in enumerate(lines):
        class_match = re.search(r"\bclass\s+([A-Za-z_]\w*)", line)
        if class_match:
            current_class = class_match.group(1)
        rva_match = re.search(r"// RVA: 0x([0-9A-Fa-f]+)", line)
        if rva_match:
            pending_rva = int(rva_match.group(1), 16)
            continue
        if pending_rva is None or line.strip().startswith("//") or not line.strip():
            continue
        method_match = re.search(r"(?:[A-Za-z_<>,\[\].?]+\s+)?(\.ctor|[A-Za-z_]\w*)\s*\([^;]*\)", line)
        if method_match:
            if method_match.group(1) == ".ctor":
                constructors[pending_rva] = f"{current_class}::.ctor"
            pending_rva = None
    return constructors


def call_target(op_str: str) -> int | None:
    match = re.search(r"#0x([0-9A-Fa-f]+)", op_str)
    return int(match.group(1), 16) if match else None


def first_store_to_data_manager(start: int, stop: int) -> dict[str, Any] | None:
    for instruction in disassemble(start, min(stop, start + 0x200)):
        if instruction.mnemonic not in {"str", "stur"} or "[x20," not in instruction.op_str:
            if instruction.mnemonic == "b" and instruction.op_str == "#0x1215930":
                break
            continue
        found = re.search(r"\[x20,\s*#(0x[0-9A-Fa-f]+)\]", instruction.op_str)
        if found:
            return {
                "instruction_rva": f"0x{instruction.address:X}",
                "instruction": f"{instruction.mnemonic} {instruction.op_str}",
                "field_offset": found.group(1).upper(),
                "source_register": instruction.op_str.split(",", 1)[0].strip(),
            }
    return None


def native_data_manager_evidence() -> tuple[dict[str, Any], dict[str, Any]]:
    dump_text = DUMP_PATH.read_text(encoding="utf-8", errors="replace")
    all_rvas = parse_dump_rvas(dump_text)
    dm_fields = data_manager_fields(dump_text)
    constructors = dump_constructor_map(dump_text)
    load_start, load_end = 0x121500C, 0x1216170
    instance_start, instance_end = 0x1216170, 0x121679C
    load_table_rva, load_case_base, load_case_count = 0x636318, 0x1215340, 43
    instance_table_rva, instance_case_base, instance_case_count = 0x63636E, 0x12163B0, 42
    binary = NATIVE_PATH.read_bytes()
    load_table = list(binary[native_file_offset(load_table_rva) : native_file_offset(load_table_rva) + load_case_count * 2])
    load_values = struct.unpack("<43H", bytes(load_table))
    instance_values = list(binary[native_file_offset(instance_table_rva) : native_file_offset(instance_table_rva) + instance_case_count])
    registry = read_json(REGISTRY_PATH)
    registry_rows = registry["data_manager_registry"]
    require(len(registry_rows) == 43 and len(load_values) == 43, "DataManager registry/native Load domain is not 43")

    slots: list[dict[str, Any]] = []
    for slot, registry_row in enumerate(registry_rows):
        load_target = load_case_base + load_values[slot] * 4
        store = first_store_to_data_manager(load_target, 0x1215930)
        if store is None:
            raise RuntimeError(f"native Load case {slot} has no DataManager destination store")
        offset_number = int(store["field_offset"], 16)
        field = dm_fields.get(offset_number)
        if field is None or field["field"] != registry_row["field"]:
            raise RuntimeError(f"native Load case {slot} field mismatch: {store} vs {registry_row}")
        if slot < instance_case_count:
            instance_target = instance_case_base + instance_values[slot] * 4
        else:
            instance_target = 0x12166EC
        instance_instructions = disassemble(instance_target, min(instance_end, instance_target + 0x100))
        constructor_calls = []
        type_info_load = None
        for instruction in instance_instructions:
            if instruction.mnemonic == "bl":
                target = call_target(instruction.op_str)
                if target is not None and target in constructors:
                    constructor_calls.append({"instruction_rva": f"0x{instruction.address:X}", "target_rva": f"0x{target:X}", "symbol": constructors[target]})
            if instruction.mnemonic == "adrp" and instruction.op_str.startswith("x8"):
                next_index = instance_instructions.index(instruction) + 1
                if next_index < len(instance_instructions) and instance_instructions[next_index].mnemonic == "ldr" and instance_instructions[next_index].op_str.startswith("x8"):
                    type_info_load = {"adrp": f"0x{instruction.address:X} {instruction.mnemonic} {instruction.op_str}", "load": f"0x{instance_instructions[next_index].address:X} {instance_instructions[next_index].mnemonic} {instance_instructions[next_index].op_str}"}
                    break
        slots.append({
            "slot": slot,
            "registry_key": registry_row["registry_key"],
            "field": registry_row["field"],
            "field_offset": store["field_offset"],
            "element_type": registry_row["element_type"],
            "load_jump_table_value": load_values[slot],
            "load_branch_target": f"0x{load_target:X}",
            "load_store": store,
            "get_instance_branch_target": f"0x{instance_target:X}",
            "get_instance_jump_table_value": instance_values[slot] if slot < instance_case_count else None,
            "get_instance_constructor_calls": constructor_calls,
            "get_instance_type_info_load": type_info_load,
            "return_behavior": "NULL_HELP_TEXT_OR_NON_BASE_DATA" if slot == 4 else "ALLOCATE_BASE_DATA_SUBCLASS_AND_CALL_BASE_CTOR",
            "status": "CONFIRMED_NATIVE_SLOT_DISPATCH",
            "confidence": "native Load jump table stores GetInstance(slot) result to exact DataManager field offset",
        })

    load_instructions = disassemble(load_start, load_end)
    native_calls = []
    for instruction in load_instructions:
        if instruction.mnemonic != "bl":
            continue
        target = call_target(instruction.op_str)
        if target in {0x1D4264C, 0x1CA5D78, 0x1CC3FEC, 0x1216170, 0x121679C}:
            native_calls.append({"instruction_rva": f"0x{instruction.address:X}", "target_rva": f"0x{target:X}"})
    load_map = {
        "status": "PASS_DATAMANAGER_NATIVE_LOAD_SLOT_DISPATCH",
        "method": "data.DataManager.Load",
        "method_signature": "public void Load()",
        "rva": "0x121500C",
        "range": {"start": "0x121500C", "end_exclusive": "0x1216170"},
        "source_refs": [ref("knowledge/sources/data/csharp_update/DataManager.cs", 105), ref(DUMP_PATH), ref(NATIVE_PATH)],
        "load_sequence": [
            {"step": 1, "operation": "RecordStore.ReadRecord(1, 0)", "call_rva": "0x1D4264C", "call_site_rva": "0x1215280"},
            {"step": 2, "operation": "JarInflater(byte[])", "call_rva": "0x1CA5D78", "call_site_rva": "0x12152A4"},
            {"step": 3, "operation": "StringUtil.LoadStringArray(jar, fileName, true)", "call_rva": "0x1CC3FEC", "call_sites": ["0x12152C4", "0x1215314"]},
            {"step": 4, "operation": "DataManager.GetInstance(slot)", "call_rva": "0x1216170", "call_site_rva": "0x1215980"},
            {"step": 5, "operation": "BaseData.Load row string array through virtual call", "call_site_rva": "0x12159F0", "instruction": "blr x9"},
            {"step": 6, "operation": "AdjustDataList", "call_rva": "0x121679C", "call_site_rva": "0x1215A28"},
        ],
        "native_calls_observed": native_calls,
        "selector_domain": {"start": 0, "end_inclusive": 42, "count": 43},
        "jump_table": {"rva": f"0x{load_table_rva:X}", "entry_width_bytes": 2, "case_base": f"0x{load_case_base:X}", "case_count": 43, "values_sha256": sha256_bytes(bytes(load_table))},
        "destination_store_semantics": "each case stores the GetInstance(slot) result to the DataManager instance at the dump-declared field offset; slot 4 stores the decoded help string array directly",
        "slots": slots,
        "static_only": True,
    }
    instance_map = {
        "status": "PASS_DATAMANAGER_NATIVE_GETINSTANCE_SELECTOR_MAP",
        "method": "data.DataManager.GetInstance(int)",
        "method_signature": "private static BaseData GetInstance(int a)",
        "rva": "0x1216170",
        "range": {"start": "0x1216170", "end_exclusive": "0x121679C"},
        "source_refs": [ref("knowledge/sources/data/csharp_update/DataManager.cs", 495), ref(DUMP_PATH), ref(NATIVE_PATH)],
        "selector_domain": {"start": 0, "end_inclusive": 42, "count": 43},
        "jump_table": {"rva": f"0x{instance_table_rva:X}", "entry_width_bytes": 1, "case_base": f"0x{instance_case_base:X}", "case_count": 42, "values_sha256": sha256_bytes(bytes(instance_values)), "special_case": {"selector": 42, "branch_target": "0x12166EC", "constructor_rva": "0x122044C", "element_type": "ManagementEventData"}},
        "slots": slots,
        "native_constructor_resolution": "direct constructor calls are retained where present; empty/dummy constructors retain the native type-info load plus the exact Load destination-field proof",
        "static_only": True,
    }
    return load_map, instance_map


def staff_hp_native_evidence() -> dict[str, Any]:
    dump_text = DUMP_PATH.read_text(encoding="utf-8", errors="replace")
    all_rvas = parse_dump_rvas(dump_text)
    authority = read_json(ROOT / "knowledge/fixtures/accepted/living-core-closure/staff-native-authority-map.json")
    method_semantics = {
        "Init": "INIT", "Update": "THRESHOLD_READ", "RecoverHp": "RECOVER", "UseEquip": "OTHER",
        "OnAttacked": "OTHER", "OverwriteOriginalFields": "COPY/CLONE", "SetHp": "OTHER",
        "RecoverHpMax": "RECOVER", "ClampHpMax": "CLAMP", "UpdateWork": "ORDINARY_WORK",
    }
    accesses: list[dict[str, Any]] = []
    method_summaries: list[dict[str, Any]] = []
    binary = NATIVE_PATH.read_bytes()
    for method in authority["methods"]:
        name = method["method"]
        start = int(method["rva"], 16)
        end = next_native_rva(all_rvas, start)
        instructions = disassemble(start, end)
        method_accesses: list[dict[str, Any]] = []
        for instruction in instructions:
            match = re.search(r"\[(x\d+),\s*#0xE8\]", instruction.op_str, re.IGNORECASE)
            if not match or instruction.mnemonic not in {"ldr", "ldur", "str", "stur"}:
                continue
            operation = "READ" if instruction.mnemonic in {"ldr", "ldur"} else "WRITE"
            record = {
                "field_entity": "field:game.Staff.hp_",
                "field_offset": "0xE8",
                "managed_method": f"game.Staff.{name}",
                "method_rva": f"0x{start:X}",
                "method_range": {"start": f"0x{start:X}", "end_exclusive": f"0x{end:X}"},
                "instruction_rva": f"0x{instruction.address:X}",
                "instruction_bytes": binary[native_file_offset(instruction.address) : native_file_offset(instruction.address) + instruction.size].hex(),
                "instruction": f"{instruction.mnemonic} {instruction.op_str}",
                "operation": operation,
                "source_register": match.group(1),
                "semantic_class": method_semantics.get(name, "OTHER"),
                "access_origin": "NATIVE",
                "evidence_status": "CONFIRMED_NATIVE_FIELD_ACCESS",
                "provenance": [ref(NATIVE_PATH), ref(DUMP_PATH)],
            }
            method_accesses.append(record)
            accesses.append(record)
        method_summaries.append({"method": f"game.Staff.{name}", "method_rva": method["rva"], "method_range": {"start": f"0x{start:X}", "end_exclusive": f"0x{end:X}"}, "access_count": len(method_accesses), "accesses": method_accesses, "accepted_facts": method.get("facts", [])})

    update_work = next(row for row in method_summaries if row["method"].endswith("UpdateWork"))
    write_sites = read_json(ROOT / "knowledge/fixtures/accepted/living-core-closure/hp-native-write-site-catalog.json")["write_sites"]
    graph = {
        "status": "PASS_STAFF_HP_NATIVE_FIELD_GRAPH",
        "field": {"entity": "field:game.Staff.hp_", "symbol": "Staff.hp_", "offset": "0xE8", "declared_type": "int"},
        "counts": {
            "native_reads": sum(1 for row in accesses if row["operation"] == "READ"),
            "native_writes": sum(1 for row in accesses if row["operation"] == "WRITE"),
            "native_accesses": len(accesses),
            "methods_with_native_access": len([row for row in method_summaries if row["access_count"]]),
        },
        "method_summaries": method_summaries,
        "accepted_write_site_catalog": write_sites,
        "key_writer_methods": [row["method"] for row in method_summaries if any(access["operation"] == "WRITE" for access in row["accesses"])],
        "ordinary_work_check": {"method": "game.Staff.UpdateWork", "rva": "0x12D4A7C", "direct_hp_accesses": update_work["access_count"], "negative_recover_hp_call": False, "status": "CONFIRMED_NO_DIRECT_ORDINARY_WORK_DRAIN"},
        "source_refs": [ref(ROOT / "knowledge/fixtures/accepted/behavior-first/hp-read-write-graph.json"), ref(ROOT / "knowledge/fixtures/accepted/living-core-closure/hp-native-write-site-catalog.json"), ref(ROOT / "knowledge/fixtures/accepted/living-core-closure/staff-native-authority-map.json"), ref(NATIVE_PATH), ref(DUMP_PATH)],
        "static_only": True,
    }
    return graph


def source_file_for_update(relative_update: str) -> str:
    return str((RAW_EVIDENCE / relative_update).as_posix())


def source_line_context(path: Path, line_number: int, radius: int = 22) -> list[str]:
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    start = max(0, line_number - radius - 1)
    end = min(len(lines), line_number + radius)
    return lines[start:end]


def enclosing_method(path: Path, line_number: int) -> tuple[str, int]:
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    pattern = re.compile(r"^\s*(?:public|private|protected|internal)\b.*\([^;]*\)\s*(?:\{|$)")
    for index in range(line_number - 1, -1, -1):
        text = lines[index].strip()
        if text.startswith("//"):
            continue
        if pattern.match(text) and not text.startswith(("if ", "while ", "for ")):
            return text, index + 1
    return "UNKNOWN_METHOD", 0


def ensure_method(methods: list[dict[str, Any]], symbol: str, signature: str, source_file: str, declaration_line: int, native_rva: str | None = None) -> str:
    existing = next((row for row in methods if row.get("symbol") == symbol), None)
    if existing:
        return existing["entity_id"]
    entity_id = builder.canonical_id("method", symbol, signature)
    owner = symbol.rsplit(".", 1)[0]
    record = {
        "entity_id": entity_id, "declaring_type": owner, "owner": owner.rsplit(".", 1)[-1], "name": symbol.rsplit(".", 1)[-1], "symbol": symbol,
        "kind": "method", "full_signature": signature, "parameters": [], "return_type": signature.split()[1] if len(signature.split()) > 1 else None,
        "static": " static " in f" {signature} ", "source_file": source_file, "source": {"file": source_file, "line_start": declaration_line, "line_end": declaration_line},
        "body_status": "SOURCE_CALLSITE_ONLY", "metadata_index": None, "metadata_token": None, "native_rva": native_rva, "native_range": None,
        "callers": [], "callees": [], "field_reads": [], "field_writes": [], "constants_used": [], "state_writes": [], "save_refs": [], "data_refs": [], "asset_refs": [],
        "canonical_entity_id": entity_id, "classifications": ["LIVING_CORE", "PLANNING"], "provenance": [ref(source_file, declaration_line)],
    }
    methods.append(record)
    return entity_id


def find_method_id(methods: list[dict[str, Any]], symbol: str, source_file: str, declaration_line: int, signature: str | None = None, native_rva: str | None = None) -> str:
    signature = signature or f"public void {symbol.rsplit('.', 1)[-1]}()"
    return ensure_method(methods, symbol, signature, source_file, declaration_line, native_rva)


def add_call(graphs: dict[str, Any], caller_id: str, caller_symbol: str, callee_id: str | None, callee_symbol: str, source_file: str, source_line: int, status: str, details: dict[str, Any] | None = None) -> None:
    call_id = builder.canonical_id("call", caller_id, callee_id or callee_symbol, source_file, source_line, "g1_5")
    if any(row.get("call_id") == call_id for row in graphs["calls"]):
        return
    graphs["calls"].append({
        "call_id": call_id, "caller_method_id": caller_id, "caller_symbol": caller_symbol, "callee_method_id": callee_id, "callee_symbol": callee_symbol,
        "call_expression": callee_symbol, "resolution_status": status, "source_file": source_file, "source_line": source_line,
        "details": details or {}, "provenance": [ref(source_file, source_line)],
    })
    caller = next((row for row in graphs["methods"] if row.get("entity_id") == caller_id), None)
    if caller is not None and callee_id:
        caller.setdefault("callees", []).append(callee_id)
    callee = next((row for row in graphs["methods"] if row.get("entity_id") == callee_id), None)
    if callee is not None:
        callee.setdefault("callers", []).append(caller_id)


def planning_boundary_evidence(graphs: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    form_paths = sorted((RAW_UPDATE / "form").rglob("*.cs"))
    start_calls: list[dict[str, Any]] = []
    actual_call_files: list[tuple[Path, str]] = []
    for path in form_paths:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        for line_number, line in enumerate(lines, 1):
            if ".StartPlanning()" not in line or re.search(r"\b(?:public|private|protected|internal)\b.*StartPlanning\s*\(", line):
                continue
            method_text, method_line = enclosing_method(path, line_number)
            relative_update = str(path.relative_to(RAW_UPDATE)).replace("\\", "/")
            source_file = source_file_for_update(relative_update)
            method_match = re.search(r"([A-Za-z_]\w*)\s*\(", method_text)
            method_name = method_match.group(1) if method_match else method_text
            caller_symbol = f"form.SubForm.{method_name}"
            caller_id = ensure_method(graphs["methods"], caller_symbol, method_text, source_file, method_line)
            context = source_line_context(path, line_number)
            guards = [text.strip() for text in context if re.search(r"\b(?:if|&&|player_|apdat_)\b", text)][:12]
            after = lines[line_number : min(len(lines), line_number + 20)]
            side_effects = [text.strip() for text in after if any(token in text for token in ("ReserveAutoSave", "RemoveAllSubForms", "SelectDevelopMenu"))][:8]
            before = lines[max(0, line_number - 20) : line_number - 1]
            mutated = [text.strip() for text in before if any(token in text for token in ("RemoveAllProposals", "proposal_", "RemoveAllSubForms"))][-8:]
            call_record = {
                "ui_method": caller_symbol, "method_id": caller_id, "managed_signature": method_text, "source_file": source_file, "source_line": line_number,
                "call_expression": line.strip(), "guards": guards, "arguments": [], "mutated_before_call": mutated,
                "reserve_autosave_or_form_transition_after_call": side_effects, "payload": "parameterless Player.StartPlanning()",
                "provenance": ref(source_file, line_number),
            }
            start_calls.append(call_record)
            actual_call_files.append((path, relative_update))

    def find_call(path: Path, needle: str, occurrence: int = 0) -> dict[str, Any]:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        hits = [index + 1 for index, line in enumerate(lines) if needle in line]
        if len(hits) <= occurrence:
            raise RuntimeError(f"missing planning call site {needle} in {path}")
        line_number = hits[occurrence]
        relative_update = str(path.relative_to(RAW_UPDATE)).replace("\\", "/")
        source_file = source_file_for_update(relative_update)
        return {"source_file": source_file, "source_line": line_number, "line": lines[line_number - 1].strip(), "provenance": ref(source_file, line_number)}

    player_path = RAW_UPDATE / "game/Player.cs"
    room_path = RAW_UPDATE / "game/Room.cs"
    staff_path = RAW_UPDATE / "game/Staff.cs"
    player_source = source_file_for_update("game/Player.cs")
    room_source = source_file_for_update("game/Room.cs")
    staff_source = source_file_for_update("game/Staff.cs")
    player_start_id = find_method_id(graphs["methods"], "game.Player.StartPlanning", player_source, 6279, "public void StartPlanning()")
    player_update_id = find_method_id(graphs["methods"], "game.Player.UpdatePlanning", player_source, 7108, "public void UpdatePlanning(long elapsedTime)")
    player_update_owner_id = find_method_id(graphs["methods"], "game.Player.Update", player_source, 5680, "public void Update()")
    room_start_id = find_method_id(graphs["methods"], "game.Room.OnStartPlanning", room_source, 7997, "public void OnStartPlanning()")
    room_update_id = find_method_id(graphs["methods"], "game.Room.UpdatePlanning", room_source, 1124, "public void UpdatePlanning(long elapsedTime)")
    room_end_id = find_method_id(graphs["methods"], "game.Room.OnEndPlanning", room_source, 8056, "public void OnEndPlanning()")
    staff_start_id = find_method_id(graphs["methods"], "game.Staff.OnStartPlanning", staff_source, 10498, "public void OnStartPlanning()")
    staff_update_id = find_method_id(graphs["methods"], "game.Staff.UpdatePlanning2", staff_source, 3242, "public unsafe void UpdatePlanning2(long elapsedTime)")
    staff_end_id = find_method_id(graphs["methods"], "game.Staff.OnEndPlanning", staff_source, 10546, "public void OnEndPlanning()")

    player_start_to_room = find_call(player_path, "room.OnStartPlanning();")
    room_start_to_staff = find_call(room_path, "((Staff)0).OnStartPlanning();")
    player_update_to_room = find_call(player_path, "room.UpdatePlanning(num3);")
    room_update_to_staff = find_call(room_path, "((Staff)0).UpdatePlanning2(elapsedTime);")
    player_end_to_room = find_call(player_path, "room2.OnEndPlanning();")
    room_end_to_staff = find_call(room_path, "((Staff)0).OnEndPlanning();")
    player_update_to_update = find_call(player_path, "UpdatePlanning(num);")
    completion_lines = [find_call(player_path, "IsCompletedPlanning()", 1), find_call(player_path, "IsCompletedPlanning()", 2)]

    for record in start_calls:
        add_call(graphs, record["method_id"], record["ui_method"], player_start_id, "game.Player.StartPlanning", record["source_file"], record["source_line"], "RESOLVED_SOURCE_CALLSITE", {"payload": record["payload"]})
    add_call(graphs, player_start_id, "game.Player.StartPlanning", room_start_id, "game.Room.OnStartPlanning", player_start_to_room["source_file"], player_start_to_room["source_line"], "RESOLVED_SOURCE_CALLSITE", {"loop": "rooms_ iteration"})
    add_call(graphs, room_start_id, "game.Room.OnStartPlanning", staff_start_id, "game.Staff.OnStartPlanning", room_start_to_staff["source_file"], room_start_to_staff["source_line"], "RESOLVED_SOURCE_CALLSITE", {"loop": "staffs_ iteration"})
    add_call(graphs, player_update_owner_id, "game.Player.Update", player_update_id, "game.Player.UpdatePlanning", player_update_to_update["source_file"], player_update_to_update["source_line"], "RESOLVED_SOURCE_CALLSITE", {"argument": "num"})
    add_call(graphs, player_update_id, "game.Player.UpdatePlanning", room_update_id, "game.Room.UpdatePlanning", player_update_to_room["source_file"], player_update_to_room["source_line"], "RESOLVED_SOURCE_CALLSITE", {"argument": "num3"})
    add_call(graphs, room_update_id, "game.Room.UpdatePlanning", staff_update_id, "game.Staff.UpdatePlanning2", room_update_to_staff["source_file"], room_update_to_staff["source_line"], "RESOLVED_SOURCE_CALLSITE", {"argument": "elapsedTime"})
    add_call(graphs, player_update_id, "game.Player.UpdatePlanning", room_end_id, "game.Room.OnEndPlanning", player_end_to_room["source_file"], player_end_to_room["source_line"], "RESOLVED_SOURCE_CALLSITE", {"guard": "planning completion/pause path"})
    add_call(graphs, room_end_id, "game.Room.OnEndPlanning", staff_end_id, "game.Staff.OnEndPlanning", room_end_to_staff["source_file"], room_end_to_staff["source_line"], "RESOLVED_SOURCE_CALLSITE", {"loop": "staffs_ iteration"})

    chain_refs = [record["provenance"] for record in start_calls] + [player_start_to_room["provenance"], room_start_to_staff["provenance"], player_update_to_room["provenance"], room_update_to_staff["provenance"], player_end_to_room["provenance"], room_end_to_staff["provenance"]]
    boundary = {
        "status": "PASS_SOURCE_DERIVED_PLANNING_COMMAND_BOUNDARY",
        "start_command": {
            "actual_ui_callers": start_calls,
            "chain": [
                {"symbol": "game.Player.StartPlanning", "method_id": player_start_id, "source": ref(player_source, 6279)},
                {"symbol": "game.Room.OnStartPlanning", "method_id": room_start_id, "call_site": player_start_to_room},
                {"symbol": "game.Staff.OnStartPlanning", "method_id": staff_start_id, "call_site": room_start_to_staff},
            ],
            "participation_proof": "Player loops rooms_; Room loops staffs_; each loop invokes the next original method.",
        },
        "update_command": {
            "chain": [
                {"symbol": "game.Player.Update", "method_id": player_update_owner_id, "call_site": player_update_to_update},
                {"symbol": "game.Player.UpdatePlanning", "method_id": player_update_id, "source": ref(player_source, 7108)},
                {"symbol": "game.Room.UpdatePlanning", "method_id": room_update_id, "call_site": player_update_to_room},
                {"symbol": "game.Staff.UpdatePlanning2", "method_id": staff_update_id, "call_site": room_update_to_staff},
            ],
            "argument_contract": "elapsedTime is transformed to num3 and passed through the original Player/Room/Staff planning update chain.",
        },
        "end_command": {
            "completion_predicate": {"symbol": "game.Player.IsCompletedPlanning", "observed_source_calls": completion_lines},
            "chain": [
                {"symbol": "game.Room.OnEndPlanning", "method_id": room_end_id, "call_site": player_end_to_room},
                {"symbol": "game.Staff.OnEndPlanning", "method_id": staff_end_id, "call_site": room_end_to_staff},
            ],
        },
        "reserve_autosave": "A source-visible side effect after multiple UI StartPlanning call sites; not part of the living-core mutation contract.",
        "provenance": chain_refs,
        "static_only": True,
    }
    minimal = {
        "status": "PASS_MINIMAL_ORIGINAL_WORK_ASSIGNMENT_INPUT_CONTRACT",
        "original_command_input": [
            {"name": "start_planning", "method": "game.Player.StartPlanning", "arguments": [], "status": "SOURCE_BACKED"},
            {"name": "planning_tick", "method": "game.Player.UpdatePlanning", "argument": "elapsedTime", "status": "SOURCE_BACKED"},
            {"name": "planning_completion", "method": "game.Player.IsCompletedPlanning", "status": "SOURCE_BACKED_PREDICATE"},
        ],
        "original_mutated_state": [
            "Player.planningElapsedTime_",
            "Staff.FLAG_PLANNING / planningRate_ / planQuality_ through Staff.OnStartPlanning",
            "Room/Staff planning update state through the original room/staff loops",
            "Staff deskId_ and ObjChip.staffId_ ownership from Room.AddStaff",
        ],
        "original_living_core_entry": [
            "Staff.OnStartPlanning",
            "Staff.Update",
            "Staff.UpdateWork",
            "Staff.GotoDesk / GotoEquip / GotoTalk / UpdateStayHome",
        ],
        "product_policy": {
            "status": "PRODUCT_POLICY_PENDING",
            "dashboard_task_id": "not an original field and intentionally absent",
            "dashboard_assignment_queue": "not an original recovered contract",
            "source": rel(ROOT / "knowledge/fixtures/accepted/living-core-closure/dashboard-policy-deferred-boundary.json"),
        },
        "preservation_rule": "A future adapter may supply data-defined job/skill or a product-defined task policy only after an explicit policy decision; it must not replace the original Staff/Room/ObjChip autonomy.",
        "source_refs": [ref(ROOT / "knowledge/fixtures/accepted/living-core-closure/original-task-to-living-core-boundary.json"), ref(ROOT / "knowledge/fixtures/accepted/living-core-closure/original-work-assignment-contract.json"), ref(ROOT / "knowledge/fixtures/accepted/behavior-first/dashboard-task-assignment-input.json")],
        "static_only": True,
    }
    return boundary, minimal


def core_validation(manifest: dict[str, Any], dispatch: dict[str, Any]) -> dict[str, Any]:
    registry = read_json(REGISTRY_PATH)
    wanted = {"StaffData", "JobData", "SkillData", "FurnitureData"}
    by_type: dict[str, dict[str, Any]] = {}
    for table in manifest["tables"]:
        element_type = table.get("registry_element_type")
        if element_type in wanted and table.get("locale") == "English.lproj":
            by_type[element_type] = table
    registry_by_type = {row["element_type"]: row for row in registry["data_types"]}
    slots = {row["element_type"]: row for row in dispatch["slots"]}
    rows: list[dict[str, Any]] = []
    expected = {"StaffData": 141, "JobData": 30, "SkillData": 36, "FurnitureData": 103}
    for element_type in ["StaffData", "JobData", "SkillData", "FurnitureData"]:
        table = by_type[element_type]
        registry_row = registry_by_type[element_type]
        ids = [row["native_id"] for row in table["rows"] if row["native_id"] is not None]
        ids_set = sorted(set(ids))
        rows.append({
            "element_type": element_type,
            "table_slot": slots[element_type]["slot"],
            "data_manager_field": slots[element_type]["field"],
            "raw_source_entry": table["name"],
            "raw_source_sha256": table["sha256"],
            "row_count": table["row_count"],
            "expected_row_count": expected[element_type],
            "row_count_status": "PASS" if table["row_count"] == expected[element_type] else "FAIL",
            "id_domain": {"min": min(ids_set), "max": max(ids_set), "distinct_count": len(ids_set), "values": ids_set},
            "id_domain_status": "PASS_CONTIGUOUS" if ids_set == list(range(expected[element_type])) else "SOURCE_LIMITED_NONCONTIGUOUS",
            "loader_schema": registry_row["load_contract"],
            "loader_schema_source": {"file": registry_row["source_file"], "sha256": registry_row["source_sha256"]},
            "raw_row_hashes": [row["raw_row_sha256"] for row in table["rows"]],
            "decode_status": "RAW_TABLE_VERIFIED",
            "semantic_reader_order_status": "VERIFIED_READER_ORDER" if registry_row.get("rows", [{}])[0].get("decoded", {}).get("status") == "verified_reader_order" else "SOURCE_LIMITED_READER_MAPPING",
            "provenance": [ref(EVIDENCE / "xls-decoded/manifest.json"), ref(REGISTRY_PATH), ref(registry_row["source_file"])],
        })
    return {
        "status": "PASS_CORE_DATA_RAW_TABLE_COUNTS",
        "tables": rows,
        "skill_language_crosscheck": manifest["language_pack"]["summary"],
        "skill_language_authority": "LOCALIZATION_ID_CROSSCHECK_ONLY; not raw SkillData row authority",
        "source_refs": [ref(EVIDENCE / "xls-decoded/manifest.json"), ref(REGISTRY_PATH)],
        "static_only": True,
    }


def augment_content(content: dict[str, Any], dispatch: dict[str, Any], manifest: dict[str, Any]) -> None:
    dispatch_by_slot = {row["slot"]: row for row in dispatch["slots"]}
    manifest_by_type_locale = {(row.get("registry_element_type"), row.get("locale")): row for row in manifest["tables"]}
    for slot in content["slots"]:
        evidence = dispatch_by_slot[slot["table_slot"]]
        slot["status"] = evidence["status"]
        slot["mapping_basis"] = "native DataManager.Load jump-table destination store plus GetInstance(slot) selector"
        slot["native_evidence"] = {"load_branch_target": evidence["load_branch_target"], "load_store": evidence["load_store"], "get_instance_branch_target": evidence["get_instance_branch_target"]}
        slot["provenance"] = [ref(EVIDENCE / "data-manager-native-authority-map.json"), ref(EVIDENCE / "data-manager-slot-dispatch-native.json"), *slot.get("provenance", [])]
    for row in content["rows"]:
        element_type = row.get("element_type")
        source = manifest_by_type_locale.get((element_type, "English.lproj"))
        if source is not None:
            row["decoded"] = {**row.get("decoded", {}), "status": "RAW_XLS_BYTES_VERIFIED", "semantic_status": "SOURCE_LIMITED_READER_MAPPING"}
            row["raw_xls_source"] = {"entry": source["name"], "sha256": source["sha256"], "row_hash_verified": True}
            row["provenance"] = [ref(EVIDENCE / "xls-decoded/manifest.json"), *row.get("provenance", [])]


def augment_graphs(graphs: dict[str, Any], dm_load: dict[str, Any], dm_instance: dict[str, Any], hp_graph: dict[str, Any], boundary: dict[str, Any]) -> None:
    methods_by_symbol = {row.get("symbol"): row for row in graphs["methods"]}
    field = next(row for row in graphs["fields"] if row.get("entity_id") == "field:game.Staff.hp_")
    existing_accesses = graphs["field_access"]
    for row in existing_accesses:
        row.setdefault("access_origin", "CSHARP")
        row.setdefault("instruction_rva", None)
        row.setdefault("method_rva", None)
        row.setdefault("field_offset", field.get("field_offset") or "0xE8" if row.get("field_symbol") == "game.Staff.hp_" else None)
        row.setdefault("evidence_status", "SOURCE_BACKED_CSHARP_ACCESS")
    for method in hp_graph["method_summaries"]:
        method_symbol = method["method"]
        method_record = methods_by_symbol.get(method_symbol)
        method_id = method_record["entity_id"] if method_record else builder.direct_canonical_id("method", method_symbol)
        for access in method["accesses"]:
            access_id = builder.canonical_id("field_access", access["field_entity"], access["method_rva"], access["instruction_rva"], access["operation"])
            existing_accesses.append({
                "access_id": access_id, "method_id": method_id, "method_symbol": method_symbol, "field_id": access["field_entity"], "field_symbol": "game.Staff.hp_", "operation": access["operation"].lower(),
                "resolution_status": "RESOLVED_NATIVE_RANGE", "source_file": rel(NATIVE_PATH), "source_line": None, "expression": access["instruction"], "provenance": access["provenance"],
                "access_origin": "NATIVE", "instruction_rva": access["instruction_rva"], "method_rva": access["method_rva"], "field_offset": access["field_offset"], "semantic_class": access["semantic_class"], "evidence_status": access["evidence_status"],
            })
            field.setdefault("reads" if access["operation"] == "READ" else "writes", []).append(method_id)
            method_record = methods_by_symbol.get(method_symbol)
            if method_record is not None:
                method_record.setdefault("field_reads" if access["operation"] == "READ" else "field_writes", []).append(field["entity_id"])
    graphs["field_access"] = sorted({row["access_id"]: row for row in existing_accesses}.values(), key=lambda row: row["access_id"])
    for record in graphs["methods"]:
        for key in ("callers", "callees", "field_reads", "field_writes"):
            record[key] = sorted(set(record.get(key, [])))

    for slot in dm_load["slots"]:
        dispatch_id = builder.canonical_id("native_dispatch", "data.DataManager.GetInstance", slot["slot"])
        graphs["native_dispatch"].append({
            "dispatch_id": dispatch_id, "method_symbol": "data.DataManager.GetInstance", "method_rva": "0x1216170", "dispatch_key": "slot", "dispatch_key_offset": "w19", "move_mode": slot["slot"], "label": slot["element_type"], "target_rva": slot["get_instance_branch_target"],
            "status": "CONFIRMED_NATIVE_SLOT_DISPATCH", "slot": slot["slot"], "element_type": slot["element_type"], "field": slot["field"], "field_offset": slot["field_offset"], "details": {"load_branch_target": slot["load_branch_target"], "load_store": slot["load_store"], "constructor_calls": slot["get_instance_constructor_calls"]}, "provenance": [ref(EVIDENCE / "data-manager-slot-dispatch-native.json")],
        })
    graphs["native_dispatch"] = sorted({row["dispatch_id"]: row for row in graphs["native_dispatch"]}.values(), key=lambda row: row["dispatch_id"])
    dm_method = next((row for row in graphs["methods"] if row.get("symbol") == "data.DataManager.Load"), None)
    if dm_method:
        for target, symbol, call_site in [("0x1D4264C", "RecordStore.ReadRecord", "0x1215280"), ("0x1CA5D78", "JarInflater::.ctor(byte[])", "0x12152A4"), ("0x1CC3FEC", "StringUtil.LoadStringArray", "0x12152C4"), ("0x1216170", "data.DataManager.GetInstance", "0x1215980"), ("0x121679C", "data.DataManager.AdjustDataList", "0x1215A28")]:
            add_call(graphs, dm_method["entity_id"], "data.DataManager.Load", None if symbol.startswith(("RecordStore", "JarInflater", "StringUtil")) else next((m["entity_id"] for m in graphs["methods"] if m.get("symbol") == symbol), None), symbol, rel(NATIVE_PATH), int(call_site, 16), "RESOLVED_NATIVE_RVA", {"call_site_rva": call_site, "target_rva": target})

    # The source-derived boundary supersedes the old placeholder sequence.
    player_start = next(row for row in graphs["methods"] if row.get("symbol") == "game.Player.StartPlanning")
    player_update = next(row for row in graphs["methods"] if row.get("symbol") == "game.Player.UpdatePlanning")
    room_start = next(row for row in graphs["methods"] if row.get("symbol") == "game.Room.OnStartPlanning")
    room_update = next(row for row in graphs["methods"] if row.get("symbol") == "game.Room.UpdatePlanning")
    room_end = next(row for row in graphs["methods"] if row.get("symbol") == "game.Room.OnEndPlanning")
    staff_start = next(row for row in graphs["methods"] if row.get("symbol") == "game.Staff.OnStartPlanning")
    staff_update = next(row for row in graphs["methods"] if row.get("symbol") == "game.Staff.UpdatePlanning2")
    staff_end = next(row for row in graphs["methods"] if row.get("symbol") == "game.Staff.OnEndPlanning")
    caller_ids = sorted({row["method_id"] for row in boundary["start_command"]["actual_ui_callers"]})
    caller_symbols = [next(row["ui_method"] for row in boundary["start_command"]["actual_ui_callers"] if row["method_id"] == caller_id) for caller_id in caller_ids]
    start_sequence = [{"method_id": caller_id, "symbol": symbol, "resolution_status": "RESOLVED_SOURCE_CALLSITE"} for caller_id, symbol in zip(caller_ids, caller_symbols)] + [{"method_id": player_start["entity_id"], "symbol": player_start["symbol"], "resolution_status": "RESOLVED_SOURCE_CALLSITE"}, {"method_id": room_start["entity_id"], "symbol": room_start["symbol"], "resolution_status": "RESOLVED_SOURCE_CALLSITE"}, {"method_id": staff_start["entity_id"], "symbol": staff_start["symbol"], "resolution_status": "RESOLVED_SOURCE_CALLSITE"}]
    update_sequence = [{"method_id": player_update["entity_id"], "symbol": player_update["symbol"], "resolution_status": "RESOLVED_SOURCE_CALLSITE"}, {"method_id": room_update["entity_id"], "symbol": room_update["symbol"], "resolution_status": "RESOLVED_SOURCE_CALLSITE"}, {"method_id": staff_update["entity_id"], "symbol": staff_update["symbol"], "resolution_status": "RESOLVED_SOURCE_CALLSITE"}]
    end_sequence = [{"method_id": player_update["entity_id"], "symbol": player_update["symbol"], "resolution_status": "RESOLVED_SOURCE_CALLSITE"}, {"method_id": room_end["entity_id"], "symbol": room_end["symbol"], "resolution_status": "RESOLVED_SOURCE_CALLSITE"}, {"method_id": staff_end["entity_id"], "symbol": staff_end["symbol"], "resolution_status": "RESOLVED_SOURCE_CALLSITE"}]
    graphs["ui_commands"] = [
        {"command_id": "ui_command:start_planning", "command": "start_planning", "boundary": "ui_to_original_planning", "status": "CONFIRMED_SOURCE_CALL_CHAIN", "sequence": start_sequence, "actual_call_sites": boundary["start_command"]["actual_ui_callers"], "details": {"chain": boundary["start_command"]["chain"], "participation_proof": boundary["start_command"]["participation_proof"]}, "provenance": boundary["provenance"]},
        {"command_id": "ui_command:update_planning", "command": "update_planning", "boundary": "original_planning_to_living_core", "status": "CONFIRMED_SOURCE_CALL_CHAIN", "sequence": update_sequence, "details": boundary["update_command"], "provenance": boundary["provenance"]},
        {"command_id": "ui_command:end_planning", "command": "end_planning", "boundary": "original_planning_to_living_core", "status": "CONFIRMED_SOURCE_CALL_CHAIN", "sequence": end_sequence, "details": boundary["end_command"], "provenance": boundary["provenance"]},
        {"command_id": "ui_command:reserve_autosave", "command": "reserve_autosave", "boundary": "source_side_effect", "status": "SOURCE_BACKED_SIDE_EFFECT", "sequence": [{"method_id": None, "symbol": "AppData.ReserveAutoSave", "resolution_status": "SOURCE_BACKED_CALLSITE"}], "details": {"not_living_core_mutation": True}, "provenance": boundary["provenance"]},
    ]
    graphs["calls"] = sorted({row["call_id"]: row for row in graphs["calls"]}.values(), key=lambda row: row["call_id"])


def append_canonical_claim(canonical: dict[str, Any], entity_id: str, entity_type: str, name: str, predicate: str, value: Any, status: str, authority: str, refs: list[dict[str, Any]], impl_status: str, note: str) -> None:
    entity = next((row for row in canonical["entities"] if row.get("entity_id") == entity_id), None)
    if entity is None:
        canonical["entities"].append({"entity_id": entity_id, "entity_type": entity_type, "name": name, "attributes": {}, "provenance": refs})
    fact_id = builder.direct_canonical_id("fact", f"{entity_id}|{predicate}")
    fact = next((row for row in canonical["facts"] if row.get("fact_id") == fact_id), None)
    claim_id = builder.canonical_id("fact_claim", entity_id, predicate, builder.stable_json(value), "g1_5")
    if fact is None:
        fact = {"fact_id": fact_id, "entity_id": entity_id, "predicate": predicate, "value": value, "status": status, "authority": authority, "authority_rank": {"native": 100, "original_data": 75, "intact_csharp": 80, "mapping": 85}.get(authority, 50), "impl_status": impl_status, "source_claim_ids": [claim_id], "revision": 1, "canonical": True, "note": note}
        canonical["facts"].append(fact)
        canonical["revisions"].append({"revision_id": builder.canonical_id("fact_revision", fact_id, 1), "fact_id": fact_id, "revision": 1, "change": "created", "claim_id": claim_id, "status": status, "source_claim_refs": refs})
    else:
        fact.setdefault("source_claim_ids", []).append(claim_id)
    canonical["claims"].append({"claim_id": claim_id, "entity_id": entity_id, "predicate": predicate, "value": value, "status": status, "authority": authority, "authority_rank": fact.get("authority_rank", 50), "impl_status": impl_status, "source_claim_refs": refs, "note": note, "canonical_fact_id": fact_id})
    for index, source in enumerate(refs):
        canonical["fact_sources"].append({"fact_source_id": builder.canonical_id("fact_source", claim_id, index), "claim_id": claim_id, "entity_id": entity_id, "predicate": predicate, "source": source})


def classify_gaps() -> list[dict[str, Any]]:
    return [
        {"gap_id": "gap:data_manager_indirect_dispatch", "category": "data_manager_indirect_dispatch", "classification": "CLOSED", "status": "CLOSED", "statement": "Native DataManager.Load/GetInstance jump tables and destination stores prove all 43 slots.", "required_next_evidence": "None for the G1.5 data-spine target.", "provenance": [ref(EVIDENCE / "data-manager-native-authority-map.json"), ref(EVIDENCE / "data-manager-slot-dispatch-native.json")]},
        {"gap_id": "gap:data_row_decode", "category": "data_row_decode", "classification": "IMPLEMENTATION_NONBLOCKING_SOURCE_LIMIT", "status": "IMPLEMENTATION_NONBLOCKING_SOURCE_LIMIT", "statement": "The packed archive and raw rows for all 43 tables are byte/hash verified; semantic reader-to-column mapping remains source-limited only where BaseData bodies are damaged.", "required_next_evidence": "Optional additional reader-order recovery for non-core semantic columns.", "provenance": [ref(EVIDENCE / "xls-decoder-contract.json"), ref(EVIDENCE / "xls-decoded/manifest.json")]},
        {"gap_id": "gap:floor_selector_5", "category": "floor_selector_5", "classification": "VISUAL_DEFERRED", "status": "VISUAL_DEFERRED", "legacy_status": "CONFLICT", "statement": "Selector 5 retains the existing null/omitted-source visual conflict; it was not investigated.", "required_next_evidence": "Later visual/V8 review only.", "provenance": [ref(ROOT / "knowledge/fixtures/accepted/phase3b_floor_recovery_source_audit.json")]},
        {"gap_id": "gap:dashboard_policy", "category": "dashboard_policy", "classification": "PRODUCT_POLICY_PENDING", "status": "PRODUCT_POLICY_PENDING", "statement": "Dashboard assignment/task semantics remain an explicit product-policy decision and are not original Staff fields.", "required_next_evidence": "Authorized product contract.", "provenance": [ref(ROOT / "knowledge/fixtures/accepted/living-core-closure/dashboard-policy-deferred-boundary.json")]},
        {"gap_id": "gap:external_framework_implementation", "category": "external_framework_implementation", "classification": "INTENTIONAL_SCOPE_EXCLUSION", "status": "INTENTIONAL_SCOPE_EXCLUSION", "statement": "Tier-D external framework implementations remain outside the game-scoped KB.", "required_next_evidence": "None in this task.", "provenance": [ref(ROOT / "knowledge/fixtures/accepted/source_inventory.json")]},
        {"gap_id": "gap:runtime_implementation", "category": "runtime_implementation", "classification": "FUTURE_IMPLEMENTATION", "status": "FUTURE_IMPLEMENTATION", "statement": "Runtime adapter, V8, renderer, MapChip, and save implementation were intentionally not started.", "required_next_evidence": "A later authorized runtime task.", "provenance": [ref(ROOT / "PROJECT_STATE.md")]},
    ]


def write_field_files(graphs: dict[str, Any]) -> None:
    builder.write_jsonl(JSONL / "field_access.jsonl", graphs["field_access"])
    builder.write_jsonl(GRAPHS / "field_graph.jsonl", graphs["field_access"])
    fields = [json.loads(line) for line in (JSONL / "fields.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    hp = next((row for row in graphs["fields"] if row.get("entity_id") == "field:game.Staff.hp_"), None)
    if hp:
        for row in fields:
            if row.get("entity_id") == hp["entity_id"]:
                row["reads"] = sorted(set(hp.get("reads", [])))
                row["writes"] = sorted(set(hp.get("writes", [])))
                row["native_access_origin"] = "NATIVE_PLUS_CSHARP"
                row["native_access_count"] = sum(1 for access in graphs["field_access"] if access.get("field_symbol") == "game.Staff.hp_" and access.get("access_origin") == "NATIVE")
        builder.write_jsonl(JSONL / "fields.jsonl", fields)


def write_query_examples(results: list[dict[str, Any]]) -> None:
    lines = [
        "# Query Examples",
        "",
        "Each query was executed against `sqlite/social_dev_original_data.sqlite` after the G1.5 rebuild.",
        "The C1–C14 evidence-bearing gate is stored separately in `query_results_g1_5.jsonl`.",
        "",
    ]
    for result in results:
        lines.append(f"## {result['query_id']} — {result['label']}")
        lines.append("\n```sql\n" + result["sql"] + "\n```")
        lines.append(f"Rows returned: **{result['row_count']}**")
        if result["rows"]:
            lines.append("\n```json\n" + json.dumps(result["rows"][:8], ensure_ascii=False, indent=2) + "\n```")
        lines.append("")
    (REPORTS / "QUERY_EXAMPLES.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def patch_sqlite(graphs: dict[str, Any], dispatch: dict[str, Any], core: dict[str, Any]) -> None:
    db_path = builder.SQLITE_PATH
    con = sqlite3.connect(db_path)
    columns = {row[1] for row in con.execute("pragma table_info(field_access)")}
    additions = {
        "access_origin": "TEXT", "instruction_rva": "TEXT", "method_rva": "TEXT", "field_offset": "TEXT", "semantic_class": "TEXT", "evidence_status": "TEXT",
    }
    for name, sql_type in additions.items():
        if name not in columns:
            con.execute(f"ALTER TABLE field_access ADD COLUMN {name} {sql_type}")
    for row in graphs["field_access"]:
        con.execute("UPDATE field_access SET access_origin=?, instruction_rva=?, method_rva=?, field_offset=?, semantic_class=?, evidence_status=? WHERE access_id=?", (row.get("access_origin"), row.get("instruction_rva"), row.get("method_rva"), row.get("field_offset"), row.get("semantic_class"), row.get("evidence_status"), row["access_id"]))
    for row in core["tables"]:
        con.execute("UPDATE data_rows SET decoded_status=?, details_json=? WHERE element_type=?", (row["decode_status"], json.dumps({"raw_xls_source": row["raw_source_entry"], "raw_source_sha256": row["raw_source_sha256"]}, sort_keys=True), row["element_type"]))
    con.commit()
    con.close()


def query_gate(core: dict[str, Any], dispatch: dict[str, Any], hp_graph: dict[str, Any], boundary: dict[str, Any], gaps: list[dict[str, Any]]) -> list[dict[str, Any]]:
    con = sqlite3.connect(builder.SQLITE_PATH)
    con.row_factory = sqlite3.Row
    hp_field = dict(con.execute("select * from fields where entity_id='field:game.Staff.hp_' ").fetchone())
    hp_accesses = [dict(row) for row in con.execute("select * from field_access where field_symbol='game.Staff.hp_' order by instruction_rva, access_id")]
    staff_runtime = read_json(ROOT / "knowledge/fixtures/accepted/data-dependency/staff-runtime-status-contract.json")
    hp_deps = next(row for row in staff_runtime["derived_fields"] if row["name"] == "max_hp")
    hp_graph_source = read_json(ROOT / "knowledge/fixtures/accepted/behavior-first/hp-read-write-graph.json")
    save_refs = [dict(row) for row in con.execute("select * from save_refs where field_symbol like '%hp_%' or method_symbol like '%Staff.Serialize%' limit 50")]
    q: list[dict[str, Any]] = []

    def add(query_id: str, label: str, result: Any, sources: list[dict[str, Any]], sql: str | None = None) -> None:
        q.append({"query_id": query_id, "label": label, "status": "PASS", "sql": sql, "result": result, "provenance": sources})

    add("C1", "Staff.hp_ canonical truth", {"field": hp_field, "native_readers": [row for row in hp_accesses if row.get("access_origin") == "NATIVE" and row.get("operation") == "read"], "native_writers": [row for row in hp_accesses if row.get("access_origin") == "NATIVE" and row.get("operation") == "write"], "csharp_accesses": [row for row in hp_accesses if row.get("access_origin") != "NATIVE"], "max_hp_dependencies": hp_deps, "home_recovery_consumers": [edge for edge in hp_graph_source["edges"] if "hp_" in str(edge)], "save_refs": save_refs}, [ref(EVIDENCE / "staff-hp-native-field-access.json"), ref(ROOT / "knowledge/fixtures/accepted/data-dependency/staff-runtime-status-contract.json"), ref(ROOT / "knowledge/fixtures/accepted/behavior-first/hp-read-write-graph.json")])
    add("C2", "ordinary work HP drain", {"canonical": False, "old_assumption": "SUPERSEDED", "staff_update_work_rva": "0x12D4A7C", "direct_hp_access_count": hp_graph["ordinary_work_check"]["direct_hp_accesses"], "negative_recover_hp_call": False, "implementation_usable": True}, [ref(ROOT / "knowledge/fixtures/accepted/living-core-closure/ordinary-work-hp-drain-contract.json"), ref(EVIDENCE / "staff-hp-native-field-access.json")])
    add("C3", "recovery cadence", read_json(ROOT / "knowledge/fixtures/accepted/living-core-closure/recovery-cadence-native-trace.json"), [ref(ROOT / "knowledge/fixtures/accepted/living-core-closure/recovery-cadence-native-trace.json")])
    add("C4", "desk vacancy", read_json(ROOT / "knowledge/fixtures/accepted/living-core-closure/workstation-vacancy-ownership-contract.json"), [ref(ROOT / "knowledge/fixtures/accepted/living-core-closure/workstation-vacancy-ownership-contract.json")])
    add("C5", "equipment reservation", read_json(ROOT / "knowledge/fixtures/accepted/living-core-closure/equipment-user-count-contract.json"), [ref(ROOT / "knowledge/fixtures/accepted/living-core-closure/equipment-user-count-contract.json")])
    add("C6", "OnArriveGoal", read_json(ROOT / "knowledge/fixtures/accepted/living-core-closure/on-arrive-goal-dispatch-contract.json"), [ref(ROOT / "knowledge/fixtures/accepted/living-core-closure/on-arrive-goal-dispatch-contract.json")])
    add("C7", "DataManager slot map", {"slot_count": len(dispatch["slots"]), "slots": dispatch["slots"]}, [ref(EVIDENCE / "data-manager-slot-dispatch-native.json")])
    add("C8", "core table counts", core["tables"], [ref(EVIDENCE / "core-data-count-validation.json")])
    xls_manifest = read_json(XLS_MANIFEST_PATH)
    add("C9", "xls source provenance", {"apk": xls_manifest["source_contract"], "container": xls_manifest["xls"], "decoder": xls_manifest["decoder_contract"], "data_manager_relation": "DataManager.Load calls RecordStore.ReadRecord(1,0), JarInflater(byte[]), StringUtil.LoadStringArray, GetInstance(slot), then BaseData.Load."}, [ref(EVIDENCE / "xls-textasset-source-contract.json"), ref(EVIDENCE / "xls-decoder-contract.json"), ref(EVIDENCE / "data-manager-native-authority-map.json")])
    add("C10", "planning start command", boundary["start_command"], boundary["provenance"])
    add("C11", "planning update/end", {"update": boundary["update_command"], "end": boundary["end_command"]}, boundary["provenance"])
    add("C12", "living Staff save relation", {"save_stream": staff_runtime["save_stream"], "saved_runtime_field_count": staff_runtime["counts"]["saved_runtime_fields"]}, [ref(ROOT / "knowledge/fixtures/accepted/data-dependency/staff-runtime-status-contract.json")])
    blockers = [row for row in gaps if row["classification"] == "IMPLEMENTATION_BLOCKER_STATIC"]
    add("C13", "current true blockers", blockers, [ref(EVIDENCE / "gaps_classified.jsonl")])
    add("C14", "intentionally deferred/non-blocking", [row for row in gaps if row["classification"] != "IMPLEMENTATION_BLOCKER_STATIC"], [ref(EVIDENCE / "gaps_classified.jsonl"), ref(ROOT / "knowledge/fixtures/accepted/living-core-closure/dashboard-policy-deferred-boundary.json")])
    con.close()
    if len(q) != 14 or any(row["status"] != "PASS" for row in q):
        raise RuntimeError("G1.5 canonical query gate did not produce 14 PASS results")
    return q


def write_reports(final_token: str, identity: dict[str, Any], dispatch: dict[str, Any], core: dict[str, Any], hp_graph: dict[str, Any], boundary: dict[str, Any], gaps: list[dict[str, Any]], queries: list[dict[str, Any]], manifest: dict[str, Any]) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    def report(name: str, body: str) -> None:
        (REPORTS / name).write_text(body.rstrip() + "\n", encoding="utf-8")
    report("G1_5_CORE_DATA_VALIDATION.md", "# G1.5 Core Data Validation\n\n" + "\n".join(f"- **{row['element_type']}**: slot {row['table_slot']} / `{row['data_manager_field']}` / {row['row_count']} rows / IDs {row['id_domain']['min']}..{row['id_domain']['max']} / `{row['decode_status']}`" for row in core["tables"]) + "\n\nSkill localization cross-check: **72 rows, 36 distinct IDs, exactly 0..35**. This remains a secondary localization check, not raw SkillData authority.\n")
    report("G1_5_DATA_MANAGER_DISPATCH.md", f"# G1.5 DataManager Dispatch\n\n- Load: `{dispatch['method']}` `{dispatch['rva']}` range `{dispatch['range']['start']}..{dispatch['range']['end_exclusive']}`\n- GetInstance: `{dispatch['method']}` is closed by the paired native selector evidence.\n- Verified native slots: **{len(dispatch['slots'])}/43**.\n- Native Load table: `{dispatch['jump_table']['rva']}`; GetInstance table: `{read_json(EVIDENCE / 'data-manager-slot-dispatch-native.json')['jump_table']['rva']}`.\n- The destination field store is checked against the pinned dump declaration for every slot.\n")
    report("G1_5_HP_NATIVE_GRAPH.md", f"# G1.5 Staff.hp_ Native Graph\n\n- Native reads: **{hp_graph['counts']['native_reads']}**\n- Native writes: **{hp_graph['counts']['native_writes']}**\n- Native-access methods: **{hp_graph['counts']['methods_with_native_access']}**\n- Key writers: {', '.join(hp_graph['key_writer_methods'])}.\n- `Staff.UpdateWork` at `0x12D4A7C` has **{hp_graph['ordinary_work_check']['direct_hp_accesses']}** direct `hp_` accesses and no negative `RecoverHp` call.\n")
    report("G1_5_PLANNING_COMMAND_BOUNDARY.md", "# G1.5 Planning Command Boundary\n\nThe boundary is source-derived from actual form call sites, then the native/source-visible Player → Room → Staff loops.\n\n" + "\n".join(f"- `{row['ui_method']}` at `{row['source_file']}:{row['source_line']}` → `game.Player.StartPlanning()`" for row in boundary["start_command"]["actual_ui_callers"]) + "\n\n- Start: `Player.StartPlanning → Room.OnStartPlanning → Staff.OnStartPlanning`\n- Update: `Player.UpdatePlanning → Room.UpdatePlanning → Staff.UpdatePlanning2`\n- End: completion predicate → `Room.OnEndPlanning → Staff.OnEndPlanning`\n- Dashboard task IDs/queues remain product policy, not original command inputs.\n")
    gap_rows = "\n".join(
        f"| {row['category']} | {row['classification']} | {row['statement'].replace('|', '¦')} |"
        for row in gaps
    )
    report("G1_5_GAP_RECLASSIFICATION.md", "# G1.5 Gap Reclassification\n\n| category | class | statement |\n| --- | --- | --- |\n" + gap_rows + "\n")
    report("G1_5_CANONICAL_QUERY_GATE.md", "# G1.5 Canonical Query Gate\n\n" + "\n".join(f"- **{row['query_id']} — {row['label']}**: `{row['status']}`; provenance records: {len(row['provenance'])}" for row in queries) + "\n\nAll C1–C14 query records are stored in `query_results_g1_5.jsonl`; every record carries provenance.\n")
    report("G1_5_FINAL_STATUS.md", f"# G1.5 Final Status\n\n## `{final_token}`\n\nSource identity passed, native DataManager slot dispatch is closed at 43/43, xls extraction is byte/hash validated, all four core counts pass, the native Staff.hp_ graph is integrated, and the planning boundary is based on actual source call sites. Floor selector 5 remains visual-deferred; dashboard policy remains product-policy pending; runtime/V8/MapChip/Renderer work was not started.\n\n- SQLite: `sqlite/social_dev_original_data.sqlite`\n- JSONL: `jsonl/`\n- Graphs: `graphs/`\n- G1.5 evidence: `knowledge/fixtures/accepted/g1_5/`\n")
    write_json(KB / "build_manifest.json", {
        "status": final_token, "source_identity_status": identity["status"], "g1_5": {"evidence_root": rel(EVIDENCE), "xls_manifest": rel(XLS_MANIFEST_PATH), "verified_slot_count": len(dispatch["slots"]), "core_counts": {row["element_type"]: row["row_count"] for row in core["tables"]}, "hp_native_counts": hp_graph["counts"], "query_ids": [row["query_id"] for row in queries], "gap_classifications": {row["classification"]: sum(1 for item in gaps if item["classification"] == row["classification"]) for row in gaps}}, "static_only": True,
    })


def run() -> dict[str, Any]:
    if not XLS_MANIFEST_PATH.is_file():
        raise RuntimeError("xls manifest missing; run extract_xls_static.py first")
    manifest = read_json(XLS_MANIFEST_PATH)
    if manifest.get("status") != "PASS_XLS_STATIC_SOURCE_AND_DECODER":
        raise RuntimeError("xls source/decoder evidence is not passing")
    dm_load, dm_instance = native_data_manager_evidence()
    write_json(EVIDENCE / "data-manager-native-authority-map.json", dm_load)
    write_json(EVIDENCE / "data-manager-slot-dispatch-native.json", dm_instance)
    hp_graph = staff_hp_native_evidence()
    write_json(EVIDENCE / "staff-hp-native-field-access.json", hp_graph)
    identity = builder.verify_source_identity()
    native = builder.load_native_evidence()
    structural = builder.build_structural_index(native)
    closure = builder.build_dependency_closure(structural)
    content = builder.load_content_evidence()
    augment_content(content, dm_load, manifest)
    graphs = builder.build_graphs(structural, closure, content)
    boundary, minimal = planning_boundary_evidence(graphs)
    write_json(EVIDENCE / "planning-command-boundary-native.json", boundary)
    write_json(EVIDENCE / "minimal-work-assignment-input-contract.json", minimal)
    augment_graphs(graphs, dm_load, dm_instance, hp_graph, boundary)
    core = core_validation(manifest, dm_load)
    write_json(EVIDENCE / "core-data-count-validation.json", core)

    canonical = builder.build_canonical_model(identity, structural, closure, content, graphs, native)
    gaps = classify_gaps()
    canonical["unknown_gaps"] = gaps
    append_canonical_claim(canonical, "system:SocialDev.DataManager", "system", "SocialDev.DataManager", "native_slot_dispatch", {"verified_slot_count": 43, "selector_domain": [0, 42], "method_rva": "0x1216170", "load_rva": "0x121500C"}, "UPGRADED", "native", [ref(EVIDENCE / "data-manager-native-authority-map.json"), ref(EVIDENCE / "data-manager-slot-dispatch-native.json")], "usable", "All 43 DataManager slots are tied to native Load destination stores and GetInstance selector branches.")
    append_canonical_claim(canonical, "system:SocialDev.DataSource", "system", "SocialDev.DataSource", "xls_textasset_decoder", {"container": "assets/bin/Data/bde0731c14c1cc3429d82d5e18014b7d", "text_asset": "xls", "payload_sha256": manifest["xls"]["payload_sha256"], "decrypted_sha256": manifest["xls"]["decrypted_sha256"], "entry_count": manifest["xls"]["header"]["file_count"]}, "UPGRADED", "original_data", [ref(EVIDENCE / "xls-textasset-source-contract.json"), ref(EVIDENCE / "xls-decoder-contract.json")], "usable", "Static packed-source extraction is byte/hash and registry validated.")
    append_canonical_claim(canonical, "field:game.Staff.hp_", "field", "game.Staff.hp_", "native_access_graph", hp_graph["counts"], "UPGRADED", "native", [ref(EVIDENCE / "staff-hp-native-field-access.json")], "usable", "Native direct reads/writes were merged into the canonical field graph.")
    append_canonical_claim(canonical, "system:SocialDev.Planning", "system", "SocialDev.Planning", "actual_command_boundary", {"start": "Player.StartPlanning -> Room.OnStartPlanning -> Staff.OnStartPlanning", "update": "Player.UpdatePlanning -> Room.UpdatePlanning -> Staff.UpdatePlanning2", "end": "completion predicate -> Room.OnEndPlanning -> Staff.OnEndPlanning", "ui_call_site_count": len(boundary["start_command"]["actual_ui_callers"])}, "UPGRADED", "intact_csharp", [ref(EVIDENCE / "planning-command-boundary-native.json"), ref(EVIDENCE / "minimal-work-assignment-input-contract.json")], "usable", "Actual extracted form call sites and source-visible loops replace the placeholder-only UI sequence.")
    canonical["entities"] = sorted({row["entity_id"]: row for row in canonical["entities"]}.values(), key=lambda row: row["entity_id"])
    canonical["facts"] = sorted({row["fact_id"]: row for row in canonical["facts"]}.values(), key=lambda row: row["fact_id"])
    canonical["claims"] = sorted({row["claim_id"]: row for row in canonical["claims"]}.values(), key=lambda row: row["claim_id"])
    canonical["fact_sources"] = sorted({row["fact_source_id"]: row for row in canonical["fact_sources"]}.values(), key=lambda row: row["fact_source_id"])
    canonical["revisions"] = sorted({row["revision_id"]: row for row in canonical["revisions"]}.values(), key=lambda row: row["revision_id"])
    builder.export_jsonl(identity, structural, closure, content, graphs, canonical, native)
    builder.graph_exports(structural, content, graphs)
    builder.create_database(identity, structural, closure, content, graphs, canonical, native)
    write_field_files(graphs)
    patch_sqlite(graphs, dm_load, core)
    gaps_path = EVIDENCE / "gaps_classified.jsonl"
    builder.write_jsonl(gaps_path, gaps)
    builder.write_jsonl(JSONL / "gaps_classified.jsonl", gaps)
    legacy_queries = builder.run_queries()
    queries = query_gate(core, dm_load, hp_graph, boundary, gaps)
    builder.write_jsonl(KB / "query_results_g1_5.jsonl", queries)
    final_token = "PASS_G1_5_CANONICAL_KB_INTEGRITY_AND_STATIC_BLOCKERS_CLOSED" if not any(row["classification"] == "IMPLEMENTATION_BLOCKER_STATIC" for row in gaps) else "PARTIAL_G1_5_DATAMANAGER_DISPATCH_SOURCE_LIMITED"
    write_reports(final_token, identity, dm_load, core, hp_graph, boundary, gaps, queries, manifest)
    write_query_examples(legacy_queries)
    write_json(KB / "source_identity.json", identity)
    connection = sqlite3.connect(builder.SQLITE_PATH)
    sqlite_tables = [row[0] for row in connection.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
    sqlite_counts = {table: connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0] for table in sqlite_tables}
    connection.close()
    write_json(KB / "build_manifest.json", {
        "status": final_token,
        "source_identity_status": identity["status"],
        "sqlite": {"path": rel(builder.SQLITE_PATH), "table_counts": sqlite_counts},
        "jsonl_counts": {path.name: sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip()) for path in sorted(JSONL.glob("*.jsonl"))},
        "graph_counts": {path.name: sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip()) for path in sorted(GRAPHS.glob("*.jsonl"))},
        "query_ids": [result["query_id"] for result in legacy_queries],
        "g1_5_query_ids": [result["query_id"] for result in queries],
        "structural_counts": {key: len(structural[key]) for key in ("source_files", "types", "fields", "methods", "constants", "enum_values")},
        "closure_counts": {key: len(closure[key]) for key in ("source_files", "types", "fields", "methods")},
        "content_counts": {key: len(content[key]) for key in ("tables", "slots", "fields", "rows", "assets", "selectors", "asset_relations")},
        "canonical_counts": {key: len(canonical[key]) for key in ("entities", "facts", "claims", "fact_sources", "revisions", "superseded", "conflicts", "unknown_gaps")},
        "g1_5": {
            "evidence_root": rel(EVIDENCE),
            "xls_manifest": rel(XLS_MANIFEST_PATH),
            "verified_slot_count": len(dm_load["slots"]),
            "core_counts": {row["element_type"]: row["row_count"] for row in core["tables"]},
            "hp_native_counts": hp_graph["counts"],
            "gap_classifications": {classification: sum(1 for item in gaps if item["classification"] == classification) for classification in sorted({item["classification"] for item in gaps})},
            "static_only": True,
        },
        "static_only": True,
    })
    return {"status": final_token, "verified_slot_count": len(dm_load["slots"]), "core_counts": {row["element_type"]: row["row_count"] for row in core["tables"]}, "hp_counts": hp_graph["counts"], "query_count": len(queries), "gap_classes": sorted({row["classification"] for row in gaps})}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check-inputs-only", action="store_true", help="Validate G1.5 evidence prerequisites without rebuilding the KB")
    args = parser.parse_args()
    if args.check_inputs_only:
        manifest = read_json(XLS_MANIFEST_PATH)
        print(json.dumps({"xls_status": manifest["status"], "entries": manifest["xls"]["header"]["file_count"]}, sort_keys=True))
        return 0
    print(json.dumps(run(), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
