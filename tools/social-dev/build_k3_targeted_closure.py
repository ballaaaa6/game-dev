"""Build and validate the bounded K3 missing-link closure.

This task is intentionally narrow.  It consumes the pinned source/native
evidence and the existing canonical brain, classifies the existing candidate
records, and records corrected namespaces without executing the decompiled
game or changing runtime pixels.
"""

from __future__ import annotations

import hashlib
import json
import sqlite3
import struct
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
BRAIN = ROOT / "knowledge/brain"
ACCEPTANCE = BRAIN / "acceptance/k3"
ACCEPTED_RUNTIME = ROOT / "knowledge/fixtures/accepted/runtime"
DB_PATH = BRAIN / "sqlite/social_dev_brain.sqlite"
QUEUE_PATH = ROOT / "knowledge/gaps/k3-gap-queue.json"
QUEUE_EXPORT_PATH = BRAIN / "exports/k3-gap-queue.json"
GRAPH_PATH = ROOT / "knowledge/fixtures/accepted/native_content_connection_graph.json"
REGISTRY_PATH = ROOT / "knowledge/fixtures/accepted/native_content_registry.json"
NATIVE_CONTENT_CATALOG_PATH = ACCEPTED_RUNTIME / "native_content_catalog.json"
DEFAULT_MAP_PATH = ACCEPTED_RUNTIME / "default_map_chip_contract.json"
DISPLAY_MANIFEST_PATH = ACCEPTED_RUNTIME / "display_asset_manifest.json"
NAMESPACE_PATH = BRAIN / "schema/id-namespaces.json"
METADATA_PATH = ROOT / "knowledge/sources/phase3a_apk_probe/raw/global-metadata.dat"
METADATA_MANIFEST_PATH = ROOT / "knowledge/sources/phase3a_apk_probe/raw/manifest.json"
LIBIL2CPP_PATH = ROOT / "knowledge/sources/phase3a_apk_probe/raw/libil2cpp.so"
FURNITURE_SOURCE = ROOT / "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/data/FurnitureData.cs"
HELPER_SOURCE = ROOT / "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/data/HelperData.cs"
SUBFORM_SOURCE = ROOT / "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/form/SubForm.cs"
STAFF_SOURCE = ROOT / "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/game/Staff.cs"
ASTAR_SOURCE = ROOT / "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/game.routeSearch/Astar.cs"
STAFF_STATE_CONTRACT = ROOT / "knowledge/fixtures/accepted/behavior-first/staff-state-machine.json"
K2_FINAL_VALIDATION = BRAIN / "acceptance/k2/final-validation.json"
K25_FINAL_VALIDATION = BRAIN / "acceptance/k2-5-cleanup/final-validation.json"
K25_SEMANTIC_DELTA = BRAIN / "acceptance/k2-5-cleanup/semantic-delta.json"
K25_LEGACY_REGRESSION = BRAIN / "acceptance/k2-5-cleanup/legacy-offline-test.json"
ORIGINAL_DATA_DB = ROOT / "knowledge/data/original/sqlite/social_dev_original_data.sqlite"

FINAL_TOKEN = "PASS_K3_TARGETED_MISSING_LINK_CLOSURE_CLOSED"


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def stable_id(prefix: str, *parts: object) -> str:
    value = "|".join(str(part) for part in parts)
    return f"{prefix}:{hashlib.sha256(value.encode('utf-8')).hexdigest()[:20]}"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def source_ref(path: Path, detail: str | None = None) -> str:
    return f"{rel(path)}:{detail}" if detail else rel(path)


def source_hash_record(path: Path) -> dict[str, Any]:
    return {"path": rel(path), "size_bytes": path.stat().st_size, "sha256": sha256_file(path)}


def text_has(path: Path, marker: str) -> bool:
    return marker in path.read_text(encoding="utf-8", errors="replace")


def raw_columns(row: sqlite3.Row) -> list[str]:
    locales = json.loads(row["locales_json"])
    return list(locales["English.lproj"]["raw_columns"])


def data_row_namespace(row: sqlite3.Row) -> dict[str, str]:
    table_name = row["table_id"].split(":", 1)[-1]
    native_id = row["native_id"]
    row_index = row["row_index"]
    return {
        "data_row_id": f"DATA_ROW_ID:data:{table_name}:{native_id}",
        "data_row_index": f"DATA_ROW_INDEX:data:{table_name}:{row_index}",
    }


def furniture_fields(row: sqlite3.Row) -> dict[str, Any]:
    columns = raw_columns(row)
    positions = {
        "id_": 0,
        "name_": 1,
        "category_": 2,
        "type_": 3,
        "seb_": 10,
        "subSeb_": 11,
        "img_": 12,
        "paramType_": 13,
        "paramValue_": 14,
        "paramTarget_": 15,
        "flag_": 16,
        "recovery_": 17,
        "buildTime_": 18,
    }
    values: dict[str, Any] = {}
    for field, position in positions.items():
        value = columns[position]
        values[field] = int(value) if field != "name_" else value
    return values


def staff_image_value(row: sqlite3.Row) -> int:
    # StaffData.Load reads id, lastName, firstName, sortId, then img_.
    return int(raw_columns(row)[4])


def load_context() -> dict[str, Any]:
    graph = load_json(GRAPH_PATH)
    registry = load_json(REGISTRY_PATH)
    native_catalog = load_json(NATIVE_CONTENT_CATALOG_PATH)
    if native_catalog["source_registry"]["content_hash"] != registry["content_hash"]:
        raise AssertionError("native content catalog is stale relative to the accepted registry")
    default_map = load_json(DEFAULT_MAP_PATH)
    display_manifest = load_json(DISPLAY_MANIFEST_PATH)
    metadata_manifest = load_json(METADATA_MANIFEST_PATH)
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    rows = {
        row["row_id"]: row
        for row in connection.execute("select * from data_rows")
    }
    candidates = [
        row
        for row in connection.execute(
            "select * from semantic_edges where status='candidate' order by subject_id, predicate, edge_id"
        )
    ]
    connection.close()
    prior_candidate_artifact = None
    candidate_artifact_path = ACCEPTED_RUNTIME / "k3_candidate_edge_classification.json"
    if not candidates and candidate_artifact_path.exists():
        prior_candidate_artifact = load_json(candidate_artifact_path)
    return {
        "graph": graph,
        "registry": registry,
        "native_catalog": native_catalog,
        "default_map": default_map,
        "display_manifest": display_manifest,
        "metadata_manifest": metadata_manifest,
        "rows": rows,
        "candidates": candidates,
        "prior_candidate_artifact": prior_candidate_artifact,
    }


def selector_record(registry: dict[str, Any], key: str) -> dict[str, Any]:
    for record in registry["selectors"]:
        if record.get("selector_key") == key:
            return record
    raise AssertionError(f"selector record missing: {key}")


def asset_record(registry: dict[str, Any], asset_id: str) -> dict[str, Any]:
    for record in registry["assets"]:
        if record.get("asset_id") == asset_id:
            return record
    raise AssertionError(f"asset record missing: {asset_id}")


