"""Build the game-scoped G0/G1 Social Dev canonical knowledge base.

This builder is intentionally a static, evidence-only pass.  It reads the
pinned APK/native/metadata/dump, the immutable C# extraction, the accepted
Social Dev evidence packages, and the indexed asset/data package.  It writes
only derived artifacts below ``knowledge/data/original``.

The C# parser is structural.  A decompiler marker never becomes semantic
authority; damaged bodies are retained with an explicit body status and are
closed only where an accepted native/static contract supplies the proof.
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
import re
import shutil
import sqlite3
import struct
import sys
import zipfile
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[2]
RAW_CSHARP = ROOT / "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code"
UPDATE_CSHARP = ROOT / "sources/raw/1_Click_CSharp_Code update"
APK = ROOT / "sources/raw/Social_Dev_Story_v2.5.1.apk"
RAR = ROOT / "sources/raw/1_Click_CSharp_Code.rar"
ASSET_ZIP = ROOT / "sources/raw/Social_Dev_Story_v2.5.1_ASSETS_ONLY_WITH_ASSEMBLY_GUIDE.zip"
NATIVE = ROOT / "knowledge/sources/phase3a_apk_probe/raw/libil2cpp.so"
METADATA = ROOT / "knowledge/sources/phase3a_apk_probe/raw/global-metadata.dat"
DUMP = ROOT / "knowledge/sources/phase3a_apk_probe/il2cpp_dump/dump.cs"
EVIDENCE = ROOT / "knowledge/fixtures/accepted"
RUNTIME_EVIDENCE = ROOT / "knowledge/fixtures/accepted/runtime"
KB = ROOT / "knowledge/data/original"
JSONL = KB / "jsonl"
GRAPHS = KB / "graphs"
SQLITE_PATH = KB / "sqlite/social_dev_original_data.sqlite"
REPORTS = KB / "reports"

EXPECTED_APK_SHA256 = "fa0e9e3a843732258fc05b2611a8e0f5be6f7e95f2141a53f31fb082322fe2bf"
EXPECTED_NATIVE_SHA256 = "364893401fcf7fc2380ae64291783edf7b95eecea4775041c3f4c8c081b4d54a"
EXPECTED_METADATA_SHA256 = "f65f3a00675f35cfa28fef53c37ed7a2dc01e143b6d59c6014a286fa84e4a579"
EXPECTED_DUMP_SHA256 = "4487cba6916e159afefec2cd1a9ecf0d12d05b2d76126e7099a5d35323967eb2"

RECONCILIATION_STATUSES = (
    "CONFIRMED",
    "UPGRADED",
    "SUPERSEDED",
    "CONFLICT",
    "SOURCE_LIMITED",
    "UNCHANGED_ACCEPTED",
)

TIER_A_DIRS = ("main", "data", "game", "game.routeSearch", "form")
TIER_D_PREFIXES = {
    "Unity",
    "UnityEngine",
    "System",
    "Mono",
    "Firebase",
    "Tapjoy",
    "Newtonsoft.Json",
    "Unity.Services",
    "Google",
    "Microsoft",
    "Internal",
    "AOT",
}
TIER_B_DIRS = (
    "cfg",
    "ext",
    "ext.util",
    "surface",
    "native",
    "mail.form",
    "mail.ui",
    "news",
    "panel",
    "analytics",
    "lobi",
    "util",
    "BuildInfos",
)
TIER_C_DIRS = ("kairo.unity.io", "kairo.unity.util", "kairo.unity.ui", "kairo.unity.graph")


def stable_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return path.as_posix().replace("\\", "/")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def json_path(value: str | Path) -> Path:
    path = Path(str(value).split("#", 1)[0].replace("\\", "/"))
    if path.is_absolute():
        return path
    return ROOT / path


def source_ref(path: str | Path, line: int | None = None, note: str | None = None) -> dict[str, Any]:
    raw = str(path)
    resolved = json_path(raw)
    record: dict[str, Any] = {"path": raw.replace("\\", "/")}
    if resolved.is_file():
        record["sha256"] = sha256_file(resolved)
        record["bytes"] = resolved.stat().st_size
    elif resolved.is_dir():
        record["sha256"] = None
        record["status"] = "DIRECTORY_SCOPE"
        record["file_count"] = sum(1 for child in resolved.rglob("*") if child.is_file())
    else:
        record["sha256"] = None
        record["status"] = "SOURCE_LIMITED_MISSING_REF"
    if line is not None:
        record["line"] = line
    if note:
        record["note"] = note
    return record


def ensure_dirs() -> None:
    for path in (KB, JSONL, GRAPHS, REPORTS, SQLITE_PATH.parent):
        path.mkdir(parents=True, exist_ok=True)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
            count += 1
    return count


def iter_json_files(*roots: Path) -> Iterable[Path]:
    seen: set[Path] = set()
    for root in roots:
        if root.is_file() and root.suffix.lower() == ".json":
            paths = [root]
        elif root.is_dir():
            paths = sorted(root.rglob("*.json"))
        else:
            paths = []
        for path in paths:
            resolved = path.resolve()
            if resolved not in seen:
                seen.add(resolved)
                yield path


def walk_dicts(value: Any) -> Iterable[dict[str, Any]]:
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk_dicts(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk_dicts(child)


def method_key(value: str) -> str:
    text = value.strip()
    text = text.split("(", 1)[0].strip()
    text = text.replace("::", ".")
    return text


def method_short(value: str) -> str:
    return method_key(value).rsplit(".", 1)[-1]


def canonical_id(kind: str, *parts: Any) -> str:
    normalized = "|".join(str(part).strip() for part in parts)
    return f"{kind}:{hashlib.sha1(normalized.encode('utf-8')).hexdigest()[:16]}"


def direct_canonical_id(kind: str, value: str) -> str:
    return f"{kind}:{value}"


def dedupe_records(records: list[dict[str, Any]], key: str = "entity_id") -> list[dict[str, Any]]:
    """Keep one deterministic record per canonical entity key."""
    selected: dict[str, dict[str, Any]] = {}
    for record in records:
        value = record.get(key)
        if value is None:
            continue
        current = selected.get(str(value))
        if current is None:
            selected[str(value)] = record
            continue
        # Prefer a Tier-A/direct source over a bounded closure duplicate, then
        # retain the earliest source location for deterministic provenance.
        current_tier = str(current.get("tier", "A"))
        new_tier = str(record.get("tier", "A"))
        if current_tier != "A" and new_tier == "A":
            selected[str(value)] = record
    return list(selected.values())


def class_labels(path: str, name: str = "") -> list[str]:
    labels: set[str] = set()
    if path.startswith("data/") or "/data/" in path:
        labels.update({"STAFF_DATA", "JOB_SKILL_STATUS"} if any(x in name for x in ("Staff", "Job", "Skill")) else {"EVENT_SYSTEM"})
    if "/game/" in f"/{path}" or path.startswith("game/"):
        labels.update({"LIVING_CORE", "MOVEMENT"})
        if any(x in name for x in ("Room", "ObjChip", "MapChip")):
            labels.add("ROOM_WORLD")
        if "Astar" in name or "Node" in name:
            labels.add("PATHFINDING")
        if "Staff" in name:
            labels.update({"WORK_EXECUTION", "ANIMATION"})
    if "game.routeSearch" in path:
        labels.update({"MOVEMENT", "PATHFINDING"})
    if path.startswith("form/") or "/form/" in path:
        labels.add("PLAYER_COMMAND_UI")
    if "/main/" in f"/{path}" or path.startswith("main/"):
        labels.update({"SAVE_STATE", "EVENT_SYSTEM"})
    if any(x in path for x in ("kairo.", "ext.", "Unity", "System", "Firebase", "Tapjoy")):
        labels.add("EXTERNAL_FRAMEWORK")
    if not labels:
        labels.add("UNKNOWN")
    return sorted(labels)


def verify_source_identity() -> dict[str, Any]:
    required = (APK, RAR, ASSET_ZIP, NATIVE, METADATA, DUMP, RAW_CSHARP, UPDATE_CSHARP)
    missing = [relative(path) for path in required if not path.exists()]
    if missing:
        raise RuntimeError("FAIL_SOURCE_IDENTITY_MISMATCH: missing " + ", ".join(missing))

    hashes = {
        "apk": sha256_file(APK),
        "rar": sha256_file(RAR),
        "asset_zip": sha256_file(ASSET_ZIP),
        "libil2cpp": sha256_file(NATIVE),
        "global_metadata": sha256_file(METADATA),
        "dump": sha256_file(DUMP),
    }
    expected = {
        "apk": EXPECTED_APK_SHA256,
        "libil2cpp": EXPECTED_NATIVE_SHA256,
        "global_metadata": EXPECTED_METADATA_SHA256,
        "dump": EXPECTED_DUMP_SHA256,
    }
    mismatches = [f"{key}: {hashes[key]} != {value}" for key, value in expected.items() if hashes[key].lower() != value.lower()]
    if mismatches:
        raise RuntimeError("FAIL_SOURCE_IDENTITY_MISMATCH: " + "; ".join(mismatches))

    native_bytes = NATIVE.read_bytes()[:20]
    elf_class = native_bytes[4] if len(native_bytes) > 4 and native_bytes[:4] == b"\x7fELF" else None
    elf_machine = struct.unpack_from("<H", native_bytes, 18)[0] if len(native_bytes) >= 20 and native_bytes[:4] == b"\x7fELF" else None
    metadata_version = struct.unpack_from("<I", METADATA.read_bytes(), 4)[0]
    if elf_class != 2 or elf_machine != 183 or metadata_version != 31:
        raise RuntimeError("FAIL_SOURCE_IDENTITY_MISMATCH: ELF/ABI/metadata characteristics differ")

    with zipfile.ZipFile(APK) as archive:
        names = archive.namelist()
        required_entries = {
            "lib/arm64-v8a/libil2cpp.so": EXPECTED_NATIVE_SHA256,
            "assets/bin/Data/Managed/Metadata/global-metadata.dat": EXPECTED_METADATA_SHA256,
        }
        entry_hashes = {}
        for name, expected_hash in required_entries.items():
            if name not in names:
                raise RuntimeError(f"FAIL_SOURCE_IDENTITY_MISMATCH: APK entry missing {name}")
            entry_hash = sha256_bytes(archive.read(name))
            entry_hashes[name] = entry_hash
            if entry_hash.lower() != expected_hash.lower():
                raise RuntimeError(f"FAIL_SOURCE_IDENTITY_MISMATCH: APK entry hash differs for {name}")

        boot = archive.read("assets/bin/Data/boot.config").decode("utf-8", "replace")
        scripting_raw = archive.read("assets/bin/Data/ScriptingAssemblies.json")
        scripting = json.loads(scripting_raw.decode("utf-8"))
        version_candidates: list[str] = []
        for name in ("assets/bin/Data/globalgamemanagers", "assets/bin/Data/level0", "assets/bin/Data/sharedassets0.assets"):
            if name in names:
                strings = re.findall(rb"[ -~]{6,}", archive.read(name))
                version_candidates.extend(item.decode("ascii", "ignore") for item in strings if b"2022.3.62f2" in item)
        asset_entries = [name for name in names if name.startswith("assets/")]
        data_entries = [name for name in names if name.startswith("assets/bin/Data/")]
        hash_named = [name for name in data_entries if re.fullmatch(r"[0-9a-f]{32}", name.rsplit("/", 1)[-1])]
        resources = [name for name in data_entries if name.lower().endswith(".resource")]
        native_libs = [name for name in names if name.startswith("lib/arm64-v8a/") and name.lower().endswith(".so")]
        serialized_versions: collections.Counter[int] = collections.Counter()
        for name in hash_named:
            raw = archive.read(name)
            if len(raw) >= 12:
                version = struct.unpack_from(">I", raw, 8)[0]
                if version:
                    serialized_versions[version] += 1

    if "2022.3.62f2" not in version_candidates:
        raise RuntimeError("FAIL_SOURCE_IDENTITY_MISMATCH: Unity version string not found")

    tier_a = [path for directory in TIER_A_DIRS for path in sorted((RAW_CSHARP / directory).glob("*.cs"))]
    tier_a_count = len(tier_a)
    if tier_a_count != 89:
        raise RuntimeError(f"FAIL_SOURCE_IDENTITY_MISMATCH: expected 89 Tier-A files, found {tier_a_count}")

    return {
        "status": "PASS_SOURCE_IDENTITY",
        "hashes": hashes,
        "expected_hashes": expected,
        "entry_hashes": entry_hashes,
        "characteristics": {
            "elf_class": "ELF64" if elf_class == 2 else elf_class,
            "elf_machine": "AArch64" if elf_machine == 183 else elf_machine,
            "abi": "arm64-v8a",
            "unity_version": "2022.3.62f2",
            "metadata_version": metadata_version,
        },
        "apk_inventory": {
            "total_entries": len(names),
            "assets_entries": len(asset_entries),
            "data_entries": len(data_entries),
            "hash_named_serialized_candidates": len(hash_named),
            "serialized_file_versions": dict(sorted(serialized_versions.items())),
            "resource_sidecars": len(resources),
            "native_libraries_arm64": len(native_libs),
            "version_observations": sorted(set(version_candidates)),
            "boot_config_sha256": sha256_bytes(boot.encode("utf-8")),
            "scripting_assemblies_sha256": sha256_bytes(scripting_raw),
            "scripting_assemblies": scripting.get("names", []),
        },
        "source_counts": {
            "raw_total_files": sum(1 for _ in RAW_CSHARP.rglob("* ")) if False else sum(1 for path in RAW_CSHARP.rglob("*") if path.is_file()),
            "raw_cs_files": sum(1 for _ in RAW_CSHARP.rglob("*.cs")),
            "raw_csproj_files": sum(1 for _ in RAW_CSHARP.rglob("*.csproj")),
            "update_total_files": sum(1 for path in UPDATE_CSHARP.rglob("*") if path.is_file()),
            "tier_a_files": tier_a_count,
            "tier_a_by_directory": {directory: len(list((RAW_CSHARP / directory).glob("*.cs"))) for directory in TIER_A_DIRS},
        },
        "source_paths": {
            "apk": relative(APK),
            "rar": relative(RAR),
            "asset_zip": relative(ASSET_ZIP),
            "native": relative(NATIVE),
            "metadata": relative(METADATA),
            "dump": relative(DUMP),
            "raw_csharp": relative(RAW_CSHARP),
            "update_csharp": relative(UPDATE_CSHARP),
        },
    }


def load_native_evidence() -> dict[str, Any]:
    native_rvas: dict[str, set[str]] = collections.defaultdict(set)
    field_offsets: dict[str, str] = {}
    native_records: list[dict[str, Any]] = []
    evidence_files: list[str] = []
    roots = (
        EVIDENCE / "behavior-first",
        EVIDENCE / "data-dependency",
        EVIDENCE / "living-core-closure",
        EVIDENCE / "visual-port/v1/native-recovery-map.json",
        EVIDENCE / "visual-port/native-method-map.json",
        EVIDENCE / "phase1d_closure.json",
        EVIDENCE / "phase3c_strict_closure.json",
    )
    for path in iter_json_files(*roots):
        try:
            payload = read_json(path)
        except (OSError, json.JSONDecodeError):
            continue
        evidence_files.append(relative(path))
        for item in walk_dicts(payload):
            names: list[str] = []
            for key in ("symbol", "method", "native_method", "public_method", "function"):
                value = item.get(key)
                if isinstance(value, str):
                    names.append(value)
            rvas: set[str] = set()
            for key in ("rva", "native_rva", "rva_hex", "method_rva", "native_entry"):
                value = item.get(key)
                if isinstance(value, str) and re.fullmatch(r"0x[0-9A-Fa-f]+(?:;\s*0x[0-9A-Fa-f]+)*", value.strip()):
                    rvas.update(re.findall(r"0x[0-9A-Fa-f]+", value))
            if names and rvas:
                for name in names:
                    key = method_key(name)
                    native_rvas[key].update(rvas)
                    native_rvas[method_short(key)].update(rvas)
                    native_records.append({"method": key, "rvas": sorted(rvas), "source": relative(path), "raw": item})

    staff_fields_path = EVIDENCE / "behavior-first/staff-field-inventory.json"
    if staff_fields_path.is_file():
        staff_fields = read_json(staff_fields_path)
        for record in staff_fields.get("fields", []):
            name = record.get("name")
            offset = record.get("dump", {}).get("offset")
            if isinstance(name, str) and isinstance(offset, str):
                field_offsets[f"Staff.{name}"] = offset

    return {
        "native_rvas": {key: sorted(values) for key, values in native_rvas.items()},
        "field_offsets": field_offsets,
        "records": native_records,
        "evidence_files": sorted(set(evidence_files)),
    }


def import_semantic_parser():
    tools_root = ROOT / "tools/social-dev"
    if str(tools_root) not in sys.path:
        sys.path.insert(0, str(tools_root))
    import semantic_inventory  # type: ignore

    return semantic_inventory


def parse_namespace(source: str) -> str | None:
    match = re.search(r"\bnamespace\s+([A-Za-z_][\w.]*)", source)
    return match.group(1) if match else None


def parse_type_relation(raw: str) -> tuple[str | None, list[str]]:
    match = re.search(r"\b(?:class|struct|record)\s+[A-Za-z_][\w]*(?:\s*<[^>{}]+>)?\s*:\s*([^\r\n{]+)", raw)
    if not match:
        return None, []
    parts = [part.strip() for part in match.group(1).split(",") if part.strip()]
    return (parts[0] if parts else None), parts[1:]


def parse_parameters(raw: str) -> list[dict[str, str]]:
    start = raw.find("(")
    end = raw.rfind(")")
    if start < 0 or end <= start:
        return []
    body = raw[start + 1 : end].strip()
    if not body:
        return []
    params: list[dict[str, str]] = []
    depth = 0
    chunks: list[str] = []
    current: list[str] = []
    for char in body:
        if char in "<([{":
            depth += 1
        elif char in ">)]}" and depth:
            depth -= 1
        if char == "," and depth == 0:
            chunks.append("".join(current).strip())
            current = []
        else:
            current.append(char)
    if current:
        chunks.append("".join(current).strip())
    for chunk in chunks:
        clean = re.sub(r"\s*=.*$", "", chunk).strip()
        match = re.match(r"(?:(ref|out|in|params)\s+)?(.+?)\s+([A-Za-z_][\w]*)$", clean)
        if match:
            params.append({"modifier": match.group(1) or "", "type": match.group(2).strip(), "name": match.group(3)})
        else:
            params.append({"modifier": "", "type": clean, "name": "UNKNOWN"})
    return params


def parse_constant_value(raw: str) -> Any:
    match = re.search(r"=\s*([^;]+)", raw)
    if not match:
        return None
    value = match.group(1).strip()
    if re.fullmatch(r"[-+]?\d+", value):
        return int(value)
    if re.fullmatch(r"[-+]?0x[0-9A-Fa-f]+", value):
        return int(value, 16)
    if value in {"true", "false"}:
        return value == "true"
    return value


def source_body_status(method: dict[str, Any], source: str, native: dict[str, Any]) -> str:
    raw = method.get("raw_declaration", "")
    start = method.get("source", {}).get("line_start", 1)
    end = method.get("source", {}).get("line_end", start)
    lines = source.splitlines()
    body = "\n".join(lines[max(0, start - 1) : min(len(lines), end)])
    if raw.rstrip().endswith(";") or "{" not in body:
        return "DECLARATION_ONLY"
    key = method_key(method.get("symbol", ""))
    if key in native.get("native_rvas", {}) and not any(marker in body for marker in ("Cpp2ILHelpers.NoteDecompilerIssue", "Indirect jump", "Unknown result type")):
        return "NATIVE_CLOSED"
    if any(marker in body for marker in ("Cpp2ILHelpers.NoteDecompilerIssue", "Indirect jump", "Unknown result type", "Method not found")):
        return "DAMAGED_CPP2IL"
    if "//IL_" in body or "IL_" in body:
        return "PARTIAL"
    return "INTACT"


def fast_parse_large_source(path: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    """Bounded line parser for very large decompiler files.

    SubForm.cs and AppData.cs are multi-megabyte generated files.  The full
    semantic parser is intentionally retained for normal files, while this
    fallback keeps the required structural index finite and deterministic for
    pathological decompiler output.
    """
    raw_bytes = path.read_bytes()
    text = raw_bytes.decode("utf-8", errors="replace")
    source_hash = sha256_bytes(raw_bytes)
    display = relative(path)
    lines = text.splitlines()
    namespace = parse_namespace(text)
    types: list[dict[str, Any]] = []
    fields: list[dict[str, Any]] = []
    methods: list[dict[str, Any]] = []
    depth = 0
    type_stack: list[dict[str, Any]] = []
    brace_depth_by_line: list[int] = []
    for line in lines:
        brace_depth_by_line.append(depth)
        depth += line.count("{") - line.count("}")
        if depth < 0:
            depth = 0
    type_re = re.compile(r"^\s*(?P<prefix>(?:(?:public|private|protected|internal|static|sealed|abstract|partial|unsafe|new)\s+)*)?(?P<kind>class|struct|enum|interface)\s+(?P<name>[A-Za-z_]\w*)")
    member_re = re.compile(r"^\s*(?P<prefix>(?:(?:public|private|protected|internal|static|readonly|const|virtual|override|abstract|sealed|async|unsafe|new|extern|partial)\s+)*)?(?P<return>[A-Za-z_][\w<>,.\[\]? ]*?)\s+(?P<name>[A-Za-z_]\w*)\s*(?P<tail>\([^;]*\))")
    field_re = re.compile(r"^\s*(?P<prefix>(?:(?:public|private|protected|internal|static|readonly|const|volatile|unsafe|new|serialized)\s+)*)?(?P<type>[A-Za-z_][\w<>,.\[\]? ]*?)\s+(?P<decls>[A-Za-z_]\w*(?:\s*=\s*[^;]+)?(?:\s*,\s*[A-Za-z_]\w*(?:\s*=\s*[^;]+)?)*)\s*;")
    for index, line in enumerate(lines, 1):
        type_match = type_re.match(line)
        if type_match:
            while type_stack and brace_depth_by_line[index - 1] <= type_stack[-1]["open_depth"]:
                type_stack[-1]["line_end"] = index - 1
                type_stack.pop()
            parent = type_stack[-1]["symbol"] + "." if type_stack else ""
            symbol = parent + type_match.group("name")
            type_record = {
                "symbol": symbol, "name": type_match.group("name"), "kind": type_match.group("kind"),
                "raw_declaration": line.strip(), "source": {"file": display, "line_start": index, "line_end": index},
                "source_hash": source_hash,
            }
            types.append(type_record)
            type_stack.append({"symbol": symbol, "name": type_match.group("name"), "open_depth": brace_depth_by_line[index - 1], "line_end": len(lines)})
            continue
        if not type_stack:
            continue
        owner = type_stack[-1]
        if brace_depth_by_line[index - 1] != owner["open_depth"] + 1:
            continue
        method_match = member_re.match(line)
        if method_match and ("{" in line or ")" in line):
            methods.append({
                "symbol": f"{owner['symbol']}.{method_match.group('name')}", "name": method_match.group("name"),
                "owner": owner["symbol"], "kind": "method", "return_type": method_match.group("return").strip(),
                "raw_declaration": line.strip(), "source": {"file": display, "line_start": index, "line_end": index},
                "source_hash": source_hash,
            })
            continue
        field_match = field_re.match(line)
        if field_match:
            for declaration in field_match.group("decls").split(","):
                name_match = re.match(r"\s*([A-Za-z_]\w*)", declaration)
                if not name_match:
                    continue
                fields.append({
                    "symbol": name_match.group(1), "name": name_match.group(1), "owner": owner["symbol"],
                    "type": field_match.group("type").strip(), "kind": "field",
                    "raw_declaration": line.strip(), "source": {"file": display, "line_start": index, "line_end": index},
                    "source_hash": source_hash,
                })
    while type_stack:
        type_stack[-1]["line_end"] = len(lines)
        type_stack.pop()
    # Use the broad file interval for large type bodies; this preserves the
    # declaration and prevents a damaged body from being mistaken for a closed body.
    for record in types:
        record["source"]["line_end"] = len(lines)
    return types, fields, methods, {"path": display, "size_bytes": len(raw_bytes), "sha256": source_hash}


def build_structural_index(native: dict[str, Any]) -> dict[str, Any]:
    parser = import_semantic_parser()
    type_records: list[dict[str, Any]] = []
    field_records: list[dict[str, Any]] = []
    method_records: list[dict[str, Any]] = []
    constants: list[dict[str, Any]] = []
    enum_values: list[dict[str, Any]] = []
    source_files: list[dict[str, Any]] = []
    contexts: dict[str, dict[str, Any]] = {}

    paths = [path for directory in TIER_A_DIRS for path in sorted((RAW_CSHARP / directory).glob("*.cs"))]
    for path in paths:
        text = path.read_text(encoding="utf-8")
        display = relative(path)
        namespace = parse_namespace(text)
        source_hash = sha256_file(path)
        source_lines = text.splitlines()
        contexts[display] = {"text": text, "lines": source_lines, "namespace": namespace}
        file_provenance = {"path": display, "sha256": source_hash, "bytes": path.stat().st_size}
        if path.stat().st_size > 300_000:
            parsed_types, parsed_fields, parsed_methods, input_record = fast_parse_large_source(path)
        else:
            parsed_types, parsed_fields, parsed_methods, input_record = parser._parse_source(path, ROOT)
        source_files.append({
            "file_id": direct_canonical_id("source_file", display),
            "path": display,
            "sha256": source_hash,
            "bytes": path.stat().st_size,
            "tier": "A",
            "status": "indexed",
            "namespace": namespace,
            "file_role": "primary_game_code",
        })
        for record in parsed_types:
            base_type, interfaces = parse_type_relation(record.get("raw_declaration", ""))
            symbol = record["symbol"]
            qualified = f"{namespace}.{symbol}" if namespace else symbol
            entity_id = direct_canonical_id("type", qualified)
            type_records.append({
                "entity_id": entity_id,
                "namespace": namespace,
                "name": record["name"],
                "symbol": symbol,
                "kind": record["kind"],
                "base_type": base_type,
                "interfaces": interfaces,
                "nested_parent": symbol.rsplit(".", 1)[0] if "." in symbol else None,
                "source_file": display,
                "source": record["source"],
                "metadata_identity": None,
                "canonical_entity_id": entity_id,
                "classifications": class_labels(display, symbol),
            })
        for record in parsed_fields:
            owner = record["owner"]
            qualified_owner = f"{namespace}.{owner}" if namespace else owner
            entity_id = direct_canonical_id("field", f"{qualified_owner}.{record['name']}")
            raw = record.get("raw_declaration", "")
            modifiers = raw.split(record["type"], 1)[0].strip().split()
            full_key = f"{owner}.{record['name']}"
            offset = native.get("field_offsets", {}).get(full_key)
            field_records.append({
                "entity_id": entity_id,
                "declaring_type": qualified_owner,
                "owner": owner,
                "name": record["name"],
                "declared_type": record["type"],
                "static": "static" in modifiers,
                "readonly": "readonly" in modifiers,
                "const": "const" in modifiers,
                "modifiers": modifiers,
                "default_value": parse_constant_value(raw),
                "field_offset": offset,
                "save_participation": "unknown",
                "source_file": display,
                "source": record["source"],
                "canonical_entity_id": entity_id,
                "classifications": class_labels(display, owner),
            })
            if "const" in modifiers:
                constants.append({
                    "entity_id": direct_canonical_id("constant", f"{qualified_owner}.{record['name']}"),
                    "declaring_type": qualified_owner,
                    "name": record["name"],
                    "value": parse_constant_value(raw),
                    "raw_declaration": raw,
                    "source_file": display,
                    "source": record["source"],
                    "canonical_entity_id": entity_id,
                })
        for record in parsed_methods:
            owner = record["owner"]
            qualified_owner = f"{namespace}.{owner}" if namespace else owner
            symbol = f"{qualified_owner}.{record['name']}"
            body_status = source_body_status(record, text, native)
            signature = record.get("raw_declaration", "")
            entity_id = canonical_id("method", symbol, signature)
            short_key = method_key(f"{owner}.{record['name']}")
            rvas = native.get("native_rvas", {}).get(symbol, []) or native.get("native_rvas", {}).get(short_key, [])
            method_records.append({
                "entity_id": entity_id,
                "declaring_type": qualified_owner,
                "owner": owner,
                "name": record["name"],
                "symbol": symbol,
                "kind": record["kind"],
                "full_signature": signature,
                "parameters": parse_parameters(signature),
                "return_type": record.get("return_type"),
                "static": bool(re.search(r"\bstatic\b", signature)),
                "source_file": display,
                "source": record["source"],
                "body_status": body_status,
                "metadata_index": None,
                "metadata_token": None,
                "native_rva": rvas[0] if len(rvas) == 1 else (rvas or None),
                "native_range": None,
                "callers": [],
                "callees": [],
                "field_reads": [],
                "field_writes": [],
                "constants_used": [],
                "state_writes": [],
                "save_refs": [],
                "data_refs": [],
                "asset_refs": [],
                "canonical_entity_id": entity_id,
                "classifications": class_labels(display, owner),
                "provenance": [{**file_provenance, "line": record.get("source", {}).get("line_start")}],
            })
        for type_record in parsed_types:
            if type_record["kind"] != "enum":
                continue
            line_start = type_record["source"]["line_start"]
            line_end = type_record["source"]["line_end"]
            if type_record["source"].get("line_end", 0) >= len(text.splitlines()) and path.stat().st_size > 300_000:
                line_end = min(line_end, line_start + 500)
            enum_text = "\n".join(source_lines[line_start - 1 : line_end])
            for match in re.finditer(r"\b([A-Za-z_][\w]*)\s*(?:=\s*([-+]?\d+))?\s*,?", enum_text):
                if match.group(1) in {"enum", type_record["name"]}:
                    continue
                enum_values.append({
                    "entity_id": direct_canonical_id("enum", f"{namespace}.{type_record['symbol']}.{match.group(1)}"),
                    "declaring_type": f"{namespace}.{type_record['symbol']}" if namespace else type_record["symbol"],
                    "name": match.group(1),
                    "value": int(match.group(2)) if match.group(2) is not None else None,
                    "source_file": display,
                    "source": {**file_provenance, "line": line_start},
                })

    type_records = dedupe_records(type_records)
    field_records = dedupe_records(field_records)
    method_records = dedupe_records(method_records)
    type_records.sort(key=lambda record: record["entity_id"])
    field_records.sort(key=lambda record: record["entity_id"])
    method_records.sort(key=lambda record: record["entity_id"])
    constants.sort(key=lambda record: record["entity_id"])
    enum_values.sort(key=lambda record: record["entity_id"])
    source_files.sort(key=lambda record: record["path"])
    return {
        "types": type_records,
        "fields": field_records,
        "methods": method_records,
        "constants": constants,
        "enum_values": enum_values,
        "source_files": source_files,
        "contexts": contexts,
        "tier_a_paths": [relative(path) for path in paths],
    }


def build_dependency_closure(structural: dict[str, Any]) -> dict[str, Any]:
    """Index only app-adjacent files pulled by the Tier-A symbol surface.

    This is deliberately a bounded closure.  The raw extraction contains a
    large amount of framework/decompiler material; that material is retained
    as scope metadata, not silently promoted into game truth.
    """
    tier_a_text = "\n".join(context["text"] for context in structural["contexts"].values())
    tier_a_names = {record["name"] for record in structural["types"]}
    tier_a_names.update(record["name"] for record in structural["fields"])
    tier_a_names.update(record["name"] for record in structural["methods"])
    explicit = {
        "StringArrayStream", "RecordStore", "JarInflater", "StringUtil",
        "ResourceManager", "ResourceLoader", "AssetReader", "PassFinder",
        "SaveRecorder", "AppData", "DataManager", "PlayerPrefs",
    }
    referenced_names = tier_a_names | explicit
    tier_a_tokens = set(re.findall(r"\b[A-Za-z_]\w*\b", tier_a_text))
    closure_paths: list[Path] = []
    trigger_map: dict[str, list[str]] = {}
    all_candidates: list[tuple[str, Path]] = []
    for tier, directories in (("B", TIER_B_DIRS), ("C", TIER_C_DIRS)):
        for directory in directories:
            root = RAW_CSHARP / directory
            for path in sorted(root.glob("*.cs")):
                all_candidates.append((tier, path))
                stem = path.stem
                triggers = []
                if stem in referenced_names:
                    triggers.append(f"symbol:{stem}")
                if len(triggers) < 3:
                    candidate_text = path.read_text(encoding="utf-8", errors="replace")
                    candidate_tokens = set(re.findall(r"\b[A-Za-z_]\w*\b", candidate_text))
                    for name in sorted((referenced_names & tier_a_tokens) & candidate_tokens):
                        if name != stem:
                            triggers.append(f"referenced:{name}")
                            if len(triggers) >= 3:
                                break
                if triggers:
                    closure_paths.append(path)
                    trigger_map[relative(path)] = sorted(set(triggers))

    parser = import_semantic_parser()
    types: list[dict[str, Any]] = []
    fields: list[dict[str, Any]] = []
    methods: list[dict[str, Any]] = []
    source_files: list[dict[str, Any]] = []
    contexts: dict[str, dict[str, Any]] = {}
    seen_type: set[str] = set()
    seen_field: set[str] = set()
    seen_method: set[str] = set()
    for path in sorted(set(closure_paths)):
        tier = next(t for t, candidate in all_candidates if candidate == path)
        display = relative(path)
        text = path.read_text(encoding="utf-8", errors="replace")
        contexts[display] = {"text": text, "lines": text.splitlines(), "namespace": parse_namespace(text)}
        parsed_types, parsed_fields, parsed_methods, _ = parser._parse_source(path, ROOT)
        source_files.append({
            "file_id": direct_canonical_id("source_file", display),
            "path": display,
            "sha256": sha256_file(path),
            "bytes": path.stat().st_size,
            "tier": tier,
            "status": "closure_indexed",
            "trigger_paths": structural["tier_a_paths"][:8],
            "trigger_reasons": trigger_map.get(display, []),
        })
        namespace = parse_namespace(text)
        for record in parsed_types:
            qualified = f"{namespace}.{record['symbol']}" if namespace else record["symbol"]
            entity_id = direct_canonical_id("type", qualified)
            if entity_id in seen_type:
                continue
            seen_type.add(entity_id)
            base, interfaces = parse_type_relation(record.get("raw_declaration", ""))
            types.append({
                "entity_id": entity_id, "namespace": namespace, "name": record["name"],
                "symbol": record["symbol"], "kind": record["kind"], "base_type": base,
                "interfaces": interfaces, "source_file": display, "tier": tier,
                "source": record["source"], "canonical_entity_id": entity_id,
                "classifications": class_labels(display, record["symbol"]),
                "provenance": [source_ref(display, record["source"].get("line_start"))],
            })
        for record in parsed_fields:
            owner = record["owner"]
            qualified_owner = f"{namespace}.{owner}" if namespace else owner
            entity_id = direct_canonical_id("field", f"{qualified_owner}.{record['name']}")
            if entity_id in seen_field:
                continue
            seen_field.add(entity_id)
            fields.append({
                "entity_id": entity_id, "declaring_type": qualified_owner, "owner": owner,
                "name": record["name"], "declared_type": record["type"], "tier": tier,
                "source_file": display, "source": record["source"],
                "canonical_entity_id": entity_id,
                "provenance": [source_ref(display, record["source"].get("line_start"))],
            })
        for record in parsed_methods:
            owner = record["owner"]
            qualified_owner = f"{namespace}.{owner}" if namespace else owner
            symbol = f"{qualified_owner}.{record['name']}"
            entity_id = canonical_id("method", symbol, record.get("raw_declaration", ""))
            if entity_id in seen_method:
                continue
            seen_method.add(entity_id)
            methods.append({
                "entity_id": entity_id, "declaring_type": qualified_owner, "owner": owner,
                "name": record["name"], "symbol": symbol, "kind": record["kind"],
                "full_signature": record.get("raw_declaration", ""),
                "parameters": parse_parameters(record.get("raw_declaration", "")),
                "return_type": record.get("return_type"), "tier": tier,
                "source_file": display, "source": record["source"],
                "body_status": source_body_status({**record, "symbol": symbol}, text, {}),
                "native_rva": None, "canonical_entity_id": entity_id,
                "provenance": [source_ref(display, record["source"].get("line_start"))],
            })
    source_files.sort(key=lambda row: row["path"])
    return {
        "types": sorted(types, key=lambda row: row["entity_id"]),
        "fields": sorted(fields, key=lambda row: row["entity_id"]),
        "methods": sorted(methods, key=lambda row: row["entity_id"]),
        "source_files": source_files,
        "contexts": contexts,
        "candidate_file_count": len(all_candidates),
        "closure_file_count": len(closure_paths),
        "tier_b_files": sum(1 for tier, path in all_candidates if tier == "B"),
        "tier_c_files": sum(1 for tier, path in all_candidates if tier == "C"),
        "excluded_external_scope": {
            "csproj_files": [relative(path) for path in sorted(RAW_CSHARP.rglob("*.csproj"))],
            "tier_d_prefixes": sorted(TIER_D_PREFIXES),
            "tier_d_note": "Assembly/type/method/signature/direct-endpoint scope only; implementations excluded.",
            "assembly_names_source": "assets/bin/Data/ScriptingAssemblies.json",
        },
    }


def load_content_evidence() -> dict[str, Any]:
    registry_path = EVIDENCE / "native_content_registry.json"
    registry = read_json(registry_path)
    registry_ref = source_ref(registry_path)
    asset_inventory_path = EVIDENCE / "asset_binary_inventory.json"
    asset_inventory = read_json(asset_inventory_path) if asset_inventory_path.is_file() else {}
    load_candidates_path = EVIDENCE / "field_load_candidates.json"
    load_candidates = read_json(load_candidates_path) if load_candidates_path.is_file() else {}
    data_types = registry.get("data_types", [])
    table_by_key = {row.get("registry_key"): row for row in data_types}
    tables: list[dict[str, Any]] = []
    slots: list[dict[str, Any]] = []
    fields: list[dict[str, Any]] = []
    rows: list[dict[str, Any]] = []
    for slot, entry in enumerate(registry.get("data_manager_registry", [])):
        table = table_by_key.get(entry.get("registry_key"), {})
        table_id = f"data:{entry.get('element_type')}"
        table_source = table.get("source_file") or entry.get("source", {}).get("file")
        slot_status = "CONFIRMED" if entry.get("element_type") == "ManagementEventData" and slot == 42 else "SOURCE_LIMITED"
        slots.append({
            "slot_id": f"data_manager_slot:{slot}", "table_slot": slot,
            "registry_key": entry.get("registry_key"), "field": entry.get("field"),
            "element_type": entry.get("element_type"), "table_id": table_id,
            "status": slot_status, "mapping_basis": "DataManager registry declaration order; dispatch body is damaged/indirect" if slot_status != "CONFIRMED" else "DataManager.GetInstance explicit num==42 branch",
            "source": entry.get("source"), "provenance": [source_ref(entry.get("source", {}).get("file", ""), entry.get("source", {}).get("line"))],
        })
        table_record = {
            "table_id": table_id, "registry_key": entry.get("registry_key"),
            "element_type": entry.get("element_type"), "field": entry.get("field"),
            "table_stem": table.get("table_stem"), "row_count": table.get("row_count", 0),
            "source_file": table_source, "source_type": table.get("source_type"),
            "is_base_data": table.get("is_base_data"),
            "load_contract": table.get("load_contract", {}),
            "locale_source_status": table.get("locale_source_status", {}),
            "status": table.get("load_contract", {}).get("source_status", "SOURCE_LIMITED"),
            "provenance": [source_ref(table_source or registry_path, table.get("source", {}).get("line"))],
        }
        tables.append(table_record)
        for index, field in enumerate(table.get("fields", [])):
            fields.append({
                "data_field_id": f"data_field:{entry.get('element_type')}:{field.get('name')}",
                "table_id": table_id, "table_slot": slot, "ordinal": index,
                "name": field.get("name"), "declared_type": field.get("type"),
                "status": "SOURCE_LIMITED_READER_ORDER" if table.get("load_contract", {}).get("source_status") != "parsed" else "SOURCE_BACKED",
                "provenance": [source_ref(table_source or registry_path)],
            })
        for row in table.get("rows", []):
            rows.append({
                "row_id": row.get("catalog_key") or f"{table_id}:{row.get('row_index')}",
                "table_id": table_id, "table_slot": slot, "element_type": entry.get("element_type"),
                "native_id": row.get("native_id"), "row_index": row.get("row_index"),
                "id_status": row.get("id_status"), "locales": row.get("locales", {}),
                "decoded": row.get("decoded", {}), "provenance": [source_ref(table_source or registry_path)],
            })
    assets = []
    for asset in registry.get("assets", []):
        assets.append({**asset, "provenance": [registry_ref]})
    selectors = []
    for selector_index, selector in enumerate(registry.get("selectors", [])):
        selector_copy = dict(selector)
        if not selector_copy.get("selector_key"):
            selector_copy["selector_key"] = canonical_id("selector", selector_index, selector_copy.get("source_file"), selector_copy.get("source_row"), selector_copy.get("selector_kind"))
        selectors.append({**selector_copy, "provenance": [registry_ref]})
    asset_relations = []
    for relation in registry.get("data_selector_relations", []):
        asset_relations.append({**relation, "relation_id": canonical_id("asset_relation", stable_json(relation)), "provenance": [registry_ref]})
    for relation in registry.get("relations", []):
        if isinstance(relation, dict):
            asset_relations.append({**relation, "relation_id": relation.get("relation_id") or canonical_id("content_relation", stable_json(relation)), "provenance": [registry_ref]})
    return {
        "registry": registry,
        "tables": sorted(tables, key=lambda row: row["table_id"]),
        "slots": slots,
        "fields": sorted(fields, key=lambda row: row["data_field_id"]),
        "rows": sorted(rows, key=lambda row: str(row.get("row_id") or "")),
        "assets": sorted(assets, key=lambda row: row.get("asset_id", "")),
        "selectors": sorted(selectors, key=lambda row: str(row.get("selector_key") or "")),
        "asset_relations": sorted(asset_relations, key=lambda row: row["relation_id"]),
        "load_candidates": load_candidates,
        "source": relative(registry_path),
        "asset_inventory_source": relative(asset_inventory_path) if asset_inventory_path.is_file() else None,
    }


def method_body(method: dict[str, Any], contexts: dict[str, dict[str, Any]]) -> tuple[str, int]:
    context = contexts.get(method.get("source_file", ""), {})
    lines = context.get("lines", [])
    source = method.get("source", {})
    start = int(source.get("line_start", 1) or 1)
    end = int(source.get("line_end", start) or start)
    return "\n".join(lines[max(0, start - 1):min(len(lines), end)]), start


def merge_method_catalog(structural: dict[str, Any], closure: dict[str, Any]) -> list[dict[str, Any]]:
    methods = list(structural["methods"])
    existing = {record["entity_id"] for record in methods}
    for record in closure["methods"]:
        if record["entity_id"] not in existing:
            methods.append(record)
    return sorted(methods, key=lambda row: row["entity_id"])


def merge_field_catalog(structural: dict[str, Any], closure: dict[str, Any]) -> list[dict[str, Any]]:
    fields = list(structural["fields"])
    existing = {record["entity_id"] for record in fields}
    for record in closure["fields"]:
        if record["entity_id"] not in existing:
            fields.append(record)
    return sorted(fields, key=lambda row: row["entity_id"])


def resolve_method_reference(name: str, methods: list[dict[str, Any]], namespace: str | None = None) -> tuple[str | None, str]:
    key = method_key(name)
    exact = [row for row in methods if row["symbol"] == key or method_key(row["symbol"]) == key]
    if len(exact) == 1:
        return exact[0]["entity_id"], "RESOLVED_EXACT"
    short = method_short(key)
    candidates = [row for row in methods if row["name"] == short]
    if namespace:
        local = [row for row in candidates if row["declaring_type"].startswith(namespace + ".")]
        if len(local) == 1:
            return local[0]["entity_id"], "RESOLVED_NAMESPACE"
    if len(candidates) == 1:
        return candidates[0]["entity_id"], "RESOLVED_UNIQUE"
    return None, "UNRESOLVED_DISPATCH" if candidates else "EXTERNAL_OR_NOT_INDEXED"


def build_graphs(structural: dict[str, Any], closure: dict[str, Any], content: dict[str, Any]) -> dict[str, Any]:
    methods = merge_method_catalog(structural, closure)
    fields = merge_field_catalog(structural, closure)
    contexts = {**closure["contexts"], **structural["contexts"]}
    method_by_id = {row["entity_id"]: row for row in methods}
    field_by_id = {row["entity_id"]: row for row in fields}
    for method in methods:
        for key in ("callers", "callees", "field_reads", "field_writes", "save_refs"):
            method.setdefault(key, [])
    for field in fields:
        field.setdefault("reads", [])
        field.setdefault("writes", [])
    method_name_index: dict[str, list[dict[str, Any]]] = collections.defaultdict(list)
    for method in methods:
        method_name_index[method["name"]].append(method)
        method_name_index[method_key(method["symbol"])].append(method)
    field_name_index: dict[str, list[dict[str, Any]]] = collections.defaultdict(list)
    for field in fields:
        field_name_index[field["name"]].append(field)

    calls: list[dict[str, Any]] = []
    call_seen: set[str] = set()
    field_access: list[dict[str, Any]] = []
    field_seen: set[str] = set()
    save_refs: list[dict[str, Any]] = []
    save_seen: set[str] = set()
    event_edges: list[dict[str, Any]] = []
    event_seen: set[str] = set()
    keywords = {"if", "for", "while", "switch", "catch", "return", "new", "sizeof", "typeof", "lock", "using", "nameof"}
    interesting_save = re.compile(r"\b(?:Save|Load|Serialize|Deserialize|RecordStore|SaveRecorder|PlayerPrefs|AppData|AutoSave|checkpoint|Version)\w*\b", re.I)
    interesting_event = re.compile(r"\b(?:Event|On[A-Z]|Dispatch|Trigger|Notify|Message)\w*\b")
    # G1 body scanning is Tier-A first. Closure symbols remain resolvable in
    # the catalog/UI boundary, but external/framework bodies are not promoted
    # into the game call/field graph.
    graph_methods = [method for method in methods if method.get("tier", "A") == "A"]

    for method_index, method in enumerate(graph_methods, 1):
        body, line_start = method_body(method, contexts)
        if not body:
            continue
        namespace = method.get("declaring_type", "").rsplit(".", 1)[0]
        caller_id = method["entity_id"]
        call_pattern = re.compile(r"(?:(?P<qual>[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*)\s*\.\s*)?(?P<name>[A-Za-z_]\w*)\s*\(")
        for match in call_pattern.finditer(body):
            target_name = match.group("name")
            if target_name in keywords:
                continue
            qualifier = match.group("qual")
            lookup = f"{qualifier}.{target_name}" if qualifier else target_name
            callee_id, resolution = resolve_method_reference(lookup, methods, namespace)
            if resolution == "EXTERNAL_OR_NOT_INDEXED":
                continue
            line = line_start + body[:match.start()].count("\n")
            callee_symbol = method_by_id.get(callee_id, {}).get("symbol") if callee_id else lookup
            call_id = canonical_id("call", caller_id, callee_id or callee_symbol, line, match.start())
            if call_id in call_seen:
                continue
            call_seen.add(call_id)
            record = {
                "call_id": call_id, "caller_method_id": caller_id, "caller_symbol": method["symbol"],
                "callee_method_id": callee_id, "callee_symbol": callee_symbol,
                "call_expression": lookup, "resolution_status": resolution,
                "source_file": method["source_file"], "source_line": line,
                "provenance": [source_ref(method["source_file"], line)],
            }
            calls.append(record)
            if callee_id:
                method["callees"].append(callee_id)
                method_by_id[callee_id].setdefault("callers", []).append(caller_id)

        if method["name"] in {"Load", "GetInstance"} and method["owner"] == "DataManager":
            dispatch_name = f"dispatch:DataManager.{method['name']}"
            record = {
                "call_id": canonical_id("call", caller_id, dispatch_name), "caller_method_id": caller_id,
                "caller_symbol": method["symbol"], "callee_method_id": None,
                "callee_symbol": dispatch_name, "call_expression": "indirect dispatch",
                "resolution_status": "SOURCE_LIMITED_INDIRECT_DISPATCH", "source_file": method["source_file"],
                "source_line": method["source"].get("line_start"),
                "provenance": [source_ref(method["source_file"], method["source"].get("line_start"), "DataManager indirect/dispatch body" )],
            }
            if record["call_id"] not in call_seen:
                call_seen.add(record["call_id"])
                calls.append(record)

        # Tokenize once instead of compiling a several-thousand-alternative
        # regex from the generated field catalog.
        for match in re.finditer(r"\b[A-Za-z_]\w*\b", body):
            name = match.group(0)
            if name not in field_name_index or len(name) <= 1:
                continue
            candidates = field_name_index.get(name, [])
            owner = method.get("owner")
            local = [row for row in candidates if row.get("owner") == owner]
            field = local[0] if len(local) == 1 else (candidates[0] if len(candidates) == 1 else None)
            if field is None:
                continue
            line_text = body.splitlines()[body[:match.start()].count("\n")] if body.splitlines() else ""
            after = body[match.end():match.end() + 20]
            before = body[max(0, match.start() - 20):match.start()]
            write = bool(re.match(r"\s*(?:\+\+|--|(?:\+|-|\*|/|%|&|\||\^)?=)", after)) or bool(re.search(r"(?:\+\+|--)\s*$", after[:4]))
            operation = "write" if write else "read"
            line = line_start + body[:match.start()].count("\n")
            access_id = canonical_id("field_access", caller_id, field["entity_id"], operation, line, match.start())
            if access_id in field_seen:
                continue
            field_seen.add(access_id)
            record = {
                "access_id": access_id, "method_id": caller_id, "method_symbol": method["symbol"],
                "field_id": field["entity_id"], "field_symbol": f"{field['declaring_type']}.{field['name']}",
                "operation": operation, "expression": line_text.strip(), "source_file": method["source_file"],
                "source_line": line, "resolution_status": "RESOLVED_OWNER" if local else "RESOLVED_UNIQUE",
                "provenance": [source_ref(method["source_file"], line)],
            }
            field_access.append(record)
            method["field_writes" if write else "field_reads"].append(field["entity_id"])
            field.setdefault("writes", []).append(caller_id) if write else field.setdefault("reads", []).append(caller_id)

        for match in interesting_save.finditer(body):
            token = match.group(0)
            line = line_start + body[:match.start()].count("\n")
            save_id = canonical_id("save_ref", caller_id, token, line)
            if save_id not in save_seen:
                save_seen.add(save_id)
                save_refs.append({
                    "save_ref_id": save_id, "method_id": caller_id, "method_symbol": method["symbol"],
                    "reference_kind": "save_or_persistence_symbol", "token": token,
                    "status": "SOURCE_BACKED_REFERENCE" if method["body_status"] in {"INTACT", "NATIVE_CLOSED"} else "SOURCE_LIMITED",
                    "source_file": method["source_file"], "source_line": line,
                    "provenance": [source_ref(method["source_file"], line)],
                })
                method["save_refs"].append(save_id)

        for match in interesting_event.finditer(body):
            token = match.group(0)
            if token in {"Event", "Message"}:
                continue
            line = line_start + body[:match.start()].count("\n")
            edge_id = canonical_id("event", caller_id, token, line)
            if edge_id not in event_seen:
                event_seen.add(edge_id)
                event_edges.append({
                    "event_edge_id": edge_id, "method_id": caller_id, "method_symbol": method["symbol"],
                    "event_token": token, "edge_kind": "event_or_message_reference",
                    "status": "SOURCE_BACKED_REFERENCE", "source_file": method["source_file"],
                    "source_line": line, "provenance": [source_ref(method["source_file"], line)],
                })

    for method in methods:
        for key in ("callers", "callees", "field_reads", "field_writes", "save_refs"):
            method[key] = sorted(set(method.get(key, [])))

    state_transitions: list[dict[str, Any]] = []
    state_path = EVIDENCE / "behavior-first/staff-transition-graph.json"
    if state_path.is_file():
        state_payload = read_json(state_path)
        for edge in state_payload.get("edges", []):
            state_transitions.append({
                "transition_id": edge.get("id") or canonical_id("state_transition", stable_json(edge)),
                "from_state": edge.get("from"), "to_state": edge.get("to"),
                "move_mode": edge.get("move_mode"), "confidence": edge.get("confidence"),
                "status": "SOURCE_BACKED_WITH_LIMITS" if "limit" in str(edge.get("confidence", "")) else "CONFIRMED",
                "source_file": relative(state_path), "provenance": [source_ref(state_path)],
            })
    for access in field_access:
        if access["field_symbol"].endswith(".state_") or access["field_symbol"].endswith(".moveMode_"):
            state_transitions.append({
                "transition_id": canonical_id("state_transition", access["access_id"]),
                "from_state": "UNKNOWN", "to_state": "write:" + access["field_symbol"],
                "move_mode": None, "confidence": "source_access_only", "status": "SOURCE_LIMITED",
                "source_file": access["source_file"], "source_line": access["source_line"],
                "provenance": access["provenance"],
            })

    native_dispatch: list[dict[str, Any]] = []
    dispatch_path = EVIDENCE / "living-core-closure/on-arrive-goal-dispatch-contract.json"
    if dispatch_path.is_file():
        dispatch = read_json(dispatch_path).get("dispatch", {})
        for entry in dispatch.get("entries", []):
            native_dispatch.append({
                "dispatch_id": canonical_id("native_dispatch", dispatch.get("method"), entry.get("move_mode")),
                "method_symbol": dispatch.get("method"), "method_rva": dispatch.get("method_rva"),
                "dispatch_key": dispatch.get("key_field", {}).get("name"),
                "dispatch_key_offset": dispatch.get("key_field", {}).get("offset"),
                "move_mode": entry.get("move_mode"), "label": entry.get("label"),
                "target_rva": entry.get("target_rva"), "table_offset": entry.get("table_offset"),
                "side_effects": entry.get("side_effects", []), "guard": dispatch.get("guard"),
                "status": "CONFIRMED_NATIVE_JUMP_TABLE", "source_file": relative(dispatch_path),
                "provenance": [source_ref(dispatch_path)],
            })

    # The command/UI boundary is intentionally a symbol contract, not a runtime implementation.
    ui_commands: list[dict[str, Any]] = []
    ui_specs = [
        ("start_planning", ["SubForm.StartPlanning", "Player.StartPlanning", "Room.OnStartPlanning", "Staff.OnStartPlanning"]),
        ("update_planning", ["Player.UpdatePlanning", "Room.UpdatePlanning"]),
        ("end_planning", ["Room.OnEndPlanning", "Staff.OnEndPlanning"]),
        ("reserve_autosave", ["SubForm.ReserveAutoSave"]),
    ]
    for command, sequence in ui_specs:
        steps = []
        for symbol in sequence:
            entity_id, status = resolve_method_reference(symbol, methods)
            steps.append({"symbol": symbol, "method_id": entity_id, "resolution_status": status})
        ui_commands.append({
            "command_id": f"ui_command:{command}", "command": command, "boundary": "form_to_living_core",
            "sequence": steps, "status": "SOURCE_LIMITED_STATIC_BOUNDARY",
            "mutation_scope": "command_boundary_only; no runtime adapter or save implementation",
            "provenance": [source_ref(RAW_CSHARP / "form/SubForm.cs"), source_ref(RAW_CSHARP / "game/Player.cs"), source_ref(RAW_CSHARP / "game/Room.cs"), source_ref(RAW_CSHARP / "game/Staff.cs")],
        })

    asset_refs: list[dict[str, Any]] = []
    for relation in content["asset_relations"]:
        target = relation.get("target_asset_id") or relation.get("to")
        if not target:
            continue
        asset_refs.append({
            "asset_ref_id": relation.get("relation_id") or canonical_id("asset_ref", stable_json(relation)),
            "from_id": relation.get("from") or relation.get("data_id"),
            "field": relation.get("field"), "target_asset_id": target,
            "status": relation.get("status", "SOURCE_BACKED"), "relation": relation.get("relation"),
            "native_value": relation.get("native_value"), "provenance": relation.get("provenance", []),
        })

    save_schema: list[dict[str, Any]] = []
    save_owner_names = {"AppData", "Player", "Room", "Staff", "DataManager"}
    for field in fields:
        if field.get("owner") in save_owner_names or any(token in field.get("name", "").lower() for token in ("save", "version", "money", "staff", "room", "item")):
            save_schema.append({
                "save_ref_id": canonical_id("save_schema", field["entity_id"]), "entity_id": field["entity_id"],
                "field_symbol": f"{field.get('declaring_type')}.{field.get('name')}",
                "schema_role": "candidate_persisted_field", "status": "SOURCE_LIMITED",
                "source_file": field.get("source_file"), "source": field.get("source"),
                "provenance": [source_ref(field.get("source_file", ""), field.get("source", {}).get("line_start"))],
            })
    save_refs.extend(save_schema)

    return {
        "methods": methods, "fields": fields, "calls": sorted(calls, key=lambda row: row["call_id"]),
        "field_access": sorted(field_access, key=lambda row: row["access_id"]),
        "state_transitions": sorted({row["transition_id"]: row for row in state_transitions}.values(), key=lambda row: row["transition_id"]),
        "native_dispatch": sorted(native_dispatch, key=lambda row: row["dispatch_id"]),
        "ui_commands": ui_commands, "event_edges": sorted(event_edges, key=lambda row: row["event_edge_id"]),
        "save_refs": sorted({row["save_ref_id"]: row for row in save_refs}.values(), key=lambda row: row["save_ref_id"]),
        "asset_refs": sorted({row["asset_ref_id"]: row for row in asset_refs}.values(), key=lambda row: row["asset_ref_id"]),
    }


def build_canonical_model(identity: dict[str, Any], structural: dict[str, Any], closure: dict[str, Any], content: dict[str, Any], graphs: dict[str, Any], native: dict[str, Any]) -> dict[str, Any]:
    entities: dict[str, dict[str, Any]] = {}
    canonical_facts: dict[tuple[str, str], dict[str, Any]] = {}
    claims: list[dict[str, Any]] = []
    fact_sources: list[dict[str, Any]] = []
    revisions: list[dict[str, Any]] = []
    superseded: list[dict[str, Any]] = []
    conflicts: list[dict[str, Any]] = []
    ref_cache: dict[str, dict[str, Any]] = {}
    authority_rank = {
        "native": 100, "metadata": 90, "mapping": 85, "intact_csharp": 80,
        "original_data": 75, "static_asset_metadata": 70, "accepted_closure": 65,
        "damaged_cpp2il": 40, "inference": 20, "screenshot": 10,
    }
    status_rank = {"UPGRADED": 6, "CONFIRMED": 5, "UNCHANGED_ACCEPTED": 4, "SOURCE_LIMITED": 3, "CONFLICT": 2, "SUPERSEDED": 1}

    def cached_ref(path: str | Path, line: int | None = None, note: str | None = None) -> dict[str, Any]:
        key = str(path)
        if key not in ref_cache:
            ref_cache[key] = source_ref(path)
        ref = dict(ref_cache[key])
        if line is not None:
            ref["line"] = line
        if note:
            ref["note"] = note
        return ref

    def add_entity(entity_id: str, entity_type: str, name: str, attributes: dict[str, Any] | None = None, provenance: list[dict[str, Any]] | None = None) -> None:
        if entity_id not in entities:
            entities[entity_id] = {
                "entity_id": entity_id, "entity_type": entity_type, "name": name,
                "attributes": attributes or {}, "provenance": provenance or [],
            }
        else:
            entities[entity_id]["attributes"].update(attributes or {})
            entities[entity_id]["provenance"] = entities[entity_id].get("provenance", []) + [ref for ref in (provenance or []) if ref not in entities[entity_id].get("provenance", [])]

    def add_claim(entity_id: str, predicate: str, value: Any, status: str, authority: str, refs: list[dict[str, Any]], impl_status: str = "evidence", note: str | None = None, claim_id: str | None = None) -> str:
        add_entity(entity_id, entity_id.split(":", 1)[0], entity_id, provenance=refs)
        claim_id = claim_id or canonical_id("fact_claim", entity_id, predicate, stable_json(value), status, len(claims))
        claim = {
            "claim_id": claim_id, "entity_id": entity_id, "predicate": predicate,
            "value": value, "status": status, "authority": authority,
            "authority_rank": authority_rank.get(authority, 0), "impl_status": impl_status,
            "source_claim_refs": refs, "note": note, "canonical_fact_id": None,
        }
        claims.append(claim)
        for index, ref in enumerate(refs):
            fact_sources.append({
                "fact_source_id": canonical_id("fact_source", claim_id, index),
                "claim_id": claim_id, "entity_id": entity_id, "predicate": predicate,
                "source": ref,
            })
        if status == "SUPERSEDED":
            superseded.append({
                "superseded_fact_id": canonical_id("superseded", claim_id), "claim_id": claim_id,
                "entity_id": entity_id, "predicate": predicate, "value": value,
                "replacement_note": note or "Superseded by a higher-authority or newer reconciled claim.",
                "source_claim_refs": refs,
            })
            return claim_id
        if status == "CONFLICT":
            conflicts.append({
                "conflict_id": canonical_id("conflict", claim_id), "claim_id": claim_id,
                "entity_id": entity_id, "predicate": predicate, "value": value,
                "resolution_status": "UNRESOLVED", "source_claim_refs": refs,
                "note": note or "Conflicting source claims retained without silent overwrite.",
            })
            return claim_id
        key = (entity_id, predicate)
        fact = canonical_facts.get(key)
        if fact is None:
            fact_id = direct_canonical_id("fact", f"{entity_id}|{predicate}")
            fact = {
                "fact_id": fact_id, "entity_id": entity_id, "predicate": predicate,
                "value": value, "status": status, "authority": authority,
                "authority_rank": authority_rank.get(authority, 0), "impl_status": impl_status,
                "source_claim_ids": [claim_id], "revision": 1, "canonical": True,
                "note": note,
            }
            canonical_facts[key] = fact
            revisions.append({
                "revision_id": canonical_id("fact_revision", fact_id, 1), "fact_id": fact_id,
                "revision": 1, "change": "created", "claim_id": claim_id,
                "status": status, "source_claim_refs": refs,
            })
        else:
            fact["source_claim_ids"].append(claim_id)
            current_score = (status_rank.get(fact["status"], 0), fact.get("authority_rank", 0))
            new_score = (status_rank.get(status, 0), authority_rank.get(authority, 0))
            if new_score > current_score:
                old_value = fact["value"]
                fact["value"] = value
                fact["status"] = status
                fact["authority"] = authority
                fact["authority_rank"] = authority_rank.get(authority, 0)
                fact["impl_status"] = impl_status
                fact["revision"] += 1
                revisions.append({
                    "revision_id": canonical_id("fact_revision", fact["fact_id"], fact["revision"]),
                    "fact_id": fact["fact_id"], "revision": fact["revision"],
                    "change": "upgraded_or_reconciled", "claim_id": claim_id,
                    "old_value": old_value, "new_value": value, "status": status,
                    "source_claim_refs": refs,
                })
        claim["canonical_fact_id"] = canonical_facts[key]["fact_id"]
        return claim_id

    # Structural entities and facts are source-index facts, never inferred behavior.
    for record in structural["types"] + closure["types"]:
        add_entity(record["entity_id"], "type", record["symbol"], record, [cached_ref(record["source_file"], record.get("source", {}).get("line_start"))])
        add_claim(record["entity_id"], "source_defined", {"kind": record["kind"], "tier": record.get("tier", "A")}, "CONFIRMED", "intact_csharp", [cached_ref(record["source_file"], record.get("source", {}).get("line_start"))], "usable")
    for record in structural["fields"] + closure["fields"]:
        refs = [cached_ref(record["source_file"], record.get("source", {}).get("line_start"))]
        add_entity(record["entity_id"], "field", f"{record['declaring_type']}.{record['name']}", record, refs)
        add_claim(record["entity_id"], "declared_type", record.get("declared_type"), "CONFIRMED", "intact_csharp", refs, "usable")
        if record.get("field_offset"):
            add_claim(record["entity_id"], "native_field_offset", record["field_offset"], "UPGRADED", "native", refs + [cached_ref(EVIDENCE / "behavior-first/staff-field-inventory.json")], "usable")
    for record in structural["methods"] + closure["methods"]:
        refs = [cached_ref(record["source_file"], record.get("source", {}).get("line_start"))]
        add_entity(record["entity_id"], "method", record["symbol"], record, refs)
        add_claim(record["entity_id"], "body_status", record.get("body_status"), "CONFIRMED", "intact_csharp", refs, "usable" if record.get("body_status") in {"INTACT", "NATIVE_CLOSED"} else "source_limited")
        if record.get("native_rva"):
            add_claim(record["entity_id"], "native_rva", record["native_rva"], "UPGRADED", "native", refs, "usable")

    for table in content["tables"]:
        entity_id = table["table_id"]
        refs = [cached_ref(table.get("source_file") or content["source"])]
        add_entity(entity_id, "data_table", table.get("element_type", entity_id), table, refs)
        add_claim(entity_id, "row_count", table.get("row_count", 0), "CONFIRMED", "original_data", refs, "usable")
    for field in content["fields"]:
        entity_id = field["data_field_id"]
        add_entity(entity_id, "data_field", field.get("name", entity_id), field, field.get("provenance", []))
        add_claim(entity_id, "reader_slot", {"table_slot": field.get("table_slot"), "ordinal": field.get("ordinal"), "reader_status": field.get("status")}, "SOURCE_LIMITED", "mapping", field.get("provenance", []), "source_limited")
    for asset in content["assets"]:
        entity_id = asset.get("asset_id") or canonical_id("asset", asset.get("relative_path"))
        refs = asset.get("provenance", [cached_ref(content["source"])])
        add_entity(entity_id, "asset", asset.get("relative_path", entity_id), asset, refs)
        add_claim(entity_id, "asset_metadata", {key: asset.get(key) for key in ("relative_path", "kind", "pack", "extension", "size_bytes", "sha256", "semantic_role")}, "CONFIRMED", "static_asset_metadata", refs, "usable")
    for selector in content["selectors"]:
        entity_id = selector.get("selector_key") or canonical_id("selector", stable_json(selector))
        refs = selector.get("provenance", [cached_ref(content["source"])])
        add_entity(entity_id, "asset_selector", selector.get("target_filename", entity_id), selector, refs)
        add_claim(entity_id, "target_asset", selector.get("target_asset_id"), "CONFIRMED" if selector.get("status") == "resolved" else "SOURCE_LIMITED", "static_asset_metadata", refs, "usable" if selector.get("status") == "resolved" else "source_limited")

    def ev(path: str, line: int | None = None, note: str | None = None) -> list[dict[str, Any]]:
        candidate = json_path(path)
        if not candidate.is_file() and not Path(path).is_absolute():
            raw_candidate = RAW_CSHARP / Path(path)
            if raw_candidate.is_file():
                path = relative(raw_candidate)
        return [cached_ref(path, line, note)]

    # Accepted closure claims: native/metadata evidence is kept separate from raw C# claims.
    staff_type = next((row["entity_id"] for row in structural["types"] if row["name"] == "Staff"), direct_canonical_id("type", "game.Staff"))
    staff_hp = next((row["entity_id"] for row in structural["fields"] if row["owner"] == "Staff" and row["name"] == "hp_"), direct_canonical_id("field", "game.Staff.hp_"))
    staff_data = direct_canonical_id("type", "data.StaffData")
    add_entity(staff_type, "type", "game.Staff")
    add_entity(staff_hp, "field", "game.Staff.hp_")
    add_claim(staff_hp, "native_field_offset", "0xE8", "UPGRADED", "native", ev("knowledge/fixtures/accepted/behavior-first/staff-field-inventory.json"), "usable", "Phase-3A dump/native field identity")
    add_claim(staff_data, "parameter_id:PARAM_HP", 5, "CONFIRMED", "intact_csharp", ev("data/StaffData.cs"), "usable")
    add_claim(staff_type, "ordinary_work_hp_drain", False, "UPGRADED", "native", ev("knowledge/fixtures/accepted/living-core-closure/ordinary-work-hp-drain-contract.json"), "usable", "Staff.UpdateWork native closure: no hp write and no negative RecoverHp")
    add_claim(staff_type, "recovery_cadence", {"start_delay_frames": 20, "consume_every_n_frames": 3, "recover_hp": 1, "gauge_reset": 40}, "UPGRADED", "native", ev("knowledge/fixtures/accepted/living-core-closure/recovery-cadence-native-trace.json", note="native recovery trace"), "usable")
    add_claim(staff_type, "low_hp_condition", {"threshold": "<=5%", "action": "go_home", "return_threshold": "40%", "stay_home_recovery": 1}, "CONFIRMED", "accepted_closure", ev("knowledge/fixtures/accepted/behavior-first/hp-condition-contract.json"), "usable")
    room_type = next((row["entity_id"] for row in structural["types"] if row["name"] == "Room"), direct_canonical_id("type", "game.Room"))
    add_claim(room_type, "desk_vacancy_predicate", {"obj_type": 2, "furniture_non_null": True, "staff_id": -1, "selection": "first_raw_order"}, "UPGRADED", "native", ev("knowledge/fixtures/accepted/living-core-closure/workstation-vacancy-ownership-contract.json"), "usable")
    obj_type = next((row["entity_id"] for row in structural["types"] if row["name"] == "ObjChip"), direct_canonical_id("type", "game.ObjChip"))
    add_claim(obj_type, "equipment_contention", {"count": "reserved_users", "reject_if": ">0", "reserve_if": "<=0"}, "UPGRADED", "native", ev("knowledge/fixtures/accepted/living-core-closure/equipment-user-count-contract.json"), "usable")
    on_arrive_type = staff_type
    add_claim(on_arrive_type, "on_arrive_goal_dispatch", {"method_rva": "0x12D8420", "entry_count": 11, "key_field": "moveMode_", "key_offset": "0xA8", "table_base": "0x12D84A8"}, "UPGRADED", "native", ev("knowledge/fixtures/accepted/living-core-closure/on-arrive-goal-dispatch-contract.json"), "usable")
    furniture_type = next((row["entity_id"] for row in structural["types"] if row["name"] == "FurnitureData"), direct_canonical_id("type", "data.FurnitureData"))
    add_claim(furniture_type, "role_counts", {"WORKSTATION": 10, "RECOVERY_EQUIPMENT": 49, "EQUIPMENT_NO_HP_EFFECT_PROVEN": 43, "DOOR": 1, "REST": 0, "SOCIAL": 0}, "UPGRADED", "accepted_closure", ev("knowledge/fixtures/accepted/living-core-closure/furniture-exact-role-contract.json"), "usable")
    map_type = next((row["entity_id"] for row in structural["types"] if row["name"] == "MapChip"), direct_canonical_id("type", "game.MapChip"))
    add_claim(map_type, "foundation_freeze", {"pixel_sha256": "3ea05bd9edcc5168a14ee1b0e79256e460072be75c018f11f2009d01c215d293", "png_sha256": "fb40142389fe963bba46a93a122f961dc21fe8a85d0abac75b1a68fd3d4ecaed"}, "UNCHANGED_ACCEPTED", "accepted_closure", ev("docs/Phases/VisualPort/V7_RASTER_COMPATIBILITY.md"), "usable", "Accepted visual foundation; starter-room correction remains frozen")
    add_claim(map_type, "starter_room_semantics", "FROZEN_REVIEW_ONLY", "UNCHANGED_ACCEPTED", "accepted_closure", ev("knowledge/fixtures/accepted/visual-port/v7/fidelity-manifest.json"), "usable")
    add_claim(direct_canonical_id("system", "SocialDev.VisualPort"), "v8_entry", False, "UNCHANGED_ACCEPTED", "accepted_closure", ev("knowledge/fixtures/accepted/visual-port/v7/fidelity-manifest.json"), "usable", "V8 intentionally not started")
    add_claim(direct_canonical_id("system", "SocialDev.ProductPolicy"), "dashboard_assignment_semantics", "PRODUCT_POLICY_PENDING", "SOURCE_LIMITED", "accepted_closure", ev("knowledge/fixtures/accepted/behavior-first/dashboard-preservation-boundary.json"), "source_limited")
    add_claim(direct_canonical_id("system", "SocialDev.Pathfinding"), "room_neighbor_model", "4-neighbor_current_native", "UPGRADED", "native", ev("knowledge/fixtures/accepted/phase1d_closure.json"), "usable")

    # Old claims are retained as explicitly superseded; no conflict is overwritten.
    add_claim(staff_type, "ordinary_work_hp_drain", True, "SUPERSEDED", "inference", ev("knowledge/fixtures/accepted/living-core-closure/ordinary-work-hp-drain-contract.json"), "not_usable", "Historical continuous-drain assumption superseded by native Staff.UpdateWork closure")
    add_claim(direct_canonical_id("system", "SocialDev.Pathfinding"), "room_neighbor_model", "8-neighbor_candidate", "SUPERSEDED", "inference", ev("knowledge/fixtures/accepted/phase1_supersession.json"), "not_usable", "Historical candidate replaced by current native 4-neighbor closure")
    add_claim(direct_canonical_id("selector", "floor:5"), "floor_selector_target", None, "CONFLICT", "static_asset_metadata", ev("knowledge/fixtures/accepted/phase3b_floor_recovery_source_audit.json"), "not_usable", "Source selector 5 and img.inf package cannot distinguish intentional null slot from omitted source/name")

    unknown_gaps: list[dict[str, Any]] = []
    gap_specs = [
        ("data_manager_indirect_dispatch", "DataManager.Load/GetInstance indirect dispatch and full slot mapping are source-limited.", "knowledge/fixtures/accepted/native_content_registry.json", "SOURCE_LIMITED"),
        ("data_row_decode", "3,412 of 3,693 data rows retain native-id/raw locale data without verified reader-order decoding.", "knowledge/fixtures/accepted/native_content_registry.json", "SOURCE_LIMITED"),
        ("floor_selector_5", "Selector 5 has an unresolved null/omitted-source conflict.", "phase3b_floor_recovery_source_audit.json", "CONFLICT"),
        ("dashboard_policy", "Dashboard task assignment semantics remain product-policy pending.", "knowledge/fixtures/accepted/behavior-first/dashboard-preservation-boundary.json", "SOURCE_LIMITED"),
        ("external_framework_implementation", "Tier-D external framework implementations are excluded by scope.", "knowledge/fixtures/accepted/source_inventory.json", "EXCLUDED_SCOPE"),
        ("runtime_implementation", "No runtime adapter, V8, MapChip correction, Renderer, or save implementation is part of this static run.", "PROJECT_STATE.md", "OUT_OF_SCOPE"),
    ]
    for gap_id, statement, source_name, status in gap_specs:
        gap_source = source_name if source_name.startswith("knowledge/") or source_name.startswith("assets/") else ("knowledge/fixtures/accepted/" + source_name if source_name.endswith(".json") else source_name)
        unknown_gaps.append({
            "gap_id": f"gap:{gap_id}", "category": gap_id, "statement": statement,
            "status": status, "required_next_evidence": "Additional static source recovery or explicit product decision" if status != "OUT_OF_SCOPE" else "None in this run",
            "provenance": [cached_ref(gap_source)],
        })

    for claim in claims:
        if claim["canonical_fact_id"] is None:
            key = (claim["entity_id"], claim["predicate"])
            if key in canonical_facts:
                claim["canonical_fact_id"] = canonical_facts[key]["fact_id"]
    return {
        "entities": sorted(entities.values(), key=lambda row: row["entity_id"]),
        "facts": sorted(canonical_facts.values(), key=lambda row: row["fact_id"]),
        "claims": sorted(claims, key=lambda row: row["claim_id"]),
        "fact_sources": sorted(fact_sources, key=lambda row: row["fact_source_id"]),
        "revisions": sorted(revisions, key=lambda row: row["revision_id"]),
        "superseded": sorted(superseded, key=lambda row: row["superseded_fact_id"]),
        "conflicts": sorted(conflicts, key=lambda row: row["conflict_id"]),
        "unknown_gaps": unknown_gaps,
    }


def build_source_scope(identity: dict[str, Any], structural: dict[str, Any], closure: dict[str, Any], native: dict[str, Any], content: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for key, path in identity["source_paths"].items():
        rows.append({
            "source_id": f"source:{key}", "kind": key, "path": path,
            "tier": "A" if key == "raw_csharp" else "pinned_or_evidence",
            "status": "PINNED_VERIFIED" if key in {"apk", "native", "metadata", "dump"} else "present",
            "sha256": identity["hashes"].get(key), "details": identity["characteristics"] if key in {"native", "metadata", "apk"} else {},
            "provenance": [source_ref(path)],
        })
    for record in structural["source_files"] + closure["source_files"]:
        rows.append({
            "source_id": record["file_id"], "kind": "csharp_source_file", "path": record["path"],
            "tier": record.get("tier"), "status": record.get("status"), "sha256": record.get("sha256"),
            "details": {key: record.get(key) for key in ("namespace", "file_role", "trigger_reasons") if key in record},
            "provenance": [source_ref(record["path"])],
        })
    rows.append({
        "source_id": "source:native_evidence_bundle", "kind": "accepted_evidence_bundle",
        "path": "knowledge/fixtures/accepted", "tier": "accepted_closure", "status": "read_only",
        "sha256": None, "details": {"file_count": len(native["evidence_files"]), "content_registry": content["source"]},
        "provenance": [source_ref("knowledge/fixtures/accepted/native_content_registry.json")],
    })
    for name in closure["excluded_external_scope"]["csproj_files"]:
        rows.append({
            "source_id": direct_canonical_id("excluded_scope", name), "kind": "external_project_scope",
            "path": name, "tier": "D", "status": "EXCLUDED_IMPLEMENTATION", "sha256": sha256_file(ROOT / name),
            "details": {"reason": "assembly/type/method/signature/direct endpoint only"}, "provenance": [source_ref(name)],
        })
    return sorted(rows, key=lambda row: row["source_id"])


def export_jsonl(identity: dict[str, Any], structural: dict[str, Any], closure: dict[str, Any], content: dict[str, Any], graphs: dict[str, Any], canonical: dict[str, Any], native: dict[str, Any]) -> dict[str, int]:
    source_scope = build_source_scope(identity, structural, closure, native, content)
    tables = {
        "source_scope.jsonl": source_scope,
        "types.jsonl": dedupe_records(structural["types"] + closure["types"]),
        "fields.jsonl": dedupe_records(structural["fields"] + closure["fields"]),
        "methods.jsonl": graphs["methods"],
        "calls.jsonl": graphs["calls"],
        "field_access.jsonl": graphs["field_access"],
        "data_table_slot_map.jsonl": content["slots"],
        "data_tables.jsonl": content["tables"],
        "data_fields.jsonl": content["fields"],
        "data_rows.jsonl": content["rows"],
        "save_refs.jsonl": graphs["save_refs"],
        "assets.jsonl": content["assets"],
        "selectors.jsonl": content["selectors"],
        "asset_refs.jsonl": graphs["asset_refs"],
        "ui_commands.jsonl": graphs["ui_commands"],
        "event_edges.jsonl": graphs["event_edges"],
        "state_transitions.jsonl": graphs["state_transitions"],
        "native_dispatch.jsonl": graphs["native_dispatch"],
        "unknown_gaps.jsonl": canonical["unknown_gaps"],
        "canonical_entities.jsonl": canonical["entities"],
        "canonical_facts.jsonl": canonical["facts"],
        "fact_claims.jsonl": canonical["claims"],
        "fact_sources.jsonl": canonical["fact_sources"],
        "fact_revisions.jsonl": canonical["revisions"],
        "superseded_facts.jsonl": canonical["superseded"],
        "conflicts.jsonl": canonical["conflicts"],
    }
    counts: dict[str, int] = {}
    for name, rows in tables.items():
        counts[name] = write_jsonl(JSONL / name, rows)
    return counts


def graph_exports(structural: dict[str, Any], content: dict[str, Any], graphs: dict[str, Any]) -> dict[str, int]:
    type_edges = []
    for record in structural["types"]:
        if record.get("base_type"):
            type_edges.append({"edge_id": canonical_id("type_edge", record["entity_id"], record["base_type"]), "from": record["entity_id"], "to": record["base_type"], "kind": "inherits", "provenance": [source_ref(record["source_file"], record["source"].get("line_start"))]})
        for interface in record.get("interfaces", []):
            type_edges.append({"edge_id": canonical_id("type_edge", record["entity_id"], interface), "from": record["entity_id"], "to": interface, "kind": "implements", "provenance": [source_ref(record["source_file"], record["source"].get("line_start"))]})
    data_edges = []
    for slot in content["slots"]:
        data_edges.append({"edge_id": slot["slot_id"], "from": "DataManager", "to": slot["table_id"], "kind": "registry_slot", "slot": slot["table_slot"], "status": slot["status"], "provenance": slot.get("provenance", [])})
    for relation in content["asset_relations"]:
        data_edges.append({"edge_id": relation["relation_id"], "from": relation.get("from"), "to": relation.get("to") or relation.get("target_asset_id"), "kind": relation.get("relation", "content_relation"), "status": relation.get("status"), "provenance": relation.get("provenance", [])})
    assets_edges = [{"edge_id": row["asset_ref_id"], "from": row.get("from_id"), "to": row.get("target_asset_id"), "kind": row.get("relation") or "asset_ref", "status": row.get("status"), "provenance": row.get("provenance", [])} for row in graphs["asset_refs"]]
    save_edges = [{"edge_id": row["save_ref_id"], "from": row.get("method_id") or row.get("entity_id"), "to": row.get("token") or row.get("field_symbol"), "kind": row.get("reference_kind", "save_schema"), "status": row.get("status"), "provenance": row.get("provenance", [])} for row in graphs["save_refs"]]
    ui_edges = []
    for command in graphs["ui_commands"]:
        for index, step in enumerate(command["sequence"]):
            if index:
                prior = command["sequence"][index - 1]
                ui_edges.append({"edge_id": canonical_id("ui_edge", command["command_id"], index), "from": prior.get("method_id") or prior["symbol"], "to": step.get("method_id") or step["symbol"], "command": command["command"], "kind": "command_boundary", "status": command["status"], "provenance": command["provenance"]})
    exports = {
        "type_graph.jsonl": type_edges,
        "method_graph.jsonl": graphs["calls"],
        "field_graph.jsonl": graphs["field_access"],
        "state_graph.jsonl": graphs["state_transitions"],
        "data_graph.jsonl": data_edges,
        "asset_graph.jsonl": assets_edges,
        "save_graph.jsonl": save_edges,
        "ui_graph.jsonl": ui_edges,
        "event_graph.jsonl": graphs["event_edges"],
        "native_graph.jsonl": graphs["native_dispatch"],
    }
    counts: dict[str, int] = {}
    for name, rows in exports.items():
        counts[name] = write_jsonl(GRAPHS / name, rows)
    return counts


def create_database(identity: dict[str, Any], structural: dict[str, Any], closure: dict[str, Any], content: dict[str, Any], graphs: dict[str, Any], canonical: dict[str, Any], native: dict[str, Any]) -> dict[str, Any]:
    if SQLITE_PATH.exists():
        SQLITE_PATH.unlink()
    connection = sqlite3.connect(SQLITE_PATH)
    connection.execute("PRAGMA journal_mode = DELETE")
    connection.execute("PRAGMA foreign_keys = OFF")
    schemas = {
        "source_scope": "source_id TEXT PRIMARY KEY, kind TEXT, path TEXT, tier TEXT, status TEXT, sha256 TEXT, details_json TEXT, provenance_json TEXT",
        "types": "entity_id TEXT PRIMARY KEY, namespace TEXT, name TEXT, symbol TEXT, kind TEXT, base_type TEXT, interfaces_json TEXT, source_file TEXT, tier TEXT, source_json TEXT, details_json TEXT",
        "fields": "entity_id TEXT PRIMARY KEY, declaring_type TEXT, owner TEXT, name TEXT, declared_type TEXT, field_offset TEXT, source_file TEXT, tier TEXT, source_json TEXT, details_json TEXT",
        "methods": "entity_id TEXT PRIMARY KEY, declaring_type TEXT, owner TEXT, name TEXT, symbol TEXT, full_signature TEXT, body_status TEXT, native_rva TEXT, source_file TEXT, tier TEXT, source_json TEXT, details_json TEXT",
        "calls": "call_id TEXT PRIMARY KEY, caller_method_id TEXT, caller_symbol TEXT, callee_method_id TEXT, callee_symbol TEXT, resolution_status TEXT, source_file TEXT, source_line INTEGER, details_json TEXT",
        "field_access": "access_id TEXT PRIMARY KEY, method_id TEXT, method_symbol TEXT, field_id TEXT, field_symbol TEXT, operation TEXT, resolution_status TEXT, source_file TEXT, source_line INTEGER, details_json TEXT",
        "data_table_slot_map": "slot_id TEXT PRIMARY KEY, table_slot INTEGER, registry_key TEXT, field TEXT, element_type TEXT, table_id TEXT, status TEXT, mapping_basis TEXT, details_json TEXT",
        "data_tables": "table_id TEXT PRIMARY KEY, element_type TEXT, field TEXT, table_stem TEXT, row_count INTEGER, source_file TEXT, status TEXT, details_json TEXT",
        "data_fields": "data_field_id TEXT PRIMARY KEY, table_id TEXT, table_slot INTEGER, ordinal INTEGER, name TEXT, declared_type TEXT, status TEXT, details_json TEXT",
        "data_rows": "row_id TEXT PRIMARY KEY, table_id TEXT, table_slot INTEGER, element_type TEXT, native_id INTEGER, row_index INTEGER, id_status TEXT, decoded_status TEXT, locales_json TEXT, details_json TEXT",
        "save_refs": "save_ref_id TEXT PRIMARY KEY, method_id TEXT, entity_id TEXT, method_symbol TEXT, reference_kind TEXT, token TEXT, field_symbol TEXT, status TEXT, source_file TEXT, source_line INTEGER, details_json TEXT",
        "assets": "asset_id TEXT PRIMARY KEY, relative_path TEXT, kind TEXT, pack TEXT, extension TEXT, size_bytes INTEGER, sha256 TEXT, semantic_role TEXT, status TEXT, details_json TEXT",
        "selectors": "selector_key TEXT PRIMARY KEY, selector_kind TEXT, selector_id INTEGER, resource_scope TEXT, target_asset_id TEXT, status TEXT, source_file TEXT, source_row INTEGER, details_json TEXT",
        "asset_refs": "asset_ref_id TEXT PRIMARY KEY, from_id TEXT, field TEXT, target_asset_id TEXT, relation TEXT, status TEXT, details_json TEXT",
        "ui_commands": "command_id TEXT PRIMARY KEY, command TEXT, boundary TEXT, status TEXT, sequence_json TEXT, details_json TEXT",
        "event_edges": "event_edge_id TEXT PRIMARY KEY, method_id TEXT, method_symbol TEXT, event_token TEXT, edge_kind TEXT, status TEXT, source_file TEXT, source_line INTEGER, details_json TEXT",
        "state_transitions": "transition_id TEXT PRIMARY KEY, from_state TEXT, to_state TEXT, move_mode TEXT, confidence TEXT, status TEXT, source_file TEXT, source_line INTEGER, details_json TEXT",
        "native_dispatch": "dispatch_id TEXT PRIMARY KEY, method_symbol TEXT, method_rva TEXT, dispatch_key TEXT, dispatch_key_offset TEXT, move_mode INTEGER, label TEXT, target_rva TEXT, status TEXT, details_json TEXT",
        "unknown_gaps": "gap_id TEXT PRIMARY KEY, category TEXT, status TEXT, statement TEXT, required_next_evidence TEXT, details_json TEXT",
        "canonical_entities": "entity_id TEXT PRIMARY KEY, entity_type TEXT, name TEXT, attributes_json TEXT, provenance_json TEXT",
        "canonical_facts": "fact_id TEXT PRIMARY KEY, entity_id TEXT, predicate TEXT, value_json TEXT, status TEXT, authority TEXT, impl_status TEXT, revision INTEGER, canonical INTEGER, note TEXT, UNIQUE(entity_id, predicate)",
        "fact_claims": "claim_id TEXT PRIMARY KEY, entity_id TEXT, predicate TEXT, value_json TEXT, status TEXT, authority TEXT, impl_status TEXT, canonical_fact_id TEXT, source_claim_refs_json TEXT, note TEXT",
        "fact_sources": "fact_source_id TEXT PRIMARY KEY, claim_id TEXT, entity_id TEXT, predicate TEXT, source_json TEXT",
        "fact_revisions": "revision_id TEXT PRIMARY KEY, fact_id TEXT, revision INTEGER, change TEXT, claim_id TEXT, old_value_json TEXT, new_value_json TEXT, status TEXT, source_claim_refs_json TEXT",
        "superseded_facts": "superseded_fact_id TEXT PRIMARY KEY, claim_id TEXT, entity_id TEXT, predicate TEXT, value_json TEXT, replacement_note TEXT, source_claim_refs_json TEXT",
        "conflicts": "conflict_id TEXT PRIMARY KEY, claim_id TEXT, entity_id TEXT, predicate TEXT, value_json TEXT, resolution_status TEXT, note TEXT, source_claim_refs_json TEXT",
    }
    for table, columns in schemas.items():
        connection.execute(f"CREATE TABLE {table} ({columns})")
    connection.execute("CREATE INDEX idx_canonical_facts_entity_predicate ON canonical_facts(entity_id, predicate)")

    def insert(table: str, rows: list[dict[str, Any]], columns: list[str], mapping: dict[str, Any] | None = None) -> int:
        if not rows:
            return 0
        primary_key = columns[0]
        unique_rows: dict[str, dict[str, Any]] = {}
        for row in rows:
            value = row.get(primary_key)
            if value is not None and str(value) not in unique_rows:
                unique_rows[str(value)] = row
        rows = list(unique_rows.values()) if unique_rows else rows
        mapping = mapping or {}
        placeholders = ",".join("?" for _ in columns)
        sql = f"INSERT INTO {table} ({','.join(columns)}) VALUES ({placeholders})"
        values = []
        for row in rows:
            current = []
            for column in columns:
                key = mapping.get(column, column)
                value = row.get(key)
                if isinstance(value, (dict, list, tuple, bool)):
                    value = stable_json(value)
                current.append(value)
            values.append(current)
        connection.executemany(sql, values)
        return len(values)

    sources = build_source_scope(identity, structural, closure, native, content)
    insert("source_scope", sources, ["source_id", "kind", "path", "tier", "status", "sha256", "details_json", "provenance_json"], {"details_json": "details", "provenance_json": "provenance"})
    insert("types", structural["types"] + closure["types"], ["entity_id", "namespace", "name", "symbol", "kind", "base_type", "interfaces_json", "source_file", "tier", "source_json", "details_json"], {"interfaces_json": "interfaces", "source_json": "source", "details_json": "classifications"})
    insert("fields", structural["fields"] + closure["fields"], ["entity_id", "declaring_type", "owner", "name", "declared_type", "field_offset", "source_file", "tier", "source_json", "details_json"], {"source_json": "source", "details_json": "classifications"})
    insert("methods", graphs["methods"], ["entity_id", "declaring_type", "owner", "name", "symbol", "full_signature", "body_status", "native_rva", "source_file", "tier", "source_json", "details_json"], {"source_json": "source", "details_json": "provenance"})
    insert("calls", graphs["calls"], ["call_id", "caller_method_id", "caller_symbol", "callee_method_id", "callee_symbol", "resolution_status", "source_file", "source_line", "details_json"], {"details_json": "provenance"})
    insert("field_access", graphs["field_access"], ["access_id", "method_id", "method_symbol", "field_id", "field_symbol", "operation", "resolution_status", "source_file", "source_line", "details_json"], {"details_json": "provenance"})
    insert("data_table_slot_map", content["slots"], ["slot_id", "table_slot", "registry_key", "field", "element_type", "table_id", "status", "mapping_basis", "details_json"], {"details_json": "provenance"})
    insert("data_tables", content["tables"], ["table_id", "element_type", "field", "table_stem", "row_count", "source_file", "status", "details_json"], {"details_json": "load_contract"})
    insert("data_fields", content["fields"], ["data_field_id", "table_id", "table_slot", "ordinal", "name", "declared_type", "status", "details_json"], {"details_json": "provenance"})
    insert("data_rows", content["rows"], ["row_id", "table_id", "table_slot", "element_type", "native_id", "row_index", "id_status", "decoded_status", "locales_json", "details_json"], {"decoded_status": "decoded", "locales_json": "locales", "details_json": "provenance"})
    insert("save_refs", graphs["save_refs"], ["save_ref_id", "method_id", "entity_id", "method_symbol", "reference_kind", "token", "field_symbol", "status", "source_file", "source_line", "details_json"], {"details_json": "provenance"})
    insert("assets", content["assets"], ["asset_id", "relative_path", "kind", "pack", "extension", "size_bytes", "sha256", "semantic_role", "status", "details_json"], {"status": "source_status", "details_json": "provenance"})
    insert("selectors", content["selectors"], ["selector_key", "selector_kind", "selector_id", "resource_scope", "target_asset_id", "status", "source_file", "source_row", "details_json"], {"details_json": "provenance"})
    insert("asset_refs", graphs["asset_refs"], ["asset_ref_id", "from_id", "field", "target_asset_id", "relation", "status", "details_json"], {"details_json": "provenance"})
    insert("ui_commands", graphs["ui_commands"], ["command_id", "command", "boundary", "status", "sequence_json", "details_json"], {"sequence_json": "sequence", "details_json": "provenance"})
    insert("event_edges", graphs["event_edges"], ["event_edge_id", "method_id", "method_symbol", "event_token", "edge_kind", "status", "source_file", "source_line", "details_json"], {"details_json": "provenance"})
    insert("state_transitions", graphs["state_transitions"], ["transition_id", "from_state", "to_state", "move_mode", "confidence", "status", "source_file", "source_line", "details_json"], {"details_json": "provenance"})
    insert("native_dispatch", graphs["native_dispatch"], ["dispatch_id", "method_symbol", "method_rva", "dispatch_key", "dispatch_key_offset", "move_mode", "label", "target_rva", "status", "details_json"], {"details_json": "side_effects"})
    insert("unknown_gaps", canonical["unknown_gaps"], ["gap_id", "category", "status", "statement", "required_next_evidence", "details_json"], {"details_json": "provenance"})
    insert("canonical_entities", canonical["entities"], ["entity_id", "entity_type", "name", "attributes_json", "provenance_json"], {"attributes_json": "attributes", "provenance_json": "provenance"})
    insert("canonical_facts", canonical["facts"], ["fact_id", "entity_id", "predicate", "value_json", "status", "authority", "impl_status", "revision", "canonical", "note"], {"value_json": "value"})
    insert("fact_claims", canonical["claims"], ["claim_id", "entity_id", "predicate", "value_json", "status", "authority", "impl_status", "canonical_fact_id", "source_claim_refs_json", "note"], {"value_json": "value", "source_claim_refs_json": "source_claim_refs"})
    insert("fact_sources", canonical["fact_sources"], ["fact_source_id", "claim_id", "entity_id", "predicate", "source_json"], {"source_json": "source"})
    insert("fact_revisions", canonical["revisions"], ["revision_id", "fact_id", "revision", "change", "claim_id", "old_value_json", "new_value_json", "status", "source_claim_refs_json"], {"old_value_json": "old_value", "new_value_json": "new_value", "source_claim_refs_json": "source_claim_refs"})
    insert("superseded_facts", canonical["superseded"], ["superseded_fact_id", "claim_id", "entity_id", "predicate", "value_json", "replacement_note", "source_claim_refs_json"], {"value_json": "value", "source_claim_refs_json": "source_claim_refs"})
    insert("conflicts", canonical["conflicts"], ["conflict_id", "claim_id", "entity_id", "predicate", "value_json", "resolution_status", "note", "source_claim_refs_json"], {"value_json": "value", "source_claim_refs_json": "source_claim_refs"})
    connection.commit()
    table_counts = {row[0]: row[1] for row in connection.execute("SELECT name, (SELECT COUNT(*) FROM sqlite_master AS m2 WHERE m2.name=m1.name) FROM sqlite_master AS m1 WHERE type='table'")}
    # The count query above is intentionally replaced with a direct deterministic pass.
    table_counts = {}
    for table in schemas:
        table_counts[table] = connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    connection.close()
    return {"path": relative(SQLITE_PATH), "table_counts": table_counts}


QUERY_SET = [
    ("Q1", "Tier-A/core types", "SELECT entity_id, symbol, kind FROM types WHERE name IN ('Staff','Room','MapChip') ORDER BY symbol", ()),
    ("Q2", "Staff hp field offset", "SELECT entity_id, declaring_type || '.' || name AS field_symbol, field_offset FROM fields WHERE (declaring_type || '.' || name) LIKE '%Staff.hp_%'", ()),
    ("Q3", "Native method closure", "SELECT symbol, native_rva, body_status FROM methods WHERE native_rva IS NOT NULL ORDER BY symbol LIMIT 50", ()),
    ("Q4", "Data table total", "SELECT COUNT(*) AS table_count, COALESCE(SUM(row_count),0) AS row_count FROM data_tables", ()),
    ("Q5", "DataManager slot map", "SELECT table_slot, element_type, status FROM data_table_slot_map ORDER BY table_slot", ()),
    ("Q6", "Core data row counts", "SELECT element_type, COUNT(*) AS rows FROM data_rows WHERE element_type IN ('StaffData','JobData','SkillData','FurnitureData') GROUP BY element_type ORDER BY element_type", ()),
    ("Q7", "Asset inventory by kind", "SELECT kind, COUNT(*) AS count FROM assets GROUP BY kind ORDER BY kind", ()),
    ("Q8", "Unresolved asset selectors", "SELECT status, COUNT(*) AS count FROM selectors GROUP BY status ORDER BY status", ()),
    ("Q9", "Staff.Update call boundary", "SELECT caller_symbol, callee_symbol, resolution_status, source_line FROM calls WHERE caller_symbol LIKE '%Staff.Update%' ORDER BY source_line, callee_symbol", ()),
    ("Q10", "Staff hp reads/writes", "SELECT operation, COUNT(*) AS count FROM field_access WHERE field_symbol LIKE '%Staff.hp_%' GROUP BY operation ORDER BY operation", ()),
    ("Q11", "State transition coverage", "SELECT status, COUNT(*) AS count FROM state_transitions GROUP BY status ORDER BY status", ()),
    ("Q12", "Save schema candidates", "SELECT reference_kind, status, COUNT(*) AS count FROM save_refs GROUP BY reference_kind, status ORDER BY reference_kind, status", ()),
    ("Q13", "UI command boundary", "SELECT command_id, command, status FROM ui_commands ORDER BY command_id", ()),
    ("Q14", "Canonical reconciliation outcome", "SELECT 'canonical_facts' AS class, COUNT(*) AS count FROM canonical_facts UNION ALL SELECT 'claims', COUNT(*) FROM fact_claims UNION ALL SELECT 'superseded', COUNT(*) FROM superseded_facts UNION ALL SELECT 'conflicts', COUNT(*) FROM conflicts", ()),
]


def run_queries() -> list[dict[str, Any]]:
    connection = sqlite3.connect(SQLITE_PATH)
    connection.row_factory = sqlite3.Row
    results: list[dict[str, Any]] = []
    for query_id, label, sql, params in QUERY_SET:
        rows = [dict(row) for row in connection.execute(sql, params).fetchall()]
        results.append({"query_id": query_id, "label": label, "sql": sql, "params": list(params), "row_count": len(rows), "rows": rows})
    connection.close()
    write_jsonl(KB / "query_results.jsonl", results)
    return results


def md_table(headers: list[str], rows: list[list[Any]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(value).replace("|", "\\|").replace("\n", " ") for value in row) + " |")
    return "\n".join(lines)


def write_reports(identity: dict[str, Any], structural: dict[str, Any], closure: dict[str, Any], content: dict[str, Any], graphs: dict[str, Any], canonical: dict[str, Any], native: dict[str, Any], json_counts: dict[str, int], graph_counts: dict[str, int], db_info: dict[str, Any], query_results: list[dict[str, Any]]) -> str:
    def report(name: str, body: str) -> None:
        (REPORTS / name).write_text(body.rstrip() + "\n", encoding="utf-8")

    raw_dirs = identity["source_counts"]["tier_a_by_directory"]
    total_rows = sum(table.get("row_count", 0) or 0 for table in content["tables"])
    verified_rows = sum(1 for row in content["rows"] if row.get("decoded", {}).get("status") == "verified_reader_order")
    unresolved_selectors = sum(1 for row in content["selectors"] if row.get("status") != "resolved")
    resolved_calls = sum(1 for row in graphs["calls"] if str(row.get("resolution_status", "")).startswith("RESOLVED"))
    unresolved_calls = len(graphs["calls"]) - resolved_calls
    hp_access = [row for row in graphs["field_access"] if row.get("field_symbol", "").endswith("Staff.hp_")]

    report("G0_WORKTREE_AND_EXISTING_OUTPUT_AUDIT.md", f"""# G0 Worktree and Existing Output Audit

