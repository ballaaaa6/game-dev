"""Structural inventory builder for the recovered C# evidence boundary.

This module deliberately performs cataloging only.  It does not compile or
execute decompiled C#; the resulting records retain source spans and hashes so
later semantic claims can be checked against the evidence that produced them.
"""

from __future__ import annotations

import bisect
import hashlib
import json
import os
import re
from pathlib import Path
from typing import Iterable


TARGET_SCHEMA_VERSION = "csharp-semantic-inventory-targets-v1"
INVENTORY_SCHEMA_VERSION = "csharp-structural-inventory-v1"

_TYPE_RE = re.compile(
    r"\b(?P<kind>class|struct|enum|interface|record)\s+"
    r"(?P<name>[A-Za-z_][A-Za-z0-9_]*)"
)
_METHOD_RE = re.compile(
    r"^\s*(?:(?:public|private|protected|internal|static|virtual|override|"
    r"abstract|sealed|partial|async|unsafe|extern|new|readonly|ref|out)\s+)*"
    r"(?P<return>[A-Za-z_@][A-Za-z0-9_@]*(?:\s*\.\s*[A-Za-z_@][A-Za-z0-9_@]*)?"
    r"(?:\s*<[^(){};]+>)?(?:\s*\[\s*,?\s*\])*\??)\s+"
    r"(?P<name>[A-Za-z_][A-Za-z0-9_]*)\s*\(",
)
_CONSTRUCTOR_RE = re.compile(
    r"^\s*(?:(?:public|private|protected|internal|static|unsafe|extern|new)\s+)*"
    r"(?P<name>[A-Za-z_][A-Za-z0-9_]*)\s*\("
)
_FIELD_RE = re.compile(
    r"^\s*(?P<modifiers>(?:(?:public|private|protected|internal|static|readonly|"
    r"const|volatile|new|unsafe|fixed|virtual|override|abstract|extern|partial)\s+)*)"
    r"(?P<type>[A-Za-z_@][A-Za-z0-9_@]*(?:\s*\.\s*[A-Za-z_@][A-Za-z0-9_@]*)?"
    r"(?:\s*<[^;{}=]+>)?(?:\s*\[\s*,?\s*\])*\??)\s+"
    r"(?P<decls>[^;]+);"
)
_CONTROL_NAMES = {
    "if",
    "for",
    "foreach",
    "while",
    "switch",
    "catch",
    "using",
    "lock",
    "return",
    "nameof",
    "typeof",
    "sizeof",
    "checked",
    "unchecked",
    "when",
}


def _stable_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _normalise_configured_path(value: str) -> str:
    return value.replace("\\", "/")


def _resolve_inside(workspace_root: Path, configured_path: str) -> Path:
    root = workspace_root.resolve()
    raw = Path(_normalise_configured_path(configured_path))
    candidate = raw.resolve() if raw.is_absolute() else (root / raw).resolve()
    try:
        candidate.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"target escapes workspace: {configured_path}") from exc
    return candidate


def load_target_manifest(path: Path) -> dict:
    """Load the JSON target manifest and validate its basic shape."""

    manifest_path = Path(path)
    with manifest_path.open("r", encoding="utf-8") as handle:
        manifest = json.load(handle)
    if not isinstance(manifest, dict):
        raise ValueError("target manifest must be a JSON object")
    if manifest.get("schema_version") != TARGET_SCHEMA_VERSION:
        raise ValueError(
            f"unsupported target schema: {manifest.get('schema_version')!r}"
        )
    required = {
        "primary_files",
        "structural_globs",
        "deep_symbols",
        "field_groups",
        "supporting_evidence_roots",
    }
    missing = sorted(required.difference(manifest))
    if missing:
        raise ValueError(f"target manifest missing keys: {', '.join(missing)}")
    return manifest


def load_claims(path: Path) -> dict:
    """Load the curated semantic claim register without resolving its files."""

    claims_path = Path(path)
    with claims_path.open("r", encoding="utf-8") as handle:
        claims = json.load(handle)
    if not isinstance(claims, dict):
        raise ValueError("semantic claims must be a JSON object")
    if claims.get("schema_version") != "csharp-semantic-claims-v1":
        raise ValueError("semantic claims have an unsupported schema version")
    entries = claims.get("claims")
    if not isinstance(entries, list):
        raise ValueError("semantic claims must contain a claims list")
    seen: set[str] = set()
    for claim in entries:
        if not isinstance(claim, dict):
            raise ValueError("each semantic claim must be an object")
        claim_id = claim.get("claim_id")
        if not isinstance(claim_id, str) or not claim_id:
            raise ValueError("each semantic claim needs a claim_id")
        if claim_id in seen:
            raise ValueError(f"duplicate semantic claim: {claim_id}")
        seen.add(claim_id)
        if not isinstance(claim.get("status"), str) or not claim["status"]:
            raise ValueError(f"claim {claim_id} needs a status")
        if not isinstance(claim.get("source_refs"), list) or not claim["source_refs"]:
            raise ValueError(f"claim {claim_id} needs source_refs")
    return claims


