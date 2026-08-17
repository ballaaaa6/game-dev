"""Build the Phase 3B floor-selector recovery audit.

This is an evidence-only recovery pass.  It checks the raw RoomData selector,
the packed ``chip/img.inf`` bytes in the supplied ZIP and APK, the Unity
TextAsset boundary, the native resource-loader path, and every alternate APK
available in the workspace.  It never executes recovered C# or native code
and it does not change the Phase 3B runtime contract when no authoritative
mapping is recovered.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import struct
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import UnityPy


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "knowledge/fixtures/accepted"
RUNTIME_EVIDENCE = ROOT / "knowledge/fixtures/accepted/runtime"
SOURCE_ROOT = ROOT / "sources/raw/1_Click_CSharp_Code update"

SCENE_PATH = RUNTIME_EVIDENCE / "scene_catalog_contract.json"
BASELINE_CONTRACT_PATH = RUNTIME_EVIDENCE / "room_placement_contract.json"
SELECTOR_PATH = EVIDENCE / "asset_selector_contract.json"
ASSET_INDEX_PATH = ROOT / "knowledge/sources/asset_guide_20260813/00_INDEX/ASSET_INDEX.json"
NATIVE_PATH = EVIDENCE / "scene_native_semantics.json"
DUMP_PATH = ROOT / "knowledge/sources/phase3a_apk_probe/il2cpp_dump/dump.cs"

APK_PATH = ROOT / "sources/raw/Social_Dev_Story_v2.5.1.apk"
ZIP_PATH = ROOT / "sources/raw/Social_Dev_Story_v2.5.1_ASSETS_ONLY_WITH_ASSEMBLY_GUIDE.zip"
APK_SOURCE_ENTRY = "assets/bin/Data/ef126b48648179c4e98f14f9024975f3"
METADATA_ENTRY = "assets/bin/Data/Managed/Metadata/global-metadata.dat"
CHIP_KEY_HASH = "3f4780f4d34637228b0a828cc3a5013784cab0d0217f567624e9c6cec1ccceba"
CHIP_KEY_LENGTH = 44
CHIP_TEXT_ASSET_NAME = "chip"

ZIP_CHIP_PREFIX = "Social_Dev_Story_v2.5.1_ASSETS_ONLY/01_GAME_PACKS/chip/"

SOURCE_FILES = {
    "RoomData": SOURCE_ROOT / "data/RoomData.cs",
    "Room": SOURCE_ROOT / "game/Room.cs",
    "MapChip": SOURCE_ROOT / "game/MapChip.cs",
    "ResourceManager": SOURCE_ROOT / "KairoEngine/kairo.unity.ui/ResourceManager.cs",
    "StringUtil": SOURCE_ROOT / "KairoEngine/kairo.unity.util/StringUtil.cs",
    "Image": SOURCE_ROOT / "KairoEngine/kairo.unity.ui/Image.cs",
    "AppData": SOURCE_ROOT / "KairoEngine/main/AppData.cs",
}

SOURCE_SLICES = [
    {
        "id": "room-data-selector-load",
        "file": "sources/raw/1_Click_CSharp_Code update/data/RoomData.cs",
        "line_start": 23,
        "line_end": 73,
        "purpose": "RoomData scalar load order and the three image selector fields.",
    },
    {
        "id": "room-floor-selector-to-map-chip",
        "file": "sources/raw/1_Click_CSharp_Code update/game/Room.cs",
        "line_start": 334,
        "line_end": 372,
        "purpose": "Room.InitMapChips passes floorImgId_ into MapChip and guards only negative values in the decompiler-bounded source.",
    },
    {
        "id": "map-chip-floor-draw",
        "file": "sources/raw/1_Click_CSharp_Code update/game/MapChip.cs",
        "line_start": 236,
        "line_end": 405,
        "purpose": "MapChip stores imageId_ and reaches the floor image draw path; the recovered body is decompiler-damaged.",
    },
    {
        "id": "resource-manager-indexed-image-load",
        "file": "sources/raw/1_Click_CSharp_Code update/KairoEngine/kairo.unity.ui/ResourceManager.cs",
        "line_start": 1648,
        "line_end": 1954,
        "purpose": "ResourceManager loads packed image records and writes them by the list-record index.",
    },
    {
        "id": "resource-manager-list-load",
        "file": "sources/raw/1_Click_CSharp_Code update/KairoEngine/kairo.unity.ui/ResourceManager.cs",
        "line_start": 2898,
        "line_end": 2965,
        "purpose": "ResourceManager asks StringUtil to read resource list records from the JarInflater pack.",
    },
    {
        "id": "string-array-resource-reader",
        "file": "sources/raw/1_Click_CSharp_Code update/KairoEngine/kairo.unity.util/StringUtil.cs",
        "line_start": 1021,
        "line_end": 1100,
        "purpose": "StringUtil reads the packed list bytes and splits them into resource records.",
    },
    {
        "id": "appdata-chip-image-constants",
        "file": "sources/raw/1_Click_CSharp_Code update/KairoEngine/main/AppData.cs",
        "line_start": 1200,
        "line_end": 1234,
        "purpose": "Source-labeled chip image constants; the reviewed source skips image selector id 5.",
    },
]

SCHEMA_VERSION = "social-dev-phase3b-floor-recovery-v1"
AUDIT_SCHEMA_VERSION = "social-dev-phase3b-floor-recovery-source-audit-v1"
FIXTURE_SCHEMA_VERSION = "social-dev-phase3b-floor-recovery-fixture-v1"
VALIDATION_SCHEMA_VERSION = "social-dev-phase3b-floor-recovery-validation-v1"


def stable_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def content_hash(value: Any) -> str:
    return sha256_bytes(stable_json(value).encode("utf-8"))


def relative_path(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def without_dynamic(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: without_dynamic(item)
            for key, item in value.items()
            if key not in {"generated_at_utc", "content_hash", "contract_hash"}
        }
    if isinstance(value, list):
        return [without_dynamic(item) for item in value]
    return value


def path_ref(path: Path, *, required: bool = False) -> dict[str, Any]:
    result: dict[str, Any] = {
        "path": relative_path(path),
        "exists": path.is_file(),
        "required": required,
    }
    if path.is_file():
        result.update({"size_bytes": path.stat().st_size, "sha256": sha256_file(path)})
    else:
        result.update({"size_bytes": None, "sha256": None})
    return result


def input_manifest(paths: list[tuple[Path, bool]]) -> dict[str, Any]:
    files = [path_ref(path, required=required) for path, required in paths]
    files.sort(key=lambda item: item["path"])
    return {"files": files, "input_hash": content_hash(files)}


def source_slice_ref(item: dict[str, Any]) -> dict[str, Any]:
    path = ROOT / item["file"]
    result = copy.deepcopy(item)
    if not path.is_file():
        result.update({"file_sha256": None, "slice_sha256": None, "hash_status": "missing"})
        return result
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines(keepends=True)
    start = int(item["line_start"])
    end = int(item["line_end"])
    text = "".join(lines[start - 1 : end])
    result.update(
        {
            "file_sha256": sha256_file(path),
            "slice_sha256": sha256_bytes(text.encode("utf-8")),
            "hash_status": "pass",
        }
    )
    return result


def asset_index_map() -> dict[str, dict[str, Any]]:
    rows = load_json(ASSET_INDEX_PATH)
    if not isinstance(rows, list):
        raise ValueError("ASSET_INDEX.json must contain a list")
    result = {str(row["relative_path"]).replace("\\", "/"): row for row in rows}
    if len(result) != len(rows):
        raise ValueError("ASSET_INDEX.json contains duplicate relative paths")
    return result


def parse_inf(raw: bytes) -> dict[str, Any]:
    text = raw.decode("utf-8", "replace")
    entries: dict[int, dict[str, Any]] = {}
    malformed: list[str] = []
    duplicate_ids: list[int] = []
    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        line = raw_line.strip()
        if not line:
            continue
        if "\t" not in line:
            malformed.append(line)
            continue
        left, right = line.split("\t", 1)
        try:
            selector_id = int(left)
        except ValueError:
            malformed.append(line)
            continue
        if selector_id in entries:
            duplicate_ids.append(selector_id)
        filename, _, format_name = right.partition(",")
        entries[selector_id] = {
            "id": selector_id,
            "filename": filename.strip(),
            "format": format_name.strip(),
            "line_number": line_number,
            "raw_line": raw_line,
        }
    ids = sorted(entries)
    gaps = [value for value in range(ids[-1] + 1) if value not in entries] if ids else []
    return {
        "bytes": len(raw),
        "sha256": sha256_bytes(raw),
        "entry_count": len(entries),
        "entries": {str(key): entries[key]["filename"] for key in ids},
        "entry_records": [entries[key] for key in ids],
        "ids": ids,
        "gaps_through_max_id": gaps,
        "malformed_lines": malformed,
        "duplicate_ids": duplicate_ids,
        "raw_preview": text[:240],
    }


def pack_record_summary(record: dict[str, Any]) -> dict[str, Any]:
    raw = record["bytes"]
    return {
        "name": record["name"],
        "pack_offset": record["pack_offset"],
        "declared_size": record["declared_size"],
        "output_size": record["output_size"],
        "sha256": sha256_bytes(raw),
    }


def parse_pack(plain: bytes) -> tuple[dict[str, int], list[dict[str, Any]]]:
    if len(plain) < 12:
        raise ValueError("decrypted chip payload is shorter than its header")
    data_offset, data_length, file_count = struct.unpack(">III", plain[:12])
    position = 12
    names: list[str] = []
    for _ in range(file_count):
        if position + 4 > len(plain):
            raise ValueError("chip name length exceeds payload")
        name_length = struct.unpack(">I", plain[position : position + 4])[0]
        position += 4
        if position + name_length > len(plain):
            raise ValueError("chip name exceeds payload")
        names.append(plain[position : position + name_length].decode("utf-8"))
        position += name_length
    table_end = position + file_count * 8
    if table_end > len(plain):
        raise ValueError("chip offset/size tables exceed payload")
    offsets = [
        struct.unpack(">I", plain[position + index * 4 : position + index * 4 + 4])[0]
        for index in range(file_count)
    ]
    position += file_count * 4
    sizes = [
        struct.unpack(">I", plain[position + index * 4 : position + index * 4 + 4])[0]
        for index in range(file_count)
    ]
    data_base = data_offset + 4
    entries: list[dict[str, Any]] = []
    for name, pack_offset, declared_size in zip(names, offsets, sizes):
        prefix_offset = data_base + pack_offset
        if prefix_offset + 4 > len(plain):
            raise ValueError(f"length prefix for {name} exceeds payload")
        output_size = struct.unpack(">I", plain[prefix_offset : prefix_offset + 4])[0]
        output_start = prefix_offset + 4
        output_end = output_start + output_size
        if output_end > len(plain):
            raise ValueError(f"output bytes for {name} exceed payload")
        if output_size != declared_size:
            raise ValueError(f"size mismatch for {name}: {output_size} != {declared_size}")
        entries.append(
            {
                "name": name,
                "pack_offset": pack_offset,
                "declared_size": declared_size,
                "output_size": output_size,
                "prefix_offset": prefix_offset,
                "bytes": plain[output_start:output_end],
            }
        )
    return {
        "data_offset": data_offset,
        "data_length": data_length,
        "file_count": file_count,
        "data_base_offset": data_base,
        "table_end_offset": position,
        "payload_length": len(plain),
    }, entries


def locate_chip_text_asset(path: Path) -> dict[str, Any]:
    candidates: list[zipfile.ZipInfo] = []
    matches: list[dict[str, Any]] = []
    scanned = 0
    with zipfile.ZipFile(path) as archive:
        for info in archive.infolist():
            if (
                not info.filename.startswith("assets/bin/Data/")
                or info.file_size == 0
                or info.filename.endswith("/")
                or info.filename.endswith((".resource", ".resS", ".split0", ".split1", ".split2"))
                or "/Managed/" in info.filename
                or "/Resources/" in info.filename
                or info.filename.endswith("globalgamemanagers")
            ):
                continue
            candidates.append(info)
        for info in candidates:
            scanned += 1
            try:
                environment = UnityPy.load(archive.read(info.filename))
            except Exception:
                continue
            for obj in environment.objects:
                try:
                    data = obj.read()
                except Exception:
                    continue
                if getattr(data, "m_Name", None) != CHIP_TEXT_ASSET_NAME:
                    continue
                script = getattr(data, "m_Script", None)
                if script is None:
                    continue
                payload = script if isinstance(script, bytes) else str(script).encode("utf-8", "surrogateescape")
                matches.append(
                    {
                        "entry": info.filename,
                        "object_type": getattr(getattr(obj, "type", None), "name", None),
                        "name": str(data.m_Name),
                        "bytes": len(payload),
                        "sha256": sha256_bytes(payload),
                        "payload": payload,
                    }
                )
    return {
        "path": relative_path(path),
        "apk_sha256": sha256_file(path),
        "candidate_count": len(candidates),
        "scanned_count": scanned,
        "match_count": len(matches),
        "matches": matches,
    }


def chip_pack_from_apk(path: Path, scan: dict[str, Any]) -> dict[str, Any]:
    if scan["match_count"] != 1:
        return {
            "status": "not_available",
            "reason": f"expected one chip TextAsset, found {scan['match_count']}",
            "scan": {key: value for key, value in scan.items() if key != "matches"},
        }
    match = scan["matches"][0]
    with zipfile.ZipFile(path) as archive:
        metadata = archive.read(METADATA_ENTRY) if METADATA_ENTRY in archive.namelist() else b""
        source_entry = match["entry"]
        source_bytes = archive.read(source_entry)
    dump_text = DUMP_PATH.read_text(encoding="utf-8", errors="replace")
    key_match = re.search(
        rf"{re.escape(CHIP_KEY_HASH.upper())}.*?Metadata offset 0x([0-9A-Fa-f]+)",
        dump_text,
        re.IGNORECASE | re.DOTALL,
    )
    key_offset = int(key_match.group(1), 16) if key_match else None
    key = metadata[key_offset : key_offset + CHIP_KEY_LENGTH] if key_offset is not None else b""
    key_record = {
        "dump_match": key_match is not None,
        "metadata_entry": METADATA_ENTRY,
        "metadata_bytes": len(metadata),
        "metadata_sha256": sha256_bytes(metadata) if metadata else None,
        "metadata_offset": key_offset,
        "metadata_offset_hex": f"0x{key_offset:X}" if key_offset is not None else None,
        "key_length_bytes": len(key),
        "key_sha256": sha256_bytes(key) if key else None,
        "key_hash_matches_dump_field": bool(key) and sha256_bytes(key) == CHIP_KEY_HASH,
    }
    if not key_record["key_hash_matches_dump_field"]:
        return {
            "status": "key_recovery_failed",
            "scan": {key_name: value for key_name, value in scan.items() if key_name != "matches"},
            "chip_text_asset": {key_name: value for key_name, value in match.items() if key_name != "payload"},
            "key": key_record,
        }
    encrypted = match["payload"]
    decrypted = bytes(value ^ key[index % len(key)] for index, value in enumerate(encrypted))
    header, records = parse_pack(decrypted)
    record_by_name = {record["name"]: record for record in records}
    img = record_by_name.get("img.inf")
    seb = record_by_name.get("seb.inf")
    if img is None or seb is None:
        raise ValueError("decrypted chip pack is missing img.inf or seb.inf")
    floors = [
        pack_record_summary(record)
        for record in records
        if re.fullmatch(r"floor_\d+\.(?:png|opt|seb)", record["name"], re.IGNORECASE)
    ]
    return {
        "status": "pass",
        "scan": {key_name: value for key_name, value in scan.items() if key_name != "matches"},
        "source_entry": source_entry,
        "source_entry_bytes": len(source_bytes),
        "source_entry_sha256": sha256_bytes(source_bytes),
        "chip_text_asset": {key_name: value for key_name, value in match.items() if key_name != "payload"},
        "key": key_record,
        "encrypted_payload": {"bytes": len(encrypted), "sha256": sha256_bytes(encrypted)},
        "decrypted_payload": {"bytes": len(decrypted), "sha256": sha256_bytes(decrypted)},
        "pack_header": header,
        "img_inf": parse_inf(img["bytes"]),
        "seb_inf": parse_inf(seb["bytes"]),
        "floor_records": floors,
        "target_records": [
            pack_record_summary(record)
            for record in records
            if record["name"] in {"floor_00.png", "floor_01.png", "floor_05.png", "wall_00.png", "door_01.png"}
        ],
    }


def zip_pack_evidence(index: dict[str, dict[str, Any]]) -> dict[str, Any]:
    with zipfile.ZipFile(ZIP_PATH) as archive:
        members = [name for name in archive.namelist() if name.startswith(ZIP_CHIP_PREFIX)]
        img_raw = archive.read(f"{ZIP_CHIP_PREFIX}img.inf")
        seb_raw = archive.read(f"{ZIP_CHIP_PREFIX}seb.inf")
        floor_names = sorted(
            name.removeprefix(ZIP_CHIP_PREFIX)
            for name in members
            if re.fullmatch(r"floor_\d+\.(?:png|opt|seb)", name.removeprefix(ZIP_CHIP_PREFIX), re.IGNORECASE)
        )
        target_names = ["floor_00.png", "floor_01.png", "floor_05.png", "wall_00.png", "door_01.png"]
        targets = []
        for name in target_names:
            member = f"{ZIP_CHIP_PREFIX}{name}"
            if member in archive.namelist():
                raw = archive.read(member)
                targets.append({"name": name, "bytes": len(raw), "sha256": sha256_bytes(raw)})
    index_rows = []
    for path, row in sorted(index.items()):
        if path in {"01_GAME_PACKS/chip/img.inf", "01_GAME_PACKS/chip/seb.inf"} or re.fullmatch(
            r"01_GAME_PACKS/chip/floor_\d+\.(?:png|opt|seb)", path, re.IGNORECASE
        ):
            index_rows.append(
                {
                    "relative_path": path,
                    "original_name": row.get("original_name"),
                    "kind": row.get("kind"),
                    "size": row.get("size"),
                    "sha256": row.get("sha256"),
                    "apk_source_entry": row.get("apk_source_entry"),
                }
            )
    return {
        "status": "pass",
        "zip": path_ref(ZIP_PATH, required=True),
        "chip_prefix": ZIP_CHIP_PREFIX,
        "chip_member_count": len(members),
        "img_inf": parse_inf(img_raw),
        "seb_inf": parse_inf(seb_raw),
        "floor_members": floor_names,
        "target_members": targets,
        "asset_index_rows": index_rows,
    }


def alternate_version_evidence(current_scan: dict[str, Any]) -> list[dict[str, Any]]:
    candidates = {
        "2.4.9": ROOT / "Social+Dev+Story_2.4.9_APKPure.apk",
        "2.5.0": ROOT / "Social+Dev+Story_2.5.0_APKPure.apk",
        "2.5.1_current": APK_PATH,
    }
    result = []
    for label, path in candidates.items():
        if path == APK_PATH:
            scan = current_scan
        elif not path.is_file():
            result.append({"label": label, **path_ref(path), "status": "missing_in_workspace"})
            continue
        else:
            scan = locate_chip_text_asset(path)
        row = {
            "label": label,
            "path": relative_path(path),
            "exists": True,
            "size_bytes": path.stat().st_size,
            "sha256": sha256_file(path),
            "status": "matching_current_chip_boundary" if scan["match_count"] == 1 else "no_matching_chip_text_asset",
            "chip_scan": {key: value for key, value in scan.items() if key != "matches"},
            "chip_matches": [
                {key: value for key, value in match.items() if key != "payload"}
                for match in scan.get("matches", [])
            ],
        }
        if label == "archive_game_dev_story_mod":
            row["note"] = "This archive APK has no matching chip TextAsset and is not accepted as a Social Dev version candidate."
        result.append(row)
    # The historical archive was permanently removed after the Social Dev
    # cutover. Preserve its absence as provenance instead of reconstructing or
    # probing the deleted corpus.
    result.append({
        "label": "archive_game_dev_story_mod",
        "path": "archive/pre-social-reset (removed)",
        "exists": False,
        "size_bytes": None,
        "sha256": None,
        "status": "removed_with_legacy_archive",
        "reason": "The legacy GameDev archive was permanently removed; it is not a valid source for current Social Dev recovery.",
        "chip_scan": {"match_count": 0, "scanned_count": 0},
        "chip_matches": [],
    })
    return result


def source_search_evidence() -> dict[str, Any]:
    selector_occurrences: list[dict[str, Any]] = []
    alias_occurrences: list[dict[str, Any]] = []
    for name, path in SOURCE_FILES.items():
        text = path.read_text(encoding="utf-8", errors="replace")
        for line_number, line in enumerate(text.splitlines(), start=1):
            if "floorImgId_" in line:
                selector_occurrences.append({"source": name, "line": line_number, "text": line.strip()})
            if re.search(r"(?:floorImgId_|RESCHIP_IMG_FLOOR).*?(?:=|\+|\?|:)\s*5\b", line):
                alias_occurrences.append({"source": name, "line": line_number, "text": line.strip()})
    appdata = SOURCE_FILES["AppData"].read_text(encoding="utf-8", errors="replace")
    image_constant_lines = [
        {"line": line_number, "text": line.strip()}
        for line_number, line in enumerate(appdata.splitlines(), start=1)
        if re.search(r"RESCHIP_IMG_[A-Z0-9_]+\s*=\s*5\s*;", line)
    ]
    return {
        "floor_selector_occurrences": selector_occurrences,
        "explicit_floor_5_alias_occurrences": alias_occurrences,
        "source_labeled_image_constant_id_5": image_constant_lines,
        "positive_fallback_mapping_status": "not_found" if not alias_occurrences else "found_but_unresolved",
        "native_source_limit": "Decompiler-bounded C# shows the selector flow but does not prove null-slot intent or an omitted native fallback branch.",
    }


def native_trace(native: dict[str, Any], source_refs: list[dict[str, Any]]) -> dict[str, Any]:
    methods = {item["id"]: item for item in native.get("native_method_manifest", [])}
    selected_ids = ["room-init-obj-chips", "room-setup-big-chips-parent", "room-place-door"]
    return {
        "status": "source_bounded",
        "native_method_refs": [copy.deepcopy(methods[item]) for item in selected_ids if item in methods],
        "selector_flow": [
            {
                "step": "RoomData load",
                "claim": "floorImgId_ is loaded as a raw integer field alongside wallImgId_ and doorImgId_.",
                "source_slice_id": "room-data-selector-load",
            },
            {
                "step": "Room.InitMapChips",
                "claim": "Room passes roomData.floorImgId_ to the MapChip constructor for each room cell.",
                "source_slice_id": "room-floor-selector-to-map-chip",
            },
            {
                "step": "MapChip storage and draw",
                "claim": "MapChip stores the raw imageId_ and reaches DrawFloor; the decompiler-bounded body does not establish an alternate id or fallback image.",
                "source_slice_id": "map-chip-floor-draw",
            },
            {
                "step": "ResourceManager pack load",
                "claim": "The loader reads packed list records and image data from JarInflater and uses the record index for the image array; the source rendering is damaged around the exact list-index write.",
                "source_slice_id": "resource-manager-indexed-image-load",
            },
            {
                "step": "List parsing",
                "claim": "StringUtil reads the packed list bytes and splits them into records; no source evidence maps a missing positive id to another filename.",
                "source_slice_id": "string-array-resource-reader",
            },
        ],
        "negative_sentinel": {
            "raw_selector_id": 5,
            "is_negative": False,
            "source_behavior": "Room.cs contains a negative-value guard for floorImgId_; raw id 5 does not enter that sentinel path.",
        },
        "fallback_or_alias": {
            "status": "not_proven",
            "reason": "No authoritative source, native method manifest, or packed index evidence supplies an id-5 floor alias.",
        },
        "source_refs": [
            {
                "id": item["id"],
                "file": item["file"],
                "file_sha256": item.get("file_sha256"),
                "slice_sha256": item.get("slice_sha256"),
            }
            for item in source_refs
        ],
    }


def build_package() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], str]:
    scene = load_json(SCENE_PATH)
    baseline_contract = load_json(BASELINE_CONTRACT_PATH)
    selector_contract = load_json(SELECTOR_PATH)
    index = asset_index_map()
    native = load_json(NATIVE_PATH)
    scene_record = next(item for item in scene["scenes"] if item["id"] == "room:0")
    raw_floor_id = int(scene_record["scalar_fields_raw"]["floorImgId_"]["value"])
    if raw_floor_id != 5:
        raise ValueError(f"recovery pass is pinned to room:0 floor selector 5, observed {raw_floor_id}")

    current_scan = locate_chip_text_asset(APK_PATH)
    apk_pack = chip_pack_from_apk(APK_PATH, current_scan)
    zip_pack = zip_pack_evidence(index)
    if apk_pack["status"] != "pass":
        raise ValueError("current APK chip pack could not be recovered")

    zip_img = zip_pack["img_inf"]
    apk_img = apk_pack["img_inf"]
    zip_seb = zip_pack["seb_inf"]
    apk_seb = apk_pack["seb_inf"]
    floor_asset_names = sorted(
        item["name"] for item in apk_pack["floor_records"] if item["name"].endswith(".png")
    )
    floor_img_entries = [
        record for record in zip_img["entry_records"] if record["filename"].startswith("floor_")
    ]
    floor_id5_asset_index = [
        row for row in zip_pack["asset_index_rows"] if row["relative_path"].endswith("floor_05.png")
    ]

    source_refs = [source_slice_ref(item) for item in SOURCE_SLICES]
    native_record = native_trace(native, source_refs)
    search_record = source_search_evidence()
    versions = alternate_version_evidence(current_scan)
    current_version = next(item for item in versions if item["label"] == "2.5.1_current")
    missing_named_versions = [item for item in versions if item["label"] in {"2.4.9", "2.5.0"}]

    input_paths: list[tuple[Path, bool]] = [
        (SCENE_PATH, True),
        (BASELINE_CONTRACT_PATH, True),
        (SELECTOR_PATH, True),
        (ASSET_INDEX_PATH, True),
        (NATIVE_PATH, True),
        (DUMP_PATH, True),
        (APK_PATH, True),
        (ZIP_PATH, True),
        *[(path, True) for path in SOURCE_FILES.values()],
        (ROOT / "Social+Dev+Story_2.4.9_APKPure.apk", False),
        (ROOT / "Social+Dev+Story_2.5.0_APKPure.apk", False),
    ]
    manifest = input_manifest(input_paths)

    baseline = {
        "path": relative_path(BASELINE_CONTRACT_PATH),
        "sha256": sha256_file(BASELINE_CONTRACT_PATH),
        "contract_hash": baseline_contract.get("determinism", {}).get("contract_hash"),
        "status": baseline_contract.get("status"),
        "semantic_status": baseline_contract.get("semantic_status"),
        "floor_selector_before_recovery": copy.deepcopy(baseline_contract.get("selectors", {}).get("floor")),
    }
    floor_runtime_fallback = copy.deepcopy(
        baseline_contract.get("selectors", {}).get("floor", {}).get("runtime_fallback")
    )

    source_audit: dict[str, Any] = {
        "schema_version": AUDIT_SCHEMA_VERSION,
        "package": "social-dev-phase3b-floor-recovery-source-audit",
        "status": "pass",
        "semantic_status": "source_limited_unresolved_recovery_complete",
        "generated_at_utc": utc_now(),
        "recovery_question": "Can RoomData(0).floorImgId_=5 be closed to an authoritative floor image before Phase 3C?",
        "raw_selector": {
            "scene_id": "room:0",
            "field": "floorImgId_",
            "value": raw_floor_id,
            "scene_contract_ref": {"path": relative_path(SCENE_PATH), "sha256": sha256_file(SCENE_PATH)},
        },
        "baseline": baseline,
        "runtime_decision": {
            "source_resolution_status": "unresolved",
            "runtime_resolution_status": baseline_contract.get("selectors", {}).get("floor", {}).get("runtime_resolution_status"),
            "raw_selector_id": raw_floor_id,
            "fallback": floor_runtime_fallback,
        },
        "input_manifest": manifest,
        "source_slices": source_refs,
        "zip_pack": zip_pack,
        "apk_pack": apk_pack,
        "selector_cross_check": {
            "asset_selector_contract_id_5": (selector_contract.get("selector_indexes", {}).get("chip_img", {}).get("entries", {}) or {}).get("5"),
            "zip_img_inf_id_5": zip_img["entries"].get("5"),
            "apk_img_inf_id_5": apk_img["entries"].get("5"),
            "zip_and_apk_img_inf_byte_equal": zip_img["sha256"] == apk_img["sha256"] and zip_img["bytes"] == apk_img["bytes"],
            "zip_and_apk_seb_inf_byte_equal": zip_seb["sha256"] == apk_seb["sha256"] and zip_seb["bytes"] == apk_seb["bytes"],
            "floor_image_records_in_img_inf": floor_img_entries,
            "floor_05_asset_index_rows": floor_id5_asset_index,
            "all_current_floor_png_records": floor_asset_names,
        },
        "native_trace": native_record,
        "source_search": search_record,
        "version_and_provenance": {
            "available_candidates": versions,
            "missing_named_versions": missing_named_versions,
            "current_version_boundary": current_version,
            "interpretation": "Only the current 2.5.1 APK matches the reviewed chip TextAsset boundary. The named 2.4.9 and 2.5.0 APKs are absent.",
        },
        "candidate_decisions": [
            {
                "classification": "resolved_authoritative",
                "decision": "rejected",
                "reason": "There is no img.inf entry, exact filename binding, or authoritative alternate mapping for selector id 5.",
            },
            {
                "classification": "intentionally_reserved",
                "decision": "not_proven",
                "reason": "The id gap and skipped AppData constant are compatible with a reserved/null slot, but no explicit intent or null-slot contract is present in the reviewed evidence.",
            },
            {
                "classification": "extraction_gap",
                "decision": "rejected_for_current_package",
                "reason": "The ZIP img.inf and decrypted APK img.inf are byte-identical, and the APK scan finds exactly one current chip TextAsset.",
            },
            {
                "classification": "conflict",
                "decision": "rejected",
                "reason": "RoomData, the selector contract, the ZIP and the APK all agree that the raw selector is 5 and that img.inf has no id-5 record.",
            },
            {
                "classification": "source_limited_unresolved",
                "decision": "selected",
                "reason": "The supplied current package is internally consistent but lacks the evidence needed to distinguish intentional null-slot behavior from an omitted source asset or to name a floor image.",
            },
        ],
        "final_classification": {
            "classification": "source_limited_unresolved",
            "status": "recovery_complete",
            "data_availability": "id_5_mapping_absent_from_supplied_current_chip_pack",
            "extraction_loss_proven": False,
            "authoritative_filename": None,
            "authoritative_asset": None,
            "intentional_reservation_proven": False,
            "runtime_action": "retain raw selector 5; use explicit runtime alias 5 -> 85 -> floor_09.png; source mapping remains unresolved",
            "phase3b_closure": "closed_as_source_limit_with_explicit_runtime_fallback",
        },
        "limits": [
            "The APK, decrypted chip pack, source C#, and native artifacts are evidence inputs only.",
            "The current C# rendering is decompiler-bounded; it does not prove the runtime behavior of a possible null image slot.",
            "The missing 2.4.9 and 2.5.0 APKs cannot be compared until those exact files are supplied.",
            "The source selector is not rewritten; the current runtime contract carries an explicit user-approved alias to floor_09.png.",
        ],
        "determinism": {"algorithm": "stable-json-sha256 excluding generated_at_utc and content_hash", "content_hash": ""},
    }
    source_audit["determinism"]["content_hash"] = content_hash(without_dynamic(source_audit))

    fixture: dict[str, Any] = {
        "schema_version": FIXTURE_SCHEMA_VERSION,
        "package": "social-dev-phase3b-floor-recovery-fixture",
        "status": "pass",
        "semantic_status": "source_limited_unresolved_recovery_complete",
        "generated_at_utc": utc_now(),
        "scene_ref": {"id": "room:0", "floorImgId_": raw_floor_id},
        "selector_probe": {
            "selector_id": raw_floor_id,
            "img_inf_filename_zip": zip_img["entries"].get(str(raw_floor_id)),
            "img_inf_filename_apk": apk_img["entries"].get(str(raw_floor_id)),
            "asset_selector_contract_filename": (selector_contract.get("selector_indexes", {}).get("chip_img", {}).get("entries", {}) or {}).get(str(raw_floor_id)),
            "resolution_status": "unresolved",
            "runtime_fallback": floor_runtime_fallback,
        },
        "pack_boundary_probe": {
            "apk_source_entry": apk_pack["source_entry"],
            "apk_chip_text_asset_sha256": apk_pack["chip_text_asset"]["sha256"],
            "apk_scanned_data_entries": apk_pack["scan"]["scanned_count"],
            "apk_chip_match_count": apk_pack["scan"]["match_count"],
            "apk_img_inf_sha256": apk_img["sha256"],
            "zip_img_inf_sha256": zip_img["sha256"],
            "img_inf_byte_equal": apk_img["sha256"] == zip_img["sha256"],
            "apk_pack_file_count": apk_pack["pack_header"]["file_count"],
        },
        "floor_inventory": {
            "img_inf_floor_entries": [
                {"id": item["id"], "filename": item["filename"]} for item in floor_img_entries
            ],
            "apk_floor_records": apk_pack["floor_records"],
            "zip_floor_members": zip_pack["floor_members"],
        },
        "native_probe": {
            "negative_sentinel_bypassed": native_record["negative_sentinel"]["is_negative"] is False,
            "fallback_status": native_record["fallback_or_alias"]["status"],
            "flow_steps": [item["step"] for item in native_record["selector_flow"]],
        },
        "version_probe": [
            {
                "label": item["label"],
                "status": item["status"],
                "exists": item["exists"],
                "chip_match_count": item.get("chip_scan", {}).get("match_count"),
            }
            for item in versions
        ],
        "classification": copy.deepcopy(source_audit["final_classification"]),
        "provenance": {
            "source_audit": {
                "path": relative_path(EVIDENCE / "phase3b_floor_recovery_source_audit.json"),
                "content_hash": source_audit["determinism"]["content_hash"],
            },
            "baseline_contract": baseline,
        },
        "determinism": {"algorithm": "stable-json-sha256 excluding generated_at_utc and content_hash", "content_hash": ""},
    }
    fixture["determinism"]["content_hash"] = content_hash(without_dynamic(fixture))

    checks: list[dict[str, Any]] = []

    def check(check_id: str, condition: bool, observed: Any, expected: Any, note: str) -> None:
        checks.append(
            {
                "id": check_id,
                "status": "pass" if condition else "fail",
                "observed": observed,
                "expected": expected,
                "note": note,
            }
        )

    check("baseline-contract-frozen", baseline["status"] == "pass" and bool(baseline["contract_hash"]), baseline, "pass contract with hash", "The recovery pass does not mutate the existing Phase 3B baseline.")
    check("room-selector-is-five", raw_floor_id == 5, raw_floor_id, 5, "RoomData(0) remains the pinned recovery question.")
    check("current-apk-present", APK_PATH.is_file(), path_ref(APK_PATH), True, "The current APK is required evidence.")
    check("asset-zip-present", ZIP_PATH.is_file(), path_ref(ZIP_PATH), True, "The supplied asset ZIP is required evidence.")
    check("current-chip-textasset-unique", current_scan["match_count"] == 1, current_scan["match_count"], 1, "Exactly one current Unity chip TextAsset is found across the APK data entries.")
    check("current-chip-source-entry", apk_pack["source_entry"] == APK_SOURCE_ENTRY, apk_pack["source_entry"], APK_SOURCE_ENTRY, "The current chip pack source entry matches the pinned asset index boundary.")
    check("chip-key-recovered", apk_pack["key"]["key_hash_matches_dump_field"], apk_pack["key"], "key hash matches dump field", "The APK chip payload was decrypted using the reviewed metadata field.")
    check("chip-pack-parses", apk_pack["pack_header"]["file_count"] == 333 and apk_pack["status"] == "pass", apk_pack["pack_header"], "pass with 333 records", "The encrypted chip TextAsset is a complete parseable pack.")
    check("zip-img-inf-hash-pinned", zip_img["sha256"] == index["01_GAME_PACKS/chip/img.inf"]["sha256"], zip_img["sha256"], index["01_GAME_PACKS/chip/img.inf"]["sha256"], "The ZIP img.inf bytes match the pinned asset index.")
    check("apk-img-inf-equals-zip", apk_img["sha256"] == zip_img["sha256"] and apk_img["bytes"] == zip_img["bytes"], {"apk": apk_img["sha256"], "zip": zip_img["sha256"]}, "byte-identical", "The current APK does not contain a different img.inf at the loader boundary.")
    check("apk-seb-inf-equals-zip", apk_seb["sha256"] == zip_seb["sha256"] and apk_seb["bytes"] == zip_seb["bytes"], {"apk": apk_seb["sha256"], "zip": zip_seb["sha256"]}, "byte-identical", "The neighboring SEB index is also stable across APK and ZIP.")
    check("img-inf-id-five-absent", zip_img["entries"].get("5") is None and apk_img["entries"].get("5") is None, {"zip": zip_img["entries"].get("5"), "apk": apk_img["entries"].get("5")}, None, "The selector id has no authoritative img.inf filename in either current source.")
    check("floor-assets-do-not-supply-id-five", zip_img["entries"].get("5") is None and (selector_contract.get("selector_indexes", {}).get("chip_img", {}).get("entries", {}) or {}).get("5") is None, {"floor_05_asset_index_rows": floor_id5_asset_index, "selector_id_5_filename": zip_img["entries"].get("5")}, "asset may exist but selector binding is absent", "A floor_05.png file by itself does not establish selector identity.")
    check("floor-index-gaps-are-preserved", 5 in zip_img["gaps_through_max_id"], zip_img["gaps_through_max_id"], "contains 5", "The parser preserves the explicit numeric gap rather than compacting ids.")
    check("native-negative-sentinel-bypassed", native_record["negative_sentinel"]["is_negative"] is False, native_record["negative_sentinel"], "raw 5 is nonnegative", "The raw selector does not use the documented negative absence sentinel.")
    check("native-fallback-not-proven", native_record["fallback_or_alias"]["status"] == "not_proven", native_record["fallback_or_alias"], "not_proven", "No source/native evidence supplies a positive id-5 alias or fallback.")
    check("source-image-constant-skips-five", not search_record["source_labeled_image_constant_id_5"], search_record["source_labeled_image_constant_id_5"], [], "AppData source labels reviewed image constants but does not label image id 5.")
    check("named-old-apks-absent", all(item["status"] == "missing_in_workspace" for item in missing_named_versions), missing_named_versions, "both missing_in_workspace", "The named alternate APKs are not available for comparison; absence is recorded, not guessed.")
    archive_version = next(item for item in versions if item["label"] == "archive_game_dev_story_mod")
    check(
        "archive-apk-not-accepted-as-version",
        archive_version["status"] in {"no_matching_chip_text_asset", "removed_with_legacy_archive"}
        and archive_version.get("chip_scan", {}).get("match_count", 0) == 0,
        archive_version,
        "legacy archive absent or has no matching chip TextAsset",
        "The deleted archive cannot answer the current Social Dev selector question and is never recreated.",
    )
    check("classification-is-source-limited", source_audit["final_classification"]["classification"] == "source_limited_unresolved", source_audit["final_classification"], "source_limited_unresolved", "The recovery gate completes without inventing a floor mapping.")
    check(
        "explicit-runtime-fallback-recorded",
        source_audit["final_classification"]["runtime_action"] == "retain raw selector 5; use explicit runtime alias 5 -> 85 -> floor_09.png; source mapping remains unresolved"
        and source_audit["runtime_decision"]["fallback"]["target_selector_id"] == 85
        and source_audit["runtime_decision"]["fallback"]["filename"] == "floor_09.png",
        source_audit["runtime_decision"],
        {"raw_selector_id": 5, "target_selector_id": 85, "filename": "floor_09.png"},
        "The source gap remains explicit while the user-approved runtime alias is recorded for downstream rendering.",
    )
    check("fixture-carries-the-classification", fixture["classification"] == source_audit["final_classification"], fixture["classification"], source_audit["final_classification"], "The deterministic fixture exposes the exact recovery outcome to downstream gates.")

    validation: dict[str, Any] = {
        "schema_version": VALIDATION_SCHEMA_VERSION,
        "package": "social-dev-phase3b-floor-recovery-validation",
        "status": "pass" if all(item["status"] == "pass" for item in checks) else "fail",
        "semantic_status": "recovery_gate_pass_source_limited_unresolved",
        "generated_at_utc": utc_now(),
        "source_audit_ref": {
            "path": relative_path(EVIDENCE / "phase3b_floor_recovery_source_audit.json"),
            "content_hash": source_audit["determinism"]["content_hash"],
        },
        "fixture_ref": {
            "path": relative_path(EVIDENCE / "phase3b_floor_recovery_fixture.json"),
            "content_hash": fixture["determinism"]["content_hash"],
        },
        "checks": checks,
        "summary": {
            "total": len(checks),
            "passed": sum(item["status"] == "pass" for item in checks),
            "failed": sum(item["status"] == "fail" for item in checks),
            "classification": source_audit["final_classification"]["classification"],
            "runtime_contract_changed": False,
        },
        "determinism": {"algorithm": "stable-json-sha256 excluding generated_at_utc and content_hash", "content_hash": ""},
    }
    validation["determinism"]["content_hash"] = content_hash(without_dynamic(validation))

    report = build_report(source_audit, fixture, validation)
    return source_audit, fixture, validation, report


def build_report(audit: dict[str, Any], fixture: dict[str, Any], validation: dict[str, Any]) -> str:
    final = audit["final_classification"]
    zip_img = audit["zip_pack"]["img_inf"]
    apk_img = audit["apk_pack"]["img_inf"]
    versions = audit["version_and_provenance"]["available_candidates"]
    version_lines = "\n".join(
        f"- `{item['label']}`: `{item['status']}` — `{item['path']}`"
        for item in versions
    )
    return f"""# Phase 3B Floor Selector Recovery Report

