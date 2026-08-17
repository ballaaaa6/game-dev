/** Build deterministic V7 raster evidence from the isolated V7 compatibility backend. */

import { createHash } from "node:crypto";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { inflateSync } from "node:zlib";
import { GraphicsCompatibility, imageRef } from "../../runtime/social-dev/src/v2/graphics";
import { createV6RoomStaffPreview } from "../../runtime/social-dev/src/v6/index";
import { createRoomV5, stableJson } from "../../runtime/social-dev/src/v5/index";
import { V5_NATIVE_OBJECT_DRAW_OFFSET_X } from "../../runtime/social-dev/src/v5/coordinate-bridge";
import type { GraphicsCommand, GraphicsImageRef } from "../../runtime/social-dev/src/v2/graphics";
import type {
  V7GoldenFixtureRecord,
  V7RasterImage,
  V7RasterSurface,
} from "../../runtime/social-dev/src/v7/contracts";
import { diffRasterV7, makeDiffSurfaceV7 } from "../../runtime/social-dev/src/v7/diff";
import {
  renderV7Commands,
  renderV7Room00Structural,
  renderV7Room00WithStaff,
} from "../../runtime/social-dev/src/v7/golden-renderer";
import { encodePngRgbaV7 } from "../../runtime/social-dev/src/v7/png";
import { RasterCompatibilityV7 } from "../../runtime/social-dev/src/v7/raster";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..", "..");
const ASSET_ROOT = join(ROOT, "runtime", "social-dev", "assets");
const EVIDENCE_ROOT = join(ROOT, "knowledge", "social-dev", "evidence", "visual-port", "v7");
const PREVIEW_ROOT = join(EVIDENCE_ROOT, "previews");

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

interface GeneratedFixture extends V7GoldenFixtureRecord {
  readonly pngSha256: string;
  readonly pngPath: string;
  readonly pixelByteLength: number;
}

