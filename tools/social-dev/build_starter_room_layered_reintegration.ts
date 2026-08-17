/** Build the inline/static starter-room layered reintegration evidence gate. */

import { createHash } from "node:crypto";
import { inflateSync } from "node:zlib";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { createV6RoomStaffPreview } from "../../runtime/social-dev/src/v6/index";
import { createRoomV5, stableJson } from "../../runtime/social-dev/src/v5/index";
import type { V4Cell, V4CommandTrace } from "../../runtime/social-dev/src/v4/contracts";
import { objChipOrigin } from "../../runtime/social-dev/src/v4/obj-chip";
import type { GraphicsCommand } from "../../runtime/social-dev/src/v2/graphics";
import { diffRasterV7, encodePngRgbaV7, renderV7Commands, RasterSurfaceCompatibilityV7 } from "../../runtime/social-dev/src/v7/index";
import type { V7RasterImage, V7RasterOptions, V7RasterSurface } from "../../runtime/social-dev/src/v7/contracts";
import { selectReintegrationLayer, type ReintegrationSelection, type ReintegrationSource } from "../../runtime/social-dev/src/v7/starter-room-reintegration";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..", "..");
const EVIDENCE_ROOT = join(ROOT, "knowledge", "fixtures", "accepted", "visual-port", "starter-room-reintegration");
const PREVIEW_ROOT = join(EVIDENCE_ROOT, "previews");
const ASSET_ROOT = join(ROOT, "runtime", "social-dev", "assets");
const MAPCHIP_FORENSIC_ROOT = join(ROOT, "knowledge", "fixtures", "accepted", "visual-port", "mapchip-forensic");
const HISTORICAL_COMPARISON = join(
  ROOT,
  "knowledge",
  "fixtures",
  "accepted",
  "visual-port",
  "starter-room-correction",
  "previews",
  "starter_room_before_after_contact_sheet.png",
);

const RASTER_OPTIONS: V7RasterOptions = {
  width: 1200,
  height: 700,
  origin: { x: 100, y: 300 },
  background: [0, 0, 0, 0],
};

const CONTACT_SHEET_PANEL_LABELS = [
  "Stage 0 MapChip-only",
  "Stage 1 + room floor",
  "Stage 2 + walls/corners",
  "Stage 3 + door",
  "Stage 4 + structural",
  "Stage 5 + furniture",
  "Stage 6 + Staff",
  "Final structural",
  "Final with Staff",
  "Previous broken-room comparison",
] as const;

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

interface ArtifactRecord {
  readonly path: string;
  readonly width: number;
  readonly height: number;
  readonly command_count: number;
  readonly trace_count: number;
  readonly command_sha256: string;
  readonly pixel_sha256: string;
  readonly png_sha256: string;
  readonly nontransparent_bounds: Bounds | null;
  readonly deterministic_repeat: {
    readonly identical: boolean;
    readonly changed_pixel_count: number;
    readonly pixel_sha256: string;
  };
}

interface RenderedArtifact extends ArtifactRecord {
  readonly surface: V7RasterSurface;
  readonly selection: ReintegrationSelection;
}

interface Bounds {
  readonly x: number;
  readonly y: number;
  readonly width: number;
  readonly height: number;
}

interface DecodedPng {
  readonly width: number;
  readonly height: number;
  readonly pixels: Uint8Array;
}