def validate_target_manifest(workspace_root: Path, manifest: dict) -> dict:
    """Validate target paths and return the resolved input boundary."""

    if not isinstance(manifest, dict):
        raise ValueError("target manifest must be a JSON object")
    if manifest.get("schema_version") != TARGET_SCHEMA_VERSION:
        raise ValueError("target manifest has an unsupported schema version")

    root = Path(workspace_root).resolve()
    primary_files = manifest.get("primary_files")
    structural_globs = manifest.get("structural_globs")
    deep_symbols = manifest.get("deep_symbols")
    field_groups = manifest.get("field_groups")
    supporting_roots = manifest.get("supporting_evidence_roots")
    if not isinstance(primary_files, list) or not primary_files:
        raise ValueError("primary_files must be a non-empty list")
    if not isinstance(structural_globs, list):
        raise ValueError("structural_globs must be a list")
    if not isinstance(deep_symbols, list):
        raise ValueError("deep_symbols must be a list")
    if not isinstance(field_groups, dict):
        raise ValueError("field_groups must be an object")
    if not isinstance(supporting_roots, list):
        raise ValueError("supporting_evidence_roots must be a list")

    resolved_primary: list[Path] = []
    for configured in primary_files:
        if not isinstance(configured, str):
            raise ValueError("primary_files entries must be strings")
        resolved = _resolve_inside(root, configured)
        if not resolved.is_file():
            raise FileNotFoundError(str(resolved))
        resolved_primary.append(resolved)

    resolved_structural: list[Path] = []
    for pattern in structural_globs:
        if not isinstance(pattern, str):
            raise ValueError("structural_globs entries must be strings")
        normalised = _normalise_configured_path(pattern)
        matches = sorted(root.glob(normalised), key=lambda item: item.as_posix())
        if not matches:
            raise FileNotFoundError(f"structural glob matched no files: {pattern}")
        for match in matches:
            resolved = match.resolve()
            try:
                resolved.relative_to(root)
            except ValueError as exc:
                raise ValueError(f"structural glob escapes workspace: {pattern}") from exc
            if resolved.is_file():
                resolved_structural.append(resolved)

    for configured in supporting_roots:
        if not isinstance(configured, str):
            raise ValueError("supporting_evidence_roots entries must be strings")
        _resolve_inside(root, configured)

    for symbol in deep_symbols:
        if not isinstance(symbol, str) or not symbol.strip():
            raise ValueError("deep_symbols entries must be non-empty strings")
    for group, fields in field_groups.items():
        if not isinstance(group, str) or not isinstance(fields, list):
            raise ValueError("field_groups must map names to lists")
        if not all(isinstance(field, str) and field for field in fields):
            raise ValueError(f"field group {group!r} contains an invalid field")

    return {
        "primary_files": sorted(set(resolved_primary), key=lambda item: item.as_posix()),
        "structural_files": sorted(
            set(resolved_structural), key=lambda item: item.as_posix()
        ),
    }


def _line_starts(text: str) -> list[int]:
    starts = [0]
    for index, char in enumerate(text):
        if char == "\n":
            starts.append(index + 1)
    return starts


def _line_number(starts: list[int], offset: int) -> int:
    return bisect.bisect_right(starts, max(offset, 0))


def _mask_non_code(text: str) -> str:
    """Mask comments and string/character literals while preserving newlines."""

    chars = list(text)
    state = "normal"
    verbatim = False
    index = 0
    while index < len(chars):
        char = chars[index]
        next_char = chars[index + 1] if index + 1 < len(chars) else ""
        if state == "normal":
            if char == "/" and next_char == "/":
                chars[index] = chars[index + 1] = " "
                state = "line_comment"
                index += 2
                continue
            if char == "/" and next_char == "*":
                chars[index] = chars[index + 1] = " "
                state = "block_comment"
                index += 2
                continue
            if char in ('"', "'"):
                verbatim = char == '"' and index > 0 and chars[index - 1] == "@"
                chars[index] = " "
                state = "verbatim_string" if verbatim else ("string" if char == '"' else "char")
                index += 1
                continue
            index += 1
            continue
        if state == "line_comment":
            if char in "\r\n":
                state = "normal"
            else:
                chars[index] = " "
            index += 1
            continue
        if state == "block_comment":
            if char == "*" and next_char == "/":
                chars[index] = chars[index + 1] = " "
                state = "normal"
                index += 2
            else:
                if char not in "\r\n":
                    chars[index] = " "
                index += 1
            continue
        if state in {"string", "char"}:
            if char == "\\":
                if char not in "\r\n":
                    chars[index] = " "
                if index + 1 < len(chars) and chars[index + 1] not in "\r\n":
                    chars[index + 1] = " "
                index += 2
                continue
            closing = (state == "string" and char == '"') or (
                state == "char" and char == "'"
            )
            if closing:
                chars[index] = " "
                state = "normal"
            elif char not in "\r\n":
                chars[index] = " "
            index += 1
            continue
        if state == "verbatim_string":
            if char == '"' and next_char == '"':
                chars[index] = chars[index + 1] = " "
                index += 2
                continue
            if char == '"':
                chars[index] = " "
                state = "normal"
            elif char not in "\r\n":
                chars[index] = " "
            index += 1
            continue
    return "".join(chars)


