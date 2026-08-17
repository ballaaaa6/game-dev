"""Regression checks for the three-version chair APK comparison."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "knowledge/sources/phase3a_apk_probe/chair_version_comparison.json"


def main() -> int:
    audit = json.loads(EVIDENCE.read_text(encoding="utf-8"))
    assert audit["disposition"]["status"] == "version_comparison_complete"
    assert set(audit["versions"]) == {"2.4.9", "2.5.0", "2.5.1"}
    comparison = audit["comparison"]
    assert comparison["all_three_chip_plaintexts_exact"] is True
    assert comparison["all_three_selected_triplets_exact"] is True
    assert comparison["all_15_outputs_match_reference_zip_in_each_version"] is True
    assert comparison["all_three_pack_file_counts"] == [333]
    assert comparison["classification"]["extraction_or_container_bug"] == "ruled_out_for_selected_triplets"
    assert comparison["classification"]["chair_00_01_source_bytes_exact_in_all_three_builds"] is True
    assert comparison["classification"]["chair_00_01_variable_piece_reconstruction_passes"] is True

    for version in audit["versions"].values():
        for stem in ("chair_00", "chair_01"):
            semantic = version["selected_assets"][stem]["semantic_validation"]
            assert semantic["opt"]["size_bytes"] == 63
            assert semantic["opt"]["partial_tail_bytes"] == 0
            assert semantic["opt"]["piece_counts"] == [1, 2, 1]
            assert semantic["reconstruction"]["status"] == "pass"
        for stem in ("chair_02", "chair_03"):
            semantic = version["selected_assets"][stem]["semantic_validation"]
            assert semantic["opt"]["status"] == "pass"
            assert semantic["reconstruction"]["status"] == "pass"
        chair_04 = version["selected_assets"]["chair_04"]["semantic_validation"]
        assert chair_04["opt"]["size_bytes"] == 49
        assert chair_04["opt"]["status"] == "pass"
        assert chair_04["opt"]["piece_counts"] == [1, 2, 0]
        assert chair_04["reconstruction"]["status"] == "pass"

    print("phase3a_chair_apk_versions_test_passed versions=3 pack_entries=333 triplets=15")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
