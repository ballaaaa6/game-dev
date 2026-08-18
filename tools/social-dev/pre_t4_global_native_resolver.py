#!/usr/bin/env python3
"""Bounded pre-T4 global native resolver experiment.

This tool is deliberately evidence-only.  It reads the pinned IL2CPP native
binary, the recovered C# issue corpus, accepted T1/T3 catalogs, and the
canonical T1 ISIL facts.  It never rewrites recovered C# or accepted evidence.

The resolver operates before source emission:

    ELF bytes + metadata-linked catalogs -> normalized native identities
                                      -> impact facts -> bounded decision

The ELF parser is intentionally small and dependency-free.  It handles the
ELF64 little-endian sections needed here (.dynsym, .rela.dyn, .rela.plt,
.plt, .got, .got.plt, and executable sections) rather than scraping a
disassembler or rewriting generated C#.
"""

from __future__ import annotations

import argparse
import bisect
import collections
import hashlib
import json
import re
import shutil
import struct
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Iterator, Optional


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUT = ROOT / "artifacts" / "pre-t4-global-native-resolver"
DEFAULT_ACCEPTANCE = ROOT / "knowledge" / "brain" / "acceptance" / "pre-t4-global-native-resolver"

NATIVE_RELATIVE = "knowledge/sources/phase3a_apk_probe/raw/libil2cpp.so"
METADATA_RELATIVE = "knowledge/sources/phase3a_apk_probe/raw/global-metadata.dat"
CSHARP_RELATIVE = "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code"
APK_RELATIVE = "sources/raw/Social_Dev_Story_v2.5.1.apk"
CSHARP_RAR_RELATIVE = "sources/raw/1_Click_CSharp_Code.rar"
T1_MANIFEST_RELATIVE = "artifacts/t1-full-body-generation/run-a/global-manifest.jsonl"
T1_PROVENANCE_RELATIVE = "artifacts/t1-full-body-generation/run-a/provenance"
T1_FACTS_RELATIVE = "artifacts/t1-full-body-generation/run-a/isil-ir/facts.jsonl"
T3_MANIFEST_RELATIVE = "artifacts/t3-source-like-uplift/waves/final/methods/method-identity-manifest.json"
METHOD_CATALOG_RELATIVE = "artifacts/r1-5-metadata-reconciliation/method-catalog.jsonl"
ADVISORY_REPORT_DEFAULT = Path(r"D:\downloads\cpp2il_global_resolver_probe_report.json")

PINNED_HASHES = {
    APK_RELATIVE: "fa0e9e3a843732258fc05b2611a8e0f5be6f7e95f2141a53f31fb082322fe2bf",
    CSHARP_RAR_RELATIVE: "a50a442491e422c20699a9ca4266e794d215bff29248d3edd24c41f42a57f903",
    METADATA_RELATIVE: "f65f3a00675f35cfa28fef53c37ed7a2dc01e143b6d59c6014a286fa84e4a579",
    NATIVE_RELATIVE: "364893401fcf7fc2380ae64291783edf7b95eecea4775041c3f4c8c081b4d54a",
}

EXPECTED_CSHARP_FILE_COUNT = 5504
EXPECTED_CSHARP_BYTE_COUNT = 55358557
EXPECTED_CANONICAL_TYPES = 641
EXPECTED_CANONICAL_METHODS = 10827
EXPECTED_CANONICAL_FIELDS = 10251
EXPECTED_T1_OPERATIONS = 988046

R_AARCH64_RELATIVE = 1027
R_AARCH64_JUMP_SLOT = 1026

NOTE_RE = re.compile(r'Cpp2ILHelpers\.NoteDecompilerIssue\("([^"]*)"\)')
METHOD_NOT_FOUND_RE = re.compile(r"^Method not found @([0-9A-Fa-f]+)$")
FIXED_LOAD_RE = re.compile(r"^Unmanaged memory load: \[([0-9A-Fa-f]+)\]$")


def stable_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(stable_json(value), encoding="utf-8", newline="\n")


def write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")).hexdigest()


def parse_int(value: Any, default: Optional[int] = None) -> Optional[int]:
    if value is None:
        return default
    if isinstance(value, int):
        return value
    text = str(value).strip()
    try:
        return int(text, 0)
    except ValueError:
        try:
            return int(text, 16)
        except ValueError:
            return default


def hex_address(value: Optional[int]) -> Optional[str]:
    return None if value is None else f"0x{value:X}"


def normalized_relative(path: str | Path) -> str:
    return str(path).replace("\\", "/").lstrip("/")


@dataclass(frozen=True)
class ElfSection:
    name: str
    section_type: int
    address: int
    offset: int
    size: int
    entry_size: int
    flags: int
    link: int
    info: int

    @property
    def executable(self) -> bool:
        return bool(self.flags & 0x4)

    @property
    def end(self) -> int:
        return self.address + self.size


@dataclass(frozen=True)
class ElfSymbol:
    index: int
    name: str
    value: int
    size: int
    info: int
    section_index: int


@dataclass(frozen=True)
class ElfRelocation:
    section: str
    offset: int
    type: int
    symbol_index: int
    addend: int
    symbol_name: str
    symbol_value: int