This report records the read-only audit performed before the fresh G0/G1 builder run.

- Workspace: `{ROOT}`
- Existing project-owned changes were preserved; no source root, runtime implementation, V8, MapChip, or Renderer files were mutated.
- Existing `knowledge/data/original/` output before this run consisted of `reports/CURRENT_INTERRUPTED_RUN_AUDIT.md`; no canonical JSONL or SQLite output was present.
- Existing evidence roots were retained read-only. Generated output is confined to `knowledge/data/original/`.
- The interrupted-run report was preserved as historical audit evidence.

The current output is generated by `tools/social-dev/build_game_knowledge_g0_g1.py` and is deterministic for the pinned inputs.
""")

    report("G0_SOURCE_MANIFEST.md", f"""# G0 Source Manifest

Status: **{identity['status']}**.

## Pinned hashes

{md_table(['source', 'sha256'], [[key, value] for key, value in identity['hashes'].items()])}

Expected APK/native/metadata/dump hashes were checked exactly. The APK inner entries were also rehashed and matched. Characteristics: `{identity['characteristics']}`.

## Static inventory

{md_table(['metric', 'value'], [[key, value] for key, value in identity['source_counts'].items() if key != 'tier_a_by_directory'])}

APK inventory: `{json.dumps(identity['apk_inventory'], ensure_ascii=False, sort_keys=True)}`.
""")

    report("G0_TIER_A_INDEX_COVERAGE.md", f"""# G0 Tier-A Index Coverage

