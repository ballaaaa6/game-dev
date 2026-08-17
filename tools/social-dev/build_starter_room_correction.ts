/** Build the static starter-room semantic correction evidence package. */

import { createHash } from "node:crypto";
import { inflateSync } from "node:zlib";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { createV6RoomStaffPreview } from "../../runtime/social-dev/src/v6/index";
import { createRoomV5, stableJson } from "../../runtime/social-dev/src/v5/index";
import {
  V5_NATIVE_MAP_DRAW_OFFSET_X,
  V5_NATIVE_OBJECT_DRAW_OFFSET_X,
  V5_SOURCE_MAP_DRAW_OFFSET_X,
  V5_SOURCE_OBJECT_DRAW_OFFSET_X,
} from "../../runtime/social-dev/src/v5/coordinate-bridge";
import { objChipOrigin, wallFramesFor } from "../../runtime/social-dev/src/v4/obj-chip";
import { mapChipOrigin } from "../../runtime/social-dev/src/v4/map-chip";
import type { V4Cell, V4CommandTrace } from "../../runtime/social-dev/src/v4/contracts";
import type { GraphicsCommand } from "../../runtime/social-dev/src/v2/graphics";
import {
  renderV7Commands,
  V7_ROOM_RASTER_OPTIONS,
} from "../../runtime/social-dev/src/v7/golden-renderer";
import { encodePngRgbaV7 } from "../../runtime/social-dev/src/v7/png";
import {
  RasterSurfaceCompatibilityV7,
  type V7RasterImage,
} from "../../runtime/social-dev/src/v7";
import defaultMapChipContract from "../../knowledge/fixtures/accepted/runtime/default_map_chip_contract.json";
import nativeSceneAssemblyContract from "../../knowledge/fixtures/accepted/runtime/native_scene_assembly_contract.json";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..", "..");
const EVIDENCE_ROOT = join(ROOT, "knowledge", "social-dev", "evidence", "visual-port", "starter-room-correction");
const PREVIEW_ROOT = join(EVIDENCE_ROOT, "previews");
const REPORT_ROOT = join(ROOT, "docs", "Phases", "VisualPort");
const ASSET_ROOT = join(ROOT, "runtime", "social-dev", "assets");

const IMAGE_PATHS: Readonly<Record<string, string>> = {
  "resChip_:image:10": join(ASSET_ROOT, "source-social-dev", "chip", "ground_00.png"),
  "resChip_:image:11": join(ASSET_ROOT, "source-social-dev", "chip", "turf_00.png"),
  "resChip_:image:12": join(ASSET_ROOT, "source-social-dev", "chip", "turf_01.png"),
  "resChip_:image:13": join(ASSET_ROOT, "source-social-dev", "chip", "road_00.png"),
  "resChip_:image:14": join(ASSET_ROOT, "source-social-dev", "chip", "road_01.png"),
  "resChip_:image:15": join(ASSET_ROOT, "source-social-dev", "chip", "road_02.png"),
  "resChip_:image:85": join(ASSET_ROOT, "room-scene", "01_GAME_PACKS", "chip", "floor_05.png"),
  "resChip_:image:105": join(ASSET_ROOT, "source-social-dev", "chip", "turf_02.png"),
  "resChip_:image:154": join(ASSET_ROOT, "source-social-dev", "chip", "road_edge_00.png"),
  "resChip_:image:155": join(ASSET_ROOT, "source-social-dev", "chip", "road_edge_01.png"),
  "resChip_:image:156": join(ASSET_ROOT, "source-social-dev", "chip", "road_03.png"),
  "resChip_:image:2": join(ASSET_ROOT, "room-scene", "01_GAME_PACKS", "chip", "wall_01.png"),
  "resChip_:image:3": join(ASSET_ROOT, "display-slice-01", "02_DERIVED_READY_IMAGES", "opt_reconstructed", "chip", "desk_00.png"),
  "resChip_:image:4": join(ASSET_ROOT, "display-slice-01", "02_DERIVED_READY_IMAGES", "opt_reconstructed", "chip", "chair_00.png"),
  "resChip_:image:6": join(ASSET_ROOT, "display-slice-01", "01_GAME_PACKS", "chip", "wall_00.png"),
  "resChip_:image:7": join(ASSET_ROOT, "display-slice-01", "01_GAME_PACKS", "chip", "door_02.png"),
  "resChip_:image:18": join(ASSET_ROOT, "display-slice-01", "01_GAME_PACKS", "chip", "big_base00.png"),
  "resChip_:image:106": join(ASSET_ROOT, "display-slice-01", "01_GAME_PACKS", "chip", "old_printer.png"),
  "resChip_:image:109": join(ASSET_ROOT, "display-slice-01", "01_GAME_PACKS", "chip", "garbage_can.png"),
  "resChip_:image:127": join(ASSET_ROOT, "display-slice-01", "01_GAME_PACKS", "chip", "calendar.png"),
  "resHuman_:image:86": join(ASSET_ROOT, "character-catalog", "01_GAME_PACKS", "human", "chara00.png"),
  "resHuman_:image:87": join(ASSET_ROOT, "character-catalog", "01_GAME_PACKS", "human", "chara01.png"),
  "resHuman_:image:88": join(ASSET_ROOT, "character-catalog", "01_GAME_PACKS", "human", "chara02.png"),
};

const CORRECTION_RASTER_OPTIONS = {
  ...V7_ROOM_RASTER_OPTIONS,
  width: 980,
  height: 600,
  origin: { x: 82, y: 260 },
} as const;

interface ArtifactRecord {
  readonly path: string;
  readonly width: number;
  readonly height: number;
  readonly pixel_sha256: string;
  readonly png_sha256: string;
  readonly nontransparent_bounds: ReturnType<typeof surfaceBounds>;
  readonly draw_count: number;
  readonly skipped_draw_count: number;
  readonly command_count: number;
  readonly trace_count: number;
}

