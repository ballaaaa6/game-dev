"""Regression checks for the R3 family-first transformer plan."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from r3_cfg_transformers import FAMILY_SPECS, plan


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the R3 transformer plan")
    parser.add_argument("--profile", required=True)
    parser.add_argument("--plan", required=True)
    args = parser.parse_args()
    generated = plan(Path(args.profile))
    recorded = json.loads(Path(args.plan).read_text(encoding="utf-8"))
    if generated["active_cfg_count"] != 2856:
        raise AssertionError(f"unexpected active CFG count: {generated['active_cfg_count']}")
    if generated["planned_eligible_count"] != 0 or generated["accepted_repair_count"] != 0:
        raise AssertionError("R3 planner must not authorize an unproven canary")
    if generated["status"] != "PASS" or not generated["semantic_proof_required"]:
        raise AssertionError("R3 transformer proof gate failed")
    if recorded["reason_counts"] != generated["reason_counts"]:
        raise AssertionError("recorded transformer plan is not deterministic")
    if sum(family["active_count"] for family in generated["families"].values()) != 2856:
        raise AssertionError("family counts do not cover the active CFG universe")
    if "OTHER_CFG" in generated["families"] and generated["families"]["OTHER_CFG"]["implemented"]:
        raise AssertionError("OTHER_CFG cannot be an automatic transformer family")
    if set(generated["families"]) - set(FAMILY_SPECS):
        raise AssertionError("unclassified CFG family appeared in the active plan")
    print(json.dumps({
        "status": "PASS",
        "active_cfg_count": generated["active_cfg_count"],
        "planned_eligible_count": generated["planned_eligible_count"],
        "accepted_repair_count": generated["accepted_repair_count"],
        "families": {name: data["active_count"] for name, data in generated["families"].items()},
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