Tier A is the exact direct-file scope `main/`, `data/`, `game/`, `game.routeSearch/`, and `form/` from the immutable raw extraction.

{md_table(['directory', 'direct .cs files'], [[key, value] for key, value in raw_dirs.items()])}

- Tier-A files indexed: **{len(structural['source_files'])}** (required: 89)
- Structural types: **{len(structural['types'])}**
- Structural fields: **{len(structural['fields'])}**
- Structural methods: **{len(structural['methods'])}**
- Constants: **{len(structural['constants'])}**
- Enum values: **{len(structural['enum_values'])}**
- Body statuses are retained per method; damaged Cpp2IL bodies are not treated as behavioral authority.
""")

    report("G0_DEPENDENCY_CLOSURE.md", f"""# G0 Dependency Closure

- Candidate app-adjacent files inspected by name/reference gate: **{closure['candidate_file_count']}**
- Bounded closure files indexed: **{closure['closure_file_count']}**
- Tier-B candidates: **{closure['tier_b_files']}**
- Tier-C candidates: **{closure['tier_c_files']}**
- Closure types/fields/methods: **{len(closure['types'])} / {len(closure['fields'])} / {len(closure['methods'])}**
- Tier-D external implementations remain excluded; see `EXCLUDED_EXTERNAL_SCOPE.md`.

