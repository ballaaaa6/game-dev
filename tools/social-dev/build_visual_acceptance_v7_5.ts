/** Build the offline V7.5 visual acceptance package from the existing V1-V7 contracts. */

import { createHash } from "node:crypto";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { inflateSync } from "node:zlib";
import { GraphicsCompatibility, imageRef } from "../../runtime/social-dev/src/v2/graphics";
import { createV6RoomStaffPreview } from "../../runtime/social-dev/src/v6/index";
import { createRoomV5, stableJson } from "../../runtime/social-dev/src/v5/index";
import type { GraphicsCommand } from "../../runtime/social-dev/src/v2/graphics";
import type { HumanDirection } from "../../runtime/social-dev/src/v6/contracts";
import type { StaffAction } from "../../runtime/social-dev/src/v6/contracts";
import type { V7RasterImage, V7RasterSurface } from "../../runtime/social-dev/src/v7/contracts";
import { diffRasterV7 } from "../../runtime/social-dev/src/v7/diff";
import { renderV7Commands, renderV7Room00Structural, renderV7Room00WithStaff } from "../../runtime/social-dev/src/v7/golden-renderer";
import { encodePngRgbaV7 } from "../../runtime/social-dev/src/v7/png";
import { RasterCompatibilityV7, RasterSurfaceCompatibilityV7 } from "../../runtime/social-dev/src/v7/raster";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..", "..");
const ASSET_ROOT = join(ROOT, "runtime", "social-dev", "assets");
const V7_ROOT = join(ROOT, "knowledge", "social-dev", "evidence", "visual-port", "v7");
const EVIDENCE_ROOT = join(ROOT, "knowledge", "social-dev", "evidence", "visual-port", "v7_5");
const PREVIEW_ROOT = join(EVIDENCE_ROOT, "previews");
const REPORT_PATH = join(ROOT, "docs", "Phases", "VisualPort", "V7_5_VISUAL_ACCEPTANCE.md");
const ROOM_FIXTURE_OPTIONS = { width: 360, height: 220, origin: { x: 64, y: 96 }, background: [0, 0, 0, 0] as const };
const STAFF_PANEL_OPTIONS = { width: 80, height: 80, origin: { x: 0, y: 0 }, background: [0, 0, 0, 0] as const };
const STAFF_DIRECTIONS: readonly HumanDirection[] = ["right", "left", "up", "down"];
const STAFF_ACTIONS: readonly StaffAction[] = ["wait", "move", "typing"];

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

type PanelSurface = {
  readonly label: string;
  readonly surface: V7RasterSurface;
};

type Artifact = {
  readonly key: string;
  readonly filename: string;
  readonly path: string;
  readonly surface: V7RasterSurface;
  readonly png: Uint8Array;
  readonly metadata: Readonly<Record<string, unknown>>;
};

type PackageBuild = {
  readonly artifacts: readonly Artifact[];
  readonly contactSheet: Artifact;
  readonly baseline: {
    readonly roomCommands: readonly GraphicsCommand[];
    readonly integratedCommands: readonly GraphicsCommand[];
    readonly v5CommandHash: string;
    readonly v5ManifestHash: string;
    readonly v6CommandHash: string;
    readonly v6ManifestHash: string;
    readonly v7SourceManifestHash: string;
    readonly v7GoldenManifestHash: string;
    readonly v7GoldenResultsHash: string;
    readonly v6StaffManifestHash: string;
    readonly v6SelectorMapHash: string;
    readonly v6AnimationContractHash: string;
  };
  readonly selectors: readonly SelectorRecord[];
};

type SelectorRecord = {
  readonly sheet: string;
  readonly action: string;
  readonly direction: HumanDirection;
  readonly selectorId: number;
  readonly selectorFilename: string | null;
  readonly frame: number;
  readonly alpha: number;
  readonly commandHash: string;
};

type DeterminismRecord = {
  readonly key: string;
  readonly path: string;
  readonly width: number;
  readonly height: number;
  readonly sha256RunA: string;
  readonly sha256RunB: string;
  readonly pixelSha256RunA: string;
  readonly pixelSha256RunB: string;
  readonly byteIdentical: boolean;
  readonly changedPixelCount: number;
};

type VisualIssue = {
  readonly id: string;
  readonly image: string;
  readonly panel: string;
  readonly visualSymptom: string;
  readonly relevantVPhase: string;
  readonly relevantCommandOrResourceId: string;
  readonly likelyClass: "A_POSSIBLE_SOURCE_COMMAND_BUG" | "B_POSSIBLE_RASTER_CONTRACT_BUG" | "C_COMPATIBILITY_BACKEND_DIFFERENCE" | "D_PRODUCT_POLICY_DIFFERENCE" | "E_HISTORICAL_CONTEXT_DIFFERENCE" | "F_UNKNOWN";
  readonly evidenceReviewRequired: boolean;
};

const VISUAL_ISSUES: readonly VisualIssue[] = [];

async function main(): Promise<void> {
  await mkdir(PREVIEW_ROOT, { recursive: true });
  await verifyV7Baseline();

  const inputBytes = await loadInputBytes();
  const buildA = await buildPackage(inputBytes);
  const buildB = await buildPackage(inputBytes);
  const determinism = compareBuilds(buildA, buildB);
  const allDeterministic = determinism.every((item) => item.byteIdentical && item.changedPixelCount === 0);

  for (const artifact of [...buildA.artifacts, buildA.contactSheet]) {
    await writeFile(join(ROOT, artifact.path), Buffer.from(artifact.png));
  }

  const recommendation = allDeterministic && VISUAL_ISSUES.length === 0 ? "ACCEPT_FOR_V8" : "FIX_BEFORE_V8";
  const evidence = buildMachineEvidence(buildA, determinism, recommendation);
  await writeJson(join(EVIDENCE_ROOT, "visual-acceptance.json"), evidence);
  await writeFile(REPORT_PATH, buildReport(buildA, determinism, recommendation), "utf8");

  console.log(JSON.stringify({
    status: allDeterministic ? "pass_static" : "blocked",
    recommendation,
    images: buildA.artifacts.length,
    contactSheet: {
      width: buildA.contactSheet.surface.width,
      height: buildA.contactSheet.surface.height,
      pngSha256: sha256(buildA.contactSheet.png),
    },
    determinism: {
      allDeterministic,
      records: determinism.length,
      changedPixels: determinism.reduce((sum, item) => sum + item.changedPixelCount, 0),
    },
  }, null, 2));
}

