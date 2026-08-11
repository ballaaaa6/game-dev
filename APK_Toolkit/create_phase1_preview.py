#!/usr/bin/env python3
"""Render derived Phase 1 office previews from the frozen PNG assets.

The preview is a visual inventory aid.  It crops the visible room area for
display, labels source files and dimensions, and deliberately does not draw a
guessed grid, pivot, collision mask, or furniture placement.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from phase_paths import phase_artifacts_dir, phase_docs_dir


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def fit_image(image: Any, box: tuple[int, int], background: tuple[int, int, int, int]) -> Any:
    from PIL import Image

    image = image.convert("RGBA")
    image.thumbnail(box, Image.Resampling.NEAREST)
    canvas = Image.new("RGBA", box, background)
    x = (box[0] - image.width) // 2
    y = (box[1] - image.height) // 2
    canvas.alpha_composite(image, (x, y))
    return canvas


def text(draw: Any, xy: tuple[int, int], value: str, fill: tuple[int, int, int, int] = (235, 240, 250, 255)) -> None:
    draw.text(xy, value, fill=fill)


def create_office_preview(workspace: Path, output: Path) -> dict[str, Any]:
    from PIL import Image, ImageDraw

    root = workspace / "game-dev-story-mod_Sprites" / "office"
    artifacts = phase_artifacts_dir(workspace, 1)
    catalog = load_json(artifacts / "phase1_asset_catalog.json")
    manifest = load_json(artifacts / "office_manifest.json")
    by_rel = {item["source"]["relative_path"]: item for item in catalog.get("files", [])}

    room_rel = "office/floor0.png"
    room_path = workspace / "game-dev-story-mod_Sprites" / room_rel
    room = Image.open(room_path).convert("RGBA")
    visible_room = room.crop((0, 0, min(600, room.width), min(600, room.height)))
    canvas = Image.new("RGBA", (1240, 840), (18, 24, 36, 255))
    draw = ImageDraw.Draw(canvas)
    text(draw, (24, 18), "Phase 1 Office Preview — source-backed visual inventory", (255, 255, 255, 255))
    text(draw, (24, 42), "No guessed grid / pivot / collision / seat overlay", (170, 190, 215, 255))

    room_panel = fit_image(visible_room, (650, 650), (42, 48, 62, 255))
    canvas.alpha_composite(room_panel, (24, 78))
    draw.rectangle((24, 78, 674, 728), outline=(120, 145, 180, 255), width=2)
    room_dims = by_rel.get(room_rel, {}).get("dimensions") or {"width": room.width, "height": room.height}
    text(draw, (40, 742), f"{room_rel}  {room_dims.get('width')}×{room_dims.get('height')} (visible crop 600×600)")
    text(draw, (40, 766), "Catalog role: room_background_atlas; runtime placement: unknown")

    panel_x = 710
    text(draw, (panel_x, 88), "Furniture atlas samples", (255, 255, 255, 255))
    samples = [
        ("chair", "office/chair_000.png"),
        ("desk", "office/desk_000.png"),
        ("pc", "office/pc_000.png"),
        ("reception", "office/reception_000.png"),
    ]
    y = 120
    for label, rel in samples:
        path = workspace / "game-dev-story-mod_Sprites" / rel
        image = Image.open(path)
        tile = fit_image(image, (220, 120), (42, 48, 62, 255))
        canvas.alpha_composite(tile, (panel_x, y))
        draw.rectangle((panel_x, y, panel_x + 220, y + 120), outline=(100, 120, 150, 255), width=1)
        dims = by_rel.get(rel, {}).get("dimensions") or {"width": image.width, "height": image.height}
        text(draw, (panel_x + 235, y + 12), label, (255, 255, 255, 255))
        text(draw, (panel_x + 235, y + 36), rel.split("/", 1)[1], (190, 205, 225, 255))
        text(draw, (panel_x + 235, y + 60), f"{dims.get('width')}×{dims.get('height')}", (190, 205, 225, 255))
        text(draw, (panel_x + 235, y + 84), "placement: unknown", (235, 190, 145, 255))
        y += 142

    text(draw, (panel_x, 708), f"Office manifest: {manifest['summary']['office_png']} PNG / {manifest['summary']['office_seb']} SEB", (190, 205, 225, 255))
    text(draw, (panel_x, 732), "DrawChair / DrawDesk / DrawReception API shapes traced; values remain source-dependent.", (190, 205, 225, 255))
    text(draw, (panel_x, 756), "See Phase1/artifacts code trace and office manifest for confidence labels.", (190, 205, 225, 255))

    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(output, "PNG")
    return {
        "path": output.relative_to(workspace).as_posix(),
        "source_room": room_rel,
        "source_samples": [rel for _, rel in samples],
        "notes": [
            "Room display uses a 600x600 crop of the top visible area from floor0.png; source PNG remains unchanged.",
            "No guessed grid, pivot, collision, seat, or furniture placement is drawn.",
        ],
    }


def create_floor_contact_sheet(workspace: Path, output: Path) -> dict[str, Any]:
    from PIL import Image, ImageDraw

    root = workspace / "game-dev-story-mod_Sprites" / "office"
    floor_paths = sorted(root.glob("floor*.png"))
    cell_w, cell_h = 260, 230
    columns = 5
    rows = (len(floor_paths) + columns - 1) // columns
    sheet = Image.new("RGBA", (columns * cell_w, rows * cell_h), (18, 24, 36, 255))
    draw = ImageDraw.Draw(sheet)
    for index, path in enumerate(floor_paths):
        x = (index % columns) * cell_w
        y = (index // columns) * cell_h
        image = Image.open(path).convert("RGBA").crop((0, 0, min(600, Image.open(path).width), min(600, Image.open(path).height)))
        tile = fit_image(image, (240, 190), (42, 48, 62, 255))
        sheet.alpha_composite(tile, (x + 10, y + 8))
        draw.rectangle((x + 10, y + 8, x + 250, y + 198), outline=(100, 120, 150, 255), width=1)
        text(draw, (x + 12, y + 204), f"{path.name}  visible crop 600×600")
    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.convert("RGB").save(output, "PNG")
    return {
        "path": output.relative_to(workspace).as_posix(),
        "source_count": len(floor_paths),
        "notes": ["Each tile is a visual crop only; no runtime coordinates or grid are implied."],
    }


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--workspace",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="workspace root containing Phase 1 artifacts",
    )
    parser.add_argument("--preview", type=Path, default=None)
    parser.add_argument("--contact-sheet", type=Path, default=None)
    args = parser.parse_args(list(argv) if argv is not None else None)
    workspace = args.workspace.expanduser().resolve()
    preview = (args.preview or (phase_docs_dir(workspace, 1) / "phase1_office_preview.png")).expanduser()
    contact = (args.contact_sheet or (phase_docs_dir(workspace, 1) / "phase1_office_floor_contact_sheet.png")).expanduser()
    if not preview.is_absolute():
        preview = workspace / preview
    if not contact.is_absolute():
        contact = workspace / contact
    try:
        preview_info = create_office_preview(workspace, preview)
        contact_info = create_floor_contact_sheet(workspace, contact)
        manifest = {
            "schema": 1,
            "generated_at_utc": utc_now(),
            "phase": "phase1",
            "source_policy": "Derived visual previews only; source PNGs are unchanged.",
            "previews": [preview_info, contact_info],
        }
        manifest_path = phase_artifacts_dir(workspace, 1) / "phase1_preview_manifest.json"
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    except Exception as exc:
        print(f"[ERROR] Phase 1 preview creation failed: {exc}", file=sys.stderr)
        return 1
    print(f"[OK] Office preview: {preview_info['path']}")
    print(f"[OK] Floor contact sheet: {contact_info['path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