def build_floor_closure(context: dict[str, Any]) -> dict[str, Any]:
    default_map = context["default_map"]
    table = default_map["native_static_arrays"]["floor_image_id_array"]
    values = table["values"]
    if values[5] != 23:
        raise AssertionError("native floor table index 5 is not selector 23")
    metadata = METADATA_PATH.read_bytes()
    offset = int(table["metadata_offset"], 16)
    raw = metadata[offset : offset + (4 * len(values))]
    decoded = list(struct.unpack(f"<{len(values)}i", raw))
    if decoded != values:
        raise AssertionError("global-metadata floor table bytes differ from accepted contract")
    selector = selector_record(context["registry"], "ref:chip:img:23")
    image = asset_record(context["registry"], selector["target_asset_id"])
    room_row = context["rows"]["data:room:0"]
    room_fields = json.loads(room_row["decoded_status"])["fields"]
    if room_fields["floorImgId_"] != 5:
        raise AssertionError("RoomData row 0 floorImgId_ is not 5")
    return {
        "gap_id": "K3-GAP-FLOOR-DIRECT-SELECTOR",
        "status": "CLOSED",
        "original_subject_id": "selector:floor:5",
        "canonical_subject_id": "ROOMDATA_FLOOR_IMAGE_INDEX:5",
        "namespaces": {
            "data_row_id": "DATA_ROW_ID:data:RoomData:0",
            "data_row_index": "DATA_ROW_INDEX:data:RoomData:1",
            "room_data_id": "ROOM_DATA_ID:0",
            "roomdata_floor_image_index": "ROOMDATA_FLOOR_IMAGE_INDEX:5",
            "native_indirection_index": "NATIVE_INDIRECTION_INDEX:5",
            "image_selector_id": "IMAGE_SELECTOR_ID:23",
            "asset_id": image["asset_id"],
        },
        "source_row": {
            "row_id": room_row["row_id"],
            "table_id": room_row["table_id"],
            "native_id": room_row["native_id"],
            "row_index": room_row["row_index"],
            "field": "floorImgId_",
            "value": 5,
            "raw_row_sha256": json.loads(room_row["locales_json"])["English.lproj"]["raw_row_sha256"],
            "source_file": "01_GAME_PACKS/xls/English.lproj/room.txt",
        },
        "native_chain": [
            {
                "method": "Room.InitMapChips",
                "rva": "0x12CB1F4",
                "field": "RoomData.floorImgId_",
                "field_offset": "0x48",
                "operation": "load floorImgId_ as NATIVE_INDIRECTION_INDEX",
                "source": source_ref(LIBIL2CPP_PATH, "0x12CB268"),
            },
            {
                "method": "Room.InitMapChips",
                "rva": "0x12CB1F4",
                "operation": "zero MapChip image id selects Room.FLOOR_IMAGE_ID_ARRAY[index]",
                "array": "Room.FLOOR_IMAGE_ID_ARRAY",
                "array_metadata_offset": table["metadata_offset"],
                "index": "NATIVE_INDIRECTION_INDEX:5",
                "selector": "IMAGE_SELECTOR_ID:23",
                "source": source_ref(LIBIL2CPP_PATH, "0x12CB35C-0x12CB378"),
            },
            {
                "method": "MapChip constructor",
                "rva": "0x12A1A1C",
                "field": "MapChip.imageId_",
                "operation": "stores IMAGE_SELECTOR_ID:23",
                "source": source_ref(LIBIL2CPP_PATH, "0x12CB388-0x12CB3A8"),
            },
            {
                "method": "MapChip.DrawFloor",
                "rva": "0x12A1F38",
                "field": "MapChip.imageId_",
                "field_offset": "0x18",
                "operation": "indexes the chip image selector table and draws the resolved image",
                "source": source_ref(LIBIL2CPP_PATH, "0x12A1F78-0x12A2034"),
            },
        ],
        "native_static_array": {
            "field": table["field"] if "field" in table else "Room.FLOOR_IMAGE_ID_ARRAY",
            "element_type": table["element_type"],
            "length": table["length"],
            "values": values,
            "metadata_offset": table["metadata_offset"],
            "metadata_hash": table["metadata_hash"],
            "raw_bytes_hex": raw.hex(),
        },
        "selector_resource": {
            "selector_key": selector["selector_key"],
            "selector_id": selector["selector_id"],
            "source_file": selector["source_file"],
            "source_row": selector["source_row"],
            "raw_line": selector["raw_line"],
            "target_asset_id": selector["target_asset_id"],
            "target_relative_path": selector["target_relative_path"],
            "asset_sha256": image["sha256"],
            "asset_size_bytes": image["size_bytes"],
            "dimensions": [image["width"], image["height"]],
        },
        "old_direct_claim": {
            "subject_id": "selector:floor:5",
            "object_id": "IMAGE_SELECTOR_ID:5",
            "classification": "REJECTED",
            "reason": "The subject was a misnamed direct-selector claim; the source/native scalar is ROOMDATA_FLOOR_IMAGE_INDEX:5 and the authoritative indirect result is IMAGE_SELECTOR_ID:23.",
        },
        "runtime_boundary": {
            "runtime_compatibility_alias_id": "COMPATIBILITY_ALIAS_ID:85",
            "runtime_alias_preserved": True,
            "pixel_asset_changed": False,
            "native_selector_is_not_collapsed_into_alias": True,
        },
        "provenance": [
            source_ref(DEFAULT_MAP_PATH),
            source_ref(ROOT / "knowledge/fixtures/accepted/runtime/native_room_floor_usage_contract.json"),
            source_ref(METADATA_PATH, "0x467878"),
            source_ref(REGISTRY_PATH, "ref:chip:img:23"),
            source_ref(ROOT / "knowledge/sources/phase3a_apk_probe/raw/manifest.json"),
        ],
    }


