"""Build the exact source-backed logical reconstruction for chair_00.

The output is generated evidence only.  The source ZIP remains read-only and
the runtime boundary is handled by the display-asset gate after this audit
passes.
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
ARCHIVE_PREFIX = "Social_Dev_Story_v2.5.1_ASSETS_ONLY/"
OUTPUT_DIR = ROOT / "knowledge/sources/phase3a_apk_probe/derived_previews"
LOGICAL_OUTPUT = OUTPUT_DIR / "chair_00.logical.png"
SOURCE_CROP_MAP_OUTPUT = OUTPUT_DIR / "chair_00.source_crop_map.png"
AUDIT_OUTPUT = ROOT / "knowledge/sources/phase3a_apk_probe/chair_00_reconstruction_audit.json"


def stable_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def relative_path(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def load_codec():
    sys.path.insert(0, str(Path(__file__).parent))
    from opt_codec import parse_opt, reconstruct_opt

    return parse_opt, reconstruct_opt


def image_pixel_sha256(image: Image.Image) -> str:
    return sha256_bytes(image.convert("RGBA").tobytes())


def build_source_crop_map(source: Image.Image, records: Any) -> Image.Image:
    scale = 16
    legend_height = 100
    canvas = Image.new("RGBA", (source.width * scale, source.height * scale + legend_height), "white")
    canvas.alpha_composite(source.resize((source.width * scale, source.height * scale), Image.Resampling.NEAREST), (0, legend_height))

    colors = [(220, 60, 60, 255), (40, 160, 70, 255), (220, 170, 30, 255), (50, 100, 220, 255)]
    draw = ImageDraw.Draw(canvas)
    for index, record in enumerate(records):
        color = colors[index % len(colors)]
        left = record.source_x * scale
        top = legend_height + record.source_y * scale
        right = (record.source_x + record.width) * scale - 1
        bottom = legend_height + (record.source_y + record.height) * scale - 1
        draw.rectangle((left, top, right, bottom), outline=color, width=3)
        draw.text((left + 3, top + 3), f"c{record.index}/p{record.part_index}", fill=color)
    draw.text((6, 8), "chair_00.png source crop map", fill=(0, 0, 0, 255))
    draw.text((6, 28), "c0/p0 = logical cell 0; c1/p0 + c1/p1 = composite cell 1; c2/p0 = logical cell 2", fill=(0, 0, 0, 255))
    draw.text((6, 48), "All rectangles are copied from the original PNG; no pixels are generated.", fill=(0, 0, 0, 255))
    return canvas


def validate_known_chip_references(archive: zipfile.ZipFile, reconstruct_opt: Any) -> dict[str, Any]:
    tested = 0
    exact = 0
    mismatches: list[str] = []
    for member in archive.namelist():
        if not member.startswith(ARCHIVE_PREFIX + "02_DERIVED_READY_IMAGES/opt_reconstructed/chip/"):
            continue
        if not member.endswith(".logical.png"):
            continue
        stem = Path(member).stem.removesuffix(".logical")
        png_member = ARCHIVE_PREFIX + f"01_GAME_PACKS/chip/{stem}.png"
        opt_member = ARCHIVE_PREFIX + f"01_GAME_PACKS/chip/{stem}.opt"
        if png_member not in archive.namelist() or opt_member not in archive.namelist():
            continue
        result = reconstruct_opt(
            archive.read(png_member),
            archive.read(opt_member),
            png_member,
            opt_member,
        )
        reference = Image.open(io.BytesIO(archive.read(member))).convert("RGBA")
        tested += 1
        if result.status == "pass" and result.image is not None and list(result.image.getdata()) == list(reference.getdata()):
            exact += 1
        else:
            mismatches.append(stem)
    return {
        "tested": tested,
        "exact_pixel_matches": exact,
        "mismatches": mismatches,
        "all_exact": tested > 0 and tested == exact and not mismatches,
    }


def validate_all_opt_payloads(archive: zipfile.ZipFile, parse_opt: Any) -> dict[str, Any]:
    tested = 0
    passed = 0
    failures: list[str] = []
    for member in archive.namelist():
        if not member.startswith(ARCHIVE_PREFIX + "01_GAME_PACKS/") or not member.endswith(".opt"):
            continue
        parsed = parse_opt(archive.read(member), member)
        tested += 1
        if parsed.status == "pass" and parsed.partial_tail_bytes == 0 and not parsed.errors:
            passed += 1
        else:
            failures.append(member.removeprefix(ARCHIVE_PREFIX))
    return {
        "tested": tested,
        "passed": passed,
        "failures": failures,
        "all_pass": tested > 0 and tested == passed and not failures,
    }


def build_audit() -> dict[str, Any]:
    if not ZIP_PATH.is_file():
        raise FileNotFoundError(ZIP_PATH)
    parse_opt, reconstruct_opt = load_codec()
    with zipfile.ZipFile(ZIP_PATH) as archive:
        png_member = ARCHIVE_PREFIX + "01_GAME_PACKS/chip/chair_00.png"
        opt_member = ARCHIVE_PREFIX + "01_GAME_PACKS/chip/chair_00.opt"
        seb_member = ARCHIVE_PREFIX + "01_GAME_PACKS/chip/chair_00.seb"
        png_raw = archive.read(png_member)
        opt_raw = archive.read(opt_member)
        seb_raw = archive.read(seb_member)
        parsed = parse_opt(opt_raw, opt_member)
        reconstruction = reconstruct_opt(png_raw, opt_raw, png_member, opt_member)
        if reconstruction.status != "pass" or reconstruction.image is None:
            raise ValueError(reconstruction.to_dict())
        known_reference_validation = validate_known_chip_references(archive, reconstruct_opt)
        all_opt_validation = validate_all_opt_payloads(archive, parse_opt)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    reconstruction.image.save(LOGICAL_OUTPUT)
    build_source_crop_map(Image.open(io.BytesIO(png_raw)).convert("RGBA"), parsed.records).save(SOURCE_CROP_MAP_OUTPUT)

    runtime_paths = {
        extension: ROOT / f"runtime/social-dev/assets/display-slice-01/01_GAME_PACKS/chip/chair_00.{extension}"
        for extension in ("png", "opt", "seb")
    }
    runtime_match = {
        extension: path.is_file() and path.read_bytes() == raw
        for extension, path, raw in (
            ("png", runtime_paths["png"], png_raw),
            ("opt", runtime_paths["opt"], opt_raw),
            ("seb", runtime_paths["seb"], seb_raw),
        )
    }

    without_dynamic: dict[str, Any] = {
        "schema_version": "social-dev-phase3a-chair-00-reconstruction-v1",
        "purpose": "Prove the exact chair_00 logical atlas from the original PNG/OPT bytes using the validated variable-piece OPT grammar.",
        "source": {
            "asset_zip_path": relative_path(ZIP_PATH),
            "asset_zip_sha256": sha256_bytes(ZIP_PATH.read_bytes()),
            "png_member": png_member.removeprefix(ARCHIVE_PREFIX),
            "png_sha256": sha256_bytes(png_raw),
            "opt_member": opt_member.removeprefix(ARCHIVE_PREFIX),
            "opt_sha256": sha256_bytes(opt_raw),
            "seb_member": seb_member.removeprefix(ARCHIVE_PREFIX),
            "seb_sha256": sha256_bytes(seb_raw),
            "source_bytes_changed": False,
        },
        "parser": {
            "grammar": "header(4) + per-cell piece_count(1) + piece descriptors(14 each)",
            "header": parsed.header.to_dict() if parsed.header else None,
            "cell_piece_counts": [cell.piece_count for cell in parsed.cells],
            "record_count": len(parsed.records),
            "partial_tail_bytes": parsed.partial_tail_bytes,
            "errors": list(parsed.errors),
            "records": [record.to_dict(parsed.header) for record in parsed.records] if parsed.header else [],
        },
        "reconstruction": {
            "status": reconstruction.status,
            "logical_size": list(reconstruction.logical_size or ()),
            "pixel_sha256": reconstruction.pixel_sha256,
            "output_path": relative_path(LOGICAL_OUTPUT),
            "source_crop_map_path": relative_path(SOURCE_CROP_MAP_OUTPUT),
            "source_crop_map_sha256": sha256_bytes(SOURCE_CROP_MAP_OUTPUT.read_bytes()),
            "game_frame_order_from_seb": [1, 0, 2],
            "issues": list(reconstruction.issues),
        },
        "validation": {
            "all_chip_opt_payloads": all_opt_validation,
            "known_chip_logical_references": known_reference_validation,
            "runtime_exact_source_match": runtime_match,
        },
        "decision": {
            "exact_source_reconstruction": True,
            "speculative_pixels_added": False,
            "donor_opt_coordinates_used": False,
            "runtime_promotion": all(runtime_match.values()),
        },
        "determinism": {"algorithm": "stable-json-sha256 excluding generated_at_utc and content_hash"},
    }
    content_hash = sha256_bytes(stable_json(without_dynamic).encode("utf-8"))
    return {
        **without_dynamic,
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "determinism": {**without_dynamic["determinism"], "content_hash": content_hash},
    }


def main() -> int:
    audit = build_audit()
    AUDIT_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    AUDIT_OUTPUT.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(
        json.dumps(
            {
                "status": audit["reconstruction"]["status"],
                "cell_piece_counts": audit["parser"]["cell_piece_counts"],
                "logical_pixel_sha256": audit["reconstruction"]["pixel_sha256"],
                "known_reference_matches": audit["validation"]["known_chip_logical_references"],
                "all_opt_payloads": audit["validation"]["all_chip_opt_payloads"],
                "runtime_promotion": audit["decision"]["runtime_promotion"],
                "audit_hash": audit["determinism"]["content_hash"],
                "output_path": relative_path(LOGICAL_OUTPUT),
                "audit_path": relative_path(AUDIT_OUTPUT),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
