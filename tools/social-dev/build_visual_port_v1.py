"""Build deterministic V1 visual-format fixtures from the immutable asset ZIP.

The artifacts intentionally retain decoded SEB records and OPT cells verbatim.
They are evidence contracts for later runtime work, not a display-list export.
"""

from __future__ import annotations

import hashlib
import json
import sys
import zipfile
from pathlib import Path
from typing import Any

from opt_codec import parse_opt, reconstruct_opt
from seb_codec import decode_seb


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "knowledge/fixtures/accepted/visual-port/v1"
SEB_CATALOG_PATH = ROOT / "knowledge/fixtures/accepted/seb_catalog.json"
DISPLAY_MANIFEST_PATH = ROOT / "knowledge/fixtures/accepted/runtime/display_asset_manifest.json"
CHARACTER_MANIFEST_PATH = ROOT / "knowledge/fixtures/accepted/runtime/character_asset_manifest.json"
RESOURCE_GROUPS_PATH = ROOT / "knowledge/fixtures/accepted/visual-port/resource-groups.json"
RUNTIME_ROOT = ROOT / "runtime/social-dev"

FIXTURES = (
    ("simple_one_layer", "01_GAME_PACKS/chip/door_02.seb"),
    ("multi_layer", "01_GAME_PACKS/chip/wall_00.seb"),
    ("multi_frame", "01_GAME_PACKS/chip/chair_00.seb"),
    ("translation", "01_GAME_PACKS/chip/desk_00.seb"),
    ("flip", "01_GAME_PACKS/human/wait_left.seb"),
    ("furniture", "01_GAME_PACKS/chip/chair_00.seb"),
    ("character", "01_GAME_PACKS/avatar_body/wait_right.seb"),
)
UNIQUE_SEB_MEMBERS = tuple(dict.fromkeys(member for _, member in FIXTURES))
IMAGE_OPT_FIXTURES = (
    "01_GAME_PACKS/chip/chair_00",
    "01_GAME_PACKS/chip/chair_02",
    "01_GAME_PACKS/chip/desk_00",
    "01_GAME_PACKS/chip/door_02",
)
RESOURCE_GROUP_IDS = (
    "resChip_",
    "resInterface_",
    "resHuman_",
    "resCom_",
    "resGame_",
    "resEffect_",
    "resMeeting_",
    "resAvatarBody_",
    "resAvatarHead_",
    "resDevelop_",
    "resWindow_",
)
RESOURCE_FIXTURE_SPECS = (
    {
        "group_id": "resChip_",
        "fixture_stem": "01_GAME_PACKS/chip/chair_00",
        "image_ids": [4],
        "seb_id": 3,
        "seb_member": "01_GAME_PACKS/chip/chair_00.seb",
    },
    {
        "group_id": "resChip_",
        "fixture_stem": "01_GAME_PACKS/chip/desk_00",
        "image_ids": [3],
        "seb_id": 1,
        "seb_member": "01_GAME_PACKS/chip/desk_00.seb",
    },
    {
        "group_id": "resChip_",
        "fixture_stem": "01_GAME_PACKS/chip/wall_00",
        "image_ids": [6],
        "seb_id": 5,
        "seb_member": "01_GAME_PACKS/chip/wall_00.seb",
    },
    {
        "group_id": "resChip_",
        "fixture_stem": "01_GAME_PACKS/chip/door_02",
        "image_ids": [7],
        "seb_id": 6,
        "seb_member": "01_GAME_PACKS/chip/door_02.seb",
    },
    {
        "group_id": "resHuman_",
        "fixture_stem": "01_GAME_PACKS/human/wait_left",
        "image_ids": [0],
        "seb_id": 11,
        "seb_member": "01_GAME_PACKS/human/wait_left.seb",
    },
    {
        "group_id": "resAvatarBody_",
        "fixture_stem": "01_GAME_PACKS/avatar_body/wait_right",
        "image_ids": [0, 1],
        "seb_id": 0,
        "seb_member": "01_GAME_PACKS/avatar_body/wait_right.seb",
    },
)


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def stable_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def add_determinism(payload: dict[str, Any]) -> dict[str, Any]:
    payload["determinism"] = {
        "algorithm": "stable-json-sha256 excluding determinism.content_hash",
        "content_hash": "",
    }
    payload["determinism"]["content_hash"] = sha256_bytes(stable_json(payload).encode("utf-8"))
    return payload


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(stable_json(add_determinism(payload)), encoding="utf-8")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def archive_member(prefix: str, member: str) -> str:
    return f"{prefix}{member}"


def parse_named_index(raw: bytes, member: str, suffix: str) -> dict[int, str]:
    """Decode a source tab-delimited selector index without guessing ownership."""

    slots: dict[int, str] = {}
    for line_number, line in enumerate(raw.decode("utf-8").splitlines(), start=1):
        if not line:
            continue
        fields = line.split("\t", 1)
        require(len(fields) == 2, f"{member}:{line_number} is not a tab-delimited slot")
        slot_text, filename_field = fields
        filename = filename_field.split(",", 1)[0]
        require(filename.endswith(suffix), f"{member}:{line_number} is not a {suffix} slot")
        slot = int(slot_text)
        require(slot not in slots, f"{member}:{line_number} duplicates image slot {slot}")
        slots[slot] = filename
    require(slots, f"{member} has no image slots")
    return slots


def parse_image_index(raw: bytes, member: str) -> dict[int, str]:
    """Decode the source's tab-delimited image slots without assigning semantics."""

    return parse_named_index(raw, member, ".png")


