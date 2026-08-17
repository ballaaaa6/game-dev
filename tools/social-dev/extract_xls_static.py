"""Recover and validate the APK's encrypted xls TextAsset with static inputs only.

The recovered files are evidence for the G1.5 canonical knowledge-base repair.
This module never launches the application, invokes ADB, or changes source
archives.  It writes only generated evidence below
``knowledge/fixtures/accepted/g1_5``.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import sys
import zipfile
from pathlib import Path
from typing import Any

import UnityPy


ROOT = Path(__file__).resolve().parents[2]
APK_PATH = ROOT / "sources/raw/Social_Dev_Story_v2.5.1.apk"
ASSET_ZIP_PATH = ROOT / "sources/raw/Social_Dev_Story_v2.5.1_ASSETS_ONLY_WITH_ASSEMBLY_GUIDE.zip"
REGISTRY_PATH = ROOT / "knowledge/fixtures/accepted/native_content_registry.json"
EVIDENCE_ROOT = ROOT / "knowledge/fixtures/accepted/g1_5"
OUTPUT_DIR = EVIDENCE_ROOT / "xls-decoded"
CONTRACT_PATH = EVIDENCE_ROOT / "xls-textasset-source-contract.json"
DECODER_CONTRACT_PATH = EVIDENCE_ROOT / "xls-decoder-contract.json"
MANIFEST_PATH = OUTPUT_DIR / "manifest.json"

EXPECTED_APK_SHA256 = "fa0e9e3a843732258fc05b2611a8e0f5be6f7e95f2141a53f31fb082322fe2bf"
XLS_CONTAINER = "assets/bin/Data/bde0731c14c1cc3429d82d5e18014b7d"
XLS_TEXT_ASSET = "xls"
XLS_CONTAINER_SHA256 = "403cb813e43d03cde7e5f88d6d7750db9d2f15747f7669889cbe99770ecf1fe3"
XLS_PAYLOAD_LENGTH = 849569
XLS_PAYLOAD_SHA256 = "0825bfe4ef17f2efe206b7f931d1715d0d0fdf48ea645e5613d6354699b2c99c"
XLS_DECRYPTED_SHA256 = "ea30e183582edf2451304577b28aaa3d039ea9cdaf497422377437284f003f60"

LANGUAGE_CONTAINER = "assets/bin/Data/3e011607c70476647900e67699290733"
LANGUAGE_TEXT_ASSET = "language_pack_template_en"
LANGUAGE_CONTAINER_SHA256 = "2b19fdbafac7346e40d7910645e1a4402f6ce8cfbb0a9cbca30d91f1924c7196"
LANGUAGE_PAYLOAD_LENGTH = 319341
LANGUAGE_PAYLOAD_SHA256 = "131979f4183112509d9ce362ea5d83d5b007edb9fca0f968302457839b09b7ce"

FORMAT_CONTAINER = "assets/bin/Data/f6ff3a51904997e4abac67717947541c"
FORMAT_TEXT_ASSET = "language_pack_format"
FORMAT_CONTAINER_SHA256 = "be79430bdea67b8d56fa7a381f0b9edc940f709205694f2d3d9dceabb2c9365f"
FORMAT_PAYLOAD_LENGTH = 652
FORMAT_PAYLOAD_SHA256 = "590f193d4fb617dc4c9ecde7450f598991979c7b154f9769af5c13b7fa78b0f3"

ARCHIVE_PREFIX = "Social_Dev_Story_v2.5.1_ASSETS_ONLY/01_GAME_PACKS/xls/"


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def stable_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def normalize_stem(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", value.lower())


def extract_text_asset(container: bytes, expected_name: str) -> tuple[str, bytes]:
    environment = UnityPy.load(container)
    matches: list[tuple[str, bytes]] = []
    for obj in environment.objects:
        data = obj.read()
        if getattr(data, "m_Name", None) != expected_name:
            continue
        script = getattr(data, "m_Script", None)
        require(script is not None, f"TextAsset {expected_name} has no m_Script payload")
        if isinstance(script, bytes):
            payload = script
        else:
            payload = str(script).encode("utf-8", "surrogateescape")
        matches.append((str(data.m_Name), payload))
    require(len(matches) == 1, f"expected one {expected_name} TextAsset, found {len(matches)}")
    return matches[0]


def recover_xor_key() -> tuple[bytes, dict[str, Any]]:
    """Use the already accepted static key recovery from the phase-3A tool."""

    tool_dir = Path(__file__).resolve().parent
    sys.path.insert(0, str(tool_dir))
    from extract_phase3a_chairs_from_apk import recover_xor_key as accepted_recover_xor_key

    return accepted_recover_xor_key()


def decrypt_xls(payload: bytes) -> tuple[bytes, dict[str, Any]]:
    key, key_record = recover_xor_key()
    decrypted = bytes(value ^ key[index % len(key)] for index, value in enumerate(payload))
    require(len(decrypted) == len(payload), "xls decryption changed payload length")
    return decrypted, {
        "key_recovery": key_record,
        "encrypted_length": len(payload),
        "encrypted_sha256": sha256_bytes(payload),
        "decrypted_length": len(decrypted),
        "decrypted_sha256": sha256_bytes(decrypted),
    }


def parse_pack(plain: bytes) -> tuple[dict[str, int], list[dict[str, Any]]]:
    """Parse the JarInflater length-prefixed pack format.

    The implementation is intentionally local and explicit so the evidence
    records the decoder contract instead of depending on a runtime loader.
    """

    import struct

    require(len(plain) >= 12, "decrypted xls payload is shorter than its header")
    data_offset, data_length, file_count = struct.unpack(">III", plain[:12])
    position = 12
    names: list[str] = []
    for _ in range(file_count):
        require(position + 4 <= len(plain), "xls name length exceeds payload")
        name_length = struct.unpack(">I", plain[position : position + 4])[0]
        position += 4
        require(position + name_length <= len(plain), "xls name exceeds payload")
        names.append(plain[position : position + name_length].decode("utf-8"))
        position += name_length

    table_end = position + file_count * 8
    require(table_end <= len(plain), "xls offset/size tables exceed payload")
    offsets = [struct.unpack(">I", plain[position + index * 4 : position + index * 4 + 4])[0] for index in range(file_count)]
    position += file_count * 4
    sizes = [struct.unpack(">I", plain[position + index * 4 : position + index * 4 + 4])[0] for index in range(file_count)]

    # JarInflater's data_ begins four bytes after the header's data_offset.
    data_base = data_offset + 4
    entries: list[dict[str, Any]] = []
    for name, pack_offset, declared_size in zip(names, offsets, sizes):
        prefix_offset = data_base + pack_offset
        require(prefix_offset + 4 <= len(plain), f"xls length prefix exceeds payload: {name}")
        output_size = struct.unpack(">I", plain[prefix_offset : prefix_offset + 4])[0]
        output_start = prefix_offset + 4
        output_end = output_start + output_size
        require(output_end <= len(plain), f"xls output exceeds payload: {name}")
        require(output_size == declared_size, f"xls size mismatch for {name}: {output_size} != {declared_size}")
        entries.append(
            {
                "name": name,
                "pack_offset": pack_offset,
                "declared_size": declared_size,
                "prefix_offset": prefix_offset,
                "output_size": output_size,
                "output_start": output_start,
                "output_end": output_end,
                "sha256": sha256_bytes(plain[output_start:output_end]),
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


def row_metadata(raw: bytes) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for physical_line, line in enumerate(raw.splitlines(), 1):
        if not line.strip():
            continue
        text = line.decode("utf-8", "replace")
        parsed = next(csv.reader([text], delimiter="\t"))
        native_id: int | None
        try:
            native_id = int(parsed[0]) if parsed else None
        except ValueError:
            native_id = None
        rows.append(
            {
                "physical_line": physical_line,
                "native_id": native_id,
                "columns": parsed,
                "raw_row_sha256": sha256_bytes(line),
            }
        )
    return rows


def language_summary(raw: bytes) -> dict[str, Any]:
    rows = list(csv.reader(io.StringIO(raw.decode("utf-8-sig"))))
    skill_rows: list[dict[str, Any]] = []
    ids: set[int] = set()
    for line_number, row in enumerate(rows, 1):
        if len(row) < 3 or row[1].lower() != "skill":
            continue
        parts = [part for part in row[2].split("&") if part]
        row_ids: list[int] = []
        for part in parts:
            match = re.match(r"^(\d+)-", part)
            require(match is not None, f"skill localization key is not numeric: {part}")
            row_id = int(match.group(1))
            row_ids.append(row_id)
            ids.add(row_id)
        skill_rows.append({"line": line_number, "id_keys": row_ids, "columns": row})
    return {
        "row_count": len(rows),
        "skill_row_count": len(skill_rows),
        "skill_unique_id_count": len(ids),
        "skill_ids": sorted(ids),
        "skill_rows": skill_rows,
    }


def compare_asset_zip(entries: dict[str, bytes]) -> dict[str, Any]:
    require(ASSET_ZIP_PATH.is_file(), f"asset ZIP is missing: {ASSET_ZIP_PATH}")
    with zipfile.ZipFile(ASSET_ZIP_PATH) as archive:
        members = {
            name[len(ARCHIVE_PREFIX) :]: archive.read(name)
            for name in archive.namelist()
            if name.startswith(ARCHIVE_PREFIX) and not name.endswith("/")
        }
    apk_names = set(entries)
    zip_names = set(members)
    missing = sorted(zip_names - apk_names)
    extra = sorted(apk_names - zip_names)
    mismatches = sorted(name for name in apk_names & zip_names if entries[name] != members[name])
    return {
        "zip_path": str(ASSET_ZIP_PATH.relative_to(ROOT)).replace("\\", "/"),
        "zip_entry_count": len(zip_names),
        "apk_entry_count": len(apk_names),
        "missing_from_apk": missing,
        "extra_in_apk": extra,
        "byte_mismatches": mismatches,
        "all_entries_byte_exact": not missing and not extra and not mismatches,
    }


def run(apk_path: Path = APK_PATH) -> dict[str, Any]:
    require(apk_path.is_file(), f"APK is missing: {apk_path}")
    require(sha256_file(apk_path) == EXPECTED_APK_SHA256, "pinned APK hash mismatch")
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))

    with zipfile.ZipFile(apk_path) as archive:
        names = set(archive.namelist())
        required_entries = {XLS_CONTAINER, LANGUAGE_CONTAINER, FORMAT_CONTAINER}
        require(required_entries <= names, "one or more pinned Unity resource containers are missing")
        xls_container = archive.read(XLS_CONTAINER)
        language_container = archive.read(LANGUAGE_CONTAINER)
        format_container = archive.read(FORMAT_CONTAINER)

    require(sha256_bytes(xls_container) == XLS_CONTAINER_SHA256, "xls container hash mismatch")
    require(sha256_bytes(language_container) == LANGUAGE_CONTAINER_SHA256, "language container hash mismatch")
    require(sha256_bytes(format_container) == FORMAT_CONTAINER_SHA256, "language format container hash mismatch")

    xls_name, xls_payload = extract_text_asset(xls_container, XLS_TEXT_ASSET)
    language_name, language_payload = extract_text_asset(language_container, LANGUAGE_TEXT_ASSET)
    format_name, format_payload = extract_text_asset(format_container, FORMAT_TEXT_ASSET)
    require(xls_name == XLS_TEXT_ASSET, "unexpected xls TextAsset name")
    require(len(xls_payload) == XLS_PAYLOAD_LENGTH and sha256_bytes(xls_payload) == XLS_PAYLOAD_SHA256, "xls payload identity mismatch")
    require(len(language_payload) == LANGUAGE_PAYLOAD_LENGTH and sha256_bytes(language_payload) == LANGUAGE_PAYLOAD_SHA256, "language payload identity mismatch")
    require(len(format_payload) == FORMAT_PAYLOAD_LENGTH and sha256_bytes(format_payload) == FORMAT_PAYLOAD_SHA256, "language format payload identity mismatch")

    plain, decrypt_record = decrypt_xls(xls_payload)
    require(sha256_bytes(plain) == XLS_DECRYPTED_SHA256, "decrypted xls identity mismatch")
    header, parsed_entries = parse_pack(plain)
    entry_bytes = {entry["name"]: entry["bytes"] for entry in parsed_entries}
    require(len(entry_bytes) == len(parsed_entries) == header["file_count"], "xls entry names are not unique")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for old in OUTPUT_DIR.rglob("*.txt"):
        old.unlink()
    for name, payload in sorted(entry_bytes.items()):
        target = OUTPUT_DIR / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(payload)

    registry_by_stem = {normalize_stem(row.get("table_stem", "")): row for row in registry.get("data_types", []) if row.get("table_stem")}
    tables: list[dict[str, Any]] = []
    for name, payload in sorted(entry_bytes.items()):
        if not name.lower().endswith(".txt") or "/" not in name:
            continue
        locale, filename = name.split("/", 1)
        stem = Path(filename).stem
        registry_row = registry_by_stem.get(normalize_stem(stem))
        rows = row_metadata(payload)
        record = {
            "name": name,
            "locale": locale,
            "table_stem": stem,
            "registry_element_type": registry_row.get("element_type") if registry_row else None,
            "registry_row_count": registry_row.get("row_count") if registry_row else None,
            "row_count": len(rows),
            "sha256": sha256_bytes(payload),
            "rows": rows,
        }
        if registry_row:
            expected = registry_row.get("rows", [])
            expected_locale = [row.get("locales", {}).get(locale, {}) for row in expected]
            expected_hashes = [row.get("raw_row_sha256") for row in expected_locale]
            actual_hashes = [row["raw_row_sha256"] for row in rows]
            record["registry_row_count_match"] = len(rows) == registry_row.get("row_count")
            record["registry_row_hashes_match"] = actual_hashes == expected_hashes
        tables.append(record)

    zip_compare = compare_asset_zip(entry_bytes)
    require(zip_compare["all_entries_byte_exact"], "xls APK entries do not match supplied asset ZIP")
    require(all(row.get("registry_row_count_match", True) for row in tables), "xls row counts disagree with the canonical registry")
    require(all(row.get("registry_row_hashes_match", True) for row in tables), "xls row hashes disagree with the canonical registry")

    language = language_summary(language_payload)
    require(language["skill_row_count"] == 72, "unexpected number of Skill localization rows")
    require(language["skill_unique_id_count"] == 36 and language["skill_ids"] == list(range(36)), "Skill localization IDs are not exactly 0..35")

    source_contract = {
        "status": "PASS_XLS_TEXTASSET_SOURCE_PINNED",
        "apk": {"path": str(apk_path.relative_to(ROOT)).replace("\\", "/"), "sha256": sha256_file(apk_path)},
        "containers": [
            {"path": XLS_CONTAINER, "sha256": sha256_bytes(xls_container), "text_asset": xls_name, "payload_length": len(xls_payload), "payload_sha256": sha256_bytes(xls_payload)},
            {"path": LANGUAGE_CONTAINER, "sha256": sha256_bytes(language_container), "text_asset": language_name, "payload_length": len(language_payload), "payload_sha256": sha256_bytes(language_payload)},
            {"path": FORMAT_CONTAINER, "sha256": sha256_bytes(format_container), "text_asset": format_name, "payload_length": len(format_payload), "payload_sha256": sha256_bytes(format_payload)},
        ],
        "language_summary": {key: value for key, value in language.items() if key != "skill_rows"},
        "static_only": True,
    }
    decoder_contract = {
        "status": "PASS_XLS_DECRYPT_AND_PACK_DECODE",
        "key_recovery": decrypt_record["key_recovery"],
        "encrypted": {"length": len(xls_payload), "sha256": sha256_bytes(xls_payload)},
        "decrypted": {"length": len(plain), "sha256": sha256_bytes(plain)},
        "pack_header": header,
        "entry_count": len(parsed_entries),
        "entry_names": sorted(entry_bytes),
        "asset_zip_compare": zip_compare,
        "registry_row_checks": {
            "table_file_count": len(tables),
            "row_count_matches": sum(1 for row in tables if row.get("registry_row_count_match", True)),
            "row_hash_matches": sum(1 for row in tables if row.get("registry_row_hashes_match", True)),
        },
        "format": {
            "data_offset_semantics": "data_base_offset = data_offset + 4",
            "entry_offset_semantics": "each table offset addresses a four-byte big-endian output-size prefix",
            "output_size_must_equal_declared_size": True,
        },
        "static_only": True,
    }
    manifest = {
        "status": "PASS_XLS_STATIC_SOURCE_AND_DECODER",
        "source_contract": str(CONTRACT_PATH.relative_to(ROOT)).replace("\\", "/"),
        "decoder_contract": str(DECODER_CONTRACT_PATH.relative_to(ROOT)).replace("\\", "/"),
        "raw_output_root": str(OUTPUT_DIR.relative_to(ROOT)).replace("\\", "/"),
        "xls": {"text_asset": xls_name, "payload_sha256": sha256_bytes(xls_payload), "decrypted_sha256": sha256_bytes(plain), "header": header},
        "language_pack": {"text_asset": language_name, "payload_sha256": sha256_bytes(language_payload), "summary": language},
        "language_pack_format": {"text_asset": format_name, "payload_sha256": sha256_bytes(format_payload)},
        "tables": tables,
        "asset_zip_compare": zip_compare,
        "static_only": True,
    }
    write_json(CONTRACT_PATH, source_contract)
    write_json(DECODER_CONTRACT_PATH, decoder_contract)
    write_json(MANIFEST_PATH, manifest)
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apk", type=Path, default=APK_PATH)
    args = parser.parse_args()
    result = run(args.apk.resolve())
    print(json.dumps({
        "status": result["status"],
        "entries": result["xls"]["header"]["file_count"],
        "asset_zip_byte_exact": result["asset_zip_compare"]["all_entries_byte_exact"],
        "skill_ids": result["language_pack"]["summary"]["skill_ids"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
