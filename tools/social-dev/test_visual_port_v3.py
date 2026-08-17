"""Static acceptance gate for V3 resource-group evidence."""

from __future__ import annotations

import hashlib
import json
import sys
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "knowledge" / "fixtures" / "accepted"
V3 = EVIDENCE / "visual-port" / "v3"
ZIP_PATH = ROOT / "sources" / "raw" / "Social_Dev_Story_v2.5.1_ASSETS_ONLY_WITH_ASSEMBLY_GUIDE.zip"
ZIP_ROOT = "Social_Dev_Story_v2.5.1_ASSETS_ONLY/"
APP_DATA = ROOT / "knowledge/sources/csharp_raw_20260813" / "1_Click_CSharp_Code" / "main" / "AppData.cs"

REQUIRED = [
    "resource-group-map.json",
    "pack-inventory.json",
    "img-index-contract.json",
    "seb-index-contract.json",
    "resource-manager-layout.json",
    "load-semantics.json",
    "image-seb-association.json",
    "group-coverage.json",
    "fixture-manifest.json",
    "native-recovery-map.json",
    "unknowns.json",
    "checkpoint-ledger.json",
]

GROUP_IDS = [
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


def load(name: str) -> dict:
    return json.loads((V3 / name).read_text(encoding="utf-8"))


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def stable_hash(value: dict) -> str:
    clone = json.loads(json.dumps(value, ensure_ascii=False))
    clone.get("determinism", {}).pop("content_hash", None)
    payload = json.dumps(clone, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return sha256_bytes(payload.encode("utf-8"))


def fail(message: str) -> None:
    raise AssertionError(message)


def main() -> None:
    acceptance = json.loads((EVIDENCE / "visual-port" / "v2" / "v2-static-acceptance.json").read_text(encoding="utf-8"))
    assert acceptance["status"] == "PASS_STATIC"
    assert acceptance["v2_entry_gate_for_v3"] == "PASS"
    assert acceptance["accepted_for_v3"] is True
    assert acceptance["pixel_parity"] == "DEFERRED_TO_V7"

    records = {name: load(name) for name in REQUIRED}
    for name, record in records.items():
        expected = record.get("determinism", {}).get("content_hash")
        assert isinstance(expected, str) and len(expected) == 64, f"missing determinism hash: {name}"
        assert stable_hash(record) == expected, f"determinism mismatch: {name}"

    archive_sha256 = sha256_bytes(ZIP_PATH.read_bytes())
    assert archive_sha256 == "c4b6ac1b6603eb8e2d7ac78e7dd3b8bffb40b7c30fe036cb644bea701087b283"
    assert records["pack-inventory.json"]["archive"]["sha256"] == archive_sha256
    assert records["img-index-contract.json"]["archive_sha256"] == archive_sha256
    assert records["seb-index-contract.json"]["archive_sha256"] == archive_sha256

    group_map = records["resource-group-map.json"]
    assert group_map["declared_group_ids"] == GROUP_IDS
    assert "global manifest" in group_map["authority"]
    groups = {group["group_id"]: group for group in group_map["groups"]}
    assert set(groups) == set(GROUP_IDS)
    assert groups["resInterface_"]["source_pack"] is None
    assert groups["resInterface_"]["proof_class"] == "DECLARED_ONLY"
    for group_id in GROUP_IDS:
        prefix = f"RES{group_id.removeprefix('res').removesuffix('_').upper()}_"
        if group_id == "resAvatarBody_":
            prefix = "RESAVATAR_BODY_"
        if group_id == "resAvatarHead_":
            prefix = "RESAVATAR_HEAD_"
        if group_id == "resInterface_":
            continue
        assert prefix in APP_DATA.read_text(encoding="utf-8"), f"missing AppData namespace: {prefix}"

    with zipfile.ZipFile(ZIP_PATH) as archive:
        names = set(archive.namelist())
        for contract_name, kind in (("img-index-contract.json", "img"), ("seb-index-contract.json", "seb")):
            for group in records[contract_name]["groups"]:
                assert group["group_id"] in GROUP_IDS
                assert group["source_index_member"] in names or ZIP_ROOT + group["source_index_member"] in names
                ids = [entry["id"] for entry in group["entries"]]
                assert ids == sorted(ids) and len(ids) == len(set(ids))
                assert group["count"] == len(ids)
                assert group["max_id"] == max(ids)
                expected_gaps = [identifier for identifier in range(group["max_id"] + 1) if identifier not in set(ids)]
                assert group["gap_ids"] == expected_gaps
                for entry in group["entries"]:
                    member = ZIP_ROOT + entry["source_member"]
                    assert member in names, f"missing source member: {member}"
                    assert entry["source_sha256"] == sha256_bytes(archive.read(member))

        fixtures = records["fixture-manifest.json"]["fixtures"]
        required_fixture_ids = {
            "resChip_:chair_00",
            "resChip_:desk_00",
            "resChip_:wall_00",
            "resChip_:door_02",
            "resHuman_:wait_left",
            "resCom_:wnd_conner",
            "resGame_:cloud_day",
            "resEffect_:effect00",
            "resMeeting_:hit_effect",
            "resAvatarBody_:wait_right",
            "resAvatarHead_:face_m_00",
            "resDevelop_:enemy_attack_timing",
            "resWindow_:install_bonus",
        }
        fixture_ids = {fixture["fixture_id"] for fixture in fixtures}
        assert required_fixture_ids <= fixture_ids
        for fixture in fixtures:
            image = fixture["image"]
            if image["source_member"] is not None:
                image_member = ZIP_ROOT + image["source_member"]
                assert image_member in names
                assert image["source_sha256"] == sha256_bytes(archive.read(image_member))
            seb = fixture["seb"]
            if seb["source_member"] is not None:
                seb_member = ZIP_ROOT + seb["source_member"]
                assert seb_member in names
                assert seb["source_sha256"] == sha256_bytes(archive.read(seb_member))

    association = records["image-seb-association.json"]
    assert association["cross_group_exceptions"] == []
    for item in association["associations"]:
        assert item["status"].startswith("PROVEN_SAME_PACK_INDEX_NAMESPACE")
        for binding in item["tex_id_bindings"]:
            assert binding["image_index_status"] in {"SOURCE_INDEXED", "SENTINEL"}
            if binding["image_index_status"] == "SOURCE_INDEXED":
                assert binding["same_pack"] is True
    assert any(binding["image_index_status"] == "SENTINEL" for item in association["associations"] for binding in item["tex_id_bindings"])

    coverage = records["group-coverage.json"]
    for category in ("PROVEN_SOURCE_INDEXED", "PROVEN_NATIVE", "PROVEN_BOTH", "DECLARED_ONLY", "UNRESOLVED_SOURCE_MEMBER", "SENTINEL", "ABSENT", "DEFERRED"):
        assert category in coverage["coverage_categories"]
    assert records["unknowns.json"]["v3_entry_blocking"] is False
    ledger = records["checkpoint-ledger.json"]
    assert ledger["status"] == "PASS_STATIC_V3_STOP_BEFORE_V4"
    assert [checkpoint["id"] for checkpoint in ledger["checkpoints"]] == [f"V3.{index}" for index in range(0, 11)]
    assert all(checkpoint["status"] in {"PASS", "PASS_WITH_ASYNC_DEFERRED", "PASS_WITH_DEFERRED_PATHS"} for checkpoint in ledger["checkpoints"])
    assert records["resource-manager-layout.json"]["native_object_fields"]["img"]["offset"] == "this+0x10"
    assert records["resource-manager-layout.json"]["native_object_fields"]["seb"]["offset"] == "this+0x18"
    assert records["resource-manager-layout.json"]["native_object_fields"]["CustomImages"]["offset"] == "this+0x60"
    assert records["native-recovery-map.json"]["execution_policy"]["runtime_execution_used"] is False
    assert records["native-recovery-map.json"]["execution_policy"]["adb_or_emulator_used"] is False
    print("visual_port_v3_evidence_passed")


if __name__ == "__main__":
    try:
        main()
    except (AssertionError, KeyError, OSError, ValueError) as error:
        print(f"visual_port_v3_evidence_failed: {error}", file=sys.stderr)
        raise
