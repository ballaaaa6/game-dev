"""Regression checks for the non-authoritative chair_00 visual variants."""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
AUDIT_PATH = ROOT / "knowledge/sources/phase3a_apk_probe/chair_variants/chair_00_variant_audit.json"
RUNTIME = ROOT / "runtime/social-dev"


def main() -> int:
    audit = json.loads(AUDIT_PATH.read_text(encoding="utf-8"))
    assert audit["schema_version"] == "social-dev-phase3a-chair-00-derived-variants-v1"
    assert audit["decision_boundary"] == {
        "source_bytes_changed": False,
        "original_chair_00_opt_repaired": False,
        "runtime_manifest_changed": False,
        "all_variants_are_derived_approximations": True,
        "exact_game_visual_recovery": False,
    }
    assert audit["known_chair_00_data"]["applied_source_records"] == [0, 1]
    assert audit["known_chair_00_data"]["duplicated_logical_cell"] == 0
    assert audit["chair_02_complete_reference"]["matches_supplied_derived_reference"] is True
    assert audit["evaluation"]["overall"]["best_functional_demo"] == "variant_2_chair_02_substitute"
    assert audit["evaluation"]["overall"]["best_source_identity"] == "variant_1_known_plus_duplicate_but_not_complete"
    assert audit["evaluation"]["overall"]["exact_chair_00_recovery"] == "not_achieved"
    assert set(audit["variants"]) == {
        "variant_1_known_plus_duplicate",
        "variant_2_chair_02_substitute",
        "variant_3_known_plus_chair_02_missing_cell",
    }
    for record in audit["variants"].values():
        preview_path = record["path"].replace(
            "knowledge/social-dev/evidence/", "knowledge/sources/"
        )
        path = ROOT / preview_path
        assert path.is_file()
        assert Image.open(path).size == (180, 32)
        assert record["authoritative_source"] is False
        assert record["runtime_promoted"] is False
    assert all(
        (RUNTIME / "assets/display-slice-01/01_GAME_PACKS/chip" / f"chair_00.{extension}").is_file()
        for extension in ("png", "opt", "seb")
    )
    print("phase3a_chair_00_variants_test_passed variants=3 historical_approximations=true exact_runtime_source=true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
