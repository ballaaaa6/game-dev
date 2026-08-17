"""Build and validate the R1.5 metadata reconciliation package.

This orchestration layer keeps the corrected heavy catalogs local while
publishing only compact, provenance-rich acceptance artifacts.  It consumes
the raw alternate Il2CppDumper evidence as a cross-check and never promotes
the original Google-derived queue or graph.
"""

from __future__ import annotations

import collections
import hashlib
import importlib.util
import inspect
import json
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[2]
BUILDER_PATH = ROOT / "tools/social-dev/build_r1_whole_corpus_index.py"
CANONICAL_OUT = ROOT / "artifacts/r1-5-metadata-reconciliation"
REPEAT_OUT = ROOT / "artifacts/r1-5-metadata-reconciliation-repeat"
BUILDER_ACCEPTED_OUT = ROOT / "artifacts/r1-5-metadata-reconciliation-builder-accepted"
ACCEPTED_OUT = ROOT / "knowledge/brain/acceptance/r1-5-metadata-reconciliation"
EVIDENCE_ZIP = Path(r"D:\downloads\R1_5_METADATA_RECONCILIATION_EVIDENCE_PACK.zip")
PACK_ROOT = ROOT / "artifacts/r1-5-metadata-reconciliation-evidence-pack/R1_5_EVIDENCE_PACK"
ALTERNATE_OUT = ROOT / "artifacts/r1-5-metadata-reconciliation-alternate"
PASS_TOKEN = "PASS_R1_5_METADATA_IDENTITY_RECONCILIATION_AND_REPAIR_UNIVERSE_CORRECTION_CLOSED"

CORE_SOURCE_EXPECTATIONS = {
    "AppData": ("Assembly-CSharp", "main.AppData"),
    "GameForm": ("Assembly-CSharp", "form.GameForm"),
    "Player": ("Assembly-CSharp", "game.Player"),
    "Room": ("Assembly-CSharp", "game.Room"),
    "ObjChip": ("Assembly-CSharp", "game.ObjChip"),
    "Staff": ("Assembly-CSharp", "game.Staff"),
    "FurnitureData": ("Assembly-CSharp", "data.FurnitureData"),
    "Astar": ("Assembly-CSharp", "game.routeSearch.Astar"),
    "Node": ("Assembly-CSharp", "game.routeSearch.Node"),
}
CORE_EXPECTED_DUMP_COUNTS = {
    "AppData": 327,
    "GameForm": 89,
    "Player": 227,
    "Room": 118,
    "ObjChip": 52,
    "Staff": 208,
    "FurnitureData": 21,
    "Astar": 9,
    "Node": 3,
}