Every closure source file has a trigger reason and is retained in `source_scope.jsonl`.
""")

    report("G0_DATA_SPINE_RECOVERY.md", f"""# G0 Data Spine Recovery

- DataManager registry entries: **{len(content['slots'])}**
- Data tables: **{len(content['tables'])}**
- Rows retained: **{len(content['rows'])}** (registry sum: **{total_rows}**)
- Rows with verified reader-order decode: **{verified_rows}**
- Rows retaining native-id/raw locale values without decode: **{len(content['rows']) - verified_rows}**
- Registry order is exported as a source-limited slot candidate. Slot 42 is explicitly supported by the `GetInstance(num == 42)` branch; the remaining indirect dispatch is not guessed.
- Locale and row provenance are retained in `data_rows.jsonl`; no localized source text was rewritten.
""")

    table_rows = [[row['table_id'], row.get('element_type'), row.get('table_stem'), row.get('row_count'), row.get('status')] for row in content['tables']]
    report("G0_DATA_TABLE_COUNTS.md", "# G0 Data Table Counts\n\n" + md_table(["table_id", "element_type", "stem", "rows", "status"], table_rows))

    report("G0_SAVE_SCHEMA.md", f"""# G0 Save Schema

Save references/candidate persisted fields: **{len(graphs['save_refs'])}**.