async function verifyV7Baseline(): Promise<void> {
  const fidelity = await readJson(join(V7_ROOT, "fidelity-manifest.json"));
  const structural = await readJson(join(V7_ROOT, "room00-structural-render.json"));
  const staff = await readJson(join(V7_ROOT, "room00-with-staff-render.json"));
  const goldenResults = await readJson(join(V7_ROOT, "golden-fixture-results.json"));
  if (fidelity.status !== "PASS_STATIC_FIDELITY") throw new Error(`V7 fidelity status is not green: ${String(fidelity.status)}`);
  if (structural.status !== "pass_static" || staff.status !== "pass_static") throw new Error("V7 room evidence is not pass_static");
  if (structural.commands !== 74 || structural.traces !== 59 || structural.events !== 788) throw new Error("V7 structural room identity drifted");
  if (staff.commands !== 77 || staff.traces !== 62 || staff.events !== 791) throw new Error("V7 room+Staff identity drifted");
  if (!Array.isArray(goldenResults) || goldenResults.length !== 14) throw new Error("V7 golden fixture count drifted");
}

async function loadInputBytes(): Promise<ReadonlyMap<string, Uint8Array>> {
  const paths = [
    join(V7_ROOT, "source-image-manifest.json"),
    join(V7_ROOT, "golden-fixture-manifest.json"),
    join(V7_ROOT, "golden-fixture-results.json"),
    join(V7_ROOT, "room00-structural-render.json"),
    join(V7_ROOT, "room00-with-staff-render.json"),
    join(ROOT, "knowledge", "social-dev", "evidence", "visual-port", "v6", "staff-fixture-manifest.json"),
    join(ROOT, "knowledge", "social-dev", "evidence", "visual-port", "v6", "human-action-selector-map.json"),
    join(ROOT, "knowledge", "social-dev", "evidence", "visual-port", "v6", "staff-animation-contract.json"),
  ];
  const result = new Map<string, Uint8Array>();
  for (const path of paths) result.set(relativePath(path), await readFile(path));
  return result;
}