def _brace_depths(masked: str, starts: list[int]) -> list[int]:
    lines = masked.splitlines()
    depths: list[int] = []
    depth = 0
    for line in lines:
        depths.append(depth)
        depth += line.count("{")
        depth -= line.count("}")
    while len(depths) < len(starts):
        depths.append(depth)
    return depths


def _matching_close(masked: str, opening: int) -> int | None:
    depth = 0
    for index in range(opening, len(masked)):
        char = masked[index]
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return index
    return None


def _find_body_open(masked: str, start: int) -> int | None:
    opening = masked.find("{", start)
    semicolon = masked.find(";", start)
    if opening == -1 or (semicolon != -1 and semicolon < opening):
        return None
    return opening


def _declaration_text(source: str, starts: list[int], line_index: int, stop: int | None) -> str:
    line_start = starts[line_index]
    line_end = starts[line_index + 1] if line_index + 1 < len(starts) else len(source)
    end = stop if stop is not None and stop >= line_start else line_end
    return source[line_start:end].strip().replace("\r\n", "\n")


def _split_declarators(value: str) -> Iterable[str]:
    depth = 0
    start = 0
    for index, char in enumerate(value):
        if char in "([{<":
            depth += 1
        elif char in ")]}>" and depth:
            depth -= 1
        elif char == "," and depth == 0:
            yield value[start:index]
            start = index + 1
    yield value[start:]


def _source_record(path: Path, line_start: int, line_end: int, raw: str, source_hash: str) -> dict:
    return {
        "source": {
            "file": path.as_posix(),
            "line_start": line_start,
            "line_end": line_end,
        },
        "raw_declaration": raw,
        "source_hash": source_hash,
    }


def _type_candidates(source: str, masked: str, starts: list[int], depths: list[int], path: Path, source_hash: str) -> list[dict]:
    candidates: list[dict] = []
    for match in _TYPE_RE.finditer(masked):
        line_index = _line_number(starts, match.start()) - 1
        opening = _find_body_open(masked, match.end())
        closing = _matching_close(masked, opening) if opening is not None else None
        line_end = _line_number(starts, closing) if closing is not None else line_index + 1
        candidates.append(
            {
                "name": match.group("name"),
                "kind": match.group("kind"),
                "line_index": line_index,
                "line_end": line_end,
                "opening": opening,
                "body_depth": depths[line_index] + 1 if opening is not None else depths[line_index],
                "match_start": match.start(),
                "path": path,
                "source_hash": source_hash,
            }
        )
    candidates.sort(key=lambda item: (item["line_index"], item["match_start"], item["name"]))
    for candidate in candidates:
        parents = [
            item
            for item in candidates
            if item is not candidate
            and item["line_index"] < candidate["line_index"]
            and item["line_end"] >= candidate["line_index"] + 1
        ]
        parent = max(parents, key=lambda item: item["line_index"], default=None)
        candidate["symbol"] = (
            f"{parent['symbol']}.{candidate['name']}" if parent else candidate["name"]
        )
    return candidates


def _enclosing_type(types: list[dict], line_number: int, depth: int) -> dict | None:
    candidates = [
        item
        for item in types
        if item["line_index"] + 1 <= line_number <= item["line_end"]
        and depth >= item["body_depth"]
    ]
    return max(candidates, key=lambda item: item["line_index"], default=None)