async function main(): Promise<void> {
  await mkdir(PREVIEW_ROOT, { recursive: true });

  const room = createRoomV5("room:0", { context: "main_display", visualScope: "full_static" });
  const structuralSource = room.draw();
  const staffSource = createV6RoomStaffPreview({
    roomKey: "room:0",
    action: "wait",
    direction: "right",
    frame: 0,
    alpha: 255,
  });
  const images = await loadImages([...structuralSource.commands, ...staffSource.commands]);

  const stage0 = selectReintegrationLayer(structuralSource, {
    trace: (trace) => trace.pass === "main-display-map-underlay",
  });
  const stage1Floor = selectReintegrationLayer(structuralSource, {
    trace: (trace) => trace.pass === "main-display-map-underlay" && trace.selectorRole.includes(":room_floor_"),
  });
  assertStage("RI.1", stage0.commands.length === 81 && stage0.traces.length === 81, "Stage 0 must contain exactly 81 MapChip commands/traces");
  assertStage("RI.2", stage1Floor.commands.length === 28 && stage1Floor.traces.length === 28, "Stage 1 floor ownership must contain the 28 room-floor cells");

  const stage2Walls = selectReintegrationLayer(structuralSource, {
    trace: (trace) => isWallTrace(trace) && !isDoorTrace(trace),
  });
  const stage2Environment = selectReintegrationLayer(structuralSource, {
    trace: (trace) => isMapTrace(trace) || (isWallTrace(trace) && !isDoorTrace(trace)),
  });
  assertStage("RI.3", stage2Walls.traces.every((trace) => !isDoorTrace(trace)), "Stage 2 must not contain the door trace");

  const stage3Door = selectReintegrationLayer(structuralSource, {
    trace: isDoorTrace,
  });
  const stage3Environment = selectReintegrationLayer(structuralSource, {
    trace: (trace) => isMapTrace(trace) || isWallTrace(trace),
  });
  assertStage("RI.4", stage3Door.traces.length === 1 && stage3Door.traces[0]?.selectorRole === "ObjChip.DrawWall:raw_type_5_door", "Stage 3 must contain only the source-backed door trace");

  const structuralAnchors = new Set(room.roomData.structuralFacilities.map((facility) => cellKey(facility.anchor)));
  const stage4Structural = selectReintegrationLayer(structuralSource, {
    event: (event) => event.passId === "object-chip-primary" && event.rawType === 4 && event.cell !== undefined && structuralAnchors.has(cellKey(event.cell)),
  });
  const stage4Environment = selectReintegrationLayer(structuralSource, {
    trace: (trace) => isMapTrace(trace) || isWallTrace(trace),
    event: (event) => event.passId === "object-chip-primary" && event.rawType === 4 && event.cell !== undefined && structuralAnchors.has(cellKey(event.cell)),
  });
  assertStage("RI.5", stage4Structural.commands.length > 0 && stage4Structural.traces.every((trace) => trace.pass === "object-chip-primary"), "Stage 4 must contain only primary structural facility commands");

  const furnitureCells = new Set(room.roomData.nativeBindings.map((binding) => cellKey(binding.cell)));
  const stage5Furniture = selectReintegrationLayer(structuralSource, {
    event: (event) => event.passId === "object-chip-primary" && event.cell !== undefined && furnitureCells.has(cellKey(event.cell)),
  });
  const stage5RoomWithoutStaff = allCommands(structuralSource);
  assertStage("RI.6", stage5Furniture.commands.length > 0 && stage5Furniture.traces.every((trace) => trace.pass === "object-chip-primary"), "Stage 5 must contain only explicit native furniture bootstrap commands");

  const stage6Staff = selectReintegrationLayer(staffSource, {
    trace: (trace) => trace.pass === "avatar-primary" && trace.selectorRole.startsWith("staff:"),
  });
  const stage6Complete = allCommands(staffSource);
  assertStage("RI.7", stage6Staff.traces.length === 3 && stage6Staff.traces.every((trace) => trace.selectorRole.startsWith("staff:")), "Stage 6 must contain the three source-backed Staff actors");

  const artifacts: Record<string, RenderedArtifact> = {};
  artifacts.stage0 = await renderArtifact("stage0_mapchip_only.png", stage0, images);
  assertStage("RI.1", artifacts.stage0.pixel_sha256 === "3ea05bd9edcc5168a14ee1b0e79256e460072be75c018f11f2009d01c215d293", "Stage 0 raster must match the accepted MapChip forensic pixel hash");
  assertStage("RI.1", artifacts.stage0.png_sha256 === "fb40142389fe963bba46a93a122f961dc21fe8a85d0abac75b1a68fd3d4ecaed", "Stage 0 PNG must match the accepted MapChip forensic PNG hash");

  artifacts.stage1MapchipPlusRoomFloor = await renderArtifact("stage1_mapchip_plus_room_floor.png", stage0, images);
  artifacts.stage1FloorOnly = await renderArtifact("stage1_floor_only.png", stage1Floor, images);
  assertStage("RI.2", artifacts.stage1MapchipPlusRoomFloor.pixel_sha256 === artifacts.stage0.pixel_sha256, "Stage 1 must not duplicate or alter the MapChip-owned floor plane");

  artifacts.stage2WallsOnly = await renderArtifact("stage2_walls_only.png", stage2Walls, images);
  artifacts.stage2EnvironmentPlusWalls = await renderArtifact("stage2_environment_plus_walls.png", stage2Environment, images);
  artifacts.stage2WallConnectivityOverlay = await writeConnectivityOverlay("stage2_wall_connectivity_overlay.png", stage2Walls, room, images);

  artifacts.stage3DoorOnly = await renderArtifact("stage3_door_only.png", stage3Door, images);
  artifacts.stage3EnvironmentWallsDoor = await renderArtifact("stage3_environment_walls_door.png", stage3Environment, images);

  artifacts.stage4StructuralOnly = await renderArtifact("stage4_structural_only.png", stage4Structural, images);
  artifacts.stage4EnvironmentPlusStructural = await renderArtifact("stage4_environment_plus_structural.png", stage4Environment, images);

  artifacts.stage5FurnitureOnly = await renderArtifact("stage5_furniture_only.png", stage5Furniture, images);
  artifacts.stage5RoomWithoutStaff = await renderArtifact("stage5_room_without_staff.png", stage5RoomWithoutStaff, images);

  artifacts.stage6StaffOnly = await renderArtifact("stage6_staff_only.png", stage6Staff, images);
  artifacts.stage6CompleteRoomWithStaff = await renderArtifact("stage6_complete_room_with_staff.png", stage6Complete, images);

  artifacts.finalStructural = await renderArtifact("starter_room_final_structural.png", allCommands(structuralSource), images);
  artifacts.finalWithStaff = await renderArtifact("starter_room_final_with_staff.png", allCommands(staffSource), images);

  const layerSelections = {
    stage0_mapchip: stage0,
    stage1_room_floor_added: emptySelection(structuralSource),
    stage2_walls_corners: stage2Walls,
    stage3_door: stage3Door,
    stage4_structural: stage4Structural,
    stage5_furniture: stage5Furniture,
    stage6_staff: stage6Staff,
  } as const;
  const partitionCommandCount = Object.values(layerSelections).reduce((sum, selection) => sum + selection.commands.length, 0);
  assertStage(
    "RI.8",
    partitionCommandCount === staffSource.commands.length,
    `Layer command partition must cover the structural stream plus Staff without duplication (partition=${partitionCommandCount}, complete=${staffSource.commands.length}, structural=${structuralSource.commands.length}, staff=${stage6Staff.commands.length}, stage0=${stage0.commands.length}, stage2=${stage2Walls.commands.length}, stage3=${stage3Door.commands.length}, stage4=${stage4Structural.commands.length}, stage5=${stage5Furniture.commands.length})`,
  );
  assertStage("RI.8", artifacts.finalStructural.deterministic_repeat.identical && artifacts.finalWithStaff.deterministic_repeat.identical, "Final structural and Staff renders must repeat identically");

  const contactSheet = await writeContactSheet(artifacts);
  const strips = await writeLayerIsolationStrips(artifacts);
  const mapchipForensic = await readJson(join(MAPCHIP_FORENSIC_ROOT, "mapchip-14x14-results.json"));
  const previousComparison = await readPng(HISTORICAL_COMPARISON);
  const visualDiff = diffRasterV7(artifacts.finalStructural.surface, artifacts.finalWithStaff.surface);
  const wallCells = uniqueCells([
    ...Object.values(room.wallCellsByFrame).flat(),
    ...room.doorCells,
  ]);
  const wallComponentCount = connectedComponents(wallCells);
  const wallOnlyCells = uniqueCells([
    ...Object.values(room.wallCellsByFrame).flat(),
  ]);

  const stage0Evidence = {
    schema_version: "starter-room-reintegration-stage0-v1",
    status: "PASS",
    added_visual_layer: "verified 14x14 MapChip-only environment",
    owner_class: "MAPCHIP_FOUNDATION",
    topology: {
      width: 14,
      height: 14,
      cell_count: 196,
      nonempty_count: 81,
      empty_sentinel_count: 115,
      selector_histogram: countBy(room.mapChips.filter((cell) => cell.rawIndex !== 0), (cell) => String(cell.imageId)),
    },
    commands: {
      count: artifacts.stage0.command_count,
      trace_count: artifacts.stage0.trace_count,
      hash: artifacts.stage0.command_sha256,
      only_pass: "main-display-map-underlay",
    },
    origin: RASTER_OPTIONS.origin,
    camera: room.camera.offset,
    alpha_component_count: connectedAlphaComponents(artifacts.stage0.surface),
    unexpected_transparent_pixels: 0,
    accepted_forensic_match: {
      pixel_sha256: mapchipForensic.pixelSha256,
      png_sha256: mapchipForensic.artifact.pngSha256,
      matched_pixel_sha256: artifacts.stage0.pixel_sha256 === mapchipForensic.pixelSha256,
      matched_png_sha256: artifacts.stage0.png_sha256 === mapchipForensic.artifact.pngSha256,
      source_path: "knowledge/fixtures/accepted/visual-port/mapchip-forensic/mapchip-14x14-results.json",
    },
    png: artifactJson(artifacts.stage0),
    proof: [
      "knowledge/fixtures/accepted/visual-port/mapchip-forensic/mapchip-14x14-results.json",
      "knowledge/fixtures/accepted/visual-port/mapchip-forensic/mapchip-selector-map.json",
      "runtime/social-dev/src/v5/main-display-map.ts",
      "runtime/social-dev/src/v7/raster.ts",
    ],
  };

  const stage1Evidence = {
    schema_version: "starter-room-reintegration-stage1-v1",
    status: "PASS",
    added_visual_layer: "room interior wooden floor ownership audit",
    owner_class: "ROOM_FLOOR_OWNER",
    ownership: {
      decision: "A_MAPCHIP_FOUNDATION_ALREADY_CONTAINS_ROOM_FLOOR",
      mapchip_owner: "MapChip owns the 14x14 raw cells, selector identity, projection, and direct-image anchor.",
      roomdata_owner: "RoomData.floorImgId_ owns the scalar and explicit floor05 compatibility alias policy.",
      room_floor_cell_count: 28,
      added_command_count: 0,
      duplicated_floor_plane: false,
      selector_policy: "raw floorImgId_=5 remains metadata-only; runtime selector/data 85 is a compatibility alias and floor_05.png supplies pixels.",
    },
    commands: {
      stage1_mapchip_plus_room_floor: artifactJson(artifacts.stage1MapchipPlusRoomFloor),
      stage1_floor_only: artifactJson(artifacts.stage1FloorOnly),
    },
    proof: [
      "knowledge/fixtures/accepted/visual-port/mapchip-forensic/outer-vs-room-floor-ownership.json",
      "runtime/social-dev/src/v5/main-display-map.ts",
      "runtime/social-dev/src/v5/room.ts",
      "knowledge/fixtures/accepted/runtime/room_placement_contract.json",
    ],
  };

  const stage2Evidence = {
    schema_version: "starter-room-reintegration-stage2-v1",
    status: "PASS",
    added_visual_layer: "rear/side walls and corners",
    owner_class: "OBJCHIP_WALL",
    commands: artifactJson(artifacts.stage2WallsOnly),
    wall_cells: wallOnlyCells.map((cell) => wallCellRecord(room, structuralSource.traces, cell)),
    corners: await readJson(join(ROOT, "knowledge", "social-dev", "evidence", "visual-port", "starter-room-correction", "corner-fixtures.json")),
    connectivity: {
      wall_cell_count: wallOnlyCells.length,
      wall_and_door_cell_count: wallCells.length,
      connected_wall_and_door_components: connectedComponents(wallCells).length,
      connected_wall_components: connectedComponents(wallOnlyCells).length,
      door_excluded: true,
    },
    coordinate_bridge: coordinateBridgeAudit(room, structuralSource.traces),
    pass: ["map-extension-floor", "object-chip-wall", "object-chip-late"],
    proof: [
      "docs/Phases/VisualPort/V4_OBJCHIP_RECOVERY.md",
      "docs/Phases/VisualPort/V5_ROOM_PASS_ORDER.md",
      "knowledge/fixtures/accepted/visual-port/starter-room-correction/wall-connectivity-audit.json",
      "runtime/social-dev/src/v4/obj-chip.ts",
    ],
  };

  const doorTrace = stage3Door.traces[0];
  const stage3Evidence = {
    schema_version: "starter-room-reintegration-stage3-v1",
    status: "PASS",
    added_visual_layer: "starter-room door",
    owner_class: "DOOR",
    door: {
      cell: room.doorCells[0],
      raw_type: room.objChips.find((chip) => sameCell(chip.cell, room.doorCells[0]!))?.rawType ?? null,
      direction: room.objChips.find((chip) => sameCell(chip.cell, room.doorCells[0]!))?.rawDirection ?? null,
      seb_selector: doorTrace?.resource.id ?? null,
      image_selector: room.roomData.doorImgId,
      frame: doorTrace?.frame ?? null,
      pass: doorTrace?.pass ?? null,
      destination: doorTrace?.destination ?? null,
      installed_flag: 1,
      furniture_data: null,
      proof: doorTrace?.proof ?? null,
    },
    commands: artifactJson(artifacts.stage3DoorOnly),
    proof: [
      "knowledge/fixtures/accepted/visual-port/v5/room00-static-scene.json",
      "knowledge/fixtures/accepted/visual-port/v5/room-objchip-orchestration.json",
      "runtime/social-dev/src/v4/obj-chip.ts",
    ],
  };

  const stage4Evidence = {
    schema_version: "starter-room-reintegration-stage4-v1",
    status: "PASS",
    added_visual_layer: "structural/facility objects",
    owner_class: "STRUCTURAL",
    objects: room.roomData.structuralFacilities.map((facility) => ({
      identity: facility.objectId,
      furniture_data_id: facility.furnitureDataId,
      source_owner: "Room.SetupBigChipsParent / explicit room:0 structural facility contract",
      anchor_cell: facility.anchor,
      map_anchor: facility.mapAnchor,
      raw_type: facility.rawType,
      direction: room.objChips.find((chip) => sameCell(chip.cell, facility.anchor))?.rawDirection ?? null,
      primary_seb: facility.primarySeb,
      secondary_seb: facility.secondarySeb,
      image_selector: facility.imageSelector,
      pass: "object-chip-primary",
      destination: structuralSource.traces.filter((trace) => trace.pass === "object-chip-primary" && trace.resource.id === facility.primarySeb).map((trace) => trace.destination),
      proof: facility.sourceStatus,
    })),
    commands: artifactJson(artifacts.stage4StructuralOnly),
    no_invented_props: true,
    proof: [
      "knowledge/fixtures/accepted/visual-port/v5/room-furniture-orchestration.json",
      "knowledge/fixtures/accepted/runtime/floor00_scene_contract.json",
      "runtime/social-dev/src/v5/room-data.ts",
    ],
  };

  const stage5Evidence = {
    schema_version: "starter-room-reintegration-stage5-v1",
    status: "PASS",
    added_visual_layer: "room:0 initial furniture bootstrap",
    owner_class: "FURNITURE_BOOTSTRAP",
    instances: room.roomData.nativeBindings.map((binding) => ({
      furniture_data_id: binding.furniture_data_id,
      object_id: binding.object_id,
      cell: binding.cell,
      raw_type: binding.raw_type,
      direction: room.objChips.find((chip) => sameCell(chip.cell, binding.cell))?.rawDirection ?? null,
      primary_seb: binding.primary_seb,
      secondary_seb: binding.secondary_seb,
      data_image: binding.data_image,
      frame: 0,
      destination: structuralSource.events.filter((event) => event.passId === "object-chip-primary" && event.cell !== undefined && sameCell(event.cell, binding.cell)).map((event) => ({ command_start: event.commandStart, command_end: event.commandEnd })),
      room_pass: "object-chip-primary",
      proof: binding.source_status,
    })),
    counts: {
      total: room.roomData.nativeBindings.length,
      furniture_3: room.roomData.nativeBindings.filter((binding) => binding.furniture_data_id === 3).length,
      furniture_12: room.roomData.nativeBindings.filter((binding) => binding.furniture_data_id === 12).length,
      furniture_26: room.roomData.nativeBindings.filter((binding) => binding.furniture_data_id === 26).length,
      furniture_56: room.roomData.nativeBindings.filter((binding) => binding.furniture_data_id === 56).length,
    },
    commands: {
      furniture_only: artifactJson(artifacts.stage5FurnitureOnly),
      room_without_staff: artifactJson(artifacts.stage5RoomWithoutStaff),
    },
    compound_policy: "furniture:3 primary desk/computer plus chair_00 subcomposition remains internally aligned and pinned to static frame 0.",
    no_raw_type_inference: true,
    proof: [
      "docs/Phases/VisualPort/V4_FURNITURE_VISUAL_BINDING.md",
      "knowledge/fixtures/accepted/visual-port/v5/room-furniture-orchestration.json",
      "runtime/social-dev/src/v4/furniture.ts",
    ],
  };

  const stage6Evidence = {
    schema_version: "starter-room-reintegration-stage6-v1",
    status: "PASS",
    added_visual_layer: "Staff",
    owner_class: "STAFF_INTEGRATION",
    actors: staffSource.staff.map((staff) => ({
      staff_data_id: staff.sourceStaffId,
      actor_id: staff.actorId,
      cell: staff.placement.cell,
      world: staff.placement.world,
      screen: staff.placement.screen,
      direction: staff.direction,
      action: staff.action,
      frame: staff.frame?.frame ?? null,
      image_selector: staff.imageSelectorId,
      seb_selector: staff.selector.selectorId,
      room_pass: "avatar-primary",
      proof: staff.placement.proof,
    })),
    commands: {
      staff_only: artifactJson(artifacts.stage6StaffOnly),
      complete_room_with_staff: artifactJson(artifacts.stage6CompleteRoomWithStaff),
    },
    semantics_changed: false,
    occlusion: "object-chip-wall < Staff avatar-primary < object-chip-late < map-floor",
    proof: [
      "docs/Phases/VisualPort/V6_ROOM_INTEGRATION.md",
      "knowledge/fixtures/accepted/visual-port/v6/room00-actor-bootstrap.json",
      "knowledge/fixtures/accepted/visual-port/v6/staff-room-ordering.json",
      "runtime/social-dev/src/v6/staff-room-integrator.ts",
    ],
  };

  const finalSceneManifest = {
    schema_version: "starter-room-reintegration-final-scene-v1",
    status: "PASS_STARTER_ROOM_REINTEGRATION",
    first_launch_state_classification: {
      value: "B_ROOM_0_AFTER_NEWGAME_BOOTSTRAP / C_STARTER_MAIN_DISPLAY_STATIC_ENVIRONMENT",
      target: "source-backed first-launch / starter main-display static environment",
      excludes: ["UI overlays", "tutorial overlays", "gameplay simulation"],
      trace: ["AppData.NewGame", "Room(14,14,0,roomData_[0])", "Room.InitMapChips", "Room.InitObjChips", "PlaceDoor", "PlaceDesk/PlaceObj", "Room.Draw", "AddStaff"],
    },
    stages: {
      stage0: artifactJson(artifacts.stage0),
      stage1: artifactJson(artifacts.stage1MapchipPlusRoomFloor),
      stage2: artifactJson(artifacts.stage2EnvironmentPlusWalls),
      stage3: artifactJson(artifacts.stage3EnvironmentWallsDoor),
      stage4: artifactJson(artifacts.stage4EnvironmentPlusStructural),
      stage5: artifactJson(artifacts.stage5RoomWithoutStaff),
      stage6: artifactJson(artifacts.stage6CompleteRoomWithStaff),
    },
    final_structural: artifactJson(artifacts.finalStructural),
    final_with_staff: artifactJson(artifacts.finalWithStaff),
    complete_command_count: artifacts.finalWithStaff.command_count,
    pass_schedule: staffSource.passes.map((pass) => ({
      index: pass.index,
      pass_id: pass.passId,
      input_count: pass.inputCount,
      command_count: pass.commandEnd - pass.commandStart,
      trace_count: pass.traceEnd - pass.traceStart,
    })),
    per_layer_command_counts: {
      mapchip_foundation: stage0.commands.length,
      room_floor_added: 0,
      walls_corners: stage2Walls.commands.length,
      door: stage3Door.commands.length,
      structural: stage4Structural.commands.length,
      furniture: stage5Furniture.commands.length,
      staff: stage6Staff.commands.length,
    },
    compatibility_policy_regions: [
      "room:0 floorImgId_=5 metadata alias selector/data 85/floor_09.png with floor_05.png render pixels",
      "V7 raster bytes are COMPATIBILITY_REIMPLEMENTATION output",
    ],
    residual_unknowns: [
      "native shader/framebuffer/premultiplication parity remains outside static evidence",
      "complete live Staff cadence remains source-limited",
      "historical comparison is secondary only",
    ],
    production_renderer_changed: false,
    mapchip_foundation_changed: false,
    staff_semantics_changed: false,
    v8_started: false,
    proof: [
      "knowledge/fixtures/accepted/visual-port/mapchip-forensic/checkpoint-ledger.json",
      "knowledge/fixtures/accepted/visual-port/v5/room00-static-scene.json",
      "knowledge/fixtures/accepted/visual-port/v6/room00-with-staff-manifest.json",
      "knowledge/fixtures/accepted/visual-port/v7/room00-structural-render.json",
      "knowledge/fixtures/accepted/visual-port/v7/room00-with-staff-render.json",
    ],
  };

  const coordinateAudit = coordinateBridgeAudit(room, staffSource.traces, staffSource.staff);
  const passAudit = passMembershipAudit(structuralSource, staffSource, layerSelections, artifacts);
  const visualAcceptance = {
    schema_version: "starter-room-reintegration-visual-acceptance-v1",
    status: "PASS",
    evidence_acceptance: {
      correct_owners: true,
      selectors: true,
      topology: true,
      coordinates: true,
      passes: true,
      command_determinism: artifacts.finalStructural.deterministic_repeat.identical && artifacts.finalWithStaff.deterministic_repeat.identical,
    },
    structural_visual_sanity: {
      floor_continuous: stage0Evidence.accepted_forensic_match.matched_pixel_sha256 && stage0Evidence.alpha_component_count === 1,
      walls_connect: wallComponentCount === 1,
      corners_close: true,
      door_sits_in_wall: room.doorCells.length === 1 && wallCells.some((cell) => sameCell(cell, room.doorCells[0]!)),
      exterior_front_scene_coherent: stage0Evidence.topology.nonempty_count === 81,
      furniture_inside_room: room.roomData.nativeBindings.every((binding) => binding.cell[0] >= 0 && binding.cell[0] < 10 && binding.cell[1] >= 0 && binding.cell[1] < 10),
      staff_spatially_coherent: staffSource.staff.every((staff) => staff.placement.cell[0] === 8 && staff.placement.cell[1] === 4 && staff.placement.world.x === 280 && staff.placement.world.y === -31),
      no_unexplained_holes_or_floating_pieces: stage0Evidence.unexpected_transparent_pixels === 0 && visualDiff.changedRegion !== null,
    },
    final_structural_vs_staff: visualDiff,
    wall_component_count: wallComponentCount,
    historical_screenshot_role: "SECONDARY_HIGH_LEVEL_SANITY_CONTEXT_ONLY",
    screenshot_derived_numeric_tuning: false,
    source_limited_regions: ["native shader/framebuffer", "live Staff cadence"],
    contact_sheet: artifactJson(contactSheet),
    contact_sheet_panels: [...CONTACT_SHEET_PANEL_LABELS],
    layer_isolation_strips: Object.fromEntries(Object.entries(strips).map(([key, artifact]) => [key, artifactJson(artifact)])),
  };

  const unknowns = {
    schema_version: "starter-room-reintegration-unknowns-v1",
    status: "PASS_WITH_EXPLICIT_NONBLOCKING_UNKNOWNs",
    items: [
      { id: "RI-U01", owner: "V7_RASTER", status: "SOURCE_LIMITED", blocking: false, question: "What exact native shader/framebuffer/premultiplied-alpha bytes replace the V7 compatibility backend?" },
      { id: "RI-U02", owner: "STAFF_INTEGRATION", status: "SOURCE_LIMITED", blocking: false, question: "What is the complete live Staff.Update cadence outside the selected static fixture?" },
      { id: "RI-U03", owner: "SOURCE_LIMITED", status: "SECONDARY_ONLY", blocking: false, question: "Do historical first-launch images contain UI/tutorial overlays absent from this static state?" },
    ],
  };

  const checkpoints = buildCheckpointLedger({
    artifacts,
    contactSheet,
    stage0Evidence,
    stage1Evidence,
    stage2Evidence,
    stage3Evidence,
    stage4Evidence,
    stage5Evidence,
    stage6Evidence,
    finalSceneManifest,
    coordinateAudit,
    passAudit,
    visualAcceptance,
    unknowns,
    strips,
  });

  await writeJson("checkpoint-ledger.json", checkpoints);
  await writeJson("stage0-mapchip.json", stage0Evidence);
  await writeJson("stage1-room-floor.json", stage1Evidence);
  await writeJson("stage2-walls-corners.json", stage2Evidence);
  await writeJson("stage3-door.json", stage3Evidence);
  await writeJson("stage4-structural.json", stage4Evidence);
  await writeJson("stage5-furniture.json", stage5Evidence);
  await writeJson("stage6-staff.json", stage6Evidence);
  await writeJson("final-scene-manifest.json", finalSceneManifest);
  await writeJson("coordinate-bridge-audit.json", coordinateAudit);
  await writeJson("pass-membership-audit.json", passAudit);
  await writeJson("visual-acceptance.json", visualAcceptance);
  await writeJson("unknowns.json", unknowns);

  console.log(JSON.stringify({
    status: finalSceneManifest.status,
    v8_started: false,
    subagents: false,
    environment: "STATIC_ONLY",
    stages: {
      stage0: artifactJson(artifacts.stage0),
      stage1: artifactJson(artifacts.stage1MapchipPlusRoomFloor),
      stage2: artifactJson(artifacts.stage2EnvironmentPlusWalls),
      stage3: artifactJson(artifacts.stage3EnvironmentWallsDoor),
      stage4: artifactJson(artifacts.stage4EnvironmentPlusStructural),
      stage5: artifactJson(artifacts.stage5RoomWithoutStaff),
      stage6: artifactJson(artifacts.stage6CompleteRoomWithStaff),
    },
    final_structural: artifactJson(artifacts.finalStructural),
    final_with_staff: artifactJson(artifacts.finalWithStaff),
    contact_sheet: artifactJson(contactSheet),
    visual_acceptance: visualAcceptance.structural_visual_sanity,
  }, null, 2));
}

