"""Regression checks for the exact chair_00 variable-piece reconstruction."""

from __future__ import annotations

import json
from pathlib import Path

from build_phase3a_chair_00_reconstruction import build_audit


ROOT = Path(__file__).resolve().parents[2]
AUDIT_PATH = ROOT / "knowledge/sources/phase3a_apk_probe/chair_00_reconstruction_audit.json"


def without_dynamic(value):
    if isinstance(value, str):
        return value.replace(
            "knowledge/social-dev/evidence/", "knowledge/sources/"
        ).replace(
            "social dev/", "sources/raw/"
        )
    if isinstance(value, dict):
        return {
            key: without_dynamic(item)
            for key, item in value.items()
            if key not in {"generated_at_utc", "content_hash"}
        }
    if isinstance(value, list):
        return [without_dynamic(item) for item in value]
    return value


def main() -> int:
    audit = json.loads(AUDIT_PATH.read_text(encoding="utf-8"))
    rebuilt = build_audit()
    assert audit["schema_version"] == "social-dev-phase3a-chair-00-reconstruction-v1"
    assert audit["parser"]["cell_piece_counts"] == [1, 2, 1]
    assert audit["parser"]["record_count"] == 4
    assert audit["parser"]["partial_tail_bytes"] == 0
    assert audit["parser"]["errors"] == []
    assert audit["reconstruction"]["status"] == "pass"
    assert audit["reconstruction"]["logical_size"] == [180, 32]
    assert audit["reconstruction"]["pixel_sha256"] == "23d8e732fa2000f18f8fd9649b5fbe2b190d95aff86475b8befd09cfbe8afeef"
    assert audit["validation"]["all_chip_opt_payloads"]["all_pass"] is True
    assert audit["validation"]["known_chip_logical_references"]["all_exact"] is True
    assert audit["validation"]["known_chip_logical_references"]["tested"] == 89
    assert audit["validation"]["known_chip_logical_references"]["exact_pixel_matches"] == 89
    assert audit["decision"] == {
        "exact_source_reconstruction": True,
        "speculative_pixels_added": False,
        "donor_opt_coordinates_used": False,
        "runtime_promotion": True,
    }
    assert without_dynamic(audit) == without_dynamic(rebuilt)
    print("phase3a_chair_00_reconstruction_test_passed cells=1,2,1 references=89 runtime_promotion=true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