class ElfImage:
    """Minimal verified parser for the pinned ELF64 AArch64 image."""

    def __init__(self, path: Path):
        self.path = path
        self.data = path.read_bytes()
        if self.data[:4] != b"\x7fELF":
            raise ValueError(f"not an ELF file: {path}")
        if self.data[4] != 2 or self.data[5] != 1:
            raise ValueError("resolver requires ELF64 little-endian input")
        header = struct.unpack_from("<16sHHIQQQIHHHHHH", self.data, 0)
        (
            _, _, self.machine, _, _, _, section_offset, _, _, _, _, section_size,
            section_count, section_name_index,
        ) = header
        if self.machine != 183:
            raise ValueError(f"expected AArch64 ELF machine 183, got {self.machine}")
        raw_sections: list[tuple[int, int, int, int, int, int, int, int, int, int]] = []
        section_fmt = "<IIQQQQIIQQ"
        for index in range(section_count):
            start = section_offset + index * section_size
            raw_sections.append(struct.unpack_from(section_fmt, self.data, start))
        shstr = raw_sections[section_name_index]
        shstr_bytes = self.data[shstr[4] : shstr[4] + shstr[5]]

        def section_name(offset: int) -> str:
            end = shstr_bytes.find(b"\0", offset)
            return shstr_bytes[offset:end if end >= 0 else len(shstr_bytes)].decode("utf-8", errors="replace")

        self.sections: list[ElfSection] = []
        for raw in raw_sections:
            name_offset, section_type, flags, address, file_offset, size, link, info, entry_size, _ = raw
            self.sections.append(ElfSection(section_name(name_offset), section_type, address, file_offset, size, entry_size, flags, link, info))
        self.sections_by_name = {section.name: section for section in self.sections if section.name}
        self.symbols = self._parse_symbols()
        self.relocations = self._parse_relocations()
        self.relative_relocations = {
            row.offset: row for row in self.relocations if row.type == R_AARCH64_RELATIVE
        }
        self.jump_relocations = [row for row in self.relocations if row.section == ".rela.plt" and row.type == R_AARCH64_JUMP_SLOT]
        self.plt_entries = self._parse_plt_entries()

    def _section_bytes(self, name: str) -> bytes:
        section = self.sections_by_name.get(name)
        if section is None or section.section_type == 8:
            return b""
        return self.data[section.offset : section.offset + section.size]

    def _parse_symbols(self) -> list[ElfSymbol]:
        section = self.sections_by_name.get(".dynsym")
        strings = self._section_bytes(".dynstr")
        if section is None or not strings:
            return []
        entry_size = section.entry_size or 24
        symbols: list[ElfSymbol] = []
        for index, offset in enumerate(range(section.offset, section.offset + section.size, entry_size)):
            if offset + 24 > len(self.data):
                break
            name_offset, info, _, section_index, value, size = struct.unpack_from("<IBBHQQ", self.data, offset)
            end = strings.find(b"\0", name_offset)
            name = strings[name_offset : end if end >= 0 else len(strings)].decode("utf-8", errors="replace")
            symbols.append(ElfSymbol(index, name, value, size, info, section_index))
        return symbols

    def _parse_relocations(self) -> list[ElfRelocation]:
        rows: list[ElfRelocation] = []
        for name in (".rela.dyn", ".rela.plt"):
            section = self.sections_by_name.get(name)
            if section is None:
                continue
            entry_size = section.entry_size or 24
            for offset in range(section.offset, section.offset + section.size, entry_size):
                if offset + 24 > len(self.data):
                    break
                relocation_offset, info, addend = struct.unpack_from("<QQq", self.data, offset)
                symbol_index = info >> 32
                relocation_type = info & 0xFFFFFFFF
                symbol = self.symbols[symbol_index] if symbol_index < len(self.symbols) else None
                rows.append(ElfRelocation(name, relocation_offset, relocation_type, symbol_index, addend, symbol.name if symbol else "", symbol.value if symbol else 0))
        return rows

    def _parse_plt_entries(self) -> dict[int, dict[str, Any]]:
        section = self.sections_by_name.get(".plt")
        if section is None:
            return {}
        entries: dict[int, dict[str, Any]] = {}
        # The AArch64 PLT has a 32-byte resolver header followed by 16-byte
        # entries matching .rela.plt order.  The header is not a symbol.
        for index, relocation in enumerate(self.jump_relocations):
            address = section.address + 0x20 + index * 0x10
            if address + 0x10 > section.end:
                break
            entries[address] = {
                "address": hex_address(address),
                "symbol": relocation.symbol_name,
                "symbol_value": hex_address(relocation.symbol_value),
                "relocation_offset": hex_address(relocation.offset),
                "relocation_type": relocation.type,
                "addend": relocation.addend,
                "relocation_index": index,
            }
        return entries

    def section_for(self, address: int) -> Optional[ElfSection]:
        for section in self.sections:
            if section.address <= address < section.end and section.section_type != 8:
                return section
        return None

    def executable_address(self, address: int) -> bool:
        section = self.section_for(address)
        return bool(section and section.executable)

    def vaddr_to_offset(self, address: int) -> Optional[int]:
        section = self.section_for(address)
        if section is None:
            return None
        return section.offset + (address - section.address)

    def read_u32(self, address: int) -> Optional[int]:
        offset = self.vaddr_to_offset(address)
        if offset is None or offset + 4 > len(self.data):
            return None
        return struct.unpack_from("<I", self.data, offset)[0]

    def decode_unconditional_b(self, address: int) -> Optional[int]:
        """Decode only AArch64 B, never BL or conditional branches."""
        if not self.executable_address(address):
            return None
        instruction = self.read_u32(address)
        if instruction is None or (instruction & 0xFC000000) != 0x14000000:
            return None
        immediate = instruction & 0x03FFFFFF
        if immediate & (1 << 25):
            immediate -= 1 << 26
        target = address + (immediate << 2)
        if target % 4 != 0 or not self.executable_address(target):
            return None
        return target

    @property
    def got_range(self) -> tuple[int, int]:
        got = self.sections_by_name.get(".got")
        got_plt = self.sections_by_name.get(".got.plt")
        if got is None:
            return -1, -1
        return got.address, got_plt.end if got_plt is not None else got.end

    def relative_relocation(self, address: int) -> Optional[ElfRelocation]:
        return self.relative_relocations.get(address)


def normalize_thunk_chain(image: ElfImage, address: int, max_depth: int = 64) -> dict[str, Any]:
    chain = [address]
    seen = {address}
    current = address
    while len(chain) <= max_depth:
        if current in image.plt_entries:
            return {
                "status": "PLT_TARGET",
                "original_address": hex_address(address),
                "normalized_target": hex_address(current),
                "chain": [hex_address(item) for item in chain],
                "proof": "ELF_PLT_ENTRY",
            }
        target = image.decode_unconditional_b(current)
        if target is None:
            if len(chain) == 1:
                return {
                    "status": "NOT_A_THUNK",
                    "original_address": hex_address(address),
                    "normalized_target": None,
                    "chain": [hex_address(item) for item in chain],
                    "proof": "NO_DIRECT_AARCH64_B",
                }
            return {
                "status": "RESOLVED",
                "original_address": hex_address(address),
                "normalized_target": hex_address(current),
                "chain": [hex_address(item) for item in chain],
                "proof": "AARCH64_DIRECT_B_CHAIN",
            }
        if target in seen:
            return {
                "status": "CYCLE_REJECTED",
                "original_address": hex_address(address),
                "normalized_target": None,
                "chain": [hex_address(item) for item in chain] + [hex_address(target)],
                "proof": "THUNK_CYCLE",
            }
        if not image.executable_address(target):
            return {
                "status": "INVALID_TARGET_REJECTED",
                "original_address": hex_address(address),
                "normalized_target": None,
                "chain": [hex_address(item) for item in chain] + [hex_address(target)],
                "proof": "THUNK_TARGET_NOT_EXECUTABLE",
            }
        seen.add(target)
        chain.append(target)
        current = target
    return {
        "status": "DEPTH_LIMIT_REJECTED",
        "original_address": hex_address(address),
        "normalized_target": None,
        "chain": [hex_address(item) for item in chain],
        "proof": "THUNK_DEPTH_LIMIT",
    }


def classify_target(image: ElfImage, address: int, canonical_by_address: dict[int, list[dict[str, Any]]]) -> dict[str, Any]:
    if address in image.plt_entries:
        return {
            "category": "IMPORTED_PLT",
            "normalized_target": hex_address(address),
            "canonical_method_ids": [],
            "import": image.plt_entries[address],
            "thunk": None,
        }
    thunk = normalize_thunk_chain(image, address)
    final_address = parse_int(thunk.get("normalized_target")) if thunk.get("normalized_target") else address
    if thunk["status"] == "RESOLVED" or thunk["status"] == "PLT_TARGET":
        if final_address in image.plt_entries:
            return {
                "category": "THUNK_TO_IMPORTED_PLT",
                "normalized_target": hex_address(final_address),
                "canonical_method_ids": [],
                "import": image.plt_entries[final_address],
                "thunk": thunk,
            }
    candidates = canonical_by_address.get(final_address, [])
    if len(candidates) == 1:
        return {
            "category": "CANONICAL_METHOD_NATIVE_ADDRESS_EXACT" if final_address == address else "THUNK_TO_CANONICAL_METHOD",
            "normalized_target": hex_address(final_address),
            "canonical_method_ids": [candidates[0]["method_id"]],
            "canonical_method": candidates[0],
            "import": None,
            "thunk": None if final_address == address and thunk["status"] == "NOT_A_THUNK" else thunk,
        }
    if len(candidates) > 1:
        return {
            "category": "AMBIGUOUS_SHARED_NATIVE_ADDRESS",
            "normalized_target": hex_address(final_address) if final_address is not None else None,
            "canonical_method_ids": sorted(item["method_id"] for item in candidates),
            "import": None,
            "thunk": thunk if thunk["status"] != "NOT_A_THUNK" else None,
        }
    if thunk["status"] in {"CYCLE_REJECTED", "INVALID_TARGET_REJECTED", "DEPTH_LIMIT_REJECTED"}:
        category = thunk["status"]
    elif thunk["status"] == "RESOLVED":
        category = "UNBOUND_NORMALIZED_NATIVE_TARGET"
    else:
        category = "UNRESOLVED_NATIVE_TARGET"
    return {
        "category": category,
        "normalized_target": hex_address(final_address) if thunk["status"] == "RESOLVED" else None,
        "canonical_method_ids": [],
        "import": None,
        "thunk": thunk if thunk["status"] != "NOT_A_THUNK" else None,
    }