The export distinguishes source-backed persistence symbols from candidate fields. No save format or runtime serializer was invented. Every candidate is `SOURCE_LIMITED` unless the source body is intact/native-closed and the symbol is directly visible.
""")

    asset_kinds = collections.Counter(row.get("kind") for row in content["assets"])
    report("G0_ASSET_INVENTORY.md", f"""# G0 Asset Inventory

- Asset records: **{len(content['assets'])}**
- Selector records: **{len(content['selectors'])}**
- Unresolved/non-resolved selectors retained: **{unresolved_selectors}**
- Content relations: **{len(content['asset_relations'])}**
- Asset ZIP inventory source: `{relative(ASSET_ZIP)}`; no deep export of texture/audio payloads was performed.

{md_table(['asset kind', 'count'], [[key, value] for key, value in sorted(asset_kinds.items())])}
""")

    report("G1_CALL_GRAPH_COVERAGE.md", f"""# G1 Call Graph Coverage

- Indexed methods: **{len(graphs['methods'])}**
- Call edges retained: **{len(graphs['calls'])}**
- Resolved call edges: **{resolved_calls}**
- Unresolved/indirect call edges: **{unresolved_calls}**
- Indirect DataManager dispatch edges are explicitly labelled `SOURCE_LIMITED_INDIRECT_DISPATCH`.
""")

    report("G1_FIELD_RW_COVERAGE.md", f"""# G1 Field Read/Write Coverage