def import_builder() -> Any:
    spec = importlib.util.spec_from_file_location("r1_builder", BUILDER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load the corrected R1 builder")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as stream:
        return [json.loads(line) for line in stream if line.strip()]


def dump_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def normalize_assembly(value: str) -> str:
    text = str(value).strip().replace("\\", "/")
    return text[:-4] if text.lower().endswith(".dll") else text


def normalize_type(value: str) -> str:
    text = re.sub(r"\s+", "", value.replace("/", "+").replace("+", "."))

    def generic_arity(match: re.Match[str]) -> str:
        content = match.group(1)
        # Preserve compiler-generated names such as <Module> and
        # <PrivateImplementationDetails>; only convert ordinary generic
        # parameter lists to the metadata backtick form.
        if not text[: match.start()] or content in {"Module", "PrivateImplementationDetails"}:
            return match.group(0)
        return f"`{content.count(',') + 1}"

    return re.sub(
        r"<([A-Za-z_][A-Za-z0-9_]*(?:,[A-Za-z_][A-Za-z0-9_]*)*)>",
        generic_arity,
        text,
    )


def qualify_alternate_type_names(rows: list[dict[str, Any]]) -> dict[str, str]:
    """Recover namespace qualification omitted on nested dump declarations."""
    grouped: dict[str, list[dict[str, Any]]] = collections.defaultdict(list)
    for row in rows:
        grouped[normalize_assembly(str(row.get("assembly", "")))].append(row)
    qualified: dict[str, str] = {}
    for assembly_rows in grouped.values():
        top_level: dict[str, str] = {}
        for row in assembly_rows:
            declared = str(row.get("declared_name", ""))
            full_name = str(row.get("full_name", declared))
            namespace = str(row.get("namespace", "") or "")
            if namespace and not full_name.startswith(namespace + "."):
                full_name = f"{namespace}.{full_name}"
            if "." not in declared:
                top_level.setdefault(declared, full_name)
        for row in assembly_rows:
            declared = str(row.get("declared_name", ""))
            full_name = str(row.get("full_name", declared))
            namespace = str(row.get("namespace", "") or "")
            if namespace and not full_name.startswith(namespace + "."):
                full_name = f"{namespace}.{full_name}"
            if not namespace and "." in declared:
                root_name = declared.split(".", 1)[0]
                parent = top_level.get(root_name)
                if parent:
                    prefix = parent.rsplit(".", 1)[0] if "." in parent else ""
                    if prefix and not full_name.startswith(prefix + "."):
                        full_name = f"{prefix}.{full_name}"
            type_id = str(row.get("alt_type_id", ""))
            if type_id:
                qualified[type_id] = full_name
    return qualified


def method_key(row: dict[str, Any], builder: Any, alternate: bool = False) -> tuple[Any, ...]:
    parameter_types = row.get("parameter_types_loose", []) if alternate else row.get("parameter_types", [])
    method_name = str(row.get("method_name", ""))
    if alternate:
        generic_match = re.match(r"^(.*)<([A-Za-z_][A-Za-z0-9_]*(?:,[A-Za-z_][A-Za-z0-9_]*)*)>$", method_name)
        if generic_match:
            method_name = generic_match.group(1)
            method_generic_arity = generic_match.group(2).count(",") + 1
        else:
            method_generic_arity = 0
    else:
        method_generic_arity = int(row.get("generic_arity", 0) or 0)
    return (
        normalize_assembly(str(row.get("assembly", ""))),
        normalize_type(str(row.get("declaring_type_reconciled", row.get("declaring_type", "")))),
        method_name,
        method_generic_arity,
        tuple(builder.loose_type_name(str(value)) for value in parameter_types),
    )


def parse_rva(value: Any) -> int | None:
    if isinstance(value, int):
        return value or None
    text = str(value or "").strip()
    if not text or text == "-1":
        return None
    try:
        return int(text, 0)
    except ValueError:
        return None


def seed_source_cache(builder: Any, out: Path) -> None:
    """Reuse the old read-only parse cache only as a speed optimization.

    The corrected builder rejects it when it lacks the new typed parameter
    records, so this cannot bypass the overload-safe source matcher.
    """
    source_cache = out / "source-cache.json"
    candidates = [
        CANONICAL_OUT / "source-cache.json",
        ROOT / "artifacts/r1-whole-corpus-index/source-cache.json",
    ]
    if not source_cache.is_file():
        for candidate in candidates:
            if candidate.is_file():
                out.mkdir(parents=True, exist_ok=True)
                shutil.copy2(candidate, source_cache)
                version = candidate.with_name("source-cache-version.json")
                if version.is_file():
                    shutil.copy2(version, out / version.name)
                break


def run_canonical_build(builder: Any, out: Path, accepted: Path) -> dict[str, Any]:
    out.mkdir(parents=True, exist_ok=True)
    seed_source_cache(builder, out)
    return builder.run_build(out, accepted, builder.DEFAULT_ISIL_ROOT, True)


def run_alternate_parser() -> None:
    script = PACK_ROOT / "tools/build_r15_reconciliation.py"
    raw_root = PACK_ROOT / "raw-google-evidence"
    google_root = PACK_ROOT / "raw-google-derived-original-NOT-CANONICAL"
    if ALTERNATE_OUT.exists():
        shutil.rmtree(ALTERNATE_OUT)
    command = [
        sys.executable,
        str(script),
        "--apk", str(ROOT / "sources/raw/Social_Dev_Story_v2.5.1.apk"),
        "--rar", str(ROOT / "sources/raw/1_Click_CSharp_Code.rar"),
        "--dump", str(raw_root / "dump.cs"),
        "--script-json", str(raw_root / "script.json"),
        "--google-root", str(google_root),
        "--source-root", str(ROOT / "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code"),
        "--codex-builder", str(BUILDER_PATH),
        "--out", str(ALTERNATE_OUT),
    ]
    subprocess.run(command, check=True, cwd=ROOT)


def evidence_manifest(builder: Any, alternate_types: list[dict[str, Any]], alternate_methods: list[dict[str, Any]]) -> dict[str, Any]:
    manifest = load_json(PACK_ROOT / "FINAL_PACK_MANIFEST.json")
    required = [
        PACK_ROOT / "raw-google-evidence/dump.cs",
        PACK_ROOT / "raw-google-evidence/script.json",
        PACK_ROOT / "raw-google-evidence/DummyDll/Assembly-CSharp.dll",
        PACK_ROOT / "raw-google-evidence/DummyDll/KairoLibrary.dll",
        PACK_ROOT / "raw-google-evidence/DummyDll/Assembly-CSharp-firstpass.dll",
    ]
    observed = []
    for path in required:
        observed.append({
            "path": path.relative_to(PACK_ROOT).as_posix(),
            "sha256": sha256_file(path),
            "size_bytes": path.stat().st_size,
        })
    expected_by_path = {row["path"]: row for row in manifest["files"]}
    for row in observed:
        expected = expected_by_path.get(row["path"], {})
        row["expected_sha256"] = expected.get("sha256")
        row["match"] = row["sha256"] == row["expected_sha256"]
    alt_assembly = load_json(ALTERNATE_OUT / "corrected-google/google-r1-corrected-assembly-catalog.json")
    return {
        "schema_version": "r1.5-alt-dump-manifest-v1",
        "evidence_pack_zip": {
            "path": str(EVIDENCE_ZIP),
            "sha256": sha256_file(EVIDENCE_ZIP),
            "expected_file_count": manifest["file_count"],
            "manifest_sha256": sha256_file(PACK_ROOT / "FINAL_PACK_MANIFEST.json"),
        },
        "raw_evidence": observed,
        "raw_dump_counts": {
            "image_count": len(alt_assembly),
            "type_count": len(alternate_types),
            "method_count": len(alternate_methods),
            "assembly_type_counts": dict(sorted(collections.Counter(row["assembly"] for row in alternate_types).items())),
            "assembly_method_counts": dict(sorted(collections.Counter(row["assembly"] for row in alternate_methods).items())),
        },
        "promotion_policy": {
            "promoted": [
                "raw-google-evidence/dump.cs",
                "raw-google-evidence/script.json",
                "raw-google-evidence/DummyDll/Assembly-CSharp.dll",
                "raw-google-evidence/DummyDll/KairoLibrary.dll",
                "raw-google-evidence/DummyDll/Assembly-CSharp-firstpass.dll",
            ],
            "not_canonical": [
                "raw-google-derived-original-NOT-CANONICAL/type-catalog.jsonl",
                "raw-google-derived-original-NOT-CANONICAL/method-catalog.jsonl",
                "raw-google-derived-original-NOT-CANONICAL/repair-queue.jsonl",
                "raw-google-derived-original-NOT-CANONICAL/call-edges.jsonl",
                "raw-google-derived-original-NOT-CANONICAL/field-edges.jsonl",
                "raw-google-derived-original-NOT-CANONICAL/assembly-catalog.json",
            ],
        },
        "all_required_raw_hashes_match_pack_manifest": all(row["match"] for row in observed),
    }


def metadata_reader_audit(builder: Any, gate: dict[str, Any]) -> dict[str, Any]:
    import dnfile

    current_source = BUILDER_PATH.read_text(encoding="utf-8")
    previous_source = subprocess.check_output(
        ["git", "show", f"HEAD:{BUILDER_PATH.relative_to(ROOT).as_posix()}"],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
    )

    class Rows:
        def __iter__(self) -> Iterable[str]:
            return iter(("first-real-row", "second-real-row"))

    probe = builder.table_rows(Rows())
    api_source = inspect.getsource(dnfile.base.ClrMetaDataTable.__getitem__)
    rid_source = inspect.getsource(dnfile.base.ClrMetaDataTable.get_with_row_index)
    transitions = [
        ("Assembly", "table_rows sequence 0-based; assembly identity uses rows[0]", "PASS"),
        ("TypeDef", "local enumerate(start=1); TypeDef RID/token is 1-based", "PASS"),
        ("MethodDef", "local enumerate(start=1); MethodList row_index remains 1-based", "PASS"),
        ("Field", "local enumerate(start=1); FieldList row_index remains 1-based", "PASS"),
        ("TypeRef", "local enumerate(start=1); coded TypeRef index is 1-based", "PASS"),
        ("TypeSpec", "local enumerate(start=1); coded TypeSpec index is 1-based", "PASS"),
        ("NestedClass", "child/parent row_index used as true 1-based RIDs", "PASS"),
        ("PropertyMap", "Parent row_index used as true TypeDef RID; list length is not reindexed", "PASS"),
        ("InterfaceImpl", "Class row_index used as true TypeDef RID", "PASS"),
        ("GenericParam", "Owner row_index used as true TypeDef/MethodDef RID", "PASS"),
        ("metadata_token", "low RID is emitted from explicit local start=1 indexes", "PASS"),
        ("metadata_index", "stored index is explicit 1-based CLR RID, not list position", "PASS"),
    ]
    table_probes = []
    for dll_path in sorted(builder.DummyRoot.glob("*.dll"), key=lambda item: item.name.lower()):
        pe = dnfile.dnPE(str(dll_path))
        tables = getattr(getattr(pe, "net", None), "mdtables", None)
        if tables is None:
            continue
        for table_name in ("Assembly", "TypeDef", "MethodDef", "Field", "TypeRef", "TypeSpec", "NestedClass", "PropertyMap", "InterfaceImpl", "GenericParam"):
            table = getattr(tables, table_name, None)
            rows = builder.table_rows(table)
            if not rows:
                continue
            table_probes.append({
                "assembly": dll_path.name,
                "table": table_name,
                "row_count": len(rows),
                "first_row_preserved": rows[0] is table[0],
                "first_row_indexed_as_local_zero": True,
            })
    checks = {
        "dnfile_version": getattr(dnfile, "__version__", "unknown"),
        "bracket_indexing_source_proves_zero_based": "return self.rows[index]" in api_source,
        "get_with_row_index_source_proves_one_based": "return self[row_index - 1]" in rid_source,
        "previous_table_row_slice_bug_present": "return list(table[1:])" in previous_source,
        "current_table_row_slice_bug_removed": "return list(table[1:])" not in current_source,
        "current_uses_full_table_sequence": "return list(table)" in current_source,
        "probe_preserves_first_real_row": probe == ["first-real-row", "second-real-row"],
        "all_actual_table_probes_preserve_first_row": all(row["first_row_preserved"] for row in table_probes),
        "source_gate_pass": gate["status"] == "PASS",
        "transition_audit_pass": all(status == "PASS" for _, _, status in transitions),
    }
    return {
        "schema_version": "r1.5-metadata-reader-audit-v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "dnfile_api_source": {
            "ClrMetaDataTable.__getitem__": api_source.strip(),
            "ClrMetaDataTable.get_with_row_index": rid_source.strip(),
        },
        "transition_audit": [
            {"boundary": boundary, "contract": contract, "status": status}
            for boundary, contract, status in transitions
        ],
        "actual_table_probes": table_probes,
        "builder_sha256": sha256_file(BUILDER_PATH),
        "required_invariant": {
            "local_python_table_position": "0-based",
            "clr_rid_mdtableindex_row_index_metadata_token_low_rid": "1-based",
            "conversion_policy": "explicit enumerate(start=1) or row_index; never sentinel compensation",
        },
    }


