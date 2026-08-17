"""Red evidence-contract checks for the V1 visual format recovery artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import zipfile


ROOT = Path(__file__).resolve().parents[2]
V1 = ROOT / "knowledge/fixtures/accepted/visual-port/v1"
REQUIRED = (
    "sprite-contract.json",
    "seb-contract.json",
    "image-opt-contract.json",
    "resource-lookup-contract.json",
    "fixture-manifest.json",
    "native-recovery-map.json",
    "parity-results.json",
    "unknowns.json",
)
TASK2_REQUIRED = (
    "seb-contract.json",
    "image-opt-contract.json",
    "fixture-manifest.json",
)
REPORTS = (
    "V1_CORE_FORMAT_RECOVERY.md",
    "V1_FIXTURE_MATRIX.md",
    "V1_NATIVE_RECOVERY.md",
    "V1_PARITY_REPORT.md",
)
REPORTS_ROOT = ROOT / "docs" / "Phases" / "VisualPort"
APK_SHA256 = "fa0e9e3a843732258fc05b2611a8e0f5be6f7e95f2141a53f31fb082322fe2bf"
DUMP_SHA256 = "4487CBA6916E159AFEFEC2CD1A9ECF0D12D05B2D76126E7099A5D35323967EB2"
EXPECTED_GROUP_IDS = [
    "resChip_",
    "resInterface_",
    "resHuman_",
    "resCom_",
    "resGame_",
    "resEffect_",
    "resMeeting_",
    "resAvatarBody_",
    "resAvatarHead_",
    "resDevelop_",
    "resWindow_",
]

EXPECTED_MEMBERS = {
    "simple_one_layer": "01_GAME_PACKS/chip/door_02.seb",
    "multi_layer": "01_GAME_PACKS/chip/wall_00.seb",
    "multi_frame": "01_GAME_PACKS/chip/chair_00.seb",
    "translation": "01_GAME_PACKS/chip/desk_00.seb",
    "flip": "01_GAME_PACKS/human/wait_left.seb",
    "furniture": "01_GAME_PACKS/chip/chair_00.seb",
    "character": "01_GAME_PACKS/avatar_body/wait_right.seb",
}


def load_artifacts(required: tuple[str, ...]) -> dict[str, object]:
    missing = [name for name in required if not (V1 / name).is_file()]
    assert not missing, f"missing V1 evidence: {missing}"
    return {
        name: json.loads((V1 / name).read_text(encoding="utf-8")) for name in required
    }


def load_task2() -> dict[str, object]:
    return load_artifacts(TASK2_REQUIRED)


def load_required() -> dict[str, object]:
    """Load the complete V1 gate; this intentionally remains the default mode."""

    return load_artifacts(REQUIRED)


def stable_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def assert_content_hash(data: dict[str, object]) -> None:
    copied = json.loads(json.dumps(data))
    determinism = copied["determinism"]
    determinism["content_hash"] = ""
    assert hashlib.sha256(stable_json(copied).encode("utf-8")).hexdigest() == data["determinism"]["content_hash"]


def _assert_v1_evidence_has_required_fixture_categories(data: dict[str, object]) -> None:
    categories = set(data["fixture-manifest.json"]["fixtures"])
    assert {
        "simple_one_layer",
        "multi_layer",
        "multi_frame",
        "translation",
        "furniture",
        "character",
    } <= categories


def _assert_fixture_members_are_real_source_members(data: dict[str, object]) -> None:
    manifest = data["fixture-manifest.json"]
    records = manifest["fixture_records"]
    by_category = {item["category"]: item for item in records}
    archive_path = ROOT / manifest["source"]["zip_path"]
    assert hashlib.sha256(archive_path.read_bytes()).hexdigest() == manifest["source"]["zip_sha256"]
    prefix = manifest["source"]["archive_prefix"]
    with zipfile.ZipFile(archive_path) as archive:
        members = set(archive.namelist())
        for category, member in EXPECTED_MEMBERS.items():
            fixture = by_category[category]
            assert fixture["source_member"] == member
            assert len(fixture["source_sha256"]) == 64
            assert f"{prefix}{member}" in members
            assert hashlib.sha256(archive.read(f"{prefix}{member}")).hexdigest() == fixture["source_sha256"]


def _assert_task2_contracts(data: dict[str, object]) -> None:
    fixture = data["fixture-manifest.json"]
    seb = data["seb-contract.json"]
    image_opt = data["image-opt-contract.json"]
    for contract in (fixture, seb, image_opt):
        assert contract["status"] == "pass"
        assert_content_hash(contract)

    assert fixture["unknown_register"] == []
    assert seb["unknown_register"] == []
    assert {record["source_member"] for record in seb["records"]} == set(EXPECTED_MEMBERS.values())
    assert all(record["decoded"]["status"] == "pass" for record in seb["records"])
    assert all(record["source_image_association"]["status"] == "PROVEN" for record in seb["records"])

    expected_stems = {
        "01_GAME_PACKS/chip/chair_00",
        "01_GAME_PACKS/chip/chair_02",
        "01_GAME_PACKS/chip/desk_00",
        "01_GAME_PACKS/chip/door_02",
    }
    assert {record["fixture_stem"] for record in image_opt["records"]} == expected_stems
    for record in image_opt["records"]:
        assert len(record["source_png"]["raw_sha256"]) == 64
        assert len(record["source_opt"]["raw_sha256"]) == 64
        assert record["source_png"]["runtime_promotion"]["status"] == "PROMOTED_EXACT"
        assert record["source_opt"]["runtime_promotion"]["status"] == "PROMOTED_EXACT"
        assert record["logical_reconstruction"]["status"] == "pass"
        assert record["logical_reconstruction"]["pixel_sha256"]
        assert record["logical_reconstruction"]["opt"]["cells"]
        assert record["logical_runtime_promotion"]["status"] == "PROMOTED_PIXEL_EXACT"


def run_task2(data: dict[str, object]) -> None:
    _assert_v1_evidence_has_required_fixture_categories(data)
    _assert_fixture_members_are_real_source_members(data)
    _assert_task2_contracts(data)


def _assert_v1_unknown_register_has_required_columns(data: dict[str, object]) -> None:
    unknowns = data["unknowns.json"]
    assert {"schema_version", "unknowns"} <= set(unknowns)
    for item in unknowns["unknowns"]:
        assert {
            "id",
            "class",
            "method",
            "question",
            "known_evidence",
            "missing_evidence",
            "affected_fixtures",
            "impact",
            "next_investigation",
        } <= set(item)


def _assert_full_v1_evidence(data: dict[str, object]) -> None:
    for artifact in data.values():
        assert artifact["schema_version"]
        assert artifact["status"]
        assert artifact.get("source") or artifact.get("source_refs")
        assert artifact["determinism"]["algorithm"] == "stable-json-sha256 excluding determinism.content_hash"
        assert re.fullmatch(r"[0-9a-f]{64}", artifact["determinism"]["content_hash"])
        assert_content_hash(artifact)

    run_task2(data)
    _assert_v1_unknown_register_has_required_columns(data)

    sprite = data["sprite-contract.json"]
    assert len(sprite["fields"]) == 14
    assert sprite["native_conversion"]["native_rva"] == "0x1C5CE64"
    assert sprite["native_conversion"]["apk_sha256"] == APK_SHA256
    assert sprite["native_conversion"]["dump_sha256"] == DUMP_SHA256

    seb = data["seb-contract.json"]
    assert seb["geometry_contract"]["bounds_formula"]["proof_class"].startswith("FORMAT-PROVEN")
    assert seb["geometry_contract"]["depth_contract"]["status"] == "deferred"
    assert seb["interpreter_contract"]["typescript_boundary"]["accepted_decoder_status"] == "pass"
    assert seb["geometry_contract"]["depth_contract"]["unknowns"]

    image_opt = data["image-opt-contract.json"]
    assert len(image_opt["records"]) == 4
    assert all(record["logical_runtime_promotion"]["status"] == "PROMOTED_PIXEL_EXACT" for record in image_opt["records"])

    resource = data["resource-lookup-contract.json"]
    assert resource["group_ids"] == EXPECTED_GROUP_IDS
    assert resource["atlas_contract"]["status"] == "deferred"
    assert resource["native_contract"]["get_image_rva"] == "0x1C53DA0"

    native = data["native-recovery-map.json"]
    assert native["apk_sha256"] == APK_SHA256
    assert native["dump_sha256"] == DUMP_SHA256
    assert len(native["records"]) >= 26
    for record in native["records"]:
        assert re.search(r"0x[0-9A-Fa-f]+", record["native_rva"])
        assert record["apk_sha256"] == APK_SHA256
        assert record["dump_sha256"] == DUMP_SHA256
        assert isinstance(record["fixture_refs"], list)
        assert record["fixture_refs"]
        assert record["csharp_ref"]
        assert record["proof_class"]
        assert record["method"]

    parity = data["parity-results.json"]
    assert parity["status"] == "pass"
    assert parity["parity_results"]
    for result in parity["parity_results"]:
        assert result["test"]
        assert result["expected_hash"] == result["actual_hash"]
        assert re.fullmatch(r"[0-9a-f]{64}", result["actual_hash"])
        assert result["status"] == "PASS"
    assert {
        (boundary["source_member"], boundary["status"])
        for boundary in parity["boundaries"]
    } >= {
        ("01_GAME_PACKS/develop/develop_menu_light.seb", "NON_SELECTED_UNSUPPORTED")
    }

    for report_name in REPORTS:
        report_path = REPORTS_ROOT / report_name
        assert report_path.is_file(), f"missing V1 report: {report_name}"
        report = report_path.read_text(encoding="utf-8")
        assert "V1" in report
        assert re.search(r"deferred|unknown", report, re.IGNORECASE)
        assert "V2" in report
        assert not re.search(r"(?:depth|atlas|resize|optimizeSeb).*is proven", report, re.IGNORECASE)


def test_v1_evidence_has_required_fixture_categories() -> None:
    _assert_v1_evidence_has_required_fixture_categories(load_required())


def test_fixture_members_are_real_source_members() -> None:
    _assert_fixture_members_are_real_source_members(load_task2())


def test_task2_contracts() -> None:
    _assert_task2_contracts(load_task2())


def test_v1_unknown_register_has_required_columns() -> None:
    _assert_v1_unknown_register_has_required_columns(load_required())


def test_v1_full_evidence() -> None:
    _assert_full_v1_evidence(load_required())


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task2", action="store_true", help="validate only the Task 2 fixture, SEB, and OPT contracts")
    args = parser.parse_args(argv)
    if args.task2:
        run_task2(load_task2())
        print("visual_port_v1_task2_passed")
        return 0

    data = load_required()
    _assert_full_v1_evidence(data)
    print("visual_port_v1_evidence_passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
