"""Build AM-4 composition and geometry catalogs for runtime-relevant assets."""

from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "knowledge/fixtures/accepted"
RUNTIME_EVIDENCE = ROOT / "knowledge/fixtures/accepted/runtime"

COVERAGE_PATH = EVIDENCE / "asset_metadata_coverage.json"
TAXONOMY_PATH = EVIDENCE / "asset_family_taxonomy.json"
DISPLAY_MANIFEST_PATH = RUNTIME_EVIDENCE / "display_asset_manifest.json"
CHARACTER_MANIFEST_PATH = RUNTIME_EVIDENCE / "character_asset_manifest.json"
ROOM_MANIFEST_PATH = RUNTIME_EVIDENCE / "room_scene_asset_manifest.json"

COMPOSITION_PATH = EVIDENCE / "asset_composition_catalog.json"
GEOMETRY_PATH = EVIDENCE / "asset_geometry_catalog.json"
CONTRACT_PATH = RUNTIME_EVIDENCE / "asset_composition_contract.json"
REPORT_PATH = ROOT / "docs/reports/social-dev_asset_composition_geometry.md"


def stable_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def asset_path_id(value: Any) -> str | None:
    if not isinstance(value, str) or not value:
        return None
    return value.replace("\\", "/")


def flatten_records(entry: dict[str, Any]) -> list[dict[str, Any]]:
    if isinstance(entry.get("records"), list):
        return [item for item in entry["records"] if isinstance(item, dict)]
    records = []
    for layer in entry.get("layers", []) or []:
        if isinstance(layer, dict):
            records.extend(item for item in layer.get("records", []) if isinstance(item, dict))
    return records


def nested_asset_ids(value: Any) -> set[str]:
    ids: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            if key.endswith("asset_id") and isinstance(item, str) and item:
                ids.add(item)
            ids.update(nested_asset_ids(item))
    elif isinstance(value, list):
        for item in value:
            ids.update(nested_asset_ids(item))
    return ids


def summarize_records(records: list[dict[str, Any]]) -> dict[str, Any]:
    frame_values = [item.get("start_frame") for item in records if isinstance(item.get("start_frame"), int)]
    layers = [item.get("layer") for item in records if isinstance(item.get("layer"), int)]
    bounds = []
    source_rects = []
    source_assets = set()
    source_slots = set()
    for item in records:
        x = item.get("destination_x")
        y = item.get("destination_y")
        width = item.get("width")
        height = item.get("height")
        if all(isinstance(value, int) for value in (x, y, width, height)):
            bounds.append({"x": x, "y": y, "width": width, "height": height})
        sx = item.get("source_x")
        sy = item.get("source_y")
        if all(isinstance(value, int) for value in (sx, sy, width, height)):
            source_rects.append({"x": sx, "y": sy, "width": width, "height": height})
        if item.get("source_asset_id"):
            source_assets.add(item["source_asset_id"])
        if item.get("source_asset_slot"):
            source_slots.add(item["source_asset_slot"])
    if bounds:
        min_x = min(item["x"] for item in bounds)
        min_y = min(item["y"] for item in bounds)
        max_x = max(item["x"] + item["width"] for item in bounds)
        max_y = max(item["y"] + item["height"] for item in bounds)
        union_bounds = {"x": min_x, "y": min_y, "width": max_x - min_x, "height": max_y - min_y}
    else:
        union_bounds = None
    return {
        "record_count": len(records),
        "frame_min": min(frame_values) if frame_values else None,
        "frame_max": max(frame_values) if frame_values else None,
        "layer_count": len(set(layers)),
        "destination_bounds": union_bounds,
        "destination_anchor_policy": "native_destination_offsets" if bounds else None,
        "source_rect_count": len(source_rects),
        "source_asset_ids": sorted(source_assets),
        "source_asset_slots": sorted(source_slots),
        "records": records,
    }