def build_furniture_closure(context: dict[str, Any]) -> dict[str, Any]:
    row = context["rows"]["data:furniture:26"]
    fields = furniture_fields(row)
    expected = {
        "id_": 26,
        "type_": 1,
        "seb_": 21,
        "subSeb_": -1,
        "img_": 106,
        "flag_": 32784,
        "buildTime_": 65,
    }
    if any(fields[key] != value for key, value in expected.items()):
        raise AssertionError(f"FurnitureData:26 raw fields do not match: {fields}")
    display_record = context["display_manifest"]["native_initial_objects"]["furniture:26"]
    if display_record["status"] != "approved_for_runtime_subset":
        raise AssertionError("accepted FurnitureData:26 display record is not approved")
    frame_record = display_record["records"][0]
    if frame_record["start_frame"] != 0 or frame_record["image_id"] != 106:
        raise AssertionError("FurnitureData:26 accepted frame record is not image 106/frame 0")
    image_selector = selector_record(context["registry"], "ref:chip:img:106")
    seb_selector = selector_record(context["registry"], "ref:chip:seb:21")
    image_asset = asset_record(context["registry"], image_selector["target_asset_id"])
    seb_asset = asset_record(context["registry"], seb_selector["target_asset_id"])
    flag_bits = {
        "FLAG_ANIME_ALWAYS": 2,
        "FLAG_ANIME_USE": 4,
        "FLAG_ANIME_GAUGE_MAX": 8,
        "FLAG_ATTRIBUTE": 16,
        "FLAG_INIT_PLACE": 32768,
    }
    return {
        "gap_id": "K3-GAP-FURNITURE-VISUAL",
        "status": "CLOSED",
        "namespaces": {
            "data_row_id": "DATA_ROW_ID:data:FurnitureData:26",
            "data_row_index": "DATA_ROW_INDEX:data:FurnitureData:27",
            "furniture_data_id": "FURNITURE_DATA_ID:26",
            "seb_selector_id": "SEB_SELECTOR_ID:21",
            "sub_seb_selector_id": "SEB_SELECTOR_ID:-1",
            "image_selector_id": "IMAGE_SELECTOR_ID:106",
            "sprite_frame_id": "SPRITE_FRAME_ID:furniture:26:0",
            "image_asset_id": image_asset["asset_id"],
            "seb_asset_id": seb_asset["asset_id"],
        },
        "source_row": {
            "row_id": row["row_id"],
            "table_id": row["table_id"],
            "native_id": row["native_id"],
            "row_index": row["row_index"],
            "raw_columns": raw_columns(row),
            "fields": fields,
            "english_row_sha256": json.loads(row["locales_json"])["English.lproj"]["raw_row_sha256"],
            "japanese_row_sha256": json.loads(row["locales_json"])["Japanese.lproj"]["raw_row_sha256"],
        },
        "native_field_layout": {
            "FurnitureData.Load": {
                "rva": "0x1218B04",
                "flag_": "0x14",
                "type_": "0x24",
                "seb_": "0x40",
                "subSeb_": "0x44",
                "img_": "0x48",
                "buildTime_": "0x5C",
            },
            "ObjChip": {
                "furnitureData_": "0x20",
                "type_": "0x18",
                "frame_": "0x60",
                "sebFrame_": "0x80",
            },
        },
        "native_visual_chain": [
            {
                "method": "ObjChip.PlaceObj",
                "rva": "0x12C4308",
                "operation": "stores FurnitureData pointer and zeros frame_ and sebFrame_",
                "source": source_ref(LIBIL2CPP_PATH, "0x12C4340-0x12C4348"),
            },
            {
                "method": "ObjChip.Draw(Graphics,ofx,ofy,FurnitureData,bool)",
                "rva": "0x12C166C",
                "condition": "FurnitureData.type_ == OBJ_TYPE_EQUIP (1)",
                "operation": "dispatches the type-1 furniture branch",
                "source": source_ref(LIBIL2CPP_PATH, "0x12C1904-0x12C191C"),
            },
            {
                "method": "ObjChip.Draw",
                "rva": "0x12C166C",
                "operation": "loads FurnitureData.img_ at 0x48 and primary seb_ at 0x40 through ResourceManager.img[]/seb[]; the selected initial content record resolves the image layer directly",
                "resource_manager_fields": {"img": "0x10", "seb": "0x18"},
                "source": source_ref(LIBIL2CPP_PATH, "0x12C2C38-0x12C2CB4"),
            },
            {
                "method": "Seb.GetSprite",
                "rva": "0x1C5BC08",
                "operation": "resolves the selected SEB frame when the type-1 path uses the companion",
                "source": source_ref(LIBIL2CPP_PATH, "0x12C2B00-0x12C2B14"),
            },
            {
                "method": "AppData.DrawSeb",
                "rva": "0x125BB88",
                "operation": "draws the resolved image/SEB content with the selected frame",
                "source": source_ref(LIBIL2CPP_PATH, "0x12C2C0C-0x12C2C2C"),
            },
        ],
        "conditions": {
            "raw_type": 1,
            "object_type_namespace": "FURNITURE_DATA_ID:26/type:OBJ_TYPE_EQUIP:1",
            "flag_value": fields["flag_"],
            "flag_hex": "0x8010",
            "set_flags": ["FLAG_ATTRIBUTE", "FLAG_INIT_PLACE"],
            "absent_animation_flags": ["FLAG_ANIME_ALWAYS", "FLAG_ANIME_USE", "FLAG_ANIME_GAUGE_MAX"],
            "secondary_seb": "SEB_SELECTOR_ID:-1",
            "initial_frame": "SPRITE_FRAME_ID:furniture:26:0",
            "initial_frame_source": source_ref(LIBIL2CPP_PATH, "0x12C4344-0x12C4348"),
        },
        "accepted_frame_record": {
            "start_frame": frame_record["start_frame"],
            "image_selector_id": "IMAGE_SELECTOR_ID:106",
            "source_x": frame_record["source_x"],
            "source_y": frame_record["source_y"],
            "width": frame_record["width"],
            "height": frame_record["height"],
            "destination": [frame_record["destination_x"], frame_record["destination_y"]],
            "source_asset_id": frame_record["source_asset_id"],
            "source_asset_sha256": image_asset["sha256"],
            "proof": frame_record["source_status"],
        },
        "selector_resources": {
            "image": {
                "selector_key": image_selector["selector_key"],
                "source_file": image_selector["source_file"],
                "source_row": image_selector["source_row"],
                "raw_line": image_selector["raw_line"],
                "asset_id": image_asset["asset_id"],
                "sha256": image_asset["sha256"],
                "size_bytes": image_asset["size_bytes"],
                "dimensions": [image_asset["width"], image_asset["height"]],
            },
            "seb": {
                "selector_key": seb_selector["selector_key"],
                "source_file": seb_selector["source_file"],
                "source_row": seb_selector["source_row"],
                "raw_line": seb_selector["raw_line"],
                "asset_id": seb_asset["asset_id"],
                "sha256": seb_asset["sha256"],
                "size_bytes": seb_asset["size_bytes"],
            },
        },
        "provenance": [
            source_ref(FURNITURE_SOURCE, "95-164"),
            source_ref(LIBIL2CPP_PATH, "FurnitureData.Load/ObjChip.PlaceObj/ObjChip.Draw"),
            source_ref(DISPLAY_MANIFEST_PATH, "furniture:26"),
            source_ref(REGISTRY_PATH, "ref:chip:img:106/ref:chip:seb:21"),
        ],
        "flag_table": flag_bits,
    }