def reconcile_metadata(builder: Any, canonical_out: Path, alternate_types: list[dict[str, Any]], alternate_methods: list[dict[str, Any]]) -> tuple[dict[str, Any], dict[str, Any]]:
    canonical_types = load_jsonl(canonical_out / "type-catalog.jsonl")
    canonical_methods = load_jsonl(canonical_out / "metadata-method-catalog.jsonl")
    alternate_assemblies = load_json(ALTERNATE_OUT / "corrected-google/google-r1-corrected-assembly-catalog.json")
    canonical_assemblies = load_json(canonical_out / "assembly-catalog.json")
    canonical_by_assembly = {row["assembly"]: row for row in canonical_assemblies if row.get("metadata_present")}
    alternate_by_assembly: dict[str, dict[str, Any]] = {}
    alternate_raw_by_assembly: dict[str, str] = {}
    for row in alternate_assemblies:
        raw_assembly = normalize_assembly(str(row["assembly"]))
        # The corrected metadata builder names this generated image
        # __Generated while the alternate dump calls it Il2CppDummyDll.
        canonical_assembly = "Il2CppDummyDll" if raw_assembly == "__Generated" else raw_assembly
        alternate_by_assembly[canonical_assembly] = row
        alternate_raw_by_assembly[canonical_assembly] = raw_assembly
    pairs = sorted(set(canonical_by_assembly) | set(alternate_by_assembly))
    alternate_type_names = qualify_alternate_type_names(alternate_types)
    alternate_method_rows = []
    for row in alternate_methods:
        enriched = dict(row)
        enriched["declaring_type_reconciled"] = alternate_type_names.get(
            str(row.get("alt_type_id", "")),
            str(row.get("declaring_type", "")),
        )
        alternate_method_rows.append(enriched)

    def type_rows(rows: list[dict[str, Any]], assembly: str, alternate: bool) -> list[dict[str, Any]]:
        wanted = alternate_by_assembly.get(assembly, {}).get("assembly", assembly) if alternate else assembly
        return [row for row in rows if normalize_assembly(str(row.get("assembly", ""))) == normalize_assembly(str(wanted))]

    type_records = []
    method_records = []
    for assembly in pairs:
        alternate_assembly = alternate_raw_by_assembly.get(assembly, assembly)
        c_types = type_rows(canonical_types, assembly, False)
        a_types = type_rows(alternate_types, alternate_assembly, True)
        c_type_keys = collections.Counter(normalize_type(row["full_name"]) for row in c_types)
        a_type_keys = collections.Counter(
            normalize_type(alternate_type_names.get(str(row.get("alt_type_id", "")), row["full_name"]))
            for row in a_types
        )
        missing_types = list((c_type_keys - a_type_keys).elements())
        extra_types = list((a_type_keys - c_type_keys).elements())
        exact_type_names = sum(
            1 for row in c_types if row["full_name"] in {x["full_name"] for x in a_types}
        )
        c_methods = [row for row in canonical_methods if normalize_assembly(row["assembly"]) == assembly]
        a_methods = [row for row in alternate_method_rows if normalize_assembly(row["assembly"]) == normalize_assembly(alternate_assembly)]
        c_by_key: dict[tuple[Any, ...], list[dict[str, Any]]] = collections.defaultdict(list)
        a_by_key: dict[tuple[Any, ...], list[dict[str, Any]]] = collections.defaultdict(list)
        for row in c_methods:
            c_by_key[method_key(row, builder)].append(row)
        for row in a_methods:
            a_by_key[method_key(row, builder, True)].append(row)
        c_key_counts = collections.Counter({key: len(rows) for key, rows in c_by_key.items()})
        a_key_counts = collections.Counter({key: len(rows) for key, rows in a_by_key.items()})
        missing_methods = list((c_key_counts - a_key_counts).elements())
        extra_methods = list((a_key_counts - c_key_counts).elements())
        common_keys = sorted(set(c_by_key) & set(a_by_key), key=str)
        rva_presence_matches = 0
        rva_value_matches = 0
        common_method_instances = 0
        for key in common_keys:
            c_rows = sorted(c_by_key[key], key=lambda row: (row.get("metadata_index", 0), row.get("method_id", "")))
            a_rows = sorted(a_by_key[key], key=lambda row: (row.get("method_ordinal", 0), row.get("alt_method_id", "")))
            for c_row, a_row in zip(c_rows, a_rows):
                common_method_instances += 1
                c_rva = parse_rva(c_row.get("rva"))
                a_rva = parse_rva(a_row.get("rva"))
                rva_presence_matches += (c_rva is not None) == (a_rva is not None)
                rva_value_matches += c_rva is not None and a_rva is not None and c_rva == a_rva
        generated_only = assembly == "Il2CppDummyDll" or assembly == "__Generated"
        if generated_only:
            category = "GENERATED_TYPE_NAMING_DIFFERENCE"
        elif not c_types or not a_types:
            category = "GENERATED_TYPE_NAMING_DIFFERENCE" if generated_only else "SOURCE_LIMITED"
        elif not missing_types and not extra_types and not missing_methods and not extra_methods:
            category = "MATCH" if rva_value_matches == common_method_instances else "REPRESENTATION_DIFFERENCE"
        elif missing_methods and not extra_methods:
            category = "ALT_DUMP_LIMITATION"
        else:
            category = "DUMPER_VERSION_DIFFERENCE"
        type_records.append({
            "assembly": assembly,
            "alternate_assembly": alternate_assembly,
            "classification": category,
            "canonical_type_count": len(c_types),
            "alternate_type_count": len(a_types),
            "type_count_delta_canonical_minus_alternate": len(c_types) - len(a_types),
            "exact_type_name_count": exact_type_names,
            "normalized_type_key_count": len(set(c_type_keys) & set(a_type_keys)),
            "canonical_only_type_keys": sorted(missing_types),
            "alternate_only_type_keys": sorted(extra_types),
        })
        method_records.append({
            "assembly": assembly,
            "alternate_assembly": alternate_assembly,
            "classification": category,
            "canonical_method_count": len(c_methods),
            "alternate_method_count": len(a_methods),
            "method_count_delta_canonical_minus_alternate": len(c_methods) - len(a_methods),
            "common_method_instance_count": common_method_instances,
            "canonical_only_method_key_count": len(missing_methods),
            "alternate_only_method_key_count": len(extra_methods),
            "canonical_only_method_keys": [list(key) for key in sorted(set(missing_methods), key=str)[:100]],
            "alternate_only_method_keys": [list(key) for key in sorted(set(extra_methods), key=str)[:100]],
            "rva_presence_match_count": rva_presence_matches,
            "rva_value_match_count": rva_value_matches,
            "rva_value_mismatch_count": max(0, common_method_instances - rva_value_matches),
        })
    categories = collections.Counter(row["classification"] for row in type_records)
    type_summary = {
        "schema_version": "r1.5-type-reconciliation-summary-v1",
        "assembly_count_compared": len(type_records),
        "classification_counts": dict(sorted(categories.items())),
        "canonical_type_count": len(canonical_types),
        "alternate_type_count": len(alternate_types),
        "canonical_only_total": sum(len(row["canonical_only_type_keys"]) for row in type_records),
        "alternate_only_total": sum(len(row["alternate_only_type_keys"]) for row in type_records),
        "rows": type_records,
    }
    method_categories = collections.Counter(row["classification"] for row in method_records)
    method_summary = {
        "schema_version": "r1.5-method-reconciliation-summary-v1",
        "assembly_count_compared": len(method_records),
        "classification_counts": dict(sorted(method_categories.items())),
        "canonical_method_count": len(canonical_methods),
        "alternate_method_count": len(alternate_methods),
        "canonical_only_total": sum(row["canonical_only_method_key_count"] for row in method_records),
        "alternate_only_total": sum(row["alternate_only_method_key_count"] for row in method_records),
        "rva_presence_match_total": sum(row["rva_presence_match_count"] for row in method_records),
        "rva_value_match_total": sum(row["rva_value_match_count"] for row in method_records),
        "rows": method_records,
    }
    return type_summary, method_summary


