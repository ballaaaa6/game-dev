#!/usr/bin/env python3
"""Build the evidence-first Phase 2 character and animation catalog.

The generator reads the frozen extraction roots and writes every generated
artifact below Phases/Phase2.  It intentionally keeps semantic animation
labels empty unless the current dump/code provides a direct connection.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

from PIL import Image, ImageDraw, ImageFont


SCHEMA = "phase2"
ALLOWED_CONFIDENCE = ["verified", "probable", "unknown", "verified-record-only"]
ROOT = Path(__file__).resolve().parents[3]
PHASE = ROOT / "Phases" / "Phase2"
ARTIFACTS = PHASE / "artifacts"
PREVIEW = ARTIFACTS / "preview"
SPRITES = ROOT / "game-dev-story-mod_Sprites"
GAME = SPRITES / "game"
DUMP = ROOT / "game-dev-story-mod_Dumped"
CODE = DUMP / "Categorized_Code"
BODYFACE = DUMP / "bodyface_records.reference.json"
IMG_INF = GAME / "img.inf"
FORM_C = CODE / "Global" / "form.c"
DUMP_CS = DUMP / "dump.cs"
SCRIPT_JSON = DUMP / "script.json"


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, sort_keys=False) + "\n", encoding="utf-8")


def parse_int(value: str) -> int | None:
    value = value.strip()
    value = re.sub(r"^\([^)]*\)\s*", "", value)
    value = re.sub(r"(?i)(?<=\d)[ul]+$", "", value)
    if not re.fullmatch(r"-?(?:0[xX][0-9a-fA-F]+|\d+)", value):
        return None
    return int(value, 0)


def split_args(value: str) -> list[str]:
    result: list[str] = []
    current: list[str] = []
    depth = 0
    for char in value:
        if char == "(":
            depth += 1
        elif char == ")":
            depth = max(depth - 1, 0)
        if char == "," and depth == 0:
            result.append("".join(current).strip())
            current = []
        else:
            current.append(char)
    if current or value:
        result.append("".join(current).strip())
    return result


def load_records() -> list[dict[str, Any]]:
    value = json.loads(BODYFACE.read_text(encoding="utf-8-sig"))
    if not isinstance(value, list):
        raise ValueError("bodyface reference must be a JSON list")
    return value


def parse_img_inf() -> dict[str, int]:
    mapping: dict[str, int] = {}
    if not IMG_INF.exists():
        return mapping
    for line in IMG_INF.read_text(encoding="utf-8", errors="replace").splitlines():
        match = re.match(r"\s*(\d+)\s+(.+?)\s*$", line)
        if match:
            mapping[match.group(2)] = int(match.group(1))
    return mapping


def image_info(path: Path) -> dict[str, Any]:
    with Image.open(path) as image:
        rgba = image.convert("RGBA")
        alpha = rgba.getchannel("A")
        bbox = alpha.getbbox()
        return {
            "dimensions": {"width": image.width, "height": image.height},
            "mode": image.mode,
            "format": image.format,
            "nontransparent_bbox": list(bbox) if bbox else None,
            "palette_transparency": image.info.get("transparency"),
        }


def asset_files() -> list[tuple[str, int, Path]]:
    result: list[tuple[str, int, Path]] = []
    for path in GAME.glob("body*.png"):
        match = re.fullmatch(r"body(\d+)\.png", path.name)
        if match:
            result.append(("body", int(match.group(1)), path))
    for path in GAME.glob("face_*.png"):
        match = re.fullmatch(r"face_(\d+)\.png", path.name)
        if match:
            result.append(("face", int(match.group(1)), path))
    return sorted(result, key=lambda item: (item[0], item[1]))


def rect_from(record: dict[str, Any], prefix: str) -> dict[str, int]:
    return {
        "x": record[f"{prefix}_src_x"],
        "y": record[f"{prefix}_src_y"],
        "width": record[f"{prefix}_width"],
        "height": record[f"{prefix}_height"],
    }


def fits(rect: dict[str, int], dimensions: dict[str, int]) -> bool:
    return (
        rect["x"] >= 0
        and rect["y"] >= 0
        and rect["width"] > 0
        and rect["height"] > 0
        and rect["x"] + rect["width"] <= dimensions["width"]
        and rect["y"] + rect["height"] <= dimensions["height"]
    )


def find_line(path: Path, pattern: str) -> int | None:
    expression = re.compile(pattern, re.IGNORECASE)
    for number, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        if expression.search(line):
            return number
    return None


def find_function_header_line(path: Path, name: str) -> int | None:
    expression = re.compile(r"^// Function:\s*" + re.escape(name) + r"\s*$", re.IGNORECASE)
    for number, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        if expression.search(line):
            return number
    return None


def find_function_header_lines(path: Path, name: str) -> list[int]:
    expression = re.compile(r"^// Function:\s*" + re.escape(name) + r"\s*$", re.IGNORECASE)
    return [number for number, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1) if expression.search(line)]


def dump_class_evidence() -> dict[str, Any]:
    lines = DUMP_CS.read_text(encoding="utf-8", errors="replace").splitlines()
    start = next((i for i, line in enumerate(lines) if line.startswith("public class GameForm :")), None)
    if start is None:
        return {"class": None, "fields": [], "methods": []}
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("public class ") and i > start), len(lines))
    wanted_fields = {
        "DebugBodyMax", "DebugFaceMax", "BodyFaceMax", "BodyFace", "HumanDexFaceG",
        "HumanDexBodyG", "HumanDexMode", "HumanDexAnime", "HumanDexWalk", "SyainFaceG", "SyainBodyG",
        "KaiwaFaceG", "KaiwaBodyG", "KeyAnimeT", "ObjecAnime", "IMG_LIST", "imgFace", "imgBody",
    }
    fields = []
    for index in range(start, end):
        line = lines[index]
        match = re.search(r"\b(?:public|private|internal|protected)\s+(?:static\s+)?(?:readonly\s+)?[^;]+\s+(\w+)\s*;", line)
        if match and match.group(1) in wanted_fields:
            fields.append({"name": match.group(1), "declaration": line.strip(), "line": index + 1})
    methods = []
    wanted_methods = {"AddBodyFace", "DrawHuman", "DrawFukidashi", "GetTalkIndex", "GetHumanTalkName", "DrawDesk", "DrawChair"}
    for index in range(start, end):
        line = lines[index]
        match = re.search(r"(?:public|private|internal|protected).*\b(\w+)\s*\(", line)
        if match and match.group(1) in wanted_methods:
            rva = None
            for back in range(max(start, index - 3), index):
                rva_match = re.search(r"RVA:\s*0x([0-9A-Fa-f]+)", lines[back])
                if rva_match:
                    rva = "0x" + rva_match.group(1).lower()
            methods.append({"name": match.group(1), "signature": line.strip(), "rva": rva, "line": index + 1})
    return {"class": "form.GameForm", "fields": fields, "methods": methods}


def script_methods() -> list[dict[str, Any]]:
    if not SCRIPT_JSON.exists():
        return []
    data = json.loads(SCRIPT_JSON.read_text(encoding="utf-8-sig"))
    result = []
    for row in data.get("ScriptMethod", []):
        name = row.get("Name", "")
        if name.startswith("form.GameForm$$") and any(token.lower() in name.lower() for token in ("Body", "Face", "Human", "Talk", "Draw", "Anime", "Walk", "Work", "Rest", "Sit")):
            result.append(row)
    return sorted(result, key=lambda row: (row.get("Name", ""), row.get("Address", 0)))


def draw_human_calls() -> list[dict[str, Any]]:
    lines = FORM_C.read_text(encoding="utf-8", errors="replace").splitlines()
    calls: list[dict[str, Any]] = []
    current_function = None
    current_address = None
    for line_no, line in enumerate(lines, 1):
        function_match = re.search(r"// Function:\s*(.+)$", line)
        if function_match:
            current_function = function_match.group(1).strip()
        address_match = re.search(r"// Address:\s*(0x)?([0-9A-Fa-f]+)", line)
        if address_match:
            current_address = "0x" + address_match.group(2).lower()
        if "form_GameForm__DrawHuman" not in line or "void form_GameForm__DrawHuman" in line:
            continue
        if current_function == "form_GameForm__DrawHuman":
            continue
        start = line.find("form_GameForm__DrawHuman") + len("form_GameForm__DrawHuman")
        call_text = line[start:]
        paren_depth = call_text.count("(") - call_text.count(")")
        while (";" not in call_text or paren_depth > 0) and line_no < len(lines):
            line_no += 1
            call_text += " " + lines[line_no - 1].strip()
            paren_depth += lines[line_no - 1].count("(") - lines[line_no - 1].count(")")
        match = re.search(r"\((.*)\)\s*;", call_text, re.DOTALL)
        if not match:
            continue
        args = split_args(match.group(1))
        if len(args) < 7:
            continue
        # Decompiler call shape: self, graphics, X, Y, TFace, TBody, TMode[, TKage].
        selectors = {}
        for name, index in (("TFace", 4), ("TBody", 5), ("TMode", 6), ("TKage", 7)):
            if len(args) > index:
                selectors[name] = {"raw": args[index], "literal": parse_int(args[index])}
        calls.append({
            "source": rel(FORM_C),
            "line": line_no,
            "function": current_function,
            "function_address": current_address,
            "raw_args": args,
            "selectors": selectors,
        })
    return calls


def code_trace(records: list[dict[str, Any]]) -> dict[str, Any]:
    calls = draw_human_calls()
    face_refs = sorted({item["selectors"]["TFace"]["literal"] for item in calls if item["selectors"].get("TFace", {}).get("literal") is not None})
    body_refs = sorted({item["selectors"]["TBody"]["literal"] for item in calls if item["selectors"].get("TBody", {}).get("literal") is not None})
    mode_refs = sorted({item["selectors"]["TMode"]["literal"] for item in calls if item["selectors"].get("TMode", {}).get("literal") is not None})
    required = dump_class_evidence()
    for method in required["methods"]:
        method["source_dump"] = rel(DUMP_CS)
    for field in required["fields"]:
        field["source_dump"] = rel(DUMP_CS)
    direct_lines = {}
    for label, pattern in {
        "AddBodyFace": r"form_GameForm__AddBodyFace",
        "DrawHuman": r"form_GameForm__DrawHuman",
        "DrawFukidashi": r"form_GameForm__DrawFukidashi",
        "GetTalkIndex": r"form_GameForm__GetTalkIndex",
        "GetHumanTalkName": r"form_GameForm__GetHumanTalkName",
    }.items():
        header_lines = find_function_header_lines(FORM_C, f"form_GameForm__{label}")
        direct_lines[label] = {
            "source": rel(FORM_C),
            "function_header_line": header_lines[-1] if header_lines else None,
            "function_header_lines": header_lines,
            "first_symbol_line": find_line(FORM_C, pattern),
        }
    field_names = {field["name"] for field in required["fields"]}
    related_tokens = ["HumanDexAnime", "HumanDexWalk", "HumanDexMode", "KaiwaFaceG", "KaiwaBodyG", "DrawFukidashi"]
    token_hits = {
        token: {
            "dump_source": rel(DUMP_CS),
            "dump_first_line": find_line(DUMP_CS, re.escape(token)),
            "categorized_code_source": rel(FORM_C),
            "categorized_code_first_line": find_line(FORM_C, re.escape(token)),
        }
        for token in related_tokens
    }
    draw_human_text = FORM_C.read_text(encoding="utf-8", errors="replace").splitlines()
    table_access_lines = [number for number, line in enumerate(draw_human_text, 1) if "uVar11 = (uint)param_7" in line]
    table_access_lines.extend(number for number, line in enumerate(draw_human_text, 1) if "0x128" in line and 41000 <= number <= 41600)
    table_access_lines = sorted(set(table_access_lines))
    human_dex_call = next(
        (
            call for call in calls
            if call["function"] == "form_GameForm___draw"
            and call["selectors"].get("TFace", {}).get("raw", "").find("lVar26") >= 0
            and call["selectors"].get("TBody", {}).get("raw", "").find("lVar27") >= 0
            and call["selectors"].get("TMode", {}).get("raw", "").find("lVar17") >= 0
        ),
        None,
    )
    composition_contract = {
        "status": "verified_with_mode_dependent_branches",
        "selector_to_image_array": [
            {
                "layer": "body",
                "selector": "TBody",
                "image_array_field": "imgBody",
                "table_fields": {"destination_x": "BodyFace[mode][0]", "destination_y": "BodyFace[mode][1]", "source_x": "BodyFace[mode][2]", "source_y": "BodyFace[mode][3]", "width": "BodyFace[mode][4]", "height": "BodyFace[mode][5]"},
                "draw_sites": {"source": rel(FORM_C), "lines": [41288, 41300, 41401, 41413]},
                "confidence": "verified",
            },
            {
                "layer": "face",
                "selector": "TFace",
                "image_array_field": "imgFace",
                "table_fields": {"destination_x": "BodyFace[mode][6]", "destination_y": "BodyFace[mode][7]", "source_x": "BodyFace[mode][8]", "source_y": "BodyFace[mode][9]", "width": "BodyFace[mode][10]", "height": "BodyFace[mode][11]"},
                "draw_sites": {"source": rel(FORM_C), "lines": [41361, 41368, 41377, 41452, 41463, 41472]},
                "confidence": "verified",
                "note": "The recovered implementation applies additional mode-dependent offset adjustments in some branches; the table destination fields remain the base offsets.",
            },
        ],
        "add_body_face_parameter_map": {
            "source": rel(FORM_C),
            "function": "form_GameForm__AddBodyFace",
            "lines": [26582, 26587, 26592, 26597, 26602, 26607, 26613, 26619, 26625, 26631, 26638, 26644, 26650, 26656],
            "parameters": {
                "P0": "body_dst_x", "P1": "body_dst_y", "P2": "body_src_x", "P3": "body_src_y", "P4": "body_width", "P5": "body_height",
                "P6": "face_dst_x", "P7": "face_dst_y", "P8": "face_src_x", "P9": "face_src_y", "P10": "face_width", "P11": "face_height",
                "P12": "shadow_dst_x", "P13": "shadow_dst_y",
            },
            "confidence": "verified",
        },
        "shadow_fields": {
            "table_fields": {"x": "BodyFace[mode][12]", "y": "BodyFace[mode][13]"},
            "confidence": "verified-record-only",
            "note": "The table stores the two values, but this catalog does not promote a universal shadow rendering rule because DrawHuman has multiple branches and optional TKage behavior.",
        },
    }
    return {
        "schema": f"{SCHEMA}.code-trace.v1",
        "sources": [rel(DUMP_CS), rel(SCRIPT_JSON), rel(FORM_C), rel(BODYFACE)],
        "game_form_class": required,
        "script_methods": script_methods(),
        "draw_human_calls": calls,
        "draw_human_call_count": len(calls),
        "literal_selector_coverage": {
            "TFace_values": face_refs,
            "TBody_values": body_refs,
            "TMode_values": mode_refs,
            "dynamic_selector_calls": sum(1 for call in calls if any(value.get("literal") is None for value in call["selectors"].values())),
        },
        "function_evidence_lines": direct_lines,
        "related_token_hits": token_hits,
        "draw_human_bodyface_table_access_lines": table_access_lines,
        "composition_contract": composition_contract,
        "dynamic_selector_trace": {
            "human_dex_draw_call": {
                "callsite": human_dex_call,
                "argument_mapping": {
                    "X": "HumanDexX[index] / 10 - 8",
                    "Y": "HumanDexY[index] / 10 - 30",
                    "TFace": "HumanDexFaceG[index]",
                    "TBody": "HumanDexBodyG[index]",
                    "TMode": "HumanDexAnime[index]",
                    "TKage": "1",
                },
                "evidence": [{"source": rel(FORM_C), "lines": [19687, 19688, 19689, 19690, 19691], "function": "form_GameForm___draw"}],
                "confidence": "verified",
                "note": "This resolves one variable-driven DrawHuman path; it does not resolve every runtime callsite or assign semantic Agent states.",
            }
        },
        "interpretations": [
            {
                "fact": "DrawHuman parameter names are TFace, TBody, TMode in the current dump.",
                "meaning": "selector_parameter_names",
                "confidence": "verified",
                "evidence": [{"source": rel(DUMP_CS), "method": "DrawHuman", "line": next((m["line"] for m in required["methods"] if m["name"] == "DrawHuman"), None)}],
            },
            {
                "fact": "DrawHuman uses TMode to index the static BodyFace table in the recovered C.",
                "meaning": "TMode_is_bodyface_table_selector",
                "confidence": "verified-record-only",
                "evidence": [{"source": rel(FORM_C), "lines": table_access_lines, "note": "Recovered DrawHuman assigns TMode to uVar11 and accesses the BodyFace table at the GameForm static offset used by the implementation."}],
            },
            {
                "fact": "Literal DrawHuman calls expose only a subset of runtime selector values; many calls are variable-driven.",
                "meaning": "literal_callsite_coverage_is_partial",
                "confidence": "verified",
                "evidence": [{"source": rel(FORM_C), "line": call["line"]} for call in calls[:5]],
            },
            {
                "fact": "The recovered DrawHuman implementation selects imgBody by TBody and imgFace by TFace, then uses BodyFace[TMode] crop and destination fields.",
                "meaning": "body_face_composition_contract",
                "confidence": "verified",
                "evidence": [{"source": rel(DUMP_CS), "fields": ["imgFace", "imgBody", "BodyFace"]}, {"source": rel(FORM_C), "lines": [41288, 41300, 41361, 41368, 41377, 41401, 41413, 41452, 41463, 41472]}],
            },
            {
                "fact": "The HumanDex draw path passes HumanDexFaceG, HumanDexBodyG, and HumanDexAnime into DrawHuman.",
                "meaning": "human_dex_dynamic_selector_path",
                "confidence": "verified" if human_dex_call else "unknown",
                "evidence": [{"source": rel(FORM_C), "lines": [19687, 19688, 19689, 19690, 19691], "note": "Expected recovered draw path; parser result is included in dynamic_selector_trace."}],
            },
        ],
    }


def build_assets(records: list[dict[str, Any]], trace: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    inf = parse_img_inf()
    body_dims: dict[int, dict[str, int]] = {}
    face_dims: dict[int, dict[str, int]] = {}
    assets = []
    literal_faces = set(trace["literal_selector_coverage"]["TFace_values"])
    literal_bodies = set(trace["literal_selector_coverage"]["TBody_values"])
    for kind, number, path in asset_files():
        metadata = image_info(path)
        dims = metadata["dimensions"]
        if kind == "body":
            body_dims[number] = dims
        else:
            face_dims[number] = dims
        filename = path.name
        item = {
            "asset_id": f"{kind}_{number}",
            "asset_kind": kind,
            "numeric_id": number,
            "filename": filename,
            "source_path": rel(path),
            "file_size_bytes": path.stat().st_size,
            "sha256": sha256(path),
            **metadata,
            "img_inf_archive_id": inf.get(filename),
            "literal_DrawHuman_selector_reference": number in (literal_bodies if kind == "body" else literal_faces),
            "mapping_status": "asset_type_and_filename_verified",
            "confidence": "verified",
        }
        if kind == "body":
            item["special_case"] = "nonstandard_width" if dims["width"] != 102 else None
        assets.append(item)
    for asset in assets:
        kind = asset["asset_kind"]
        dimensions = asset["dimensions"]
        compatible = []
        for record in records:
            rect = rect_from(record, kind)
            if fits(rect, dimensions):
                compatible.append(record["mode"])
        asset["bodyface_crop_modes_that_fit"] = compatible
        asset["crop_coverage_status"] = "all_records_fit" if len(compatible) == len(records) else "partial_record_coverage"
    summary = {
        "body_asset_count": sum(1 for asset in assets if asset["asset_kind"] == "body"),
        "face_asset_count": sum(1 for asset in assets if asset["asset_kind"] == "face"),
        "body_dimensions": sorted({tuple(asset["dimensions"].values()) for asset in assets if asset["asset_kind"] == "body"}),
        "face_dimensions": sorted({tuple(asset["dimensions"].values()) for asset in assets if asset["asset_kind"] == "face"}),
        "body_assets_with_nonstandard_width": [asset["asset_id"] for asset in assets if asset["asset_kind"] == "body" and asset["dimensions"]["width"] != 102],
    }
    return assets, summary


def input_audit(records: list[dict[str, Any]], assets: list[dict[str, Any]], trace: dict[str, Any]) -> dict[str, Any]:
    body_assets = [asset for asset in assets if asset["asset_kind"] == "body"]
    face_assets = [asset for asset in assets if asset["asset_kind"] == "face"]
    body_ids = {asset["numeric_id"] for asset in body_assets}
    face_ids = {asset["numeric_id"] for asset in face_assets}
    body_refs = set(trace["literal_selector_coverage"]["TBody_values"])
    face_refs = set(trace["literal_selector_coverage"]["TFace_values"])
    missing = []
    for value in sorted(body_refs - body_ids):
        missing.append({"selector": "TBody", "numeric_id": value, "reason": "literal DrawHuman reference has no extracted body asset"})
    for value in sorted(face_refs - face_ids):
        missing.append({"selector": "TFace", "numeric_id": value, "reason": "literal DrawHuman reference has no extracted face asset"})
    source_files = [BODYFACE, FORM_C, DUMP_CS, SCRIPT_JSON, IMG_INF] + [GAME / asset["filename"] for asset in assets]
    source_manifest = []
    for path in sorted({path for path in source_files if path.exists()}, key=lambda p: rel(p)):
        source_manifest.append({"source_path": rel(path), "file_size_bytes": path.stat().st_size, "sha256": sha256(path)})
    raw_keys = list(records[0].keys()) if records else []
    duplicate_modes = [mode for mode, count in Counter(record.get("mode") for record in records).items() if count > 1]
    return {
        "schema": f"{SCHEMA}.input-audit.v1",
        "generator": rel(Path(__file__)),
        "canonical_source_roots": [rel(DUMP), rel(GAME), rel(CODE)],
        "source_manifest": source_manifest,
        "bodyface_baseline": {
            "source_path": rel(BODYFACE),
            "record_count": len(records),
            "mode_values": [record.get("mode") for record in records],
            "field_count": len(raw_keys),
            "fields": raw_keys,
            "duplicate_mode_values": duplicate_modes,
            "callsite_values": [record.get("callsite") for record in records],
        },
        "assets": assets,
        "assets_summary": {
            "total_character_assets": len(assets),
            "body_assets": len(body_assets),
            "face_assets": len(face_assets),
            "body_assets_with_literal_code_reference": sum(asset["literal_DrawHuman_selector_reference"] for asset in body_assets),
            "face_assets_with_literal_code_reference": sum(asset["literal_DrawHuman_selector_reference"] for asset in face_assets),
        },
        "missing_references": missing,
        "orphan_like_assets": {
            "body": [asset["asset_id"] for asset in body_assets if not asset["literal_DrawHuman_selector_reference"]],
            "face": [asset["asset_id"] for asset in face_assets if not asset["literal_DrawHuman_selector_reference"]],
            "interpretation": "No literal DrawHuman selector was found; variable-driven/runtime references may still select these assets.",
        },
        "unresolved_items": [
            "The reference records contain crop/offset data but no concrete TFace/TBody asset IDs.",
            "Variable-driven DrawHuman callsites cannot be resolved to numeric selectors from recovered C alone.",
            "Missing literal TFace IDs are retained as unresolved references; source assets are not synthesized.",
        ],
    }


def bodyface_analysis(records: list[dict[str, Any]], assets: list[dict[str, Any]]) -> dict[str, Any]:
    body_assets = [asset for asset in assets if asset["asset_kind"] == "body"]
    face_assets = [asset for asset in assets if asset["asset_kind"] == "face"]
    analyzed = []
    for record in records:
        body_rect = rect_from(record, "body")
        face_rect = rect_from(record, "face")
        body_fit = [asset["asset_id"] for asset in body_assets if record["mode"] in asset["bodyface_crop_modes_that_fit"]]
        face_fit = [asset["asset_id"] for asset in face_assets if record["mode"] in asset["bodyface_crop_modes_that_fit"]]
        analyzed.append({
            "mode": record["mode"],
            "raw_record": record,
            "callsite_hex": hex(record["callsite"]),
            "derived": {
                "body_source_rect": body_rect,
                "face_source_rect": face_rect,
                "body_destination_offset": {"x": record["body_dst_x"], "y": record["body_dst_y"]},
                "face_destination_offset": {"x": record["face_dst_x"], "y": record["face_dst_y"]},
                "shadow_destination": {"x": record["shadow_dst_x"], "y": record["shadow_dst_y"]},
                "body_assets_where_crop_fits": body_fit,
                "face_assets_where_crop_fits": face_fit,
                "body_fit_count": len(body_fit),
                "face_fit_count": len(face_fit),
            },
            "interpretation": {
                "mode": {"meaning": "BodyFace table selector used by DrawHuman TMode", "confidence": "verified-record-only"},
                "crop_and_destination_fields": {"meaning": "data-driven source rectangle and destination offset", "confidence": "verified-record-only"},
                "semantic_state": {"meaning": None, "confidence": "unknown"},
                "direction": {"meaning": None, "confidence": "unknown"},
                "timing": {"meaning": None, "confidence": "unknown"},
            },
            "evidence": [
                {"source": rel(BODYFACE), "record_mode": record["mode"], "callsite": hex(record["callsite"])},
                {"source": rel(DUMP_CS), "class": "form.GameForm", "field": "BodyFace"},
                {"source": rel(DUMP_CS), "method": "DrawHuman", "parameters": ["TFace", "TBody", "TMode"]},
            ],
        })
    ranges = {}
    for key in records[0].keys() if records else []:
        values = [record[key] for record in records]
        if all(isinstance(value, int) for value in values):
            ranges[key] = {"min": min(values), "max": max(values), "unique_count": len(set(values))}
    return {
        "schema": f"{SCHEMA}.bodyface-analysis.v1",
        "source": rel(BODYFACE),
        "record_count": len(records),
        "field_count": len(records[0]) if records else 0,
        "field_ranges": ranges,
        "records": analyzed,
        "summary": {
            "all_modes_have_unique_values": len({record["mode"] for record in records}) == len(records),
            "body_crop_fits_all_standard_bodies": sum(1 for record in analyzed if record["derived"]["body_fit_count"] == len(body_assets)),
            "body25_compatible_modes": [record["mode"] for record in analyzed if "body_25" in record["derived"]["body_assets_where_crop_fits"]],
            "face_crop_fits_all_faces": sum(1 for record in analyzed if record["derived"]["face_fit_count"] == len(face_assets)),
            "semantic_modes_verified": 0,
            "semantic_modes_unknown": len(records),
        },
        "unknowns": [
            "No record field is promoted to a legacy state, pose, direction, or timing label.",
            "A record's crop fitting multiple atlases does not prove which asset selector is used at runtime.",
            "The reference data does not include a concrete body ID or face ID per mode.",
        ],
    }


def character_manifest(records: list[dict[str, Any]], assets: list[dict[str, Any]], trace: dict[str, Any]) -> dict[str, Any]:
    body_assets = [asset for asset in assets if asset["asset_kind"] == "body"]
    face_assets = [asset for asset in assets if asset["asset_kind"] == "face"]
    modes = []
    for record in records:
        body_rect = rect_from(record, "body")
        face_rect = rect_from(record, "face")
        compatible_bodies = [asset["asset_id"] for asset in body_assets if record["mode"] in asset["bodyface_crop_modes_that_fit"]]
        compatible_faces = [asset["asset_id"] for asset in face_assets if record["mode"] in asset["bodyface_crop_modes_that_fit"]]
        modes.append({
            "mode_id": record["mode"],
            "semantic_label": None,
            "confidence": "verified-record-only",
            "body": {
                "runtime_selector_parameter": "TBody",
                "source_rect": body_rect,
                "destination_offset": {"x": record["body_dst_x"], "y": record["body_dst_y"]},
                "compatible_asset_ids_by_crop_geometry": compatible_bodies,
                "selected_asset_id": None,
            },
            "face": {
                "runtime_selector_parameter": "TFace",
                "source_rect": face_rect,
                "destination_offset": {"x": record["face_dst_x"], "y": record["face_dst_y"]},
                "compatible_asset_ids_by_crop_geometry": compatible_faces,
                "selected_asset_id": None,
            },
            "shadow": {
                "destination_offset": {"x": record["shadow_dst_x"], "y": record["shadow_dst_y"]},
                "source_asset_id": None,
                "rendered_by_catalog": False,
                "note": "The record has a shadow destination, but no shadow source asset/primitive is promoted here.",
            },
            "evidence": [{"source": rel(BODYFACE), "record_mode": record["mode"], "callsite": hex(record["callsite"])}],
            "unknowns": ["concrete TFace/TBody pair", "semantic state", "direction", "pivot/anchor", "timing"],
        })
    return {
        "schema": f"{SCHEMA}.character-manifest.v1",
        "composition_model": "original body atlas + original face atlas + BodyFace crop/offset record",
        "runtime_selector_contract": {
            "source_method": "form.GameForm.DrawHuman",
            "parameters": {"face": "TFace", "body": "TBody", "mode": "TMode", "optional_shadow": "TKage"},
            "confidence": "verified",
            "evidence": [{"source": rel(DUMP_CS), "class": "form.GameForm", "method": "DrawHuman"}],
        },
        "body_assets": [asset["asset_id"] for asset in body_assets],
        "face_assets": [asset["asset_id"] for asset in face_assets],
        "characters": [],
        "bodyface_mode_compositions": modes,
        "coverage": {
            "bodyface_mode_records": len(records),
            "mode_records_with_concrete_asset_pair": 0,
            "mode_records_with_verified_crop_geometry": len(records),
            "semantic_character_states_verified": 0,
        },
        "notes": [
            "The manifest is a traceable composition catalog, not a claim that every geometry-compatible asset pair is used by the original runtime.",
            "No replacement sprites, mirroring, shadow primitives, or guessed offsets are introduced.",
        ],
    }


def mechanical_groups(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[int, int], list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        grouped[(record["body_src_y"], record["face_src_y"])].append(record)
    result = []
    for index, (key, group) in enumerate(sorted(grouped.items(), key=lambda item: (item[0][0], item[0][1], item[1][0]["mode"]))):
        ordered = sorted(group, key=lambda record: record["mode"])
        result.append({
            "animation_id": f"mechanical_group_{index:03d}",
            "semantic_label": None,
            "candidate": True,
            "confidence": "unknown",
            "group_basis": "same body source y and face source y in BodyFace records",
            "body_source_y": key[0],
            "face_source_y": key[1],
            "mode_sequence_candidate": [record["mode"] for record in ordered],
            "frame_timing_ms": None,
            "loop_mode": None,
            "direction": None,
            "mirroring": None,
            "evidence": [{"source": rel(BODYFACE), "record_modes": [record["mode"] for record in ordered]}],
            "unknowns": ["whether records are time-ordered frames", "direction", "timing", "loop behavior", "semantic state"],
        })
    return result


def animation_manifest(records: list[dict[str, Any]], assets: list[dict[str, Any]], trace: dict[str, Any]) -> dict[str, Any]:
    frames = []
    for record in records:
        frames.append({
            "frame_id": f"mode_{record['mode']:02d}",
            "mode_id": record["mode"],
            "semantic_label": None,
            "body_asset_selector": "TBody",
            "face_asset_selector": "TFace",
            "body_source_rect": rect_from(record, "body"),
            "face_source_rect": rect_from(record, "face"),
            "body_destination_offset": {"x": record["body_dst_x"], "y": record["body_dst_y"]},
            "face_destination_offset": {"x": record["face_dst_x"], "y": record["face_dst_y"]},
            "frame_timing_ms": None,
            "loop_mode": None,
            "direction": None,
            "mirroring": None,
            "confidence": "verified-record-only",
            "bodyface_record_mode": record["mode"],
            "evidence": [{"source": rel(BODYFACE), "callsite": hex(record["callsite"])}],
        })
    groups = mechanical_groups(records)
    return {
        "schema": f"{SCHEMA}.animation-manifest.v1",
        "animation_model": "neutral BodyFace crop descriptors and mechanically grouped source-layout candidates",
        "semantic_animations": [],
        "frame_descriptors": frames,
        "mechanical_groups": groups,
        "coverage": {
            "frame_descriptors": len(frames),
            "mechanical_groups_discovered": len(groups),
            "verified_semantic_animations": 0,
            "probable_semantic_animations": 0,
            "unknown_semantic_animations": len(frames),
        },
        "notes": [
            "A repeated source row is cataloged as a candidate group only; it is not promoted to walking, working, sitting, or another semantic label.",
            "No frame timing or loop behavior was found in the current Phase 2 evidence set.",
        ],
    }


def agent_state_mapping(trace: dict[str, Any], records: list[dict[str, Any]]) -> dict[str, Any]:
    draw_human_lines = trace["function_evidence_lines"]["DrawHuman"]
    draw_human_reference_line = draw_human_lines.get("function_header_line") or draw_human_lines.get("first_symbol_line")
    states = []
    for state in ("idle", "walking", "working", "sitting", "break"):
        states.append({
            "agent_state": state,
            "status": "unknown",
            "legacy_state_or_mode": None,
            "frame_sequence": [],
            "bodyface_records": [],
            "face_behavior": None,
            "direction_behavior": None,
            "timing": None,
            "loop_behavior": None,
            "furniture_or_seat_requirement": None,
            "evidence": [
                {"source": rel(DUMP_CS), "fields": ["HumanDexMode", "HumanDexAnime", "HumanDexWalk"], "note": "Named fields exist, but current evidence does not connect them to a verified mode sequence for this Agent state."},
                {"source": rel(FORM_C), "line": draw_human_reference_line, "note": "DrawHuman exists, but individual call context is not sufficient to assign this state."},
            ],
            "unresolved_questions": ["which mode(s) represent this state", "direction", "timing", "loop", "placement/seat semantics"],
        })
    states.append({
        "agent_state": "talking",
        "status": "probable",
        "legacy_state_or_mode": "Kaiwa/dialogue rendering context; candidate TMode values 8 and 9",
        "frame_sequence": ["mode_08", "mode_09"],
        "bodyface_records": [8, 9],
        "face_behavior": "TFace is supplied by a dialogue/person selector in the observed call; exact face-change timing is unknown.",
        "direction_behavior": None,
        "timing": None,
        "loop_behavior": None,
        "furniture_or_seat_requirement": None,
        "evidence": [
            {"source": rel(FORM_C), "line": 71726, "note": "A DrawHuman call in the Kaiwa-related SubForm draw path uses TMode = iVar11 % 2 + 8 with TFace/TBody values loaded from form state."},
            {"source": rel(FORM_C), "line": 80668, "note": "A DrawHuman call with TMode = iVar14 % 2 + 8 is adjacent to DrawFukidashi."},
            {"source": rel(FORM_C), "line": 80682, "note": "The adjacent chat-bubble renderer is DrawFukidashi."},
            {"source": rel(DUMP_CS), "fields": ["KaiwaFaceG", "KaiwaBodyG"], "note": "GameForm exposes dialogue character selectors."},
        ],
        "unresolved_questions": ["whether modes 8/9 are a talking loop or another alternating visual", "timing", "face-change behavior", "text/bubble timing"],
    })
    return {
        "schema": f"{SCHEMA}.agent-state-mapping.v1",
        "adaptation_layer": "Virtual AI Office state mapping; does not rewrite original-game facts",
        "states": states,
        "coverage": {"verified": 0, "probable": 1, "unknown": 5},
        "policy": "Unknown is retained when the current extraction does not connect a semantic state to a specific original frame sequence.",
    }


def make_label_font() -> ImageFont.ImageFont:
    try:
        return ImageFont.truetype("DejaVuSans.ttf", 10)
    except OSError:
        return ImageFont.load_default()


def paste_scaled(canvas: Image.Image, source: Image.Image, box: tuple[int, int, int, int], scale: int = 3) -> None:
    crop = source.crop(box).convert("RGBA")
    crop = crop.resize((crop.width * scale, crop.height * scale), Image.Resampling.NEAREST)
    canvas.alpha_composite(crop)


def contact_sheet(assets: list[dict[str, Any]], output: Path, title: str) -> None:
    font = make_label_font()
    columns = 5
    cell_w, cell_h = 180, 115
    rows = (len(assets) + columns - 1) // columns
    image = Image.new("RGBA", (columns * cell_w, max(rows, 1) * cell_h), (238, 238, 238, 255))
    draw = ImageDraw.Draw(image)
    draw.text((8, 4), title, fill=(0, 0, 0, 255), font=font)
    for index, asset in enumerate(assets):
        path = ROOT / asset["source_path"]
        with Image.open(path) as source:
            x = (index % columns) * cell_w + 8
            y = (index // columns) * cell_h + 22
            crop = source.convert("RGBA")
            scale = min(3, max(1, (cell_w - 16) // max(crop.width, 1)))
            crop = crop.resize((crop.width * scale, crop.height * scale), Image.Resampling.NEAREST)
            image.alpha_composite(crop, (x, y))
            draw.text((x, y + crop.height + 3), asset["filename"], fill=(0, 0, 0, 255), font=font)
            if asset.get("special_case"):
                draw.text((x, y + crop.height + 15), "special width", fill=(160, 70, 0, 255), font=font)
    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output)


def mode_preview(records: list[dict[str, Any]], output: Path, animated: bool = False) -> None:
    body_path = GAME / "body0.png"
    face_path = GAME / "face_0.png"
    with Image.open(body_path) as body, Image.open(face_path) as face:
        body = body.convert("RGBA")
        face = face.convert("RGBA")
        font = make_label_font()
        columns = 7
        cell_w, cell_h = 100, 88
        rows = (len(records) + columns - 1) // columns
        image = Image.new("RGBA", (columns * cell_w, rows * cell_h), (245, 245, 245, 255))
        draw = ImageDraw.Draw(image)
        draw.text((8, 2), "Diagnostic sample: body0 + face_0 | semantic/state: UNKNOWN", fill=(120, 45, 0, 255), font=font)
        for index, record in enumerate(records):
            x = (index % columns) * cell_w + 8
            y = (index // columns) * cell_h + 34
            canvas = Image.new("RGBA", (30, 34), (255, 255, 255, 0))
            br = rect_from(record, "body")
            fr = rect_from(record, "face")
            paste_scaled(canvas, body, (br["x"], br["y"], br["x"] + br["width"], br["y"] + br["height"]), 1)
            face_crop = face.crop((fr["x"], fr["y"], fr["x"] + fr["width"], fr["y"] + fr["height"])).convert("RGBA")
            canvas.alpha_composite(face_crop, (record["face_dst_x"], record["face_dst_y"]))
            image.alpha_composite(canvas.resize((canvas.width * 2, canvas.height * 2), Image.Resampling.NEAREST), (x, y))
            draw.text((x, y - 12), f"mode_{record['mode']:02d}", fill=(0, 0, 0, 255), font=font)
        output.parent.mkdir(parents=True, exist_ok=True)
        image.save(output)


def write_report(audit: dict[str, Any], analysis: dict[str, Any], trace: dict[str, Any], animation: dict[str, Any], states: dict[str, Any], output: Path) -> None:
    bodyface = audit["bodyface_baseline"]
    missing = audit["missing_references"]
    lines = [
        "# Phase 2 — Character and animation catalog",
        "",
        "สถานะ: `complete_with_known_limitations` สำหรับหลักฐานที่มีใน extraction ปัจจุบัน",
        "",
        "เอกสารนี้แยกข้อเท็จจริงจาก extraction ออกจาก adaptation layer ของ Virtual AI Office.",
        "",
        "## Verified",
        "",
        f"- `bodyface_records.reference.json` มี {bodyface['record_count']} records, mode {bodyface['mode_values'][0]}–{bodyface['mode_values'][-1]} และทุก mode ไม่ซ้ำกัน.",
        f"- พบ body asset {audit['assets_summary']['body_assets']} ไฟล์ และ face asset {audit['assets_summary']['face_assets']} ไฟล์; asset files ถูก hash และตรวจ dimensions แล้ว.",
        "- `GameForm.DrawHuman` ระบุพารามิเตอร์ `TFace`, `TBody`, `TMode` ใน `dump.cs`; recovered C ใช้ `TMode` เพื่อเลือกข้อมูลจาก static `BodyFace` table.",
        "- กลไกประกอบภาพที่ยืนยันได้คือ `imgBody[TBody]` + `imgFace[TFace]` โดยใช้ crop/offset จาก `BodyFace[TMode]`; `AddBodyFace` ยืนยัน mapping ของ P0–P13 เป็น body/face/shadow fields. บาง branch มี offset ปรับเพิ่มตาม mode.",
        "- HumanDex draw path ส่ง `HumanDexFaceG`, `HumanDexBodyG`, `HumanDexAnime` เข้า `DrawHuman` โดยตรง; นี่เป็น dynamic selector path ที่ยืนยันได้หนึ่งเส้นทาง แต่ยังไม่ใช่ semantic mapping ของ Agent state.",
        f"- crop/offset record ที่ parse และ trace ได้: {analysis['record_count']}/{analysis['record_count']}.",
        f"- สร้าง neutral frame descriptors: {animation['coverage']['frame_descriptors']} และ mechanical source-layout groups: {animation['coverage']['mechanical_groups_discovered']}.",
        "",
        "## Probable",
        "",
        "- `talking` มี candidate mapping เป็น mode 8/9 ใน Kaiwa/dialogue draw path เพราะเห็น TMode สลับ `iVar % 2 + 8` และมี callsite ของ `DrawFukidashi` ในอีก dialogue-like draw path; timing/loop/face timing ยังไม่ยืนยัน.",
        "- Mechanical groups เป็นกลุ่ม candidate จาก source-row geometry เท่านั้น ไม่ใช่ semantic animation.",
        "",
        "## Unknown",
        "",
        "- ไม่สามารถยืนยัน semantic ของ mode ใด ๆ ว่าเป็น idle/walking/working/sitting/break ได้จากหลักฐานชุดนี้; ห้า state แรกจึงคงเป็น `unknown`.",
        "- direction, frame timing, loop mode, mirroring, pivot/baseline, seat/placement และ exact runtime body/face pairing ของทุก callsite ยังไม่ยืนยัน.",
        "- literal selector references ที่ไม่มี extracted asset: " + (", ".join(f"TFace={item['numeric_id']}" for item in missing) if missing else "ไม่มี") + ".",
        "",
        "## Coverage",
        "",
        f"- BodyFace records: {bodyface['record_count']} parsed; semantic modes verified: {analysis['summary']['semantic_modes_verified']}.",
        f"- Agent states: verified {states['coverage']['verified']}, probable {states['coverage']['probable']}, unknown {states['coverage']['unknown']}.",
        f"- Literal DrawHuman callsites scanned: {trace['draw_human_call_count']}; selector coverage is partial because {trace['literal_selector_coverage']['dynamic_selector_calls']} calls contain variable-driven selectors.",
        "",
        "## Preview policy",
        "",
        "- `body_contact_sheet.png` และ `face_contact_sheet.png` แสดง original atlases.",
        "- `bodyface_mode_preview.png` ใช้ `body0.png` + `face_0.png` เป็น diagnostic sample เท่านั้น; ไม่ใช่ข้อสรุปว่า runtime เลือก pair นี้.",
        "- ไม่มี GIF/WebP animation ที่อ้าง timing ได้ จึงไม่สร้าง loop ที่เดาขึ้นเอง.",
        "",
        "## Dependencies and next evidence",
        "",
        "- Phase 1 placement/seat/grid/depth unknowns ยังไม่ถูกปิด และไม่ถูกใช้เป็นเงื่อนไข block Phase 2.",
        "- งานถัดไปที่คุ้มค่าคือ trace dynamic `DrawHuman` ที่เหลือกลับไปยัง `DrawObj`/Syain/Kaiwa data, ยืนยันลำดับ resource array กับชื่อไฟล์จริง และหา initialization ของ BodyFace table ที่ยังหายจาก categorized callsites.",
        "",
        "## Artifacts",
        "",
        "- `artifacts/phase2_input_audit.json`",
        "- `artifacts/bodyface_analysis.json`",
        "- `artifacts/character_asset_catalog.json`",
        "- `artifacts/character_manifest.json`",
        "- `artifacts/animation_manifest.json`",
        "- `artifacts/phase2_code_trace.json`",
        "- `artifacts/agent_state_mapping.json`",
        "- `artifacts/phase2_validation_report.json`",
        "- `artifacts/preview/*.png`",
        "",
    ]
    output.write_text("\n".join(lines), encoding="utf-8")


def validate(artifact_paths: Iterable[Path], audit: dict[str, Any], records: list[dict[str, Any]], character: dict[str, Any], animation: dict[str, Any], states: dict[str, Any]) -> dict[str, Any]:
    checks = []
    errors: list[str] = []
    for path in artifact_paths:
        try:
            json.loads(path.read_text(encoding="utf-8"))
            checks.append({"check": "json_parse", "path": rel(path), "status": "pass"})
        except Exception as exc:
            errors.append(f"{rel(path)}: {exc}")
            checks.append({"check": "json_parse", "path": rel(path), "status": "fail", "error": str(exc)})
    allowed = set(ALLOWED_CONFIDENCE)
    confidence_values: list[str] = []
    def walk(value: Any) -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                if key == "confidence" and isinstance(child, str):
                    confidence_values.append(child)
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)
    walk(character)
    walk(animation)
    walk(states)
    bad_confidence = sorted(set(confidence_values) - allowed)
    checks.append({"check": "confidence_vocabulary", "status": "pass" if not bad_confidence else "fail", "invalid": bad_confidence, "allowed": sorted(allowed)})
    if bad_confidence:
        errors.append("invalid confidence values: " + ", ".join(bad_confidence))
    mode_ids = [record["mode"] for record in records]
    duplicate_modes = sorted(mode for mode, count in Counter(mode_ids).items() if count > 1)
    checks.append({"check": "unique_bodyface_modes", "status": "pass" if not duplicate_modes else "fail", "duplicates": duplicate_modes})
    if duplicate_modes:
        errors.append("duplicate bodyface modes")
    source_failures = []
    for item in audit["source_manifest"]:
        path = ROOT / item["source_path"]
        if not path.exists() or sha256(path) != item["sha256"]:
            source_failures.append(item["source_path"])
    checks.append({"check": "canonical_source_integrity_since_audit", "status": "pass" if not source_failures else "fail", "failures": source_failures})
    if source_failures:
        errors.append("canonical source changed or missing: " + ", ".join(source_failures))
    missing_paths = []
    for asset in audit["assets"]:
        if not (ROOT / asset["source_path"]).exists():
            missing_paths.append(asset["source_path"])
    checks.append({"check": "asset_paths_exist", "status": "pass" if not missing_paths else "fail", "missing": missing_paths})
    if missing_paths:
        errors.append("missing asset paths")
    checks.append({"check": "bodyface_manifest_shape", "status": "pass" if len(character["bodyface_mode_compositions"]) == len(records) else "fail", "expected": len(records), "actual": len(character["bodyface_mode_compositions"])})
    checks.append({"check": "animation_frame_shape", "status": "pass" if len(animation["frame_descriptors"]) == len(records) else "fail", "expected": len(records), "actual": len(animation["frame_descriptors"])})
    return {
        "schema": f"{SCHEMA}.validation-report.v1",
        "status": "pass" if not errors else "fail",
        "checks": checks,
        "errors": errors,
        "coverage": {
            "bodyface_records": len(records),
            "body_assets": sum(1 for asset in audit["assets"] if asset["asset_kind"] == "body"),
            "face_assets": sum(1 for asset in audit["assets"] if asset["asset_kind"] == "face"),
            "verified_mode_crop_records": len(records),
            "mechanical_animation_groups": len(animation["mechanical_groups"]),
            "semantic_animations_verified": animation["coverage"]["verified_semantic_animations"],
            "agent_states_verified": states["coverage"]["verified"],
            "agent_states_probable": states["coverage"]["probable"],
            "agent_states_unknown": states["coverage"]["unknown"],
            "missing_literal_references": len(audit["missing_references"]),
        },
    }


def build() -> int:
    for path in (BODYFACE, FORM_C, DUMP_CS, SCRIPT_JSON, GAME):
        if not path.exists():
            print(f"[ERROR] missing Phase 2 input: {path}", file=sys.stderr)
            return 2
    records = load_records()
    trace = code_trace(records)
    assets, asset_summary = build_assets(records, trace)
    audit = input_audit(records, assets, trace)
    audit["assets_summary"].update(asset_summary)
    analysis = bodyface_analysis(records, assets)
    character = character_manifest(records, assets, trace)
    animation = animation_manifest(records, assets, trace)
    states = agent_state_mapping(trace, records)
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    write_json(ARTIFACTS / "phase2_input_audit.json", audit)
    write_json(ARTIFACTS / "bodyface_analysis.json", analysis)
    write_json(ARTIFACTS / "character_asset_catalog.json", {"schema": f"{SCHEMA}.character-asset-catalog.v1", "assets_summary": asset_summary, "assets": assets, "source": rel(GAME), "selector_evidence": trace["literal_selector_coverage"]})
    write_json(ARTIFACTS / "character_manifest.json", character)
    write_json(ARTIFACTS / "animation_manifest.json", animation)
    write_json(ARTIFACTS / "phase2_code_trace.json", trace)
    write_json(ARTIFACTS / "agent_state_mapping.json", states)
    bodies = [asset for asset in assets if asset["asset_kind"] == "body"]
    faces = [asset for asset in assets if asset["asset_kind"] == "face"]
    contact_sheet(bodies, PREVIEW / "body_contact_sheet.png", "Original body atlases")
    contact_sheet(faces, PREVIEW / "face_contact_sheet.png", "Original face atlases")
    mode_preview(records, PREVIEW / "bodyface_mode_preview.png")
    mode_preview(records, PREVIEW / "animation_mode_contact_sheet.png")
    write_report(audit, analysis, trace, animation, states, PHASE / "docs" / "phase2_report.md")
    validation = validate([
        ARTIFACTS / "phase2_input_audit.json", ARTIFACTS / "bodyface_analysis.json", ARTIFACTS / "character_asset_catalog.json",
        ARTIFACTS / "character_manifest.json", ARTIFACTS / "animation_manifest.json", ARTIFACTS / "phase2_code_trace.json", ARTIFACTS / "agent_state_mapping.json",
    ], audit, records, character, animation, states)
    write_json(ARTIFACTS / "phase2_validation_report.json", validation)
    print(json.dumps({"records": len(records), "body_assets": len(bodies), "face_assets": len(faces), "draw_human_calls": trace["draw_human_call_count"], "validation": validation["status"]}, indent=2))
    return 0 if validation["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(build())