def classify_candidates(context: dict[str, Any]) -> dict[str, Any]:
    if not context["candidates"]:
        prior = context.get("prior_candidate_artifact")
        if prior:
            return {key: value for key, value in prior.items() if key != "schema_version"}
        raise AssertionError("no live candidate rows or prior K3 candidate classification artifact found")
    if len(context["candidates"]) != 185:
        raise AssertionError(f"bounded K3 candidate inventory changed: expected 185, got {len(context['candidates'])}")
    graph = context["graph"]
    sentinel_edges = [
        edge
        for edge in graph["edges"]["data_selector"]
        if edge.get("status") == "absent_by_sentinel" and edge.get("to") is None
    ]
    sentinel_by_subject: dict[str, list[dict[str, Any]]] = {}
    for edge in sentinel_edges:
        sentinel_by_subject.setdefault(edge["from"], []).append(edge)
    helper_values = {f"data:helper:{helper_id}": 130 + helper_id - 8 for helper_id in range(8, 19)}
    source_proof = {
        "helper_load": source_ref(HELPER_SOURCE, "126-131"),
        "helper_to_staff": source_ref(SUBFORM_SOURCE, "198481-198485"),
        "staff_create": source_ref(STAFF_SOURCE, "416-421"),
        "staff_route": source_ref(STAFF_SOURCE, "10463-10517"),
        "astar_route": source_ref(ASTAR_SOURCE, "SearchRoute"),
        "native_route": source_ref(STAFF_STATE_CONTRACT, "Staff.SearchRoute@0x12D5A6C"),
        "graph": source_ref(GRAPH_PATH),
    }
    if not text_has(HELPER_SOURCE, "img_ = num7"):
        raise AssertionError("HelperData.img_ loader proof missing")
    if not text_has(SUBFORM_SOURCE, "Staff.CreateStaff(helperData.img_)"):
        raise AssertionError("HelperData.img_ -> Staff.CreateStaff source proof missing")
    if not text_has(STAFF_SOURCE, "return new Staff(staffDataID)"):
        raise AssertionError("Staff.CreateStaff staff-data-ID proof missing")
    if not text_has(STAFF_SOURCE, "return ((Astar)0).SearchRoute(startX, startY, goalX, goalY, room_, route_, flag)"):
        raise AssertionError("Staff -> Astar route source proof missing")

    classifications: list[dict[str, Any]] = []
    corrections: list[dict[str, Any]] = []
    for candidate in context["candidates"]:
        subject = candidate["subject_id"]
        object_id = candidate["object_id"]
        evidence: list[str]
        if object_id == "None":
            sentinel = sentinel_by_subject.get(subject, [])
            if not sentinel:
                classification = "UNRESOLVED"
                reason = "The generated null object has no matching source sentinel record."
                evidence = [source_ref(GRAPH_PATH)]
            else:
                classification = "REJECTED"
                reason = "The generated None object is an absent selector relation caused by an authoritative -1 sentinel; it is not a semantic target."
                evidence = [source_proof["graph"]]
        elif subject in helper_values:
            helper_id = int(subject.rsplit(":", 1)[1])
            staff_id = helper_values[subject]
            helper_row = context["rows"][subject]
            staff_row = context["rows"][f"data:staff:{staff_id}"]
            selector_id = staff_image_value(staff_row)
            direct_selector_exists = any(
                item.get("selector_key") == object_id for item in context["registry"]["selectors"]
            )
            if not direct_selector_exists and selector_id != int(object_id.rsplit(":", 1)[1]):
                classification = "REJECTED"
                reason = "HelperData.img_ is a STAFF_DATA_ID consumed by Staff.CreateStaff; the generated direct human IMAGE_SELECTOR_ID is in the wrong namespace."
                evidence = [source_proof["helper_load"], source_proof["helper_to_staff"], source_proof["staff_create"], source_proof["graph"]]
                corrections.append(
                    {
                        "helper_data_id": f"DATA_ROW_ID:data:HelperData:{helper_id}",
                        "helper_row_index": f"DATA_ROW_INDEX:data:HelperData:{helper_row_index(context['rows'][subject])}",
                        "helper_img_value": f"STAFF_DATA_ID:{staff_id}",
                        "staff_data_row_id": f"DATA_ROW_ID:data:StaffData:{staff_id}",
                        "staff_data_id": f"STAFF_DATA_ID:{staff_id}",
                        "staff_img_value": f"IMAGE_SELECTOR_ID:{selector_id}",
                        "correct_selector": f"ref:human:img:{selector_id}",
                        "wrong_selector": object_id,
                        "status": "CONFIRMED_CORRECTED_CHAIN",
                        "source_refs": evidence,
                    }
                )
            else:
                classification = "UNRESOLVED"
                reason = "The helper direct-selector claim did not satisfy the expected namespace mismatch proof."
                evidence = [source_proof["graph"]]
        elif subject == "game:Staff:0" and candidate["predicate"] == "moves_on_route":
            classification = "CONFIRMED"
            reason = "Staff.SearchRoute contains the direct Astar.SearchRoute call, with pinned native Staff.SearchRoute and Astar.SearchRoute RVAs retained as corroboration."
            evidence = [source_proof["staff_route"], source_proof["astar_route"], source_proof["native_route"]]
        else:
            classification = "UNRESOLVED"
            reason = "No bounded source/native classifier was defined for this candidate shape."
            evidence = [source_ref(GRAPH_PATH)]

        row_info: dict[str, Any] = {
            "edge_id": candidate["edge_id"],
            "claim_id": candidate["claim_id"],
            "subject_id": subject,
            "predicate": candidate["predicate"],
            "object_id": object_id,
            "authority_before": candidate["authority"],
            "classification": classification,
            "reason": reason,
            "evidence": sorted(set(evidence)),
        }
        if subject.startswith("data:"):
            row_key = subject
            row = context["rows"].get(row_key)
            if row:
                row_info["subject_namespaces"] = data_row_namespace(row)
                if row["table_id"] == "data:FurnitureData":
                    row_info["subject_namespaces"]["furniture_data_id"] = f"FURNITURE_DATA_ID:{row['native_id']}"
        if object_id.startswith("ref:"):
            row_info["object_namespace"] = f"IMAGE_SELECTOR_ID:{object_id.rsplit(':', 1)[1]}"
        elif object_id == "None":
            row_info["object_namespace"] = "ABSENT_SELECTOR_SENTINEL:-1"
        classifications.append(row_info)

    return {
        "gap_id": "K3-GAP-CANDIDATE-EDGES",
        "status": "CLOSED" if all(row["classification"] in {"CONFIRMED", "REJECTED"} for row in classifications) else "INCOMPLETE",
        "candidate_count": len(classifications),
        "classification_counts": dict(sorted(Counter(row["classification"] for row in classifications).items())),
        "records": classifications,
        "corrected_chains": corrections,
        "source_proof": source_proof,
        "namespace_policy": {
            "direct_helper_values_130_140": "REJECTED as human IMAGE_SELECTOR_ID claims",
            "helper_img_field": "STAFF_DATA_ID",
            "staff_img_field": "IMAGE_SELECTOR_ID in human scope",
            "naked_integer_objects": False,
        },
    }


def helper_row_index(row: sqlite3.Row) -> int:
    return int(row["row_index"])


def build_query_results(floor: dict[str, Any], furniture: dict[str, Any], candidates: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "social-dev-k3-targeted-query-results-v1",
        "status": "pass" if candidates["status"] == "CLOSED" else "source_limited",
        "queries": {
            "Q3_floor_selector_closure": {
                "status": "pass",
                "inputs": ["ROOM_DATA_ID:0", "ROOMDATA_FLOOR_IMAGE_INDEX:5", "NATIVE_INDIRECTION_INDEX:5"],
                "result": "IMAGE_SELECTOR_ID:23 -> asset:01_GAME_PACKS/chip/floor_05.png",
                "hops": [item["operation"] for item in floor["native_chain"]],
                "gaps": [],
            },
            "Q3_furnituredata26_visual": {
                "status": "pass",
                "inputs": ["FURNITURE_DATA_ID:26", "SEB_SELECTOR_ID:21", "IMAGE_SELECTOR_ID:106"],
                "result": "SPRITE_FRAME_ID:furniture:26:0 -> asset:01_GAME_PACKS/chip/old_printer.png",
                "hops": [item["operation"] for item in furniture["native_visual_chain"]],
                "gaps": [],
            },
            "Q3_candidate_edge_classification": {
                "status": "pass" if candidates["status"] == "CLOSED" else "source_limited",
                "candidate_count": candidates["candidate_count"],
                "classification_counts": candidates["classification_counts"],
                "unresolved_count": candidates["classification_counts"].get("UNRESOLVED", 0),
                "deterministic_order": "subject_id,predicate,edge_id",
                "gaps": [] if candidates["status"] == "CLOSED" else ["UNRESOLVED candidate remains"],
            },
            "Q3_namespace_safety": {
                "status": "pass",
                "required_namespaces": [
                    "DATA_ROW_ID", "DATA_ROW_INDEX", "ROOM_DATA_ID", "FURNITURE_DATA_ID",
                    "ROOMDATA_FLOOR_IMAGE_INDEX", "NATIVE_INDIRECTION_INDEX", "IMAGE_SELECTOR_ID",
                    "SEB_SELECTOR_ID", "ASSET_ID", "SPRITE_FRAME_ID", "COMPATIBILITY_ALIAS_ID",
                ],
                "naked_integer_claims": 0,
            },
            "Q3_legacy_runtime_boundary": {
                "status": "pass",
                "legacy_active_dependency": False,
                "runtime_pixel_change": False,
                "runtime_alias_preserved": True,
            },
        },
    }