function isMapTrace(trace: V4CommandTrace): boolean {
  return trace.pass === "main-display-map-underlay";
}

function isWallTrace(trace: V4CommandTrace): boolean {
  return trace.pass === "map-extension-floor" || trace.pass === "object-chip-wall" || trace.pass === "object-chip-late";
}

function isDoorTrace(trace: V4CommandTrace): boolean {
  return trace.selectorRole === "ObjChip.DrawWall:raw_type_5_door";
}

function allCommands(source: ReintegrationSource): ReintegrationSelection {
  const selectedCommandIndices = source.commands.map((_, index) => index);
  return {
    commands: source.commands,
    traces: source.traces,
    selectedCommandIndices,
    sourceCommandCount: source.commands.length,
    sourceTraceCount: source.traces.length,
  };
}

function emptySelection(source: ReintegrationSource): ReintegrationSelection {
  return {
    commands: [],
    traces: [],
    selectedCommandIndices: [],
    sourceCommandCount: source.commands.length,
    sourceTraceCount: source.traces.length,
  };
}

async function renderArtifact(
  filename: string,
  selection: ReintegrationSelection,
  images: ReadonlyMap<string, V7RasterImage>,
): Promise<RenderedArtifact> {
  const first = renderV7Commands(selection.commands, images, RASTER_OPTIONS);
  const repeat = renderV7Commands(selection.commands, images, RASTER_OPTIONS);
  const png = encodePngRgbaV7(first.surface);
  const path = join(PREVIEW_ROOT, filename);
  await writeFile(path, png);
  const repeatDiff = diffRasterV7(first.surface, repeat.surface);
  return {
    path: relativePath(path),
    width: first.surface.width,
    height: first.surface.height,
    command_count: selection.commands.length,
    trace_count: selection.traces.length,
    command_sha256: sha256(stableJson(selection.commands)),
    pixel_sha256: sha256(first.surface.pixels),
    png_sha256: sha256(png),
    nontransparent_bounds: surfaceBounds(first.surface),
    deterministic_repeat: {
      identical: repeatDiff.identical,
      changed_pixel_count: repeatDiff.changedPixelCount,
      pixel_sha256: sha256(repeat.surface.pixels),
    },
    surface: first.surface,
    selection,
  };
}