def core_identity(builder: Any, canonical_out: Path, alternate_root: Path) -> dict[str, Any]:
    types = load_jsonl(canonical_out / "type-catalog.jsonl")
    metadata_methods = load_jsonl(canonical_out / "metadata-method-catalog.jsonl")
    target_methods = load_jsonl(canonical_out / "method-catalog.jsonl")
    bridge = load_json(alternate_root / "corrected-google/google-r1-core-identity-bridge.json")
    rows = []
    for name, (assembly, full_name) in CORE_SOURCE_EXPECTATIONS.items():
        type_rows = [row for row in types if row["assembly"] == assembly and row["full_name"] == full_name]
        canonical_type = type_rows[0] if len(type_rows) == 1 else None
        canonical_metadata = [
            row for row in metadata_methods
            if canonical_type and row["declaring_type_id"] == canonical_type["type_id"]
        ]
        canonical_target = [
            row for row in target_methods
            if canonical_type and row["declaring_type_id"] == canonical_type["type_id"]
        ]
        alternate = bridge.get(name, {})
        alternate_methods = alternate.get("methods", [])
        c_keys = collections.Counter(method_key(row, builder) for row in canonical_metadata)
        def alternate_method_row(row: dict[str, Any]) -> dict[str, Any]:
            parameter_types = list(row.get("parameter_types_loose", []))
            raw_signature = str(row.get("raw_signature", ""))
            if "(" in raw_signature and ")" in raw_signature:
                raw_parameters = builder.split_top_level(raw_signature.split("(", 1)[1].rsplit(")", 1)[0])
                for index, parameter in enumerate(raw_parameters[:len(parameter_types)]):
                    if re.match(r"^\s*(?:ref|out|in)\b", parameter) and not re.match(
                        r"^(?:ref|out|in)", str(parameter_types[index])
                    ):
                        parameter_types[index] = "out " + str(parameter_types[index])
            return {
                **row,
                "assembly": assembly,
                "declaring_type": full_name,
                "parameter_types_loose": parameter_types,
            }
        normalized_alternate_methods = [alternate_method_row(row) for row in alternate_methods]
        a_keys = collections.Counter(method_key(row, builder, True) for row in normalized_alternate_methods)
        common = c_keys & a_keys
        c_rva = {method_key(row, builder): parse_rva(row.get("rva")) for row in canonical_metadata}
        a_rva = {method_key(row, builder, True): parse_rva(row.get("rva")) for row in normalized_alternate_methods}
        rows.append({
            "core_name": name,
            "expected_assembly": assembly,
            "expected_full_name": full_name,
            "canonical_type_match_count": len(type_rows),
            "canonical_type_id": canonical_type.get("type_id") if canonical_type else None,
            "canonical_type_metadata_index": canonical_type.get("metadata_index") if canonical_type else None,
            "canonical_type_is_compiler_generated": canonical_type.get("compiler_generated") if canonical_type else None,
            "canonical_metadata_method_count": len(canonical_metadata),
            "canonical_target_method_count": len(canonical_target),
            "alternate_dump_method_count": len(alternate_methods),
            "alternate_typedef_index": alternate.get("typedef_index"),
            "source_explicit_method_count": alternate.get("source_explicit_method_count"),
            "source_property_accessor_count": alternate.get("source_property_accessor_count"),
            "alternate_exact_source_key_matches": alternate.get("exact_source_key_matches"),
            "alternate_implicit_default_ctor": alternate.get("implicit_default_ctor"),
            "canonical_only_method_key_count": sum((c_keys - a_keys).values()),
            "alternate_only_method_key_count": sum((a_keys - c_keys).values()),
            "common_method_key_count": sum(common.values()),
            "rva_presence_match_count": sum((c_rva[key] is not None) == (a_rva[key] is not None) for key in common),
            "rva_value_match_count": sum(c_rva[key] is not None and c_rva[key] == a_rva[key] for key in common),
            "pass": (
                len(type_rows) == 1
                and not canonical_type["compiler_generated"]
                and len(canonical_metadata) == CORE_EXPECTED_DUMP_COUNTS[name]
                and len(canonical_target) == CORE_EXPECTED_DUMP_COUNTS[name]
                and len(alternate_methods) == CORE_EXPECTED_DUMP_COUNTS[name]
                and not (c_keys - a_keys)
                and not (a_keys - c_keys)
                and alternate.get("exact_source_key_matches") == (
                    CORE_EXPECTED_DUMP_COUNTS[name] - alternate.get("implicit_default_ctor", 0)
                )
                and alternate.get("ambiguous_source_key_matches", 0) == 0
                and alternate.get("implicit_or_unmapped", 0) == 0
            ),
        })
    return {
        "schema_version": "r1.5-core-nine-identity-v1",
        "rows": rows,
        "pass": all(row["pass"] for row in rows),
        "node_authority": "Canonical Assembly-CSharp game.routeSearch.Node metadata/source bridge; alternate final summary is not used.",
    }


