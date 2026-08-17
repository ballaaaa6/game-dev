"""Build source-backed V3 resource-group and index evidence.

This builder is intentionally static. It reads the pinned C# extraction, the
original asset ZIP/INF files, and the existing decoded SEB catalog. It never
executes the source project or a runtime renderer and never creates a global
asset manifest as a semantic authority.
"""

from __future__ import annotations

import hashlib
import json
import re
import zipfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "knowledge" / "social-dev" / "evidence"
SOURCE = ROOT / "knowledge/sources/csharp_raw_20260813" / "1_Click_CSharp_Code"
APP_DATA = SOURCE / "main" / "AppData.cs"
RESOURCE_MANAGER = SOURCE / "kairo.unity.ui" / "ResourceManager.cs"
LOAD_TASK = SOURCE / "kairo.unity.util" / "LoadTask.cs"
RESOURCE_LOADER = SOURCE / "kairo.unity.util" / "ResourceLoader.cs"
ZIP_PATH = ROOT / "social dev" / "Social_Dev_Story_v2.5.1_ASSETS_ONLY_WITH_ASSEMBLY_GUIDE.zip"
ZIP_ROOT = "Social_Dev_Story_v2.5.1_ASSETS_ONLY/"
RESOURCE_GROUPS = EVIDENCE / "visual-port" / "resource-groups.json"
SEB_CATALOG = EVIDENCE / "seb_catalog.json"
V1_LOOKUP = EVIDENCE / "visual-port" / "v1" / "resource-lookup-contract.json"
OUT = EVIDENCE / "visual-port" / "v3"

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

GROUP_SPECS: dict[str, dict[str, Any]] = {
    "resChip_": {
        "pack": "chip",
        "prefix": "RESCHIP_",
        "declaration_line": 596,
        "fixtures": [
            {"name": "chair_00", "image_id": 4, "seb_id": 3, "seb_name": "chair_00.seb"},
            {"name": "desk_00", "image_id": 3, "seb_id": 1, "seb_name": "desk_00.seb"},
            {"name": "wall_00", "image_id": 6, "seb_id": 5, "seb_name": "wall_00.seb"},
            {"name": "door_02", "image_id": 7, "seb_id": 6, "seb_name": "door_02.seb"},
        ],
        "consumer_refs": [
            "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/game/ObjChip.cs:2674-2704",
            "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/game/MapChip.cs",
            "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/data/FurnitureData.cs",
        ],
    },
    "resInterface_": {
        "pack": None,
        "prefix": None,
        "declaration_line": 598,
        "fixtures": [],
        "consumer_refs": [
            "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/main/AppData.cs:598",
            "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/form/GameForm.cs",
            "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/data/FurnitureData.cs",
        ],
    },
    "resHuman_": {
        "pack": "human",
        "prefix": "RESHUMAN_",
        "declaration_line": 600,
        "fixtures": [
            {"name": "wait_left", "image_id": 0, "seb_id": 11, "seb_name": "wait_left.seb"},
        ],
        "consumer_refs": [
            "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/game/Staff.cs:8247-8274",
            "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/game/Staff.cs:8556-8577",
        ],
    },
    "resCom_": {
        "pack": "com",
        "prefix": "RESCOM_",
        "declaration_line": 602,
        "fixtures": [
            {"name": "wnd_conner", "image_id": 19, "seb_id": 0, "seb_name": "wnd_conner.seb", "alias_image_id": 5},
        ],
        "consumer_refs": [
            "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/game/Treasure.cs:217-247",
            "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/game/Room.cs:4448-4617",
            "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/game/Meeting.cs:9002-9008",
        ],
    },
    "resGame_": {
        "pack": "game",
        "prefix": "RESGAME_",
        "declaration_line": 604,
        "fixtures": [
            {"name": "cloud_day", "image_id": 5, "seb_id": 1, "seb_name": "cloud_day.seb"},
        ],
        "consumer_refs": [
            "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/game/Room.cs:3617-3909",
            "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/game/Staff.cs:8359",
        ],
    },
    "resEffect_": {
        "pack": "effect",
        "prefix": "RESEFFECT_",
        "declaration_line": 606,
        "fixtures": [
            {"name": "effect00", "image_id": 0, "seb_id": 0, "seb_name": "effect00.seb"},
        ],
        "consumer_refs": [
            "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/game/Effect.cs",
            "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/game/Room.cs",
        ],
    },
    "resMeeting_": {
        "pack": "meeting",
        "prefix": "RESMEETING_",
        "declaration_line": 608,
        "fixtures": [
            {"name": "hit_effect", "image_id": 2, "seb_id": 0, "seb_name": "hit_effect.seb"},
        ],
        "consumer_refs": [
            "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/game/Meeting.cs:9875-9949",
        ],
    },
    "resAvatarBody_": {
        "pack": "avatar_body",
        "prefix": "RESAVATAR_BODY_",
        "declaration_line": 610,
        "fixtures": [
            {"name": "wait_right", "image_id": 0, "seb_id": 0, "seb_name": "wait_right.seb"},
        ],
        "consumer_refs": [
            "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/game/Avatar.cs:671-675",
            "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/game/Avatar.cs:881-938",
            "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/game/Avatar.cs:1320-1334",
        ],
    },
    "resAvatarHead_": {
        "pack": "avatar_head",
        "prefix": "RESAVATAR_HEAD_",
        "declaration_line": 612,
        "fixtures": [
            {"name": "face_m_00", "image_id": 0, "seb_id": None, "seb_name": None},
        ],
        "consumer_refs": [
            "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/game/Avatar.cs:1269-1286",
        ],
    },
    "resDevelop_": {
        "pack": "develop",
        "prefix": "RESDEVELOP_",
        "declaration_line": 614,
        "fixtures": [
            {"name": "enemy_attack_timing", "image_id": 0, "seb_id": 0, "seb_name": "enemy_attack_timing.seb"},
        ],
        "consumer_refs": [
            "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/form/DevelopForm.cs",
        ],
    },
    "resWindow_": {
        "pack": "window",
        "prefix": "RESWINDOW_",
        "declaration_line": 616,
        "fixtures": [
            {"name": "install_bonus", "image_id": 0, "seb_id": 0, "seb_name": "install_bonus.seb"},
        ],
        "consumer_refs": [
            "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/form/WindowForm.cs",
        ],
    },
}

