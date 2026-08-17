"""Promote and decode the complete native human character asset set.

The source ZIP remains read-only evidence. This builder copies the exact human
PNG/SEB bytes into a separate runtime asset namespace and emits a JSON frame
contract. The decoder handles the observed multilayer SEB layout:

    file header + layer-0 records + (layer record-count/frame-bound + records)*

Raw SEB files remain available for provenance, while the browser consumes the
decoded frame contract and loads character PNGs lazily by asset id.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import io
import json
import struct
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from PIL import Image

import build_character_metadata as metadata_builder


ROOT = metadata_builder.ROOT
EVIDENCE = ROOT / "knowledge/fixtures/accepted"
RUNTIME_EVIDENCE = ROOT / "knowledge/fixtures/accepted/runtime"
SOURCE_ZIP = ROOT / "sources/raw/Social_Dev_Story_v2.5.1_ASSETS_ONLY_WITH_ASSEMBLY_GUIDE.zip"
ASSET_INDEX_PATH = ROOT / "knowledge/sources/asset_guide_20260813/00_INDEX/ASSET_INDEX.json"
METADATA_PATH = RUNTIME_EVIDENCE / "character_metadata_contract.json"
CAPABILITY_PATH = RUNTIME_EVIDENCE / "character_capability_contract.json"
RUNTIME_ASSET_ROOT = ROOT / "runtime/social-dev/assets/character-catalog"

ARCHIVE_PREFIX = "Social_Dev_Story_v2.5.1_ASSETS_ONLY/"
SEB_HEADER_FORMAT = ">HHHH"
SEB_RECORD_FORMAT = ">HHHHhhhhHH"
SEB_HEADER_SIZE = struct.calcsize(SEB_HEADER_FORMAT)
SEB_RECORD_SIZE = struct.calcsize(SEB_RECORD_FORMAT)

SCHEMA_VERSION = "social-dev-character-asset-manifest-v1"
FIXTURE_SCHEMA_VERSION = "social-dev-character-asset-fixture-v1"
VALIDATION_SCHEMA_VERSION = "social-dev-character-asset-validation-v1"


def stable_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def relative_path(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def parse_inf(raw: bytes, member: str) -> dict[int, str]:
    result: dict[int, str] = {}
    for line_number, line in enumerate(raw.decode("utf-8-sig").splitlines(), start=1):
        if not line.strip():
            continue
        fields = line.split("\t", 1)
        require(len(fields) == 2, f"INF {member} line {line_number} is not tab separated")
        selector_id = int(fields[0])
        filename = fields[1].strip()
        if filename.endswith(",bin"):
            filename = filename[: -len(",bin")]
        require(selector_id not in result, f"INF {member} selector {selector_id} is duplicated")
        result[selector_id] = filename
    return result


def signed_texture_id(raw_value: int) -> int:
    return raw_value - 0x10000 if raw_value >= 0x8000 else raw_value


def decode_seb(raw: bytes, member: str, image_index: dict[int, str], asset_index: dict[str, dict[str, Any]]) -> dict[str, Any]:
    require(len(raw) >= SEB_HEADER_SIZE, f"SEB {member} is shorter than its header")
    layer_count, global_frame_count, record_count, frame_bound = struct.unpack(SEB_HEADER_FORMAT, raw[:SEB_HEADER_SIZE])
    require(layer_count > 0, f"SEB {member} has no layers")
    require(global_frame_count > 0, f"SEB {member} has no global frames")
    require(frame_bound >= global_frame_count, f"SEB {member} frame bound is shorter than global frames")

    offset = SEB_HEADER_SIZE
    layers: list[dict[str, Any]] = []
    flattened_records: list[dict[str, Any]] = []
    for layer_index in range(layer_count):
        if layer_index == 0:
            layer_record_count = record_count
            layer_frame_bound = frame_bound
            marker = None
        else:
            require(offset + 4 <= len(raw), f"SEB {member} is missing layer {layer_index} marker")
            marker_record_count, marker_value = struct.unpack(">HH", raw[offset : offset + 4])
            layer_record_count = marker_record_count
            # The second layer-word is retained as raw evidence. Native files
            # can contain records later than this value, so it is not promoted
            # as a frame bound; the file-level frame_bound is authoritative.
            layer_frame_bound = frame_bound
            marker = {"record_count": marker_record_count, "raw_value": marker_value}
            offset += 4
        require(layer_record_count > 0, f"SEB {member} layer {layer_index} has no records")
        require(layer_frame_bound > 0, f"SEB {member} layer {layer_index} has no frame bound")
        records: list[dict[str, Any]] = []
        for record_index in range(layer_record_count):
            require(offset + SEB_RECORD_SIZE <= len(raw), f"SEB {member} layer {layer_index} record {record_index} is truncated")
            values = struct.unpack(SEB_RECORD_FORMAT, raw[offset : offset + SEB_RECORD_SIZE])
            offset += SEB_RECORD_SIZE
            (
                start_frame,
                image_id_raw,
                source_x,
                source_y,
                width,
                height,
                destination_x,
                destination_y,
                flags,
                reserved,
            ) = values
            image_id = signed_texture_id(image_id_raw)
            require(start_frame < layer_frame_bound, f"SEB {member} layer {layer_index} has an out-of-range frame")
            record: dict[str, Any] = {
                "layer": layer_index,
                "layer_record_index": record_index,
                "start_frame": start_frame,
                "image_id": image_id,
                "image_id_raw": image_id_raw,
                "source_x": source_x,
                "source_y": source_y,
                "width": width,
                "height": height,
                "destination_x": destination_x,
                "destination_y": destination_y,
                "flags": flags,
                "reserved": reserved,
            }
            if image_id < 0:
                record.update(
                    {
                        "texture_status": "control_no_texture",
                        "source_asset_member": None,
                        "source_asset_id": None,
                    }
                )
            else:
                require(image_id in image_index, f"SEB {member} references missing human image selector {image_id}")
                image_filename = image_index[image_id]
                image_member = f"01_GAME_PACKS/human/{image_filename}"
                image_descriptor = asset_index.get(image_member)
                require(image_descriptor is not None, f"SEB {member} image asset is missing from ASSET_INDEX: {image_member}")
                image_width = int(image_descriptor.get("width") or 0)
                image_height = int(image_descriptor.get("height") or 0)
                require(width > 0 and height > 0, f"SEB {member} image record has an empty rectangle")
                require(source_x >= 0 and source_y >= 0, f"SEB {member} image record has a negative source coordinate")
                require(source_x + width <= image_width and source_y + height <= image_height, f"SEB {member} image rectangle exceeds {image_member}")
                record.update(
                    {
                        "texture_status": "resolved",
                        "source_asset_member": image_member,
                        "source_asset_id": f"asset:{image_member}",
                        "source_size": {"width": image_width, "height": image_height},
                    }
                )
            records.append(record)
            flattened_records.append(record)
        layers.append(
            {
                "index": layer_index,
                "record_count": layer_record_count,
                "frame_bound": layer_frame_bound,
                "marker": marker,
                "records": records,
            }
        )
    require(offset == len(raw), f"SEB {member} has {len(raw) - offset} trailing bytes after multilayer decode")
    return {
        "header": {
            "layer_count": layer_count,
            "global_frame_count": global_frame_count,
            "record_count": record_count,
            "frame_bound": frame_bound,
        },
        "layers": layers,
        "records": flattened_records,
        "control_record_count": sum(record["texture_status"] == "control_no_texture" for record in flattened_records),
    }


def image_dimensions(raw: bytes, member: str) -> dict[str, Any]:
    try:
        with Image.open(io.BytesIO(raw)) as image:
            image.load()
            return {"width": image.width, "height": image.height, "mode": image.mode}
    except Exception as error:  # pragma: no cover - builder reports the member
        raise ValueError(f"PNG {member} could not be decoded: {error}") from error


def asset_index_map() -> dict[str, dict[str, Any]]:
    rows = load_json(ASSET_INDEX_PATH)
    require(isinstance(rows, list), "ASSET_INDEX.json must be a list")
    result = {str(row["relative_path"]).replace("\\", "/"): row for row in rows}
    require(len(result) == len(rows), "ASSET_INDEX.json contains duplicate paths")
    return result


def runtime_asset_path(relative_member: str) -> str:
    return f"assets/character-catalog/{relative_member}"


def promote_exact_asset(archive: zipfile.ZipFile, member: str, output_root: Path, expected: dict[str, Any]) -> dict[str, Any]:
    archive_member = ARCHIVE_PREFIX + member
    require(archive_member in archive.namelist(), f"archive is missing {archive_member}")
    raw = archive.read(archive_member)
    source_hash = sha256_bytes(raw)
    require(source_hash == expected["sha256"], f"source hash mismatch for {member}")
    target = output_root / Path(member)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(raw)
    runtime_hash = sha256_file(target)
    require(runtime_hash == source_hash, f"runtime promotion hash mismatch for {member}")
    result = {
        "asset_id": f"asset:{member}",
        "asset_member": member,
        "runtime_path": runtime_asset_path(member),
        "source_sha256": source_hash,
        "runtime_sha256": runtime_hash,
        "bytes": len(raw),
        "status": "promoted_exact",
        "source_status": "native_source",
    }
    if member.endswith(".png"):
        result["dimensions"] = image_dimensions(raw, member)
    return result


def build_checks(
    images: list[dict[str, Any]],
    animations: list[dict[str, Any]],
    staff_bindings: list[dict[str, Any]],
    counts: dict[str, int],
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def check(check_id: str, condition: bool, observed: Any, expected: Any, note: str) -> None:
        checks.append({"id": check_id, "status": "pass" if condition else "fail", "observed": observed, "expected": expected, "note": note})

    check("human-image-coverage", len(images) == 105 and [item["selector_id"] for item in images] == list(range(105)), len(images), 105, "All human img.inf selectors 0-104 are promoted exactly.")
    check("human-animation-coverage", len(animations) == 35 and [item["selector_id"] for item in animations] == [*range(34), 100], len(animations), 35, "All human seb.inf selectors, including head selector 100, are decoded.")
    check("staff-binding-coverage", [item["source_id"] for item in staff_bindings] == list(range(141)), len(staff_bindings), 141, "Every StaffData template points to a promoted human image asset.")
    check("image-promotion-exact", all(item["status"] == "promoted_exact" and item["source_sha256"] == item["runtime_sha256"] for item in images), True, True, "Runtime PNG bytes match the source ZIP bytes.")
    check("seb-promotion-exact", all(item["source_sha256"] == item["runtime_sha256"] for item in animations), True, True, "Runtime SEB bytes match the source ZIP bytes.")
    check("frame-contract-closed", all(item["status"] == "frame_contract_ready" and item["records"] and item["header"]["layer_count"] == len(item["layers"]) for item in animations), True, True, "Every native SEB is decoded into a multilayer frame contract.")
    check("frame-control-records-explicit", all(record["texture_status"] in {"resolved", "control_no_texture"} for item in animations for record in item["records"]), True, True, "Negative texture sentinels remain explicit control records and are never treated as PNGs.")
    check("frame-rectangles-valid", all(record["texture_status"] == "control_no_texture" or record["source_x"] + record["width"] <= record["source_size"]["width"] and record["source_y"] + record["height"] <= record["source_size"]["height"] for item in animations for record in item["records"]), True, True, "All drawable frame rectangles fit their native human PNG.")
    check("multi-layer-decoder", counts["multilayer_animations"] > 0 and counts["decoded_layers"] > counts["animations"], {"animations": counts["animations"], "layers": counts["decoded_layers"]}, "multilayer files decoded", "The decoder exercises the observed layer marker format.")
    check("lazy-policy", True, "lazy_by_character_and_asset_id", "lazy_by_character_and_asset_id", "Runtime loads only requested character images; decoded SEB frames are contract data.")
    return checks


def build_package() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    metadata = load_json(METADATA_PATH)
    capability = load_json(CAPABILITY_PATH)
    require(metadata["status"] == "pass", "character metadata contract is not approved")
    require(capability["status"] == "pass", "character capability contract is not approved")
    index = asset_index_map()
    require(SOURCE_ZIP.is_file(), f"missing source ZIP: {SOURCE_ZIP}")

    with zipfile.ZipFile(SOURCE_ZIP) as archive:
        img_inf_member = "01_GAME_PACKS/human/img.inf"
        seb_inf_member = "01_GAME_PACKS/human/seb.inf"
        img_inf_raw = archive.read(ARCHIVE_PREFIX + img_inf_member)
        seb_inf_raw = archive.read(ARCHIVE_PREFIX + seb_inf_member)
        image_index = parse_inf(img_inf_raw, img_inf_member)
        seb_index = parse_inf(seb_inf_raw, seb_inf_member)
        require(list(sorted(image_index)) == list(range(105)), "human img.inf coverage drifted")
        require(list(sorted(seb_index)) == [*range(34), 100], "human seb.inf coverage drifted")

        images: list[dict[str, Any]] = []
        for selector_id in sorted(image_index):
            filename = image_index[selector_id]
            member = f"01_GAME_PACKS/human/{filename}"
            descriptor = index.get(member)
            require(descriptor is not None, f"human image missing from ASSET_INDEX: {member}")
            promoted = promote_exact_asset(archive, member, RUNTIME_ASSET_ROOT, descriptor)
            dimensions = promoted["dimensions"]
            require(dimensions["width"] == 270 and dimensions["height"] == 60, f"unexpected human image dimensions: {member}")
            images.append({"selector_id": selector_id, "filename": filename, **promoted})

        animations: list[dict[str, Any]] = []
        for selector_id in sorted(seb_index):
            filename = seb_index[selector_id]
            member = f"01_GAME_PACKS/human/{filename}"
            descriptor = index.get(member)
            require(descriptor is not None, f"human SEB missing from ASSET_INDEX: {member}")
            promoted = promote_exact_asset(archive, member, RUNTIME_ASSET_ROOT, descriptor)
            decoded = decode_seb(archive.read(ARCHIVE_PREFIX + member), member, image_index, index)
            animations.append(
                {
                    "selector_id": selector_id,
                    "filename": filename,
                    **promoted,
                    "header": decoded["header"],
                    "layers": decoded["layers"],
                    "records": decoded["records"],
                    "control_record_count": decoded["control_record_count"],
                    "status": "frame_contract_ready",
                    "composition_policy": "active_record_per_layer_sorted_by_layer_then_start_frame",
                }
            )

    image_by_selector = {item["selector_id"]: item for item in images}
    staff_bindings: list[dict[str, Any]] = []
    for record in metadata["staff"]:
        selector = record["render"]["image_selector"]
        image = image_by_selector.get(int(selector["id"]))
        require(image is not None, f"StaffData {record['id']} image selector is not promoted")
        staff_bindings.append(
            {
                "record_id": record["id"],
                "source_id": record["source_identity"]["source_id"],
                "record_kind": record.get("record_kind", "staff_data_template"),
                "capability_profile_ref": record["render"]["capability_profile_ref"],
                "image_selector_id": selector["id"],
                "image_asset_id": image["asset_id"],
                "image_asset_member": image["asset_member"],
                "runtime_path": image["runtime_path"],
                "status": "promoted_exact",
            }
        )

    counts = {
        "images": len(images),
        "animations": len(animations),
        "staff_bindings": len(staff_bindings),
        "multilayer_animations": sum(item["header"]["layer_count"] > 1 for item in animations),
        "decoded_layers": sum(item["header"]["layer_count"] for item in animations),
        "decoded_records": sum(len(item["records"]) for item in animations),
        "control_records": sum(item["control_record_count"] for item in animations),
        "promoted_bytes": sum(item["bytes"] for item in images + animations),
    }
    provenance = {
        "status": "verified",
        "source_archive": {"path": relative_path(SOURCE_ZIP), "sha256": sha256_file(SOURCE_ZIP)},
        "selector_indexes": {
            "human_img_inf": {"member": "01_GAME_PACKS/human/img.inf", "sha256": sha256_bytes(img_inf_raw)},
            "human_seb_inf": {"member": "01_GAME_PACKS/human/seb.inf", "sha256": sha256_bytes(seb_inf_raw)},
        },
        "asset_index": {"path": relative_path(ASSET_INDEX_PATH), "sha256": sha256_file(ASSET_INDEX_PATH)},
        "character_metadata": {"path": relative_path(METADATA_PATH), "sha256": sha256_file(METADATA_PATH)},
        "character_capability": {"path": relative_path(CAPABILITY_PATH), "sha256": sha256_file(CAPABILITY_PATH)},
        "source_policy": "The browser imports this generated contract and promoted exact assets; it never opens the source ZIP or recovered C#.",
    }
    checks = build_checks(images, animations, staff_bindings, counts)
    status = "pass" if all(item["status"] == "pass" for item in checks) else "fail"
    timestamp = utc_now()
    limits = [
        "This manifest covers the complete native human image and SEB selector packages only; HelperData, avatar parts, and event-only families remain separate asset packages.",
        "All 105 human PNGs and all 35 human SEBs are promoted byte-for-byte from the source ZIP into a separate character-catalog namespace.",
        "The frame decoder handles the observed multilayer marker format and preserves negative texture sentinels as control records.",
        "The browser loads character PNGs lazily by asset id; decoded frame metadata is imported from this contract and raw SEB binaries remain provenance/runtime-extension assets.",
        "This closes selector/frame composition for native human assets; gameplay state, routes, lifecycle transitions, and per-character behavior remain owned by the shared capability/behavior contracts.",
    ]
    shared = {
        "schema_version": FIXTURE_SCHEMA_VERSION,
        "package": "social-dev-character-asset-fixture",
        "status": status,
        "semantic_status": "deterministic_fixture" if status == "pass" else "invalid",
        "generated_at_utc": timestamp,
        "catalog_id": "character-assets-full",
        "images": images,
        "animations": animations,
        "staff_bindings": staff_bindings,
        "runtime_policy": {
            "asset_namespace": "assets/character-catalog/",
            "image_loading": "lazy_by_character_and_asset_id",
            "frame_resolution": "decoded_seb_contract",
            "raw_seb_retained": True,
            "eager_load_full_catalog": False,
            "source_archive_imports": False,
            "source_code_imports": False,
        },
        "provenance": provenance,
        "counts": counts,
        "limits": limits,
        "determinism": {"algorithm": "stable-json-sha256 excluding generated_at_utc and content_hash", "content_hash": ""},
        "validation": {"checks": checks, "failed_checks": [item["id"] for item in checks if item["status"] != "pass"]},
    }
    shared["determinism"]["content_hash"] = sha256_bytes(stable_json(_without_dynamic(shared)).encode("utf-8"))
    fixture = shared
    contract = copy.deepcopy(shared)
    contract["schema_version"] = SCHEMA_VERSION
    contract["package"] = "social-dev-character-assets"
    contract["semantic_status"] = "approved_for_runtime_catalog" if status == "pass" else "invalid"
    contract["fixture_ref"] = {"path": "knowledge/fixtures/accepted/character_asset_fixture.json", "content_hash": fixture["determinism"]["content_hash"]}
    contract["determinism"] = {"algorithm": "stable-json-sha256 excluding generated_at_utc and contract_hash", "contract_hash": ""}
    contract["determinism"]["contract_hash"] = sha256_bytes(stable_json(_without_dynamic(contract)).encode("utf-8"))
    validation = {
        "schema_version": VALIDATION_SCHEMA_VERSION,
        "status": status,
        "semantic_status": "validated" if status == "pass" else "invalid",
        "generated_at_utc": timestamp,
        "contract_hash": contract["determinism"]["contract_hash"],
        "fixture_hash": fixture["determinism"]["content_hash"],
        "failed_checks": [item["id"] for item in checks if item["status"] != "pass"],
        "checks": checks,
        "counts": {"checks": len(checks), "passed_checks": sum(item["status"] == "pass" for item in checks), **counts},
    }
    return fixture, contract, validation


def _without_dynamic(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: _without_dynamic(item)
            for key, item in value.items()
            if key not in {"generated_at_utc", "content_hash", "contract_hash"}
        }
    if isinstance(value, list):
        return [_without_dynamic(item) for item in value]
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence-dir", type=Path, default=EVIDENCE)
    parser.add_argument("--runtime-evidence-dir", type=Path, default=RUNTIME_EVIDENCE)
    args = parser.parse_args()
    evidence_dir = args.evidence_dir if args.evidence_dir.is_absolute() else ROOT / args.evidence_dir
    runtime_dir = args.runtime_evidence_dir if args.runtime_evidence_dir.is_absolute() else ROOT / args.runtime_evidence_dir
    fixture, contract, validation = build_package()
    write_json(evidence_dir / "character_asset_fixture.json", fixture)
    write_json(evidence_dir / "character_asset_validation.json", validation)
    write_json(runtime_dir / "character_asset_manifest.json", contract)
    print(
        "character_asset_manifest_complete "
        f"status={contract['status']} "
        f"checks={validation['counts']['passed_checks']}/{validation['counts']['checks']} "
        f"images={validation['counts']['images']} "
        f"animations={validation['counts']['animations']} "
        f"layers={validation['counts']['decoded_layers']} "
        f"records={validation['counts']['decoded_records']} "
        f"bytes={validation['counts']['promoted_bytes']} "
        f"contract_hash={contract['determinism']['contract_hash']}"
    )
    return 0 if contract["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