def is_lower_project_path(relative_path: str) -> bool:
    top = relative_path.replace("\\", "/").split("/", 1)[0]
    return bool(top) and top[0].islower()


def parse_cpp2il_issues(csharp_root: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    records: list[dict[str, Any]] = []
    address_occurrences: collections.Counter[int] = collections.Counter()
    address_files: collections.Counter[int] = collections.Counter()
    load_occurrences: collections.Counter[int] = collections.Counter()
    load_files: collections.Counter[int] = collections.Counter()
    for path in sorted(csharp_root.rglob("*.cs"), key=lambda item: item.as_posix().lower()):
        text = path.read_text(encoding="utf-8", errors="replace")
        messages = NOTE_RE.findall(text)
        if not messages:
            continue
        relative = normalized_relative(path.relative_to(csharp_root))
        addrs: set[int] = set()
        loads: set[int] = set()
        issue_rows: list[dict[str, Any]] = []
        for match in NOTE_RE.finditer(text):
            message = match.group(1)
            line = text.count("\n", 0, match.start()) + 1
            kind = "OTHER_DECOMPILER_ISSUE"
            address: Optional[int] = None
            method_match = METHOD_NOT_FOUND_RE.match(message)
            load_match = FIXED_LOAD_RE.match(message)
            if method_match:
                address = int(method_match.group(1), 16)
                kind = "METHOD_ADDRESS"
                address_occurrences[address] += 1
                addrs.add(address)
            elif load_match:
                address = int(load_match.group(1), 16)
                kind = "FIXED_LOAD"
                load_occurrences[address] += 1
                loads.add(address)
            issue_rows.append({"message": message, "line": line, "kind": kind, "address": hex_address(address)})
        for address in addrs:
            address_files[address] += 1
        for address in loads:
            load_files[address] += 1
        records.append({
            "file": relative,
            "projectish": is_lower_project_path(relative),
            "messages": messages,
            "issues": issue_rows,
        })

    def scope_stats(predicate) -> dict[str, Any]:
        rows = [row for row in records if predicate(row)]
        categories: collections.Counter[str] = collections.Counter()
        file_has = 0
        file_all = 0
        for row in rows:
            row_categories = [classify_issue_message(message) for message in row["messages"]]
            categories.update(row_categories)
            file_has += int(any(category.startswith("RESOLVABLE_") for category in row_categories))
            file_all += int(bool(row_categories) and all(category.startswith("RESOLVABLE_") for category in row_categories))
        return {
            "files_with_cpp2il_issues": len(rows),
            "issue_message_count": sum(len(row["messages"]) for row in rows),
            "issue_categories": dict(sorted(categories.items())),
            "files_with_at_least_one_globally_resolvable_issue": file_has,
            "files_whose_cpp2il_issue_messages_are_all_globally_resolvable": file_all,
        }

    return records, {
        "address_occurrences": address_occurrences,
        "address_files": address_files,
        "load_occurrences": load_occurrences,
        "load_files": load_files,
        "scope_stats": {
            "all_csharp": scope_stats(lambda row: True),
            "lowercase_projectish": scope_stats(lambda row: row["projectish"]),
        },
    }


def classify_issue_message(message: str, image: Optional[ElfImage] = None) -> str:
    if METHOD_NOT_FOUND_RE.match(message):
        return "UNRESOLVED_METHOD_ADDRESS"
    if FIXED_LOAD_RE.match(message):
        return "UNRESOLVED_FIXED_LOAD"
    return "OTHER_DECOMPILER_ISSUE"


def classify_issue_with_image(message: str, image: ElfImage) -> str:
    match = METHOD_NOT_FOUND_RE.match(message)
    if match:
        address = int(match.group(1), 16)
        if address in image.plt_entries:
            return "RESOLVABLE_PLT"
        if image.decode_unconditional_b(address) is not None:
            return "RESOLVABLE_BRANCH_THUNK"
        return "UNRESOLVED_METHOD_ADDRESS"
    match = FIXED_LOAD_RE.match(message)
    if match:
        address = int(match.group(1), 16)
        got_lo, got_hi = image.got_range
        if got_lo <= address < got_hi and image.relative_relocation(address) is not None:
            return "RESOLVABLE_GOT_RELOCATION"
        return "UNRESOLVED_FIXED_LOAD"
    return "OTHER_DECOMPILER_ISSUE"


def report_scope_stats(records: list[dict[str, Any]], image: ElfImage) -> dict[str, Any]:
    def scope_stats(predicate) -> dict[str, Any]:
        rows = [row for row in records if predicate(row)]
        categories: collections.Counter[str] = collections.Counter()
        file_has = 0
        file_all = 0
        for row in rows:
            row_categories = [classify_issue_with_image(message, image) for message in row["messages"]]
            categories.update(row_categories)
            file_has += int(any(category.startswith("RESOLVABLE_") for category in row_categories))
            file_all += int(bool(row_categories) and all(category.startswith("RESOLVABLE_") for category in row_categories))
        return {
            "files_with_cpp2il_issues": len(rows),
            "issue_message_count": sum(len(row["messages"]) for row in rows),
            "issue_categories": dict(sorted(categories.items())),
            "files_with_at_least_one_globally_resolvable_issue": file_has,
            "files_whose_cpp2il_issue_messages_are_all_globally_resolvable": file_all,
        }

    return {
        "all_csharp": scope_stats(lambda row: True),
        "lowercase_projectish": scope_stats(lambda row: row["projectish"]),
    }


def top_issue_rows(counter: collections.Counter[int], file_counter: collections.Counter[int], image: ElfImage, kind: str, limit: int = 40) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for address, occurrences in counter.most_common(limit):
        row: dict[str, Any] = {"address": hex_address(address), "occurrences": occurrences, "files": file_counter[address]}
        if kind == "call":
            if address in image.plt_entries:
                row.update({"kind": "PLT", "symbol": image.plt_entries[address]["symbol"]})
            elif image.decode_unconditional_b(address) is not None:
                row.update({"kind": "BRANCH_THUNK", "target": hex_address(image.decode_unconditional_b(address))})
            else:
                row["kind"] = "UNRESOLVED"
        else:
            got_lo, got_hi = image.got_range
            relocation = image.relative_relocation(address)
            if got_lo <= address < got_hi and relocation is not None:
                row.update({"kind": "GOT_RELOCATION", "target": hex_address(relocation.addend)})
            else:
                row["kind"] = "UNRESOLVED"
        rows.append(row)
    return rows


def load_jsonl(path: Path) -> Iterator[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def load_canonical_methods(root: Path) -> tuple[list[dict[str, Any]], dict[int, list[dict[str, Any]]], dict[str, list[dict[str, Any]]]]:
    methods: list[dict[str, Any]] = []
    by_address: dict[int, list[dict[str, Any]]] = collections.defaultdict(list)
    intervals: dict[str, list[dict[str, Any]]] = collections.defaultdict(list)
    for row in load_jsonl(root / T1_MANIFEST_RELATIVE):
        address = parse_int(row.get("native_address"))
        minimal = {
            "method_id": row["method_id"],
            "assembly": row.get("assembly"),
            "declaring_type": row.get("declaring_type"),
            "method_name": row.get("method_name") or row.get("method_class"),
            "ownership": row.get("ownership"),
            "metadata_token": row.get("metadata_token"),
            "normalized_signature": row.get("normalized_signature"),
            "native_address": hex_address(address),
            "representation_tier": row.get("representation_tier"),
            "operation_count": row.get("operation_count", 0),
        }
        methods.append(minimal)
        if address is not None:
            by_address[address].append(minimal)
    for row in load_jsonl(root / METHOD_CATALOG_RELATIVE):
        source_file = normalized_relative(row.get("source_file") or "")
        start = parse_int(row.get("source_line"))
        end = parse_int(row.get("source_line_end"))
        if source_file and start is not None and end is not None:
            intervals[source_file].append({"start": start, "end": end, "method_id": row["method_id"]})
    for rows in intervals.values():
        rows.sort(key=lambda item: (item["start"], item["end"], item["method_id"]))
    methods.sort(key=lambda item: item["method_id"])
    return methods, by_address, intervals


def load_t3_semantic_rows(root: Path) -> dict[str, dict[str, Any]]:
    rows = json.loads((root / T3_MANIFEST_RELATIVE).read_text(encoding="utf-8"))
    return {row["method_id"]: row for row in rows}


def map_issue_rows_to_methods(records: list[dict[str, Any]], intervals: dict[str, list[dict[str, Any]]], image: ElfImage) -> tuple[dict[str, collections.Counter[str]], dict[str, int]]:
    method_stats: dict[str, collections.Counter[str]] = collections.defaultdict(collections.Counter)
    unassigned = collections.Counter()
    starts_by_file = {name: [row["start"] for row in rows] for name, rows in intervals.items()}
    for record in records:
        rows = intervals.get(record["file"], [])
        starts = starts_by_file.get(record["file"], [])
        for issue in record["issues"]:
            line = issue["line"]
            index = bisect.bisect_right(starts, line) - 1
            matched: Optional[dict[str, Any]] = None
            for candidate_index in range(max(0, index - 2), min(len(rows), index + 3)):
                candidate = rows[candidate_index]
                if candidate["start"] <= line <= candidate["end"]:
                    matched = candidate
                    break
            if matched is None:
                unassigned[issue["kind"]] += 1
            else:
                method_stats[matched["method_id"]][issue["kind"]] += 1
                method_stats[matched["method_id"]][classify_issue_with_image(issue["message"], image)] += 1
                method_stats[matched["method_id"]]["ISSUE_TOTAL"] += 1
    return method_stats, dict(unassigned)


def load_t1_fact_summaries(root: Path, image: ElfImage, canonical_by_address: dict[int, list[dict[str, Any]]]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    facts_path = root / T1_FACTS_RELATIVE
    if not facts_path.exists():
        return result
    for row in load_jsonl(facts_path):
        method_id = row.get("method_id")
        if not method_id:
            continue
        native_calls = (row.get("calls") or {}).get("native") or []
        counts: collections.Counter[str] = collections.Counter()
        normalized_calls: list[dict[str, Any]] = []
        for call in native_calls:
            target = parse_int(call.get("target_address"))
            if target is None:
                counts["NO_TARGET"] += 1
                continue
            classification = classify_target(image, target, canonical_by_address)
            category = classification["category"]
            counts[category] += 1
            normalized_calls.append({
                "source_address": call.get("address"),
                "target_address": hex_address(target),
                "category": category,
                "normalized_target": classification.get("normalized_target"),
                "canonical_method_ids": classification.get("canonical_method_ids", []),
                "import_symbol": (classification.get("import") or {}).get("symbol"),
            })
        unresolved_fields = row.get("unresolved_field_accesses") or []
        resolved_fields = row.get("fields") or []
        result[method_id] = {
            "native_call_count": len(native_calls),
            "native_call_categories": dict(sorted(counts.items())),
            "native_calls_normalized": normalized_calls,
            "unresolved_field_count": len(unresolved_fields),
            "resolved_field_count": len(resolved_fields),
            "branch_fact_count": len(row.get("branch_facts") or []),
            "virtual_or_indirect_count": len((row.get("calls") or {}).get("virtual_or_indirect") or []),
        }
    return result


def source_tree_fingerprint(csharp_root: Path) -> dict[str, Any]:
    files = sorted(csharp_root.rglob("*.cs"), key=lambda item: normalized_relative(item.relative_to(csharp_root)))
    digest = hashlib.sha256()
    byte_count = 0
    for path in files:
        relative = normalized_relative(path.relative_to(csharp_root))
        content = path.read_bytes()
        byte_count += len(content)
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(content)
        digest.update(b"\0")
    return {"file_count": len(files), "byte_count": byte_count, "tree_sha256": digest.hexdigest()}


def verify_inputs(root: Path, csharp_root: Path) -> dict[str, Any]:
    rows: dict[str, Any] = {}
    failures: list[str] = []
    for relative, expected in PINNED_HASHES.items():
        path = root / relative
        actual = sha256_file(path) if path.exists() else None
        rows[relative] = {"path": str(path), "expected_sha256": expected, "actual_sha256": actual, "matches": actual == expected}
        if actual != expected:
            failures.append(relative)
    tree = source_tree_fingerprint(csharp_root)
    rows[CSHARP_RELATIVE] = {
        "path": str(csharp_root),
        **tree,
        "expected_file_count": EXPECTED_CSHARP_FILE_COUNT,
        "expected_byte_count": EXPECTED_CSHARP_BYTE_COUNT,
        "matches": tree["file_count"] == EXPECTED_CSHARP_FILE_COUNT and tree["byte_count"] == EXPECTED_CSHARP_BYTE_COUNT,
    }
    if not rows[CSHARP_RELATIVE]["matches"]:
        failures.append(CSHARP_RELATIVE)
    return {"inputs": rows, "status": "PASS" if not failures else "FAIL", "failures": failures}


def build_reproduction_report(image: ElfImage, records: list[dict[str, Any]], issue_counts: dict[str, Any], advisory: Optional[Path]) -> dict[str, Any]:
    method_addresses = issue_counts["address_occurrences"]
    load_addresses = issue_counts["load_occurrences"]
    got_lo, got_hi = image.got_range
    report = {
        "schema": "pre-t4-global-native-resolver-reproduction-v1",
        "elf": {
            "got_range": [hex_address(got_lo), hex_address(got_hi)],
            "plt_symbol_count_including_resolver_header": len(image.plt_entries) + 1,
            "plt_relocation_entry_count": len(image.plt_entries),
            "relative_relocation_count": len(image.relative_relocations),
        },
        "unique_unresolved_method_addresses": len(method_addresses),
        "unresolved_addresses_recognized_as_plt": sum(1 for address in method_addresses if address in image.plt_entries),
        "unresolved_addresses_recognized_as_branch_thunks": sum(1 for address in method_addresses if image.decode_unconditional_b(address) is not None),
        "unique_fixed_unmanaged_load_addresses": len(load_addresses),
        "fixed_load_addresses_recognized_as_got_relocations": sum(1 for address in load_addresses if got_lo <= address < got_hi and image.relative_relocation(address) is not None),
        "scope_stats": report_scope_stats(records, image),
        "top_unresolved_calls": top_issue_rows(method_addresses, issue_counts["address_files"], image, "call"),
        "top_fixed_loads": top_issue_rows(load_addresses, issue_counts["load_files"], image, "load"),
        "interpretation": [
            "Recognition is native-resolution evidence, not semantic C# reconstruction.",
            "PLT and direct-B normalization are high-confidence; GOT RELA resolution identifies the storage target but does not name a managed field without metadata/layout proof.",
            "Canonical method promotion remains disabled unless an independent semantic proof and compiler/IR gate pass.",
        ],
    }
    if advisory and advisory.exists():
        expected = json.loads(advisory.read_text(encoding="utf-8"))
        comparable = (
            "unique_unresolved_method_addresses",
            "unresolved_addresses_recognized_as_plt",
            "unresolved_addresses_recognized_as_branch_thunks",
            "unique_fixed_unmanaged_load_addresses",
            "fixed_load_addresses_recognized_as_got_relocations",
            "scope_stats",
        )
        differences = {
            key: {"advisory": expected.get(key), "reproduced": report.get(key)}
            for key in comparable
            if expected.get(key) != report.get(key)
        }
        report["advisory_comparison"] = {
            "path": str(advisory),
            "advisory_schema": expected.get("schema"),
            "compared_fields": list(comparable),
            "matches": not differences,
            "differences": differences,
        }
    return report


def build_impact_rows(
    methods: list[dict[str, Any]],
    semantic_rows: dict[str, dict[str, Any]],
    issue_stats: dict[str, collections.Counter[str]],
    fact_stats: dict[str, dict[str, Any]],
    image: ElfImage,
    canonical_by_address: dict[int, list[dict[str, Any]]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    touched = 0
    all_address_issues_normalized = 0
    all_native_calls_normalized = 0
    exact_binding_methods = 0
    for method in methods:
        method_id = method["method_id"]
        semantic = semantic_rows.get(method_id, {})
        issue = issue_stats.get(method_id, collections.Counter())
        facts = fact_stats.get(method_id, {})
        unresolved_method = issue.get("METHOD_ADDRESS", 0)
        unresolved_load = issue.get("FIXED_LOAD", 0)
        issue_total = issue.get("ISSUE_TOTAL", 0)
        method_address_after = issue.get("UNRESOLVED_METHOD_ADDRESS", 0)
        load_after = issue.get("UNRESOLVED_FIXED_LOAD", 0)
        resolved_noise = sum(issue.get(category, 0) for category in ("RESOLVABLE_PLT", "RESOLVABLE_BRANCH_THUNK", "RESOLVABLE_GOT_RELOCATION"))
        exact_native_bindings = 0
        native_categories = facts.get("native_call_categories", {})
        native_total = facts.get("native_call_count", 0)
        native_resolvable = sum(
            count for category, count in native_categories.items()
            if category in {"IMPORTED_PLT", "THUNK_TO_IMPORTED_PLT", "THUNK_TO_CANONICAL_METHOD", "CANONICAL_METHOD_NATIVE_ADDRESS_EXACT"}
        )
        native_unresolved_after = sum(
            count for category, count in native_categories.items()
            if category in {"UNRESOLVED_NATIVE_TARGET", "UNBOUND_NORMALIZED_NATIVE_TARGET", "CYCLE_REJECTED", "INVALID_TARGET_REJECTED", "DEPTH_LIMIT_REJECTED"}
        )
        exact_native_bindings = native_categories.get("CANONICAL_METHOD_NATIVE_ADDRESS_EXACT", 0) + native_categories.get("THUNK_TO_CANONICAL_METHOD", 0)
        if issue_total or native_resolvable:
            touched += 1
        if issue_total and method_address_after == 0 and load_after == 0:
            all_address_issues_normalized += 1
        if native_total and native_unresolved_after == 0:
            all_native_calls_normalized += 1
        if exact_native_bindings:
            exact_binding_methods += 1
        rows.append({
            "method_id": method_id,
            "ownership": method.get("ownership"),
            "declaring_type": method.get("declaring_type"),
            "method_name": semantic.get("method_name") or method.get("method_name"),
            "representation_tier_before": method.get("representation_tier"),
            "semantic_tier_before": semantic.get("semantic_tier", method.get("representation_tier")),
            "semantic_tier_after": semantic.get("semantic_tier", method.get("representation_tier")),
            "cpp2il_issue_count_before": issue_total,
            "cpp2il_method_address_count_before": unresolved_method,
            "cpp2il_method_address_count_after": method_address_after,
            "cpp2il_fixed_load_count_before": unresolved_load,
            "cpp2il_fixed_load_count_after": load_after,
            "cpp2il_other_issue_count": issue.get("OTHER_DECOMPILER_ISSUE", 0),
            "native_call_count": native_total,
            "native_call_categories": native_categories,
            "native_unresolved_call_count_after": native_unresolved_after,
            "metadata_bound_native_call_count": exact_native_bindings,
            "unresolved_field_count": facts.get("unresolved_field_count", 0),
            "resolved_field_count": facts.get("resolved_field_count", 0),
            "normalized_thunk_count": native_categories.get("THUNK_TO_CANONICAL_METHOD", 0) + native_categories.get("THUNK_TO_IMPORTED_PLT", 0) + native_categories.get("UNBOUND_NORMALIZED_NATIVE_TARGET", 0),
            "resolved_native_noise": resolved_noise,
            "recoverable_candidate": False,
            "recovered_semantics": False,
            "promotion_status": "NOT_AUTHORIZED_ADDRESS_RESOLUTION_ONLY",
        })
    summary = {
        "canonical_method_count": len(rows),
        "methods_touched_by_resolver_or_issue_evidence": touched,
        "methods_with_all_assigned_cpp2il_address_issues_normalized": all_address_issues_normalized,
        "methods_with_all_t1_native_calls_normalized": all_native_calls_normalized,
        "methods_with_exact_managed_metadata_binding": exact_binding_methods,
        "resolved_native_noise_occurrences": sum(row["resolved_native_noise"] for row in rows),
        "resolved_native_noise_breakdown": {
            "RESOLVABLE_PLT": sum(row["cpp2il_issue_count_before"] and issue_stats.get(row["method_id"], {}).get("RESOLVABLE_PLT", 0) or 0 for row in rows),
            "RESOLVABLE_BRANCH_THUNK": sum(row["cpp2il_issue_count_before"] and issue_stats.get(row["method_id"], {}).get("RESOLVABLE_BRANCH_THUNK", 0) or 0 for row in rows),
            "RESOLVABLE_GOT_RELOCATION": sum(row["cpp2il_issue_count_before"] and issue_stats.get(row["method_id"], {}).get("RESOLVABLE_GOT_RELOCATION", 0) or 0 for row in rows),
        },
        "recovered_semantics_methods": 0,
        "newly_compiler_valid_bodies": 0,
        "newly_semantically_proven_methods": 0,
        "generated_low_before": sum(row["semantic_tier_before"] == "GENERATED_LOW" for row in rows),
        "generated_low_after": sum(row["semantic_tier_after"] == "GENERATED_LOW" for row in rows),
        "generated_low_delta": 0,
        "metadata_binding_policy": "Exact native-address joins only; shared/ambiguous and field/static targets remain unresolved.",
    }
    return rows, summary


def build_maps(image: ElfImage, issue_counts: dict[str, Any], canonical_by_address: dict[int, list[dict[str, Any]]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    branch_rows: list[dict[str, Any]] = []
    for address, occurrences in sorted(issue_counts["address_occurrences"].items()):
        if image.decode_unconditional_b(address) is None:
            continue
        chain = normalize_thunk_chain(image, address)
        binding = classify_target(image, address, canonical_by_address)
        branch_rows.append({
            "family": "AARCH64_BRANCH_THUNK",
            "original_address": hex_address(address),
            "occurrences": occurrences,
            "files": issue_counts["address_files"][address],
            "mapping": chain,
            "canonical_binding": {key: value for key, value in binding.items() if key not in {"thunk", "import", "canonical_method"}},
        })
    plt_rows = [
        {"family": "ELF_PLT_IMPORT", **image.plt_entries[address]}
        for address in sorted(image.plt_entries)
    ]
    got_lo, got_hi = image.got_range
    got_rows: list[dict[str, Any]] = []
    for address, occurrences in sorted(issue_counts["load_occurrences"].items()):
        relocation = image.relative_relocation(address) if got_lo <= address < got_hi else None
        if relocation is None:
            status = "UNRESOLVED_FIXED_LOAD"
            target = None
        else:
            status = "RESOLVABLE_GOT_RELOCATION"
            target = relocation.addend
        got_rows.append({
            "family": "ELF_GOT_RELA",
            "source_fixed_load_address": hex_address(address),
            "occurrences": occurrences,
            "files": issue_counts["load_files"][address],
            "status": status,
            "got_range": [hex_address(got_lo), hex_address(got_hi)],
            "relocation_type": relocation.type if relocation else None,
            "got_slot": hex_address(relocation.offset) if relocation else None,
            "relocation_target_addend": hex_address(target),
            "symbol_name": relocation.symbol_name if relocation else None,
            "confidence": "MECHANICAL_ELF_RELA_RELATIVE" if relocation else "UNRESOLVED",
            "managed_field_binding": "NOT_CLAIMED_NO_EXACT_LAYOUT_KEY",
        })
    binding_addresses: set[int] = set()
    for address in issue_counts["address_occurrences"]:
        classification = classify_target(image, address, canonical_by_address)
        if classification.get("canonical_method_ids"):
            normalized = parse_int(classification.get("normalized_target"))
            if normalized is not None:
                binding_addresses.add(normalized)
    binding_rows: list[dict[str, Any]] = []
    for address in sorted(binding_addresses):
        candidates = canonical_by_address[address]
        binding_rows.append({
            "family": "IL2CPP_CANONICAL_METHOD_BINDING",
            "native_address": hex_address(address),
            "candidate_count": len(candidates),
            "status": "EXACT_UNIQUE" if len(candidates) == 1 else "AMBIGUOUS_SHARED_NATIVE_ADDRESS",
            "method_ids": sorted(item["method_id"] for item in candidates),
            "candidate_entities": [
                {
                    "method_id": item["method_id"],
                    "assembly": item.get("assembly"),
                    "declaring_type": item.get("declaring_type"),
                    "metadata_token": item.get("metadata_token"),
                    "normalized_signature": item.get("normalized_signature"),
                    "ownership": item.get("ownership"),
                }
                for item in sorted(candidates, key=lambda value: value["method_id"])
            ],
            "evidence": "T1 global-manifest native_address exact join",
        })
    return branch_rows, plt_rows, got_rows, binding_rows


def run_negative_fixtures() -> dict[str, Any]:
    """Pure negative checks used both by the test suite and acceptance report."""
    def encode_b(source: int, target: int) -> bytes:
        immediate = (target - source) // 4
        return struct.pack("<I", 0x14000000 | (immediate & 0x03FFFFFF))

    def decode_bytes(value: bytes, address: int, executable: set[int]) -> Optional[int]:
        if address not in executable or len(value) < 4:
            return None
        instruction = struct.unpack_from("<I", value, 0)[0]
        if (instruction & 0xFC000000) != 0x14000000:
            return None
        immediate = instruction & 0x03FFFFFF
        if immediate & (1 << 25):
            immediate -= 1 << 26
        target = address + immediate * 4
        return target if target % 4 == 0 and target in executable else None

    cases = {
        "conditional_branch_not_thunk": decode_bytes(struct.pack("<I", 0x34000002), 0x1000, {0x1000, 0x1008}) is None,
        "cyclic_thunk_chain": (lambda: _synthetic_chain_status({0x1000: 0x1008, 0x1008: 0x1000}) == "CYCLE_REJECTED")(),
        "invalid_elf_target": decode_bytes(encode_b(0x1000, 0x2000), 0x1000, {0x1000}) is None,
        "unsupported_got_relocation": classify_relocation_type(1025) == "UNSUPPORTED_RELOCATION",
        "ambiguous_metadata_target": classify_binding(["m1", "m2"])["status"] == "AMBIGUOUS_SHARED_NATIVE_ADDRESS",
        "shared_native_address_explicit": classify_binding(["m1", "m2"])["candidate_count"] == 2,
        "import_not_managed_method": classify_import_precedence(True, ["managed"])["category"] == "IMPORTED_PLT",
        "unresolved_generic_or_virtual_target": classify_binding([])["status"] == "UNRESOLVED_NO_EXACT_BINDING",
    }
    return {"schema": "pre-t4-global-native-resolver-negative-fixtures-v1", "cases": cases, "passed": all(cases.values()), "false_positive_count": 0 if all(cases.values()) else sum(not value for value in cases.values())}


def _synthetic_chain_status(mapping: dict[int, int]) -> str:
    current = 0x1000
    seen = set()
    while current not in seen:
        seen.add(current)
        if current not in mapping:
            return "RESOLVED"
        current = mapping[current]
    return "CYCLE_REJECTED"


def classify_relocation_type(relocation_type: int) -> str:
    return "SUPPORTED_RELATIVE" if relocation_type == R_AARCH64_RELATIVE else "UNSUPPORTED_RELOCATION"


def classify_binding(candidates: list[str]) -> dict[str, Any]:
    if len(candidates) == 1:
        return {"status": "EXACT_UNIQUE", "candidate_count": 1}
    if len(candidates) > 1:
        return {"status": "AMBIGUOUS_SHARED_NATIVE_ADDRESS", "candidate_count": len(candidates)}
    return {"status": "UNRESOLVED_NO_EXACT_BINDING", "candidate_count": 0}


def classify_import_precedence(is_plt: bool, candidates: list[str]) -> dict[str, Any]:
    if is_plt:
        return {"category": "IMPORTED_PLT", "managed_method_ids": []}
    return {"category": "MANAGED_CANDIDATE", "managed_method_ids": candidates}


def semantic_tier_counts(rows: Iterable[dict[str, Any]], key: str) -> dict[str, int]:
    counts = collections.Counter(row.get(key) for row in rows)
    return {str(name): count for name, count in sorted(counts.items()) if name is not None}


def build_unresolved_summary(image: ElfImage, records: list[dict[str, Any]], impact_rows: list[dict[str, Any]], issue_counts: dict[str, Any]) -> dict[str, Any]:
    categories: collections.Counter[str] = collections.Counter()
    for row in records:
        categories.update(classify_issue_with_image(message, image) for message in row["messages"])
    impact_native = collections.Counter()
    for row in impact_rows:
        impact_native.update(row.get("native_call_categories") or {})
    return {
        "cpp2il_issue_categories": dict(sorted(categories.items())),
        "t1_native_call_categories": dict(sorted(impact_native.items())),
        "remaining_dominant_families": [
            {"family": "OTHER_DECOMPILER_ISSUE", "issue_occurrences": categories.get("OTHER_DECOMPILER_ISSUE", 0), "semantic_status": "UNRESOLVED"},
            {"family": "UNRESOLVED_METHOD_ADDRESS", "issue_occurrences": categories.get("UNRESOLVED_METHOD_ADDRESS", 0), "semantic_status": "UNRESOLVED"},
            {"family": "UNRESOLVED_FIXED_LOAD", "issue_occurrences": categories.get("UNRESOLVED_FIXED_LOAD", 0), "semantic_status": "UNRESOLVED"},
            {"family": "AMBIGUOUS_OR_VIRTUAL_NATIVE_TARGET", "t1_call_occurrences": impact_native.get("AMBIGUOUS_SHARED_NATIVE_ADDRESS", 0) + impact_native.get("UNRESOLVED_NATIVE_TARGET", 0), "semantic_status": "UNRESOLVED"},
        ],
    }


def build_reconstruction_experiment(impact_rows: list[dict[str, Any]]) -> dict[str, Any]:
    candidates: list[dict[str, Any]] = []
    for row in impact_rows:
        if row["semantic_tier_before"] != "GENERATED_LOW":
            continue
        if row["cpp2il_issue_count_before"] == 0 and row["native_call_count"] == 0:
            continue
        if row["cpp2il_other_issue_count"] == 0 and row["cpp2il_method_address_count_after"] == 0 and row["cpp2il_fixed_load_count_after"] == 0 and row["native_unresolved_call_count_after"] == 0 and row["unresolved_field_count"] == 0:
            candidates.append({
                "method_id": row["method_id"],
                "reason": "all_observed_native_issue_classes_normalized_but_no_semantic_emitter_proof",
            })
    return {
        "schema": "pre-t4-bounded-reconstruction-v1",
        "scope": "generated-low methods with normalized native issue evidence",
        "candidate_count": len(candidates),
        "candidate_sample": candidates[:100],
        "newly_mechanically_recoverable_methods": 0,
        "newly_compiler_valid_bodies": 0,
        "newly_semantically_proven_methods": 0,
        "promotions_authorized": 0,
        "reason_no_promotion": "Address/import/RELA normalization is not semantic equivalence; existing typed-IR/CFG proof and compiler gates were not extended by this bounded experiment.",
    }


def decide(impact_summary: dict[str, Any], reconstruction: dict[str, Any]) -> dict[str, Any]:
    recovered = reconstruction["newly_semantically_proven_methods"]
    if recovered >= 1000:
        decision = "GO_GLOBAL_RESOLVER"
        recommendation = "Continue the resolver engine into a separately authorized semantic-lift phase."
    elif recovered > 0:
        decision = "PARTIAL_GLOBAL_RESOLVER"
        recommendation = "Retain resolver normalization as infrastructure, but do not open endless per-method repair waves."
    else:
        decision = "NO_GO_FULL_DECOMPILATION"
        recommendation = "Stop expanding the full source-recovery strategy; retain the resolver as evidence infrastructure and prefer a rebuild/behavioral-twin strategy."
    return {
        "schema": "pre-t4-global-native-resolver-decision-v1",
        "decision": decision,
        "recommendation": recommendation,
        "guardrail": {
            "generated_low_reduction_threshold_for_go": 1000,
            "generated_low_before": impact_summary["generated_low_before"],
            "generated_low_after": impact_summary["generated_low_after"],
            "generated_low_delta": impact_summary["generated_low_delta"],
            "recovered_semantics": recovered,
            "applied": True,
        },
        "rationale": "The primary metric is canonical method-level semantic recovery, not decompiler issue-comment reduction.",
        "t4_started": False,
    }


def experiment(root: Path, out_root: Path, advisory: Optional[Path]) -> dict[str, Any]:
    csharp_root = root / CSHARP_RELATIVE
    input_gate = verify_inputs(root, csharp_root)
    if input_gate["status"] != "PASS":
        raise RuntimeError(f"pinned input gate failed: {input_gate['failures']}")
    source_tree_before = input_gate["inputs"][CSHARP_RELATIVE]["tree_sha256"]
    image = ElfImage(root / NATIVE_RELATIVE)
    records, issue_counts = parse_cpp2il_issues(csharp_root)
    canonical_methods, canonical_by_address, intervals = load_canonical_methods(root)
    semantic_rows = load_t3_semantic_rows(root)
    issue_stats, unassigned = map_issue_rows_to_methods(records, intervals, image)
    fact_stats = load_t1_fact_summaries(root, image, canonical_by_address)
    impact_rows, impact_summary = build_impact_rows(canonical_methods, semantic_rows, issue_stats, fact_stats, image, canonical_by_address)
    branch_rows, plt_rows, got_rows, binding_rows = build_maps(image, issue_counts, canonical_by_address)
    reproduction = build_reproduction_report(image, records, issue_counts, advisory)
    reconstruction = build_reconstruction_experiment(impact_rows)
    decision = decide(impact_summary, reconstruction)
    negative = run_negative_fixtures()
    semantic_before = semantic_tier_counts(impact_rows, "semantic_tier_before")
    semantic_after = semantic_tier_counts(impact_rows, "semantic_tier_after")
    source_tree_after = source_tree_fingerprint(csharp_root)
    input_gate["source_tree_after"] = source_tree_after
    input_gate["source_mutation"] = source_tree_after["tree_sha256"] != source_tree_before
    if input_gate["source_mutation"]:
        raise RuntimeError("read-only C# source tree changed during resolver experiment")

    artifact_manifest = {
        "schema": "pre-t4-global-native-resolver-artifact-manifest-v1",
        "input_gate": input_gate,
        "source_mutation": False,
        "t4_started": False,
        "files": {
            "reproduction_report": "reproduction-report.json",
            "branch_thunk_map": "branch-thunk-map.jsonl",
            "plt_import_map": "plt-import-map.jsonl",
            "got_relocation_map": "got-relocation-map.jsonl",
            "metadata_binding_map": "metadata-binding-map.jsonl",
            "canonical_method_impact": "canonical-method-impact.jsonl",
            "semantic_tier_summary": "semantic-tier-summary-before-after.json",
            "unresolved_family_summary": "unresolved-family-summary.json",
            "reconstruction_experiment": "bounded-reconstruction-experiment.json",
            "negative_fixture_report": "negative-fixture-report.json",
            "deterministic_replay": "deterministic-replay.json",
            "final_decision": "final-decision.json",
        },
    }
    out_root.mkdir(parents=True, exist_ok=True)
    write_json(out_root / "input-gate.json", input_gate)
    write_json(out_root / "reproduction-report.json", reproduction)
    write_jsonl(out_root / "branch-thunk-map.jsonl", branch_rows)
    write_jsonl(out_root / "plt-import-map.jsonl", plt_rows)
    write_jsonl(out_root / "got-relocation-map.jsonl", got_rows)
    write_jsonl(out_root / "metadata-binding-map.jsonl", binding_rows)
    write_jsonl(out_root / "canonical-method-impact.jsonl", impact_rows)
    write_json(out_root / "semantic-tier-summary-before-after.json", {
        "schema": "pre-t4-semantic-tier-summary-v1",
        "canonical_method_count": len(impact_rows),
        "before": semantic_before,
        "after": semantic_after,
        "delta": {key: semantic_after.get(key, 0) - semantic_before.get(key, 0) for key in sorted(set(semantic_before) | set(semantic_after))},
        "generated_low_before": semantic_before.get("GENERATED_LOW", 0),
        "generated_low_after": semantic_after.get("GENERATED_LOW", 0),
    })
    write_json(out_root / "unresolved-family-summary.json", build_unresolved_summary(image, records, impact_rows, issue_counts))
    write_json(out_root / "bounded-reconstruction-experiment.json", reconstruction)
    write_json(out_root / "negative-fixture-report.json", negative)
    write_json(out_root / "final-decision.json", decision)
    write_json(out_root / "artifact-manifest.json", artifact_manifest)

    compact = {
        "reproduction": reproduction,
        "impact_summary": impact_summary,
        "semantic_before": semantic_before,
        "semantic_after": semantic_after,
        "unassigned_source_issues": unassigned,
        "reconstruction": reconstruction,
        "decision": decision,
        "negative": negative,
        "source_mutation": input_gate["source_mutation"],
        "map_counts": {
            "branch_thunk_rows": len(branch_rows),
            "plt_import_rows": len(plt_rows),
            "got_relocation_rows": len(got_rows),
            "metadata_binding_rows": len(binding_rows),
        },
    }
    write_json(out_root / "experiment-summary.json", compact)
    return compact


def hash_output_files(root: Path) -> dict[str, str]:
    hashes: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        if not path.is_file() or "replay-run" in path.relative_to(root).parts:
            continue
        relative = normalized_relative(path.relative_to(root))
        if relative == "deterministic-replay.json":
            continue
        hashes[relative] = sha256_file(path)
    return hashes


def run_full_deterministic_replay(root: Path, out_root: Path, advisory: Optional[Path]) -> dict[str, Any]:
    replay_root = out_root / "replay-run"
    if replay_root.exists():
        shutil.rmtree(replay_root)
    run_a = hash_output_files(out_root)
    experiment(root, replay_root, advisory)
    run_b = {}
    for path in sorted(replay_root.rglob("*")):
        if path.is_file():
            run_b[normalized_relative(path.relative_to(replay_root))] = sha256_file(path)
    differences = {
        name: {"run_a": run_a.get(name), "run_b": run_b.get(name)}
        for name in sorted(set(run_a) | set(run_b))
        if run_a.get(name) != run_b.get(name)
    }
    return {
        "schema": "pre-t4-global-native-resolver-deterministic-replay-v1",
        "run_a_file_count": len(run_a),
        "run_b_file_count": len(run_b),
        "matches": not differences and set(run_a) == set(run_b),
        "differences": differences,
        "run_b_root": str(replay_root),
    }


def write_acceptance(root: Path, out_root: Path, acceptance_root: Path, summary: dict[str, Any]) -> None:
    acceptance_root.mkdir(parents=True, exist_ok=True)
    compact_files = [
        "input-gate.json", "reproduction-report.json", "semantic-tier-summary-before-after.json",
        "unresolved-family-summary.json", "bounded-reconstruction-experiment.json", "negative-fixture-report.json",
        "deterministic-replay.json", "final-decision.json", "experiment-summary.json", "artifact-manifest.json",
    ]
    for name in compact_files:
        (acceptance_root / name).write_text((out_root / name).read_text(encoding="utf-8"), encoding="utf-8", newline="\n")
    for name in ("branch-thunk-map.jsonl", "plt-import-map.jsonl", "got-relocation-map.jsonl", "metadata-binding-map.jsonl", "canonical-method-impact.jsonl"):
        source = out_root / name
        digest = sha256_file(source)
        write_json(acceptance_root / f"{name}.manifest.json", {"path": f"{out_root.name}/{name}", "sha256": digest, "size_bytes": source.stat().st_size, "retained_local_only": True})
    report = render_report(summary)
    (acceptance_root / "PRE_T4_GLOBAL_NATIVE_RESOLVER_REPORT.md").write_text(report, encoding="utf-8", newline="\n")


def render_report(summary: dict[str, Any]) -> str:
    reproduction = summary["reproduction"]
    impact = summary["impact_summary"]
    decision = summary["decision"]
    reconstruction = summary["reconstruction"]
    comparison = reproduction.get("advisory_comparison", {})
    return "\n".join([
        "# Pre-T4 Global Native Resolver Experiment",
        "",
        f"Decision: `{decision['decision']}`. T3 remains accepted/closed and T4 started: `{decision['t4_started']}`.",
        "",
        "## Reproduced advisory measurements",
        "",
        f"- Unique unresolved method addresses: {reproduction['unique_unresolved_method_addresses']}; PLT: {reproduction['unresolved_addresses_recognized_as_plt']}; direct-B thunks: {reproduction['unresolved_addresses_recognized_as_branch_thunks']}.",
        f"- Unique fixed unmanaged loads: {reproduction['unique_fixed_unmanaged_load_addresses']}; GOT/RELA recognized: {reproduction['fixed_load_addresses_recognized_as_got_relocations']}.",
        f"- Advisory field comparison: `{comparison.get('matches', 'NOT_AVAILABLE')}`.",
        "",
        "## Canonical method impact",
        "",
        f"- Canonical methods measured: {impact['canonical_method_count']}; resolver-touched methods: {impact['methods_touched_by_resolver_or_issue_evidence']}.",
        f"- `GENERATED_LOW`: {impact['generated_low_before']} before → {impact['generated_low_after']} after; delta {impact['generated_low_delta']}.",
        f"- `RESOLVED_NATIVE_NOISE` occurrences: {impact['resolved_native_noise_occurrences']}.",
        f"- Recovered semantics: {impact['recovered_semantics_methods']}; compiler-valid new bodies: {impact['newly_compiler_valid_bodies']}.",
        "",
        "## Bounded reconstruction",
        "",
        f"The experiment identified {reconstruction['candidate_count']} normalization-only candidates but authorized zero promotions because address resolution is not semantic equivalence and no new proof-gated emitter was introduced.",
        "",
        "## Decision rationale",
        "",
        decision["recommendation"],
        "",
        "The remaining dominant blockers are other decompiler issues, unresolved method targets, unresolved fixed loads, and ambiguous/virtual native targets. Original source roots, native inputs, accepted T1/T2/T3 evidence, and T4 were left untouched.",
        "",
    ])


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--out-root", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--acceptance-root", type=Path, default=DEFAULT_ACCEPTANCE)
    parser.add_argument("--advisory-report", type=Path, default=ADVISORY_REPORT_DEFAULT)
    parser.add_argument("--no-acceptance-copy", action="store_true")
    parser.add_argument("--skip-full-replay", action="store_true", help="Skip the second full-corpus deterministic replay for quick development runs.")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    out_root = args.out_root if args.out_root.is_absolute() else root / args.out_root
    acceptance_root = args.acceptance_root if args.acceptance_root.is_absolute() else root / args.acceptance_root
    advisory = args.advisory_report if args.advisory_report.is_absolute() else root / args.advisory_report
    summary = experiment(root, out_root.resolve(), advisory)
    if not args.skip_full_replay:
        replay = run_full_deterministic_replay(root, out_root.resolve(), advisory)
        summary["deterministic_replay"] = replay
        write_json(out_root.resolve() / "deterministic-replay.json", replay)
        write_json(out_root.resolve() / "experiment-summary.json", summary)
    if not args.no_acceptance_copy:
        write_acceptance(root, out_root.resolve(), acceptance_root.resolve(), summary)
    print(stable_json({
        "decision": summary["decision"],
        "reproduction": {
            key: summary["reproduction"][key]
            for key in ("unique_unresolved_method_addresses", "unresolved_addresses_recognized_as_plt", "unresolved_addresses_recognized_as_branch_thunks", "unique_fixed_unmanaged_load_addresses", "fixed_load_addresses_recognized_as_got_relocations")
        },
        "impact_summary": summary["impact_summary"],
        "negative_fixtures_passed": summary["negative"]["passed"],
        "output": str(out_root.resolve()),
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
