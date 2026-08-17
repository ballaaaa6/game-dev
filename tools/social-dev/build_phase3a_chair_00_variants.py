"""Build historical non-authoritative visual variants for chair_00.

The source ZIP and APK outputs remain read-only.  This tool creates derived
previews only; it does not replace ``chair_00.opt`` or promote any variant to
the runtime asset boundary. These variants predate the validated variable-piece
OPT grammar and are retained only as comparison evidence; the exact
source-backed reconstruction is produced by
``build_phase3a_chair_00_reconstruction.py``.

Variants:

1. ``known_plus_duplicate`` keeps the two source-backed chair_00 OPT records
   and duplicates the largest known logical cell into the missing third cell.
2. ``chair_02_substitute`` uses the complete chair_02 logical atlas for all
   three frames, preserving the chair_00 SEB frame layout but changing the
   visual identity.
3. ``known_plus_chair_02_missing_cell`` keeps chair_00's known cells and uses
   chair_02 only for the missing third cell.
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

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[2]
ZIP_PATH = ROOT / "sources/raw/Social_Dev_Story_v2.5.1_ASSETS_ONLY_WITH_ASSEMBLY_GUIDE.zip"
ZIP_PREFIX = "Social_Dev_Story_v2.5.1_ASSETS_ONLY/"
OUTPUT_DIR = ROOT / "knowledge/sources/phase3a_apk_probe/chair_variants"
AUDIT_PATH = OUTPUT_DIR / "chair_00_variant_audit.json"
COMPARISON_PATH = OUTPUT_DIR / "chair_00_variant_comparison.png"
CHAIR00_OPT_SHA256 = "5cf124773282b1693210853c6fb04a35426a55d04b08cccb61daa4b8f7454f0a"
CHAIR02_PIXEL_SHA256 = "caf40e4a94974d85520fae1eb06f93a615af76dd11973118185598fafbf7dcde"
FRAME_WIDTH = 60
FRAME_HEIGHT = 32
FRAME_ORDER = (1, 0, 2)  # chair_00.seb source rectangles for game frames 0,1,2
SCALE = 6


def stable_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def relative_path(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def member_name(path: str) -> str:
    return ZIP_PREFIX + path


def load_opt_codec():
    sys.path.insert(0, str(Path(__file__).parent))
    from opt_codec import OptHeader, OptPayload, OptRecord, parse_opt, reconstruct_opt

    return OptHeader, OptPayload, OptRecord, parse_opt, reconstruct_opt


def paste_clipped(destination: Image.Image, source: Image.Image, x: int, y: int) -> None:
    left = max(0, -x)
    top = max(0, -y)
    right = min(source.width, destination.width - x)
    bottom = min(source.height, destination.height - y)
    if left >= right or top >= bottom:
        return
    cropped = source.crop((left, top, right, bottom))
    destination.alpha_composite(cropped, (max(0, x), max(0, y)))


def apply_record(atlas: Image.Image, source: Image.Image, header: Any, record: Any) -> None:
    crop = source.crop(
        (
            record.source_x,
            record.source_y,
            record.source_x + record.width,
            record.source_y + record.height,
        )
    )
    destination_x, destination_y = record.destination(header)
    paste_clipped(atlas, crop, destination_x, destination_y)


def checker(size: tuple[int, int], square: int = 4) -> Image.Image:
    image = Image.new("RGBA", size, (236, 236, 236, 255))
    draw = ImageDraw.Draw(image)
    for y in range(0, size[1], square):
        for x in range(0, size[0], square):
            if ((x // square) + (y // square)) % 2:
                draw.rectangle((x, y, min(size[0] - 1, x + square - 1), min(size[1] - 1, y + square - 1)), fill=(205, 205, 205, 255))
    return image


def frame_preview(atlas: Image.Image, logical_cell: int) -> Image.Image:
    crop = atlas.crop((logical_cell * FRAME_WIDTH, 0, (logical_cell + 1) * FRAME_WIDTH, FRAME_HEIGHT))
    background = checker(crop.size)
    background.alpha_composite(crop)
    return background.resize((FRAME_WIDTH * SCALE, FRAME_HEIGHT * SCALE), Image.Resampling.NEAREST)


def nontransparent_count(image: Image.Image) -> int:
    return sum(1 for pixel in image.getdata() if pixel[3] > 0)


def logical_cell_metrics(atlas: Image.Image) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for cell in range(3):
        crop = atlas.crop((cell * FRAME_WIDTH, 0, (cell + 1) * FRAME_WIDTH, FRAME_HEIGHT))
        alpha = crop.getchannel("A")
        bbox = alpha.getbbox()
        result.append(
            {
                "logical_cell": cell,
                "nontransparent_pixels": nontransparent_count(crop),
                "alpha_bbox": list(bbox) if bbox else None,
            }
        )
    return result


def build_known_atlas(chair00_png: bytes, chair00_opt: bytes) -> tuple[Image.Image, dict[str, Any]]:
    OptHeader, _, _, parse_opt, _ = load_opt_codec()
    parsed = parse_opt(chair00_opt, "chair_00.opt")
    assert parsed.header is not None
    assert parsed.sha256 == CHAIR00_OPT_SHA256
    source = Image.open(io.BytesIO(chair00_png)).convert("RGBA")
    atlas = Image.new("RGBA", (parsed.header.logical_width, parsed.header.logical_height), (0, 0, 0, 0))
    applied: list[int] = []
    for record in parsed.records[:2]:
        assert record.source_x >= 0 and record.source_y >= 0
        assert record.source_x + record.width <= source.width
        assert record.source_y + record.height <= source.height
        apply_record(atlas, source, parsed.header, record)
        applied.append(record.index)
    cell0 = atlas.crop((0, 0, FRAME_WIDTH, FRAME_HEIGHT))
    atlas.alpha_composite(cell0, (2 * FRAME_WIDTH, 0))
    return atlas, {
        "source_png_size": [source.width, source.height],
        "source_opt_size_bytes": len(chair00_opt),
        "source_opt_sha256": parsed.sha256,
        "source_opt_status": parsed.status,
        "source_opt_partial_tail_bytes": parsed.partial_tail_bytes,
        "source_opt_errors": list(parsed.errors),
        "applied_source_records": applied,
        "duplicated_logical_cell": 0,
        "duplicate_reason": "Cell 0 has the largest source-backed known sprite and is used as the explicit missing-frame fallback.",
    }


def replace_logical_cell(atlas: Image.Image, source_atlas: Image.Image, target_cell: int, source_cell: int) -> Image.Image:
    result = atlas.copy()
    crop = source_atlas.crop((source_cell * FRAME_WIDTH, 0, (source_cell + 1) * FRAME_WIDTH, FRAME_HEIGHT))
    result.alpha_composite(crop, (target_cell * FRAME_WIDTH, 0))
    return result


def build_comparison_sheet(variants: list[tuple[str, Image.Image]]) -> Image.Image:
    frame_width = FRAME_WIDTH * SCALE
    frame_height = FRAME_HEIGHT * SCALE
    label_height = 28
    row_height = frame_height + label_height + 16
    sheet = Image.new("RGBA", (frame_width * 3 + 32, row_height * len(variants) + 20), (250, 250, 250, 255))
    draw = ImageDraw.Draw(sheet)
    for row, (label, atlas) in enumerate(variants):
        y = 10 + row * row_height
        draw.text((8, y + 2), label, fill=(20, 20, 20, 255))
        for column, logical_cell in enumerate(FRAME_ORDER):
            x = 8 + column * (frame_width + 4)
            preview = frame_preview(atlas, logical_cell)
            sheet.alpha_composite(preview, (x, y + label_height))
            draw.text((x + 4, y + label_height + 4), f"game frame {column}", fill=(255, 255, 255, 255), stroke_width=1, stroke_fill=(0, 0, 0, 255))
    return sheet


def build_audit() -> dict[str, Any]:
    _, _, _, parse_opt, reconstruct_opt = load_opt_codec()
    with zipfile.ZipFile(ZIP_PATH) as archive:
        read = lambda path: archive.read(member_name(path))
        chair00_png = read("01_GAME_PACKS/chip/chair_00.png")
        chair00_opt = read("01_GAME_PACKS/chip/chair_00.opt")
        chair02_png = read("01_GAME_PACKS/chip/chair_02.png")
        chair02_opt = read("01_GAME_PACKS/chip/chair_02.opt")
        chair02_reference = read("02_DERIVED_READY_IMAGES/opt_reconstructed/chip/chair_02.logical.png")

    chair02_result = reconstruct_opt(chair02_png, chair02_opt, "chair_02.png", "chair_02.opt")
    assert chair02_result.status == "pass"
    assert chair02_result.image is not None
    assert chair02_result.pixel_sha256 == CHAIR02_PIXEL_SHA256
    chair02_atlas = chair02_result.image
    reference_image = Image.open(io.BytesIO(chair02_reference)).convert("RGBA")
    assert list(chair02_atlas.getdata()) == list(reference_image.getdata())

    known_atlas, known_details = build_known_atlas(chair00_png, chair00_opt)
    substitute_atlas = chair02_atlas.copy()
    hybrid_atlas = replace_logical_cell(known_atlas, chair02_atlas, target_cell=2, source_cell=2)

    variants = [
        ("variant_1_known_plus_duplicate", known_atlas, "closest_to_chair_00_identity; missing cell 2 duplicates known cell 0"),
        ("variant_2_chair_02_substitute", substitute_atlas, "complete and coherent; uses chair_02 for all three cells"),
        ("variant_3_known_plus_chair_02_missing_cell", hybrid_atlas, "keeps chair_00 cells 0/1; uses chair_02 cell 2"),
    ]
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    variant_records: dict[str, Any] = {}
    for name, atlas, rationale in variants:
        path = OUTPUT_DIR / f"chair_00.{name}.logical.png"
        atlas.save(path)
        variant_records[name] = {
            "path": relative_path(path),
            "sha256": sha256_bytes(path.read_bytes()),
            "size_bytes": path.stat().st_size,
            "logical_size": list(atlas.size),
            "game_frame_order": list(FRAME_ORDER),
            "cell_metrics": logical_cell_metrics(atlas),
            "rationale": rationale,
            "authoritative_source": False,
            "runtime_promoted": False,
        }

    comparison = build_comparison_sheet([(name, atlas) for name, atlas, _ in variants])
    comparison.save(COMPARISON_PATH)

    audit_without_dynamic: dict[str, Any] = {
        "schema_version": "social-dev-phase3a-chair-00-derived-variants-v1",
        "purpose": "Retain three historical non-authoritative chair_00 approximation previews for comparison after the exact variable-piece reconstruction was identified.",
        "source": {
            "asset_zip_path": str(ZIP_PATH.relative_to(ROOT)).replace("\\", "/"),
            "asset_zip_sha256": sha256_bytes(ZIP_PATH.read_bytes()),
            "chair_00_png_sha256": sha256_bytes(chair00_png),
            "chair_00_png_size": list(Image.open(io.BytesIO(chair00_png)).size),
            "chair_00_opt_sha256": sha256_bytes(chair00_opt),
            "chair_00_opt_size_bytes": len(chair00_opt),
            "chair_00_seb_member": "01_GAME_PACKS/chip/chair_00.seb",
            "chair_02_reference_pixel_sha256": CHAIR02_PIXEL_SHA256,
        },
        "known_chair_00_data": known_details,
        "chair_02_complete_reference": {
            "opt_status": chair02_result.parsed.status,
            "opt_size_bytes": chair02_result.parsed.size_bytes,
            "logical_size": list(chair02_atlas.size),
            "pixel_sha256": chair02_result.pixel_sha256,
            "matches_supplied_derived_reference": True,
        },
        "variants": variant_records,
        "comparison_sheet": {
            "path": relative_path(COMPARISON_PATH),
            "sha256": sha256_bytes(COMPARISON_PATH.read_bytes()),
            "size_bytes": COMPARISON_PATH.stat().st_size,
            "frame_order_note": "Columns are game frame 0, 1, 2; chair_00.seb maps them to logical cells 1, 0, 2.",
        },
        "evaluation": {
            "variant_1_known_plus_duplicate": {
                "identity_fidelity": "best_available",
                "frame_completeness": "partial",
                "visual_result": "blue chair identity is retained, but game frame 0 remains a small source-backed fragment",
                "verdict": "not_ready_for_runtime",
            },
            "variant_2_chair_02_substitute": {
                "identity_fidelity": "wrong_variant",
                "frame_completeness": "complete",
                "visual_result": "all three frames are coherent and renderable, but the pixels belong to chair_02",
                "verdict": "best_for_functional_demo_only",
            },
            "variant_3_known_plus_chair_02_missing_cell": {
                "identity_fidelity": "mixed",
                "frame_completeness": "partial_identity",
                "visual_result": "chair_00 and chair_02 pixels visibly mix; frame 0 remains the sparse chair_00 fragment",
                "verdict": "not_recommended",
            },
            "overall": {
                "best_functional_demo": "variant_2_chair_02_substitute",
                "best_source_identity": "variant_1_known_plus_duplicate_but_not_complete",
                "exact_chair_00_recovery": "not_achieved",
                "runtime_promotion": "none",
            },
        },
        "decision_boundary": {
            "source_bytes_changed": False,
            "original_chair_00_opt_repaired": False,
            "runtime_manifest_changed": False,
            "all_variants_are_derived_approximations": True,
            "exact_game_visual_recovery": False,
        },
        "determinism": {"algorithm": "stable-json-sha256 excluding generated_at_utc and content_hash"},
    }
    content_hash = sha256_bytes(stable_json(audit_without_dynamic).encode("utf-8"))
    return {
        **audit_without_dynamic,
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "determinism": {**audit_without_dynamic["determinism"], "content_hash": content_hash},
    }


def main() -> int:
    audit = build_audit()
    AUDIT_PATH.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(
        json.dumps(
            {
                "status": "derived_variants_created",
                "variants": list(audit["variants"]),
                "comparison_sheet": relative_path(COMPARISON_PATH),
                "audit_hash": audit["determinism"]["content_hash"],
                "audit_path": relative_path(AUDIT_PATH),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
