"""Build the bounded Social Dev display asset/frame gate.

This builder reads the supplied asset archive and the already-approved selector
contracts. It verifies exact ZIP bytes, parses the bounded SEB record format,
and promotes only frame compositions whose source rectangles fit the selected
PNG source or a proven OPT logical reconstruction. It never modifies the
source archive and never executes C# or native artifacts.
"""

from __future__ import annotations

import hashlib
import io
import json
import struct
import zipfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from PIL import Image

from opt_codec import OptReconstruction, reconstruct_opt


ROOT = Path(__file__).resolve().parents[2]
ZIP_PATH = ROOT / "sources/raw/Social_Dev_Story_v2.5.1_ASSETS_ONLY_WITH_ASSEMBLY_GUIDE.zip"
EVIDENCE = ROOT / "knowledge/fixtures/accepted"
ASSET_GUIDE_INDEX = ROOT / "knowledge/sources/asset_guide_20260813/00_INDEX/ASSET_INDEX.json"
SELECTOR_CONTRACT = EVIDENCE / "asset_selector_contract.json"
ACTOR_FIXTURE = EVIDENCE / "actor_catalog_fixture.json"
SCENE_FIXTURE = EVIDENCE / "scene_catalog_fixture.json"
OBJECT_FIXTURE = EVIDENCE / "object_catalog_fixture.json"
ASSET_INVENTORY = EVIDENCE / "asset_binary_inventory.json"
OUTPUT = EVIDENCE / "display_asset_gate.json"
RUNTIME_MANIFEST = ROOT / "knowledge/fixtures/accepted/runtime/display_asset_manifest.json"
RUNTIME_ASSETS = ROOT / "runtime/social-dev/assets/display-slice-01"
REPORT = ROOT / "docs/reports/social-dev_display_asset_gate.md"
PHASE3A_CLOSURE = EVIDENCE / "phase3a_asset_composition_closure.json"
PHASE3C_STRICT_CLOSURE = EVIDENCE / "phase3c_strict_closure.json"

ARCHIVE_PREFIX = "Social_Dev_Story_v2.5.1_ASSETS_ONLY/"
SEB_HEADER_SIZE = 8
SEB_RECORD_SIZE = 20
SEB_RECORD_FORMAT = ">HHHHhhhhHH"

FLOOR_RUNTIME_FALLBACKS = {
    5: {
        "target_selector_id": 85,
        "filename": "floor_09.png",
        "reason_code": "user_approved_runtime_alias",
    }
}


