#!/usr/bin/env python3
"""Create the evidence-first Phase 1 asset catalog.

The script only reads the Phase 0 source roots. It produces derived JSON
artifacts under ``Phases/Phase1/artifacts`` and never edits extracted assets,
dump files, or the Ghidra project.

Outputs:
  Phases/Phase1/artifacts/phase1_input_audit.json
  Phases/Phase1/artifacts/phase1_asset_catalog.json
  Phases/Phase1/artifacts/phase1_legacy_asset_map.json

The catalog deliberately keeps unresolved and repaired-looking references
visible.  In particular, several INF files end with a filename whose suffix
is missing.  A unique basename match is recorded in the adapter, but the
source INF is never rewritten.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from decode_seb import parse_seb_bytes
from phase_paths import phase_artifacts_dir


TARGET_GROUPS = ("office", "game", "com", "system")
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
TYPE_NAMES = {
    0: "floor",
    1: "reception",
    2: "pc",
    3: "desk",
    4: "chair",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=False) + "\n",
        encoding="utf-8",
    )


def rel_posix(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def parse_phase0_checksums(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.is_file():
        return values
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        match = re.match(r"^([0-9a-fA-F]{64})\s{2}(.+)$", line)
        if match:
            values[match.group(2).replace("\\", "/")] = match.group(1).lower()
    return values


def parse_png(path: Path) -> dict[str, Any]:
    """Return dimensions and alpha bounds without making PNG assumptions.

    Pillow is available in the workspace, but the fallback still validates the
    PNG signature/IHDR/IEND when Pillow is unavailable.  Alpha bounds are a
    derived convenience field; they are never treated as a pivot or collision
    contract.
    """

    data = path.read_bytes()
    result: dict[str, Any] = {
        "signature_valid": data.startswith(PNG_SIGNATURE),
        "iend_present": data.endswith(b"IEND\xaeB`\x82"),
        "valid": False,
        "dimensions": None,
        "mode": None,
        "has_alpha": None,
        "alpha_bounds": None,
        "alpha_bounds_status": "unavailable",
    }
    if not result["signature_valid"]:
        result["error"] = "invalid_png_signature"
        return result

    try:
        if len(data) < 24 or data[12:16] != b"IHDR":
            raise ValueError("missing IHDR")
        width = int.from_bytes(data[16:20], "big")
        height = int.from_bytes(data[20:24], "big")
        result["dimensions"] = {"width": width, "height": height}
    except Exception as exc:  # pragma: no cover - defensive path
        result["error"] = f"png_header_error:{exc}"
        return result

    try:
        from PIL import Image, ImageFile  # type: ignore

        ImageFile.LOAD_TRUNCATED_IMAGES = False
        with Image.open(path) as image:
            image.verify()
        with Image.open(path) as image:
            result["mode"] = image.mode
            has_alpha = "A" in image.getbands() or "transparency" in image.info
            result["has_alpha"] = bool(has_alpha)
            rgba = image.convert("RGBA")
            alpha = rgba.getchannel("A")
            bbox = alpha.getbbox()
            result["alpha_bounds"] = list(bbox) if bbox else None
            result["alpha_bounds_status"] = "decoded"
            if bbox is None:
                result["visible_bounds"] = None
            else:
                result["visible_bounds"] = list(bbox)
            result["valid"] = True
    except Exception as exc:
        # Keep the low-level header information and make the failure explicit.
        result["error"] = f"png_decode_error:{exc}"
        result["alpha_bounds_status"] = "decode_error"
    return result


def parse_inf(path: Path, sprites_root: Path, asset_by_rel: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """Parse an image/SEB index while preserving every raw token."""

    records: list[dict[str, Any]] = []
    errors: list[str] = []
    directory = path.parent
    inf_kind = "png" if path.name.lower() == "img.inf" else "seb" if path.name.lower() == "seb.inf" else None
    lines = path.read_text(encoding="ascii", errors="replace").splitlines()

    for line_number, raw_line in enumerate(lines, start=1):
        if not raw_line.strip():
            continue
        fields = raw_line.split("\t")
        legacy_index: int | None = None
        if len(fields) >= 2 and fields[0].strip().isdigit():
            legacy_index = int(fields[0].strip())
            raw_name = fields[1].strip()
        else:
            raw_name = fields[0].strip()

        candidate = directory / raw_name
        resolved: Path | None = candidate if candidate.is_file() else None
        resolution = "exact" if resolved else "unresolved"
        confidence = "verified" if resolved else "unknown"
        anomaly: str | None = None

        if resolved is None and inf_kind and Path(raw_name).suffix == "":
            expected = sorted(directory.glob(raw_name + "." + inf_kind))
            if len(expected) == 1:
                resolved = expected[0]
                resolution = "unique_basename_extension"
                confidence = "probable"
                anomaly = "missing_extension_in_source_inf"
            elif len(expected) > 1:
                resolution = "ambiguous_basename_extension"
                anomaly = "ambiguous_missing_extension"

        resolved_rel = rel_posix(resolved, sprites_root) if resolved else None
        if resolved_rel and resolved_rel not in asset_by_rel:
            errors.append(f"{path.name}:{line_number} resolved file is outside catalog: {resolved_rel}")
        records.append(
            {
                "line": line_number,
                "legacy_index": legacy_index,
                "raw_name": raw_name,
                "resolved_relative_path": resolved_rel,
                "resolution": resolution,
                "confidence": confidence,
                "anomaly": anomaly,
            }
        )

    return {
        "path": rel_posix(path, sprites_root.parent),
        "relative_path": rel_posix(path, sprites_root),
        "kind": inf_kind or "unknown",
        "records": records,
        "errors": errors,
    }


def parse_bonus(path: Path, sprites_root: Path, asset_by_rel: dict[str, dict[str, Any]]) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    errors: list[str] = []
    text = path.read_text(encoding="utf-8", errors="replace")
    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        if not raw_line.strip():
            continue
        fields = raw_line.split("\t")
        def as_int(index: int) -> int | None:
            try:
                return int(fields[index])
            except (IndexError, TypeError, ValueError):
                return None

        catalog_id = as_int(0)
        item_id = as_int(1)
        type_id = as_int(3)
        asset_ref = fields[2].strip() if len(fields) > 2 else ""
        category = TYPE_NAMES.get(type_id, "unknown")
        office_rel = f"office/{asset_ref}.png" if asset_ref and asset_ref != "-1" else None
        linked = office_rel in asset_by_rel if office_rel else False
        if office_rel and not linked:
            errors.append(f"line {line_number}: missing office asset for {asset_ref}")
        rows.append(
            {
                "line": line_number,
                "catalog_id": catalog_id,
                "item_id": item_id,
                "asset_ref": asset_ref,
                "asset_relative_path": office_rel if linked else None,
                "type_id": type_id,
                "category": category,
                "unlock_or_flag": as_int(4),
                "name_en": fields[5] if len(fields) > 5 else "",
                "raw_field_count": len(fields),
                "resolution": "linked" if linked else "placeholder" if asset_ref == "-1" else "missing",
            }
        )

    return {
        "path": rel_posix(path, sprites_root.parent),
        "relative_path": rel_posix(path, sprites_root),
        "rows": rows,
        "errors": errors,
    }


def role_for(group: str, name: str, extension: str) -> tuple[str, str]:
    stem = Path(name).stem.lower()
    if group == "office":
        if extension == "inf":
            return "metadata_index", "supporting_metadata"
        if extension == "seb":
            return "sprite_descriptor", "visual_map"
        if stem.startswith("floor"):
            return "room_background_atlas", "visual_map"
        if stem.startswith("chair"):
            return "furniture_chair_atlas", "visual_map"
        if stem.startswith("desk"):
            return "furniture_desk_atlas", "visual_map"
        if stem.startswith("pc"):
            return "furniture_pc_atlas", "visual_map"
        if stem.startswith("reception"):
            return "furniture_reception_atlas", "visual_map"
        return "office_visual_unknown", "visual_map"
    if group == "game":
        if extension == "inf":
            return "metadata_index", "supporting_metadata"
        if extension == "seb":
            return "sprite_descriptor", "supporting_metadata"
        if stem in {"floor0", "floor1", "floor2"}:
            return "base_room_background", "visual_map"
        if stem in {"floorparts0", "floorcover"}:
            return "room_parts_or_cover", "visual_map"
        if stem in {"chair0_origin", "desk0_origin", "pc"}:
            return "furniture_origin_atlas", "visual_map"
        if stem.startswith("body") or stem.startswith("face_"):
            return "character_asset", "deferred_phase2"
        if stem in {"fukidasi", "bugbubble"}:
            return "speech_or_status_ui", "deferred_phase2"
        return "game_visual_or_ui", "supporting_metadata"
    if group == "com":
        if stem == "office_cover":
            return "office_customization_ui", "supporting_metadata"
        return "gameplay_ui", "deferred_non_office"
    if group == "system":
        return "system_ui", "deferred_non_office"
    return "unknown", "unknown"


def build_catalog(workspace: Path, generated_at: str) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    sprites_root = workspace / "game-dev-story-mod_Sprites"
    phase0_artifacts = phase_artifacts_dir(workspace, 0)
    manifest_path = phase0_artifacts / "asset_manifest.json"
    checksum_path = phase0_artifacts / "phase0_checksums.sha256"
    manifest = load_json(manifest_path)
    phase0_checksums = parse_phase0_checksums(checksum_path)

    entries = [entry for entry in manifest.get("files", []) if entry.get("group") in TARGET_GROUPS]
    asset_by_rel: dict[str, dict[str, Any]] = {}
    files: list[dict[str, Any]] = []
    png_validation: list[dict[str, Any]] = []
    seb_validation: list[dict[str, Any]] = []

    for entry in sorted(entries, key=lambda value: value.get("relative_path", "")):
        relative_path = str(entry["relative_path"]).replace("\\", "/")
        source_path = sprites_root / Path(relative_path)
        group = str(entry.get("group") or relative_path.split("/", 1)[0])
        extension = str(entry.get("extension") or source_path.suffix.lstrip(".")).lower()
        role, scope = role_for(group, source_path.name, extension)
        actual_hash = sha256_file(source_path) if source_path.is_file() else None
        phase0_hash = phase0_checksums.get(f"game-dev-story-mod_Sprites/{relative_path}")
        record: dict[str, Any] = {
            # Use the relative path because localized/system subdirectories
            # can also contain same-named PNGs.  The extension is therefore
            # retained naturally (for example asset.office.floor0.png).
            "id": "asset." + relative_path.replace("/", "."),
            "source": {
                "archive": group,
                "path": f"game-dev-story-mod_Sprites/{relative_path}",
                "relative_path": relative_path,
                "size_bytes": source_path.stat().st_size if source_path.is_file() else None,
                "sha256": actual_hash,
                "phase0_sha256": phase0_hash,
                "phase0_hash_match": actual_hash is not None and phase0_hash == actual_hash,
            },
            "extension": extension,
            "role": role,
            "scope": scope,
            "dimensions": entry.get("dimensions"),
            "paired_assets": [],
            "legacy": {"inf": [], "bonus": []},
            "confidence": "verified" if source_path.is_file() and actual_hash == phase0_hash else "unknown",
            "evidence": [
                {
                    "kind": "phase0_asset_manifest",
                    "path": "Phases/Phase0/artifacts/asset_manifest.json",
                    "claim": "file exists in frozen extraction manifest",
                }
            ],
        }
        if extension == "png" and source_path.is_file():
            info = parse_png(source_path)
            record["png"] = info
            if info.get("dimensions") and not record.get("dimensions"):
                record["dimensions"] = info["dimensions"]
            png_validation.append({"path": relative_path, **info})
        elif extension == "seb" and source_path.is_file():
            data = source_path.read_bytes()
            decoded = parse_seb_bytes(data, relative_path)
            info = {
                "nonempty": bool(data),
                "length_bytes": len(data),
                "even_length": len(data) % 2 == 0,
                "header_hex": data[:32].hex(),
                "structure": {
                    "format_code": decoded.get("format_code"),
                    "format_name": decoded.get("format_name"),
                    "group_count": decoded.get("header", {}).get("group_count"),
                    "max_frame": decoded.get("header", {}).get("max_frame"),
                    "groups_decoded": len(decoded.get("groups", [])),
                    "records_declared": sum(
                        int(group.get("record_count") or 0)
                        for group in decoded.get("groups", [])
                    ),
                    "records_complete": sum(
                        1
                        for group in decoded.get("groups", [])
                        for record in group.get("records", [])
                        if record.get("complete")
                    ),
                    "status": decoded.get("status"),
                    "expected_bytes": decoded.get("expected_bytes"),
                    "bytes_consumed": decoded.get("bytes_consumed"),
                    "tail_shortfall_bytes": decoded.get("tail_shortfall_bytes", 0),
                    "trailing_bytes": decoded.get("trailing_bytes", 0),
                    "errors": decoded.get("errors", []),
                },
            }
            record["seb"] = info
            seb_validation.append({"path": relative_path, **info})
        files.append(record)
        asset_by_rel[relative_path] = record

    # Pair files by same directory/stem.  A pair is a fact about extraction,
    # not proof that the files are used together at runtime.
    by_stem: dict[tuple[str, str], list[str]] = defaultdict(list)
    for record in files:
        rel = record["source"]["relative_path"]
        source = Path(rel)
        by_stem[(source.parent.as_posix(), source.stem)].append(rel)
    for record in files:
        rel = record["source"]["relative_path"]
        source = Path(rel)
        record["paired_assets"] = sorted(
            value for value in by_stem[(source.parent.as_posix(), source.stem)] if value != rel
        )

    inf_documents: list[dict[str, Any]] = []
    for path in sorted(sprites_root.rglob("*.inf")):
        if path.parent.name not in TARGET_GROUPS:
            continue
        inf_documents.append(parse_inf(path, sprites_root, asset_by_rel))
        document = inf_documents[-1]
        for item in document["records"]:
            resolved = item.get("resolved_relative_path")
            if resolved in asset_by_rel:
                asset_by_rel[resolved]["legacy"]["inf"].append(
                    {
                        "source": document["relative_path"],
                        "legacy_index": item.get("legacy_index"),
                        "raw_name": item.get("raw_name"),
                        "resolution": item.get("resolution"),
                        "confidence": item.get("confidence"),
                    }
                )

    bonus_path = sprites_root / "xls" / "English.lproj" / "bonus.txt"
    bonus_document = parse_bonus(bonus_path, sprites_root, asset_by_rel) if bonus_path.is_file() else {
        "path": None,
        "relative_path": None,
        "rows": [],
        "errors": ["bonus.txt is missing"],
    }
    for row in bonus_document["rows"]:
        resolved = row.get("asset_relative_path")
        if resolved in asset_by_rel:
            asset_by_rel[resolved]["legacy"]["bonus"].append(
                {
                    "catalog_id": row.get("catalog_id"),
                    "item_id": row.get("item_id"),
                    "type_id": row.get("type_id"),
                    "category": row.get("category"),
                    "name_en": row.get("name_en"),
                    "confidence": "verified",
                }
            )
            asset_by_rel[resolved]["evidence"].append(
                {
                    "kind": "bonus_catalog",
                    "path": bonus_document["relative_path"],
                    "line": row.get("line"),
                    "claim": "catalog category/name and legacy IDs",
                }
            )

    office_pngs = sorted(
        record["source"]["relative_path"]
        for record in files
        if record["source"]["relative_path"].startswith("office/") and record["extension"] == "png"
    )
    bonus_direct = {
        row["asset_relative_path"]
        for row in bonus_document["rows"]
        if row.get("asset_relative_path")
    }
    office_orphans = [path for path in office_pngs if path not in bonus_direct]
    office_floor_pair_gaps = []
    for path in office_pngs:
        if Path(path).stem.lower().startswith("floor"):
            seb_rel = str(Path(path).with_suffix(".seb")).replace("\\", "/")
            if seb_rel not in asset_by_rel:
                office_floor_pair_gaps.append({"png": path, "expected_seb": seb_rel})

    phase0_match_count = sum(1 for record in files if record["source"]["phase0_hash_match"])
    audit_checks: list[dict[str, Any]] = []
    audit_checks.append(
        {
            "id": "source_root_present",
            "status": "pass" if sprites_root.is_dir() else "fail",
            "details": str(sprites_root),
        }
    )
    audit_checks.append(
        {
            "id": "target_manifest_coverage",
            "status": "pass" if len(files) == sum(manifest.get("by_group", {}).get(group, 0) for group in TARGET_GROUPS) else "attention",
            "details": f"catalog={len(files)} target_manifest={sum(manifest.get('by_group', {}).get(group, 0) for group in TARGET_GROUPS)}",
        }
    )
    audit_checks.append(
        {
            "id": "phase0_checksum_match",
            "status": "pass" if phase0_match_count == len(files) else "fail",
            "details": f"{phase0_match_count}/{len(files)} target files match Phase 0 checksums",
        }
    )
    png_invalid = [item["path"] for item in png_validation if not item.get("valid")]
    audit_checks.append(
        {
            "id": "png_integrity",
            "status": "pass" if not png_invalid else "fail",
            "details": f"invalid={len(png_invalid)} of {len(png_validation)} target PNG files",
        }
    )
    seb_invalid = [
        item["path"]
        for item in seb_validation
        if not item.get("nonempty")
        or not item.get("even_length")
        or item.get("structure", {}).get("errors")
    ]
    seb_tail_shortfalls = [
        {
            "path": item["path"],
            "bytes": item.get("structure", {}).get("tail_shortfall_bytes", 0),
            "expected_bytes": item.get("structure", {}).get("expected_bytes"),
            "actual_bytes": item.get("length_bytes"),
        }
        for item in seb_validation
        if item.get("structure", {}).get("tail_shortfall_bytes", 0)
    ]
    audit_checks.append(
        {
            "id": "seb_container_sanity",
            "status": "fail" if seb_invalid else "pass",
            "details": f"nonempty/even/parse failures={len(seb_invalid)} of {len(seb_validation)}",
        }
    )
    audit_checks.append(
        {
            "id": "seb_structure_decode",
            "status": "attention" if seb_tail_shortfalls else "pass",
            "details": f"structurally decoded={len(seb_validation) - len(seb_invalid)}; tail_shortfall={len(seb_tail_shortfalls)}",
        }
    )
    inf_anomalies = [
        {"source": document["relative_path"], "line": item["line"], "raw_name": item["raw_name"], "anomaly": item["anomaly"]}
        for document in inf_documents
        for item in document["records"]
        if item.get("anomaly")
    ]
    audit_checks.append(
        {
            "id": "inf_resolution",
            "status": "attention" if inf_anomalies else "pass",
            "details": f"{len(inf_anomalies)} missing-extension reference(s) resolved in adapter",
        }
    )
    audit_checks.append(
        {
            "id": "office_floor_seb_pairing",
            "status": "attention" if office_floor_pair_gaps else "pass",
            "details": f"{len(office_floor_pair_gaps)} office floor PNG(s) have no same-name SEB",
        }
    )
    audit_checks.append(
        {
            "id": "bonus_reference_resolution",
            "status": "attention" if bonus_document["errors"] else "pass",
            "details": f"direct_missing={len(bonus_document['errors'])}; placeholders={sum(1 for row in bonus_document['rows'] if row.get('asset_ref') == '-1')}",
        }
    )

    audit = {
        "schema": 1,
        "generated_at_utc": generated_at,
        "phase": "phase1",
        "status": "complete_with_known_limitations" if not any(check["status"] == "fail" for check in audit_checks) else "blocked_by_integrity_failure",
        "source_policy": "Read-only source roots; all repairs are adapter metadata only.",
        "source_roots": {
            "sprites": "game-dev-story-mod_Sprites",
            "dumped": "game-dev-story-mod_Dumped",
            "extracted": "game-dev-story-mod_Extracted",
        },
        "target_groups": list(TARGET_GROUPS),
        "checks": audit_checks,
        "counts": {
            "target_files": len(files),
            "target_png": sum(1 for record in files if record["extension"] == "png"),
            "target_seb": sum(1 for record in files if record["extension"] == "seb"),
            "target_inf": sum(1 for record in files if record["extension"] == "inf"),
            "phase0_hash_matches": phase0_match_count,
            "bonus_rows": len(bonus_document["rows"]),
            "office_png": len(office_pngs),
            "office_bonus_direct_refs": len(bonus_direct),
            "office_bonus_orphans": len(office_orphans),
        },
        "anomalies": {
            "inf_missing_extension": inf_anomalies,
            "office_floor_without_same_name_seb": office_floor_pair_gaps,
            "office_png_not_directly_referenced_by_bonus": office_orphans,
            "bonus_errors": bonus_document["errors"],
            "png_invalid": png_invalid,
            "seb_sanity_failures": seb_invalid,
            "seb_parse_errors": [
                {
                    "path": item["path"],
                    "errors": item.get("structure", {}).get("errors", []),
                }
                for item in seb_validation
                if item.get("structure", {}).get("errors")
            ],
            "seb_tail_shortfall": seb_tail_shortfalls,
        },
        "known_limitations": [
            "SEB structural decoding follows the decompiled legacy ten-short record format, but all current extracted SEBs end four bytes early in the final record; no source padding is applied.",
            "The SEB tail shortfall needs source/archive boundary verification before any runtime renderer is trusted.",
            "A unique basename extension match is not a source-file repair and remains marked probable.",
            "No collision, seat, pivot, or depth meaning is inferred from alpha bounds or filenames.",
        ],
    }

    catalog = {
        "schema": 1,
        "generated_at_utc": generated_at,
        "phase": "phase1",
        "source_root": "game-dev-story-mod_Sprites",
        "source_policy": "Current extraction output is read-only; derived metadata is separate.",
        "target_groups": list(TARGET_GROUPS),
        "file_count": len(files),
        "files": files,
        "summary": {
            "by_group": dict(Counter(record["source"]["archive"] for record in files)),
            "by_extension": dict(Counter(record["extension"] for record in files)),
            "by_role": dict(Counter(record["role"] for record in files)),
            "by_scope": dict(Counter(record["scope"] for record in files)),
        },
    }

    legacy_map = {
        "schema": 1,
        "generated_at_utc": generated_at,
        "phase": "phase1",
        "source_policy": "Raw INF and catalog rows are preserved; only links are derived.",
        "inf_documents": inf_documents,
        "bonus_catalog": bonus_document,
        "office_asset_audit": {
            "png_count": len(office_pngs),
            "direct_bonus_reference_count": len(bonus_direct),
            "unreferenced_pngs": office_orphans,
            "floor_png_without_same_name_seb": office_floor_pair_gaps,
        },
    }
    return audit, catalog, legacy_map


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--workspace",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="workspace root containing game-dev-story-mod_Sprites and Phase 0 manifests",
    )
    args = parser.parse_args(list(argv) if argv is not None else None)
    workspace = args.workspace.expanduser().resolve()
    generated_at = utc_now()
    try:
        audit, catalog, legacy_map = build_catalog(workspace, generated_at)
        artifacts = phase_artifacts_dir(workspace, 1)
        write_json(artifacts / "phase1_input_audit.json", audit)
        write_json(artifacts / "phase1_asset_catalog.json", catalog)
        write_json(artifacts / "phase1_legacy_asset_map.json", legacy_map)
    except Exception as exc:
        print(f"[ERROR] Phase 1 catalog generation failed: {exc}", file=sys.stderr)
        return 1

    print(f"[OK] Phase 1 input audit: {audit['status']}")
    print(f"[OK] Cataloged {catalog['file_count']} target files.")
    print(
        "[INFO] PNG={png} SEB={seb} INF={inf}; checksum matches={matches}.".format(
            png=audit["counts"]["target_png"],
            seb=audit["counts"]["target_seb"],
            inf=audit["counts"]["target_inf"],
            matches=audit["counts"]["phase0_hash_matches"],
        )
    )
    for check in audit["checks"]:
        print(f"[{check['status'].upper()}] {check['id']}: {check['details']}")
    return 0 if audit["status"] != "blocked_by_integrity_failure" else 1


if __name__ == "__main__":
    raise SystemExit(main())