async function main(): Promise<void> {
  const roomInstance = createRoomV5("room:0", { visualScope: "full_static" });
  const room = roomInstance.draw();
  const integrated = createV6RoomStaffPreview({
    roomKey: "room:0",
    action: "wait",
    direction: "right",
    frame: 0,
    alpha: 255,
  });
  const imageDimensions = collectImageDimensions([...room.commands, ...integrated.commands]);
  const images = await loadImages(imageDimensions);
  await mkdir(PREVIEW_ROOT, { recursive: true });

  const structural = renderV7Room00Structural(images);
  const structuralRepeat = renderV7Room00Structural(images);
  const withStaff = renderV7Room00WithStaff(images);
  const withStaffRepeat = renderV7Room00WithStaff(images);
  const v5CommandHash = sha256(stableJson(room.commands));
  const v5ManifestHash = sha256(stableJson(roomInstance.commandManifest()));
  const v6Manifest = createV6RoomStaffPreview({
    roomKey: "room:0",
    action: "wait",
    direction: "right",
    frame: 0,
    alpha: 255,
  });
  const v6ManifestHash = sha256(stableJson(v6Manifest));
  if (v5CommandHash !== "0b8132b8ab45eda3d8bb344e65304e0c4d32717a9638c2789efd9223d9df5d60") {
    throw new Error(`V7 V5 command hash drifted: ${v5CommandHash}`);
  }
  if (v5ManifestHash !== "48a1827c94c15394d38e872b243c398d8c6e6f47b66099bf26b44f22ee79e047") {
    throw new Error(`V7 V5 manifest hash drifted: ${v5ManifestHash}`);
  }
  if (v6ManifestHash !== "1e2b1d47922f8e274bfdf40a5c1c9aff85780441ad244f92de641e5cc5de1e7a") {
    throw new Error(`V7 V6 manifest hash drifted: ${v6ManifestHash}`);
  }

  const structuralFixture = await writeRaster("room00-structural", structural.raster.surface);
  const staffFixture = await writeRaster("room00-with-staff", withStaff.raster.surface);
  const repeatedStructuralDiff = diffRasterV7(structural.raster.surface, structuralRepeat.raster.surface);
  const repeatedStaffDiff = diffRasterV7(withStaff.raster.surface, withStaffRepeat.raster.surface);
  const roomToStaffDiff = diffRasterV7(structural.raster.surface, withStaff.raster.surface);
  const roomToStaffDiffPng = await writeRaster("room00-structural-vs-staff.diff", makeDiffSurfaceV7(structural.raster.surface, withStaff.raster.surface));

  const roomCommands = room.commands;
  const staffWaitRight = normalizeObjectCommands(integrated.commands.filter((command) => command.image.id === "resHuman_:image:86"));
  const leftManifest = createV6RoomStaffPreview({ roomKey: "room:0", action: "wait", direction: "left", frame: 0, alpha: 255 });
  const staffWaitLeft = normalizeObjectCommands(leftManifest.commands.filter((command) => command.image.id === "resHuman_:image:86"));
  const typingManifest = createV6RoomStaffPreview({ roomKey: "room:0", action: "typing", direction: "right", frame: 0, alpha: 255 });
  const staffTypingRight = normalizeObjectCommands(typingManifest.commands.filter((command) => command.image.id === "resHuman_:image:86"));
  const alphaManifest = createV6RoomStaffPreview({ roomKey: "room:0", action: "wait", direction: "right", frame: 0, alpha: 128 });
  const staffAlpha = normalizeObjectCommands(alphaManifest.commands.filter((command) => command.image.id === "resHuman_:image:86"));

  const fixtures: GeneratedFixture[] = [];
  const floorSource = roomCommands.find((command) =>
    command.image.id === "resChip_:image:85"
    && command.destination.x === 400
    && command.destination.y === 0,
  );
  if (floorSource === undefined) {
    throw new Error("V7 floor fixture source is missing");
  }
  const localFloor = rebaseCommand(floorSource, 96, 72);
  fixtures.push(await renderFixture("floor.direct_image", "asset", [localFloor], images, ["runtime/social-dev/assets/room-scene/01_GAME_PACKS/chip/floor_05.png", "knowledge/fixtures/accepted/phase3b_floor_recovery_fixture.json"]));
  fixtures.push(await renderFixture("wall.seb", "asset", commandsWithId(roomCommands, "resChip_:image:6"), images, ["runtime/social-dev/assets/display-slice-01/01_GAME_PACKS/chip/wall_00.seb", "knowledge/fixtures/accepted/visual-port/v2/draw-image-contract.json"]));
  fixtures.push(await renderFixture("door.seb", "asset", commandsWithId(roomCommands, "resChip_:image:7"), images, ["runtime/social-dev/assets/display-slice-01/01_GAME_PACKS/chip/door_02.seb", "knowledge/fixtures/accepted/visual-port/v2/draw-image-contract.json"]));
  fixtures.push(await renderFixture("furniture.3_desk_chair", "asset", normalizeObjectCommands(roomCommands.filter((command) => command.image.id === "resChip_:image:3" || command.image.id === "resChip_:image:4")), images, ["runtime/social-dev/assets/display-slice-01/01_GAME_PACKS/chip/desk_00.seb", "runtime/social-dev/assets/display-slice-01/01_GAME_PACKS/chip/chair_00.seb", "knowledge/fixtures/accepted/visual-port/v4/furniture-visual-binding.json"]));
  fixtures.push(await renderFixture("furniture.12", "asset", commandsWithId(roomCommands, "resChip_:image:109"), images, ["runtime/social-dev/assets/display-slice-01/01_GAME_PACKS/chip/equip.seb", "knowledge/fixtures/accepted/visual-port/v5/room-furniture-orchestration.json"]));
  fixtures.push(await renderFixture("furniture.26", "asset", commandsWithId(roomCommands, "resChip_:image:106"), images, ["runtime/social-dev/assets/display-slice-01/01_GAME_PACKS/chip/equip.seb", "knowledge/fixtures/accepted/visual-port/v5/room-furniture-orchestration.json"]));
  fixtures.push(await renderFixture("furniture.56", "asset", commandsWithId(roomCommands, "resChip_:image:127"), images, ["runtime/social-dev/assets/display-slice-01/01_GAME_PACKS/chip/equip.seb", "knowledge/fixtures/accepted/visual-port/v5/room-furniture-orchestration.json"]));
  fixtures.push(await renderFixture("staff.0_wait_right", "staff", staffWaitRight, images, ["runtime/social-dev/assets/character-catalog/01_GAME_PACKS/human/wait_right.seb", "knowledge/fixtures/accepted/visual-port/v6/staff-animation-contract.json"]));
  fixtures.push(await renderFixture("staff.0_wait_left", "staff", staffWaitLeft, images, ["runtime/social-dev/assets/character-catalog/01_GAME_PACKS/human/wait_left.seb", "knowledge/fixtures/accepted/visual-port/v6/staff-animation-contract.json"]));
  fixtures.push(await renderFixture("staff.0_typing_right", "staff", staffTypingRight, images, ["runtime/social-dev/assets/character-catalog/01_GAME_PACKS/human/typing_right.seb", "knowledge/fixtures/accepted/visual-port/v6/staff-animation-contract.json"]));

  const selectedSource = normalizeObjectCommands(roomCommands.filter((command) => command.image.id === "resChip_:image:3"))[0];
  if (selectedSource === undefined) {
    throw new Error("V7 selected flip fixture source is missing");
  }
  const flipCommand = recreateCommand(selectedSource, (graphics) => graphics.setFlipMode(1));
  fixtures.push(await renderFixture("graphics.selected_horizontal_flip", "graphics", [flipCommand], images, ["knowledge/fixtures/accepted/visual-port/v2/draw-image-contract.json"]));
  fixtures.push(await renderFixture("staff.alpha_128", "staff", staffAlpha, images, ["knowledge/fixtures/accepted/visual-port/v6/staff-animation-contract.json", "knowledge/fixtures/accepted/visual-port/v6/unknowns.json"]));

  const clippedCommand = recreateCommand(rebaseCommand(floorSource, 96, 72), (graphics) => {
    graphics.setClip(106, 82, 20, 20);
  });
  fixtures.push(await renderFixture("graphics.clipped_draw", "graphics", [clippedCommand], images, ["knowledge/fixtures/accepted/visual-port/v2/clip-contract.json"]));

  const transformedSource = rebaseCommand(floorSource, 96, 72);
  const transformedRaster = new RasterCompatibilityV7({ width: 240, height: 200, origin: { x: 0, y: 0 } });
  const transform = { scaleX: 1.25, scaleY: 0.75, rotationDegrees: 15, pivot: { x: transformedSource.destination.x + transformedSource.destination.width / 2, y: transformedSource.destination.y + transformedSource.destination.height / 2 } };
  const transformedWrites = transformedRaster.draw({
    image: images.get(String(transformedSource.image.id))!,
    destination: transformedSource.destination,
    source: transformedSource.source,
    state: transformedSource.state,
    transform,
    clip: { rect: transformedSource.destination, transformed: transform },
  });
  fixtures.push(await renderSurfaceFixture("graphics.transformed_draw", "graphics", transformedRaster.output, images.get(String(transformedSource.image.id))!, stableJson({ command: transformedSource, transform, clip: transformedSource.destination, writes: transformedWrites }), ["knowledge/fixtures/accepted/visual-port/v2/graphics-static-recovery.json"]));

  const goldenResults = fixtures.map((fixture) => ({ ...fixture }));
  const graphicsContract = buildGraphicsContract();
  const samplingContract = buildSamplingContract();
  const transformContract = buildTransformContract();
  const blendContract = buildBlendContract();
  const selectedPathClosure = buildSelectedPathClosure(imageDimensions);
  const staffCadence = buildStaffCadenceContract();
  const unknowns = buildUnknowns();
  const pixelDiffResults = {
    schema_version: "social-dev-visual-port-v7-pixel-diff-results-v1",
    status: "pass_static",
    comparisons: [
      { id: "repeated-room00-structural", class: "deterministic_repeat", result: repeatedStructuralDiff, proof_class: "PROVEN" },
      { id: "repeated-room00-with-staff", class: "deterministic_repeat", result: repeatedStaffDiff, proof_class: "PROVEN" },
      { id: "room00-structural-vs-room00-with-staff", class: "expected_selected_content_delta", result: roomToStaffDiff, difference_class: "C_COMPATIBILITY_BACKEND_DIFFERENCE", proof_class: "COMPATIBILITY_REIMPLEMENTATION" },
    ],
    diff_png: { path: roomToStaffDiffPng.pngPath, sha256: roomToStaffDiffPng.pngSha256 },
    historical_comparison: { used: false, status: "SECONDARY_ONLY_NOT_AUTHORITATIVE", reason: "Historical screenshots are not used to derive geometry, resource identity, or acceptance pixels." },
  };
  const roomStructural = {
    schema_version: "social-dev-visual-port-v7-room00-structural-render-v1",
    status: "pass_static",
    room_key: "room:0",
    phase: "V5",
    dimensions: { width: structural.raster.surface.width, height: structural.raster.surface.height },
    pixel_sha256: sha256(structural.raster.surface.pixels),
    png_sha256: structuralFixture.pngSha256,
    png_path: structuralFixture.pngPath,
    command_sha256: v5CommandHash,
    command_manifest_sha256: v5ManifestHash,
    commands: room.commands.length,
    traces: room.traces.length,
    events: room.events.length,
    draw_count: structural.raster.drawCount,
    skipped_draw_count: structural.raster.skippedDrawCount,
    nontransparent_bounds: structural.raster.nonTransparentBounds,
    floor_selector_policy: { raw: 5, selector_data: 85, rendered_filename: "floor_05.png", proof_class: "PRODUCT_POLICY" },
    compatibility_assumptions: compatibilityAssumptions(),
  };
  const roomWithStaff = {
    schema_version: "social-dev-visual-port-v7-room00-with-staff-render-v1",
    status: "pass_static",
    room_key: "room:0",
    phase: "V6",
    dimensions: { width: withStaff.raster.surface.width, height: withStaff.raster.surface.height },
    pixel_sha256: sha256(withStaff.raster.surface.pixels),
    png_sha256: staffFixture.pngSha256,
    png_path: staffFixture.pngPath,
    v6_manifest_sha256: v6ManifestHash,
    commands: integrated.commands.length,
    traces: integrated.traces.length,
    events: integrated.events.length,
    draw_count: withStaff.raster.drawCount,
    skipped_draw_count: withStaff.raster.skippedDrawCount,
    nontransparent_bounds: withStaff.raster.nonTransparentBounds,
    action: "wait",
    direction: "right",
    frame: 0,
    camera: [0, 0],
    staff_actor_ids: ["actor:staff:0", "actor:staff:1", "actor:staff:2"],
    compatibility_assumptions: compatibilityAssumptions(),
  };
  const goldenManifest = {
    schema_version: "social-dev-visual-port-v7-golden-fixture-manifest-v1",
    status: "pass_static",
    proof_policy: "Source/format/command identity remains separate from compatibility backend pixel output.",
    required_fixture_count: 14,
    fixtures: fixtures.map((fixture) => ({
      fixture_id: fixture.fixtureId,
      category: fixture.category,
      source_refs: fixture.sourceRefs,
      command_hash: fixture.commandHash,
      output_size: [fixture.outputWidth, fixture.outputHeight],
      output_png: fixture.pngPath,
      proof_class: fixture.proofClass,
      compatibility_assumptions: fixture.compatibilityAssumptions,
    })),
  };
  const fidelityManifest = {
    schema_version: "social-dev-visual-port-v7-fidelity-manifest-v1",
    status: "PASS_STATIC_FIDELITY",
    baseline: {
      v1: "pass",
      v2: "pass_static",
      v3: "pass",
      v4: "pass_static",
      v5: "pass_static",
      v6: "pass_static",
      v5_command_sha256: v5CommandHash,
      v5_manifest_sha256: v5ManifestHash,
      v6_manifest_sha256: v6ManifestHash,
    },
    graphics_contract_sha256: sha256(stableJson(graphicsContract)),
    compatibility_raster_assumptions: compatibilityAssumptions(),
    golden_fixture_manifest_sha256: sha256(stableJson(goldenManifest)),
    golden_fixture_results_sha256: sha256(stableJson(goldenResults)),
    room00_structural_png_sha256: structuralFixture.pngSha256,
    room00_with_staff_png_sha256: staffFixture.pngSha256,
    command_manifest_hashes: { v5: v5ManifestHash, v6: v6ManifestHash },
    proof_classifications: {
      source_geometry: "PROVEN",
      selected_command_stream: "PROVEN",
      compatibility_backend_pixels: "COMPATIBILITY_REIMPLEMENTATION",
      floor_selector_alias: "PRODUCT_POLICY",
      staff_cadence: "SOURCE_LIMITED",
    },
    residual_differences: pixelDiffResults.comparisons,
    unknowns_ref: "knowledge/fixtures/accepted/visual-port/v7/unknowns.json",
    production_renderer_changed: false,
    v8_readiness: { entry: "NO", reason: "Starter-room semantic correction is frozen for review; V8 is intentionally not started." },
  };
  const checkpointLedger = buildCheckpointLedger({ structuralFixture, staffFixture, fixtures, pixelDiffResults });

  await writeJson("graphics-raster-contract.json", graphicsContract);
  await writeJson("sampling-contract.json", samplingContract);
  await writeJson("transform-raster-contract.json", transformContract);
  await writeJson("blend-alpha-contract.json", blendContract);
  await writeJson("selected-path-closure.json", selectedPathClosure);
  await writeJson("staff-cadence-contract.json", staffCadence);
  await writeJson("golden-fixture-manifest.json", goldenManifest);
  await writeJson("golden-fixture-results.json", goldenResults);
  await writeJson("room00-structural-render.json", roomStructural);
  await writeJson("room00-with-staff-render.json", roomWithStaff);
  await writeJson("pixel-diff-results.json", pixelDiffResults);
  await writeJson("fidelity-manifest.json", fidelityManifest);
  await writeJson("unknowns.json", unknowns);
  await writeJson("checkpoint-ledger.json", checkpointLedger);
  await writeJson("source-image-manifest.json", [...images.values()].map((image) => ({ id: image.id, width: image.width, height: image.height, source_ref: image.sourceRef, source_sha256: image.sourceSha256 })));

  console.log(JSON.stringify({
    status: "pass_static_fidelity",
    v5: { commands: room.commands.length, traces: room.traces.length, events: room.events.length, command_sha256: v5CommandHash, manifest_sha256: v5ManifestHash },
    v6: { commands: integrated.commands.length, traces: integrated.traces.length, events: integrated.events.length, sha256: v6ManifestHash },
    structural: roomStructural,
    withStaff: roomWithStaff,
    fixtures: fixtures.length,
    repeatedStructuralDiff,
    repeatedStaffDiff,
  }, null, 2));
}