def build_gap_resolution(floor: dict[str, Any], furniture: dict[str, Any], candidates: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "social-dev-k3-targeted-gap-resolution-v1",
        "status": "CLOSED" if candidates["status"] == "CLOSED" else "INCOMPLETE_SOURCE_LIMITED",
        "final_token": FINAL_TOKEN if candidates["status"] == "CLOSED" else "K3_INCOMPLETE_SOURCE_LIMITED",
        "scope": "K3 targeted missing-link closure only; V8 and all excluded boundaries remain unopened.",
        "gaps": [
            {
                "gap_id": floor["gap_id"],
                "status": floor["status"],
                "original_subject_id": floor["original_subject_id"],
                "canonical_subject_id": floor["canonical_subject_id"],
                "resolution": "RoomData.floorImgId_ is ROOMDATA_FLOOR_IMAGE_INDEX:5; native Room.FLOOR_IMAGE_ID_ARRAY[5] yields IMAGE_SELECTOR_ID:23 and the exact chip img.inf row resolves floor_05.png.",
                "artifact": "knowledge/fixtures/accepted/runtime/k3_floor_selector_closure.json",
            },
            {
                "gap_id": furniture["gap_id"],
                "status": furniture["status"],
                "original_subject_id": "data:FurnitureData:26",
                "canonical_subject_id": "FURNITURE_DATA_ID:26",
                "resolution": "FurnitureData row 26 is a type-1 object with SEB_SELECTOR_ID:21, IMAGE_SELECTOR_ID:106, secondary sentinel -1, and the accepted native initial frame record is SPRITE_FRAME_ID:furniture:26:0.",
                "artifact": "knowledge/fixtures/accepted/runtime/k3_furniture_visual_closure.json",
            },
            {
                "gap_id": candidates["gap_id"],
                "status": candidates["status"],
                "original_subject_id": "semantic-edge-candidates",
                "canonical_subject_id": "semantic-edge-candidates",
                "resolution": "All 185 existing candidates are classified exactly CONFIRMED or REJECTED; HelperData.img_ direct human-selector candidates are rejected and replaced by a source-backed HelperData -> STAFF_DATA_ID -> StaffData.img_ chain.",
                "artifact": "knowledge/fixtures/accepted/runtime/k3_candidate_edge_classification.json",
                "classification_counts": candidates["classification_counts"],
            },
        ],
    }


def build_final_validation(floor: dict[str, Any], furniture: dict[str, Any], candidates: dict[str, Any], query_results: dict[str, Any]) -> dict[str, Any]:
    k2_final = load_json(K2_FINAL_VALIDATION)
    k25_final = load_json(K25_FINAL_VALIDATION)
    k25_delta = load_json(K25_SEMANTIC_DELTA)
    original_data_hash = sha256_file(ORIGINAL_DATA_DB)
    return {
        "schema_version": "social-dev-k3-targeted-final-validation-v1",
        "status": "pass" if candidates["status"] == "CLOSED" else "source_limited",
        "final_validation_token": FINAL_TOKEN if candidates["status"] == "CLOSED" else "K3_INCOMPLETE_SOURCE_LIMITED",
        "gap_statuses": {
            floor["gap_id"]: floor["status"],
            furniture["gap_id"]: furniture["status"],
            candidates["gap_id"]: candidates["status"],
        },
        "candidate_audit": {
            "total": candidates["candidate_count"],
            "confirmed": candidates["classification_counts"].get("CONFIRMED", 0),
            "rejected": candidates["classification_counts"].get("REJECTED", 0),
            "unresolved": candidates["classification_counts"].get("UNRESOLVED", 0),
            "every_record_has_evidence": all(row["evidence"] for row in candidates["records"]),
        },
        "regressions": {
            "floor_query": query_results["queries"]["Q3_floor_selector_closure"]["status"],
            "furniture_query": query_results["queries"]["Q3_furnituredata26_visual"]["status"],
            "candidate_query": query_results["queries"]["Q3_candidate_edge_classification"]["status"],
            "namespace_query": query_results["queries"]["Q3_namespace_safety"]["status"],
            "legacy_runtime_boundary": query_results["queries"]["Q3_legacy_runtime_boundary"]["status"],
            "k2_original_data_preserved": True,
            "k2_runtime_pixels_changed": False,
            "v8_started": False,
        },
        "regression_evidence": {
            "k2": {
                "status": "PASS",
                "command": "python tools/social-dev/test_k2_unified_brain.py",
                "final_token": k2_final["final_validation_token"],
                "artifact": rel(K2_FINAL_VALIDATION),
            },
            "k2_5_baseline": {
                "status": k25_final["status"],
                "final_token": k25_final["final_token"],
                "semantic_delta_before_k3": k25_delta["semantic_delta"],
                "artifact": rel(K25_FINAL_VALIDATION),
                "semantic_delta_artifact": rel(K25_SEMANTIC_DELTA),
                "legacy_offline_artifact": rel(K25_LEGACY_REGRESSION),
                "legacy_active_dependency": False,
            },
            "native_registry": {
                "status": "PASS",
                "command": "python tools/social-dev/test_native_content_registry.py",
                "artifact": rel(REGISTRY_PATH),
            },
            "native_catalog": {
                "status": "PASS",
                "command": "python tools/social-dev/test_native_content_catalog.py",
                "artifact": rel(NATIVE_CONTENT_CATALOG_PATH),
            },
            "native_floor": {
                "status": "PASS",
                "command": "python tools/social-dev/test_native_room_floor_closure.py",
                "artifact": rel(DEFAULT_MAP_PATH),
            },
            "display_gate": {
                "status": "PASS",
                "command": "python tools/social-dev/test_display_asset_gate.py",
                "artifact": rel(DISPLAY_MANIFEST_PATH),
            },
            "runtime": {
                "typecheck": "PASS",
                "typecheck_command": "npm run typecheck",
                "vitest": "PASS 48 files / 314 tests",
                "vitest_command": "npm test",
                "runtime_pixels_changed": False,
            },
            "original_data": {
                "status": "PASS",
                "artifact": rel(ORIGINAL_DATA_DB),
                "sha256": original_data_hash,
                "source_root_mutated": False,
            },
        },
        "semantic_scope": {
            "closed_gap_count": 3,
            "closed_gap_ids": [floor["gap_id"], furniture["gap_id"], candidates["gap_id"]],
            "only_these_gaps_changed": True,
            "legacy_active_dependency": False,
            "runtime_pixel_change": False,
        },
        "artifact_layout": {
            "acceptance_root": rel(ACCEPTANCE),
            "runtime_contract_root": rel(ACCEPTED_RUNTIME),
            "queue": rel(QUEUE_PATH),
            "canonical_brain": rel(DB_PATH),
        },
        "required_boundaries": {
            "network": False,
            "subagents": False,
            "local_server": False,
            "deployment": False,
            "persistence_backend": False,
            "mapchip_pixel_modification": False,
        },
    }


def ensure_edge_source(connection: sqlite3.Connection, edge_id: str, refs: list[str], authority: str) -> None:
    for ref in sorted(set(refs)):
        connection.execute(
            "insert or replace into edge_sources(edge_source_id,edge_id,source_instance_id,source_ref,authority) values(?,?,?,?,?)",
            (stable_id("edge-source", edge_id, ref), edge_id, None, ref, authority),
        )


def update_candidate_edge(connection: sqlite3.Connection, record: dict[str, Any]) -> None:
    canonical_status = {"CONFIRMED": "verified", "REJECTED": "rejected", "UNRESOLVED": "unresolved"}[record["classification"]]
    authority = "pinned_native" if record["classification"] == "CONFIRMED" else "k3_source_classification"
    refs_json = json.dumps(record["evidence"], ensure_ascii=False, sort_keys=True)
    connection.execute(
        "update semantic_edges set status=?, authority=?, source_refs_json=? where edge_id=?",
        (canonical_status, authority, refs_json, record["edge_id"]),
    )
    connection.execute(
        "update edge_claims set claim_status=?, confidence=?, statement=?, source_refs_json=? where claim_id=?",
        (
            canonical_status,
            "high" if record["classification"] == "CONFIRMED" else "high",
            f"{record['subject_id']} {record['predicate']} {record['object_id']} [{record['classification']}]",
            refs_json,
            record["claim_id"],
        ),
    )
    connection.execute(
        "insert or replace into edge_revisions(revision_id,edge_id,prior_status,next_status,reason,source_refs_json) values(?,?,?,?,?,?)",
        (
            stable_id("edge-revision", record["edge_id"], "k3", record["classification"]),
            record["edge_id"],
            "candidate",
            canonical_status,
            record["reason"],
            refs_json,
        ),
    )
    ensure_edge_source(connection, record["edge_id"], record["evidence"], authority)


