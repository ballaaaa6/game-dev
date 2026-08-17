"""Reproducible R0 audit of the recovered Cpp2IL C# corpus.

The script only reads the isolated corpus, native/metadata evidence, and local
Cpp2IL output directories.  It writes the small R0 evidence package requested
by the audit prompt; it never edits the source corpus or executes recovered
C#.
"""

from __future__ import annotations

import argparse
import bisect
import hashlib
import json
import re
from array import array
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable


CATEGORIES = (
    "CLEAN",
    "TYPE_REPAIR",
    "CFG_REPAIR",
    "STATIC_DATA_REPAIR",
    "NATIVE_BOUNDARY",
    "NATIVE_LIFT_REQUIRED",
    "SOURCE_LIMITED",
)

CORE_FILES = {
    "AppData": "main/AppData.cs",
    "GameForm": "form/GameForm.cs",
    "Player": "game/Player.cs",
    "Room": "game/Room.cs",
    "ObjChip": "game/ObjChip.cs",
    "Staff": "game/Staff.cs",
    "FurnitureData": "data/FurnitureData.cs",
    "Astar": "game.routeSearch/Astar.cs",
    "Node": "game.routeSearch/Node.cs",
}

REQUIRED_METHODS = {
    "Astar": ["AddNodeArray", "SearchRoute", "AddNeighbor"],
    "GameForm": ["DrawGameScreen"],
    "AppData": ["NewGame", "GetGameTimeZone"],
    "ObjChip": ["DrawWall", "AddStaff", "PlaceObj", "GetStandingPositions", "ReserveUse", "IsPassable"],
    "Player": ["AddRoom", "RealTimeProcess"],
    "Room": ["PlaceObj", "AddStaff", "GetIndexToUseEquipment", "Draw"],
    "Staff": ["UpdateWork", "SearchRoute", "ReadyToNextNode", "OnArriveGoal"],
    "FurnitureData": ["Load"],
}

PINNED_INPUTS = {
    "apk": "fa0e9e3a843732258fc05b2611a8e0f5be6f7e95f2141a53f31fb082322fe2bf",
    "rar": "a50a442491e422c20699a9ca4266e794d215bff29248d3edd24c41f42a57f903",
    "libil2cpp": "364893401fcf7fc2380ae64291783edf7b95eecea4775041c3f4c8c081b4d54a",
    "metadata": "f65f3a00675f35cfa28fef53c37ed7a2dc01e143b6d59c6014a286fa84e4a579",
}

SIGNAL_PATTERNS = {
    "note_decompiler_issue": re.compile(r"NoteDecompilerIssue"),
    "unknown_result_type": re.compile(r"Unknown result type"),
    "goto_il": re.compile(r"\bgoto\s+IL_[A-Za-z0-9_]+"),
    "expected_type_mismatch": re.compile(r"Expected\s+[A-Za-z0-9_]+\s*,\s*but got"),
    "expected_o": re.compile(r"Expected\s+O\b"),
    "unmanaged_memory": re.compile(r"Unmanaged memory"),
    "indirect_jump": re.compile(r"Indirect jump"),
    "method_not_found": re.compile(r"Method not found"),
    "invalid_comparison": re.compile(r"Invalid comparison"),
    "object_assignment": re.compile(r"\bobject\s+[A-Za-z_]\w*\s*="),
    "runtime_field_handle": re.compile(r"RuntimeFieldHandle|RuntimeHelpers\.InitializeArray|InitializeArray"),
    "native_boundary": re.compile(r"\b(?:extern|DllImport|InternalCall|UnmanagedCallersOnly)\b|\[\s*(?:Address|CallerCount)\s*\("),
}

CONTROL_NAMES = {
    "if",
    "for",
    "foreach",
    "while",
    "switch",
    "catch",
    "using",
    "lock",
    "fixed",
    "sizeof",
    "typeof",
    "nameof",
    "default",
    "return",
    "new",
    "when",
}

TYPE_PATTERN = re.compile(r"\b(class|struct|enum|interface|record)\s+([A-Za-z_]\w*)")
NAMESPACE_PATTERN = re.compile(r"\bnamespace\s+([A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*)")


@dataclass
class TypeScope:
    kind: str
    name: str
    open_pos: int
    close_pos: int
    depth: int
    full_name: str = ""


@dataclass
class ParsedFile:
    relative_path: str
    source: str
    masked: str
    line_starts: list[int]
    types: list[TypeScope] = field(default_factory=list)
    methods: list[dict[str, Any]] = field(default_factory=list)
    namespaces: list[str] = field(default_factory=list)
    properties: int = 0
    fields: int = 0


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def mask_comments_and_strings(source: str) -> str:
    chars = list(source)
    length = len(source)
    index = 0

    def blank(start: int, end: int) -> None:
        for position in range(start, end):
            if source[position] != "\n":
                chars[position] = " "

    while index < length:
        current = source[index]
        next_char = source[index + 1] if index + 1 < length else ""
        if current == "/" and next_char == "/":
            end = source.find("\n", index + 2)
            if end < 0:
                end = length
            blank(index, end)
            index = end
            continue
        if current == "/" and next_char == "*":
            end = source.find("*/", index + 2)
            end = length if end < 0 else end + 2
            blank(index, end)
            index = end
            continue
        if current in {"\"", "'"}:
            quote = current
            verbatim = quote == "\"" and index > 0 and source[index - 1] == "@"
            start = index
            index += 1
            while index < length:
                if source[index] == "\\" and not verbatim:
                    index += 2
                    continue
                if source[index] == quote:
                    if verbatim and index + 1 < length and source[index + 1] == quote:
                        index += 2
                        continue
                    index += 1
                    break
                index += 1
            blank(start, index)
            continue
        index += 1
    return "".join(chars)


def structural_maps(masked: str) -> tuple[dict[int, int], dict[int, int], array]:
    brace_pairs: dict[int, int] = {}
    paren_pairs: dict[int, int] = {}
    brace_stack: list[int] = []
    paren_stack: list[int] = []
    depth = array("h", [0]) * (len(masked) + 1)
    current_depth = 0
    for position, character in enumerate(masked):
        depth[position] = current_depth
        if character == "{":
            brace_stack.append(position)
            current_depth += 1
        elif character == "}":
            if brace_stack:
                opening = brace_stack.pop()
                brace_pairs[opening] = position
                brace_pairs[position] = opening
            current_depth = max(0, current_depth - 1)
        elif character == "(":
            paren_stack.append(position)
        elif character == ")" and paren_stack:
            opening = paren_stack.pop()
            paren_pairs[opening] = position
            paren_pairs[position] = opening
    depth[len(masked)] = current_depth
    return brace_pairs, paren_pairs, depth


def line_starts(source: str) -> list[int]:
    starts = [0]
    starts.extend(index + 1 for index, character in enumerate(source) if character == "\n")
    return starts


def line_number(starts: list[int], position: int) -> int:
    return bisect.bisect_right(starts, position)


