"""Build provenance-first inventories for the Social Dev source reset.

This tool only reads source/extraction roots. It writes derived manifests and a
short report under knowledge/fixtures/accepted and docs/reports.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, Mapping


ROOT = Path(__file__).resolve().parents[2]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def file_record(path: Path, root: Path) -> dict:
    stat = path.stat()
    relative = path.relative_to(root).as_posix()
    return {
        "path": relative,
        "extension": path.suffix.lower(),
        "bytes": stat.st_size,
        "sha256": sha256_file(path),
    }


def records(root: Path) -> Dict[str, dict]:
    return {
        path.relative_to(root).as_posix(): file_record(path, root)
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def source_summary(items: Mapping[str, dict]) -> dict:
    extensions = Counter(item["extension"] or "[none]" for item in items.values())
    return {
        "files": len(items),
        "bytes": sum(item["bytes"] for item in items.values()),
        "extensions": dict(sorted(extensions.items())),
    }


def scope_for(relative: str) -> str:
    first = relative.split("/", 1)[0]
    if first in {"data", "game", "game.routeSearch"}:
        return "gameplay_candidate"
    if first == "form":
        return "presentation_candidate"
    if first == "main":
        return "lifecycle_candidate"
    if first == "KairoEngine":
        return "engine_or_framework"
    if first in {
        "Dependencies",
        "Firebase",
        "Firebase.Messaging",
        "Firebase.Platform",
        "Firebase.Platform.Default",
        "Firebase.Unity",
        "System",
        "system",
        "Microsoft.CSharp",
        "Microsoft.Win32",
        "java.io",
        "java.lang",
        "java.native",
        "java.net",
        "java.util",
        "Internal.Cryptography",
        "Internal.Cryptography.Pal",
        "Internal.Runtime.Augments",
        "Internal.Threading.Tasks.Tracing",
    }:
        return "dependency_or_generated"
    if first in {"AOT", "BuildInfos", "Cpp2ILInjected", "Properties"}:
        return "extraction_support"
    if first.startswith("kairo.") or first in {
        "kfw.bsp",
        "kfw.panel",
        "surface",
        "panel",
        "native",
        "util",
        "ext",
        "ext.util",
        "mail.form",
        "mail.ui",
        "news",
    }:
        return "engine_or_framework"
    return "review_required"


def source_scope(label: str, relative: str) -> str:
    if label == "csharp_update":
        if relative.startswith("KairoEngine/main/"):
            return "lifecycle_candidate"
        if relative.startswith("KairoEngine/"):
            return "engine_or_framework"
        if relative.startswith("Dependencies/"):
            return "dependency_or_generated"
    return scope_for(relative)


def source_payload(label: str, root: Path) -> dict:
    items = records(root)
    scoped = Counter(source_scope(label, relative) for relative in items)
    return {
        "label": label,
        "root": str(root),
        "summary": source_summary(items),
        "scope_counts": dict(sorted(scoped.items())),
        "files": items,
    }


def comparable_path(relative: str, corpus: str) -> str:
    """Normalize layout-only wrappers used by the curated update corpus."""
    if corpus == "update":
        if relative.startswith("Dependencies/"):
            return relative[len("Dependencies/") :]
        if relative.startswith("KairoEngine/"):
            return relative[len("KairoEngine/") :]
        if relative.startswith("form/SubForm_Split/"):
            return "__split__" + relative
    return relative


def normalized_items(items: Mapping[str, dict], corpus: str) -> dict:
    output = {}
    for relative, item in items.items():
        comparable = comparable_path(relative, corpus)
        # Keep both records if a cleanup/split produced a collision. It is
        # deliberately represented as a conflict instead of silently merging.
        if comparable in output:
            existing = output[comparable]
            if isinstance(existing, list):
                existing.append(item)
            else:
                output[comparable] = [existing, item]
        else:
            output[comparable] = item
    return output


def one_item(value):
    return value[0] if isinstance(value, list) else value


def compare(raw: Mapping[str, dict], update: Mapping[str, dict]) -> dict:
    raw_normalized = normalized_items(raw, "raw")
    update_normalized = normalized_items(update, "update")
    paths = sorted(set(raw_normalized) | set(update_normalized))
    entries = []
    statuses = Counter()
    for comparable in paths:
        raw_value = raw_normalized.get(comparable)
        update_value = update_normalized.get(comparable)
        raw_item = one_item(raw_value) if raw_value else None
        update_item = one_item(update_value) if update_value else None
        collision = isinstance(raw_value, list) or isinstance(update_value, list)
        if raw_item and update_item:
            if collision:
                status = "path_collision"
            else:
                status = "exact_match" if raw_item["sha256"] == update_item["sha256"] else "modified"
        elif update_item:
            status = "update_only_collision" if collision else "update_only"
        else:
            status = "raw_only_collision" if collision else "raw_only"
        statuses[status] += 1
        entries.append(
            {
                "comparable_path": comparable,
                "raw_paths": [item["path"] for item in raw_value] if isinstance(raw_value, list) else ([raw_item["path"]] if raw_item else []),
                "update_paths": [item["path"] for item in update_value] if isinstance(update_value, list) else ([update_item["path"]] if update_item else []),
                "scope": scope_for(comparable),
                "status": status,
                "raw_bytes": raw_item["bytes"] if raw_item else None,
                "update_bytes": update_item["bytes"] if update_item else None,
                "raw_sha256": raw_item["sha256"] if raw_item else None,
                "update_sha256": update_item["sha256"] if update_item else None,
            }
        )
    return {
        "raw_summary": source_summary(raw),
        "update_summary": source_summary(update),
        "status_counts": dict(sorted(statuses.items())),
        "scope_status_counts": {
            scope: dict(sorted(Counter(entry["status"] for entry in entries if entry["scope"] == scope).items()))
            for scope in sorted({entry["scope"] for entry in entries})
        },
        "entries": entries,
    }


def external_file_record(path: Path) -> dict:
    stat = path.stat()
    return {"path": str(path), "bytes": stat.st_size, "sha256": sha256_file(path)}


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_report(path: Path, payload: dict) -> None:
    raw = payload["sources"]["rar_extracted"]
    update = payload["sources"]["csharp_update"]
    comparison = payload["comparison"]
    lines = [
        "# Social Dev reset — source inventory",
        "",
        f"Generated: `{payload['generated_at']}`",
        "",
        "This is a read-only provenance pass over the active Social Dev source and evidence roots.",
        "",
        "## Source summary",
        "",
        "| Source | Files | Bytes | Initial role |",
        "|---|---:|---:|---|",
        f"| RAR extraction | {raw['summary']['files']} | {raw['summary']['bytes']:,} | immutable C# evidence baseline |",
        f"| C# update | {update['summary']['files']} | {update['summary']['bytes']:,} | curated candidate corpus |",
        "",
        "## C# update comparison",
        "",
        "The comparison uses canonical paths: the archive's top-level `1_Click_CSharp_Code` directory is removed and layout-only `Dependencies/` and `KairoEngine/` wrappers in the update are removed. Split `form/SubForm_Split/` files remain explicit update-only candidates.",
        "",
        "| Status | Files | Meaning |",
        "|---|---:|---|",
    ]
    meanings = {
        "exact_match": "same canonical path and SHA-256",
        "modified": "same canonical path but different bytes; review before promotion",
        "update_only": "present only in the update corpus",
        "raw_only": "present only in the RAR baseline",
        "path_collision": "normalization produced multiple files; manual review required",
        "update_only_collision": "update-only path with a collision; manual review required",
        "raw_only_collision": "raw-only path with a collision; manual review required",
    }
    for status, count in comparison["status_counts"].items():
        lines.append(f"| {status} | {count} | {meanings.get(status, '')} |")
    lines.extend(
        [
            "",
            "## Initial classification",
            "",
            "| Scope | Update files | Treatment |",
            "|---|---:|---|",
        ]
    )
    treatments = {
        "gameplay_candidate": "promote only after semantic/provenance review",
        "lifecycle_candidate": "save/load and lifecycle evidence; keep separate from entities",
        "presentation_candidate": "UI evidence; do not use as state owner",
        "engine_or_framework": "dependency evidence; exclude from game schema",
        "dependency_or_generated": "inventory only unless a bounded dependency is required",
        "extraction_support": "retain for provenance, not gameplay semantics",
        "review_required": "manual classification required",
    }
    for scope, count in sorted(update["scope_counts"].items()):
        lines.append(f"| {scope} | {count} | {treatments.get(scope, '')} |")
    lines.extend(
        [
            "",
            "## Next gate",
            "",
            "Review modified/raw-only/update-only paths, then build the Social Dev canonical schema from `data`, `game`, and bounded `main` lifecycle evidence. Asset promotion remains blocked until the C# selectors and ZIP/APK provenance agree.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    root = args.root.resolve()

    raw_root = root / "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code"
    update_root = root / "sources/raw/1_Click_CSharp_Code update"
    for required in (raw_root, update_root):
        if not required.is_dir():
            raise SystemExit(f"Missing input directory: {required}")

    raw_items = records(raw_root)
    update_items = records(update_root)
    source_files = {}
    for relative in (
        "sources/raw/1_Click_CSharp_Code.rar",
        "sources/raw/Social_Dev_Story_v2.5.1.apk",
        "sources/raw/Social_Dev_Story_v2.5.1_ASSETS_ONLY_WITH_ASSEMBLY_GUIDE.zip",
    ):
        path = root / relative
        if path.is_file():
            source_files[relative] = external_file_record(path)

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "purpose": "Social Dev clean-room reset; read-only source inventory",
        "source_files": source_files,
        "sources": {
            "rar_extracted": source_payload("rar_extracted", raw_root),
            "csharp_update": source_payload("csharp_update", update_root),
        },
        "comparison": compare(raw_items, update_items),
    }

    evidence = root / "knowledge/fixtures/accepted"
    write_json(evidence / "source_inventory.json", payload)
    write_json(evidence / "csharp_update_comparison.json", payload["comparison"])
    write_report(root / "docs/reports/social-dev_reset_inventory.md", payload)
    print(json.dumps({
        "source_files": len(source_files),
        "rar_files": len(raw_items),
        "update_files": len(update_items),
        "comparison": payload["comparison"]["status_counts"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