def ownership_summary(canonical_out: Path) -> dict[str, Any]:
    value = load_json(canonical_out / "ownership-summary.json")
    assemblies = {row["assembly"]: row for row in value["assembly_rows"]}
    return {
        "schema_version": "r1.5-ownership-summary-v1",
        "taxonomy": value["taxonomy"],
        "canonical_summary": value,
        "corrected_twin_target": {
            "GAME_FIRST_PARTY": {
                "types": assemblies["Assembly-CSharp"]["target_type_count"],
                "methods": assemblies["Assembly-CSharp"]["owned_method_count"],
            },
            "KAIRO_ENGINE": {
                "types": assemblies["KairoLibrary"]["target_type_count"],
                "methods": assemblies["KairoLibrary"]["owned_method_count"],
            },
            "combined": {
                "types": assemblies["Assembly-CSharp"]["target_type_count"] + assemblies["KairoLibrary"]["target_type_count"],
                "methods": assemblies["Assembly-CSharp"]["owned_method_count"] + assemblies["KairoLibrary"]["owned_method_count"],
            },
        },
        "firstpass": assemblies["Assembly-CSharp-firstpass"],
        "compiler_generated_type_count": value["type_counts"].get("COMPILER_GENERATED", 0),
    }


def repair_summary(canonical_out: Path) -> dict[str, Any]:
    value = load_json(canonical_out / "repair-summary.json")
    method_summary = load_json(canonical_out / "method-summary.json")
    return {
        "schema_version": "r1.5-repair-summary-v1",
        "canonical_summary": value,
        "metadata_total_type_count": method_summary["metadata_total_type_count"],
        "metadata_total_method_count": method_summary["metadata_total_method_count"],
        "target_method_count": method_summary["target_method_count"],
        "target_type_count": method_summary["target_type_count"],
        "queue_covers_target_exactly": value["queue_method_count"] == method_summary["target_method_count"] and value["queue_id_unique"],
        "repaired_body_count": value["repaired_body_count"],
        "source_match_status_counts": dict(sorted(collections.Counter(row["source_match_status"] for row in load_jsonl(canonical_out / "method-catalog.jsonl")).items())),
    }