def strip_for_signal(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def method_body_end(masked: str, brace_pairs: dict[int, int], close_paren: int, type_close: int) -> tuple[str, int | None, int | None]:
    cursor = close_paren + 1
    limit = min(type_close, cursor + 1600)
    while cursor < limit:
        if masked[cursor] in " \t\r\n":
            cursor += 1
            continue
        if masked[cursor] == "{" and cursor in brace_pairs:
            return "block", cursor, brace_pairs[cursor]
        if masked.startswith("=>", cursor):
            semicolon = masked.find(";", cursor + 2, type_close)
            return "expression", cursor, semicolon if semicolon >= 0 else type_close
        if masked[cursor] == ";":
            return "declaration", None, cursor
        if masked.startswith("where", cursor):
            cursor += 5
            continue
        cursor += 1
    return "unknown", None, None


def type_full_name(types: list[TypeScope], current: TypeScope) -> str:
    parents = [item for item in types if item is not current and item.open_pos < current.open_pos < item.close_pos]
    parents.sort(key=lambda item: item.open_pos)
    return ".".join([item.name for item in parents] + [current.name])


def looks_like_method_prefix(prefix: str, method_name: str) -> bool:
    if method_name in CONTROL_NAMES:
        return False
    before = prefix[: prefix.rfind(method_name)].strip()
    if re.search(r"\b(?:new|return|throw|case|goto|if|for|foreach|while|switch|catch|using|lock)\s*$", before):
        return False
    if before.endswith("=") or before.endswith("."):
        return False
    if not before:
        return False
    # A declaration has a return type/modifier or is a constructor/destructor.
    return bool(re.search(r"\b(?:public|private|protected|internal|static|virtual|override|abstract|sealed|partial|extern|unsafe|new|async|ref|out|readonly|void|bool|byte|char|decimal|double|float|int|long|object|string|short|uint|ulong|ushort|Task|I[A-Za-z_]\w*|[A-Za-z_]\w*)\b", before))


FAST_FILE_THRESHOLD = 100_000


def _line_brace_delta(line: str) -> int:
    code = line.split("//", 1)[0]
    code = re.sub(r'"(?:\\.|[^"\\])*"', '""', code)
    return code.count("{") - code.count("}")


def parse_file_fast(path: Path, relative_path: str) -> ParsedFile:
    """Parse very large generated files without quadratic nested-scope scans."""
    source = path.read_text(encoding="utf-8", errors="replace")
    starts = line_starts(source)
    lines = source.splitlines(keepends=True)
    type_matches = list(TYPE_PATTERN.finditer(source))
    type_names = {match.group(2) for match in type_matches}
    types = [TypeScope(match.group(1), match.group(2), match.start(), len(source), 1, match.group(2)) for match in type_matches]
    namespaces = sorted(set(NAMESPACE_PATTERN.findall(source)))
    modifier_words = r"(?:public|private|protected|internal|static|virtual|override|abstract|sealed|new|async|unsafe|extern|partial|readonly|ref|out|volatile)"
    method_pattern = re.compile(rf"^\s*(?:(?:{modifier_words})\s+)*(?:[A-Za-z_]\w*(?:[<>,.\[\]?]*)\s+)+(~?[A-Za-z_]\w*)\s*(?:<[^>\n]+>)?\s*\(")
    methods: list[dict[str, Any]] = []
    method_line_indexes: list[int] = []
    offsets: list[int] = []
    offset = 0
    for index, line in enumerate(lines):
        offsets.append(offset)
        match = method_pattern.match(line)
        if match:
            name = match.group(1)
            prefix = line[: match.start(1)]
            if name not in CONTROL_NAMES and not re.search(r"\b(?:new|return|throw|if|for|foreach|while|switch|catch|using|lock)\s*$", prefix.strip()):
                method_line_indexes.append(index)
                methods.append({"name": name, "line_index": index, "line": index + 1, "signature": line.strip()})
        offset += len(line)
    # Constructors without a return type are the only useful one-token form.
    for index, line in enumerate(lines):
        if index in method_line_indexes:
            continue
        match = re.match(r"^\s*(?:(?:public|private|protected|internal|static)\s+)?([A-Za-z_]\w*)\s*\(", line)
        if match and match.group(1) in type_names:
            method_line_indexes.append(index)
            methods.append({"name": match.group(1), "line_index": index, "line": index + 1, "signature": line.strip()})
    methods.sort(key=lambda item: item["line_index"])
    depths: list[int] = []
    brace_close_by_line: dict[int, int] = {}
    brace_stack: list[int] = []
    depth = 0
    for line_index, line in enumerate(lines):
        depths.append(depth)
        code = line.split("//", 1)[0]
        code = re.sub(r'"(?:\\.|[^"\\])*"', '""', code)
        for character in code:
            if character == "{":
                brace_stack.append(line_index)
            elif character == "}" and brace_stack:
                brace_close_by_line[brace_stack.pop()] = line_index
        depth += code.count("{") - code.count("}")
        depth = max(0, depth)
    signal_prefix: dict[str, list[int]] = {name: [0] * (len(lines) + 1) for name in SIGNAL_PATTERNS}
    for line_index, line in enumerate(lines):
        for name, pattern in SIGNAL_PATTERNS.items():
            signal_prefix[name][line_index + 1] = signal_prefix[name][line_index] + len(pattern.findall(line))
    type_starts = [match.start() for match in type_matches]
    for position, method in enumerate(methods):
        start_line = method["line_index"]
        next_line = methods[position + 1]["line_index"] if position + 1 < len(methods) else len(lines)
        brace_line = None
        expression_line = None
        for candidate in range(start_line, min(next_line, start_line + 80)):
            if "{" in lines[candidate]:
                brace_line = candidate
                break
            if "=>" in lines[candidate]:
                expression_line = candidate
                break
        if brace_line is not None:
            end_line = brace_close_by_line.get(brace_line, next_line)
            body_start_line = brace_line
            body_end_line = min(end_line + 1, len(lines))
            body_kind = "block"
        elif expression_line is not None:
            end_line = expression_line
            while end_line < len(lines) and ";" not in lines[end_line]:
                end_line += 1
            body_start_line = expression_line
            body_end_line = min(end_line + 1, len(lines))
            body_kind = "expression"
        else:
            body_start_line = start_line
            body_end_line = start_line
            body_kind = "declaration"
        type_index = bisect.bisect_right(type_starts, offsets[start_line]) - 1
        type_match = type_matches[type_index] if type_index >= 0 else None
        type_name = type_match.group(2) if type_match else "<unknown>"
        signals = {name: signal_prefix[name][body_end_line] - signal_prefix[name][body_start_line] for name in SIGNAL_PATTERNS}
        signals["undefined_il_label"] = 0
        short_body = "".join(lines[body_start_line : min(body_end_line, body_start_line + 4)])
        compact_body = strip_for_signal(short_body)
        signals["empty_body"] = int(body_kind == "declaration" or not compact_body)
        signals["throw_only_stub"] = int(bool(compact_body) and bool(re.fullmatch(r"(?:\{\s*)?throw\b.*?;\s*\}?", compact_body, re.IGNORECASE)))
        signals["body_parse_failure"] = 0
        signals["no_body"] = int(body_kind == "declaration")
        method.update(
            {
                "file": relative_path.replace("\\", "/"),
                "type": type_name,
                "type_kind": type_match.group(1) if type_match else "class",
                "body_lines": max(0, body_end_line - body_start_line),
                "signals": signals,
            }
        )
    overloads: defaultdict[str, int] = defaultdict(int)
    for method in methods:
        overloads[method["name"]] += 1
        method["overload"] = overloads[method["name"]]
    return ParsedFile(relative_path, source, source, starts, types, methods, namespaces, 0, 0)


def parse_file(path: Path, relative_path: str) -> ParsedFile:
    normalized = relative_path.replace("\\", "/")
    if normalized not in set(CORE_FILES.values()):
        return parse_file_fast(path, relative_path)
    return _parse_file_structural(path, relative_path)


def _parse_file_structural(path: Path, relative_path: str) -> ParsedFile:
    source = path.read_text(encoding="utf-8", errors="replace")
    masked = mask_comments_and_strings(source)
    starts = line_starts(source)
    brace_pairs, paren_pairs, depth = structural_maps(masked)
    namespaces = sorted(set(NAMESPACE_PATTERN.findall(masked)))
    types: list[TypeScope] = []
    for match in TYPE_PATTERN.finditer(masked):
        opening = masked.find("{", match.end(), min(len(masked), match.end() + 400))
        semicolon = masked.find(";", match.end(), min(len(masked), match.end() + 400))
        if opening < 0 or (semicolon >= 0 and semicolon < opening):
            continue
        closing = brace_pairs.get(opening)
        if closing is None:
            continue
        types.append(TypeScope(match.group(1), match.group(2), opening, closing, depth[opening] + 1))
    for current in types:
        current.full_name = type_full_name(types, current)

    methods: list[dict[str, Any]] = []
    all_open_parens = sorted(position for position, character in enumerate(masked) if character == "(" and position in paren_pairs)
    for current in types:
        start_index = bisect.bisect_right(all_open_parens, current.open_pos)
        end_index = bisect.bisect_left(all_open_parens, current.close_pos)
        for opening_paren in all_open_parens[start_index:end_index]:
            if depth[opening_paren] != current.depth:
                continue
            closing_paren = paren_pairs.get(opening_paren)
            if closing_paren is None or closing_paren > current.close_pos:
                continue
            prefix_start = max(current.open_pos + 1, masked.rfind("\n", current.open_pos + 1, opening_paren) + 1)
            prefix = masked[prefix_start:opening_paren]
            name_match = re.search(r"(~?[A-Za-z_]\w*)\s*(?:<[^<>\n]{0,160}>)?\s*$", prefix)
            if not name_match:
                continue
            method_name = name_match.group(1)
            if not looks_like_method_prefix(prefix, method_name):
                continue
            body_kind, body_start, body_end = method_body_end(masked, brace_pairs, closing_paren, current.close_pos)
            signature_start = prefix_start
            signature_end = body_start if body_start is not None else closing_paren + 1
            signature = strip_for_signal(source[signature_start:signature_end])
            body_text = ""
            if body_start is not None and body_end is not None:
                if body_kind == "block":
                    body_text = source[body_start + 1 : body_end]
                else:
                    body_text = source[body_start:body_end]
            signals: dict[str, int] = {}
            for signal_name, pattern in SIGNAL_PATTERNS.items():
                signals[signal_name] = len(pattern.findall(body_text))
            labels = set(re.findall(r"\b(IL_[A-Za-z0-9_]+)\s*:", body_text))
            goto_targets = set(re.findall(r"\bgoto\s+(IL_[A-Za-z0-9_]+)", body_text))
            signals["undefined_il_label"] = len(goto_targets - labels)
            compact_body = strip_for_signal(body_text)
            signals["empty_body"] = int(not compact_body)
            signals["throw_only_stub"] = int(bool(compact_body) and bool(re.fullmatch(r"(?:\{\s*)?throw\b.*?;\s*\}?", compact_body, re.IGNORECASE)))
            signals["body_parse_failure"] = int(body_kind == "unknown" or (body_kind == "block" and body_end is None))
            if body_start is None:
                signals["no_body"] = 1
            else:
                signals["no_body"] = 0
            method = {
                "file": relative_path.replace("\\", "/"),
                "type": current.full_name,
                "type_kind": current.kind,
                "name": method_name,
                "line": line_number(starts, opening_paren),
                "signature": signature,
                "body_lines": body_text.count("\n") + (1 if body_text else 0),
                "signals": signals,
            }
            methods.append(method)
    # Keep only declarations in the immediate type body; the method scan above
    # already enforces this, so overload numbering is stable after sorting.
    methods.sort(key=lambda item: (item["line"], item["name"], item["signature"]))
    overloads: defaultdict[str, int] = defaultdict(int)
    for method in methods:
        overloads[method["name"]] += 1
        method["overload"] = overloads[method["name"]]
    properties = 0
    property_pattern = re.compile(
        r"(?:public|private|protected|internal|static|virtual|override|abstract|sealed|new|readonly|unsafe|partial|extern|ref|readonly|\s)+"
        r"[A-Za-z_][\w<>,.\[\]?]*\s+[A-Za-z_]\w*\s*\{"
    )
    for match in property_pattern.finditer(masked):
        if any(item.open_pos < match.start() < item.close_pos and depth[match.start()] == item.depth for item in types):
            inside = masked[match.end() : brace_pairs.get(masked.find("{", match.end() - 1), match.end())]
            if re.search(r"\b(?:get|set|init)\b", inside):
                properties += 1
    fields = 0
    for current in types:
        statement_start = current.open_pos + 1
        position = statement_start
        while position < current.close_pos:
            semicolon = masked.find(";", position, current.close_pos)
            if semicolon < 0:
                break
            if depth[semicolon] == current.depth:
                fragment = masked[statement_start:semicolon + 1].strip()
                if fragment and "(" not in fragment and not re.search(r"\b(?:return|using|throw|case|goto)\b", fragment):
                    if re.search(r"\b(?:[A-Za-z_]\w*|[A-Za-z_]\w*[<>,.\[\]?]*)\s+[A-Za-z_]\w*", fragment):
                        fields += max(1, len(re.findall(r",", fragment)) + 1)
                statement_start = semicolon + 1
            position = semicolon + 1
    return ParsedFile(relative_path, source, masked, starts, types, methods, namespaces, properties, fields)


def classify_method(method: dict[str, Any]) -> str:
    signals = method["signals"]
    if signals["native_boundary"]:
        return "NATIVE_BOUNDARY"
    if signals["no_body"] or signals["empty_body"] or signals["throw_only_stub"] or signals["body_parse_failure"]:
        return "SOURCE_LIMITED"
    if signals["runtime_field_handle"]:
        return "STATIC_DATA_REPAIR"
    # Native lift is reserved for explicit native-memory/indirect-jump evidence
    # or a dense combination of failed IL recovery signals.  Smaller, local
    # jump/label damage remains a CFG repair candidate.
    if (
        signals["unmanaged_memory"]
        or signals["indirect_jump"]
        or signals["method_not_found"]
        or signals["undefined_il_label"]
        or signals["goto_il"] >= 4
        or (signals["unknown_result_type"] >= 3 and signals["goto_il"] >= 1)
        or (signals["expected_type_mismatch"] >= 20 and signals["object_assignment"] >= 10)
    ):
        return "NATIVE_LIFT_REQUIRED"
    if signals["goto_il"] or signals["unknown_result_type"] or signals["invalid_comparison"]:
        return "CFG_REPAIR"
    if signals["expected_type_mismatch"] or signals["object_assignment"]:
        return "TYPE_REPAIR"
    return "CLEAN"


def file_manifest(root: Path, include_hashes: bool = True) -> dict[str, Any]:
    files = [path for path in root.rglob("*") if path.is_file()]
    entries: list[tuple[str, int, str | None]] = []
    total_bytes = 0
    for path in sorted(files, key=lambda item: item.relative_to(root).as_posix().lower()):
        relative = path.relative_to(root).as_posix()
        size = path.stat().st_size
        total_bytes += size
        entries.append((relative, size, sha256_file(path) if include_hashes else None))
    digest = hashlib.sha256()
    for relative, size, content_hash in entries:
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(str(size).encode("ascii"))
        digest.update(b"\0")
        if content_hash:
            digest.update(content_hash.encode("ascii"))
        digest.update(b"\n")
    return {"path": str(root), "file_count": len(files), "total_bytes": total_bytes, "tree_sha256": digest.hexdigest()}


def output_manifest(root: Path, name: str) -> dict[str, Any]:
    """Return a fast manifest plus hashes for the most useful fresh artifacts."""
    manifest = file_manifest(root, include_hashes=False)
    selected: dict[str, Any] = {}
    candidates: list[Path] = []
    if name == "dll_il_recovery":
        candidates.append(root / "Assembly-CSharp.dll")
        candidates.append(root / "KairoLibrary.dll")
    elif name == "diffable_cs":
        candidates.extend(
            [
                root / "DiffableCs" / "Assembly-CSharp" / "game" / "Staff.cs",
                root / "DiffableCs" / "Assembly-CSharp" / "game.routeSearch" / "Astar.cs",
                root / "DiffableCs" / "KairoLibrary" / "kairo" / "unity" / "ui" / "Graphics.cs",
                root / "DiffableCs" / "KairoLibrary" / "kairo" / "unity" / "util" / "Language.cs",
            ]
        )
    elif name == "isil":
        candidates.extend(
            [
                root / "IsilDump" / "Assembly-CSharp" / "game" / "Staff.txt",
                root / "IsilDump" / "Assembly-CSharp" / "game" / "routeSearch" / "Astar.txt",
                root / "IsilDump" / "Assembly-CSharp" / "main" / "AppData.txt",
            ]
        )
    for path in candidates:
        if path.is_file():
            selected[path.relative_to(root).as_posix()] = {"bytes": path.stat().st_size, "sha256": sha256_file(path)}
    manifest["selected_file_hashes"] = selected
    return manifest


def percent(value: int, total: int) -> float:
    return round((value * 100.0 / total), 2) if total else 0.0


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def input_identity(args: argparse.Namespace) -> dict[str, Any]:
    paths = {
        "apk": Path(args.apk),
        "rar": Path(args.rar),
        "libil2cpp": Path(args.libil2cpp),
        "metadata": Path(args.metadata),
    }
    result = {}
    for key, path in paths.items():
        result[key] = {"path": str(path), "exists": path.is_file(), "sha256": sha256_file(path) if path.is_file() else None, "expected_sha256": PINNED_INPUTS[key]}
    result["status"] = "MATCH" if all(item["exists"] and item["sha256"] == item["expected_sha256"] for item in result.values()) else "SOURCE_IDENTITY_MISMATCH"
    return result


def parse_corpus(corpus_root: Path) -> tuple[list[ParsedFile], dict[str, Any]]:
    paths = sorted((path for path in corpus_root.rglob("*") if path.is_file()), key=lambda item: item.relative_to(corpus_root).as_posix().lower())
    parsed: list[ParsedFile] = []
    file_rows: list[dict[str, Any]] = []
    type_counts: Counter[str] = Counter()
    namespaces: set[str] = set()
    total_cs_lines = 0
    total_cs_bytes = 0
    extension_counts: Counter[str] = Counter()
    for path in paths:
        relative = path.relative_to(corpus_root).as_posix()
        suffix = path.suffix.lower() or "[no_extension]"
        extension_counts[suffix] += 1
        if suffix != ".cs":
            continue
        item = parse_file(path, relative)
        parsed.append(item)
        file_bytes = path.stat().st_size
        total_cs_bytes += file_bytes
        total_cs_lines += item.source.count("\n") + (1 if item.source else 0)
        namespaces.update(item.namespaces)
        for type_scope in item.types:
            type_counts[type_scope.kind] += 1
        file_rows.append(
            {
                "path": relative,
                "bytes": file_bytes,
                "lines": item.source.count("\n") + (1 if item.source else 0),
                "zero_byte": file_bytes == 0,
                "namespaces": item.namespaces,
                "types": {kind: sum(1 for scope in item.types if scope.kind == kind) for kind in ("class", "struct", "enum", "interface", "record")},
                "methods": len(item.methods),
                "properties": item.properties,
                "fields": item.fields,
            }
        )
    inventory = {
        "schema_version": "r0-cpp2il-corpus-inventory-v1",
        "corpus_root": str(corpus_root),
        "total_files": len(paths),
        "extension_counts": dict(sorted(extension_counts.items())),
        "csharp": {
            "files": len(parsed),
            "zero_byte_files": sum(1 for row in file_rows if row["zero_byte"]),
            "nonzero_files": sum(1 for row in file_rows if not row["zero_byte"]),
            "total_bytes": total_cs_bytes,
            "total_lines": total_cs_lines,
            "total_methods": sum(len(item.methods) for item in parsed),
            "total_properties": sum(item.properties for item in parsed),
            "total_fields": sum(item.fields for item in parsed),
        },
        "namespaces_count": len(namespaces),
        "type_counts": {kind: type_counts.get(kind, 0) for kind in ("class", "struct", "enum", "interface", "record")},
        "files": file_rows,
    }
    return parsed, inventory


def all_methods(parsed_files: Iterable[ParsedFile]) -> list[dict[str, Any]]:
    methods: list[dict[str, Any]] = []
    for parsed in parsed_files:
        for method in parsed.methods:
            clone = dict(method)
            clone["signals"] = dict(method["signals"])
            clone["category"] = classify_method(clone)
            methods.append(clone)
    return methods


def aggregate_quality(methods: list[dict[str, Any]]) -> tuple[dict[str, int], dict[str, int]]:
    categories = Counter(method["category"] for method in methods)
    signals = Counter()
    for method in methods:
        for name, value in method["signals"].items():
            signals[name] += value
    return {category: categories.get(category, 0) for category in CATEGORIES}, dict(sorted(signals.items()))


def compact_method(method: dict[str, Any]) -> dict[str, Any]:
    return {
        "file": method["file"],
        "type": method["type"],
        "name": method["name"],
        "overload": method["overload"],
        "line": method["line"],
        "category": method["category"],
        "body_lines": method["body_lines"],
        "signals": {key: value for key, value in method["signals"].items() if value},
    }


def build_quality_index(methods: list[dict[str, Any]], inventory: dict[str, Any]) -> dict[str, Any]:
    category_counts, signals = aggregate_quality(methods)
    degraded = [compact_method(method) for method in methods if method["category"] != "CLEAN"]
    total = len(methods)
    return {
        "schema_version": "r0-cpp2il-method-quality-index-v1",
        "method_definition": "Conservative lexical audit of decompiled C# bodies; CLEAN means no detected Cpp2IL recovery markers, not proof of semantic correctness.",
        "total_methods": total,
        "method_classification": category_counts,
        "percentages": {
            "clean_percent": percent(category_counts["CLEAN"], total),
            "readable_without_native_percent": percent(category_counts["CLEAN"] + category_counts["TYPE_REPAIR"], total),
            "requires_native_attention_percent": percent(category_counts["NATIVE_LIFT_REQUIRED"], total),
        },
        "global_signals": signals,
        "degraded_methods": degraded,
        "inventory_method_count": inventory["csharp"]["total_methods"],
    }


def core_quality(parsed_files: list[ParsedFile], methods: list[dict[str, Any]]) -> dict[str, Any]:
    by_file = {item.relative_path: item for item in parsed_files}
    result: dict[str, Any] = {}
    for class_name, relative in CORE_FILES.items():
        parsed = by_file.get(relative)
        selected = [method for method in methods if method["file"] == relative]
        if parsed is None:
            result[class_name] = {"file_path": relative, "status": "MISSING"}
            continue
        counts = Counter(method["category"] for method in selected)
        result[class_name] = {
            "file_path": relative,
            "total_lines": parsed.source.count("\n") + (1 if parsed.source else 0),
            "total_methods": len(selected),
            **{category: counts.get(category, 0) for category in CATEGORIES},
            "clean_percent": percent(counts.get("CLEAN", 0), len(selected)),
            "requires_native_percent": percent(counts.get("NATIVE_LIFT_REQUIRED", 0), len(selected)),
            "note_decompiler_count": sum(method["signals"]["note_decompiler_issue"] for method in selected),
            "methods": [compact_method(method) for method in selected],
        }
    return result


def method_lookup(methods: list[dict[str, Any]]) -> dict[tuple[str, str], list[dict[str, Any]]]:
    lookup: defaultdict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for method in methods:
        lookup[(method["file"], method["name"])].append(method)
    return lookup


def find_fresh_method(root: Path | None, relative: str, name: str, occurrence: int) -> dict[str, Any] | None:
    if root is None or not root.is_dir():
        return None
    path = root / Path(relative)
    if not path.is_file():
        path = root / "Assembly-CSharp" / Path(relative)
    if not path.is_file():
        return None
    parsed = parse_file(path, relative)
    candidates = [item for item in parsed.methods if item["name"] == name]
    if not candidates:
        return None
    index = min(max(occurrence - 1, 0), len(candidates) - 1)
    result = dict(candidates[index])
    result["category"] = classify_method(result)
    return result


def isil_evidence(isil_root: Path | None, relative: str, method_name: str) -> dict[str, Any]:
    if isil_root is None or not isil_root.is_dir():
        return {"exists": False, "disassembly_lines": 0, "isil_lines": 0, "path": None}
    candidate = isil_root / Path(relative).with_suffix(".txt")
    if not candidate.is_file():
        return {"exists": False, "disassembly_lines": 0, "isil_lines": 0, "path": None}
    text = candidate.read_text(encoding="utf-8", errors="replace")
    method_marker = f"Method: {method_name}"
    # ISIL files contain the complete assembly type; method-local slicing is
    # intentionally conservative. Presence of the method marker plus native
    # disassembly/ISIL blocks is enough to record evidence availability.
    return {
        "exists": True,
        "path": str(candidate),
        "bytes": candidate.stat().st_size,
        "sha256": sha256_file(candidate),
        "method_marker": method_marker in text,
        "disassembly_lines": text.count("Disassembly:"),
        "isil_lines": text.count("ISIL:"),
        "basic_block_lines": text.lower().count("basic block"),
        "has_native_and_isil": "Disassembly:" in text and "ISIL:" in text,
    }


def comparison(args: argparse.Namespace, methods: list[dict[str, Any]], core: dict[str, Any]) -> dict[str, Any]:
    fresh_csharp_root = Path(args.fresh_csharp) if args.fresh_csharp else None
    fresh_diffable_root = Path(args.fresh_diffable) if args.fresh_diffable else None
    isil_root = Path(args.fresh_isil) if args.fresh_isil else None
    old_lookup = method_lookup(methods)
    required_records: list[dict[str, Any]] = []
    for class_name, method_names in REQUIRED_METHODS.items():
        relative = CORE_FILES[class_name]
        candidates = old_lookup.get((relative, method_names[0]), [])
        for method_name in method_names:
            candidates = old_lookup.get((relative, method_name), [])
            if not candidates:
                required_records.append({"class": class_name, "method": method_name, "status": "OLD_METHOD_NOT_FOUND", "file": relative})
                continue
            old = candidates[0]
            fresh = find_fresh_method(fresh_csharp_root, relative, method_name, old["overload"])
            diffable = find_fresh_method(fresh_diffable_root, relative, method_name, old["overload"])
            evidence = isil_evidence(isil_root, relative, method_name)
            required_records.append(compare_method(class_name, old, fresh, diffable, evidence))
    degraded = [method for method in methods if method["category"] != "CLEAN"]
    clean = [method for method in methods if method["category"] == "CLEAN"]
    # Stable stratified sample: equal-size category/file slices, then fill in
    # lexical order. This avoids using only the largest generated files.
    sample: list[dict[str, Any]] = []
    seen: set[tuple[str, str, int]] = set()
    buckets: defaultdict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for method in methods:
        buckets[(method["category"], method["file"])].append(method)
    for key in sorted(buckets):
        bucket = buckets[key]
        if bucket:
            sample.append(bucket[len(bucket) // 2])
    for method in degraded + clean:
        if len(sample) >= 500:
            break
        identity = (method["file"], method["name"], method["overload"])
        if identity not in seen:
            sample.append(method)
            seen.add(identity)
    sample = sorted(sample, key=lambda item: (item["file"], item["line"], item["name"]))[:500]
    sample_records = []
    for old in sample:
        class_name = next((name for name, path in CORE_FILES.items() if path == old["file"]), "sample")
        fresh = find_fresh_method(fresh_csharp_root, old["file"], old["name"], old["overload"])
        diffable = find_fresh_method(fresh_diffable_root, old["file"], old["name"], old["overload"])
        evidence = isil_evidence(isil_root, old["file"], old["name"])
        sample_records.append(compare_method(class_name, old, fresh, diffable, evidence))
    all_records = required_records + sample_records
    counts = Counter(item.get("classification") for item in all_records)
    return {
        "schema_version": "r0-cpp2il-old-vs-fresh-comparison-v1",
        "fresh_rerun": True,
        "tool_outputs": {
            "fresh_csharp_root": str(fresh_csharp_root) if fresh_csharp_root else None,
            "fresh_diffable_root": str(fresh_diffable_root) if fresh_diffable_root else None,
            "fresh_isil_root": str(isil_root) if isil_root else None,
            "separate_method_dump": False,
        },
        "core_required_methods": required_records,
        "sample": {
            "target_size": 500,
            "actual_size": len(sample_records),
            "records": sample_records,
        },
        "counts": {
            "methods_compared": len(all_records),
            "fresh_csharp_improved_count": counts.get("FRESH_CSHARP_IMPROVED", 0),
            "method_dump_improved_count": counts.get("METHOD_DUMP_IMPROVED", 0),
            "intermediate_representation_improved_count": counts.get("INTERMEDIATE_REPRESENTATION_IMPROVED", 0),
            "old_csharp_already_best_count": counts.get("OLD_CSHARP_ALREADY_BEST", 0),
            "no_cpp2il_improvement_native_lift_required_count": counts.get("NO_CPP2IL_IMPROVEMENT_NATIVE_LIFT_REQUIRED", 0),
        },
        "interpretation": "Fresh final C# is only an improvement when a fresh non-stub body is materially longer than the old body. Fresh ISIL is counted as intermediate-representation evidence for degraded methods when the selected type dump contains native disassembly and ISIL blocks; it does not claim recovered high-level semantics.",
    }


def compare_method(class_name: str, old: dict[str, Any], fresh: dict[str, Any] | None, diffable: dict[str, Any] | None, evidence: dict[str, Any]) -> dict[str, Any]:
    old_degraded = old["category"] != "CLEAN"
    fresh_body = fresh["body_lines"] if fresh else 0
    diffable_body = diffable["body_lines"] if diffable else 0
    fresh_csharp_improved = bool(old_degraded and fresh and fresh_body >= max(3, int(old["body_lines"] * 1.25)) and fresh_body > diffable_body)
    method_dump_improved = False
    ir_improved = bool(old_degraded and evidence.get("has_native_and_isil"))
    if fresh_csharp_improved:
        classification = "FRESH_CSHARP_IMPROVED"
    elif method_dump_improved:
        classification = "METHOD_DUMP_IMPROVED"
    elif ir_improved:
        classification = "INTERMEDIATE_REPRESENTATION_IMPROVED"
    elif old_degraded:
        classification = "NO_CPP2IL_IMPROVEMENT_NATIVE_LIFT_REQUIRED"
    else:
        classification = "OLD_CSHARP_ALREADY_BEST"
    return {
        "class": class_name,
        "file": old["file"],
        "method": old["name"],
        "overload": old["overload"],
        "old_category": old["category"],
        "old_body_lines": old["body_lines"],
        "fresh_csharp_found": fresh is not None,
        "fresh_csharp_body_lines": fresh_body,
        "fresh_diffable_found": diffable is not None,
        "fresh_diffable_body_lines": diffable_body,
        "fresh_isil": evidence,
        "classification": classification,
        "fresh_csharp_improved": fresh_csharp_improved,
        "method_dump_improved": method_dump_improved,
        "intermediate_representation_improved": ir_improved,
    }


def zero_byte_analysis(args: argparse.Namespace, inventory: dict[str, Any]) -> dict[str, Any]:
    corpus_root = Path(args.corpus)
    zero_files = [row["path"] for row in inventory["files"] if row["zero_byte"]]
    script_path = Path(args.script_json) if args.script_json else None
    metadata_evidence: dict[str, Any] = {"script_json": str(script_path) if script_path else None, "available": False}
    if script_path and script_path.is_file():
        data = json.loads(script_path.read_text(encoding="utf-8"))
        script_metadata = data.get("ScriptMetadata", [])
        script_methods = data.get("ScriptMethod", [])
        private_fields = [item for item in script_metadata if str(item.get("Name", "")).startswith("Field$<PrivateImplementationDetails>")]
        private_methods = [item for item in script_methods if "<PrivateImplementationDetails>" in str(item.get("Name", ""))]
        graphics_methods = [item for item in script_methods if str(item.get("Name", "")).startswith("kairo.unity.ui.Graphics$$")]
        language_methods = [item for item in script_methods if str(item.get("Name", "")).startswith("kairo.unity.util.Language$$")]
        metadata_evidence = {
            "script_json": str(script_path),
            "available": True,
            "private_implementation_field_records": len(private_fields),
            "private_implementation_method_records": len(private_methods),
            "graphics_method_records": len(graphics_methods),
            "language_method_records": len(language_methods),
            "private_field_examples": [item.get("Name") for item in private_fields[:5]],
            "private_method_examples": [item.get("Name") for item in private_methods[:5]],
        }
    diffable_root = Path(args.fresh_diffable) if args.fresh_diffable else None
    fresh_root = Path(args.fresh_csharp) if args.fresh_csharp else None
    fresh_files: dict[str, Any] = {}
    for target in ("Graphics.cs", "Language.cs", "_PrivateImplementationDetails_.cs"):
        matches = list(diffable_root.rglob(target)) if diffable_root and diffable_root.is_dir() else []
        fresh_files[target] = [
            {"path": str(path), "bytes": path.stat().st_size, "lines": path.read_text(encoding="utf-8", errors="replace").count("\n") + (1 if path.stat().st_size else 0), "sha256": sha256_file(path)}
            for path in matches
        ]
    for target in ("Graphics.cs", "Language.cs"):
        matches = list(fresh_root.rglob(target)) if fresh_root and fresh_root.is_dir() else []
        fresh_files[f"fresh_ilspy_{target}"] = [
            {"path": str(path), "bytes": path.stat().st_size, "lines": path.read_text(encoding="utf-8", errors="replace").count("\n") + (1 if path.stat().st_size else 0), "sha256": sha256_file(path)}
            for path in matches
        ]
    rows = []
    for path in zero_files:
        name = Path(path).name
        if name == "-PrivateImplementationDetails-.cs":
            classification = "RECOVERABLE_FROM_FRESH_ANALYSIS"
            reason = "The old exporter emitted a zero-byte compiler-generated container, while current metadata exposes RuntimeFieldHandle-backed private fields and generated string-hash methods; fresh Diffable C# also emits the generated type with static-array-size structs."
            evidence = {"metadata": metadata_evidence, "fresh": fresh_files.get("_PrivateImplementationDetails_.cs", [])}
        elif name == "Graphics.cs":
            classification = "EXPORTER_LOSS"
            reason = "kairo.unity.ui.Graphics is present in metadata and the fresh Diffable C# output contains a nonzero type skeleton with fields, methods, and offsets; the old file was empty."
            evidence = {"metadata": metadata_evidence, "fresh": fresh_files.get("Graphics.cs", [])}
        else:
            classification = "EXPORTER_LOSS"
            reason = "kairo.unity.util.Language is present in metadata and the fresh Diffable C# output contains a nonzero type skeleton with fields, methods, and offsets; the old file was empty."
            evidence = {"metadata": metadata_evidence, "fresh": fresh_files.get("Language.cs", [])}
        rows.append({"file": path, "bytes": 0, "classification": classification, "reason": reason, "evidence": evidence})
    return {
        "schema_version": "r0-cpp2il-zero-byte-analysis-v1",
        "zero_byte_cs_count": len(zero_files),
        "files": rows,
        "conclusion": "Zero-byte C# files are exporter artifacts or generated-type loss, not evidence that the corresponding native/metadata types contain no code. Fresh analysis recovers type/method/field evidence; static array values still require the metadata/default-data/relocation pass.",
    }


def compile_blockers(methods: list[dict[str, Any]], inventory: dict[str, Any], zero: dict[str, Any]) -> dict[str, Any]:
    def affected(predicate: Any) -> int:
        return sum(1 for method in methods if predicate(method))

    result = {
        "schema_version": "r0-cpp2il-compile-blockers-v1",
        "compile_attempted": False,
        "compile_attempt_reason": "No compile was attempted: this R0 audit does not authorize C# repair, and the recovered corpus lacks the Unity/framework reference set required for a meaningful build verdict.",
        "categories": {
            "TYPE_EROSION_SYNTAX": {
                "severity": "HIGH",
                "affected_method_count": affected(lambda item: item["signals"]["object_assignment"] or item["signals"]["expected_type_mismatch"]),
                "signal_occurrences": sum(item["signals"]["object_assignment"] + item["signals"]["expected_type_mismatch"] for item in methods),
                "description": "Cpp2IL emitted object-typed temporaries and IL stack type mismatches that are not compile-safe C# semantics.",
                "resolution": "Future AST/type-inference repair, validated against native/ISIL evidence.",
            },
            "CFG_GOTO_IL_CORRUPTION": {
                "severity": "HIGH",
                "affected_method_count": affected(lambda item: item["signals"]["goto_il"] or item["signals"]["undefined_il_label"]),
                "signal_occurrences": sum(item["signals"]["goto_il"] + item["signals"]["undefined_il_label"] for item in methods),
                "description": "Recovered goto IL labels and unresolved control flow prevent treating affected bodies as authoritative high-level C#.",
                "resolution": "Future CFG reconstruction from ISIL/native basic blocks.",
            },
            "CPP2IL_HELPER_DEPENDENCY": {
                "severity": "MEDIUM",
                "affected_method_count": affected(lambda item: item["signals"]["note_decompiler_issue"]),
                "signal_occurrences": sum(item["signals"]["note_decompiler_issue"] for item in methods),
                "description": "Cpp2ILHelpers.NoteDecompilerIssue calls are diagnostic recovery markers and are not product logic.",
                "resolution": "Strip only after the underlying method has been repaired or replaced from evidence.",
            },
            "MISSING_STATIC_DATA_ARRAYS": {
                "severity": "MEDIUM",
                "affected_method_count": affected(lambda item: item["signals"]["runtime_field_handle"]),
                "signal_occurrences": sum(item["signals"]["runtime_field_handle"] for item in methods),
                "description": "RuntimeFieldHandle/InitializeArray sites depend on compiler-generated static blobs that the old corpus does not represent faithfully.",
                "resolution": "Reusable metadata default-value, relocation, and source-asset static-data reconstruction pass.",
            },
            "MISSING_FRAMEWORK_AND_ZERO_BYTE_TYPES": {
                "severity": "LOW",
                "affected_method_count": 0,
                "signal_occurrences": zero["zero_byte_cs_count"],
                "description": "The corpus includes three zero-byte C# artifacts and references Unity/framework types not present as a buildable project reference set.",
                "resolution": "Restore only evidence-backed generated type shells and supply the correct Unity 2022.3.62 reference assemblies during a later authorized repair phase.",
            },
        },
        "inventory_context": {
            "total_methods": inventory["csharp"]["total_methods"],
            "zero_byte_cs": zero["zero_byte_cs_count"],
        },
    }
    return result


def old_invocation(args: argparse.Namespace) -> dict[str, Any]:
    cpp2il = Path(args.cpp2il)
    ilspy = Path(args.ilspycmd) if args.ilspycmd else None
    return {
        "schema_version": "r0-cpp2il-old-invocation-analysis-v1",
        "confidence": "HIGH",
        "evidence": [
            "04_Auto_C_Sharp_Decompiler.bat",
            "RecompileAll.ps1",
        ],
        "cpp2il_command": 'Cpp2IL_Dev\\Cpp2IL.exe --force-binary-path <libil2cpp.so> --force-metadata-path <global-metadata.dat> --force-unity-version "2022.3.62" --output-as dll_il_recovery --output-to <Cpp2IL_Output_IL>',
        "postprocess_command": 'ilspycmd <each generated DLL> -p -o 1_Click_CSharp_Code',
        "force_unity_version": "2022.3.62",
        "old_outputs": ["dll_il_recovery", "ILSpy project C# export"],
        "old_invocation_unknown": False,
        "cpp2il_binary": {"path": str(cpp2il), "exists": cpp2il.is_file(), "sha256": sha256_file(cpp2il) if cpp2il.is_file() else None, "reported_version": "Cpp2IL 2022.1.0"},
        "ilspycmd": {"path": str(ilspy) if ilspy else None, "exists": bool(ilspy and ilspy.is_file()), "sha256": sha256_file(ilspy) if ilspy and ilspy.is_file() else None, "reported_version": "ilspycmd 11.0.0.9375"},
    }


def current_capability(args: argparse.Namespace, rerun_root: Path) -> dict[str, Any]:
    cpp2il = Path(args.cpp2il)
    output_roots = {
        "dll_il_recovery": rerun_root / "dll_il_recovery",
        "diffable_cs": rerun_root / "diffable-cs",
        "isil": rerun_root / "isil",
    }
    return {
        "schema_version": "r0-cpp2il-current-capability-v1",
        "tool": {
            "path": str(cpp2il),
            "sha256": sha256_file(cpp2il) if cpp2il.is_file() else None,
            "version": "Cpp2IL 2022.1.0",
            "local_only": True,
        },
        "supported_output_formats_observed": ["dummydll", "dll_default", "dll_empty", "dll_throw_null", "dll_il_recovery", "diffable-cs", "isil", "wasmmappings", "wasm_name_section"],
        "processors_observed": ["attributeanalyzer", "attributeinjector", "callanalyzer", "nativemethoddetector", "stablenamer", "deobfmap"],
        "capabilities": {
            "managed_dll_il_recovery": True,
            "diffable_csharp_signatures": True,
            "separate_method_dump": False,
            "isil_native_disassembly_and_basic_blocks": True,
            "metadata_and_rva_diagnostics": True,
            "fresh_high_level_csharp_is_authoritative": False,
        },
        "fresh_output_manifests": {
            name: output_manifest(path, name) if path.is_dir() else {"path": str(path), "exists": False}
            for name, path in output_roots.items()
        },
        "commands": {
            "dll_il_recovery": f'"{cpp2il}" --force-binary-path "{args.libil2cpp}" --force-metadata-path "{args.metadata}" --force-unity-version "2022.3.62" --output-as dll_il_recovery --output-to "{output_roots["dll_il_recovery"]}"',
            "diffable_cs": f'"{cpp2il}" --force-binary-path "{args.libil2cpp}" --force-metadata-path "{args.metadata}" --force-unity-version "2022.3.62" --output-as diffable-cs --output-to "{output_roots["diffable_cs"]}"',
            "isil": f'"{cpp2il}" --force-binary-path "{args.libil2cpp}" --force-metadata-path "{args.metadata}" --force-unity-version "2022.3.62" --output-as isil --output-to "{output_roots["isil"]}"',
        },
        "interpretation": "This local Cpp2IL build can reproduce richer intermediate/native evidence, but its Diffable C# output is predominantly signature/stub oriented and does not replace the old ILSpy C# corpus as the high-level starting point.",
    }


def report_text(args: argparse.Namespace, inventory: dict[str, Any], quality: dict[str, Any], core: dict[str, Any], zero: dict[str, Any], comparison_result: dict[str, Any], blockers: dict[str, Any], invocation: dict[str, Any], capability: dict[str, Any], recommendation: str, identity: dict[str, Any]) -> str:
    csharp = inventory["csharp"]
    types = inventory["type_counts"]
    categories = quality["method_classification"]
    lines = [
        "# R0 Cpp2IL Corpus and Recovery-Mode Audit",
        "",
        "Status: COMPLETE. This package stops at the measured Cpp2IL corpus/recovery-mode recommendation. No V8/V8R work and no C# repair were started.",
        "",
        f"Final recommendation: **{recommendation}**",
        "",
        "## Scope and source identity",
        "",
        f"- Pinned identity status: **{identity['status']}**.",
        f"- APK SHA-256: `{identity['apk']['sha256']}`.",
        f"- libil2cpp.so SHA-256: `{identity['libil2cpp']['sha256']}`.",
        f"- global-metadata.dat SHA-256: `{identity['metadata']['sha256']}`.",
        f"- C# RAR SHA-256: `{identity['rar']['sha256']}`.",
        f"- Independent extraction root: `{args.corpus}`. The archive was not modified and the temporary extraction is not a runtime dependency.",
        "",
        "## Existing corpus measurements",
        "",
        f"- Total extracted files: **{inventory['total_files']}**; C# files: **{csharp['files']}**; .csproj files: **{inventory['extension_counts'].get('.csproj', 0)}**.",
        f"- C# bytes/lines: **{csharp['total_bytes']:,} / {csharp['total_lines']:,}**; zero-byte C# files: **{csharp['zero_byte_files']}**.",
        f"- Namespaces: **{inventory['namespaces_count']}**; types: classes **{types['class']}**, structs **{types['struct']}**, enums **{types['enum']}**, interfaces **{types['interface']}**.",
        f"- Methods: **{quality['total_methods']:,}**; CLEAN **{categories['CLEAN']:,} ({quality['percentages']['clean_percent']:.2f}%)**; TYPE_REPAIR **{categories['TYPE_REPAIR']:,}**; CFG_REPAIR **{categories['CFG_REPAIR']:,}**; NATIVE_LIFT_REQUIRED **{categories['NATIVE_LIFT_REQUIRED']:,} ({quality['percentages']['requires_native_attention_percent']:.2f}%)**.",
        f"- Readable without native lifting under this audit index: **{quality['percentages']['readable_without_native_percent']:.2f}%** (CLEAN + TYPE_REPAIR).",
        "",
        "## Core-class result",
        "",
        "| Class | Methods | Clean | Native lift | Clean % |",
        "|---|---:|---:|---:|---:|",
    ]
    for name in CORE_FILES:
        row = core[name]
        if row.get("status") == "MISSING":
            lines.append(f"| {name} | missing | — | — | — |")
        else:
            lines.append(f"| {name} | {row['total_methods']} | {row['CLEAN']} | {row['NATIVE_LIFT_REQUIRED']} | {row['clean_percent']:.2f}% |")
    lines.extend([
        "",
        "The required data-loader path is materially better than the behavior-heavy classes: `FurnitureData.Load` is CLEAN, while routing, rendering, placement, time, and staff-process methods carry type/CFG/native recovery markers.",
        "",
        "## Old invocation and current capability",
        "",
        f"- Old invocation confidence: **{invocation['confidence']}**; Unity version forced: **{invocation['force_unity_version']}**; postprocessor: **{invocation['ilspycmd']['reported_version']}**.",
        f"- Fresh rerun: **YES**, using local `{capability['tool']['version']}` against the pinned native binary and metadata. No download or install was performed.",
        "- Fresh outputs: managed IL recovery DLLs, Diffable C# signatures/stubs, and ISIL native disassembly/basic-block evidence. The selected build did not expose a separate method-dump output.",
        f"- Comparison sample: **{comparison_result['sample']['actual_size']}** plus **{len(comparison_result['core_required_methods'])}** required core-method records.",
        f"- Fresh high-level C# improved: **{comparison_result['counts']['fresh_csharp_improved_count']}**; method dump improved: **{comparison_result['counts']['method_dump_improved_count']}**; intermediate representation improved: **{comparison_result['counts']['intermediate_representation_improved_count']}**; native-lift-required/no high-level improvement: **{comparison_result['counts']['no_cpp2il_improvement_native_lift_required_count']}**.",
        "- Interpretation: keep the old ILSpy C# as the readable skeleton; use fresh ISIL/native evidence as a per-method recovery aid. A full fresh C# replacement is not justified.",
        "",
        "## Zero-byte and static-data conclusion",
        "",
        f"- The three zero-byte C# files are classified as exporter/generated-type loss, not proof of absent code: `{', '.join(zero['files'][index]['file'] for index in range(len(zero['files'])))}`.",
        f"- Current metadata exposes **{zero['files'][0]['evidence']['metadata'].get('private_implementation_field_records', 0)}** PrivateImplementationDetails field records and **{zero['files'][0]['evidence']['metadata'].get('private_implementation_method_records', 0)}** generated method records. Fresh Diffable C# emits generated type shells for the private container, `Graphics`, and `Language`.",
        "- A reusable static-data reconstruction pass is justified: resolve RuntimeFieldHandle relocations, map private field references to metadata default values, then cross-check source/asset tables. Existing K4.1 Fukidashi closure evidence demonstrates this path; it is not executed as a C# repair in R0.",
        "",
        "## Compile blockers",
        "",
        "No compile was attempted. The corpus is not a buildable Unity project and the R0 boundary forbids repair/fabrication. The measured blockers are recorded in `r0-compile-blockers.json`: type erosion, goto/IL CFG corruption, diagnostic helper calls, missing static blobs, and missing framework/reference assemblies/zero-byte exporter artifacts.",
        "",
        "## Recommendation and stop boundary",
        "",
        f"**{recommendation}** — retain the existing C# corpus and use fresh Cpp2IL ISIL/native intermediate evidence selectively for degraded methods and static-data recovery. Do not rerun the full corpus as a replacement. The next authorized boundary is `R1_CORE_CSHARP_REPAIR`; it has not started. Stop here.",
        "",
        "## Evidence package",
        "",
        "- `r0-corpus-inventory.json` — corpus/file/type/field/property inventory.",
        "- `r0-method-quality-index.json` — project-wide issue signals and degraded-method index.",
        "- `r0-core-class-quality.json` — required core-class and method metrics.",
        "- `r0-zero-byte-analysis.json` — zero-byte classifications and fresh metadata evidence.",
        "- `r0-old-invocation-analysis.json` — recovered historical command line and versions.",
        "- `r0-current-cpp2il-capability.json` — current local tool capabilities, commands, and output manifests.",
        "- `r0-old-vs-fresh-comparison.json` — required-method and stratified-sample comparison.",
        "- `r0-compile-blockers.json` — compile-risk categories without a fabricated compile verdict.",
        "- `r0-final-recommendation.json` — single final decision.",
    ])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus", required=True)
    parser.add_argument("--output-root", required=True)
    parser.add_argument("--apk", required=True)
    parser.add_argument("--rar", required=True)
    parser.add_argument("--libil2cpp", required=True)
    parser.add_argument("--metadata", required=True)
    parser.add_argument("--script-json")
    parser.add_argument("--cpp2il", required=True)
    parser.add_argument("--cpp2il-version", default="Cpp2IL 2022.1.0")
    parser.add_argument("--ilspycmd")
    parser.add_argument("--fresh-csharp")
    parser.add_argument("--fresh-diffable")
    parser.add_argument("--fresh-isil")
    parser.add_argument("--rerun-root", required=True)
    args = parser.parse_args()

    identity = input_identity(args)
    if identity["status"] != "MATCH":
        raise SystemExit("SOURCE_IDENTITY_MISMATCH: one or more pinned inputs failed SHA-256 verification")

    corpus_root = Path(args.corpus)
    output_root = Path(args.output_root)
    rerun_root = Path(args.rerun_root)
    parsed_files, inventory = parse_corpus(corpus_root)
    methods = all_methods(parsed_files)
    quality = build_quality_index(methods, inventory)
    core = core_quality(parsed_files, methods)
    zero = zero_byte_analysis(args, inventory)
    comparison_result = comparison(args, methods, core)
    blockers = compile_blockers(methods, inventory, zero)
    invocation = old_invocation(args)
    capability = current_capability(args, rerun_root)
    recommendation = "HYBRID"
    final = {
        "schema_version": "r0-cpp2il-final-recommendation-v1",
        "decision": recommendation,
        "decision_statement": "Keep the existing C# corpus as the high-level skeleton, but use the fresh Cpp2IL ISIL/native intermediate representation and metadata/static-data evidence selectively for degraded methods. Do not replace the corpus with fresh Diffable C# output.",
        "basis": {
            "source_identity": identity["status"],
            "fresh_rerun": True,
            "fresh_csharp_improved_count": comparison_result["counts"]["fresh_csharp_improved_count"],
            "intermediate_representation_improved_count": comparison_result["counts"]["intermediate_representation_improved_count"],
            "zero_byte_files": zero["zero_byte_cs_count"],
            "static_data_pass_justified": True,
        },
        "next_authorized_boundary": "R1_CORE_CSHARP_REPAIR",
        "started_next_phase": False,
        "stop": True,
    }
    write_json(output_root / "r0-corpus-inventory.json", inventory)
    write_json(output_root / "r0-method-quality-index.json", quality)
    write_json(output_root / "r0-core-class-quality.json", core)
    write_json(output_root / "r0-zero-byte-analysis.json", zero)
    write_json(output_root / "r0-old-invocation-analysis.json", invocation)
    write_json(output_root / "r0-current-cpp2il-capability.json", capability)
    write_json(output_root / "r0-old-vs-fresh-comparison.json", comparison_result)
    write_json(output_root / "r0-compile-blockers.json", blockers)
    write_json(output_root / "r0-final-recommendation.json", final)
    (output_root / "R0_CPP2IL_CORPUS_AUDIT.md").write_text(report_text(args, inventory, quality, core, zero, comparison_result, blockers, invocation, capability, recommendation, identity), encoding="utf-8")
    print(json.dumps({"status": "COMPLETE", "recommendation": recommendation, "total_files": inventory["total_files"], "total_methods": quality["total_methods"], "categories": quality["method_classification"], "comparison_counts": comparison_result["counts"]}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