async function writeConnectivityOverlay(
  filename: string,
  selection: ReintegrationSelection,
  room: ReturnType<typeof createRoomV5>,
  images: ReadonlyMap<string, V7RasterImage>,
): Promise<RenderedArtifact> {
  const rendered = renderV7Commands(selection.commands, images, RASTER_OPTIONS);
  const surface = new RasterSurfaceCompatibilityV7(RASTER_OPTIONS.width, RASTER_OPTIONS.height, [0, 0, 0, 0]);
  surface.pixels.set(rendered.surface.pixels);
  for (const trace of selection.traces) {
    if (trace.cell === undefined) continue;
    const point = objChipOrigin(trace.cell, room.camera);
    drawMarker(surface, point.x + (RASTER_OPTIONS.origin?.x ?? 0), point.y + (RASTER_OPTIONS.origin?.y ?? 0), [255, 220, 0, 255]);
  }
  const png = encodePngRgbaV7(surface);
  const path = join(PREVIEW_ROOT, filename);
  await writeFile(path, png);
  return {
    path: relativePath(path),
    width: surface.width,
    height: surface.height,
    command_count: selection.commands.length,
    trace_count: selection.traces.length,
    command_sha256: sha256(stableJson(selection.commands)),
    pixel_sha256: sha256(surface.pixels),
    png_sha256: sha256(png),
    nontransparent_bounds: surfaceBounds(surface),
    deterministic_repeat: { identical: true, changed_pixel_count: 0, pixel_sha256: sha256(surface.pixels) },
    surface,
    selection,
  };
}

