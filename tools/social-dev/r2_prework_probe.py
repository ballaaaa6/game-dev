#!/usr/bin/env python3
import argparse
import collections
import hashlib
import json
import pathlib


SAFE_TYPE_RULE = {
    "source_match_status": "EXACT_TYPE",
    "max_body_lines": 40,
    "max_control_flow_signal": 2,
    "max_inferred_type_signal": 2,
    "native_signal": 0,
    "static_data_signal": 0,
}


def read_jsonl(path):
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def dump_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    parser = argparse.ArgumentParser(description="R2 advisory profiler for the canonical R1.5 queue")
    parser.add_argument("--artifact-root", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    root = pathlib.Path(args.artifact_root)
    out = pathlib.Path(args.out)
    methods = read_jsonl(root / "method-catalog.jsonl")
    queue = read_jsonl(root / "repair-queue.jsonl")
    by_id = {method["method_id"]: method for method in methods}

    profile = {
        "schema_version": "r2-prework-profile-v1",
        "input_root": str(root),
        "input_files": {
            "method-catalog.jsonl": sha256(root / "method-catalog.jsonl"),
            "repair-queue.jsonl": sha256(root / "repair-queue.jsonl"),
        },
        "method_count": len(methods),
        "queue_count": len(queue),
        "ownership": dict(collections.Counter(method.get("ownership") for method in methods)),
        "quality": dict(collections.Counter(method.get("quality_class") for method in methods)),
        "disposition": dict(collections.Counter(method.get("repair_disposition") for method in methods)),
        "source_match": dict(collections.Counter(method.get("source_match_status") for method in methods)),
        "source_present": sum(bool(method.get("source_present")) for method in methods),
        "source_body_present": sum(bool(method.get("source_body_present")) for method in methods),
        "isil_available": sum(bool(method.get("isil_available")) for method in methods),
        "native_available": sum(bool(method.get("native_available")) for method in methods),
        "rva_present": sum(bool(method.get("rva")) for method in methods),
    }
    dump_json(out / "r2-alternate-queue-profile.json", profile)

    by_status = {}
    for status in sorted({method.get("source_match_status") for method in methods}):
        rows = [method for method in methods if method.get("source_match_status") == status]
        by_status[status] = {
            "count": len(rows),
            "by_disposition": dict(collections.Counter(method.get("repair_disposition") for method in rows)),
            "body_present": sum(bool(method.get("source_body_present")) for method in rows),
        }
    dump_json(out / "r2-source-match-risk.json", {
        "schema_version": "r2-prework-source-match-risk-v1",
        "note": "Advisory profile only. Canonical R2 must recompute from current R1.5 artifacts.",
        "statuses": by_status,
        "write_gate_recommendation": [
            "Never mutate a method solely from an ambiguous or missing source match.",
            "Require exact full-type + overload-safe signature mapping before any source rewrite.",
            "Resolve ambiguity with Roslyn/metadata; do not use deterministic-first matching as repair authority.",
        ],
    })

    type_rows = []
    for queue_row in queue:
        if queue_row.get("repair_disposition") != "AUTO_TYPE_REPAIR":
            continue
        method = by_id[queue_row["method_id"]]
        signals = method.get("r0_signals") or {}
        exact = method.get("source_match_status") == "EXACT_TYPE"
        safe = (
            exact
            and (method.get("body_lines") or 10**9) <= 40
            and signals.get("control_flow", 999) <= 2
            and signals.get("inferred_type", 999) <= 2
            and signals.get("native_signal", 0) == 0
            and signals.get("static_data", 0) == 0
        )
        if not exact:
            tier = "BLOCKED_SOURCE_AMBIGUITY"
            reason = "source_match_status is not EXACT_TYPE"
        elif safe:
            tier = "SAFE_CANARY"
            reason = "exact source mapping + small body + low control-flow signal + type-only degradation signal"
        else:
            tier = "REVIEW_WAVE_2"
            reason = "type-repair label is plausible but body/control-flow complexity exceeds conservative canary gate"
        type_rows.append({
            "method_id": method["method_id"],
            "assembly": method["assembly"],
            "ownership": method["ownership"],
            "declaring_type": method["declaring_type"],
            "method_name": method["method_name"],
            "normalized_signature": method["normalized_signature"],
            "source_file": method.get("source_file"),
            "source_line": method.get("source_line"),
            "source_line_end": method.get("source_line_end"),
            "source_match_status": method.get("source_match_status"),
            "body_lines": method.get("body_lines"),
            "signals": signals,
            "dependency_layer": method.get("dependency_layer"),
            "tier": tier,
            "reason": reason,
            "evidence_refs": method.get("evidence_refs", []),
        })
    type_summary = {
        "schema_version": "r2-prework-auto-type-safety-v1",
        "rule": SAFE_TYPE_RULE,
        "total": len(type_rows),
        "tiers": dict(collections.Counter(row["tier"] for row in type_rows)),
        "methods": type_rows,
        "important": "This is a conservative advisory split, not permission to patch without Roslyn/metadata proof.",
    }
    dump_json(out / "r2-auto-type-safety.json", type_summary)

    cfg = [method for method in methods if method.get("repair_disposition") == "CFG_REPAIR"]

    def control_flow(method):
        return (method.get("r0_signals") or {}).get("control_flow", 999)

    cfg_counts = {
        "all_cfg": len(cfg),
        "exact_source": sum(method.get("source_match_status") == "EXACT_TYPE" for method in cfg),
        "tiny_body_le_10_exact": sum(method.get("source_match_status") == "EXACT_TYPE" and (method.get("body_lines") or 999999) <= 10 for method in cfg),
        "heuristic_small_le_20_cf_le_3_exact": sum(method.get("source_match_status") == "EXACT_TYPE" and (method.get("body_lines") or 999999) <= 20 and control_flow(method) <= 3 for method in cfg),
        "heuristic_medium_le_40_cf_le_6_exact": sum(method.get("source_match_status") == "EXACT_TYPE" and (method.get("body_lines") or 999999) <= 40 and control_flow(method) <= 6 for method in cfg),
    }
    dump_json(out / "r2-cfg-complexity-profile.json", {
        "schema_version": "r2-prework-cfg-profile-v1",
        "counts": cfg_counts,
        "policy": "These are candidate complexity buckets only. Small does not mean semantically safe. R2 may repair CFG only when a deterministic pattern proves equivalence; otherwise defer to R3.",
    })

    disposition_exact = {}
    for disposition in sorted({method.get("repair_disposition") for method in methods}):
        rows = [method for method in methods if method.get("repair_disposition") == disposition]
        disposition_exact[disposition] = {
            "count": len(rows),
            "exact_source": sum(method.get("source_match_status") == "EXACT_TYPE" for method in rows),
            "ambiguous_source": sum(method.get("source_match_status") == "AMBIGUOUS_DETERMINISTIC_FIRST" for method in rows),
            "missing_source": sum(method.get("source_match_status") == "MISSING" for method in rows),
            "body_present": sum(bool(method.get("source_body_present")) for method in rows),
        }
    dump_json(out / "r2-disposition-source-coverage.json", {
        "schema_version": "r2-prework-disposition-source-coverage-v1",
        "rows": disposition_exact,
    })

    with (out / "r2-type-canary-methods.jsonl").open("w", encoding="utf-8") as handle:
        for row in sorted((row for row in type_rows if row["tier"] == "SAFE_CANARY"), key=lambda row: row["method_id"]):
            handle.write(json.dumps(row, sort_keys=True) + "\n")

    print(json.dumps({"status": "PASS", "methods": len(methods), "queue": len(queue), "type_tiers": type_summary["tiers"], "cfg": cfg_counts}, indent=2))


if __name__ == "__main__":
    raise SystemExit(main())
