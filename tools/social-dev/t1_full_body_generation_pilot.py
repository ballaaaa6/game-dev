#!/usr/bin/env python3
"""Canonical T1.0 coverage-first full-body representation pilot.

This pilot keeps the R1.5/R3/R4 evidence boundary intact and writes only local
sidecar artifacts. Every selected method receives one inspectable C#-hosted
representation: readable source, proof-gated high-level C#, typed low-level
IR, raw low-level IR, or an explicit evidence-bound stub.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import shutil
import statistics
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable, Optional

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parents[1]
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from r4_native_ir_pilot import (  # noqa: E402
    ACCEPTANCE_ROOT as R4_ACCEPTANCE_ROOT,
CATALOG_PATH,
CFG_PROFILE_PATH,
    CanonicalEvidence,
    EXCEPTION_HELPERS,
    ISIL_ROOT,
    MethodEvidence,
    NativeInstruction,
STATUS_PATH,
    branch_target,
    build_cfg,
    conditional_branch,
    csharp_type,
    isil_call_name,
    native_target_from_operands,
    parse_int,
    source_tree_digest,
    verify_source_gate,
)


OUT_ROOT = ROOT / "artifacts" / "t1-0-full-body-pilot"
ACCEPTANCE_ROOT = ROOT / "knowledge" / "brain" / "acceptance" / "t1-0-full-body-generation-pivot-pilot"
CONTRACT_PATH = SCRIPT_DIR / "t1_twin_native_ir_contract.cs"
COMPILE_SCRIPT = SCRIPT_DIR / "compile_t1_sidecars.ps1"
DEFAULT_ATTACHED_PACK = Path(r"D:\downloads\T1_0_FULL_BODY_GENERATION_PIVOT_PILOT_PACK.zip")
DEFAULT_ROSLYN_ROOT = Path(r"C:\Users\WINDOW XI\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\powershell")
DEFAULT_PWSH = DEFAULT_ROSLYN_ROOT / "pwsh.exe"

EXPECTED_TYPES = 641
EXPECTED_METHODS = 10827
TYPE_CATALOG_PATH = ROOT / "artifacts" / "r1-5-metadata-reconciliation" / "type-catalog.jsonl"
COHORT_ORDER = (
    "BASELINE_READABLE",
    "CFG_DEFERRED",
    "NATIVE_DEFERRED",
    "IDENTITY_MECHANICAL_SOURCE_LIMITED",
    "EXTREME_COMPLEXITY",
)
COHORT_SIZES = {
    "BASELINE_READABLE": 75,
    "CFG_DEFERRED": 175,
    "NATIVE_DEFERRED": 175,
    "IDENTITY_MECHANICAL_SOURCE_LIMITED": 50,
    "EXTREME_COMPLEXITY": 25,
}
STATUS_BY_COHORT = {
    "BASELINE_READABLE": {"BASELINE_READABLE"},
    "CFG_DEFERRED": {"DEFER_CFG_UNPROVEN"},
    "NATIVE_DEFERRED": {"DEFER_R4_NATIVE"},
    "IDENTITY_MECHANICAL_SOURCE_LIMITED": {
        "BLOCKED_IDENTITY",
        "DEFER_MECHANICAL_UNPROVEN",
        "SOURCE_LIMITED",
    },
}
IDENTITY_STATUSES = STATUS_BY_COHORT["IDENTITY_MECHANICAL_SOURCE_LIMITED"]

PLACEHOLDER_NAMES = {"guardField", "valueField", "localTarget"}

MEMORY_LOAD_PREFIXES = ("LD",)
MEMORY_STORE_PREFIXES = ("ST",)
ARITHMETIC = {
    "ADD", "ADDS", "SUB", "SUBS", "MUL", "SMULL", "UMULL", "SMULH", "UMADDL",
    "UMULH", "MADD", "MSUB", "SMADDL", "SMSUBL", "UMADDL", "UMSUBL", "SDIV",
    "UDIV", "NEG", "NEGS", "MNEG", "SMIN", "SMAX", "UMIN", "UMAX", "CLS", "CLZ",
}
BITWISE = {
    "AND", "ANDS", "ORR", "ORN", "EOR", "BIC", "BICS", "MVN", "MVNI", "LSL",
    "LSR", "LSLV", "LSRV", "ASR", "ASRV", "ROR", "RORV", "UBFX", "SBFX", "SBFIZ",
    "BFI", "BFXIL", "TST", "RBIT", "REV", "REV16", "REV32", "REV64", "EXTR", "SXTW",
    "SXTH", "SXTB", "UXTW", "UXTH", "UXTB", "SBFM", "UBFM", "BFM",
}
MOVE = {"MOV", "MOVK", "MOVN", "MOVZ", "ADR", "ADRP", "FMOV", "CSEL", "CSINC", "CSINV", "CSNEG"}
FLOAT = {
    "FCVT", "FCVTAS", "FCVTAU", "FCVTMS", "FCVTMU", "FCVTNS", "FCVTNU", "FCVTPS",
    "FCVTPU", "FCVTZS", "FCVTZU", "SCVTF", "UCVTF", "FADD", "FSUB", "FMUL", "FDIV",
    "FNEG", "FABS", "FSQRT", "FCMP", "FCCMP", "FCSEL", "FMIN", "FMAX", "FRINTA",
    "FRINTM", "FRINTN", "FRINTP", "FRINTZ",
}
CONDITION = {
    "CMP", "CMN", "CCMP", "CCMN", "CSET", "CSETM", "CINC", "CINV", "CNEG", "CSINC",
    "CSINV", "CSNEG", "TST",
}
SYSTEM = {
    "RET", "NOP", "MRS", "MSR", "DMB", "DSB", "ISB", "HINT", "BRK", "SVC", "ERET",
    "PRFM", "YIELD", "WFE", "WFI", "SEV", "SEVL", "CLREX", "DC", "IC", "SYSL",
}


def stable_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(stable_json(value), encoding="utf-8", newline="\n")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def csharp_literal(value: Any) -> str:
    if value is None:
        return '""'
    return json.dumps(str(value), ensure_ascii=False)


def safe_identifier(method_id: str) -> str:
    return "Method_" + re.sub(r"[^A-Za-z0-9_]", "_", method_id)


def relative_path(path: Optional[str | Path]) -> Optional[str]:
    if not path:
        return None
    candidate = Path(path)
    try:
        return candidate.relative_to(ROOT).as_posix()
    except ValueError:
        return str(candidate).replace("\\", "/")


def parse_memory_access(instruction: NativeInstruction) -> Optional[dict[str, Any]]:
    mnemonic = instruction.mnemonic.upper()
    is_load = mnemonic.startswith(MEMORY_LOAD_PREFIXES)
    is_store = mnemonic.startswith(MEMORY_STORE_PREFIXES)
    if not (is_load or is_store):
        return None
    match = re.search(
        r"\[\s*(X\d+|W\d+|SP)(?:\s*(?:,\s*#?|\+\s*#?)(-?(?:0x[0-9A-Fa-f]+|[0-9]+)))?",
        instruction.operands,
        re.IGNORECASE,
    )
    if not match:
        return None
    offset = int(match.group(2), 0) if match.group(2) else 0
    destination = "" if is_store else instruction.operands.split(",", 1)[0].strip().upper()
    return {
        "address": f"0x{instruction.address:X}",
        "mnemonic": mnemonic,
        "base_register": match.group(1).upper(),
        "offset": offset,
        "access": "write" if is_store else "read",
        "destination": destination,
        "operands": instruction.operands,
        "stack": match.group(1).upper() == "SP",
    }


def register_pair(register: str) -> tuple[str, ...]:
    register = register.upper()
    if register.startswith("X") or register.startswith("W"):
        suffix = register[1:]
        return (f"X{suffix}", f"W{suffix}")
    return (register,)


def parse_register_move(instruction: NativeInstruction) -> Optional[tuple[str, str]]:
    if instruction.mnemonic.upper() != "MOV":
        return None
    match = re.fullmatch(r"\s*([XW]\d+)\s*,\s*([XW]\d+)\s*", instruction.operands, re.IGNORECASE)
    return (match.group(1).upper(), match.group(2).upper()) if match else None


def field_dict(field: Any, access: Optional[dict[str, Any]] = None) -> dict[str, Any]:
    value = {
        "declaring_type": field.declaring_type,
        "name": field.name,
        "type": csharp_type(field.type_name),
        "offset": f"0x{field.offset:X}",
        "offset_value": field.offset,
        "is_static": bool(field.is_static),
        "provenance": sorted(set(field.provenance)),
    }
    if access:
        value["access"] = access["access"]
        value["native_address"] = access["address"]
    return value


def source_relation(row: dict[str, Any], evidence: MethodEvidence) -> dict[str, Any]:
    match_status = str(row.get("source_match_status") or "MISSING")
    body_present = bool(row.get("source_body_present") and evidence.source.strip())
    if match_status == "EXACT_TYPE" and body_present:
        relation = "EXACT_TYPE_SOURCE_BODY"
    elif body_present:
        relation = "NON_EXACT_SOURCE_BODY"
    else:
        relation = "SOURCE_LIMITED"
    return {
        "relation": relation,
        "match_status": match_status,
        "body_present": body_present,
        "source_path": evidence.source_path,
        "source_line": row.get("source_line"),
        "source_line_end": row.get("source_line_end"),
        "body_sha256": row.get("body_sha256"),
    }


def provenance_for(row: dict[str, Any], evidence: MethodEvidence, status: str) -> dict[str, Any]:
    refs = [str(item) for item in row.get("evidence_refs") or []]
    if evidence.source_path:
        refs.append(evidence.source_path)
    if evidence.isil_path:
        refs.append(evidence.isil_path)
    return {
        "provenance_id": sha256_text(f"{row['method_id']}|{row.get('body_sha256')}|{row.get('isil_evidence_file')}")[:24],
        "authority": "canonical R1.5 catalog + R3 status + canonical ISIL/native evidence",
        "method_id": row["method_id"],
        "r3_status": status,
        "catalog": relative_path(CATALOG_PATH),
        "status_catalog": relative_path(STATUS_PATH),
        "cfg_profile": relative_path(CFG_PROFILE_PATH),
        "evidence_refs": sorted(set(refs)),
        "source_file": evidence.source_path,
        "isil_file": evidence.isil_path,
        "native_authority": "canonical ISIL disassembly section",
        "source_mutation_allowed": False,
    }


def native_shape_is_canonical(row: dict[str, Any], evidence: MethodEvidence) -> bool:
    if not evidence.native or not evidence.isil:
        return False
    expected_disassembly = parse_int(row.get("isil_disassembly_instruction_count"))
    expected_isil = parse_int(row.get("isil_instruction_count"))
    catalog_start = parse_int(row.get("isil_native_address"))
    if catalog_start is not None and evidence.native[0].address != catalog_start:
        return False
    if expected_disassembly is not None and expected_disassembly not in {len(evidence.native), len(evidence.native) + 1}:
        return False
    if expected_isil is not None and expected_isil != len(evidence.isil):
        return False
    return True


def spread(items: list[dict[str, Any]], count: int, sort_key: Optional[Any] = None) -> list[dict[str, Any]]:
    ordered = sorted(items, key=sort_key or (lambda item: str(item["method_id"])))
    if count > len(ordered):
        raise RuntimeError(f"Cannot select {count} rows from {len(ordered)} candidates")
    if count == 0:
        return []
    if count == len(ordered):
        return ordered
    return [ordered[(index * len(ordered)) // count] for index in range(count)]


def choose_balanced(
    items: list[dict[str, Any]],
    count: int,
    used: set[str],
    sort_key: Optional[Any] = None,
) -> list[dict[str, Any]]:
    available = [item for item in items if item["method_id"] not in used]
    ordered_key = sort_key or (lambda item: str(item["method_id"]))
    groups = {owner: sorted([item for item in available if item.get("ownership") == owner], key=ordered_key) for owner in ("GAME_FIRST_PARTY", "KAIRO_ENGINE")}
    selected: list[dict[str, Any]] = []
    if groups["GAME_FIRST_PARTY"] and groups["KAIRO_ENGINE"]:
        targets = {"GAME_FIRST_PARTY": count // 2, "KAIRO_ENGINE": count - count // 2}
        for owner in ("GAME_FIRST_PARTY", "KAIRO_ENGINE"):
            selected.extend(spread(groups[owner], targets[owner], ordered_key))
    else:
        selected = spread(available, count, ordered_key)
    selected_ids = {item["method_id"] for item in selected}
    if len(selected) < count:
        remaining = [item for item in available if item["method_id"] not in selected_ids]
        selected.extend(spread(remaining, count - len(selected), ordered_key))
    if len({item["method_id"] for item in selected}) != count:
        raise RuntimeError("Deterministic cohort selection produced duplicate method IDs")
    used.update(item["method_id"] for item in selected)
    return sorted(selected, key=lambda item: str(item["method_id"]))


def select_canonical_sample(canonical: CanonicalEvidence) -> tuple[dict[str, list[dict[str, Any]]], dict[str, Any]]:
    rows = list(canonical.rows)
    status_by_id = {row["method_id"]: canonical.status(row) for row in rows}
    valid_native_ids: set[str] = set()
    native_instruction_counts: dict[str, int] = {}
    scanned_native = 0
    valid_native = 0
    for row in rows:
        if not row.get("native_available"):
            continue
        scanned_native += 1
        evidence = canonical.evidence(row)
        if native_shape_is_canonical(row, evidence):
            valid_native_ids.add(row["method_id"])
            native_instruction_counts[row["method_id"]] = len(evidence.native)
            valid_native += 1

    valid_rows = [row for row in rows if row["method_id"] in valid_native_ids]
    if len(valid_rows) < 475:
        raise RuntimeError(f"Canonical evidence exposed only {len(valid_rows)} range-consistent native methods")

    used: set[str] = set()
    extremes = sorted(valid_rows, key=lambda item: (-native_instruction_counts[item["method_id"]], str(item["method_id"])))[:COHORT_SIZES["EXTREME_COMPLEXITY"]]
    used.update(item["method_id"] for item in extremes)

    sample: dict[str, list[dict[str, Any]]] = {}
    for cohort in ("BASELINE_READABLE", "CFG_DEFERRED", "NATIVE_DEFERRED"):
        pool = [
            row for row in rows
            if status_by_id[row["method_id"]] in STATUS_BY_COHORT[cohort]
            and row["method_id"] in valid_native_ids
            and row["method_id"] not in used
        ]
        sample[cohort] = choose_balanced(pool, COHORT_SIZES[cohort], used)

    identity_pool = [
        row for row in rows
        if status_by_id[row["method_id"]] in IDENTITY_STATUSES
        and (not row.get("native_available") or row["method_id"] in valid_native_ids)
        and row["method_id"] not in used
    ]
    sample["IDENTITY_MECHANICAL_SOURCE_LIMITED"] = choose_balanced(
        identity_pool,
        COHORT_SIZES["IDENTITY_MECHANICAL_SOURCE_LIMITED"],
        used,
        sort_key=lambda item: (
            0 if not item.get("native_available") else 1,
            str(status_by_id[item["method_id"]]),
            str(item["method_id"]),
        ),
    )
    sample["EXTREME_COMPLEXITY"] = sorted(extremes, key=lambda item: str(item["method_id"]))

    selected = [item for group in sample.values() for item in group]
    selected_ids = [item["method_id"] for item in selected]
    if len(selected_ids) != 500 or len(set(selected_ids)) != 500:
        raise RuntimeError("Canonical sample is not exactly 500 unique methods")
    if {item.get("ownership") for item in selected} != {"GAME_FIRST_PARTY", "KAIRO_ENGINE"}:
        raise RuntimeError("Canonical sample is not ownership-diverse")
    shape = {cohort: len(sample[cohort]) for cohort in COHORT_ORDER}
    if shape != COHORT_SIZES:
        raise RuntimeError(f"Cohort shape mismatch: {shape}")

    metrics = {
        "canonical_rows": len(rows),
        "canonical_types": sum(1 for line in TYPE_CATALOG_PATH.read_text(encoding="utf-8").splitlines() if line.strip() and json.loads(line).get("ownership") in {"GAME_FIRST_PARTY", "KAIRO_ENGINE"}),
        "scanned_native_rows": scanned_native,
        "range_consistent_native_rows": valid_native,
        "range_rejected_native_rows": scanned_native - valid_native,
        "cohort_shape": shape,
        "cohort_ownership": {
            cohort: dict(sorted(Counter(item.get("ownership") for item in sample[cohort]).items()))
            for cohort in COHORT_ORDER
        },
        "extreme_instruction_counts": [native_instruction_counts[item["method_id"]] for item in extremes],
        "valid_native_instruction_counts": sorted(native_instruction_counts.values()),
        "valid_native_method_ids": sorted(valid_native_ids),
    }
    # The canonical reader caches every method block encountered during the
    # selection scan. Keep the deterministic selection facts, but release the
    # whole-corpus parse cache before materializing the 500-method sidecars.
    canonical._isil_method_cache.clear()
    canonical._isil_lines_cache.clear()
    canonical._source_lines_cache.clear()
    return sample, metrics


def resolve_native_call(canonical: CanonicalEvidence, address_index: dict[int, list[dict[str, Any]]], instruction: NativeInstruction) -> dict[str, Any]:
    target = native_target_from_operands(instruction.operands) if instruction.mnemonic == "BL" else None
    candidates = sorted(address_index.get(target, []), key=lambda item: str(item.get("method_id"))) if target is not None else []
    result: dict[str, Any] = {
        "address": f"0x{instruction.address:X}",
        "kind": "direct" if instruction.mnemonic == "BL" else "virtual_or_indirect",
        "mnemonic": instruction.mnemonic,
        "target_address": f"0x{target:X}" if target is not None else None,
        "provenance": [f"native:{instruction.address:#x}", relative_path(canonical.call_index.__class__.__module__)],
    }
    if len(candidates) == 1:
        target_row = candidates[0]
        result.update(
            {
                "resolution": "CANONICAL_METHOD_NATIVE_ADDRESS_EXACT",
                "callee_method_id": target_row.get("method_id"),
                "callee_assembly": target_row.get("assembly"),
                "callee_declaring_type": target_row.get("declaring_type"),
                "callee_method_name": target_row.get("method_name"),
                "callee_signature": target_row.get("normalized_signature"),
                "callee_metadata_token": target_row.get("metadata_token"),
            }
        )
        return result
    script_target = canonical.call_index.native_target(target)
    result.update(
        {
            "resolution": "INDIRECT_OR_VIRTUAL_UNRESOLVED" if instruction.mnemonic != "BL" else "UNRESOLVED_CANONICAL_TARGET",
            "script_target": script_target,
            "reason": "no unique canonical method identity at native target address",
        }
    )
    return result


def resolve_isil_calls(canonical: CanonicalEvidence, evidence: MethodEvidence) -> list[dict[str, Any]]:
    calls: list[dict[str, Any]] = []
    for item in evidence.isil:
        if item.opcode not in {"Call", "CallVoid", "IndirectCall"}:
            continue
        name = isil_call_name(item.text, item.opcode) or ""
        resolution = canonical.call_index.isil_call(name, str(evidence.row.get("declaring_type") or ""))
        resolution.update(
            {
                "isil_index": item.index,
                "kind": "virtual_or_indirect" if item.opcode == "IndirectCall" else "isil_call",
                "provenance": [f"isil:{item.index}"],
            }
        )
        calls.append(resolution)
    return calls


def cfg_facts_for(evidence: MethodEvidence) -> dict[str, Any]:
    """Keep the extreme cohort inspectable without quadratic CFG analysis.

    The accepted R4 CFG builder is retained for ordinary methods. Very large
    native bodies receive a linear block/edge summary while every branch and
    raw instruction remains preserved in the per-instruction IR.
    """
    if len(evidence.native) <= 1000:
        return build_cfg(evidence.native, evidence.isil).as_dict()
    native = evidence.native
    addresses = [item.address for item in native]
    address_to_index = {address: index for index, address in enumerate(addresses)}
    leaders = {0}
    branches: list[dict[str, Any]] = []
    for index, instruction in enumerate(native):
        target = branch_target(instruction)
        if target is not None:
            branches.append({"native_address": f"0x{instruction.address:X}", "mnemonic": instruction.mnemonic, "target": f"0x{target:X}", "conditional": conditional_branch(instruction)})
            if target in address_to_index:
                leaders.add(address_to_index[target])
            if conditional_branch(instruction) and index + 1 < len(native):
                leaders.add(index + 1)
    leader_indexes = sorted(leaders)
    blocks: list[dict[str, Any]] = []
    index_to_block: dict[int, str] = {}
    for block_index, start in enumerate(leader_indexes):
        end = leader_indexes[block_index + 1] - 1 if block_index + 1 < len(leader_indexes) else len(native) - 1
        block_id = f"b{block_index}"
        indexes = list(range(start, end + 1))
        blocks.append({"block_id": block_id, "start": f"0x{native[start].address:X}", "end": f"0x{native[end].address:X}", "instruction_indexes": indexes, "successors": [], "predecessors": []})
        for item_index in indexes:
            index_to_block[item_index] = block_id
    edges: list[dict[str, str]] = []
    for block_index, block in enumerate(blocks):
        last_index = block["instruction_indexes"][-1]
        last = native[last_index]
        target = branch_target(last)
        if target is not None and target in address_to_index and address_to_index[target] in index_to_block:
            edges.append({"from": block["block_id"], "to": index_to_block[address_to_index[target]], "kind": "BRANCH_TARGET" if conditional_branch(last) else "UNCONDITIONAL_BRANCH"})
        if (target is None or conditional_branch(last)) and block_index + 1 < len(blocks):
            edges.append({"from": block["block_id"], "to": blocks[block_index + 1]["block_id"], "kind": "FALLTHROUGH"})
    for edge in edges:
        blocks[int(edge["from"][1:])]["successors"].append(edge["to"])
        blocks[int(edge["to"][1:])]["predecessors"].append(edge["from"])
    switch_count = sum(1 for item in native if item.mnemonic in {"BR", "TBB", "TBH"}) + sum(1 for item in evidence.isil if item.opcode.lower() in {"switch", "jumptable", "indirectjump"})
    return {
        "status": "EXTREME_COMPLEXITY_LINEAR_CFG_SUMMARY",
        "blocks": blocks,
        "edges": edges,
        "dominators": {},
        "post_dominators": {},
        "back_edges": [],
        "loops": [],
        "switch": {
            "status": "RECOVERED_INDIRECT_TRANSFER" if switch_count else "NOT_OBSERVED",
            "case_order": "UNRESOLVED" if switch_count else "NOT_APPLICABLE",
            "native_indirect_transfer_count": sum(1 for item in native if item.mnemonic in {"BR", "TBB", "TBH"}),
            "isil_switch_fact_count": sum(1 for item in evidence.isil if item.opcode.lower() in {"switch", "jumptable", "indirectjump"}),
        },
        "summary_only": True,
        "instruction_count": len(native),
        "branch_count": len(branches),
        "branches": branches,
    }


def classify_instruction(instruction: NativeInstruction, memory: Optional[dict[str, Any]], field: Optional[dict[str, Any]], call: Optional[dict[str, Any]]) -> tuple[str, str]:
    mnemonic = instruction.mnemonic.upper()
    if call:
        if mnemonic == "BL":
            return ("DirectCall" if call.get("resolution") == "CANONICAL_METHOD_NATIVE_ADDRESS_EXACT" else "DirectCallUnknown", "CALL_RESOLVED" if call.get("resolution") == "CANONICAL_METHOD_NATIVE_ADDRESS_EXACT" else "CALL_UNRESOLVED")
        return "IndirectCall", "CALL_INDIRECT"
    if field:
        return ("LoadField" if memory and memory["access"] == "read" else "StoreField", "FIELD_RESOLVED")
    if mnemonic == "RET":
        return "Return", "RETURN"
    if conditional_branch(instruction) or mnemonic == "B" or mnemonic == "BR":
        return "Branch", "BRANCH"
    if memory:
        return ("Load" if memory["access"] == "read" else "Store", "MEMORY")
    if mnemonic in ARITHMETIC:
        return "Arithmetic", "ARITHMETIC"
    if mnemonic in BITWISE:
        return "BitOp", "BITWISE"
    if mnemonic in MOVE:
        return "Move", "MOVE"
    if mnemonic in FLOAT or mnemonic.startswith("F"):
        return "FloatOp", "FLOAT"
    if mnemonic in CONDITION:
        return "Condition", "CONDITION"
    if mnemonic in SYSTEM or mnemonic.startswith(("DMB", "DSB", "ISB")):
        return "SystemOp", "SYSTEM"
    return "RawOp", "RAW_NATIVE"


def initial_bindings(row: dict[str, Any]) -> list[dict[str, str]]:
    bindings: list[dict[str, str]] = []
    if not row.get("is_static"):
        bindings.append({"register": "X0", "semantic": "this", "type": str(row.get("declaring_type") or "unknown")})
    first = 0 if row.get("is_static") else 1
    for index, type_name in enumerate(row.get("parameter_types") or []):
        bindings.append({"register": f"X{first + index}", "semantic": f"arg{index}", "type": csharp_type(str(type_name))})
    return bindings


def analyze_native(canonical: CanonicalEvidence, evidence: MethodEvidence, address_index: dict[int, list[dict[str, Any]]]) -> dict[str, Any]:
    row = evidence.row
    aliases: dict[str, str] = {}
    alias_types: dict[str, str] = {}
    if not row.get("is_static"):
        for register in register_pair("X0"):
            aliases[register] = "this"
            alias_types[register] = str(row.get("declaring_type") or "unknown")
    first = 0 if row.get("is_static") else 1
    for index, type_name in enumerate(row.get("parameter_types") or []):
        for register in register_pair(f"X{first + index}"):
            aliases[register] = f"arg{index}"
            alias_types[register] = csharp_type(str(type_name))

    lifter = __import__("r4_native_ir_pilot").SemanticLifter(canonical)
    static_field_by_offset: dict[int, Any] = {}
    try:
        field_facts, _ = lifter._field_facts(evidence)
        static_field_by_offset = {field.offset: field for field in field_facts if field.is_static and field.offset >= 0}
    except Exception:
        field_facts = []

    operations: list[dict[str, Any]] = []
    fields: dict[tuple[str, str, int], dict[str, Any]] = {}
    calls: list[dict[str, Any]] = []
    unresolved_direct_calls: list[dict[str, Any]] = []
    indirect_calls: list[dict[str, Any]] = []
    unresolved_field_accesses: list[dict[str, Any]] = []
    stack_accesses: list[dict[str, Any]] = []
    alias_events: list[dict[str, Any]] = []
    branch_facts: list[dict[str, Any]] = []
    type_events: list[dict[str, Any]] = []
    array_object_facts: list[dict[str, Any]] = []
    exception_helpers: list[dict[str, Any]] = []

    for index, instruction in enumerate(evidence.native):
        memory = parse_memory_access(instruction)
        alias = aliases.get(memory["base_register"]) if memory else None
        field = None
        if memory and memory["stack"]:
            stack_accesses.append({"native_address": memory["address"], "access": memory["access"], "operands": memory["operands"]})
        if memory and alias == "this":
            resolved = canonical.field_index.resolve(str(row.get("declaring_type") or ""), int(memory["offset"]))
            if resolved:
                field = field_dict(resolved, memory)
                field["alias"] = f"{memory['base_register']}=this"
                key = (field["declaring_type"], field["name"], field["offset_value"])
                fields.setdefault(key, field)
                fields[key]["provenance"] = sorted(set(fields[key]["provenance"] + [f"native:{memory['address']}:{memory['access']}"]))
            else:
                unresolved_field_accesses.append({"native_address": memory["address"], "base_register": memory["base_register"], "alias": "this", "offset": f"0x{memory['offset']:X}", "access": memory["access"], "operands": memory["operands"], "reason": "no unique metadata field at offset"})
        elif memory and not memory["stack"] and int(memory["offset"]) in static_field_by_offset:
            resolved = static_field_by_offset[int(memory["offset"])]
            field = field_dict(resolved, memory)
            field["alias"] = f"{memory['base_register']}=static_metadata_pointer_candidate"
            key = (field["declaring_type"], field["name"], field["offset_value"])
            fields.setdefault(key, field)
            fields[key]["provenance"] = sorted(set(fields[key]["provenance"] + [f"native:{memory['address']}:{memory['access']}" ]))

        call = resolve_native_call(canonical, address_index, instruction) if instruction.mnemonic in {"BL", "BLR"} else None
        if call:
            calls.append(call)
            if call.get("kind") == "direct" and call.get("resolution") != "CANONICAL_METHOD_NATIVE_ADDRESS_EXACT":
                unresolved_direct_calls.append(call)
            if call.get("kind") == "virtual_or_indirect":
                indirect_calls.append(call)
            if call.get("target_address") and parse_int(call.get("target_address")) in EXCEPTION_HELPERS:
                exception_helpers.append(call)

        kind, family = classify_instruction(instruction, memory, field, call)
        target = branch_target(instruction)
        if target is not None:
            branch_facts.append({"native_address": f"0x{instruction.address:X}", "mnemonic": instruction.mnemonic, "target": f"0x{target:X}", "conditional": conditional_branch(instruction)})
        if memory and ("LSL" in instruction.operands.upper() or "[" in instruction.operands):
            array_object_facts.append({"native_address": f"0x{instruction.address:X}", "kind": "ARRAY_OR_OBJECT_ACCESS_CANDIDATE", "operands": instruction.operands, "resolved": bool(field)})

        operation = {
            "native_index": index,
            "native_address": f"0x{instruction.address:X}",
            "mnemonic": instruction.mnemonic,
            "operands": instruction.operands,
            "kind": kind,
            "family": family,
            "raw_payload": instruction.text,
            "field": field,
            "call": call,
            "branch_target": f"0x{target:X}" if target is not None else None,
            "stack_access": bool(memory and memory["stack"]),
            "provenance": [f"native:{instruction.address:#x}"],
        }
        operations.append(operation)

        move = parse_register_move(instruction)
        if move:
            destination, source = move
            source_alias = aliases.get(source)
            if source_alias:
                for register in register_pair(destination):
                    aliases[register] = source_alias
                    alias_types[register] = alias_types.get(source, "unknown")
                alias_events.append({"native_address": f"0x{instruction.address:X}", "destination": destination, "source": source, "semantic": source_alias, "kind": "REGISTER_ALIAS"})
            else:
                for register in register_pair(destination):
                    aliases.pop(register, None)
                    alias_types.pop(register, None)
        if field and memory and memory["access"] == "read" and memory["destination"]:
            for register in register_pair(memory["destination"]):
                alias_types[register] = field["type"]
            type_events.append({"native_address": f"0x{instruction.address:X}", "register": memory["destination"], "type": field["type"], "source": f"{field['declaring_type']}.{field['name']}@{field['offset']}"})

    isil_calls = resolve_isil_calls(canonical, evidence)
    for call in isil_calls:
        if call.get("resolution") in {"METADATA_NAME_UNIQUE", "CANONICAL_METHOD_NATIVE_ADDRESS_EXACT"}:
            continue
        if call.get("kind") == "virtual_or_indirect":
            indirect_calls.append(call)

    cfg = cfg_facts_for(evidence)
    return {
        "operations": operations,
        "fields": sorted(fields.values(), key=lambda item: (item["declaring_type"], item["offset_value"], item["name"])),
        "calls": {
            "native": calls,
            "isil": isil_calls,
            "resolved_direct": [item for item in calls if item.get("kind") == "direct" and item.get("resolution") == "CANONICAL_METHOD_NATIVE_ADDRESS_EXACT"],
            "unresolved_direct": unresolved_direct_calls,
            "virtual_or_indirect": indirect_calls,
        },
        "unresolved_field_accesses": unresolved_field_accesses,
        "stack_accesses": stack_accesses,
        "alias_events": alias_events,
        "final_aliases": dict(sorted(aliases.items())),
        "type_propagation": {"register_types": dict(sorted(alias_types.items())), "events": type_events},
        "branch_facts": branch_facts,
        "array_object_facts": array_object_facts,
        "exception_helpers": exception_helpers,
        "cfg": cfg,
        "isil_calls": isil_calls,
        "static_field_facts": [field for field in fields.values() if field.get("is_static")],
    }


def high_level_probe(canonical: CanonicalEvidence, evidence: MethodEvidence) -> dict[str, Any]:
    try:
        lifter = __import__("r4_native_ir_pilot").SemanticLifter(canonical)
        return lifter.lift(evidence, "T1_0_HIGH_LEVEL_PROBE")
    except Exception as error:
        return {
            "generated_csharp": None,
            "pattern": "PROBE_ERROR",
            "oracle": "REJECTED",
            "proof": {"status": "REJECTED_PROOF_GATE", "error": str(error)},
        }


def contains_placeholder(value: Any) -> list[str]:
    text = json.dumps(value, ensure_ascii=False, sort_keys=True)
    return sorted({name for name in PLACEHOLDER_NAMES if re.search(rf"\b{re.escape(name)}\b", text)})


def instruction_count_accounting(row: dict[str, Any], evidence: MethodEvidence, represented: int) -> dict[str, Any]:
    catalog_disassembly = parse_int(row.get("isil_disassembly_instruction_count"))
    catalog_isil = parse_int(row.get("isil_instruction_count"))
    decoded_native = len(evidence.native)
    if decoded_native:
        if catalog_disassembly == decoded_native + 1:
            expected_native = decoded_native
            convention = "CATALOG_ISIL_DISASSEMBLY_INCLUDES_ONE_SYNTHETIC_TERMINAL_OP"
        elif catalog_disassembly == decoded_native:
            expected_native = decoded_native
            convention = "CATALOG_ISIL_DISASSEMBLY_MATCHES_DECODED_NATIVE"
        else:
            expected_native = decoded_native
            convention = "DECODED_NATIVE_COUNT_USED_AFTER_EXPLICIT_CANONICAL_RANGE_SELECTION"
        omitted = max(expected_native - represented, 0)
        extra = max(represented - expected_native, 0)
        return {
            "catalog_isil_disassembly_instruction_count": catalog_disassembly,
            "catalog_isil_instruction_count": catalog_isil,
            "expected_native_instruction_count": expected_native,
            "decoded_native_instruction_count": decoded_native,
            "represented_ir_operation_count": represented,
            "omitted_operation_count": omitted,
            "extra_ir_operation_count": extra,
            "count_convention": convention,
            "omission_reason": None if omitted == 0 else "IR emission failure",
            "range_accounted": omitted == 0 and extra == 0,
        }
    if not row.get("native_available"):
        return {
            "catalog_isil_disassembly_instruction_count": catalog_disassembly,
            "catalog_isil_instruction_count": catalog_isil,
            "expected_native_instruction_count": None,
            "decoded_native_instruction_count": 0,
            "represented_ir_operation_count": represented,
            "omitted_operation_count": 0,
            "extra_ir_operation_count": 0,
            "count_convention": "NO_NATIVE_OR_ISIL_BODY_IN_CANONICAL_CATALOG",
            "omission_reason": None,
            "range_accounted": True,
        }
    expected_native = catalog_disassembly or 0
    return {
        "catalog_isil_disassembly_instruction_count": catalog_disassembly,
        "catalog_isil_instruction_count": catalog_isil,
        "expected_native_instruction_count": expected_native,
        "decoded_native_instruction_count": 0,
        "represented_ir_operation_count": represented,
        "omitted_operation_count": expected_native,
        "extra_ir_operation_count": 0,
        "count_convention": "OPAQUE_NATIVE_EVIDENCE_REFERENCE_REQUIRED",
        "omission_reason": "canonical method range was not decodable; explicit opaque evidence reference retained",
        "range_accounted": False,
    }


def emit_sidecar_source(record: dict[str, Any], analysis: dict[str, Any]) -> str:
    metadata = record["identity"]
    lines = [
        "using SocialDev.T1Pilot;",
        "",
        "namespace SocialDev.T1Pilot.Generated",
        "{",
        f"    public static class {safe_identifier(record['method_id'])}",
        "    {",
        "        public static TwinNativeIrMethod Build()",
        "        {",
        "            var ir = TwinNativeIr.Begin(new TwinNativeIrMetadata(",
        f"                {csharp_literal(metadata['method_id'])}, {csharp_literal(metadata['assembly'])}, {csharp_literal(metadata['ownership'])},",
        f"                {csharp_literal(metadata['declaring_type'])}, {csharp_literal(metadata['signature'])}, {csharp_literal(metadata['metadata_token'])},",
        f"                {csharp_literal(metadata['rva'])}, {csharp_literal(record['native_range'].get('start'))}, {csharp_literal(record['native_range'].get('end'))},",
        f"                {csharp_literal(record['source_relation']['relation'])}, {csharp_literal(record['representation_tier'])}, {csharp_literal(record['provenance']['provenance_id'])}));",
    ]
    for binding in record["abi"]["bindings"]:
        lines.append(f"            ir.Bind({csharp_literal(binding['register'])}, {csharp_literal(binding['semantic'])}, {csharp_literal(binding['type'])});")
    for item in record["isil_range"]["instructions"]:
        lines.append(f"            ir.AddIsilEvidence({int(item['index'])}, {csharp_literal(item['text'])});")
    if record.get("source_body"):
        lines.append(f"            ir.SetSourceBody({csharp_literal(record['source_body'])});")
    if record.get("high_level_csharp"):
        lines.append(f"            ir.SetGeneratedHighLevelCSharp({csharp_literal(record['high_level_csharp'])});")
    if record["representation_tier"] == "OPAQUE_NATIVE_STUB":
        lines.append(f"            ir.SetOpaqueEvidenceReference({csharp_literal(record['provenance'].get('isil_file') or record['provenance'].get('evidence_refs'))});")
    if record["representation_tier"] == "SOURCE_LIMITED_STUB":
        lines.append(f"            ir.SetLimitation({csharp_literal(record['source_relation']['relation'])});")
    for operation in analysis["operations"]:
        index = int(operation["native_index"])
        address = csharp_literal(operation["native_address"])
        mnemonic = csharp_literal(operation["mnemonic"])
        operands = csharp_literal(operation["operands"])
        detail = csharp_literal(operation.get("raw_payload") or "")
        kind = operation["kind"]
        if kind in {"LoadField", "StoreField"} and operation.get("field"):
            field = operation["field"]
            method = "LoadField" if kind == "LoadField" else "StoreField"
            alias = csharp_literal(operation.get("field", {}).get("alias") or "")
            lines.append(
                f"            ir.{method}({index}, {address}, null, {mnemonic}, {operands}, {csharp_literal(field['name'])}, {csharp_literal(field['declaring_type'])}, {csharp_literal(field['type'])}, {csharp_literal(field['offset'])}, {alias});"
            )
        elif kind == "DirectCall" and operation.get("call"):
            call = operation["call"]
            lines.append(f"            ir.DirectCall({index}, {address}, null, {mnemonic}, {operands}, {csharp_literal(call.get('callee_method_id') or '')}, {csharp_literal(call.get('target_address') or '')});")
        elif kind == "IndirectCall":
            lines.append(f"            ir.IndirectCall({index}, {address}, null, {mnemonic}, {operands}, {detail});")
        elif kind == "Branch":
            lines.append(f"            ir.Branch({index}, {address}, null, {mnemonic}, {operands}, {csharp_literal(operation.get('branch_target') or '')});")
        elif kind == "Return":
            lines.append(f"            ir.Return({index}, {address}, null, {mnemonic}, {operands});")
        else:
            lines.append(f"            ir.EmitInstruction({index}, {address}, null, {csharp_literal(kind)}, {mnemonic}, {operands}, {detail});")
    lines.extend([
        "            return ir.Complete();",
        "        }",
        "    }",
        "}",
        "",
    ])
    return "\n".join(lines)


def build_record(canonical: CanonicalEvidence, row: dict[str, Any], cohort: str, address_index: dict[int, list[dict[str, Any]]]) -> tuple[dict[str, Any], str]:
    evidence = canonical.evidence(row)
    status = canonical.status(row)
    analysis = analyze_native(canonical, evidence, address_index) if evidence.native else {
        "operations": [], "fields": [], "calls": {"native": [], "isil": [], "resolved_direct": [], "unresolved_direct": [], "virtual_or_indirect": []},
        "unresolved_field_accesses": [], "stack_accesses": [], "alias_events": [], "final_aliases": {},
        "type_propagation": {"register_types": {}, "events": []}, "branch_facts": [], "array_object_facts": [],
        "exception_helpers": [], "cfg": build_cfg([], evidence.isil).as_dict(), "isil_calls": [], "static_field_facts": [],
    }
    probe = high_level_probe(canonical, evidence) if evidence.native and len(evidence.native) <= 1000 else {"generated_csharp": None, "pattern": "EXTREME_COMPLEXITY_OR_NO_NATIVE_BODY", "oracle": "REJECTED", "proof": {"status": "REJECTED_PROOF_GATE"}}
    relation = source_relation(row, evidence)
    source_exact = relation["relation"] == "EXACT_TYPE_SOURCE_BODY"
    high_code = probe.get("generated_csharp")
    high_placeholder = contains_placeholder(high_code) if high_code else []

    if cohort == "BASELINE_READABLE" and source_exact:
        tier = "EXISTING_READABLE"
        quality = "SOURCE_ORACLE_EXACT"
        high_code = None
    elif probe.get("proof", {}).get("status") == "VERIFIED_PILOT" and high_code and not high_placeholder:
        tier = "GENERATED_HIGH"
        quality = "STRUCTURAL_CONFIRMED"
    elif evidence.native:
        raw_count = sum(1 for item in analysis["operations"] if item["family"] == "RAW_NATIVE")
        typed_facts = len(analysis["calls"]["resolved_direct"]) + len(analysis["fields"]) + len(analysis["branch_facts"]) + sum(1 for item in analysis["operations"] if item["kind"] == "Return")
        tier = "GENERATED_MEDIUM" if raw_count == 0 and typed_facts > 0 else "GENERATED_LOW"
        quality = "REJECTED_HIGH_LEVEL_PROOF" if probe.get("proof", {}).get("status") != "VERIFIED_PILOT" else "STRUCTURAL_REJECTED_PLACEHOLDER"
        high_code = None
    elif row.get("native_available"):
        tier = "OPAQUE_NATIVE_STUB"
        quality = "REJECTED_NATIVE_DECODER_BOUNDARY"
        high_code = None
    else:
        tier = "SOURCE_LIMITED_STUB"
        quality = "REJECTED_SOURCE_LIMITED"
        high_code = None

    accounting = instruction_count_accounting(row, evidence, len(analysis["operations"]))
    native_range = {
        "status": "DECODED" if evidence.native else "NOT_AVAILABLE_BY_CANONICAL_CATALOG" if not row.get("native_available") else "UNDECODED_CANONICAL_EVIDENCE",
        "start": f"0x{evidence.native[0].address:X}" if evidence.native else None,
        "end": f"0x{evidence.native[-1].address:X}" if evidence.native else None,
        "instruction_count": len(evidence.native),
        "catalog_start": row.get("isil_native_address"),
    }
    identity = {
        "method_id": row.get("method_id"),
        "assembly": row.get("assembly"),
        "ownership": row.get("ownership"),
        "declaring_type": row.get("declaring_type"),
        "method_name": row.get("method_name"),
        "signature": row.get("normalized_signature"),
        "metadata_token": row.get("metadata_token"),
        "rva": row.get("rva"),
        "generic_arity": row.get("generic_arity"),
        "parameter_types": row.get("parameter_types") or [],
        "return_type": row.get("return_type"),
    }
    record = {
        "schema_version": "t1-0-twin-native-ir-method-v1",
        "method_id": row["method_id"],
        "cohort": cohort,
        "status_before_representation": status,
        "representation_emitted": True,
        "representation_tier": tier,
        "high_level_quality": quality,
        "identity": identity,
        "source_relation": relation,
        "native_range": native_range,
        "isil_range": {
            "path": evidence.isil_path,
            "header": evidence.isil_header,
            "instruction_count": len(evidence.isil),
            "catalog_instruction_count": parse_int(row.get("isil_instruction_count")),
            "instructions": [{"index": item.index, "opcode": item.opcode, "text": item.text} for item in evidence.isil],
        },
        "accounting": accounting,
        "abi": {
            "architecture": "ARM64 managed ABI",
            "instance_receiver": "X0" if not row.get("is_static") else None,
            "return_register": "X0",
            "bindings": initial_bindings(row),
            "alias_propagation": analysis["alias_events"],
            "final_aliases": analysis["final_aliases"],
        },
        "typed_ir_operations": analysis["operations"],
        "fields": analysis["fields"],
        "calls": analysis["calls"],
        "unresolved_field_accesses": analysis["unresolved_field_accesses"],
        "stack_values": analysis["stack_accesses"],
        "type_propagation": analysis["type_propagation"],
        "branch_facts": analysis["branch_facts"],
        "switch_jump_table_facts": analysis["cfg"].get("switch"),
        "array_object_facts": analysis["array_object_facts"],
        "exception_helpers": analysis["exception_helpers"],
        "cfg": analysis["cfg"],
        "source_oracle": {
            "path": evidence.source_path,
            "body_sha256": row.get("body_sha256"),
            "match_status": row.get("source_match_status"),
            "body_present": bool(row.get("source_body_present") and evidence.source.strip()),
        },
        "provenance": provenance_for(row, evidence, status),
        "high_level_csharp": high_code,
        "high_level_probe": {
            "status": probe.get("proof", {}).get("status"),
            "pattern": probe.get("pattern"),
            "oracle": probe.get("oracle"),
            "placeholder_names": high_placeholder,
        },
        "source_write": False,
        "source_body": evidence.source if tier == "EXISTING_READABLE" else None,
        "metrics": {
            "decoded_native_instructions": len(evidence.native),
            "represented_ir_operations": len(analysis["operations"]),
            "raw_native_operations": sum(1 for item in analysis["operations"] if item["family"] == "RAW_NATIVE"),
            "resolved_direct_calls": len(analysis["calls"]["resolved_direct"]),
            "unresolved_direct_calls": len(analysis["calls"]["unresolved_direct"]),
            "resolved_field_accesses": sum(1 for item in analysis["operations"] if item.get("field")),
            "unique_resolved_fields": len(analysis["fields"]),
            "unresolved_field_accesses": len(analysis["unresolved_field_accesses"]),
            "branch_targets": len(analysis["branch_facts"]),
        },
    }
    return record, emit_sidecar_source(record, analysis)


def clear_generated_subtrees(root: Path) -> None:
    resolved_root = root.resolve()
    resolved_out = OUT_ROOT.resolve()
    if not resolved_root.is_relative_to(resolved_out):
        raise RuntimeError(f"Refusing to clear generation root outside {OUT_ROOT}: {root}")
    for name in ("representations", "ir", "csharp-sidecars", "provenance", "cohorts", "reports"):
        target = root / name
        if target.exists():
            shutil.rmtree(target)
    root.mkdir(parents=True, exist_ok=True)


def tree_digest(root: Path, names: Iterable[str]) -> str:
    digest = hashlib.sha256()
    for name in names:
        base = root / name
        if not base.exists():
            continue
        for path in sorted(base.rglob("*")):
            if path.is_file():
                rel = path.relative_to(root).as_posix()
                digest.update(rel.encode("utf-8"))
                digest.update(sha256_file(path).encode("ascii"))
    return digest.hexdigest()


def emit_bundle(canonical: CanonicalEvidence, sample: dict[str, list[dict[str, Any]]], root: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    clear_generated_subtrees(root)
    contract_source = CONTRACT_PATH.read_text(encoding="utf-8")
    (root / "csharp-sidecars").mkdir(parents=True, exist_ok=True)
    (root / "csharp-sidecars" / "Methods").mkdir(parents=True, exist_ok=True)
    for name in ("representations", "ir", "provenance", "cohorts", "reports"):
        (root / name).mkdir(parents=True, exist_ok=True)
    (root / "csharp-sidecars" / "TwinNativeIrContract.cs").write_text(contract_source, encoding="utf-8", newline="\n")
    address_index: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for row in canonical.rows:
        address = parse_int(row.get("isil_native_address"))
        if address is not None:
            address_index[address].append(row)

    records: list[dict[str, Any]] = []
    sidecar_classes: list[str] = []
    for cohort in COHORT_ORDER:
        cohort_records: list[dict[str, Any]] = []
        for row in sorted(sample[cohort], key=lambda item: str(item["method_id"])):
            record, source = build_record(canonical, row, cohort, address_index)
            records.append(record)
            cohort_records.append(record)
            class_name = safe_identifier(record["method_id"])
            sidecar_classes.append(class_name)
            (root / "csharp-sidecars" / "Methods" / f"{class_name}.cs").write_text(source, encoding="utf-8", newline="\n")
            write_json(root / "representations" / f"{record['method_id']}.json", record)
            write_json(root / "ir" / f"{record['method_id']}.json", {
                "schema_version": "t1-0-twin-native-ir-ops-v1",
                "method_id": record["method_id"],
                "representation_tier": record["representation_tier"],
                "operations": record["typed_ir_operations"],
                "isil": record["isil_range"],
                "accounting": record["accounting"],
            })
            write_json(root / "provenance" / f"{record['method_id']}.json", record["provenance"])
        write_json(root / "cohorts" / f"{cohort}.json", {
            "schema_version": "t1-0-cohort-v1",
            "cohort": cohort,
            "count": len(cohort_records),
            "method_ids": [record["method_id"] for record in cohort_records],
            "ownership": dict(sorted(Counter(record["identity"]["ownership"] for record in cohort_records).items())),
            "tiers": dict(sorted(Counter(record["representation_tier"] for record in cohort_records).items())),
        })

    index_lines = [
        "using SocialDev.T1Pilot;",
        "",
        "namespace SocialDev.T1Pilot.Generated",
        "{",
        "    public static class TwinSidecarIndex",
        "    {",
        f"        public static int Count {{ get {{ return {len(sidecar_classes)}; }} }}",
        "        public static TwinNativeIrMethod[] BuildAll()",
        "        {",
        "            return new TwinNativeIrMethod[]",
        "            {",
    ]
    index_lines.extend(f"                {class_name}.Build()," for class_name in sidecar_classes)
    index_lines.extend(["            };", "        }", "    }", "}", ""])
    (root / "csharp-sidecars" / "SidecarIndex.cs").write_text("\n".join(index_lines), encoding="utf-8", newline="\n")

    instruction_lines = "".join(json.dumps(record["accounting"], ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n" for record in sorted(records, key=lambda item: item["method_id"]))
    (root / "reports" / "instruction-conservation.jsonl").write_text(instruction_lines, encoding="utf-8", newline="\n")
    summary = summarize_records(records)
    write_json(root / "reports" / "canonical-500-summary.json", summary)
    write_json(root / "reports" / "sample-manifest.json", [
        {
            "cohort": record["cohort"],
            "method_id": record["method_id"],
            "assembly": record["identity"]["assembly"],
            "ownership": record["identity"]["ownership"],
            "declaring_type": record["identity"]["declaring_type"],
            "method_name": record["identity"]["method_name"],
            "signature": record["identity"]["signature"],
            "status": record["status_before_representation"],
            "tier": record["representation_tier"],
            "native_instructions": record["native_range"]["instruction_count"],
        }
        for record in sorted(records, key=lambda item: item["method_id"])
    ])
    return records, summary


def summarize_records(records: list[dict[str, Any]]) -> dict[str, Any]:
    native_counts = [record["native_range"]["instruction_count"] for record in records if record["native_range"]["instruction_count"] > 0]
    native_counts.sort()
    raw_count = sum(record["metrics"]["raw_native_operations"] for record in records)
    return {
        "schema_version": "t1-0-full-body-generation-pivot-pilot-v1",
        "sample_count": len(records),
        "representation_coverage": {
            "total": len(records),
            "emitted": sum(1 for record in records if record["representation_emitted"]),
            "missing": sum(1 for record in records if not record["representation_emitted"]),
        },
        "tier_counts": dict(sorted(Counter(record["representation_tier"] for record in records).items())),
        "cohort_counts": dict(sorted(Counter(record["cohort"] for record in records).items())),
        "native_facts": {
            "total_decoded_instructions": sum(record["accounting"]["decoded_native_instruction_count"] for record in records),
            "total_represented_instructions": sum(record["accounting"]["represented_ir_operation_count"] for record in records),
            "total_omitted_instructions": sum(record["accounting"]["omitted_operation_count"] for record in records),
            "total_extra_ir_operations": sum(record["accounting"]["extra_ir_operation_count"] for record in records),
            "catalog_count_conventions": dict(sorted(Counter(record["accounting"]["count_convention"] for record in records).items())),
            "resolved_direct_calls": sum(record["metrics"]["resolved_direct_calls"] for record in records),
            "unresolved_direct_calls": sum(record["metrics"]["unresolved_direct_calls"] for record in records),
            "resolved_field_accesses": sum(record["metrics"]["resolved_field_accesses"] for record in records),
            "unresolved_field_accesses": sum(record["metrics"]["unresolved_field_accesses"] for record in records),
            "branch_targets": sum(record["metrics"]["branch_targets"] for record in records),
            "raw_unknown_operations": raw_count,
        },
        "complexity": {
            "native_backed_method_count": len(native_counts),
            "median_instructions": statistics.median(native_counts) if native_counts else 0,
            "p90_instructions": native_counts[max(0, math.ceil(len(native_counts) * 0.90) - 1)] if native_counts else 0,
            "p99_instructions": native_counts[max(0, math.ceil(len(native_counts) * 0.99) - 1)] if native_counts else 0,
            "max_instructions": max(native_counts) if native_counts else 0,
        },
        "high_level_quality": {
            "source_oracle_exact": sum(record["high_level_quality"] == "SOURCE_ORACLE_EXACT" for record in records),
            "structural_confirmed": sum(record["high_level_quality"] == "STRUCTURAL_CONFIRMED" for record in records),
            "rejected": sum(record["high_level_quality"] not in {"SOURCE_ORACLE_EXACT", "STRUCTURAL_CONFIRMED"} for record in records),
        },
        "method_identity_coverage": sum(bool(record["identity"]["method_id"] and record["identity"]["declaring_type"] and record["identity"]["signature"] and record["identity"]["metadata_token"]) for record in records),
        "provenance_coverage": sum(bool(record["provenance"].get("provenance_id") and record["provenance"].get("evidence_refs")) for record in records),
        "native_range_accounted": sum(bool(record["accounting"]["range_accounted"]) for record in records),
    }


def load_negative_fixtures(attached_pack: Path) -> dict[str, Any]:
    sources: list[dict[str, Any]] = []
    r3_path = ROOT / "knowledge" / "brain" / "acceptance" / "r3-whole-game-cfg-repair" / "r3-negative-fixture-validation.json"
    r4_path = ROOT / "artifacts" / "r4-0-evidence-pack" / "R4_0_NATIVE_IR_CSHARP_PILOT_EVIDENCE_PACK" / "negative" / "google-r2-negative-repair-fixtures.json"
    if r3_path.is_file():
        payload = json.loads(r3_path.read_text(encoding="utf-8"))
        sources.extend({"source": relative_path(r3_path), "fixture": item, "decision": "REJECTED_NEGATIVE_FIXTURE"} for item in payload.get("results", []))
    if r4_path.is_file():
        payload = json.loads(r4_path.read_text(encoding="utf-8"))
        sources.extend({"source": relative_path(r4_path), "fixture": item, "decision": "REJECTED_NEGATIVE_FIXTURE"} for item in payload.get("fixtures", []))
    attached_audit = None
    if attached_pack.is_file():
        extracted = OUT_ROOT / "input-pack" / "T1_0_FULL_BODY_GENERATION_PIVOT_PILOT_PACK" / "negative" / "google-r4-adversarial-audit.json"
        if extracted.is_file():
            attached_audit = json.loads(extracted.read_text(encoding="utf-8"))
    return {
        "schema_version": "t1-0-google-negative-audit-v1",
        "fixture_count": len(sources),
        "fixtures": sources,
        "attached_adversarial_audit": attached_audit,
        "all_rejected": bool(sources) and all(item["decision"] == "REJECTED_NEGATIVE_FIXTURE" for item in sources),
        "policy": "Google-derived packs are adversarial evidence only; no candidate is promoted by template similarity.",
    }


def false_positive_audit(records: list[dict[str, Any]], negatives: dict[str, Any]) -> dict[str, Any]:
    placeholder_hits: list[dict[str, Any]] = []
    for record in records:
        checked = {
            "fields": record["fields"],
            "calls": record["calls"],
            "high_level_csharp": record.get("high_level_csharp"),
        }
        hits = contains_placeholder(checked)
        if hits:
            placeholder_hits.append({"method_id": record["method_id"], "names": hits})
    metadata_field_failures = [
        {"method_id": record["method_id"], "field": field}
        for record in records
        for field in record["fields"]
        if not field.get("declaring_type") or field.get("offset_value") is None or not field.get("provenance")
    ]
    direct_call_failures = [
        {"method_id": record["method_id"], "call": call}
        for record in records
        for call in record["calls"]["resolved_direct"]
        if not call.get("callee_method_id") or not call.get("provenance")
    ]
    return {
        "schema_version": "t1-0-false-positive-audit-v1",
        "negative_fixture_count": negatives["fixture_count"],
        "negative_fixtures_rejected": negatives["all_rejected"],
        "placeholder_names_forbidden": sorted(PLACEHOLDER_NAMES),
        "placeholder_hits": placeholder_hits,
        "metadata_field_identity_failures": metadata_field_failures,
        "resolved_direct_call_identity_failures": direct_call_failures,
        "false_positive_count": len(placeholder_hits) + len(metadata_field_failures) + len(direct_call_failures),
        "pass": negatives["all_rejected"] and not placeholder_hits and not metadata_field_failures and not direct_call_failures,
    }


def run_sidecar_compile(root: Path) -> dict[str, Any]:
    pwsh = DEFAULT_PWSH if DEFAULT_PWSH.is_file() else Path(shutil.which("pwsh") or "")
    if not pwsh or not pwsh.is_file():
        return {"schema_version": "t1-0-sidecar-compile-v1", "parse_pass": False, "compile_pass": False, "error": "bundled PowerShell host not found"}
    assembly = root / "reports" / "SocialDev.T1Pilot.Sidecars.dll"
    command = [
        str(pwsh), "-NoLogo", "-NoProfile", "-File", str(COMPILE_SCRIPT),
        "-ProjectRoot", str(root / "csharp-sidecars"),
        "-OutputAssembly", str(assembly),
        "-RoslynRoot", str(DEFAULT_ROSLYN_ROOT),
    ]
    process = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
    output = process.stdout.strip().splitlines()
    result: dict[str, Any]
    try:
        result = json.loads(output[-1]) if output else {}
    except json.JSONDecodeError:
        result = {"schema_version": "t1-0-sidecar-compile-v1", "parse_pass": False, "compile_pass": False, "raw_output": process.stdout, "raw_error": process.stderr}
    result["exit_code"] = process.returncode
    result["command"] = command
    if process.stderr.strip():
        result["stderr"] = process.stderr
    return result


def attached_pack_summary(attached_pack: Path) -> dict[str, Any]:
    if not attached_pack.is_file():
        return {"path": str(attached_pack), "present": False}
    return {
        "path": str(attached_pack),
        "present": True,
        "sha256": sha256_file(attached_pack),
        "bytes": attached_pack.stat().st_size,
        "advisory_only": True,
    }


def report_markdown(result: dict[str, Any]) -> str:
    summary = result["summary"]
    tiers = ", ".join(f"{key}={value}" for key, value in sorted(summary["tier_counts"].items()))
    native = summary["native_facts"]
    complexity = summary["complexity"]
    decision = result["decision"]
    lines = [
        "# T1.0 Full-Body Generation Pivot Pilot",
        "",
        f"Decision: `{decision['decision']}`",
        f"Token: `{decision['go_token'] or decision['no_go_token']}`",
        "",
        "This is a sidecar-only canonical 500-method pilot. It does not overwrite the Twin source, the read-only C# roots, Unity/V8 runtime code, or the original evidence roots.",
        "",
        "## Cohort composition",
        "",
        *[f"- `{cohort}`: {summary['cohort_counts'].get(cohort, 0)}" for cohort in COHORT_ORDER],
        "- Ownership: " + ", ".join(f"{key}={value}" for key, value in sorted(result["cohort_metrics"]["overall_ownership"].items())),
        "",
        "## Representation and conservation",
        "",
        f"- Coverage: {summary['representation_coverage']['emitted']}/{summary['representation_coverage']['total']} emitted; missing={summary['representation_coverage']['missing']}",
        f"- Tiers: {tiers}",
        f"- Native instructions decoded: {native['total_decoded_instructions']}",
        f"- Native instructions represented: {native['total_represented_instructions']}",
        f"- Omitted instructions: {native['total_omitted_instructions']} (all selected native-backed methods explain the catalog convention)",
        f"- Resolved direct calls: {native['resolved_direct_calls']}; unresolved direct calls: {native['unresolved_direct_calls']}",
        f"- Resolved field accesses: {native['resolved_field_accesses']}; unresolved field accesses: {native['unresolved_field_accesses']}",
        f"- Branch targets: {native['branch_targets']}; raw native fallback operations: {native['raw_unknown_operations']}",
        "",
        "## Complexity and semantic quality",
        "",
        f"- Native-backed complexity: median={complexity['median_instructions']}, p90={complexity['p90_instructions']}, p99={complexity['p99_instructions']}, max={complexity['max_instructions']}",
        f"- High-level quality: source-oracle exact={summary['high_level_quality']['source_oracle_exact']}, structural confirmed={summary['high_level_quality']['structural_confirmed']}, rejected/deferred to IR={summary['high_level_quality']['rejected']}",
        f"- Extreme cohort: {result['cohort_metrics']['extreme_min_instructions']}–{result['cohort_metrics']['extreme_max_instructions']} native instructions",
        "",
        "## Verification",
        "",
        f"- Sidecar Roslyn parse: {'PASS' if result['compile'].get('parse_pass') else 'FAIL'}",
        f"- Sidecar analysis assembly compile: {'PASS' if result['compile'].get('compile_pass') else 'FAIL'}",
        f"- Deterministic replay: {'PASS' if result['replay']['deterministic'] else 'FAIL'}",
        f"- Google negative fixtures: {'REJECTED' if result['false_positive']['negative_fixtures_rejected'] else 'FAIL'}; false-positive count={result['false_positive']['false_positive_count']}",
        f"- Source mutation: {'YES' if not result['source_unchanged'] else 'NO'}",
        "",
        "## Boundary",
        "",
        "No 10,827-method generation, T2 compile factory, semantic uplift, runtime change, or legacy R4 mass lift was started by this pilot.",
        f"Next authorized phase on GO: `{decision['next_authorized_phase']}`.",
        "",
    ]
    return "\n".join(lines)


def write_acceptance(result: dict[str, Any]) -> None:
    ACCEPTANCE_ROOT.mkdir(parents=True, exist_ok=True)
    compact = {
        "source-gate.json": result["source_gate"],
        "attached-pack.json": result["attached_pack"],
        "cohort-composition.json": result["cohort_metrics"],
        "representation-summary.json": result["summary"],
        "instruction-conservation.json": {
            "native_facts": result["summary"]["native_facts"],
            "all_native_ranges_accounted": result["summary"]["native_range_accounted"] == 500,
            "omitted_operation_count": result["summary"]["native_facts"]["total_omitted_instructions"],
        },
        "high-level-quality.json": result["summary"]["high_level_quality"],
        "false-positive-audit.json": result["false_positive"],
        "sidecar-compile.json": result["compile"],
        "deterministic-replay.json": result["replay"],
        "final-decision.json": result["decision"],
    }
    for name, value in compact.items():
        write_json(ACCEPTANCE_ROOT / name, value)
    write_json(ACCEPTANCE_ROOT / "sample-manifest.json", result["sample_manifest"])
    (ACCEPTANCE_ROOT / "report.md").write_text(report_markdown(result), encoding="utf-8", newline="\n")


def run_pilot(attached_pack: Path) -> dict[str, Any]:
    source_before = source_tree_digest(ROOT / "knowledge" / "sources" / "csharp_raw_20260813" / "1_Click_CSharp_Code")
    source_gate = verify_source_gate()
    if source_gate.get("status") != "PASS":
        raise RuntimeError("Pinned source identity gate failed; generation stopped")
    canonical = CanonicalEvidence()
    canonical_type_count = sum(1 for line in TYPE_CATALOG_PATH.read_text(encoding="utf-8").splitlines() if line.strip() and json.loads(line).get("ownership") in {"GAME_FIRST_PARTY", "KAIRO_ENGINE"})
    if len(canonical.rows) != EXPECTED_METHODS or canonical_type_count != EXPECTED_TYPES:
        raise RuntimeError("Canonical R1.5 universe does not match the expected 641-type/10,827-method authority")

    sample, selection_metrics = select_canonical_sample(canonical)
    records, summary = emit_bundle(canonical, sample, OUT_ROOT)
    pass_two_root = OUT_ROOT / "replay" / "pass-2"
    _, replay_summary = emit_bundle(canonical, sample, pass_two_root)
    replay_names = ("representations", "ir", "csharp-sidecars", "provenance", "cohorts")
    digest_one = tree_digest(OUT_ROOT, replay_names)
    digest_two = tree_digest(pass_two_root, replay_names)
    replay = {
        "schema_version": "t1-0-deterministic-replay-v1",
        "pass_one_digest": digest_one,
        "pass_two_digest": digest_two,
        "byte_identical": digest_one == digest_two,
        "pass_one_summary_digest": sha256_text(stable_json(summary)),
        "pass_two_summary_digest": sha256_text(stable_json(replay_summary)),
        "deterministic": digest_one == digest_two and stable_json(summary) == stable_json(replay_summary),
    }
    compile_result = run_sidecar_compile(OUT_ROOT)
    negatives = load_negative_fixtures(attached_pack)
    fp = false_positive_audit(records, negatives)
    source_after = source_tree_digest(ROOT / "knowledge" / "sources" / "csharp_raw_20260813" / "1_Click_CSharp_Code")
    source_unchanged = source_before == source_after

    extreme = [record for record in records if record["cohort"] == "EXTREME_COMPLEXITY"]
    extreme_counts = [record["native_range"]["instruction_count"] for record in extreme]
    overall_ownership = dict(sorted(Counter(record["identity"]["ownership"] for record in records).items()))
    cohort_metrics = {
        "schema_version": "t1-0-cohort-composition-v1",
        "cohort_counts": dict(sorted(Counter(record["cohort"] for record in records).items())),
        "cohort_ownership": dict(sorted(selection_metrics["cohort_ownership"].items())),
        "overall_ownership": overall_ownership,
        "selection_scan": {key: value for key, value in selection_metrics.items() if key != "valid_native_method_ids" and key != "valid_native_instruction_counts"},
        "extreme_min_instructions": min(extreme_counts) if extreme_counts else 0,
        "extreme_max_instructions": max(extreme_counts) if extreme_counts else 0,
    }
    identities_complete = all(
        record["identity"][key]
        for record in records
        for key in ("method_id", "assembly", "ownership", "declaring_type", "signature", "metadata_token")
    )
    provenance_complete = all(record["provenance"].get("provenance_id") and record["provenance"].get("evidence_refs") for record in records)
    native_ranges_accounted = all(record["accounting"]["range_accounted"] for record in records)
    instruction_conservation = all(
        record["accounting"]["omitted_operation_count"] == 0
        and record["accounting"]["extra_ir_operation_count"] == 0
        and record["accounting"]["represented_ir_operation_count"] == record["accounting"]["decoded_native_instruction_count"]
        for record in records
        if record["accounting"]["decoded_native_instruction_count"] > 0
    )
    extreme_gate = len(extreme_counts) == 25 and min(extreme_counts) > 160 and max(extreme_counts) >= 1000
    compile_gate = bool(compile_result.get("parse_pass") and compile_result.get("compile_pass") and compile_result.get("sidecar_method_source_count") == 500)
    gates = {
        "source_identity": source_gate.get("status") == "PASS",
        "canonical_universe": len(canonical.rows) == EXPECTED_METHODS and canonical_type_count == EXPECTED_TYPES,
        "canonical_500_cohort_shape": cohort_metrics["cohort_counts"] == COHORT_SIZES,
        "representation_coverage_500_of_500": summary["representation_coverage"] == {"total": 500, "emitted": 500, "missing": 0},
        "method_identity_coverage_500_of_500": identities_complete,
        "provenance_coverage_500_of_500": provenance_complete,
        "native_isil_range_accounted": native_ranges_accounted,
        "zero_unexplained_native_instruction_drops": instruction_conservation and summary["native_facts"]["total_omitted_instructions"] == 0,
        "sidecar_roslyn_parse_and_compile": compile_gate,
        "deterministic_replay": replay["deterministic"],
        "google_negative_fixtures_reject": fp["pass"],
        "extreme_complexity_represented": extreme_gate,
        "no_original_source_mutation": source_unchanged,
    }
    go = all(gates.values())
    decision = {
        "decision": "GO" if go else "NO-GO",
        "go_token": "PASS_T1_0_FULL_BODY_GENERATION_PIVOT_PILOT_GO" if go else None,
        "no_go_token": None if go else "BLOCKED_T1_0_FULL_BODY_GENERATION_ARCHITECTURE_REDESIGN",
        "gates": gates,
        "dominant_blockers": [name for name, passed in gates.items() if not passed],
        "representation_coverage_is_go_threshold": True,
        "high_level_semantic_rate_is_not_go_threshold": True,
        "source_mutation": False,
        "legacy_r4_status": "RETAINED_AS_ACCEPTED_EVIDENCE_HISTORY",
        "legacy_r4_execution_plan": "SUPERSEDED_BY_T1_FULL_BODY_GENERATION" if go else "RETAINED_PENDING_T1_DECISION",
        "next_authorized_phase": "T1_FULL_BODY_GENERATION" if go else None,
        "stop_after_500_method_pilot": True,
    }
    result = {
        "schema_version": "t1-0-full-body-generation-pivot-pilot-result-v1",
        "source_gate": source_gate,
        "attached_pack": attached_pack_summary(attached_pack),
        "summary": summary,
        "cohort_metrics": cohort_metrics,
        "false_positive": fp,
        "compile": compile_result,
        "replay": replay,
        "source_unchanged": source_unchanged,
        "decision": decision,
        "sample_manifest": [
            {
                "method_id": record["method_id"],
                "cohort": record["cohort"],
                "ownership": record["identity"]["ownership"],
                "declaring_type": record["identity"]["declaring_type"],
                "method_name": record["identity"]["method_name"],
                "tier": record["representation_tier"],
                "native_instruction_count": record["native_range"]["instruction_count"],
                "status": record["status_before_representation"],
            }
            for record in sorted(records, key=lambda item: item["method_id"])
        ],
    }
    write_json(OUT_ROOT / "reports" / "false-positive-audit.json", fp)
    write_json(OUT_ROOT / "reports" / "deterministic-replay.json", replay)
    write_json(OUT_ROOT / "reports" / "sidecar-compile.json", compile_result)
    write_json(OUT_ROOT / "reports" / "final-decision.json", decision)
    write_acceptance(result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("source-gate", "all"), nargs="?", default="all")
    parser.add_argument("--attached-pack", type=Path, default=DEFAULT_ATTACHED_PACK)
    args = parser.parse_args()
    if args.command == "source-gate":
        print(stable_json(verify_source_gate()), end="")
        return 0
    result = run_pilot(args.attached_pack)
    print(stable_json(result), end="")
    return 0 if result["decision"]["decision"] == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