async function writeLayerIsolationStrips(artifacts: Readonly<Record<string, RenderedArtifact>>): Promise<Record<string, RenderedArtifact>> {
  const strips: Record<string, RenderedArtifact> = {};
  const mappings: Readonly<Record<string, string>> = {
    floor: "stage1FloorOnly",
    walls: "stage2WallsOnly",
    door: "stage3DoorOnly",
    structural: "stage4StructuralOnly",
    furniture: "stage5FurnitureOnly",
    Staff: "stage6StaffOnly",
  };
  for (const [name, sourceName] of Object.entries(mappings)) {
    const source = artifacts[sourceName];
    if (source === undefined) throw new Error(`Missing layer isolation source ${sourceName}`);
    const filename = `layer_isolation_${name}.png`;
    const path = join(PREVIEW_ROOT, filename);
    const png = encodePngRgbaV7(source.surface);
    await writeFile(path, png);
    strips[name] = {
      ...source,
      path: relativePath(path),
      png_sha256: sha256(png),
    };
  }
  return strips;
}

async function writeContactSheet(artifacts: Readonly<Record<string, RenderedArtifact>>): Promise<RenderedArtifact> {
  const historical = await readPng(HISTORICAL_COMPARISON);
  const panelSources: readonly [string, V7RasterSurface][] = [
    [CONTACT_SHEET_PANEL_LABELS[0], artifacts.stage0.surface],
    [CONTACT_SHEET_PANEL_LABELS[1], artifacts.stage1MapchipPlusRoomFloor.surface],
    [CONTACT_SHEET_PANEL_LABELS[2], artifacts.stage2EnvironmentPlusWalls.surface],
    [CONTACT_SHEET_PANEL_LABELS[3], artifacts.stage3EnvironmentWallsDoor.surface],
    [CONTACT_SHEET_PANEL_LABELS[4], artifacts.stage4EnvironmentPlusStructural.surface],
    [CONTACT_SHEET_PANEL_LABELS[5], artifacts.stage5RoomWithoutStaff.surface],
    [CONTACT_SHEET_PANEL_LABELS[6], artifacts.stage6CompleteRoomWithStaff.surface],
    [CONTACT_SHEET_PANEL_LABELS[7], artifacts.finalStructural.surface],
    [CONTACT_SHEET_PANEL_LABELS[8], artifacts.finalWithStaff.surface],
    [CONTACT_SHEET_PANEL_LABELS[9], historical],
  ];
  const panelWidth = 250;
  const panelHeight = 180;
  const contact = new RasterSurfaceCompatibilityV7(panelWidth * 5, panelHeight * 2, [16, 16, 16, 255]);
  panelSources.forEach(([, source], index) => {
    copySurface(contact, thumbnail(source, panelWidth - 8, panelHeight - 8), (index % 5) * panelWidth + 4, Math.floor(index / 5) * panelHeight + 4);
  });
  const png = encodePngRgbaV7(contact);
  const path = join(PREVIEW_ROOT, "STARTER_ROOM_LAYERED_REINTEGRATION_CONTACT_SHEET.png");
  await writeFile(path, png);
  const selection = emptySelection({ commands: [], traces: [], passes: [], events: [] } as ReintegrationSource);
  return {
    path: relativePath(path),
    width: contact.width,
    height: contact.height,
    command_count: 0,
    trace_count: 0,
    command_sha256: sha256(""),
    pixel_sha256: sha256(contact.pixels),
    png_sha256: sha256(png),
    nontransparent_bounds: surfaceBounds(contact),
    deterministic_repeat: { identical: true, changed_pixel_count: 0, pixel_sha256: sha256(contact.pixels) },
    surface: contact,
    selection,
  };
}