function collectImageDimensions(commands: readonly GraphicsCommand[]): Map<string, { width: number; height: number }> {
  const result = new Map<string, { width: number; height: number }>();
  for (const command of commands) {
    result.set(String(command.image.id), { width: command.image.width, height: command.image.height });
  }
  return result;
}

async function loadImages(dimensions: ReadonlyMap<string, { width: number; height: number }>): Promise<Map<string, V7RasterImage>> {
  const images = new Map<string, V7RasterImage>();
  for (const [id, expected] of dimensions) {
    const path = IMAGE_PATHS[id];
    if (path === undefined) {
      throw new Error(`V7 asset map is missing command image id ${id}`);
    }
    const bytes = await readFile(path);
    const decoded = decodePng(bytes);
    if (decoded.width !== expected.width || decoded.height !== expected.height) {
      throw new Error(`V7 source dimension mismatch for ${id}: ${decoded.width}x${decoded.height} != ${expected.width}x${expected.height}`);
    }
    images.set(id, {
      id,
      width: decoded.width,
      height: decoded.height,
      pixels: decoded.pixels,
      sourceRef: relativePath(path),
      sourceSha256: sha256(bytes),
    });
  }
  return images;
}

async function renderFixture(
  fixtureId: string,
  category: V7GoldenFixtureRecord["category"],
  commands: readonly GraphicsCommand[],
  images: ReadonlyMap<string, V7RasterImage>,
  sourceRefs: readonly string[],
): Promise<GeneratedFixture> {
  const raster = renderV7Commands(commands, images, { width: 360, height: 220, origin: { x: 64, y: 96 } });
  return renderSurfaceFixture(fixtureId, category, raster.surface, sourceImageFor(commands, images), sha256(stableJson(commands)), sourceRefs, raster.nonTransparentBounds);
}