def parse_seb_index(raw: bytes, member: str) -> dict[int, str]:
    """Decode the source's tab-delimited SEB slots without filename inference."""

    return parse_named_index(raw, member, ".seb")


def manifest_runtime_entries(display: dict[str, Any], character: dict[str, Any]) -> dict[str, dict[str, Any]]:
    entries: dict[str, dict[str, Any]] = {}
    for item in display["assets"]:
        entries[item["asset_member"]] = item
    for key in ("images", "animations"):
        for item in character[key]:
            entries[item["asset_member"]] = item
    return entries


def runtime_promotion(member: str, source_sha256: str, entries: dict[str, dict[str, Any]]) -> dict[str, Any]:
    item = entries.get(member)
    if item is None:
        return {"status": "NOT_PROMOTED"}
    runtime_path = RUNTIME_ROOT / item["runtime_path"]
    require(runtime_path.is_file(), f"missing promoted runtime asset: {runtime_path}")
    runtime_sha256 = sha256_file(runtime_path)
    declared_sha256 = item.get("runtime_sha256") or item.get("sha256")
    require(declared_sha256 is not None, f"runtime manifest has no SHA-256 for {member}")
    require(runtime_sha256 == declared_sha256, f"runtime manifest hash mismatch for {member}")
    require(runtime_sha256 == source_sha256, f"runtime asset is not byte-exact for {member}")
    return {
        "status": "PROMOTED_EXACT",
        "runtime_path": item["runtime_path"],
        "runtime_sha256": runtime_sha256,
    }


