"""Stage the cleaned Social Dev data slice into the active data store.

The original Social Dev source tree is intentionally preserved as read-only
provenance. This command makes an idempotent, hash-checked organized copy of
the cleaned `data` slice for active analysis; it does not execute the C#.
"""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "social dev" / "1_Click_CSharp_Code update" / "data"
DATA_ROOT = ROOT / "knowledge" / "social-dev" / "data"
DESTINATION = DATA_ROOT / "csharp_update"
MANIFEST = DATA_ROOT / "data_package_manifest.json"
REPORT = ROOT / "docs" / "reports" / "social-dev_data_package.md"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    if not SOURCE.is_dir():
        raise FileNotFoundError(f"source data directory missing: {SOURCE}")

    records = []
    for source_path in sorted(SOURCE.glob("*.cs")):
        destination_path = DESTINATION / source_path.name
        source_hash = sha256(source_path)
        if destination_path.exists():
            destination_hash = sha256(destination_path)
            if destination_hash != source_hash:
                raise ValueError(
                    f"destination differs from source: {destination_path} "
                    f"{destination_hash} != {source_hash}"
                )
        else:
            DESTINATION.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_path, destination_path)
        records.append(
            {
                "source": source_path.relative_to(ROOT).as_posix(),
                "destination": destination_path.relative_to(ROOT).as_posix(),
                "bytes": source_path.stat().st_size,
                "sha256": source_hash,
                "status": "organized_copy",
            }
        )

    payload = {
        "schema_version": "social-dev-data-package-v1",
        "package": "csharp_update_data",
        "source_status": "read_only_source_preserved",
        "runtime_status": "evidence_and_analysis_only",
        "source_root": "sources/raw/1_Click_CSharp_Code update/data",
        "destination_root": "knowledge/sources/data/csharp_update",
        "policy": "This package is an organized data copy. Decompiled C# is not executed as runtime code.",
        "records": records,
        "summary": {
            "files": len(records),
            "bytes": sum(item["bytes"] for item in records),
            "all_hashes_recorded": all(item["sha256"] for item in records),
        },
    }
    DATA_ROOT.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Social Dev organized data package",
        "",
        "The cleaned C# `data` slice is now available under `knowledge/sources/data/csharp_update/` for analysis and contract work.",
        "",
        "- Source: `sources/raw/1_Click_CSharp_Code update/data/`",
        "- Destination: `knowledge/sources/data/csharp_update/`",
        f"- Files: `{payload['summary']['files']}`",
        f"- Bytes: `{payload['summary']['bytes']}`",
        "- Status: `organized_copy`; source remains read-only and is not deleted",
        "",
        "| File | Bytes | SHA-256 |",
        "|---|---:|---|",
    ]
    for item in records:
        lines.append(f"| `{Path(item['destination']).name}` | {item['bytes']} | `{item['sha256']}` |")
    lines.extend(
        [
            "",
            "## Gate",
            "",
            "This package is not a buildable C# project and is not imported into a browser runtime. Semantic promotion still requires the Social Dev contract gates.",
            "",
            "Machine-readable manifest: `knowledge/sources/data/data_package_manifest.json`.",
        ]
    )
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"staged_data_package files={len(records)} bytes={payload['summary']['bytes']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