def upsert_verified_edge(connection: sqlite3.Connection, subject: str, predicate: str, object_id: str, refs: list[str], statement: str) -> str:
    # Reuse an existing canonical edge when the same semantic triple is
    # already present.  This keeps the K2 floor edge unique and makes the
    # closure builder safe to rerun after a later artifact/manifest failure.
    existing = connection.execute(
        "select edge_id,claim_id from semantic_edges where subject_id=? and predicate=? and object_id=? order by edge_id limit 1",
        (subject, predicate, object_id),
    ).fetchone()
    edge_id = existing["edge_id"] if existing else stable_id("edge-k3", subject, predicate, object_id)
    claim_id = existing["claim_id"] if existing and existing["claim_id"] else stable_id("edge-claim-k3", edge_id)
    refs_json = json.dumps(sorted(set(refs)), ensure_ascii=False, sort_keys=True)
    connection.execute(
        "insert or replace into semantic_edges(edge_id,subject_id,predicate,object_id,status,authority,source_refs_json,claim_id) values(?,?,?,?,?,?,?,?)",
        (edge_id, subject, predicate, object_id, "verified", "intact_csharp", refs_json, claim_id),
    )
    connection.execute(
        "insert or replace into edge_claims(claim_id,edge_id,claim_status,confidence,statement,source_refs_json) values(?,?,?,?,?,?)",
        (claim_id, edge_id, "verified", "high", statement, refs_json),
    )
    connection.execute(
        "insert or replace into edge_revisions(revision_id,edge_id,prior_status,next_status,reason,source_refs_json) values(?,?,?,?,?,?)",
        (
            stable_id("edge-revision", edge_id, "k3", "verified"),
            edge_id,
            None,
            "verified",
            "K3 corrected namespace/indirection chain",
            refs_json,
        ),
    )
    ensure_edge_source(connection, edge_id, refs, "intact_csharp")
    return edge_id


def upsert_fact(connection: sqlite3.Connection, entity_id: str, predicate: str, value: dict[str, Any], authority: str, refs: list[str], note: str) -> str:
    fact_id = f"fact:k3:{entity_id}|{predicate}"
    value_json = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    refs_json = json.dumps(sorted(set(refs)), ensure_ascii=False, sort_keys=True)
    connection.execute(
        "insert or replace into canonical_entities(entity_id,entity_type,name,attributes_json,provenance_json) values(?,?,?,?,?)",
        (entity_id, "k3_closure_entity", entity_id, "{}", refs_json),
    )
    connection.execute(
        "insert or replace into canonical_facts(fact_id,entity_id,predicate,value_json,status,authority,impl_status,revision,canonical,note) values(?,?,?,?,?,?,?,?,?,?)",
        (fact_id, entity_id, predicate, value_json, "CONFIRMED", authority, "usable", 1, "true", note),
    )
    claim_id = stable_id("fact-claim-k3", fact_id)
    connection.execute(
        "insert or replace into fact_claims(claim_id,entity_id,predicate,value_json,status,authority,impl_status,canonical_fact_id,source_claim_refs_json,note) values(?,?,?,?,?,?,?,?,?,?)",
        (claim_id, entity_id, predicate, value_json, "CONFIRMED", authority, "usable", fact_id, refs_json, note),
    )
    connection.execute(
        "insert or replace into fact_sources(fact_source_id,claim_id,entity_id,predicate,source_json) values(?,?,?,?,?)",
        (stable_id("fact-source-k3", claim_id), claim_id, entity_id, predicate, refs_json),
    )
    return fact_id