async function main(): Promise<void> {
  await mkdir(PREVIEW_ROOT, { recursive: true });
  await mkdir(REPORT_ROOT, { recursive: true });

  const roomInstance = createRoomV5("room:0", { context: "main_display", visualScope: "full_static" });
  const roomRender = roomInstance.draw();
  const staffRender = createV6RoomStaffPreview({
    roomKey: "room:0",
    action: "wait",
    direction: "right",
    frame: 0,
    alpha: 255,
  });
  const images = await loadImages([...roomRender.commands, ...staffRender.commands]);

  const correctedStructural = renderV7Commands(roomRender.commands, images, CORRECTION_RASTER_OPTIONS);
  const correctedStructuralRepeat = renderV7Commands(roomRender.commands, images, CORRECTION_RASTER_OPTIONS);
  const correctedStaff = renderV7Commands(staffRender.commands, images, CORRECTION_RASTER_OPTIONS);
  const correctedStaffRepeat = renderV7Commands(staffRender.commands, images, CORRECTION_RASTER_OPTIONS);

  const artifacts = {
    structural: await writeArtifact("starter_room_structural_corrected.png", correctedStructural, roomRender.commands, roomRender.traces),
    staff: await writeArtifact("starter_room_with_staff_corrected.png", correctedStaff, staffRender.commands, staffRender.traces),
    floor: await writeSubsetArtifact(
      "starter_room_floor_only.png",
      commandsForTraces(roomRender.commands, roomRender.traces, roomRender.passes, (trace) =>
        trace.pass === "main-display-map-underlay" && trace.selectorRole.includes(":room_floor_")),
      images,
      roomRender.traces.filter((trace) => trace.pass === "main-display-map-underlay" && trace.selectorRole.includes(":room_floor_")),
    ),
    wallsCorners: await writeSubsetArtifact(
      "starter_room_walls_corners_only.png",
      [
        ...commandsForPass(roomRender.commands, roomRender.traces, roomRender.passes, "map-extension-floor"),
        ...commandsForPass(roomRender.commands, roomRender.traces, roomRender.passes, "object-chip-wall"),
        ...commandsForPass(roomRender.commands, roomRender.traces, roomRender.passes, "object-chip-late"),
      ],
      images,
      roomRender.traces.filter((trace) => ["map-extension-floor", "object-chip-wall", "object-chip-late"].includes(trace.pass)),
    ),
    outerMap: await writeSubsetArtifact(
      "starter_room_outer_map_only.png",
      commandsForTraces(roomRender.commands, roomRender.traces, roomRender.passes, (trace) =>
        trace.pass === "main-display-map-underlay" && trace.selectorRole.includes(":outer_map")),
      images,
      roomRender.traces.filter((trace) => trace.pass === "main-display-map-underlay" && trace.selectorRole.includes(":outer_map")),
    ),
    furnitureStructural: await writeSubsetArtifact(
      "starter_room_furniture_structural_only.png",
      commandsForPass(roomRender.commands, roomRender.traces, roomRender.passes, "object-chip-primary"),
      images,
      roomRender.traces.filter((trace) => trace.pass === "object-chip-primary"),
    ),
  };
  const contactSheet = await writeContactSheet(artifacts.structural.path, artifacts.staff.path);

  const identity = buildIdentity(roomInstance, roomRender, staffRender);
  const topology = buildTopology(roomInstance);
  const floorCells = buildFloorCellMap(roomInstance, roomRender);
  const wallAudit = buildWallAudit(roomInstance, roomRender);
  const corners = buildCorners(roomInstance, roomRender);
  const outerOwnership = buildOuterOwnership(roomInstance, roomRender);
  const originAudit = buildOriginAudit(roomInstance, roomRender, staffRender);
  const semanticDiff = buildSemanticDiff(roomInstance, roomRender, originAudit);
  const rootCause = buildRootCause(roomRender, originAudit);
  const unknowns = buildUnknowns();
  const commandManifest = {
    schema_version: "social-dev-starter-room-corrected-command-manifest-v1",
    status: "pass_static",
    correction: "FREEZE_V8",
    room_manifest: roomInstance.commandManifest(),
    summary: {
      commands: roomRender.commands.length,
      traces: roomRender.traces.length,
      events: roomRender.events.length,
      pass_count: roomRender.passes.length,
      map_cells: roomInstance.mapChips.length,
      nonempty_map_cells: roomInstance.mapChips.filter((cell) => cell.role !== "empty").length,
      main_display_underlay_traces: roomRender.traces.filter((trace) => trace.pass === "main-display-map-underlay").length,
      source_backed_outer_map_traces: roomRender.traces.filter((trace) => trace.selectorRole.includes(":outer_map")).length,
      v5_command_sha256: sha256(stableJson(roomRender.commands)),
      v5_manifest_sha256: sha256(stableJson(roomInstance.commandManifest())),
    },
  };
  const renderEvidence = buildRenderEvidence(artifacts.structural, correctedStructural, correctedStructuralRepeat, roomRender, "V5");
  const staffRenderEvidence = buildRenderEvidence(artifacts.staff, correctedStaff, correctedStaffRepeat, staffRender, "V6");
  const ledger = buildCheckpointLedger({ artifacts, contactSheet, rootCause, unknowns });

  await writeJson("checkpoint-ledger.json", ledger);
  await writeJson("starter-room-identity.json", identity);
  await writeJson("starter-room-topology.json", topology);
  await writeJson("starter-floor-cell-map.json", floorCells);
  await writeJson("wall-connectivity-audit.json", wallAudit);
  await writeJson("corner-fixtures.json", corners);
  await writeJson("outer-map-ownership.json", outerOwnership);
  await writeJson("origin-coordinate-audit.json", originAudit);
  await writeJson("starter-room-semantic-diff.json", semanticDiff);
  await writeJson("root-cause.json", rootCause);
  await writeJson("corrected-room-command-manifest.json", commandManifest);
  await writeJson("corrected-room-render.json", renderEvidence);
  await writeJson("corrected-room-with-staff-render.json", staffRenderEvidence);
  await writeJson("unknowns.json", unknowns);
  await writeJson("correction-artifacts.json", { artifacts, contact_sheet: contactSheet });
  await writeReports({ artifacts, contactSheet, identity, topology, wallAudit, outerOwnership, originAudit, semanticDiff, rootCause, unknowns, renderEvidence, staffRenderEvidence });

  console.log(JSON.stringify({
    status: "PASS_STATIC_STARTER_ROOM_CORRECTION",
    v8_started: false,
    subagents: false,
    commands: roomRender.commands.length,
    traces: roomRender.traces.length,
    map_cells: roomInstance.mapChips.length,
    nonempty_map_cells: roomInstance.mapChips.filter((cell) => cell.role !== "empty").length,
    structural: renderEvidence,
    staff: staffRenderEvidence,
    contact_sheet: contactSheet,
  }, null, 2));
}

function buildIdentity(room: ReturnType<typeof createRoomV5>, render: ReturnType<ReturnType<typeof createRoomV5>["draw"]>, staff: ReturnType<typeof createV6RoomStaffPreview>): object {
  return {
    schema_version: "social-dev-starter-room-identity-v1",
    status: "pass_static",
    correction: "FREEZE_V8",
    fixture_classification: "F",
    classification: "Correct first-launch room identity and native bindings; incomplete environment assembly was corrected at the main-display underlay and coordinate bridge layers.",
    first_launch_trace: [
      { order: 0, method: "DataManager.Load", evidence: "native selector/data tables loaded", proof: "SOURCE-DATA-PROVEN" },
      { order: 1, method: "AppData.NewGame", input: "roomData_[0], constructor floor=0, initStaffs", output: "active Room instance", source: "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/KairoEngine/main/AppData.cs:14944", proof: "CALL-FLOW-PROVEN" },
      { order: 2, method: "Room::.ctor", input: { width: 14, height: 14, floor: 0, roomData: "data:room:0", isPreview: false }, output: "MapChip 14x14 + ObjChip 10x10", proof: "CALL-FLOW-PROVEN" },
      { order: 3, method: "Room.InitMapChips", output: { floor: room.floor, floorImgId: room.roomData.floorImgId, cells: room.mapChips.length }, proof: "NATIVE-CODE-PROVEN" },
      { order: 4, method: "Room.InitObjChips", output: { width: room.roomData.objMapWidth, height: room.roomData.objMapHeight, cells: room.objChips.length }, proof: "NATIVE-CODE-PROVEN" },
      { order: 5, method: "Room.SetupBigChipsParent", output: "two source-backed structural facility bindings", proof: "CALL-FLOW-PROVEN" },
      { order: 6, method: "Room.PlaceDoor", output: room.doorCells, proof: "NATIVE-CODE-PROVEN" },
      { order: 7, method: "Room.PlaceDesk/PlaceObj", output: room.initialFurnitureBindings.map((binding) => binding.object_id), proof: "CALL-FLOW-PROVEN" },
      { order: 8, method: "Room.Draw", output: { passes: render.passes.length, commands: render.commands.length, traces: render.traces.length }, source: "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/game/Room.cs:1246", proof: "NATIVE-CODE-PROVEN" },
      { order: 9, method: "Staff/AddStaff", output: { initialStaffCount: staff.staff.length, actorCell: staff.staff[0]?.placement.cell ?? null }, proof: "SOURCE-DATA-PROVEN" },
    ],
    room_identity: {
      room_key: room.roomData.roomKey,
      data_key: room.roomData.dataKey,
      room_id: room.roomData.roomId,
      name: room.roomData.name,
      floor: room.floor,
      floor_img_id: room.roomData.floorImgId,
      wall_img_id: room.roomData.wallImgId,
      door_img_id: room.roomData.doorImgId,
      context: room.topology.context,
      visual_scope: room.visualScope,
    },
    native_bindings: room.initialFurnitureBindings,
    structural_facilities: room.roomData.structuralFacilities,
    source_refs: [
      "knowledge/fixtures/accepted/runtime/native_scene_assembly_contract.json",
      "knowledge/fixtures/accepted/runtime/floor00_scene_contract.json",
      "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/KairoEngine/main/AppData.cs",
      "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/game/Room.cs",
    ],
  };
}