def _parse_source(path: Path, workspace_root: Path) -> tuple[list[dict], list[dict], list[dict], dict]:
    source_bytes = path.read_bytes()
    source = source_bytes.decode("utf-8")
    source_hash = hashlib.sha256(source_bytes).hexdigest()
    display_path = path.resolve().relative_to(workspace_root.resolve())
    masked = _mask_non_code(source)
    starts = _line_starts(source)
    depths = _brace_depths(masked, starts)
    types = _type_candidates(source, masked, starts, depths, path, source_hash)
    type_records: list[dict] = []
    for item in types:
        stop = item["opening"]
        raw = _declaration_text(source, starts, item["line_index"], stop)
        record = {
            "symbol": item["symbol"],
            "name": item["name"],
            "kind": item["kind"],
            **_source_record(
                display_path,
                item["line_index"] + 1,
                item["line_end"],
                raw,
                source_hash,
            ),
        }
        type_records.append(record)

    field_records: list[dict] = []
    method_records: list[dict] = []
    lines = source.splitlines(keepends=True)
    for line_index, masked_line in enumerate(masked.splitlines(keepends=True)):
        line_number = line_index + 1
        owner = _enclosing_type(types, line_number, depths[line_index])
        if owner is None or depths[line_index] != owner["body_depth"]:
            continue
        actual_line = lines[line_index] if line_index < len(lines) else ""
        field_match = _FIELD_RE.match(masked_line)
        if field_match and "(" not in masked_line.split(";", 1)[0]:
            declarations = field_match.group("decls")
            for declaration in _split_declarators(declarations):
                name_match = re.match(r"\s*([A-Za-z_][A-Za-z0-9_]*)", declaration)
                if not name_match:
                    continue
                field_name = name_match.group(1)
                field_records.append(
                    {
                        "symbol": field_name,
                        "name": field_name,
                        "owner": owner["symbol"],
                        "type": field_match.group("type").strip(),
                        "kind": "field",
                        **_source_record(
                            display_path,
                            line_number,
                            line_number,
                            actual_line.strip(),
                            source_hash,
                        ),
                    }
                )

        method_match = _METHOD_RE.match(masked_line)
        method_kind = "method"
        if method_match is None:
            constructor_match = _CONSTRUCTOR_RE.match(masked_line)
            if constructor_match and constructor_match.group("name") == owner["name"]:
                method_match = constructor_match
                method_kind = "constructor"
        if method_match is None:
            continue
        method_name = method_match.group("name")
        opening = _find_body_open(masked, starts[line_index])
        closing = _matching_close(masked, opening) if opening is not None else None
        end_line = _line_number(starts, closing) if closing is not None else line_number
        raw = _declaration_text(source, starts, line_index, opening)
        method_records.append(
            {
                "symbol": f"{owner['symbol']}.{method_name}",
                "name": method_name,
                "owner": owner["symbol"],
                "kind": method_kind,
                **({"return_type": method_match.group("return").strip()} if method_kind == "method" else {}),
                **_source_record(display_path, line_number, end_line, raw, source_hash),
            }
        )

    input_record = {
        "path": display_path.as_posix(),
        "size_bytes": len(source_bytes),
        "sha256": source_hash,
    }
    return type_records, field_records, method_records, input_record


def build_structural_inventory(workspace_root: Path, manifest: dict) -> dict:
    """Build deterministic type, field and method catalogs for the target set."""

    root = Path(workspace_root).resolve()
    boundary = validate_target_manifest(root, manifest)
    paths = sorted(
        set(boundary["primary_files"] + boundary["structural_files"]),
        key=lambda item: item.as_posix(),
    )
    all_types: list[dict] = []
    all_fields: list[dict] = []
    all_methods: list[dict] = []
    inputs: list[dict] = []
    for path in paths:
        types, fields, methods, input_record = _parse_source(path, root)
        all_types.extend(types)
        all_fields.extend(fields)
        all_methods.extend(methods)
        inputs.append(input_record)

    all_types.sort(key=lambda item: (item["symbol"], item["source"]["file"], item["source"]["line_start"]))
    all_fields.sort(key=lambda item: (item["symbol"], item["owner"], item["source"]["file"], item["source"]["line_start"]))
    all_methods.sort(key=lambda item: (item["symbol"], item["source"]["file"], item["source"]["line_start"], item["raw_declaration"]))
    inputs.sort(key=lambda item: item["path"])

    inventory = {
        "schema_version": INVENTORY_SCHEMA_VERSION,
        "target_schema_version": manifest["schema_version"],
        "deep_symbols": sorted(manifest["deep_symbols"]),
        "field_groups": {
            group: sorted(fields)
            for group, fields in sorted(manifest["field_groups"].items())
        },
        "inputs": inputs,
        "types": all_types,
        "fields": all_fields,
        "methods": all_methods,
    }
    inventory["content_fingerprint"] = hashlib.sha256(
        _stable_json(inventory).encode("utf-8")
    ).hexdigest()
    return inventory


def _claim_targets(claim: dict, key: str) -> list[str]:
    values = claim.get(key, [])
    if isinstance(values, str):
        return [values]
    if not isinstance(values, list):
        return []
    return [value for value in values if isinstance(value, str)]