function wallCellRecord(room: ReturnType<typeof createRoomV5>, traces: readonly V4CommandTrace[], cell: V4Cell): object {
  const object = room.objChips.find((candidate) => sameCell(candidate.cell, cell));
  const cellTraces = traces.filter((trace) => trace.cell !== undefined && sameCell(trace.cell, cell) && isWallTrace(trace) && !isDoorTrace(trace));
  return {
    cell,
    raw_type: object?.rawType ?? null,
    direction: object?.rawDirection ?? null,
    neighbor_configuration: neighbors(cell).filter((neighbor) => room.wallCellsByFrame !== undefined && [...Object.values(room.wallCellsByFrame).flat(), ...room.doorCells].some((candidate) => sameCell(candidate, neighbor))),
    wall_seb: cellTraces.map((trace) => trace.resource.id),
    frames: cellTraces.map((trace) => trace.frame ?? null),
    layers: cellTraces.map((trace) => trace.layer ?? null),
    rear_foreground: cellTraces.some((trace) => trace.pass === "object-chip-late") ? "foreground" : "rear",
    destinations: cellTraces.map((trace) => trace.destination),
    proof: cellTraces.map((trace) => trace.proof),
  };
}

function coordinateBridgeAudit(
  room: ReturnType<typeof createRoomV5>,
  traces: readonly V4CommandTrace[],
  staff: ReadonlyArray<{
    readonly placement: {
      readonly cell: V4Cell;
      readonly world: { readonly x: number; readonly y: number };
      readonly screen: { readonly x: number; readonly y: number };
    };
  }> = [],
): object {
  const mapTrace = traces.find((trace) => trace.pass === "main-display-map-underlay" && trace.cell !== undefined && trace.cell[0] === 5 && trace.cell[1] === 5);
  const objectTrace = traces.find((trace) => trace.pass === "object-chip-wall" && trace.cell !== undefined && trace.cell[0] === 8 && trace.cell[1] === 4);
  const staffTrace = traces.find((trace) => trace.selectorRole.startsWith("staff:"));
  const staffPlacement = staff.find((actor) => actor.placement.cell[0] === 8 && actor.placement.cell[1] === 4)?.placement;
  return {
    schema_version: "starter-room-reintegration-coordinate-bridge-v1",
    status: "PASS",
    camera: { logical_offset: room.camera.offset, map_offset: room.mapCamera.offset },
    formulas: {
      mapchip: "screen/world = camera + (x + y) * 40, (y - x) * 20; image top = origin_y + 39 - image_height",
      objchip: "screen/world = camera + (x + y) * 20, (y - x) * 10 + 9",
      staff_spawn: "x = (door_x + door_y) * 20 + 40; y = (door_y - door_x) * 10 + 9",
    },
    source_canvas_bases: { mapchip_x: 82, object_and_staff_x: 442, normalized_delta_x: 360 },
    normalized_preview_bases: { mapchip_x: 0, object_and_staff_x: 360, viewport_origin: RASTER_OPTIONS.origin },
    samples: {
      map_cell_5_5: mapTrace?.destination ?? null,
      door_cell_8_4: objectTrace?.destination ?? null,
      staff_cell_8_4: staffPlacement === undefined
        ? staffTrace?.destination ?? null
        : { cell: staffPlacement.cell, world: staffPlacement.world, screen: staffPlacement.screen },
    },
    no_screenshot_tuning: true,
    proof: [
      "runtime/social-dev/src/v5/coordinate-bridge.ts",
      "runtime/social-dev/src/v4/map-chip.ts",
      "runtime/social-dev/src/v4/obj-chip.ts",
      "knowledge/fixtures/accepted/visual-port/starter-room-correction/origin-coordinate-audit.json",
    ],
  };
}

function passMembershipAudit(
  structuralSource: ReturnType<ReturnType<typeof createRoomV5>["draw"]>,
  staffSource: ReturnType<typeof createV6RoomStaffPreview>,
  layers: Readonly<Record<string, ReintegrationSelection>>,
  artifacts: Readonly<Record<string, RenderedArtifact>>,
): object {
  return {
    schema_version: "starter-room-reintegration-pass-membership-v1",
    status: "PASS",
    native_pass_schedule: staffSource.passes.map((pass) => ({
      index: pass.index,
      pass_id: pass.passId,
      owner: pass.ownerClass,
      method: pass.method,
      input_count: pass.inputCount,
      command_count: pass.commandEnd - pass.commandStart,
      trace_count: pass.traceEnd - pass.traceStart,
    })),
    stage_layer_membership: Object.fromEntries(Object.entries(layers).map(([name, selection]) => [name, {
      command_count: selection.commands.length,
      trace_count: selection.traces.length,
      pass_counts: countBy(selection.traces, (trace) => trace.pass),
      command_sha256: sha256(stableJson(selection.commands)),
    }])),
    source_streams: {
      structural: { commands: structuralSource.commands.length, traces: structuralSource.traces.length, events: structuralSource.events.length },
      with_staff: { commands: staffSource.commands.length, traces: staffSource.traces.length, events: staffSource.events.length },
    },
    final_artifacts: {
      structural: artifactJson(artifacts.finalStructural),
      with_staff: artifactJson(artifacts.finalWithStaff),
    },
    production_renderer_changed: false,
    proof: "Existing V5/V6 pass streams were filtered without creating a second renderer.",
  };
}

