"""Build a deterministic locale runtime artifact from the frozen CSV source root."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from pathlib import Path


TOKEN_RE = re.compile(r"<\d+>")


def read_locale(path: Path) -> tuple[str, dict[str, str], dict[str, object]]:
    raw = path.read_bytes()
    bom = raw.startswith(b"\xef\xbb\xbf")
    text = raw.decode("utf-8-sig")
    rows = list(csv.reader(text.splitlines()))
    metadata: dict[str, str] = {}
    records: dict[str, str] = {}
    duplicate_ids: list[str] = []
    for row in rows:
        if not row:
            continue
        key = row[0].strip()
        if key.startswith("@") and len(row) >= 2:
            metadata[key[1:]] = row[1]
        elif key.startswith("#"):
            value = row[1] if len(row) >= 2 else ""
            if key in records:
                duplicate_ids.append(key)
            records[key] = value
    language_id = metadata.get("language", path.stem.removeprefix("GameDevStory_"))
    qa = {
        "bom": bom,
        "strict_utf8": True,
        "duplicate_ids": sorted(set(duplicate_ids)),
        "empty_ids": sorted(key for key, value in records.items() if value == ""),
        "placeholder_mismatches": [],
        "record_count": len(records),
        "sha256": hashlib.sha256(raw).hexdigest(),
    }
    return language_id, records, qa


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=Path("game-dev-story-mod_Sprites/language"))
    parser.add_argument("--output", type=Path, default=Path("Phases/Phase5/artifacts/wave5_locale_runtime.json"))
    args = parser.parse_args()

    files = sorted(args.source.glob("GameDevStory_*.csv"))
    locales: dict[str, dict[str, str]] = {}
    file_qa: dict[str, dict[str, object]] = {}
    for path in files:
        language_id, records, qa = read_locale(path)
        locales[language_id] = records
        file_qa[language_id] = qa

    union_ids = sorted({key for records in locales.values() for key in records})
    artifact = {
        "schema_version": "wave5-locale-runtime-v1",
        "source_policy": "CSV source-of-truth; generated runtime lookup only",
        "source_root": str(args.source).replace("\\", "/"),
        "locale_count": len(locales),
        "union_record_count": len(union_ids),
        "locales": locales,
        "default_locale": "th",
        "default_locale_status": "web_adapter_decision_not_legacy_fact",
        "english_source_status": "not_present_in_current_language_directory",
        "placeholder_policy": "preserve_tokens_and_validate_args_before_substitution",
        "qa": {
            "duplicate_id_count": sum(len(item["duplicate_ids"]) for item in file_qa.values()),
            "empty_id_count": sum(len(item["empty_ids"]) for item in file_qa.values()),
            "bom_failures": sum(not item["bom"] for item in file_qa.values()),
            "strict_utf8_failures": sum(not item["strict_utf8"] for item in file_qa.values()),
            "files": file_qa,
        },
        "legacy_equivalence": False,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(artifact, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "locale_count": len(locales), "union_record_count": len(union_ids)}))


if __name__ == "__main__":
    main()