def _validate_claims(workspace_root: Path, structural: dict, claims: dict) -> None:
    root = Path(workspace_root).resolve()
    field_names = {record["symbol"] for record in structural["fields"]}
    method_names = {record["symbol"] for record in structural["methods"]}
    for claim in claims["claims"]:
        claim_id = claim["claim_id"]
        for field in _claim_targets(claim, "field_symbols"):
            if field not in field_names:
                raise ValueError(f"claim {claim_id} references unknown field: {field}")
        for method in _claim_targets(claim, "method_symbols"):
            if method not in method_names:
                raise ValueError(f"claim {claim_id} references unknown method: {method}")
        for reference in claim["source_refs"]:
            if not isinstance(reference, dict) or not isinstance(reference.get("file"), str):
                raise ValueError(f"claim {claim_id} has an invalid source reference")
            source_path = _resolve_inside(root, reference["file"])
            if not source_path.is_file():
                raise FileNotFoundError(str(source_path))
            for line_key in ("line_start", "line_end"):
                if line_key in reference and (
                    not isinstance(reference[line_key], int) or reference[line_key] < 1
                ):
                    raise ValueError(f"claim {claim_id} has an invalid {line_key}")
        for access in claim.get("accesses", []):
            if not isinstance(access, dict):
                raise ValueError(f"claim {claim_id} has an invalid access record")
            if access.get("field") not in field_names:
                raise ValueError(
                    f"claim {claim_id} access references unknown field: {access.get('field')}"
                )
            if access.get("method") not in method_names:
                raise ValueError(
                    f"claim {claim_id} access references unknown method: {access.get('method')}"
                )
            evidence_ref = access.get("evidence_ref")
            if not isinstance(evidence_ref, str):
                raise ValueError(f"claim {claim_id} access needs evidence_ref")
            if not _resolve_inside(root, evidence_ref).is_file():
                raise FileNotFoundError(str(_resolve_inside(root, evidence_ref)))


def _claim_index(claims: dict, key: str) -> dict[str, list[dict]]:
    index: dict[str, list[dict]] = {}
    for claim in claims["claims"]:
        for target in _claim_targets(claim, key):
            index.setdefault(target, []).append(claim)
    return index


def _claim_status(claim_list: list[dict]) -> str:
    statuses = {claim["status"] for claim in claim_list}
    if not statuses:
        return "raw_only"
    if len(statuses) != 1:
        raise ValueError(f"conflicting semantic claim statuses: {sorted(statuses)}")
    return next(iter(statuses))


def _claim_refs(claim_list: list[dict]) -> list[dict]:
    references: list[dict] = []
    seen: set[str] = set()
    for claim in claim_list:
        for reference in claim["source_refs"]:
            key = _stable_json(reference)
            if key not in seen:
                seen.add(key)
                references.append(dict(reference))
    return sorted(references, key=_stable_json)


def _method_for_line(methods: list[dict], source_file: str, line_number: int) -> dict | None:
    matches = [
        record
        for record in methods
        if record["source"]["file"] == source_file
        and record["source"]["line_start"] <= line_number <= record["source"]["line_end"]
    ]
    return min(
        matches,
        key=lambda record: (
            record["source"]["line_end"] - record["source"]["line_start"],
            record["source"]["line_start"],
        ),
        default=None,
    )


def _access_operation(masked: str, start: int, end: int) -> str:
    tail = masked[end : end + 512].splitlines()[0]
    prefix = masked[max(0, start - 32) : start]
    if re.match(
        r"\s*(?:\[[^\r\n;]*\])?\s*(?:\+\+|--|\+=|-=|\*=|/=|%=|&=|\|=|\^=|=(?!=|>))",
        tail,
    ):
        return "write"
    if re.search(r"(?:\+\+|--)\s*$", prefix) or re.search(
        r"\b(?:ref|out)\s*$", prefix
    ):
        return "write"
    return "read"


