"""Reviewed facts from the current APK's IL2CPP native-method extraction.

This module is a small, source-controlled ledger for normalized facts that were
read from the current APK with Il2CppDumper metadata and Ghidra method-body
extraction.  It is evidence tooling only: it is never imported by the browser
runtime and it does not execute recovered C#.
"""

from __future__ import annotations


APK_RELATIVE_PATH = "sources/raw/Social_Dev_Story_v2.5.1.apk"
IL2CPP_METADATA_VERSION = 31

NATIVE_EXTRACTION_RECIPE = {
    "metadata": "Il2CppDumper v6.7.46",
    "native_body_review": "Ghidra 12.1.2 no-analysis decompile/disassembly at metadata RVAs",
    "architecture": "arm64-v8a",
    "elf_rva_file_offset": {
        "status": "reviewed_current_apk",
        "rule": "For the reviewed APK's relevant second LOAD segment, file_offset = RVA - 0x4000.",
        "segment_virtual_start": "0xE6805C",
        "segment_file_offset": "0xE6405C",
        "scope": "Relevant reviewed RVAs in this package; do not generalize to another APK.",
    },
    "status": "reviewed_current_apk",
}


NATIVE_METHODS = [
    {
        "id": "room-init-obj-chips",
        "class": "Room",
        "method": "InitObjChips",
        "signature": "void InitObjChips(RoomData roomData)",
        "rva_hex": "0x12CB448",
        "rva_decimal": 19706952,
        "body_status": "reviewed_native_body",
    },
    {
        "id": "room-place-door",
        "class": "Room",
        "method": "PlaceDoor",
        "signature": "void PlaceDoor()",
        "rva_hex": "0x12CB5E8",
        "rva_decimal": 19707368,
        "body_status": "metadata_and_source_anchor",
    },
    {
        "id": "room-setup-big-chips-parent",
        "class": "Room",
        "method": "SetupBigChipsParent",
        "signature": "void SetupBigChipsParent()",
        "rva_hex": "0x12CB864",
        "rva_decimal": 19708004,
        "body_status": "reviewed_native_body",
    },
    {
        "id": "room-place-object",
        "class": "Room",
        "method": "PlaceObj",
        "signature": "bool PlaceObj(int ix, int iy, FurnitureData furnitureData, bool immediately)",
        "rva_hex": "0x12CE540",
        "rva_decimal": 19719488,
        "body_status": "reviewed_native_body",
    },
    {
        "id": "objchip-constructor",
        "class": "ObjChip",
        "method": ".ctor",
        "signature": "void .ctor(int ix, int iy, int type, FurnitureData furnitureData, Room room)",
        "rva_hex": "0x12BEA30",
        "rva_decimal": 19655216,
        "body_status": "reviewed_native_body",
    },
    {
        "id": "objchip-standing-positions",
        "class": "ObjChip",
        "method": "GetStandingPositions",
        "signature": "Vector2D[] GetStandingPositions()",
        "rva_hex": "0x12C4868",
        "rva_decimal": 19679336,
        "body_status": "reviewed_native_body",
    },
    {
        "id": "objchip-is-passable",
        "class": "ObjChip",
        "method": "IsPassable",
        "signature": "bool IsPassable()",
        "rva_hex": "0x12C4AB8",
        "rva_decimal": 19679928,
        "body_status": "reviewed_native_body",
    },
    {
        "id": "objchip-place-object",
        "class": "ObjChip",
        "method": "PlaceObj",
        "signature": "void PlaceObj(FurnitureData furnitureData, bool var_override, bool immediately)",
        "rva_hex": "0x12C4308",
        "rva_decimal": 19677960,
        "body_status": "reviewed_native_body",
    },
    {
        "id": "room-place-desk",
        "class": "Room",
        "method": "PlaceDesk",
        "signature": "void PlaceDesk(int num)",
        "rva_hex": "0x12CEFC8",
        "rva_decimal": 19722184,
        "body_status": "reviewed_native_body",
    },
    {
        "id": "appdata-new-game",
        "class": "AppData",
        "method": "NewGame",
        "signature": "bool NewGame(string companyName, int firstGenreId, FastVector initStaffs)",
        "rva_hex": "0x1263A70",
        "rva_decimal": 19282544,
        "body_status": "metadata_and_source_anchor",
    },
    {
        "id": "astar-connect-neighbors",
        "class": "Astar",
        "method": "ConnectNeighbors",
        "signature": "void ConnectNeighbors(Room room)",
        "rva_hex": "0x110DF4C",
        "rva_decimal": 17882956,
        "body_status": "reviewed_native_body",
    },
    {
        "id": "astar-add-neighbor",
        "class": "Astar",
        "method": "AddNeighbor",
        "signature": "void AddNeighbor(int nodeX, int nodeY, Room room)",
        "rva_hex": "0x110F248",
        "rva_decimal": 17887816,
        "body_status": "reviewed_native_body",
    },
    {
        "id": "astar-search-route",
        "class": "Astar",
        "method": "_searchRoute",
        "signature": "bool _searchRoute(int startX, int startY, int goalX, int goalY, Room room, FastVector route)",
        "rva_hex": "0x110EBF0",
        "rva_decimal": 17886192,
        "body_status": "reviewed_native_body",
    },
    {
        "id": "astar-search-route-public",
        "class": "Astar",
        "method": "SearchRoute",
        "signature": "bool SearchRoute(int startX, int startY, int goalX, int goalY, Room room, FastVector route, int flag)",
        "rva_hex": "0x110E080",
        "rva_decimal": 17883264,
        "body_status": "reviewed_native_body",
    },
]


