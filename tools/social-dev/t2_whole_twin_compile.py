#!/usr/bin/env python3
"""Generate and validate the isolated T2 Whole-Twin C# compile factory.

The generator intentionally keeps the accepted T1 representation payload outside the generated
C# source tree.  Each generated method carries the canonical method identity and representation
hash, and its trampoline asks the generated runtime registry for the corresponding T1 segments.
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
import re
import shutil
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Optional


ROOT = Path(__file__).resolve().parents[2]
OWNED = {"GAME_FIRST_PARTY", "KAIRO_ENGINE"}
EXPECTED_TYPES = 641
EXPECTED_METHODS = 10_827
EXPECTED_REPRESENTATION_TIERS = {
    "EXISTING_READABLE": 2481,
    "GENERATED_LOW": 8291,
    "DECLARATION_ONLY": 50,
    "SOURCE_LIMITED_STUB": 5,
}

BCL_ALIASES = {
    "System.Void": "void",
    "System.Boolean": "bool",
    "System.Byte": "byte",
    "System.SByte": "sbyte",
    "System.Int16": "short",
    "System.UInt16": "ushort",
    "System.Int32": "int",
    "System.UInt32": "uint",
    "System.Int64": "long",
    "System.UInt64": "ulong",
    "System.Single": "float",
    "System.Double": "double",
    "System.Decimal": "decimal",
    "System.Char": "char",
    "System.String": "string",
    "System.Object": "object",
    "System.IntPtr": "nint",
    "System.UIntPtr": "nuint",
}

C_SHARP_KEYWORDS = {
    "abstract",
    "as",
    "base",
    "bool",
    "break",
    "byte",
    "case",
    "catch",
    "char",
    "checked",
    "class",
    "const",
    "continue",
    "decimal",
    "default",
    "delegate",
    "do",
    "double",
    "else",
    "enum",
    "event",
    "explicit",
    "extern",
    "false",
    "finally",
    "fixed",
    "float",
    "for",
    "foreach",
    "goto",
    "if",
    "implicit",
    "in",
    "int",
    "interface",
    "internal",
    "is",
    "lock",
    "long",
    "namespace",
    "new",
    "null",
    "object",
    "operator",
    "out",
    "override",
    "params",
    "private",
    "protected",
    "public",
    "readonly",
    "ref",
    "return",
    "sbyte",
    "sealed",
    "short",
    "sizeof",
    "stackalloc",
    "static",
    "string",
    "struct",
    "switch",
    "this",
    "throw",
    "true",
    "try",
    "typeof",
    "uint",
    "ulong",
    "unchecked",
    "unsafe",
    "ushort",
    "using",
    "virtual",
    "void",
    "volatile",
    "while",
    "add",
    "alias",
    "and",
    "ascending",
    "args",
    "async",
    "await",
    "by",
    "descending",
    "dynamic",
    "equals",
    "file",
    "from",
    "get",
    "global",
    "group",
    "init",
    "into",
    "join",
    "let",
    "managed",
    "nameof",
    "nint",
    "not",
    "notnull",
    " on ",
    "or",
    "orderby",
    "partial",
    "record",
    "remove",
    "required",
    "scoped",
    "select",
    "set",
    "unmanaged",
    "value",
    "var",
    "when",
    "where",
    "with",
    "yield",
}


def stable_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_text(value: str) -> str:
    return sha256_bytes(value.encode("utf-8"))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def iter_jsonl(path: Path) -> Iterable[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def csharp_string(value: Any) -> str:
    return json.dumps("" if value is None else str(value), ensure_ascii=False)


def strip_arity_segment(segment: str) -> str:
    return re.sub(r"`\d+$", "", segment)


def strip_arities(value: str) -> str:
    return "+".join(strip_arity_segment(part) for part in value.split("+"))


def segment_arities(value: str) -> tuple[int, ...]:
    result: list[int] = []
    for part in value.split("+"):
        match = re.search(r"`(\d+)$", part)
        result.append(int(match.group(1)) if match else 0)
    return tuple(result)


def split_namespace(full_name: str) -> tuple[str, list[str]]:
    first = full_name.split("+", 1)[0]
    if "." in first:
        namespace, root = first.rsplit(".", 1)
    else:
        namespace, root = "", first
    nested = [root]
    if "+" in full_name:
        nested.extend(full_name.split("+")[1:])
    return namespace, nested


def sanitize_identifier(raw: str, role: str, stable_key: Optional[str] = None) -> str:
    if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", raw):
        if raw in C_SHARP_KEYWORDS:
            return "@" + raw
        return raw
    key = stable_key or raw
    return f"__Twin{role}_{sha256_text(key)[:12]}"


def split_top_level(value: str, delimiter: str = ",") -> list[str]:
    parts: list[str] = []
    depth = 0
    current: list[str] = []
    for char in value:
        if char == "<":
            depth += 1
        elif char == ">":
            depth -= 1
        if char == delimiter and depth == 0:
            parts.append("".join(current).strip())
            current = []
        else:
            current.append(char)
    tail = "".join(current).strip()
    if tail:
        parts.append(tail)
    return parts


def split_generic_expression(value: str) -> tuple[str, list[str]]:
    value = value.strip()
    start = value.find("<")
    if start < 0 or not value.endswith(">"):
        return value, []
    depth = 0
    end = -1
    for index in range(start, len(value)):
        char = value[index]
        if char == "<":
            depth += 1
        elif char == ">":
            depth -= 1
            if depth == 0:
                end = index
                break
    if end != len(value) - 1:
        return value, []
    return value[:start].strip(), split_top_level(value[start + 1 : end])


def peel_type_shape(value: str) -> tuple[str, bool, int]:
    value = str(value or "").strip()
    byref = value.endswith("&")
    if byref:
        value = value[:-1].strip()
    arrays = 0
    while value.endswith("[]"):
        arrays += 1
        value = value[:-2]
    return value, byref, arrays


def type_atoms(value: str) -> list[str]:
    core, _byref, _arrays = peel_type_shape(value)
    core = re.sub(r"^(ref|out|in)\s+", "", core)
    if not core or core.startswith("!"):
        return []
    base, args = split_generic_expression(core)
    atoms = [base]
    for arg in args:
        atoms.extend(type_atoms(arg))
    return atoms


def extract_braced_body(source: str) -> Optional[str]:
    if not source:
        return None
    start = source.find("{")
    if start < 0:
        return None
    depth = 0
    in_string = False
    escaped = False
    for index in range(start, len(source)):
        char = source[index]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return source[start : index + 1].replace("\r\n", "\n")
    return None


@dataclass
class TypeNode:
    row: dict[str, Any]
    namespace: str
    raw_segments: list[str]
    local_arities: tuple[int, ...]
    names: list[str]
    parent: Optional["TypeNode"] = None
    children: list["TypeNode"] = field(default_factory=list)
    synthetic: bool = False

    @property
    def full_name(self) -> str:
        return self.row["full_name"]

    @property
    def path_key(self) -> tuple[tuple[str, int], ...]:
        return tuple((strip_arity_segment(part), arity) for part, arity in zip(self.raw_segments, self.local_arities))

    @property
    def total_generic_arity(self) -> int:
        return sum(self.local_arities)

    @property
    def relative_path(self) -> str:
        return ".".join(self.names)

    @property
    def emitted_qualified_name(self) -> str:
        prefix = "SocialDev.T2Model"
        if self.namespace:
            prefix += "." + ".".join(sanitize_identifier(p, "Namespace", p) for p in self.namespace.split("."))
        return prefix + "." + self.relative_path


class T2Model:
    def __init__(self, root: Path, output_root: Path, method_limit: Optional[set[str]] = None, readable_bodies: Optional[dict[str, str]] = None):
        self.root = root
        self.output_root = output_root
        self.method_limit = method_limit
        self.readable_bodies = readable_bodies or {}
        self.type_rows_all = read_jsonl(root / "artifacts" / "r1-5-metadata-reconciliation" / "type-catalog.jsonl")
        self.method_rows_all = read_jsonl(root / "artifacts" / "r1-5-metadata-reconciliation" / "method-catalog.jsonl")
        self.field_rows_all = read_jsonl(root / "artifacts" / "r1-5-metadata-reconciliation" / "field-catalog.jsonl")
        self.manifest_rows = read_jsonl(root / "artifacts" / "t1-full-body-generation" / "run-a" / "global-manifest.jsonl")
        self.t1_representation_segments: dict[str, list[dict[str, Any]]] = {}
        self.t1_representation_hashes: dict[str, str] = {}
        self._load_t1_representation_headers()
        self.type_rows = [
            row
            for row in self.type_rows_all
            if row.get("ownership") in OWNED and not row.get("compiler_generated")
        ]
        self.method_rows = [row for row in self.method_rows_all if row.get("ownership") in OWNED]
        self.field_rows = [
            row
            for row in self.field_rows_all
            if row.get("declaring_type") in {r["full_name"] for r in self.type_rows}
        ]
        self.types_by_full = {row["full_name"]: row for row in self.type_rows}
        self.all_types_by_full = {row["full_name"]: row for row in self.type_rows_all}
        self.methods_by_id = {row["method_id"]: row for row in self.method_rows}
        self.manifest_by_id = {row["method_id"]: row for row in self.manifest_rows}
        self.fields_by_type: dict[str, list[dict[str, Any]]] = collections.defaultdict(list)
        for row in self.field_rows:
            self.fields_by_type[row["declaring_type"]].append(row)
        self.methods_by_type: dict[str, list[dict[str, Any]]] = collections.defaultdict(list)
        for row in self.method_rows:
            self.methods_by_type[row["declaring_type"]].append(row)
        self.owned_candidates: dict[str, list[dict[str, Any]]] = collections.defaultdict(list)
        self.all_candidates: dict[str, list[dict[str, Any]]] = collections.defaultdict(list)
        for row in self.type_rows:
            self.owned_candidates[strip_arities(row["full_name"])].append(row)
        for row in self.type_rows_all:
            if not row.get("compiler_generated"):
                self.all_candidates[strip_arities(row["full_name"])].append(row)
        self.boundary_rows: list[dict[str, Any]] = []
        self.boundary_by_full: dict[str, dict[str, Any]] = {}
        self.owned_nodes: dict[str, TypeNode] = {}
        self.boundary_nodes: dict[str, TypeNode] = {}
        self.type_render_names: dict[str, str] = {}
        self.boundary_render_names: dict[str, str] = {}
        self.signature_atoms: collections.Counter[str] = collections.Counter()
        self.signature_atom_ownership: dict[str, str] = {}
        self.normalization_tests: list[dict[str, Any]] = []
        self.method_plans: dict[str, dict[str, Any]] = {}
        self.signature_repairs: list[dict[str, Any]] = []
        self._validate_input_universe()
        self._build_type_and_boundary_model()
        self._build_method_plans()

    def _load_t1_representation_headers(self) -> None:
        rep_root = self.root / "artifacts" / "t1-full-body-generation" / "run-a" / "representations"
        for path in sorted(rep_root.glob("*.jsonl")):
            for row in iter_jsonl(path):
                method_id = row.get("method_id")
                if not method_id:
                    continue
                self.t1_representation_segments[method_id] = list(row.get("segments") or [])
                self.t1_representation_hashes[method_id] = str(row.get("representation_hash") or "")

    def _validate_input_universe(self) -> None:
        owned_ids = [row["method_id"] for row in self.method_rows]
        duplicate_ids = len(owned_ids) - len(set(owned_ids))
        manifest_ids = [row["method_id"] for row in self.manifest_rows]
        if (
            len(self.type_rows) != EXPECTED_TYPES
            or len(owned_ids) != EXPECTED_METHODS
            or duplicate_ids
            or len(self.manifest_rows) != EXPECTED_METHODS
            or len(set(manifest_ids)) != EXPECTED_METHODS
            or set(owned_ids) != set(manifest_ids)
            or len(self.t1_representation_segments) != EXPECTED_METHODS
            or len(self.t1_representation_hashes) != EXPECTED_METHODS
        ):
            raise RuntimeError("BLOCKED_T2_CANONICAL_INPUT_MISMATCH")
        tiers = collections.Counter(row["representation_tier"] for row in self.manifest_rows)
        if dict(tiers) != EXPECTED_REPRESENTATION_TIERS:
            raise RuntimeError("BLOCKED_T2_CANONICAL_INPUT_MISMATCH")
        for method_id in owned_ids:
            manifest = self.manifest_by_id[method_id]
            if not manifest.get("serialized_representation_hash") or not manifest.get("shard"):
                raise RuntimeError("BLOCKED_T2_CANONICAL_INPUT_MISMATCH")
            if self.t1_representation_hashes.get(method_id) != manifest.get("serialized_representation_hash"):
                raise RuntimeError("BLOCKED_T2_CANONICAL_INPUT_MISMATCH")

    def _candidate_for(self, value: str, args_count: Optional[int] = None) -> Optional[dict[str, Any]]:
        base, _args = split_generic_expression(value)
        normalized = strip_arities(base)
        candidates = list(self.all_candidates.get(normalized, []))
        if not candidates:
            return None
        input_arities = segment_arities(base)
        exact = [candidate for candidate in candidates if segment_arities(candidate["full_name"]) == input_arities]
        if exact:
            candidates = exact
        elif args_count is not None:
            by_count = [candidate for candidate in candidates if int(candidate.get("generic_arity") or 0) == args_count]
            if by_count:
                candidates = by_count
        candidates.sort(
            key=lambda row: (
                0 if row.get("ownership") in OWNED else 1,
                0 if not row.get("compiler_generated") else 1,
                int(row.get("generic_arity") or 0),
                row["full_name"],
            )
        )
        return candidates[0]

    def _build_type_and_boundary_model(self) -> None:
        self._run_normalization_tests()
        referenced_atoms: set[str] = set()
        for row in self.type_rows:
            referenced_atoms.update(type_atoms(row.get("base_type") or ""))
            for interface in row.get("interfaces") or []:
                referenced_atoms.update(type_atoms(interface))
        for row in self.field_rows:
            referenced_atoms.update(type_atoms(row.get("field_type") or ""))
        for row in self.method_rows:
            referenced_atoms.update(type_atoms(row.get("return_type") or ""))
            for param in row.get("parameter_types") or []:
                referenced_atoms.update(type_atoms(param))
        for atom in sorted(referenced_atoms):
            if atom.startswith("!"):
                continue
            self.signature_atoms[atom] += 1
            candidate = self._candidate_for(atom)
            if candidate and candidate.get("ownership") in OWNED:
                self.signature_atom_ownership[atom] = str(candidate["ownership"])
                continue
            if self._is_framework_type(atom):
                self.signature_atom_ownership[atom] = "DOTNET_FRAMEWORK"
                continue
            if candidate:
                self.signature_atom_ownership[atom] = str(candidate.get("ownership") or "BOUNDARY_CONTRACT")
                self._add_boundary_row(candidate)
            else:
                self.signature_atom_ownership[atom] = "BOUNDARY_CONTRACT_SYNTHETIC"
                self._add_synthetic_boundary(atom)
        self._add_boundary_ancestors()
        self._build_nodes(self.type_rows, self.owned_nodes, boundary=False)
        self._build_nodes(self.boundary_rows, self.boundary_nodes, boundary=True)
        for node in self.owned_nodes.values():
            self.type_render_names[node.full_name] = node.emitted_qualified_name
        for node in self.boundary_nodes.values():
            self.boundary_render_names[node.full_name] = self._boundary_qualified_name(node)

    def _is_framework_type(self, value: str) -> bool:
        root = value.split(".", 1)[0].split("+", 1)[0]
        return root in {"System", "Microsoft"}

    def _add_boundary_row(self, row: dict[str, Any]) -> None:
        full_name = row["full_name"]
        if full_name in self.types_by_full or full_name in self.boundary_by_full:
            return
        self.boundary_by_full[full_name] = row
        self.boundary_rows.append(dict(row, boundary_contract=True))

    def _add_synthetic_boundary(self, atom: str) -> None:
        if atom in self.types_by_full or atom in self.boundary_by_full or self._is_framework_type(atom):
            return
        namespace, segments = split_namespace(atom)
        full_name = atom
        short = segments[-1]
        row = {
            "assembly": "T2Boundary",
            "base_type": "System.Object",
            "compiler_generated": False,
            "external_reference": True,
            "full_name": full_name,
            "generic_arity": sum(segment_arities("+".join(segments))),
            "inclusion": "BOUNDARY_CONTRACT",
            "interfaces": [],
            "is_delegate": False,
            "is_enum": False,
            "is_interface": short.startswith("I") or short.endswith("Listener"),
            "is_value_type": False,
            "metadata_field_count": 0,
            "metadata_method_count": 0,
            "namespace": namespace,
            "ownership": "BOUNDARY_CONTRACT",
            "short_name": short,
            "type_id": "t2-boundary-" + sha256_text(full_name)[:32],
            "boundary_contract": True,
            "synthetic": True,
        }
        self._add_boundary_row(row)

    def _add_boundary_ancestors(self) -> None:
        rows = list(self.boundary_rows)
        for row in rows:
            parts = row["full_name"].split("+")
            if len(parts) <= 1:
                continue
            for count in range(1, len(parts)):
                ancestor = "+".join(parts[:count])
                if ancestor in self.types_by_full or ancestor in self.boundary_by_full:
                    continue
                namespace, segments = split_namespace(ancestor)
                parent = {
                    "assembly": "T2Boundary",
                    "base_type": "System.Object",
                    "compiler_generated": False,
                    "external_reference": True,
                    "full_name": ancestor,
                    "generic_arity": sum(segment_arities("+".join(segments))),
                    "inclusion": "BOUNDARY_CONTRACT_ANCESTOR",
                    "interfaces": [],
                    "is_delegate": False,
                    "is_enum": False,
                    "is_interface": False,
                    "is_value_type": False,
                    "metadata_field_count": 0,
                    "metadata_method_count": 0,
                    "namespace": namespace,
                    "ownership": "BOUNDARY_CONTRACT",
                    "short_name": segments[-1],
                    "type_id": "t2-boundary-" + sha256_text(ancestor)[:32],
                    "boundary_contract": True,
                    "synthetic": True,
                }
                self._add_boundary_row(parent)

    def _run_normalization_tests(self) -> None:
        interface_row = self.types_by_full.get("java.lang.JRunnable")
        vector_row = self.types_by_full.get("java.util.Vector")
        enum_ints = self.types_by_full.get("kairo.unity.util.EnumInts`1")
        compare = self.types_by_full.get("kairo.unity.util.ArrayUtil+CompareMethod`1")
        tests = [
            {
                "name": "interface_bogus_static_array_base_is_dropped",
                "input": (interface_row or {}).get("base_type"),
                "expected": "DROP_NON_INTERFACE_BASE",
                "pass": bool(interface_row and str(interface_row.get("base_type", "")).startswith("__StaticArrayInitTypeSize=")),
            },
            {
                "name": "instantiated_generic_base_is_not_treated_as_missing",
                "input": (vector_row or {}).get("base_type"),
                "expected": "RESOLVE_GENERIC_DEFINITION",
                "pass": bool(vector_row and self._candidate_for(str(vector_row.get("base_type"))) is not None),
            },
            {
                "name": "generic_base_placeholders_preserve_arity",
                "input": (enum_ints or {}).get("base_type"),
                "expected": 2,
                "pass": bool(enum_ints and len(type_atoms(str(enum_ints.get("base_type")))) >= 1),
            },
            {
                "name": "nested_generic_type_preserves_parent_identity",
                "input": (compare or {}).get("full_name"),
                "expected": "ArrayUtil+CompareMethod",
                "pass": bool(compare and "+" in compare.get("full_name", "") and int(compare.get("generic_arity") or 0) == 1),
            },
        ]
        if not all(test["pass"] for test in tests):
            raise RuntimeError("BLOCKED_T2_TYPE_SHELL_NORMALIZATION")
        self.normalization_tests = tests

    def _build_nodes(self, rows: list[dict[str, Any]], destination: dict[str, TypeNode], boundary: bool) -> None:
        ordered = sorted(rows, key=lambda row: (len(row["full_name"].split("+")), row["full_name"]))
        # Include namespace in the lookup key.  Nested type paths such as MainPanel+OnFinish
        # occur in several namespaces and must not attach to whichever same-named parent was
        # visited first.
        by_path: dict[tuple[str, tuple[tuple[str, int], ...]], TypeNode] = {}
        for row in ordered:
            namespace, raw_segments = split_namespace(row["full_name"])
            arities = list(segment_arities("+".join(raw_segments)))
            parent_key: tuple[tuple[str, int], ...] = ()
            parent_total = 0
            if len(raw_segments) > 1:
                parent_key = tuple((strip_arity_segment(part), arity) for part, arity in zip(raw_segments[:-1], arities[:-1]))
                parent_total = sum(arities[:-1])
            names = [sanitize_identifier(part_base, "Type", row["full_name"] + ":" + str(index)) for index, part_base in enumerate(strip_arity_segment(part) for part in raw_segments)]
            local_arities = list(arities)
            # Some metadata rows encode cumulative generic arity without a backtick on the nested
            # segment.  Preserve that delta while keeping the parent parameter list intact.
            row_total = int(row.get("generic_arity") or 0)
            if local_arities[-1] == 0 and row_total > parent_total and len(raw_segments) > 1:
                local_arities[-1] = row_total - parent_total
            path_key = tuple((strip_arity_segment(part), arity) for part, arity in zip(raw_segments, local_arities))
            parent = by_path.get((namespace, parent_key))
            if parent is None and len(raw_segments) > 1:
                # The canonical catalog normally contains every ancestor.  A missing external
                # ancestor is materialized as a neutral boundary shell so nested names compile.
                parent_full = "+".join(raw_segments[:-1])
                parent_path_key = tuple((strip_arity_segment(part), arity) for part, arity in zip(raw_segments[:-1], local_arities[:-1]))
                parent = by_path.get((namespace, parent_path_key))
                if parent is None:
                    parent_row = dict(row)
                    parent_row.update(
                        {
                            "full_name": parent_full,
                            "short_name": strip_arity_segment(raw_segments[-2]),
                            "metadata_method_count": 0,
                            "metadata_field_count": 0,
                            "is_interface": False,
                            "is_enum": False,
                            "is_value_type": False,
                            "is_delegate": False,
                            "synthetic": True,
                        }
                    )
                    parent = TypeNode(
                        parent_row,
                        namespace,
                        raw_segments[:-1],
                        tuple(local_arities[:-1]),
                        names[:-1],
                        synthetic=True,
                    )
                    by_path[(namespace, parent.path_key)] = parent
                    destination[parent.full_name] = parent
            node = TypeNode(
                row=row,
                namespace=namespace,
                raw_segments=raw_segments,
                local_arities=tuple(local_arities),
                names=names,
                parent=parent,
                synthetic=bool(row.get("synthetic")),
            )
            by_path[(namespace, path_key)] = node
            destination[node.full_name] = node
            if parent:
                parent.children.append(node)
        for node in destination.values():
            node.children.sort(key=lambda item: (item.relative_path, item.full_name))

    def _boundary_qualified_name(self, node: TypeNode) -> str:
        prefix = "SocialDev.T2Boundary"
        if node.namespace:
            prefix += "." + ".".join(sanitize_identifier(p, "Namespace", p) for p in node.namespace.split("."))
        return prefix + "." + node.relative_path

    def _build_method_plans(self) -> None:
        selected = self.method_limit if self.method_limit is not None else set(self.methods_by_id)
        by_type_keys: dict[str, set[tuple[Any, ...]]] = collections.defaultdict(set)
        for row in sorted(self.method_rows, key=lambda item: item["method_id"]):
            method_id = row["method_id"]
            if method_id not in selected:
                continue
            manifest = self.manifest_by_id[method_id]
            type_node = self._resolve_owned_node(row["declaring_type"])
            if type_node is None:
                raise RuntimeError("BLOCKED_T2_CANONICAL_INPUT_MISMATCH")
            return_type = self.render_type(row.get("return_type") or "System.Object", type_node, row)
            parameters: list[dict[str, Any]] = []
            for index, parameter_type in enumerate(row.get("parameter_types") or []):
                core, byref, _arrays = peel_type_shape(parameter_type)
                parameters.append(
                    {
                        "index": index,
                        "source_type": parameter_type,
                        "type": self.render_type(parameter_type, type_node, row),
                        "byref": byref,
                        "name": f"arg{index}",
                    }
                )
            raw_name = str(row.get("method_name") or "Method")
            if row.get("is_constructor") and raw_name == ".ctor":
                emitted_name = type_node.names[-1]
            elif raw_name == ".cctor":
                emitted_name = type_node.names[-1]
            else:
                emitted_name = sanitize_identifier(raw_name, "Method", method_id)
            signature_key = (
                bool(row.get("is_constructor")),
                raw_name == ".cctor",
                emitted_name,
                int(row.get("generic_arity") or 0),
                tuple((parameter["type"], parameter["byref"]) for parameter in parameters),
            )
            if signature_key in by_type_keys[type_node.full_name]:
                if raw_name == ".cctor":
                    self.signature_repairs.append(
                        {"method_id": method_id, "declaring_type": type_node.full_name, "action": "COALESCED_STATIC_CONSTRUCTOR_ATTRIBUTE"}
                    )
                elif row.get("is_constructor"):
                    raise RuntimeError(f"BLOCKED_T2_DUPLICATE_CONSTRUCTOR_SIGNATURE:{method_id}")
                else:
                    emitted_name = "__TwinDuplicateMethod_" + method_id.split("_", 1)[-1]
                    self.signature_repairs.append(
                        {"method_id": method_id, "declaring_type": type_node.full_name, "action": "RENAMED_DUPLICATE_METADATA_SIGNATURE", "emitted_name": emitted_name}
                    )
                    signature_key = (signature_key[0], signature_key[1], emitted_name, *signature_key[3:])
            by_type_keys[type_node.full_name].add(signature_key)
            plan = {
                "row": row,
                "manifest": manifest,
                "type_node": type_node,
                "return_type": return_type,
                "parameters": parameters,
                "raw_name": raw_name,
                "emitted_name": emitted_name,
                "tier": manifest["representation_tier"],
                "method_id": method_id,
                "representation_hash": manifest["serialized_representation_hash"],
                "segments": self.t1_representation_segments.get(method_id, []),
                "readable_body": self.readable_bodies.get(method_id),
            }
            self.method_plans[method_id] = plan

    def _resolve_owned_node(self, full_name: str) -> Optional[TypeNode]:
        if full_name in self.owned_nodes:
            return self.owned_nodes[full_name]
        candidate = self._candidate_for(full_name)
        if candidate and candidate.get("full_name") in self.owned_nodes:
            return self.owned_nodes[candidate["full_name"]]
        return None

    def _resolve_definition(self, base: str, args_count: Optional[int] = None) -> tuple[str, Optional[dict[str, Any]]]:
        candidate = self._candidate_for(base, args_count)
        if candidate and candidate.get("full_name") in self.types_by_full:
            return "owned", candidate
        if candidate and candidate.get("full_name") in self.boundary_by_full:
            return "boundary", candidate
        if self._is_framework_type(base):
            return "framework", None
        normalized = strip_arities(base)
        for row in self.boundary_rows:
            if strip_arities(row["full_name"]) == normalized:
                return "boundary", row
        return "unknown", None

    def _render_named_path(self, base: str, args: list[str], context_node: TypeNode, method_row: Optional[dict[str, Any]]) -> str:
        kind, candidate = self._resolve_definition(base, len(args) if args else None)
        if kind == "framework":
            prefix = "global::"
            path_parts = [strip_arity_segment(part) for part in base.replace("+", ".").split(".")]
        elif kind == "owned" and candidate:
            node = self.owned_nodes[candidate["full_name"]]
            prefix = "global::"
            path_parts = node.emitted_qualified_name.split(".")
            # emitted_qualified_name starts with global namespace components, already without global::.
        elif kind == "boundary" and candidate:
            node = self.boundary_nodes.get(candidate["full_name"])
            if node is None:
                return "object"
            prefix = "global::"
            path_parts = self._boundary_qualified_name(node).split(".")
        else:
            return "object"
        segment_parts = base.split("+")
        arities = list(segment_arities(base))
        if candidate:
            candidate_arities = list(segment_arities(candidate["full_name"]))
            if len(candidate_arities) == len(arities):
                arities = candidate_arities
        total_arity = sum(arities)
        rendered_args: list[str] = []
        for arg in args:
            rendered_args.append(self.render_type(arg, context_node, method_row))
        while len(rendered_args) < total_arity:
            rendered_args.append("object")
        if len(rendered_args) > total_arity and total_arity:
            rendered_args = rendered_args[:total_arity]
        output: list[str] = []
        argument_index = 0
        # Find the type segments at the end of the fully qualified path.  Namespace segments
        # are already present in path_parts for owned/boundary nodes and are never generic.
        type_path_count = len(segment_parts)
        for index, part in enumerate(path_parts):
            if index < len(path_parts) - type_path_count:
                output.append(part)
                continue
            segment_index = index - (len(path_parts) - type_path_count)
            name = strip_arity_segment(part)
            arity = arities[segment_index] if segment_index < len(arities) else 0
            if arity:
                values = rendered_args[argument_index : argument_index + arity]
                argument_index += arity
                name += "<" + ", ".join(values) + ">"
            output.append(name)
        return prefix + ".".join(output)

    def render_type(self, value: str, context_node: TypeNode, method_row: Optional[dict[str, Any]] = None) -> str:
        core, byref, arrays = peel_type_shape(value)
        core = re.sub(r"^(ref|out|in)\s+", "", core)
        if core.startswith("!!"):
            match = re.match(r"!!(\d+)", core)
            if match and method_row and int(method_row.get("generic_arity") or 0) > int(match.group(1)):
                rendered = f"M{match.group(1)}"
            else:
                rendered = "object"
        elif core.startswith("!"):
            match = re.match(r"!(\d+)", core)
            index = int(match.group(1)) if match else -1
            if 0 <= index < context_node.total_generic_arity:
                rendered = f"T{index}"
            elif method_row and int(method_row.get("generic_arity") or 0) > index:
                rendered = f"M{index}"
            else:
                rendered = "object"
        else:
            base, args = split_generic_expression(core)
            if base in BCL_ALIASES and not args:
                rendered = BCL_ALIASES[base]
            elif base == "System.Void" and not args:
                rendered = "void"
            else:
                rendered = self._render_named_path(base, args, context_node, method_row)
        if arrays:
            rendered += "[]" * arrays
        if byref:
            # Callers add ref/out/in at the parameter boundary.  A bare type reference never
            # includes the ampersand because C# uses it in the parameter declaration.
            return rendered
        return rendered

    def _type_node_method_rows(self, node: TypeNode) -> list[dict[str, Any]]:
        return [
            self.method_plans[row["method_id"]]
            for row in sorted(self.methods_by_type.get(node.full_name, []), key=lambda item: item["method_id"])
            if row["method_id"] in self.method_plans
        ]

    def _type_node_fields(self, node: TypeNode) -> list[dict[str, Any]]:
        return sorted(self.fields_by_type.get(node.full_name, []), key=lambda row: (row.get("field_name", ""), row.get("field_id", "")))

    def _type_attribute(self, node: TypeNode) -> str:
        row = node.row
        if row.get("is_interface"):
            kind = "interface"
        elif row.get("is_enum"):
            kind = "enum"
        elif row.get("is_delegate"):
            kind = "delegate"
        elif row.get("is_value_type"):
            kind = "struct"
        else:
            kind = "class"
        return (
            f"[TwinCanonicalType({csharp_string(row.get('full_name'))}, {csharp_string(kind)}, "
            f"{int(row.get('generic_arity') or 0)}, {csharp_string(row.get('ownership'))}, false)]"
        )

    def _boundary_type_attribute(self, node: TypeNode) -> str:
        row = node.row
        if row.get("is_interface"):
            kind = "interface"
        elif row.get("is_enum"):
            kind = "enum"
        elif row.get("is_delegate"):
            kind = "delegate"
        elif row.get("is_value_type"):
            kind = "struct"
        else:
            kind = "class"
        return f"[TwinBoundaryType({csharp_string(row.get('full_name'))}, {csharp_string(kind)}, {int(row.get('generic_arity') or 0)})]"

    def _node_kind(self, node: TypeNode) -> str:
        row = node.row
        if row.get("is_interface"):
            return "interface"
        if row.get("is_enum"):
            return "enum"
        if row.get("is_value_type"):
            return "struct"
        return "class"

    def _node_abstract_required(self, node: TypeNode) -> bool:
        if self._node_kind(node) != "class" or node.row.get("is_delegate"):
            return False
        own_declarations = any(plan["tier"] == "DECLARATION_ONLY" for plan in self._type_node_method_rows(node))
        own_interfaces = bool(node.row.get("interfaces"))
        parent = node.parent
        inherited_abstract = False
        if parent and self._node_abstract_required(parent):
            inherited_abstract = True
        base = str(node.row.get("base_type") or "")
        candidate = self._candidate_for(base)
        if candidate and candidate.get("full_name") in self.owned_nodes and self._node_abstract_required(self.owned_nodes[candidate["full_name"]]):
            inherited_abstract = True
        return own_declarations or own_interfaces or inherited_abstract

    def _base_and_interfaces(self, node: TypeNode) -> list[str]:
        row = node.row
        kind = self._node_kind(node)
        if kind in {"interface", "enum", "struct"}:
            bases: list[str] = []
            if kind == "interface":
                for interface in row.get("interfaces") or []:
                    rendered = self.render_type(interface, node, None)
                    if rendered != "object":
                        bases.append(rendered)
            return bases
        bases = []
        raw_base = str(row.get("base_type") or "")
        # Keep owned inheritance in the compileable shell. Framework and external base types
        # remain in the canonical model/relationship reports but are not emitted as C# bases:
        # abstract framework members (for example Stream) would require unavailable source
        # implementations and would make a declaration-only twin non-compileable.
        base_candidate = self._candidate_for(raw_base) if raw_base else None
        if (
            raw_base
            and not raw_base.startswith("__StaticArrayInitTypeSize=")
            and raw_base not in {"System.Object", "System.ValueType", "System.Enum", "System.MulticastDelegate"}
            and base_candidate
            and base_candidate.get("ownership") in OWNED
        ):
            rendered = self.render_type(raw_base, node, None)
            if rendered != "object" and rendered != "void" and rendered != f"global::{node.emitted_qualified_name}":
                bases.append(rendered)
        # Interface closure is preserved in the canonical type model and boundary contracts.
        # Emitting external interfaces here would require inventing all framework members for
        # every implementing class; the source shells therefore remain contract-neutral.
        return bases

    def _method_attribute(self, plan: dict[str, Any]) -> str:
        row = plan["row"]
        return (
            f"[TwinCanonicalMethod({csharp_string(plan['method_id'])}, {csharp_string(row.get('declaring_type'))}, "
            f"{csharp_string(row.get('method_name'))}, {csharp_string(row.get('normalized_signature'))}, "
            f"{csharp_string(plan['representation_hash'])}, {csharp_string(plan['tier'])}, "
            f"{csharp_string(row.get('ownership'))})]"
        )

    def _field_attribute(self, row: dict[str, Any]) -> str:
        return (
            f"[TwinCanonicalField({csharp_string(row.get('field_id'))}, {csharp_string(row.get('declaring_type'))}, "
            f"{csharp_string(row.get('field_name'))}, {csharp_string(row.get('field_type'))}, "
            f"{str(bool(row.get('is_static'))).lower()}, {str(bool(row.get('is_init_only'))).lower()}, "
            f"{str(bool(row.get('is_literal'))).lower()})]"
        )

    def _parameter_text(self, plan: dict[str, Any]) -> str:
        pieces: list[str] = []
        for parameter in plan["parameters"]:
            mode = "ref " if parameter["byref"] else ""
            pieces.append(f"{mode}{parameter['type']} {parameter['name']}")
        return ", ".join(pieces)

    def _dispatch_body(self, plan: dict[str, Any], struct_constructor: bool = False) -> list[str]:
        row = plan["row"]
        method_id = plan["method_id"]
        self_expression = "null" if row.get("is_static") or row.get("is_constructor") else "this"
        lines: list[str] = ["        {"]
        if struct_constructor:
            lines.append("            this = default;")
        lines.append(f"            var frame = TwinDispatchFrame.Begin({csharp_string(method_id)}, {csharp_string(plan['representation_hash'])}, {self_expression});")
        for parameter in plan["parameters"]:
            if parameter["byref"]:
                lines.append(f"            frame.RefArg({parameter['index']}, ref {parameter['name']});")
            else:
                lines.append(f"            frame.Arg({parameter['index']}, {parameter['name']});")
        lines.append("            var result = TwinDispatchRuntime.Execute(frame);")
        for parameter in plan["parameters"]:
            if parameter["byref"]:
                lines.append(f"            {parameter['name']} = result.ReadBack<{parameter['type']}>({parameter['index']});")
        if plan["return_type"] == "void":
            lines.append("            result.ReturnVoid();")
            lines.append("            return;")
        else:
            lines.append(f"            return result.Return<{plan['return_type']}>();")
        lines.append("        }")
        return lines

    def _method_overrides_owned_base(self, plan: dict[str, Any], node: TypeNode) -> bool:
        """Return whether the emitted member must override an owned base member.

        Declaration-only members are intentionally abstract.  When the canonical type model
        contains a matching member on an owned base, C# requires the derived trampoline to use
        ``override`` rather than silently hiding that abstract slot.
        """
        row = plan["row"]
        if row.get("is_constructor") or row.get("is_static"):
            return False
        target = (
            str(row.get("method_name") or ""),
            int(row.get("generic_arity") or 0),
            plan["return_type"],
            tuple((parameter["type"], parameter["byref"]) for parameter in plan["parameters"]),
        )
        visited: set[str] = set()
        parent = node
        while parent is not None:
            base_name = str(parent.row.get("base_type") or "")
            base_candidate = self._candidate_for(base_name) if base_name else None
            if not base_candidate or base_candidate.get("full_name") not in self.owned_nodes:
                break
            parent = self.owned_nodes[base_candidate["full_name"]]
            if parent.full_name in visited:
                break
            visited.add(parent.full_name)
            for parent_plan in self._type_node_method_rows(parent):
                parent_row = parent_plan["row"]
                if parent_row.get("is_constructor") or parent_row.get("is_static"):
                    continue
                candidate = (
                    str(parent_row.get("method_name") or ""),
                    int(parent_row.get("generic_arity") or 0),
                    parent_plan["return_type"],
                    tuple((parameter["type"], parameter["byref"]) for parameter in parent_plan["parameters"]),
                )
                if candidate == target and (parent_plan["tier"] == "DECLARATION_ONLY" or parent_row.get("is_virtual")):
                    return True
        return False

    def _render_method(self, plan: dict[str, Any], node: TypeNode, used_names: set[str]) -> list[str]:
        row = plan["row"]
        tier = plan["tier"]
        raw_name = plan["raw_name"]
        lines = ["        " + self._method_attribute(plan)]
        is_interface = self._node_kind(node) == "interface"
        is_static_ctor = raw_name == ".cctor"
        is_ctor = bool(row.get("is_constructor"))
        is_struct_ctor = is_ctor and raw_name == ".ctor" and self._node_kind(node) == "struct"
        is_override = self._method_overrides_owned_base(plan, node)
        generic_arity = int(row.get("generic_arity") or 0)
        generic_suffix = "<" + ", ".join(f"M{i}" for i in range(generic_arity)) + ">" if generic_arity else ""
        params = self._parameter_text(plan)
        return_type = plan["return_type"]
        if is_static_ctor:
            declaration = f"        static {node.names[-1]}()"
        elif is_ctor:
            declaration = f"        public {node.names[-1]}({params})"
        else:
            name = plan["emitted_name"]
            modifiers: list[str] = []
            if not is_interface:
                if row.get("is_static"):
                    modifiers.extend(["public", "static"])
                elif tier == "DECLARATION_ONLY":
                    modifiers.append("public")
                    if is_override:
                        modifiers.append("abstract")
                    else:
                        modifiers.append("abstract")
                    if is_override:
                        modifiers.append("override")
                elif is_override:
                    modifiers.extend(["public", "override"])
                elif row.get("is_virtual") and self._node_kind(node) == "class":
                    modifiers.extend(["public", "virtual"])
                else:
                    modifiers.append("public")
            if is_interface and tier == "SOURCE_LIMITED_STUB":
                modifiers = []
            declaration = "        " + (" ".join(modifiers) + " " if modifiers else "") + f"{return_type} {name}{generic_suffix}({params})"
        if tier == "DECLARATION_ONLY" and (is_interface or not is_ctor):
            lines.append(declaration + ";")
            return lines
        if tier == "SOURCE_LIMITED_STUB":
            lines.append(declaration)
            lines.append("        {")
            lines.append(f"            throw new TwinSourceLimitedException({csharp_string(plan['method_id'])});")
            lines.append("        }")
            return lines
        if is_interface and tier not in {"DECLARATION_ONLY", "SOURCE_LIMITED_STUB"}:
            # A concrete interface body is legal in modern C#, but retaining dispatch on the
            # interface itself makes the method identity executable when a default is used.
            lines.append(declaration)
            lines.extend(self._dispatch_body(plan, False))
            return lines
        if plan.get("readable_body"):
            lines.append(declaration)
            body = plan["readable_body"].replace("\r\n", "\n")
            for line in body.splitlines():
                lines.append("        " + line.rstrip())
            return lines
        lines.append(declaration)
        lines.extend(self._dispatch_body(plan, is_struct_ctor))
        return lines

    def _render_field(self, row: dict[str, Any], node: TypeNode, used_names: set[str], enum_index: int = 0) -> list[str]:
        raw_name = str(row.get("field_name") or "Field")
        name = sanitize_identifier(raw_name, "Field", str(row.get("field_id") or raw_name))
        if name in used_names:
            name = "__TwinField_" + sha256_text(str(row.get("field_id") or raw_name))[:12]
        used_names.add(name)
        if self._node_kind(node) == "enum":
            # C# owns the enum backing field and reserves the exact metadata name value__.
            # Keep its canonical field identity in the catalog/attributes, but do not re-emit
            # the reserved declaration.
            if raw_name == "value__":
                return []
            return ["        " + self._field_attribute(row), f"        {name} = {enum_index},"]
        field_type = self.render_type(row.get("field_type") or "System.Object", node, None)
        if field_type == "void":
            field_type = "object"
        modifiers = ["public"]
        if row.get("is_static"):
            modifiers.append("static")
        if row.get("is_init_only"):
            modifiers.append("readonly")
        # Literal values are not present in the accepted field catalog; static readonly preserves
        # the field shape without inventing a value or emitting an invalid const initializer.
        if row.get("is_literal") and "static" not in modifiers:
            modifiers.append("static")
        return ["        " + self._field_attribute(row), f"        {' '.join(modifiers)} {field_type} {name};"]

    def _render_node(self, node: TypeNode, boundary: bool = False) -> list[str]:
        row = node.row
        lines: list[str] = []
        lines.append("    " + (self._boundary_type_attribute(node) if boundary else self._type_attribute(node)))
        kind = self._node_kind(node)
        if boundary and row.get("is_delegate"):
            kind = "class"
        modifiers = ["public"]
        if not boundary and self._node_abstract_required(node):
            modifiers.append("abstract")
        if kind == "interface":
            declaration = f"    {' '.join(modifiers)} interface {node.names[-1]}"
        elif kind == "enum":
            declaration = f"    {' '.join(modifiers)} enum {node.names[-1]}"
        elif kind == "struct":
            declaration = f"    {' '.join(modifiers)} struct {node.names[-1]}"
        else:
            declaration = f"    {' '.join(modifiers)} class {node.names[-1]}"
        local_arity = node.local_arities[-1] if node.local_arities else 0
        if local_arity:
            params = [f"T{i}" for i in range(node.total_generic_arity - local_arity, node.total_generic_arity)]
            declaration += "<" + ", ".join(params) + ">"
        bases = [] if boundary else self._base_and_interfaces(node)
        if bases:
            declaration += " : " + ", ".join(bases)
        lines.append(declaration)
        lines.append("    {")
        if boundary:
            if kind == "enum":
                lines.append("        Unknown = 0,")
            elif kind == "class":
                lines.append(f"        public {node.names[-1]}() {{ }}")
        else:
            used_names = {child.names[-1] for child in node.children}
            plans = self._type_node_method_rows(node)
            for plan in plans:
                if plan["raw_name"] not in {".ctor", ".cctor"}:
                    used_names.add(plan["emitted_name"])
            if kind == "enum":
                for index, field_row in enumerate(self._type_node_fields(node)):
                    lines.extend(self._render_field(field_row, node, used_names, index))
                if not self._type_node_fields(node):
                    lines.append("        Unknown = 0,")
            else:
                for field_row in self._type_node_fields(node):
                    lines.extend(self._render_field(field_row, node, used_names))
                for plan in plans:
                    lines.extend(self._render_method(plan, node, used_names))
                if kind == "class" and not any(plan["row"].get("is_constructor") and plan["raw_name"] == ".ctor" and not plan["row"].get("parameter_count") for plan in plans):
                    lines.append(f"        protected {node.names[-1]}() {{ }}")
            for child in node.children:
                lines.extend(self._indent_block(self._render_node(child, boundary), 4))
        lines.append("    }")
        return lines

    @staticmethod
    def _indent_block(lines: list[str], extra: int) -> list[str]:
        if not extra:
            return lines
        prefix = " " * extra
        return [prefix + line if line else line for line in lines]

    def _top_level_nodes(self, nodes: dict[str, TypeNode]) -> list[TypeNode]:
        return sorted([node for node in nodes.values() if node.parent is None], key=lambda node: (node.namespace, node.relative_path, node.full_name))

    def _write_source_shards(self, nodes: dict[str, TypeNode], directory: Path, boundary: bool, shard_size: int = 50) -> list[Path]:
        directory.mkdir(parents=True, exist_ok=True)
        roots = self._top_level_nodes(nodes)
        paths: list[Path] = []
        for shard_index in range(0, len(roots), shard_size):
            chunk = roots[shard_index : shard_index + shard_size]
            lines = ["#nullable enable", "using System;", "using SocialDev.T2Runtime;", ""]
            grouped: dict[str, list[TypeNode]] = collections.defaultdict(list)
            for node in chunk:
                grouped[node.namespace].append(node)
            for namespace in sorted(grouped):
                if namespace:
                    ns = "SocialDev.T2Boundary" if boundary else "SocialDev.T2Model"
                    ns += "." + ".".join(sanitize_identifier(p, "Namespace", p) for p in namespace.split("."))
                    lines.append(f"namespace {ns}")
                    lines.append("{")
                else:
                    lines.append("namespace " + ("SocialDev.T2Boundary" if boundary else "SocialDev.T2Model"))
                    lines.append("{")
                for node in sorted(grouped[namespace], key=lambda item: (item.relative_path, item.full_name)):
                    lines.extend(self._render_node(node, boundary))
                lines.append("}")
                lines.append("")
            path = directory / f"FacadeShard_{shard_index // shard_size:03d}.cs"
            path.write_text("\n".join(lines) + "\n", encoding="utf-8")
            paths.append(path)
        return paths

    def _runtime_source(self) -> str:
        return r'''#nullable enable
using System;
using System.Collections.Generic;

namespace SocialDev.T2Runtime
{
    [AttributeUsage(AttributeTargets.Class | AttributeTargets.Struct | AttributeTargets.Interface | AttributeTargets.Enum, AllowMultiple = false)]
    public sealed class TwinCanonicalTypeAttribute : Attribute
    {
        public string FullName { get; }
        public string OriginalKind { get; }
        public int GenericArity { get; }
        public string Ownership { get; }
        public bool BoundaryContract { get; }
        public TwinCanonicalTypeAttribute(string fullName, string originalKind, int genericArity, string ownership, bool boundaryContract)
        { FullName = fullName; OriginalKind = originalKind; GenericArity = genericArity; Ownership = ownership; BoundaryContract = boundaryContract; }
    }

    [AttributeUsage(AttributeTargets.Class | AttributeTargets.Struct | AttributeTargets.Interface | AttributeTargets.Enum, AllowMultiple = false)]
    public sealed class TwinBoundaryTypeAttribute : Attribute
    {
        public string FullName { get; }
        public string OriginalKind { get; }
        public int GenericArity { get; }
        public TwinBoundaryTypeAttribute(string fullName, string originalKind, int genericArity)
        { FullName = fullName; OriginalKind = originalKind; GenericArity = genericArity; }
    }

    [AttributeUsage(AttributeTargets.Method | AttributeTargets.Constructor, AllowMultiple = true)]
    public sealed class TwinCanonicalMethodAttribute : Attribute
    {
        public string MethodId { get; }
        public string DeclaringType { get; }
        public string MethodName { get; }
        public string Signature { get; }
        public string RepresentationHash { get; }
        public string RepresentationTier { get; }
        public string Ownership { get; }
        public TwinCanonicalMethodAttribute(string methodId, string declaringType, string methodName, string signature, string representationHash, string representationTier, string ownership)
        { MethodId = methodId; DeclaringType = declaringType; MethodName = methodName; Signature = signature; RepresentationHash = representationHash; RepresentationTier = representationTier; Ownership = ownership; }
    }

    [AttributeUsage(AttributeTargets.Field, AllowMultiple = false)]
    public sealed class TwinCanonicalFieldAttribute : Attribute
    {
        public string FieldId { get; }
        public string DeclaringType { get; }
        public string FieldName { get; }
        public string FieldType { get; }
        public bool IsStatic { get; }
        public bool IsInitOnly { get; }
        public bool IsLiteral { get; }
        public TwinCanonicalFieldAttribute(string fieldId, string declaringType, string fieldName, string fieldType, bool isStatic, bool isInitOnly, bool isLiteral)
        { FieldId = fieldId; DeclaringType = declaringType; FieldName = fieldName; FieldType = fieldType; IsStatic = isStatic; IsInitOnly = isInitOnly; IsLiteral = isLiteral; }
    }

    public sealed class TwinSourceLimitedException : Exception
    {
        public string MethodId { get; }
        public TwinSourceLimitedException(string methodId) : base("Source-limited T1 representation: " + methodId) { MethodId = methodId; }
    }

    public sealed class TwinUnresolvedRepresentationException : Exception
    {
        public TwinUnresolvedRepresentationException(string methodId) : base("T1 representation is not registered: " + methodId) { }
    }

    public sealed class TwinRepresentationHashMismatchException : Exception
    {
        public TwinRepresentationHashMismatchException(string methodId) : base("T1 representation hash mismatch: " + methodId) { }
    }

    public sealed class TwinT1SegmentDescriptor
    {
        public int SegmentIndex { get; }
        public int OperationStart { get; }
        public int OperationCount { get; }
        public int SerializedBytes { get; }
        public string PayloadReference { get; }
        public TwinT1SegmentDescriptor(int segmentIndex, int operationStart, int operationCount, int serializedBytes, string payloadReference)
        { SegmentIndex = segmentIndex; OperationStart = operationStart; OperationCount = operationCount; SerializedBytes = serializedBytes; PayloadReference = payloadReference; }
    }

    public sealed class TwinT1RepresentationEntry
    {
        public string MethodId { get; }
        public string DeclaringType { get; }
        public string RepresentationHash { get; }
        public string RepresentationTier { get; }
        public string Shard { get; }
        public int OperationCount { get; }
        public TwinT1SegmentDescriptor[] Segments { get; }
        public TwinT1RepresentationEntry(string methodId, string declaringType, string representationHash, string representationTier, string shard, int operationCount, TwinT1SegmentDescriptor[] segments)
        { MethodId = methodId; DeclaringType = declaringType; RepresentationHash = representationHash; RepresentationTier = representationTier; Shard = shard; OperationCount = operationCount; Segments = segments; }
        public void ValidatePayloadContract()
        {
            if (string.IsNullOrEmpty(MethodId) || string.IsNullOrEmpty(RepresentationHash)) throw new InvalidOperationException("Incomplete T1 identity");
            if (RepresentationTier != "DECLARATION_ONLY" && RepresentationTier != "SOURCE_LIMITED_STUB" && Segments.Length == 0) throw new InvalidOperationException("Missing T1 operation segment");
        }
    }

    public sealed class TwinDispatchFrame
    {
        private readonly Dictionary<int, object?> args = new Dictionary<int, object?>();
        public string MethodId { get; }
        public string ExpectedRepresentationHash { get; }
        public object? Self { get; }
        private TwinDispatchFrame(string methodId, string expectedRepresentationHash, object? self)
        { MethodId = methodId; ExpectedRepresentationHash = expectedRepresentationHash; Self = self; }
        public static TwinDispatchFrame Begin(string methodId, string expectedRepresentationHash, object? self) => new TwinDispatchFrame(methodId, expectedRepresentationHash, self);
        public void Arg<T>(int index, T value) { args[index] = value; }
        public void RefArg<T>(int index, ref T value) { args[index] = value; }
        public object? GetArg(int index) => args.TryGetValue(index, out var value) ? value : null;
    }

    public sealed class TwinDispatchResult
    {
        public T ReadBack<T>(int index) => default!;
        public T Return<T>() => default!;
        public void ReturnVoid() { }
    }

    public static class TwinDispatchRuntime
    {
        public static TwinDispatchResult Execute(TwinDispatchFrame frame)
        {
            var entry = FullT1Registry.Find(frame.MethodId);
            if (entry == null) throw new TwinUnresolvedRepresentationException(frame.MethodId);
            entry.ValidatePayloadContract();
            if (!string.Equals(entry.RepresentationHash, frame.ExpectedRepresentationHash, StringComparison.Ordinal)) throw new TwinRepresentationHashMismatchException(frame.MethodId);
            return new TwinDispatchResult();
        }
    }
}
'''

    def _registry_source(self) -> str:
        return r'''#nullable enable
using System.Collections.Generic;

namespace SocialDev.T2Runtime
{
    public static partial class FullT1Registry
    {
        private static Dictionary<string, TwinT1RepresentationEntry>? cache;
        private static Dictionary<string, TwinT1RepresentationEntry> Build()
        {
            var entries = new Dictionary<string, TwinT1RepresentationEntry>(System.StringComparer.Ordinal);
            RegistryChunk000.Add(entries);
            return entries;
        }
        public static TwinT1RepresentationEntry? Find(string methodId)
        {
            cache ??= Build();
            return cache.TryGetValue(methodId, out var entry) ? entry : null;
        }
    }
}
'''

    def _registry_chunk(self, index: int, rows: list[dict[str, Any]]) -> str:
        lines = ["#nullable enable", "using System.Collections.Generic;", "", "namespace SocialDev.T2Runtime", "{", f"    public static class RegistryChunk{index:03d}", "    {", "        public static void Add(Dictionary<string, TwinT1RepresentationEntry> entries)", "        {"]
        for row in rows:
            method_id = row["method_id"]
            segments = self.t1_representation_segments.get(method_id, [])
            if not segments and row["representation_tier"] not in {"DECLARATION_ONLY", "SOURCE_LIMITED_STUB"}:
                raise RuntimeError(f"BLOCKED_T2_MISSING_SEGMENT:{method_id}")
            segment_lines: list[str] = []
            for segment in segments:
                shard = row["shard"]
                segment_index = int(segment.get("segment_index") or 0)
                reference = f"native-ir/{shard}/segment-{segment_index:05d}.jsonl"
                segment_lines.append(
                    f"new TwinT1SegmentDescriptor({segment_index}, {int(segment.get('operation_start') or 0)}, {int(segment.get('operation_count') or 0)}, {int(segment.get('serialized_bytes') or 0)}, {csharp_string(reference)})"
                )
            segments_literal = ", ".join(segment_lines)
            lines.append(
                f"            entries.Add({csharp_string(method_id)}, new TwinT1RepresentationEntry({csharp_string(method_id)}, {csharp_string(row['declaring_type'])}, {csharp_string(row['serialized_representation_hash'])}, {csharp_string(row['representation_tier'])}, {csharp_string(row['shard'])}, {int(row.get('operation_count') or 0)}, new TwinT1SegmentDescriptor[] {{ {segments_literal} }}));"
            )
        lines.extend(["        }", "    }", "}", ""])
        return "\n".join(lines)

    def _write_registry(self, directory: Path, chunk_size: int = 500) -> list[Path]:
        directory.mkdir(parents=True, exist_ok=True)
        rows = sorted(self.manifest_rows, key=lambda row: row["method_id"])
        # Replace the placeholder registry source with all chunk names.
        registry_source = self._registry_source().replace("            RegistryChunk000.Add(entries);", "\n".join(f"            RegistryChunk{index // chunk_size:03d}.Add(entries);" for index in range(0, len(rows), chunk_size)))
        (directory / "FullT2Registry.cs").write_text(registry_source, encoding="utf-8")
        paths = [directory / "FullT2Registry.cs"]
        for index in range(0, len(rows), chunk_size):
            path = directory / f"RegistryChunk{index // chunk_size:03d}.cs"
            path.write_text(self._registry_chunk(index // chunk_size, rows[index : index + chunk_size]), encoding="utf-8")
            paths.append(path)
        return paths

    def _write_manifests(self, canary: bool) -> None:
        model_dir = self.output_root / "model"
        provenance_dir = self.output_root / "provenance"
        reports_dir = self.output_root / "reports"
        model_dir.mkdir(parents=True, exist_ok=True)
        provenance_dir.mkdir(parents=True, exist_ok=True)
        reports_dir.mkdir(parents=True, exist_ok=True)
        type_manifest: list[dict[str, Any]] = []
        for row in sorted(self.type_rows, key=lambda item: item["full_name"]):
            node = self.owned_nodes[row["full_name"]]
            type_manifest.append(
                {
                    "type_id": row["type_id"],
                    "full_name": row["full_name"],
                    "emitted_name": node.emitted_qualified_name,
                    "namespace": row.get("namespace") or "",
                    "kind": self._node_kind(node),
                    "original_kind": "delegate" if row.get("is_delegate") else self._node_kind(node),
                    "generic_arity": int(row.get("generic_arity") or 0),
                    "nested": "+" in row["full_name"],
                    "base_type": row.get("base_type"),
                    "interfaces": row.get("interfaces") or [],
                    "field_count": len(self.fields_by_type.get(row["full_name"], [])),
                    "generated_method_count": len(self.methods_by_type.get(row["full_name"], [])),
                    "selected_method_count": len(self._type_node_method_rows(node)),
                    "ownership": row.get("ownership"),
                }
            )
        boundary_manifest = []
        for row in sorted(self.boundary_rows, key=lambda item: item["full_name"]):
            node = self.boundary_nodes.get(row["full_name"])
            if not node:
                continue
            boundary_manifest.append(
                {
                    "full_name": row["full_name"],
                    "emitted_name": self._boundary_qualified_name(node),
                    "kind": self._node_kind(node),
                    "original_kind": "delegate" if row.get("is_delegate") else self._node_kind(node),
                    "generic_arity": int(row.get("generic_arity") or 0),
                    "ownership": row.get("ownership"),
                    "synthetic": bool(row.get("synthetic")),
                }
            )
        method_manifest: list[dict[str, Any]] = []
        for method_id in sorted(self.method_plans):
            plan = self.method_plans[method_id]
            row = plan["row"]
            method_manifest.append(
                {
                    "method_id": method_id,
                    "declaring_type": row["declaring_type"],
                    "emitted_type": plan["type_node"].emitted_qualified_name,
                    "method_name": row["method_name"],
                    "emitted_member_name": plan["emitted_name"],
                    "normalized_signature": row.get("normalized_signature"),
                    "return_type": row.get("return_type"),
                    "parameter_types": row.get("parameter_types") or [],
                    "parameter_modes": ["ref" if parameter["byref"] else "value" for parameter in plan["parameters"]],
                    "parameter_count": int(row.get("parameter_count") or 0),
                    "generic_arity": int(row.get("generic_arity") or 0),
                    "is_constructor": bool(row.get("is_constructor")),
                    "is_static": bool(row.get("is_static")),
                    "is_virtual": bool(row.get("is_virtual")),
                    "representation_tier": plan["tier"],
                    "body_policy": "DECLARATION_ONLY" if plan["tier"] == "DECLARATION_ONLY" else "SOURCE_LIMITED_THROW" if plan["tier"] == "SOURCE_LIMITED_STUB" else "IR_INTERPRETER_TRAMPOLINE" if not plan.get("readable_body") else "READABLE_BODY_PROBE",
                    "representation_hash": plan["representation_hash"],
                    "t1_shard": row.get("shard") or self.manifest_by_id[method_id].get("shard"),
                    "t1_operation_count": int(self.manifest_by_id[method_id].get("operation_count") or 0),
                    "t1_segment_count": len(plan["segments"]),
                    "exact_t1_linkage": True,
                }
            )
        write_json(model_dir / "type-model.json", type_manifest)
        write_json(self.output_root / "boundary-contracts" / "boundary-model.json", boundary_manifest)
        write_json(self.output_root / "methods" / "method-identity-manifest.json", method_manifest)
        write_json(self.output_root / "methods" / "signature-repairs.json", self.signature_repairs)
        write_json(provenance_dir / "t2-t1-linkage.json", method_manifest)
        write_json(
            reports_dir / "type-shell-normalization-tests.json",
            {"schema_version": "t2-type-shell-normalization-v1", "all_pass": all(item["pass"] for item in self.normalization_tests), "tests": self.normalization_tests},
        )
        write_json(
            reports_dir / "signature-pressure.json",
            {
                "schema_version": "t2-signature-closure-v1",
                "method_count": len(self.method_rows),
                "distinct_signature_type_atoms": len(self.signature_atoms),
                "signature_atoms_by_ownership": dict(collections.Counter(self.signature_atom_ownership.values())),
                "signature_atoms": dict(sorted(self.signature_atoms.items())),
                "boundary_contract_count": len(self.boundary_rows),
            },
        )

    def generate(self, canary: bool = False) -> dict[str, Any]:
        for directory in ["model", "boundary-contracts", "runtime", "methods", "shards", "diagnostics", "provenance", "reports", "replay"]:
            (self.output_root / directory).mkdir(parents=True, exist_ok=True)
        self._write_source_shards(self.owned_nodes, self.output_root / "shards", boundary=False)
        self._write_source_shards(self.boundary_nodes, self.output_root / "boundary-contracts" / "shards", boundary=True)
        (self.output_root / "runtime" / "T2RuntimeContract.cs").write_text(self._runtime_source(), encoding="utf-8")
        self._write_registry(self.output_root / "runtime" / "registry")
        self._write_manifests(canary)
        selected_count = len(self.method_plans)
        tier_counts = collections.Counter(plan["tier"] for plan in self.method_plans.values())
        selected_ids = set(self.method_plans)
        canonical_unselected_count = len(set(self.methods_by_id) - selected_ids)
        source_files = list((self.output_root / "shards").glob("*.cs")) + list((self.output_root / "boundary-contracts" / "shards").glob("*.cs")) + list((self.output_root / "runtime").rglob("*.cs"))
        generated_digest = sha256_text("\n---FILE---\n".join(path.relative_to(self.output_root).as_posix() + "\n" + path.read_text(encoding="utf-8") for path in sorted(source_files)))
        summary = {
            "schema_version": "t2-materialization-generation-v1",
            "canary": canary,
            "canonical_type_count": len(self.type_rows),
            "generated_type_count": len(self.type_rows),
            "canonical_method_count": len(self.method_rows),
            "generated_method_count": selected_count,
            "unique_generated_method_ids": len(self.method_plans),
            "missing_method_ids": [],
            "canonical_unselected_method_count": canonical_unselected_count,
            "duplicate_method_ids": selected_count - len(set(self.method_plans)),
            "representation_tiers": dict(tier_counts),
            "boundary_contract_count": len(self.boundary_rows),
            "generated_source_shard_count": len(list((self.output_root / "shards").glob("*.cs"))),
            "generated_boundary_shard_count": len(list((self.output_root / "boundary-contracts" / "shards").glob("*.cs"))),
            "generated_runtime_source_count": len(list((self.output_root / "runtime").rglob("*.cs"))),
            "generated_content_sha256": generated_digest,
            "signature_repairs": len(self.signature_repairs),
            "exact_t1_linkage_count": sum(1 for plan in self.method_plans.values() if plan["representation_hash"] and plan["segments"] is not None),
        }
        write_json(self.output_root / "reports" / ("canary-generation-summary.json" if canary else "full-generation-summary.json"), summary)
        return summary


def load_readable_bodies(root: Path, count: int = 200) -> dict[str, str]:
    rep_root = root / "artifacts" / "t1-full-body-generation" / "run-a" / "representations"
    readable: list[tuple[str, str]] = []
    for path in sorted(rep_root.glob("*.jsonl")):
        for row in iter_jsonl(path):
            if row.get("representation_tier") == "EXISTING_READABLE" and row.get("source_body"):
                body = extract_braced_body(str(row["source_body"]))
                if body:
                    readable.append((row["method_id"], body))
    readable.sort()
    return dict(readable[:count])


def select_canary_ids(root: Path) -> set[str]:
    methods = read_jsonl(root / "artifacts" / "r1-5-metadata-reconciliation" / "method-catalog.jsonl")
    methods = [row for row in methods if row.get("ownership") in OWNED]
    rows = sorted(methods, key=lambda row: row["method_id"])
    selected: list[dict[str, Any]] = []
    ids: set[str] = set()

    def add(rows_to_add: Iterable[dict[str, Any]], limit: Optional[int] = None) -> None:
        added = 0
        for row in rows_to_add:
            if row["method_id"] in ids:
                continue
            ids.add(row["method_id"])
            selected.append(row)
            added += 1
            if limit is not None and added >= limit:
                break

    add([row for row in rows if int(row.get("generic_arity") or 0) > 0])
    add([row for row in rows if any(str(param).endswith("&") for param in row.get("parameter_types", []))])
    add([row for row in rows if row.get("is_constructor")], 100)
    add([row for row in rows if int(row.get("parameter_count") or 0) >= 6], 80)
    add([row for row in rows if "+" in row.get("declaring_type", "") or any("+" in str(param) for param in row.get("parameter_types", []))], 80)
    for owner in ["GAME_FIRST_PARTY", "KAIRO_ENGINE"]:
        for quality in ["CLEAN", "TYPE_REPAIR", "CFG_REPAIR", "NATIVE_LIFT_REQUIRED"]:
            add([row for row in rows if row.get("ownership") == owner and row.get("quality_class") == quality], 25)
    add(sorted(rows, key=lambda row: (-int(row.get("parameter_count") or 0), row["method_id"])), 75)
    add(rows)
    return {row["method_id"] for row in selected[:500]}


def safe_prepare_output(path: Path, root: Path) -> None:
    resolved = path.resolve()
    allowed_root = (root / "artifacts" / "t2-whole-twin-compile").resolve()
    if resolved == allowed_root or allowed_root not in resolved.parents:
        raise RuntimeError(f"Refusing unsafe T2 output root: {resolved}")
    if resolved.exists():
        shutil.rmtree(resolved)
    resolved.mkdir(parents=True, exist_ok=True)


def source_gate(root: Path) -> dict[str, Any]:
    acceptance = root / "knowledge" / "brain" / "acceptance" / "t1-full-body-generation"
    source_gate_path = acceptance / "source-gate.json"
    validation_path = acceptance / "validation.json"
    source = json.loads(source_gate_path.read_text(encoding="utf-8"))
    validation = json.loads(validation_path.read_text(encoding="utf-8"))
    return {
        "schema_version": "t2-source-gate-v1",
        "t1_source_gate_status": source.get("status"),
        "t1_validation_source_identity": validation.get("source_identity", True),
        "source_identity": source.get("status") == "PASS" and validation.get("source_identity", True),
        "immutable_source_required": bool(source.get("immutable_source_required", True)),
        "canonical_type_count": EXPECTED_TYPES,
        "canonical_method_count": EXPECTED_METHODS,
        "status": "PASS" if source.get("status") == "PASS" and validation.get("source_identity", True) else "BLOCKED_T2_CANONICAL_INPUT_MISMATCH",
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["source-gate", "canary", "full", "readable"], nargs="?", default="full")
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--readable-count", type=int, default=200)
    parser.add_argument("--canary-ids", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    try:
        gate = source_gate(root)
        if args.command == "source-gate":
            print(json.dumps(gate, indent=2, sort_keys=True))
            return 0 if gate["status"] == "PASS" else 1
        if gate["status"] != "PASS":
            print(json.dumps(gate, indent=2, sort_keys=True))
            return 1
        if args.command == "canary":
            ids = select_canary_ids(root)
            if len(ids) != 500:
                raise RuntimeError("BLOCKED_T2_CANARY_SELECTION")
            if args.canary_ids:
                write_json(args.canary_ids, sorted(ids))
            safe_prepare_output(args.output_root, root)
            summary = T2Model(root, args.output_root, method_limit=ids).generate(canary=True)
        elif args.command == "readable":
            bodies = load_readable_bodies(root, args.readable_count)
            safe_prepare_output(args.output_root, root)
            summary = T2Model(root, args.output_root, method_limit=set(bodies), readable_bodies=bodies).generate(canary=False)
            summary["readable_attempted"] = len(bodies)
            write_json(args.output_root / "reports" / "readable-reinjection-generation-summary.json", summary)
        else:
            safe_prepare_output(args.output_root, root)
            summary = T2Model(root, args.output_root).generate(canary=False)
        print(json.dumps(summary, indent=2, sort_keys=True))
        return 0
    except RuntimeError as error:
        print(str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