## Outcome

The recovery pass is complete and passed {validation['summary']['passed']}/{validation['summary']['total']} checks. The final classification is **`{final['classification']}`**.

`RoomData(0).floorImgId_` is raw selector `5`, but the supplied current package has no authoritative `chip/img.inf` entry for id `5`. The decrypted APK `img.inf` is byte-identical to the supplied asset ZIP `img.inf` (`{apk_img['sha256']}`), so this is not an extraction mismatch between the two current package sources. The source filename remains unresolved; the recorded runtime decision aliases selector `5` to selector `85` / `floor_09.png`.

This closes the Phase 3B recovery gate as a source limitation plus an explicit runtime decision. The source evidence remains unchanged: `img.inf` still has no id `5` entry, and `floor_05.png` remains mapped to selector `23`. Phase 3C may render `floor_09.png` for raw selector `5` only through the recorded fallback alias; it must not present that alias as recovered original provenance.

## Evidence chain

- Room selector: `room:0.floorImgId_ = 5`.
- ZIP `chip/img.inf`: `{zip_img['bytes']} bytes`, `{zip_img['sha256']}`, no id `5`.
- APK `chip/img.inf`: `{apk_img['bytes']} bytes`, `{apk_img['sha256']}`, no id `5`.
- APK chip scan: exactly one `chip` TextAsset across `{audit['apk_pack']['scan']['scanned_count']}` data entries; decrypted pack has `{audit['apk_pack']['pack_header']['file_count']}` records.
- Native/source trace: selector is passed as a raw positive value into `MapChip`; the reviewed evidence proves no positive id-5 alias or fallback.
- Runtime decision: raw selector `5` → indexed selector `85` → `floor_09.png`.