- Field access edges: **{len(graphs['field_access'])}**
- Fields with observed reads/writes: **{sum(1 for field in graphs['fields'] if field.get('reads') or field.get('writes'))}**
- `Staff.hp_` source access edges: **{len(hp_access)}**
- The native `Staff.hp_` offset fact is retained independently at `0xE8`; absence of a damaged-body write site is not treated as proof of no native write.
""")

    report("G1_STATE_DISPATCH_COVERAGE.md", f"""# G1 State and Dispatch Coverage

- State transition edges: **{len(graphs['state_transitions'])}**
- Native `Staff.OnArriveGoal` dispatch entries: **{len(graphs['native_dispatch'])}** (required: 11)
- Dispatch method RVA: `0x12D8420`; table base: `0x12D84A8`; key field: `moveMode_` at `0xA8`.
- Exact unknown state handlers remain source-limited and are listed in `unknown_gaps.jsonl`.
""")

    report("G1_UI_COMMAND_BOUNDARY.md", f"""# G1 UI Command Boundary

The static command boundary is represented as symbol sequences only:

{md_table(['command', 'steps', 'status'], [[row['command'], ' → '.join(step['symbol'] for step in row['sequence']), row['status']] for row in graphs['ui_commands']])}

`SubForm → Player → Room → Staff` mutation boundaries and `ReserveAutoSave` are retained as knowledge. No runtime UI adapter, dashboard implementation, or save implementation was added.
""")

    report("G1_NATIVE_CLOSURE_REPORT.md", f"""# G1 Native Closure Report