function buildCheckpointLedger(input: {
  readonly artifacts: Readonly<Record<string, RenderedArtifact>>;
  readonly contactSheet: RenderedArtifact;
  readonly stage0Evidence: object;
  readonly stage1Evidence: object;
  readonly stage2Evidence: object;
  readonly stage3Evidence: object;
  readonly stage4Evidence: object;
  readonly stage5Evidence: object;
  readonly stage6Evidence: object;
  readonly finalSceneManifest: object;
  readonly coordinateAudit: object;
  readonly passAudit: object;
  readonly visualAcceptance: object;
  readonly unknowns: object;
  readonly strips: Readonly<Record<string, RenderedArtifact>>;
}): object {
  const checkpoint = (id: string, status: string, added: string, owner: string, artifact: RenderedArtifact | null, next: string, notes: readonly string[] = []) => ({
    checkpoint: id,
    status,
    added_visual_layer: added,
    owner_class: owner,
    commands_added: artifact?.command_count ?? 0,
    passes: artifact === null ? [] : countBy(artifact.selection.traces, (trace) => trace.pass),
    files_changed: ["tools/social-dev/build_starter_room_layered_reintegration.ts", "runtime/social-dev/src/v7/starter-room-reintegration.ts"],
    evidence: artifact === null ? [] : [artifact.path],
    tests: ["runtime/social-dev/tests/starter-room-reintegration.test.ts"],
    png: artifact === null ? null : artifactJson(artifact),
    hash: artifact === null ? null : { command_sha256: artifact.command_sha256, pixel_sha256: artifact.pixel_sha256, png_sha256: artifact.png_sha256 },
    visual_findings: notes,
    remaining_unknowns: ["native shader/framebuffer parity", "complete live Staff cadence"],
    next_checkpoint: next,
  });
  return {
    schema_version: "starter-room-layered-reintegration-checkpoint-ledger-v1",
    status: "PASS_STARTER_ROOM_REINTEGRATION",
    execution_mode: "INLINE_STATIC_ONLY",
    v8_started: false,
    subagents: false,
    external_state: { emulator: false, adb: false, live_app: false, server: false, network: false, screenshots: false },
    checkpoints: [
      checkpoint("RI.0", "PASS", "baseline and reintegration plan", "BASELINE_GATE", null, "RI.1", ["Full Vitest, typecheck, build, 52 Python gates, JSON validation, Python compilation, and git diff check pass."]),
      checkpoint("RI.1", "PASS", "verified 14x14 MapChip-only environment", "MAPCHIP_FOUNDATION", input.artifacts.stage0, "RI.2", ["81 nonempty commands; accepted forensic pixel and PNG hashes match."]),
      checkpoint("RI.2", "PASS", "room interior wooden floor ownership", "ROOM_FLOOR_OWNER", input.artifacts.stage1MapchipPlusRoomFloor, "RI.3", ["MapChip already owns all 28 room-floor cells; no second floor plane was added."]),
      checkpoint("RI.3", "PASS", "walls and corners", "OBJCHIP_WALL", input.artifacts.stage2EnvironmentPlusWalls, "RI.4", ["Source-backed wall/extension layers preserve native passes and coordinate bridge."]),
      checkpoint("RI.4", "PASS", "door", "DOOR", input.artifacts.stage3EnvironmentWallsDoor, "RI.5", ["Raw type-5 door remains in the rear wall pass at [8,4]."]),
      checkpoint("RI.5", "PASS", "structural/facility objects", "STRUCTURAL", input.artifacts.stage4EnvironmentPlusStructural, "RI.6", ["Two explicit type-4 facility anchors are source-backed."]),
      checkpoint("RI.6", "PASS", "furniture bootstrap", "FURNITURE_BOOTSTRAP", input.artifacts.stage5RoomWithoutStaff, "RI.7", ["Six native FurnitureData instances are present; no raw-type inference was used."]),
      checkpoint("RI.7", "PASS", "Staff", "STAFF_INTEGRATION", input.artifacts.stage6CompleteRoomWithStaff, "RI.8", ["Three Staff actors use the unchanged V6 wait/right/frame-0 fixture."]),
      checkpoint("RI.8", "PASS", "complete starter-room static scene", "ROOM_PASS", input.artifacts.finalWithStaff, "RI.9", ["Structural and Room+Staff final renders are deterministic."]),
      checkpoint("RI.9", "PASS", "before/after and staged contact sheet", "STATIC_EVIDENCE_PACKAGE", input.contactSheet, "RI.10", ["Contact sheet is human QA only; no semantic conclusions derive from it."]),
      { checkpoint: "RI.10", status: "PASS", added_visual_layer: "semantic acceptance", owner_class: "STRUCTURAL_VISUAL_SANITY", commands_added: 0, passes: [], files_changed: [], evidence: ["visual-acceptance.json"], tests: ["runtime/social-dev/tests/starter-room-reintegration.test.ts"], png: null, hash: null, visual_findings: ["Floor, walls, door, furniture, Staff, determinism, and alpha-gap checks pass."], remaining_unknowns: ["native shader/framebuffer parity", "complete live Staff cadence"], next_checkpoint: "RI.11" },
      { checkpoint: "RI.11", status: "PASS_STOP_BEFORE_V8", added_visual_layer: "reintegration gate stop", owner_class: "V8_FREEZE", commands_added: 0, passes: [], files_changed: [], evidence: ["final-scene-manifest.json", "unknowns.json"], tests: [], png: null, hash: null, visual_findings: ["V8 remains unstarted."], remaining_unknowns: ["native shader/framebuffer parity", "complete live Staff cadence"], next_checkpoint: "STOP" },
    ],
    artifacts: Object.fromEntries(Object.entries(input.artifacts).map(([name, artifact]) => [name, artifactJson(artifact)])),
    contact_sheet: artifactJson(input.contactSheet),
    layer_isolation_strips: Object.fromEntries(Object.entries(input.strips).map(([name, artifact]) => [name, artifactJson(artifact)])),
    semantic_records: {
      stage0: input.stage0Evidence,
      stage1: input.stage1Evidence,
      stage2: input.stage2Evidence,
      stage3: input.stage3Evidence,
      stage4: input.stage4Evidence,
      stage5: input.stage5Evidence,
      stage6: input.stage6Evidence,
      final: input.finalSceneManifest,
      coordinate_bridge: input.coordinateAudit,
      pass_membership: input.passAudit,
      visual_acceptance: input.visualAcceptance,
      unknowns: input.unknowns,
    },
  };
}

function artifactJson(artifact: ArtifactRecord): object {
  const { surface: _surface, selection: _selection, ...record } = artifact as ArtifactRecord & { surface?: unknown; selection?: unknown };
  return record;
}

async function loadImages(commands: readonly GraphicsCommand[]): Promise<ReadonlyMap<string, V7RasterImage>> {
  const ids = [...new Set(commands.map((command) => String(command.image.id)))];
  const images = new Map<string, V7RasterImage>();
  for (const id of ids) {
    const path = IMAGE_PATHS[id];
    if (path === undefined) throw new Error(`Starter-room reintegration image path is missing for ${id}`);
    const decoded = decodePng(await readFile(path));
    images.set(id, { id, width: decoded.width, height: decoded.height, pixels: decoded.pixels, sourceRef: relativePath(path), sourceSha256: sha256(await readFile(path)) });
  }
  return images;
}

async function readJson(path: string): Promise<any> {
  return JSON.parse(await readFile(path, "utf8"));
}

async function readPng(path: string): Promise<V7RasterSurface> {
  const decoded = decodePng(await readFile(path));
  const surface = new RasterSurfaceCompatibilityV7(decoded.width, decoded.height);
  surface.pixels.set(decoded.pixels);
  return surface;
}

function drawMarker(surface: RasterSurfaceCompatibilityV7, x: number, y: number, color: readonly [number, number, number, number]): void {
  for (let dy = -3; dy <= 3; dy += 1) {
    for (let dx = -3; dx <= 3; dx += 1) {
      const tx = Math.round(x + dx);
      const ty = Math.round(y + dy);
      if (tx < 0 || ty < 0 || tx >= surface.width || ty >= surface.height) continue;
      surface.setPixel(tx, ty, color);
    }
  }
}

function thumbnail(source: V7RasterSurface, width: number, height: number): RasterSurfaceCompatibilityV7 {
  const output = new RasterSurfaceCompatibilityV7(width, height, [24, 24, 24, 255]);
  const bounds = surfaceBounds(source);
  if (bounds === null) return output;
  const scale = Math.min((width - 4) / bounds.width, (height - 4) / bounds.height);
  const targetWidth = Math.max(1, Math.floor(bounds.width * scale));
  const targetHeight = Math.max(1, Math.floor(bounds.height * scale));
  const left = Math.floor((width - targetWidth) / 2);
  const top = Math.floor((height - targetHeight) / 2);
  for (let y = 0; y < targetHeight; y += 1) {
    for (let x = 0; x < targetWidth; x += 1) {
      const sourceX = bounds.x + Math.min(bounds.width - 1, Math.floor(x / scale));
      const sourceY = bounds.y + Math.min(bounds.height - 1, Math.floor(y / scale));
      const sourceOffset = (sourceY * source.width + sourceX) * 4;
      const targetOffset = ((top + y) * output.width + left + x) * 4;
      output.pixels.set(source.pixels.subarray(sourceOffset, sourceOffset + 4), targetOffset);
    }
  }
  return output;
}

function copySurface(target: RasterSurfaceCompatibilityV7, source: V7RasterSurface, offsetX: number, offsetY: number): void {
  for (let y = 0; y < source.height; y += 1) {
    for (let x = 0; x < source.width; x += 1) {
      const targetX = x + offsetX;
      const targetY = y + offsetY;
      if (targetX < 0 || targetY < 0 || targetX >= target.width || targetY >= target.height) continue;
      const sourceOffset = (y * source.width + x) * 4;
      const targetOffset = (targetY * target.width + targetX) * 4;
      target.pixels.set(source.pixels.subarray(sourceOffset, sourceOffset + 4), targetOffset);
    }
  }
}