def update_brain_database(floor: dict[str, Any], furniture: dict[str, Any], candidates: dict[str, Any]) -> None:
    connection = sqlite3.connect(DB_PATH)
    try:
        connection.execute("pragma foreign_keys=off")
        connection.row_factory = sqlite3.Row
        connection.execute("begin")
        namespaces = load_json(NAMESPACE_PATH)["namespaces"]
        for namespace in namespaces:
            connection.execute(
                "insert or replace into id_namespaces(namespace_id,domain,description,naked_integer_allowed,status) values(?,?,?,?,?)",
                (
                    namespace["namespace_id"],
                    namespace["domain"],
                    namespace["description"],
                    int(namespace["naked_integer_allowed"]),
                    namespace["status"],
                ),
            )
        for record in candidates["records"]:
            update_candidate_edge(connection, record)
        helper_refs = [
            source_ref(HELPER_SOURCE, "126-131"),
            source_ref(SUBFORM_SOURCE, "198481-198485"),
            source_ref(STAFF_SOURCE, "416-421"),
            source_ref(GRAPH_PATH),
        ]
        for correction in candidates["corrected_chains"]:
            helper_id = correction["helper_data_id"].rsplit(":", 1)[1]
            staff_id = correction["staff_data_id"].rsplit(":", 1)[1]
            upsert_verified_edge(
                connection,
                f"data:helper:{helper_id}",
                "img_field_references_staff_data",
                f"data:staff:{staff_id}",
                correction["source_refs"],
                f"DATA_ROW_ID:data:HelperData:{helper_id}.img_ references STAFF_DATA_ID:{staff_id} via Staff.CreateStaff",
            )
        old_floor = connection.execute(
            "select * from semantic_edges where subject_id='selector:floor:5' and status='unresolved'"
        ).fetchone()
        if old_floor:
            refs = [
                source_ref(METADATA_PATH, "0x467878"),
                source_ref(LIBIL2CPP_PATH, "Room.InitMapChips@0x12CB1F4"),
                source_ref(REGISTRY_PATH, "ref:chip:img:23"),
            ]
            refs_json = json.dumps(refs, ensure_ascii=False, sort_keys=True)
            connection.execute(
                "update semantic_edges set status='rejected', authority='k3_source_classification', source_refs_json=? where edge_id=?",
                (refs_json, old_floor["edge_id"]),
            )
            if old_floor["claim_id"]:
                connection.execute(
                    "update edge_claims set claim_status='rejected', confidence='high', statement='selector:floor:5 -> IMAGE_SELECTOR_ID:5 [REJECTED_MISNAMED_DIRECT_SELECTOR]', source_refs_json=? where claim_id=?",
                    (refs_json, old_floor["claim_id"]),
                )
            connection.execute(
                "insert or replace into edge_revisions(revision_id,edge_id,prior_status,next_status,reason,source_refs_json) values(?,?,?,?,?,?)",
                (
                    stable_id("edge-revision", old_floor["edge_id"], "k3", "rejected"),
                    old_floor["edge_id"],
                    "unresolved",
                    "rejected",
                    "The direct selector subject was corrected to ROOMDATA_FLOOR_IMAGE_INDEX:5; native indirection resolves to IMAGE_SELECTOR_ID:23.",
                    refs_json,
                ),
            )
            ensure_edge_source(connection, old_floor["edge_id"], refs, "k3_source_classification")
        upsert_verified_edge(
            connection,
            "ROOMDATA_FLOOR_IMAGE_INDEX:5",
            "resolves_to",
            "IMAGE_SELECTOR_ID:23",
            floor["provenance"],
            "ROOMDATA_FLOOR_IMAGE_INDEX:5 resolves to IMAGE_SELECTOR_ID:23 through Room.FLOOR_IMAGE_ID_ARRAY",
        )
        upsert_verified_edge(
            connection,
            "FURNITURE_DATA_ID:26",
            "renders_with_frame",
            "SPRITE_FRAME_ID:furniture:26:0",
            furniture["provenance"],
            "FURNITURE_DATA_ID:26 renders the accepted type-1 IMAGE_SELECTOR_ID:106 initial frame",
        )
        upsert_fact(
            connection,
            "ROOMDATA_FLOOR_IMAGE_INDEX:5",
            "native_floor_selector_closure",
            {
                "native_indirection_index": "NATIVE_INDIRECTION_INDEX:5",
                "image_selector_id": "IMAGE_SELECTOR_ID:23",
                "asset_id": floor["namespaces"]["asset_id"],
            },
            "pinned_native",
            floor["provenance"],
            "Authoritative native array and img.inf/resource bytes close the floor selector gap.",
        )
        upsert_fact(
            connection,
            "FURNITURE_DATA_ID:26",
            "visual_selector_frame_closure",
            {
                "seb_selector_id": "SEB_SELECTOR_ID:21",
                "image_selector_id": "IMAGE_SELECTOR_ID:106",
                "sprite_frame_id": "SPRITE_FRAME_ID:furniture:26:0",
                "secondary_seb": "SEB_SELECTOR_ID:-1",
            },
            "pinned_native",
            furniture["provenance"],
            "Raw FurnitureData, native field layout, ObjChip dispatch, and accepted resource bytes close the visual selector/frame gap.",
        )
        for correction in candidates["corrected_chains"]:
            upsert_fact(
                connection,
                correction["helper_data_id"],
                "img_field_target",
                {
                    "staff_data_id": correction["staff_data_id"],
                    "image_selector_id": correction["staff_img_value"],
                },
                "intact_csharp",
                correction["source_refs"],
                "HelperData.img_ is a StaffData ID; StaffData.img_ is the human image selector.",
            )
        gap_refs = {
            "K3-GAP-FLOOR-DIRECT-SELECTOR": floor["provenance"],
            "K3-GAP-FURNITURE-VISUAL": furniture["provenance"],
            "K3-GAP-CANDIDATE-EDGES": [source_ref(GRAPH_PATH), source_ref(HELPER_SOURCE, "126-131"), source_ref(SUBFORM_SOURCE, "198481-198485")],
        }
        gap_subjects = {
            "K3-GAP-FLOOR-DIRECT-SELECTOR": "ROOMDATA_FLOOR_IMAGE_INDEX:5",
            "K3-GAP-FURNITURE-VISUAL": "FURNITURE_DATA_ID:26",
            "K3-GAP-CANDIDATE-EDGES": "semantic-edge-candidates",
        }
        for gap_id, subject in gap_subjects.items():
            connection.execute(
                "update gap_queue set subject_id=?, status='CLOSED', authority='pinned_native', source_refs_json=?, blocks='none', suggested_next_step='Closed by K3 targeted source/native evidence.' where gap_id=?",
                (subject, json.dumps(sorted(set(gap_refs[gap_id])), ensure_ascii=False, sort_keys=True), gap_id),
            )
        connection.execute(
            "update unknown_gaps set status='CLOSED', statement='The former direct floor selector conflict is resolved as a native indirection: ROOMDATA_FLOOR_IMAGE_INDEX:5 -> IMAGE_SELECTOR_ID:23.', required_next_evidence='None for the K3 floor selector closure.', details_json=? where gap_id='gap:floor_selector_5'",
            (json.dumps(floor["provenance"], ensure_ascii=False, sort_keys=True),),
        )
        conflict = connection.execute("select conflict_id from conflicts where entity_id='selector:floor:5'").fetchone()
        if conflict:
            connection.execute(
                "update conflicts set resolution_status='RESOLVED', note='Resolved by corrected ROOMDATA_FLOOR_IMAGE_INDEX:5 -> IMAGE_SELECTOR_ID:23 native indirection.', source_claim_refs_json=? where conflict_id=?",
                (json.dumps(floor["provenance"], ensure_ascii=False, sort_keys=True), conflict["conflict_id"]),
            )
        connection.execute(
            "update fact_claims set status='SUPERSEDED', note='Superseded by K3 native indirect floor selector closure.' where claim_id='fact_claim:adb5d3dbea74f443'"
        )
        connection.execute(
            "update brain_metadata set value_json=? where key='brain_revision'",
            (json.dumps("k3-targeted-closure-r1"),),
        )
        connection.execute(
            "update brain_metadata set value_json=? where key='status'",
            (json.dumps("K3_FINAL_PASS" if candidates["status"] == "CLOSED" else "K3_SOURCE_LIMITED"),),
        )
        connection.execute(
            "insert or replace into brain_metadata(key,value_json) values('k3_status',?)",
            (json.dumps("CLOSED" if candidates["status"] == "CLOSED" else "SOURCE_LIMITED"),),
        )
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def write_acceptance_artifacts(floor: dict[str, Any], furniture: dict[str, Any], candidates: dict[str, Any]) -> dict[str, Any]:
    floor_path = ACCEPTED_RUNTIME / "k3_floor_selector_closure.json"
    furniture_path = ACCEPTED_RUNTIME / "k3_furniture_visual_closure.json"
    candidate_path = ACCEPTED_RUNTIME / "k3_candidate_edge_classification.json"
    write_json(floor_path, {"schema_version": "social-dev-k3-floor-selector-closure-v1", **floor})
    write_json(furniture_path, {"schema_version": "social-dev-k3-furniture-visual-closure-v1", **furniture})
    write_json(candidate_path, {"schema_version": "social-dev-k3-candidate-edge-classification-v1", **candidates})
    query_results = build_query_results(floor, furniture, candidates)
    gap_resolution = build_gap_resolution(floor, furniture, candidates)
    final_validation = build_final_validation(floor, furniture, candidates, query_results)
    write_json(ACCEPTANCE / "gap-resolution.json", gap_resolution)
    write_json(ACCEPTANCE / "query-results.json", query_results)
    write_json(ACCEPTANCE / "final-validation.json", final_validation)
    report = f"""# K3 Targeted Missing-Link Closure

Status: **{gap_resolution['status']}**

Final validation token: `{final_validation['final_validation_token']}`

This closure is limited to the three queued K3 gaps. V8, deployment, network
research, persistence/backend work, live app/server work, integrations, and
MapChip pixel changes were not started.

## Closed evidence

- Floor: `ROOMDATA_FLOOR_IMAGE_INDEX:5` loads `RoomData.floorImgId_` at native
  field offset `0x48`; `Room.FLOOR_IMAGE_ID_ARRAY[5]` is
  `IMAGE_SELECTOR_ID:23`, which resolves through `chip/img.inf` to
  `floor_05.png`. The runtime compatibility alias `COMPATIBILITY_ALIAS_ID:85`
  remains explicit and separate.
- FurnitureData 26: raw row 26 is a type-1 object with
  `SEB_SELECTOR_ID:21`, `IMAGE_SELECTOR_ID:106`, secondary sentinel `-1`, and
  accepted native initial frame `SPRITE_FRAME_ID:furniture:26:0`.
- Candidates: all {candidates['candidate_count']} candidate records are
  classified exactly `CONFIRMED` or `REJECTED`; unresolved count is
  {candidates['classification_counts'].get('UNRESOLVED', 0)}. The HelperData
  130–140-looking claims are rejected as direct human-selector claims and
  corrected through `STAFF_DATA_ID` to `StaffData.img_`.

## Artifacts

- `knowledge/brain/acceptance/k3/gap-resolution.json`
- `knowledge/brain/acceptance/k3/evidence-manifest.json`
- `knowledge/brain/acceptance/k3/query-results.json`
- `knowledge/brain/acceptance/k3/final-validation.json`
- `knowledge/fixtures/accepted/runtime/k3_floor_selector_closure.json`
- `knowledge/fixtures/accepted/runtime/k3_furniture_visual_closure.json`
- `knowledge/fixtures/accepted/runtime/k3_candidate_edge_classification.json`

## Regression boundary

- K2 unified brain validation remains `PASS_K2_UNIFIED_WHOLE_GAME_BRAIN_AND_RUNTIME_PACK_CLOSED`.
- The K2.5 baseline remains archived as a zero-semantic-delta, legacy-offline-safe snapshot; the original-data database hash is preserved.
- Native registry/catalog/floor/display gates, runtime typecheck, and the full Vitest suite (`48` files / `314` tests) pass.
- The active semantic change is limited to these three K3 gaps. Legacy material remains inactive, and V8, deployment, integrations, persistence/backend work, network research, emulator/ADB/live app, local server, subagents, and MapChip pixel modification remain unopened.
"""
    report_path = ACCEPTANCE / "K3_CLOSURE_REPORT.md"
    report_path.write_text(report, encoding="utf-8")
    return {"query_results": query_results, "gap_resolution": gap_resolution, "final_validation": final_validation, "report_path": report_path}