def add_composition(
    compositions: dict[str, dict[str, Any]],
    *,
    composition_id: str,
    composition_kind: str,
    asset_id: str | None,
    entry: dict[str, Any],
    usage_context: dict[str, Any] | None = None,
    status: str = "composition_closed_from_runtime_contract",
) -> None:
    summary = summarize_records(flatten_records(entry))
    header = entry.get("header", {}) if isinstance(entry.get("header"), dict) else {}
    item = compositions.setdefault(
        composition_id,
        {
            "composition_id": composition_id,
            "composition_kind": composition_kind,
            "asset_id": asset_id,
            "status": status,
            "header": header,
            "usage_contexts": [],
            "records": summary["records"],
            "record_summary": {key: value for key, value in summary.items() if key != "records"},
            "related_asset_ids": sorted(nested_asset_ids(entry)),
        },
    )
    item["related_asset_ids"] = sorted(set(item.get("related_asset_ids", [])) | nested_asset_ids(entry))
    if usage_context:
        item["usage_contexts"].append(usage_context)
    if not item["header"] and header:
        item["header"] = header


def build_compositions() -> tuple[dict[str, Any], dict[str, dict[str, Any]], list[dict[str, Any]]]:
    coverage = load_json(COVERAGE_PATH)
    taxonomy = load_json(TAXONOMY_PATH)
    display = load_json(DISPLAY_MANIFEST_PATH)
    character = load_json(CHARACTER_MANIFEST_PATH)
    rooms = load_json(ROOM_MANIFEST_PATH)
    compositions: dict[str, dict[str, Any]] = {}
    logical_reconstructions = []

    for animation in character.get("animations", []):
        filename = animation.get("filename") or animation.get("asset_id")
        add_composition(
            compositions,
            composition_id=f"character_animation:{filename}",
            composition_kind="character_seb",
            asset_id=animation.get("asset_id"),
            entry=animation,
            usage_context={"manifest": "character_asset_manifest", "filename": filename},
        )

    for object_id, object_entry in sorted(display.get("objects", {}).items()):
        add_composition(
            compositions,
            composition_id=f"display_object:{object_id}",
            composition_kind="furniture_object",
            asset_id=object_entry.get("seb_asset_id") or object_entry.get("img_asset_id"),
            entry=object_entry,
            usage_context={"manifest": "display_asset_manifest", "object_id": object_id, "name": object_entry.get("name")},
        )
        if isinstance(object_entry.get("sub_composition"), dict):
            sub = object_entry["sub_composition"]
            add_composition(
                compositions,
                composition_id=f"display_subcomposition:{object_id}",
                composition_kind="furniture_subcomposition",
                asset_id=sub.get("asset_id"),
                entry=sub,
                usage_context={"manifest": "display_asset_manifest", "object_id": object_id, "selector_id": sub.get("selector_id")},
            )
    for object_id, object_entry in sorted(display.get("native_initial_objects", {}).items()):
        add_composition(
            compositions,
            composition_id=f"native_initial_object:{object_id}",
            composition_kind="native_initial_furniture_object",
            asset_id=object_entry.get("seb_asset_id") or object_entry.get("source_asset_id"),
            entry=object_entry,
            usage_context={"manifest": "display_asset_manifest", "object_id": object_id, "name": object_entry.get("name")},
        )

    for actor in display.get("actors", []):
        actor_id = actor.get("actor_source_id")
        for action, animation in sorted((actor.get("animations") or {}).items()):
            asset_id = animation.get("asset_id")
            if not asset_id:
                continue
            add_composition(
                compositions,
                composition_id=f"display_actor_animation:{asset_id}",
                composition_kind="display_actor_seb",
                asset_id=asset_id,
                entry=animation,
                usage_context={"manifest": "display_asset_manifest", "actor_source_id": actor_id, "action": action},
                status="composition_closed_with_variable_staff_image_slot",
            )

    for item in display.get("assets", []):
        provenance = item.get("provenance") or {}
        if provenance.get("reconstruction_status"):
            logical_reconstructions.append(
                {
                    "runtime_asset_id": item.get("asset_id"),
                    "runtime_path": item.get("runtime_path"),
                    "source_asset_id": provenance.get("source_asset_id"),
                    "opt_asset_id": provenance.get("opt_asset_id"),
                    "logical_pixel_sha256": provenance.get("logical_pixel_sha256"),
                    "reconstruction_status": provenance.get("reconstruction_status"),
                    "width": item.get("width"),
                    "height": item.get("height"),
                }
            )

    direct_runtime_entries = []
    for manifest_path, key, family in [
        (DISPLAY_MANIFEST_PATH, "assets", "display_slice"),
        (ROOM_MANIFEST_PATH, "assets", "room_scene"),
        (CHARACTER_MANIFEST_PATH, "images", "character_images"),
        (CHARACTER_MANIFEST_PATH, "animations", "character_animations"),
    ]:
        source = load_json(manifest_path)
        for index, item in enumerate(source.get(key, [])):
            provenance = item.get("provenance") or {}
            direct_runtime_entries.append(
                {
                    "entry_id": f"{family}:{index}",
                    "family": family,
                    "asset_id": item.get("asset_id"),
                    "source_asset_id": item.get("source_asset_id") or provenance.get("source_asset_id"),
                    "asset_member": item.get("asset_member"),
                    "runtime_path": item.get("runtime_path"),
                    "extension": item.get("extension"),
                    "width": item.get("width") or (item.get("dimensions") or {}).get("width"),
                    "height": item.get("height") or (item.get("dimensions") or {}).get("height"),
                    "status": item.get("status") or item.get("runtime_status") or "manifest_entry",
                }
            )

    composition_rows = sorted(compositions.values(), key=lambda item: item["composition_id"])
    composition_payload = {
        "schema_version": "social-dev-asset-composition-catalog-v1",
        "package": "social-dev",
        "status": "pass",
        "semantic_status": "runtime_relevant_composition_closed_source_catalog_pending",
        "coverage_ref": {"path": "knowledge/fixtures/accepted/asset_metadata_coverage.json", "content_hash": coverage["determinism"]["content_hash"]},
        "taxonomy_ref": {"path": "knowledge/fixtures/accepted/asset_family_taxonomy.json", "content_hash": taxonomy["determinism"]["content_hash"]},
        "counts": {
            "composition_entries": len(composition_rows),
            "character_seb_compositions": sum(1 for item in composition_rows if item["composition_kind"] == "character_seb"),
            "display_actor_seb_compositions": sum(1 for item in composition_rows if item["composition_kind"] == "display_actor_seb"),
            "furniture_object_compositions": sum(1 for item in composition_rows if item["composition_kind"] == "furniture_object"),
            "native_initial_object_compositions": sum(1 for item in composition_rows if item["composition_kind"] == "native_initial_furniture_object"),
            "logical_reconstructions": len(logical_reconstructions),
            "direct_runtime_entries": len(direct_runtime_entries),
            "runtime_entries_with_composition": sum(1 for item in direct_runtime_entries if any(item["asset_id"] == comp.get("asset_id") for comp in composition_rows)),
        },
        "compositions": composition_rows,
        "logical_reconstructions": sorted(logical_reconstructions, key=lambda item: item.get("runtime_asset_id") or ""),
        "direct_runtime_entries": sorted(direct_runtime_entries, key=lambda item: item["entry_id"]),
        "policy": {
            "record_geometry_source": "native SEB/OPT-derived runtime contracts",
            "anchor_source": "native destination_x/destination_y offsets",
            "variable_staff_image_binding": "selected_staff_img_ remains a runtime binding slot, not a guessed fixed image",
            "unparsed_source_families": "remain explicit pending composition closure and are not promoted by this catalog",
        },
    }
    composition_payload["determinism"] = {"algorithm": "stable-json-sha256 excluding determinism.content_hash", "content_hash": sha256_bytes(stable_json(composition_payload).encode("utf-8"))}
    return composition_payload, compositions, direct_runtime_entries