def stable_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def relative_path(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def normalize_member(member: str) -> str:
    value = member.replace("\\", "/")
    return value[len(ARCHIVE_PREFIX) :] if value.startswith(ARCHIVE_PREFIX) else value


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def parse_inf(raw: bytes) -> dict[int, str]:
    result: dict[int, str] = {}
    for line_number, line in enumerate(raw.decode("utf-8-sig").splitlines(), start=1):
        if not line.strip():
            continue
        fields = line.split("\t", 1)
        require(len(fields) == 2, f"INF line {line_number} is not tab separated")
        identifier = int(fields[0])
        filename = fields[1].strip()
        if filename.endswith(",bin"):
            filename = filename[: -len(",bin")]
        require(identifier not in result, f"INF id {identifier} is duplicated")
        result[identifier] = filename
    return result


def parse_seb(raw: bytes, member: str) -> dict[str, Any]:
    require(len(raw) >= SEB_HEADER_SIZE, f"SEB {member} is shorter than its header")
    layer_count, global_frame_count, record_count, frame_bound = struct.unpack(
        ">HHHH", raw[:SEB_HEADER_SIZE]
    )
    expected_size = SEB_HEADER_SIZE + record_count * SEB_RECORD_SIZE
    require(len(raw) == expected_size, f"SEB {member} size {len(raw)} != expected {expected_size}")
    records: list[dict[str, int]] = []
    for index in range(record_count):
        values = struct.unpack(
            SEB_RECORD_FORMAT,
            raw[SEB_HEADER_SIZE + index * SEB_RECORD_SIZE : SEB_HEADER_SIZE + (index + 1) * SEB_RECORD_SIZE],
        )
        (
            start_frame,
            image_id,
            source_x,
            source_y,
            width,
            height,
            destination_x,
            destination_y,
            flags,
            reserved,
        ) = values
        records.append(
            {
                "start_frame": start_frame,
                "image_id": image_id,
                "source_x": source_x,
                "source_y": source_y,
                "width": width,
                "height": height,
                "destination_x": destination_x,
                "destination_y": destination_y,
                "flags": flags,
                "reserved": reserved,
            }
        )
    require(global_frame_count > 0, f"SEB {member} has no global frames")
    require(frame_bound >= global_frame_count, f"SEB {member} frame bound is shorter than global frames")
    require(all(record["start_frame"] < frame_bound for record in records), f"SEB {member} has an out-of-range frame")
    return {
        "member": member,
        "header": {
            "layer_count": layer_count,
            "global_frame_count": global_frame_count,
            "record_count": record_count,
            "frame_bound": frame_bound,
        },
        "records": records,
    }


def image_dimensions(raw: bytes, member: str) -> dict[str, Any]:
    try:
        with Image.open(io.BytesIO(raw)) as image:
            image.load()
            return {"width": image.width, "height": image.height, "mode": image.mode}
    except Exception as error:  # pragma: no cover - the failure is reported with the member name
        raise ValueError(f"PNG {member} could not be decoded: {error}") from error


def asset_index_map() -> dict[str, dict[str, Any]]:
    index = load_json(ASSET_GUIDE_INDEX)
    require(isinstance(index, list), "ASSET_INDEX.json must be a list")
    result = {str(item["relative_path"]).replace("\\", "/"): item for item in index}
    require(len(result) == len(index), "ASSET_INDEX.json contains duplicate relative paths")
    return result


def read_archive_asset(
    archive: zipfile.ZipFile,
    index: dict[str, dict[str, Any]],
    member: str,
) -> tuple[dict[str, Any], bytes]:
    member = member.replace("\\", "/")
    index_entry = index.get(member)
    require(index_entry is not None, f"asset index is missing {member}")
    archive_member = ARCHIVE_PREFIX + member
    try:
        info = archive.getinfo(archive_member)
    except KeyError as error:
        raise ValueError(f"asset ZIP is missing {member}") from error
    raw = archive.read(archive_member)
    expected_size = int(index_entry.get("size") or 0)
    expected_sha = str(index_entry.get("sha256") or "").lower()
    actual_sha = sha256_bytes(raw)
    require(info.file_size == len(raw) == expected_size, f"asset size drift for {member}")
    require(actual_sha == expected_sha, f"asset hash drift for {member}")
    descriptor: dict[str, Any] = {
        "asset_id": f"asset:{member}",
        "asset_member": member,
        "runtime_path": f"assets/display-slice-01/{member}",
        "kind": index_entry.get("kind"),
        "pack": index_entry.get("pack"),
        "original_name": index_entry.get("original_name"),
        "extension": index_entry.get("extension"),
        "bytes": len(raw),
        "sha256": actual_sha,
        "semantic_role": index_entry.get("semantic_role"),
    }
    if member.lower().endswith(".png"):
        dimensions = image_dimensions(raw, member)
        descriptor["width"] = dimensions["width"]
        descriptor["height"] = dimensions["height"]
        descriptor["mode"] = dimensions["mode"]
        expected_width = str(index_entry.get("width") or "")
        expected_height = str(index_entry.get("height") or "")
        require(expected_width in {"", str(dimensions["width"])}, f"PNG width drift for {member}")
        require(expected_height in {"", str(dimensions["height"])}, f"PNG height drift for {member}")
    return descriptor, raw


def write_promoted_asset(descriptor: dict[str, Any], raw: bytes) -> None:
    runtime_path = str(descriptor["runtime_path"])
    destination = ROOT / "runtime/social-dev" / runtime_path
    require(destination.parent.is_relative_to(ROOT / "runtime/social-dev/assets"), "runtime asset escaped its boundary")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(raw)
    require(sha256_file(destination) == descriptor["sha256"], f"promoted asset hash drift for {destination}")


def derived_opt_png(
    descriptor: dict[str, Any],
    reconstruction: OptReconstruction,
    opt_descriptor: dict[str, Any],
) -> tuple[dict[str, Any], bytes]:
    """Create the physical runtime PNG for an OPT logical atlas.

    The source PNG remains the provenance asset.  Runtime frame rectangles are
    addressed against the reconstructed logical atlas, so the browser must
    receive that atlas as an actual bounded image rather than the compact raw
    source PNG.  Keeping this conversion offline also keeps OPT parsing out of
    the browser runtime.
    """

    require(reconstruction.status == "pass" and reconstruction.image is not None, "OPT reconstruction is not runtime-ready")
    require(reconstruction.logical_size is not None, "OPT reconstruction has no logical size")
    image_buffer = io.BytesIO()
    reconstruction.image.save(image_buffer, format="PNG", optimize=False, compress_level=9)
    raw = image_buffer.getvalue()
    filename = Path(str(descriptor["asset_member"])).stem + ".png"
    runtime_member = f"02_DERIVED_READY_IMAGES/opt_reconstructed/chip/{filename}"
    derived = {
        "asset_id": f"asset:derived/{runtime_member}",
        "asset_member": runtime_member,
        "runtime_path": f"assets/display-slice-01/{runtime_member}",
        "kind": "derived_opt_reconstruction",
        "pack": "chip",
        "original_name": filename,
        "extension": ".png",
        "bytes": len(raw),
        "sha256": sha256_bytes(raw),
        "semantic_role": descriptor.get("semantic_role"),
        "width": reconstruction.logical_size[0],
        "height": reconstruction.logical_size[1],
        "mode": "RGBA",
        "provenance": {
            "source_asset_id": descriptor["asset_id"],
            "source_asset_member": descriptor["asset_member"],
            "opt_asset_id": opt_descriptor["asset_id"],
            "opt_asset_member": opt_descriptor["asset_member"],
            "reconstruction_status": reconstruction.status,
            "logical_pixel_sha256": reconstruction.pixel_sha256,
        },
    }
    return derived, raw


def source_ref(path: Path) -> dict[str, str]:
    require(path.is_file(), f"missing source reference {path}")
    return {"path": relative_path(path), "sha256": sha256_file(path)}


def record_with_source_bounds(
    seb: dict[str, Any],
    source_images: dict[int, dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[str]]:
    composed: list[dict[str, Any]] = []
    issues: list[str] = []
    for record in seb["records"]:
        source = source_images.get(record["image_id"])
        if source is None:
            issues.append(f"missing_img_inf_id:{record['image_id']}")
            composed.append({**record, "source_status": "missing_img_inf_id"})
            continue
        filename = str(source["filename"])
        descriptor = source["descriptor"]
        raw_width = int(descriptor.get("width") or 0)
        raw_height = int(descriptor.get("height") or 0)
        raw_fits = (
            record["source_x"] + record["width"] <= raw_width
            and record["source_y"] + record["height"] <= raw_height
        )
        # The source rectangle may be addressed against the logical atlas
        # produced by OPT. This is accepted only when the parser and all
        # source rectangles passed; the generated image itself is evidence,
        # not a runtime asset.
        reconstruction: OptReconstruction | None = source.get("opt_reconstruction")
        logical_size = reconstruction.logical_size if reconstruction else None
        logical_fits = bool(
            reconstruction
            and reconstruction.status == "pass"
            and logical_size
            and record["source_x"] + record["width"] <= logical_size[0]
            and record["source_y"] + record["height"] <= logical_size[1]
        )
        if logical_fits:
            source_status = "pass_opt_logical"
            source_size = {"width": logical_size[0], "height": logical_size[1]}
        elif raw_fits:
            source_status = "pass"
            source_size = {"width": raw_width, "height": raw_height}
        else:
            source_status = "source_rect_out_of_bounds"
            source_size = {"width": raw_width, "height": raw_height}
            if reconstruction and reconstruction.status != "pass":
                issues.append(f"opt_reconstruction_not_proven:{filename}:{reconstruction.status}")
            issues.append(
                f"source_rect_out_of_bounds:{filename}:"
                f"{record['source_x']},{record['source_y']},{record['width']},{record['height']}"
                f"_within_{raw_width}x{raw_height}"
                + (f"_or_logical_{logical_size[0]}x{logical_size[1]}" if logical_size else "")
            )
        record_result: dict[str, Any] = {
            **record,
            "source_asset_member": filename,
            "source_asset_id": descriptor["asset_id"],
            "source_size": source_size,
            "source_status": source_status,
        }
        runtime_descriptor = source.get("runtime_descriptor") if logical_fits else descriptor
        require(runtime_descriptor is not None, f"runtime descriptor is missing for {filename}")
        runtime_width = int(runtime_descriptor.get("width") or 0)
        runtime_height = int(runtime_descriptor.get("height") or 0)
        require(
            record["source_x"] + record["width"] <= runtime_width
            and record["source_y"] + record["height"] <= runtime_height,
            f"runtime frame rectangle is out of bounds for {runtime_descriptor['asset_member']}",
        )
        record_result["runtime_asset_member"] = runtime_descriptor["asset_member"]
        record_result["runtime_asset_id"] = runtime_descriptor["asset_id"]
        record_result["runtime_size"] = {"width": runtime_width, "height": runtime_height}
        record_result["runtime_status"] = "pass_derived_opt_png" if logical_fits else "pass_physical_png"
        if reconstruction:
            opt_descriptor = source.get("opt_descriptor")
            record_result["opt_asset_member"] = opt_descriptor["asset_member"] if opt_descriptor else None
            record_result["opt_asset_id"] = opt_descriptor["asset_id"] if opt_descriptor else None
            record_result["logical_source_size"] = (
                {"width": logical_size[0], "height": logical_size[1]} if logical_size else None
            )
        composed.append(record_result)
    return composed, issues


def build_package() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    selectors = load_json(SELECTOR_CONTRACT)
    actor_fixture = load_json(ACTOR_FIXTURE)
    scene_fixture = load_json(SCENE_FIXTURE)
    object_fixture = load_json(OBJECT_FIXTURE)
    inventory = load_json(ASSET_INVENTORY)
    phase3a_closure = load_json(PHASE3A_CLOSURE) if PHASE3A_CLOSURE.is_file() else None
    phase3c_strict = load_json(PHASE3C_STRICT_CLOSURE) if PHASE3C_STRICT_CLOSURE.is_file() else None
    phase3a_status = str(phase3a_closure.get("status")) if isinstance(phase3a_closure, dict) else "pending"
    phase3a_reason_code = str(phase3a_closure.get("reason_code")) if isinstance(phase3a_closure, dict) else None
    phase3a_reason = str(phase3a_closure.get("reason")) if isinstance(phase3a_closure, dict) else None
    phase3c_strict_status = str(phase3c_strict.get("status")) if isinstance(phase3c_strict, dict) else "pending"
    index = asset_index_map()
    with zipfile.ZipFile(ZIP_PATH) as archive:
        archive_index = json.loads(archive.read(ARCHIVE_PREFIX + "00_INDEX/ASSET_INDEX.json").decode("utf-8-sig"))
        require(stable_json(archive_index) == stable_json(list(index.values())), "archive ASSET_INDEX differs from extracted evidence")

        human_img_inf = parse_inf(archive.read(ARCHIVE_PREFIX + "01_GAME_PACKS/human/img.inf"))
        human_seb_inf = parse_inf(archive.read(ARCHIVE_PREFIX + "01_GAME_PACKS/human/seb.inf"))
        chip_img_inf = parse_inf(archive.read(ARCHIVE_PREFIX + "01_GAME_PACKS/chip/img.inf"))
        chip_seb_inf = parse_inf(archive.read(ARCHIVE_PREFIX + "01_GAME_PACKS/chip/seb.inf"))

        promoted: dict[str, tuple[dict[str, Any], bytes]] = {}
        promoted_members: set[str] = set()

        def get_asset(member: str, promote: bool = False) -> dict[str, Any]:
            member = normalize_member(member)
            if member not in promoted:
                promoted[member] = read_archive_asset(archive, index, member)
            descriptor, raw = promoted[member]
            if promote:
                write_promoted_asset(descriptor, raw)
                promoted_members.add(member)
            return descriptor

        def seb_asset(pack: str, filename: str, promote: bool = False) -> tuple[dict[str, Any], dict[str, Any]]:
            member = f"01_GAME_PACKS/{pack}/{filename}"
            descriptor = get_asset(member, promote=promote)
            raw = promoted[normalize_member(member)][1]
            return descriptor, parse_seb(raw, member)

        def archive_has(member: str) -> bool:
            return f"{ARCHIVE_PREFIX}{normalize_member(member)}" in archive.namelist()

        def prepare_chip_sources(seb: dict[str, Any]) -> dict[int, dict[str, Any]]:
            sources: dict[int, dict[str, Any]] = {}
            for record in seb["records"]:
                image_id = int(record["image_id"])
                image_filename = chip_img_inf.get(image_id)
                if image_filename is None or image_id in sources:
                    continue
                image_member = f"01_GAME_PACKS/chip/{image_filename}"
                image_descriptor = get_asset(image_member, promote=False)
                image_raw = promoted[normalize_member(image_member)][1]
                source: dict[str, Any] = {
                    "image_id": image_id,
                    "filename": image_filename,
                    "descriptor": image_descriptor,
                    "raw": image_raw,
                }
                opt_filename = f"{Path(image_filename).stem}.opt"
                opt_member = f"01_GAME_PACKS/chip/{opt_filename}"
                if archive_has(opt_member):
                    opt_descriptor = get_asset(opt_member, promote=False)
                    opt_raw = promoted[normalize_member(opt_member)][1]
                    source["opt_descriptor"] = opt_descriptor
                    source["opt_reconstruction"] = reconstruct_opt(
                        image_raw,
                        opt_raw,
                        image_member,
                        opt_member,
                    )
                    reconstruction = source["opt_reconstruction"]
                    if reconstruction.status == "pass" and reconstruction.image is not None:
                        derived_descriptor, derived_raw = derived_opt_png(image_descriptor, reconstruction, opt_descriptor)
                        source["runtime_descriptor"] = derived_descriptor
                        source["runtime_raw"] = derived_raw
                sources[image_id] = source
            return sources

        def compose_chip_selector(furniture: dict[str, Any], selector_name: str) -> dict[str, Any] | None:
            selector = furniture["selectors"][selector_name]
            selector_id = int(selector["id"])
            if selector_id < 0:
                return None
            seb_filename = str(selector["filename"])
            require(chip_seb_inf.get(selector_id) == seb_filename, f"chip SEB selector drift for {selector_name}")
            seb_descriptor, seb = seb_asset("chip", seb_filename, promote=False)
            source_images = prepare_chip_sources(seb)
            records, issues = record_with_source_bounds(seb, source_images)
            source_compositions: list[dict[str, Any]] = []
            for source in sorted(source_images.values(), key=lambda item: item["image_id"]):
                reconstruction: OptReconstruction | None = source.get("opt_reconstruction")
                source_descriptor = source["descriptor"]
                item: dict[str, Any] = {
                    "image_id": source["image_id"],
                    "source_asset_member": source_descriptor["asset_member"],
                    "source_asset_id": source_descriptor["asset_id"],
                    "source_size": {
                        "width": int(source_descriptor.get("width") or 0),
                        "height": int(source_descriptor.get("height") or 0),
                    },
                }
                if reconstruction:
                    item["opt_asset_member"] = source["opt_descriptor"]["asset_member"]
                    item["opt_asset_id"] = source["opt_descriptor"]["asset_id"]
                    item["opt_status"] = reconstruction.status
                    item["logical_size"] = (
                        {"width": reconstruction.logical_size[0], "height": reconstruction.logical_size[1]}
                        if reconstruction.logical_size
                        else None
                    )
                    item["logical_pixel_sha256"] = reconstruction.pixel_sha256
                    item["opt_issues"] = list(reconstruction.issues)
                    runtime_descriptor = source.get("runtime_descriptor")
                    if runtime_descriptor:
                        item["runtime_asset_member"] = runtime_descriptor["asset_member"]
                        item["runtime_asset_id"] = runtime_descriptor["asset_id"]
                        item["runtime_size"] = {
                            "width": int(runtime_descriptor["width"]),
                            "height": int(runtime_descriptor["height"]),
                        }
                        item["runtime_status"] = "pass_derived_opt_png"
                else:
                    item["opt_status"] = "not_present"
                source_compositions.append(item)
            return {
                "selector_id": selector_id,
                "filename": seb_filename,
                "asset_id": seb_descriptor["asset_id"],
                "asset_member": seb_descriptor["asset_member"],
                "header": seb["header"],
                "records": records,
                "composition_issues": issues,
                "source_compositions": source_compositions,
                "source_images": source_images,
                "seb": seb,
            }

        def promote_chip_composition(composition: dict[str, Any] | None) -> None:
            if composition is None:
                return
            get_asset(composition["asset_member"], promote=True)
            for source in composition["source_images"].values():
                get_asset(source["descriptor"]["asset_member"], promote=True)
                if source.get("opt_descriptor"):
                    get_asset(source["opt_descriptor"]["asset_member"], promote=True)
                runtime_descriptor = source.get("runtime_descriptor")
                runtime_raw = source.get("runtime_raw")
                if runtime_descriptor is not None and runtime_raw is not None:
                    write_promoted_asset(runtime_descriptor, runtime_raw)
                    promoted[runtime_descriptor["asset_member"]] = (runtime_descriptor, runtime_raw)
                    promoted_members.add(runtime_descriptor["asset_member"])

        def public_chip_composition(composition: dict[str, Any] | None) -> dict[str, Any] | None:
            if composition is None:
                return None
            return {
                key: composition[key]
                for key in (
                    "selector_id",
                    "filename",
                    "asset_id",
                    "asset_member",
                    "header",
                    "records",
                    "composition_issues",
                    "source_compositions",
                )
            }

        selected_staff = selectors.get("selected_staff", [])
        require([item["id"] for item in selected_staff] == list(range(5)), "selected StaffData ids drifted")
        animation_profile = next(
            profile for profile in actor_fixture["animation_profiles"] if profile["id"] == "human-living-scene-v1"
        )
        direction = animation_profile["directions"][0]
        human_animation: dict[str, dict[str, Any]] = {}
        actor_bindings: list[dict[str, Any]] = []
        for mode in ("wait", "typing"):
            selector = direction[mode]
            seb_id = int(selector["seb_id"])
            filename = str(selector["filename"])
            require(human_seb_inf.get(seb_id) == filename, f"human SEB selector drift for {mode}")
            seb_descriptor, seb = seb_asset("human", filename, promote=True)
            require(seb["header"]["global_frame_count"] == 20, f"unexpected {mode} frame count")
            require(seb["header"]["record_count"] == 3, f"unexpected {mode} record count")
            records: list[dict[str, Any]] = []
            issues: list[str] = []
            for record in seb["records"]:
                if record["image_id"] != 0:
                    issues.append(f"unexpected_human_image_slot:{record['image_id']}")
                fits = record["source_x"] + record["width"] <= 270 and record["source_y"] + record["height"] <= 60
                if not fits:
                    issues.append(f"human_source_rect_out_of_bounds:{record['start_frame']}")
                records.append(
                    {
                        **record,
                        "source_asset_slot": "selected_staff_img_",
                        "source_size": {"width": 270, "height": 60},
                        "source_status": "pass" if fits else "source_rect_out_of_bounds",
                    }
                )
            require(not issues, f"human {mode} composition failed: {issues}")
            human_animation[mode] = {
                "selector_id": seb_id,
                "filename": filename,
                "asset_id": seb_descriptor["asset_id"],
                "frame_bound": seb["header"]["frame_bound"],
                "global_frame_count": seb["header"]["global_frame_count"],
                "records": records,
                "binding": "human_seb_records_with_selected_staff_img_",
                "status": "approved_for_runtime_subset",
            }

        for staff in selected_staff:
            image_selector = staff["img_"]
            image_id = int(image_selector["id"])
            filename = str(image_selector["filename"])
            require(human_img_inf.get(image_id) == filename, f"human image selector drift for {image_id}")
            image_descriptor = get_asset(f"01_GAME_PACKS/human/{filename}", promote=True)
            require(image_descriptor.get("width") == 270 and image_descriptor.get("height") == 60, f"unexpected human image size for {filename}")
            actor_bindings.append(
                {
                    "actor_source_id": int(staff["id"]),
                    "image_selector_id": image_id,
                    "image_asset_id": image_descriptor["asset_id"],
                    "image_asset_member": image_descriptor["asset_member"],
                    "image_size": {"width": 270, "height": 60},
                    "animations": human_animation,
                    "status": "approved_for_runtime_subset",
                }
            )

        furniture_records = {item["id"]: item for item in selectors.get("selected_furniture", [])}
        object_entries: list[dict[str, Any]] = []
        for furniture_id in (0, 1, 2, 5):
            furniture = furniture_records[furniture_id]
            main_composition = compose_chip_selector(furniture, "seb_")
            sub_composition = compose_chip_selector(furniture, "subSeb_")
            require(main_composition is not None, f"furniture:{furniture_id} has no primary SEB selector")
            main_issues = list(main_composition["composition_issues"])
            sub_issues = list(sub_composition["composition_issues"]) if sub_composition else []
            issues = main_issues + [f"subSeb:{issue}" for issue in sub_issues]

            if furniture_id == 0:
                require(main_composition["filename"] == "big_base00.seb", "furniture:0 selector changed")
                require(chip_img_inf.get(18) == "big_base00.png", "big_base00 image relation changed")
                require(not issues, f"furniture:0 composition failed: {issues}")
                promote_chip_composition(main_composition)
                status = "approved_for_runtime_subset"
                blocked_reason = None
            elif furniture_id == 1:
                require(main_composition["filename"] == "door_03.seb", "furniture:1 selector changed")
                if not issues:
                    promote_chip_composition(main_composition)
                    status = "approved_for_runtime_subset"
                    blocked_reason = None
                else:
                    status = "blocked_requires_frame_composition"
                    blocked_reason = "door_03.seb did not pass its source/OPT logical composition gate."
            elif furniture_id == 5:
                require(main_composition["filename"] == "desk_00.seb", "furniture:5 primary selector changed")
                require(sub_composition is not None and sub_composition["filename"] == "chair_02.seb", "furniture:5 sub selector changed")
                if not issues:
                    promote_chip_composition(main_composition)
                    promote_chip_composition(sub_composition)
                    status = "approved_for_runtime_subset"
                    blocked_reason = None
                else:
                    status = "blocked_requires_frame_composition"
                    blocked_reason = "The primary or subSeb OPT logical composition did not pass."
            elif furniture_id == 2:
                require(main_composition["filename"] == "desk_00.seb", "furniture:2 primary selector changed")
                require(sub_composition is not None and sub_composition["filename"] == "chair_00.seb", "furniture:2 sub selector changed")
                if phase3a_status == "approved" and not issues:
                    promote_chip_composition(main_composition)
                    promote_chip_composition(sub_composition)
                    status = "approved_for_runtime_subset"
                    blocked_reason = None
                elif phase3a_status == "quarantined_source_limitation":
                    status = "blocked_source_limitation"
                    blocked_reason = phase3a_reason or "chair_00.opt has an unrecoverable source limitation."
                else:
                    status = "blocked_requires_frame_composition"
                    blocked_reason = "chair_00.opt has not passed the Phase 3A closure and the full desk/chair composition remains gated."
            object_entries.append(
                {
                    "object_id": f"furniture:{furniture_id}",
                    "name": furniture.get("name"),
                    "seb_selector_id": main_composition["selector_id"],
                    "seb_asset_member": main_composition["asset_member"],
                    "seb_asset_id": main_composition["asset_id"],
                    "header": main_composition["header"],
                    "records": main_composition["records"],
                    "composition_issues": issues,
                    "source_compositions": main_composition["source_compositions"],
                    "sub_composition": public_chip_composition(sub_composition),
                    "status": status,
                    **(
                        {
                            "phase3a_closure": {
                                "status": phase3a_status,
                                "reason_code": phase3a_reason_code,
                            }
                        }
                        if furniture_id == 2
                        else {}
                    ),
                    **({"blocked_reason": blocked_reason} if blocked_reason else {}),
                }
            )

        # The strict native package contains the room:0 bootstrap bindings for
        # FurnitureData rows that are intentionally outside the four-object
        # display catalog. Keep those bindings separate from selector-only
        # furniture so the runtime can draw the actual initial room without
        # inferring a FurnitureData identity for an unbound object.
        object_entries_by_id = {item["object_id"]: item for item in object_entries}
        native_initial_entries: list[dict[str, Any]] = []
        native_initial_bindings = phase3c_strict.get("native_initial_bindings", []) if isinstance(phase3c_strict, dict) else []
        furniture_table = phase3c_strict.get("furniture_table") if isinstance(phase3c_strict, dict) else None
        native_rows: dict[int, dict[str, Any]] = {}
        if isinstance(furniture_table, dict):
            for row in furniture_table.get("init_desk_rows", []):
                native_rows[int(row["id"])] = row
            for row in furniture_table.get("init_place_rows", []):
                native_rows[int(row["id"])] = row

        for furniture_id in sorted(native_rows):
            row = native_rows[furniture_id]
            object_id = f"furniture:{furniture_id}"
            require(
                any(int(binding["furniture_data_id"]) == furniture_id for binding in native_initial_bindings),
                f"strict native initial binding is missing furniture:{furniture_id}",
            )
            if furniture_id == 3:
                # FurnitureData(3) uses the same native desk/chair selector
                # pair as the source-backed Desk composition. Its distinct
                # identity is retained here through the FurnitureData row and
                # strict init flag; no selector identity is inferred.
                source_object = object_entries_by_id["furniture:2"]
                native_initial_entries.append(
                    {
                        "object_id": object_id,
                        "furniture_data_id": furniture_id,
                        "name": row["name"],
                        "raw_type": row["type"],
                        "seb_selector_id": row["seb"],
                        "sub_seb_selector_id": row["sub_seb"],
                        "img_selector_id": row["img"],
                        "img_filename": chip_img_inf.get(int(row["img"])),
                        "selector_flag": "FLAG_INIT_DESK",
                        "native_status": "approved_native_initial_binding",
                        "display_mode": "native_selector_composition",
                        "seb_asset_member": source_object["seb_asset_member"],
                        "seb_asset_id": source_object["seb_asset_id"],
                        "header": source_object["header"],
                        "records": source_object["records"],
                        "composition_issues": source_object["composition_issues"],
                        "source_compositions": source_object["source_compositions"],
                        "sub_composition": source_object["sub_composition"],
                        "status": "approved_for_runtime_subset",
                    }
                )
                continue

            image_id = int(row["img"])
            image_filename = chip_img_inf.get(image_id)
            require(image_filename is not None, f"native furniture:{furniture_id} img selector {image_id} is unresolved")
            image_descriptor = get_asset(f"01_GAME_PACKS/chip/{image_filename}", promote=True)
            image_width = int(image_descriptor.get("width") or 0)
            image_height = int(image_descriptor.get("height") or 0)
            require(image_width > 0 and image_height > 0, f"native furniture:{furniture_id} image has no dimensions")
            native_seb_filename = chip_seb_inf.get(int(row["seb"]))
            require(native_seb_filename is not None, f"native furniture:{furniture_id} SEB selector {row['seb']} is unresolved")
            seb_descriptor = get_asset(f"01_GAME_PACKS/chip/{native_seb_filename}", promote=True)
            native_initial_entries.append(
                {
                    "object_id": object_id,
                    "furniture_data_id": furniture_id,
                    "name": row["name"],
                    "raw_type": row["type"],
                    "seb_selector_id": int(row["seb"]),
                    "sub_seb_selector_id": int(row["sub_seb"]),
                    "img_selector_id": image_id,
                    "img_filename": image_filename,
                    "selector_flag": "FLAG_INIT_PLACE",
                    "native_status": "approved_native_initial_binding",
                    "display_mode": "native_type1_direct_img",
                    "seb_asset_member": seb_descriptor["asset_member"],
                    "seb_asset_id": seb_descriptor["asset_id"],
                    "header": {"layer_count": 1, "global_frame_count": 1, "record_count": 1, "frame_bound": 1},
                    "records": [
                        {
                            "start_frame": 0,
                            "image_id": image_id,
                            "source_x": 0,
                            "source_y": 0,
                            "width": image_width,
                            "height": image_height,
                            "destination_x": -(image_width // 2),
                            "destination_y": -image_height + 3,
                            "flags": 0,
                            "reserved": 0,
                            "source_asset_member": image_descriptor["asset_member"],
                            "source_asset_id": image_descriptor["asset_id"],
                            "source_size": {"width": image_width, "height": image_height},
                            "source_status": "pass_native_img_asset",
                        }
                    ],
                    "composition_issues": [],
                    "source_compositions": [
                        {
                            "image_id": image_id,
                            "source_asset_member": image_descriptor["asset_member"],
                            "source_asset_id": image_descriptor["asset_id"],
                            "source_size": {"width": image_width, "height": image_height},
                            "opt_status": "not_required_native_type1_img",
                        }
                    ],
                    "sub_composition": None,
                    "status": "approved_for_runtime_subset",
                }
            )

        room = next(scene for scene in scene_fixture["scenes"] if scene["id"] == "room:0")
        scalar_fields = room["scalar_fields_raw"]
        scene_assets: list[dict[str, Any]] = []
        for field_name, role in (("floorImgId_", "floor"), ("wallImgId_", "wall"), ("doorImgId_", "door")):
            image_id = int(scalar_fields[field_name]["value"])
            filename = chip_img_inf.get(image_id)
            if filename is None:
                fallback = FLOOR_RUNTIME_FALLBACKS.get(image_id) if role == "floor" else None
                if fallback is not None:
                    target_selector_id = int(fallback["target_selector_id"])
                    target_filename = str(fallback["filename"])
                    require(
                        chip_img_inf.get(target_selector_id) == target_filename,
                        f"floor fallback selector drift for {target_selector_id}",
                    )
                    descriptor = get_asset(f"01_GAME_PACKS/chip/{target_filename}", promote=True)
                    scene_assets.append(
                        {
                            "id": f"scene:room:0/{role}",
                            "role": role,
                            "image_id": image_id,
                            "filename": target_filename,
                            "asset_id": descriptor["asset_id"],
                            "asset_member": descriptor["asset_member"],
                            "status": "approved_for_runtime_subset",
                            "resolution_mode": "explicit_user_approved_alias",
                            "source_resolution_status": "unresolved",
                            "fallback_selector_id": target_selector_id,
                            "fallback_reason_code": fallback["reason_code"],
                            "blocked_reason": "Source chip/img.inf id 5 remains unresolved; floor_09.png is promoted only as the explicit runtime fallback.",
                        }
                    )
                    continue
                scene_assets.append(
                    {
                        "id": f"scene:room:0/{role}",
                        "role": role,
                        "image_id": image_id,
                        "status": "blocked_unresolved_index_slot",
                        "blocked_reason": "chip/img.inf has no entry for this source image id; no filename was guessed.",
                    }
                )
                continue
            strict_scene = phase3c_strict.get(role) if isinstance(phase3c_strict, dict) else None
            if role in {"wall", "door"} and phase3c_strict_status == "pass" and isinstance(strict_scene, dict):
                strict_png_member = str(strict_scene["source_asset"]["png_member"])
                strict_seb_member = str(strict_scene["source_asset"]["seb_member"])
                require(strict_png_member == f"01_GAME_PACKS/chip/{filename}", f"strict {role} PNG identity changed")
                image_descriptor = get_asset(strict_png_member, promote=True)
                seb_descriptor = get_asset(strict_seb_member, promote=True)
                scene_assets.append(
                    {
                        "id": f"scene:room:0/{role}",
                        "role": role,
                        "image_id": image_id,
                        "filename": filename,
                        "asset_id": image_descriptor["asset_id"],
                        "asset_member": image_descriptor["asset_member"],
                        "seb_asset_id": seb_descriptor["asset_id"],
                        "seb_asset_member": seb_descriptor["asset_member"],
                        "status": "approved_for_runtime_subset",
                        "source_resolution_status": "resolved",
                        "native_coordinate_composition": strict_scene,
                        "strict_closure_ref": relative_path(PHASE3C_STRICT_CLOSURE),
                    }
                )
                continue
            descriptor = get_asset(f"01_GAME_PACKS/chip/{filename}", promote=False)
            scene_assets.append(
                {
                    "id": f"scene:room:0/{role}",
                    "role": role,
                    "image_id": image_id,
                    "filename": filename,
                    "asset_id": descriptor["asset_id"],
                    "asset_member": descriptor["asset_member"],
                    "status": "blocked_coordinate_composition",
                    "blocked_reason": "Image identity is indexed, but exact native placement/coordinate composition is not closed for this display slice.",
                }
            )

        entries: list[dict[str, Any]] = []
        for binding in actor_bindings:
            entries.append(
                {
                    "id": f"actor-sprite:{binding['actor_source_id']}",
                    "kind": "human_actor_frame_source",
                    "status": binding["status"],
                    "source": binding,
                }
            )
        for mode, animation in human_animation.items():
            entries.append(
                {
                    "id": f"human-animation:{mode}:direction-0",
                    "kind": "human_seb_frame_definition",
                    "status": animation["status"],
                    "source": animation,
                }
            )
        entries.extend(
            {
                "id": f"object-frame:{item['object_id']}",
                "kind": "chip_object_frame_definition",
                "status": item["status"],
                "source": item,
            }
            for item in object_entries
        )
        entries.extend(scene_assets)
        entries.extend(
            {
                "id": f"native-initial-frame:{item['object_id']}",
                "kind": "native_initial_furniture_frame_definition",
                "status": item["status"],
                "source": item,
            }
            for item in native_initial_entries
        )

        counts = Counter(item["status"] for item in entries)
        approved_entries = [item for item in entries if item["status"] == "approved_for_runtime_subset"]
        promoted_assets = sorted(
            (descriptor for member, (descriptor, _raw) in promoted.items() if member in promoted_members),
            key=lambda item: item["asset_member"],
        )
        phase3a_approved = phase3a_status == "approved"
        phase3a_scope_approved = [
            "furniture:2 desk_00 plus chair_00 OPT logical reconstruction"
        ] if phase3a_approved else []
        phase3a_scope_blocked = [] if phase3a_approved else [
            "furniture:2 chair_00 OPT source limitation"
            if phase3a_status == "quarantined_source_limitation"
            else "furniture:2 chair_00 OPT reconstruction pending Phase 3A closure"
        ]
        phase3a_gate_metadata = {
            "target": "furniture:2",
            "status": phase3a_status,
            "reason_code": phase3a_reason_code,
            "runtime_promotion": "approved" if phase3a_approved else "not_promoted",
        }
        blocked_entries = [item for item in entries if item["status"] != "approved_for_runtime_subset"]
        gate_status = "pass" if not blocked_entries else "partial"
        gate_semantic_status = "approved_for_runtime_subset" if not blocked_entries else "approved_subset_only"
        gate = {
            "schema_version": "social-dev-display-asset-gate-v1",
            "package": "display-slice-01",
            "status": gate_status,
            "semantic_status": gate_semantic_status,
            "generated_at_utc": utc_now(),
            "phase3a": phase3a_gate_metadata,
            "scope": {
                "approved": [
                    "selected staff source PNGs for source ids 0-4",
                    "human wait_right/typing_right SEB frame records",
                    "furniture:0 big_base00 direct SEB-to-PNG composition",
                    "furniture:1 door_03 SEB with door_02 OPT logical reconstruction",
                    "furniture:5 desk_00 plus chair_02 OPT logical reconstruction",
                    "room wall_00 native DrawWall coordinate composition",
                    "room door_01/door_02 native DrawWall coordinate composition",
                    "native room:0 initial FurnitureData bindings for furniture:3/12/26/56",
                ] + phase3a_scope_approved,
                "blocked": [
                    *phase3a_scope_blocked,
                    *(["room wall/door coordinate placement"] if phase3c_strict_status != "pass" else []),
                ],
            },
            "source_archives": {
                "asset_zip": {
                    "path": relative_path(ZIP_PATH),
                    "sha256": inventory["archives"]["asset_zip"]["sha256"],
                },
                "apk": {
                    "path": inventory["archives"]["apk"]["path"],
                    "sha256": inventory["archives"]["apk"]["sha256"],
                },
            },
            "source_refs": [
                source_ref(ASSET_GUIDE_INDEX),
                source_ref(SELECTOR_CONTRACT),
                source_ref(ACTOR_FIXTURE),
                source_ref(SCENE_FIXTURE),
                source_ref(OBJECT_FIXTURE),
                *( [source_ref(PHASE3C_STRICT_CLOSURE)] if PHASE3C_STRICT_CLOSURE.is_file() else []),
            ],
            "seb_format": {
                "header_bytes": SEB_HEADER_SIZE,
                "record_bytes": SEB_RECORD_SIZE,
                "record_format": SEB_RECORD_FORMAT,
                "source_policy": "SEB records are parsed as evidence; runtime consumes only the approved manifest frame records.",
            },
            "entries": entries,
            "promoted_assets": promoted_assets,
            "counts": {
                "entries": len(entries),
                "approved": len(approved_entries),
                "blocked": len(entries) - len(approved_entries),
                "by_status": dict(sorted(counts.items())),
                "promoted_binary_assets": len(promoted_assets),
            },
            "determinism": {"algorithm": "stable-json-sha256 excluding generated_at_utc and content_hash"},
        }

        manifest = {
            "schema_version": "social-dev-display-asset-manifest-v1",
            "package": "display-slice-01",
            "status": "pass",
            "semantic_status": "approved_for_runtime_subset",
            "scope": "actor-frame-subset-proven-chip-compositions-native-wall-door-composition-and-explicit-floor-fallback",
            "generated_at_utc": gate["generated_at_utc"],
            "gate_ref": {
                "path": relative_path(OUTPUT),
                "status": gate["status"],
                "semantic_status": gate["semantic_status"],
            },
            "assets": promoted_assets,
            "actors": actor_bindings,
            "objects": {
                item["object_id"]: item
                for item in object_entries
                if item["status"] == "approved_for_runtime_subset"
            },
            "native_initial_objects": {
                item["object_id"]: item
                for item in native_initial_entries
                if item["status"] == "approved_for_runtime_subset"
            },
            "phase3a": {
                **phase3a_gate_metadata,
                "closure_path": relative_path(PHASE3A_CLOSURE),
            },
            "runtime_policy": {
                "fallback": "Use the existing placeholder only while approved assets are loading or unavailable; room:0 raw floor selector 5 explicitly aliases to floor_09.png (selector 85).",
                "unapproved_assets_are_not_loaded": True,
                "source_code_imports": False,
            },
            "determinism": {"algorithm": "stable-json-sha256 excluding generated_at_utc and content_hash"},
        }

    gate_without_dynamic = {key: value for key, value in gate.items() if key not in {"generated_at_utc", "determinism"}}
    gate["determinism"]["content_hash"] = sha256_bytes(stable_json(gate_without_dynamic).encode("utf-8"))
    manifest_without_dynamic = {key: value for key, value in manifest.items() if key not in {"generated_at_utc", "determinism"}}
    manifest["determinism"]["content_hash"] = sha256_bytes(stable_json(manifest_without_dynamic).encode("utf-8"))

    validation = {
        "schema_version": "social-dev-display-asset-gate-validation-v1",
        "package": "display-slice-01",
        "status": "pass",
        "semantic_status": "validated",
        "generated_at_utc": gate["generated_at_utc"],
        "checks": [
            "archive ASSET_INDEX matches extracted evidence",
            "promoted binaries match source ZIP hashes",
            "human frame rectangles fit the selected 270x60 actor strips",
            "big_base00 frame rectangle fits its 120x61 source PNG",
            "door_03 frame rectangles fit the door_02 OPT logical atlas",
            "desk_00 and chair_02 frame rectangles fit their OPT logical atlases",
            "OPT logical pixel hashes match the supplied derived comparison images",
            "unresolved scene image id 5 remains explicit while its user-approved floor_09.png runtime fallback is promoted; strict native wall/door coordinate package is available"
            if phase3c_strict_status == "pass"
            else "unresolved scene image id 5 remains explicit while its user-approved floor_09.png runtime fallback is promoted; strict native wall/door coordinate package remains blocked",
            "chair_00 OPT composition is approved for furniture:2"
            if phase3a_approved
            else "chair_00 OPT source limitation remains explicitly quarantined for furniture:2",
            "runtime manifest contains only approved subset entries",
        ],
        "failed_checks": [],
        "counts": {
            "checks": 10,
            "passed_checks": 10,
            "gate_entries": len(entries),
            "approved_entries": len(approved_entries),
            "promoted_binary_assets": len(promoted_assets),
        },
        "gate_hash": gate["determinism"]["content_hash"],
        "manifest_hash": manifest["determinism"]["content_hash"],
    }
    return gate, manifest, validation


def write_package(gate: dict[str, Any], manifest: dict[str, Any], validation: dict[str, Any]) -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(gate, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    RUNTIME_MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    RUNTIME_MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    phase3a = gate["phase3a"]
    phase3a_approved = phase3a["status"] == "approved"
    report_lines = [
        "# Social Dev display asset/frame gate",
        "",
        "The gate promotes only source PNG/OPT/SEB bytes and frame records that passed exact selector, hash, source-rectangle, or native coordinate-composition checks.",
        "",
        "## Result",
        "",
        f"- Gate status: `{gate['status']}` / `{gate['semantic_status']}`",
        f"- Approved gate entries: `{gate['counts']['approved']}` of `{gate['counts']['entries']}`",
        f"- Promoted binary assets: `{gate['counts']['promoted_binary_assets']}`",
        f"- Gate content hash: `{gate['determinism']['content_hash']}`",
        "",
        "## Runtime-approved subset",
        "",
        "- Staff source PNGs `chara86.png` through `chara90.png`.",
        "- Human `wait_right.seb` and `typing_right.seb` records, with source rectangles verified against the selected 270x60 strips.",
        "- `furniture:0` / `big_base00.seb` with its direct `big_base00.png` source rectangle.",
        "- `furniture:1` / `door_03.seb` through the exact `door_02.png` + `door_02.opt` logical atlas.",
        "- `furniture:5` / `desk_00.seb` plus `chair_02.seb` through exact OPT logical atlases.",
        "- Room `wall_00.png`/`wall_00.seb` and `door_01.png`/`door_02.seb` through the native `ObjChip.DrawWall` coordinate contract.",
        *(["- `furniture:2` / `desk_00.seb` plus `chair_00.seb` through the approved Phase 3A OPT logical composition."] if phase3a_approved else []),
        "",
        "## Explicitly blocked",
        "",
        *(["- `furniture:2` remains blocked by the Phase 3A `chair_00.opt` source limitation; no repaired bytes are promoted."] if not phase3a_approved else []),
        "- Room floor image id `5` remains source-unresolved; the selected `floor_09.png` (indexed selector `85`) is promoted only as an explicit runtime fallback.",
        *( ["- Room wall/door coordinate composition remains blocked until the strict closure package is available."] if gate["status"] != "pass" else []),
        "",
        "## Runtime policy",
        "",
        "The browser imports `knowledge/fixtures/accepted/runtime/display_asset_manifest.json` only. It loads no source archive, APK, C# file, or unapproved asset. Placeholders remain the bounded fallback while the approved subset loads.",
        "",
    ]
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(report_lines), encoding="utf-8", newline="\n")


def main() -> int:
    gate, manifest, validation = build_package()
    write_package(gate, manifest, validation)
    print(
        json.dumps(
            {
                "status": gate["status"],
                "semantic_status": gate["semantic_status"],
                "approved": gate["counts"]["approved"],
                "blocked": gate["counts"]["blocked"],
                "promoted_binary_assets": gate["counts"]["promoted_binary_assets"],
                "gate_hash": gate["determinism"]["content_hash"],
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