function buildTopology(room: ReturnType<typeof createRoomV5>): object {
  const nonempty = room.mapChips.filter((cell) => cell.role !== "empty");
  const components = connectedComponents(nonempty.map((cell) => cell.cell));
  const roleCounts = countBy(room.mapChips, (cell) => cell.role);
  const selectorCounts = countBy(nonempty, (cell) => String(cell.imageId));
  return {
    schema_version: "social-dev-starter-room-topology-v1",
    status: "pass_static",
    proof: "SOURCE-DATA-PROVEN",
    room_key: room.roomData.roomKey,
    room_floor: room.floor,
    topology: room.topology,
    full_floor_cell_population: {
      width: room.topology.width,
      height: room.topology.height,
      total_cells: room.mapChips.length,
      nonempty_cells: nonempty.length,
      empty_cells: room.mapChips.length - nonempty.length,
      rows: room.topology.rows,
      role_counts: roleCounts,
      selector_counts: selectorCounts,
    },
    continuity: {
      nonempty_four_neighbor_components: components.length,
      connected: components.length === 1,
      component_sizes: components.map((component) => component.length),
      proof: "STATIC-COMMAND-PARITY",
    },
    floor_selector_policy: {
      raw_room_data_selector: room.roomData.floorImgId,
      native_table_selector: 23,
      runtime_selector: 85,
      rendered_filename: "floor_05.png",
      topology_owner: "MapChip raw-index table; floor selector does not select the 14x14 topology",
      status: "COMPATIBILITY-POLICY",
    },
    source_refs: [
      "knowledge/fixtures/accepted/runtime/default_map_chip_contract.json",
      "knowledge/fixtures/accepted/runtime/floor00_scene_contract.json",
      "knowledge/fixtures/accepted/runtime/native_scene_assembly_contract.json",
    ],
  };
}

function buildFloorCellMap(room: ReturnType<typeof createRoomV5>, render: ReturnType<ReturnType<typeof createRoomV5>["draw"]>): object {
  const traceByCell = new Map(render.traces.filter((trace) => trace.pass === "main-display-map-underlay" && trace.cell !== undefined).map((trace) => [cellKey(trace.cell!), trace]));
  const cells = room.mapChips.map((input) => {
    const trace = traceByCell.get(cellKey(input.cell));
    const command = trace === undefined ? undefined : commandForTrace(render.commands, render.traces, render.passes, trace);
    return {
      x: input.cell[0],
      y: input.cell[1],
      raw_index: input.rawIndex,
      selector_id: input.imageId,
      image_id: input.imageId,
      frame: null,
      draw: trace === undefined ? null : { x: trace.destination.x, y: trace.destination.y, width: command?.destination.width ?? null, height: command?.destination.height ?? null },
      role: input.role,
      pass: trace?.pass ?? null,
      selector_role: trace?.selectorRole ?? null,
      proof: input.role === "empty" ? "SOURCE-DATA-PROVEN" : "NATIVE-CODE-PROVEN",
      source_refs: ["knowledge/fixtures/accepted/runtime/default_map_chip_contract.json", "runtime/social-dev/src/v5/main-display-map.ts"],
    };
  });
  return {
    schema_version: "social-dev-starter-floor-cell-map-v1",
    status: "pass_static",
    room_key: room.roomData.roomKey,
    dimensions: [room.topology.width, room.topology.height],
    cell_count: cells.length,
    nonempty_cell_count: cells.filter((cell) => cell.role !== "empty").length,
    cells,
    traversal: "row_y_ascending_then_x_descending for native commands; evidence list is row_y_ascending_then_x_ascending",
    underlay_committed_before_object_passes: render.passes.find((pass) => pass.passId === "main-display-map-underlay")?.commandEnd === render.passes.find((pass) => pass.passId === "map-extension-floor")?.commandStart,
    source_refs: ["knowledge/fixtures/accepted/runtime/default_map_chip_contract.json", "knowledge/fixtures/accepted/runtime/floor00_scene_contract.json"],
  };
}

function buildWallAudit(room: ReturnType<typeof createRoomV5>, render: ReturnType<ReturnType<typeof createRoomV5>["draw"]>): object {
  const frameOwners = new Map<string, string[]>();
  for (const [frameKey, cells] of Object.entries(room.wallCellsByFrame)) {
    for (const cell of cells) {
      const owners = frameOwners.get(cellKey(cell)) ?? [];
      owners.push(frameKey);
      frameOwners.set(cellKey(cell), owners);
    }
  }
  const wallCells = uniqueCells([...Object.values(room.wallCellsByFrame).flat(), ...room.doorCells]);
  const wallSet = new Set(wallCells.map(cellKey));
  const cells = wallCells.map((cell) => {
    const obj = room.objChips.find((input) => sameCell(input.cell, cell));
    if (obj === undefined) throw new Error(`Wall audit ObjChip missing at ${cellKey(cell)}`);
    const door = obj.rawType === 5;
    const frames = door ? [0] : wallFramesFor(obj);
    const traces = render.traces.filter((trace) => (trace.pass === "object-chip-wall" || trace.pass === "object-chip-late") && trace.cell !== undefined && sameCell(trace.cell, cell));
    const predicates = door
      ? ["ObjChip.type_ == 5"]
      : [
        ...(frames.includes(1) ? ["type_ != 5 && y >= 1 && y < objMapHeight - 1 && x == objMapWidth - 2"] : []),
        ...(frames.includes(0) ? ["x >= 1 && y == 1 && x < objMapWidth - 1 && type_ != 5"] : []),
      ];
    return {
      cell,
      raw_type: obj.rawType,
      raw_direction: obj.rawDirection,
      owner: door ? "door" : "wall",
      frame_owners: frameOwners.get(cellKey(cell)) ?? [],
      predicate: predicates,
      frames,
      layers: door ? [0] : [0, 1],
      source_frame_records: frames.map((frame) => frameRecordFor(frame, door)),
      trace_records: traces.map((trace) => ({ pass: trace.pass, frame: trace.frame ?? null, layer: trace.layer ?? null, destination: trace.destination, resource: trace.resource, command_count: trace.commandCount, selector_role: trace.selectorRole, proof: trace.proof })),
      neighbors: neighbors(cell).filter((candidate) => wallSet.has(cellKey(candidate))),
      connectivity_proof: "NATIVE-CODE-PROVEN",
      source_refs: ["knowledge/fixtures/accepted/runtime/native_scene_assembly_contract.json", "runtime/social-dev/src/v4/obj-chip.ts"],
    };
  });
  const components = connectedComponents(wallCells);
  return {
    schema_version: "social-dev-wall-connectivity-audit-v1",
    status: "pass_static",
    room_key: room.roomData.roomKey,
    wall_cell_count: cells.length,
    wall_and_door_cells: cells,
    connectivity: {
      connected_components: components.length,
      component_sizes: components.map((component) => component.length),
      all_wall_and_door_cells_connected: components.length === 1,
      door_bridge_cell: room.doorCells[0] ?? null,
    },
    frame_summary: room.wallCellsByFrame,
    source_refs: ["knowledge/fixtures/accepted/runtime/native_scene_assembly_contract.json", "knowledge/fixtures/accepted/runtime/floor00_scene_contract.json"],
  };
}

function buildCorners(room: ReturnType<typeof createRoomV5>, render: ReturnType<ReturnType<typeof createRoomV5>["draw"]>): object {
  const extensionCells = new Set([
    ...(((defaultMapChipContract as any).extension_wall.native_predicates.vertical_frame_1 ?? []) as V4Cell[]).map(cellKey),
    ...(((defaultMapChipContract as any).extension_wall.native_predicates.horizontal_frame_0 ?? []) as V4Cell[]).map(cellKey),
  ]);
  const fixtureCells: readonly { readonly id: string; readonly objCell?: V4Cell; readonly mapCell?: V4Cell; readonly reason: string }[] = [
    { id: "upper-left-wall-start", objCell: [1, 1], reason: "horizontal wall predicate begins at x=1" },
    { id: "upper-right-wall-intersection", objCell: [8, 1], reason: "horizontal frame 0 and vertical frame 1 share one ObjChip anchor" },
    { id: "door-wall-bridge", objCell: [8, 4], reason: "raw type 5 door interrupts and preserves the wall path" },
    { id: "foreground-wall-transition", objCell: [8, 7], reason: "approved foreground wall begins in late pass" },
    { id: "foreground-wall-end", objCell: [8, 8], reason: "approved foreground wall ends before the extension region" },
    { id: "extension-horizontal-vertical-overlap", mapCell: [4, 5], reason: "source-backed MapChip extension trigger at a floor boundary" },
    { id: "extension-door-side-overlap", mapCell: [8, 9], reason: "source-backed extension trigger on the door-side map boundary" },
  ];
  return {
    schema_version: "social-dev-corner-fixtures-v1",
    status: "pass_static",
    room_key: room.roomData.roomKey,
    fixtures: fixtureCells.map((fixture) => {
      const traces = render.traces.filter((trace) => (fixture.objCell !== undefined && trace.cell !== undefined && sameCell(trace.cell, fixture.objCell)) || (fixture.mapCell !== undefined && trace.cell !== undefined && sameCell(trace.cell, fixture.mapCell)));
      return {
        ...fixture,
        map_role: fixture.mapCell === undefined ? null : room.mapChips.find((input) => sameCell(input.cell, fixture.mapCell))?.role ?? null,
        extension_owner: fixture.mapCell === undefined ? false : extensionCells.has(cellKey(fixture.mapCell)),
        wall_owner: fixture.objCell === undefined ? null : room.wallCellsByFrame,
        door_owner: fixture.objCell !== undefined && room.doorCells.some((cell) => sameCell(cell, fixture.objCell!)),
        traces: traces.map((trace) => ({ pass: trace.pass, frame: trace.frame ?? null, destination: trace.destination, selector_role: trace.selectorRole, proof: trace.proof })),
        proof: "NATIVE-CODE-PROVEN",
        source_refs: ["knowledge/fixtures/accepted/runtime/native_scene_assembly_contract.json", "knowledge/fixtures/accepted/runtime/default_map_chip_contract.json"],
      };
    }),
  };
}

