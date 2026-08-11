#!/usr/bin/env python3
"""Build an evidence-first office asset/visual manifest for Phase 1."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from phase_paths import phase_artifacts_dir


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def bonus_summary(record: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "catalog_id": item.get("catalog_id"),
            "item_id": item.get("item_id"),
            "type_id": item.get("type_id"),
            "category": item.get("category"),
            "name_en": item.get("name_en"),
            "confidence": item.get("confidence", "verified"),
        }
        for item in record.get("legacy", {}).get("bonus", [])
    ]


def inf_summary(record: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "source": item.get("source"),
            "legacy_index": item.get("legacy_index"),
            "raw_name": item.get("raw_name"),
            "resolution": item.get("resolution"),
            "confidence": item.get("confidence"),
        }
        for item in record.get("legacy", {}).get("inf", [])
    ]


def semantics_for(record: dict[str, Any]) -> dict[str, Any]:
    role = record.get("role")
    extension = record.get("extension")
    bonus = bonus_summary(record)
    category = bonus[0].get("category") if bonus else None
    if extension != "png":
        return {
            "visual_role": role,
            "visual_role_confidence": "verified" if role == "sprite_descriptor" else "probable",
            "interaction": "unknown",
            "position_contract": "unknown",
            "anchor": "unknown",
            "baseline": "unknown",
            "pivot": "unknown",
            "depth_layer": "unknown",
        }
    role_confidence = "verified" if category in {"floor", "reception", "pc", "desk", "chair"} else "probable"
    position_contract = "verified_api_shape_unknown_values"
    if category == "chair":
        render_api = "form_GameForm__DrawChair"
        source_slot = "AppData +0x1110 image slot +0x28"
    elif category == "desk":
        render_api = "form_GameForm__DrawDesk"
        source_slot = "AppData +0x1110 image slot +0x30"
    elif category == "reception":
        render_api = "form_GameForm__DrawReception"
        source_slot = "AppData +0x1128 reception image"
    elif category == "floor":
        render_api = "not directly resolved for office floor PNG"
        source_slot = "unknown"
        position_contract = "unknown"
    else:
        render_api = "form_GameForm__DrawObj branch or direct DrawImage (not uniquely resolved)"
        source_slot = "unknown"
        position_contract = "unknown"
    return {
        "catalog_category": category,
        "visual_role": role,
        "visual_role_confidence": role_confidence,
        "render_api": render_api,
        "render_source_slot": source_slot,
        "interaction": "unknown",
        "collision": "unknown",
        "seat": "unknown",
        "walkable": "unknown",
        "zone": "unknown",
        "position_contract": position_contract,
        "anchor": "unknown",
        "baseline": "unknown",
        "pivot": "unknown",
        "depth_layer": "unknown",
        "semantic_note": "Bonus type/name is a catalog mapping; it does not prove collision, seat, or runtime placement.",
    }


def build_manifest(workspace: Path, generated_at: str) -> dict[str, Any]:
    artifacts = phase_artifacts_dir(workspace, 1)
    catalog = load_json(artifacts / "phase1_asset_catalog.json")
    legacy = load_json(artifacts / "phase1_legacy_asset_map.json")
    trace = load_json(artifacts / "phase1_code_trace.json")
    files = [
        record
        for record in catalog.get("files", [])
        if record.get("source", {}).get("relative_path", "").startswith("office/")
    ]
    by_rel = {record["source"]["relative_path"]: record for record in files}
    office_pngs = [record for record in files if record.get("extension") == "png"]
    office_sebs = [record for record in files if record.get("extension") == "seb"]

    assets: list[dict[str, Any]] = []
    for record in office_pngs:
        rel = record["source"]["relative_path"]
        assets.append(
            {
                "id": record.get("id"),
                "path": rel,
                "extension": "png",
                "sha256": record.get("source", {}).get("sha256"),
                "size_bytes": record.get("source", {}).get("size_bytes"),
                "dimensions": record.get("dimensions"),
                "alpha_bounds": record.get("png", {}).get("alpha_bounds"),
                "inf": inf_summary(record),
                "bonus_catalog": bonus_summary(record),
                "semantics": semantics_for(record),
                "paired_assets": record.get("paired_assets", []),
            }
        )
    for record in office_sebs:
        rel = record["source"]["relative_path"]
        structure = record.get("seb", {}).get("structure", {})
        assets.append(
            {
                "id": record.get("id"),
                "path": rel,
                "extension": "seb",
                "sha256": record.get("source", {}).get("sha256"),
                "size_bytes": record.get("source", {}).get("size_bytes"),
                "structure": structure,
                "semantics": semantics_for(record),
                "paired_assets": record.get("paired_assets", []),
            }
        )

    floor_sets: list[dict[str, Any]] = []
    furniture: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in office_pngs:
        rel = record["source"]["relative_path"]
        bonus = bonus_summary(record)
        category = bonus[0]["category"] if bonus else "unmapped"
        if category == "floor":
            seb_rel = str(Path(rel).with_suffix(".seb")).replace("\\", "/")
            seb = by_rel.get(seb_rel)
            floor_sets.append(
                {
                    "asset": rel,
                    "asset_id": record.get("id"),
                    "name_en": bonus[0].get("name_en") if bonus else None,
                    "dimensions": record.get("dimensions"),
                    "same_name_seb": seb_rel if seb else None,
                    "same_name_seb_status": seb.get("seb", {}).get("structure", {}).get("status") if seb else "missing",
                    "confidence": "verified_catalog_probable_runtime_role",
                    "placement": "unknown",
                }
            )
        else:
            furniture[category].append(
                {
                    "asset": rel,
                    "asset_id": record.get("id"),
                    "name_en": bonus[0].get("name_en") if bonus else None,
                    "dimensions": record.get("dimensions"),
                    "render_api": semantics_for(record).get("render_api"),
                    "placement": "unknown",
                    "interaction": "unknown",
                    "confidence": "verified_catalog_probable_runtime_role" if bonus else "probable",
                }
            )

    anomalies = legacy.get("office_asset_audit", {})
    return {
        "schema": 1,
        "generated_at_utc": generated_at,
        "phase": "phase1",
        "source_policy": "Read-only source assets; semantic fields stay unknown unless supported by catalog or decompiled callsite evidence.",
        "source_roots": {
            "sprites": "game-dev-story-mod_Sprites/office",
            "code_trace": "Phases/Phase1/artifacts/phase1_code_trace.json",
            "legacy_map": "Phases/Phase1/artifacts/phase1_legacy_asset_map.json",
        },
        "render_evidence": [
            item
            for item in trace.get("evidence", [])
            if item.get("id")
            in {
                "drawobj_dispatches_human",
                "drawobj_dispatches_chair",
                "drawobj_dispatches_desk",
                "drawobj_dispatches_ceo_desk",
                "drawobj_dispatches_reception",
                "floor_cover_source_rect",
                "chair_image_source",
                "desk_image_source",
                "reception_image_source",
                "desk_index_lookup",
                "chair_index_lookup",
            }
        ],
        "assets": assets,
        "scene_families": floor_sets,
        "furniture": {key: values for key, values in sorted(furniture.items())},
        "unresolved": {
            "office_bonus_orphans": anomalies.get("unreferenced_pngs", []),
            "floor_png_without_same_name_seb": anomalies.get("floor_png_without_same_name_seb", []),
            "anchor_baseline_pivot": "unknown",
            "collision_seat_walkable_zone": "unknown",
            "grid_and_depth_contract": "unknown; see Phases/Phase1/artifacts/phase1_code_trace.json",
        },
        "summary": {
            "office_assets": len(assets),
            "office_png": len(office_pngs),
            "office_seb": len(office_sebs),
            "floor_families": len(floor_sets),
            "furniture_by_category": {key: len(values) for key, values in sorted(furniture.items())},
            "bonus_linked_png": sum(1 for record in office_pngs if record.get("legacy", {}).get("bonus")),
            "bonus_orphan_png": len(anomalies.get("unreferenced_pngs", [])),
        },
    }


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--workspace",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="workspace root containing Phase 1 derived artifacts",
    )
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args(list(argv) if argv is not None else None)
    workspace = args.workspace.expanduser().resolve()
    output = (args.output or (phase_artifacts_dir(workspace, 1) / "office_manifest.json")).expanduser()
    if not output.is_absolute():
        output = workspace / output
    output.parent.mkdir(parents=True, exist_ok=True)
    try:
        payload = build_manifest(workspace, utc_now())
        output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    except Exception as exc:
        print(f"[ERROR] Office manifest creation failed: {exc}", file=sys.stderr)
        return 1
    print(
        f"[OK] Office manifest: {payload['summary']['office_png']} PNG + "
        f"{payload['summary']['office_seb']} SEB; floors={payload['summary']['floor_families']}"
    )
    print(f"[INFO] Furniture: {payload['summary']['furniture_by_category']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