def source_image_association(
    archive: zipfile.ZipFile,
    prefix: str,
    seb_member: str,
    decoded: dict[str, Any],
    image_indexes: dict[str, dict[int, str]],
    runtime_entries: dict[str, dict[str, Any]],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Associate texture IDs only through the source pack's own img.inf slots."""

    pack = "/".join(seb_member.split("/")[:2])
    index_member = f"{pack}/img.inf"
    slots = image_indexes[pack]
    observed_ids = sorted({record["image_id"] for record in decoded["records"]})
    bindings: list[dict[str, Any]] = []
    unknowns: list[dict[str, Any]] = []
    for image_id in observed_ids:
        if image_id < 0:
            bindings.append(
                {
                    "image_id": image_id,
                    "status": "CONTROL_RECORD_NO_TEXTURE",
                    "record_count": sum(1 for record in decoded["records"] if record["image_id"] == image_id),
                }
            )
            continue
        filename = slots.get(image_id)
        if filename is None:
            unknown_id = f"visual-port-v1:texture-slot:{seb_member}:{image_id}"
            bindings.append({"image_id": image_id, "status": "UNKNOWN"})
            unknowns.append(
                {
                    "id": unknown_id,
                    "class": "SEB texture association",
                    "method": "img.inf slot lookup",
                    "question": f"Which {pack} PNG is referenced by image slot {image_id}?",
                    "known_evidence": [seb_member, index_member],
                    "missing_evidence": [f"{index_member} slot {image_id}"],
                    "affected_fixtures": [category for category, member in FIXTURES if member == seb_member],
                    "impact": "The decoded records are retained, but their source texture cannot be named.",
                    "next_investigation": "Recover the missing source img.inf slot without guessing from the SEB filename.",
                }
            )
            continue
        image_member = f"{pack}/{filename}"
        raw = archive.read(archive_member(prefix, image_member))
        source_sha256 = sha256_bytes(raw)
        bindings.append(
            {
                "image_id": image_id,
                "source_index_member": index_member,
                "source_member": image_member,
                "source_sha256": source_sha256,
                "status": "PROVEN_BY_SOURCE_SLOT",
                "runtime_promotion": runtime_promotion(image_member, source_sha256, runtime_entries),
            }
        )
    status = "PROVEN" if not unknowns else "UNKNOWN"
    return {"status": status, "bindings": bindings}, unknowns


def optimize_values(record: Any) -> list[int]:
    """Project one validated OPT record in the original seven-slot order."""

    return [
        record.source_reference,
        record.offset_x,
        record.offset_y,
        record.source_x,
        record.source_y,
        record.width,
        record.height,
    ]


def build_optimize_access(parsed: Any) -> dict[str, Any]:
    """Expose GetOptimize access keys without reimplementing OPT decoding."""

    require(parsed.header is not None, "OPT access requires a parsed header")
    access: dict[str, list[int]] = {}
    type_index: dict[str, list[int]] = {}
    for ordinal, record in enumerate(parsed.records):
        column = record.index % parsed.header.columns
        row = record.index // parsed.header.columns
        values = optimize_values(record)
        access[f"{column},{row},{record.part_index}"] = values
        type_index[f"0,{ordinal}"] = values
    return {
        "access": access,
        "type_index": type_index,
        "grid": {
            "columns": parsed.header.columns,
            "rows": parsed.header.rows,
            "max_pass": max((cell.piece_count for cell in parsed.cells), default=0),
        },
    }


def build_image_seb_associations(
    image_member: str,
    seb_records: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Keep Image-to-SEB source-slot relationships separate from OPT tuples."""

    associations: list[dict[str, Any]] = []
    for seb_record in seb_records:
        association = seb_record["source_image_association"]
        for binding in association["bindings"]:
            if binding.get("source_member") != image_member:
                continue
            associations.append(
                {
                    "seb_member": seb_record["source_member"],
                    "seb_sha256": seb_record["source_sha256"],
                    "image_id": binding["image_id"],
                    "source_index_member": binding["source_index_member"],
                    "status": binding["status"],
                }
            )
    return associations


def build_resource_lookup_contract(
    archive: zipfile.ZipFile,
    prefix: str,
    runtime_entries: dict[str, dict[str, Any]],
    resource_groups: dict[str, Any],
    image_indexes: dict[str, dict[int, str]],
    seb_records: list[dict[str, Any]],
    image_opt_records: list[dict[str, Any]],
    shared_source: dict[str, Any],
) -> dict[str, Any]:
    """Build group-plus-ID evidence only from source INF selectors and contracts."""

    seb_by_member = {record["source_member"]: record for record in seb_records}
    image_contract_by_member = {
        record["source_png"]["member"]: record["fixture_stem"] for record in image_opt_records
    }
    seb_indexes: dict[str, dict[int, str]] = {}
    image_bindings_by_group: dict[str, dict[int, dict[str, Any]]] = {
        group_id: {} for group_id in RESOURCE_GROUP_IDS
    }
    seb_bindings_by_group: dict[str, dict[int, dict[str, Any]]] = {
        group_id: {} for group_id in RESOURCE_GROUP_IDS
    }
    fixtures_by_group: dict[str, list[dict[str, Any]]] = {
        group_id: [] for group_id in RESOURCE_GROUP_IDS
    }

    for spec in RESOURCE_FIXTURE_SPECS:
        group_id = spec["group_id"]
        seb_member = spec["seb_member"]
        pack = "/".join(seb_member.split("/")[:2])
        image_index_member = f"{pack}/img.inf"
        image_slots = image_indexes[pack]
        if pack not in seb_indexes:
            seb_index_member = f"{pack}/seb.inf"
            seb_raw = archive.read(archive_member(prefix, seb_index_member))
            seb_indexes[pack] = parse_seb_index(seb_raw, seb_index_member)
        seb_index_member = f"{pack}/seb.inf"
        seb_slots = seb_indexes[pack]
        require(seb_slots.get(spec["seb_id"]) == seb_member.rsplit("/", 1)[-1], f"SEB selector drift for {seb_member}")

        for image_id in spec["image_ids"]:
            image_filename = image_slots.get(image_id)
            require(image_filename is not None, f"missing image selector {pack} slot {image_id}")
            image_member = f"{pack}/{image_filename}"
            image_raw = archive.read(archive_member(prefix, image_member))
            image_sha256 = sha256_bytes(image_raw)
            image_contract_stem = image_contract_by_member.get(image_member)
            binding = {
                "id": image_id,
                "source_index_member": image_index_member,
                "source_member": image_member,
                "source_sha256": image_sha256,
                "image_contract_stem": image_contract_stem,
                "runtime_promotion": runtime_promotion(image_member, image_sha256, runtime_entries),
                "status": "PROVEN_BY_SOURCE_SLOT_AND_IMAGE_CONTRACT"
                if image_contract_stem
                else "PROVEN_BY_SOURCE_SLOT",
            }
            existing = image_bindings_by_group[group_id].get(image_id)
            if existing is not None:
                require(existing == binding, f"conflicting image binding for {group_id}:{image_id}")
            image_bindings_by_group[group_id][image_id] = binding

        seb_filename = seb_slots[spec["seb_id"]]
        resolved_seb_member = f"{pack}/{seb_filename}"
        require(resolved_seb_member == seb_member, f"SEB source member drift for {seb_member}")
        seb_source_record = seb_by_member.get(resolved_seb_member)
        seb_raw = archive.read(archive_member(prefix, resolved_seb_member))
        seb_binding = {
            "id": spec["seb_id"],
            "source_index_member": seb_index_member,
            "source_member": resolved_seb_member,
            "source_sha256": sha256_bytes(seb_raw),
            "seb_contract_member": resolved_seb_member if seb_source_record is not None else None,
            "status": "PROVEN_BY_SOURCE_SLOT_AND_SEB_CONTRACT"
            if seb_source_record is not None
            else "PROVEN_BY_SOURCE_SLOT",
        }
        existing_seb = seb_bindings_by_group[group_id].get(spec["seb_id"])
        if existing_seb is not None:
            require(existing_seb == seb_binding, f"conflicting SEB binding for {group_id}:{spec['seb_id']}")
        seb_bindings_by_group[group_id][spec["seb_id"]] = seb_binding

        primary_image_id = spec["image_ids"][0] if spec["image_ids"] else None
        primary_image_member = (
            f"{pack}/{image_slots[primary_image_id]}" if primary_image_id is not None else None
        )
        primary_image_contract = (
            image_contract_by_member.get(primary_image_member) if primary_image_member is not None else None
        )
        fixtures_by_group[group_id].append(
            {
                "fixture_id": f"{group_id}:{spec['fixture_stem'].rsplit('/', 1)[-1]}",
                "group_id": group_id,
                "fixture_stem": spec["fixture_stem"],
                "image_id": primary_image_id,
                "seb_id": spec["seb_id"],
                "image_member": primary_image_member,
                "seb_member": resolved_seb_member,
                "image_contract_stem": primary_image_contract,
                "seb_contract_member": resolved_seb_member if seb_source_record is not None else None,
                "status": "PROVEN_BY_SOURCE_INDEX_AND_SELECTED_CONTRACT",
            }
        )

    group_catalog = {record["group_id"]: record for record in resource_groups["records"]}
    groups: list[dict[str, Any]] = []
    all_fixtures: list[dict[str, Any]] = []
    for group_id in RESOURCE_GROUP_IDS:
        source_group = group_catalog[group_id]
        group_fixtures = fixtures_by_group[group_id]
        all_fixtures.extend(group_fixtures)
        groups.append(
            {
                "group_id": group_id,
                "source_declaration": source_group["source_declaration"],
                "source_ref": source_group["source_ref"],
                "group_kind": source_group["group_kind"],
                "status": source_group["status"],
                "membership_status": "proven_selected_fixture_membership"
                if group_fixtures
                else "declaration_only_membership_unknown",
                "ownership": source_group["ownership"],
                "image_bindings": [
                    image_bindings_by_group[group_id][key]
                    for key in sorted(image_bindings_by_group[group_id])
                ],
                "seb_bindings": [
                    seb_bindings_by_group[group_id][key]
                    for key in sorted(seb_bindings_by_group[group_id])
                ],
                "fixtures": group_fixtures,
            }
        )

    return {
        "schema_version": "social-dev-visual-port-v1-resource-lookup-contract",
        "status": "pass",
        "source": {
            **shared_source,
            "resource_groups_path": "knowledge/fixtures/accepted/visual-port/resource-groups.json",
            "resource_groups_sha256": sha256_file(RESOURCE_GROUPS_PATH),
        },
        "group_ids": list(RESOURCE_GROUP_IDS),
        "groups": groups,
        "fixtures": all_fixtures,
        "atlas_contract": {
            "status": "deferred",
            "reason": "All selected Image contracts retain image_atlas_id=-1 and atlas_region=null; no atlas-backed fixture relationship is proven.",
            "affected_fixtures": [spec["fixture_stem"] for spec in RESOURCE_FIXTURE_SPECS],
        },
        "native_contract": {
            "load_image_seb_rvas": ["0x1C4FE24", "0x1C4FE94", "0x1C4FF04", "0x1C50050"],
            "load_rvas": ["0x1C506D0", "0x1C507CC", "0x1C51D1C", "0x1C51E4C", "0x1C51F6C"],
            "load_ready_rvas": ["0x1C52074", "0x1C507F4"],
            "load_start_rvas": ["0x1C521DC", "0x1C50F60"],
            "get_image_rva": "0x1C53DA0",
            "source_ref": "knowledge/fixtures/accepted/visual-port/native-method-map.json",
            "proof_class": "NATIVE-RVA-PINNED_SOURCE-INF-SELECTOR-MAPPED",
        },
    }


def build_unknowns_contract(
    shared_source: dict[str, Any],
    resource_lookup_contract: dict[str, Any],
    seb_contract: dict[str, Any],
    image_opt_contract: dict[str, Any],
) -> dict[str, Any]:
    """Materialize unresolved V1 branches with the required nine register fields."""

    unknowns: list[dict[str, Any]] = []
    for group in resource_lookup_contract["groups"]:
        if group["membership_status"] != "declaration_only_membership_unknown":
            continue
        unknowns.append(
            {
                "id": f"resource-group-membership:{group['group_id']}",
                "class": "ResourceManager",
                "method": "Load/LoadImage/LoadSeb",
                "question": f"Which source image and SEB IDs belong to the declared {group['group_id']} group for the standalone visual runtime?",
                "known_evidence": [group["source_ref"], "knowledge/fixtures/accepted/visual-port/resource-groups.json", "knowledge/fixtures/accepted/visual-port/v1/resource-lookup-contract.json"],
                "missing_evidence": ["A source load trace or selected fixture that binds this group to concrete img.inf/seb.inf IDs."],
                "affected_fixtures": [],
                "impact": "The group declaration is preserved, but no membership is exposed through a guessed runtime binding.",
                "next_investigation": "Trace the native ResourceManager load call for this group and promote one source-index-backed visual fixture before adding IDs.",
            }
        )

    depth_unknown = seb_contract["geometry_contract"]["depth_contract"]["unknowns"][0]
    unknowns.append(
        {
            "id": depth_unknown["id"],
            "class": depth_unknown["class"],
            "method": depth_unknown["method"],
            "question": depth_unknown["question"],
            "known_evidence": depth_unknown["known_evidence"],
            "missing_evidence": depth_unknown["missing_evidence"],
            "affected_fixtures": depth_unknown["affected_fixtures"],
            "impact": depth_unknown["impact"],
            "next_investigation": depth_unknown["next_investigation"],
        }
    )
    unknowns.extend(
        [
            {
                "id": "image-optimize-seb-payload-v1",
                "class": "Image",
                "method": "GetOptimizeSeb",
                "question": "Which OPT encoding produces a non-null optimizeSeb_ payload and how does it associate an Image with SEB records?",
                "known_evidence": ["Image.cs:6035", "native Image.GetOptimizeSeb 0x1C38ADC", "knowledge/fixtures/accepted/visual-port/v1/image-opt-contract.json"],
                "missing_evidence": ["A selected raw OPT fixture entering the optimizeSeb_ branch and a native return-value comparison."],
                "affected_fixtures": [record["fixture_stem"] for record in image_opt_contract["records"]],
                "impact": "The standard OPT path is proven; the separate optimizeSeb payload branch remains unimplemented.",
                "next_investigation": "Promote a source OPT/SEB pair with a nonzero optimizeSeb payload and compare all four returned fields to native output.",
            },
            {
                "id": "image-raster-resize-v1",
                "class": "Image",
                "method": "Resize",
                "question": "Which raster/backend state changes are required for native Image.Resize to update texture pixels and atlas regions?",
                "known_evidence": ["Image.cs:8433-8455", "native Image.Resize 0x1C3B5F0; 0x1C3B644; 0x1C3B654", "knowledge/fixtures/accepted/visual-port/v1/image-opt-contract.json"],
                "missing_evidence": ["Native texture pixel output and atlas-region state before and after Resize."],
                "affected_fixtures": [record["fixture_stem"] for record in image_opt_contract["records"]],
                "impact": "V1 exposes requested dimension metadata only; it does not claim raster pixel parity after resize.",
                "next_investigation": "Capture a native Image resize fixture with texture pixels and compare dimensions, ownership, and atlas mapping before porting raster behavior.",
            },
            {
                "id": "image-atlas-relationship-v1",
                "class": "ImageAtlas/ImageAtlasManager",
                "method": "ImageToAtlas/AtlasToImage",
                "question": "Which selected Image fixtures require non-default atlas identity or coordinate conversion?",
                "known_evidence": resource_lookup_contract["atlas_contract"]["reason"],
                "missing_evidence": ["A selected fixture with imageAtlasId != -1 or a non-null AtlasRegion and native coordinate conversion output."],
                "affected_fixtures": resource_lookup_contract["atlas_contract"]["affected_fixtures"],
                "impact": "Atlas methods remain outside the runtime path; selected images retain identity -1 and no region.",
                "next_investigation": "Trace a promoted atlas-backed resource through ImageAtlasManager before adding an atlas packer or coordinate transform.",
            },
        ]
    )
    return {
        "schema_version": "social-dev-visual-port-v1-unknowns",
        "status": "pass",
        "source": {
            **shared_source,
            "resource_lookup_contract": "knowledge/fixtures/accepted/visual-port/v1/resource-lookup-contract.json",
            "image_opt_contract": "knowledge/fixtures/accepted/visual-port/v1/image-opt-contract.json",
            "seb_contract": "knowledge/fixtures/accepted/visual-port/v1/seb-contract.json",
        },
        "unknowns": unknowns,
    }


def build_geometry_contract(seb_records: list[dict[str, Any]]) -> dict[str, Any]:
    """Materialize bounds from selected SEB destination records only.

    The observed layered grammar has no pixelBoundingRects_ or depth-line
    payload. Keep the native metadata boundary explicit instead of deriving
    bounds from a texture PNG or inventing depth values.
    """

    categories_by_member: dict[str, list[str]] = {}
    for category, member in FIXTURES:
        categories_by_member.setdefault(member, []).append(category)

    fixture_results: dict[str, Any] = {}
    for record in seb_records:
        decoded = record["decoded"]
        frames: dict[str, Any] = {}
        for frame in range(decoded["header"]["frame_bound"]):
            selected: list[dict[str, Any]] = []
            for layer in decoded["layers"]:
                candidates = [item for item in layer["records"] if item["start_frame"] <= frame]
                require(candidates, f"no active geometry record for {record['source_member']} frame {frame}")
                selected.append(candidates[-1])
            layer_rects = [
                [item["destination_x"], item["destination_y"], item["width"], item["height"]]
                for item in selected
            ]
            left = min(rect[0] for rect in layer_rects)
            top = min(rect[1] for rect in layer_rects)
            right = max(rect[0] + rect[2] for rect in layer_rects)
            bottom = max(rect[1] + rect[3] for rect in layer_rects)
            union = [left, top, right - left, bottom - top]
            frames[str(frame)] = {
                "layer_rects": layer_rects,
                "bounding_rect": union,
                "pixel_rect": union,
                "proof_class": "FORMAT-PROVEN_FALLBACK_NO_PIXEL_BOUNDING_METADATA",
            }
        fixture_results[record["source_member"]] = {
            "category_refs": categories_by_member[record["source_member"]],
            "frames": frames,
        }

    return {
        "status": "pass",
        "bounds_formula": {
            "b_rect": "Selected Sprite destination rect [TransX, TransY, W, H]; layer unions retain negative translations and source layer order.",
            "bounding_rect": "Union of selected layer destination rects for the explicit frame.",
            "pixel_rect": "Native GetPixelRect(frame) fallback to GetBRect(frame) when pixelBoundingRects_ is absent; no PNG dimensions are used.",
            "proof_class": "FORMAT-PROVEN_WITH_NATIVE_FALLBACK_BOUNDARY",
            "native_rvas": {
                "get_bounding_rect": ["0x1C5B290", "0x1C53444"],
                "get_pixel_rect": ["0x1C5B5A4", "0x1C5B6F8"],
            },
            "source_ref": "sources/raw/1_Click_CSharp_Code update/KairoEngine/kairo.unity.ui/Seb.cs:3167-3890",
        },
        "fixture_results": fixture_results,
        "depth_contract": {
            "status": "deferred",
            "reason": "The selected layered SEB grammar retains records but no native depth-line or depth metadata payload; GetDepthInfo therefore cannot be claimed as a recovered numeric result in V1.",
            "native_rvas": ["0x1C5D5EC", "0x1C52994", "0x1C61CE0"],
            "source_ref": "sources/raw/1_Click_CSharp_Code update/KairoEngine/kairo.unity.ui/Seb.cs:12280-13180",
            "unknowns": [
                {
                    "id": "seb-depth-info-format-v1",
                    "class": "Seb",
                    "method": "GetDepthInfo",
                    "question": "Which source/native payload populates depthLines and the per-frame DepthInfo groups for the selected SEBs?",
                    "known_evidence": "GetDepthInfo overload RVAs and the damaged source algorithm are pinned; selected decoded SEBs expose no depth-line payload.",
                    "missing_evidence": "Native depth metadata bytes or a closed parser for the depth-line payload.",
                    "affected_fixtures": sorted(fixture_results),
                    "impact": "Depth-aware ordering remains deferred; sprite flags and geometric bounds are still recovered.",
                    "next_investigation": "Trace the native SEB load path and inspect a fixture with a proven non-default depth payload before implementing numeric depth output.",
                }
            ],
        },
    }


def assert_fixture_properties(decoded_by_member: dict[str, dict[str, Any]]) -> None:
    door = decoded_by_member["01_GAME_PACKS/chip/door_02.seb"]
    require(door["header"]["layer_count"] == 1, "door_02 must have one layer")
    require(door["header"]["global_frame_count"] == 1, "door_02 must have one frame")

    wall = decoded_by_member["01_GAME_PACKS/chip/wall_00.seb"]
    require(wall["header"]["layer_count"] == 2, "wall_00 must have two layers")
    require(wall["header"]["global_frame_count"] == 4, "wall_00 must have four frames")

    for member in ("01_GAME_PACKS/chip/chair_00.seb", "01_GAME_PACKS/chip/desk_00.seb"):
        require(decoded_by_member[member]["header"]["global_frame_count"] == 3, f"{member} must have three frames")

    wait_left = decoded_by_member["01_GAME_PACKS/human/wait_left.seb"]
    require(any(record["flags"] != 0 for record in wait_left["records"]), "wait_left must retain a non-zero flip flag")

    avatar = decoded_by_member["01_GAME_PACKS/avatar_body/wait_right.seb"]
    require(avatar["header"]["layer_count"] > 1, "avatar-body wait_right must be multi-layer")
    require(avatar["header"]["global_frame_count"] > 1, "avatar-body wait_right must be multi-frame")


def build() -> dict[str, str]:
    seb_catalog = load_json(SEB_CATALOG_PATH)
    display_manifest = load_json(DISPLAY_MANIFEST_PATH)
    character_manifest = load_json(CHARACTER_MANIFEST_PATH)
    resource_groups = load_json(RESOURCE_GROUPS_PATH)
    source = seb_catalog["source"]
    archive_path = ROOT / source["zip_path"]
    require(archive_path.is_file(), f"source ZIP is missing: {archive_path}")
    archive_sha256 = sha256_file(archive_path)
    require(archive_sha256 == source["zip_sha256"], "source ZIP SHA-256 differs from seb_catalog.json")

    prefix = source["archive_prefix"]
    catalog_by_member = {item["member"]: item for item in seb_catalog["assets"]}
    runtime_entries = manifest_runtime_entries(display_manifest, character_manifest)
    image_indexes: dict[str, dict[int, str]] = {}
    decoded_by_member: dict[str, dict[str, Any]] = {}
    seb_records: list[dict[str, Any]] = []
    unknown_register: list[dict[str, Any]] = []

    with zipfile.ZipFile(archive_path, "r") as archive:
        for member in UNIQUE_SEB_MEMBERS:
            require(archive_member(prefix, member) in archive.namelist(), f"missing source member: {member}")
            catalog_entry = catalog_by_member.get(member)
            require(catalog_entry is not None, f"SEB catalog does not include {member}")
            raw = archive.read(archive_member(prefix, member))
            source_sha256 = sha256_bytes(raw)
            require(source_sha256 == catalog_entry["sha256"], f"SEB catalog SHA-256 mismatch for {member}")
            decoded = decode_seb(raw, member)
            require(decoded == catalog_entry["decode"], f"SEB decoder output drift for {member}")
            decoded_by_member[member] = decoded

            pack = "/".join(member.split("/")[:2])
            if pack not in image_indexes:
                index_member = f"{pack}/img.inf"
                index_raw = archive.read(archive_member(prefix, index_member))
                image_indexes[pack] = parse_image_index(index_raw, index_member)
            association, unknowns = source_image_association(
                archive, prefix, member, decoded, image_indexes, runtime_entries
            )
            unknown_register.extend(unknowns)
            seb_records.append(
                {
                    "source_member": member,
                    "source_sha256": source_sha256,
                    "source_bytes": len(raw),
                    "catalog_ref": {
                        "path": "knowledge/fixtures/accepted/seb_catalog.json",
                        "content_hash": seb_catalog["determinism"]["content_hash"],
                    },
                    "decoded": decoded,
                    "source_image_association": association,
                    "runtime_promotion": runtime_promotion(member, source_sha256, runtime_entries),
                }
            )

        assert_fixture_properties(decoded_by_member)

        image_opt_records: list[dict[str, Any]] = []
        for stem in IMAGE_OPT_FIXTURES:
            png_member = f"{stem}.png"
            opt_member = f"{stem}.opt"
            png_raw = archive.read(archive_member(prefix, png_member))
            opt_raw = archive.read(archive_member(prefix, opt_member))
            parsed = parse_opt(opt_raw, opt_member)
            reconstruction = reconstruct_opt(png_raw, opt_raw, png_member, opt_member)
            require(parsed.status == "pass", f"OPT parser did not pass for {opt_member}: {parsed.errors}")
            require(reconstruction.status == "pass", f"OPT reconstruction did not pass for {stem}: {reconstruction.issues}")
            png_sha256 = sha256_bytes(png_raw)
            opt_sha256 = sha256_bytes(opt_raw)
            png_runtime = runtime_promotion(png_member, png_sha256, runtime_entries)
            opt_runtime = runtime_promotion(opt_member, opt_sha256, runtime_entries)
            require(png_runtime["status"] == "PROMOTED_EXACT", f"{png_member} must be promoted exactly")
            require(opt_runtime["status"] == "PROMOTED_EXACT", f"{opt_member} must be promoted exactly")

            derived = next(
                (
                    item
                    for item in display_manifest["assets"]
                    if item.get("kind") == "derived_opt_reconstruction"
                    and item.get("provenance", {}).get("source_asset_member") == png_member
                ),
                None,
            )
            require(derived is not None, f"missing promoted logical image for {png_member}")
            logical_runtime_path = RUNTIME_ROOT / derived["runtime_path"]
            require(logical_runtime_path.is_file(), f"missing logical runtime image: {logical_runtime_path}")
            logical_runtime_raw = logical_runtime_path.read_bytes()
            require(sha256_bytes(logical_runtime_raw) == derived["sha256"], f"logical runtime raw hash mismatch for {stem}")
            from PIL import Image  # Imported here to keep the codec as the image-processing authority.
            from io import BytesIO

            source_image = Image.open(BytesIO(png_raw)).convert("RGBA")
            source_pixel_sha256 = sha256_bytes(source_image.tobytes())
            logical_runtime_pixels = Image.open(BytesIO(logical_runtime_raw)).convert("RGBA").tobytes()
            require(
                sha256_bytes(logical_runtime_pixels) == reconstruction.pixel_sha256,
                f"logical runtime pixels differ from source reconstruction for {stem}",
            )
            require(reconstruction.pixel_sha256 is not None, f"missing logical pixel hash for {stem}")
            optimize_access = build_optimize_access(parsed)
            seb_associations = build_image_seb_associations(png_member, seb_records)
            image_opt_records.append(
                {
                    "fixture_stem": stem,
                    "source_png": {
                        "member": png_member,
                        "raw_sha256": png_sha256,
                        "bytes": len(png_raw),
                        "runtime_promotion": png_runtime,
                    },
                    "source_opt": {
                        "member": opt_member,
                        "raw_sha256": opt_sha256,
                        "bytes": len(opt_raw),
                        "runtime_promotion": opt_runtime,
                    },
                    "logical_reconstruction": reconstruction.to_dict(),
                    "logical_runtime_promotion": {
                        "status": "PROMOTED_PIXEL_EXACT",
                        "runtime_path": derived["runtime_path"],
                        "raw_sha256": sha256_bytes(logical_runtime_raw),
                        "pixel_sha256": sha256_bytes(logical_runtime_pixels),
                    },
                    "opt": reconstruction.to_dict()["opt"],
                    "source_size": {
                        "width": source_image.width,
                        "height": source_image.height,
                    },
                    "logical_size": {
                        "width": reconstruction.logical_size[0] if reconstruction.logical_size else 0,
                        "height": reconstruction.logical_size[1] if reconstruction.logical_size else 0,
                    },
                    "pixel_sha256": reconstruction.pixel_sha256,
                    "source_png_pixel_sha256": source_pixel_sha256,
                    "optimize_access": optimize_access["access"],
                    "optimize_type_index": optimize_access["type_index"],
                    "optimize_grid": optimize_access["grid"],
                    "seb_associations": [None],
                    "optimize_seb_contract": {
                        "status": "absent_standard_opt_path",
                        "proof_class": "FORMAT-PROVEN_NO_OPTIMIZE_SEB_PAYLOAD",
                        "source_ref": "sources/raw/1_Click_CSharp_Code update/KairoEngine/kairo.unity.ui/Image.cs:2484-5535",
                    },
                    "associated_seb_ids": seb_associations,
                    "image_atlas_id": -1,
                    "atlas_region": None,
                    "native_contract": {
                        "load_optimize_rvas": ["0x1C375E4", "0x1C386B4"],
                        "get_optimize_rvas": ["0x1C387C8", "0x1C38ABC", "0x1C38ACC", "0x1C38864"],
                        "get_optimize_seb_rva": "0x1C38ADC",
                        "use_unuse_rvas": ["0x1C38C90", "0x1C38D98"],
                        "resize_rvas": ["0x1C3B5F0", "0x1C3B644", "0x1C3B654"],
                        "set_image_atlas_id_rva": "0x1C3BD84",
                        "proof_class": "NATIVE-RVA-PINNED_FORMAT-PROVEN_VALUES",
                        "source_ref": "knowledge/fixtures/accepted/visual-port/native-method-map.json",
                    },
                    "lifetime_contract": {
                        "status": "metadata_only",
                        "use": "increments contract useCount",
                        "unuse": "decrements contract useCount and is a no-op at zero",
                        "raster_loading": "deferred",
                    },
                    "resize_contract": {
                        "status": "metadata_only",
                        "raster_parity": "deferred",
                        "source_ref": "sources/raw/1_Click_CSharp_Code update/KairoEngine/kairo.unity.ui/Image.cs:8433-8455",
                    },
                }
            )

        resource_lookup_contract = build_resource_lookup_contract(
            archive,
            prefix,
            runtime_entries,
            resource_groups,
            image_indexes,
            seb_records,
            image_opt_records,
            shared_source={
                "zip_path": source["zip_path"],
                "zip_sha256": archive_sha256,
                "archive_prefix": prefix,
                "seb_catalog_path": "knowledge/fixtures/accepted/seb_catalog.json",
                "seb_catalog_content_hash": seb_catalog["determinism"]["content_hash"],
            },
        )

    seb_by_member = {record["source_member"]: record for record in seb_records}
    fixture_records = [
        {
            "category": category,
            "source_member": member,
            "source_sha256": seb_by_member[member]["source_sha256"],
            "seb_contract_member": member,
            "source_image_association_status": seb_by_member[member]["source_image_association"]["status"],
        }
        for category, member in FIXTURES
    ]
    shared_source = {
        "zip_path": source["zip_path"],
        "zip_sha256": archive_sha256,
        "archive_prefix": prefix,
        "seb_catalog_path": "knowledge/fixtures/accepted/seb_catalog.json",
        "seb_catalog_content_hash": seb_catalog["determinism"]["content_hash"],
    }
    fixture_manifest = {
        "schema_version": "social-dev-visual-port-v1-fixture-manifest",
        "status": "pass",
        "source": shared_source,
        "fixtures": [category for category, _ in FIXTURES],
        "fixture_records": fixture_records,
        "unknown_register": unknown_register,
    }
    seb_contract = {
        "schema_version": "social-dev-visual-port-v1-seb-contract",
        "status": "pass",
        "source": shared_source,
        "decoder": "tools/social-dev/seb_codec.py:decode_seb",
        "interpreter_contract": {
            "explicit_frame_rule": {
                "active_record": "Within each preserved source layer, select the final source-order record whose start_frame is less than or equal to the explicit frame reduced by the native signed remainder frame % 10000.",
                "counterexamples": [
                    {
                        "fixture": "multi_layer",
                        "input_frame": 4,
                        "layer": 0,
                        "must_select_source_record_index": 3,
                        "must_not_wrap_to_source_record_index": 0,
                        "source_member": "01_GAME_PACKS/chip/wall_00.seb",
                    },
                    {
                        "fixture": "flip",
                        "input_frame": 10,
                        "layer": 0,
                        "must_select_source_record_index": 1,
                        "must_not_select_source_record_index": 0,
                        "source_member": "01_GAME_PACKS/human/wait_left.seb",
                    },
                ],
                "native_rva": "0x1C5BC08",
                "proof_class": "native_GetSprite_frameNo_remainder_10000_plus_source_order_start_frame_selection",
                "source_ref": "sources/raw/1_Click_CSharp_Code update/KairoEngine/kairo.unity.ui/Seb.cs:4251-7374",
            },
            "frame_state_rule": {
                "Frame": "currentFrame_ = (currentFrame_ + 1) % maxFrame_",
                "SetCurFrame": "Stores the supplied native integer frame directly; it does not normalize the value.",
                "counterexample": {
                    "fixture": "multi_layer",
                    "input_current_frame": 4,
                    "max_frame": 4,
                    "result_after_Frame": 1,
                },
                "native_rva": "0x1C5B9CC",
                "source_ref": "sources/raw/1_Click_CSharp_Code update/KairoEngine/kairo.unity.ui/Seb.cs:3894-3940",
            },
            "source_order_rule": {
                "GetSprites": "Calls GetSprite(frameNo, layer) once for each layer head in ascending source layer order; the TypeScript projection keeps that order and every decoded layer_record_index.",
                "native_rva": "0x1C5BAA4",
                "source_ref": "sources/raw/1_Click_CSharp_Code update/KairoEngine/kairo.unity.ui/Seb.cs:3942-4117",
            },
            "typescript_boundary": {
                "accepted_decoder_status": "pass",
                "rejected_decoder_conditions": [
                    "nonzero trailing_bytes",
                    "nonempty metadata_warnings",
                    "record frame_status other than in_header_frame_bound",
                ],
                "raw_byte_decoding": "deferred_to_tools/social-dev/seb_codec.py; TypeScript consumes only decoded JSON contracts",
                "status": "task4_recovered",
            },
        },
        "geometry_contract": build_geometry_contract(seb_records),
        "records": seb_records,
        "unknown_register": unknown_register,
    }
    image_opt_contract = {
        "schema_version": "social-dev-visual-port-v1-image-opt-contract",
        "status": "pass",
        "source": shared_source,
        "codec": {
            "parse_opt": "tools/social-dev/opt_codec.py:parse_opt",
            "reconstruct_opt": "tools/social-dev/opt_codec.py:reconstruct_opt",
        },
        "records": image_opt_records,
    }
    unknowns_contract = build_unknowns_contract(
        shared_source,
        resource_lookup_contract,
        seb_contract,
        image_opt_contract,
    )
    write_json(EVIDENCE / "fixture-manifest.json", fixture_manifest)
    write_json(EVIDENCE / "seb-contract.json", seb_contract)
    write_json(EVIDENCE / "image-opt-contract.json", image_opt_contract)
    write_json(EVIDENCE / "resource-lookup-contract.json", resource_lookup_contract)
    write_json(EVIDENCE / "unknowns.json", unknowns_contract)
    return {
        "fixture_manifest_hash": add_determinism(fixture_manifest)["determinism"]["content_hash"],
        "seb_contract_hash": add_determinism(seb_contract)["determinism"]["content_hash"],
        "image_opt_contract_hash": add_determinism(image_opt_contract)["determinism"]["content_hash"],
        "resource_lookup_contract_hash": add_determinism(resource_lookup_contract)["determinism"]["content_hash"],
        "unknowns": str(len(unknowns_contract["unknowns"])),
    }


def main() -> int:
    print(json.dumps(build(), sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