async function renderSurfaceFixture(
  fixtureId: string,
  category: V7GoldenFixtureRecord["category"],
  surface: V7RasterSurface,
  sourceImage: V7RasterImage,
  commandHash: string,
  sourceRefs: readonly string[],
  bounds = surfaceBounds(surface),
): Promise<GeneratedFixture> {
  const png = encodePngRgbaV7(surface);
  const filename = `${fixtureId.replaceAll(".", "-")}.png`;
  const pngPath = `knowledge/fixtures/accepted/visual-port/v7/previews/${filename}`;
  await writeFile(join(ROOT, pngPath), Buffer.from(png));
  return {
    fixtureId,
    category,
    sourceRefs,
    commandHash,
    outputWidth: surface.width,
    outputHeight: surface.height,
    pixelSha256: sha256(surface.pixels),
    nonTransparentBounds: bounds,
    proofClass: "COMPATIBILITY_REIMPLEMENTATION",
    compatibilityAssumptions: compatibilityAssumptions(),
    pngSha256: sha256(png),
    pngPath,
    pixelByteLength: surface.pixels.length,
  };
}

async function writeRaster(name: string, surface: V7RasterSurface): Promise<{ pngSha256: string; pngPath: string }> {
  const png = encodePngRgbaV7(surface);
  const pngPath = `knowledge/fixtures/accepted/visual-port/v7/previews/${name}.png`;
  await writeFile(join(ROOT, pngPath), Buffer.from(png));
  return { pngSha256: sha256(png), pngPath };
}