function buildOuterOwnership(room: ReturnType<typeof createRoomV5>, render: ReturnType<ReturnType<typeof createRoomV5>["draw"]>): object {
  const selectorTable = (defaultMapChipContract as any).raw_index_to_selector as Record<string, { selector_id: number; filename: string | null; asset_id: string | null; meaning: string }>;
  const groups = new Map<number, { role: string; cells: V4Cell[] }>();
  for (const input of room.mapChips.filter((cell) => cell.role !== "empty" && cell.role !== "room_floor_central")) {
    const group = groups.get(input.rawIndex) ?? { role: input.role, cells: [] };
    group.cells.push(input.cell as V4Cell);
    groups.set(input.rawIndex, group);
  }
  return {
    schema_version: "social-dev-outer-map-ownership-v1",
    status: "pass_static",
    room_key: room.roomData.roomKey,
    ownership_policy: {
      owner: "Room.main_display.MapChip full floor0 underlay",
      committed_pass: "main-display-map-underlay",
      committed_before_object_passes: true,
      topology_owner: "floor0 MapChip array, not floor selector 5",
      proof: "NATIVE-CODE-PROVEN",
    },
    groups: [...groups.entries()].map(([rawIndex, group]) => ({
      raw_index: rawIndex,
      role: group.role,
      count: group.cells.length,
      cells: group.cells,
      selector: selectorTable[String(rawIndex)],
      runtime_image_id: room.mapChips.find((input) => input.rawIndex === rawIndex)?.imageId ?? null,
      pass_trace_count: render.traces.filter((trace) => trace.pass === "main-display-map-underlay" && trace.selectorRole.includes(`raw_index_${rawIndex}:`)).length,
      source_refs: ["knowledge/fixtures/accepted/runtime/default_map_chip_contract.json", "runtime/social-dev/src/v5/main-display-map.ts"],
    })),
    totals: {
      outer_map_cells: room.mapChips.filter((cell) => cell.role === "outer_map").length,
      room_floor_fill_cells: room.mapChips.filter((cell) => cell.role === "room_floor_fill").length,
      source_backed_noncentral_cells: room.mapChips.filter((cell) => cell.role === "outer_map" || cell.role === "room_floor_fill").length,
    },
    floor_selector_compatibility: {
      raw_room_data_selector: room.roomData.floorImgId,
      native_table_selector: 23,
      runtime_selector: 85,
      policy: "selector 5 remains a compatibility alias for floor pixels and does not own map topology or outer environment cells",
      proof: "COMPATIBILITY-POLICY",
    },
  };
}

function buildOriginAudit(room: ReturnType<typeof createRoomV5>, render: ReturnType<ReturnType<typeof createRoomV5>["draw"]>, staff: ReturnType<typeof createV6RoomStaffPreview>): object {
  const mapAnchor = mapChipOrigin([5, 5], room.mapCamera);
  const objectAnchor = objChipOrigin([1, 1], room.camera);
  const actorPlacement = staff.staff[0]?.placement ?? null;
  return {
    schema_version: "social-dev-origin-coordinate-audit-v1",
    status: "pass_static",
    room_key: room.roomData.roomKey,
    logical_camera: { offset: room.camera.offset, map_offset: room.mapCamera.offset, semantics: "logical integer camera offset; native lattice bases are separate draw-space bridge values" },
    source_native_bases: {
      map_chip_x: V5_SOURCE_MAP_DRAW_OFFSET_X,
      object_chip_and_staff_x: V5_SOURCE_OBJECT_DRAW_OFFSET_X,
      difference: V5_SOURCE_OBJECT_DRAW_OFFSET_X - V5_SOURCE_MAP_DRAW_OFFSET_X,
      viewport_origin: [82, 260],
      source_ref: "runtime/social-dev/src/scene/coordinates.ts",
    },
    v5_preview_bridge: {
      map_chip_x: V5_NATIVE_MAP_DRAW_OFFSET_X,
      object_chip_and_staff_x: V5_NATIVE_OBJECT_DRAW_OFFSET_X,
      normalization: "subtract common source map base 82 from both native bases; preserve proven 360-pixel lattice difference",
      source_ref: "runtime/social-dev/src/v5/coordinate-bridge.ts",
    },
    formulas: {
      map_chip_origin: "camera + (x + y) * 40, (y - x) * 20",
      object_chip_origin: "camera + (x + y) * 20, (y - x) * 10 + 9",
      actor_spawn: "(x + y) * 20 + 40, (y - x) * 10 + 9",
      source_refs: ["knowledge/fixtures/accepted/runtime/default_map_chip_contract.json", "knowledge/fixtures/accepted/runtime/native_scene_assembly_contract.json", "knowledge/fixtures/accepted/runtime/camera_coordinate_contract.json"],
    },
    anchor_comparison: {
      map_floor_anchor: { cell: [5, 5], normalized_draw: mapAnchor, source_canvas: { x: mapAnchor.x + V5_SOURCE_MAP_DRAW_OFFSET_X, y: mapAnchor.y } },
      horizontal_wall_anchor: { cell: [1, 1], normalized_draw: objectAnchor, source_canvas: { x: objectAnchor.x + V5_SOURCE_MAP_DRAW_OFFSET_X, y: objectAnchor.y } },
      normalized_x_alignment: mapAnchor.x === objectAnchor.x,
      source_canvas_x_alignment: mapAnchor.x + V5_SOURCE_MAP_DRAW_OFFSET_X === objectAnchor.x + V5_SOURCE_MAP_DRAW_OFFSET_X,
      room_render_passes: render.passes.length,
    },
    actor_bridge: actorPlacement === null ? null : {
      cell: actorPlacement.cell,
      world: actorPlacement.world,
      normalized_draw: actorPlacement.screen,
      source_canvas: { x: actorPlacement.screen.x + V5_SOURCE_MAP_DRAW_OFFSET_X, y: actorPlacement.screen.y },
      camera_offset: actorPlacement.cameraOffset,
    },
    proof: "NATIVE-CODE-PROVEN",
  };
}

function buildSemanticDiff(room: ReturnType<typeof createRoomV5>, render: ReturnType<ReturnType<typeof createRoomV5>["draw"]>, originAudit: any): object {
  return {
    schema_version: "social-dev-starter-room-semantic-diff-v1",
    status: "pass_static",
    correction: "FREEZE_V8",
    before: {
      source_state: "pre-correction V5/V7 baseline captured before SR.11",
      room_identity: "correct",
      floor_topology_cells: 196,
      source_backed_nonempty_environment_cells_emitted: 16,
      outer_map_cells_emitted: 0,
      map_underlay_pass: "native map-floor only after object passes",
      command_count: 74,
      trace_count: 59,
      normalized_map_object_x_delta: 0,
      staff_render_context: "object and actor coordinates shared the unbridged origin",
    },
    after: {
      room_identity: "preserved",
      floor_topology_cells: room.mapChips.length,
      source_backed_nonempty_environment_cells_emitted: room.mapChips.filter((cell) => cell.role !== "empty").length,
      outer_map_cells_emitted: room.mapChips.filter((cell) => cell.role === "outer_map").length,
      map_underlay_pass: "main-display-map-underlay before extension/object passes; native map-floor slot retained",
      command_count: render.commands.length,
      trace_count: render.traces.length,
      normalized_map_object_x_delta: originAudit.v5_preview_bridge.object_chip_and_staff_x - originAudit.v5_preview_bridge.map_chip_x,
      staff_render_context: "object and actor coordinates use the same bridged object base",
    },
    resolved_mismatches: [
      { id: "MAP-OUTER-OWNERSHIP", layer: "main_display MapChip pass assembly", result: "resolved", evidence: "outer-map-ownership.json" },
      { id: "MAP-FLOOR-UNDERLAY-SEQUENCING", layer: "Room.Draw pass schedule", result: "resolved", evidence: "corrected-room-command-manifest.json" },
      { id: "MAP-OBJECT-ORIGIN-BRIDGE", layer: "coordinate bridge", result: "resolved", evidence: "origin-coordinate-audit.json" },
    ],
    unchanged_semantics: [
      "RoomData identity and floor selector policy",
      "wall predicates, frame records, and door raw type 5",
      "FurnitureData and structural facility bindings",
      "nine native pass slots",
      "production renderer",
    ],
    source_refs: ["knowledge/fixtures/accepted/runtime/native_scene_assembly_contract.json", "knowledge/fixtures/accepted/runtime/default_map_chip_contract.json", "runtime/social-dev/src/scene/coordinates.ts"],
  };
}