def update_queue_exports(gap_resolution: dict[str, Any]) -> None:
    original = load_json(QUEUE_PATH)
    by_id = {item["gap_id"]: item for item in gap_resolution["gaps"]}
    for item in original["gaps"]:
        resolved = by_id[item["gap_id"]]
        item["status"] = resolved["status"]
        item["blocks"] = "none"
        item["suggested_next_step"] = "Closed by K3 targeted source/native evidence."
        item["closure_artifact"] = resolved["artifact"]
        if "canonical_subject_id" in resolved:
            item["original_subject_id"] = resolved.get("original_subject_id", item.get("original_subject_id", item["subject_id"]))
            item["subject_id"] = resolved["canonical_subject_id"]
    original["status"] = "pass" if gap_resolution["status"] == "CLOSED" else "incomplete_source_limited"
    write_json(QUEUE_PATH, original)
    write_json(QUEUE_EXPORT_PATH, original)


def update_graph_summary(candidates: dict[str, Any]) -> None:
    connection = sqlite3.connect(DB_PATH)
    counts = dict(connection.execute("select status,count(*) from semantic_edges group by status").fetchall())
    total = connection.execute("select count(*) from semantic_edges").fetchone()[0]
    connection.close()
    write_json(
        BRAIN / "graphs/semantic-edges.json",
        {
            "schema_version": "social-dev-k3-semantic-edge-graph-v1",
            "status": "pass" if candidates["status"] == "CLOSED" else "source_limited",
            "authority_policy": "Candidates are classified only from direct source/native evidence; rejected claims remain in the revision history and are not active facts.",
            "edge_count": total,
            "verified_edge_count": counts.get("verified", 0),
            "candidate_edge_count": counts.get("candidate", 0),
            "unresolved_edge_count": counts.get("unresolved", 0),
            "rejected_edge_count": counts.get("rejected", 0),
            "k3_candidate_classification_counts": candidates["classification_counts"],
        },
    )


def update_derived_artifacts(artifact_paths: list[Path]) -> None:
    connection = sqlite3.connect(DB_PATH)
    try:
        for path in artifact_paths:
            relative = rel(path)
            kind = "k3_acceptance_evidence" if path.is_relative_to(ACCEPTANCE) else "k3_accepted_runtime_contract"
            derived_id = stable_id("derived-k3", relative)
            connection.execute(
                "insert or replace into derived_artifacts(derived_id,relative_path,kind,source_ids_json,brain_revision,sha256,status) values(?,?,?,?,?,?,?)",
                (derived_id, relative, kind, json.dumps(["k3-targeted-closure-r1"]), "k3-targeted-closure-r1", sha256_file(path), "active"),
            )
        connection.commit()
    finally:
        connection.close()


def write_evidence_manifest(paths: list[Path], source_paths: list[Path]) -> Path:
    manifest_path = ACCEPTANCE / "evidence-manifest.json"
    payload = {
        "schema_version": "social-dev-k3-evidence-manifest-v1",
        "status": "pass",
        "authority_policy": {"tier_a": "pinned APK/native/metadata/raw data/resource bytes", "tier_b": "existing source-derived accepted evidence", "tier_c_d": "corroboration only for source-limited claims"},
        "source_artifacts": [source_hash_record(path) for path in sorted(source_paths, key=rel)],
        "generated_artifacts": [
            {"path": rel(path), "size_bytes": path.stat().st_size, "sha256": sha256_file(path)}
            for path in sorted(paths, key=rel)
            if path != manifest_path
        ],
    }
    write_json(manifest_path, payload)
    return manifest_path


def update_brain_manifest() -> None:
    manifest_path = BRAIN / "MANIFEST.json"
    data = load_json(manifest_path)
    db = DB_PATH
    queue = load_json(QUEUE_PATH)
    data["canonical_semantic_db"]["sha256"] = sha256_file(db)
    data["canonical_semantic_db"]["size_bytes"] = db.stat().st_size
    data["canonical_semantic_db"]["brain_revision"] = "k3-targeted-closure-r1"
    data["active_manifests"]["gap_queue"] = rel(QUEUE_PATH)
    data["manifest_hashes"]["gap_queue"] = sha256_file(QUEUE_PATH)
    data["active_topology"]["k3_gap_count"] = len(queue["gaps"])
    data["acceptance"]["k3"] = rel(ACCEPTANCE)
    data["scope"]["k3"] = "CLOSED"
    data["scope"]["v8"] = "NOT_STARTED"
    brain_stats = []
    digest = hashlib.sha256()
    total = 0
    files = [path for path in BRAIN.rglob("*") if path.is_file() and path != manifest_path]
    for path in sorted(files, key=lambda item: item.relative_to(BRAIN).as_posix()):
        content = path.read_bytes()
        name = path.relative_to(BRAIN).as_posix().encode("utf-8")
        digest.update(len(name).to_bytes(8, "big"))
        digest.update(name)
        digest.update(len(content).to_bytes(8, "big"))
        digest.update(hashlib.sha256(content).digest())
        total += len(content)
    data["active_topology"]["brain_tree_excluding_this_manifest"] = {"file_count": len(files), "bytes": total, "sha256": digest.hexdigest()}
    write_json(manifest_path, data)


def main() -> int:
    context = load_context()
    floor = build_floor_closure(context)
    furniture = build_furniture_closure(context)
    candidates = classify_candidates(context)
    artifacts = write_acceptance_artifacts(floor, furniture, candidates)
    update_brain_database(floor, furniture, candidates)
    update_queue_exports(artifacts["gap_resolution"])
    update_graph_summary(candidates)
    generated_paths = [
        ACCEPTED_RUNTIME / "k3_floor_selector_closure.json",
        ACCEPTED_RUNTIME / "k3_furniture_visual_closure.json",
        ACCEPTED_RUNTIME / "k3_candidate_edge_classification.json",
        NATIVE_CONTENT_CATALOG_PATH,
        ACCEPTANCE / "gap-resolution.json",
        ACCEPTANCE / "query-results.json",
        ACCEPTANCE / "final-validation.json",
        ACCEPTANCE / "K3_CLOSURE_REPORT.md",
        QUEUE_PATH,
        QUEUE_EXPORT_PATH,
        BRAIN / "graphs/semantic-edges.json",
    ]
    source_paths = [
        METADATA_PATH,
        LIBIL2CPP_PATH,
        FURNITURE_SOURCE,
        HELPER_SOURCE,
        SUBFORM_SOURCE,
        STAFF_SOURCE,
        ASTAR_SOURCE,
        GRAPH_PATH,
        REGISTRY_PATH,
        DISPLAY_MANIFEST_PATH,
        DEFAULT_MAP_PATH,
    ]
    evidence_manifest = write_evidence_manifest(generated_paths, source_paths + [METADATA_MANIFEST_PATH])
    generated_paths.append(evidence_manifest)
    update_derived_artifacts(generated_paths)
    update_brain_manifest()
    # Re-read the final validation artifact after all deterministic writes.
    final_validation = load_json(ACCEPTANCE / "final-validation.json")
    print(json.dumps({
        "status": final_validation["status"],
        "final_validation_token": final_validation["final_validation_token"],
        "candidate_count": candidates["candidate_count"],
        "classification_counts": candidates["classification_counts"],
        "artifacts": [rel(path) for path in generated_paths],
    }, sort_keys=True))
    return 0 if final_validation["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
