#!/usr/bin/env python3
"""Validate extracted Kairosoft assets before the pipeline reports success."""

from __future__ import annotations

import json
import sys
from pathlib import Path


PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
UTF8_BOM = b"\xef\xbb\xbf"


def fail(message: str, errors: list[str]) -> None:
    errors.append(message)


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    if len(args) != 1:
        print("Usage: validate_assets.py <sprites_output>", file=sys.stderr)
        return 2

    output = Path(args[0]).expanduser().resolve()
    report_path = output / "extraction_report.json"
    errors: list[str] = []

    if not output.is_dir():
        fail(f"Asset output directory does not exist: {output}", errors)
    if not report_path.is_file():
        fail(f"Extraction report is missing: {report_path}", errors)

    report = None
    if report_path.is_file():
        try:
            report = json.loads(report_path.read_text(encoding="utf-8"))
        except Exception as exc:  # pragma: no cover - diagnostic path
            fail(f"Could not read extraction report: {exc}", errors)

    png_files = sorted(output.rglob("*.png")) if output.is_dir() else []
    csv_files = sorted(output.rglob("*.csv")) if output.is_dir() else []

    for path in png_files:
        data = path.read_bytes()
        if not data.startswith(PNG_SIGNATURE):
            fail(f"PNG header is invalid: {path}", errors)

    for path in csv_files:
        data = path.read_bytes()
        if not data.startswith(UTF8_BOM):
            fail(f"CSV is missing UTF-8 BOM for Excel: {path}", errors)
        try:
            text = data.decode("utf-8-sig")
        except UnicodeDecodeError as exc:
            fail(f"CSV is not valid UTF-8: {path} ({exc})", errors)
            continue
        first_line = text.splitlines()[0] if text.splitlines() else ""
        if first_line and not first_line.startswith("@title,"):
            fail(f"CSV still has a non-CSV header: {path}", errors)

    if isinstance(report, dict) and report.get("errors"):
        fail(f"Extractor reported {len(report['errors'])} error(s)", errors)

    if isinstance(report, dict) and report.get("warnings"):
        print(f"[WARN] Extractor repaired {len(report['warnings'])} trailing CSV UTF-8 sequence(s).")

    print(f"[INFO] Asset validation: PNG={len(png_files)}, CSV={len(csv_files)}")
    if errors:
        for message in errors:
            print(f"[ERROR] {message}", file=sys.stderr)
        return 1

    print("[OK] PNG signatures and Excel-compatible UTF-8 CSV files are valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