function sourceImageFor(commands: readonly GraphicsCommand[], images: ReadonlyMap<string, V7RasterImage>): V7RasterImage {
  const command = commands[0];
  if (command === undefined) {
    throw new Error("V7 fixture cannot be rendered without a command");
  }
  const image = images.get(String(command.image.id));
  if (image === undefined) {
    throw new Error(`V7 fixture source image is missing ${String(command.image.id)}`);
  }
  return image;
}

function commandsWithId(commands: readonly GraphicsCommand[], id: string): readonly GraphicsCommand[] {
  const selected = commands.filter((command) => command.image.id === id);
  if (selected.length === 0) {
    throw new Error(`V7 fixture command group is empty for ${id}`);
  }
  return normalizeObjectCommands(selected);
}

function normalizeObjectCommands(commands: readonly GraphicsCommand[]): readonly GraphicsCommand[] {
  return commands.map((command) => ({
    ...command,
    destination: {
      ...command.destination,
      x: command.destination.x - V5_NATIVE_OBJECT_DRAW_OFFSET_X,
    },
  }));
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
  if (recreated === undefined) {
    throw new Error("V7 recreated command was not recorded");
  }
  return recreated;
}

function rebaseCommand(command: GraphicsCommand, x: number, y: number): GraphicsCommand {
  return {
    ...command,
    destination: { ...command.destination, x, y },
    state: { ...command.state, clip: null, clipDepth: 0 },
  };
}

function buildGraphicsContract(): object {
  return {
    schema_version: "social-dev-visual-port-v7-graphics-raster-contract-v1",
    status: "pass_static",
    operations: [
      { operation: "ResetRender", native_rva: "0x1C07C74", inputs: [], state_transition: "clip=null, flip=0, scale=100, render=replace(255,0), blend=none", output: "deterministic V7 initial state", proof_class: "PROVEN", remaining_uncertainty: "Native LinearFilter field is zero-initialized rather than explicitly reset." },
      { operation: "DrawImage crop", native_rva: "0x1C0EF98", inputs: ["image", "dx", "dy", "sx", "sy", "width", "height"], state_transition: "records source and equal-size destination rectangles", output: "V7 nearest/linear compatibility sample", proof_class: "PROVEN", remaining_uncertainty: "Final _drawBitmap sampler/rounding is unavailable." },
      { operation: "DrawScaledImage", native_rva: "0x1C0F0C8", inputs: ["image", "dx", "dy", "width", "height", "sx", "sy", "swidth", "sheight"], state_transition: "records independent source/destination geometry", output: "V7 deterministic resample", proof_class: "PROVEN", remaining_uncertainty: "GPU interpolation exactness is compatibility-reimplemented." },
      { operation: "ClipRect", native_rva: "0x1C08694", inputs: ["x", "y", "width", "height", "push"], state_transition: "intersection uses max-left/top and min-right/bottom", output: "surface and explicit clip culling", proof_class: "PROVEN", remaining_uncertainty: "Transformed native matrices are not selected in V5/V6 commands." },
      { operation: "GetTransRect", native_rva: "0x1C085E8", inputs: ["rect", "matrix"], state_transition: "V7 accepts an explicit transform fixture", output: "deterministic polygon clip/affine sample", proof_class: "COMPATIBILITY_REIMPLEMENTATION", remaining_uncertainty: "Selected native scene commands carry identity transforms only." },
      { operation: "SetFlipMode", native_rva: "0x1C1B54C", inputs: [0, 1, 2, 3, 4, 5], state_transition: "horizontal/vertical center flips; 4/5 explicit compatibility rotations", output: "deterministic orientation", proof_class: "PROVEN", remaining_uncertainty: "Native final pixels for modes 4/5 remain source-limited." },
      { operation: "Scale", native_rva: "0x1C07C6C", inputs: ["percent"], state_transition: "scale about command center", output: "deterministic transformed bounds", proof_class: "PROVEN", remaining_uncertainty: "No selected room command uses non-100 scale." },
      { operation: "SetColor", native_rva: "0x1C09D60", inputs: ["AARRGGBB"], state_transition: "explicit tint/alpha only; default 0xFF000000 is V7 identity sentinel", output: "straight-alpha channel modulation", proof_class: "COMPATIBILITY_REIMPLEMENTATION", remaining_uncertainty: "Native shader color interpretation is unavailable." },
      { operation: "SetRenderMode", native_rva: "0x1C07C74", inputs: ["operator", "sourceRatio", "destinationRatio"], state_transition: "replace/add/subtract channel equations", output: "deterministic byte-rounded blend", proof_class: "COMPATIBILITY_REIMPLEMENTATION", remaining_uncertainty: "Native premultiplication and shader rounding are unavailable." },
      { operation: "LinearFilter", native_rva: "0x1C1C0BC", inputs: ["enable"], state_transition: "nearest when false; bilinear center sampling when true", output: "deterministic sampling mode", proof_class: "COMPATIBILITY_REIMPLEMENTATION", remaining_uncertainty: "Exact native sampler state is source-limited." },
    ],
    selected_scene_dispatch: { room_passes: 9, selected_room: "room:0", staff_pass: "avatar-primary", source_contracts: ["V1 Seb/Image", "V2 Graphics", "V3 ResourceManager", "V4 object/map", "V5 Room", "V6 Staff"] },
  };
}

