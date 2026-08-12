#!/usr/bin/env python3
"""Build the Wave 1 resource truth and assembly branch-index artifacts.

The tool reads the extracted source and asset roots without modifying them. It
models the resource-list behavior visible in the recovered C code:

* an explicit ``index<TAB>filename`` keeps its declared resource index;
* an unindexed filename is assigned to the lowest unused resource index;
* image lookup is by resource index, not by the number embedded in a filename;
* GameForm selector expressions are recorded separately from resource indices;
* NewGamePara/DoEvent assembly is indexed structurally before any lifecycle
  slice is attempted.

Generated output is written below ``Phases/Phase4/artifacts``.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import struct
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
PHASE = ROOT / "Phases" / "Phase4"
ARTIFACTS = PHASE / "artifacts"
DUMP = ROOT / "game-dev-story-mod_Dumped"
SPRITES = ROOT / "game-dev-story-mod_Sprites"

FORM_C = DUMP / "Categorized_Code" / "Global" / "form.c"
METHOD_C = DUMP / "Categorized_Code" / "Global" / "Method.c"
KAIRO_C = DUMP / "Categorized_Code" / "Global" / "kairo.c"
MAIN_C = DUMP / "Categorized_Code" / "Global" / "main.c"
STRINGLITERAL = DUMP / "stringliteral.json"
DUMP_CS = DUMP / "dump.cs"

ASM_FILES = {
    "form_GameForm__NewGamePara": DUMP / "Failed_Functions_Assembly" / "00f265b8_form_GameForm__NewGamePara.asm.txt",
    "form_GameForm__DoEvent": DUMP / "Failed_Functions_Assembly" / "00f5c704_form_GameForm__DoEvent.asm.txt",
}
ASSEMBLY_TO_RAW_DELTA = 0x100000


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
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def line_number(text: str, position: int) -> int:
    return text.count("\n", 0, position) + 1


def source_ref(path: Path, text: str, needle: str, occurrence: int = 1) -> dict[str, Any]:
    positions = [match.start() for match in re.finditer(re.escape(needle), text)]
    if not positions:
        return {"file": rel(path), "line": None, "needle": needle, "status": "not_found"}
    index = min(occurrence - 1, len(positions) - 1)
    return {"file": rel(path), "line": line_number(text, positions[index]), "needle": needle}


def load_literals() -> list[dict[str, Any]]:
    return json.loads(STRINGLITERAL.read_text(encoding="utf-8"))


def literal_value(literals: list[dict[str, Any]], literal_id: int) -> str | None:
    if 0 <= literal_id < len(literals):
        return literals[literal_id].get("value")
    return None


def parse_inf(path: Path, asset_dir: Path) -> dict[str, Any]:
    """Parse a ResourceManager list and apply its lowest-free-index behavior."""

    pending: list[dict[str, Any]] = []
    warnings: list[str] = []
    for line_no, raw in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        value = raw.lstrip("\ufeff").strip()
        if not value:
            continue
        parts = value.split("\t", 1)
        explicit_index: int | None = None
        if len(parts) == 2 and re.fullmatch(r"\d+", parts[0].strip()):
            explicit_index = int(parts[0].strip())
            filename_and_options = parts[1].strip()
        else:
            filename_and_options = value
        name_parts = [part.strip() for part in filename_and_options.split(",")]
        raw_filename = name_parts[0]
        options = [part for part in name_parts[1:] if part]
        pending.append(
            {
                "manifest_line": line_no,
                "raw_line": raw,
                "declared_resource_index": explicit_index,
                "filename": raw_filename,
                "options": options,
            }
        )

    explicit = [row["declared_resource_index"] for row in pending if row["declared_resource_index"] is not None]
    duplicates = sorted(index for index, count in Counter(explicit).items() if count > 1)
    if duplicates:
        warnings.append(f"duplicate explicit resource indices: {duplicates}")
    used = set(explicit)
    next_free = 0
    records: list[dict[str, Any]] = []
    for row in pending:
        resource_index = row["declared_resource_index"]
        assignment = "declared"
        if resource_index is None:
            while next_free in used:
                next_free += 1
            resource_index = next_free
            used.add(resource_index)
            assignment = "lowest_unused_index"
        else:
            used.add(resource_index)
        raw_filename = row["filename"].replace("\\", "/")
        candidate_names = [raw_filename]
        if not Path(raw_filename).suffix:
            candidate_names.extend([raw_filename + ".png", raw_filename + ".seb", raw_filename + ".bytes"])
        resolved: Path | None = None
        for candidate in candidate_names:
            candidate_path = asset_dir / candidate
            if candidate_path.is_file():
                resolved = candidate_path
                break
        records.append(
            {
                "resource_index": resource_index,
                "declared_resource_index": row["declared_resource_index"],
                "assignment": assignment,
                "manifest_line": row["manifest_line"],
                "raw_line": row["raw_line"],
                "filename": raw_filename,
                "options": row["options"],
                "asset_path": rel(resolved) if resolved else None,
                "asset_resolution": "exact_or_extension_candidate" if resolved else "missing_from_extracted_root",
            }
        )
    records.sort(key=lambda item: item["resource_index"])
    return {
        "manifest": rel(path),
        "asset_root": rel(asset_dir),
        "record_count": len(records),
        "records": records,
        "warnings": warnings,
        "contract": {
            "explicit_entry": "index<TAB>filename[,option...]",
            "implicit_entry": "assign lowest unused resource index in manifest order",
            "lookup_key": "resource_index",
        },
    }


def png_metadata(path: Path) -> dict[str, Any] | None:
    if path.suffix.lower() != ".png":
        return None
    data = path.read_bytes()
    metadata: dict[str, Any] = {"bytes": len(data), "sha256": sha256(path)}
    if data[:8] == b"\x89PNG\r\n\x1a\n" and len(data) >= 24:
        metadata["width"], metadata["height"] = struct.unpack(">II", data[16:24])
        metadata["format"] = "png"
    else:
        metadata["format"] = "invalid_png_signature"
    return metadata


def family_for(filename: str, root_name: str) -> str:
    stem = Path(filename).stem.lower()
    if root_name == "game":
        if re.fullmatch(r"body\d+", stem):
            return "body"
        if re.fullmatch(r"face_?\d+", stem):
            return "face"
        if re.fullmatch(r"event\d+", stem):
            return "event"
        if re.fullmatch(r"hard\d+", stem):
            return "hard"
        if re.fullmatch(r"floor\d+", stem):
            return "floor"
        if stem == "floorparts0":
            return "floor_parts"
        if stem == "floorcover":
            return "floor_cover"
    if root_name == "office":
        for prefix in ("chair_", "desk_", "pc_", "reception_"):
            if stem.startswith(prefix):
                return prefix[:-1]
        if re.fullmatch(r"floor\d+", stem):
            return "floor"
    return "other"


def enrich_manifest(manifest: dict[str, Any], root_name: str) -> dict[str, Any]:
    families: Counter[str] = Counter()
    for record in manifest["records"]:
        family = family_for(record["filename"], root_name)
        record["family"] = family
        families[family] += 1
        if record["asset_path"]:
            metadata = png_metadata(ROOT / record["asset_path"])
            if metadata is None:
                path = ROOT / record["asset_path"]
                metadata = {"bytes": path.stat().st_size, "sha256": sha256(path)}
            record["asset_metadata"] = metadata
        else:
            record["asset_metadata"] = None
    manifest["family_counts"] = dict(sorted(families.items()))
    return manifest


def parse_static_img_list(form_text: str, literals: list[dict[str, Any]]) -> dict[str, Any]:
    allocation = re.search(
        r"lVar17\s*=\s*FUN_00db0c30\(\*\(undefined8 \*\)puVar7,0x50\);",
        form_text,
    )
    assignment = re.search(r"\+ 0x68\) = lVar17;", form_text[allocation.end() :] if allocation else "")
    if not allocation or not assignment:
        return {"status": "not_found", "entries": []}
    start = allocation.end()
    end = start + assignment.start()
    chunk = form_text[start:end]
    ids = [int(value) for value in re.findall(r"PTR_StringLiteral_(\d+)", chunk)]
    entries = [
        {
            "selector_index": index,
            "literal_id": literal_id,
            "base_name": literal_value(literals, literal_id),
            "source_status": "literal_resolved" if literal_value(literals, literal_id) is not None else "literal_missing",
        }
        for index, literal_id in enumerate(ids)
    ]
    return {
        "status": "verified_from_recovered_c",
        "field": "form.GameForm.IMG_LIST",
        "field_offset": "0x68",
        "length": len(entries),
        "source": {
            "file": rel(FORM_C),
            "allocation_line": line_number(form_text, allocation.start()),
            "assignment_line": line_number(form_text, end),
        },
        "entries": entries,
    }


def attach_static_matches(static_list: dict[str, Any], game_manifest: dict[str, Any]) -> None:
    by_name: dict[str, list[tuple[dict[str, Any], str]]] = defaultdict(list)
    for record in game_manifest["records"]:
        by_name[record["filename"].lower()].append((record, "manifest_filename"))
        if record.get("asset_path"):
            asset_name = Path(record["asset_path"]).name.lower()
            if asset_name != record["filename"].lower():
                by_name[asset_name].append((record, "resolved_asset_basename"))
    for entry in static_list.get("entries", []):
        base = entry.get("base_name") or ""
        candidates = [base]
        if base and not Path(base).suffix:
            candidates.append(base + ".png")
        matches: list[tuple[dict[str, Any], str]] = []
        for candidate in candidates:
            matches.extend(by_name.get(candidate.lower(), []))
        unique_matches: dict[tuple[int, str], dict[str, Any]] = {}
        for record, basis in matches:
            unique_matches[(record["resource_index"], record["asset_path"])] = {
                "resource_index": record["resource_index"],
                "filename": record["filename"],
                "asset_path": record["asset_path"],
                "match_basis": basis,
            }
        entry["manifest_matches"] = list(unique_matches.values())
        entry["mapping_status"] = "resolved" if matches else "unknown_or_not_a_game_image"


def selector_contracts(method_text: str, form_text: str, main_text: str) -> list[dict[str, Any]]:
    png_suffix = {"literal_id": 833, "value": ".png.bytes", "extracted_asset_equivalent": ".png"}
    contracts = [
        {
            "family": "face",
            "destination_field": "form.GameForm.imgFace",
            "destination_offset": "0x1150",
            "count": 36,
            "selector_expression": "StringLiteral_7514 + i + StringLiteral_833",
            "prefix_literal_id": 7514,
            "prefix_value": "false",
            "suffix": png_suffix,
            "mapping_status": "unknown",
            "confidence": "verified_for_expression_unknown_for_filename",
            "source": source_ref(METHOD_C, method_text, "*(undefined8 *)(*(long *)(lVar10 + 0xb8) + 0x1150) = uVar11;"),
            "note": "Recovered C names the prefix literal as 7514 ('false'), which does not match extracted face_* assets; retain as an explicit evidence gap.",
        },
        {
            "family": "body",
            "destination_field": "form.GameForm.imgBody",
            "destination_offset": "0x1158",
            "count": 25,
            "selector_expression": "IMG_LIST[DDBody + i] + StringLiteral_833",
            "base_selector_field": "form.GameForm.DDBody",
            "base_selector_offset": "0xA8",
            "suffix": png_suffix,
            "mapping_status": "base_selector_value_unknown",
            "confidence": "verified_for_expression",
            "source": source_ref(METHOD_C, method_text, "plVar19 = *(long **)(lVar16 + 0x1158);"),
            "note": "The C trace proves selector provenance but the static DDBody value is not recovered as a named scalar in the available C export.",
        },
        {
            "family": "bihin",
            "destination_field": "form.GameForm.imgBihin_",
            "destination_offset": "0x1110",
            "count": 3,
            "selector_expression": "IMG_LIST[DDPC|DDChair|DDDesk] + StringLiteral_833",
            "base_selector_fields": [
                {"name": "DDPC", "offset": "0xD4", "slot": 0},
                {"name": "DDChair", "offset": "0xAC", "slot": 1},
                {"name": "DDDesk", "offset": "0xB0", "slot": 2},
            ],
            "suffix": png_suffix,
            "mapping_status": "base_selector_values_unknown",
            "confidence": "verified_for_expression",
            "source": source_ref(FORM_C, form_text, "// Function: form_GameForm__LoadBihinImage"),
        },
        {
            "family": "floor_and_event",
            "destination_field": "form.GameForm.imgFloorMain/imgFloorParts/imgFloorCover/imgEvent",
            "destination_offsets": ["0x1120", "0x1128", "0x1130", "0x1170"],
            "selector_expression": "IMG_LIST[index_field + event_or_floor_selector] + StringLiteral_833",
            "index_fields": ["IndexImgFloorMain", "IndexImgFloorParts", "IndexImgEvent"],
            "suffix": png_suffix,
            "mapping_status": "selector_expression_verified_asset_join_pending",
            "confidence": "verified_for_expression",
            "source": source_ref(FORM_C, form_text, "// Function: form_GameForm__EventGChange"),
        },
    ]
    contracts.append(
        {
            "family": "resource_lookup",
            "destination_field": "main.AppData.GetImage",
            "selector_expression": "resource manifest name -> AppData.GetImage(string) -> ResourceManager image array",
            "mapping_status": "verified",
            "confidence": "verified",
            "source": source_ref(MAIN_C, main_text, "// Function: main_AppData__GetImage"),
        }
    )
    return contracts


def fixture_rows(manifests: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    preferred = {"body", "face", "floor", "desk", "chair", "pc", "reception", "event"}
    for manifest in manifests:
        root_name = Path(manifest["asset_root"]).name
        for family in sorted(preferred):
            candidates = [
                record
                for record in manifest["records"]
                if record["family"] == family and record["asset_path"] and record["asset_metadata"]
            ]
            if not candidates:
                continue
            record = sorted(candidates, key=lambda item: item["resource_index"])[0]
            rows.append(
                {
                    "fixture_id": f"{root_name}_{family}_{record['resource_index']}",
                    "manifest": manifest["manifest"],
                    "family": family,
                    "input": {
                        "resource_index": record["resource_index"],
                        "filename": record["filename"],
                    },
                    "expected": {
                        "asset_path": record["asset_path"],
                        "sha256": record["asset_metadata"]["sha256"],
                        "bytes": record["asset_metadata"]["bytes"],
                        "width": record["asset_metadata"].get("width"),
                        "height": record["asset_metadata"].get("height"),
                    },
                    "confidence": "verified_manifest_and_asset",
                }
            )
    return rows


ASM_LINE = re.compile(r"^(?P<address>[0-9a-fA-F]{8})\s+(?P<body>.*?)\s+;\s*(?P<operands>.*)$")
BRANCHES = {"b", "bl", "blr", "br", "ret", "cbz", "cbnz", "tbz", "tbnz"}


def parse_assembly(path: Path) -> dict[str, Any]:
    instructions: list[dict[str, Any]] = []
    for line_no, raw in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        match = ASM_LINE.match(raw)
        if not match:
            continue
        tokens = match.group("body").split()
        mnemonic_index = next((index for index, token in enumerate(tokens) if not re.fullmatch(r"[0-9a-fA-F]{2}", token)), None)
        if mnemonic_index is None:
            continue
        mnemonic = tokens[mnemonic_index]
        address = int(match.group("address"), 16)
        operands = match.group("operands").strip()
        targets = [int(value, 16) for value in re.findall(r"0x([0-9a-fA-F]+)", operands)]
        raw_address = address - ASSEMBLY_TO_RAW_DELTA
        raw_targets = [target - ASSEMBLY_TO_RAW_DELTA for target in targets]
        instructions.append(
            {
                "address": f"0x{address:08x}",
                "address_int": address,
                "raw_address": f"0x{raw_address:08x}",
                "raw_address_int": raw_address,
                "line": line_no,
                "mnemonic": mnemonic,
                "operands": operands,
                "targets": [f"0x{target:08x}" for target in targets],
                "raw_targets": [f"0x{target:08x}" for target in raw_targets],
            }
        )
    if not instructions:
        return {"file": rel(path), "status": "not_found", "instructions": []}
    entry = instructions[0]["address_int"]
    branch_records = [
        {
            "address": row["address"],
            "line": row["line"],
            "mnemonic": row["mnemonic"],
            "operands": row["operands"],
            "targets": row["targets"],
            "raw_address": row["raw_address"],
            "raw_targets": row["raw_targets"],
            "kind": "call" if row["mnemonic"] in {"bl", "blr"} else "control_flow",
        }
        for row in instructions
        if row["mnemonic"].split(".", 1)[0] in BRANCHES
    ]
    starts = {entry}
    for index, row in enumerate(instructions):
        mnemonic = row["mnemonic"].split(".", 1)[0]
        if mnemonic in {"b", "cbz", "cbnz", "tbz", "tbnz"}:
            starts.update(int(target, 16) for target in row["targets"])
            if index + 1 < len(instructions):
                starts.add(instructions[index + 1]["address_int"])
        elif mnemonic == "ret" and index + 1 < len(instructions):
            starts.add(instructions[index + 1]["address_int"])
    starts = sorted(start for start in starts if start in {row["address_int"] for row in instructions})
    start_to_index = {row["address_int"]: index for index, row in enumerate(instructions)}
    blocks: list[dict[str, Any]] = []
    for index, block_start in enumerate(starts):
        first = start_to_index[block_start]
        last = start_to_index[starts[index + 1]] if index + 1 < len(starts) else len(instructions)
        block_instructions = instructions[first:last]
        block_branches = [row for row in branch_records if first <= start_to_index.get(int(row["address"], 16), -1) < last]
        blocks.append(
            {
                "block_id": f"B{index:04d}",
                "start": f"0x{block_start:08x}",
                "end": block_instructions[-1]["address"],
                "raw_start": block_instructions[0]["raw_address"],
                "raw_end": block_instructions[-1]["raw_address"],
                "instruction_count": len(block_instructions),
                "branch_targets": sorted({target for row in block_branches for target in row["targets"]}),
                "call_targets": sorted({target for row in block_branches if row["kind"] == "call" for target in row["targets"]}),
                "raw_branch_targets": sorted({target for row in block_branches for target in row["raw_targets"]}),
                "raw_call_targets": sorted({target for row in block_branches if row["kind"] == "call" for target in row["raw_targets"]}),
            }
        )
    calls = Counter(target for row in branch_records if row["kind"] == "call" for target in row["targets"])
    raw_calls = Counter(target for row in branch_records if row["kind"] == "call" for target in row["raw_targets"])
    return {
        "file": rel(path),
        "status": "structural_assembly_index",
        "address_namespace": "recovered_c_and_assembly_export",
        "raw_address_namespace": "script_json_and_elf_virtual_address",
        "raw_address_delta": -ASSEMBLY_TO_RAW_DELTA,
        "entry": f"0x{entry:08x}",
        "end": instructions[-1]["address"],
        "raw_entry": instructions[0]["raw_address"],
        "raw_end": instructions[-1]["raw_address"],
        "instruction_count": len(instructions),
        "branch_count": len(branch_records),
        "basic_block_count": len(blocks),
        "calls_by_target": [{"target": target, "count": count} for target, count in calls.most_common()],
        "raw_calls_by_target": [{"target": target, "count": count} for target, count in raw_calls.most_common()],
        "branches": branch_records,
        "basic_blocks": blocks,
        "semantic_limit": "addresses and CFG structure are indexed; branch meaning and field semantics remain unknown until a slice is translated",
    }


def build() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    literals = load_literals()
    game = enrich_manifest(parse_inf(SPRITES / "game" / "img.inf", SPRITES / "game"), "game")
    office = enrich_manifest(parse_inf(SPRITES / "office" / "img.inf", SPRITES / "office"), "office")
    load = enrich_manifest(parse_inf(SPRITES / "load" / "img.inf", SPRITES / "load"), "load")
    office_seb = enrich_manifest(parse_inf(SPRITES / "office" / "seb.inf", SPRITES / "office"), "office")
    manifests = [game, office, load, office_seb]

    form_text = FORM_C.read_text(encoding="utf-8", errors="replace")
    method_text = METHOD_C.read_text(encoding="utf-8", errors="replace")
    main_text = MAIN_C.read_text(encoding="utf-8", errors="replace")
    kairo_text = KAIRO_C.read_text(encoding="utf-8", errors="replace")
    static_list = parse_static_img_list(form_text, literals)
    attach_static_matches(static_list, game)
    contracts = selector_contracts(method_text, form_text, main_text)
    fixtures = fixture_rows(manifests)

    branch_index = {
        "schema_version": "wave1-branch-index-v2",
        "source_status": "assembly_fallback_only",
        "functions": {symbol: parse_assembly(path) for symbol, path in ASM_FILES.items()},
        "contract": {
            "purpose": "group NewGamePara and DoEvent into structural slices before semantic translation",
            "address_namespace": "assembly export addresses use recovered-C namespace; raw script/ELF addresses are assembly addresses minus 0x100000",
            "branch_targets": "parsed from disassembly addresses",
            "call_targets": "bl/blr targets retained as unresolved addresses",
            "field_semantics": "not inferred from raw offsets",
        },
    }

    resource_map = {
        "schema_version": "wave1-resource-selector-map-v1",
        "source_roots_read_only": True,
        "resource_manager_contract": {
            "ResourceManager": {
                "list_fields": ["img.inf", "seb.inf", "snd.inf", "fig.inf", "act.inf", "tex.inf", "grp.inf"],
                "image_array_lookup": "ResourceManager.GetImage(texId) -> img[texId]",
                "list_entry_parser": "split by TAB; first token is explicit resource index when numeric",
                "implicit_index_rule": "lowest unused resource index in list order",
                "source": source_ref(KAIRO_C, kairo_text, "// Function: kairo_unity_ui_ResourceManager__LoadStart"),
            },
            "AppData.GetImage": {
                "lookup": "resource-name string matches list_ entry name; returns matching resource array item",
                "source": source_ref(MAIN_C, main_text, "// Function: main_AppData__GetImage"),
            },
            "JarInflater": {
                "extension_normalization": "Config.ConvertExtension; archive lookup may use .bytes",
                "search": "case-insensitive access-file candidates, then dictionary lookup",
                "source": source_ref(KAIRO_C, kairo_text, "// Function: kairo_unity_util_JarInflater__ConvertExtension"),
            },
        },
        "manifests": manifests,
        "gameform_img_list": static_list,
        "selector_contracts": contracts,
        "fixtures": fixtures,
        "summary": {
            "manifest_count": len(manifests),
            "fixture_count": len(fixtures),
            "fixture_families": sorted({row["family"] for row in fixtures}),
            "img_list_entries": static_list.get("length", 0),
            "selector_contract_count": len(contracts),
            "unknown_selector_contracts": sum(1 for row in contracts if row.get("mapping_status", "").startswith("unknown") or "pending" in row.get("mapping_status", "")),
        },
        "source_files": {
            rel(path): {"sha256": sha256(path)}
            for path in [FORM_C, METHOD_C, MAIN_C, KAIRO_C, DUMP_CS, STRINGLITERAL]
        },
    }
    manifest = {
        "schema_version": "wave1-build-manifest-v1",
        "builder": rel(Path(__file__)),
        "source_roots_read_only": True,
        "artifacts": [
            "Phases/Phase4/artifacts/resource_selector_map.json",
            "Phases/Phase4/artifacts/wave1_branch_index.json",
        ],
        "source_sha256": resource_map["source_files"],
        "counts": resource_map["summary"],
        "branch_index_counts": {
            symbol: {
                "instructions": data.get("instruction_count", 0),
                "branches": data.get("branch_count", 0),
                "basic_blocks": data.get("basic_block_count", 0),
            }
            for symbol, data in branch_index["functions"].items()
        },
    }
    return resource_map, branch_index, manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="build in memory and compare with existing artifacts")
    args = parser.parse_args()
    resource_map, branch_index, manifest = build()
    outputs = {
        ARTIFACTS / "resource_selector_map.json": resource_map,
        ARTIFACTS / "wave1_branch_index.json": branch_index,
        ARTIFACTS / "wave1_build_manifest.json": manifest,
    }
    if args.check:
        mismatches = []
        for path, expected in outputs.items():
            if not path.exists() or json.loads(path.read_text(encoding="utf-8")) != expected:
                mismatches.append(rel(path))
        if mismatches:
            raise SystemExit("artifact mismatch: " + ", ".join(mismatches))
        return
    for path, value in outputs.items():
        write_json(path, value)
    print(json.dumps(manifest["counts"], ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