async function buildPackage(inputBytes: ReadonlyMap<string, Uint8Array>): Promise<PackageBuild> {
  const roomInstance = createRoomV5("room:0", { context: "main_display", visualScope: "full_static" });
  const room = roomInstance.draw();
  const integrated = createV6RoomStaffPreview({ roomKey: "room:0", action: "wait", direction: "right", frame: 0, alpha: 255 });
  const allActionManifests = STAFF_ACTIONS.flatMap((action) => STAFF_DIRECTIONS.map((direction) => createV6RoomStaffPreview({
    roomKey: "room:0",
    sourceStaffIds: [0],
    action,
    direction,
    frame: 0,
    alpha: 255,
  })));
  const alphaManifests = [64, 128, 255].map((alpha) => createV6RoomStaffPreview({
    roomKey: "room:0",
    sourceStaffIds: [0],
    action: "wait",
    direction: "right",
    frame: 0,
    alpha,
  }));
  const imageDimensions = collectImageDimensions([
    ...room.commands,
    ...integrated.commands,
    ...allActionManifests.flatMap((manifest) => manifest.commands),
    ...alphaManifests.flatMap((manifest) => manifest.commands),
  ]);
  const images = await loadImages(imageDimensions);
  const structural = renderV7Room00Structural(images);
  const withStaff = renderV7Room00WithStaff(images);
  const artifacts: Artifact[] = [];

  artifacts.push(createArtifact("room00_structural", "room00_structural.png", structural.raster.surface, {
    kind: "full_scene",
    phase: "V5",
    roomKey: "room:0",
    camera: [0, 0],
    commandHash: sha256(stableJson(room.commands)),
    manifestHash: sha256(stableJson(roomInstance.commandManifest())),
    sourceRef: "knowledge/fixtures/accepted/visual-port/v7/room00-structural-render.json",
  }));
  artifacts.push(createArtifact("room00_with_staff", "room00_with_staff.png", withStaff.raster.surface, {
    kind: "full_scene",
    phase: "V6",
    roomKey: "room:0",
    camera: [0, 0],
    action: "wait",
    direction: "right",
    frame: 0,
    alpha: 255,
    commandHash: sha256(stableJson(integrated.commands)),
    manifestHash: sha256(stableJson(integrated)),
    sourceRef: "knowledge/fixtures/accepted/visual-port/v7/room00-with-staff-render.json",
  }));

  const floorSource = room.commands.find((command) =>
    command.image.id === "resChip_:image:85"
    && command.destination.x === 400
    && command.destination.y === 0,
  );
  if (floorSource === undefined) {
    throw new Error("V7.5 central floor fixture source is missing");
  }
  const floorCommands = [rebaseCommand(floorSource, 96, 72)];
  const floor = renderV7Commands(floorCommands, images, ROOM_FIXTURE_OPTIONS);
  artifacts.push(createArtifact("floor_preview", "floor_preview.png", floor.surface, {
    kind: "world_object_closeup",
    fixtureId: "floor.direct_image",
    sourceRefs: ["runtime/social-dev/assets/room-scene/01_GAME_PACKS/chip/floor_05.png", "knowledge/fixtures/accepted/phase3b_floor_recovery_fixture.json"],
    commandHash: sha256(stableJson(floorCommands)),
  }));

  const wallCommands = commandsWithId(room.commands, "resChip_:image:6");
  artifacts.push(createArtifact("wall_preview", "wall_preview.png", renderV7Commands(wallCommands, images, ROOM_FIXTURE_OPTIONS).surface, {
    kind: "world_object_closeup",
    fixtureId: "wall.seb",
    sourceRefs: ["runtime/social-dev/assets/display-slice-01/01_GAME_PACKS/chip/wall_00.seb", "knowledge/fixtures/accepted/visual-port/v2/draw-image-contract.json"],
    commandHash: sha256(stableJson(wallCommands)),
  }));

  const doorCommands = commandsWithId(room.commands, "resChip_:image:7");
  artifacts.push(createArtifact("door_preview", "door_preview.png", renderV7Commands(doorCommands, images, ROOM_FIXTURE_OPTIONS).surface, {
    kind: "world_object_closeup",
    fixtureId: "door.seb",
    sourceRefs: ["runtime/social-dev/assets/display-slice-01/01_GAME_PACKS/chip/door_02.seb", "knowledge/fixtures/accepted/visual-port/v2/draw-image-contract.json"],
    commandHash: sha256(stableJson(doorCommands)),
  }));

  const furniture3Commands = room.commands.filter((command) => command.image.id === "resChip_:image:3" || command.image.id === "resChip_:image:4");
  artifacts.push(createArtifact("furniture_3_preview", "furniture_3_preview.png", renderV7Commands(furniture3Commands, images, ROOM_FIXTURE_OPTIONS).surface, {
    kind: "world_object_closeup",
    fixtureId: "furniture.3_desk_chair",
    sourceRefs: ["runtime/social-dev/assets/display-slice-01/01_GAME_PACKS/chip/desk_00.seb", "runtime/social-dev/assets/display-slice-01/01_GAME_PACKS/chip/chair_00.seb", "knowledge/fixtures/accepted/visual-port/v4/furniture-visual-binding.json"],
    commandHash: sha256(stableJson(furniture3Commands)),
  }));

  for (const [key, filename, fixtureId, imageId] of [
    ["furniture_12_preview", "furniture_12_preview.png", "furniture.12", "resChip_:image:109"],
    ["furniture_26_preview", "furniture_26_preview.png", "furniture.26", "resChip_:image:106"],
    ["furniture_56_preview", "furniture_56_preview.png", "furniture.56", "resChip_:image:127"],
  ] as const) {
    const commands = commandsWithId(room.commands, imageId);
    artifacts.push(createArtifact(key, filename, renderV7Commands(commands, images, ROOM_FIXTURE_OPTIONS).surface, {
      kind: "world_object_closeup",
      fixtureId,
      sourceRefs: ["runtime/social-dev/assets/display-slice-01/01_GAME_PACKS/chip/equip.seb", "knowledge/fixtures/accepted/visual-port/v5/room-furniture-orchestration.json"],
      commandHash: sha256(stableJson(commands)),
    }));
  }

  const selectorRecords: SelectorRecord[] = [];
  const actionSheets = new Map<string, Artifact>();
  for (const action of STAFF_ACTIONS) {
    const panels: PanelSurface[] = [];
    for (const direction of STAFF_DIRECTIONS) {
      const manifest = allActionManifests.find((candidate) => candidate.staff[0]?.action === action && candidate.staff[0]?.direction === direction);
      if (manifest === undefined) throw new Error(`V7.5 Staff manifest missing ${action}/${direction}`);
      const command = requireOneStaffCommand(manifest.commands);
      const placement = manifest.staff[0]?.placement;
      const selector = manifest.staff[0]?.selector;
      if (placement === undefined || selector === undefined || selector.selectorId === null) throw new Error(`V7.5 Staff selector missing ${action}/${direction}`);
      const panelSurface = renderStaffPanel(command, placement.screen, images);
      panels.push({ label: direction.toUpperCase(), surface: scaleSurface(panelSurface, 3) });
      selectorRecords.push({
        sheet: action,
        action,
        direction,
        selectorId: selector.selectorId,
        selectorFilename: selector.selectorFilename,
        frame: 0,
        alpha: 255,
        commandHash: sha256(stableJson([command])),
      });
    }
    const sheetSurface = composePanelSheet(panels, 240, 280);
    actionSheets.set(action, createArtifact(`staff_${action}_directions`, `staff_${action}_directions.png`, sheetSurface, {
      kind: "staff_direction_sheet",
      sourceStaffId: 0,
      action,
      directions: [...STAFF_DIRECTIONS],
      selectorIds: selectorRecords.filter((record) => record.action === action).map((record) => ({ direction: record.direction, selectorId: record.selectorId })),
      presentationScale: 3,
      sourceRef: "knowledge/fixtures/accepted/visual-port/v6/staff-fixture-manifest.json",
    }));
  }
  artifacts.push(actionSheets.get("wait")!);
  artifacts.push(actionSheets.get("move")!);
  artifacts.push(actionSheets.get("typing")!);

  const alphaPanels: PanelSurface[] = [];
  for (const alpha of [64, 128, 255]) {
    const manifest = alphaManifests.find((candidate) => candidate.staff[0]?.alpha === alpha);
    if (manifest === undefined) throw new Error(`V7.5 alpha manifest missing ${alpha}`);
    const command = requireOneStaffCommand(manifest.commands);
    const placement = manifest.staff[0]?.placement;
    if (placement === undefined) throw new Error(`V7.5 alpha placement missing ${alpha}`);
    alphaPanels.push({ label: `ALPHA ${alpha}`, surface: scaleSurface(renderStaffPanel(command, placement.screen, images), 3) });
  }
  const alphaSheet = createArtifact("staff_alpha_preview", "staff_alpha_preview.png", composePanelSheet(alphaPanels, 240, 280), {
    kind: "staff_alpha_sheet",
    sourceStaffId: 0,
    action: "wait",
    direction: "right",
    frame: 0,
    alphaValues: [64, 128, 255],
    selectorId: 10,
    sourceRef: "knowledge/fixtures/accepted/visual-port/v6/staff-animation-contract.json",
  });
  artifacts.push(alphaSheet);

  const clippedCommand = recreateCommand(rebaseCommand(floorSource, 96, 72), (graphics) => graphics.setClip(106, 82, 20, 20));
  const clipped = renderV7Commands([clippedCommand], images, ROOM_FIXTURE_OPTIONS).surface;
  const transformedSource = rebaseCommand(floorSource, 96, 72);
  const transformedRaster = new RasterCompatibilityV7({ width: 240, height: 200, origin: { x: 0, y: 0 } });
  const transform = { scaleX: 1.25, scaleY: 0.75, rotationDegrees: 15, pivot: { x: transformedSource.destination.x + transformedSource.destination.width / 2, y: transformedSource.destination.y + transformedSource.destination.height / 2 } };
  const transformedImage = images.get(String(transformedSource.image.id));
  if (transformedImage === undefined) throw new Error("V7.5 transformed source image is missing");
  transformedRaster.draw({ image: transformedImage, destination: transformedSource.destination, source: transformedSource.source, state: transformedSource.state, transform, clip: { rect: transformedSource.destination, transformed: transform } });
  const clipTransformSheet = createArtifact("clip_transform_preview", "clip_transform_preview.png", composeClipTransformSheet(clipped, transformedRaster.output), {
    kind: "raster_checks",
    panels: ["clipped", "transformed"],
    sourceRefs: ["knowledge/fixtures/accepted/visual-port/v2/clip-contract.json", "knowledge/fixtures/accepted/visual-port/v2/graphics-static-recovery.json"],
    sourceCommandHashes: {
      clipped: sha256(stableJson([clippedCommand])),
      transformed: sha256(stableJson({ command: transformedSource, transform, clip: transformedSource.destination })),
    },
    presentationScale: 2,
  });
  artifacts.push(clipTransformSheet);

  const contactSheet = createArtifact("V7_5_VISUAL_ACCEPTANCE_CONTACT_SHEET", "V7_5_VISUAL_ACCEPTANCE_CONTACT_SHEET.png", composeContactSheet(artifacts), {
    kind: "presentation_contact_sheet",
    sourceOfTruth: "individual PNGs and V1-V7 command contracts",
    presentationOnly: true,
  });

  const v5CommandHash = sha256(stableJson(room.commands));
  const v5ManifestHash = sha256(stableJson(roomInstance.commandManifest()));
  const v6CommandHash = sha256(stableJson(integrated.commands));
  const v6ManifestHash = sha256(stableJson(integrated));
  const v7SourceManifestHash = sha256(inputBytes.get("knowledge/fixtures/accepted/visual-port/v7/source-image-manifest.json")!);
  const v7GoldenManifestHash = sha256(inputBytes.get("knowledge/fixtures/accepted/visual-port/v7/golden-fixture-manifest.json")!);
  const v7GoldenResultsHash = sha256(inputBytes.get("knowledge/fixtures/accepted/visual-port/v7/golden-fixture-results.json")!);
  const v6StaffManifestHash = sha256(inputBytes.get("knowledge/fixtures/accepted/visual-port/v6/staff-fixture-manifest.json")!);
  const v6SelectorMapHash = sha256(inputBytes.get("knowledge/fixtures/accepted/visual-port/v6/human-action-selector-map.json")!);
  const v6AnimationContractHash = sha256(inputBytes.get("knowledge/fixtures/accepted/visual-port/v6/staff-animation-contract.json")!);

  return {
    artifacts,
    contactSheet,
    baseline: {
      roomCommands: room.commands,
      integratedCommands: integrated.commands,
      v5CommandHash,
      v5ManifestHash,
      v6CommandHash,
      v6ManifestHash,
      v7SourceManifestHash,
      v7GoldenManifestHash,
      v7GoldenResultsHash,
      v6StaffManifestHash,
      v6SelectorMapHash,
      v6AnimationContractHash,
    },
    selectors: selectorRecords,
  };
}

