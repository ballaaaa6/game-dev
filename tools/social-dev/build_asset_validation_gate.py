"""Cross-check the Social Dev asset index against ZIP/APK member inventories."""

from __future__ import annotations

import json
import zipfile
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ZIP_PATH = ROOT / "sources/raw/Social_Dev_Story_v2.5.1_ASSETS_ONLY_WITH_ASSEMBLY_GUIDE.zip"
INVENTORY = ROOT / "knowledge/fixtures/accepted/asset_binary_inventory.json"
OUTPUT = ROOT / "knowledge/fixtures/accepted/asset_validation_gate.json"
REPORT = ROOT / "docs/reports/social-dev_asset_validation_gate.md"
INDEX_PATH = "Social_Dev_Story_v2.5.1_ASSETS_ONLY/00_INDEX/ASSET_INDEX.json"
MAP_PATH = "Social_Dev_Story_v2.5.1_ASSETS_ONLY/00_INDEX/PACK_SOURCE_MAP.json"
FINGERPRINT_PATH = "Social_Dev_Story_v2.5.1_ASSETS_ONLY/00_INDEX/SOURCE_FINGERPRINT.json"


def main() -> int:
    inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
    zip_files = {record["path"]: record for record in inventory["archives"]["asset_zip"]["files"]}
    apk_files = {record["path"]: record for record in inventory["archives"]["apk"]["files"]}
    with zipfile.ZipFile(ZIP_PATH) as archive:
        asset_index = json.loads(archive.read(INDEX_PATH).decode("utf-8-sig"))
        source_map = json.loads(archive.read(MAP_PATH).decode("utf-8-sig"))
        source_fingerprint = json.loads(archive.read(FINGERPRINT_PATH).decode("utf-8-sig"))

    rows = []
    statuses = Counter()
    source_statuses = Counter()
    kind_counts = Counter()
    for item in asset_index:
        relative = item["relative_path"].replace("\\", "/")
        zip_record = zip_files.get(relative)
        expected_sha = str(item.get("sha256", "")).upper()
        if zip_record is None:
            zip_status = "zip_missing"
        elif int(item.get("size") or 0) != zip_record["bytes"]:
            zip_status = "zip_size_mismatch"
        elif expected_sha and expected_sha != zip_record["sha256"]:
            zip_status = "zip_hash_mismatch"
        else:
            zip_status = "zip_exact"
        source_entry = str(item.get("apk_source_entry") or "").replace("\\", "/")
        source_status = "apk_entry_present" if source_entry in apk_files else "apk_entry_missing"
        statuses[zip_status] += 1
        source_statuses[source_status] += 1
        kind = item.get("kind") or "unknown"
        kind_counts[kind] += 1
        rows.append(
            {
                "relative_path": relative,
                "kind": kind,
                "pack": item.get("pack"),
                "semantic_role": item.get("semantic_role"),
                "zip_status": zip_status,
                "apk_source_entry": source_entry,
                "apk_source_status": source_status,
                "runtime_status": "blocked_selector_unverified",
            }
        )

    roundtrip = Counter(str(item.get("roundtrip_exact")) for item in source_map)
    actual_apk_sha = inventory["archives"]["apk"]["sha256"]
    fingerprint_apk_sha = str(source_fingerprint.get("source_apk_sha256", "")).upper()
    payload = {
        "schema_version": "social-dev-asset-validation-gate-v1",
        "status": "evidence_gate_only",
        "asset_index_count": len(asset_index),
        "pack_source_map_count": len(source_map),
        "zip_status_counts": dict(sorted(statuses.items())),
        "apk_source_status_counts": dict(sorted(source_statuses.items())),
        "kind_counts": dict(sorted(kind_counts.items())),
        "roundtrip_exact_counts": dict(sorted(roundtrip.items())),
        "source_fingerprint": {
            "recorded_apk_sha256": fingerprint_apk_sha,
            "actual_apk_sha256": actual_apk_sha,
            "matches": fingerprint_apk_sha == actual_apk_sha,
            "matched_handoff": source_fingerprint.get("matched_handoff"),
        },
        "rows": rows,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Social Dev asset validation gate",
        "",
        "Evidence-only consistency check. No asset is runtime-approved because selector/semantic validation is still pending.",
        "",
        "## ZIP index consistency",
        "",
        "| Status | Files |",
        "|---|---:|",
    ]
    for status, count in payload["zip_status_counts"].items():
        lines.append(f"| `{status}` | {count} |")
    lines.extend(
        [
            "",
            "## APK source-entry consistency",
            "",
            "| Status | Files |",
            "|---|---:|",
        ]
    )
    for status, count in payload["apk_source_status_counts"].items():
        lines.append(f"| `{status}` | {count} |")
    lines.extend(
        [
            "",
            "## Asset kinds",
            "",
            "| Kind | Files | Runtime policy |",
            "|---|---:|---|",
        ]
    )
    for kind, count in payload["kind_counts"].items():
        policy = "candidate after selector review" if kind == "original_pack_asset" else "derived/catalog; blocked from identity promotion"
        lines.append(f"| `{kind}` | {count} | {policy} |")
    lines.extend(
        [
            "",
            "## Source fingerprint",
            "",
            f"- Recorded APK SHA-256: `{fingerprint_apk_sha}`",
            f"- Actual APK SHA-256: `{actual_apk_sha}`",
            f"- Match: `{payload['source_fingerprint']['matches']}`",
            f"- Guide matched handoff: `{source_fingerprint.get('matched_handoff')}`",
            "",
            "## Gate result",
            "",
            "ZIP/APK references are structurally consistent only when their statuses are exact/present. Every row remains `blocked_selector_unverified` until C# selectors and asset relationships are proven.",
            "",
        ]
    )
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({
        "asset_index_count": len(asset_index),
        "zip_status_counts": payload["zip_status_counts"],
        "apk_source_status_counts": payload["apk_source_status_counts"],
        "apk_fingerprint_matches": payload["source_fingerprint"]["matches"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