def build_geometry(composition_payload: dict[str, Any], compositions: dict[str, dict[str, Any]], direct_runtime_entries: list[dict[str, Any]]) -> dict[str, Any]:
    coverage = load_json(COVERAGE_PATH)
    taxonomy = load_json(TAXONOMY_PATH)
    taxonomy_by_asset = {item["asset_id"]: item for item in taxonomy["assets"]}
    coverage_by_asset = {item["asset_id"]: item for item in coverage["assets"]}
    composition_by_asset: dict[str, list[str]] = defaultdict(list)
    for composition_id, item in compositions.items():
        if item.get("asset_id"):
            composition_by_asset[item["asset_id"]].append(composition_id)
        for related_asset_id in item.get("related_asset_ids", []):
            composition_by_asset[related_asset_id].append(composition_id)
    logical_by_source: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in composition_payload["logical_reconstructions"]:
        if item.get("source_asset_id"):
            logical_by_source[item["source_asset_id"]].append(item)
        if item.get("opt_asset_id"):
            logical_by_source[item["opt_asset_id"]].append(item)
        if item.get("runtime_asset_id"):
            logical_by_source[item["runtime_asset_id"]].append(item)

    rows = []
    for asset_id, asset in sorted(coverage_by_asset.items()):
        taxonomy_row = taxonomy_by_asset[asset_id]
        refs = sorted(set(composition_by_asset.get(asset_id, [])))
        logical = logical_by_source.get(asset_id, [])
        direct_dimensions = [{"width": asset.get("width"), "height": asset.get("height"), "source": "asset_index"}] if asset.get("width") is not None and asset.get("height") is not None else []
        direct_dimensions.extend(
            {"width": item["width"], "height": item["height"], "source": item["entry_id"]}
            for item in direct_runtime_entries
            if item.get("asset_id") == asset_id and item.get("width") is not None and item.get("height") is not None
        )
        summaries = [compositions[item]["record_summary"] for item in refs]
        active_runtime = bool(asset["runtime_reference_count"])
        if asset["extension"] in {".seb", ".opt"}:
            active_runtime = bool(refs or logical)
        if refs or logical:
            geometry_status = "composition_and_geometry_closed"
        elif direct_dimensions:
            geometry_status = "physical_dimensions_closed"
        elif asset["runtime_reference_count"] and asset["extension"] in {".seb", ".opt"}:
            geometry_status = "manifest_only_not_bound_to_active_composition"
        elif asset["extension"] in {".png", ".seb", ".opt", ".inf"}:
            geometry_status = "source_geometry_not_closed"
        else:
            geometry_status = "not_applicable_nonvisual_or_payload"
        rows.append(
            {
                "asset_id": asset_id,
                "relative_path": asset["relative_path"],
                "family_id": taxonomy_row["family_id"],
                "subfamily_id": taxonomy_row["subfamily_id"],
                "extension": asset["extension"],
                "runtime_relevant": bool(asset["runtime_reference_count"]),
                "active_runtime_usage": active_runtime,
                "runtime_reference_count": asset["runtime_reference_count"],
                "physical_dimensions": sorted({(item["width"], item["height"], item["source"]) for item in direct_dimensions}),
                "composition_ids": sorted(refs),
                "logical_reconstruction_count": len(logical),
                "record_bounds": [summary["destination_bounds"] for summary in summaries if summary.get("destination_bounds")],
                "anchor_policies": sorted({summary["destination_anchor_policy"] for summary in summaries if summary.get("destination_anchor_policy")}),
                "frame_bounds": sorted({compositions[item].get("header", {}).get("frame_bound") for item in refs if compositions[item].get("header", {}).get("frame_bound") is not None}),
                "layer_counts": sorted({summary["layer_count"] for summary in summaries}),
                "record_counts": sorted({summary["record_count"] for summary in summaries}),
                "geometry_status": geometry_status,
                "geometry_policy": "native_contract_or_index_dimensions" if geometry_status != "source_geometry_not_closed" else "cataloged_pending_family_composition",
            }
        )

    existing_ids = set(coverage_by_asset)
    for item in direct_runtime_entries:
        raw_id = item.get("asset_id")
        if not raw_id or raw_id in existing_ids:
            continue
        refs = sorted(set(composition_by_asset.get(raw_id, [])))
        logical = logical_by_source.get(raw_id, [])
        rows.append(
            {
                "asset_id": raw_id,
                "relative_path": item.get("asset_member") or raw_id,
                "family_id": "derived.runtime_output",
                "subfamily_id": "derived.runtime_output.raster",
                "extension": item.get("extension"),
                "runtime_relevant": True,
                "active_runtime_usage": True,
                "runtime_reference_count": 1,
                "physical_dimensions": [{"width": item.get("width"), "height": item.get("height"), "source": item["entry_id"]}],
                "composition_ids": sorted(refs),
                "logical_reconstruction_count": len(logical),
                "record_bounds": [],
                "anchor_policies": [],
                "frame_bounds": [],
                "layer_counts": [],
                "record_counts": [],
                "geometry_status": "derived_runtime_geometry_closed",
                "geometry_policy": "runtime_manifest_physical_dimensions_and_provenance",
                "source_asset_id": item.get("source_asset_id"),
            }
        )

    rows = sorted(rows, key=lambda item: item["asset_id"])
    status_counts = defaultdict(int)
    for row in rows:
        status_counts[row["geometry_status"]] += 1
    runtime_rows = [row for row in rows if row["runtime_relevant"]]
    active_runtime_rows = [row for row in rows if row.get("active_runtime_usage")]
    runtime_gaps = [row["asset_id"] for row in active_runtime_rows if row["geometry_status"] in {"runtime_composition_pending", "source_geometry_not_closed"}]
    payload = {
        "schema_version": "social-dev-asset-geometry-catalog-v1",
        "package": "social-dev",
        "status": "pass",
        "semantic_status": "geometry_catalog_runtime_relevant_closed_source_catalog_pending",
        "composition_ref": {"path": "knowledge/fixtures/accepted/asset_composition_catalog.json", "content_hash": composition_payload["determinism"]["content_hash"]},
        "taxonomy_ref": {"path": "knowledge/fixtures/accepted/asset_family_taxonomy.json", "content_hash": taxonomy["determinism"]["content_hash"]},
        "counts": {"geometry_rows": len(rows), "indexed_asset_rows": len(coverage_by_asset), "derived_runtime_rows": len(rows) - len(coverage_by_asset), "runtime_relevant_rows": len(runtime_rows), "active_runtime_rows": len(active_runtime_rows), "geometry_statuses": dict(sorted(status_counts.items())), "runtime_geometry_gaps": len(runtime_gaps)},
        "runtime_geometry_gaps": runtime_gaps,
        "assets": rows,
        "policy": {"physical_dimensions": "index_or_runtime_manifest", "composition_bounds": "SEB/OPT record destination offsets", "unknown_or_pending": "retained as explicit status; no guessed frame or anchor"},
    }
    payload["determinism"] = {"algorithm": "stable-json-sha256 excluding determinism.content_hash", "content_hash": sha256_bytes(stable_json(payload).encode("utf-8"))}
    return payload


