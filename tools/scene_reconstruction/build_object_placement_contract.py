"""Build the Task 5 object-placement contract.

The contract keeps three different things separate:

- verified source asset identity;
- producer-to-consumer lineage that can be traced with explicit coordinate fields;
- the current adapter page's fixture coordinates, which are diagnostic only and
  must not be promoted to original room placement.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]

SOURCE_INVENTORY = ROOT / "knowledge/world-assets/evidence/scene_reconstruction/source_inventory.json"
RESOURCE_CONTRACT = ROOT / "knowledge/world-assets/evidence/scene_reconstruction/resource_contract.json"
SEB_SEMANTICS_CONTRACT = ROOT / "knowledge/world-assets/evidence/scene_reconstruction/seb_semantics_contract.json"
WAVE2_PLACEMENT_FIXTURE = ROOT / "knowledge/reverse-engineering/evidence/wave2_placement_fixture.json"
WAVE2_FURNITURE_CONTRACT = ROOT / "knowledge/reverse-engineering/evidence/wave2_furniture_contract.json"
WAVE5_1_FURNITURE_MANIFEST = ROOT / "runtime/office/evidence/wave5_1_furniture_manifest.json"
WAVE5_2_FURNITURE_DRAW_FIXTURE = ROOT / "runtime/office/evidence/wave5_2_furniture_draw_fixture.json"
WAVE5_8_ROOM_CALLER_CONTRACT = ROOT / "runtime/office/evidence/wave5_8_room_caller_contract.json"
WAVE5_9_OBJECT_PRODUCER_CONTRACT = ROOT / "runtime/office/evidence/wave5_9_object_producer_contract.json"
ROOM_MANIFEST = ROOT / "runtime/office/app/data/room_manifest.json"
OUTPUT = ROOT / "knowledge/world-assets/evidence/scene_reconstruction/object_placement_contract.json"

GAMEFORM_CS = ROOT / "knowledge/csharp/primary/form/GameForm.cs"
FORM_C = ROOT / "game-dev-story-mod_Dumped/Categorized_Code/Global/form.c"


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def _line_number(path: Path, needle: str) -> int:
    text = path.read_text(encoding="utf-8", errors="replace")
    position = text.find(needle)
    if position < 0:
        raise ValueError(f"needle not found in {path}: {needle}")
    return text.count("\n", 0, position) + 1


def _source_ref(path: Path, needle: str, *, function: str | None = None, status: str = "verified") -> dict[str, Any]:
    ref: dict[str, Any] = {
        "file": _relative(path),
        "line": _line_number(path, needle),
        "needle": needle,
        "source_hash": _sha256(path),
        "status": status,
    }
    if function:
        ref["function"] = function
    return ref


def _json_ref(path: Path, json_pointer: str, *, status: str = "verified", note: str | None = None) -> dict[str, Any]:
    ref: dict[str, Any] = {
        "file": _relative(path),
        "json_pointer": json_pointer,
        "source_hash": _sha256(path),
        "status": status,
    }
    if note:
        ref["note"] = note
    return ref


@dataclass(frozen=True)
class PlacementClassification:
    asset_ref: str
    source_kind: str
    status: str
    authority: str
    x: int | None = None
    y: int | None = None
    coordinate_field: str | None = None
    notes: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ObjectPlacementContract:
    schema_version: str
    phase: str
    wave: str
    status: str
    authority: str
    source_roots_read_only: bool
    legacy_equivalence: bool
    explanation: str
    absence_scope: str
    adapter_page: dict[str, Any]
    floor0_snapshot: dict[str, Any]
    records: tuple[dict[str, Any], ...] = field(default_factory=tuple)
    candidate_records: tuple[dict[str, Any], ...] = field(default_factory=tuple)
    summary: dict[str, Any] = field(default_factory=dict)
    evidence: tuple[dict[str, Any], ...] = field(default_factory=tuple)
    source_files: dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "phase": self.phase,
            "wave": self.wave,
            "status": self.status,
            "authority": self.authority,
            "source_roots_read_only": self.source_roots_read_only,
            "legacy_equivalence": self.legacy_equivalence,
            "explanation": self.explanation,
            "absence_scope": self.absence_scope,
            "adapter_page": self.adapter_page,
            "floor0_snapshot": self.floor0_snapshot,
            "records": list(self.records),
            "candidate_records": list(self.candidate_records),
            "summary": self.summary,
            "evidence": list(self.evidence),
            "source_files": self.source_files,
        }


def classify_placement(
    *,
    asset_ref: str,
    x: int | None = None,
    y: int | None = None,
    source_kind: str,
    coordinate_field: str | None = None,
) -> PlacementClassification:
    if source_kind == "producer_to_consumer_lineage" and coordinate_field:
        return PlacementClassification(
            asset_ref=asset_ref,
            source_kind=source_kind,
            status="verified",
            authority="producer_lineage",
            x=x,
            y=y,
            coordinate_field=coordinate_field,
            notes=("explicit_coordinate_field_present",),
        )

    if source_kind == "producer_to_consumer_lineage":
        return PlacementClassification(
            asset_ref=asset_ref,
            source_kind=source_kind,
            status="candidate",
            authority="producer_lineage",
            x=x,
            y=y,
            coordinate_field=coordinate_field,
            notes=("producer_lineage_without_explicit_coordinate_field",),
        )

    if source_kind == "runtime_adapter_fixture":
        return PlacementClassification(
            asset_ref=asset_ref,
            source_kind=source_kind,
            status="unknown",
            authority="diagnostic_only",
            x=x,
            y=y,
            coordinate_field=coordinate_field,
            notes=("adapter_fixture_coordinates_are_diagnostic_only",),
        )

    return PlacementClassification(
        asset_ref=asset_ref,
        source_kind=source_kind,
        status="unknown",
        authority="diagnostic_only",
        x=x,
        y=y,
        coordinate_field=coordinate_field,
        notes=("insufficient_evidence_for_original_room_placement",),
    )


def _asset_index(source_inventory: dict[str, Any]) -> dict[str, dict[str, Any]]:
    files = source_inventory.get("files", {})
    if isinstance(files, dict):
        return {entry["path"]: entry for entry in files.values() if isinstance(entry, dict) and "path" in entry}
    return {entry["path"]: entry for entry in files if isinstance(entry, dict) and "path" in entry}


def _find_room_item(room_manifest: dict[str, Any], object_id: str) -> dict[str, Any]:
    for record in room_manifest.get("objects", []):
        if record.get("id") == object_id:
            return record
    raise KeyError(f"room manifest object not found: {object_id}")


def _find_manifest_record(manifest: dict[str, Any], object_id: str) -> dict[str, Any]:
    for record in manifest.get("records", []):
        if record.get("id") == object_id:
            return record
    raise KeyError(f"furniture manifest record not found: {object_id}")


def _base_record(
    *,
    manifest_record: dict[str, Any],
    room_record: dict[str, Any],
    room_manifest: dict[str, Any],
    source_inventory_index: dict[str, dict[str, Any]],
    source_file: Path,
) -> dict[str, Any]:
    asset_path = manifest_record["source_path"]
    inventory_entry = source_inventory_index.get(asset_path, {})
    asset_identity = {
        "status": "verified",
        "asset_id": manifest_record["source_family"],
        "source_family": manifest_record["source_family"],
        "source_path": asset_path,
        "dimensions": manifest_record["dimensions"],
        "inventory_entry": {
            "size": inventory_entry.get("size"),
            "sha256": inventory_entry.get("sha256"),
            "source_path": inventory_entry.get("path"),
            "status": "verified" if inventory_entry else "unknown",
        },
        "evidence": [
            _source_ref(
                SOURCE_INVENTORY,
                f'"{asset_path}": {{',
                status="verified",
            ),
            _json_ref(
                WAVE5_1_FURNITURE_MANIFEST,
                f"/records/{manifest_record.get('id')}",
                status="verified",
                note="current page adapter fixture asset identity",
            ),
        ],
    }

    seb_crop = {
        "status": "verified",
        "local_crop_fields": ["ObjecCX", "ObjecCY", "ObjecWX", "ObjecWY"],
        "evidence": [
            _json_ref(
                WAVE5_2_FURNITURE_DRAW_FIXTURE,
                "/objects",
                status="verified",
                note="bounded furniture draw fixture keeps crop fields separate from placement",
            ),
            _json_ref(
                WAVE5_8_ROOM_CALLER_CONTRACT,
                "/room_draw_path/direct_img_floor_parts_branch",
                status="verified",
                note="DrawObj direct floor-parts branch keeps crop semantics separate from placement",
            ),
        ],
    }

    fixture_probe = {
        "status": "verified",
        "source_kind": "runtime_adapter_fixture",
        "screen_coordinate": [room_record["x"], room_record["y"]],
        "sort_depth": room_record["sort_key"],
        "coordinate_space": room_manifest.get("coordinate_profile", {}).get("space", "adapter_canvas_pixels"),
        "evidence": [
            _json_ref(
                ROOM_MANIFEST,
                f"/objects/{room_record.get('id')}",
                status="verified",
                note="adapter fixture coordinate probe only",
            )
        ],
    }

    screen_coordinate = classify_placement(
        asset_ref=manifest_record["source_family"],
        x=room_record["x"],
        y=room_record["y"],
        source_kind="runtime_adapter_fixture",
    ).to_dict()

    return {
        "id": manifest_record["id"],
        "type": manifest_record["type"],
        "asset_identity": asset_identity,
        "seb_crop": seb_crop,
        "fixture_probe": fixture_probe,
        "screen_coordinate": screen_coordinate,
        "room_base_destination": {
            "status": "unknown",
            "authority": "diagnostic_only",
            "value": None,
            "evidence": [
                _json_ref(
                    WAVE5_9_OBJECT_PRODUCER_CONTRACT,
                    "/room_placement",
                    status="unknown",
                    note="room/base destination not recovered from producer lineage",
                )
            ],
        },
        "world_coordinate": {
            "status": "unknown",
            "authority": "diagnostic_only",
            "value": None,
            "evidence": [
                _json_ref(
                    WAVE5_9_OBJECT_PRODUCER_CONTRACT,
                    "/camera_transform_boundary",
                    status="unknown",
                    note="world transform remains open; adapter page coordinates are not a world map",
                )
            ],
        },
        "sort_depth": {
            "status": "unknown",
            "authority": "diagnostic_only",
            "value": room_record["sort_key"],
            "evidence": [
                _json_ref(
                    ROOM_MANIFEST,
                    f"/objects/{room_record.get('id')}/sort_key",
                    status="verified",
                    note="sort key present on adapter page only",
                )
            ],
        },
        "floor_snapshot_presence": {
            "status": "unknown",
            "authority": "diagnostic_only",
            "scope": "no_persisted_or_generated_floor0_room_state_record",
            "evidence": [
                _json_ref(
                    WAVE5_1_FURNITURE_MANIFEST,
                    "/records",
                    status="verified",
                    note="three fixture records exist, but they are adapter fixtures, not a floor snapshot",
                ),
                _json_ref(
                    WAVE5_2_FURNITURE_DRAW_FIXTURE,
                    "/scope",
                    status="verified",
                    note="explicit adapter fixture, not recovered room placement",
                ),
            ],
        },
        "placement": classify_placement(
            asset_ref=manifest_record["source_family"],
            x=room_record["x"],
            y=room_record["y"],
            source_kind="runtime_adapter_fixture",
        ).to_dict(),
        "source_record_status": manifest_record.get("placement_status", "unknown"),
        "source_file": _relative(source_file),
    }


def _lineage_record(
    *,
    record_id: str,
    object_id: str,
    status: str,
    authority: str,
    source_kind: str,
    coordinate_field: str | None,
    x: int | None,
    y: int | None,
    evidence: list[dict[str, Any]],
    note: str,
) -> dict[str, Any]:
    return {
        "id": record_id,
        "object_id": object_id,
        "status": status,
        "authority": authority,
        "source_kind": source_kind,
        "coordinate_field": coordinate_field,
        "coordinates": {"x": x, "y": y},
        "evidence": evidence,
        "note": note,
    }


def build_object_placement_contract() -> ObjectPlacementContract:
    source_inventory = _load_json(SOURCE_INVENTORY)
    resource_contract = _load_json(RESOURCE_CONTRACT)
    seb_semantics_contract = _load_json(SEB_SEMANTICS_CONTRACT)
    wave2_placement = _load_json(WAVE2_PLACEMENT_FIXTURE)
    wave2_furniture = _load_json(WAVE2_FURNITURE_CONTRACT)
    wave5_1_manifest = _load_json(WAVE5_1_FURNITURE_MANIFEST)
    wave5_2_fixture = _load_json(WAVE5_2_FURNITURE_DRAW_FIXTURE)
    wave5_8 = _load_json(WAVE5_8_ROOM_CALLER_CONTRACT)
    wave5_9 = _load_json(WAVE5_9_OBJECT_PRODUCER_CONTRACT)
    room_manifest = _load_json(ROOM_MANIFEST)

    source_inventory_index = _asset_index(source_inventory)
    room_records = {record["id"]: record for record in room_manifest.get("objects", [])}
    manifest_records = {record["id"]: record for record in wave5_1_manifest.get("records", [])}

    records = tuple(
        _base_record(
            manifest_record=manifest_records[object_id],
            room_record=room_records[object_id],
            room_manifest=room_manifest,
            source_inventory_index=source_inventory_index,
            source_file=WAVE5_1_FURNITURE_MANIFEST,
        )
        for object_id in ("reception.fixture.0", "desk.fixture.0", "chair.fixture.0")
    )

    candidate_records = (
        _lineage_record(
            record_id="callhikkosi_param2_0_first_desk_object",
            object_id="desk.fixture.0",
            status="candidate",
            authority="producer_lineage",
            source_kind="bounded_fixture_trace",
            coordinate_field="AddObjec(TX/TY)",
            x=46,
            y=61,
            evidence=[
                _json_ref(
                    WAVE2_PLACEMENT_FIXTURE,
                    "/placement_trace",
                    status="verified",
                    note="bounded legacy call trace without full room placement semantics",
                ),
                _source_ref(
                    FORM_C,
                    "0x2e,0x3d,100,0,0x21,0x2e,0x20);",
                    function="form_GameForm__CallHikkosi",
                ),
            ],
            note="bounded desk placement trace preserves lineage but not original floor state",
        ),
        _lineage_record(
            record_id="callhikkosi_explicit_coordinate_lineage",
            object_id="desk.fixture.0",
            status="verified",
            authority="producer_lineage",
            source_kind="producer_to_consumer_lineage",
            coordinate_field="TX/TY",
            x=82,
            y=36,
            evidence=[
                _source_ref(
                    GAMEFORM_CS,
                    "int num7 = gameForm2.AddObjec(tSyurui, 82, 36, 96, 46, 30, 48, 39);",
                    function="CallHikkosi",
                ),
                _source_ref(
                    FORM_C,
                    "0x2e,0x3d,100,0,0x21,0x2e,0x20);",
                    function="form_GameForm__CallHikkosi",
                ),
            ],
            note="explicit coordinate field in producer-to-consumer lineage is verified, but still not a room snapshot",
        ),
        _lineage_record(
            record_id="callchairchange_bounded_update_trace",
            object_id="chair.fixture.0",
            status="candidate",
            authority="producer_lineage",
            source_kind="producer_update_trace",
            coordinate_field="ObjecX/ObjecY",
            x=340,
            y=354,
            evidence=[
                _json_ref(
                    WAVE2_FURNITURE_CONTRACT,
                    "/relation_traces/2",
                    status="verified",
                    note="chair change relation trace keeps seat/furniture relation separate from placement",
                ),
                _json_ref(
                    WAVE5_9_OBJECT_PRODUCER_CONTRACT,
                    "/producer_inventory/call_graph/CallHikkosi/internal_producer_calls/8",
                    status="verified",
                    note="CallChairChange is reached from CallHikkosi but does not prove original placement",
                ),
                _source_ref(
                    GAMEFORM_CS,
                    "public void CallChairChange(int TOffice, int TChair)",
                    function="CallChairChange",
                ),
            ],
            note="chair update trace is preserved as a candidate lineage record",
        ),
        _lineage_record(
            record_id="reception_dispatch_probe",
            object_id="reception.fixture.0",
            status="candidate",
            authority="producer_lineage",
            source_kind="consumer_dispatch_probe",
            coordinate_field="DrawReception local crop",
            x=236,
            y=286,
            evidence=[
                _source_ref(
                    GAMEFORM_CS,
                    "private void DrawReception(Graphics g, int x, int y, int ux, int uy, int uw, int uh)",
                    function="DrawReception",
                ),
                _json_ref(
                    WAVE5_8_ROOM_CALLER_CONTRACT,
                    "/room_draw_path/reception_helper",
                    status="verified",
                    note="DrawReception helper proves the consumer boundary but not the room snapshot",
                ),
            ],
            note="reception dispatch is a consumer probe only; it does not establish original room placement",
        ),
    )

    adapter_page = {
        "status": "verified",
        "source": _relative(ROOM_MANIFEST),
        "object_count": len(room_manifest.get("objects", [])),
        "placement_semantics": room_manifest.get("seb", {}).get("placement_semantics"),
        "object_ids": [record["id"] for record in room_manifest.get("objects", [])],
        "evidence": [
            _json_ref(
                ROOM_MANIFEST,
                "/objects",
                status="verified",
                note="current page manifest exposes exactly three fixture objects",
            )
        ],
    }

    floor0_snapshot = {
        "status": "unknown",
        "authority": "diagnostic_only",
        "scope": "no_persisted_or_generated_floor0_room_state_record_tied_to_producer_lineage",
        "evidence": [
            _json_ref(
                ROOM_MANIFEST,
                "/seb",
                status="verified",
                note="floor0 seb is partial fixture only, not a room state record",
            ),
            _json_ref(
                WAVE5_2_FURNITURE_DRAW_FIXTURE,
                "/runtime_policy/placement",
                status="verified",
                note="explicit adapter fixture, not recovered room placement",
            ),
        ],
    }

    explanation = (
        "The current page shows three fixture objects because the adapter manifest enumerates "
        "exactly three verified source assets (reception, desk, chair). Their current x/y and "
        "sort values are diagnostic-only fixture coordinates, while the scoped source evidence "
        "still lacks a persisted/generated floor0 room snapshot that ties those objects back to "
        "an original room map."
    )
    absence_scope = (
        "no persisted floor0 room-state record or generated room-state record was found in the "
        "scoped C#/C/assembly evidence. The only floor0 data available is the partial "
        "fixture/adapter manifest and the bounded producer traces, so the original room/object "
        "placement remains unknown."
    )

    evidence = (
        _source_ref(GAMEFORM_CS, "internal static int[] OfficeObjecList;", function=None),
        _source_ref(GAMEFORM_CS, "public int AddObjec(int TSyurui, int TX, int TY, int TCX, int TCY, int TWX, int TWY, int TSY)", function="AddObjec"),
        _source_ref(GAMEFORM_CS, "public unsafe void CallHikkosi(int TOffice, int TMode, bool isLoad = false)", function="CallHikkosi"),
        _source_ref(GAMEFORM_CS, "public void CallPCChange(int TOffice, int TPC)", function="CallPCChange"),
        _source_ref(GAMEFORM_CS, "public void CallDeskChange(int TOffice, int TDesk)", function="CallDeskChange"),
        _source_ref(GAMEFORM_CS, "public void CallChairChange(int TOffice, int TChair)", function="CallChairChange"),
        _source_ref(GAMEFORM_CS, "private static int[] GetDeskImgData(int desk)", function="GetDeskImgData"),
        _source_ref(GAMEFORM_CS, "public static int[] GetChairImgData(int chair)", function="GetChairImgData"),
        _source_ref(GAMEFORM_CS, "private void DrawDesk(Graphics g, int desk, int pc, int display, int x, int y, int ux, int uy, int uw, int uh)", function="DrawDesk"),
        _source_ref(GAMEFORM_CS, "private void DrawChair(Graphics g, int chair, int x, int y, int ux, int uy, int uw, int uh)", function="DrawChair"),
        _source_ref(GAMEFORM_CS, "private void DrawReception(Graphics g, int x, int y, int ux, int uy, int uw, int uh)", function="DrawReception"),
        _source_ref(FORM_C, "void form_GameForm__CallHikkosi(undefined8 param_1,int param_2,int param_3)", function="form_GameForm__CallHikkosi"),
        _source_ref(FORM_C, "void form_GameForm__CallPCChange(undefined8 param_1,uint param_2,undefined4 param_3)", function="form_GameForm__CallPCChange"),
        _source_ref(FORM_C, "void form_GameForm__CallDeskChange(undefined8 param_1,uint param_2,undefined4 param_3)", function="form_GameForm__CallDeskChange"),
        _source_ref(FORM_C, "void form_GameForm__CallChairChange(undefined8 param_1,uint param_2,undefined4 param_3)", function="form_GameForm__CallChairChange"),
    )

    source_files = {
        _relative(SOURCE_INVENTORY): _sha256(SOURCE_INVENTORY),
        _relative(RESOURCE_CONTRACT): _sha256(RESOURCE_CONTRACT),
        _relative(SEB_SEMANTICS_CONTRACT): _sha256(SEB_SEMANTICS_CONTRACT),
        _relative(WAVE2_PLACEMENT_FIXTURE): _sha256(WAVE2_PLACEMENT_FIXTURE),
        _relative(WAVE2_FURNITURE_CONTRACT): _sha256(WAVE2_FURNITURE_CONTRACT),
        _relative(WAVE5_1_FURNITURE_MANIFEST): _sha256(WAVE5_1_FURNITURE_MANIFEST),
        _relative(WAVE5_2_FURNITURE_DRAW_FIXTURE): _sha256(WAVE5_2_FURNITURE_DRAW_FIXTURE),
        _relative(WAVE5_8_ROOM_CALLER_CONTRACT): _sha256(WAVE5_8_ROOM_CALLER_CONTRACT),
        _relative(WAVE5_9_OBJECT_PRODUCER_CONTRACT): _sha256(WAVE5_9_OBJECT_PRODUCER_CONTRACT),
        _relative(ROOM_MANIFEST): _sha256(ROOM_MANIFEST),
        _relative(GAMEFORM_CS): _sha256(GAMEFORM_CS),
        _relative(FORM_C): _sha256(FORM_C),
    }

    summary = {
        "fixture_object_count": len(records),
        "verified_asset_count": sum(1 for record in records if record["asset_identity"]["status"] == "verified"),
        "verified_lineage_count": sum(1 for record in candidate_records if record["status"] == "verified"),
        "candidate_lineage_count": sum(1 for record in candidate_records if record["status"] == "candidate"),
        "unknown_floor_snapshot": floor0_snapshot["status"] == "unknown",
        "classification": "asset_identity_verified_placement_unknown",
    }

    return ObjectPlacementContract(
        schema_version="object-placement-contract-v1",
        phase="Phase5",
        wave="Wave5",
        status="unknown",
        authority="diagnostic_only",
        source_roots_read_only=True,
        legacy_equivalence=False,
        explanation=explanation,
        absence_scope=absence_scope,
        adapter_page=adapter_page,
        floor0_snapshot=floor0_snapshot,
        records=records,
        candidate_records=candidate_records,
        summary=summary,
        evidence=evidence,
        source_files=source_files,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    contract = build_object_placement_contract()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(contract.to_dict(), indent=2, sort_keys=True) + "\n")
    print(
        json.dumps(
            {
                "output": _relative(args.output),
                "status": contract.status,
                "fixture_object_count": contract.summary["fixture_object_count"],
                "verified_lineage_count": contract.summary["verified_lineage_count"],
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