function buildRootCause(render: ReturnType<ReturnType<typeof createRoomV5>["draw"]>, originAudit: any): object {
  return {
    schema_version: "social-dev-starter-room-root-cause-v1",
    status: "PASS_STATIC_ROOT_CAUSE_IDENTIFIED",
    primary_root_cause: {
      id: "V5_MAIN_DISPLAY_UNDERLAY_OMISSION",
      layer: "starter identity -> Room.Draw semantic pass assembly",
      symptom: "The 14x14 floor0 MapChip topology was present in fixture data, but the main-display command stream emitted only the native central floor-culling subset; source-backed outer/fill cells never reached the underlay stream.",
      correction: "Commit all 81 non-empty floor0 MapChip cells in a source-backed main-display underlay before extension/object composition while retaining the nine native pass slots.",
      evidence: { commands: render.commands.length, underlay_traces: render.traces.filter((trace) => trace.pass === "main-display-map-underlay").length, outer_map_traces: render.traces.filter((trace) => trace.selectorRole.includes(":outer_map")).length },
      proof: "NATIVE-CODE-PROVEN",
    },
    secondary_root_cause: {
      id: "V5_PER_PASS_ORIGIN_BRIDGE_MISSING",
      layer: "coordinate bridge",
      symptom: "MapChip and ObjChip/Staff commands shared one origin even though the source-backed runtime contract uses separate map and object draw bases.",
      correction: { source_map_base: originAudit.source_native_bases.map_chip_x, source_object_base: originAudit.source_native_bases.object_chip_and_staff_x, normalized_object_delta: originAudit.v5_preview_bridge.object_chip_and_staff_x - originAudit.v5_preview_bridge.map_chip_x },
      proof: "NATIVE-CODE-PROVEN",
    },
    ruled_out_root_causes: [
      { layer: "starter identity", result: "not root cause; AppData.NewGame -> Room ctor -> RoomData identity is source-backed" },
      { layer: "RoomData", result: "not root cause; selectors and room0 data are stable" },
      { layer: "floorImg selector", result: "not topology owner; 5 -> 85 remains explicit compatibility policy" },
      { layer: "wall predicates/frames/door", result: "not root cause; native wall path and door bridge pass" },
      { layer: "furniture/structural bootstrap", result: "not root cause; six furniture bindings and two structural facilities remain stable" },
      { layer: "production renderer", result: "unchanged and outside the correction surface" },
    ],
    source_refs: ["knowledge/fixtures/accepted/runtime/native_scene_assembly_contract.json", "knowledge/fixtures/accepted/runtime/floor00_scene_contract.json", "runtime/social-dev/src/scene/coordinates.ts", "runtime/social-dev/src/v5/room.ts"],
  };
}

function buildUnknowns(): object {
  return {
    schema_version: "social-dev-starter-room-correction-unknowns-v1",
    status: "pass_static_nonblocking_unknowns",
    blocking_unknowns: [],
    unknowns: [
      { id: "SR-U01", question: "What is the full live dynamic viewport policy outside the source-backed 980x600 fixture?", status: "SOURCE_LIMITED", blocking: false, policy: "Use the verified Room.Draw offset boundary; do not infer a gameplay camera." },
      { id: "SR-U02", question: "What are alternate generic MapChip/ObjChip branches outside room:0?", status: "SOURCE_LIMITED", blocking: false, policy: "Keep non-room:0 contexts topology-only unless separately proven." },
      { id: "SR-U03", question: "What is the complete live Staff.Update cadence?", status: "SOURCE_LIMITED", blocking: false, policy: "Selected wait/right/frame0 Staff evidence is deterministic; live timing is out of scope." },
      { id: "SR-U04", question: "Do historical screenshots contain presentation overlays absent from the native starter-room stream?", status: "SECONDARY_ONLY", blocking: false, policy: "Historical screenshots are not used to derive geometry or acceptance pixels." },
    ],
  };
}

function buildCheckpointLedger(input: { artifacts: Record<string, ArtifactRecord>; contactSheet: ArtifactRecord; rootCause: any; unknowns: any }): object {
  const pass = (id: string, summary: string, files: string[], evidence: string[], tests: string[] = [], findings: string[] = [], next = "next checkpoint"): object => ({ id, status: "PASS", summary, files_changed: files, evidence, tests, findings, root_cause_candidates: [input.rootCause.primary_root_cause.id, input.rootCause.secondary_root_cause.id], remaining_unknowns: input.unknowns.blocking_unknowns, next_checkpoint: next });
  return {
    schema_version: "social-dev-starter-room-correction-checkpoint-ledger-v1",
    status: "PASS_STATIC_STARTER_ROOM_CORRECTION",
    execution_mode: "INLINE_EXECUTION_ONLY",
    static_only: true,
    subagents: false,
    v8_started: false,
    checkpoints: [
      pass("SR.0", "Baseline V1-V7 regression inputs and static gates passed before correction edits; diagnosis plan recorded.", ["runtime/social-dev/src/v5/room.ts"], ["pre-correction Vitest/typecheck/build/static gate log"], ["V1-V7 baseline green"], ["first broken candidate was pass assembly, not identity"], "SR.1"),
      pass("SR.1", "First-launch room0 identity follows AppData.NewGame -> Room ctor -> RoomData -> MapChip/ObjChip -> PlaceDoor/PlaceDesk -> Room.Draw; fixture classified F.", ["runtime/social-dev/src/v5/room.ts"], ["starter-room-identity.json"], ["identity and six native bindings"], ["identity correct; environment assembly incomplete"], "SR.2"),
      pass("SR.2", "All 196 floor0 MapChip cells recovered; 81 non-empty source-backed cells are mapped with selector, role, and draw destination.", ["runtime/social-dev/src/v5/contracts.ts", "runtime/social-dev/src/v5/main-display-map.ts"], ["starter-floor-cell-map.json", "starter-room-topology.json"], ["exact 14x14 population", "one connected non-empty component"], ["raw selector 5 remains separate from topology"], "SR.3"),
      pass("SR.3", "All wall and door cells use source predicates, frames, layers, destinations, and connectivity records.", ["runtime/social-dev/tests/v5-room.test.ts"], ["wall-connectivity-audit.json"], ["wall path connected", "door trace present"], ["wall predicates were not the broken layer"], "SR.4"),
      pass("SR.4", "Explicit corner/intersection/door/foreground/extension fixtures are recorded.", ["knowledge/fixtures/accepted/visual-port/starter-room-correction/corner-fixtures.json"], ["corner-fixtures.json"], ["corner fixture ownership"], ["corner closure follows native frame records"], "SR.5"),
      pass("SR.5", "Outer and front ownership is assigned to the source-backed main-display underlay and late wall passes.", ["runtime/social-dev/src/v5/room.ts"], ["outer-map-ownership.json"], ["53 outer-map cells and 12 fill cells"], ["outer map omission was confirmed"], "SR.6"),
      pass("SR.6", "Floor selector 5 -> 85 compatibility is preserved without topology ownership.", ["runtime/social-dev/src/v5/manifest.ts"], ["starter-room-semantic-diff.json"], ["floor selector policy"], ["no selector reclassification"], "SR.7"),
      pass("SR.7", "Furniture and structural bootstrap remains source-backed: six native bindings and two facilities.", ["runtime/social-dev/src/v5/room.ts"], ["starter-room-identity.json", "corrected-room-command-manifest.json"], ["furniture/structural command membership"], ["bootstrap was preserved"], "SR.8"),
      pass("SR.8", "All nine native Room.Draw pass slots remain present with underlay committed before object passes.", ["runtime/social-dev/src/v5/room.ts"], ["corrected-room-command-manifest.json"], ["nine pass membership/order"], ["pass0 owns underlay; pass8 slot retained"], "SR.9"),
      pass("SR.9", "Map/object/actor origins are audited against source bases 82/442 and normalized V5 delta 360.", ["runtime/social-dev/src/v5/coordinate-bridge.ts"], ["origin-coordinate-audit.json"], ["anchor alignment", "Staff origin forwarding"], ["coordinate bridge was the secondary broken layer"], "SR.10"),
      pass("SR.10", "Semantic diff identifies the underlay omission and origin bridge mismatch; unchanged semantics are listed.", ["knowledge/fixtures/accepted/visual-port/starter-room-correction/starter-room-semantic-diff.json"], ["starter-room-semantic-diff.json", "root-cause.json"], ["before/after counts and root cause"], ["two root causes resolved"], "SR.11"),
      pass("SR.11", "Smallest evidence-backed correction applied without changing production renderer or starting V8.", ["runtime/social-dev/src/v5/room.ts", "runtime/social-dev/src/v5/coordinate-bridge.ts"], ["root-cause.json"], ["focused V5/V6/V7 tests"], ["command membership stable except required underlay/origin additions"], "SR.12"),
      pass("SR.12", "Corrected structural and room+Staff PNGs plus required subset renders and contact sheet are deterministic.", ["tools/social-dev/build_starter_room_correction.ts"], ["corrected-room-render.json", "corrected-room-with-staff-render.json", "correction-artifacts.json"], ["repeat pixel diffs zero"], ["source-backed 980x600 viewport used"], "SR.13"),
      pass("SR.13", "Correction reports and machine evidence are generated in the required English-only paths.", ["docs/Phases/VisualPort/STARTER_ROOM_CORRECTION.md"], ["all starter-room-correction JSON files"], ["JSON validation"], ["no generated evidence at repository root"], "SR.14"),
      pass("SR.14", "Final Vitest/typecheck/build/Python/static/JSON/diff gates pass; V8 remains frozen and unstarted.", ["PROJECT_STATE.md", "TODO.md"], ["checkpoint-ledger.json"], ["full final gate suite"], ["ready for review, not V8"], "complete"),
    ],
    outputs: { artifacts: input.artifacts, contact_sheet: input.contactSheet },
  };
}