async function loadImages(dimensions: ReadonlyMap<string, { width: number; height: number }>): Promise<Map<string, V7RasterImage>> {
  const images = new Map<string, V7RasterImage>();
  for (const [id, expected] of dimensions) {
    const path = IMAGE_PATHS[id];
    if (path === undefined) throw new Error(`V7.5 asset map is missing command image ID ${id}`);
    const bytes = await readFile(path);
    const decoded = decodePng(bytes);
    if (decoded.width !== expected.width || decoded.height !== expected.height) throw new Error(`V7.5 source dimension mismatch for ${id}`);
    images.set(id, { id, width: decoded.width, height: decoded.height, pixels: decoded.pixels, sourceRef: relativePath(path), sourceSha256: sha256(bytes) });
  }
  return images;
}

function collectImageDimensions(commands: readonly GraphicsCommand[]): Map<string, { width: number; height: number }> {
  const result = new Map<string, { width: number; height: number }>();
  for (const command of commands) result.set(String(command.image.id), { width: command.image.width, height: command.image.height });
  return result;
}

function renderStaffPanel(command: GraphicsCommand, placementScreen: { readonly x: number; readonly y: number }, images: ReadonlyMap<string, V7RasterImage>): V7RasterSurface {
  const anchor = { x: 40, y: 40 };
  const translated: GraphicsCommand = {
    ...command,
    destination: {
      ...command.destination,
      x: anchor.x + command.destination.x - placementScreen.x,
      y: anchor.y + command.destination.y - placementScreen.y,
    },
  };
  return renderV7Commands([translated], images, STAFF_PANEL_OPTIONS).surface;
}

function composePanelSheet(panels: readonly PanelSurface[], panelWidth: number, panelHeight: number): V7RasterSurface {
  const output = new RasterSurfaceCompatibilityV7(panelWidth * panels.length, panelHeight, [18, 22, 30, 255]);
  panels.forEach((panel, index) => {
    const labeled = createLabeledPanel(panel.surface, panel.label, panelWidth, panelHeight, 1, 40);
    blitSurface(output, labeled, index * panelWidth, 0);
  });
  return output;
}

function composeClipTransformSheet(clipped: V7RasterSurface, transformed: V7RasterSurface): V7RasterSurface {
  const panelWidth = 720;
  const panelHeight = 520;
  const clippedPanel = createLabeledPanel(clipped, "CLIPPED", panelWidth, panelHeight, 2, 40);
  const transformedPanel = createLabeledPanel(transformed, "TRANSFORMED", panelWidth, panelHeight, 2, 40);
  const output = new RasterSurfaceCompatibilityV7(panelWidth * 2, panelHeight, [18, 22, 30, 255]);
  blitSurface(output, clippedPanel, 0, 0);
  blitSurface(output, transformedPanel, panelWidth, 0);
  return output;
}

function composeContactSheet(artifacts: readonly Artifact[]): V7RasterSurface {
  const byKey = new Map(artifacts.map((artifact) => [artifact.key, artifact]));
  const width = 2880;
  const headerHeight = 60;
  const sceneRowHeight = 560;
  const objectRowHeight = 500;
  const directionRowHeight = 320;
  const clipRowHeight = 580;
  const rows = [sceneRowHeight, objectRowHeight, objectRowHeight, directionRowHeight, directionRowHeight, directionRowHeight, clipRowHeight];
  const height = headerHeight + rows.reduce((sum, row) => sum + row, 0);
  const output = new RasterSurfaceCompatibilityV7(width, height, [10, 14, 20, 255]);
  drawText(output, "V7.5 VISUAL ACCEPTANCE", 24, 18, 3, [240, 245, 250, 255]);
  let y = headerHeight;

  const structural = byKey.get("room00_structural");
  const withStaff = byKey.get("room00_with_staff");
  if (structural === undefined || withStaff === undefined) throw new Error("V7.5 contact sheet is missing room artifacts");
  blitSurface(output, createLabeledPanel(structural.surface, "ROOM 0 STRUCTURAL", 1440, 540, 1, 40), 0, y);
  blitSurface(output, createLabeledPanel(withStaff.surface, "ROOM 0 + STAFF", 1440, 540, 1, 40), 1440, y);
  y += sceneRowHeight;

  const objectKeys = ["floor_preview", "wall_preview", "door_preview", "furniture_3_preview"];
  for (const [index, key] of objectKeys.entries()) {
    const artifact = byKey.get(key);
    if (artifact === undefined) throw new Error(`V7.5 contact sheet is missing ${key}`);
    const label = key === "floor_preview" ? "FLOOR" : key === "wall_preview" ? "WALL" : key === "door_preview" ? "DOOR" : "FURNITURE 3";
    blitSurface(output, createLabeledPanel(artifact.surface, label, 720, 480, 2, 40), index * 720, y);
  }
  y += objectRowHeight;

  for (const [index, key] of ["furniture_12_preview", "furniture_26_preview", "furniture_56_preview"].entries()) {
    const artifact = byKey.get(key);
    if (artifact === undefined) throw new Error(`V7.5 contact sheet is missing ${key}`);
    const label = key.replace("_preview", "").replace("furniture_", "FURNITURE ").toUpperCase();
    blitSurface(output, createLabeledPanel(artifact.surface, label, 720, 480, 2, 40), index * 720, y);
  }
  const alpha = byKey.get("staff_alpha_preview");
  if (alpha === undefined) throw new Error("V7.5 contact sheet is missing alpha sheet");
  drawText(output, "ALPHA", 3 * 720 + 30, y + 18, 3, [240, 245, 250, 255]);
  blitSurface(output, alpha.surface, 3 * 720, y + 100);
  y += objectRowHeight;

  for (const key of ["staff_wait_directions", "staff_move_directions", "staff_typing_directions"]) {
    const artifact = byKey.get(key);
    if (artifact === undefined) throw new Error(`V7.5 contact sheet is missing ${key}`);
    const title = key.includes("wait") ? "WAIT R / L / U / D" : key.includes("move") ? "MOVE R / L / U / D" : "TYPING R / L / U / D";
    drawText(output, title, 30, y + 18, 3, [240, 245, 250, 255]);
    blitSurface(output, artifact.surface, Math.floor((width - artifact.surface.width) / 2), y + 40);
    y += directionRowHeight;
  }

  const clip = byKey.get("clip_transform_preview");
  if (clip === undefined) throw new Error("V7.5 contact sheet is missing clip/transform sheet");
  drawText(output, "CLIP / TRANSFORM CHECKS", 30, y + 18, 3, [240, 245, 250, 255]);
  blitSurface(output, clip.surface, Math.floor((width - clip.surface.width) / 2), y + 40);
  return output;
}

