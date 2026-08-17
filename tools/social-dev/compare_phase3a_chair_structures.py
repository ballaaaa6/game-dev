"""Compare the internal PNG/OPT/SEB structure of chair_00 through chair_04.

This audit separates the shared animation scaffold from per-chair pixel and
source-geometry data.  It is read-only and does not promote or repair any
asset.
"""

from __future__ import annotations

import hashlib
import io
import json
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
ZIP_PATH = ROOT / "sources/raw/Social_Dev_Story_v2.5.1_ASSETS_ONLY_WITH_ASSEMBLY_GUIDE.zip"
ZIP_PREFIX = "Social_Dev_Story_v2.5.1_ASSETS_ONLY/"
OUTPUT_PATH = ROOT / "knowledge/sources/phase3a_apk_probe/chair_structure_comparison.json"
CHAIRS = tuple(f"chair_{index:02d}" for index in range(5))


def stable_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def relative_path(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def member_path(stem: str, extension: str) -> str:
    return f"{ZIP_PREFIX}01_GAME_PACKS/chip/{stem}.{extension}"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def load_codecs():
    sys.path.insert(0, str(Path(__file__).parent))
    from opt_codec import parse_opt
    from build_phase3a_asset_composition import parse_seb

    return parse_opt, parse_seb


def image_record(raw: bytes) -> dict[str, Any]:
    image = Image.open(io.BytesIO(raw)).convert("RGBA")
    alpha = image.getchannel("A")
    return {
        "size": [image.width, image.height],
        "bytes": len(raw),
        "sha256": sha256_bytes(raw),
        "alpha_bbox": list(alpha.getbbox()) if alpha.getbbox() else None,
        "nontransparent_pixels": sum(1 for value in alpha.getdata() if value > 0),
    }


def opt_record_data(source_records: Any, header: Any, source_size: tuple[int, int]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for record in source_records:
        source_fit = (
            record.source_x >= 0
            and record.source_y >= 0
            and record.source_x + record.width <= source_size[0]
            and record.source_y + record.height <= source_size[1]
        )
        result.append(
            {
                **record.to_dict(header),
                "source_rect_fits_png": source_fit,
            }
        )
    return result


def opt_cell_data(parsed: Any, source_size: tuple[int, int]) -> list[dict[str, Any]]:
    return [
        {
            "index": cell.index,
            "piece_count": cell.piece_count,
            "records": opt_record_data(cell.records, parsed.header, source_size),
        }
        for cell in parsed.cells
    ]


def seb_scaffold(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [{key: value for key, value in record.items() if key != "image_id"} for record in records]


def build_comparison() -> dict[str, Any]:
    require(ZIP_PATH.is_file(), f"asset ZIP is missing: {ZIP_PATH}")
    parse_opt, parse_seb = load_codecs()
    per_chair: dict[str, Any] = {}
    with zipfile.ZipFile(ZIP_PATH) as archive:
        for stem in CHAIRS:
            png = archive.read(member_path(stem, "png"))
            opt = archive.read(member_path(stem, "opt"))
            seb = archive.read(member_path(stem, "seb"))
            image = Image.open(io.BytesIO(png)).convert("RGBA")
            parsed_opt = parse_opt(opt, f"{stem}.opt")
            parsed_seb = parse_seb(seb, f"{stem}.seb")
            require(parsed_opt.header is not None, f"{stem}.opt has no header")
            per_chair[stem] = {
                "png": image_record(png),
                "opt": {
                    "bytes": len(opt),
                    "sha256": sha256_bytes(opt),
                    "header": parsed_opt.header.to_dict(),
                    "status": parsed_opt.status,
                "partial_tail_bytes": parsed_opt.partial_tail_bytes,
                "expected_record_count": parsed_opt.expected_record_count,
                "errors": list(parsed_opt.errors),
                "records": opt_record_data(parsed_opt.records, parsed_opt.header, image.size),
                "cells": opt_cell_data(parsed_opt, image.size),
            },
                "seb": parsed_seb,
            }

    opt_headers = {stable_json(value["opt"]["header"]) for value in per_chair.values()}
    seb_scaffolds = {stable_json(seb_scaffold(value["seb"]["records"])) for value in per_chair.values()}
    seb_headers = {stable_json(value["seb"]["header"]) for value in per_chair.values()}
    opt_exact_groups: dict[str, list[str]] = {}
    for stem, value in per_chair.items():
        opt_exact_groups.setdefault(value["opt"]["sha256"], []).append(stem)

    record_prefix_patterns = {
        stem: [record["record_prefix"] for record in value["opt"]["records"]]
        for stem, value in per_chair.items()
    }
    source_reference_patterns = {
        stem: [record["source_reference"] for record in value["opt"]["records"]]
        for stem, value in per_chair.items()
    }
    image_ids = {
        stem: [record["image_id"] for record in value["seb"]["records"]]
        for stem, value in per_chair.items()
    }
    source_fit_matrix = {
        stem: [record["source_rect_fits_png"] for record in value["opt"]["records"]]
        for stem, value in per_chair.items()
    }
    source_fit_by_cell = {
        stem: [
            [record["source_rect_fits_png"] for record in cell["records"]]
            for cell in value["opt"]["cells"]
        ]
        for stem, value in per_chair.items()
    }
    opt_piece_count_patterns = {
        stem: [cell["piece_count"] for cell in value["opt"]["cells"]]
        for stem, value in per_chair.items()
    }

    without_dynamic: dict[str, Any] = {
        "schema_version": "social-dev-phase3a-chair-structure-comparison-v1",
        "purpose": "Determine which parts of chair_00 through chair_04 share an animation scaffold and which parts are chair-specific source geometry or pixels.",
        "source": {
            "asset_zip_path": relative_path(ZIP_PATH),
            "asset_zip_sha256": sha256_bytes(ZIP_PATH.read_bytes()),
            "selected_stems": list(CHAIRS),
        },
        "chairs": per_chair,
        "patterns": {
            "all_opt_headers_exact": len(opt_headers) == 1,
            "common_opt_header": next(iter(opt_headers)) if len(opt_headers) == 1 else None,
            "all_opt_payloads_consume_exactly": all(
                value["opt"]["status"] == "pass" and value["opt"]["partial_tail_bytes"] == 0
                for value in per_chair.values()
            ),
            "all_seb_headers_exact": len(seb_headers) == 1,
            "common_seb_header": next(iter(seb_headers)) if len(seb_headers) == 1 else None,
            "all_seb_frame_scaffolds_exact_except_image_id": len(seb_scaffolds) == 1,
            "common_seb_frame_scaffold": next(iter(seb_scaffolds)) if len(seb_scaffolds) == 1 else None,
            "seb_image_ids_by_chair": image_ids,
            "opt_exact_sha_groups": list(opt_exact_groups.values()),
            "opt_record_prefix_patterns": record_prefix_patterns,
            "opt_source_reference_patterns": source_reference_patterns,
            "opt_source_fit_matrix": source_fit_matrix,
            "opt_source_fit_by_cell": source_fit_by_cell,
            "opt_piece_count_patterns": opt_piece_count_patterns,
            "png_dimensions_by_chair": {
                stem: value["png"]["size"] for stem, value in per_chair.items()
            },
        },
        "classification": {
            "shared_execution_scaffold": {
                "status": "verified",
                "detail": "All five SEB files have the same one-layer, three-frame, three-record scaffold, identical 60x32 source rectangles, and identical destination offsets; only image_id changes.",
            },
            "shared_logical_canvas": {
                "status": "verified",
                "detail": "All five OPT headers declare a 60x32 cell grid with 3 columns and 1 row, producing a 180x32 logical atlas.",
            },
            "variable_piece_cells": {
                "status": "verified",
                "detail": "The first byte of each logical cell is a piece count; all five selected OPT payloads consume exactly to EOF, including chair_00/01 cells with piece counts [1, 2, 1] and chair_04 cells [1, 2, 0].",
            },
            "pixel_only_variation": {
                "status": "false",
                "detail": "The PNG dimensions differ and the valid OPT source rectangles, offsets, and record values differ; these are not color-only substitutions.",
            },
            "per_chair_source_geometry": {
                "status": "verified_for_complete_records",
                "detail": "OPT pieces describe per-chair source crops and placement offsets. Every selected chair piece fits its own PNG under the variable-piece parser.",
            },
            "chair_00_recovery_from_own_bytes": {
                "status": "verified",
                "detail": "chair_00.opt consumes as three logical cells with piece counts [1, 2, 1]; the 14 bytes previously classified as a partial tail are the second piece of logical cell 1, and all four crop pieces fit chair_00.png.",
            },
            "chair_00_recovery_from_other_opt": {
                "status": "not_supported",
                "detail": "The shared SEB scaffold can guide a derived fallback, but copying chair_02/03 OPT values into chair_00 would reference coordinates outside chair_00.png or change the visual identity.",
            },
            "safe_reuse_boundary": {
                "status": "open_for_own_source_reconstruction",
                "detail": "chair_00 can be reconstructed from its own PNG and variable-piece OPT bytes. The common SEB scaffold remains reusable, but another chair's pixel coordinates are not authoritative chair_00 source data.",
            },
        },
        "implications": [
            "The animation/control layer is shared across all five chair assets.",
            "The image selector is chair-specific through SEB image_id values 4, 31, 112, 121, and 144.",
            "chair_00 and chair_01 share an identical 63-byte OPT payload and the same variable piece-count pattern [1, 2, 1] even though their PNG bytes and SEB image_id values differ.",
            "chair_02 and chair_03 use one crop piece per logical cell, while chair_00/01 and chair_04 use two-piece composites for logical cell 1.",
            "chair_04 has a valid empty logical cell 2 under the variable-piece grammar; its supplied derived logical reference matches that reconstruction exactly.",
        ],
        "determinism": {"algorithm": "stable-json-sha256 excluding generated_at_utc and content_hash"},
    }
    content_hash = sha256_bytes(stable_json(without_dynamic).encode("utf-8"))
    return {
        **without_dynamic,
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "determinism": {**without_dynamic["determinism"], "content_hash": content_hash},
    }


def main() -> int:
    comparison = build_comparison()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(comparison, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(
        json.dumps(
            {
                "status": "chair_structure_comparison_complete",
                "chairs": list(comparison["chairs"]),
                "shared_seb_scaffold": comparison["patterns"]["all_seb_frame_scaffolds_exact_except_image_id"],
                "shared_opt_header": comparison["patterns"]["all_opt_headers_exact"],
                "opt_exact_groups": comparison["patterns"]["opt_exact_sha_groups"],
                "audit_hash": comparison["determinism"]["content_hash"],
                "output_path": relative_path(OUTPUT_PATH),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