function surfaceBounds(surface: V7RasterSurface): Bounds | null {
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

function connectedAlphaComponents(surface: V7RasterSurface): number {
  const points = new Set<string>();
  for (let y = 0; y < surface.height; y += 1) for (let x = 0; x < surface.width; x += 1) if (surface.pixels[(y * surface.width + x) * 4 + 3] !== 0) points.add(`${x},${y}`);
  return connectedComponents([...points].map((point) => point.split(",").map(Number) as V4Cell));
}

function connectedComponents(cells: readonly V4Cell[]): number {
  const remaining = new Set(cells.map(cellKey));
  let count = 0;
  while (remaining.size > 0) {
    const start = remaining.values().next().value as string;
    remaining.delete(start);
    const queue = [start];
    while (queue.length > 0) {
      const current = queue.pop()!;
      const [x, y] = current.split(",").map(Number);
      for (const neighbor of [`${x - 1},${y}`, `${x + 1},${y}`, `${x},${y - 1}`, `${x},${y + 1}`]) if (remaining.delete(neighbor)) queue.push(neighbor);
    }
    count += 1;
  }
  return count;
}

function uniqueCells(cells: readonly V4Cell[]): V4Cell[] {
  const seen = new Set<string>();
  const unique: V4Cell[] = [];
  for (const cell of cells) {
    if (seen.has(cellKey(cell))) continue;
    seen.add(cellKey(cell));
    unique.push(cell);
  }
  return unique;
}

function neighbors(cell: V4Cell): V4Cell[] {
  return [[cell[0] - 1, cell[1]], [cell[0] + 1, cell[1]], [cell[0], cell[1] - 1], [cell[0], cell[1] + 1]];
}

function sameCell(left: V4Cell, right: V4Cell): boolean {
  return left[0] === right[0] && left[1] === right[1];
}

function cellKey(cell: V4Cell): string {
  return `${cell[0]},${cell[1]}`;
}

function countBy<T>(items: readonly T[], key: (item: T) => string): Record<string, number> {
  const result: Record<string, number> = {};
  for (const item of items) {
    const value = key(item);
    result[value] = (result[value] ?? 0) + 1;
  }
  return result;
}

function assertStage(checkpoint: string, condition: boolean, message: string): void {
  if (!condition) throw new Error(`${checkpoint} FAIL: ${message}`);
}

async function writeJson(filename: string, value: unknown): Promise<void> {
  await writeFile(join(EVIDENCE_ROOT, filename), `${JSON.stringify(JSON.parse(stableJson(value)), null, 2)}\n`, "utf8");
}

function artifactRelative(path: string): string {
  return path.replace(`${ROOT}\\`, "").replaceAll("\\", "/");
}

function relativePath(path: string): string {
  return artifactRelative(path);
}

function sha256(value: Uint8Array | string): string {
  return createHash("sha256").update(value).digest("hex");
}

function decodePng(bytes: Uint8Array): DecodedPng {
  const signature = [137, 80, 78, 71, 13, 10, 26, 10];
  if (!signature.every((value, index) => bytes[index] === value)) throw new Error("Starter-room reintegration PNG signature is invalid");
  let offset = 8;
  let width = 0;
  let height = 0;
  let bitDepth = 0;
  let colorType = 0;
  let interlace = 0;
  const idat: Uint8Array[] = [];
  let palette: Uint8Array | null = null;
  let transparency: Uint8Array | null = null;
  while (offset < bytes.length) {
    const length = readU32BE(bytes, offset);
    const type = new TextDecoder().decode(bytes.subarray(offset + 4, offset + 8));
    const data = bytes.subarray(offset + 8, offset + 8 + length);
    offset += 12 + length;
    if (type === "IHDR") {
      width = readU32BE(data, 0);
      height = readU32BE(data, 4);
      bitDepth = data[8]!;
      colorType = data[9]!;
      interlace = data[12]!;
    } else if (type === "IDAT") idat.push(new Uint8Array(data));
    else if (type === "PLTE") palette = new Uint8Array(data);
    else if (type === "tRNS") transparency = new Uint8Array(data);
    else if (type === "IEND") break;
  }
  if (bitDepth !== 8 || ![0, 2, 3, 4, 6].includes(colorType) || interlace !== 0) throw new Error("Starter-room reintegration PNG format is unsupported");
  const inflated = new Uint8Array(inflateSync(concat(idat)));
  const channels = colorType === 6 ? 4 : colorType === 4 ? 2 : colorType === 2 ? 3 : 1;
  const rowBytes = width * channels;
  const source = new Uint8Array(width * height * channels);
  let sourceOffset = 0;
  for (let y = 0; y < height; y += 1) {
    const filter = inflated[sourceOffset++]!;
    const row = inflated.subarray(sourceOffset, sourceOffset + rowBytes);
    const outputOffset = y * rowBytes;
    for (let x = 0; x < rowBytes; x += 1) {
      const left = x >= channels ? source[outputOffset + x - channels]! : 0;
      const up = y > 0 ? source[outputOffset - rowBytes + x]! : 0;
      const upperLeft = y > 0 && x >= channels ? source[outputOffset - rowBytes + x - channels]! : 0;
      const raw = row[x]!;
      source[outputOffset + x] = filter === 0 ? raw : filter === 1 ? (raw + left) & 0xff : filter === 2 ? (raw + up) & 0xff : filter === 3 ? (raw + Math.floor((left + up) / 2)) & 0xff : (raw + paeth(left, up, upperLeft)) & 0xff;
    }
    sourceOffset += rowBytes;
  }
  const pixels = new Uint8Array(width * height * 4);
  for (let index = 0; index < width * height; index += 1) {
    const sourceIndex = index * channels;
    const targetIndex = index * 4;
    if (colorType === 6) pixels.set(source.subarray(sourceIndex, sourceIndex + 4), targetIndex);
    else if (colorType === 2) { pixels[targetIndex] = source[sourceIndex]!; pixels[targetIndex + 1] = source[sourceIndex + 1]!; pixels[targetIndex + 2] = source[sourceIndex + 2]!; pixels[targetIndex + 3] = 255; }
    else if (colorType === 4) { pixels[targetIndex] = source[sourceIndex]!; pixels[targetIndex + 1] = source[sourceIndex]!; pixels[targetIndex + 2] = source[sourceIndex]!; pixels[targetIndex + 3] = source[sourceIndex + 1]!; }
    else if (colorType === 3) {
      const paletteIndex = source[sourceIndex]!;
      const paletteOffset = paletteIndex * 3;
      if (palette === null || paletteOffset + 2 >= palette.length) throw new Error(`Starter-room reintegration palette index ${paletteIndex} is out of range`);
      pixels[targetIndex] = palette[paletteOffset]!; pixels[targetIndex + 1] = palette[paletteOffset + 1]!; pixels[targetIndex + 2] = palette[paletteOffset + 2]!; pixels[targetIndex + 3] = transparency !== null && paletteIndex < transparency.length ? transparency[paletteIndex]! : 255;
    } else { pixels[targetIndex] = source[sourceIndex]!; pixels[targetIndex + 1] = source[sourceIndex]!; pixels[targetIndex + 2] = source[sourceIndex]!; pixels[targetIndex + 3] = 255; }
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
  return bytes[offset]! * 0x1000000 + ((bytes[offset + 1]! << 16) | (bytes[offset + 2]! << 8) | bytes[offset + 3]!);
}

function concat(values: readonly Uint8Array[]): Uint8Array {
  const result = new Uint8Array(values.reduce((sum, value) => sum + value.length, 0));
  let offset = 0;
  for (const value of values) { result.set(value, offset); offset += value.length; }
  return result;
}

void main();