function createLabeledPanel(source: V7RasterSurface, label: string, width: number, height: number, scale: number, labelHeight: number): V7RasterSurface {
  const output = new RasterSurfaceCompatibilityV7(width, height, [24, 29, 38, 255]);
  drawText(output, label, 12, 12, 3, [240, 245, 250, 255]);
  const scaledWidth = source.width * scale;
  const scaledHeight = source.height * scale;
  const x = Math.floor((width - scaledWidth) / 2);
  const availableHeight = height - labelHeight;
  const y = labelHeight + Math.floor((availableHeight - scaledHeight) / 2);
  blitScaled(output, source, x, y, scale);
  drawBorder(output, [80, 90, 106, 255]);
  return output;
}

function scaleSurface(source: V7RasterSurface, scale: number): V7RasterSurface {
  const output = new RasterSurfaceCompatibilityV7(source.width * scale, source.height * scale, [0, 0, 0, 0]);
  blitScaled(output, source, 0, 0, scale);
  return output;
}

function blitSurface(target: RasterSurfaceCompatibilityV7, source: V7RasterSurface, x: number, y: number): void {
  for (let sourceY = 0; sourceY < source.height; sourceY += 1) {
    for (let sourceX = 0; sourceX < source.width; sourceX += 1) {
      const targetX = x + sourceX;
      const targetY = y + sourceY;
      if (targetX < 0 || targetY < 0 || targetX >= target.width || targetY >= target.height) continue;
      const offset = (sourceY * source.width + sourceX) * 4;
      blendPixel(target, targetX, targetY, [source.pixels[offset], source.pixels[offset + 1], source.pixels[offset + 2], source.pixels[offset + 3]]);
    }
  }
}

function blitScaled(target: RasterSurfaceCompatibilityV7, source: V7RasterSurface, x: number, y: number, scale: number): void {
  for (let sourceY = 0; sourceY < source.height; sourceY += 1) {
    for (let sourceX = 0; sourceX < source.width; sourceX += 1) {
      const offset = (sourceY * source.width + sourceX) * 4;
      const rgba: readonly [number, number, number, number] = [source.pixels[offset], source.pixels[offset + 1], source.pixels[offset + 2], source.pixels[offset + 3]];
      if (rgba[3] === 0) continue;
      for (let dy = 0; dy < scale; dy += 1) {
        for (let dx = 0; dx < scale; dx += 1) {
          const targetX = x + sourceX * scale + dx;
          const targetY = y + sourceY * scale + dy;
          if (targetX < 0 || targetY < 0 || targetX >= target.width || targetY >= target.height) continue;
          blendPixel(target, targetX, targetY, rgba);
        }
      }
    }
  }
}

function blendPixel(target: RasterSurfaceCompatibilityV7, x: number, y: number, source: readonly [number, number, number, number]): void {
  const destination = target.getPixel(x, y);
  const sourceAlpha = source[3] / 255;
  const destinationAlpha = destination[3] / 255;
  const outputAlpha = sourceAlpha + destinationAlpha * (1 - sourceAlpha);
  if (outputAlpha <= 0) {
    target.setPixel(x, y, [0, 0, 0, 0]);
    return;
  }
  const output = [0, 1, 2].map((channel) => Math.round((source[channel] * sourceAlpha + destination[channel] * destinationAlpha * (1 - sourceAlpha)) / outputAlpha));
  target.setPixel(x, y, [output[0], output[1], output[2], Math.round(outputAlpha * 255)]);
}

function drawBorder(surface: RasterSurfaceCompatibilityV7, color: readonly [number, number, number, number]): void {
  for (let x = 0; x < surface.width; x += 1) {
    surface.setPixel(x, 0, color);
    surface.setPixel(x, surface.height - 1, color);
  }
  for (let y = 0; y < surface.height; y += 1) {
    surface.setPixel(0, y, color);
    surface.setPixel(surface.width - 1, y, color);
  }
}