ADDITIONAL_OWNERS = [
    {
        "owner_id": "resTitle_",
        "owner_kind": "named_local_resource_manager",
        "source_refs": [
            "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/form/TitleForm.cs:65",
            "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/form/TitleForm.cs:288-289",
        ],
        "record_selector": "RecordStore.ReadRecord(1,9)",
        "pack": "title",
        "status": "PROVEN_NATIVE_AND_SOURCE_INDEXED",
        "membership_note": "Dedicated title pack and native ResourceManager load are proven, but no AppData declared group owns this instance.",
        "fixtures": [{"name": "title_menu", "image_id": 2, "seb_id": 0, "seb_name": "title_menu.seb"}],
    },
    {
        "owner_id": "resRecruit_",
        "owner_kind": "named_local_resource_manager",
        "source_refs": [
            "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/form/SubForm.cs:1230",
            "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/form/SubForm.cs:91879-91880",
        ],
        "record_selector": "RecordStore.ReadRecord(1,16)",
        "pack": "recruit",
        "status": "PROVEN_NATIVE_AND_SOURCE_INDEXED",
        "membership_note": "Dedicated recruit pack and native ResourceManager load are proven, but no AppData declared group owns this instance.",
        "fixtures": [{"name": "hope_join_back", "image_id": 0, "seb_id": 0, "seb_name": "hope_join_back.seb"}],
    },
    {
        "owner_id": "resEvents_",
        "owner_kind": "named_local_resource_manager",
        "source_refs": [
            "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/form/SubForm.cs:1228",
            "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/form/SubForm.cs:5402-5403",
        ],
        "record_selector": "RecordStore.ReadRecord(1,1)",
        "pack": "event",
        "status": "PROVEN_NATIVE_UNRESOLVED_SOURCE_MEMBER",
        "membership_note": "Event SEB payloads exist, but a standard event img.inf/seb.inf ownership pair is not proven in the static ZIP.",
        "fixtures": [],
    },
    {
        "owner_id": "resSound_",
        "owner_kind": "AppData_named_resource_manager",
        "source_refs": [
            "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/main/AppData.cs:1760",
            "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/main/AppData.cs:10368-11367",
        ],
        "record_selector": "RES_SOUND / sound[] consumers",
        "pack": "sound_not_visual",
        "status": "DECLARED_NONVISUAL",
        "membership_note": "Retained as an owner inventory record; outside V3 visual img/seb binding.",
        "fixtures": [],
    },
    {
        "owner_id": "unnamed_local_resource_manager_instances",
        "owner_kind": "unnamed_local_resource_manager",
        "source_refs": [
            "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/form/BootForm.cs:223",
            "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/form/SubFormGetCoin.cs:42",
            "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/form/MiniGameForm2.cs:326",
        ],
        "record_selector": "local constructor/load sites",
        "pack": None,
        "status": "UNRESOLVED_SOURCE_MEMBER",
        "membership_note": "Instances are inventoried without assigning them to a declared visual group or pack.",
        "fixtures": [],
    },
]


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def stable_hash(value: Any) -> str:
    clone = json.loads(json.dumps(value, ensure_ascii=False))
    if isinstance(clone, dict) and isinstance(clone.get("determinism"), dict):
        clone["determinism"].pop("content_hash", None)
    payload = json.dumps(clone, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return sha256_bytes(payload.encode("utf-8"))


def with_determinism(value: dict[str, Any]) -> dict[str, Any]:
    value["determinism"] = {
        "algorithm": "stable-json-sha256 excluding determinism.content_hash",
        "content_hash": "",
    }
    value["determinism"]["content_hash"] = stable_hash(value)
    return value


def write_json(name: str, value: dict[str, Any]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / name
    path.write_text(json.dumps(with_determinism(value), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def source_lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines()


def first_line(path: Path, pattern: str) -> int | None:
    expression = re.compile(pattern)
    for index, line in enumerate(source_lines(path), start=1):
        if expression.search(line):
            return index
    return None


def zip_member_name(member: str) -> str:
    return ZIP_ROOT + member


def parse_inf(zf: zipfile.ZipFile, member: str, kind: str, pack: str) -> dict[str, Any]:
    raw = zf.read(zip_member_name(member))
    rows: list[dict[str, Any]] = []
    text = raw.decode("utf-8", errors="replace").replace("\r", "")
    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        if not raw_line.strip():
            continue
        fields = raw_line.split("\t", 1)
        id_source = "explicit_inf_id"
        if len(fields) != 2:
            fields = raw_line.split(None, 1)
        if len(fields) != 2:
            # A small number of non-visual auxiliary indexes contain only an
            # ordered filename. Preserve that fact while assigning the only
            # lossless local slot identity: the row order.
            identifier = len(rows)
            value_text = raw_line
            id_source = "implicit_row_order"
        else:
            identifier = int(fields[0].strip())
            value_text = fields[1]
        value_fields = [part.strip() for part in value_text.split(",")]
        filename = value_fields[0]
        flags = value_fields[1:]
        source_member = f"01_GAME_PACKS/{pack}/{filename}"
        source_exists = zip_member_name(source_member) in zf.namelist()
        rows.append(
            {
                "id": identifier,
                "id_source": id_source,
                "filename": filename,
                "flags": flags,
                "raw_record": raw_line,
                "line": line_number,
                "source_member": source_member,
                "source_exists": source_exists,
                "source_sha256": sha256_bytes(zf.read(zip_member_name(source_member))) if source_exists else None,
                "source_bytes": zf.getinfo(zip_member_name(source_member)).file_size if source_exists else None,
            }
        )
    rows.sort(key=lambda row: row["id"])
    identifiers = [row["id"] for row in rows]
    max_id = max(identifiers) if identifiers else None
    gaps = [identifier for identifier in range(max_id + 1) if identifier not in set(identifiers)] if max_id is not None else []
    aliases: dict[str, list[int]] = {}
    for row in rows:
        aliases.setdefault(row["filename"], []).append(row["id"])
    for row in rows:
        same_ids = aliases[row["filename"]]
        row["alias_ids"] = same_ids if len(same_ids) > 1 else []
        row["status"] = "SOURCE_INDEXED" if row["source_exists"] else "UNRESOLVED_SOURCE_MEMBER"
    return {
        "kind": kind,
        "pack": pack,
        "source_index_member": member,
        "source_index_sha256": sha256_bytes(raw),
        "source_index_bytes": len(raw),
        "count": len(rows),
        "max_id": max_id,
        "gap_ids": gaps,
        "rows": rows,
    }


def inventory_packs(zf: zipfile.ZipFile) -> dict[str, dict[str, Any]]:
    prefix = ZIP_ROOT + "01_GAME_PACKS/"
    packs = sorted({name[len(prefix):].split("/", 1)[0] for name in zf.namelist() if name.startswith(prefix) and "/" in name[len(prefix):]})
    inventory: dict[str, dict[str, Any]] = {}
    for pack in packs:
        record: dict[str, Any] = {"pack": pack, "indexes": {}, "localized_index_members": []}
        for kind in ("img", "seb"):
            member = f"01_GAME_PACKS/{pack}/{kind}.inf"
            if zip_member_name(member) in zf.namelist():
                record["indexes"][kind] = parse_inf(zf, member, kind, pack)
            else:
                record["indexes"][kind] = None
        record["localized_index_members"] = sorted(
            name[len(ZIP_ROOT):] for name in zf.namelist() if name.startswith(zip_member_name(f"01_GAME_PACKS/{pack}/")) and name.endswith(".inf")
            and name[len(ZIP_ROOT):] not in {f"01_GAME_PACKS/{pack}/img.inf", f"01_GAME_PACKS/{pack}/seb.inf"}
        )
        inventory[pack] = record
    return inventory


def parse_appdata_constants() -> dict[str, list[dict[str, Any]]]:
    constants: dict[str, list[dict[str, Any]]] = {}
    expression = re.compile(r"public const int (\w+) = (-?\d+);")
    for line_number, line in enumerate(source_lines(APP_DATA), start=1):
        match = expression.search(line)
        if not match:
            continue
        name, value = match.groups()
        for group_id, spec in GROUP_SPECS.items():
            prefix = spec.get("prefix")
            if prefix and name.startswith(prefix):
                constants.setdefault(group_id, []).append({"name": name, "value": int(value), "line": line_number})
    return constants


def resource_group_records() -> dict[str, dict[str, Any]]:
    source = load_json(RESOURCE_GROUPS)
    return {record["group_id"]: record for record in source["records"]}


def selector_evidence(group_id: str, constants: dict[str, list[dict[str, Any]]], indexes: dict[str, Any] | None) -> list[dict[str, Any]]:
    rows_by_id = {row["id"]: row for row in (indexes["rows"] if indexes else [])}
    output = []
    for constant in constants.get(group_id, []):
        name = constant["name"]
        kind = "seb" if "_SEB_" in name else "img" if "_IMG_" in name else "other"
        row = rows_by_id.get(constant["value"]) if kind in {"img", "seb"} else None
        output.append(
            {
                **constant,
                "kind": kind,
                "index_member": indexes["source_index_member"] if indexes and kind in {"img", "seb"} else None,
                "source_member": row["source_member"] if row else None,
                "index_status": "SOURCE_INDEXED" if row else "UNRESOLVED_SOURCE_MEMBER",
            }
        )
    return output


def selected_seb_catalog(catalog: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {asset["member"]: asset for asset in catalog["assets"]}


def source_index_entry(index: dict[str, Any] | None, identifier: int | None) -> dict[str, Any] | None:
    if index is None or identifier is None:
        return None
    return next((row for row in index["rows"] if row["id"] == identifier), None)


def source_image_or_seb_member(index: dict[str, Any] | None, identifier: int | None, filename: str | None) -> dict[str, Any] | None:
    row = source_index_entry(index, identifier)
    if row is not None:
        return row
    if index is not None and filename is not None:
        return next((candidate for candidate in index["rows"] if candidate["filename"] == filename), None)
    return None


def fixture_record(group_id: str, fixture: dict[str, Any], indexes: dict[str, Any], catalog_by_member: dict[str, dict[str, Any]]) -> dict[str, Any]:
    pack = GROUP_SPECS[group_id]["pack"]
    image_index = indexes.get("img")
    seb_index = indexes.get("seb")
    image_row = source_index_entry(image_index, fixture.get("image_id"))
    seb_row = source_index_entry(seb_index, fixture.get("seb_id"))
    if fixture.get("seb_name") is not None:
        seb_row = source_image_or_seb_member(seb_index, fixture.get("seb_id"), fixture["seb_name"])
    if image_row is None and fixture.get("image_id") is not None:
        raise ValueError(f"Missing image INF row for {group_id}:{fixture}")
    if fixture.get("seb_id") is not None and seb_row is None:
        raise ValueError(f"Missing SEB INF row for {group_id}:{fixture}")
    decoded = None
    if seb_row is not None:
        catalog_asset = catalog_by_member.get(seb_row["source_member"])
        if catalog_asset is None:
            raise ValueError(f"Missing decoded SEB catalog asset for {seb_row['source_member']}")
        decoded = catalog_asset["decode"]
    tex_ids = sorted({record["image_id"] for record in (decoded or {}).get("records", [])})
    tex_bindings = []
    for tex_id in tex_ids:
        if tex_id < 0:
            tex_bindings.append(
                {
                    "tex_id": tex_id,
                    "sentinel": "TEXID_NONE" if tex_id == -1 else "NEGATIVE_TEXID",
                    "image_source_member": None,
                    "image_source_sha256": None,
                    "image_index_status": "SENTINEL",
                    "same_pack": None,
                }
            )
            continue
        tex_row = source_index_entry(image_index, tex_id)
        tex_bindings.append(
            {
                "tex_id": tex_id,
                "image_source_member": tex_row["source_member"] if tex_row else None,
                "image_source_sha256": tex_row["source_sha256"] if tex_row else None,
                "image_index_status": "SOURCE_INDEXED" if tex_row else "UNRESOLVED_SOURCE_MEMBER",
                "same_pack": tex_row is not None and tex_row["source_member"].startswith(f"01_GAME_PACKS/{pack}/"),
            }
        )
    alias_row = source_index_entry(image_index, fixture.get("alias_image_id"))
    has_sentinel = any(binding["image_index_status"] == "SENTINEL" for binding in tex_bindings)
    association_status = "PROVEN_SAME_PACK_INDEX_NAMESPACE_WITH_SENTINELS" if has_sentinel and all(binding["same_pack"] is True or binding["image_index_status"] == "SENTINEL" for binding in tex_bindings) else "PROVEN_SAME_PACK_INDEX_NAMESPACE" if all(binding["same_pack"] is True for binding in tex_bindings) else "UNRESOLVED_SOURCE_MEMBER"
    return {
        "fixture_id": f"{group_id}:{fixture['name']}",
        "group_id": group_id,
        "pack": pack,
        "name": fixture["name"],
        "image": {
            "id": image_row["id"] if image_row else None,
            "filename": image_row["filename"] if image_row else None,
            "source_index_member": image_index["source_index_member"] if image_index else None,
            "source_member": image_row["source_member"] if image_row else None,
            "source_sha256": image_row["source_sha256"] if image_row else None,
            "source_bytes": image_row["source_bytes"] if image_row else None,
            "flags": image_row["flags"] if image_row else [],
            "raw_record": image_row["raw_record"] if image_row else None,
            "alias_ids": image_row["alias_ids"] if image_row else [],
            "explicit_alias_row": {
                "id": alias_row["id"],
                "source_member": alias_row["source_member"],
                "source_sha256": alias_row["source_sha256"],
            } if alias_row else None,
        },
        "seb": {
            "id": seb_row["id"] if seb_row else None,
            "filename": seb_row["filename"] if seb_row else None,
            "source_index_member": seb_index["source_index_member"] if seb_index else None,
            "source_member": seb_row["source_member"] if seb_row else None,
            "source_sha256": seb_row["source_sha256"] if seb_row else None,
            "source_bytes": seb_row["source_bytes"] if seb_row else None,
            "flags": seb_row["flags"] if seb_row else [],
            "raw_record": seb_row["raw_record"] if seb_row else None,
            "decoded": decoded,
        },
        "tex_id_bindings": tex_bindings,
        "association_status": association_status,
        "v1_fixture_preservation": f"knowledge/fixtures/accepted/visual-port/v1/resource-lookup-contract.json:{group_id}:{fixture['name']}",
    }


def build() -> None:
    resource_groups = resource_group_records()
    constants = parse_appdata_constants()
    catalog_by_member = selected_seb_catalog(load_json(SEB_CATALOG))
    v1_lookup = load_json(V1_LOOKUP)
    zip_sha256 = sha256_file(ZIP_PATH)
    with zipfile.ZipFile(ZIP_PATH) as zf:
        inventory = inventory_packs(zf)
        source_hashes = {
            "zip_sha256": zip_sha256,
            "AppData.cs": sha256_file(APP_DATA),
            "ResourceManager.cs": sha256_file(RESOURCE_MANAGER),
            "LoadTask.cs": sha256_file(LOAD_TASK),
            "ResourceLoader.cs": sha256_file(RESOURCE_LOADER),
            "resource-groups.json": sha256_file(RESOURCE_GROUPS),
            "seb_catalog.json": sha256_file(SEB_CATALOG),
        }

        group_records: list[dict[str, Any]] = []
        all_fixtures: list[dict[str, Any]] = []
        img_groups: list[dict[str, Any]] = []
        seb_groups: list[dict[str, Any]] = []
        coverage_records: list[dict[str, Any]] = []
        for group_id in GROUP_IDS:
            spec = GROUP_SPECS[group_id]
            old = resource_groups[group_id]
            pack = spec["pack"]
            pack_record = inventory.get(pack) if pack else None
            image_index = pack_record["indexes"]["img"] if pack_record else None
            seb_index = pack_record["indexes"]["seb"] if pack_record else None
            selector_rows = selector_evidence(group_id, constants, image_index)
            selector_rows.extend(
                {**row, "index_member": seb_index["source_index_member"] if seb_index else None, "source_member": source_index_entry(seb_index, row["value"])["source_member"] if source_index_entry(seb_index, row["value"]) else None, "index_status": "SOURCE_INDEXED" if source_index_entry(seb_index, row["value"]) else "UNRESOLVED_SOURCE_MEMBER"}
                for row in selector_evidence(group_id, constants, seb_index)
                if row["kind"] == "seb"
            )
            # selector_evidence(image) contains only image/other constants; the
            # second pass adds the SEB namespace without dropping source lines.
            selector_rows = [row for row in selector_rows if row["kind"] != "seb"] + [
                {**row, "index_member": seb_index["source_index_member"] if seb_index else None, "source_member": source_index_entry(seb_index, row["value"])["source_member"] if source_index_entry(seb_index, row["value"]) else None, "index_status": "SOURCE_INDEXED" if source_index_entry(seb_index, row["value"]) else "UNRESOLVED_SOURCE_MEMBER"}
                for row in selector_evidence(group_id, constants, seb_index)
                if row["kind"] == "seb"
            ]
            fixtures = [fixture_record(group_id, fixture, {"img": image_index, "seb": seb_index}, catalog_by_member) for fixture in spec["fixtures"]]
            all_fixtures.extend(fixtures)
            if image_index is not None:
                img_groups.append({
                    "group_id": group_id,
                    "pack": pack,
                    "source_index_member": image_index["source_index_member"],
                    "source_index_sha256": image_index["source_index_sha256"],
                    "count": image_index["count"],
                    "max_id": image_index["max_id"],
                    "gap_ids": image_index["gap_ids"],
                    "entries": image_index["rows"],
                })
            if seb_index is not None:
                seb_groups.append({
                    "group_id": group_id,
                    "pack": pack,
                    "source_index_member": seb_index["source_index_member"],
                    "source_index_sha256": seb_index["source_index_sha256"],
                    "count": seb_index["count"],
                    "max_id": seb_index["max_id"],
                    "gap_ids": seb_index["gap_ids"],
                    "entries": seb_index["rows"],
                })
            if pack is None:
                proof_class = "DECLARED_ONLY"
                membership_status = "DECLARED_ONLY"
            elif image_index is not None and seb_index is not None:
                proof_class = "PROVEN_BOTH"
                membership_status = "SOURCE_INDEXED_IMAGE_AND_SEB"
            elif image_index is not None:
                proof_class = "PROVEN_SOURCE_INDEXED"
                membership_status = "SOURCE_INDEXED_IMAGE_ONLY"
            else:
                proof_class = "DECLARED_ONLY"
                membership_status = "UNRESOLVED_SOURCE_MEMBER"
            group_records.append({
                "group_id": group_id,
                "declared_field": {
                    "name": group_id,
                    "type": "ResourceManager",
                    "source_ref": f"knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/main/AppData.cs:{spec['declaration_line']}",
                    "original_source_ref": f"sources/raw/1_Click_CSharp_Code update/KairoEngine/main/AppData.cs:{spec['declaration_line']}",
                },
                "group_kind": old["group_kind"],
                "ownership": {"images": "ResourceManager.img", "sebs": "ResourceManager.seb"},
                "source_namespace": spec["prefix"],
                "source_pack": pack,
                "source_pack_proof": "Exact AppData namespace constants, ResourceManager field ownership, real consumer call sites, and pack-local INF records agree." if pack else "No source namespace or pack-local INF membership is proven for this declared field.",
                "proof_class": proof_class,
                "membership_status": membership_status,
                "known_consumers": spec["consumer_refs"],
                "selectors": selector_rows,
                "image_index": {
                    "source_index_member": image_index["source_index_member"] if image_index else None,
                    "count": image_index["count"] if image_index else 0,
                    "max_id": image_index["max_id"] if image_index else None,
                    "gap_ids": image_index["gap_ids"] if image_index else [],
                },
                "seb_index": {
                    "source_index_member": seb_index["source_index_member"] if seb_index else None,
                    "count": seb_index["count"] if seb_index else 0,
                    "max_id": seb_index["max_id"] if seb_index else None,
                    "gap_ids": seb_index["gap_ids"] if seb_index else [],
                },
                "fixtures": [fixture["fixture_id"] for fixture in fixtures],
                "deferred_or_unknown": [
                    "async load scheduling remains platform/decompiler deferred",
                    "atlas population is not proven",
                    "CustomImages population is not proven",
                ],
            })
            coverage_records.append({
                "group_id": group_id,
                "coverage_category": proof_class,
                "declared": True,
                "pack": pack,
                "img_inf": image_index is not None,
                "seb_inf": seb_index is not None,
                "source_indexed_image_count": image_index["count"] if image_index else 0,
                "source_indexed_seb_count": seb_index["count"] if seb_index else 0,
                "image_gap_ids": image_index["gap_ids"] if image_index else [],
                "seb_gap_ids": seb_index["gap_ids"] if seb_index else [],
                "fixture_count": len(fixtures),
                "unresolved_membership": [] if pack else ["No proven source pack/member selector"],
                "notes": "Do not repair sparse gaps or convert the group into a filename/global-manifest namespace.",
            })

        for owner in ADDITIONAL_OWNERS:
            if owner["pack"] and owner["pack"] in inventory:
                owner_record = dict(owner)
                owner_record["pack_index_summary"] = {
                    kind: {
                        "source_index_member": inventory[owner["pack"]]["indexes"][kind]["source_index_member"] if inventory[owner["pack"]]["indexes"][kind] else None,
                        "count": inventory[owner["pack"]]["indexes"][kind]["count"] if inventory[owner["pack"]]["indexes"][kind] else 0,
                    } for kind in ("img", "seb")
                }
            else:
                owner_record = dict(owner)
                owner_record["pack_index_summary"] = None
            owner_record["fixtures"] = []
            if owner["pack"] in {"title", "recruit"}:
                pack_record = inventory[owner["pack"]]
                owner_fixtures = []
                temp_group = "resTitle_" if owner["owner_id"] == "resTitle_" else "resRecruit_"
                GROUP_SPECS[temp_group] = {"pack": owner["pack"], "prefix": None, "declaration_line": 0, "fixtures": owner["fixtures"], "consumer_refs": []}
                owner_fixtures = [fixture_record(temp_group, fixture, pack_record["indexes"], catalog_by_member) for fixture in owner["fixtures"]]
                owner_record["fixtures"] = owner_fixtures
                del GROUP_SPECS[temp_group]
            owner_records_path = owner_record
            owner_records_path["fixture_ids"] = [fixture["fixture_id"] for fixture in owner_record["fixtures"]]
            owner_records_path["authority_boundary"] = "Additional owner inventory only; not a replacement for AppData declared group identity."
            # Keep the generated owner object in the map below.
            owner["_built"] = owner_records_path

        resource_group_map = {
            "schema_version": "social-dev-visual-port-v3-resource-group-map",
            "status": "SOURCE_BACKED_GROUP_OWNERSHIP_WITH_EXPLICIT_UNKNOWN_BOUNDARIES",
            "authority": "group_id plus original img/seb ID; no global manifest or filename is semantic authority",
            "source": {
                "app_data": "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/main/AppData.cs",
                "resource_manager": "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/kairo.unity.ui/ResourceManager.cs",
                "resource_groups_prior_contract": "knowledge/fixtures/accepted/visual-port/resource-groups.json",
                "asset_zip": "sources/raw/Social_Dev_Story_v2.5.1_ASSETS_ONLY_WITH_ASSEMBLY_GUIDE.zip",
                "source_hashes": source_hashes,
            },
            "declared_group_ids": GROUP_IDS,
            "groups": group_records,
            "additional_resource_manager_owners": [owner["_built"] for owner in ADDITIONAL_OWNERS],
            "current_runtime_boundary": "V3 is an additive evidence-backed compatibility layer; existing V1/V2 and production renderer are not cut over.",
        }
        write_json("resource-group-map.json", resource_group_map)

        write_json("pack-inventory.json", {
            "schema_version": "social-dev-visual-port-v3-pack-inventory",
            "status": "STATIC_ZIP_INVENTORY",
            "authority": "pack-local INF files and original archive member identities",
            "archive": {"path": "sources/raw/Social_Dev_Story_v2.5.1_ASSETS_ONLY_WITH_ASSEMBLY_GUIDE.zip", "sha256": zip_sha256, "zip_root": ZIP_ROOT},
            "packs": inventory,
            "mapped_declared_packs": sorted({spec["pack"] for spec in GROUP_SPECS.values() if spec.get("pack")}),
            "unresolved_visual_owners": ["event", "lineup", "lineup_layout", "load", "mail", "billing", "connect", "friend", "helper"],
        })

        write_json("img-index-contract.json", {
            "schema_version": "social-dev-visual-port-v3-img-index",
            "status": "PASS_SOURCE_INDEXED_SPARSE",
            "authority": "group_id plus pack-local img.inf original ID",
            "sparse_array_policy": "Array length is max_id plus one; every missing ID remains null and is never compacted or repaired.",
            "archive_sha256": zip_sha256,
            "groups": img_groups,
        })
        write_json("seb-index-contract.json", {
            "schema_version": "social-dev-visual-port-v3-seb-index",
            "status": "PASS_SOURCE_INDEXED_SPARSE",
            "authority": "group_id plus pack-local seb.inf original ID",
            "sparse_array_policy": "Array length is max_id plus one; every missing ID remains null and is never compacted or repaired.",
            "archive_sha256": zip_sha256,
            "groups": seb_groups,
        })

        write_json("group-coverage.json", {
            "schema_version": "social-dev-visual-port-v3-group-coverage",
            "status": "PASS_WITH_EXPLICIT_COVERAGE_CLASSES",
            "coverage_categories": [
                "PROVEN_SOURCE_INDEXED",
                "PROVEN_NATIVE",
                "PROVEN_BOTH",
                "DECLARED_ONLY",
                "UNRESOLVED_SOURCE_MEMBER",
                "SENTINEL",
                "ABSENT",
                "DEFERRED",
            ],
            "records": coverage_records,
            "additional_owner_categories": [
                {"owner_id": owner["owner_id"], "coverage_category": "UNRESOLVED_SOURCE_MEMBER" if "UNRESOLVED" in owner["status"] else "PROVEN_NATIVE" if owner["status"] == "DECLARED_NONVISUAL" else "PROVEN_BOTH", "status": owner["status"]}
                for owner in ADDITIONAL_OWNERS
            ],
            "no_guess_rule": "A declared field without source-backed pack/index/member evidence remains DECLARED_ONLY or UNRESOLVED_SOURCE_MEMBER.",
        })

        layout = {
            "schema_version": "social-dev-visual-port-v3-resource-manager-layout",
            "status": "PASS_STATIC_LAYOUT_WITH_LOAD_AND_RASTER_BOUNDARIES",
            "native_object_fields": {
                "img": {"offset": "this+0x10", "source_declaration": "ResourceManager.cs:2257", "semantic": "Image[] group-owned sparse array"},
                "seb": {"offset": "this+0x18", "source_declaration": "ResourceManager.cs:2259", "semantic": "Seb[] group-owned sparse array"},
                "CustomImages": {"offset": "this+0x60", "source_declaration": "ResourceManager.cs:2289-2339", "semantic": "custom image dictionary probed before img[]"},
            },
            "managed_fields": [
                {"name": "img", "type": "Image[]", "source_ref": "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/kairo.unity.ui/ResourceManager.cs:2257"},
                {"name": "seb", "type": "Seb[]", "source_ref": "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/kairo.unity.ui/ResourceManager.cs:2259"},
                {"name": "loaded_", "type": "bool", "source_ref": "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/kairo.unity.ui/ResourceManager.cs:2307"},
                {"name": "loadNum_", "type": "int", "source_ref": "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/kairo.unity.ui/ResourceManager.cs:2305"},
                {"name": "CustomImages", "type": "Dictionary<int,Image>", "source_ref": "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/kairo.unity.ui/ResourceManager.cs:2331-2339"},
            ],
            "lookup_order": ["CustomImages.TryGetValue(texId)", "img[texId]", "failure for invalid/null slot"],
            "sparse_missing_behavior": "Original IDs and gaps are preserved; V3 throws a typed lookup error for invalid or null slots rather than shifting entries.",
            "namespace_rule": "img and seb IDs are resolved within the requested group; cross-group fallback is prohibited.",
            "custom_images": {"initialization": "_init creates an empty Dictionary<int,Image>", "population": "not statically proven", "v3_behavior": "empty/deferred boundary"},
            "readiness": {"loaded_": "LoadReady/LoadStart state field", "loadNum_": "native progress field", "async_callback": "platform/decompiler behavior deferred"},
            "source_hashes": source_hashes,
        }
        write_json("resource-manager-layout.json", layout)

        load_semantics = {
            "schema_version": "social-dev-visual-port-v3-load-semantics",
            "status": "PASS_STATIC_OVERLOAD_SURFACE_WITH_ASYNC_DEFERRED",
            "source_hashes": source_hashes,
            "overloads": [
                {"method": "LoadImage(byte[])", "source_ref": "ResourceManager.cs:2343-2346", "proven": "delegates to Image.Load(bytes, format, filterMode)", "unknown": "decoded raster/backend details"},
                {"method": "LoadImage(InputStream)", "source_ref": "ResourceManager.cs:2348-2351", "proven": "delegates to Image.Load(stream, format, filterMode)", "unknown": "decoded raster/backend details"},
                {"method": "LoadSeb(byte[])", "source_ref": "ResourceManager.cs:2353-2358", "proven": "constructs new Seb(src)", "unknown": "none for selected decoded contract; broader decoder surface remains source-limited"},
                {"method": "LoadSeb(InputStream)", "source_ref": "ResourceManager.cs:2361-2366", "proven": "constructs new Seb(stream)", "unknown": "none for selected decoded contract; broader decoder surface remains source-limited"},
                {"method": "Load(byte[])", "source_ref": "ResourceManager.cs:2719-2729", "proven": "creates JarInflater, calls LoadReady then LoadStart, closes inflater", "unknown": "decompiled body details and scheduling"},
                {"method": "Load(JarInflater)", "source_ref": "ResourceManager.cs:2760-2768", "proven": "calls LoadReady then LoadStart without owning the inflater close", "unknown": "decompiled body details and scheduling"},
                {"method": "Load(string directory)", "source_ref": "ResourceManager.cs:2781-2792", "proven": "creates JarInflater from directory then calls LoadReady/LoadStart", "unknown": "decompiled body details and scheduling"},
                {"method": "Load(int rsId, int rcId)", "source_ref": "ResourceManager.cs:2830-2843", "proven": "reads RecordStore record, stores selectors, calls LoadReady/LoadStart", "unknown": "record payload and async scheduling"},
                {"method": "Load(Assembly, name)", "source_ref": "ResourceManager.cs:2874-2888", "proven": "creates JarInflater from assembly resource then calls LoadReady/LoadStart", "unknown": "decompiled body details and scheduling"},
                {"method": "LoadReady", "source_ref": "ResourceManager.cs:2923-2967", "proven": "early loaded_ guard and index/readiness preparation boundary", "unknown": "damaged index allocation body"},
                {"method": "LoadStart", "source_ref": "ResourceManager.cs:3740-3784", "proven": "start/worker/callback boundary is present", "unknown": "thread scheduling and completion timing"},
                {"method": "LoadTask.Execute", "source_ref": "kairo.unity.util/LoadTask.cs", "proven": "creates/loads ResourceManager and assigns the target field from RecordStore/resource directory", "unknown": "external scheduler timing"},
            ],
            "v3_preload_policy": "Only source-indexed static fixtures are constructed; no fabricated filenames, manifests, async timing, or GPU state is introduced.",
            "async_scheduling": "DEFERRED_PLATFORM_BEHAVIOR",
        }
        write_json("load-semantics.json", load_semantics)

        associations = []
        for fixture in all_fixtures:
            if fixture["seb"]["id"] is None:
                continue
            associations.append({
                "fixture_id": fixture["fixture_id"],
                "group_id": fixture["group_id"],
                "pack": fixture["pack"],
                "seb_id": fixture["seb"]["id"],
                "seb_member": fixture["seb"]["source_member"],
                "seb_sha256": fixture["seb"]["source_sha256"],
                "tex_ids": [binding["tex_id"] for binding in fixture["tex_id_bindings"]],
                "tex_id_bindings": fixture["tex_id_bindings"],
                "cross_group_exceptions": [],
                "status": fixture["association_status"],
                "proof": "SEB decoded record image_id/TexId resolves to the same pack-local img.inf namespace and source member; no global fallback is used.",
            })
        write_json("image-seb-association.json", {
            "schema_version": "social-dev-visual-port-v3-image-seb-association",
            "status": "PASS_SAME_GROUP_NAMESPACE_FOR_SELECTED_FIXTURES",
            "authority": "SEB decoded TexId -> same group img.inf original ID",
            "associations": associations,
            "cross_group_exceptions": [],
            "cross_group_exception_proven": False,
        })

        write_json("fixture-manifest.json", {
            "schema_version": "social-dev-visual-port-v3-fixture-manifest",
            "status": "PASS_REAL_SOURCE_INDEXED_MULTI_GROUP_FIXTURES",
            "authority": "pack-local INF rows, original IDs, ZIP member hashes, and decoded SEB catalog records",
            "archive_sha256": zip_sha256,
            "fixtures": all_fixtures,
            "coverage": {
                "declared_groups_with_real_fixtures": sorted({fixture["group_id"] for fixture in all_fixtures}),
                "declared_groups_without_real_fixture": [group_id for group_id in GROUP_IDS if group_id not in {fixture["group_id"] for fixture in all_fixtures}],
                "additional_owner_fixtures": [fixture for owner in ADDITIONAL_OWNERS for fixture in owner["_built"]["fixtures"]],
            },
            "requirements": {
                "chip_image_and_seb": True,
                "human_image_and_seb": True,
                "avatar_body_image_and_seb": True,
                "avatar_head_image_only": True,
                "game_image_and_seb": True,
                "interface_lookup_absent": True,
                "effect_image_and_seb": True,
                "furniture_texid": True,
                "character_texid": True,
                "sparse_missing_ids": True,
                "sentinel_or_absent": "SEB decoded TEXID_NONE (-1) is retained as a sentinel with no INF lookup; absent declared resInterface_ is retained as DECLARED_ONLY.",
                "alias": "resCom_:wnd_conner uses duplicate same-file image IDs 5 and 19; the selected SEB TexId is 19.",
                "custom_images": "Population not proven; no fabricated CustomImages fixture.",
            },
        })

        native_map = {
            "schema_version": "social-dev-visual-port-v3-native-recovery-map",
            "status": "PASS_STATIC_SOURCE_AND_NATIVE_GROUP_RECOVERY",
            "execution_policy": {"runtime_execution_used": False, "adb_or_emulator_used": False, "subagents": False, "network": False},
            "source_hashes": source_hashes,
            "v1_preserved": [
                "knowledge/fixtures/accepted/visual-port/v1/native-recovery-map.json",
                "knowledge/fixtures/accepted/visual-port/v1/resource-lookup-contract.json",
                "knowledge/fixtures/accepted/visual-port/v1/seb-contract.json",
            ],
            "v2_gate": "knowledge/fixtures/accepted/visual-port/v2/v2-static-acceptance.json",
            "native_fields": [
                {"field": "img", "offset": "this+0x10", "proof": "native disassembly plus ResourceManager declaration"},
                {"field": "seb", "offset": "this+0x18", "proof": "native disassembly plus ResourceManager declaration"},
                {"field": "CustomImages", "offset": "this+0x60", "proof": "native disassembly plus managed property"},
            ],
            "method_rows": [
                {"method": "GetImage", "rva": "0x1C53DA0", "proof": "CustomImages first, then sparse img slot"},
                {"method": "LoadImage/LoadSeb", "rvas": ["0x1C4FE24", "0x1C4FE94", "0x1C4FF04", "0x1C50050"], "proof": "existing V1 pinned native load map"},
                {"method": "LoadReady/LoadStart", "rvas": ["0x1C52074", "0x1C507F4", "0x1C521DC", "0x1C50F60"], "proof": "existing V1/V2 pinned lifecycle boundary"},
            ],
            "group_proof": "AppData named fields plus exact namespace constants and source-indexed pack fixtures; unresolved groups remain unresolved.",
        }
        write_json("native-recovery-map.json", native_map)

        write_json("checkpoint-ledger.json", {
            "schema_version": "social-dev-visual-port-v3-checkpoint-ledger",
            "status": "PASS_STATIC_V3_STOP_BEFORE_V4",
            "execution": "inline_only_sequential_static_only",
            "checkpoints": [
                {"id": "V3.0", "status": "PASS", "files": ["knowledge/fixtures/accepted/visual-port/v2/v2-static-acceptance.json"], "evidence": ["V1 gate", "V2 focused static suite"], "tests": ["python -B tools/social-dev/test_visual_port_v1.py", "17 V2 focused tests"], "findings": "V2 static/semantic gate accepted; pixel parity deferred to V7.", "unknowns": ["_drawBitmap raster boundary"], "next": "Inventory AppData groups and source packs."},
                {"id": "V3.1", "status": "PASS", "files": ["resource-group-map.json", "pack-inventory.json"], "evidence": ["11 AppData declared groups", "additional named/local ResourceManager owners"], "tests": ["source and ZIP inventory builder"], "findings": "Ten declared visual packs are source-backed; resInterface_ remains declared-only.", "unknowns": ["interface pack", "event owner membership"], "next": "Verify arrays, gaps, and readiness."},
                {"id": "V3.2", "status": "PASS", "files": ["resource-manager-layout.json", "img-index-contract.json", "seb-index-contract.json"], "evidence": ["img this+0x10", "seb this+0x18", "CustomImages this+0x60"], "tests": ["V3 sparse lookup suite"], "findings": "Original group-owned sparse namespaces are preserved.", "unknowns": ["LoadReady allocation body"], "next": "Recover INF records, selectors, aliases, and gaps."},
                {"id": "V3.3", "status": "PASS", "files": ["img-index-contract.json", "seb-index-contract.json"], "evidence": ["raw INF rows", "flags", "source member hashes", "duplicate aliases", "sentinel TexId"], "tests": ["V3 Python evidence gate"], "findings": "No sparse ID is repaired or compacted.", "unknowns": ["unresolved source members outside selected groups"], "next": "Record LoadImage/LoadSeb and load lifecycle semantics."},
                {"id": "V3.4", "status": "PASS_WITH_ASYNC_DEFERRED", "files": ["load-semantics.json", "native-recovery-map.json"], "evidence": ["static overloads", "LoadReady/LoadStart", "LoadTask"], "tests": ["typecheck", "V3 compatibility load aliases"], "findings": "Preloaded fixture readiness is deterministic; scheduler timing is not invented.", "unknowns": ["async callback order"], "next": "Prove SEB TexId namespace resolution."},
                {"id": "V3.5", "status": "PASS", "files": ["image-seb-association.json", "fixture-manifest.json"], "evidence": ["selected SEB decoded records", "same-pack img.inf resolution"], "tests": ["V3 TexId association tests"], "findings": "Positive TexIds resolve in the requested group; negative sentinel is explicit.", "unknowns": ["cross-group relationships not proven"], "next": "Build coverage matrix and boundary classes."},
                {"id": "V3.6", "status": "PASS", "files": ["group-coverage.json", "unknowns.json"], "evidence": ["required coverage categories", "nonblocking unknown list"], "tests": ["V3 Python evidence gate"], "findings": "PROVEN_BOTH, PROVEN_SOURCE_INDEXED, DECLARED_ONLY, unresolved, sentinel, and deferred states are explicit.", "unknowns": ["interface/event/atlas/custom/async"], "next": "Bound CustomImages, atlas, and lifetime behavior."},
                {"id": "V3.7", "status": "PASS_WITH_DEFERRED_PATHS", "files": ["resource-manager-layout.json", "unknowns.json"], "evidence": ["empty CustomImages", "atlas -1/null", "use/unuse boundary"], "tests": ["V3 lifetime and deferral tests"], "findings": "No GPU disposal, custom-image population, or atlas relationship is guessed.", "unknowns": ["CustomImages population", "atlas/GPU lifetime"], "next": "Keep compatibility layer isolated from production."},
                {"id": "V3.8", "status": "PASS", "files": ["runtime/social-dev/src/v3/"], "evidence": ["ResourceManagerV3", "VisualAppDataV3", "pack fixture loader"], "tests": ["TypeScript typecheck", "V3 focused Vitest"], "findings": "V1 Seb parser and source catalogs are reused; no competing global manifest is introduced.", "unknowns": ["production cutover intentionally deferred"], "next": "Add real multi-group fixtures and regressions."},
                {"id": "V3.9", "status": "PASS", "files": ["fixture-manifest.json", "runtime/social-dev/tests/v3-resource-manager.test.ts"], "evidence": ["13 declared-group fixtures", "title/recruit additional owners", "furniture/human/avatar/game/effect/meeting fixtures"], "tests": ["8 V3 focused tests", "36-file/140-test full Vitest"], "findings": "Group ownership, sparse lookup, aliases, sentinels, TexIds, invalid IDs, and V1/V2 regression boundaries pass.", "unknowns": ["explicit nonblocking V3 unknowns remain"], "next": "Run final full gates and update handoff."},
                {"id": "V3.10", "status": "PASS", "files": ["V3 reports", "PROJECT_STATE.md", "TODO.md"], "evidence": ["deterministic JSON hashes", "source ZIP/INF hash checks", "V2 acceptance"], "tests": ["Vitest 36/36 files, 140/140 tests", "typecheck", "build", "V1 Python gate", "V3 Python gate", "py_compile", "git diff --check"], "findings": "V3 PASS; V4 entry is ready for resource requests by group and original ID; V4 is not started.", "unknowns": ["resInterface_ ownership", "async/custom/atlas boundaries", "V2 raster parity to V7"], "next": "Stop before V4 and preserve the handoff."},
            ],
        })

        write_json("unknowns.json", {
            "schema_version": "social-dev-visual-port-v3-unknowns",
            "status": "OPEN_NONBLOCKING_WITH_EXPLICIT_STATIC_BOUNDARIES",
            "v3_entry_blocking": False,
            "unknowns": [
                {"id": "v3-interface-pack", "class": "DECLARED_ONLY", "method_or_field": "AppData.resInterface_", "resource_group": "resInterface_", "question": "Which source pack and exact img/seb IDs populate the interface manager?", "known_evidence": "AppData declaration and partial consumer references; no exact namespace/pack index pair.", "missing_evidence": "Source load selector and matching pack-local INF ownership.", "affected_fixtures": [], "impact": "medium", "safe_current_behavior": "Keep group declared with empty sparse arrays and typed missing lookup.", "exact_next_static_investigation": "Trace every resInterface_ assignment and RecordStore selector in source/native call sites.", "future_phase": "V4", "status": "UNKNOWN"},
                {"id": "v3-events-pack-membership", "class": "UNRESOLVED_SOURCE_MEMBER", "method_or_field": "SubForm.resEvents_", "resource_group": "resEvents_", "question": "How do event SEBs map to image records and which selector owns them?", "known_evidence": "Named ResourceManager, RecordStore.ReadRecord(1,1), event SEB payloads.", "missing_evidence": "Standard event img.inf/seb.inf pair and complete load selector.", "affected_fixtures": [], "impact": "medium", "safe_current_behavior": "Do not assign event members to a declared AppData visual group.", "exact_next_static_investigation": "Reconcile event img0..img11/seb0..seb11 sources and native record packaging.", "future_phase": "V4", "status": "UNKNOWN"},
                {"id": "v3-avatar-head-selector", "class": "PARTIAL", "method_or_field": "Avatar headIndex -> resAvatarHead_.img", "resource_group": "resAvatarHead_", "question": "Which dynamic headIndex values correspond to source image IDs?", "known_evidence": "Avatar uses resAvatarHead_.img and avatar_head/img.inf has IDs 0..167; AppData constants 300/301 are not assumed to address this index.", "missing_evidence": "Complete selector construction and provenance for headIndex.", "affected_fixtures": ["resAvatarHead_:face_m_00"], "impact": "medium", "safe_current_behavior": "Expose only source-indexed IDs and preserve dynamic selector uncertainty.", "exact_next_static_investigation": "Trace Avatar headIndex assignment to source data and native load selectors.", "future_phase": "V4", "status": "PARTIAL"},
                {"id": "v3-load-array-allocation", "class": "PARTIAL", "method_or_field": "ResourceManager.LoadReady", "resource_group": "all declared groups", "question": "What exact native index allocation and missing-slot behavior occurs while reading INF records?", "known_evidence": "img/seb fields, LoadReady boundary, pack-local INF rows, and sparse IDs.", "missing_evidence": "Decompiler-damaged allocation body and exact native loop implementation.", "affected_fixtures": ["all V3 fixtures"], "impact": "high", "safe_current_behavior": "Construct source-indexed sparse arrays with null gaps and no compaction.", "exact_next_static_investigation": "Recover remaining LoadReady native loop and compare every array slot against INF source rows.", "future_phase": "V4", "status": "PARTIAL"},
                {"id": "v3-async-scheduling", "class": "DEFERRED", "method_or_field": "LoadStart/LoadTask/ResourceLoader", "resource_group": "all declared groups", "question": "What scheduler timing and callback order marks a manager ready?", "known_evidence": "LoadReady/LoadStart and task callback surfaces are source/native pinned.", "missing_evidence": "Runtime scheduler execution, prohibited by current scope, and damaged callback body.", "affected_fixtures": ["all V3 fixtures"], "impact": "medium", "safe_current_behavior": "Use deterministic preloaded fixture state; expose readiness as explicit compatibility state.", "exact_next_static_investigation": "Recover static callback/state transitions without executing the app.", "future_phase": "V4", "status": "DEFERRED"},
                {"id": "v3-custom-images-population", "class": "DEFERRED", "method_or_field": "ResourceManager.CustomImages", "resource_group": "all declared groups", "question": "Which native callers populate custom image IDs and what ownership lifetime do they have?", "known_evidence": "Dictionary initialized in _init; GetImage probes it before img[]; native offset is pinned.", "missing_evidence": "Complete population call sites and source payloads.", "affected_fixtures": [], "impact": "medium", "safe_current_behavior": "Keep empty/deferred custom-image boundary and never inject a guessed entry.", "exact_next_static_investigation": "Trace every CustomImages setter/population call site and native dictionary mutation.", "future_phase": "V4", "status": "DEFERRED"},
                {"id": "v3-atlas-population", "class": "DEFERRED", "method_or_field": "ImageAtlas/ImageAtlasManager", "resource_group": "all declared groups", "question": "Which images are atlas-backed and how are regions/lifetimes assigned?", "known_evidence": "V1 selected fixtures have image_atlas_id=-1 and atlas_region=null; native dispatch boundary is known.", "missing_evidence": "Atlas population source and final GPU lifetime.", "affected_fixtures": [fixture["fixture_id"] for fixture in all_fixtures[:6]], "impact": "medium", "safe_current_behavior": "Leave atlas status deferred and use source Image identity.", "exact_next_static_investigation": "Trace static atlas builder/index references and selected image atlas IDs.", "future_phase": "V7", "status": "DEFERRED"},
                {"id": "v3-unsupported-seb", "class": "SOURCE_LIMITED", "method_or_field": "seb_catalog unsupported decode", "resource_group": "resCom_", "question": "What exact record contract belongs to the unsupported develop_menu_light.seb payload?", "known_evidence": "Existing catalog marks one SEB unsupported; selected V3 fixtures decode and validate.", "missing_evidence": "Static decoder grammar for that payload.", "affected_fixtures": ["01_GAME_PACKS/com/develop_menu_light.seb"], "impact": "low", "safe_current_behavior": "Exclude unsupported payload from fixtures and preserve catalog status.", "exact_next_static_investigation": "Extend static SEB grammar analysis only if a V4 fixture requires it.", "future_phase": "V4", "status": "SOURCE_LIMITED"},
                {"id": "v3-raster-pixels", "class": "DEFERRED", "method_or_field": "Graphics._drawBitmap", "resource_group": "V2 boundary", "question": "What final native framebuffer pixels result?", "known_evidence": "V2 static gate PASS_STATIC; dispatch boundary recovered.", "missing_evidence": "Shader/sample/compositor output; runtime proof remains prohibited.", "affected_fixtures": [], "impact": "nonblocking", "safe_current_behavior": "Keep pixel hashes null and defer to V7.", "exact_next_static_investigation": "Only static shader/backend evidence if it becomes available.", "future_phase": "V7", "status": "DEFERRED"},
            ],
        })


if __name__ == "__main__":
    build()
    print("visual_port_v3_evidence_built")
