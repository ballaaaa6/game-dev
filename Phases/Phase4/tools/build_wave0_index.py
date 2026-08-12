#!/usr/bin/env python3
"""Build the Wave 0 evidence and translation index.

This tool does not translate gameplay or mutate extraction roots.  It creates a
machine-readable index for the small office-runtime slice that will be
translated in later waves:

* dump.cs class fields, offsets and method signatures
* script.json method/RVA matches
* categorized C definitions and call evidence
* assembly fallback call targets
* string-literal values and references
* translation coverage for direct, sliced and contract-only units

All generated files are written below ``Phases/Phase4/artifacts``.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[3]
PHASE = ROOT / "Phases" / "Phase4"
ARTIFACTS = PHASE / "artifacts"
DUMP = ROOT / "game-dev-story-mod_Dumped"
CODE = DUMP / "Categorized_Code"
DUMP_CS = DUMP / "dump.cs"
SCRIPT_JSON = DUMP / "script.json"
STRINGLITERAL_JSON = DUMP / "stringliteral.json"
FAILED_REPORT = DUMP / "Failed_Functions_Assembly" / "failed_functions.asm.report.json"
ASM_DIR = DUMP / "Failed_Functions_Assembly"


CLASS_SPECS: dict[tuple[str, str], str] = {
    ("main", "AppData"): "main_AppData",
    ("form", "GameForm"): "form_GameForm",
    ("kairo.unity.util", "Language"): "kairo_unity_util_Language",
    ("kairo.unity.util", "JarInflater"): "kairo_unity_util_JarInflater",
    ("kairo.unity.ui", "ResourceManager"): "kairo_unity_ui_ResourceManager",
    ("kairo.unity.ui", "Seb"): "kairo_unity_ui_Seb",
    ("kairo.unity.ui", "Graphics"): "kairo_unity_ui_Graphics",
    ("kairo.unity.ui", "Image"): "kairo_unity_ui_Image",
    ("kairo.unity.ui", "TextFormat"): "kairo_unity_ui_TextFormat",
    ("kairo.unity.ui", "TextLayout"): "kairo_unity_ui_TextLayout",
    ("kairo.unity.graphics", "Offscreen"): "kairo_unity_graphics_Offscreen",
    ("surface", "GameView"): "surface_GameView",
}


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8", errors="replace").splitlines()


def parse_hex(value: str | None) -> int | None:
    if not value:
        return None
    match = re.search(r"0x([0-9a-fA-F]+)", value)
    return int(match.group(1), 16) if match else None


def method_symbol(prefix: str, method_name: str) -> str:
    """Convert a dump method name to the IL2CPP C symbol convention."""

    if method_name == ".ctor":
        return prefix + "___ctor"
    if method_name == ".cctor":
        return prefix + "___cctor"
    return prefix + "_" + method_name if method_name.startswith("_") else prefix + "__" + method_name


CLASS_HEADER = re.compile(
    r"^(?:public|private|internal|protected)\s+"
    r"(?:(?:sealed|abstract|static)\s+)*"
    r"(?:class|struct|enum)\s+(?P<name>[^\s:]+).*// TypeDefIndex:\s*(?P<index>\d+)"
)
FIELD_LINE = re.compile(r"^\t(?!\t)(?P<decl>.+?);(?:\s*//\s*(?P<comment>.*))?$")
METHOD_LINE = re.compile(r"^\t(?!\t)(?P<decl>.+?\s+\{\s*\})$")
RVA_LINE = re.compile(r"// RVA:\s*(0x[0-9a-fA-F]+)")


def class_blocks(lines: list[str]) -> list[dict[str, Any]]:
    """Parse top-level dump classes with line ranges and namespace context."""

    blocks: list[dict[str, Any]] = []
    namespace: str | None = None
    index = 0
    while index < len(lines):
        namespace_match = re.match(r"^// Namespace:\s*(.*)$", lines[index])
        if namespace_match:
            namespace = namespace_match.group(1).strip() or None
        match = CLASS_HEADER.match(lines[index])
        if not match:
            index += 1
            continue
        depth = 0
        opened = False
        end = index
        while end < len(lines):
            line = lines[end]
            depth += line.count("{") - line.count("}")
            if "{" in line:
                opened = True
            if opened and depth == 0:
                break
            end += 1
        blocks.append(
            {
                "namespace": namespace,
                "name": match.group("name"),
                "typedef_index": int(match.group("index")),
                "line_start": index + 1,
                "line_end": min(end + 1, len(lines)),
            }
        )
        index = max(end + 1, index + 1)
    return blocks


def modifiers_and_decl(declaration: str) -> tuple[list[str], str]:
    tokens = declaration.split()
    modifiers: list[str] = []
    while tokens and tokens[0] in {
        "public",
        "private",
        "protected",
        "internal",
        "static",
        "readonly",
        "const",
        "volatile",
        "abstract",
        "sealed",
        "virtual",
        "override",
        "extern",
    }:
        modifiers.append(tokens.pop(0))
    return modifiers, " ".join(tokens)


def parse_field(line: str, line_number: int, source: str) -> dict[str, Any] | None:
    match = FIELD_LINE.match(line)
    if not match or "(" in match.group("decl"):
        return None
    declaration = match.group("decl").strip()
    modifiers, rest = modifiers_and_decl(declaration)
    if not rest:
        return None
    name_and_value = rest.rsplit(" ", 1)
    if len(name_and_value) != 2:
        return None
    type_name, name_value = name_and_value
    value: str | None = None
    if "=" in name_value:
        name, value = [part.strip() for part in name_value.split("=", 1)]
    else:
        name = name_value
    comment = (match.group("comment") or "").strip()
    offset = parse_hex(comment)
    return {
        "name": name,
        "type": type_name,
        "modifiers": modifiers,
        "offset": f"0x{offset:X}" if offset is not None else None,
        "offset_int": offset,
        "const_value": value,
        "line": line_number,
        "source": source,
    }


def parse_method(line: str, line_number: int, lines: list[str], start: int, source: str, prefix: str) -> dict[str, Any] | None:
    match = METHOD_LINE.match(line)
    if not match:
        return None
    declaration = match.group("decl").strip()
    if "(" not in declaration:
        return None
    signature = declaration[:-3].rstrip()
    method_name = signature.split("(", 1)[0].split()[-1]
    rva: int | None = None
    for previous in range(max(start, line_number - 5), line_number):
        rva_match = RVA_LINE.search(lines[previous - 1])
        if rva_match:
            rva = int(rva_match.group(1), 16)
    return {
        "name": method_name,
        "c_symbol": method_symbol(prefix, method_name),
        "signature": signature,
        "rva": f"0x{rva:X}" if rva is not None else None,
        "rva_int": rva,
        "line": line_number,
        "source": source,
    }


def parse_selected_classes(lines: list[str]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    blocks = class_blocks(lines)
    selected: list[dict[str, Any]] = []
    fields: list[dict[str, Any]] = []
    methods: list[dict[str, Any]] = []
    wanted = set(CLASS_SPECS)
    for block in blocks:
        key = (block["namespace"], block["name"])
        if key not in wanted:
            continue
        prefix = CLASS_SPECS[key]
        source = "game-dev-story-mod_Dumped/dump.cs"
        block_fields: list[dict[str, Any]] = []
        block_methods: list[dict[str, Any]] = []
        for line_number in range(block["line_start"], block["line_end"] + 1):
            line = lines[line_number - 1]
            field = parse_field(line, line_number, source)
            if field:
                block_fields.append(field)
            method = parse_method(line, line_number, lines, block["line_start"], source, prefix)
            if method:
                block_methods.append(method)
        selected.append({**block, "c_prefix": prefix, "field_count": len(block_fields), "method_count": len(block_methods)})
        for field in block_fields:
            fields.append({**block, "declaring_class": block["name"], **field})
        for method in block_methods:
            methods.append({**block, **method})
    return selected, fields, methods


FUNCTION_HEADER = re.compile(r"^// Function:\s*([A-Za-z_][A-Za-z0-9_]*)\s*$")
C_ADDRESS = re.compile(r"^// Address:\s*(0x[0-9a-fA-F]+|[0-9a-fA-F]+)\s*$")
CALL_SYMBOL = re.compile(
    r"\b((?:form|main|kairo|surface)_[A-Za-z0-9_]+)\s*\("
)


def parse_c_definitions() -> tuple[dict[str, list[dict[str, Any]]], list[dict[str, Any]]]:
    by_symbol: dict[str, list[dict[str, Any]]] = defaultdict(list)
    all_segments: list[dict[str, Any]] = []
    for path in sorted(CODE.rglob("*.c")):
        lines = read_lines(path)
        headers = [(index, match.group(1)) for index, line in enumerate(lines) if (match := FUNCTION_HEADER.match(line))]
        for header_index, (start_index, symbol) in enumerate(headers):
            end_index = headers[header_index + 1][0] - 1 if header_index + 1 < len(headers) else len(lines) - 1
            address: int | None = None
            for probe in range(start_index + 1, min(start_index + 6, len(lines))):
                address_match = C_ADDRESS.match(lines[probe])
                if address_match:
                    address = int(address_match.group(1), 16)
                    break
            body = "\n".join(lines[start_index : end_index + 1])
            calls = Counter(CALL_SYMBOL.findall(body))
            calls.pop(symbol, None)
            definition = {
                "symbol": symbol,
                "source": rel(path),
                "line_start": start_index + 1,
                "line_end": end_index + 1,
                "line_count": end_index - start_index + 1,
                "address": f"0x{address:X}" if address is not None else None,
                "address_int": address,
                "calls": [{"symbol": target, "count": count} for target, count in sorted(calls.items())],
            }
            by_symbol[symbol].append(definition)
            all_segments.append(definition)
    return dict(by_symbol), all_segments


def load_script_methods() -> tuple[dict[str, list[dict[str, Any]]], dict[int, str]]:
    raw = json.loads(SCRIPT_JSON.read_text(encoding="utf-8"))
    by_symbol: dict[str, list[dict[str, Any]]] = defaultdict(list)
    by_runtime_address: dict[int, str] = {}
    signature_pattern = re.compile(r"\b([A-Za-z_][A-Za-z0-9_]*)\s*\(")
    for row in raw.get("ScriptMethod", []):
        signature = row.get("Signature", "")
        matches = signature_pattern.findall(signature)
        if not matches:
            continue
        symbol = matches[-1]
        address = int(row["Address"])
        item = {
            "address": address,
            "address_hex": f"0x{address:X}",
            "decompiler_address": f"0x{address + 0x100000:X}",
            "name": row.get("Name"),
            "signature": signature,
            "type_signature": row.get("TypeSignature"),
        }
        by_symbol[symbol].append(item)
        by_runtime_address[address + 0x100000] = symbol
    return dict(by_symbol), by_runtime_address


def load_failed_functions() -> dict[str, dict[str, Any]]:
    if not FAILED_REPORT.exists():
        return {}
    report = json.loads(FAILED_REPORT.read_text(encoding="utf-8"))
    result: dict[str, dict[str, Any]] = {}
    for row in report.get("functions", []):
        raw_file = str(row.get("file", ""))
        file_path = Path(raw_file)
        # The report stores absolute paths from the extraction machine.  Keep
        # the portable filename here; assembly lookup is rooted at the frozen
        # local Failed_Functions_Assembly directory.
        file_name = file_path.name or raw_file
        result[row["name"]] = {
            "address": row.get("address"),
            "file": rel(file_path) if file_path.exists() and file_path.is_relative_to(ROOT) else file_name,
            "instructions": row.get("instructions"),
            "status": row.get("status"),
        }
    return result


def parse_assembly_targets(failed: dict[str, dict[str, Any]], runtime_address_map: dict[int, str]) -> dict[str, Any]:
    output: dict[str, Any] = {}
    for symbol, meta in failed.items():
        file_name = Path(meta["file"]).name
        path = ASM_DIR / file_name
        if not path.exists():
            continue
        targets = Counter()
        for line in read_lines(path):
            match = re.search(r"\bbl\s*;\s*(0x[0-9a-fA-F]+)", line)
            if match:
                targets[int(match.group(1), 16)] += 1
        resolved: list[dict[str, Any]] = []
        for address, count in sorted(targets.items()):
            resolved.append(
                {
                    "address": f"0x{address:X}",
                    "count": count,
                    "symbol": runtime_address_map.get(address),
                    "resolution": "script_method" if address in runtime_address_map else "unresolved",
                }
            )
        output[symbol] = {
            "source": rel(path),
            "instruction_count": meta.get("instructions"),
            "branch_target_count": sum(targets.values()),
            "targets": resolved,
        }
    return output


def load_string_literals() -> tuple[list[dict[str, Any]], dict[int, dict[str, Any]]]:
    raw = json.loads(STRINGLITERAL_JSON.read_text(encoding="utf-8"))
    entries: list[dict[str, Any]] = []
    by_id: dict[int, dict[str, Any]] = {}
    for literal_id, row in enumerate(raw):
        value = row.get("value", "")
        item = {
            "literal_id": literal_id,
            "address": row.get("address"),
            "value": value,
            "utf8_length": len(value.encode("utf-8")),
            "has_newline": "\n" in value or "\r" in value,
            "placeholder_tokens": sorted(set(re.findall(r"<\d+>", value))),
        }
        entries.append(item)
        by_id[literal_id] = item
    return entries, by_id


def literal_references(all_segments: Iterable[dict[str, Any]], literal_by_id: dict[int, dict[str, Any]]) -> dict[str, Any]:
    references: dict[int, list[dict[str, Any]]] = defaultdict(list)
    line_cache: dict[str, list[str]] = {}
    for segment in all_segments:
        source = segment["source"]
        if source not in line_cache:
            line_cache[source] = read_lines(ROOT / source)
        lines = line_cache[source]
        for line_number, line in enumerate(lines[segment["line_start"] - 1 : segment["line_end"]], start=segment["line_start"]):
            for match in re.finditer(r"StringLiteral_(\d+)", line):
                literal_id = int(match.group(1))
                if len(references[literal_id]) < 12:
                    references[literal_id].append(
                        {"source": segment["source"], "line": line_number, "function": segment["symbol"]}
                    )
    summary = []
    for literal_id in sorted(references):
        summary.append(
            {
                "literal_id": literal_id,
                "known_in_table": literal_id in literal_by_id,
                "reference_count_sampled": len(references[literal_id]),
                "references": references[literal_id],
            }
        )
    out_of_range = sorted(set(references) - set(literal_by_id))
    # The extracted C names include a terminal ``StringLiteral_<count>``
    # pointer, while stringliteral.json is zero-based (0..count-1). Preserve
    # this as explicit evidence rather than treating it as a missing value.
    terminal_sentinel_ids = [literal_id for literal_id in out_of_range if literal_id == len(literal_by_id)]
    return {
        "reference_basis": "StringLiteral_<index> labels in categorized C",
        "sample_limit_per_literal": 12,
        "referenced_literals": summary,
        "referenced_count": len(summary),
        "missing_from_table": [literal_id for literal_id in out_of_range if literal_id not in terminal_sentinel_ids],
        "out_of_range_references": out_of_range,
        "terminal_sentinel_ids": terminal_sentinel_ids,
    }


def shortlist() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(category: str, priority: str, action: str, symbols: Iterable[str], reason: str) -> None:
        for symbol in symbols:
            rows.append(
                {
                    "symbol": symbol,
                    "category": category,
                    "priority": priority,
                    "action": action,
                    "reason": reason,
                }
            )

    add(
        "foundation",
        "P0",
        "translate",
        [
            "form_GameForm___cctor",
            "form_GameForm__NewGamePara",
            "main_AppData__Init",
            "main_AppData__GetInstance",
            "main_AppData__GetImage",
            "main_AppData__GetTalkTexts",
        ],
        "Restore named fields, initial tables and source/resource lookup before translating dependent paths.",
    )
    add(
        "resource",
        "P0",
        "translate",
        [
            "kairo_unity_util_JarInflater__GetInputStream",
            "kairo_unity_util_JarInflater__GetData",
            "kairo_unity_util_JarInflater__GetFiles",
            "kairo_unity_util_JarInflater__ConvertExtension",
            "kairo_unity_ui_ResourceManager__LoadImage",
            "kairo_unity_ui_ResourceManager__LoadSeb",
            "kairo_unity_ui_ResourceManager__Load",
            "kairo_unity_ui_ResourceManager__LoadReady",
            "kairo_unity_ui_ResourceManager__LoadStart",
            "kairo_unity_ui_ResourceManager__GetImage",
            "kairo_unity_ui_Seb___load",
            "kairo_unity_ui_Seb__GetSprites",
            "kairo_unity_ui_Seb__GetDepthInfo",
            "kairo_unity_ui_Seb__Draw",
            "kairo_unity_ui_Seb__DrawFrame",
            "form_GameForm__LoadBihinImage",
            "form_GameForm__EventGChange",
        ],
        "Resolve resource order, image/SEB loading and the selector-to-file contract.",
    )
    add(
        "render",
        "P0",
        "translate",
        [
            "form_GameForm__Init",
            "form_GameForm__GameScreenLayout",
            "form_GameForm__RenderGameScreen",
            "form_GameForm__Update",
            "form_GameForm___update",
            "form_GameForm__Draw",
            "form_GameForm___draw",
            "form_GameForm__SmartBeginPaint",
            "form_GameForm__SetScale",
            "form_GameForm__GetGameWidth",
            "form_GameForm__GetGameHeight",
            "surface_GameView__GetGameWidth",
            "surface_GameView__GetGameHeight",
        ],
        "Translate only the frame, coordinate, camera and draw orchestration used by the office view.",
    )
    add(
        "scene",
        "P0",
        "translate",
        [
            "form_GameForm__CallHikkosi",
            "form_GameForm__AddObjec",
            "form_GameForm__AddTarget",
            "form_GameForm__CallPCChange",
            "form_GameForm__CallDeskChange",
            "form_GameForm__CallChairChange",
            "form_GameForm__GetPcImgData",
            "form_GameForm__GetDeskImgData",
            "form_GameForm__GetChairImgData",
            "form_GameForm__DrawObj",
            "form_GameForm__DrawFloorCover",
            "form_GameForm__DrawDesk",
            "form_GameForm__DrawCeoDesk",
            "form_GameForm__DrawDisplay",
            "form_GameForm__DrawChair",
            "form_GameForm__DrawReception",
        ],
        "Restore room/object records, furniture relations, coordinate placement and draw order.",
    )
    add(
        "actor",
        "P0",
        "translate",
        [
            "form_GameForm__AddBodyFace",
            "form_GameForm__DrawHuman",
            "form_GameForm__AddSyain",
            "form_GameForm__CallSyain",
            "form_GameForm__NextTarget",
            "form_GameForm__NextPoint",
            "form_GameForm__Atan2",
            "form_GameForm__Distan",
        ],
        "Restore character composition, employee binding, movement and neutral animation selectors.",
    )
    add(
        "dialogue_language",
        "P1",
        "translate",
        [
            "form_GameForm__AddFuki",
            "form_GameForm__CallFuki",
            "form_GameForm__DrawFukidashi",
            "form_GameForm__AddKaiwaTalkData",
            "form_GameForm__GetTalkIndex",
            "form_GameForm__GetHumanTalkName",
            "form_GameForm__AddKaiwa",
            "form_GameForm__ResetTextLayout",
            "kairo_unity_util_Language__SetTextTable",
            "kairo_unity_util_Language__MakeTextTable",
            "kairo_unity_util_Language__TranslateText",
            "kairo_unity_util_Language___translateText",
            "kairo_unity_util_Language___translateText2",
            "kairo_unity_util_Language__LT",
        ],
        "Connect talk tags, language entries, placeholders and bubble layout for office messages.",
    )
    add(
        "lifecycle",
        "P1",
        "slice",
        [
            "form_GameForm__MainProcess",
            "form_GameForm__AddEvent",
            "form_GameForm__DoEvent",
            "form_GameForm__ProcessEvent",
            "form_GameForm__AddMessage",
        ],
        "Translate only branches that mutate actor, dialogue, bubble, office object or Agent-facing lifecycle state.",
    )
    add(
        "render_contract",
        "P1",
        "contract_only",
        [
            "kairo_unity_ui_Graphics__DrawImage",
            "kairo_unity_ui_Graphics__SetOrigin",
            "kairo_unity_ui_Graphics__Scale",
            "kairo_unity_ui_Image__GetWidth",
            "kairo_unity_ui_Image__GetHeight",
            "kairo_unity_graphics_Offscreen__CreateOffscreen",
            "kairo_unity_ui_TextLayout__SetText",
            "kairo_unity_ui_TextLayout__Draw",
            "kairo_unity_ui_TextLayout__Replace",
        ],
        "Capture caller-visible behavior without porting generic framework internals.",
    )
    return rows


def source_status(c_definitions: dict[str, list[dict[str, Any]]], script_methods: dict[str, list[dict[str, Any]]], failed: dict[str, dict[str, Any]]) -> str:
    if c_definitions.get("symbol"):
        return "categorized_c"
    if failed.get("symbol"):
        return "assembly_fallback_only"
    if script_methods.get("symbol"):
        return "dump_or_script_only"
    return "unresolved"


def build_function_inventory(
    selected_classes: list[dict[str, Any]],
    dump_methods: list[dict[str, Any]],
    c_definitions: dict[str, list[dict[str, Any]]],
    script_methods: dict[str, list[dict[str, Any]]],
    failed: dict[str, dict[str, Any]],
    assembly_targets: dict[str, Any],
) -> dict[str, Any]:
    short = shortlist()
    by_symbol: dict[str, dict[str, Any]] = {}
    for row in short:
        symbol = row["symbol"]
        dump_rows = [item for item in dump_methods if item["c_symbol"] == symbol]
        c_rows = c_definitions.get(symbol, [])
        script_rows = script_methods.get(symbol, [])
        script_addresses = {item["address"] + 0x100000 for item in script_rows}
        c_rows_with_match = []
        for definition in c_rows:
            c_rows_with_match.append(
                {
                    **definition,
                    "address_matches_script": definition.get("address_int") in script_addresses if definition.get("address_int") is not None else None,
                }
            )
        failed_row = failed.get(symbol)
        item = {
            **row,
            "source_status": (
                "categorized_c"
                if c_rows
                else "assembly_fallback_only"
                if failed_row
                else "dump_or_script_only"
                if dump_rows or script_rows
                else "unresolved"
            ),
            "dump_method_count": len(dump_rows),
            "dump_methods": dump_rows,
            "script_method_count": len(script_rows),
            "script_methods": script_rows,
            "c_definition_count": len(c_rows_with_match),
            "c_definitions": c_rows_with_match,
            "assembly_fallback": failed_row,
            "assembly_call_targets": assembly_targets.get(symbol),
        }
        by_symbol[symbol] = item
    return {
        "schema": "phase4.wave0.function-inventory.v1",
        "generated_at_utc": now_utc(),
        "source_policy": "Frozen dump/source roots are read-only; shortlist is office-runtime scope only.",
        "selected_classes": selected_classes,
        "shortlist": list(by_symbol.values()),
        "dump_methods_selected_classes": dump_methods,
        "summary": {
            "shortlist_count": len(by_symbol),
            "categorized_c": sum(item["source_status"] == "categorized_c" for item in by_symbol.values()),
            "assembly_fallback_only": sum(item["source_status"] == "assembly_fallback_only" for item in by_symbol.values()),
            "dump_or_script_only": sum(item["source_status"] == "dump_or_script_only" for item in by_symbol.values()),
            "unresolved": sum(item["source_status"] == "unresolved" for item in by_symbol.values()),
        },
        "source_files": {
            "dump": rel(DUMP_CS),
            "script": rel(SCRIPT_JSON),
            "categorized_code": rel(CODE),
            "failed_report": rel(FAILED_REPORT),
        },
    }


def build_call_graph(shortlist_rows: list[dict[str, Any]], c_definitions: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    selected_symbols = {row["symbol"] for row in shortlist_rows}
    node_symbols = set(selected_symbols)
    edges: Counter[tuple[str, str]] = Counter()
    evidence: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for caller in sorted(selected_symbols):
        for definition in c_definitions.get(caller, []):
            for call in definition["calls"]:
                callee = call["symbol"]
                node_symbols.add(callee)
                edge = (caller, callee)
                edges[edge] += call["count"]
                if len(evidence[edge]) < 6:
                    evidence[edge].append({"source": definition["source"], "line": definition["line_start"]})
    nodes = []
    for symbol in sorted(node_symbols):
        nodes.append(
            {
                "symbol": symbol,
                "selected": symbol in selected_symbols,
                "has_c_definition": bool(c_definitions.get(symbol)),
                "definition_count": len(c_definitions.get(symbol, [])),
            }
        )
    edge_rows = []
    for (caller, callee), count in sorted(edges.items()):
        edge_rows.append({"caller": caller, "callee": callee, "count": count, "evidence": evidence[(caller, callee)]})
    unresolved = [node["symbol"] for node in nodes if not node["has_c_definition"]]
    return {
        "schema": "phase4.wave0.office-runtime-call-graph.v1",
        "generated_at_utc": now_utc(),
        "scope": "Shortlist callers and relevant IL2CPP symbols in categorized C.",
        "nodes": nodes,
        "edges": edge_rows,
        "unresolved_or_external_nodes": unresolved,
        "summary": {"nodes": len(nodes), "edges": len(edge_rows), "unresolved_nodes": len(unresolved)},
    }


def build_coverage(function_inventory: dict[str, Any]) -> dict[str, Any]:
    rows = []
    for item in function_inventory["shortlist"]:
        rows.append(
            {
                "symbol": item["symbol"],
                "category": item["category"],
                "priority": item["priority"],
                "action": item["action"],
                "source_status": item["source_status"],
                "dump_method_count": item["dump_method_count"],
                "script_method_count": item["script_method_count"],
                "c_definition_count": item["c_definition_count"],
                "assembly_instruction_count": (item.get("assembly_fallback") or {}).get("instructions"),
                "evidence_ready": item["source_status"] in {"categorized_c", "assembly_fallback_only"},
                "next_action": (
                    "slice_and_translate"
                    if item["action"] == "slice"
                    else "write_contract"
                    if item["action"] == "contract_only"
                    else "translate_with_evidence"
                ),
            }
        )
    statuses = Counter(item["source_status"] for item in rows)
    actions = Counter(item["action"] for item in rows)
    return {
        "schema": "phase4.wave0.translation-coverage.v1",
        "generated_at_utc": now_utc(),
        "status_policy": {
            "categorized_c": "Recovered categorized C exists; still requires named field/branch translation.",
            "assembly_fallback_only": "C decompile failed; assembly branch index is evidence, not a translated implementation.",
            "dump_or_script_only": "Signature exists but source implementation was not found in current categorized roots.",
            "unresolved": "No current signature/source evidence; must be resolved or explicitly scoped out.",
        },
        "units": rows,
        "summary": {
            "unit_count": len(rows),
            "by_source_status": dict(sorted(statuses.items())),
            "by_action": dict(sorted(actions.items())),
            "evidence_ready_units": sum(item["evidence_ready"] for item in rows),
        },
    }


def build_field_map(selected_classes: list[dict[str, Any]], fields: list[dict[str, Any]]) -> dict[str, Any]:
    by_class: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for field in fields:
        clean = {key: value for key, value in field.items() if key not in {"line_start", "line_end", "typedef_index", "field_count", "method_count"}}
        by_class[f"{field['namespace']}.{field['declaring_class']}"].append(clean)
    return {
        "schema": "phase4.wave0.field-offset-map.v1",
        "generated_at_utc": now_utc(),
        "source": rel(DUMP_CS),
        "offset_basis": "dump.cs field comments; static and instance offsets are retained as reported.",
        "classes": selected_classes,
        "fields_by_class": dict(sorted(by_class.items())),
        "summary": {
            "selected_class_count": len(selected_classes),
            "field_count": len(fields),
            "fields_with_offsets": sum(field["offset_int"] is not None for field in fields),
            "fields_without_offsets": sum(field["offset_int"] is None for field in fields),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ARTIFACTS, help="Output artifact directory")
    args = parser.parse_args()
    output = args.output if args.output.is_absolute() else ROOT / args.output
    output.mkdir(parents=True, exist_ok=True)

    dump_lines = read_lines(DUMP_CS)
    selected_classes, fields, dump_methods = parse_selected_classes(dump_lines)
    c_definitions, c_segments = parse_c_definitions()
    script_methods, runtime_address_map = load_script_methods()
    failed = load_failed_functions()
    assembly_targets = parse_assembly_targets(failed, runtime_address_map)
    literals, literal_by_id = load_string_literals()
    references = literal_references(c_segments, literal_by_id)

    function_inventory = build_function_inventory(
        selected_classes,
        dump_methods,
        c_definitions,
        script_methods,
        failed,
        assembly_targets,
    )
    coverage = build_coverage(function_inventory)
    graph = build_call_graph(function_inventory["shortlist"], c_definitions)
    field_map = build_field_map(selected_classes, fields)

    string_map = {
        "schema": "phase4.wave0.string-literal-map.v1",
        "generated_at_utc": now_utc(),
        "source": rel(STRINGLITERAL_JSON),
        "mapping_basis": "literal_id is the zero-based index in stringliteral.json; C labels are cross-referenced separately.",
        "mapping_confidence": "probable",
        "literal_count": len(literals),
        "entries": literals,
        "references": references,
    }

    source_manifest = {
        rel(path): {"bytes": path.stat().st_size, "sha256": sha256(path)}
        for path in [DUMP_CS, SCRIPT_JSON, STRINGLITERAL_JSON, FAILED_REPORT]
        if path.exists()
    }
    metadata = {
        "schema": "phase4.wave0.index-build.v1",
        "generated_at_utc": now_utc(),
        "source_manifest": source_manifest,
        "artifacts": [
            "field_offset_map.json",
            "function_inventory.json",
            "string_literal_map.json",
            "office_runtime_call_graph.json",
            "translation_coverage.json",
        ],
    }

    write_json(output / "field_offset_map.json", field_map)
    write_json(output / "function_inventory.json", function_inventory)
    write_json(output / "string_literal_map.json", string_map)
    write_json(output / "office_runtime_call_graph.json", graph)
    write_json(output / "translation_coverage.json", coverage)
    write_json(output / "wave0_build_manifest.json", metadata)
    print(json.dumps({"output": rel(output), "artifacts": metadata["artifacts"], "coverage": coverage["summary"]}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