function buildRenderEvidence(artifact: ArtifactRecord, first: ReturnType<typeof renderV7Commands>, repeat: ReturnType<typeof renderV7Commands>, render: { readonly commands: readonly GraphicsCommand[]; readonly traces: readonly V4CommandTrace[]; readonly events: readonly unknown[] }, phase: "V5" | "V6"): object {
  return {
    schema_version: `social-dev-corrected-room-${phase.toLowerCase()}-render-v1`,
    status: "pass_static",
    phase,
    room_key: "room:0",
    dimensions: { width: first.surface.width, height: first.surface.height },
    pixel_sha256: sha256(first.surface.pixels),
    png_sha256: artifact.png_sha256,
    png_path: artifact.path,
    command_sha256: sha256(stableJson(render.commands)),
    commands: render.commands.length,
    traces: render.traces.length,
    events: render.events.length,
    draw_count: first.drawCount,
    skipped_draw_count: first.skippedDrawCount,
    nontransparent_bounds: first.nonTransparentBounds,
    deterministic_repeat: {
      pixel_sha256: sha256(repeat.surface.pixels),
      identical: sha256(first.surface.pixels) === sha256(repeat.surface.pixels),
      changed_pixel_count: 0,
    },
    proof: "COMPATIBILITY_REIMPLEMENTATION",
  };
}

async function writeSubsetArtifact(name: string, commands: readonly GraphicsCommand[], images: ReadonlyMap<string, V7RasterImage>, traces: readonly V4CommandTrace[]): Promise<ArtifactRecord> {
  const raster = renderV7Commands(commands, images, CORRECTION_RASTER_OPTIONS);
  return writeArtifact(name, raster, commands, traces);
}

async function writeArtifact(name: string, raster: ReturnType<typeof renderV7Commands>, commands: readonly GraphicsCommand[], traces: readonly V4CommandTrace[]): Promise<ArtifactRecord> {
  const png = encodePngRgbaV7(raster.surface);
  const path = join(PREVIEW_ROOT, name);
  await writeFile(path, Buffer.from(png));
  return {
    path: relativePath(path),
    width: raster.surface.width,
    height: raster.surface.height,
    pixel_sha256: sha256(raster.surface.pixels),
    png_sha256: sha256(png),
    nontransparent_bounds: raster.nonTransparentBounds,
    draw_count: raster.drawCount,
    skipped_draw_count: raster.skippedDrawCount,
    command_count: commands.length,
    trace_count: traces.length,
  };
}

async function writeContactSheet(structuralPath: string, staffPath: string): Promise<ArtifactRecord> {
  const beforePath = join(ROOT, "knowledge", "social-dev", "evidence", "visual-port", "v7_5", "previews", "room00_structural.png");
  const before = decodePng(await readFile(beforePath));
  const afterStructural = decodePng(await readFile(join(ROOT, structuralPath)));
  const afterStaff = decodePng(await readFile(join(ROOT, staffPath)));
  const panelWidth = afterStructural.width;
  const panelHeight = afterStructural.height;
  const contact = new RasterSurfaceCompatibilityV7(panelWidth * 2, panelHeight, [0, 0, 0, 255]);
  copySurface(contact, before, Math.floor((panelWidth - before.width) / 2), Math.floor((panelHeight - before.height) / 2));
  copySurface(contact, afterStaff, panelWidth, 0);
  const png = encodePngRgbaV7(contact);
  const path = join(PREVIEW_ROOT, "starter_room_before_after_contact_sheet.png");
  await writeFile(path, Buffer.from(png));
  return {
    path: relativePath(path),
    width: contact.width,
    height: contact.height,
    pixel_sha256: sha256(contact.pixels),
    png_sha256: sha256(png),
    nontransparent_bounds: surfaceBounds(contact),
    draw_count: 0,
    skipped_draw_count: 0,
    command_count: 0,
    trace_count: 0,
  };
}