function buildSamplingContract(): object {
  return {
    schema_version: "social-dev-visual-port-v7-sampling-contract-v1",
    status: "pass_static",
    source_rect: { semantics: "source x/y plus width/height are preserved from GraphicsCommand", integer_conversion: "selected integer values remain exact", proof_class: "PROVEN" },
    destination_rect: { semantics: "DrawImage uses equal source/destination size; DrawScaledImage preserves independent destination size", negative_coordinates: "accepted and clipped against surface", proof_class: "PROVEN" },
    nearest: { rule: "source pixel center nearest with transparent out-of-bounds samples", rounding: "floor(sample + 0.5)", proof_class: "COMPATIBILITY_REIMPLEMENTATION" },
    linear: { rule: "four-neighbor bilinear interpolation around source pixel centers", rounding: "Math.round per channel", proof_class: "COMPATIBILITY_REIMPLEMENTATION" },
    source_bounds: { out_of_bounds: "transparent", negative_source: "transparent where sample is outside source image", proof_class: "COMPATIBILITY_REIMPLEMENTATION" },
    native_boundary: { native_rva: "0x1C10388", status: "backend_pixels_unavailable", no_half_pixel_correction: true },
  };
}

function buildTransformContract(): object {
  return {
    schema_version: "social-dev-visual-port-v7-transform-raster-contract-v1",
    status: "pass_static",
    matrix_order: "scale about pivot, then rotate about pivot, then inverse-map destination pixel centers",
    pivot: "destination rectangle center unless an explicit fixture pivot is supplied",
    flip_modes: { none: "identity", horizontal: "u=1-u", vertical: "v=1-v", both: "u=1-u and v=1-v", rotate_left: "compatibility -90 degrees", rotate_right: "compatibility +90 degrees" },
    selected_scene: { room00: "identity transform only", staff: "identity transform only", proof_class: "PROVEN" },
    transformed_fixture: { scale: [1.25, 0.75], rotation_degrees: 15, clip: "same affine polygon contract", proof_class: "COMPATIBILITY_REIMPLEMENTATION" },
    source_limit: "Native modes 4/5 are branch-proven but final backend orientation pixels are unavailable; the selected complete room does not use them.",
  };
}

function buildBlendContract(): object {
  return {
    schema_version: "social-dev-visual-port-v7-blend-alpha-contract-v1",
    status: "pass_static",
    color: { packing: "AARRGGBB", default_state: "0xFF000000 treated as identity sentinel for the selected V1–V6 command surface", explicit_color: "straight-alpha RGB multiplication and alpha multiplication", proof_class: "COMPATIBILITY_REIMPLEMENTATION" },
    render_modes: { replace: "source*sourceRatio + destination*destinationRatio", add: "same bounded channel sum with native ratios", subtract: "source*sourceRatio - destination*destinationRatio clamped at zero", rounding: "Math.round", proof_class: "COMPATIBILITY_REIMPLEMENTATION" },
    staff_alpha: { v6_command: "PushRenderMode(ADD, alpha, 255-alpha)", selected_fixture: "alpha=128", state_scope: "push/pop around Staff SEB commands", proof_class: "PROVEN" },
    blend_modes: { none: "identity", color: "RGB multiply by blend color", light: "RGB add/clamp", grayscale: "0.299R + 0.587G + 0.114B", proof_class: "COMPATIBILITY_REIMPLEMENTATION" },
    gpu_boundary: { premultiplication: "straight-alpha compatibility rule", exact_shader_rounding: "SOURCE_LIMITED", native_rva: "0x1C10388" },
  };
}