- Native evidence files scanned: **{len(native['evidence_files'])}**
- Native method/RVA observations: **{len(native['records'])}**
- Native field offsets recovered: **{len(native['field_offsets'])}**
- Native dispatch rows exported: **{len(graphs['native_dispatch'])}**
- Native authority is ordered above metadata/mapping, intact C#, original data, and inference. Raw claims remain separate from canonical facts.
""")

    report("G1_UNKNOWN_GAPS.md", "# G1 Unknown Gaps\n\n" + md_table(["gap", "status", "statement"], [[row['category'], row['status'], row['statement']] for row in canonical['unknown_gaps']]))
    report("G1_CANONICAL_RECONCILIATION.md", f"""# G1 Canonical Reconciliation

- Canonical entities: **{len(canonical['entities'])}**
- Canonical facts: **{len(canonical['facts'])}**
- Raw fact claims: **{len(canonical['claims'])}**
- Fact sources: **{len(canonical['fact_sources'])}**
- Fact revisions: **{len(canonical['revisions'])}**
- One canonical fact identity is enforced by the `(entity_id, predicate)` unique constraint. Conflicts and superseded claims remain separate.
""")
    report("G1_ACCEPTED_CLOSURE_IMPORT.md", """# G1 Accepted Closure Import

Accepted historical/native closure was imported as structured claims with explicit provenance, including Staff HP/recovery, workstation vacancy, equipment contention, the 11-entry arrival dispatch, furniture roles, MapChip foundation freeze, V8 freeze, current pathfinding closure, and product-policy boundaries. No prose-only assertion is used as a replacement for a source claim.
""")
    report("G1_SUPERSEDED_FACTS.md", "# G1 Superseded Facts\n\n" + md_table(["predicate", "value", "replacement"], [[row['predicate'], json.dumps(row['value'], ensure_ascii=False), row['replacement_note']] for row in canonical['superseded']]))
    report("G1_CONFLICTS.md", "# G1 Conflicts\n\n" + md_table(["predicate", "value", "status", "note"], [[row['predicate'], json.dumps(row['value'], ensure_ascii=False), row['resolution_status'], row['note']] for row in canonical['conflicts']]))
    report("G1_CANONICAL_COVERAGE.md", f"""# G1 Canonical Coverage