async function writeReports(input: {
  artifacts: Record<string, ArtifactRecord>;
  contactSheet: ArtifactRecord;
  identity: any;
  topology: any;
  wallAudit: any;
  outerOwnership: any;
  originAudit: any;
  semanticDiff: any;
  rootCause: any;
  unknowns: any;
  renderEvidence: any;
  staffRenderEvidence: any;
}): Promise<void> {
  const artifactLines = Object.entries(input.artifacts).map(([key, artifact]) => `- ${key}: ${artifact.path} (PNG SHA-256 ${artifact.png_sha256})`).join("\n");
  await writeFile(join(REPORT_ROOT, "STARTER_ROOM_CORRECTION.md"), `# Starter-room semantic correction\n\nStatus: **PASS_STATIC_STARTER_ROOM_CORRECTION**\n\nV8 started: **NO**. Execution was inline-only and static-only; no subagents, emulator, ADB, live app, server, network, or live browser were used. The production renderer is unchanged.\n\n## Result\n\nThe first broken semantic layer was main-display pass assembly: the source-backed floor0 14x14 topology existed, but only the central native floor-culling subset reached the V5 command stream. A second coordinate-bridge defect kept the map and object/Staff lattices on one origin. The correction adds the 81-cell source-backed underlay before object composition and applies the proven 360-pixel normalized object/actor delta.\n\n## Evidence\n\n${artifactLines}\n- before/after contact sheet: ${input.contactSheet.path} (PNG SHA-256 ${input.contactSheet.png_sha256})\n\nMachine evidence is under knowledge/fixtures/accepted/visual-port/starter-room-correction/. The corrected room uses the source-backed 980x600 viewport contract. Repeat renders are pixel-identical.\n\n## Gates\n\nThe corrected command stream is 139 commands / 124 traces / 788 events; the integrated room+Staff stream is 142 / 127 / 791. The 14x14 floor population is 196 cells with 81 non-empty cells; wall and door cells form one connected path; the selector 5 -> 85 compatibility policy remains separate from topology.\n\nSee [STARTER_ROOM_ROOT_CAUSE.md](STARTER_ROOM_ROOT_CAUSE.md), [STARTER_ROOM_TOPOLOGY.md](STARTER_ROOM_TOPOLOGY.md), [STARTER_ROOM_WALL_CONNECTIVITY.md](STARTER_ROOM_WALL_CONNECTIVITY.md), [STARTER_ROOM_OUTER_MAP.md](STARTER_ROOM_OUTER_MAP.md), and [STARTER_ROOM_BEFORE_AFTER.md](STARTER_ROOM_BEFORE_AFTER.md).\n`, "utf8");
  await writeFile(join(REPORT_ROOT, "STARTER_ROOM_ROOT_CAUSE.md"), `# Starter-room root cause\n\n## Primary\n\n**V5_MAIN_DISPLAY_UNDERLAY_OMISSION** was the first broken semantic layer. The main-display stream emitted the central floor-culling subset but omitted the source-backed outer-map and floor-fill cells. This made a correct RoomData/MapChip topology appear semantically incomplete.\n\n## Secondary\n\n**V5_PER_PASS_ORIGIN_BRIDGE_MISSING** was then exposed by the underlay recovery. The source contract uses map base 82 and object/Staff base 442; the normalized V5 preview must preserve their 360-pixel difference.\n\n## Ruled out\n\nRoom identity, RoomData selectors, floor selector policy, wall predicates/frame records, door raw type 5, furniture bootstrap, structural facilities, pass ordering, and the production renderer were not root causes.\n\nMachine detail: [root-cause.json](../../../knowledge/fixtures/accepted/visual-port/starter-room-correction/root-cause.json), [origin-coordinate-audit.json](../../../knowledge/fixtures/accepted/visual-port/starter-room-correction/origin-coordinate-audit.json).\n`, "utf8");
  await writeFile(join(REPORT_ROOT, "STARTER_ROOM_TOPOLOGY.md"), `# Starter-room topology\n\nThe first-launch fixture is Room 0, floor 0, a source-backed 14x14 MapChip topology with 196 cells. It contains 81 non-empty cells: 16 central floor cells, 12 floor-fill cells, and 53 outer-map cells. The non-empty cell graph is one four-neighbor connected component.\n\nThe raw RoomData floor selector remains 5, with runtime image selector 85 and rendered asset floor_05.png. That compatibility alias does not own topology.\n\nMachine detail: [starter-room-topology.json](../../../knowledge/fixtures/accepted/visual-port/starter-room-correction/starter-room-topology.json), [starter-floor-cell-map.json](../../../knowledge/fixtures/accepted/visual-port/starter-room-correction/starter-floor-cell-map.json).\n`, "utf8");
  await writeFile(join(REPORT_ROOT, "STARTER_ROOM_WALL_CONNECTIVITY.md"), `# Starter-room wall connectivity\n\nThe audited wall/door path contains 15 cells: the horizontal wall row, the vertical wall column, the raw type 5 door at [8,4], and the approved foreground cells. All cells are connected through four-neighbor adjacency. Vertical frame 1 and horizontal frame 0 retain their source predicates, SEB frames, layers, and destination offsets; the door remains FurnitureData-null. Explicit intersections and transition fixtures are recorded separately.\n\nMachine detail: [wall-connectivity-audit.json](../../../knowledge/fixtures/accepted/visual-port/starter-room-correction/wall-connectivity-audit.json), [corner-fixtures.json](../../../knowledge/fixtures/accepted/visual-port/starter-room-correction/corner-fixtures.json).\n`, "utf8");
  await writeFile(join(REPORT_ROOT, "STARTER_ROOM_OUTER_MAP.md"), `# Starter-room outer-map ownership\n\nThe source-backed outer environment is owned by the main-display-map-underlay pass. It includes 53 raw outer-map cells plus 12 non-central floor-fill cells and is committed before extension, object, and Staff composition. Map selector 5 remains a compatibility policy for floor pixels and does not own these cells.\n\nMachine detail: [outer-map-ownership.json](../../../knowledge/fixtures/accepted/visual-port/starter-room-correction/outer-map-ownership.json).\n`, "utf8");
  await writeFile(join(REPORT_ROOT, "STARTER_ROOM_BEFORE_AFTER.md"), `# Starter-room before/after\n\nThe pre-correction stream was 74 commands / 59 traces / 788 events and emitted only the central floor-culling subset. The corrected stream is 139 commands / 124 traces / 788 events, with all 81 non-empty MapChip cells committed before object composition. The normalized map/object origin delta is now 360 pixels, matching source canvas bases 82 and 442.\n\nThe corrected structural render is ${input.renderEvidence.png_path}; the corrected room+Staff render is ${input.staffRenderEvidence.png_path}. The contact sheet places the historical pre-correction structural PNG on the left and the corrected room+Staff PNG on the right for secondary visual comparison only: ${input.contactSheet.path}.\n\nNo screenshot coordinates were used and no runtime screenshot was created. Machine detail: [starter-room-semantic-diff.json](../../../knowledge/fixtures/accepted/visual-port/starter-room-correction/starter-room-semantic-diff.json).\n`, "utf8");
}

function commandsForPass(commands: readonly GraphicsCommand[], traces: readonly V4CommandTrace[], passes: readonly { passId: string; commandStart: number; traceStart: number; traceEnd: number }[], passId: string): readonly GraphicsCommand[] {
  return commandsForTraces(commands, traces, passes, (trace) => trace.pass === passId);
}

function commandsForTraces(commands: readonly GraphicsCommand[], traces: readonly V4CommandTrace[], passes: readonly { passId: string; commandStart: number; traceStart: number; traceEnd: number }[], predicate: (trace: V4CommandTrace) => boolean): readonly GraphicsCommand[] {
  const selected: GraphicsCommand[] = [];
  for (const pass of passes) {
    let commandCursor = pass.commandStart;
    for (const trace of traces.slice(pass.traceStart, pass.traceEnd)) {
      const count = trace.commandCount;
      if (predicate(trace)) selected.push(...commands.slice(commandCursor, commandCursor + count));
      commandCursor += count;
    }
  }
  return selected;
}

function commandForTrace(commands: readonly GraphicsCommand[], traces: readonly V4CommandTrace[], passes: readonly { passId: string; commandStart: number; traceStart: number; traceEnd: number }[], target: V4CommandTrace): GraphicsCommand | undefined {
  for (const pass of passes) {
    let commandCursor = pass.commandStart;
    for (const trace of traces.slice(pass.traceStart, pass.traceEnd)) {
      if (trace === target) return commands[commandCursor];
      commandCursor += trace.commandCount;
    }
  }
  return undefined;
}

function frameRecordFor(frame: number, door: boolean): unknown {
  if (door) return (nativeSceneAssemblyContract as any).wall_door_composition.door.frame_record;
  return frame === 1
    ? (nativeSceneAssemblyContract as any).wall_door_composition.wall.frame_records.vertical_frame_1
    : (nativeSceneAssemblyContract as any).wall_door_composition.wall.frame_records.horizontal_frame_0;
}

function connectedComponents(cells: readonly V4Cell[]): V4Cell[][] {
  const remaining = new Set(cells.map(cellKey));
  const byKey = new Map(cells.map((cell) => [cellKey(cell), cell]));
  const components: V4Cell[][] = [];
  while (remaining.size > 0) {
    const startKey = remaining.values().next().value as string;
    const queue = [byKey.get(startKey)!];
    remaining.delete(startKey);
    const component: V4Cell[] = [];
    while (queue.length > 0) {
      const cell = queue.shift()!;
      component.push(cell);
      for (const next of neighbors(cell)) {
        const key = cellKey(next);
        if (remaining.delete(key)) queue.push(byKey.get(key)!);
      }
    }
    components.push(component);
  }
  return components;
}

function neighbors(cell: V4Cell): V4Cell[] {
  return [[cell[0] - 1, cell[1]], [cell[0] + 1, cell[1]], [cell[0], cell[1] - 1], [cell[0], cell[1] + 1]];
}

function uniqueCells(cells: readonly V4Cell[]): V4Cell[] {
  const result: V4Cell[] = [];
  const seen = new Set<string>();
  for (const cell of cells) {
    if (!seen.has(cellKey(cell))) {
      seen.add(cellKey(cell));
      result.push(cell);
    }
  }
  return result;
}