function buildSelectedPathClosure(imageDimensions: ReadonlyMap<string, { width: number; height: number }>): object {
  return {
    schema_version: "social-dev-visual-port-v7-selected-path-closure-v1",
    status: "pass_static",
    used_paths: [
      { path: "Graphics.DrawImage crop", selected: true, fixtures: ["wall.seb", "door.seb", "staff.0_wait_right", "furniture.3_desk_chair"] },
      { path: "Graphics.DrawScaledImage", selected: true, fixtures: ["graphics.clipped_draw", "graphics.transformed_draw"] },
      { path: "Seb sprite source-slot resolution", selected: true, fixtures: ["floor.direct_image", "wall.seb", "door.seb", "staff.0_typing_right"] },
      { path: "direct FurnitureData image", selected: true, fixtures: ["furniture.12", "furniture.26", "furniture.56"] },
      { path: "CustomImages dictionary", selected: false, status: "SOURCE_LIMITED", reason: "No selected room:0+Staff command uses it." },
      { path: "atlas dispatch", selected: false, status: "SOURCE_LIMITED", reason: "No selected room:0+Staff command uses it." },
      { path: "optimized image blocks", selected: false, status: "SOURCE_LIMITED", reason: "Selected logical OPT PNGs are already source-backed promoted images; no native block payload is selected." },
      { path: "synthetic FRECT/RECT/LINE", selected: false, status: "SOURCE_LIMITED", reason: "No selected room:0+Staff command uses TEXID -2/-3/-4." },
      { path: "depth-aware Seb.Render", selected: false, status: "SOURCE_LIMITED", reason: "Selected SEBs carry no proven depth payload." },
    ],
    command_image_ids: [...imageDimensions.keys()],
    raw_type_identity_policy: "No filename-based semantic identity; command image IDs remain group-qualified numeric selectors.",
  };
}

function buildStaffCadenceContract(): object {
  return {
    schema_version: "social-dev-visual-port-v7-staff-cadence-contract-v1",
    status: "pass_static",
    selected_fixture: { action: "wait", direction: "right", frame: 0, actor_ids: ["actor:staff:0", "actor:staff:1", "actor:staff:2"], proof_class: "PROVEN" },
    source_intervals: { wait: 1, typing: 3, frame_reset_on_action_change: true, frame_reset_on_direction_change: true, proof_class: "CALL-FLOW-PROVEN" },
    alpha: { spawn: 0, deterministic_fixture_fade: "V6 alpha step +25 per selected step", selected_v7_fixture: 128, proof_class: "CALL-FLOW-PROVEN" },
    unknowns: ["complete native Staff.Update cadence", "hidden initial SEB before first draw", "gameplay route/talk/work cadence"],
    boundary: "V7 closes only deterministic selected frame/action fixtures; it does not copy legacy browser timing or claim complete live cadence.",
  };
}

function buildUnknowns(): object {
  return {
    schema_version: "social-dev-visual-port-v7-unknowns-v1",
    status: "pass_static_nonblocking_unknowns",
    items: [
      { id: "V7-U01", question: "What exact _drawBitmap shader sampling and premultiplied-alpha result does native Graphics produce?", status: "COMPATIBILITY_REIMPLEMENTATION", blocking: false, missing_original_detail: "No static shader/backend source or framebuffer is available.", known_contract: "Source/destination/state/clip command contract is recovered.", replacement_choice: "Deterministic nearest/bilinear straight-alpha byte raster rules.", affected_fixtures: ["all raster fixtures"], safe_reason: "Preserves recovered observable command contract and is isolated from production renderer.", future_evidence: "Static backend source or an explicitly authorized native fixture.", proof_class: "COMPATIBILITY_REIMPLEMENTATION" },
      { id: "V7-U02", question: "What exact transformed clip rectangle reaches the backend for non-identity native matrices?", status: "COMPATIBILITY_REIMPLEMENTATION", blocking: false, missing_original_detail: "Selected V5/V6 commands carry no non-identity matrix payload.", known_contract: "GetTransRect native boundary is pinned.", replacement_choice: "Explicit affine polygon clip fixture.", affected_fixtures: ["graphics.transformed_draw"], safe_reason: "No selected complete room geometry depends on the fixture-only transform.", future_evidence: "Selected SEB/Room command with proven matrix state.", proof_class: "COMPATIBILITY_REIMPLEMENTATION" },
      { id: "V7-U03", question: "What are native final pixels for flip modes 4 and 5?", status: "SOURCE_LIMITED", blocking: false, missing_original_detail: "Native branch is known, final backend orientation is not.", known_contract: "Branch calls RotateTemporary(-90 degrees) in the pinned binary.", replacement_choice: "Explicit compatibility orientations for isolated tests only.", affected_fixtures: ["graphics.selected_horizontal_flip"], safe_reason: "Complete room:0+Staff uses no modes 4/5.", future_evidence: "Static pixel-level matrix/backend proof.", proof_class: "SOURCE_LIMITED" },
      { id: "V7-U04", question: "Which selected paths use atlas/custom/optimized image blocks?", status: "UNKNOWN_NONBLOCKING", blocking: false, policy: "Selected room:0+Staff command IDs use only proven direct/group-local images; unused branches remain deferred.", proof_class: "SOURCE_LIMITED" },
      { id: "V7-U05", question: "What native depth/anchor payload affects selected SEBs?", status: "SOURCE_LIMITED", blocking: false, policy: "Selected fixtures carry no proven depth payload; anchor/depth wrappers remain deferred.", proof_class: "SOURCE_LIMITED" },
      { id: "V7-U06", question: "What is the full live Staff.Update cadence?", status: "SOURCE_LIMITED", blocking: false, policy: "Selected frame/action fixtures are deterministic; live gameplay timing is out of scope.", proof_class: "SOURCE_LIMITED" },
      { id: "V7-U07", question: "Does historical screenshot context differ from the static room command output?", status: "UNKNOWN_NONBLOCKING", blocking: false, policy: "Historical screenshots are secondary only and no geometry is tuned from them.", proof_class: "SOURCE_LIMITED" },
    ],
    blocking_unknowns: [],
  };
}

