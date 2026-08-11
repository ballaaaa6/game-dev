#!/usr/bin/env python3
"""Extract a compact, line-addressable renderer trace for Phase 1.

This is deliberately a source-evidence index, not a decompiler rewrite.  It
records function ranges, direct call sites, and the small set of geometry
claims that can be read from the current C export.  Unknown field names and
unresolved semantics remain explicit.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from phase_paths import phase_artifacts_dir


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8", errors="replace").splitlines()


def find_function_range(lines: list[str], function_name: str) -> tuple[int | None, int | None]:
    marker = f"// Function: {function_name}"
    start: int | None = None
    for index, line in enumerate(lines):
        if marker in line:
            start = index + 1
            break
    if start is None:
        return None, None
    # Function sections are separated by a banner before the next
    # ``// Function:`` marker.  Looking for the next marker keeps the whole
    # body, including nested labels and blank lines, in the range.
    end = len(lines)
    for index in range(start, len(lines)):
        if lines[index].startswith("// Function:"):
            end = index
            break
    return start, end


def find_line(lines: list[str], pattern: str, start: int = 0) -> int | None:
    compiled = re.compile(pattern)
    for index in range(start, len(lines)):
        if compiled.search(lines[index]):
            return index + 1
    return None


def call_sites(lines: list[str], function_name: str) -> list[dict[str, Any]]:
    pattern = re.compile(rf"\b{re.escape(function_name)}\b")
    sites: list[dict[str, Any]] = []
    for index, line in enumerate(lines):
        if pattern.search(line):
            sites.append({"line": index + 1, "text": line.strip()})
    return sites


def function_record(path: Path, lines: list[str], name: str) -> dict[str, Any]:
    start, end = find_function_range(lines, name)
    record: dict[str, Any] = {
        "name": name,
        "path": path.as_posix(),
        "start_line": start,
        "end_line": end,
        "confidence": "verified" if start is not None else "unknown",
    }
    if start is not None and end is not None:
        record["sha256"] = hashlib.sha256("\n".join(lines[start - 1 : end]).encode()).hexdigest()
    return record


def build_trace(workspace: Path, generated_at: str) -> dict[str, Any]:
    dumped_root = workspace / "game-dev-story-mod_Dumped" / "Categorized_Code" / "Global"
    form_path = dumped_root / "form.c"
    kairo_path = dumped_root / "kairo.c"
    method_path = dumped_root / "Method.c"
    form_lines = read_lines(form_path)
    kairo_lines = read_lines(kairo_path)
    method_lines = read_lines(method_path)

    function_names = [
        "form_GameForm__SetScale",
        "form_GameForm__GetGameWidth",
        "form_GameForm__GetGameHeight",
        "form_GameForm__DrawObj",
        "form_GameForm__DrawFloorCover",
        "form_GameForm__GetDeskImgData",
        "form_GameForm__GetChairImgData",
        "form_GameForm__DrawChair",
        "form_GameForm__DrawDesk",
        "form_GameForm__DrawCeoDesk",
        "form_GameForm__DrawReception",
        "form_GameForm__SetOrigin",
        "form_GameForm__LoadBihinImage",
        "form_GameForm___cctor",
    ]
    functions = [function_record(form_path, form_lines, name) for name in function_names]
    for function in functions:
        function["path"] = form_path.relative_to(workspace).as_posix()

    evidence: list[dict[str, Any]] = []

    def add(
        evidence_id: str,
        claim: str,
        confidence: str,
        path: Path,
        pattern: str,
        *,
        note: str | None = None,
        scope: str | None = None,
    ) -> None:
        lines = form_lines if path == form_path else kairo_lines if path == kairo_path else method_lines
        search_start = 0
        search_end = len(lines)
        if scope and path == form_path:
            scoped_start, scoped_end = find_function_range(lines, scope)
            if scoped_start is not None:
                search_start = scoped_start - 1
            if scoped_end is not None:
                search_end = scoped_end
        line = find_line(lines[:search_end], pattern, search_start)
        entry: dict[str, Any] = {
            "id": evidence_id,
            "claim": claim,
            "confidence": confidence,
            "source": {"path": path.relative_to(workspace).as_posix(), "line": line},
        }
        if note:
            entry["note"] = note
        if line is None:
            entry["confidence"] = "unknown"
            entry["note"] = (entry.get("note", "") + " pattern not found").strip()
        evidence.append(entry)

    add(
        "drawobj_dispatches_human",
        "DrawObj contains a direct branch that calls DrawHuman with computed integer coordinates.",
        "verified",
        form_path,
        r"form_GameForm__DrawHuman\s*$",
        note="The surrounding expression combines two AppData array values; the decompiler does not name their semantic axes.",
        scope="form_GameForm__DrawObj",
    )
    add(
        "drawobj_dispatches_chair",
        "DrawObj dispatches object rendering to DrawChair.",
        "verified",
        form_path,
        r"form_GameForm__DrawChair\(lVar15,param_2\)",
        scope="form_GameForm__DrawObj",
    )
    add(
        "drawobj_dispatches_desk",
        "DrawObj dispatches object rendering to DrawDesk.",
        "verified",
        form_path,
        r"form_GameForm__DrawDesk\(lVar15,param_2\)",
        scope="form_GameForm__DrawObj",
    )
    add(
        "drawobj_dispatches_ceo_desk",
        "DrawObj has a distinct DrawCeoDesk branch.",
        "verified",
        form_path,
        r"form_GameForm__DrawCeoDesk\(lVar15,param_2\)",
        scope="form_GameForm__DrawObj",
    )
    add(
        "drawobj_dispatches_reception",
        "DrawObj dispatches reception rendering with computed x/y plus source-rectangle arguments.",
        "verified",
        form_path,
        r"form_GameForm__DrawReception",
        scope="form_GameForm__DrawObj",
    )
    add(
        "drawobj_sort_comparison",
        "DrawObj performs an ordering comparison over two AppData-backed integer arrays before swapping entries.",
        "verified",
        form_path,
        r"lVar23 \+ \(long\)",
        note="Ordering behavior is verified; the field meaning (for example y/depth) remains unknown.",
        scope="form_GameForm__DrawObj",
    )
    add(
        "floor_cover_source_rect",
        "DrawFloorCover selects an entry from an AppData array at offset +0x78 and passes its x/y/w/h fields to DrawImage with caller offsets.",
        "verified",
        form_path,
        r"\*\(long \*\)\(lVar6 \+ 0x78\)",
        scope="form_GameForm__DrawFloorCover",
    )
    add(
        "chair_image_source",
        "DrawChair reads the furniture image list at AppData +0x1110 and uses its +0x28 image slot with caller source rectangle fields.",
        "verified",
        form_path,
        r"\*\(undefined8 \*\)\(lVar2 \+ 0x28\)",
        scope="form_GameForm__DrawChair",
    )
    add(
        "desk_image_source",
        "DrawDesk reads the furniture image list at AppData +0x1110 and uses its +0x30 image slot.",
        "verified",
        form_path,
        r"\*\(undefined8 \*\)\(lVar2 \+ 0x30\)",
        scope="form_GameForm__DrawDesk",
    )
    add(
        "reception_image_source",
        "DrawReception reads the reception image at AppData +0x1128 and uses caller source rectangle fields.",
        "verified",
        form_path,
        r"\+ 0x1128\)",
        scope="form_GameForm__DrawReception",
    )
    add(
        "desk_index_lookup",
        "GetDeskImgData maps an integer index by quotient/remainder into an AppData array at +0x488.",
        "verified",
        form_path,
        r"\+ 0x488\)",
        scope="form_GameForm__GetDeskImgData",
    )
    add(
        "chair_index_lookup",
        "GetChairImgData maps an integer index by quotient/remainder into an AppData array at +0x490.",
        "verified",
        form_path,
        r"\+ 0x490\)",
        scope="form_GameForm__GetChairImgData",
    )
    add(
        "scale_clamp",
        "SetScale clamps the requested scale through GetScaleRange/AppData Clamp and stores the result at GameForm +0x108.",
        "verified",
        form_path,
        r"main_AppData__Clamp",
        scope="form_GameForm__SetScale",
    )
    add(
        "game_width_formula",
        "GetGameWidth derives a scaled width from surface_GameView.GetGameWidth and the stored scale.",
        "verified",
        form_path,
        r"surface_GameView__GetGameWidth",
        scope="form_GameForm__GetGameWidth",
    )
    add(
        "game_height_formula",
        "GetGameHeight derives a scaled height from surface_GameView.GetGameHeight and subtracts the decompiled constant 0x898 before division.",
        "verified",
        form_path,
        r"\* 100 \+ -0x898",
        scope="form_GameForm__GetGameHeight",
    )
    add(
        "setorigin_empty_export",
        "The exported form_GameForm__SetOrigin body is an empty return.",
        "verified",
        form_path,
        r"return;",
        note="This does not prove that every origin operation is a no-op; another overload or renderer may own the actual transform.",
        scope="form_GameForm__SetOrigin",
    )
    add(
        "bihin_image_loading",
        "LoadBihinImage builds image names from AppData name entries plus a suffix and stores loaded images in the furniture image container.",
        "verified",
        form_path,
        r"main_AppData__GetImage",
        scope="form_GameForm__LoadBihinImage",
    )
    add(
        "seb_eof_behavior",
        "The shared StreamUtil.Read loop raises EOFException when a requested read returns fewer bytes.",
        "verified",
        method_path,
        r"java_io_EOFException___ctor",
        note="This supports treating the four-byte SEB tail shortfall as extraction/source evidence, not a safe zero-fill.",
    )

    unresolved = [
        {
            "id": "grid_contract",
            "claim": "A tile grid, A*, or fixed furniture footprint is not established by this trace.",
            "confidence": "unknown",
            "reason": "No direct occupancy/pathfinding/seat contract was identified in the selected renderer entry points.",
        },
        {
            "id": "collision_contract",
            "claim": "Collision, walkable, seat, and interaction zones remain unverified.",
            "confidence": "unknown",
            "reason": "The selected draw functions consume arrays and image data but do not name a collision schema.",
        },
        {
            "id": "depth_field_semantics",
            "claim": "The sort key used by DrawObj is not named as y/depth/z by the decompiler.",
            "confidence": "unknown",
            "reason": "The compare-and-swap pattern is visible, but array offsets are not recovered field names.",
        },
    ]

    callsite_targets = [
        "form_GameForm__DrawFloorCover",
        "form_GameForm__DrawObj",
        "form_GameForm__DrawHuman",
        "form_GameForm__DrawDesk",
        "form_GameForm__DrawChair",
        "form_GameForm__DrawReception",
        "form_GameForm__SetOrigin",
        "form_GameForm__SetScale",
    ]
    callsite_index = {
        target: call_sites(form_lines, target)
        for target in callsite_targets
    }
    return {
        "schema": 1,
        "generated_at_utc": generated_at,
        "phase": "phase1",
        "source_policy": "Read-only decompiled sources; claims retain line-addressable evidence and confidence.",
        "functions": functions,
        "call_sites": callsite_index,
        "evidence": evidence,
        "unresolved": unresolved,
        "summary": {
            "functions_indexed": sum(1 for item in functions if item.get("start_line")),
            "evidence_verified": sum(1 for item in evidence if item["confidence"] == "verified"),
            "evidence_unknown": sum(1 for item in evidence if item["confidence"] == "unknown"),
            "unresolved_contracts": len(unresolved),
        },
        "source_files": [
            {
                "path": path.relative_to(workspace).as_posix(),
                "sha256": sha256_file(path),
                "line_count": len(lines),
            }
            for path, lines in ((form_path, form_lines), (kairo_path, kairo_lines), (method_path, method_lines))
        ],
    }


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--workspace",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="workspace root containing game-dev-story-mod_Dumped",
    )
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args(list(argv) if argv is not None else None)
    workspace = args.workspace.expanduser().resolve()
    output = (args.output or (phase_artifacts_dir(workspace, 1) / "phase1_code_trace.json")).expanduser()
    if not output.is_absolute():
        output = workspace / output
    output.parent.mkdir(parents=True, exist_ok=True)
    try:
        payload = build_trace(workspace, utc_now())
        output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    except Exception as exc:
        print(f"[ERROR] Phase 1 code trace failed: {exc}", file=sys.stderr)
        return 1
    print(
        f"[OK] Indexed {payload['summary']['functions_indexed']} functions and "
        f"{payload['summary']['evidence_verified']} verified evidence claims."
    )
    print(f"[INFO] Unknown contracts retained: {payload['summary']['unresolved_contracts']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