STANDING_POSITIONS = {
    "base": {
        "x": "(ix + iy) * 20",
        "y": "(iy - ix) * 10",
    },
    "order": [
        {"index": 0, "x": "baseX + 34", "y": "baseY + 25"},
        {"index": 1, "x": "baseX + 6", "y": "baseY + 11"},
        {"index": 2, "x": "baseX + 34", "y": "baseY + 11"},
        {"index": 3, "x": "baseX + 6", "y": "baseY + 25"},
    ],
    "status": "contract_ready",
}


NEIGHBOR_POLICY = {
    "shape": "3x3 centered neighborhood",
    "connectivity": 4,
    "offsets": [
        {"dx": -1, "dy": 0, "name": "west"},
        {"dx": 1, "dy": 0, "name": "east"},
        {"dx": 0, "dy": -1, "name": "north"},
        {"dx": 0, "dy": 1, "name": "south"},
    ],
    "corners_included": False,
    "center_included": False,
    "out_of_bounds": "GetNode result is skipped",
    "status": "contract_ready",
}


PASSMAP_CONSUMER = {
    "field": "FurnitureData.passMap_",
    "pass_cell_value_candidate": 0,
    "anchor_index": "dx_ + dy_ * 3 + 4",
    "window": {
        "rows": 3,
        "columns": 3,
        "row_start": "floor(anchor / 3) * 3",
        "column_start": "(anchor mod 3) * 3",
        "access": "passMap[rowStart + rowOffset][columnStart + columnOffset]",
    },
    "zero_cell_branch": "returns the current loop boolean immediately; for a valid 3x3 scan this is true before the final all-nonzero row completes",
    "null_furniture_branch": "type 3/4 with furnitureData_ == null takes a separate fallback branch",
    "boolean_semantics": "true iff at least one selected passMap cell is zero; all nine nonzero cells return false",
    "status": "contract_ready_fixture_verified",
}


FURNITURE_PLACEMENT_MODEL = {
    "obj_map_role": "layout/type grid; native InitObjChips passes the raw cell as ObjChip.type_",
    "obj_map_does_not_store": "FurnitureData id per occupied cell",
    "objchip_place_obj": [
        "binds furnitureData_",
        "resets frame_, sebFrame_ and useNum_",
        "type 2 reads RoomData.objDir_[iy][ix] for direction_",
        "type 1 derives border direction from the chip position",
        "type 4 placement expands through its multi-chip parent/footprint path",
    ],
    "room_place_desk": {
        "empty_chip_type": 2,
        "selector": "FurnitureData.Check(FLAG_INIT_DESK)",
        "flag_value": 16384,
        "action": "PlaceObj on an empty type-2 chip until the requested count is reached",
    },
    "new_game_initial_place": {
        "empty_chip_type": 1,
        "selector": "FurnitureData.Check(FLAG_INIT_PLACE)",
        "flag_value": 32768,
        "action": "AppData.NewGame consumes empty type-1 chips while scanning initial-place furniture",
    },
    "status": "bounded_contract",
    "catalog_status": "pending_runtime_inventory_and_selector_review",
}


ROUTE_FILTER = {
    "source_observed_bounded": [
        "type 2 with HasObj() is rejected",
        "type 3/4 with IsPassable() == false is rejected",
        "type 6 is rejected",
    ],
    "native_search_body_status": "reviewed_native_body",
    "goal_filter": {
        "public_method": "SearchRoute(..., int flag)",
        "flag_values": {
            "FLAG_GOAL_IS_DESK": 1,
            "FLAG_GOAL_IS_EQUIP": 2,
            "FLAG_GOAL_IS_STAFF": 4,
        },
        "postprocess": "bit 1 skips equip/staff goal handling; bit 2 derives an equipment direction from a type-1 goal's objDir; bit 4 is recognized by the public postprocess branch; otherwise the default direction is used",
    },
    "status": "contract_ready_fixture_verified",
}