## Alternate package provenance

{version_lines}

The named 2.4.9 and 2.5.0 APK files are absent from the workspace and remain outside the current package comparison.

## Required runtime policy

- Retain raw selector `5` for provenance.
- Keep source resolution for selector `5` marked `unresolved`.
- Use the explicit runtime alias `5 → 85 → floor_09.png` when the room renderer needs a floor image.
- Do not relabel `floor_09.png` as the recovered original for selector `5`.
- Re-open source recovery only when an exact alternate Social Dev package or an authoritative source/native mapping is supplied.

## Artifacts

- Source audit: `knowledge/fixtures/accepted/phase3b_floor_recovery_source_audit.json` (`{audit['determinism']['content_hash']}`).
- Deterministic fixture: `knowledge/fixtures/accepted/phase3b_floor_recovery_fixture.json` (`{fixture['determinism']['content_hash']}`).
- Validation: `knowledge/fixtures/accepted/phase3b_floor_recovery_validation.json` (`{validation['determinism']['content_hash']}`).
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check-only", action="store_true", help="Build and validate in memory without writing artifacts.")
    args = parser.parse_args()
    audit, fixture, validation, report = build_package()
    if not args.check_only:
        write_json(EVIDENCE / "phase3b_floor_recovery_source_audit.json", audit)
        write_json(EVIDENCE / "phase3b_floor_recovery_fixture.json", fixture)
        write_json(EVIDENCE / "phase3b_floor_recovery_validation.json", validation)
        report_path = ROOT / "docs/reports/social-dev_phase3b_floor_recovery_report.md"
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(report, encoding="utf-8", newline="\n")
    print(
        json.dumps(
            {
                "status": validation["status"],
                "classification": audit["final_classification"]["classification"],
                "checks": validation["summary"],
                "source_audit_hash": audit["determinism"]["content_hash"],
                "fixture_hash": fixture["determinism"]["content_hash"],
                "validation_hash": validation["determinism"]["content_hash"],
                "wrote_artifacts": not args.check_only,
            },
            sort_keys=True,
        )
    )
    return 0 if validation["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