def _build_access_edges(
    workspace_root: Path,
    structural: dict,
    field_names: set[str],
) -> tuple[list[dict], list[dict]]:
    root = Path(workspace_root).resolve()
    methods = structural["methods"]
    declaration_lines = {
        (record["source"]["file"], record["source"]["line_start"], record["symbol"])
        for record in structural["fields"]
    }
    method_names = {
        symbol.rsplit(".", 1)[-1] for symbol in structural.get("deep_symbols", [])
    }
    method_symbols_by_short: dict[str, list[str]] = {}
    for record in methods:
        method_symbols_by_short.setdefault(record["name"], []).append(record["symbol"])
    access_edges: list[dict] = []
    call_edges: list[dict] = []
    input_paths = [root / Path(item["path"]) for item in structural["inputs"]]
    for path in input_paths:
        source_bytes = path.read_bytes()
        source = source_bytes.decode("utf-8")
        masked = _mask_non_code(source)
        starts = _line_starts(source)
        source_file = path.relative_to(root).as_posix()
        for field in sorted(field_names, key=len, reverse=True):
            token_re = re.compile(rf"\b{re.escape(field)}\b")
            for match in token_re.finditer(masked):
                line_number = _line_number(starts, match.start())
                if (source_file, line_number, field) in declaration_lines:
                    continue
                owner = _method_for_line(methods, source_file, line_number)
                access_edges.append(
                    {
                        "field": field,
                        "operation": _access_operation(masked, match.start(), match.end()),
                        "method": owner["symbol"] if owner else None,
                        "source": {
                            "file": source_file,
                            "line_start": line_number,
                            "line_end": line_number,
                        },
                        "raw_expression": source.splitlines()[line_number - 1].strip(),
                    }
                )

        if not method_names:
            continue
        calls_re = re.compile(
            r"\b(?:" + "|".join(re.escape(name) for name in sorted(method_names)) + r")\s*\("
        )
        for match in calls_re.finditer(masked):
            callee_name = re.match(r"[A-Za-z_][A-Za-z0-9_]*", masked[match.start() :]).group(0)
            line_number = _line_number(starts, match.start())
            declared = any(
                record["source"]["file"] == source_file
                and record["source"]["line_start"] == line_number
                and record["name"] == callee_name
                for record in methods
            )
            if declared:
                continue
            owner = _method_for_line(methods, source_file, line_number)
            candidates = sorted(method_symbols_by_short.get(callee_name, []))
            call_edges.append(
                {
                    "caller": owner["symbol"] if owner else None,
                    "callee": candidates[0] if candidates else callee_name,
                    "callee_candidates": candidates,
                    "source": {
                        "file": source_file,
                        "line_start": line_number,
                        "line_end": line_number,
                    },
                }
            )
    access_edges.sort(
        key=lambda edge: (
            edge["field"],
            edge["source"]["file"],
            edge["source"]["line_start"],
            edge["operation"],
        )
    )
    call_edges.sort(
        key=lambda edge: (
            edge["callee"],
            edge["source"]["file"],
            edge["source"]["line_start"],
        )
    )
    return access_edges, call_edges


def _build_transitions(
    fields: list[dict],
    access_edges: list[dict],
    claims: dict,
) -> list[dict]:
    claim_by_id = {claim["claim_id"]: claim for claim in claims["claims"]}
    access_by_field: dict[str, list[dict]] = {}
    for edge in access_edges:
        access_by_field.setdefault(edge["field"], []).append(edge)
    # The frozen transition catalogue is intentionally not carried into the
    # Social Dev parser. Social transitions must be authored from Social
    # Dev evidence and contracts, not inherited from the frozen corpus.
    definitions: list[tuple[str, str, list[str]]] = []
    transitions: list[dict] = []
    for claim_id, transition_id, raw_fields in definitions:
        claim = claim_by_id[claim_id]
        transitions.append(
            {
                "transition_id": transition_id,
                "claim_id": claim_id,
                "status": claim["status"],
                "fields": raw_fields,
                "observed_operations": {
                    field: sorted({edge["operation"] for edge in access_by_field.get(field, [])})
                    for field in raw_fields
                },
                "evidence_refs": claim["source_refs"],
                "rationale": claim["rationale"],
            }
        )
    return transitions


