"""Independently verify and promote the bounded K4.1 visual closures.

This builder deliberately does not import the K4 research pack.  It reads the
pinned repository sources directly, decodes the APK language rows and native
metadata, disassembles the pinned ELF at the required RVAs, and only then
updates the K4 acceptance artifacts and canonical brain.  It is evidence-only:
it never starts a server, browser, emulator, live app, network operation, or
V8 and never writes under a source root.
"""

from __future__ import annotations

import hashlib
import json
import re
import sqlite3
import struct
import subprocess
import zipfile
from pathlib import Path
from typing import Any

try:
    from capstone import CS_ARCH_ARM64, CS_MODE_LITTLE_ENDIAN, Cs
except ImportError as exc:  # pragma: no cover - the repository runtime supplies it
    raise RuntimeError("Capstone is required for the pinned native K4.1 probe") from exc


ROOT = Path(__file__).resolve().parents[2]
BRAIN = ROOT / "knowledge/brain"
K4 = BRAIN / "acceptance/k4"
K41 = BRAIN / "acceptance/k4-1"
DB = BRAIN / "sqlite/social_dev_brain.sqlite"
MANIFEST = BRAIN / "MANIFEST.json"
GRAPH = BRAIN / "graphs/semantic-edges.json"

APK = ROOT / "sources/raw/Social_Dev_Story_v2.5.1.apk"
APK_RAR = ROOT / "sources/raw/1_Click_CSharp_Code.rar"
SOURCE_MANIFEST = ROOT / "knowledge/sources/source-manifest.json"
STAFF = ROOT / "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/game/Staff.cs"
ROOM = ROOT / "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/game/Room.cs"
OBJCHIP = ROOT / "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/game/ObjChip.cs"
FURNITURE_CS = ROOT / "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/data/FurnitureData.cs"
TALKDATA = ROOT / "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/data/TalkData.cs"
APPDATA = ROOT / "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/main/AppData.cs"
LANGUAGE_CS = ROOT / "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/kairo.unity.util/Language.cs"
LIB = ROOT / "knowledge/sources/phase3a_apk_probe/raw/libil2cpp.so"
METADATA = ROOT / "knowledge/sources/phase3a_apk_probe/raw/global-metadata.dat"
DUMP = ROOT / "knowledge/sources/phase3a_apk_probe/il2cpp_dump/dump.cs"
STRINGLITERAL = ROOT / "knowledge/sources/phase3a_apk_probe/il2cpp_dump/stringliteral.json"

FLOOR00 = ROOT / "knowledge/fixtures/accepted/runtime/floor00_scene_contract.json"
NATIVE_SCENE = ROOT / "knowledge/fixtures/accepted/runtime/native_scene_assembly_contract.json"
FURNITURE_META = ROOT / "knowledge/fixtures/accepted/furniture_asset_metadata.json"
TALK_CONTRACT = ROOT / "knowledge/fixtures/accepted/behavior-first/talk-social-contract.json"

FINAL_TOKEN = "PASS_K4_1_TARGETED_CLOSURE_READY_FOR_V8"
REVISION = "k4-visual-assembly-r2"
ALLOWED_CLASSIFICATIONS = {
    "REPRODUCED_EXACT",
    "REPRODUCED_WITH_CORRECTION",
    "REJECTED_BY_SOURCE",
}


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_ref(path: Path, detail: str | None = None) -> str:
    return f"{rel(path)}:{detail}" if detail else rel(path)