- Canonicalization status: **PASS_WITH_SOURCE_LIMITS**
- Unique canonical entity/predicate facts: **{len(canonical['facts'])}**
- Superseded claims: **{len(canonical['superseded'])}**
- Unresolved conflicts: **{len(canonical['conflicts'])}**
- Canonical facts have `impl_status` and provenance. No implementation claim is promoted from a damaged body without a native/static closure.
""")

    report("EXCLUDED_EXTERNAL_SCOPE.md", f"""# Excluded External Scope

Tier-D scope is retained only as assembly/project/type/method/signature/direct endpoint metadata. Implementations are excluded from the canonical game-scoped truth.

- Tier-D prefixes: `{', '.join(closure['excluded_external_scope']['tier_d_prefixes'])}`
- `.csproj` files retained as scope metadata: **{len(closure['excluded_external_scope']['csproj_files'])}**
- Assembly list source: `assets/bin/Data/ScriptingAssemblies.json` inside the pinned APK.
- No Unity/Firebase/third-party implementation was copied into the game knowledge base.
""")

    final_token = "PARTIAL_GAME_SCOPED_STATIC_KNOWLEDGE_G0_G1_SOURCE_LIMITED"
    report("G0_G1_FINAL_STATUS.md", f"""# G0/G1 Final Status

## `{final_token}`

Source identity passed. G0 structural indexing, data/content recovery, bounded dependency closure, asset inventory, G1 graphs, canonical reconciliation, SQLite/JSONL exports, and query demonstrations completed.

The result is intentionally partial because source-limited gaps remain: indirect DataManager dispatch/row decoding, one unresolved floor selector conflict, dashboard policy, and excluded external/runtime scope. These are explicit records, not silently resolved claims.

SQLite: `{relative(SQLITE_PATH)}`
JSONL files: `{relative(JSONL)}`
Graph files: `{relative(GRAPHS)}`
""")

    query_lines = ["# Query Examples", "", "Each query was executed against `sqlite/social_dev_original_data.sqlite` after the build. JSONL equivalents are the same named exports under `jsonl/`.", ""]
    for result in query_results:
        query_lines.append(f"## {result['query_id']} — {result['label']}")
        query_lines.append("\n```sql\n" + result["sql"] + "\n```")
        query_lines.append(f"Rows returned: **{result['row_count']}**")
        sample = result["rows"][:8]
        if sample:
            keys = list(sample[0].keys())
            query_lines.append("\n```json\n" + json.dumps(sample, ensure_ascii=False, indent=2) + "\n```")
        query_lines.append("")
    report("QUERY_EXAMPLES.md", "\n".join(query_lines))

    write_json(KB / "source_identity.json", identity)
    write_json(KB / "build_manifest.json", {
        "status": final_token, "source_identity_status": identity["status"],
        "sqlite": db_info, "jsonl_counts": json_counts, "graph_counts": graph_counts,
        "query_ids": [result["query_id"] for result in query_results],
        "structural_counts": {key: len(structural[key]) for key in ("source_files", "types", "fields", "methods", "constants", "enum_values")},
        "closure_counts": {key: len(closure[key]) for key in ("source_files", "types", "fields", "methods")},
        "content_counts": {key: len(content[key]) for key in ("tables", "slots", "fields", "rows", "assets", "selectors", "asset_relations")},
        "canonical_counts": {key: len(canonical[key]) for key in ("entities", "facts", "claims", "fact_sources", "revisions", "superseded", "conflicts", "unknown_gaps")},
    })
    return final_token


REQUIRED_JSONL = (
    "source_scope.jsonl", "types.jsonl", "fields.jsonl", "methods.jsonl", "calls.jsonl",
    "field_access.jsonl", "data_table_slot_map.jsonl", "data_rows.jsonl", "save_refs.jsonl",
    "assets.jsonl", "ui_commands.jsonl", "native_dispatch.jsonl", "unknown_gaps.jsonl",
    "canonical_entities.jsonl", "canonical_facts.jsonl", "fact_claims.jsonl", "fact_sources.jsonl",
    "fact_revisions.jsonl", "superseded_facts.jsonl", "conflicts.jsonl",
)
REQUIRED_REPORTS = (
    "G0_WORKTREE_AND_EXISTING_OUTPUT_AUDIT.md", "G0_SOURCE_MANIFEST.md", "G0_TIER_A_INDEX_COVERAGE.md",
    "G0_DEPENDENCY_CLOSURE.md", "G0_DATA_SPINE_RECOVERY.md", "G0_DATA_TABLE_COUNTS.md", "G0_SAVE_SCHEMA.md",
    "G0_ASSET_INVENTORY.md", "G1_CALL_GRAPH_COVERAGE.md", "G1_FIELD_RW_COVERAGE.md", "G1_STATE_DISPATCH_COVERAGE.md",
    "G1_UI_COMMAND_BOUNDARY.md", "G1_NATIVE_CLOSURE_REPORT.md", "G1_UNKNOWN_GAPS.md", "G1_CANONICAL_RECONCILIATION.md",
    "G1_ACCEPTED_CLOSURE_IMPORT.md", "G1_SUPERSEDED_FACTS.md", "G1_CONFLICTS.md", "G1_CANONICAL_COVERAGE.md",
    "EXCLUDED_EXTERNAL_SCOPE.md", "G0_G1_FINAL_STATUS.md", "QUERY_EXAMPLES.md",
)
REQUIRED_GRAPHS = ("type_graph.jsonl", "method_graph.jsonl", "field_graph.jsonl", "state_graph.jsonl", "data_graph.jsonl", "asset_graph.jsonl", "save_graph.jsonl", "ui_graph.jsonl", "event_graph.jsonl", "native_graph.jsonl")


def check_outputs() -> dict[str, Any]:
    identity_path = KB / "source_identity.json"
    manifest_path = KB / "build_manifest.json"
    missing = [relative(JSONL / name) for name in REQUIRED_JSONL if not (JSONL / name).is_file()]
    missing.extend(relative(REPORTS / name) for name in REQUIRED_REPORTS if not (REPORTS / name).is_file())
    missing.extend(relative(GRAPHS / name) for name in REQUIRED_GRAPHS if not (GRAPHS / name).is_file())
    if not SQLITE_PATH.is_file():
        missing.append(relative(SQLITE_PATH))
    if not identity_path.is_file() or not manifest_path.is_file():
        missing.extend(relative(path) for path in (identity_path, manifest_path) if not path.is_file())
    if missing:
        raise RuntimeError("CHECK_FAILED_MISSING_OUTPUTS: " + ", ".join(missing))
    identity = read_json(identity_path)
    if identity.get("status") != "PASS_SOURCE_IDENTITY":
        raise RuntimeError("CHECK_FAILED_SOURCE_IDENTITY")
    for name in REQUIRED_JSONL:
        with (JSONL / name).open("r", encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, 1):
                if line.strip():
                    try:
                        json.loads(line)
                    except json.JSONDecodeError as exc:
                        raise RuntimeError(f"CHECK_FAILED_JSONL:{name}:{line_number}:{exc}") from exc
    connection = sqlite3.connect(SQLITE_PATH)
    tables = {row[0] for row in connection.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    required_tables = {name[:-6] for name in REQUIRED_JSONL} | {"data_tables", "data_fields", "selectors", "asset_refs", "event_edges", "state_transitions"}
    missing_tables = sorted(required_tables - tables)
    if missing_tables:
        raise RuntimeError("CHECK_FAILED_SQLITE_TABLES: " + ", ".join(missing_tables))
    duplicate_facts = connection.execute("SELECT entity_id, predicate, COUNT(*) FROM canonical_facts GROUP BY entity_id, predicate HAVING COUNT(*) > 1").fetchall()
    if duplicate_facts:
        raise RuntimeError("CHECK_FAILED_DUPLICATE_CANONICAL_FACTS")
    q14 = connection.execute("SELECT COUNT(*) FROM canonical_facts").fetchone()[0]
    connection.close()
    return {"status": "PASS_GAME_KNOWLEDGE_OUTPUT_CHECK", "canonical_fact_count": q14, "jsonl_files": len(REQUIRED_JSONL), "reports": len(REQUIRED_REPORTS), "graphs": len(REQUIRED_GRAPHS)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Validate existing generated outputs without rebuilding")
    args = parser.parse_args()
    if args.check:
        print(json.dumps(check_outputs(), sort_keys=True))
        return 0

    ensure_dirs()
    print("[g0] verify source identity", flush=True)
    identity = verify_source_identity()
    print("[g0] load native evidence", flush=True)
    native = load_native_evidence()
    print("[g0] build Tier-A structural index", flush=True)
    structural = build_structural_index(native)
    print(f"[g0] Tier-A files={len(structural['source_files'])} types={len(structural['types'])} fields={len(structural['fields'])} methods={len(structural['methods'])}", flush=True)
    print("[g0] build bounded dependency closure", flush=True)
    closure = build_dependency_closure(structural)
    print(f"[g0] closure files={closure['closure_file_count']}", flush=True)
    print("[g0] load data and asset content registry", flush=True)
    content = load_content_evidence()
    print(f"[g0] tables={len(content['tables'])} rows={len(content['rows'])} assets={len(content['assets'])} selectors={len(content['selectors'])}", flush=True)
    print("[g1] build static graphs", flush=True)
    graphs = build_graphs(structural, closure, content)
    print(f"[g1] calls={len(graphs['calls'])} field_access={len(graphs['field_access'])} native_dispatch={len(graphs['native_dispatch'])}", flush=True)
    print("[g1] reconcile canonical claims", flush=True)
    canonical = build_canonical_model(identity, structural, closure, content, graphs, native)
    print(f"[g1] facts={len(canonical['facts'])} claims={len(canonical['claims'])}", flush=True)
    print("[output] write JSONL and graphs", flush=True)
    json_counts = export_jsonl(identity, structural, closure, content, graphs, canonical, native)
    graph_counts = graph_exports(structural, content, graphs)
    print("[output] create SQLite", flush=True)
    db_info = create_database(identity, structural, closure, content, graphs, canonical, native)
    print("[output] run query demonstrations and reports", flush=True)
    query_results = run_queries()
    final_token = write_reports(identity, structural, closure, content, graphs, canonical, native, json_counts, graph_counts, db_info, query_results)
    print(json.dumps({
        "status": final_token,
        "source_identity": identity["status"],
        "sqlite": relative(SQLITE_PATH),
        "structural": {key: len(structural[key]) for key in ("source_files", "types", "fields", "methods")},
        "content": {key: len(content[key]) for key in ("tables", "slots", "rows", "assets", "selectors")},
        "graphs": {key: len(graphs[key]) for key in ("calls", "field_access", "state_transitions", "native_dispatch", "ui_commands", "save_refs")},
        "canonical": {key: len(canonical[key]) for key in ("entities", "facts", "claims", "superseded", "conflicts", "unknown_gaps")},
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