def build_semantic_slices(workspace_root: Path, structural: dict, claims: dict) -> dict:
    """Build access, transition and provenance records from bounded claims."""

    _validate_claims(workspace_root, structural, claims)
    field_names = {
        field
        for fields in structural.get("field_groups", {}).values()
        for field in fields
    }
    field_claims = _claim_index(claims, "field_symbols")
    method_claims = _claim_index(claims, "method_symbols")

    enriched_fields: list[dict] = []
    for record in structural["fields"]:
        matches = field_claims.get(record["symbol"], [])
        enriched = dict(record)
        enriched["semantic_status"] = _claim_status(matches)
        enriched["claim_ids"] = sorted(claim["claim_id"] for claim in matches)
        enriched["evidence_refs"] = _claim_refs(matches)
        if matches and all("semantic_name" in claim for claim in matches):
            semantic_names = {claim["semantic_name"] for claim in matches}
            if len(semantic_names) == 1:
                enriched["semantic_name"] = next(iter(semantic_names))
        enriched_fields.append(enriched)

    enriched_methods: list[dict] = []
    for record in structural["methods"]:
        matches = method_claims.get(record["symbol"], [])
        enriched = dict(record)
        enriched["semantic_status"] = (
            _claim_status(matches) if matches else "structural_only"
        )
        enriched["claim_ids"] = sorted(claim["claim_id"] for claim in matches)
        enriched["evidence_refs"] = _claim_refs(matches)
        enriched_methods.append(enriched)

    access_edges, call_edges = _build_access_edges(workspace_root, structural, field_names)
    for claim in claims["claims"]:
        for access in claim.get("accesses", []):
            access_edges.append(
                {
                    "field": access["field"],
                    "operation": access["operation"],
                    "method": access["method"],
                    "claim_id": claim["claim_id"],
                    "source": {
                        "file": access["evidence_ref"],
                        "line_start": None,
                        "line_end": None,
                    },
                    "evidence_ref": access["evidence_ref"],
                }
            )
    access_edges.sort(
        key=lambda edge: (
            edge["field"],
            edge["source"]["file"],
            edge["source"]["line_start"] or 0,
            edge["operation"],
        )
    )
    transitions = _build_transitions(enriched_fields, access_edges, claims)
    provenance_index = [
        {
            "claim_id": claim["claim_id"],
            "status": claim["status"],
            "field_symbols": sorted(_claim_targets(claim, "field_symbols")),
            "method_symbols": sorted(_claim_targets(claim, "method_symbols")),
            "field_path": claim.get("field_path"),
            "source_refs": claim["source_refs"],
            "rationale": claim["rationale"],
        }
        for claim in sorted(claims["claims"], key=lambda item: item["claim_id"])
    ]
    field_status_counts: dict[str, int] = {}
    for record in enriched_fields:
        if record["symbol"] not in field_names:
            continue
        status = record["semantic_status"]
        field_status_counts[status] = field_status_counts.get(status, 0) + 1
    method_status_counts: dict[str, int] = {}
    for record in enriched_methods:
        status = record["semantic_status"]
        method_status_counts[status] = method_status_counts.get(status, 0) + 1

    semantic_payload = {
        "fields": enriched_fields,
        "methods": enriched_methods,
        "access_edges": access_edges,
        "call_edges": call_edges,
        "transitions": transitions,
        "provenance_index": provenance_index,
    }
    semantic_fingerprint = hashlib.sha256(
        _stable_json(semantic_payload).encode("utf-8")
    ).hexdigest()
    result = {
        **semantic_payload,
        "claim_status_counts": {
            "claims": {
                status: sum(1 for claim in claims["claims"] if claim["status"] == status)
                for status in sorted({claim["status"] for claim in claims["claims"]})
            },
            "fields": dict(sorted(field_status_counts.items())),
            "methods": dict(sorted(method_status_counts.items())),
        },
        "unresolved": {
            "fields": sorted(
                record["symbol"]
                for record in enriched_fields
                if record["symbol"] in field_names
                if record["semantic_status"]
                in {"unknown", "raw_only", "assembly_fallback_bounded_slice_required"}
            ),
            "methods": sorted(
                record["symbol"]
                for record in enriched_methods
                if record["semantic_status"]
                in {"structural_only", "unknown", "raw_only", "assembly_fallback_bounded_slice_required"}
            ),
        },
        "semantic_fingerprint": semantic_fingerprint,
    }
    result["runtime_projection"] = build_runtime_projection(structural, result)
    return result


def _render_inventory_report(inventory: dict, slices: dict) -> str:
    counts = slices["claim_status_counts"]
    unresolved_fields = slices["unresolved"]["fields"]
    unresolved_methods = slices["unresolved"]["methods"]
    lines = [
        "# C# Semantic Inventory Report",
        "",
        "- Structural schema: `" + inventory["schema_version"] + "`",
        "- Structural fingerprint: `" + inventory["content_fingerprint"] + "`",
        "- Semantic fingerprint: `" + slices["semantic_fingerprint"] + "`",
        "- Input files: " + str(len(inventory["inputs"])),
        "- Structural counts: "
        + f"types={len(inventory['types'])}, fields={len(inventory['fields'])}, methods={len(inventory['methods'])}",
        "- Access edges: " + str(len(slices["access_edges"])),
        "- Call edges: " + str(len(slices["call_edges"])),
        "- Claims by status: `" + _stable_json(counts["claims"]) + "`",
        "",
        "## Evidence boundary",
        "",
        "The recovered C# is cataloged as read-only evidence. No decompiled C# body is executed by the runtime.",
        "Numeric mode/state values remain raw unless a bounded claim supplies a verified semantic contract.",
        "",
        "## Unresolved records",
        "",
        "- Fields: " + (", ".join(unresolved_fields) if unresolved_fields else "none"),
        "- Methods: " + (", ".join(unresolved_methods) if unresolved_methods else "none"),
    ]
    return "\n".join(lines) + "\n"