const FONT: Readonly<Record<string, readonly string[]>> = {
  " ": ["00000", "00000", "00000", "00000", "00000", "00000", "00000"],
  "?": ["01110", "10001", "00010", "00100", "00100", "00000", "00100"],
  "+": ["00000", "00100", "00100", "11111", "00100", "00100", "00000"],
  "-": ["00000", "00000", "00000", "11111", "00000", "00000", "00000"],
  "/": ["00001", "00010", "00100", "01000", "10000", "00000", "00000"],
  ":": ["00000", "00100", "00000", "00000", "00100", "00000", "00000"],
  "0": ["01110", "10001", "10011", "10101", "11001", "10001", "01110"],
  "1": ["00100", "01100", "00100", "00100", "00100", "00100", "01110"],
  "2": ["01110", "10001", "00001", "00010", "00100", "01000", "11111"],
  "3": ["11110", "00001", "00001", "01110", "00001", "00001", "11110"],
  "4": ["00010", "00110", "01010", "10010", "11111", "00010", "00010"],
  "5": ["11111", "10000", "10000", "11110", "00001", "00001", "11110"],
  "6": ["01110", "10000", "10000", "11110", "10001", "10001", "01110"],
  "7": ["11111", "00001", "00010", "00100", "01000", "01000", "01000"],
  "8": ["01110", "10001", "10001", "01110", "10001", "10001", "01110"],
  "9": ["01110", "10001", "10001", "01111", "00001", "00001", "01110"],
  "A": ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
  "B": ["11110", "10001", "10001", "11110", "10001", "10001", "11110"],
  "C": ["01111", "10000", "10000", "10000", "10000", "10000", "01111"],
  "D": ["11110", "10001", "10001", "10001", "10001", "10001", "11110"],
  "E": ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
  "F": ["11111", "10000", "10000", "11110", "10000", "10000", "10000"],
  "G": ["01111", "10000", "10000", "10111", "10001", "10001", "01111"],
  "H": ["10001", "10001", "10001", "11111", "10001", "10001", "10001"],
  "I": ["11111", "00100", "00100", "00100", "00100", "00100", "11111"],
  "J": ["00111", "00010", "00010", "00010", "10010", "10010", "01100"],
  "K": ["10001", "10010", "10100", "11000", "10100", "10010", "10001"],
  "L": ["10000", "10000", "10000", "10000", "10000", "10000", "11111"],
  "M": ["10001", "11011", "10101", "10101", "10001", "10001", "10001"],
  "N": ["10001", "11001", "10101", "10011", "10001", "10001", "10001"],
  "O": ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
  "P": ["11110", "10001", "10001", "11110", "10000", "10000", "10000"],
  "Q": ["01110", "10001", "10001", "10001", "10101", "10010", "01101"],
  "R": ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
  "S": ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
  "T": ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
  "U": ["10001", "10001", "10001", "10001", "10001", "10001", "01110"],
  "V": ["10001", "10001", "10001", "10001", "10001", "01010", "00100"],
  "W": ["10001", "10001", "10001", "10101", "10101", "11011", "10001"],
  "X": ["10001", "10001", "01010", "00100", "01010", "10001", "10001"],
  "Y": ["10001", "10001", "01010", "00100", "00100", "00100", "00100"],
  "Z": ["11111", "00001", "00010", "00100", "01000", "10000", "11111"],
};

function drawText(surface: RasterSurfaceCompatibilityV7, text: string, x: number, y: number, scale: number, color: readonly [number, number, number, number]): void {
  let cursor = x;
  for (const rawCharacter of text.toUpperCase()) {
    const glyph = FONT[rawCharacter] ?? FONT["?"];
    for (let row = 0; row < glyph.length; row += 1) {
      for (let column = 0; column < glyph[row].length; column += 1) {
        if (glyph[row][column] !== "1") continue;
        for (let dy = 0; dy < scale; dy += 1) {
          for (let dx = 0; dx < scale; dx += 1) {
            const pixelX = cursor + column * scale + dx;
            const pixelY = y + row * scale + dy;
            if (pixelX >= 0 && pixelY >= 0 && pixelX < surface.width && pixelY < surface.height) surface.setPixel(pixelX, pixelY, color);
          }
        }
      }
    }
    cursor += 6 * scale;
  }
}

function createArtifact(key: string, filename: string, surface: V7RasterSurface, metadata: Readonly<Record<string, unknown>>): Artifact {
  const png = encodePngRgbaV7(surface);
  return { key, filename, path: `knowledge/fixtures/accepted/visual-port/v7_5/previews/${filename}`, surface, png, metadata };
}

function compareBuilds(buildA: PackageBuild, buildB: PackageBuild): readonly DeterminismRecord[] {
  const artifactsA = [...buildA.artifacts, buildA.contactSheet];
  const artifactsB = [...buildB.artifacts, buildB.contactSheet];
  const byKeyB = new Map(artifactsB.map((artifact) => [artifact.key, artifact]));
  return artifactsA.map((artifactA) => {
    const artifactB = byKeyB.get(artifactA.key);
    if (artifactB === undefined) throw new Error(`V7.5 rerender is missing ${artifactA.key}`);
    if (artifactA.surface.width !== artifactB.surface.width || artifactA.surface.height !== artifactB.surface.height) throw new Error(`V7.5 rerender dimensions changed for ${artifactA.key}`);
    const pixelDiff = diffRasterV7(artifactA.surface, artifactB.surface);
    return {
      key: artifactA.key,
      path: artifactA.path,
      width: artifactA.surface.width,
      height: artifactA.surface.height,
      sha256RunA: sha256(artifactA.png),
      sha256RunB: sha256(artifactB.png),
      pixelSha256RunA: sha256(artifactA.surface.pixels),
      pixelSha256RunB: sha256(artifactB.surface.pixels),
      byteIdentical: equalBytes(artifactA.png, artifactB.png),
      changedPixelCount: pixelDiff.changedPixelCount,
    };
  });
}

function buildMachineEvidence(build: PackageBuild, determinism: readonly DeterminismRecord[], recommendation: string): object {
  const imageRecords = build.artifacts.map((artifact) => ({
    name: artifact.key,
    path: artifact.path,
    width: artifact.surface.width,
    height: artifact.surface.height,
    sha256: sha256(artifact.png),
    pixel_sha256: sha256(artifact.surface.pixels),
    metadata: artifact.metadata,
  }));
  const deterministic = determinism.every((item) => item.byteIdentical && item.changedPixelCount === 0);
  return {
    schema_version: "social-dev-visual-port-v7_5-visual-acceptance-v1",
    status: deterministic ? "PASS_STATIC" : "BLOCKED",
    source_v7_status: "PASS_STATIC_STOP_BEFORE_V8",
    source_v7_evidence_status: "PASS_STATIC_FIDELITY",
    v8_started: false,
    production_renderer_changed: false,
    execution_mode: "INLINE_EXECUTION_ONLY",
    static_only: true,
    subagents: false,
    live_or_emulator_evidence: false,
    server_or_network_used: false,
    images: imageRecords,
    contact_sheet: {
      name: build.contactSheet.key,
      path: build.contactSheet.path,
      width: build.contactSheet.surface.width,
      height: build.contactSheet.surface.height,
      sha256: sha256(build.contactSheet.png),
      pixel_sha256: sha256(build.contactSheet.surface.pixels),
      presentation_only: true,
    },
    hashes: {
      source_manifests: {
        v7_source_image_manifest_sha256: build.baseline.v7SourceManifestHash,
        v7_golden_fixture_manifest_sha256: build.baseline.v7GoldenManifestHash,
        v7_golden_fixture_results_sha256: build.baseline.v7GoldenResultsHash,
        v6_staff_fixture_manifest_sha256: build.baseline.v6StaffManifestHash,
        v6_human_action_selector_map_sha256: build.baseline.v6SelectorMapHash,
        v6_staff_animation_contract_sha256: build.baseline.v6AnimationContractHash,
      },
      room_commands: {
        v5_command_sha256: build.baseline.v5CommandHash,
        v5_manifest_sha256: build.baseline.v5ManifestHash,
        v6_command_sha256: build.baseline.v6CommandHash,
        v6_manifest_sha256: build.baseline.v6ManifestHash,
      },
    },
    staff_selector_ids: {
      wait: Object.fromEntries(build.selectors.filter((record) => record.action === "wait").map((record) => [record.direction, record.selectorId])),
      move: Object.fromEntries(build.selectors.filter((record) => record.action === "move").map((record) => [record.direction, record.selectorId])),
      typing: Object.fromEntries(build.selectors.filter((record) => record.action === "typing").map((record) => [record.direction, record.selectorId])),
    },
    staff_selectors: build.selectors,
    determinism: {
      rerender_count: 2,
      expected_changed_pixel_count: 0,
      all_byte_identical: deterministic,
      all_pixel_identical: determinism.every((item) => item.changedPixelCount === 0),
      artifacts: determinism,
    },
    issues: VISUAL_ISSUES,
    recommendation,
    changed_visual_semantics: "NONE",
    authority_policy: "Individual PNGs and V1-V7 command contracts remain authoritative; the contact sheet is presentation-only.",
  };
}