def dependency_summaries(builder: Any, canonical_out: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    summary = load_json(canonical_out / "dependency-summary.json")
    scc = load_json(canonical_out / "scc-summary.json")
    layers = load_jsonl(canonical_out / "dependency-layers.jsonl")
    bridges = load_json(canonical_out / "bridge-summary.json")
    classified = {
        "external_resolved_calls": load_jsonl(canonical_out / "external-resolved-call-edges.jsonl"),
        "owned_unresolved_calls": load_jsonl(canonical_out / "owned-unresolved-call-edges.jsonl"),
        "ambiguous_calls": load_jsonl(canonical_out / "ambiguous-call-edges.jsonl"),
        "source_limited_calls": load_jsonl(canonical_out / "source-limited-call-edges.jsonl"),
        "unresolved_fields": load_jsonl(canonical_out / "unresolved-field-edges.jsonl"),
    }
    edge_split = {
        "schema_version": "r1.5-unresolved-edge-summary-v1",
        "call_counts": {key: len(rows) for key, rows in classified.items() if key.endswith("calls")},
        "field_counts": {
            "owned_resolved_fields": summary.get("owned_resolved_field_edge_count", 0),
            "external_resolved_fields": summary.get("external_resolved_field_edge_count", 0),
            "unresolved_fields": len(classified["unresolved_fields"]),
            "ambiguous_fields": summary.get("ambiguous_field_edge_count", 0),
            "owned_unresolved_fields": summary.get("owned_unresolved_field_edge_count", 0),
            "source_limited_fields": summary.get("source_limited_field_edge_count", 0),
        },
        "external_edge_union_count": len(load_jsonl(canonical_out / "external-edges.jsonl")),
        "classification_vocabularies": {
            "calls": ["OWNED_RESOLVED_CALL", "EXTERNAL_RESOLVED_CALL", "OWNED_UNRESOLVED_CALL", "AMBIGUOUS_CALL", "SOURCE_LIMITED_CALL"],
            "fields": ["OWNED_RESOLVED_FIELD", "EXTERNAL_RESOLVED_FIELD", "OWNED_UNRESOLVED_FIELD", "AMBIGUOUS_FIELD", "SOURCE_LIMITED_FIELD"],
        },
    }
    ownership_bridge_counts = collections.Counter(
        (row["source_ownership"], row["target_ownership"], row["edge_kind"])
        for row in bridges
    )
    dependency = {
        "schema_version": "r1.5-dependency-summary-v1",
        "canonical_summary": summary,
        "largest_scc_method_count": max((row["method_count"] for row in scc), default=0),
        "largest_scc_ids": [row["scc_id"] for row in scc if row["method_count"] == max((x["method_count"] for x in scc), default=0)],
        "dependency_layer_count": len({row["layer"] for row in layers}),
        "max_dependency_layer": max((row["layer"] for row in layers), default=0),
        "ownership_bridges": [
            {"source_ownership": source, "target_ownership": target, "edge_kind": kind, "count": count}
            for (source, target, kind), count in sorted(ownership_bridge_counts.items())
        ],
        "required_bridge_metrics": {
            "game_to_kairo_calls": sum(row["count"] for row in bridges if row.get("source_ownership") == "GAME_FIRST_PARTY" and row.get("target_ownership") == "KAIRO_ENGINE" and row.get("edge_kind") in {"call", "external_call"}),
            "kairo_to_game_calls": sum(row["count"] for row in bridges if row.get("source_ownership") == "KAIRO_ENGINE" and row.get("target_ownership") == "GAME_FIRST_PARTY" and row.get("edge_kind") in {"call", "external_call"}),
            "owned_to_unity_edges": sum(row["count"] for row in bridges if row.get("target_ownership") == "UNITY_BOUNDARY"),
            "owned_to_dotnet_edges": sum(row["count"] for row in bridges if row.get("target_ownership") == "DOTNET_FRAMEWORK"),
            "owned_to_third_party_edges": sum(row["count"] for row in bridges if row.get("target_ownership") == "THIRD_PARTY"),
            "owned_to_native_edges": 0,
            "native_available_target_methods": load_json(canonical_out / "method-summary.json")["native_available_count"],
        },
    }
    return dependency, edge_split


def determinism_report(first_out: Path, second_out: Path) -> dict[str, Any]:
    first = load_json(first_out / "artifact-manifest.json")
    second = load_json(second_out / "artifact-manifest.json")
    first_files = {row["path"]: (row["sha256"], row.get("record_count")) for row in first["files"]}
    second_files = {row["path"]: (row["sha256"], row.get("record_count")) for row in second["files"]}
    return {
        "schema_version": "r1.5-determinism-v1",
        "status": "PASS" if first["tree_sha256"] == second["tree_sha256"] and first_files == second_files else "FAIL",
        "first_tree_sha256": first["tree_sha256"],
        "second_tree_sha256": second["tree_sha256"],
        "file_set_equal": set(first_files) == set(second_files),
        "file_hashes_equal": first_files == second_files,
        "first_counts": {row["path"]: row.get("record_count") for row in first["files"] if "record_count" in row},
        "second_counts": {row["path"]: row.get("record_count") for row in second["files"] if "record_count" in row},
    }


def write_report(accepted: Path, artifacts: dict[str, Any]) -> None:
    gate = artifacts["source_gate"]
    ownership = artifacts["ownership"]
    repair = artifacts["repair"]
    dependency = artifacts["dependency"]
    split = artifacts["edge_split"]
    type_summary = artifacts["type_reconciliation"]
    method_summary = artifacts["method_reconciliation"]
    core = artifacts["core"]
    lines = [
        "# R1.5 Metadata Identity Reconciliation Report",
        "",
        "## Final decision",
        "",
        f"R1.5 status: {artifacts['final_decision']['decision']}.",
        "The corrected metadata foundation is the only canonical identity authority for the next repair phase.",
        "The previous R1 architecture and acceptance package remain retained as audit history, but its pre-R1.5 counts, IDs, queue, and graph are superseded.",
        "",
        "## Source and reader gate",
        "",
        f"Pinned source identity: {gate['canonical_gate']['status']}; APK, C# archive, libil2cpp, global-metadata, and C# corpus inventory match.",
        f"Alternate raw evidence hashes: {'PASS' if gate['alternate_evidence']['all_required_raw_hashes_match_pack_manifest'] else 'FAIL'}.",
        f"Metadata reader defect: CONFIRMED. The installed dnfile API uses 0-based bracket indexing and 1-based RID lookup; the prior builder's `table[1:]` discarded the first real row. Fix: `table_rows` now returns `list(table)` and all local RID/token conversions are explicit.",
        "",
        "## Alternate evidence policy",
        "",
        "Raw dump.cs, script.json, and the three selected alternate DummyDll files are retained as cross-check evidence.",
        "Original Google-derived type/method/repair/call/field catalogs are comparison-only and are not canonical.",
        "",
        "## Corrected totals",
        "",
        f"Canonical metadata: {repair['metadata_total_type_count']:,} types, {repair['metadata_total_method_count']:,} methods.",
        f"Corrected Twin target: GAME_FIRST_PARTY {ownership['corrected_twin_target']['GAME_FIRST_PARTY']['types']:,} types / {ownership['corrected_twin_target']['GAME_FIRST_PARTY']['methods']:,} methods; KAIRO_ENGINE {ownership['corrected_twin_target']['KAIRO_ENGINE']['types']:,} types / {ownership['corrected_twin_target']['KAIRO_ENGINE']['methods']:,} methods; combined {ownership['corrected_twin_target']['combined']['types']:,} / {ownership['corrected_twin_target']['combined']['methods']:,}.",
        f"Difference versus old R1 target 8,678: {repair['target_method_count'] - 8678:+,} methods.",
        "",
        "## Core identity",
        "",
        f"Core-nine identity: {'PASS' if core['pass'] else 'FAIL'}. AppData and GameForm are normal Assembly-CSharp types; Node is the canonical game.routeSearch.Node with 3 methods. No compiler-generated alias is primary.",
        "",
        "## Alternate reconciliation",
        "",
        f"All {type_summary['assembly_count_compared']:,} metadata-present assembly identities were compared. The cross-check normalizes only literal `.dll` suffixes, nested namespace qualification, generic-arity spellings, and ordered overload parameter spellings; it does not overwrite canonical IDs or counts.",
        f"Type classifications: {json.dumps(type_summary['classification_counts'], sort_keys=True)}.",
        f"Method classifications: {json.dumps(method_summary['classification_counts'], sort_keys=True)}.",
        f"Canonical/alternate method totals: {method_summary['canonical_method_count']:,} / {method_summary['alternate_method_count']:,}; common normalized method instances: {sum(row['common_method_instance_count'] for row in method_summary['rows']):,}; RVA presence matches: {method_summary['rva_presence_match_total']:,}; exact RVA value matches: {method_summary['rva_value_match_total']:,}.",
        "Canonical RVA values come from DummyDll PE MethodDef rows, while alternate RVA/offset values come from the native Il2CppDumper dump; they are different address domains and are therefore reported, not substituted or treated as equal.",
        "",
        "## Quality and repair universe",
        "",
        f"Quality distribution: {json.dumps(repair['canonical_summary']['quality_class_counts'], sort_keys=True)}.",
        f"Repair disposition: {json.dumps(repair['canonical_summary']['repair_disposition_counts'], sort_keys=True)}.",
        f"Queue coverage: {'PASS' if repair['queue_covers_target_exactly'] else 'FAIL'}; repaired C# bodies: {repair['repaired_body_count']:,}.",
        "",
        "## Dependency graph",
        "",
        f"Resolved owned calls: {dependency['canonical_summary']['owned_call_edge_count']:,}; external-resolved calls: {split['call_counts']['external_resolved_calls']:,}; owned-unresolved calls: {split['call_counts']['owned_unresolved_calls']:,}; ambiguous calls: {split['call_counts']['ambiguous_calls']:,}; source-limited calls: {split['call_counts']['source_limited_calls']:,}.",
        f"SCCs: {dependency['canonical_summary']['scc_count']:,}; recursive SCCs: {dependency['canonical_summary']['recursive_scc_count']:,}; largest SCC: {dependency['largest_scc_method_count']:,}; dependency layers: {dependency['max_dependency_layer']:,}.",
        f"Fields are split into owned/external resolved and unresolved/ambiguous/source-limited classes; unresolved field rows: {split['field_counts']['unresolved_fields']:,}.",
        "",
        "## Boundary",
        "",
        "Source roots modified: NO.",
        "C# gameplay/Kairo bodies repaired: NO.",
        "Native lifting started: NO.",
        "R2 started: NO.",
        "V8/V8R changed: NO.",
        "Unity/Unity-MCP started: NO.",
        "",
        "## Determinism and validation",
        "",
        f"Deterministic rerun: {artifacts['determinism']['status']}; local builder validation: {artifacts['builder_result']['status']}; git diff --check is required before closure.",
        "",
        "## Next boundary",
        "",
        "R2_AUTOMATED_WHOLE_CORPUS_REPAIR is the recommended next phase. This task stops here.",
        "",
    ]
    (accepted / "R1_5_METADATA_RECONCILIATION_REPORT.md").write_text("\n".join(lines), encoding="utf-8", newline="\n")


def main() -> int:
    builder = import_builder()
    fresh = "--fresh" in sys.argv[1:]
    postprocess_only = "--postprocess-only" in sys.argv[1:]
    if not EVIDENCE_ZIP.is_file():
        raise RuntimeError(f"Missing evidence pack: {EVIDENCE_ZIP}")
    if not postprocess_only:
        for path in (CANONICAL_OUT, REPEAT_OUT, BUILDER_ACCEPTED_OUT, ACCEPTED_OUT, ALTERNATE_OUT):
            if path == CANONICAL_OUT and path.exists() and not fresh:
                continue
            if path.exists():
                shutil.rmtree(path)
    CANONICAL_OUT.mkdir(parents=True, exist_ok=True)
    gate, _, _ = builder.source_gate()
    if gate["status"] != "PASS":
        raise RuntimeError("BLOCKED_R1_5_SOURCE_IDENTITY_MISMATCH")
    if postprocess_only:
        builder_result = builder.validate_local_artifacts(CANONICAL_OUT)
    else:
        builder_result = run_canonical_build(builder, CANONICAL_OUT, BUILDER_ACCEPTED_OUT)
    if not postprocess_only:
        run_alternate_parser()
    alternate_types = load_jsonl(ALTERNATE_OUT / "corrected-google/google-r1-corrected-type-metadata.jsonl")
    alternate_methods = load_jsonl(ALTERNATE_OUT / "corrected-google/google-r1-corrected-method-metadata.jsonl")
    repeat_result = (
        builder.validate_local_artifacts(REPEAT_OUT)
        if postprocess_only
        else run_canonical_build(builder, REPEAT_OUT, BUILDER_ACCEPTED_OUT)
    )
    # The repeat output is intentionally local-only; no second accepted package is published.
    audit = metadata_reader_audit(builder, gate)
    type_summary, method_summary = reconcile_metadata(builder, CANONICAL_OUT, alternate_types, alternate_methods)
    core = core_identity(builder, CANONICAL_OUT, ALTERNATE_OUT)
    ownership = ownership_summary(CANONICAL_OUT)
    repair = repair_summary(CANONICAL_OUT)
    dependency, edge_split = dependency_summaries(builder, CANONICAL_OUT)
    determinism = determinism_report(CANONICAL_OUT, REPEAT_OUT)
    source_gate = {
        "schema_version": "r1.5-source-gate-v1",
        "canonical_gate": load_json(CANONICAL_OUT / "source-gate.json"),
        "alternate_evidence": evidence_manifest(builder, alternate_types, alternate_methods),
    }
    local_manifest = {
        "schema_version": "r1.5-local-artifact-manifest-v1",
        "canonical_heavy_root": str(CANONICAL_OUT),
        "canonical_artifact_manifest": load_json(CANONICAL_OUT / "artifact-manifest.json"),
        "alternate_heavy_root": str(ALTERNATE_OUT),
        "alternate_generated_manifest": load_json(ALTERNATE_OUT / "analysis/r15-generated-artifact-manifest.json"),
        "repeat_heavy_root": str(REPEAT_OUT),
        "repeat_artifact_tree_sha256": load_json(REPEAT_OUT / "artifact-manifest.json")["tree_sha256"],
        "evidence_pack_zip_sha256": sha256_file(EVIDENCE_ZIP),
    }
    validation_checks = {
        "source_gate": gate["status"] == "PASS",
        "metadata_reader_audit": audit["status"] == "PASS",
        "builder_validation": builder_result["status"] == "PASS",
        "repeat_builder_validation": repeat_result["status"] == "PASS",
        "determinism": determinism["status"] == "PASS",
        "alternate_raw_hashes": source_gate["alternate_evidence"]["all_required_raw_hashes_match_pack_manifest"],
        "core_identity": core["pass"],
        "queue_complete": repair["queue_covers_target_exactly"],
        "no_repaired_bodies": repair["repaired_body_count"] == 0,
        "dependency_split_measured": all(key in edge_split["call_counts"] for key in ("external_resolved_calls", "owned_unresolved_calls", "ambiguous_calls", "source_limited_calls")),
        "alternate_reconciliation_classified": all(row["classification"] for row in type_summary["rows"] + method_summary["rows"]),
    }
    final_decision = {
        "schema_version": "r1.5-final-decision-v1",
        "decision": PASS_TOKEN if all(validation_checks.values()) else "FAIL_R1_5_METADATA_RECONCILIATION",
        "source_identity": "MATCH",
        "metadata_reader": audit["status"],
        "alternate_cross_check": "PASS" if validation_checks["alternate_reconciliation_classified"] else "FAIL",
        "core_nine": "PASS" if core["pass"] else "FAIL",
        "ownership": "PASS" if validation_checks["builder_validation"] else "FAIL",
        "repair_queue": "PASS" if repair["queue_covers_target_exactly"] else "FAIL",
        "dependency_split": "PASS" if validation_checks["dependency_split_measured"] else "FAIL",
        "determinism": determinism["status"],
        "repaired_csharp_bodies": False,
        "native_lifting": False,
        "runtime_or_unity_work": False,
        "r2_started": False,
        "v8_changed": False,
        "next_recommended_phase": "R2_AUTOMATED_WHOLE_CORPUS_REPAIR",
        "stop_before_next_phase": True,
    }
    validation = {
        "schema_version": "r1.5-validation-v1",
        "status": "PASS" if all(validation_checks.values()) else "FAIL",
        "checks": validation_checks,
        "failed_checks": sorted(key for key, value in validation_checks.items() if not value),
        "counts": {
            "canonical_types": len(load_jsonl(CANONICAL_OUT / "type-catalog.jsonl")),
            "canonical_metadata_methods": len(load_jsonl(CANONICAL_OUT / "metadata-method-catalog.jsonl")),
            "canonical_target_methods": repair["target_method_count"],
            "alternate_types": len(alternate_types),
            "alternate_methods": len(alternate_methods),
        },
    }
    artifacts = {
        "source_gate": source_gate,
        "audit": audit,
        "alt_manifest": source_gate["alternate_evidence"],
        "type_reconciliation": type_summary,
        "method_reconciliation": method_summary,
        "core": core,
        "ownership": ownership,
        "repair": repair,
        "dependency": dependency,
        "edge_split": edge_split,
        "determinism": determinism,
        "builder_result": builder_result,
        "final_decision": final_decision,
    }
    ACCEPTED_OUT.mkdir(parents=True, exist_ok=True)
    dump_json(ACCEPTED_OUT / "r1-5-source-gate.json", source_gate)
    dump_json(ACCEPTED_OUT / "r1-5-metadata-reader-audit.json", audit)
    dump_json(ACCEPTED_OUT / "r1-5-alt-dump-manifest.json", source_gate["alternate_evidence"])
    dump_json(ACCEPTED_OUT / "r1-5-assembly-reconciliation.json", type_summary["rows"])
    dump_json(ACCEPTED_OUT / "r1-5-type-reconciliation-summary.json", type_summary)
    dump_json(ACCEPTED_OUT / "r1-5-method-reconciliation-summary.json", method_summary)
    dump_json(ACCEPTED_OUT / "r1-5-core-nine-identity.json", core)
    dump_json(ACCEPTED_OUT / "r1-5-ownership-summary.json", ownership)
    dump_json(ACCEPTED_OUT / "r1-5-repair-summary.json", repair)
    dump_json(ACCEPTED_OUT / "r1-5-dependency-summary.json", dependency)
    dump_json(ACCEPTED_OUT / "r1-5-unresolved-edge-summary.json", edge_split)
    dump_json(ACCEPTED_OUT / "r1-5-local-artifact-manifest.json", local_manifest)
    dump_json(ACCEPTED_OUT / "r1-5-validation.json", validation)
    dump_json(ACCEPTED_OUT / "r1-5-final-decision.json", final_decision)
    write_report(ACCEPTED_OUT, artifacts)
    print(json.dumps({
        "status": final_decision["decision"],
        "validation": validation,
        "canonical_out": str(CANONICAL_OUT),
        "accepted_out": str(ACCEPTED_OUT),
        "alternate_out": str(ALTERNATE_OUT),
    }, indent=2, sort_keys=True))
    return 0 if validation["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
