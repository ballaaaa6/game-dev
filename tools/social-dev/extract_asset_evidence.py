"""Extract only text/index evidence from the Social Dev asset ZIP."""

from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ZIP_PATH = ROOT / "sources/raw/Social_Dev_Story_v2.5.1_ASSETS_ONLY_WITH_ASSEMBLY_GUIDE.zip"
OUTPUT = ROOT / "knowledge/sources/asset_guide_20260813"
PREFIX = "Social_Dev_Story_v2.5.1_ASSETS_ONLY/"
ALLOW = ("00_INDEX/", "05_ASSEMBLY_GUIDE/", "01_GAME_PACKS/xls/")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def main() -> int:
    records = []
    with zipfile.ZipFile(ZIP_PATH) as archive:
        for info in archive.infolist():
            archive_name = info.filename.replace("\\", "/")
            if not archive_name.startswith(PREFIX):
                continue
            relative = archive_name[len(PREFIX) :]
            if relative.endswith("/") or not relative.startswith(ALLOW):
                continue
            data = archive.read(info)
            destination = OUTPUT / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(data)
            records.append(
                {
                    "source_archive_member": archive_name,
                    "relative_path": relative,
                    "bytes": len(data),
                    "sha256": digest(data),
                }
            )
    manifest = {
        "schema_version": "social-dev-asset-evidence-extraction-v1",
        "source_archive": str(ZIP_PATH),
        "source_archive_sha256": digest(ZIP_PATH.read_bytes()),
        "policy": "Only index, assembly guide, and xls text evidence was extracted. Binary image packs remain in the source ZIP.",
        "files": sorted(records, key=lambda item: item["relative_path"]),
    }
    (OUTPUT / "extraction_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({"files": len(records), "bytes": sum(item["bytes"] for item in records)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