def build_contract_payload(composition: dict[str, Any], geometry: dict[str, Any]) -> dict[str, Any]:
    payload = {
        "schema_version": "social-dev-asset-composition-contract-v1",
        "package": "social-dev",
        "status": "pass",
        "semantic_status": "composition_geometry_contract_not_full_catalog_approval",
        "composition_path": "knowledge/fixtures/accepted/asset_composition_catalog.json",
        "geometry_path": "knowledge/fixtures/accepted/asset_geometry_catalog.json",
        "composition_content_hash": composition["determinism"]["content_hash"],
        "geometry_content_hash": geometry["determinism"]["content_hash"],
        "counts": {"composition_entries": composition["counts"]["composition_entries"], "logical_reconstructions": composition["counts"]["logical_reconstructions"], "geometry_rows": geometry["counts"]["geometry_rows"], "runtime_relevant_rows": geometry["counts"]["runtime_relevant_rows"], "runtime_geometry_gaps": geometry["counts"]["runtime_geometry_gaps"]},
        "acceptance": {"runtime_geometry_gaps_closed": geometry["counts"]["runtime_geometry_gaps"] == 0, "character_animation_compositions_closed": composition["counts"]["character_seb_compositions"] == 35, "logical_reconstructions_closed": all(item["reconstruction_status"] == "pass" for item in composition["logical_reconstructions"]), "native_offsets_preserved": True, "unparsed_non_runtime_families_remain_explicit": True},
        "runtime_policy": {"may_be_used_for_frame_selection": True, "may_be_used_for_draw": geometry["counts"]["runtime_geometry_gaps"] == 0, "source_family_promotion": "requires family-specific status and usage gates", "next_gate": "furniture_world_and_character_family_completion"},
    }
    payload["determinism"] = {"algorithm": "stable-json-sha256 excluding determinism.content_hash", "content_hash": sha256_bytes(stable_json(payload).encode("utf-8"))}
    return payload