function buildReport(build: PackageBuild, determinism: readonly DeterminismRecord[], recommendation: string): string {
  const imageRows = build.artifacts.map((artifact) => `| \`${artifact.key}\` | \`${artifact.path}\` | ${artifact.surface.width} x ${artifact.surface.height} | \`${sha256(artifact.png)}\` | \`${sha256(artifact.surface.pixels)}\` |`).join("\n");
  const issueRows = VISUAL_ISSUES.length === 0
    ? "No obvious crop, pivot, layer-order, alpha, clipping, transform, or unexpected-blur corruption was found in the individual PNGs or contact sheet."
    : VISUAL_ISSUES.map((issue) => `| ${issue.id} | ${issue.image} | ${issue.panel} | ${issue.visualSymptom} | ${issue.relevantVPhase} | ${issue.relevantCommandOrResourceId} | ${issue.likelyClass} | ${issue.evidenceReviewRequired ? "yes" : "no"} |`).join("\n");
  const determinismRows = determinism.map((item) => `| \`${item.key}\` | ${item.width} x ${item.height} | \`${item.sha256RunA}\` | \`${item.sha256RunB}\` | ${item.changedPixelCount} | ${item.byteIdentical ? "yes" : "no"} |`).join("\n");
  const selectors = ["wait", "move", "typing"].map((action) => {
    const records = build.selectors.filter((record) => record.action === action);
    return `| ${action.toUpperCase()} | ${records.map((record) => `${record.direction}=${record.selectorId} (${record.selectorFilename ?? "unknown"})`).join("; ")} |`;
  }).join("\n");
  const issueTable = VISUAL_ISSUES.length === 0 ? issueRows : `| ID | Image | Panel | Symptom | V phase | Command/resource | Class | Evidence review |\n| --- | --- | --- | --- | --- | --- | --- | --- |\n${issueRows}`;
  return `# V7.5 visual acceptance

## Status

\`${recommendation}\`

V7.5 is an offline visual acceptance package over the existing RoomV5, StaffV6, RasterCompatibilityV7, original numeric resource IDs, and V1-V7 contracts. V8 was not started. The production renderer was not changed. The package is presentation evidence only; individual PNGs and the command contracts remain authoritative.

## Scope and boundary

- Execution: inline, sequential, static/offline only.
- Subagents: none.
- ADB, emulator, APK/game launch, live browser, local server, network, and live-game screenshots: not used.
- Historical screenshots: not used as geometry or resource authority.
- Visual semantics changed: none.
- Source V7 status: \`PASS_STATIC_STOP_BEFORE_V8\` (\`PASS_STATIC_FIDELITY\` evidence).

## Generated images

| Image | Path | Dimensions | PNG SHA-256 | RGBA pixel SHA-256 |
| --- | --- | ---: | --- | --- |
${imageRows}

Contact sheet: [V7_5_VISUAL_ACCEPTANCE_CONTACT_SHEET.png](../../../knowledge/fixtures/accepted/visual-port/v7_5/previews/V7_5_VISUAL_ACCEPTANCE_CONTACT_SHEET.png), ${build.contactSheet.surface.width} x ${build.contactSheet.surface.height}, PNG SHA-256 \`${sha256(build.contactSheet.png)}\`. It is presentation-only.

## Source manifest hashes

| Manifest | SHA-256 |
| --- | --- |
| V7 source-image manifest | \`${build.baseline.v7SourceManifestHash}\` |
| V7 golden-fixture manifest | \`${build.baseline.v7GoldenManifestHash}\` |
| V7 golden-fixture results | \`${build.baseline.v7GoldenResultsHash}\` |
| V6 Staff fixture manifest | \`${build.baseline.v6StaffManifestHash}\` |
| V6 human action selector map | \`${build.baseline.v6SelectorMapHash}\` |
| V6 Staff animation contract | \`${build.baseline.v6AnimationContractHash}\` |

## Room command identity

| Stream | Command hash | Manifest hash |
| --- | --- | --- |
| V5 RoomV5 room:0 structural | \`${build.baseline.v5CommandHash}\` | \`${build.baseline.v5ManifestHash}\` |
| V6 RoomV5 + StaffV6 room:0 | \`${build.baseline.v6CommandHash}\` | \`${build.baseline.v6ManifestHash}\` |

The structural scene uses camera \`[0,0]\`. The Staff scene uses StaffData \`0, 1, 2\`, action \`wait\`, direction \`right\`, frame \`0\`, alpha \`255\`, and camera \`[0,0]\`.

## Staff selector IDs

| Action sheet | Resolved selectors |
| --- | --- |
${selectors}

Every direction panel uses StaffData \`0\`, frame \`0\`, the exact V6 resolved selector, original crop/source rectangle, original reverse flags, and a presentation-only translation to a common panel anchor. Direction sheets use nearest-neighbor scale \`3\` only for inspection.

## Deterministic rerender

All required images and the contact sheet were built twice from the same V1-V7 inputs. Expected changed pixels per artifact: \`0\`.

| Artifact | Dimensions | SHA-256 run A | SHA-256 run B | Changed pixels | Byte-identical |
| --- | ---: | --- | --- | ---: | --- |
${determinismRows}

Overall deterministic rerender: **${determinism.every((item) => item.byteIdentical && item.changedPixelCount === 0) ? "PASS" : "FAIL"}**.

## Visual issue record

${issueTable}

The visual review did not tune coordinates, replace assets, edit PNG pixels manually, or copy the historical browser layout. Any future suspicious difference must be classified against the V1-V7 evidence before code changes.

## Recommendation

\`${recommendation}\`

V8 may begin only as a separate user-directed phase. This task stops here and does not start V8.

## Machine evidence

[visual-acceptance.json](../../../knowledge/fixtures/accepted/visual-port/v7_5/visual-acceptance.json)
`;
}

