"""Deterministic checks for APK-derived Phase 3A chair evidence."""

from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "knowledge/sources/phase3a_apk_probe"
AUDIT_PATH = EVIDENCE / "chair_extraction_audit.json"
ZIP_PATH = ROOT / "sources/raw/Social_Dev_Story_v2.5.1_ASSETS_ONLY_WITH_ASSEMBLY_GUIDE.zip"
ARCHIVE_PREFIX = "Social_Dev_Story_v2.5.1_ASSETS_ONLY/"


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def main() -> int:
    audit = json.loads(AUDIT_PATH.read_text(encoding="utf-8"))
    assert audit["schema_version"] == "social-dev-phase3a-apk-chair-extraction-v1"
    assert audit["decryption"]["text_asset_name"] == "chip"
    assert audit["decryption"]["decrypted_sha256"] == "98175857839ced6784ba7cba3560a962bf8fe8fab251d901dda291bdb5b4817e"
    assert audit["pack"]["file_count"] == 333
    assert audit["selected_stems"] == ["chair_00", "chair_01", "chair_02", "chair_03", "chair_04"]

    with zipfile.ZipFile(ZIP_PATH) as archive:
        for stem in audit["selected_stems"]:
            records = audit["selected_assets"][stem]["assets"]
            assert set(records) == {"png", "opt", "seb"}
            for extension, record in records.items():
                # The extracted audit is preserved byte-for-byte under the read-only
                # source root; resolve its historical pre-promotion path to the
                # canonical source namespace when opening the promoted copy.
                output_path = record["output_path"].replace(
                    "knowledge/social-dev/evidence/", "knowledge/sources/"
                )
                path = ROOT / output_path
                raw = path.read_bytes()
                source = archive.read(ARCHIVE_PREFIX + record["source_zip_member"])
                assert raw == source
                assert record["matches_source_zip"] is True
                assert record["extracted_size"] == len(raw)
                assert record["extracted_sha256"] == sha256(raw)
                assert record["source_zip_sha256"] == sha256(source)

        assert audit["selected_assets"]["chair_00"]["semantic_validation"]["opt"]["partial_tail_bytes"] == 0
        assert audit["selected_assets"]["chair_00"]["semantic_validation"]["opt"]["piece_counts"] == [1, 2, 1]
        assert audit["selected_assets"]["chair_00"]["semantic_validation"]["reconstruction"]["status"] == "pass"
        assert audit["selected_assets"]["chair_01"]["semantic_validation"]["opt"]["partial_tail_bytes"] == 0
        assert audit["selected_assets"]["chair_01"]["semantic_validation"]["opt"]["piece_counts"] == [1, 2, 1]
        assert audit["selected_assets"]["chair_01"]["semantic_validation"]["reconstruction"]["status"] == "pass"
        assert audit["selected_assets"]["chair_02"]["semantic_validation"]["opt"]["status"] == "pass"
        assert audit["selected_assets"]["chair_03"]["semantic_validation"]["opt"]["status"] == "pass"
        assert audit["selected_assets"]["chair_04"]["semantic_validation"]["opt"]["piece_counts"] == [1, 2, 0]
        assert audit["selected_assets"]["chair_04"]["semantic_validation"]["reconstruction"]["status"] == "pass"

    print("phase3a_apk_chair_extraction_test_passed assets=15 exact_zip_match=true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