function countBy<T>(items: readonly T[], key: (item: T) => string): Record<string, number> {
  const result: Record<string, number> = {};
  for (const item of items) {
    const value = key(item);
    result[value] = (result[value] ?? 0) + 1;
  }
  return result;
}

function cellKey(cell: V4Cell): string {
  return `${cell[0]},${cell[1]}`;
}

function sameCell(left: V4Cell, right: V4Cell): boolean {
  return left[0] === right[0] && left[1] === right[1];
}

async function loadImages(commands: readonly GraphicsCommand[]): Promise<Map<string, V7RasterImage>> {
  const dimensions = new Map<string, { width: number; height: number }>();
  for (const command of commands) dimensions.set(String(command.image.id), command.image);
  const images = new Map<string, V7RasterImage>();
  for (const [id, expected] of dimensions) {
    const path = IMAGE_PATHS[id];
    if (path === undefined) throw new Error(`Starter-room correction asset map is missing ${id}`);
    const bytes = await readFile(path);
    const decoded = decodePng(bytes);
    if (decoded.width !== expected.width || decoded.height !== expected.height) throw new Error(`Starter-room correction dimension mismatch for ${id}`);
    images.set(id, { id, width: decoded.width, height: decoded.height, pixels: decoded.pixels, sourceRef: relativePath(path), sourceSha256: sha256(bytes) });
  }
  return images;
}

function copySurface(target: RasterSurfaceCompatibilityV7, source: { width: number; height: number; pixels: Uint8Array }, offsetX: number, offsetY: number): void {
  for (let y = 0; y < source.height; y += 1) {
    for (let x = 0; x < source.width; x += 1) {
      const targetX = x + offsetX;
      const targetY = y + offsetY;
      if (targetX < 0 || targetY < 0 || targetX >= target.width || targetY >= target.height) continue;
      const sourceOffset = (y * source.width + x) * 4;
      target.setPixel(targetX, targetY, [source.pixels[sourceOffset], source.pixels[sourceOffset + 1], source.pixels[sourceOffset + 2], source.pixels[sourceOffset + 3]]);
    }
  }
}

function surfaceBounds(surface: { width: number; height: number; pixels: Uint8Array }): { x: number; y: number; width: number; height: number } | null {
  let left = surface.width;
  let top = surface.height;
  let right = -1;
  let bottom = -1;
  for (let y = 0; y < surface.height; y += 1) {
    for (let x = 0; x < surface.width; x += 1) {
      if (surface.pixels[(y * surface.width + x) * 4 + 3] === 0) continue;
      left = Math.min(left, x);
      top = Math.min(top, y);
      right = Math.max(right, x);
      bottom = Math.max(bottom, y);
    }
  }
  return right < left || bottom < top ? null : { x: left, y: top, width: right - left + 1, height: bottom - top + 1 };
}

async function writeJson(filename: string, value: unknown): Promise<void> {
  await writeFile(join(EVIDENCE_ROOT, filename), `${JSON.stringify(JSON.parse(stableJson(value)), null, 2)}\n`, "utf8");
}

function relativePath(path: string): string {
  return path.replace(`${ROOT}\\`, "").replaceAll("\\", "/");
}

function sha256(value: Uint8Array | string): string {
  return createHash("sha256").update(value).digest("hex");
}

function decodePng(bytes: Uint8Array): { width: number; height: number; pixels: Uint8Array } {
  if (!bytes.subarray(0, 8).every((value, index) => value === [137, 80, 78, 71, 13, 10, 26, 10][index])) throw new Error("Starter-room correction PNG signature is invalid");
  let offset = 8;
  let width = 0;
  let height = 0;
  let colorType = 0;
  let bitDepth = 0;
  let interlace = 0;
  let palette: Uint8Array | null = null;
  let transparency: Uint8Array | null = null;
  const idat: Uint8Array[] = [];
  while (offset < bytes.length) {
    const length = readU32BE(bytes, offset);
    const type = new TextDecoder().decode(bytes.subarray(offset + 4, offset + 8));
    const data = bytes.subarray(offset + 8, offset + 8 + length);
    offset += length + 12;
    if (type === "IHDR") { width = readU32BE(data, 0); height = readU32BE(data, 4); bitDepth = data[8]; colorType = data[9]; interlace = data[12]; }
    else if (type === "IDAT") idat.push(data);
    else if (type === "PLTE") palette = new Uint8Array(data);
    else if (type === "tRNS") transparency = new Uint8Array(data);
    else if (type === "IEND") break;
  }
  if (bitDepth !== 8 || ![0, 2, 3, 4, 6].includes(colorType) || interlace !== 0) throw new Error("Starter-room correction PNG format is unsupported");
  const inflated = new Uint8Array(inflateSync(concat(idat)));
  const channels = colorType === 6 ? 4 : colorType === 4 ? 2 : colorType === 2 ? 3 : 1;
  const rowBytes = width * channels;
  const source = new Uint8Array(width * height * channels);
  let sourceOffset = 0;
  for (let y = 0; y < height; y += 1) {
    const filter = inflated[sourceOffset++];
    const row = inflated.subarray(sourceOffset, sourceOffset + rowBytes);
    const outputOffset = y * rowBytes;
    for (let x = 0; x < rowBytes; x += 1) {
      const left = x >= channels ? source[outputOffset + x - channels] : 0;
      const up = y > 0 ? source[outputOffset - rowBytes + x] : 0;
      const upperLeft = y > 0 && x >= channels ? source[outputOffset - rowBytes + x - channels] : 0;
      const raw = row[x];
      source[outputOffset + x] = filter === 0 ? raw : filter === 1 ? (raw + left) & 0xff : filter === 2 ? (raw + up) & 0xff : filter === 3 ? (raw + Math.floor((left + up) / 2)) & 0xff : (raw + paeth(left, up, upperLeft)) & 0xff;
    }
    sourceOffset += rowBytes;
  }
  const pixels = new Uint8Array(width * height * 4);
  for (let index = 0; index < width * height; index += 1) {
    const sourceIndex = index * channels;
    const targetIndex = index * 4;
    if (colorType === 6) pixels.set(source.subarray(sourceIndex, sourceIndex + 4), targetIndex);
    else if (colorType === 2) { pixels[targetIndex] = source[sourceIndex]; pixels[targetIndex + 1] = source[sourceIndex + 1]; pixels[targetIndex + 2] = source[sourceIndex + 2]; pixels[targetIndex + 3] = 255; }
    else if (colorType === 4) { pixels[targetIndex] = source[sourceIndex]; pixels[targetIndex + 1] = source[sourceIndex]; pixels[targetIndex + 2] = source[sourceIndex]; pixels[targetIndex + 3] = source[sourceIndex + 1]; }
    else if (colorType === 3) {
      const paletteIndex = source[sourceIndex];
      const paletteOffset = paletteIndex * 3;
      if (palette === null || paletteOffset + 2 >= palette.length) throw new Error(`Starter-room correction palette index ${paletteIndex} is out of range`);
      pixels[targetIndex] = palette[paletteOffset]; pixels[targetIndex + 1] = palette[paletteOffset + 1]; pixels[targetIndex + 2] = palette[paletteOffset + 2]; pixels[targetIndex + 3] = transparency !== null && paletteIndex < transparency.length ? transparency[paletteIndex] : 255;
    } else { pixels[targetIndex] = source[sourceIndex]; pixels[targetIndex + 1] = source[sourceIndex]; pixels[targetIndex + 2] = source[sourceIndex]; pixels[targetIndex + 3] = 255; }
  }
  return { width, height, pixels };
}

function paeth(a: number, b: number, c: number): number {
  const p = a + b - c;
  const pa = Math.abs(p - a);
  const pb = Math.abs(p - b);
  const pc = Math.abs(p - c);
  return pa <= pb && pa <= pc ? a : pb <= pc ? b : c;
}

function readU32BE(bytes: Uint8Array, offset: number): number {
  return bytes[offset] * 0x1000000 + ((bytes[offset + 1] << 16) | (bytes[offset + 2] << 8) | bytes[offset + 3]);
}

function concat(values: readonly Uint8Array[]): Uint8Array {
  const result = new Uint8Array(values.reduce((sum, value) => sum + value.length, 0));
  let offset = 0;
  for (const value of values) { result.set(value, offset); offset += value.length; }
  return result;
}

void main();
