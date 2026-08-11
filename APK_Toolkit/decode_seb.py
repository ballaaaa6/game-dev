#!/usr/bin/env python3
"""Decode the evidence visible in Kairosoft ``.seb`` sprite descriptors.

The decompiled ``kairo_unity_ui_Seb`` loader reads the legacy variant as:

    group_count, max_frame, then for each group:
    record_count, group_id, and ``record_count`` records of ten big-endian
    signed shorts (frame, texture, UV/size, translation, reverse flags).

The current extracted files are consistently four bytes shorter than that
format predicts.  This module therefore never pads or repairs source bytes;
it decodes complete fields, records the exact shortfall, and marks a partial
final record explicitly.  It is intentionally a structural decoder, not a
claim about runtime animation semantics.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from phase_paths import phase_artifacts_dir


TARGET_GROUPS = ("office", "game", "com", "system")
FORMAT0_FIELDS = (
    "frame",
    "texture_id",
    "u",
    "v",
    "w",
    "h",
    "trans_x",
    "trans_y",
    "reverse_u",
    "reverse_v",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def signed_byte(value: int) -> int:
    return value - 256 if value & 0x80 else value


def signed_short(data: bytes, offset: int) -> int:
    return int.from_bytes(data[offset : offset + 2], "big", signed=True)


class SebReader:
    """Small bounds-aware reader that preserves the source offset."""

    def __init__(self, data: bytes):
        self.data = data
        self.offset = 0

    def take(self, length: int) -> bytes:
        start = self.offset
        end = min(len(self.data), start + length)
        self.offset = end
        return self.data[start:end]

    def byte(self) -> int | None:
        chunk = self.take(1)
        return chunk[0] if len(chunk) == 1 else None

    def short(self) -> int | None:
        chunk = self.take(2)
        return int.from_bytes(chunk, "big", signed=True) if len(chunk) == 2 else None

    def remaining(self) -> int:
        return max(0, len(self.data) - self.offset)


def _record_status(missing_fields: list[str], raw: bytes) -> str:
    if not missing_fields:
        return "complete"
    if raw:
        return "partial_final_record"
    return "missing_record_bytes"


def decode_format0_record(reader: SebReader, record_index: int) -> dict[str, Any]:
    start = reader.offset
    values: dict[str, int] = {}
    missing: list[str] = []
    for field in FORMAT0_FIELDS:
        value = reader.short()
        if value is None:
            missing.append(field)
        else:
            values[field] = value
    end = reader.offset
    raw_end = min(len(reader.data), start + 2 * len(FORMAT0_FIELDS))
    raw = reader.data[start:raw_end]
    return {
        "index": record_index,
        "offset": start,
        "expected_bytes": 2 * len(FORMAT0_FIELDS),
        "available_bytes": len(raw),
        "fields": values,
        "missing_fields": missing,
        "complete": not missing,
        "status": _record_status(missing, raw),
        "raw_hex": raw.hex(),
    }


def _read_format1_short(reader: SebReader, fields: dict[str, int], name: str, missing: list[str]) -> None:
    value = reader.short()
    if value is None:
        missing.append(name)
    else:
        fields[name] = value


def _read_format1_byte(reader: SebReader, fields: dict[str, int], name: str, missing: list[str]) -> None:
    value = reader.byte()
    if value is None:
        missing.append(name)
    else:
        fields[name] = value


def decode_format1_record(reader: SebReader, record_index: int) -> dict[str, Any]:
    """Best-effort decode of the compact variant visible in the decompile.

    No current Phase 1 target uses this variant.  The conditional reads mirror
    the branches in ``kairo.c`` closely enough to preserve offsets and EOF
    evidence if a future extraction introduces one.
    """

    start = reader.offset
    fields: dict[str, int] = {}
    missing: list[str] = []
    _read_format1_short(reader, fields, "frame", missing)
    _read_format1_short(reader, fields, "texture_id", missing)
    texture_id = fields.get("texture_id")

    # The decompiled call at this point is InputStream.Read(), i.e. one byte
    # represented as an int.  Keep the byte value and the source distinction.
    _read_format1_byte(reader, fields, "blend_byte", missing)

    if texture_id is not None and texture_id < 0:
        # Negative textures may carry four colour bytes in the compact path.
        # The source condition is texture_id + 6 < 5 (texture_id < -1) or a
        # non-zero blend byte.  This is the only branch that consumes colour.
        if texture_id < -1 or fields.get("blend_byte", 0) != 0:
            for name in ("color_r", "color_g", "color_b", "color_a"):
                _read_format1_byte(reader, fields, name, missing)

    if texture_id is not None and (texture_id >= 0 or texture_id == -8):
        _read_format1_short(reader, fields, "u", missing)
        _read_format1_short(reader, fields, "v", missing)
    _read_format1_short(reader, fields, "w", missing)
    _read_format1_short(reader, fields, "h", missing)

    if texture_id is not None and texture_id >= 0:
        flag = reader.byte()
        if flag is None:
            missing.append("flags")
        else:
            fields["flags"] = flag
            fields["reverse_u"] = 1 if flag & 1 else 0
            fields["reverse_v"] = 1 if flag & 2 else 0

    end = reader.offset
    raw = reader.data[start:min(len(reader.data), end)]
    return {
        "index": record_index,
        "offset": start,
        "expected_bytes": None,
        "available_bytes": len(raw),
        "fields": fields,
        "missing_fields": missing,
        "complete": not missing,
        "status": _record_status(missing, raw),
        "raw_hex": raw.hex(),
    }


def parse_seb_bytes(data: bytes, relative_path: str | None = None) -> dict[str, Any]:
    """Parse one SEB byte sequence without mutating or padding it."""

    result: dict[str, Any] = {
        "relative_path": relative_path,
        "size_bytes": len(data),
        "sha256": sha256_bytes(data),
        "format_code": None,
        "format_name": None,
        "header": {},
        "groups": [],
        "bytes_consumed": 0,
        "expected_bytes": None,
        "trailing_bytes": 0,
        "tail_shortfall_bytes": 0,
        "status": "parse_error",
        "errors": [],
        "confidence": "unknown",
    }
    reader = SebReader(data)
    first = reader.byte()
    if first is None:
        result["errors"].append("missing_format_selector")
        return result

    if first & 0x80:
        format_code = -signed_byte(first)
        format_name = "compact_variant"
        group_count = reader.short()
    else:
        format_code = 0
        format_name = "legacy_ten_short_record"
        second = reader.byte()
        group_count = (first << 8) | second if second is not None else None

    max_frame = reader.short()
    result["format_code"] = format_code
    result["format_name"] = format_name
    result["header"] = {
        "format_selector_byte": first,
        "group_count": group_count,
        "max_frame": max_frame,
        "header_bytes": reader.offset,
    }
    if group_count is None:
        result["errors"].append("truncated_group_count")
        result["bytes_consumed"] = reader.offset
        return result
    if max_frame is None:
        result["errors"].append("truncated_max_frame")
        result["bytes_consumed"] = reader.offset
        return result
    if group_count < 0:
        result["errors"].append("negative_group_count")
        result["bytes_consumed"] = reader.offset
        return result

    expected_bytes: int | None = reader.offset
    record_decoder = decode_format0_record if format_code == 0 else decode_format1_record
    if format_code != 0:
        # This remains an evidence-preserving parser, but the format-1 record
        # size is conditional and therefore cannot be predicted up front.
        expected_bytes = None

    for group_index in range(group_count):
        group_start = reader.offset
        record_count = reader.short()
        group_id: int | None = None
        if format_code == 0:
            group_id = reader.short()
        group: dict[str, Any] = {
            "index": group_index,
            "offset": group_start,
            "record_count": record_count,
            "group_id": group_id,
            "header_bytes": reader.offset - group_start,
            "records": [],
            "status": "complete",
        }
        if record_count is None or (format_code == 0 and group_id is None):
            group["status"] = "truncated_group_header"
            group["missing_header_bytes"] = (2 if record_count is None else 0) + (
                2 if format_code == 0 and group_id is None else 0
            )
            result["groups"].append(group)
            result["errors"].append(f"group_{group_index}_header_truncated")
            break
        if record_count < 0:
            group["status"] = "negative_record_count"
            result["groups"].append(group)
            result["errors"].append(f"group_{group_index}_negative_record_count")
            break
        if expected_bytes is not None:
            expected_bytes += 4 + record_count * 2 * len(FORMAT0_FIELDS)

        for record_index in range(record_count):
            record = record_decoder(reader, record_index)
            group["records"].append(record)
            if not record["complete"]:
                group["status"] = "truncated_record"
                # Once EOF has been observed, the remaining declared records
                # cannot have any bytes.  Keep their count visible without
                # pretending that missing bytes were present.
                for missing_index in range(record_index + 1, record_count):
                    group["records"].append(
                        {
                            "index": missing_index,
                            "offset": len(data),
                            "expected_bytes": 2 * len(FORMAT0_FIELDS) if format_code == 0 else None,
                            "available_bytes": 0,
                            "fields": {},
                            "missing_fields": list(FORMAT0_FIELDS) if format_code == 0 else [],
                            "complete": False,
                            "status": "missing_record_bytes",
                            "raw_hex": "",
                        }
                    )
                    group["status"] = "truncated_record"
                break
        result["groups"].append(group)
        if group["status"] != "complete":
            break

    result["bytes_consumed"] = reader.offset
    result["expected_bytes"] = expected_bytes
    if expected_bytes is not None:
        result["tail_shortfall_bytes"] = max(0, expected_bytes - len(data))
        result["trailing_bytes"] = max(0, len(data) - expected_bytes)
    else:
        result["trailing_bytes"] = reader.remaining()

    partial_records = [
        (group["index"], record["index"])
        for group in result["groups"]
        for record in group.get("records", [])
        if not record.get("complete")
    ]
    if result["errors"]:
        result["status"] = "parse_error"
        result["confidence"] = "unknown"
    elif partial_records:
        result["status"] = "truncated_final_record" if result["tail_shortfall_bytes"] else "partial_record"
        result["confidence"] = "partial"
    elif result["trailing_bytes"]:
        result["status"] = "decoded_with_trailing_bytes"
        result["confidence"] = "structural"
    else:
        result["status"] = "decoded"
        result["confidence"] = "structural"
    return result


def discover_seb_files(workspace: Path) -> list[Path]:
    root = workspace / "game-dev-story-mod_Sprites"
    return sorted(
        path
        for group in TARGET_GROUPS
        for path in (root / group).rglob("*.seb")
        if path.is_file()
    )


def build_manifest(workspace: Path, generated_at: str) -> dict[str, Any]:
    root = workspace / "game-dev-story-mod_Sprites"
    files: list[dict[str, Any]] = []
    for path in discover_seb_files(workspace):
        relative_path = path.relative_to(root).as_posix()
        decoded = parse_seb_bytes(path.read_bytes(), relative_path)
        files.append(decoded)

    status_counts: dict[str, int] = {}
    format_counts: dict[str, int] = {}
    for item in files:
        status_counts[item["status"]] = status_counts.get(item["status"], 0) + 1
        name = str(item.get("format_name"))
        format_counts[name] = format_counts.get(name, 0) + 1
    tail_shortfalls = [item for item in files if item.get("tail_shortfall_bytes")]
    errors = [item for item in files if item.get("errors")]
    return {
        "schema": 1,
        "generated_at_utc": generated_at,
        "phase": "phase1",
        "source_root": "game-dev-story-mod_Sprites",
        "source_policy": "Read-only source bytes; decoder records missing/trailing bytes without padding or repair.",
        "format_evidence": {
            "selector_rule": "high bit clear: two-byte group count; high bit set: negative selector plus short group count",
            "legacy_record_fields": list(FORMAT0_FIELDS),
            "source_references": [
                {
                    "path": "game-dev-story-mod_Dumped/Categorized_Code/Global/kairo.c",
                    "function": "kairo_unity_ui_Seb___load",
                    "line_hint": "112950-113050",
                    "claim": "format 0 reads group count, max frame, group id, then ten big-endian shorts per record",
                },
                {
                    "path": "game-dev-story-mod_Dumped/Categorized_Code/Global/Method.c",
                    "function": "Method_kairo_unity_util_StreamUtil_Read",
                    "line_hint": "107096-107250",
                    "claim": "short reads throw EOFException when the requested bytes are not available",
                },
            ],
        },
        "counts": {
            "files": len(files),
            "by_status": status_counts,
            "by_format": format_counts,
            "tail_shortfall_files": len(tail_shortfalls),
            "parse_error_files": len(errors),
        },
        "known_limitations": [
            "All current extracted SEB files use the legacy selector, but every one is four bytes shorter than the declared ten-short record structure predicts.",
            "The shortfall is preserved as source/extraction evidence; no zero padding or inferred reverse flags are emitted.",
            "This decoder establishes structural fields only. It does not assign animation semantics, pivots, collision, seat, or depth meaning.",
        ],
        "files": files,
    }


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--workspace",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="workspace root containing game-dev-story-mod_Sprites",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="output JSON path (default: <workspace>/Phases/Phase1/artifacts/phase1_seb_manifest.json)",
    )
    args = parser.parse_args(list(argv) if argv is not None else None)
    workspace = args.workspace.expanduser().resolve()
    output = (args.output or (phase_artifacts_dir(workspace, 1) / "phase1_seb_manifest.json")).expanduser()
    if not output.is_absolute():
        output = workspace / output
    try:
        manifest = build_manifest(workspace, utc_now())
        write_json(output, manifest)
    except Exception as exc:
        print(f"[ERROR] SEB decode failed: {exc}", file=sys.stderr)
        return 1

    print(f"[OK] Decoded {manifest['counts']['files']} SEB files structurally.")
    print(f"[INFO] Statuses: {manifest['counts']['by_status']}")
    print(
        f"[INFO] Tail shortfall files={manifest['counts']['tail_shortfall_files']}; "
        f"parse errors={manifest['counts']['parse_error_files']}"
    )
    return 0 if not manifest["counts"]["parse_error_files"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