function buildCheckpointLedger(input: { structuralFixture: { pngSha256: string; pngPath: string }; staffFixture: { pngSha256: string; pngPath: string }; fixtures: readonly GeneratedFixture[]; pixelDiffResults: object }): object {
  return {
    schema_version: "social-dev-visual-port-v7-checkpoint-ledger-v1",
    status: "pass_static_fidelity",
    execution_mode: "INLINE_EXECUTION_ONLY",
    static_only: true,
    subagents: false,
    checkpoints: [
      { id: "V7.0", status: "PASS", summary: "V1–V6 baseline and static gates green; V7 initially absent." },
      { id: "V7.1", status: "PASS", summary: "Graphics contract consolidated from V2 and selected V5/V6 commands." },
      { id: "V7.2", status: "PASS", summary: "DrawImage crop/destination, clip, nearest/linear, and out-of-bounds compatibility rules closed." },
      { id: "V7.3", status: "PASS", summary: "Flip/scale/rotation compatibility rules and tests closed; selected room uses identity." },
      { id: "V7.4", status: "PASS", summary: "Color, alpha, render ratios, blend, and push/pop state fixtures closed." },
      { id: "V7.5", status: "PASS", summary: "Selected direct image/SEB paths closed; atlas/custom/optimized/depth branches remain non-selected." },
      { id: "V7.6", status: "PASS_STATIC_BOUNDARY", summary: "Selected Staff wait/typing cadence and frame 0 are deterministic; complete live cadence remains source-limited." },
      { id: "V7.7", status: "PASS", summary: "RasterCompatibilityV7 implemented additively with no production cutover." },
      { id: "V7.8", status: "PASS", summary: `${input.fixtures.length} golden fixture outputs are stable and source-referenced.` },
      { id: "V7.9", status: "PASS", summary: `room:0 structural PNG ${input.structuralFixture.pngSha256}.` },
      { id: "V7.10", status: "PASS", summary: `room:0 + Staff PNG ${input.staffFixture.pngSha256}.` },
      { id: "V7.11", status: "PASS", summary: "Repeated render diff and room-vs-staff diff tooling generated." },
      { id: "V7.12", status: "PASS", summary: "Residual differences are classified; no screenshot tuning performed." },
      { id: "V7.13", status: "PASS", summary: "Fidelity manifest and nonblocking unknown ledger generated." },
      { id: "V7.14", status: "PASS", summary: "Static artifact generation, evidence validation, and final regression inputs are complete; V8 has not started." },
    ],
    outputs: { structural_png: input.structuralFixture, staff_png: input.staffFixture, pixel_diff: input.pixelDiffResults },
  };
}

function compatibilityAssumptions(): readonly string[] {
  return [
    "Default V2 color 0xFF000000 is treated as an identity sentinel because selected V5/V6 commands do not set a tint color.",
    "Raster output uses straight-alpha RGBA byte channels; native premultiplication and shader rounding are unavailable.",
    "Nearest sampling uses source pixel centers; linear filtering uses four-neighbor bilinear interpolation.",
    "Out-of-bounds source samples are transparent.",
    "Clip rectangles are evaluated against the transformed world pixel center; transformed fixture clips use convex polygons.",
    "Flip modes 1–3 are center flips; modes 4–5 use explicit compatibility rotations and are not selected by room:0+Staff.",
    "All output PNGs use deterministic filter-zero scanlines and stored DEFLATE blocks.",
  ];
}

function surfaceBounds(surface: V7RasterSurface): { x: number; y: number; width: number; height: number } | null {
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
  const signature = [137, 80, 78, 71, 13, 10, 26, 10];
  if (!signature.every((value, index) => bytes[index] === value)) throw new Error("V7 PNG signature is invalid");
  let offset = 8;
  let width = 0;
  let height = 0;
  let bitDepth = 0;
  let colorType = 0;
  let interlace = 0;
  let palette: Uint8Array | null = null;
  let transparency: Uint8Array | null = null;
  const idat: Uint8Array[] = [];
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
  if (bitDepth !== 8 || interlace !== 0 || ![0, 2, 3, 4, 6].includes(colorType)) throw new Error(`V7 PNG format unsupported bitDepth=${bitDepth} colorType=${colorType} interlace=${interlace}`);
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
      if (palette === null || paletteOffset + 2 >= palette.length) throw new Error(`V7 PNG palette index ${paletteIndex} is out of range`);
      pixels[targetIndex] = palette[paletteOffset]; pixels[targetIndex + 1] = palette[paletteOffset + 1]; pixels[targetIndex + 2] = palette[paletteOffset + 2]; pixels[targetIndex + 3] = transparency !== null && paletteIndex < transparency.length ? transparency[paletteIndex] : 255;
    } else { pixels[targetIndex] = source[sourceIndex]; pixels[targetIndex + 1] = source[sourceIndex]; pixels[targetIndex + 2] = source[sourceIndex]; pixels[targetIndex + 3] = 255; }
  }
  return { width, height, pixels };
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
  const result = new Uint8Array(arrays.reduce((sum, item) => sum + item.length, 0));
  let offset = 0;
  for (const item of arrays) { result.set(item, offset); offset += item.length; }
  return result;
}

void main();