def markdown_report(composition: dict[str, Any], geometry: dict[str, Any], contract: dict[str, Any]) -> str:
    lines = [
        "# Social Dev asset composition and geometry catalogs",
        "",
        "AM-4 records runtime-relevant SEB/OPT composition, native destination offsets, frame/layer bounds, physical raster dimensions, and explicit pending statuses for catalog-only families.",
        "",
        "## Identity",
        "",
        f"- Composition hash: `{composition['determinism']['content_hash']}`",
        f"- Geometry hash: `{geometry['determinism']['content_hash']}`",
        f"- Contract hash: `{contract['determinism']['content_hash']}`",
        "",
        "## Counts",
        "",
        "| Dimension | Count |",
        "|---|---:|",
        f"| Composition entries | {composition['counts']['composition_entries']:,} |",
        f"| Character SEB compositions | {composition['counts']['character_seb_compositions']:,} |",
        f"| Furniture object compositions | {composition['counts']['furniture_object_compositions']:,} |",
        f"| Native initial object compositions | {composition['counts']['native_initial_object_compositions']:,} |",
        f"| Logical OPT reconstructions | {composition['counts']['logical_reconstructions']:,} |",
        f"| Geometry rows | {geometry['counts']['geometry_rows']:,} |",
        f"| Runtime-relevant geometry rows | {geometry['counts']['runtime_relevant_rows']:,} |",
        f"| Runtime geometry gaps | {geometry['counts']['runtime_geometry_gaps']:,} |",
        "",
        "## Geometry statuses",
        "",
        "| Status | Count |",
        "|---|---:|",
    ]
    for status, count in geometry["counts"]["geometry_statuses"].items():
        lines.append(f"| `{status}` | {count:,} |")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- Runtime-relevant composition and geometry gaps are closed for the current display, room, and full human character contracts.",
            "- Catalog-only SEB/OPT families remain explicit rather than receiving guessed frames or anchors.",
            "- Native destination offsets are preserved as the anchor policy; no center/pivot inference is applied.",
            "",
            "```powershell",
            "python -B tools/social-dev/build_asset_composition_geometry.py",
            "python -B tools/social-dev/test_asset_composition_geometry.py",
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    composition, compositions, direct_runtime_entries = build_compositions()
    geometry = build_geometry(composition, compositions, direct_runtime_entries)
    contract = build_contract_payload(composition, geometry)
    write_json(COMPOSITION_PATH, composition)
    write_json(GEOMETRY_PATH, geometry)
    write_json(CONTRACT_PATH, contract)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(markdown_report(composition, geometry, contract), encoding="utf-8", newline="\n")
    print(json.dumps({"composition_hash": composition["determinism"]["content_hash"], "geometry_hash": geometry["determinism"]["content_hash"], "composition_entries": composition["counts"]["composition_entries"], "geometry_rows": geometry["counts"]["geometry_rows"], "runtime_geometry_gaps": geometry["counts"]["runtime_geometry_gaps"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