def write_inventory(
    output_dir: Path,
    inventory: dict,
    slices: dict | None = None,
    runtime_projection_path: Path | None = None,
) -> None:
    """Write structural catalogs beneath the generated evidence directory."""

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    fingerprint = inventory["content_fingerprint"]
    common = {
        "schema_version": inventory["schema_version"],
        "content_fingerprint": fingerprint,
    }
    if slices is not None:
        common["semantic_fingerprint"] = slices["semantic_fingerprint"]
    files = {
        "inventory_manifest.json": {
            **common,
            "target_schema_version": inventory["target_schema_version"],
            "inputs": inventory["inputs"],
            "deep_symbols": inventory["deep_symbols"],
            "field_groups": inventory["field_groups"],
            "counts": {
                "types": len(inventory["types"]),
                "fields": len(inventory["fields"]),
                "methods": len(inventory["methods"]),
            },
        },
        "type_catalog.json": {**common, "records": inventory["types"]},
        "field_catalog.json": {
            **common,
            "records": slices["fields"] if slices else inventory["fields"],
            **({"access_edges": slices["access_edges"]} if slices else {}),
        },
        "method_catalog.json": {
            **common,
            "records": slices["methods"] if slices else inventory["methods"],
            **({"call_edges": slices["call_edges"]} if slices else {}),
        },
    }
    if slices is not None:
        files["transition_catalog.json"] = {
            **common,
            "records": slices["transitions"],
        }
        files["provenance_index.json"] = {
            **common,
            "records": slices["provenance_index"],
            "claim_status_counts": slices["claim_status_counts"],
            "unresolved": slices["unresolved"],
        }
        (output / "inventory_report.md").write_text(
            _render_inventory_report(inventory, slices), encoding="utf-8"
        )
    for filename, payload in files.items():
        (output / filename).write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    if slices is not None and runtime_projection_path is not None:
        runtime_path = Path(runtime_projection_path)
        runtime_path.parent.mkdir(parents=True, exist_ok=True)
        runtime_path.write_text(
            json.dumps(slices["runtime_projection"], ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )


def check_inventory(workspace_root: Path, manifest_path: Path, output_dir: Path) -> dict:
    """Rebuild in memory and compare the generated inventory fingerprint."""

    manifest = load_target_manifest(manifest_path)
    inventory = build_structural_inventory(workspace_root, manifest)
    manifest_file = Path(output_dir) / "inventory_manifest.json"
    if not manifest_file.is_file():
        raise FileNotFoundError(str(manifest_file))
    with manifest_file.open("r", encoding="utf-8") as handle:
        generated = json.load(handle)
    if generated.get("content_fingerprint") != inventory["content_fingerprint"]:
        raise ValueError(
            "inventory fingerprint mismatch: "
            f"expected {inventory['content_fingerprint']}, "
            f"found {generated.get('content_fingerprint')}"
        )
    claims_path = Path(workspace_root) / "tools" / "social-dev" / "semantic_inventory_claims.json"
    slices = None
    if claims_path.is_file():
        slices = build_semantic_slices(workspace_root, inventory, load_claims(claims_path))
        if generated.get("semantic_fingerprint") != slices["semantic_fingerprint"]:
            raise ValueError(
                "semantic inventory fingerprint mismatch: "
                f"expected {slices['semantic_fingerprint']}, "
                f"found {generated.get('semantic_fingerprint')}"
            )
    return {
        "status": "check_pass",
        "content_fingerprint": inventory["content_fingerprint"],
        "semantic_fingerprint": slices["semantic_fingerprint"] if slices else None,
        "counts": {
            "types": len(inventory["types"]),
            "fields": len(inventory["fields"]),
            "methods": len(inventory["methods"]),
        },
    }


def build_runtime_projection(inventory: dict, slices: dict | None = None) -> dict:
    """Return a source-free status summary safe for browser diagnostics."""

    projection = {
        "schema_version": "csharp-semantic-inventory-runtime-v1",
        "inventory_schema_version": inventory["schema_version"],
        "content_fingerprint": inventory["content_fingerprint"],
        "input_count": len(inventory["inputs"]),
        "counts": {
            "types": len(inventory["types"]),
            "fields": len(inventory["fields"]),
            "methods": len(inventory["methods"]),
        },
        "source_bodies_included": False,
    }
    if slices is not None:
        projection["semantic_fingerprint"] = slices["semantic_fingerprint"]
        projection["claim_status_counts"] = slices["claim_status_counts"]
        projection["unresolved"] = slices["unresolved"]
        projection["fields"] = [
            {
                "symbol": record["symbol"],
                "semantic_status": record["semantic_status"],
                "claim_ids": record["claim_ids"],
                "evidence_ref_count": len(record["evidence_refs"]),
            }
            for record in slices["fields"]
            if record["symbol"] in {
                field
                for fields in inventory.get("field_groups", {}).values()
                for field in fields
            }
        ]
        projection["methods"] = [
            {
                "symbol": record["symbol"],
                "semantic_status": record["semantic_status"],
                "claim_ids": record["claim_ids"],
                "evidence_ref_count": len(record["evidence_refs"]),
            }
            for record in slices["methods"]
            if record["symbol"] in set(inventory.get("deep_symbols", []))
        ]
        projection["provenance"] = [
            {
                "claim_id": record["claim_id"],
                "status": record["status"],
                "source_refs": record["source_refs"],
            }
            for record in slices["provenance_index"]
        ]
    return projection