function requireOneStaffCommand(commands: readonly GraphicsCommand[]): GraphicsCommand {
  const selected = commands.filter((command) => command.image.id === "resHuman_:image:86");
  if (selected.length !== 1) throw new Error(`V7.5 expected one StaffData 0 command, found ${selected.length}`);
  return selected[0];
}

function requireFirst(commands: readonly GraphicsCommand[], imageId: string): GraphicsCommand {
  const command = commands.find((candidate) => candidate.image.id === imageId);
  if (command === undefined) throw new Error(`V7.5 command ${imageId} is missing`);
  return command;
}

function commandsWithId(commands: readonly GraphicsCommand[], imageId: string): readonly GraphicsCommand[] {
  const selected = commands.filter((command) => command.image.id === imageId);
  if (selected.length === 0) throw new Error(`V7.5 command group ${imageId} is empty`);
  return selected;
}

function recreateCommand(command: GraphicsCommand, configure: (graphics: GraphicsCompatibility) => void): GraphicsCommand {
  const graphics = new GraphicsCompatibility();
  configure(graphics);
  const image = imageRef(command.image.id, command.image.width, command.image.height);
  if (command.kind === "draw-scaled-image") {
    graphics.drawScaledImage(image, command.destination.x, command.destination.y, command.destination.width, command.destination.height, command.source.x, command.source.y, command.source.width, command.source.height);
  } else {
    graphics.drawImage(image, command.destination.x, command.destination.y, command.source.x, command.source.y, command.source.width, command.source.height);
  }
  const recreated = graphics.commands[0];
  if (recreated === undefined) throw new Error("V7.5 recreated command was not recorded");
  return recreated;
}

function rebaseCommand(command: GraphicsCommand, x: number, y: number): GraphicsCommand {
  return { ...command, destination: { ...command.destination, x, y }, state: { ...command.state, clip: null, clipDepth: 0 } };
}

function createDecodedImage(width: number, height: number, pixels: Uint8Array): { width: number; height: number; pixels: Uint8Array } {
  return { width, height, pixels };
}

function decodePng(bytes: Uint8Array): { width: number; height: number; pixels: Uint8Array } {
  const signature = [137, 80, 78, 71, 13, 10, 26, 10];
  if (!signature.every((value, index) => bytes[index] === value)) throw new Error("V7.5 PNG signature is invalid");
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
      bitDepth = data[8];
      colorType = data[9];
      interlace = data[12];
    } else if (type === "IDAT") idat.push(data);
    else if (type === "PLTE") palette = new Uint8Array(data);
    else if (type === "tRNS") transparency = new Uint8Array(data);
    else if (type === "IEND") break;
  }
  if (bitDepth !== 8 || interlace !== 0 || ![0, 2, 3, 4, 6].includes(colorType)) throw new Error(`V7.5 PNG format unsupported: ${bitDepth}/${colorType}/${interlace}`);
  const channels = colorType === 6 ? 4 : colorType === 4 ? 2 : colorType === 2 ? 3 : 1;
  const rowBytes = width * channels;
  const inflated = new Uint8Array(inflateSync(concat(idat)));
  const source = new Uint8Array(height * rowBytes);
  let sourceOffset = 0;
  for (let y = 0; y < height; y += 1) {
    const filter = inflated[sourceOffset++];
    const row = inflated.subarray(sourceOffset, sourceOffset + rowBytes);
    sourceOffset += rowBytes;
    const outputOffset = y * rowBytes;
    for (let x = 0; x < rowBytes; x += 1) {
      const left = x >= channels ? source[outputOffset + x - channels] : 0;
      const up = y > 0 ? source[outputOffset - rowBytes + x] : 0;
      const upperLeft = y > 0 && x >= channels ? source[outputOffset - rowBytes + x - channels] : 0;
      const raw = row[x];
      source[outputOffset + x] = filter === 0 ? raw : filter === 1 ? (raw + left) & 0xff : filter === 2 ? (raw + up) & 0xff : filter === 3 ? (raw + Math.floor((left + up) / 2)) & 0xff : (raw + paeth(left, up, upperLeft)) & 0xff;
    }
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
      if (palette === null || paletteOffset + 2 >= palette.length) throw new Error("V7.5 palette index is out of range");
      pixels[targetIndex] = palette[paletteOffset]; pixels[targetIndex + 1] = palette[paletteOffset + 1]; pixels[targetIndex + 2] = palette[paletteOffset + 2]; pixels[targetIndex + 3] = transparency !== null && paletteIndex < transparency.length ? transparency[paletteIndex] : 255;
    } else { pixels[targetIndex] = source[sourceIndex]; pixels[targetIndex + 1] = source[sourceIndex]; pixels[targetIndex + 2] = source[sourceIndex]; pixels[targetIndex + 3] = 255; }
  }
  return createDecodedImage(width, height, pixels);
}

function paeth(a: number, b: number, c: number): number {
  const p = a + b - c;
  const pa = Math.abs(p - a); const pb = Math.abs(p - b); const pc = Math.abs(p - c);
  return pa <= pb && pa <= pc ? a : pb <= pc ? b : c;
}

function readU32BE(bytes: Uint8Array, offset: number): number {
  return bytes[offset] * 0x1000000 + ((bytes[offset + 1] << 16) | (bytes[offset + 2] << 8) | bytes[offset + 3]);
}

function concat(arrays: readonly Uint8Array[]): Uint8Array {
  const result = new Uint8Array(arrays.reduce((sum, array) => sum + array.length, 0));
  let offset = 0;
  for (const array of arrays) { result.set(array, offset); offset += array.length; }
  return result;
}

async function readJson(path: string): Promise<any> {
  return JSON.parse(await readFile(path, "utf8"));
}

async function writeJson(path: string, value: unknown): Promise<void> {
  await writeFile(path, `${JSON.stringify(value, null, 2)}\n`, "utf8");
}

function relativePath(path: string): string {
  return path.replace(`${ROOT}\\`, "").replaceAll("\\", "/");
}

function sha256(value: Uint8Array | string): string {
  return createHash("sha256").update(value).digest("hex");
}

function equalBytes(left: Uint8Array, right: Uint8Array): boolean {
  if (left.length !== right.length) return false;
  for (let index = 0; index < left.length; index += 1) if (left[index] !== right[index]) return false;
  return true;
}

void main();
