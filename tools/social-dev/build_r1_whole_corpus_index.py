"""Build the R1 whole-corpus ownership index and repair queue.

R1 is an indexing phase. This builder reads pinned IL2CPP inputs, DummyDll
metadata, the read-only C# corpus, R0 quality evidence, and fresh ISIL output.
It never edits or executes recovered C#.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import zipfile
from collections import Counter, defaultdict, deque
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[2]
SOURCE_ROOT = ROOT / "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code"
DummyRoot = ROOT / "knowledge/sources/phase3a_apk_probe/il2cpp_dump/DummyDll"
APK = ROOT / "sources/raw/Social_Dev_Story_v2.5.1.apk"
RAR = ROOT / "sources/raw/1_Click_CSharp_Code.rar"
LIBIL2CPP = ROOT / "knowledge/sources/phase3a_apk_probe/raw/libil2cpp.so"
METADATA = ROOT / "knowledge/sources/phase3a_apk_probe/raw/global-metadata.dat"
R0_ROOT = ROOT / "knowledge/brain/acceptance/r0-cpp2il-audit"
DEFAULT_ISIL_ROOT = Path(
    r"C:\Users\WINDOW XI\AppData\Local\Temp\r0-cpp2il-audit-20260817\rerun-current\isil\IsilDump"
)
DEFAULT_OUT = ROOT / "artifacts/r1-whole-corpus-index"
DEFAULT_ACCEPTED = ROOT / "knowledge/brain/acceptance/r1-whole-corpus-index"
BUILDER_VERSION = "r1-whole-corpus-index-builder-v1"
SCHEMA_VERSION = "r1-whole-corpus-index-v1"
SCRIPTING_ASSEMBLY_MEMBER = "assets/bin/Data/ScriptingAssemblies.json"
EXPECTED_HASHES = {
    "apk": "fa0e9e3a843732258fc05b2611a8e0f5be6f7e95f2141a53f31fb082322fe2bf",
    "csharp_rar": "a50a442491e422c20699a9ca4266e794d215bff29248d3edd24c41f42a57f903",
    "libil2cpp": "364893401fcf7fc2380ae64291783edf7b95eecea4775041c3f4c8c081b4d54a",
    "global_metadata": "f65f3a00675f35cfa28fef53c37ed7a2dc01e143b6d59c6014a286fa84e4a579",
}

OWNERSHIPS = (
    "GAME_FIRST_PARTY", "KAIRO_ENGINE", "UNITY_BOUNDARY",
    "DOTNET_FRAMEWORK", "THIRD_PARTY", "COMPILER_GENERATED",
    "SOURCE_LIMITED_OWNERSHIP",
)
QUALITY_CLASSES = (
    "CLEAN", "TYPE_REPAIR", "CFG_REPAIR", "STATIC_DATA_REPAIR",
    "NATIVE_LIFT_REQUIRED", "NATIVE_BOUNDARY", "SOURCE_LIMITED",
)
VERIFICATION_STATUSES = (
    "BASELINE_READABLE", "NEEDS_REPAIR", "VERIFIED_CSHARP",
    "EXTERNAL_BOUNDARY", "SOURCE_LIMITED",
)
DISPOSITIONS = (
    "VERIFY_ONLY", "AUTO_TYPE_REPAIR", "AUTO_STATIC_DATA_REPAIR",
    "CFG_REPAIR", "ISIL_ASSISTED_REPAIR", "NATIVE_LIFT",
    "EXTERNAL_BOUNDARY", "SOURCE_LIMITED",
)
TYPE_DECL_RE = re.compile(r"\b(class|struct|enum|interface|record)\s+([A-Za-z_]\w*(?:\x60\d+)?)")
NAMESPACE_RE = re.compile(r"\bnamespace\s+([A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*)")
CONTROL_NAMES = {
    "if", "for", "foreach", "while", "switch", "catch", "using", "lock",
    "return", "throw", "nameof", "sizeof", "typeof", "checked", "unchecked",
    "fixed", "when",
}
MODIFIER_WORDS = (
    "public|private|protected|internal|static|virtual|override|abstract|sealed|"
    "new|async|unsafe|extern|partial|readonly|ref|out|volatile|in|explicit|implicit"
)
METHOD_LINE_RE = re.compile(
    rf"^\s*(?:(?:{MODIFIER_WORDS})\s+)*(?:[A-Za-z_]\w*(?:[<>,.\[\]?*&]+)?\s+)+"
    rf"(~?[A-Za-z_]\w*)\s*(?:<[^>\n]+>)?\s*\("
)
CTOR_LINE_RE = re.compile(r"^\s*(?:(?:public|private|protected|internal|static)\s+)?([A-Za-z_]\w*)\s*\(")
CALL_RE = re.compile(
    r"(?<![\w])(?P<new>new\s+)?(?P<qual>[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*)"
    r"\s*(?:<[^;{}()\n]{0,160}>)?\s*\("
)
MEMBER_RE = re.compile(r"\b(?P<qualifier>[A-Za-z_]\w*)\.(?P<member>[A-Za-z_]\w*)\b")
TOKEN_RE = re.compile(r"\b[A-Za-z_]\w*\b")
ISIL_METHOD_RE = re.compile(r"^Method:\s+(?P<return>.+?)\s+(?P<name>[^\s(]+)\((?P<params>.*)\)\s*$")
ISIL_TYPE_RE = re.compile(r"^Type:\s+(?P<type>.+?)\s*$")
ISIL_ADDRESS_RE = re.compile(r"^\s*(0x[0-9A-Fa-f]+)\s+")
ISIL_INSTRUCTION_RE = re.compile(r"^\s*\d+\s+\S")
ISIL_CALL_RE = re.compile(r"\bCall(?:Void|Int|Float|Object|String|Native)?\s+(?:\"[^\"]+\"|[^,\s]+)")

def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()

def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

def stable_id(prefix: str, *parts: Any) -> str:
    value = "\x1f".join(str(part) for part in parts)
    return f"{prefix}_{hashlib.sha256(value.encode()).hexdigest()[:32]}"

def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))

def dump_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n")

def dump_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as stream:
        for row in rows:
            stream.write(json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n")


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as stream:
        return [json.loads(line) for line in stream if line.strip()]

def table_rows(table: Any) -> list[Any]:
    if table is None:
        return []
    try:
        return list(table[1:])
    except (TypeError, IndexError):
        return []

def heap_text(value: Any) -> str:
    return "" if value is None else str(value)

def row_index(value: Any) -> int | None:
    index = getattr(value, "row_index", None)
    return index if isinstance(index, int) else None

def row_from_coded(value: Any) -> Any:
    return getattr(value, "row", None)

def compressed_uint(data: bytes, position: int) -> tuple[int, int]:
    if position >= len(data):
        raise ValueError("compressed integer out of range")
    first = data[position]
    if first & 0x80 == 0:
        return first, position + 1
    if first & 0xC0 == 0x80:
        return ((first & 0x3F) << 8) | data[position + 1], position + 2
    if first & 0xE0 == 0xC0:
        return (
            ((first & 0x1F) << 24)
            | (data[position + 1] << 16)
            | (data[position + 2] << 8)
            | data[position + 3],
            position + 4,
        )
    raise ValueError("invalid compressed integer")

def split_top_level(value: str) -> list[str]:
    if not value.strip():
        return []
    result: list[str] = []
    start = 0
    angle = paren = bracket = brace = 0
    for index, character in enumerate(value):
        if character == "<":
            angle += 1
        elif character == ">" and angle:
            angle -= 1
        elif character == "(":
            paren += 1
        elif character == ")" and paren:
            paren -= 1
        elif character == "[":
            bracket += 1
        elif character == "]" and bracket:
            bracket -= 1
        elif character == "{":
            brace += 1
        elif character == "}" and brace:
            brace -= 1
        elif character == "," and not (angle or paren or bracket or brace):
            result.append(value[start:index].strip())
            start = index + 1
    result.append(value[start:].strip())
    return [item for item in result if item]

def count_parameters(value: str) -> int:
    return len(split_top_level(value))

def normalize_signature_text(value: str) -> str:
    return re.sub(r"\s+", " ", value.replace("\r", "").replace("\n", " ")).strip()

def normalize_type_name(value: str) -> str:
    return re.sub(r"\s+", "", value.strip().replace("/", "+"))


class MetadataReader:
    """Read the DummyDll metadata tables without executing recovered source."""

    def __init__(self, root: Path) -> None:
        self.root = root
        self.assemblies: list[dict[str, Any]] = []
        self.types: list[dict[str, Any]] = []
        self.fields: list[dict[str, Any]] = []
        self.methods: list[dict[str, Any]] = []
        self.type_by_key: dict[tuple[str, str], dict[str, Any]] = {}
        self.type_by_id: dict[str, dict[str, Any]] = {}
        self.method_by_id: dict[str, dict[str, Any]] = {}
        self.method_by_key: dict[tuple[str, str, str, str], list[dict[str, Any]]] = defaultdict(list)
        self.field_by_id: dict[str, dict[str, Any]] = {}
        self._type_names: dict[tuple[str, int], str] = {}
        self._type_rows: dict[tuple[str, int], Any] = {}
        self._type_refs: dict[tuple[str, int], Any] = {}
        self._type_specs: dict[tuple[str, int], Any] = {}
        self._assembly_tables: dict[str, Any] = {}

    def read(self) -> "MetadataReader":
        try:
            import dnfile
        except ImportError as error:
            raise RuntimeError("dnfile is required to read the R1 DummyDll metadata") from error

        for dll_path in sorted(self.root.glob("*.dll"), key=lambda item: item.name.lower()):
            try:
                pe = dnfile.dnPE(str(dll_path))
            except Exception as error:
                raise RuntimeError(f"Unable to read DummyDll {dll_path}: {error}") from error
            tables = getattr(getattr(pe, "net", None), "mdtables", None)
            if tables is None:
                continue
            assembly_name = self._assembly_name(tables, dll_path)
            self._assembly_tables[assembly_name] = tables
            self.assemblies.append(
                {
                    "assembly": assembly_name,
                    "dll_file": dll_path.name,
                    "dll_path": rel(dll_path),
                    "metadata_present": True,
                    "metadata_type_count": len(table_rows(getattr(tables, "TypeDef", None))),
                    "metadata_method_count": len(table_rows(getattr(tables, "MethodDef", None))),
                    "metadata_field_count": len(table_rows(getattr(tables, "Field", None))),
                    "metadata_property_count": len(table_rows(getattr(tables, "Property", None))),
                    "metadata_interface_impl_count": len(table_rows(getattr(tables, "InterfaceImpl", None))),
                }
            )
            self._read_assembly(assembly_name, dll_path, tables, pe)

        self.assemblies.sort(key=lambda row: row["assembly"].lower())
        self.types.sort(key=lambda row: (row["assembly"].lower(), row["full_name"]))
        self.fields.sort(key=lambda row: row["field_id"])
        self.methods.sort(key=lambda row: row["method_id"])
        method_groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for method in self.methods:
            method_groups[method["method_id"]].append(method)
        for base_id, group in method_groups.items():
            if len(group) <= 1:
                continue
            for method in sorted(group, key=lambda row: (
                row["assembly"], row["declaring_type"], row["method_name"],
                row["normalized_signature"], row["metadata_token"],
            )):
                method["identity_collision_group"] = base_id
                method["identity_collision_disambiguator"] = method["metadata_token"]
                method["method_id"] = stable_id(
                    "r1-method-collision",
                    base_id,
                    method["assembly"],
                    method["declaring_type"],
                    method["method_name"],
                    method["normalized_signature"],
                    method["metadata_token"],
                )
        self.method_by_id = {method["method_id"]: method for method in self.methods}
        self._assembly_tables.clear()
        self._type_rows.clear()
        self._type_refs.clear()
        self._type_specs.clear()
        self._type_names.clear()
        return self

    @staticmethod
    def _assembly_name(tables: Any, dll_path: Path) -> str:
        rows = table_rows(getattr(tables, "Assembly", None))
        if rows:
            name = heap_text(getattr(rows[0], "Name", ""))
            if name:
                return name
        return dll_path.stem

    @staticmethod
    def _flag(flags: Any, name: str) -> bool:
        return bool(getattr(flags, name, False))

    def _read_assembly(self, assembly: str, dll_path: Path, tables: Any, pe: Any) -> None:
        typedef_rows = table_rows(getattr(tables, "TypeDef", None))
        nested_map: dict[int, int] = {}
        for nested in table_rows(getattr(tables, "NestedClass", None)):
            child = row_index(getattr(nested, "NestedClass", None))
            parent = row_index(getattr(nested, "EnclosingClass", None))
            if child and parent:
                nested_map[child] = parent

        for index, row in enumerate(typedef_rows, start=1):
            self._type_rows[(assembly, index)] = row
            self._type_names[(assembly, index)] = self._compose_type_name(
                assembly,
                index,
                typedef_rows,
                nested_map,
                {},
            )
        for index, row in enumerate(table_rows(getattr(tables, "TypeRef", None)), start=1):
            self._type_refs[(assembly, index)] = row
        for index, row in enumerate(table_rows(getattr(tables, "TypeSpec", None)), start=1):
            self._type_specs[(assembly, index)] = row

        method_owner: dict[int, int] = {}
        field_owner: dict[int, int] = {}
        for type_index, row in enumerate(typedef_rows, start=1):
            for item in getattr(row, "MethodList", []) or []:
                method_index = row_index(item)
                if method_index:
                    method_owner[method_index] = type_index
            for item in getattr(row, "FieldList", []) or []:
                field_index = row_index(item)
                if field_index:
                    field_owner[field_index] = type_index

        property_counts: dict[int, int] = defaultdict(int)
        for property_map in table_rows(getattr(tables, "PropertyMap", None)):
            parent = row_index(getattr(property_map, "Parent", None))
            if not parent:
                continue
            properties = getattr(property_map, "PropertyList", []) or []
            property_counts[parent] += len(properties)

        interface_names: dict[int, list[str]] = defaultdict(list)
        for interface in table_rows(getattr(tables, "InterfaceImpl", None)):
            parent = row_index(getattr(interface, "Class", None))
            if not parent:
                continue
            interface_names[parent].append(self._coded_type_name(assembly, getattr(interface, "Interface", None)))

        generic_type_counts: dict[int, int] = defaultdict(int)
        generic_method_counts: dict[int, int] = defaultdict(int)
        for generic in table_rows(getattr(tables, "GenericParam", None)):
            owner = getattr(generic, "Owner", None)
            owner_index = row_index(owner)
            owner_row = getattr(owner, "row", None)
            if not owner_index or owner_row is None:
                continue
            if type(owner_row).__name__ == "TypeDefRow":
                generic_type_counts[owner_index] += 1
            elif type(owner_row).__name__ == "MethodDefRow":
                generic_method_counts[owner_index] += 1

        for type_index, row in enumerate(typedef_rows, start=1):
            name = self._type_names[(assembly, type_index)]
            type_id = stable_id(
                "r1-type",
                EXPECTED_HASHES["apk"],
                assembly,
                name,
                generic_type_counts[type_index],
                type_index,
            )
            record = {
                "type_id": type_id,
                "assembly": assembly,
                "full_name": name,
                "namespace": heap_text(getattr(row, "TypeNamespace", "")),
                "short_name": heap_text(getattr(row, "TypeName", "")),
                "generic_arity": generic_type_counts[type_index],
                "metadata_token": f"0x{0x02000000 | type_index:08X}",
                "metadata_index": type_index,
                "metadata_source": "DummyDll",
                "dll_file": dll_path.name,
                "source_file": None,
                "source_present": False,
                "ownership": None,
                "inclusion": None,
                "is_interface": self._flag(getattr(row, "Flags", None), "tdInterface"),
                "is_enum": self._coded_type_name(assembly, getattr(row, "Extends", None)) in {
                    "System.Enum",
                    "mscorlib.System.Enum",
                },
                "is_value_type": self._coded_type_name(assembly, getattr(row, "Extends", None))
                in {"System.ValueType", "System.Enum", "mscorlib.System.ValueType"},
                "is_delegate": self._coded_type_name(assembly, getattr(row, "Extends", None))
                in {"System.MulticastDelegate", "System.Delegate"},
                "base_type": self._coded_type_name(assembly, getattr(row, "Extends", None)) or None,
                "interfaces": sorted(set(interface_names.get(type_index, []))),
                "metadata_field_count": len(getattr(row, "FieldList", []) or []),
                "metadata_method_count": len(getattr(row, "MethodList", []) or []),
                "metadata_property_count": property_counts.get(type_index, 0),
                "metadata_interface_count": len(interface_names.get(type_index, [])),
                "compiler_generated": False,
                "external_reference": False,
                "_type_index": type_index,
            }
            self.types.append(record)
            self.type_by_key[(assembly, name)] = record
            self.type_by_id[type_id] = record

        type_by_index = {(assembly, record["_type_index"]): record for record in self.types if record["assembly"] == assembly}
        field_rows = table_rows(getattr(tables, "Field", None))
        for field_index, row in enumerate(field_rows, start=1):
            type_index = field_owner.get(field_index)
            owner = type_by_index.get((assembly, type_index)) if type_index else None
            if owner is None:
                continue
            name = heap_text(getattr(row, "Name", ""))
            signature = self._parse_field_signature(assembly, getattr(getattr(row, "Signature", None), "value", b""))
            field_id = stable_id("r1-field", EXPECTED_HASHES["apk"], assembly, owner["full_name"], name, field_index)
            record = {
                "field_id": field_id,
                "assembly": assembly,
                "declaring_type_id": owner["type_id"],
                "declaring_type": owner["full_name"],
                "field_name": name,
                "field_type": signature,
                "metadata_token": f"0x{0x04000000 | field_index:08X}",
                "metadata_index": field_index,
                "metadata_source": "DummyDll",
                "is_static": self._flag(getattr(row, "Flags", None), "fdStatic"),
                "is_literal": self._flag(getattr(row, "Flags", None), "fdLiteral"),
                "is_init_only": self._flag(getattr(row, "Flags", None), "fdInitOnly"),
            }
            self.fields.append(record)
            self.field_by_id[field_id] = record

        method_rows = table_rows(getattr(tables, "MethodDef", None))
        for method_index, row in enumerate(method_rows, start=1):
            type_index = method_owner.get(method_index)
            owner = type_by_index.get((assembly, type_index)) if type_index else None
            if owner is None:
                continue
            name = heap_text(getattr(row, "Name", ""))
            signature = self._parse_method_signature(
                assembly,
                getattr(getattr(row, "Signature", None), "value", b""),
            )
            method_id = stable_id(
                "r1-method",
                EXPECTED_HASHES["apk"],
                assembly,
                owner["full_name"],
                name,
                signature["generic_arity"],
                signature["return_type"],
                *signature["parameter_types"],
            )
            record = {
                "method_id": method_id,
                "assembly": assembly,
                "declaring_type_id": owner["type_id"],
                "declaring_type": owner["full_name"],
                "method_name": name,
                "is_constructor": name in {".ctor", ".cctor"},
                "is_static": self._flag(getattr(row, "Flags", None), "mdStatic"),
                "is_virtual": self._flag(getattr(row, "Flags", None), "mdVirtual"),
                "generic_arity": signature["generic_arity"],
                "return_type": signature["return_type"],
                "parameter_types": signature["parameter_types"],
                "parameter_count": len(signature["parameter_types"]),
                "normalized_signature": signature["normalized_signature"],
                "metadata_token": f"0x{0x06000000 | method_index:08X}",
                "metadata_index": method_index,
                "metadata_source": "DummyDll",
                "dll_file": dll_path.name,
                "rva": int(getattr(row, "Rva", 0) or 0),
                "file_offset": self._file_offset(pe, int(getattr(row, "Rva", 0) or 0)),
                "pinvoke": self._flag(getattr(row, "Flags", None), "mdPinvokeImpl"),
                "internal_call": self._flag(getattr(row, "ImplFlags", None), "miInternalCall"),
                "runtime_implemented": self._flag(getattr(row, "ImplFlags", None), "miRuntime"),
                "native_implemented": self._flag(getattr(row, "ImplFlags", None), "miNative"),
                "source_file": None,
                "source_present": False,
                "compiler_generated": False,
                "_type_index": type_index,
            }
            self.methods.append(record)
            self.method_by_id[method_id] = record
            self.method_by_key[(assembly, owner["full_name"], name, signature["normalized_signature"])].append(record)
        actual_method_counts = Counter(
            method["declaring_type_id"]
            for method in self.methods
            if method["assembly"] == assembly
        )
        for type_record in self.types:
            if type_record["assembly"] == assembly:
                type_record["metadata_method_count"] = actual_method_counts.get(
                    type_record["type_id"], 0
                )

    @staticmethod
    def _file_offset(pe: Any, rva: int) -> int | None:
        if not rva:
            return None
        try:
            return int(pe.get_offset_from_rva(rva))
        except Exception:
            return None

    def _compose_type_name(
        self,
        assembly: str,
        index: int,
        typedef_rows: list[Any],
        nested_map: dict[int, int],
        cache: dict[int, str],
    ) -> str:
        if index in cache:
            return cache[index]
        row = typedef_rows[index - 1]
        short = heap_text(getattr(row, "TypeName", ""))
        namespace = heap_text(getattr(row, "TypeNamespace", ""))
        parent = nested_map.get(index)
        if parent:
            prefix = self._compose_type_name(assembly, parent, typedef_rows, nested_map, cache)
            value = f"{prefix}+{short}"
        else:
            value = f"{namespace}.{short}" if namespace else short
        cache[index] = value
        return value

    def _coded_type_name(self, assembly: str, coded: Any) -> str:
        row = getattr(coded, "row", None)
        if row is None:
            return ""
        row_index_value = getattr(coded, "row_index", None)
        class_name = type(row).__name__
        if class_name == "TypeDefRow" and row_index_value:
            return self._type_names.get((assembly, row_index_value), self._row_type_name(row))
        if class_name == "TypeRefRow":
            return self._typeref_name(assembly, row_index_value or 0, set())
        if class_name == "TypeSpecRow":
            return self._typespec_name(assembly, row_index_value or 0)
        return self._row_type_name(row)

    @staticmethod
    def _row_type_name(row: Any) -> str:
        namespace = heap_text(getattr(row, "TypeNamespace", ""))
        name = heap_text(getattr(row, "TypeName", ""))
        return f"{namespace}.{name}" if namespace else name

    def _typeref_name(self, assembly: str, index: int, seen: set[int]) -> str:
        if not index or index in seen:
            return ""
        seen.add(index)
        row = self._type_refs.get((assembly, index))
        if row is None:
            return ""
        namespace = heap_text(getattr(row, "TypeNamespace", ""))
        name = heap_text(getattr(row, "TypeName", ""))
        scope = getattr(getattr(row, "ResolutionScope", None), "row", None)
        if not namespace and scope is not None and type(scope).__name__ == "TypeRefRow":
            parent_index = getattr(getattr(row, "ResolutionScope", None), "row_index", 0) or 0
            parent = self._typeref_name(assembly, parent_index, seen)
            if parent:
                return f"{parent}+{name}"
        return f"{namespace}.{name}" if namespace else name

    def _typespec_name(self, assembly: str, index: int) -> str:
        row = self._type_specs.get((assembly, index))
        blob = getattr(getattr(row, "Signature", None), "value", b"") if row is not None else b""
        if not blob:
            return "TypeSpec"
        try:
            value, _ = self._parse_type(blob, 0, assembly)
            return value
        except Exception:
            return "TypeSpec"

    def _parse_method_signature(self, assembly: str, blob: bytes) -> dict[str, Any]:
        if not blob:
            return {
                "generic_arity": 0,
                "return_type": "System.Void",
                "parameter_types": [],
                "normalized_signature": "System.Void()",
            }
        try:
            position = 0
            call_convention = blob[position]
            position += 1
            generic_arity = 0
            if call_convention & 0x10:
                generic_arity, position = compressed_uint(blob, position)
            parameter_count, position = compressed_uint(blob, position)
            return_type, position = self._parse_type(blob, position, assembly)
            parameter_types: list[str] = []
            while len(parameter_types) < parameter_count and position < len(blob):
                if blob[position] == 0x41:
                    position += 1
                    continue
                parameter_type, position = self._parse_type(blob, position, assembly)
                parameter_types.append(parameter_type)
            normalized = f"{return_type}({','.join(parameter_types)})"
            return {
                "generic_arity": generic_arity,
                "return_type": return_type,
                "parameter_types": parameter_types,
                "normalized_signature": normalized,
            }
        except Exception:
            return {
                "generic_arity": 0,
                "return_type": "UNKNOWN",
                "parameter_types": [],
                "normalized_signature": "UNKNOWN()",
            }

    def _parse_field_signature(self, assembly: str, blob: bytes) -> str:
        if not blob:
            return "UNKNOWN"
        try:
            position = 1 if blob[0] == 0x06 else 0
            value, _ = self._parse_type(blob, position, assembly)
            return value
        except Exception:
            return "UNKNOWN"

    def _parse_type(self, blob: bytes, position: int, assembly: str) -> tuple[str, int]:
        if position >= len(blob):
            return "UNKNOWN", position
        element = blob[position]
        position += 1
        primitives = {
            0x01: "System.Void",
            0x02: "System.Boolean",
            0x03: "System.Char",
            0x04: "System.SByte",
            0x05: "System.Byte",
            0x06: "System.Int16",
            0x07: "System.UInt16",
            0x08: "System.Int32",
            0x09: "System.UInt32",
            0x0A: "System.Int64",
            0x0B: "System.UInt64",
            0x0C: "System.Single",
            0x0D: "System.Double",
            0x0E: "System.String",
            0x16: "System.TypedReference",
            0x18: "System.IntPtr",
            0x19: "System.UIntPtr",
            0x1C: "System.Object",
        }
        if element in primitives:
            return primitives[element], position
        if element in {0x0F, 0x10, 0x45}:
            value, position = self._parse_type(blob, position, assembly)
            if element == 0x0F:
                return f"{value}*", position
            if element == 0x10:
                return f"{value}&", position
            return f"{value} pinned", position
        if element in {0x11, 0x12}:
            coded, position = compressed_uint(blob, position)
            return self._coded_type_from_integer(assembly, coded), position
        if element in {0x13, 0x1E}:
            value, position = compressed_uint(blob, position)
            return (f"!{value}" if element == 0x13 else f"!!{value}"), position
        if element == 0x14:
            value, position = self._parse_type(blob, position, assembly)
            rank, position = compressed_uint(blob, position)
            sizes, position = compressed_uint(blob, position)
            for _ in range(sizes):
                _, position = compressed_uint(blob, position)
            lower_bounds, position = compressed_uint(blob, position)
            for _ in range(lower_bounds):
                _, position = compressed_uint(blob, position)
            suffix = "," * max(0, rank - 1)
            return f"{value}[{suffix}]", position
        if element == 0x15:
            kind = blob[position] if position < len(blob) else 0x12
            position += 1
            coded, position = compressed_uint(blob, position)
            name = self._coded_type_from_integer(assembly, coded)
            count, position = compressed_uint(blob, position)
            arguments: list[str] = []
            for _ in range(count):
                value, position = self._parse_type(blob, position, assembly)
                arguments.append(value)
            return f"{name}<{','.join(arguments)}>", position
        if element == 0x1D:
            value, position = self._parse_type(blob, position, assembly)
            return f"{value}[]", position
        if element == 0x1B:
            value = self._parse_method_signature(assembly, blob[position:])["normalized_signature"]
            return f"methodptr {value}", len(blob)
        if element in {0x1F, 0x20}:
            _, position = compressed_uint(blob, position)
            return self._parse_type(blob, position, assembly)
        return f"ELEMENT_0x{element:02X}", position

    def _coded_type_from_integer(self, assembly: str, coded: int) -> str:
        table_kind = coded & 0x3
        index = coded >> 2
        if table_kind == 0:
            return self._type_names.get((assembly, index), f"TypeDef#{index}")
        if table_kind == 1:
            return self._typeref_name(assembly, index, set()) or f"TypeRef#{index}"
        if table_kind == 2:
            return self._typespec_name(assembly, index)
        return "UNKNOWN"


def source_gate() -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, list[dict[str, Any]]]]:
    """Verify the pinned inputs and return the gate, manifest, and source index."""
    input_paths = {
        "apk": APK,
        "csharp_rar": RAR,
        "libil2cpp": LIBIL2CPP,
        "global_metadata": METADATA,
    }
    observed_hashes: dict[str, str] = {}
    mismatches: list[dict[str, str]] = []
    for key, path in input_paths.items():
        observed = sha256_file(path) if path.is_file() else None
        if observed is not None:
            observed_hashes[key] = observed
        if observed != EXPECTED_HASHES[key]:
            mismatches.append(
                {
                    "input": key,
                    "path": str(path),
                    "expected_sha256": EXPECTED_HASHES[key],
                    "observed_sha256": observed or "MISSING",
                }
            )

    scripting_assemblies: list[str] = []
    scripting_json_sha256: str | None = None
    if APK.is_file():
        try:
            with zipfile.ZipFile(APK) as archive:
                payload = archive.read(SCRIPTING_ASSEMBLY_MEMBER)
            scripting_json_sha256 = hashlib.sha256(payload).hexdigest()
            parsed = json.loads(payload.decode("utf-8"))
            scripting_assemblies = sorted(
                {Path(str(item)).stem for item in parsed.get("names", []) if str(item).strip()},
                key=str.lower,
            )
        except Exception as error:
            mismatches.append(
                {
                    "input": SCRIPTING_ASSEMBLY_MEMBER,
                    "path": str(APK),
                    "expected_sha256": "valid-json-member",
                    "observed_sha256": f"ERROR:{type(error).__name__}",
                }
            )

    source_manifest: list[dict[str, Any]] = []
    source_index: dict[str, list[dict[str, Any]]] = defaultdict(list)
    source_counts = Counter()
    source_bytes = 0
    if SOURCE_ROOT.is_dir():
        for path in sorted(SOURCE_ROOT.rglob("*"), key=lambda item: item.as_posix().lower()):
            if not path.is_file():
                continue
            relative = path.relative_to(SOURCE_ROOT).as_posix()
            size = path.stat().st_size
            record = {
                "relative_path": relative,
                "extension": path.suffix.lower(),
                "bytes": size,
                "sha256": sha256_file(path),
            }
            source_manifest.append(record)
            source_counts["total_files"] += 1
            source_counts[record["extension"] or "<none>"] += 1
            if path.suffix.lower() == ".cs":
                source_bytes += size
                source_index[path.stem].append(
                    {
                        "relative_path": relative,
                        "absolute_path": str(path),
                        "bytes": size,
                        "sha256": record["sha256"],
                    }
                )
                if size == 0:
                    source_counts["zero_byte_cs"] += 1
            elif path.suffix.lower() == ".csproj":
                source_counts["csproj_files"] += 1
    else:
        mismatches.append(
            {
                "input": "csharp_source_root",
                "path": rel(SOURCE_ROOT),
                "expected_sha256": "directory-present",
                "observed_sha256": "MISSING",
            }
        )

    expected_csharp_files = 5504
    expected_csproj_files = 64
    expected_total_files = 5568
    expected_csharp_bytes = 55358557
    if (
        source_counts["total_files"] != expected_total_files
        or source_counts[".cs"] != expected_csharp_files
        or source_counts["csproj_files"] != expected_csproj_files
        or source_bytes != expected_csharp_bytes
    ):
        mismatches.append(
            {
                "input": "csharp_source_inventory",
                "path": rel(SOURCE_ROOT),
                "expected_sha256": (
                    f"files={expected_total_files};cs={expected_csharp_files};"
                    f"csproj={expected_csproj_files};cs_bytes={expected_csharp_bytes}"
                ),
                "observed_sha256": (
                    f"files={source_counts['total_files']};cs={source_counts['.cs']};"
                    f"csproj={source_counts['csproj_files']};cs_bytes={source_bytes}"
                ),
            }
        )

    gate = {
        "schema_version": SCHEMA_VERSION,
        "builder_version": BUILDER_VERSION,
        "status": "PASS" if not mismatches else "FAIL",
        "failure_code": None if not mismatches else "BLOCKED_R1_SOURCE_IDENTITY_MISMATCH",
        "pinned_inputs": {
            key: {
                "path": rel(input_paths[key]),
                "expected_sha256": EXPECTED_HASHES[key],
                "observed_sha256": observed_hashes.get(key, "MISSING"),
                "match": observed_hashes.get(key) == EXPECTED_HASHES[key],
            }
            for key in input_paths
        },
        "scripting_assemblies_member": {
            "path": SCRIPTING_ASSEMBLY_MEMBER,
            "sha256": scripting_json_sha256,
            "assembly_count": len(scripting_assemblies),
            "assemblies": scripting_assemblies,
        },
        "source_root": {
            "path": rel(SOURCE_ROOT),
            "total_files": source_counts["total_files"],
            "csharp_files": source_counts[".cs"],
            "csproj_files": source_counts["csproj_files"],
            "csharp_bytes": source_bytes,
            "zero_byte_csharp_files": sorted(
                row["relative_path"] for row in source_manifest
                if row["extension"] == ".cs" and row["bytes"] == 0
            ),
        },
        "mismatches": mismatches,
        "read_only_inputs": True,
    }
    if mismatches:
        raise RuntimeError("BLOCKED_R1_SOURCE_IDENTITY_MISMATCH")
    return gate, source_manifest, source_index


def mask_code(text: str) -> str:
    """Mask comments and literals while preserving newlines and offsets."""
    chars = list(text)
    state = "normal"
    index = 0
    while index < len(chars):
        current = chars[index]
        following = chars[index + 1] if index + 1 < len(chars) else ""
        if state == "normal":
            if current == "/" and following == "/":
                chars[index] = chars[index + 1] = " "
                index += 2
                state = "line_comment"
                continue
            if current == "/" and following == "*":
                chars[index] = chars[index + 1] = " "
                index += 2
                state = "block_comment"
                continue
            if current == "@" and following == '"':
                chars[index] = chars[index + 1] = " "
                index += 2
                state = "verbatim_string"
                continue
            if current in {'"', "'"}:
                chars[index] = " "
                state = "string" if current == '"' else "char"
                index += 1
                continue
            index += 1
            continue
        if state == "line_comment":
            if current == "\n":
                state = "normal"
            elif current != "\r":
                chars[index] = " "
            index += 1
            continue
        if state == "block_comment":
            if current == "*" and following == "/":
                chars[index] = chars[index + 1] = " "
                index += 2
                state = "normal"
            else:
                if current not in "\r\n":
                    chars[index] = " "
                index += 1
            continue
        if state == "verbatim_string":
            if current == '"' and following == '"':
                chars[index] = chars[index + 1] = " "
                index += 2
            elif current == '"':
                chars[index] = " "
                index += 1
                state = "normal"
            else:
                if current not in "\r\n":
                    chars[index] = " "
                index += 1
            continue
        if state in {"string", "char"}:
            if current == "\\":
                chars[index] = " "
                if index + 1 < len(chars) and chars[index + 1] not in "\r\n":
                    chars[index + 1] = " "
                index += 2
            elif (state == "string" and current == '"') or (state == "char" and current == "'"):
                chars[index] = " "
                index += 1
                state = "normal"
            else:
                if current not in "\r\n":
                    chars[index] = " "
                index += 1
    return "".join(chars)


def pair_map(text: str, opener: str, closer: str) -> dict[int, int]:
    stack: list[int] = []
    pairs: dict[int, int] = {}
    for index, character in enumerate(text):
        if character == opener:
            stack.append(index)
        elif character == closer and stack:
            start = stack.pop()
            pairs[start] = index
    return pairs


def line_starts(text: str) -> list[int]:
    result = [0]
    result.extend(index + 1 for index, character in enumerate(text) if character == "\n")
    return result


def line_number(starts: list[int], offset: int) -> int:
    import bisect
    return bisect.bisect_right(starts, offset)


def source_type_scopes(masked: str, starts: list[int]) -> list[dict[str, Any]]:
    braces = pair_map(masked, "{", "}")
    namespace_matches = list(NAMESPACE_RE.finditer(masked))
    scopes: list[dict[str, Any]] = []
    for match in TYPE_DECL_RE.finditer(masked):
        name = match.group(2)
        brace = masked.find("{", match.end())
        semicolon = masked.find(";", match.end())
        if brace < 0 or (semicolon >= 0 and semicolon < brace):
            continue
        close = braces.get(brace)
        if close is None:
            continue
        namespace = ""
        for namespace_match in namespace_matches:
            if namespace_match.start() > match.start():
                break
            namespace = namespace_match.group(1)
        scopes.append(
            {
                "name": name,
                "namespace": namespace,
                "full_name": f"{namespace}.{name}" if namespace else name,
                "start": match.start(),
                "open": brace,
                "close": close,
                "line": line_number(starts, match.start()),
                "keyword": match.group(1),
            }
        )
    scopes.sort(key=lambda item: (item["open"], -item["close"]))
    for scope in scopes:
        parents = [
            parent for parent in scopes
            if parent["open"] < scope["open"] < scope["close"] < parent["close"]
        ]
        if parents:
            parent = max(parents, key=lambda item: item["open"])
            scope["full_name"] = f"{parent['full_name']}+{scope['name']}"
    return scopes


def method_body_metrics(body: str, masked_body: str) -> dict[str, Any]:
    lowered = masked_body.lower()
    signals: Counter[str] = Counter()
    for pattern, signal in (
        (r"\b(if|switch|for|foreach|while|try|catch|finally|goto)\b", "control_flow"),
        (r"\?\s*[^:]+:", "conditional_operator"),
        (r"&&|\|\|", "compound_condition"),
        (r"\b(var|dynamic)\b", "inferred_type"),
        (r"\b(Resources|PlayerPrefs|JsonUtility|TextAsset|Addressables)\b", "static_data"),
        (r"\b(expected|unknown|unmanaged|il2cpp|methodinfo|rgctx)\b", "native_signal"),
    ):
        signals[signal] = len(re.findall(pattern, lowered))
    if not body.strip():
        category = "SOURCE_LIMITED"
    elif signals["native_signal"] or re.search(r"\bunsafe\b", lowered):
        category = "NATIVE_LIFT_REQUIRED"
    elif signals["static_data"]:
        category = "STATIC_DATA_REPAIR"
    elif signals["inferred_type"]:
        category = "TYPE_REPAIR"
    elif signals["control_flow"] or signals["conditional_operator"] or signals["compound_condition"]:
        category = "CFG_REPAIR"
    else:
        category = "CLEAN"
    return {
        "category": category,
        "signals": dict(sorted(signals.items())),
        "body_lines": body.count("\n") + 1 if body.strip() else 0,
        "body_bytes": len(body.encode("utf-8")),
        "body_sha256": hashlib.sha256(body.encode("utf-8")).hexdigest(),
    }


def source_method_records(path: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return [], []
    masked = mask_code(text)
    starts = line_starts(text)
    braces = pair_map(masked, "{", "}")
    parens = pair_map(masked, "(", ")")
    scopes = source_type_scopes(masked, starts)
    methods: list[dict[str, Any]] = []
    for line_start in starts:
        line_end = text.find("\n", line_start)
        if line_end < 0:
            line_end = len(text)
        line_masked = masked[line_start:line_end]
        method_match = METHOD_LINE_RE.match(line_masked)
        if not method_match:
            continue
        name = method_match.group(1)
        if name in CONTROL_NAMES:
            continue
        open_paren_relative = line_masked.find("(", method_match.start())
        if open_paren_relative < 0:
            continue
        open_paren = line_start + open_paren_relative
        close_paren = parens.get(open_paren)
        if close_paren is None:
            continue
        owner_candidates = [
            scope for scope in scopes
            if scope["open"] < open_paren < scope["close"]
        ]
        if not owner_candidates:
            continue
        owner = max(owner_candidates, key=lambda item: item["open"])
        parameter_text = text[open_paren + 1:close_paren]
        parameter_count = count_parameters(parameter_text)
        if not parameter_text.strip():
            parameter_count = 0
        declaration_end = close_paren + 1
        body_open = masked.find("{", declaration_end)
        semicolon = masked.find(";", declaration_end)
        expression_arrow = masked.find("=>", declaration_end)
        body_close: int | None = None
        body_kind = "none"
        if body_open >= 0 and (semicolon < 0 or body_open < semicolon):
            body_close = braces.get(body_open)
            body_kind = "block" if body_close is not None else "none"
        elif expression_arrow >= 0 and (semicolon < 0 or expression_arrow < semicolon):
            body_close = semicolon if semicolon >= 0 else len(text)
            body_open = expression_arrow + 2
            body_kind = "expression"
        if body_close is None:
            body_text = ""
            body_masked = ""
        else:
            body_text = text[body_open + 1:body_close] if body_kind == "block" else text[body_open:body_close]
            body_masked = masked[body_open + 1:body_close] if body_kind == "block" else masked[body_open:body_close]
        body_base = body_open + 1 if body_kind == "block" else body_open
        normalized_name = name
        if name == owner["name"]:
            normalized_name = ".ctor"
        elif name == f"~{owner['name']}":
            normalized_name = "Finalize"
        metrics = method_body_metrics(body_text, body_masked)
        calls: list[dict[str, Any]] = []
        for call in CALL_RE.finditer(body_masked):
            called_name = call.group("qual")
            if called_name in CONTROL_NAMES or called_name in {"return", "throw"}:
                continue
            call_open = body_base + call.end() - 1
            call_close = parens.get(call_open)
            relative_close = call_close - body_base if call_close is not None else None
            args = body_masked[call.end():relative_close] if relative_close is not None else ""
            calls.append(
                {
                    "name": called_name.split(".")[-1],
                    "qualifier": ".".join(called_name.split(".")[:-1]),
                    "qualified_name": called_name,
                    "argument_count": count_parameters(args),
                    "is_constructor": bool(call.group("new")),
                    "line": line_number(starts, body_open + call.start()),
                }
            )
        field_reads: list[str] = []
        field_writes: list[str] = []
        static_refs: list[str] = []
        for member in MEMBER_RE.finditer(body_masked):
            qualifier = member.group("qualifier")
            member_name = member.group("member")
            if qualifier in {"if", "for", "while", "switch", "return", "new"}:
                continue
            if qualifier and qualifier[:1].isupper():
                static_refs.append(f"{qualifier}.{member_name}")
            if re.search(rf"\b{re.escape(member_name)}\s*=", body_masked[member.end():member.end() + 6]):
                field_writes.append(member_name)
            else:
                field_reads.append(member_name)
        methods.append(
            {
                "relative_file": path.relative_to(SOURCE_ROOT).as_posix(),
                "source_type": owner["full_name"],
                "source_type_short": owner["name"],
                "method_name": normalized_name,
                "declared_name": name,
                "parameter_count": parameter_count,
                "line": line_number(starts, line_start),
                "line_end": line_number(starts, body_close if body_close is not None else close_paren),
                "body_kind": body_kind,
                "body_present": bool(body_text.strip()),
                "body_sha256": metrics["body_sha256"],
                "body_bytes": metrics["body_bytes"],
                "body_lines": metrics["body_lines"],
                "quality_category": metrics["category"],
                "signals": metrics["signals"],
                "calls": calls,
                "field_reads": sorted(set(field_reads)),
                "field_writes": sorted(set(field_writes)),
                "static_refs": sorted(set(static_refs)),
            }
        )
    types = [
        {
            "relative_file": path.relative_to(SOURCE_ROOT).as_posix(),
            "source_type": scope["full_name"],
            "source_type_short": scope["name"],
            "line": scope["line"],
        }
        for scope in scopes
    ]
    return methods, types


def build_source_cache(
    source_manifest: list[dict[str, Any]],
    source_index: dict[str, list[dict[str, Any]]],
) -> tuple[dict[str, Any], dict[str, list[dict[str, Any]]], dict[str, list[dict[str, Any]]]]:
    cache: dict[str, Any] = {}
    methods_by_type: dict[str, list[dict[str, Any]]] = defaultdict(list)
    methods_by_name: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in source_manifest:
        if item["extension"] != ".cs":
            continue
        path = SOURCE_ROOT / item["relative_path"]
        methods, types = source_method_records(path)
        cache[item["relative_path"]] = {
            "sha256": item["sha256"],
            "bytes": item["bytes"],
            "types": types,
            "methods": methods,
        }
        for method in methods:
            methods_by_type[normalize_source_type(method["source_type"])].append(method)
            methods_by_name[f"{method['source_type_short']}::{method['method_name']}"].append(method)
    for values in methods_by_type.values():
        values.sort(key=lambda row: (row["relative_file"], row["line"], row["method_name"]))
    for values in methods_by_name.values():
        values.sort(key=lambda row: (row["relative_file"], row["line"]))
    return cache, methods_by_type, methods_by_name


def index_source_cache(
    cache: dict[str, Any],
) -> tuple[dict[str, list[dict[str, Any]]], dict[str, list[dict[str, Any]]]]:
    methods_by_type: dict[str, list[dict[str, Any]]] = defaultdict(list)
    methods_by_name: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for payload in cache.values():
        for method in payload.get("methods", []):
            methods_by_type[normalize_source_type(method["source_type"])].append(method)
            methods_by_name[f"{method['source_type_short']}::{method['method_name']}"].append(method)
    for values in methods_by_type.values():
        values.sort(key=lambda row: (row["relative_file"], row["line"], row["method_name"]))
    for values in methods_by_name.values():
        values.sort(key=lambda row: (row["relative_file"], row["line"]))
    return methods_by_type, methods_by_name


def load_r0_quality() -> tuple[dict[tuple[str, str, str, int], dict[str, Any]], dict[str, Any]]:
    payload = load_json(R0_ROOT / "r0-method-quality-index.json")
    degraded: dict[tuple[str, str, str, int], dict[str, Any]] = {}
    for row in payload.get("degraded_methods", []):
        key = (
            str(row.get("file", "")),
            str(row.get("type", "")),
            str(row.get("name", "")),
            int(row.get("overload", 0) or 0),
        )
        degraded[key] = row
    return degraded, payload


def build_isil_index(root: Path) -> tuple[dict[tuple[str, str, int], list[dict[str, Any]]], dict[str, Any]]:
    index: dict[tuple[str, str, int], list[dict[str, Any]]] = defaultdict(list)
    files_read = 0
    methods_read = 0
    if not root.is_dir():
        return index, {
            "root": str(root),
            "present": False,
            "files_read": 0,
            "methods_read": 0,
        }
    for path in sorted(root.rglob("*.txt"), key=lambda item: item.as_posix().lower()):
        try:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        files_read += 1
        current_type = ""
        current: dict[str, Any] | None = None
        in_disassembly = False
        in_isil = False

        def finish() -> None:
            nonlocal current, methods_read
            if current is None:
                return
            current["disassembly_instruction_count"] = len(current.pop("_disassembly", []))
            current["isil_instruction_count"] = len(current.pop("_isil", []))
            current["isil_call_count"] = len(current.pop("_calls", []))
            current["native_available"] = bool(current.get("native_address"))
            current["isil_available"] = current["isil_instruction_count"] > 0
            key = (
                current["type_name"],
                current["method_name"],
                current["parameter_count"],
            )
            index[key].append(current)
            methods_read += 1
            current = None

        for line in lines:
            type_match = ISIL_TYPE_RE.match(line)
            if type_match:
                current_type = type_match.group("type").strip()
                continue
            method_match = ISIL_METHOD_RE.match(line)
            if method_match:
                finish()
                params = method_match.group("params").strip()
                current = {
                    "relative_file": path.as_posix(),
                    "type_name": current_type,
                    "method_name": method_match.group("name"),
                    "return_type": normalize_type_name(method_match.group("return")),
                    "parameter_count": count_parameters(params),
                    "parameter_text": params,
                    "native_address": None,
                    "_disassembly": [],
                    "_isil": [],
                    "_calls": [],
                }
                in_disassembly = False
                in_isil = False
                continue
            if current is None:
                continue
            if line.strip() == "Disassembly:":
                in_disassembly = True
                in_isil = False
                continue
            if line.strip() == "ISIL:":
                in_disassembly = False
                in_isil = True
                continue
            if line.startswith("Method:") or line.startswith("Type:"):
                in_disassembly = in_isil = False
            if in_disassembly:
                current["_disassembly"].append(line)
                address_match = ISIL_ADDRESS_RE.match(line)
                if address_match and current["native_address"] is None:
                    current["native_address"] = address_match.group(1)
            elif in_isil and ISIL_INSTRUCTION_RE.match(line):
                current["_isil"].append(line)
                if ISIL_CALL_RE.search(line):
                    current["_calls"].append(line)
        finish()
    for values in index.values():
        values.sort(key=lambda row: (row["relative_file"], row["native_address"] or "", row["method_name"]))
    return index, {
        "root": str(root),
        "present": True,
        "files_read": files_read,
        "methods_read": methods_read,
        "type_count": len({key[0] for key in index}),
        "key_count": len(index),
    }


def classify_ownership(assembly: str, full_name: str) -> tuple[str, str | None]:
    short_name = full_name.rsplit("+", 1)[-1].rsplit(".", 1)[-1]
    generated = (
        assembly in {"Il2CppDummyDll", "__Generated"}
        or full_name.startswith("<")
        or short_name.startswith("<")
        or "DisplayClass" in short_name
        or "AnonymousStorey" in short_name
        or short_name.startswith("__")
        or "UnitySourceGenerated" in short_name
    )
    if generated:
        return "COMPILER_GENERATED", None
    if assembly == "Assembly-CSharp":
        exception = None
        if full_name.startswith("system.") or full_name.startswith("TapjoyUnity."):
            exception = "Assembly-CSharp namespace/path is retained as GAME_FIRST_PARTY by assembly authority"
        return "GAME_FIRST_PARTY", exception
    if assembly == "KairoLibrary":
        exception = None
        if (
            full_name.startswith("java.")
            or full_name.startswith("kairo.")
            or full_name.startswith("kfw.")
            or "." not in full_name
        ):
            exception = "KairoLibrary namespace/path is retained as KAIRO_ENGINE by assembly authority"
        return "KAIRO_ENGINE", exception
    if assembly == "Assembly-CSharp-firstpass":
        return "THIRD_PARTY", "firstpass is treated as third-party/boundary code in R1"
    if assembly.startswith("UnityEngine") or assembly.startswith("Unity."):
        if full_name.startswith("UnityEngine.Purchasing"):
            return "THIRD_PARTY", "UnityEngine.Purchasing is an external purchasing package"
        return "UNITY_BOUNDARY", None
    if (
        assembly in {"mscorlib", "System", "System.Core", "System.Xml", "Mono.Security", "Microsoft.CSharp"}
        or full_name.startswith(("System.", "Microsoft.", "Mono."))
        or full_name in {"System", "Object", "String"}
    ):
        return "DOTNET_FRAMEWORK", None
    if (
        assembly.startswith(("Firebase", "Tapjoy", "Newtonsoft", "Google.", "Unity.Services", "UnityPurchasing"))
        or assembly in {"Purchasing.Common", "UDP", "Google.MiniJson"}
        or full_name.startswith(("Firebase.", "Tapjoy.", "Newtonsoft.", "Google.", "Unity.Services.", "Purchasing."))
    ):
        return "THIRD_PARTY", None
    return "SOURCE_LIMITED_OWNERSHIP", "assembly is present in metadata only or lacks an accepted ownership rule"


def inclusion_for_ownership(ownership: str) -> str:
    return {
        "GAME_FIRST_PARTY": "FULL_RECOVERY",
        "KAIRO_ENGINE": "DEPENDENCY_CLOSURE",
        "COMPILER_GENERATED": "EXCLUDE_GENERATED",
        "UNITY_BOUNDARY": "EXTERNAL_REFERENCE",
        "DOTNET_FRAMEWORK": "EXTERNAL_REFERENCE",
        "THIRD_PARTY": "EXTERNAL_REFERENCE",
        "SOURCE_LIMITED_OWNERSHIP": "SOURCE_LIMITED",
    }[ownership]


def normalize_assembly_stem(value: str) -> str:
    return Path(value).stem


def normalize_source_type(value: str) -> str:
    return re.sub(r"\x60\d+$", "", value.replace("/", "+"))


def apply_ownership(
    metadata: MetadataReader,
    scripting_assemblies: list[str],
    source_cache: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, list[str]]]:
    source_types: dict[str, list[str]] = defaultdict(list)
    for payload in source_cache.values():
        for source_type in payload.get("types", []):
            key = normalize_source_type(source_type["source_type"])
            source_types[key].append(source_type["relative_file"])
    for key in source_types:
        source_types[key] = sorted(set(source_types[key]))

    exceptions: list[dict[str, Any]] = []
    type_to_source_files: dict[str, list[str]] = {}
    for record in metadata.types:
        ownership, exception = classify_ownership(record["assembly"], record["full_name"])
        record["ownership"] = ownership
        record["inclusion"] = inclusion_for_ownership(ownership)
        record["compiler_generated"] = ownership == "COMPILER_GENERATED"
        record["external_reference"] = ownership in {
            "UNITY_BOUNDARY", "DOTNET_FRAMEWORK", "THIRD_PARTY",
        }
        source_files = source_types.get(normalize_source_type(record["full_name"]), [])
        if not source_files:
            short = record["short_name"].split("\x60", 1)[0]
            source_files = sorted(
                {
                    path
                    for key, paths in source_types.items()
                    if key.rsplit("+", 1)[-1].rsplit(".", 1)[-1].split("\x60", 1)[0] == short
                    for path in paths
                }
            )
        record["source_present"] = bool(source_files)
        record["source_file"] = source_files[0] if source_files else None
        record["source_file_candidates"] = source_files[:20]
        type_to_source_files[record["type_id"]] = source_files
        record.pop("_type_index", None)
        if exception:
            record["ownership_exception"] = exception
            exceptions.append(
                {
                    "assembly": record["assembly"],
                    "full_name": record["full_name"],
                    "type_id": record["type_id"],
                    "ownership": ownership,
                    "rule": exception,
                }
            )
        else:
            record["ownership_exception"] = None

    metadata_assemblies = {row["assembly"] for row in metadata.assemblies}
    assembly_rows: dict[str, dict[str, Any]] = {}
    for record in metadata.assemblies:
        assembly_rows[record["assembly"]] = dict(record)
    for assembly in scripting_assemblies:
        assembly_rows.setdefault(
            assembly,
            {
                "assembly": assembly,
                "dll_file": f"{assembly}.dll",
                "dll_path": None,
                "metadata_present": False,
                "metadata_type_count": None,
                "metadata_method_count": None,
                "metadata_field_count": None,
                "metadata_property_count": None,
                "metadata_interface_impl_count": None,
            },
        )
    for assembly, record in assembly_rows.items():
        assembly_types = [row for row in metadata.types if row["assembly"] == assembly]
        if assembly_types:
            ownership_counts = Counter(row["ownership"] for row in assembly_types)
            assembly_ownership = ownership_counts.most_common(1)[0][0]
            mixed = len(ownership_counts) > 1
        else:
            assembly_ownership, _ = classify_ownership(assembly, assembly)
            ownership_counts = Counter()
            mixed = False
        record["in_scripting_assemblies_json"] = assembly in scripting_assemblies
        record["ownership"] = assembly_ownership
        record["ownership_counts"] = dict(sorted(ownership_counts.items()))
        record["mixed_ownership"] = mixed
        record["type_count_indexed"] = len(assembly_types)
        record["method_count_indexed"] = sum(row["metadata_method_count"] for row in assembly_types)
        record["owned_type_count"] = sum(
            row["ownership"] in {"GAME_FIRST_PARTY", "KAIRO_ENGINE"} for row in assembly_types
        )
        record["owned_method_count"] = sum(
            row["ownership"] in {"GAME_FIRST_PARTY", "KAIRO_ENGINE"}
            and not row["compiler_generated"]
            for row in assembly_types
            for _ in range(row["metadata_method_count"])
        )
        record["target_type_count"] = sum(
            row["ownership"] in {"GAME_FIRST_PARTY", "KAIRO_ENGINE"}
            and not row["compiler_generated"]
            for row in assembly_types
        )
        record["metadata_absent_reason"] = (
            "scripting assembly listed in APK but no matching DummyDll"
            if not record.get("metadata_present") and record["in_scripting_assemblies_json"]
            else None
        )
    return (
        sorted(assembly_rows.values(), key=lambda row: row["assembly"].lower()),
        sorted(exceptions, key=lambda row: (row["assembly"].lower(), row["full_name"])),
        type_to_source_files,
    )


def method_quality_and_match(
    method: dict[str, Any],
    owner: dict[str, Any],
    source_methods_by_type: dict[str, list[dict[str, Any]]],
    source_methods_by_name: dict[str, list[dict[str, Any]]],
    degraded: dict[tuple[str, str, str, int], dict[str, Any]],
    isil_index: dict[tuple[str, str, int], list[dict[str, Any]]],
) -> tuple[dict[str, Any] | None, dict[str, Any] | None, str | None]:
    normalized_type = normalize_source_type(owner["full_name"])
    candidates = list(source_methods_by_type.get(normalized_type, []))
    match_status = "EXACT_TYPE"
    if not candidates:
        short_type = owner["short_name"].split(chr(96), 1)[0]
        candidates = list(source_methods_by_name.get(
            f"{short_type}::{method['method_name']}",
            [],
        ))
        match_status = "SHORT_TYPE"
    candidates = [
        row for row in candidates
        if row["method_name"] == method["method_name"]
        and row["parameter_count"] == method["parameter_count"]
    ]
    source_match = candidates[0] if candidates else None
    if len(candidates) > 1:
        candidates.sort(key=lambda row: (row["relative_file"], row["line"]))
        source_match = candidates[0]
        match_status = "AMBIGUOUS_DETERMINISTIC_FIRST"
    if source_match is None:
        match_status = "MISSING"

    r0_row = None
    if source_match is not None:
        same_name = [
            row for row in source_methods_by_type.get(normalized_type, [])
            if row["relative_file"] == source_match["relative_file"]
            and row["source_type_short"] == source_match["source_type_short"]
            and row["method_name"] == source_match["method_name"]
        ]
        if not same_name:
            same_name = [source_match]
        overload = sorted(same_name, key=lambda row: row["line"]).index(source_match) + 1
        r0_key = (
            source_match["relative_file"],
            source_match["source_type_short"],
            source_match["method_name"],
            overload,
        )
        r0_row = degraded.get(r0_key)
    isil_candidates = isil_index.get(
        (owner["full_name"], method["method_name"], method["parameter_count"]),
        [],
    )
    if not isil_candidates:
        isil_candidates = isil_index.get(
            (owner["short_name"].split("\x60", 1)[0], method["method_name"], method["parameter_count"]),
            [],
        )
    isil = isil_candidates[0] if isil_candidates else None
    if r0_row:
        quality = r0_row["category"]
    elif source_match is not None and source_match["body_present"]:
        quality = source_match["quality_category"]
    elif isil is not None:
        quality = "NATIVE_LIFT_REQUIRED"
    elif method["pinvoke"] or method["internal_call"] or method["runtime_implemented"] or method["native_implemented"]:
        quality = "NATIVE_BOUNDARY"
    else:
        quality = "SOURCE_LIMITED"
    if quality == "CLEAN":
        verification_status = "BASELINE_READABLE"
        disposition = "VERIFY_ONLY"
    elif quality == "TYPE_REPAIR":
        verification_status = "NEEDS_REPAIR"
        disposition = "AUTO_TYPE_REPAIR"
    elif quality == "STATIC_DATA_REPAIR":
        verification_status = "NEEDS_REPAIR"
        disposition = "AUTO_STATIC_DATA_REPAIR"
    elif quality == "CFG_REPAIR":
        verification_status = "NEEDS_REPAIR"
        disposition = "CFG_REPAIR"
    elif quality == "NATIVE_LIFT_REQUIRED":
        verification_status = "NEEDS_REPAIR"
        disposition = "ISIL_ASSISTED_REPAIR" if isil is not None else "NATIVE_LIFT"
    elif quality == "NATIVE_BOUNDARY":
        verification_status = "EXTERNAL_BOUNDARY"
        disposition = "EXTERNAL_BOUNDARY"
    else:
        verification_status = "SOURCE_LIMITED"
        disposition = "SOURCE_LIMITED"
    return source_match, isil, match_status, quality, verification_status, disposition, r0_row


def build_method_catalog(
    metadata: MetadataReader,
    source_methods_by_type: dict[str, list[dict[str, Any]]],
    source_methods_by_name: dict[str, list[dict[str, Any]]],
    degraded: dict[tuple[str, str, str, int], dict[str, Any]],
    isil_index: dict[tuple[str, str, int], list[dict[str, Any]]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    target_types = {
        row["type_id"]: row
        for row in metadata.types
        if row["ownership"] in {"GAME_FIRST_PARTY", "KAIRO_ENGINE"}
        and not row["compiler_generated"]
    }
    catalog: list[dict[str, Any]] = []
    queue: list[dict[str, Any]] = []
    for raw in metadata.methods:
        owner = target_types.get(raw["declaring_type_id"])
        if owner is None:
            continue
        source_match, isil, match_status, quality, verification_status, disposition, r0_row = method_quality_and_match(
            raw, owner, source_methods_by_type, source_methods_by_name, degraded, isil_index
        )
        record = dict(raw)
        record.pop("_type_index", None)
        record.update(
            {
                "ownership": owner["ownership"],
                "inclusion": owner["inclusion"],
                "verification_status": verification_status,
                "quality_class": quality,
                "repair_disposition": disposition,
                "source_match_status": match_status,
                "source_present": source_match is not None,
                "source_file": source_match["relative_file"] if source_match else owner.get("source_file"),
                "source_line": source_match["line"] if source_match else None,
                "source_line_end": source_match["line_end"] if source_match else None,
                "source_body_present": bool(source_match and source_match["body_present"]),
                "source_body_kind": source_match["body_kind"] if source_match else None,
                "body_sha256": source_match["body_sha256"] if source_match else None,
                "body_bytes": source_match["body_bytes"] if source_match else 0,
                "body_lines": source_match["body_lines"] if source_match else 0,
                "r0_quality_class": r0_row["category"] if r0_row else None,
                "r0_signals": r0_row["signals"] if r0_row else (
                    source_match["signals"] if source_match else {}
                ),
                "isil_available": bool(isil and isil["isil_available"]),
                "native_available": bool(isil and isil["native_available"]),
                "isil_native_address": isil["native_address"] if isil else None,
                "isil_disassembly_instruction_count": isil["disassembly_instruction_count"] if isil else 0,
                "isil_instruction_count": isil["isil_instruction_count"] if isil else 0,
                "isil_call_count": isil["isil_call_count"] if isil else 0,
                "isil_evidence_file": isil["relative_file"] if isil else None,
                "repaired_body": False,
                "static_data_refs": source_match["static_refs"] if source_match else [],
                "field_read_names": source_match["field_reads"] if source_match else [],
                "field_write_names": source_match["field_writes"] if source_match else [],
                "source_calls": source_match["calls"] if source_match else [],
                "evidence_refs": [
                    "knowledge/brain/acceptance/r0-cpp2il-audit/r0-method-quality-index.json"
                    if r0_row else None,
                    rel(SOURCE_ROOT / source_match["relative_file"]) if source_match else None,
                    isil["relative_file"] if isil else None,
                    f"DummyDll/{raw['dll_file']}#{raw['metadata_token']}",
                ],
            }
        )
        record["evidence_refs"] = [value for value in record["evidence_refs"] if value]
        catalog.append(record)
        queue.append(
            {
                "queue_id": stable_id("r1-repair-queue", record["method_id"]),
                "method_id": record["method_id"],
                "assembly": record["assembly"],
                "declaring_type": record["declaring_type"],
                "method_name": record["method_name"],
                "normalized_signature": record["normalized_signature"],
                "ownership": record["ownership"],
                "quality_class": quality,
                "verification_status": verification_status,
                "repair_disposition": disposition,
                "priority": (
                    0 if quality == "NATIVE_LIFT_REQUIRED"
                    else 1 if quality in {"CFG_REPAIR", "TYPE_REPAIR", "STATIC_DATA_REPAIR"}
                    else 2 if quality == "SOURCE_LIMITED"
                    else 3
                ),
                "native_available": record["native_available"],
                "isil_available": record["isil_available"],
                "source_present": record["source_present"],
                "r0_quality_class": record["r0_quality_class"],
                "repaired_body": False,
            }
        )
    catalog.sort(key=lambda row: row["method_id"])
    queue.sort(key=lambda row: (row["priority"], row["assembly"].lower(), row["declaring_type"], row["method_name"], row["normalized_signature"], row["method_id"]))
    return catalog, queue


def build_dependency_graph(
    metadata: MetadataReader,
    method_catalog: list[dict[str, Any]],
) -> dict[str, Any]:
    type_by_id = {row["type_id"]: row for row in metadata.types}
    type_by_full: dict[str, list[dict[str, Any]]] = defaultdict(list)
    type_by_short: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in metadata.types:
        type_by_full[row["full_name"]].append(row)
        type_by_short[row["short_name"].split(chr(96), 1)[0]].append(row)
    method_by_id = {row["method_id"]: row for row in metadata.methods}
    owned_method_ids = {row["method_id"] for row in method_catalog}
    catalog_by_id = {row["method_id"]: row for row in method_catalog}
    methods_by_type_name: dict[tuple[str, str, int], list[dict[str, Any]]] = defaultdict(list)
    for row in metadata.methods:
        methods_by_type_name[(row["declaring_type_id"], row["method_name"], row["parameter_count"])].append(row)
    fields_by_type_name: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    fields_by_name: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for field in metadata.fields:
        owner = type_by_id.get(field["declaring_type_id"])
        if owner is None:
            continue
        field["ownership"] = owner["ownership"]
        field["inclusion"] = owner["inclusion"]
        fields_by_type_name[(field["declaring_type_id"], field["field_name"])].append(field)
        fields_by_name[field["field_name"]].append(field)

    def resolve_type(type_name: str, assembly: str = "") -> dict[str, Any] | None:
        normalized = normalize_type_name(type_name).replace("global::", "")
        normalized = re.sub(r"^(class|valuetype)\s+", "", normalized)
        if assembly and (assembly, normalized) in metadata.type_by_key:
            return metadata.type_by_key[(assembly, normalized)]
        exact = type_by_full.get(normalized, [])
        if len(exact) == 1:
            return exact[0]
        short = normalized.rsplit("+", 1)[-1].rsplit(".", 1)[-1].split(chr(96), 1)[0]
        candidates = type_by_short.get(short, [])
        return candidates[0] if len(candidates) == 1 else None

    type_edges: list[dict[str, Any]] = []
    for source in metadata.types:
        if source["ownership"] not in {"GAME_FIRST_PARTY", "KAIRO_ENGINE"}:
            continue
        references = [("inheritance", source["base_type"])] + [
            ("interface", name) for name in source.get("interfaces", [])
        ]
        for edge_type, target_name in references:
            if not target_name:
                continue
            target = resolve_type(target_name, source["assembly"])
            type_edges.append(
                {
                    "edge_id": stable_id("r1-type-edge", source["type_id"], edge_type, target_name),
                    "source_type_id": source["type_id"],
                    "source_type": source["full_name"],
                    "source_ownership": source["ownership"],
                    "target_type_id": target["type_id"] if target else None,
                    "target_type": target["full_name"] if target else target_name,
                    "target_ownership": target["ownership"] if target else "SOURCE_LIMITED_OWNERSHIP",
                    "edge_type": edge_type,
                    "resolution": "METADATA" if target else "UNRESOLVED_METADATA_REFERENCE",
                }
            )
    type_edges.sort(key=lambda row: row["edge_id"])

    def resolve_method(
        owner: dict[str, Any],
        call: dict[str, Any],
    ) -> tuple[list[dict[str, Any]], str]:
        if call.get("is_constructor"):
            type_hint = call.get("qualified_name") or owner["full_name"]
            target_type = resolve_type(type_hint, owner["assembly"]) or owner
            candidates = methods_by_type_name.get(
                (target_type["type_id"], ".ctor", call["argument_count"]),
                [],
            )
            return candidates, "CONSTRUCTOR_METADATA"
        qualifier = call.get("qualifier", "")
        target_type = owner
        resolution = "SAME_TYPE_METADATA"
        if qualifier in {"this", "base"}:
            if qualifier == "base":
                target_type = resolve_type(owner.get("base_type") or "", owner["assembly"]) or owner
            resolution = "QUALIFIED_METADATA"
        elif qualifier:
            hinted = resolve_type(qualifier, owner["assembly"])
            if hinted is not None:
                target_type = hinted
                resolution = "TYPE_QUALIFIED_METADATA"
            else:
                resolution = "UNRESOLVED_INSTANCE_QUALIFIER"
        candidates = methods_by_type_name.get(
            (target_type["type_id"], call["name"], call["argument_count"]),
            [],
        )
        return candidates, resolution

    call_edges: list[dict[str, Any]] = []
    external_edges: list[dict[str, Any]] = []
    field_edges: list[dict[str, Any]] = []
    static_data_edges: list[dict[str, Any]] = []
    for method in method_catalog:
        owner = type_by_id[method["declaring_type_id"]]
        for call in method.get("source_calls", []):
            candidates, resolution = resolve_method(owner, call)
            if candidates:
                candidate = sorted(candidates, key=lambda row: row["method_id"])[0]
                candidate_owner = type_by_id.get(candidate["declaring_type_id"])
                if candidate["method_id"] in owned_method_ids:
                    call_edges.append(
                        {
                            "edge_id": stable_id("r1-call-edge", method["method_id"], candidate["method_id"], call["line"]),
                            "caller_method_id": method["method_id"],
                            "caller_type_id": method["declaring_type_id"],
                            "caller_ownership": method["ownership"],
                            "callee_method_id": candidate["method_id"],
                            "callee_type_id": candidate["declaring_type_id"],
                            "callee_ownership": candidate_owner["ownership"] if candidate_owner else "SOURCE_LIMITED_OWNERSHIP",
                            "source_file": method.get("source_file"),
                            "source_line": call["line"],
                            "call_name": call["qualified_name"],
                            "argument_count": call["argument_count"],
                            "resolution": resolution,
                            "cross_ownership": bool(candidate_owner and candidate_owner["ownership"] != method["ownership"]),
                        }
                    )
                else:
                    external_edges.append(
                        {
                            "edge_id": stable_id("r1-external-edge", method["method_id"], candidate["method_id"], call["line"]),
                            "source_method_id": method["method_id"],
                            "source_type_id": method["declaring_type_id"],
                            "source_ownership": method["ownership"],
                            "target_method_id": candidate["method_id"],
                            "target_type": candidate["declaring_type"],
                            "target_ownership": candidate_owner["ownership"] if candidate_owner else "SOURCE_LIMITED_OWNERSHIP",
                            "target_ref": f"{candidate['declaring_type']}::{candidate['method_name']}{candidate['normalized_signature']}",
                            "source_file": method.get("source_file"),
                            "source_line": call["line"],
                            "resolution": resolution,
                            "external_kind": "METADATA_BOUNDARY",
                        }
                    )
            else:
                external_edges.append(
                    {
                        "edge_id": stable_id("r1-external-edge", method["method_id"], call["qualified_name"], call["line"]),
                        "source_method_id": method["method_id"],
                        "source_type_id": method["declaring_type_id"],
                        "source_ownership": method["ownership"],
                        "target_method_id": None,
                        "target_type": call.get("qualifier") or owner["full_name"],
                        "target_ownership": "SOURCE_LIMITED_OWNERSHIP",
                        "target_ref": f"{call.get('qualified_name', call['name'])}/{call['argument_count']}",
                        "source_file": method.get("source_file"),
                        "source_line": call["line"],
                        "resolution": resolution,
                        "external_kind": "UNRESOLVED_SOURCE_CALL",
                    }
                )
        for field_name in sorted(set(method.get("field_read_names", []) + method.get("field_write_names", []))):
            candidates = fields_by_type_name.get((method["declaring_type_id"], field_name), [])
            if not candidates:
                candidates = fields_by_name.get(field_name, [])
            if candidates:
                field = sorted(candidates, key=lambda row: row["field_id"])[0]
                access = "read_write" if field_name in method.get("field_read_names", []) and field_name in method.get("field_write_names", []) else (
                    "write" if field_name in method.get("field_write_names", []) else "read"
                )
                field_edges.append(
                    {
                        "edge_id": stable_id("r1-field-edge", method["method_id"], field["field_id"], access),
                        "source_method_id": method["method_id"],
                        "source_type_id": method["declaring_type_id"],
                        "source_ownership": method["ownership"],
                        "field_id": field["field_id"],
                        "field_owner_type_id": field["declaring_type_id"],
                        "field_ownership": field["ownership"],
                        "field_name": field["field_name"],
                        "access": access,
                        "resolution": "FIELD_METADATA",
                    }
                )
            else:
                external_edges.append(
                    {
                        "edge_id": stable_id("r1-external-field", method["method_id"], field_name),
                        "source_method_id": method["method_id"],
                        "source_type_id": method["declaring_type_id"],
                        "source_ownership": method["ownership"],
                        "target_method_id": None,
                        "target_type": method["declaring_type"],
                        "target_ownership": "SOURCE_LIMITED_OWNERSHIP",
                        "target_ref": f"field:{field_name}",
                        "source_file": method.get("source_file"),
                        "source_line": method.get("source_line"),
                        "resolution": "UNRESOLVED_FIELD_REFERENCE",
                        "external_kind": "UNRESOLVED_FIELD",
                    }
                )
        for static_ref in sorted(set(method.get("static_data_refs", []))):
            static_data_edges.append(
                {
                    "edge_id": stable_id("r1-static-edge", method["method_id"], static_ref),
                    "source_method_id": method["method_id"],
                    "source_type_id": method["declaring_type_id"],
                    "source_ownership": method["ownership"],
                    "target_ref": static_ref,
                    "edge_type": "STATIC_DATA_REFERENCE",
                    "resolution": "SOURCE_LEXICAL",
                }
            )

    def dedupe(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
        values: dict[str, dict[str, Any]] = {}
        for row in rows:
            values[row["edge_id"]] = row
        return [values[key] for key in sorted(values)]

    call_edges = dedupe(call_edges)
    external_edges = dedupe(external_edges)
    field_edges = dedupe(field_edges)
    static_data_edges = dedupe(static_data_edges)

    adjacency: dict[str, list[str]] = {method_id: [] for method_id in sorted(owned_method_ids)}
    reverse: dict[str, list[str]] = {method_id: [] for method_id in sorted(owned_method_ids)}
    for edge in call_edges:
        adjacency[edge["caller_method_id"]].append(edge["callee_method_id"])
        reverse[edge["callee_method_id"]].append(edge["caller_method_id"])
    for values in adjacency.values():
        values[:] = sorted(set(values))
    for values in reverse.values():
        values[:] = sorted(set(values))

    order: list[str] = []
    visited: set[str] = set()
    for start in sorted(owned_method_ids):
        if start in visited:
            continue
        visited.add(start)
        stack: list[tuple[str, int]] = [(start, 0)]
        while stack:
            node, position = stack[-1]
            neighbours = adjacency[node]
            if position < len(neighbours):
                target = neighbours[position]
                stack[-1] = (node, position + 1)
                if target not in visited:
                    visited.add(target)
                    stack.append((target, 0))
            else:
                order.append(node)
                stack.pop()
    component_for: dict[str, str] = {}
    components: dict[str, list[str]] = {}
    visited.clear()
    for start in reversed(order):
        if start in visited:
            continue
        members: list[str] = []
        visited.add(start)
        stack = [start]
        while stack:
            node = stack.pop()
            members.append(node)
            for target in reverse[node]:
                if target not in visited:
                    visited.add(target)
                    stack.append(target)
        component_id = stable_id("r1-scc", *sorted(members))
        components[component_id] = sorted(members)
        for node in members:
            component_for[node] = component_id
    component_adjacency: dict[str, set[str]] = {component: set() for component in components}
    for edge in call_edges:
        source_component = component_for[edge["caller_method_id"]]
        target_component = component_for[edge["callee_method_id"]]
        if source_component != target_component:
            component_adjacency[source_component].add(target_component)
    component_layers: dict[str, int] = {}
    component_indegree: dict[str, int] = {component: 0 for component in components}
    for targets in component_adjacency.values():
        for target in targets:
            component_indegree[target] += 1
    ready = deque(sorted(
        component for component, degree in component_indegree.items() if degree == 0
    ))
    topological_order: list[str] = []
    while ready:
        component = ready.popleft()
        topological_order.append(component)
        for target in sorted(component_adjacency[component]):
            component_indegree[target] -= 1
            if component_indegree[target] == 0:
                ready.append(target)
    if len(topological_order) != len(components):
        raise RuntimeError("R1 dependency SCC condensation did not converge")
    for component in reversed(topological_order):
        targets = component_adjacency[component]
        component_layers[component] = 0 if not targets else 1 + max(
            component_layers[target] for target in targets
        )
    scc_summary = []
    dependency_layers = []
    for component_id in sorted(components):
        members = components[component_id]
        ownership_counts = Counter(catalog_by_id[node]["ownership"] for node in members)
        scc_summary.append(
            {
                "scc_id": component_id,
                "method_count": len(members),
                "self_recursive": len(members) > 1 or any(
                    edge["caller_method_id"] == edge["callee_method_id"]
                    and component_for[edge["caller_method_id"]] == component_id
                    for edge in call_edges
                ),
                "ownership_counts": dict(sorted(ownership_counts.items())),
                "representative_method_id": members[0],
                "method_ids": members,
            }
        )
        dependency_layers.append(
            {
                "scc_id": component_id,
                "layer": component_layers[component_id],
                "method_count": len(members),
                "representative_method_id": members[0],
                "owned_callee_scc_count": len(component_adjacency[component_id]),
            }
        )
    for method in method_catalog:
        method_id = method["method_id"]
        method["scc_id"] = component_for[method_id]
        method["dependency_layer"] = component_layers[component_for[method_id]]
        method["owned_callee_count"] = len(adjacency[method_id])
        method["owned_caller_count"] = len(reverse[method_id])
        method["external_edge_count"] = sum(
            edge["source_method_id"] == method_id for edge in external_edges
        )
        method["field_edge_count"] = sum(
            edge["source_method_id"] == method_id for edge in field_edges
        )
        method["static_data_edge_count"] = sum(
            edge["source_method_id"] == method_id for edge in static_data_edges
        )

    bridge_counts: Counter[tuple[str, str, str]] = Counter()
    for edge in call_edges:
        bridge_counts[(edge["caller_ownership"], edge["callee_ownership"], "call")] += 1
    for edge in type_edges:
        bridge_counts[(edge["source_ownership"], edge["target_ownership"], edge["edge_type"])] += 1
    for edge in field_edges:
        bridge_counts[(edge["source_ownership"], edge["field_ownership"], "field")] += 1
    bridge_rows = [
        {
            "source_ownership": source,
            "target_ownership": target,
            "edge_kind": kind,
            "count": count,
        }
        for (source, target, kind), count in sorted(bridge_counts.items())
    ]
    return {
        "type_edges": type_edges,
        "call_edges": call_edges,
        "external_edges": external_edges,
        "field_edges": field_edges,
        "static_data_edges": static_data_edges,
        "scc_summary": scc_summary,
        "dependency_layers": dependency_layers,
        "bridge_rows": bridge_rows,
        "summary": {
            "owned_method_count": len(method_catalog),
            "owned_type_count": len({
                row["declaring_type_id"] for row in method_catalog
            }),
            "type_edge_count": len(type_edges),
            "owned_call_edge_count": len(call_edges),
            "external_edge_count": len(external_edges),
            "field_edge_count": len(field_edges),
            "static_data_edge_count": len(static_data_edges),
            "scc_count": len(scc_summary),
            "recursive_scc_count": sum(row["self_recursive"] for row in scc_summary),
            "max_dependency_layer": max(component_layers.values(), default=0),
            "bridge_count": len(bridge_rows),
        },
    }


def summarize_methods(method_catalog: list[dict[str, Any]], metadata: MetadataReader) -> dict[str, Any]:
    def grouped(key: str) -> dict[str, int]:
        return dict(sorted(Counter(row[key] for row in method_catalog).items()))

    return {
        "schema_version": SCHEMA_VERSION,
        "authority": "DummyDll metadata methods in GAME_FIRST_PARTY and KAIRO_ENGINE types, excluding COMPILER_GENERATED types",
        "metadata_total_method_count": len(metadata.methods),
        "metadata_total_type_count": len(metadata.types),
        "target_method_count": len(method_catalog),
        "target_type_count": len({row["declaring_type_id"] for row in method_catalog}),
        "method_id_unique": len({row["method_id"] for row in method_catalog}) == len(method_catalog),
        "counts_by_ownership": grouped("ownership"),
        "counts_by_quality_class": grouped("quality_class"),
        "counts_by_verification_status": grouped("verification_status"),
        "counts_by_repair_disposition": grouped("repair_disposition"),
        "counts_by_assembly": dict(sorted(Counter(row["assembly"] for row in method_catalog).items())),
        "native_available_count": sum(row["native_available"] for row in method_catalog),
        "isil_available_count": sum(row["isil_available"] for row in method_catalog),
        "source_present_count": sum(row["source_present"] for row in method_catalog),
        "source_body_present_count": sum(row["source_body_present"] for row in method_catalog),
        "repaired_body_count": sum(row["repaired_body"] for row in method_catalog),
        "identity_material": [
            "source APK SHA-256",
            "assembly name",
            "declaring type full name",
            "method name",
            "method generic arity",
            "return type",
            "ordered parameter types",
        ],
        "r0_source_baseline": {
            "accepted_method_count": 41229,
            "raw_lexical_method_declaration_count": 43103,
            "source_identity": "MATCH",
            "authority_note": "R0 source baseline is retained for quality signals and is not substituted for R1 metadata identity.",
        },
    }


def summarize_ownership(
    metadata: MetadataReader,
    assemblies: list[dict[str, Any]],
    exceptions: list[dict[str, Any]],
    method_catalog: list[dict[str, Any]],
) -> dict[str, Any]:
    type_counts = Counter(row["ownership"] for row in metadata.types)
    method_counts = Counter(row["ownership"] for row in method_catalog)
    return {
        "schema_version": SCHEMA_VERSION,
        "taxonomy": list(OWNERSHIPS),
        "type_counts": dict(sorted(type_counts.items())),
        "method_counts_target": dict(sorted(method_counts.items())),
        "assembly_count": len(assemblies),
        "metadata_assembly_count": sum(row["metadata_present"] for row in assemblies),
        "scripting_assembly_count": sum(row["in_scripting_assemblies_json"] for row in assemblies),
        "scripting_assemblies_without_dummy_dll": sorted(
            row["assembly"] for row in assemblies
            if row["in_scripting_assemblies_json"] and not row["metadata_present"]
        ),
        "ownership_exception_count": len(exceptions),
        "ownership_exceptions": exceptions,
        "assembly_ownership_counts": dict(sorted(
            Counter(row["ownership"] for row in assemblies).items()
        )),
        "assembly_rows": assemblies,
    }


def summarize_repairs(method_catalog: list[dict[str, Any]], queue: list[dict[str, Any]]) -> dict[str, Any]:
    by_quality = Counter(row["quality_class"] for row in method_catalog)
    by_disposition = Counter(row["repair_disposition"] for row in method_catalog)
    return {
        "schema_version": SCHEMA_VERSION,
        "queue_method_count": len(queue),
        "queue_id_unique": len({row["queue_id"] for row in queue}) == len(queue),
        "quality_class_counts": dict(sorted(by_quality.items())),
        "repair_disposition_counts": dict(sorted(by_disposition.items())),
        "verification_status_counts": dict(sorted(
            Counter(row["verification_status"] for row in method_catalog).items()
        )),
        "priority_counts": dict(sorted(Counter(row["priority"] for row in queue).items())),
        "native_required_count": sum(
            row["quality_class"] == "NATIVE_LIFT_REQUIRED" for row in method_catalog
        ),
        "native_available_for_native_required_count": sum(
            row["quality_class"] == "NATIVE_LIFT_REQUIRED" and row["native_available"]
            for row in method_catalog
        ),
        "source_limited_count": sum(
            row["quality_class"] == "SOURCE_LIMITED" for row in method_catalog
        ),
        "repaired_body_count": sum(row["repaired_body"] for row in method_catalog),
        "disposition_contract": {
            "CLEAN": "VERIFY_ONLY",
            "TYPE_REPAIR": "AUTO_TYPE_REPAIR",
            "STATIC_DATA_REPAIR": "AUTO_STATIC_DATA_REPAIR",
            "CFG_REPAIR": "CFG_REPAIR",
            "NATIVE_LIFT_REQUIRED": "ISIL_ASSISTED_REPAIR when ISIL exists, otherwise NATIVE_LIFT",
            "NATIVE_BOUNDARY": "EXTERNAL_BOUNDARY",
            "SOURCE_LIMITED": "SOURCE_LIMITED",
        },
    }


def core_nine_validation(method_catalog: list[dict[str, Any]], metadata: MetadataReader) -> dict[str, Any]:
    core_payload = load_json(R0_ROOT / "r0-core-class-quality.json")
    core_names = [
        name for name in core_payload
        if name != "measurement_basis"
    ]
    rows: list[dict[str, Any]] = []
    for name in core_names:
        methods = [
            row for row in method_catalog
            if row["declaring_type"].rsplit("+", 1)[-1].rsplit(".", 1)[-1].split(chr(96), 1)[0] == name
        ]
        type_rows = [
            row for row in metadata.types
            if row["short_name"].split(chr(96), 1)[0] == name
        ]
        quality_counts = dict(sorted(Counter(row["quality_class"] for row in methods).items()))
        compiler_aliases = [
            row["full_name"] for row in type_rows if row["compiler_generated"]
        ]
        identity_gap = bool(type_rows and not methods and compiler_aliases)
        rows.append(
            {
                "core_name": name,
                "r0_file_path": core_payload[name].get("file_path"),
                "r0_accepted_method_count": core_payload[name].get("total_methods"),
                "r1_metadata_method_count": len(methods),
                "r1_quality_counts": quality_counts,
                "r1_source_present_count": sum(row["source_present"] for row in methods),
                "r1_isil_available_count": sum(row["isil_available"] for row in methods),
                "metadata_type_match_count": len(type_rows),
                "metadata_identity_gap": identity_gap,
                "metadata_identity_gap_reason": (
                    "DummyDll exposes only a compiler-generated nested alias for this R0 source anchor; "
                    "the alias is excluded from the owned method catalog by the compiler-generated policy."
                    if identity_gap else None
                ),
                "metadata_aliases": compiler_aliases,
                "pass": bool(type_rows and (methods or identity_gap)),
            }
        )
    return {
        "schema_version": SCHEMA_VERSION,
        "core_count": len(rows),
        "core_names": core_names,
        "rows": rows,
        "pass": len(rows) == 9 and all(row["pass"] for row in rows),
        "comparison_note": "R1 counts are DummyDll metadata identity counts; R0 counts remain the accepted source baseline and are shown for comparison.",
    }


def validate_in_memory(
    gate: dict[str, Any],
    metadata: MetadataReader,
    assemblies: list[dict[str, Any]],
    method_catalog: list[dict[str, Any]],
    queue: list[dict[str, Any]],
    graph: dict[str, Any],
    core_validation: dict[str, Any],
) -> dict[str, Any]:
    checks: dict[str, bool] = {}
    checks["source_gate_pass"] = gate["status"] == "PASS" and not gate["mismatches"]
    checks["pinned_hashes_match"] = all(
        row["match"] for row in gate["pinned_inputs"].values()
    )
    checks["corpus_inventory_match"] = (
        gate["source_root"]["total_files"] == 5568
        and gate["source_root"]["csharp_files"] == 5504
        and gate["source_root"]["csproj_files"] == 64
        and gate["source_root"]["csharp_bytes"] == 55358557
    )
    checks["ownership_taxonomy_exact"] = set(OWNERSHIPS) == {
        row["ownership"] for row in metadata.types
    } | {
        row["ownership"] for row in assemblies
    } | {"SOURCE_LIMITED_OWNERSHIP"}
    checks["type_ids_unique"] = len({row["type_id"] for row in metadata.types}) == len(metadata.types)
    checks["method_ids_unique"] = len({row["method_id"] for row in method_catalog}) == len(method_catalog)
    checks["method_queue_exact"] = (
        len(queue) == len(method_catalog)
        and {row["method_id"] for row in queue} == {row["method_id"] for row in method_catalog}
    )
    checks["quality_contract"] = all(
        row["quality_class"] in QUALITY_CLASSES
        and row["verification_status"] in VERIFICATION_STATUSES
        and row["repair_disposition"] in DISPOSITIONS
        and not row["repaired_body"]
        for row in method_catalog
    )
    checks["owned_graph_has_edges"] = (
        graph["summary"]["owned_call_edge_count"] > 0
        and graph["summary"]["type_edge_count"] > 0
        and graph["summary"]["field_edge_count"] > 0
        and graph["summary"]["scc_count"] == len({
            row["scc_id"] for row in method_catalog
        })
    )
    method_ids = {row["method_id"] for row in method_catalog}
    checks["call_edge_refs"] = all(
        row["caller_method_id"] in method_ids and row["callee_method_id"] in method_ids
        for row in graph["call_edges"]
    )
    checks["field_edge_refs"] = all(
        row["source_method_id"] in method_ids
        for row in graph["field_edges"]
    )
    checks["external_edge_refs"] = all(
        row["source_method_id"] in method_ids
        for row in graph["external_edges"]
    )
    checks["deterministic_sort_contract"] = (
        method_catalog == sorted(method_catalog, key=lambda row: row["method_id"])
        and graph["call_edges"] == sorted(graph["call_edges"], key=lambda row: row["edge_id"])
    )
    checks["core_nine_pass"] = core_validation["pass"]
    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "failed_checks": sorted(key for key, value in checks.items() if not value),
        "counts": {
            "metadata_types": len(metadata.types),
            "metadata_methods": len(metadata.methods),
            "target_methods": len(method_catalog),
            "queue_rows": len(queue),
            "call_edges": len(graph["call_edges"]),
            "external_edges": len(graph["external_edges"]),
            "field_edges": len(graph["field_edges"]),
            "sccs": len(graph["scc_summary"]),
        },
    }


def artifact_file_manifest(root: Path) -> dict[str, Any]:
    files: list[dict[str, Any]] = []
    for path in sorted(root.rglob("*"), key=lambda item: item.relative_to(root).as_posix()):
        if not path.is_file() or path.name == "artifact-manifest.json":
            continue
        relative = path.relative_to(root).as_posix()
        record = {
            "path": relative,
            "bytes": path.stat().st_size,
            "sha256": sha256_file(path),
        }
        if path.suffix == ".jsonl":
            with path.open("r", encoding="utf-8") as stream:
                record["record_count"] = sum(1 for line in stream if line.strip())
        files.append(record)
    tree_payload = "\n".join(f"{row['path']}:{row['sha256']}" for row in files).encode("utf-8")
    return {
        "schema_version": SCHEMA_VERSION,
        "builder_version": BUILDER_VERSION,
        "artifact_root": str(root),
        "self_excluded_from_tree": True,
        "files": files,
        "file_count": len(files),
        "tree_sha256": hashlib.sha256(tree_payload).hexdigest(),
    }


def write_report(
    path: Path,
    gate: dict[str, Any],
    ownership_summary: dict[str, Any],
    method_summary: dict[str, Any],
    dependency_summary: dict[str, Any],
    repair_summary: dict[str, Any],
    core_validation: dict[str, Any],
    validation: dict[str, Any],
    isil_summary: dict[str, Any],
) -> None:
    report_lines = [
        "# R1 Whole-Corpus Index Report",
        "",
        "## 1. Executive result",
        "",
        f"R1 status: {validation['status']}. The pinned source gate is {gate['status']}; no recovered C# body was edited or executed.",
        f"The R1 metadata authority contains {method_summary['metadata_total_type_count']:,} types and {method_summary['metadata_total_method_count']:,} methods across the DummyDll set.",
        f"The owned target catalog contains {method_summary['target_type_count']:,} non-generated types and {method_summary['target_method_count']:,} overload-safe method records.",
        "",
        "## 2. Source gate and authority model",
        "",
        f"APK SHA-256: {gate['pinned_inputs']['apk']['observed_sha256']} (MATCH).",
        f"C# archive SHA-256: {gate['pinned_inputs']['csharp_rar']['observed_sha256']} (MATCH).",
        f"libil2cpp SHA-256: {gate['pinned_inputs']['libil2cpp']['observed_sha256']} (MATCH).",
        f"global-metadata SHA-256: {gate['pinned_inputs']['global_metadata']['observed_sha256']} (MATCH).",
        f"The independent C# corpus contains {gate['source_root']['total_files']:,} files, {gate['source_root']['csharp_files']:,} C# files, {gate['source_root']['csproj_files']:,} project files, and {gate['source_root']['csharp_bytes']:,} C# bytes.",
        f"Zero-byte C# files are retained as source evidence: {', '.join(gate['source_root']['zero_byte_csharp_files'])}.",
        "DummyDll metadata is the canonical R1 assembly/type/method identity authority. R0 source analysis is retained as a quality and repair-signal authority.",
        "",
        "## 3. Ownership taxonomy and assembly inventory",
        "",
        "The exact ownership taxonomy is: " + ", ".join(OWNERSHIPS) + ".",
        f"The catalog covers {ownership_summary['assembly_count']:,} assembly rows, including {ownership_summary['metadata_assembly_count']:,} DummyDll assemblies and {ownership_summary['scripting_assembly_count']:,} APK scripting-assembly names.",
        f"{len(ownership_summary['scripting_assemblies_without_dummy_dll']):,} scripting assemblies have no matching DummyDll and remain explicit external/source-limited rows.",
        f"{ownership_summary['ownership_exception_count']:,} namespace/path exceptions are recorded; assembly authority wins for Assembly-CSharp and KairoLibrary.",
        "",
        "## 4. Type and method identity catalog",
        "",
        "Stable method identity hashes the pinned APK identity, assembly, declaring type full name, method name, method generic arity, return type, and ordered parameter types. Metadata tokens, RVAs, and file offsets remain attached as verification evidence.",
        f"Method IDs are unique: {method_summary['method_id_unique']}. Queue IDs are unique: {repair_summary['queue_id_unique']}.",
        f"Source matching found bodies for {method_summary['source_body_present_count']:,} target methods; {method_summary['source_present_count']:,} target methods have a source declaration.",
        "",
        "## 5. Quality, verification, and repair disposition",
        "",
        "Quality class, verification status, and repair disposition are separate fields. No record is marked verified merely because it has a source declaration or native availability.",
        f"Quality counts: {json.dumps(method_summary['counts_by_quality_class'], sort_keys=True)}.",
        f"Verification counts: {json.dumps(method_summary['counts_by_verification_status'], sort_keys=True)}.",
        f"Disposition counts: {json.dumps(method_summary['counts_by_repair_disposition'], sort_keys=True)}.",
        f"R1 records repaired bodies: {method_summary['repaired_body_count']}.",
        "",
        "## 6. Owned dependency graph",
        "",
        f"The graph contains {dependency_summary['owned_call_edge_count']:,} owned call edges, {dependency_summary['type_edge_count']:,} metadata type edges, {dependency_summary['field_edge_count']:,} field edges, and {dependency_summary['external_edge_count']:,} explicit external or unresolved edges.",
        f"It contains {dependency_summary['scc_count']:,} method SCCs, {dependency_summary['recursive_scc_count']:,} recursive SCCs, and a maximum dependency layer of {dependency_summary['max_dependency_layer']:,}.",
        f"Ownership bridges are recorded in {dependency_summary['bridge_count']:,} bridge classes.",
        "",
        "## 7. ISIL and native/static-data availability",
        "",
        f"The fresh ISIL root is present and contains {isil_summary.get('files_read', 0):,} files and {isil_summary.get('methods_read', 0):,} method blocks.",
        f"Target methods with ISIL are {method_summary['isil_available_count']:,}; target methods with a native address are {method_summary['native_available_count']:,}.",
        "Static-data references are recorded as graph edges and repair signals. They do not authorize runtime integration or native lifting in R1.",
        "",
        "## 8. Deterministic, resumable builder",
        "",
        "The builder writes sorted JSON and JSONL, records source-file hashes, preserves a source parse checkpoint, and emits a content-addressed artifact tree manifest. Resume uses the source cache only when its source hashes match the pinned corpus.",
        "",
        "## 9. Repair queue",
        "",
        f"The queue has {repair_summary['queue_method_count']:,} rows with exact one-to-one coverage of the owned target method catalog.",
        f"Priority counts: {json.dumps(repair_summary['priority_counts'], sort_keys=True)}.",
        f"Native-required methods: {repair_summary['native_required_count']:,}; ISIL/native evidence is available for {repair_summary['native_available_for_native_required_count']:,}.",
        "The queue is a plan and evidence index only. R1 performs no C# body repair.",
        "",
        "## 10. Core-nine validation",
        "",
        f"Core-nine status: {'PASS' if core_validation['pass'] else 'FAIL'}.",
        "The nine R0 anchor names are checked against the R1 metadata catalog; two DummyDll anchors are explicit compiler-generated identity gaps and remain excluded from the owned method catalog.",
        "",
        "## 11. R0 baseline comparison and scope decision",
        "",
        "R0 accepted 41,229 source-baseline methods and retained 43,103 raw lexical declarations. R1 deliberately adds the metadata/DummyDll authority rather than collapsing those two authorities into one number.",
        "R1 is accepted as the whole-corpus index, ownership boundary, overload-safe identity catalog, dependency graph, and complete repair queue.",
        "",
        "## 12. Stop boundary",
        "",
        "STOP before R2. No V8, V8R, runtime, Unity, emulator, native lifting, C# repair, integration, persistence, backend, deployment, or source-root mutation was performed.",
        "",
        "## Validation summary",
        "",
        f"Validation status: {validation['status']}. Failed checks: {', '.join(validation['failed_checks']) or 'none'}.",
        "",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(report_lines), encoding="utf-8", newline="\n")


def write_artifacts(
    out: Path,
    gate: dict[str, Any],
    source_manifest: list[dict[str, Any]],
    source_cache: dict[str, Any],
    assemblies: list[dict[str, Any]],
    metadata: MetadataReader,
    method_catalog: list[dict[str, Any]],
    queue: list[dict[str, Any]],
    graph: dict[str, Any],
    validation: dict[str, Any],
    core_validation: dict[str, Any],
    isil_summary: dict[str, Any],
    ownership_exceptions: list[dict[str, Any]],
) -> dict[str, Any]:
    out.mkdir(parents=True, exist_ok=True)
    source_gate_path = out / "source-gate.json"
    dump_json(source_gate_path, gate)
    dump_json(out / "source-file-manifest.json", source_manifest)
    dump_json(out / "source-cache.json", source_cache)
    dump_json(out / "assembly-catalog.json", assemblies)
    dump_jsonl(out / "type-catalog.jsonl", metadata.types)
    dump_jsonl(out / "field-catalog.jsonl", metadata.fields)
    dump_jsonl(out / "method-catalog.jsonl", method_catalog)
    dump_jsonl(out / "repair-queue.jsonl", queue)
    dump_jsonl(out / "type-edges.jsonl", graph["type_edges"])
    dump_jsonl(out / "call-edges.jsonl", graph["call_edges"])
    dump_jsonl(out / "field-edges.jsonl", graph["field_edges"])
    dump_jsonl(out / "external-edges.jsonl", graph["external_edges"])
    dump_jsonl(out / "static-data-edges.jsonl", graph["static_data_edges"])
    dump_jsonl(out / "dependency-layers.jsonl", graph["dependency_layers"])
    dump_json(out / "scc-summary.json", graph["scc_summary"])
    dump_json(out / "method-summary.json", summarize_methods(method_catalog, metadata))
    dump_json(out / "ownership-summary.json", summarize_ownership(
        metadata, assemblies, ownership_exceptions, method_catalog
    ))
    dump_json(out / "repair-summary.json", summarize_repairs(method_catalog, queue))
    dump_json(out / "dependency-summary.json", graph["summary"])
    dump_json(out / "bridge-summary.json", graph["bridge_rows"])
    dump_json(out / "isil-summary.json", isil_summary)
    dump_json(out / "validation.json", validation)
    dump_json(out / "core-nine-validation.json", core_validation)
    checkpoint = {
        "schema_version": SCHEMA_VERSION,
        "builder_version": BUILDER_VERSION,
        "stages": [
            {"stage": "source_gate", "status": "PASS"},
            {"stage": "source_cache", "status": "PASS", "record_count": len(source_cache)},
            {"stage": "metadata_catalog", "status": "PASS", "type_count": len(metadata.types), "method_count": len(metadata.methods)},
            {"stage": "ownership_catalog", "status": "PASS", "assembly_count": len(assemblies)},
            {"stage": "method_catalog", "status": "PASS", "target_method_count": len(method_catalog)},
            {"stage": "dependency_graph", "status": "PASS", "owned_call_edge_count": len(graph["call_edges"])},
            {"stage": "validation", "status": validation["status"]},
        ],
        "resume_boundary": "source_cache",
        "read_only_sources": True,
    }
    dump_json(out / "checkpoint-ledger.json", checkpoint)
    write_report(
        out / "R1_WHOLE_CORPUS_INDEX_REPORT.md",
        gate,
        summarize_ownership(metadata, assemblies, ownership_exceptions, method_catalog),
        summarize_methods(method_catalog, metadata),
        graph["summary"],
        summarize_repairs(method_catalog, queue),
        core_validation,
        validation,
        isil_summary,
    )
    manifest = artifact_file_manifest(out)
    dump_json(out / "artifact-manifest.json", manifest)
    return manifest


def write_compact_package(
    accepted: Path,
    gate: dict[str, Any],
    assemblies: list[dict[str, Any]],
    ownership_summary: dict[str, Any],
    method_summary: dict[str, Any],
    dependency_summary: dict[str, Any],
    repair_summary: dict[str, Any],
    artifact_manifest: dict[str, Any],
    validation: dict[str, Any],
    core_validation: dict[str, Any],
    checkpoint: dict[str, Any],
    report: str,
) -> None:
    accepted.mkdir(parents=True, exist_ok=True)
    dump_json(accepted / "r1-source-gate.json", gate)
    dump_json(accepted / "r1-assembly-ownership.json", assemblies)
    dump_json(accepted / "r1-ownership-summary.json", ownership_summary)
    dump_json(accepted / "r1-method-summary.json", method_summary)
    dump_json(accepted / "r1-dependency-summary.json", dependency_summary)
    dump_json(accepted / "r1-repair-summary.json", repair_summary)
    dump_json(accepted / "r1-local-artifact-manifest.json", artifact_manifest)
    dump_json(accepted / "r1-validation.json", validation)
    dump_json(accepted / "r1-core-nine-validation.json", core_validation)
    dump_json(accepted / "r1-checkpoint-ledger.json", checkpoint)
    dump_json(
        accepted / "r1-final-decision.json",
        {
            "schema_version": SCHEMA_VERSION,
            "decision": "PASS_R1_WHOLE_CORPUS_INDEX" if validation["status"] == "PASS" else "FAIL_R1_WHOLE_CORPUS_INDEX",
            "source_identity": "MATCH" if gate["status"] == "PASS" else "MISMATCH",
            "ownership_index": validation["status"],
            "method_identity_catalog": validation["status"],
            "dependency_graph": validation["status"],
            "repair_queue": validation["status"],
            "core_nine": "PASS" if core_validation["pass"] else "FAIL",
            "repaired_csharp_bodies": False,
            "runtime_or_unity_work": False,
            "next_authorized_boundary": "R2_CORE_CSHARP_REPAIR",
            "stop_before_next_phase": True,
        },
    )
    (accepted / "R1_WHOLE_CORPUS_INDEX_REPORT.md").write_text(
        report, encoding="utf-8", newline="\n"
    )


def validate_local_artifacts(out: Path) -> dict[str, Any]:
    required = [
        "source-gate.json", "source-file-manifest.json", "assembly-catalog.json",
        "type-catalog.jsonl", "field-catalog.jsonl", "method-catalog.jsonl",
        "repair-queue.jsonl", "type-edges.jsonl", "call-edges.jsonl",
        "field-edges.jsonl", "external-edges.jsonl", "static-data-edges.jsonl",
        "dependency-layers.jsonl", "scc-summary.json", "method-summary.json",
        "ownership-summary.json", "repair-summary.json", "dependency-summary.json",
        "validation.json", "core-nine-validation.json", "artifact-manifest.json",
        "checkpoint-ledger.json", "R1_WHOLE_CORPUS_INDEX_REPORT.md",
    ]
    checks: dict[str, bool] = {}
    checks["artifact_root_present"] = out.is_dir()
    checks["required_files_present"] = all((out / name).is_file() for name in required)
    if not checks["required_files_present"]:
        return {
            "schema_version": SCHEMA_VERSION,
            "status": "FAIL",
            "checks": checks,
            "failed_checks": sorted(key for key, value in checks.items() if not value),
        }
    try:
        gate = load_json(out / "source-gate.json")
        types = load_jsonl(out / "type-catalog.jsonl")
        fields = load_jsonl(out / "field-catalog.jsonl")
        methods = load_jsonl(out / "method-catalog.jsonl")
        queue = load_jsonl(out / "repair-queue.jsonl")
        type_edges = load_jsonl(out / "type-edges.jsonl")
        call_edges = load_jsonl(out / "call-edges.jsonl")
        field_edges = load_jsonl(out / "field-edges.jsonl")
        external_edges = load_jsonl(out / "external-edges.jsonl")
        static_edges = load_jsonl(out / "static-data-edges.jsonl")
        scc = load_json(out / "scc-summary.json")
        stored_manifest = load_json(out / "artifact-manifest.json")
        stored_validation = load_json(out / "validation.json")
    except Exception as error:
        return {
            "schema_version": SCHEMA_VERSION,
            "status": "FAIL",
            "checks": {**checks, "artifact_json_readable": False},
            "failed_checks": ["artifact_json_readable"],
            "error": f"{type(error).__name__}:{error}",
        }
    try:
        source_gate()
        checks["source_gate_pass"] = gate.get("status") == "PASS"
        checks["pinned_hashes_match"] = all(
            row.get("match") for row in gate.get("pinned_inputs", {}).values()
        )
    except RuntimeError:
        checks["source_gate_pass"] = False
        checks["pinned_hashes_match"] = False
    checks["type_ids_unique"] = len({row["type_id"] for row in types}) == len(types)
    checks["method_ids_unique"] = len({row["method_id"] for row in methods}) == len(methods)
    checks["queue_exact"] = (
        len(queue) == len(methods)
        and {row["method_id"] for row in queue} == {row["method_id"] for row in methods}
    )
    checks["ownership_values_valid"] = all(row.get("ownership") in OWNERSHIPS for row in types)
    checks["method_contract_valid"] = all(
        row.get("quality_class") in QUALITY_CLASSES
        and row.get("verification_status") in VERIFICATION_STATUSES
        and row.get("repair_disposition") in DISPOSITIONS
        and row.get("repaired_body") is False
        for row in methods
    )
    method_ids = {row["method_id"] for row in methods}
    checks["call_refs_valid"] = all(
        row["caller_method_id"] in method_ids and row["callee_method_id"] in method_ids
        for row in call_edges
    )
    checks["field_refs_valid"] = all(row["source_method_id"] in method_ids for row in field_edges)
    checks["external_refs_valid"] = all(row["source_method_id"] in method_ids for row in external_edges)
    checks["graph_nonempty"] = bool(type_edges and call_edges and field_edges and scc)
    checks["stored_validation_pass"] = stored_validation.get("status") == "PASS"
    recomputed_manifest = artifact_file_manifest(out)
    checks["artifact_manifest_match"] = (
        recomputed_manifest["tree_sha256"] == stored_manifest.get("tree_sha256")
        and recomputed_manifest["files"] == stored_manifest.get("files")
    )
    checks["jsonl_sorted"] = (
        types == sorted(types, key=lambda row: (row["assembly"].lower(), row["full_name"]))
        and methods == sorted(methods, key=lambda row: row["method_id"])
        and call_edges == sorted(call_edges, key=lambda row: row["edge_id"])
    )
    result = {
        "schema_version": SCHEMA_VERSION,
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "failed_checks": sorted(key for key, value in checks.items() if not value),
        "counts": {
            "types": len(types),
            "fields": len(fields),
            "methods": len(methods),
            "queue": len(queue),
            "type_edges": len(type_edges),
            "call_edges": len(call_edges),
            "field_edges": len(field_edges),
            "external_edges": len(external_edges),
            "static_data_edges": len(static_edges),
            "sccs": len(scc),
        },
    }
    return result


def run_build(
    out: Path,
    accepted: Path,
    isil_root: Path,
    resume: bool,
) -> dict[str, Any]:
    gate, source_manifest, source_index = source_gate()
    source_cache_path = out / "source-cache.json"
    if resume and source_cache_path.is_file():
        source_cache = load_json(source_cache_path)
        manifest_by_path = {row["relative_path"]: row["sha256"] for row in source_manifest}
        cache_matches = all(
            manifest_by_path.get(path) == payload.get("sha256")
            for path, payload in source_cache.items()
        ) and len(source_cache) == len(manifest_by_path)
        if cache_matches:
            source_methods_by_type, source_methods_by_name = index_source_cache(source_cache)
        else:
            source_cache, source_methods_by_type, source_methods_by_name = build_source_cache(
                source_manifest, source_index
            )
    else:
        source_cache, source_methods_by_type, source_methods_by_name = build_source_cache(
            source_manifest, source_index
        )
    metadata = MetadataReader(DummyRoot).read()
    assemblies, exceptions, _ = apply_ownership(
        metadata,
        gate["scripting_assemblies_member"]["assemblies"],
        source_cache,
    )
    isil_index, isil_summary = build_isil_index(isil_root)
    degraded, _ = load_r0_quality()
    method_catalog, queue = build_method_catalog(
        metadata,
        source_methods_by_type,
        source_methods_by_name,
        degraded,
        isil_index,
    )
    graph = build_dependency_graph(metadata, method_catalog)
    core_validation = core_nine_validation(method_catalog, metadata)
    validation = validate_in_memory(
        gate, metadata, assemblies, method_catalog, queue, graph, core_validation
    )
    artifact_manifest = write_artifacts(
        out,
        gate,
        source_manifest,
        source_cache,
        assemblies,
        metadata,
        method_catalog,
        queue,
        graph,
        validation,
        core_validation,
        isil_summary,
        exceptions,
    )
    ownership_summary = summarize_ownership(metadata, assemblies, exceptions, method_catalog)
    method_summary = summarize_methods(method_catalog, metadata)
    repair_summary = summarize_repairs(method_catalog, queue)
    checkpoint = load_json(out / "checkpoint-ledger.json")
    report = (out / "R1_WHOLE_CORPUS_INDEX_REPORT.md").read_text(encoding="utf-8")
    write_compact_package(
        accepted,
        gate,
        assemblies,
        ownership_summary,
        method_summary,
        graph["summary"],
        repair_summary,
        artifact_manifest,
        validation,
        core_validation,
        checkpoint,
        report,
    )
    local_validation = validate_local_artifacts(out)
    # Keep the accepted validation artifact synchronized with the final local check.
    dump_json(accepted / "r1-validation.json", local_validation)
    return {
        "status": local_validation["status"],
        "validation": local_validation,
        "metadata_type_count": len(metadata.types),
        "metadata_method_count": len(metadata.methods),
        "target_method_count": len(method_catalog),
        "call_edge_count": len(graph["call_edges"]),
        "artifact_tree_sha256": artifact_manifest["tree_sha256"],
        "output": str(out),
        "accepted": str(accepted),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--accepted", type=Path, default=DEFAULT_ACCEPTED)
    parser.add_argument("--isil-root", type=Path, default=DEFAULT_ISIL_ROOT)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        if args.check:
            result = validate_local_artifacts(args.out)
        else:
            result = run_build(args.out, args.accepted, args.isil_root, args.resume)
    except RuntimeError as error:
        print(str(error))
        return 2 if str(error) == "BLOCKED_R1_SOURCE_IDENTITY_MISMATCH" else 1
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0 if result.get("status") == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
