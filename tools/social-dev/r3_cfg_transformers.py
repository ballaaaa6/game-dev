"""Strict family-first R3 CFG transformer planner.

The actual syntax rewrite is implemented in the Roslyn-backed
``TwinRepair.Core.R3CfgTransformers`` class.  This Python layer consumes the
canonical evidence bundles, applies the proof preconditions, and emits a
deterministic no-write plan.  It never mutates source or treats a regex match
as a rewrite proof.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


EXACT_SOURCE_MAPPINGS = {
    "EXACT_R1_5_LINE_SPAN_BODY_HASH",
    "EXACT_R1_5_EXPRESSION_BODY_HASH",
    "BODY_HASH_MATCH_WITH_NONSTANDARD_SPAN",
}


FAMILY_SPECS: dict[str, dict[str, Any]] = {
    "LOCAL_GOTO_BRANCH_CFG": {
        "implemented": True,
        "preconditions": [
            "exact R1.5 source identity and body hash",
            "unique ISIL signature selection and branch-target facts",
            "Roslyn semantic binding proof before and after",
            "graph-equivalence proof for every control transfer",
        ],
        "forbidden": [
            "multiple incoming gotos",
            "indirect or computed branch targets",
            "protected-region boundary changes",
            "syntax-only or visual graph improvement",
        ],
        "rewrite": "Roslyn SyntaxNode rewrite of a proven redundant immediate label/goto only",
        "negative_fixture_requirements": [
            "identifier binding",
            "local type evidence",
            "semantic diagnostics",
            "generic conversion proof",
        ],
    },
    "LOOP_CFG_COLLAPSE": {
        "implemented": False,
        "preconditions": ["exact loop header, back-edge, exit, and dominance proof"],
        "forbidden": ["loop reconstruction from goto count alone", "unknown break/continue targets"],
        "rewrite": "deferred; no proven transformer",
        "negative_fixture_requirements": [],
    },
    "SWITCH_OR_JUMP_TABLE_COLLAPSE": {
        "implemented": False,
        "preconditions": ["complete jump-table case mapping and default-target proof"],
        "forbidden": ["case ordering guesses", "fall-through inference without ISIL proof"],
        "rewrite": "deferred; no proven transformer",
        "negative_fixture_requirements": [],
    },
    "TRY_FINALLY_CFG_COLLAPSE": {
        "implemented": False,
        "preconditions": ["protected-region, exceptional-edge, and exit equivalence proof"],
        "forbidden": ["moving statements across catch/finally boundaries"],
        "rewrite": "deferred; no proven transformer",
        "negative_fixture_requirements": [],
    },
    "TYPE_EROSION_PLUS_HEAVY_GOTO": {
        "implemented": False,
        "preconditions": ["separate local-type proof and complete CFG proof"],
        "forbidden": ["declaring-type substitution", "identifier renaming without binding"],
        "rewrite": "deferred; no proven transformer",
        "negative_fixture_requirements": [],
    },
    "DECOMPILER_TYPE_CFG_DAMAGE": {
        "implemented": False,
        "preconditions": ["type/data-flow proof independent of CFG normalization"],
        "forbidden": ["object-temporary replacement by declaring type"],
        "rewrite": "deferred; no proven transformer",
        "negative_fixture_requirements": [],
    },
    "SWITCH_STRUCTURAL_DAMAGE": {
        "implemented": False,
        "preconditions": ["Roslyn switch structure and ISIL jump-table equivalence"],
        "forbidden": ["switch reconstruction from syntax shape alone"],
        "rewrite": "deferred; no proven transformer",
        "negative_fixture_requirements": [],
    },
    "STRUCTURED_CONTROL_SUSPECT": {
        "implemented": False,
        "preconditions": ["structured-control hypothesis plus native control-flow proof"],
        "forbidden": ["treating a suspect classification as a repair authorization"],
        "rewrite": "deferred; no proven transformer",
        "negative_fixture_requirements": [],
    },
    "OTHER_CFG": {
        "implemented": False,
        "preconditions": ["new family specification and independent equivalence proof"],
        "forbidden": ["generic remove-goto or generic CFG cleanup"],
        "rewrite": "forbidden in R3",
        "negative_fixture_requirements": [],
    },
}

for _family, _spec in FAMILY_SPECS.items():
    _spec.setdefault("isil_facts", [
        "unique method-block selection",
        "control-transfer sequence",
        "branch targets and protected-region facts",
    ])
    _spec.setdefault("cfg_signature", {
        "before": "canonical source CFG plus exact ISIL control-transfer facts",
        "after": "same exits, calls, field/static references, and protected regions",
        "conservation_required": True,
    })
    _spec.setdefault("positive_fixtures", ["Roslyn self-test"] if _family == "LOCAL_GOTO_BRANCH_CFG" else [])
    _spec.setdefault("negative_fixtures", ["tools/social-dev/r3_negative_repair_fixtures.json"] if _family == "LOCAL_GOTO_BRANCH_CFG" else [])
    _spec.setdefault("deterministic_replay", [
        "replay the same evidence bundle and require byte-identical plan output",
        "replay the Roslyn SyntaxNode rewrite and require identical normalized source",
    ])


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def plan_row(row: dict[str, Any]) -> dict[str, Any]:
    family = row.get("cfg_family", "OTHER_CFG")
    spec = FAMILY_SPECS.get(family, FAMILY_SPECS["OTHER_CFG"])
    identity = row.get("source_mapping") in EXACT_SOURCE_MAPPINGS and row.get("source_body_sha256") == row.get("body_sha256")
    isil = row.get("isil_facts", {}).get("selection_status") == "EXACT_SIGNATURE_UNIQUE"
    semantic = row.get("roslyn", {}).get("semantic_diagnostics_available") is True
    graph = row.get("graph_equivalence_proof") is True
    if not identity:
        reason = "EXACT_SOURCE_IDENTITY_REQUIRED"
    elif not isil:
        reason = "EXACT_ISIL_SELECTION_REQUIRED"
    elif not semantic:
        reason = "SEMANTIC_BINDING_PROOF_UNAVAILABLE"
    elif not graph:
        reason = "GRAPH_EQUIVALENCE_PROOF_REQUIRED"
    elif not spec["implemented"]:
        reason = "FAMILY_TRANSFORMER_NOT_PROVEN"
    else:
        reason = "ROSlyn_ENGINE_INVOCATION_REQUIRED"
    return {
        "method_id": row["method_id"],
        "cfg_family": family,
        "structural_risk": row.get("structural_risk"),
        "eligible": False,
        "status": "DEFERRED_NO_CANARY",
        "reason": reason,
        "identity_proven": identity,
        "isil_selection_proven": isil,
        "semantic_binding_proven": semantic,
        "graph_equivalence_proven": graph,
        "source_mutation_performed": False,
    }


def plan(profile_path: Path) -> dict[str, Any]:
    rows = read_jsonl(profile_path)
    decisions = [plan_row(row) for row in sorted(rows, key=lambda row: row["method_id"])]
    family_counts: dict[str, Counter[str]] = defaultdict(Counter)
    reason_counts = Counter()
    for decision in decisions:
        family_counts[decision["cfg_family"]][decision["reason"]] += 1
        reason_counts[decision["reason"]] += 1
    return {
        "schema_version": "r3-transformer-plan-v1",
        "status": "PASS" if all(not decision["eligible"] for decision in decisions) else "FAIL",
        "active_cfg_count": len(decisions),
        "planned_eligible_count": sum(decision["eligible"] for decision in decisions),
        "accepted_repair_count": 0,
        "source_mutation_performed": False,
        "semantic_proof_required": True,
        "rewrite_engine": "TwinRepair.Core.R3CfgTransformers",
        "rewrite_mode": "Roslyn SyntaxNode; no regex or text splice",
        "families": {
            family: {
                "active_count": sum(counter.values()),
                "implemented": FAMILY_SPECS.get(family, FAMILY_SPECS["OTHER_CFG"])["implemented"],
                "reason_counts": dict(sorted(counter.items())),
                "spec": FAMILY_SPECS.get(family, FAMILY_SPECS["OTHER_CFG"]),
            }
            for family, counter in sorted(family_counts.items())
        },
        "reason_counts": dict(sorted(reason_counts.items())),
        "decisions": decisions,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Plan R3 family-first CFG transforms")
    parser.add_argument("--profile", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    result = plan(Path(args.profile))
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({key: result[key] for key in (
        "status", "active_cfg_count", "planned_eligible_count", "accepted_repair_count", "reason_counts"
    )}, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