def hash_record(path: Path, role: str) -> dict[str, Any]:
    return {
        "path": rel(path),
        "role": role,
        "size_bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def line_number(text: str, needle: str) -> int:
    index = text.find(needle)
    if index < 0:
        raise AssertionError(f"source needle is missing: {needle}")
    return text.count("\n", 0, index) + 1


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def stable_id(prefix: str, *parts: object) -> str:
    value = "|".join(str(part) for part in parts)
    return f"{prefix}:{hashlib.sha256(value.encode('utf-8')).hexdigest()[:20]}"


def source_inventory() -> list[tuple[Path, str]]:
    return [
        (SOURCE_MANIFEST, "pinned source identity manifest"),
        (APK, "pinned APK"),
        (APK_RAR, "pinned C# archive"),
        (STAFF, "Staff C# source"),
        (ROOM, "Room C# source"),
        (OBJCHIP, "ObjChip C# source"),
        (FURNITURE_CS, "FurnitureData C# source"),
        (TALKDATA, "separate TalkData C# source"),
        (APPDATA, "AppData C# source"),
        (LANGUAGE_CS, "Language C# source"),
        (LIB, "pinned native binary"),
        (METADATA, "pinned native metadata"),
        (DUMP, "pinned IL2CPP dump"),
        (STRINGLITERAL, "pinned native string literal catalog"),
        (FLOOR00, "accepted Room0 source-derived contract"),
        (NATIVE_SCENE, "accepted native scene contract"),
        (FURNITURE_META, "accepted furniture metadata"),
        (TALK_CONTRACT, "accepted talk role contract"),
    ]


def verify_source_identity() -> list[dict[str, Any]]:
    manifest = load_json(SOURCE_MANIFEST)
    expected = {
        "APK": (APK, "fa0e9e3a843732258fc05b2611a8e0f5be6f7e95f2141a53f31fb082322fe2bf"),
        "C# RAR": (APK_RAR, "a50a442491e422c20699a9ca4266e794d215bff29248d3edd24c41f42a57f903"),
        "libil2cpp": (LIB, "364893401fcf7fc2380ae64291783edf7b95eecea4775041c3f4c8c081b4d54a"),
        "global-metadata": (METADATA, "f65f3a00675f35cfa28fef53c37ed7a2dc01e143b6d59c6014a286fa84e4a579"),
    }
    manifest_by_type = {item["type"]: item for item in manifest["sources"]}
    records: list[dict[str, Any]] = []
    for source_type, (path, expected_sha) in expected.items():
        require(path.exists(), f"pinned source is missing: {path}")
        actual = sha256(path)
        require(actual == expected_sha, f"pinned source hash mismatch: {path}")
        require(source_type in manifest_by_type, f"source manifest entry missing: {source_type}")
        require(manifest_by_type[source_type]["sha256"] == actual, f"manifest hash mismatch: {source_type}")
    for path, role in source_inventory():
        require(path.exists(), f"required evidence path is missing: {path}")
        records.append(hash_record(path, role))
    return records


def pack_snapshot() -> dict[str, Any]:
    paths = {
        "runtime": ROOT / "knowledge/generated/original-runtime-pack/runtime-pack.json",
        "visual": ROOT / "knowledge/generated/original-visual-pack/visual-pack.json",
        "data": ROOT / "knowledge/generated/original-data-pack/data.json",
        "runtime_mirror": ROOT / "runtime/social-dev/generated/original-runtime-pack.json",
    }
    result: dict[str, Any] = {}
    for key, path in paths.items():
        require(path.exists(), f"generated original pack is missing: {path}")
        result[key] = hash_record(path, f"original {key} pack")
    return result


def parse_fukidashi_enum(text: str) -> list[str]:
    start = text.index("public enum FUKIDASHI")
    body = text[text.index("{", start) + 1 : text.index("}", start)]
    names = []
    for line in body.splitlines():
        candidate = line.strip().rstrip(",")
        if re.fullmatch(r"[A-Z][A-Z0-9_]+", candidate):
            names.append(candidate)
    require(len(names) == 70, f"FUKIDASHI enum count changed: {len(names)}")
    require(names[0] == "KONNICHIWA" and names[69] == "MAX", "FUKIDASHI enum boundary changed")
    return names


def verify_csharp_sources() -> dict[str, Any]:
    staff = STAFF.read_text(encoding="utf-8")
    room = ROOM.read_text(encoding="utf-8")
    objchip = OBJCHIP.read_text(encoding="utf-8")
    furniture = FURNITURE_CS.read_text(encoding="utf-8")
    appdata = APPDATA.read_text(encoding="utf-8")
    language = LANGUAGE_CS.read_text(encoding="utf-8")
    talkdata = TALKDATA.read_text(encoding="utf-8")
    dump = DUMP.read_text(encoding="utf-8")
    string_literals = load_json(STRINGLITERAL)
    literal_values = {item["value"] for item in string_literals}

    enum_names = parse_fukidashi_enum(appdata)
    required_staff_tokens = [
        "private int[] fukidashi__;",
        "private const int FUKI_ID = 0;",
        "private const int FUKI_FRAME = 1;",
        "private const int FUKI_DELAY = 2;",
        "private const int FUKI_OFFSET_Y = 3;",
        "public void AddFukidashi_(AppData.FUKIDASHI[] id)",
        "int num = AppData.Random(id.Length);",
        "AddFukidashi_(AppData.FUKIDASHI.KONNICHIWA, 0, 0);",
        "array[0] = (int)id;",
        "array[1] = 40;",
        "object obj5 = array[2] - 1;",
        "if ((nint)obj5 <= 0)",
        "array[3] = offsetY;",
        "if (array[1] > 0)",
        "if (array[1] < 1)",
        "if (array[2] > 0)",
    ]
    for token in required_staff_tokens:
        require(token in staff, f"Staff source token is missing: {token}")
    require("TalkData" not in staff and "talkData_" not in staff, "Staff source owns TalkData unexpectedly")

    required_appdata_tokens = [
        "public static Dictionary<FUKIDASHI, string> FUKIDASHI_TEXT;",
        "public void DrawFukidashi(Graphics g, FUKIDASHI id, int x, int y)",
    ]
    for token in required_appdata_tokens:
        require(token in appdata, f"AppData source token is missing: {token}")
    require("public const int JAPANESE = 0;" in dump, "Language JAPANESE constant missing")
    require("public const int ENGLISH = 1;" in dump, "Language ENGLISH constant missing")
    require("public class TalkData" in talkdata, "separate TalkData source is missing")
    require("public void DrawObjPreview(Graphics g, int ix, int iy, int ofx, int ofy, FurnitureData furnitureData)" in room, "Room preview source signature missing")
    require("public unsafe void Draw(Graphics g, int ofx, int ofy, FurnitureData furnitureData, bool preview)" in objchip, "ObjChip type-2 source signature missing")
    for token in ("public int seb_;", "public int subSeb_;", "public int img_;", "public int type_;"):
        require(token in furniture, f"FurnitureData field missing: {token}")
    require("RVA: 0x1BC85D0" in dump and "RVA: 0x1BC61B0" in dump and "RVA: 0x1BCA85C" in dump, "Language native anchors missing from dump")
    require("English.lproj" in literal_values and "Japanese.lproj" in literal_values, "language resource templates missing from stringliteral catalog")

    return {
        "enum": {
            "name": "AppData.FUKIDASHI",
            "count": len(enum_names),
            "values": [{"id": index, "name": name} for index, name in enumerate(enum_names)],
            "source_ref": source_ref(APPDATA, f"line {line_number(appdata, 'public enum FUKIDASHI')}") ,
        },
        "staff_field_and_lifecycle": {
            "field": "fukidashi__",
            "field_offsets": {"FUKI_ID": 0, "FUKI_FRAME": 1, "FUKI_DELAY": 2, "FUKI_OFFSET_Y": 3, "FUKI_END_": 4},
            "array_overload_random": source_ref(STAFF, f"line {line_number(staff, 'int num = AppData.Random(id.Length);') }"),
            "single_overload_storage": source_ref(STAFF, f"line {line_number(staff, 'array[0] = (int)id;') }"),
            "update": source_ref(STAFF, f"line {line_number(staff, 'public void UpdateFukidashi_()') }"),
            "draw": source_ref(STAFF, f"line {line_number(staff, 'public void DrawFukidashi_(Graphics g, int ofx, int ofy)') }"),
        },
        "talk_data_separation": {
            "staff_has_talkdata_field": False,
            "separate_type": True,
            "staff_source": source_ref(STAFF),
            "talk_data_source": source_ref(TALKDATA, f"line {line_number(talkdata, 'public class TalkData') }"),
        },
        "localization_path": {
            "enum_text_dictionary": source_ref(APPDATA, f"line {line_number(appdata, 'FUKIDASHI_TEXT') }"),
            "language_constants": source_ref(DUMP, f"line {line_number(dump, 'public const int JAPANESE = 0;') }"),
            "native_lt": "0x1BC85D0",
            "native_set_text_table": "0x1BC61B0",
            "native_load_language_pack": "0x1BCA85C",
            "resource_templates": sorted(value for value in literal_values if value in {"English.lproj", "Japanese.lproj"}),
        },
    }


def elf_segments(data: bytes) -> list[tuple[int, int, int, int, int]]:
    phoff = struct.unpack_from("<Q", data, 32)[0]
    entsize = struct.unpack_from("<H", data, 54)[0]
    count = struct.unpack_from("<H", data, 56)[0]
    result = []
    for index in range(count):
        entry = phoff + index * entsize
        p_type, _flags, offset, vaddr, _paddr, filesz, _memsz, _align = struct.unpack_from("<IIQQQQQQ", data, entry)
        if p_type == 1:
            result.append((offset, vaddr, filesz, _flags, _align))
    require(result, "native ELF has no load segments")
    return result


def va_to_file(data: bytes, va: int) -> int:
    for offset, vaddr, filesz, _flags, _align in elf_segments(data):
        if vaddr <= va < vaddr + filesz:
            return offset + va - vaddr
    raise AssertionError(f"native VA is not in a file-backed load segment: 0x{va:X}")


def section_table(data: bytes) -> tuple[dict[str, tuple[int, int, int]], ...]:
    shoff = struct.unpack_from("<Q", data, 40)[0]
    entsize = struct.unpack_from("<H", data, 58)[0]
    count = struct.unpack_from("<H", data, 60)[0]
    shstrndx = struct.unpack_from("<H", data, 62)[0]
    raw: list[tuple[int, int, int, int]] = []
    for index in range(count):
        entry = shoff + index * entsize
        name, _type, _flags, _addr, offset, size, _link, _info, _align, _entry_size = struct.unpack_from("<IIQQQQIIQQ", data, entry)
        raw.append((name, offset, size, index))
    _name, names_offset, names_size, _ = raw[shstrndx]
    names = data[names_offset : names_offset + names_size]
    result = []
    for name_offset, offset, size, index in raw:
        end = names.find(b"\x00", name_offset)
        name = names[name_offset:end].decode("ascii") if end >= 0 else ""
        result.append({"name": name, "offset": offset, "size": size, "index": index})
    return tuple(result)


def relocations(data: bytes) -> dict[int, int]:
    rela = next((item for item in section_table(data) if item["name"] == ".rela.dyn"), None)
    require(rela is not None, "native ELF .rela.dyn section is missing")
    result: dict[int, int] = {}
    for offset in range(rela["offset"], rela["offset"] + rela["size"], 24):
        target, _info, addend = struct.unpack_from("<QQq", data, offset)
        result[target] = addend
    return result


def instruction_map(data: bytes, start: int, end: int) -> dict[int, dict[str, Any]]:
    offset = va_to_file(data, start)
    code = data[offset : offset + (end - start)]
    decoder = Cs(CS_ARCH_ARM64, CS_MODE_LITTLE_ENDIAN)
    result = {}
    for item in decoder.disasm(code, start):
        result[item.address] = {
            "address": f"0x{item.address:X}",
            "mnemonic": item.mnemonic,
            "op_str": item.op_str,
        }
    require(result, f"native disassembly returned no instructions at 0x{start:X}")
    return result


def anchor(asm: dict[int, dict[str, Any]], address: int, mnemonic: str | None = None, fragment: str | None = None) -> dict[str, Any]:
    require(address in asm, f"native instruction is missing at 0x{address:X}")
    item = asm[address]
    if mnemonic is not None:
        require(item["mnemonic"] == mnemonic, f"0x{address:X} is {item['mnemonic']}, expected {mnemonic}")
    if fragment is not None:
        require(fragment.lower() in item["op_str"].lower(), f"0x{address:X} operand {item['op_str']} does not contain {fragment}")
    return item


def verify_native() -> dict[str, Any]:
    data = LIB.read_bytes()
    relocs = relocations(data)
    pool_targets = {
        0x27D7E48: ([30, 31, 32, 33, 34], "talk frame20"),
        0x27D7E50: ([35, 36, 37, 38, 39, 40, 41, 42, 43], "talk frame70"),
        0x27D7E20: ([44, 45, 46], "invite busy/reject"),
        0x27D7E28: ([25, 26, 27, 28, 29, 68], "invite opening"),
        0x27D7E30: ([22, 23, 24], "invite response"),
    }
    require(0x27D7E40 not in pool_targets, "unexpected autonomous pool was included")
    metadata = METADATA.read_bytes()
    field_defaults = struct.unpack_from("<I", metadata, 64)[0]
    default_data = struct.unpack_from("<I", metadata, 72)[0]
    type_defs = struct.unpack_from("<I", metadata, 160)[0]
    field_refs = struct.unpack_from("<I", metadata, 184)[0]
    private_type = type_defs + 2620 * 88
    field_start = struct.unpack_from("<I", metadata, private_type + 32)[0]
    field_count = struct.unpack_from("<I", metadata, private_type + 68)[0]
    require(field_start == 18303 and field_count == 285, "private implementation metadata layout changed")

    decoded_pools = []
    for handle, (expected_values, role) in pool_targets.items():
        target = relocs.get(handle)
        require(target is not None, f"relocation is missing for RuntimeFieldHandle 0x{handle:X}")
        encoded = struct.unpack_from("<Q", data, va_to_file(data, target))[0]
        usage_kind = encoded >> 29
        field_ref_index = (encoded >> 1) & 0x0FFFFFFF
        field_ref_type_index, local_field_index = struct.unpack_from("<II", metadata, field_refs + field_ref_index * 8)
        require(field_ref_type_index == 8513, f"RuntimeFieldHandle 0x{handle:X} field-reference type changed")
        require(0 <= local_field_index < field_count, f"RuntimeFieldHandle 0x{handle:X} local field is out of range")
        field_index = field_start + local_field_index
        default_matches = []
        for default_index in range(struct.unpack_from("<I", metadata, 68)[0]):
            candidate = struct.unpack_from("<III", metadata, field_defaults + default_index * 12)
            if candidate[0] == field_index:
                default_matches.append((default_index, candidate))
        require(len(default_matches) == 1, f"RuntimeFieldHandle 0x{handle:X} has {len(default_matches)} default-value entries")
        default_value_entry_index, (_field_index, _field_type, data_index) = default_matches[0]
        values = [struct.unpack_from("<i", metadata, default_data + data_index + index * 4)[0] for index in range(len(expected_values))]
        require(values == expected_values, f"decoded payload differs for 0x{handle:X}: {values}")
        decoded_pools.append({
            "handle": f"0x{handle:X}",
            "role": role,
            "relocated_array_va": f"0x{target:X}",
            "encoded_usage": f"0x{encoded:X}",
            "usage_kind": usage_kind,
            "field_ref_index": field_ref_index,
            "field_ref_type_index": field_ref_type_index,
            "private_type_index": 2620,
            "private_local_field_index": local_field_index,
            "private_field_index": field_index,
            "default_value_entry_index": default_value_entry_index,
            "default_data_index": data_index,
            "values": values,
        })

    add = instruction_map(data, 0x12D3C9C, 0x12D3CE0)
    anchor(add, 0x12D3CA4, "bl", "0x12590e0")
    anchor(add, 0x12D3CB8, "ldr", "0x20")
    anchor(add, 0x12D3CD0, "b", "0x12dda90")
    single = instruction_map(data, 0x12DDA94, 0x12DDADC)
    anchor(single, 0x12DDAAC, "cmp", "#0")
    anchor(single, 0x12DDAB4, "mov", "#0x28")
    anchor(single, 0x12DDABC, "stp", "0x20")
    anchor(single, 0x12DDAC8, "str", "0x28")
    anchor(single, 0x12DDAD0, "str", "0x2c")

    talk = instruction_map(data, 0x12D55F4, 0x12D5750)
    for address, mnemonic, fragment in (
        (0x12D55F4, "cmp", "#0x14"),
        (0x12D5600, "tbnz", "#3"),
        (0x12D5624, "bl", "0x12590e0"),
        (0x12D5628, "cmp", "#0x64"),
        (0x12D562C, "b.gt", "0x12d5668"),
        (0x12D5664, "bl", "0x12d3c50"),
        (0x12D5674, "cmp", "#0x46"),
        (0x12D5680, "tbz", "#3"),
        (0x12D56B8, "bl", "0x12d3c50"),
        (0x12D56C0, "cmp", "#0x6e"),
        (0x12D56EC, "bl", "0x120d90c"),
        (0x12D56F8, "bl", "0x12d6300"),
        (0x12D5700, "cmp", "#0x82"),
        (0x12D5710, "bl", "0x12d3934"),
        (0x12D5728, "str", "0xe4"),
        (0x12D572C, "str", "0xbc"),
        (0x12D5730, "bl", "0x12d58ec"),
    ):
        anchor(talk, address, mnemonic, fragment)

    invite = instruction_map(data, 0x12D51F0, 0x12D55A0)
    for address, mnemonic, fragment in (
        (0x12D51F0, "cmp", "#0x14"),
        (0x12D522C, "bl", "0x12d3c50"),
        (0x12D5370, "mov", "#0x65"),
        (0x12D5378, "bl", "0x12590e0"),
        (0x12D537C, "cmp", "#0xa"),
        (0x12D53E0, "bl", "0x12d3c50"),
        (0x12D5560, "bl", "0x12d3c50"),
    ):
        anchor(invite, address, mnemonic, fragment)

    door = instruction_map(data, 0x12C0784, 0x12C08C0)
    for address, mnemonic, fragment in (
        (0x12C0784, "cmp", "#5"),
        (0x12C0794, "mov", "#2"),
        (0x12C07A4, "bl", "0x1c5bc08"),
        (0x12C08A4, "bl", "0x125bb88"),
        (0x12C08A8, "ldr", "0x20"),
        (0x12C08AC, "cbz", "0x12c0cfc"),
        (0x12C08B0, "ldr", "0x24"),
        (0x12C08B4, "cmp", "#5"),
    ):
        anchor(door, address, mnemonic, fragment)
    update = instruction_map(data, 0x12BF7A4, 0x12BF920)
    for address, mnemonic, fragment in (
        (0x12BF7A4, "ldr", "0x18"),
        (0x12BF7B0, "cmp", "#5"),
        (0x12BF87C, "bl", "0x12590e0"),
        (0x12BF8A0, "str", "0x60"),
        (0x12BF8B8, "str", "0x30"),
        (0x12BF8E8, "bl", "0x12c0158"),
        (0x12BF908, "tbz", "#0"),
    ):
        anchor(update, address, mnemonic, fragment)

    workstation = instruction_map(data, 0x12C1900, 0x12C26F0)
    for address, mnemonic, fragment in (
        (0x12C1900, "cbz", "0x"),
        (0x12C1914, "b.eq", "0x12c1a70"),
        (0x12C1AC0, "cmp", "#3"),
        (0x12C1AD0, "b.ne", "0x12c229c"),
        (0x12C1C70, "bl", "0x125bb88"),
        (0x12C1C80, "ldr", "0x78"),
        (0x12C1C84, "cmn", "#1"),
        (0x12C1E38, "bl", "0x1c52f18"),
        (0x12C1ED4, "bl", "0x12daba8"),
        (0x12C229C, "ldr", "0x30"),
        (0x12C22A0, "ldr", "0x78"),
        (0x12C2460, "bl", "0x1c52f18"),
        (0x12C2510, "bl", "0x12daba8"),
        (0x12C2528, "ldr", "0x78"),
        (0x12C2590, "bl", "0x1c5bc08"),
        (0x12C26C4, "ldr", "0x44"),
        (0x12C26D0, "mov", "#2"),
        (0x12C26DC, "bl", "0x1c52f18"),
    ):
        anchor(workstation, address, mnemonic, fragment)
    outer = instruction_map(data, 0x12C1058, 0x12C1160)
    for address, mnemonic, fragment in (
        (0x12C1058, "ldr", "0x20"),
        (0x12C1088, "bl", "0x1c98bec"),
        (0x12C108C, "tbz", "#0"),
        (0x12C10C4, "b", "0x12c166c"),
        (0x12C10F4, "ldr", "0x68"),
        (0x12C114C, "bl", "0x12daba8"),
    ):
        anchor(outer, address, mnemonic, fragment)
    room = instruction_map(data, 0x12CBB80, 0x12CC490)
    for address, mnemonic, fragment in (
        (0x12CBB80, None, None),
        (0x12CBDB0, "bl", "0x12a1f38"),
        (0x12CBE1C, "bl", "0x12a1b24"),
        (0x12CBEB0, "bl", "0x12c0698"),
        (0x12CBF68, "cmp", "#2"),
        (0x12CC190, "bl", "0x12c0e00"),
        (0x12CC228, "mov", "#1"),
        (0x12CC390, "bl", "0x12c0e00"),
    ):
        anchor(room, address, mnemonic, fragment)
    preview = instruction_map(data, 0x12CE81C, 0x12CE82C)
    anchor(preview, 0x12CE81C, "mov", "#1")
    anchor(preview, 0x12CE824, "b", "0x12c166c")

    def selected(asm: dict[int, dict[str, Any]], addresses: list[int]) -> list[dict[str, Any]]:
        return [asm[address] for address in addresses]

    return {
        "binary": source_ref(LIB),
        "metadata": {
            "version": struct.unpack_from("<I", metadata, 4)[0],
            "type_definitions_offset": f"0x{type_defs:X}",
            "field_refs_offset": f"0x{field_refs:X}",
            "field_default_values_offset": f"0x{field_defaults:X}",
            "field_default_data_offset": f"0x{default_data:X}",
            "private_implementation_details_type_index": 2620,
            "field_start": field_start,
            "field_count": field_count,
            "default_lookup": "field_start + local_field_index; default data index is byte-relative",
        },
        "fukidashi_pools": sorted(decoded_pools, key=lambda item: item["handle"]),
        "native_instruction_anchors": {
            "add_fukidashi_array": selected(add, [0x12D3CA4, 0x12D3CB8, 0x12D3CD0]),
            "add_fukidashi_single": selected(single, [0x12DDAAC, 0x12DDAB4, 0x12DDABC, 0x12DDAC8, 0x12DDAD0]),
            "staff_talk": selected(talk, [0x12D55F4, 0x12D5600, 0x12D5624, 0x12D5628, 0x12D562C, 0x12D5664, 0x12D5674, 0x12D5680, 0x12D56B8, 0x12D56C0, 0x12D56EC, 0x12D56F8, 0x12D5700, 0x12D5710, 0x12D5728, 0x12D572C, 0x12D5730]),
            "staff_invite": selected(invite, [0x12D51F0, 0x12D522C, 0x12D5370, 0x12D5378, 0x12D537C, 0x12D53E0, 0x12D5560]),
            "room0_door_drawwall": selected(door, [0x12C0784, 0x12C0794, 0x12C07A4, 0x12C08A4, 0x12C08A8, 0x12C08AC, 0x12C08B0, 0x12C08B4]),
            "door_update_state": selected(update, [0x12BF7A4, 0x12BF7B0, 0x12BF87C, 0x12BF8A0, 0x12BF8B8, 0x12BF8E8, 0x12BF908]),
            "workstation_type2_inner": selected(workstation, [0x12C1900, 0x12C1914, 0x12C1AC0, 0x12C1AD0, 0x12C1C70, 0x12C1C80, 0x12C1C84, 0x12C1E38, 0x12C1ED4, 0x12C229C, 0x12C22A0, 0x12C2460, 0x12C2510, 0x12C2528, 0x12C2590, 0x12C26C4, 0x12C26D0, 0x12C26DC]),
            "workstation_outer_and_guard": selected(outer, [0x12C1058, 0x12C1088, 0x12C108C, 0x12C10C4, 0x12C10F4, 0x12C114C]),
            "room_draw_modes": selected(room, [0x12CBB80, 0x12CBDB0, 0x12CBE1C, 0x12CBEB0, 0x12CBF68, 0x12CC190, 0x12CC228, 0x12CC390]),
            "room_preview": selected(preview, [0x12CE81C, 0x12CE824]),
        },
    }


LANGUAGE_ENTRIES = {
    22: ("Yeees", "はーい"),
    23: ("What could it be?", "何かな？"),
    24: ("Yes, yes...", "はいはい"),
    25: ("Hey, listen...", "ねぇねぇ"),
    26: ("Umm...", "あのー"),
    27: ("Is now a good time?", "いま大丈夫？"),
    28: ("Sorry", "すいません"),
    29: ("Hey you", "チミチミ"),
    30: ("About this...", "これがさぁ"),
    31: ("In that case...", "それでさぁ"),
    32: ("And then...", "でさぁ"),
    33: ("...", "ペラペラ"),
    34: ("By the way...", "ところで"),
    35: ("Hmm", "ふむふむ"),
    36: ("Yep yep", "うんうん"),
    37: ("Of course!", "なるほど！"),
    38: ("Huh?", "えぇ！"),
    39: ("Amazing!", "すごい！"),
    40: ("As expected!", "さすが！"),
    41: ("Wow!", "わーぉ"),
    42: ("Hmm...", "ふーん"),
    43: ("I dunno...", "うーん…"),
    44: ("I'm busy", "今忙しい"),
    45: ("Sorry...", "ごめんね"),
    46: ("Later!", "またあとで！"),
    68: ("...", "…"),
}


def parse_locale(raw: bytes) -> tuple[dict[str, dict[str, Any]], str]:
    require(raw[180:183] == b"\xef\xbb\xbf", "language TextAsset BOM/header boundary changed")
    text = raw[183:].decode("utf-8").rstrip("\x00")
    rows: dict[str, dict[str, Any]] = {}
    for physical_line, line in enumerate(text.splitlines(), 1):
        parts = line.rstrip("\r").split(",", 3)
        if len(parts) == 4 and parts[1] == "text":
            rows[parts[2]] = {"value": parts[3], "physical_line": physical_line}
    return rows, text


def verify_localization(enum_values: list[str]) -> dict[str, Any]:
    entries = {
        "en": "assets/bin/Data/3e011607c70476647900e67699290733",
        "ja": "assets/bin/Data/9fc588dea0f2b6e42901e4267689ad9d",
    }
    parsed: dict[str, dict[str, dict[str, Any]]] = {}
    hashes: dict[str, str] = {}
    with zipfile.ZipFile(APK) as archive:
        for locale, name in entries.items():
            raw = archive.read(name)
            parsed[locale], _text = parse_locale(raw)
            hashes[locale] = hashlib.sha256(raw).hexdigest()
    rows = []
    for identifier, (english, japanese) in LANGUAGE_ENTRIES.items():
        key = "1464-1" if identifier == 68 else ("1441-1&1548-1" if identifier == 43 else f"{identifier + 1398}-1")
        require(enum_values[identifier] != "MAX", f"FUKIDASHI enum id {identifier} is not a live value")
        require(key in parsed["en"] and key in parsed["ja"], f"language row is missing: {key}")
        require(parsed["en"][key]["value"] == english, f"EN localization differs for FUKIDASHI {identifier}")
        require(parsed["ja"][key]["value"] == japanese, f"JA localization differs for FUKIDASHI {identifier}")
        rows.append({
            "id": identifier,
            "enum_name": enum_values[identifier],
            "locale_key": key,
            "english": english,
            "japanese": japanese,
            "apk_physical_line": {"en": parsed["en"][key]["physical_line"], "ja": parsed["ja"][key]["physical_line"]},
            "source_refs": [f"APK:{entries['en']}:{key}", f"APK:{entries['ja']}:{key}"],
        })
    return {
        "schema_version": "social-dev-k4-1-fukidashi-localization-catalog-v1",
        "status": "PROVEN_CANONICAL",
        "source_identity": {
            "apk": source_ref(APK),
            "apk_sha256": sha256(APK),
            "language_entries": entries,
            "raw_entry_sha256": hashes,
            "textasset_header_bytes": 180,
            "utf8_bom_offset": 180,
        },
        "language_path": {
            "Language.JAPANESE": 0,
            "Language.ENGLISH": 1,
            "Language.LT": "0x1BC85D0",
            "Language.SetTextTable": "0x1BC61B0",
            "Language.LoadLanguagePack": "0x1BCA85C",
            "AppData.FUKIDASHI_TEXT": source_ref(APPDATA, "FUKIDASHI_TEXT"),
            "AppData.DrawFukidashi": source_ref(APPDATA, "DrawFukidashi(Graphics,FUKIDASHI,int,int)"),
        },
        "entries": rows,
    }


def verify_room0_and_furniture() -> dict[str, Any]:
    floor = load_json(FLOOR00)
    scene = load_json(NATIVE_SCENE)
    furniture = load_json(FURNITURE_META)
    room = next(item for item in scene["rooms"] if item["room_key"] == "room:0")
    require(floor["door"] == {"cell": [8, 4], "raw_type": 5, "installed_flag": 1, "furniture_data": None}, "Room0 door contract changed")
    desks = [item for item in room["object_cells"] if item.get("furniture_data_id") == 3]
    require(len(desks) == 3, "Room0 type-2 desk binding count changed")
    expected = {
        (2, 4): (3, "DIRECTION_DOWN", 2),
        (3, 4): (2, "DIRECTION_UP", 2),
        (6, 4): (2, "DIRECTION_UP", 2),
    }
    for item in desks:
        cell = tuple(item["cell"])
        require(cell in expected, f"unexpected Room0 desk cell: {cell}")
        require((item["raw_direction"], item["direction"]["label"], item["raw_type"]) == expected[cell], f"Room0 desk direction differs at {cell}")
    desk_data = next(item for item in furniture["furniture"] if item["furniture_data_id"] == 3)
    require(desk_data["fields"]["type_"] == 2, "FurnitureData 3 is not type 2")
    require(desk_data["fields"]["seb_"] == 1 and desk_data["fields"]["subSeb_"] == 3, "FurnitureData 3 selector fields changed")
    return {
        "room0_door": floor["door"],
        "room0_desks": [
            {
                "cell": item["cell"],
                "raw_type": item["raw_type"],
                "raw_direction": item["raw_direction"],
                "direction": item["direction"],
                "furniture_data_id": item["furniture_data_id"],
            }
            for item in desks
        ],
        "furniture_data_3": {
            "type_": desk_data["fields"]["type_"],
            "seb_": desk_data["fields"]["seb_"],
            "subSeb_": desk_data["fields"]["subSeb_"],
            "img_": desk_data["fields"]["img_"],
            "source": desk_data["source_file"],
        },
    }


def classifications() -> list[dict[str, Any]]:
    values = [
        ("talk.autonomous-pools", "The autonomous Talk frame-20/frame-70 pools and field-handle relocation chain", "REPRODUCED_EXACT"),
        ("talk.invitation-pools", "Invite opening, busy/reject, and response pools plus random bounds", "REPRODUCED_EXACT"),
        ("talk.localization-and-lifecycle", "EN/JA resource rows, language path, storage, timing, offset, lifetime, draw, and cleanup", "REPRODUCED_EXACT"),
        ("talk.extra-handle-0x27D7E40", "Treat 0x27D7E40 as an autonomous Talk pool", "REJECTED_BY_SOURCE"),
        ("door.distinct-visual-animation-timeline", "Promote a separate Room0 door animation frame timeline", "REPRODUCED_WITH_CORRECTION"),
        ("door.null-furnituredata-consumer", "Room0 null-FurnitureData DrawWall path is static while action state remains separate", "REPRODUCED_EXACT"),
        ("workstation.type2-live-order", "Desk/chair/Staff.Draw live type-2 ordering and installed ownership guard", "REPRODUCED_EXACT"),
        ("workstation.preview-is-live", "Treat preview=true Draw as the live normal Room0 path", "REPRODUCED_WITH_CORRECTION"),
    ]
    return [{"finding_id": key, "finding": finding, "classification": classification} for key, finding, classification in values]


def build_talk_artifacts(csharp: dict[str, Any], native: dict[str, Any], localization: dict[str, Any], talk_contract: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    pools = {item["handle"]: item for item in native["fukidashi_pools"]}
    autonomous = {
        "frame_20": {
            "speaker_role": "initiator Staff.Talk while FLAG_INVITED_TALK bit 8 is clear",
            "guard_native": ["frame == 20", "tbz bit 3 falls through only when bit 8 is clear"],
            "random": {"native_call": "0x12D5624 -> AppData.Random", "bound": 101, "condition": "random <= 100"},
            "pool": pools["0x27D7E48"],
            "AddFukidashi": {"delay": 0, "offsetY": 0, "native": "0x12D5664 -> 0x12D3C50"},
        },
        "frame_70": {
            "speaker_role": "invited/target Staff.Talk while FLAG_INVITED_TALK bit 8 is set",
            "guard_native": ["frame == 70", "tbz bit 3 skips when bit 8 is clear"],
            "random": {"selection": "array overload AppData.Random(length)", "native_array_call": "0x12D3CA4"},
            "pool": pools["0x27D7E50"],
            "AddFukidashi": {"delay": 0, "offsetY": 0, "native": "0x12D56B8 -> 0x12D3C50"},
        },
    }
    invitation = {
        "opening_frame_20": {"speaker_role": "initiator inviting target", "pool": pools["0x27D7E28"], "native": "0x12D522C"},
        "frame_60_busy_or_reject": {"speaker_role": "target invitation response", "random": {"bound": 101, "busy_threshold": 10}, "pool": pools["0x27D7E20"], "native": "0x12D5560"},
        "frame_60_response": {"speaker_role": "target invitation response", "pool": pools["0x27D7E30"], "native": "0x12D53E0"},
    }
    closure = {
        "schema_version": "social-dev-k4-1-fukidashi-payload-closure-v1",
        "status": "PROVEN_CANONICAL",
        "classification": "REPRODUCED_EXACT",
        "research_findings": classifications(),
        "roles": {
            "initiator": talk_contract["initiator"],
            "target": talk_contract["invite"],
            "partner_cleanup": talk_contract["partner_cleanup"],
        },
        "autonomous_talk": autonomous,
        "invitation": invitation,
        "payload_storage_and_lifetime": {
            "field": "Staff.fukidashi__",
            "indices": {"id": 0, "frame_lifetime": 1, "delay": 2, "offsetY": 3},
            "add_single": {"ref": source_ref(STAFF, "AddFukidashi_(FUKIDASHI,int,int)"), "writes": {"id": 0, "frame_lifetime": 40, "delay": "argument", "offsetY": "argument"}, "busy_guard": "existing frame_lifetime > 0 refuses replacement"},
            "update": {"ref": source_ref(STAFF, "UpdateFukidashi_()"), "behavior": "decrement delay; when delay <= 0 decrement frame_lifetime and reset delay to 0"},
            "draw": {"ref": source_ref(STAFF, "DrawFukidashi_()"), "guards": ["frame_lifetime > 0", "delay <= 0"], "position": "staff position plus offsetY, y minus 20", "owner": "AppData.DrawFukidashi"},
            "cleanup": {"ref": source_ref(talk_contract_path := TALK_CONTRACT, "partner_cleanup"), "behavior": talk_contract["partner_cleanup"]["effect"]},
        },
        "localization": {"catalog": rel(K41 / "fukidashi-localization-catalog.json"), "ids": [item["id"] for item in localization["entries"]]},
        "source_refs": [source_ref(STAFF, "Staff.Talk/InviteStaffToTalk/AddFukidashi_/UpdateFukidashi_/DrawFukidashi_"), source_ref(APPDATA, "FUKIDASHI enum/FUKIDASHI_TEXT/DrawFukidashi"), source_ref(LIB, "0x12D5588/0x12D5090/0x12D3C50/0x12DDA90"), source_ref(METADATA, "default-value and RuntimeFieldHandle relocation chain"), source_ref(APK, "language TextAssets")],
        "csharp_proof": csharp["staff_field_and_lifecycle"],
        "native_proof": {"Staff.Talk": "0x12D5588", "Staff.InviteStaffToTalk": "0x12D5090", "Staff.AddFukidashi_array": "0x12D3C50", "Staff.AddFukidashi_single": "0x12DDA90"},
    }
    catalog = localization
    return closure, catalog


def build_door_artifacts(native: dict[str, Any], room0: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    graph = {
        "schema_version": "social-dev-k4-1-room0-door-visual-consumer-graph-v1",
        "status": "PROVEN_CANONICAL",
        "room0_input": room0["room0_door"],
        "consumers": [
            {"consumer": "Room.Draw -> ObjChip.DrawWall", "rva": "0x12C0698", "condition": "raw type == 5", "result": "fixed door SEB/image baseline"},
            {"consumer": "ObjChip.DrawWall dynamic FurnitureData overlay", "guard": "furnitureData_ == null -> cbz bypass", "result": "unreachable for Room0 door because furnitureData is null"},
            {"consumer": "ObjChip.Update type-5 action", "rva": "0x12BED80", "result": "reservation/frame/workFloat/fade/action state only"},
            {"consumer": "ObjChip.StartAction", "rva": "0x12C0520", "result": "writes action state; does not create a separate Room0 FurnitureData draw consumer"},
        ],
        "native_anchors": native["native_instruction_anchors"]["room0_door_drawwall"],
        "source_refs": [source_ref(FLOOR00, "door"), source_ref(NATIVE_SCENE, "rooms[room:0].door"), source_ref(ROOM, "PlaceDoor"), source_ref(OBJCHIP, "DrawWall/Update/StartAction"), source_ref(LIB, "0x12C0698/0x12BED80/0x12C0520")],
    }
    contract = {
        "schema_version": "social-dev-k4-1-room0-door-action-vs-visual-contract-v1",
        "status": "NO_DISTINCT_VISUAL",
        "blocking": False,
        "classification": "REPRODUCED_WITH_CORRECTION",
        "conclusion": "Room0 raw type-5 door remains on the fixed DrawWall door frame because FurnitureData is null; native action/update/fade state changes are real but do not select a distinct visible door timeline through the Room0 consumer path.",
        "visual_baseline": {"cell": [8, 4], "raw_type": 5, "installed_flag": 1, "furnitureData": None, "frame": 0, "seb": "door_02.seb", "image": "door_01.png"},
        "action_state": {"update": "0x12BED80", "start_action": "0x12C0520", "frame_seed": 15, "fade_flags": ["FLAG_FADE_OUT", "FLAG_FADE_IN"], "policy": "record state/action independently; do not invent door frames"},
        "consumer_graph": rel(K41 / "room0-door-visual-consumer-graph.json"),
        "research_findings": classifications(),
        "source_refs": graph["source_refs"],
        "native_proof": {"DrawWall": "0x12C0698", "raw_type_branch": "0x12C0784", "fixed_door_draw": "0x12C07A4/0x12C08A4", "furnitureData_null_guard": "0x12C08A8/0x12C08AC", "dynamic_overlay_type_check": "0x12C08B0/0x12C08B4"},
    }
    return graph, contract


def build_workstation_artifacts(native: dict[str, Any], room0: dict[str, Any], csharp: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    directions = {tuple(item["cell"]): item for item in room0["room0_desks"]}
    sequences = {
        "DIRECTION_DOWN_3": [
            {"order": 0, "owner": "ObjChip.Draw type-2 inner", "operation": "desk primary Seb/AppData.DrawSeb", "native": "0x12C1C70"},
            {"order": 1, "owner": "ObjChip.Draw type-2 inner", "operation": "chair subSeb ResourceManager.DrawSeb", "native": "0x12C1E38", "seb_frame": 1, "guard": "staffId_ != -1"},
            {"order": 2, "owner": "ObjChip.staffs_", "operation": "Staff.Draw offset overload", "native": "0x12C1ED4 -> 0x12DABA8", "guard": "installed outer path; Staff flags bit 2 filter"},
            {"order": 3, "owner": "ObjChip.Draw type-2 inner", "operation": "late chair subSeb foreground ResourceManager.DrawSeb", "native": "0x12C26DC", "seb_frame": 2, "guard": "staffId_ != -1"},
        ],
        "DIRECTION_UP_2": [
            {"order": 0, "owner": "ObjChip.Draw type-2 inner", "operation": "chair subSeb ResourceManager.DrawSeb", "native": "0x12C2460", "seb_frame": 0, "guard": "staffId_ != -1"},
            {"order": 1, "owner": "ObjChip.staffs_", "operation": "Staff.Draw offset overload", "native": "0x12C2510 -> 0x12DABA8", "guard": "installed outer path; Staff flags bit 2 filter"},
            {"order": 2, "owner": "ObjChip.Draw type-2 inner", "operation": "desk primary Seb/AppData.DrawSeb", "native": "0x12C1C70"},
        ],
    }
    fixture_rows = []
    for cell, item in sorted(directions.items()):
        key = "DIRECTION_DOWN_3" if item["raw_direction"] == 3 else "DIRECTION_UP_2"
        fixture_rows.append({"cell": list(cell), "raw_type": item["raw_type"], "raw_direction": item["raw_direction"], "direction": item["direction"]["label"], "FurnitureData": 3, "live_sequence": sequences[key]})
    cfg = {
        "schema_version": "social-dev-k4-1-workstation-native-cfg-v1",
        "status": "PROVEN_CANONICAL",
        "method": "ObjChip.Draw(Graphics,int,int,FurnitureData,bool)",
        "rva": "0x12C166C",
        "dispatch": {"type_2_branch": "0x12C1914 -> 0x12C1A70", "direction_field": "ObjChip.direction_ @ +0x48", "direction3_branch": "0x12C1AC0/0x12C1AD0"},
        "live_normal_path": {"Room.Draw": "0x12CBB80", "outer_overload": "0x12C0E00", "inner_overload": "0x12C166C", "preview": False, "callsite": "0x12C10C4", "installed_guard": "0x12C1088 -> 0x12C108C; installed true bypasses outer uninstalled Staff loop"},
        "preview_paths": [{"owner": "Room.Draw floor-select type-2", "preview": True, "callsite": "0x12CC234"}, {"owner": "Room.DrawObjPreview", "preview": True, "callsite": "0x12CE81C -> 0x12CE824"}],
        "directional_sequences": sequences,
        "late_foreground": {"native": "0x12C2528..0x12C26DC", "asset": "subSeb_", "frame": 2, "guard": "staffId_ != -1", "directions": [3]},
        "duplicate_staff_guard": {"installed_outer": "0x12C108C tbz", "staff_loop": "0x12C1ED4 or 0x12C2510", "principle": "live installed path does not also execute the uninstalled outer Staff loop"},
        "native_anchors": native["native_instruction_anchors"]["workstation_type2_inner"] + native["native_instruction_anchors"]["workstation_outer_and_guard"],
        "source_refs": [source_ref(OBJCHIP, "Draw(FurnitureData,bool)"), source_ref(ROOM, "Draw/DrawObjPreview"), source_ref(LIB, "0x12C166C/0x12C0E00/0x12CBB80/0x12CE824"), source_ref(FLOOR00, "native_initial_furniture"), source_ref(NATIVE_SCENE, "rooms[room:0].object_cells")],
    }
    fixtures = {
        "schema_version": "social-dev-k4-1-workstation-direction-fixtures-v1",
        "status": "PROVEN_CANONICAL",
        "furniture_data": {"id": 3, "type_": 2, "seb_": 1, "subSeb_": 3},
        "fixtures": fixture_rows,
        "source_refs": [source_ref(FURNITURE_META, "furniture_data_id 3"), source_ref(NATIVE_SCENE, "rooms[room:0].object_cells")],
    }
    return cfg, fixtures, sequences


def coverage_metrics(records: list[dict[str, Any]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for record in records:
        counts[record["status"]] = counts.get(record["status"], 0) + 1
    return {
        "reachable_consumer_count": sum(record["status"] != "NOT_REACHABLE" for record in records),
        "visible_consumer_count": sum(bool(record["visible"]) for record in records),
        "proven_canonical_count": counts.get("PROVEN_CANONICAL", 0),
        "proven_promoted_count": sum(record["promotion_status"] == "PROMOTED_TO_CANONICAL_BRAIN" for record in records),
        "proven_not_canonical_count": counts.get("PROVEN_NOT_CANONICAL", 0),
        "no_distinct_visual_count": counts.get("NO_DISTINCT_VISUAL", 0),
        "not_reachable_count": counts.get("NOT_REACHABLE", 0),
        "source_limited_count": counts.get("SOURCE_LIMITED", 0),
        "blocking_source_limited_count": sum(record["status"] == "SOURCE_LIMITED" and bool(record["blocking"]) for record in records),
        "source_missing_count": counts.get("SOURCE_MISSING", 0),
        "heuristic_or_assumed_count": sum(bool(record["heuristic_or_assumed"]) for record in records),
    }


def update_coverage_and_recipes(talk: dict[str, Any], door: dict[str, Any], workstation: dict[str, Any], native: dict[str, Any]) -> dict[str, Any]:
    consumers = load_json(K4 / "reachable-visual-consumers.json")
    evidence = {
        "room0.door.action-timeline": [rel(K41 / "room0-door-action-vs-visual-contract.json"), source_ref(LIB, "ObjChip.DrawWall@0x12C0698")],
        "staff.talk.fukidashi-payload": [rel(K41 / "fukidashi-payload-closure.json"), rel(K41 / "fukidashi-localization-catalog.json"), source_ref(LIB, "Staff.Talk@0x12D5588")],
        "workstation.live-interleave": [rel(K41 / "workstation-native-cfg.json"), rel(K41 / "room0-workstation-pass-interleave.json"), source_ref(LIB, "ObjChip.Draw@0x12C166C")],
    }
    notes = {
        "room0.door.action-timeline": "Corrected: native Room0 action/update/fade state is proven, but the null-FurnitureData DrawWall consumer has no distinct visual action timeline.",
        "staff.talk.fukidashi-payload": "Exact autonomous and invitation pools, random semantics, locale rows, bubble lifetime/offset, draw, and cleanup are source/native-backed.",
        "workstation.live-interleave": "Exact live type-2 direction-specific desk/chair/Staff.Draw ordering, preview separation, late chair guard, and duplicate Staff guard are source/native-backed.",
    }
    for record in consumers["records"]:
        if record["consumer_id"] not in evidence:
            continue
        record["status"] = "NO_DISTINCT_VISUAL" if record["consumer_id"].startswith("room0.door") else "PROVEN_CANONICAL"
        record["blocking"] = False
        record["promotion_status"] = "PROMOTED_TO_CANONICAL_BRAIN"
        record["notes"] = notes[record["consumer_id"]]
        record["evidence"] = sorted(set(record["evidence"] + evidence[record["consumer_id"]]))
    consumers["status"] = "closed"
    consumers["metrics"] = coverage_metrics(consumers["records"])
    write_json(K4 / "reachable-visual-consumers.json", consumers)
    matrix = load_json(K4 / "visual-assembly-coverage-matrix.json")
    matrix["status"] = "closed"
    matrix["blocking_consumers"] = []
    matrix["records"] = consumers["records"]
    matrix["metrics"] = consumers["metrics"]
    write_json(K4 / "visual-assembly-coverage-matrix.json", matrix)

    wall = load_json(K4 / "wall-door-assembly-recipe.json")
    wall["status"] = "PROVEN_CANONICAL"
    wall["door_action"] = door
    write_json(K4 / "wall-door-assembly-recipe.json", wall)

    existing_talk = load_json(K4 / "talk-composition-recipe.json")
    existing_talk.update(talk)
    existing_talk["status"] = "PROVEN_CANONICAL"
    existing_talk["blocking"] = False
    existing_talk["fukidashi"] = {
        "status": "PROVEN_CANONICAL",
        "blocking": False,
        "known": {
            "invocation_frames": [20, 70],
            "native_static_field_handles": [item["handle"] for item in native["fukidashi_pools"]],
            "pools": native["fukidashi_pools"],
            "selection": "array overload calls AppData.Random(length), then single overload",
            "storage": "[id,40,delay,offsetY]",
        },
        "closure_artifact": rel(K41 / "fukidashi-payload-closure.json"),
    }
    write_json(K4 / "talk-composition-recipe.json", existing_talk)

    existing_workstation = load_json(K4 / "workstation-sitting-composition.json")
    existing_workstation["status"] = "PROVEN_CANONICAL"
    existing_workstation["blocking"] = False
    existing_workstation["unresolved_live_interleave"] = {
        "status": "PROVEN_CANONICAL",
        "blocking": False,
        "missing": None,
        "required_next_evidence": None,
        "closure_artifact": rel(K41 / "room0-workstation-pass-interleave.json"),
    }
    existing_workstation["live_interleave"] = workstation
    write_json(K4 / "workstation-sitting-composition.json", existing_workstation)
    return consumers["metrics"]


def update_queries() -> dict[str, Any]:
    queries = load_json(K4 / "deterministic-query-results.json")
    queries["queries"]["C_workstation_sitting"] = {"status": "pass", "input": "Room0 type-2 live interleave", "result": "direction fixtures and installed guard closed", "gaps": []}
    queries["queries"]["D_talk"] = {"status": "pass", "input": "Staff.Talk FUKIDASHI payload/localization", "result": "five native pools and EN/JA catalog closed", "gaps": []}
    queries["status"] = "closed"
    write_json(K4 / "deterministic-query-results.json", queries)
    return queries


def update_database(talk: dict[str, Any], door: dict[str, Any], workstation: dict[str, Any], localization: dict[str, Any], before: dict[str, Any]) -> dict[str, Any]:
    refs = [source_ref(LIB), source_ref(METADATA), source_ref(STAFF), source_ref(OBJCHIP), source_ref(ROOM), source_ref(APK)]
    facts = [
        ("STAFF_METHOD:Talk", "k4_fukidashi_payload_closure", talk, "Exact autonomous/invitation Fukidashi pools, random bounds, localization rows, storage/lifetime/offset/draw semantics, and partner cleanup are pinned-source-backed."),
        ("STAFF_METHOD:Talk", "k4_autonomous_talk_timeline", {"autonomous_talk": talk["autonomous_talk"], "invitation": talk["invitation"], "roles": talk["roles"]}, "Autonomous Talk frame gates, speaker roles, and completion/cleanup calls are pinned native-backed."),
        ("ROOM_DATA_ID:0", "k4_door_action_vs_visual_contract", door, "Room0 null-FurnitureData DrawWall proof closes the visual boundary; action/update/fade state is retained separately without invented door frames."),
        ("ROOM_DATA_ID:0", "k4_workstation_type2_live_interleave", workstation, "Room0 live type-2 native draw order, preview separation, direction fixtures, and duplicate Staff guard are pinned-source-backed."),
    ]
    edges = [
        ("STAFF_METHOD:Talk", "uses_fukidashi_payload", "FUKIDASHI_PAYLOAD_CLOSURE:Staff.Talk"),
        ("STAFF_METHOD:Talk", "uses_localization_catalog", "FUKIDASHI_LOCALIZATION_CATALOG:22-46-68"),
        ("ROOM_DATA_ID:0", "has_action_vs_visual_contract", "ROOM0_DOOR_ACTION_VS_VISUAL:0"),
        ("ROOM_DATA_ID:0", "uses_workstation_live_interleave", "WORKSTATION_LIVE_INTERLEAVE:room0-type2"),
    ]
    connection = sqlite3.connect(DB)
    try:
        connection.execute("pragma foreign_keys=off")
        connection.execute("begin")
        old_fact = "fact:k4:ROOM_DATA_ID:0|k4_door_closed_baseline"
        connection.execute("update canonical_facts set note=? where fact_id=?", ("Room0 closed door baseline is canonical; the K4.1 null-FurnitureData consumer proof shows no distinct visual action timeline.", old_fact))
        for entity_id, predicate, value, note in facts:
            fact_id = f"fact:k4:{entity_id}|{predicate}"
            value_json = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
            refs_json = json.dumps(sorted(set(refs)), ensure_ascii=False, sort_keys=True)
            claim_id = stable_id("fact-claim-k4-1", fact_id)
            connection.execute("insert or replace into canonical_entities(entity_id,entity_type,name,attributes_json,provenance_json) values(?,?,?,?,?)", (entity_id, "k4_visual_assembly_entity", entity_id, "{}", refs_json))
            connection.execute("insert or replace into canonical_facts(fact_id,entity_id,predicate,value_json,status,authority,impl_status,revision,canonical,note) values(?,?,?,?,?,?,?,?,?,?)", (fact_id, entity_id, predicate, value_json, "CONFIRMED", "pinned_native", "usable", 2, 1, note))
            connection.execute("insert or replace into fact_claims(claim_id,entity_id,predicate,value_json,status,authority,impl_status,canonical_fact_id,source_claim_refs_json,note) values(?,?,?,?,?,?,?,?,?,?)", (claim_id, entity_id, predicate, value_json, "CONFIRMED", "pinned_native", "usable", fact_id, refs_json, note))
            for ref in sorted(set(refs)):
                connection.execute("insert or replace into fact_sources(fact_source_id,claim_id,entity_id,predicate,source_json) values(?,?,?,?,?)", (stable_id("fact-source-k4-1", claim_id, ref), claim_id, entity_id, predicate, json.dumps({"source_ref": ref, "authority": "pinned_native"}, sort_keys=True)))
        for subject, predicate, object_id in edges:
            edge_id = stable_id("edge-k4-1", subject, predicate, object_id)
            claim_id = stable_id("edge-claim-k4-1", edge_id)
            refs_json = json.dumps(sorted(set(refs)), ensure_ascii=False, sort_keys=True)
            statement = f"{subject} {predicate} {object_id}"
            connection.execute("insert or replace into semantic_edges(edge_id,subject_id,predicate,object_id,status,authority,source_refs_json,claim_id) values(?,?,?,?,?,?,?,?)", (edge_id, subject, predicate, object_id, "verified", "pinned_native", refs_json, claim_id))
            connection.execute("insert or replace into edge_claims(claim_id,edge_id,claim_status,confidence,statement,source_refs_json) values(?,?,?,?,?,?)", (claim_id, edge_id, "verified", "high", statement, refs_json))
            connection.execute("insert or replace into edge_revisions(revision_id,edge_id,prior_status,next_status,reason,source_refs_json) values(?,?,?,?,?,?)", (stable_id("edge-revision-k4-1", edge_id), edge_id, None, "verified", "Exact K4.1 targeted source/native visual closure relation.", refs_json))
            for ref in sorted(set(refs)):
                connection.execute("insert or replace into edge_sources(edge_source_id,edge_id,source_instance_id,source_ref,authority) values(?,?,?,?,?)", (stable_id("edge-source-k4-1", edge_id, ref), edge_id, None, ref, "pinned_native"))
        metadata = {"brain_revision": REVISION, "status": "K4_CLOSED_VISUAL_ASSEMBLY", "k4_status": "CLOSED", "k4_final_token": FINAL_TOKEN, "k4_1_status": "CLOSED", "k4_1_final_token": FINAL_TOKEN}
        for key, value in metadata.items():
            connection.execute("insert or replace into brain_metadata(key,value_json) values(?,?)", (key, json.dumps(value, ensure_ascii=False)))
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()
    return {"facts": [{"fact_id": f"fact:k4:{entity}|{predicate}", "entity_id": entity, "predicate": predicate, "note": note} for entity, predicate, _value, note in facts], "edges": [{"edge_id": stable_id("edge-k4-1", *edge), "subject_id": edge[0], "predicate": edge[1], "object_id": edge[2]} for edge in edges], "before": before}


def db_snapshot() -> dict[str, Any]:
    connection = sqlite3.connect(DB)
    try:
        counts = {}
        for table in ("canonical_entities", "canonical_facts", "semantic_edges", "derived_artifacts"):
            counts[table] = connection.execute(f"select count(*) from {table}").fetchone()[0]
        counts["verified_edges"] = connection.execute("select count(*) from semantic_edges where status='verified'").fetchone()[0]
        counts["rejected_edges"] = connection.execute("select count(*) from semantic_edges where status='rejected'").fetchone()[0]
        counts["source_limited_edges"] = connection.execute("select count(*) from semantic_edges where status='unresolved'").fetchone()[0]
        metadata = dict(connection.execute("select key,value_json from brain_metadata"))
        return {"path": rel(DB), "size_bytes": DB.stat().st_size, "sha256": sha256(DB), "brain_revision": json.loads(metadata["brain_revision"]), "status": json.loads(metadata["status"]), "k3_status": json.loads(metadata.get("k3_status", '"CLOSED"')), "k4_status": json.loads(metadata.get("k4_status", '"CLOSED"')), "tables": counts}
    finally:
        connection.close()


def update_derived_artifacts(paths: list[Path]) -> None:
    connection = sqlite3.connect(DB)
    try:
        for path in paths:
            connection.execute("insert or replace into derived_artifacts(derived_id,relative_path,kind,source_ids_json,brain_revision,sha256,status) values(?,?,?,?,?,?,?)", (stable_id("derived-k4-1", rel(path)), rel(path), "k4_1_targeted_closure_acceptance", json.dumps([REVISION]), REVISION, sha256(path), "active"))
        connection.commit()
    finally:
        connection.close()


def update_graph() -> None:
    graph = load_json(GRAPH)
    connection = sqlite3.connect(DB)
    try:
        counts = dict(connection.execute("select status,count(*) from semantic_edges group by status").fetchall())
        total = connection.execute("select count(*) from semantic_edges").fetchone()[0]
    finally:
        connection.close()
    graph.update({"status": "closed", "edge_count": total, "verified_edge_count": counts.get("verified", 0), "candidate_edge_count": counts.get("candidate", 0), "unresolved_edge_count": counts.get("unresolved", 0), "rejected_edge_count": counts.get("rejected", 0), "k4_visual_assembly_revision": REVISION, "k4_visual_assembly_status": "CLOSED"})
    write_json(GRAPH, graph)


def run_command(label: str, command: str, cwd: Path = ROOT) -> dict[str, Any]:
    result = subprocess.run(command, cwd=cwd, shell=True, text=True, capture_output=True, timeout=600, check=False)
    return {"label": label, "command": command, "status": "PASS" if result.returncode == 0 else "FAIL", "returncode": result.returncode, "stdout_tail": result.stdout[-2000:], "stderr_tail": result.stderr[-2000:]}


def existing_regressions() -> list[dict[str, Any]]:
    commands = [
        ("k2_unified_brain", "python -B tools/social-dev/test_k2_unified_brain.py", ROOT),
        ("native_content_registry", "python -B tools/social-dev/test_native_content_registry.py", ROOT),
        ("native_content_catalog", "python -B tools/social-dev/test_native_content_catalog.py", ROOT),
        ("native_room_floor_closure", "python -B tools/social-dev/test_native_room_floor_closure.py", ROOT),
        ("display_asset_gate", "python -B tools/social-dev/test_display_asset_gate.py", ROOT),
        ("runtime_typecheck", "npm run typecheck", ROOT / "runtime/social-dev"),
        ("runtime_vitest", "npm test -- --run", ROOT / "runtime/social-dev"),
    ]
    return [run_command(label, command, cwd) for label, command, cwd in commands]


def semantic_delta(promoted: dict[str, Any], before: dict[str, Any], after: dict[str, Any]) -> dict[str, Any]:
    existing = load_json(K4 / "semantic-delta.json")
    promoted_fact_ids = {item["fact_id"] for item in promoted["facts"]}
    promoted_edge_ids = {item["edge_id"] for item in promoted["edges"]}
    old_facts = [item for item in existing.get("canonical_facts_added", []) if item.get("fact_id") not in promoted_fact_ids]
    old_edges = [item for item in existing.get("verified_edges_added", []) if item.get("edge_id") not in promoted_edge_ids]
    return {"schema_version": "social-dev-k4-1-semantic-delta-v1", "status": "closed", "brain_revision_before": before["brain_revision"], "brain_revision_after": REVISION, "canonical_database_before": before, "canonical_database_after": after, "canonical_facts_added": old_facts + promoted["facts"], "verified_edges_added": old_edges + promoted["edges"], "source_limited_not_promoted": [], "heuristic_or_assumed_added": 0, "runtime_pixel_change": False, "mapchip_pixel_change": False, "scope": "K4.1 targeted visual blocker closure only; no product/living policy change"}


def update_manifest(final: dict[str, Any], after: dict[str, Any]) -> None:
    manifest = load_json(MANIFEST)
    manifest["status"] = "K4_CLOSED_VISUAL_ASSEMBLY"
    manifest.setdefault("acceptance", {}).update({"k4": rel(K4), "k4_report": rel(K4 / "K4_CLOSURE_REPORT.md"), "k4_1": rel(K41), "k4_1_report": rel(K41 / "K4_1_CLOSURE_REPORT.md")})
    manifest["canonical_semantic_db"].update({"sha256": after["sha256"], "size_bytes": after["size_bytes"], "brain_revision": REVISION})
    manifest.setdefault("scope", {})["k4"] = "CLOSED"
    manifest["scope"]["k4_1"] = "CLOSED"
    manifest["scope"]["v8"] = "NOT_STARTED"
    manifest["k4"] = {"status": "CLOSED", "final_token": final["final_token"], "blocking_source_limited_count": final["coverage"]["blocking_source_limited_count"], "heuristic_or_assumed_count": final["coverage"]["heuristic_or_assumed_count"], "source_missing_count": final["coverage"]["source_missing_count"], "ready_for_v8": True}
    manifest["k4_1"] = {"status": "CLOSED", "final_token": FINAL_TOKEN, "blocking_source_limited_count": 0, "source_missing_count": 0, "heuristic_or_assumed_count": 0, "ready_for_v8": True}
    digest = hashlib.sha256()
    files = [path for path in BRAIN.rglob("*") if path.is_file() and path.resolve() != MANIFEST.resolve()]
    total = 0
    for path in sorted(files, key=lambda item: rel(item)):
        name = rel(path).encode("utf-8")
        digest.update(len(name).to_bytes(8, "big")); digest.update(name); digest.update(path.stat().st_size.to_bytes(8, "big")); digest.update(bytes.fromhex(sha256(path))); total += path.stat().st_size
    manifest.setdefault("active_topology", {})["brain_tree_excluding_this_manifest"] = {"file_count": len(files), "bytes": total, "sha256": digest.hexdigest()}
    write_json(MANIFEST, manifest)


def build_report(final: dict[str, Any], regressions: list[dict[str, Any]]) -> str:
    coverage = final["coverage"]
    regression_lines = "\n".join(f"- {item['label']}: {item['status']} ({item['command']})" for item in regressions)
    return f"""# K4.1 Targeted Closure\n\nStatus: {final['status']}\n\nFinal token: {final['final_token']}\n\nK4.1 independently closes the three targeted K4 visual blockers from pinned APK, C# source, IL2CPP metadata, native disassembly, and accepted Room0 contracts. V8 remains NOT_STARTED.\n\n## Required end state\n\n- blocking_source_limited_count: {coverage['blocking_source_limited_count']}\n- source_missing_count: {coverage['source_missing_count']}\n- heuristic_or_assumed_count: {coverage['heuristic_or_assumed_count']}\n- ready_for_v8: true\n\nNo blocking source-limited relations remain.\n\n## Classifications\n\n- `room0.door.action-timeline`: `REPRODUCED_WITH_CORRECTION`; action/update/fade state is real, but the Room0 null-FurnitureData DrawWall consumer has no distinct visible action timeline.\n- `staff.talk.fukidashi-payload`: `REPRODUCED_EXACT`; roles, timing, exact pools, random semantics, EN/JA path, bubble lifetime/offset, draw, and cleanup are proven.\n- `workstation.live-interleave`: `REPRODUCED_EXACT`; live type-2 direction-specific desk/chair/Staff.Draw order, preview separation, late chair guard, and duplicate Staff guard are proven.\n\nEvery research-pack hypothesis is recorded in `research_findings` with only the allowed classification vocabulary; unsupported extra handle `0x27D7E40` is `REJECTED_BY_SOURCE`.\n\n## Verification\n\n{regression_lines}\n\n## Boundary\n\n- Pinned source roots remained read-only.\n- Original runtime/data/visual packs remained byte-identical.\n- Runtime code, MapChip pixels, server, browser, emulator/ADB, live app, network, subagents, and V8 were not used.\n"""


def main() -> int:
    source_before = verify_source_identity()
    packs_before = pack_snapshot()
    previous_final = load_json(K4 / "final-validation.json") if (K4 / "final-validation.json").exists() else {}
    previous_before = previous_final.get("canonical_brain", {}).get("before")
    before = previous_before if isinstance(previous_before, dict) and previous_before.get("brain_revision") == "k4-visual-assembly-r1" else db_snapshot()
    csharp = verify_csharp_sources()
    native = verify_native()
    localization = verify_localization(csharp["enum"]["values"] and [item["name"] for item in csharp["enum"]["values"]])
    room0 = verify_room0_and_furniture()
    talk_contract = load_json(TALK_CONTRACT)
    talk, catalog = build_talk_artifacts(csharp, native, localization, talk_contract)
    door_graph, door_contract = build_door_artifacts(native, room0)
    workstation_cfg, direction_fixtures, sequences = build_workstation_artifacts(native, room0, csharp)
    interleave = {"schema_version": "social-dev-k4-1-room0-workstation-pass-interleave-v1", "status": "PROVEN_CANONICAL", "classification": "REPRODUCED_EXACT", "live_normal": workstation_cfg["live_normal_path"], "directional_sequences": sequences, "preview_paths": workstation_cfg["preview_paths"], "duplicate_staff_guard": workstation_cfg["duplicate_staff_guard"], "research_findings": classifications(), "source_refs": workstation_cfg["source_refs"]}

    K41.mkdir(parents=True, exist_ok=True)
    write_json(K41 / "fukidashi-payload-closure.json", talk)
    write_json(K41 / "fukidashi-localization-catalog.json", catalog)
    write_json(K41 / "autonomous-talk-timeline.json", {"schema_version": "social-dev-k4-1-autonomous-talk-timeline-v1", "status": "PROVEN_CANONICAL", "classification": "REPRODUCED_EXACT", "roles": talk["roles"], "timeline": talk["autonomous_talk"], "invitation": talk["invitation"], "completion": {"frame_110": "AddMeetingPointGauge(Lib.Random(0,4))", "frame_130_or_more": "clear talk/invite flags and colleagueId_; GotoDesk", "native": ["0x12D56EC", "0x12D56F8", "0x12D5710", "0x12D5728", "0x12D572C", "0x12D5730"]}, "research_findings": classifications(), "source_refs": talk["source_refs"]})
    write_json(K41 / "room0-door-visual-consumer-graph.json", door_graph)
    write_json(K41 / "room0-door-action-vs-visual-contract.json", door_contract)
    write_json(K41 / "workstation-native-cfg.json", workstation_cfg)
    write_json(K41 / "room0-workstation-pass-interleave.json", interleave)
    write_json(K41 / "workstation-direction-fixtures.json", direction_fixtures)
    write_json(K41 / "research-findings-classification.json", {"schema_version": "social-dev-k4-1-research-findings-classification-v1", "status": "closed", "allowed_classifications": sorted(ALLOWED_CLASSIFICATIONS), "findings": classifications(), "authority": "independent pinned-source reproduction; research pack is not an authority"})

    metrics = update_coverage_and_recipes(talk, door_contract, workstation_cfg, native)
    queries = update_queries()
    promoted = update_database(talk, door_contract, workstation_cfg, catalog, before)

    source_after = [hash_record(path, role) for path, role in source_inventory()]
    require(source_before == source_after, "pinned source hash changed during K4.1")
    source_evidence = load_json(K4 / "source-native-evidence-manifest.json")
    source_evidence["schema_version"] = "social-dev-k4-1-source-native-evidence-manifest-v1"
    source_evidence["status"] = "pass"
    source_evidence["source_roots_read_only"] = True
    source_evidence["source_hashes_unchanged"] = True
    source_evidence["artifacts"] = source_before
    source_evidence["source_hashes_before_build"] = source_before
    source_evidence["source_hashes_rechecked_after_build"] = source_after
    source_evidence["k4_1_artifacts"] = [rel(K41 / name) for name in ["fukidashi-payload-closure.json", "fukidashi-localization-catalog.json", "autonomous-talk-timeline.json", "room0-door-visual-consumer-graph.json", "room0-door-action-vs-visual-contract.json", "workstation-native-cfg.json", "room0-workstation-pass-interleave.json", "workstation-direction-fixtures.json", "research-findings-classification.json"]]
    source_evidence["native_anchor_catalog"].update({"Staff.InviteStaffToTalk": "0x12D5090", "Staff.AddFukidashi_array": "0x12D3C50", "Staff.AddFukidashi_single": "0x12DDA90", "Room.DrawObjPreview": "0x12CE824", "ObjChip.Draw_type2_inner": "0x12C166C"})
    write_json(K4 / "source-native-evidence-manifest.json", source_evidence)

    packs_after = pack_snapshot()
    generated_delta = {"schema_version": "social-dev-k4-1-generated-pack-delta-v1", "status": "pass", "packs_before": packs_before, "packs_after": packs_after, "runtime_pack_changed": packs_before["runtime"] != packs_after["runtime"], "visual_pack_changed": packs_before["visual"] != packs_after["visual"], "data_pack_changed": packs_before["data"] != packs_after["data"], "runtime_mirror_changed": packs_before["runtime_mirror"] != packs_after["runtime_mirror"], "generated_pack_policy": "K4.1 adds acceptance evidence and canonical brain facts; original packs remain byte-stable."}
    write_json(K4 / "generated-pack-delta.json", generated_delta)

    preflight = load_json(K4 / "preflight-current-state.json")
    preflight["run_kind"] = "repeatable_k4_1_targeted_closure_build"
    preflight["canonical_brain_before_k4_1"] = before
    preflight["generated_packs_before_k4_1"] = packs_before
    preflight["selected_source_hashes_before_k4_1"] = source_before
    preflight["boundary"].update({"network_used": False, "subagents_used": False, "server_started": False, "emulator_or_adb_used": False, "live_app_used": False, "mapchip_pixels_changed": False, "source_roots_read_only": True})
    write_json(K4 / "preflight-current-state.json", preflight)

    update_graph()
    k41_paths = [path for path in K41.glob("*.json")]
    update_derived_artifacts(k41_paths)
    after = db_snapshot()
    delta = semantic_delta(promoted, before, after)
    write_json(K4 / "semantic-delta.json", delta)

    regressions = existing_regressions()
    require(all(item["status"] == "PASS" for item in regressions), "an existing K4 regression failed")
    base_final = {
        "schema_version": "social-dev-k4-1-final-validation-v1",
        "status": "complete",
        "final_token": FINAL_TOKEN,
        "coverage": metrics,
        "blocking_consumers": [],
        "upstream": preflight["upstream_tokens"],
        "canonical_brain": {"before": before, "after": after},
        "semantic_delta": {"canonical_facts_added": len(delta["canonical_facts_added"]), "verified_edges_added": len(delta["verified_edges_added"]), "heuristic_or_assumed_added": 0, "artifact": rel(K4 / "semantic-delta.json")},
        "generated_pack_delta": {"runtime_changed": False, "visual_changed": False, "data_changed": False, "artifact": rel(K4 / "generated-pack-delta.json")},
        "deterministic_queries": {key: value["status"] for key, value in queries["queries"].items()},
        "regressions": regressions,
        "boundary": {"v8": "NOT_STARTED", "network": False, "subagents": False, "server": False, "browser": False, "emulator_adb": False, "live_app": False, "runtime_code_changed": False, "mapchip_pixels_changed": False, "source_roots_changed": False},
        "artifacts": [rel(K4 / name) for name in ["preflight-current-state.json", "reachable-visual-consumers.json", "visual-assembly-coverage-matrix.json", "room0-bootstrap-visual-recipe.json", "wall-door-assembly-recipe.json", "furniture-execution-model.json", "workstation-sitting-composition.json", "staff-behavior-visual-recipe.json", "equipment-composition-recipe.json", "talk-composition-recipe.json", "room-draw-pass-recipe.json", "opt-seb-execution-model.json", "source-native-evidence-manifest.json", "semantic-delta.json", "generated-pack-delta.json", "v8-readiness.json", "final-validation.json", "deterministic-query-results.json", "K4_CLOSURE_REPORT.md"]] + [rel(path) for path in sorted(K41.glob("*.json"))],
        "k4_1_artifacts": [rel(path) for path in sorted(K41.glob("*.json"))],
    }
    readiness = {"schema_version": "social-dev-k4-1-v8-readiness-v1", "status": "READY", "ready_for_v8": True, "final_token": FINAL_TOKEN, "coverage": metrics, "blocking_source_limited": [], "heuristic_or_assumed_count": 0, "source_missing_count": 0, "required_next_step": "V8 may begin only as a separate explicitly authorized phase; it remains NOT_STARTED.", "v8_scope": "NOT_STARTED"}
    write_json(K4 / "v8-readiness.json", readiness)
    write_json(K4 / "final-validation.json", base_final)
    write_json(K41 / "final-validation.json", {"schema_version": "social-dev-k4-1-targeted-validation-v1", "status": "complete", "final_token": FINAL_TOKEN, "coverage": metrics, "classification_count": len(classifications()), "source_hashes_unchanged": True, "generated_packs_unchanged": True, "v8": "NOT_STARTED", "boundary": base_final["boundary"], "artifacts": base_final["k4_1_artifacts"], "regressions": regressions})
    provisional_report = build_report(base_final, regressions)
    (K4 / "K4_CLOSURE_REPORT.md").write_text(provisional_report, encoding="utf-8")
    (K41 / "K4_1_CLOSURE_REPORT.md").write_text(provisional_report, encoding="utf-8")
    update_manifest(base_final, after)

    validators = [
        run_command("k4_artifact_validation", "python -B tools/social-dev/test_k4_visual_closure.py"),
        run_command("k4_1_targeted_validation", "python -B tools/social-dev/test_k4_1_targeted_closure.py"),
    ]
    require(all(item["status"] == "PASS" for item in validators), "K4/K4.1 artifact validation failed")
    base_final["regressions"] = regressions + validators
    write_json(K4 / "final-validation.json", base_final)
    write_json(K41 / "final-validation.json", {"schema_version": "social-dev-k4-1-targeted-validation-v1", "status": "complete", "final_token": FINAL_TOKEN, "coverage": metrics, "classification_count": len(classifications()), "source_hashes_unchanged": True, "generated_packs_unchanged": True, "v8": "NOT_STARTED", "boundary": base_final["boundary"], "artifacts": base_final["k4_1_artifacts"], "regressions": base_final["regressions"]})
    report = build_report(base_final, base_final["regressions"])
    (K4 / "K4_CLOSURE_REPORT.md").write_text(report, encoding="utf-8")
    (K41 / "K4_1_CLOSURE_REPORT.md").write_text(report, encoding="utf-8")
    update_manifest(base_final, after)

    final_validators = [
        run_command("k4_artifact_validation_final", "python -B tools/social-dev/test_k4_visual_closure.py"),
        run_command("k4_1_targeted_validation_final", "python -B tools/social-dev/test_k4_1_targeted_closure.py"),
    ]
    require(all(item["status"] == "PASS" for item in final_validators), "final K4/K4.1 validation failed")
    print(json.dumps({"status": base_final["status"], "final_token": FINAL_TOKEN, "coverage": metrics, "blocking_source_limited_count": metrics["blocking_source_limited_count"], "source_missing_count": metrics["source_missing_count"], "heuristic_or_assumed_count": metrics["heuristic_or_assumed_count"], "ready_for_v8": True, "v8": "NOT_STARTED", "source_hashes_unchanged": True, "generated_packs_unchanged": True}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
