"""Inventory the Social Dev asset ZIP and APK without extracting or modifying them."""

from __future__ import annotations

import csv
import hashlib
import io
import json
import zipfile
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ZIP_PATH = ROOT / "sources/raw/Social_Dev_Story_v2.5.1_ASSETS_ONLY_WITH_ASSEMBLY_GUIDE.zip"
APK_PATH = ROOT / "sources/raw/Social_Dev_Story_v2.5.1.apk"
OUTPUT = ROOT / "knowledge/fixtures/accepted/asset_binary_inventory.json"
REPORT = ROOT / "docs/reports/social-dev_asset_binary_inventory.md"
INDEX_NAMES = {
    "00_INDEX/ASSEMBLY_GUIDE_MANIFEST.json",
    "00_INDEX/ASSET_INDEX.json",
    "00_INDEX/PACK_SOURCE_MAP.json",
    "00_INDEX/SOURCE_FINGERPRINT.json",
    "00_INDEX/ASSET_INDEX.csv",
    "00_INDEX/PACK_SOURCE_MAP.csv",
    "00_INDEX/SHA256SUMS.txt",
}


def digest_member(archive: zipfile.ZipFile, info: zipfile.ZipInfo) -> str:
    digest = hashlib.sha256()
    with archive.open(info, "r") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def summarize_json(data: bytes) -> dict:
    try:
        value = json.loads(data.decode("utf-8-sig"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        return {"parse_status": "invalid", "error": type(exc).__name__}
    summary = {"parse_status": "valid", "value_type": type(value).__name__}
    if isinstance(value, dict):
        summary["keys"] = sorted(str(key) for key in value)[:100]
        summary["key_count"] = len(value)
        for key, item in value.items():
            if isinstance(item, (list, dict)):
                summary[f"{key}_count"] = len(item)
    elif isinstance(value, list):
        summary["item_count"] = len(value)
        if value and isinstance(value[0], dict):
            summary["first_item_keys"] = sorted(str(key) for key in value[0])[:100]
    return summary


def summarize_csv(data: bytes) -> dict:
    text = data.decode("utf-8-sig", errors="replace")
    rows = list(csv.reader(io.StringIO(text)))
    return {
        "parse_status": "read",
        "row_count_including_header": len(rows),
        "header": rows[0] if rows else [],
    }


def inventory_archive(
    path: Path,
    label: str,
    read_indices: bool = False,
    strip_prefix: str = "",
) -> dict:
    with zipfile.ZipFile(path) as archive:
        records = []
        groups = Counter()
        duplicates = Counter()
        index_summary = {}
        seen = set()
        for info in archive.infolist():
            archive_name = info.filename.replace("\\", "/")
            name = archive_name
            if strip_prefix and name.startswith(strip_prefix):
                name = name[len(strip_prefix) :]
            if name.endswith("/"):
                continue
            if name in seen:
                duplicates[name] += 1
            seen.add(name)
            groups[name.split("/", 1)[0]] += 1
            record = {
                "path": name,
                "archive_path": archive_name,
                "bytes": info.file_size,
                "compressed_bytes": info.compress_size,
                "crc32": f"{info.CRC:08X}",
                "compression": info.compress_type,
                "sha256": digest_member(archive, info),
            }
            records.append(record)
            if read_indices and name in INDEX_NAMES:
                raw = archive.read(info)
                if name.endswith(".json"):
                    index_summary[name] = summarize_json(raw)
                elif name.endswith(".csv"):
                    index_summary[name] = summarize_csv(raw)
                else:
                    index_summary[name] = {
                        "parse_status": "text",
                        "line_count": len(raw.decode("utf-8-sig", errors="replace").splitlines()),
                    }
        return {
            "path": str(path),
            "bytes": path.stat().st_size,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest().upper(),
            "members": len(records),
            "total_uncompressed_bytes": sum(item["bytes"] for item in records),
            "top_level_groups": dict(sorted(groups.items())),
            "duplicate_paths": dict(sorted(duplicates.items())),
            "index_summaries": index_summary,
            "files": records,
        }


def main() -> int:
    payload = {
        "schema_version": "social-dev-asset-binary-inventory-v1",
        "policy": "Read-only ZIP/APK inventory; no asset is promoted to runtime by this report.",
        "archives": {
            "asset_zip": inventory_archive(
                ZIP_PATH,
                "asset_zip",
                read_indices=True,
                strip_prefix="Social_Dev_Story_v2.5.1_ASSETS_ONLY/",
            ),
            "apk": inventory_archive(APK_PATH, "apk", read_indices=False),
        },
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    zip_info = payload["archives"]["asset_zip"]
    apk_info = payload["archives"]["apk"]
    lines = [
        "# Social Dev asset and APK binary inventory",
        "",
        "Read-only inventory. ZIP/APK members were hashed in place; neither archive was extracted or modified.",
        "",
        "| Source | Members | Uncompressed bytes | SHA-256 |",
        "|---|---:|---:|---|",
        f"| Asset ZIP | {zip_info['members']} | {zip_info['total_uncompressed_bytes']:,} | `{zip_info['sha256']}` |",
        f"| APK | {apk_info['members']} | {apk_info['total_uncompressed_bytes']:,} | `{apk_info['sha256']}` |",
        "",
        "## Asset ZIP groups",
        "",
        "| Group | Files |",
        "|---|---:|",
    ]
    for group, count in zip_info["top_level_groups"].items():
        lines.append(f"| `{group}` | {count} |")
    lines.extend(
        [
            "",
            "## APK groups",
            "",
            "| Group | Files |",
            "|---|---:|",
        ]
    )
    for group, count in apk_info["top_level_groups"].items():
        lines.append(f"| `{group}` | {count} |")
    lines.extend(
        [
            "",
            "## Index summaries",
            "",
            "The assembly guide/index files are parsed only for shape and counts. Their rows still require cross-checking against C# selectors and APK provenance.",
            "",
            "| Index | Summary |",
            "|---|---|",
        ]
    )
    for name, summary in zip_info["index_summaries"].items():
        lines.append(f"| `{name}` | `{json.dumps(summary, ensure_ascii=False, sort_keys=True)}` |")
    lines.extend(
        [
            "",
            "## Gate",
            "",
            "No image, animation, `.inf`, `.opt`, or `.seb` member is runtime-approved by this inventory. Promotion waits for identity/selector/relationship validation.",
            "",
        ]
    )
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"asset_zip_members": zip_info["members"], "apk_members": apk_info["members"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
