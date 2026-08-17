"""Regression checks for chair_00 through chair_04 structure comparison."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
AUDIT = ROOT / "knowledge/sources/phase3a_apk_probe/chair_structure_comparison.json"


def main() -> int:
    value = json.loads(AUDIT.read_text(encoding="utf-8"))
    assert value["schema_version"] == "social-dev-phase3a-chair-structure-comparison-v1"
    assert set(value["chairs"]) == {"chair_00", "chair_01", "chair_02", "chair_03", "chair_04"}
    patterns = value["patterns"]
    assert patterns["all_opt_headers_exact"] is True
    assert patterns["all_opt_payloads_consume_exactly"] is True
    assert patterns["all_seb_headers_exact"] is True
    assert patterns["all_seb_frame_scaffolds_exact_except_image_id"] is True
    assert ["chair_00", "chair_01"] in patterns["opt_exact_sha_groups"]
    assert patterns["png_dimensions_by_chair"] == {
        "chair_00": [34, 15],
        "chair_01": [34, 15],
        "chair_02": [14, 41],
        "chair_03": [18, 55],
        "chair_04": [20, 10],
    }
    assert patterns["seb_image_ids_by_chair"] == {
        "chair_00": [4, 4, 4],
        "chair_01": [31, 31, 31],
        "chair_02": [112, 112, 112],
        "chair_03": [121, 121, 121],
        "chair_04": [144, 144, 144],
    }
    assert patterns["opt_piece_count_patterns"] == {
        "chair_00": [1, 2, 1],
        "chair_01": [1, 2, 1],
        "chair_02": [1, 1, 1],
        "chair_03": [1, 1, 1],
        "chair_04": [1, 2, 0],
    }
    assert value["classification"]["pixel_only_variation"]["status"] == "false"
    assert value["classification"]["chair_00_recovery_from_own_bytes"]["status"] == "verified"
    assert value["classification"]["chair_00_recovery_from_other_opt"]["status"] == "not_supported"
    print("phase3a_chair_structures_test_passed chairs=5 shared_seb_scaffold=true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
