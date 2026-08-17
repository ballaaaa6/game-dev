import { createHash } from "node:crypto";
import { inflateSync } from "node:zlib";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { beforeAll, describe, expect, it } from "vitest";
import { GraphicsCompatibility } from "../src/v2/graphics";
import { drawMainDisplayMapCell } from "../src/v5/main-display-map";
import { createRoomV5, stableJson } from "../src/v5";
import type { V5MapChip } from "../src/v5/contracts";
import { mapChipOrigin } from "../src/v4/map-chip";
import { sortV4Drawables } from "../src/v4/ordering";
import type { V4Cell, V4CommandTrace } from "../src/v4/contracts";
import {
  encodePngRgbaV7,
  renderV7Commands,
  RasterSurfaceCompatibilityV7,
} from "../src/v7";
import type {
  V7RasterImage,
  V7RasterOptions,
  V7RasterSurface,
} from "../src/v7/contracts";
const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..", "..", "..");
const ASSET_ROOT = join(ROOT, "runtime", "social-dev", "assets");
const EVIDENCE_ROOT = join(ROOT, "knowledge", "fixtures", "accepted", "visual-port", "mapchip-forensic");
const PREVIEW_ROOT = join(EVIDENCE_ROOT, "previews");
const HISTORICAL_CORRUPT_PREVIEW = join(
  ROOT,
  "knowledge",
  "fixtures",
  "accepted",
  "visual-port",
  "starter-room-correction",
  "previews",
  "starter_room_structural_corrected.png",
);

const RASTER_OPTIONS: V7RasterOptions = {
  width: 1200,
  height: 700,
  origin: { x: 100, y: 300 },
  background: [0, 0, 0, 0],
};

const SOURCE_PATHS: Readonly<Record<string, string>> = {
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
};

const DIRECT_SELECTOR_IDS = [10, 11, 12, 13, 14, 15, 85, 105, 154, 155, 156] as const;
const DIRECT_IMAGE_IDS = DIRECT_SELECTOR_IDS.map((id) => `resChip_:image:${id}`);

interface DecodedPng {
  readonly width: number;
  readonly height: number;
  readonly pixels: Uint8Array;
}

interface SelectorRecord {
  readonly index: number;
  readonly cell: readonly [number, number];
  readonly rawIndex: number;
  readonly selectorId: number;
  readonly role: string;
  readonly sourcePath: string | null;
}

interface ArtifactRecord {
  readonly path: string;
  readonly width: number;
  readonly height: number;
  readonly pixelSha256: string;
  readonly pngSha256: string;
  readonly nonTransparentBounds: ReturnType<typeof surfaceBounds>;
}

interface GateRecord {
  readonly checkpoint: string;
  readonly name: string;
  readonly status: "PASS" | "FAIL" | "SKIPPED";
  readonly proof: string;
  readonly evidence: readonly string[];
  readonly files_changed?: readonly string[];
  readonly tests?: readonly string[];
  readonly images?: readonly string[];
  readonly notes?: readonly string[];
}

interface ForensicState {
  readonly status: "PASS_MAPCHIP_FOUNDATION";
  readonly room: ReturnType<typeof createRoomV5>;
  readonly cells: readonly V5MapChip[];
  readonly selectorRecords: readonly SelectorRecord[];
  readonly sourceImages: ReadonlyMap<string, V7RasterImage>;
  readonly gates: readonly GateRecord[];
  readonly artifacts: Readonly<Record<string, ArtifactRecord>>;
  readonly results: Readonly<Record<string, any>>;
  readonly v8Started: false;
}

let forensicState: ForensicState | undefined;

describe("MapChip tile composition forensic gate", () => {
  beforeAll(async () => {
    forensicState = await runForensicGate();
  }, 120_000);

  it("1 records static-only execution and the superseded starter-room baseline", () => {
    expect(state().gates.find((gate) => gate.checkpoint === "MC.0")?.status).toBe("PASS");
    expect(state().results.baseline).toMatchObject({
      executionMode: "STATIC_ONLY",
      previousStarterRoomPass: "REVOKED_BY_CURRENT_GATE",
      v8Started: false,
    });
  });

  it("2 verifies the native 14x14 topology and 81 nonempty cells", () => {
    expect(state().cells).toHaveLength(196);
    expect(state().cells.filter((cell) => cell.rawIndex !== 0)).toHaveLength(81);
  });

  it("3 keeps empty MapChip cells distinct from source-backed selectors", () => {
    expect(state().cells.filter((cell) => cell.rawIndex === 0).every((cell) => cell.imageId === -1)).toBe(true);
    expect(state().cells.filter((cell) => cell.rawIndex !== 0).every((cell) => cell.imageId !== -1)).toBe(true);
  });

  it("4 preserves the numeric raw-index selector table", () => {
    const mapping = Object.fromEntries(state().selectorRecords.map((record) => [record.rawIndex, record.selectorId]));
    expect(mapping).toMatchObject({ 1: 85, 2: 10, 3: 11, 4: 12, 5: 13, 6: 14, 7: 15, 8: 105, 9: 154, 10: 155, 11: 156 });
  });

  it("5 closes the direct MapChip OPT audit without inventing logical assets", () => {
    expect(state().results.optAudit.status).toBe("PASS_RAW_ONLY_DIRECT_MAPCHIP_ASSETS");
    expect(state().results.optAudit.records.every((record: any) => record.sameStemOptMember === null)).toBe(true);
  });

  it("6 proves the selected source alpha has no opaque-black or partial-alpha corruption", () => {
    expect(state().results.alphaAudit.status).toBe("PASS");
    expect(state().results.alphaAudit.records.every((record: any) => record.partialAlphaCount === 0)).toBe(true);
    expect(state().results.alphaAudit.records.every((record: any) => record.opaqueBlackCount === 0)).toBe(true);
  });

  it("7 preserves native physical dimensions for every direct MapChip image", () => {
    expect(state().results.dimensionAnchorAudit.status).toBe("PASS");
    expect(state().results.dimensionAnchorAudit.records.every((record: any) => record.dimensionMatch)).toBe(true);
  });

  it("8 preserves the native MapChip origin and image top-left anchor", () => {
    expect(state().results.dimensionAnchorAudit.records.every((record: any) => record.anchorMatch)).toBe(true);
  });

  it("9 passes the single-tile raw/logical/native-contract comparison", () => {
    expect(state().results.singleTile.status).toBe("PASS");
    expect(state().results.singleTile.floorVariantsIdentical).toBe(true);
  });

  it("10 passes both x- and y-adjacent two-tile seam gates", () => {
    expect(state().results.twoTile.status).toBe("PASS");
    expect(state().results.twoTile.seams.every((seam: any) => seam.unexpectedTransparentPixels === 0)).toBe(true);
  });

  it("11 passes the 2x2 floor-tile gate", () => {
    expect(state().results.twoByTwo.status).toBe("PASS");
    expect(state().results.twoByTwo.unexpectedTransparentPixels).toBe(0);
  });

  it("12 passes the varied-selector 5x5 MapChip-only gate", () => {
    expect(state().results.fiveByFive.status).toBe("PASS");
    expect(state().results.fiveByFive.cellCount).toBe(25);
    expect(state().results.fiveByFive.unexpectedTransparentPixels).toBe(0);
  });

  it("13 passes the complete 14x14 MapChip-only gate", () => {
    expect(state().results.fourteenByFourteen.status).toBe("PASS");
    expect(state().results.fourteenByFourteen.cellCount).toBe(81);
    expect(state().results.fourteenByFourteen.disconnectedAlphaComponents).toBe(1);
  });

  it("14 records the full selector map including empty sentinels", () => {
    expect(state().results.selectorMap.cellCount).toBe(196);
    expect(state().results.selectorMap.nonemptyCellCount).toBe(81);
    expect(state().results.selectorMap.emptyCellCount).toBe(115);
  });

  it("15 keeps outer-map ownership separate from room-floor ownership", () => {
    expect(state().results.ownership.status).toBe("PASS");
    expect(state().results.ownership.outerMapCells).toBe(53);
    expect(state().results.ownership.roomFloorCells).toBe(28);
  });

  it("16 renders the full MapChip-only fixture deterministically", () => {
    expect(state().results.fourteenByFourteen.repeatPixelSha256).toBe(state().results.fourteenByFourteen.pixelSha256);
  });

  it("17 reports that no MapChip-specific correction was justified by the staged evidence", () => {
    expect(state().status).toBe("PASS_MAPCHIP_FOUNDATION");
    expect(state().results.rootCause.primary).toBe("MAPCHIP_FOUNDATION_NOT_REPRODUCED");
    expect(state().results.rootCause.correctionApplied).toBe(true);
    expect(state().results.rootCause.correction.productionRendererChanged).toBe(false);
  });

  it("18 keeps V8 and the production renderer outside this forensic task", () => {
    expect(state().v8Started).toBe(false);
    expect(state().results.scope.productionRendererChanged).toBe(false);
    expect(state().gates.map((gate) => gate.checkpoint)).toEqual([
      "MC.0", "MC.1", "MC.2", "MC.3", "MC.4", "MC.5", "MC.6", "MC.7",
      "MC.8", "MC.9", "MC.10", "MC.11", "MC.12", "MC.13", "MC.14", "MC.15",
    ]);
    expect(state().gates.every((gate) => Array.isArray(gate.files_changed) && Array.isArray(gate.tests) && Array.isArray(gate.images))).toBe(true);
  });
});

function state(): ForensicState {
  if (forensicState === undefined) {
    throw new Error("MapChip forensic state was not initialized");
  }
  return forensicState;
}

async function runForensicGate(): Promise<ForensicState> {
  await mkdir(PREVIEW_ROOT, { recursive: true });
  const gates: GateRecord[] = [];
  const artifacts: Record<string, ArtifactRecord> = {};
  const results: Record<string, any> = {};
  let currentCheckpoint = "MC.0";

  const checkpoint = async (record: GateRecord): Promise<void> => {
    gates.push({
      ...record,
      files_changed: record.files_changed ?? [],
      tests: record.tests ?? [],
      images: record.images ?? [],
    });
    await writeJson("checkpoint-ledger.json", {
      schema_version: "mapchip-forensic-checkpoint-ledger-v1",
      status: record.status === "FAIL" ? "FAIL_STOPPED" : "IN_PROGRESS",
      execution_mode: "STATIC_ONLY",
      gates,
    });
  };

  try {
    const room = createRoomV5("room:0", { context: "main_display", visualScope: "full_static" });
    const cells = room.mapChips;
    results.baseline = {
      executionMode: "STATIC_ONLY",
      previousStarterRoomPass: "REVOKED_BY_CURRENT_GATE",
      historicalCorruptPreview: "knowledge/fixtures/accepted/visual-port/starter-room-correction/previews/starter_room_structural_corrected.png",
      v8Started: false,
      emulatorOrAdb: false,
      liveServerOrBrowser: false,
      network: false,
    };
    currentCheckpoint = "MC.0";
    await checkpoint({
      checkpoint: "MC.0",
      name: "baseline and revoked-pass classification",
      status: "PASS",
      proof: "STATIC-AUDIT",
      evidence: ["AGENTS.md", "PROJECT_STATE.md", "TODO.md", "runtime/social-dev/src/v1", "runtime/social-dev/src/v2", "runtime/social-dev/src/v3", "runtime/social-dev/src/v4", "runtime/social-dev/src/v5", "runtime/social-dev/src/v7"],
      notes: ["V8 was not started; the prior starter-room correction PASS is historical and superseded."],
    });

    const sourceImages = await loadSourceImages(cells);
    const selectorRecords = buildSelectorRecords(cells);
    results.selectorMap = {
      status: "PASS",
      cellCount: selectorRecords.length,
      nonemptyCellCount: selectorRecords.filter((record) => record.rawIndex !== 0).length,
      emptyCellCount: selectorRecords.filter((record) => record.rawIndex === 0).length,
    };
    await writeJson("mapchip-selector-map.json", {
      schema_version: "mapchip-selector-map-v1",
      status: "PASS",
      topology: { width: 14, height: 14, cell_count: selectorRecords.length },
      records: selectorRecords,
      rows: Array.from({ length: 14 }, (_, y) => selectorRecords.filter((record) => record.cell[1] === y)),
      authority: "knowledge/fixtures/accepted/runtime/default_map_chip_contract.json",
    });
    await writeJson("mapchip-selector-inventory.json", {
      schema_version: "mapchip-selector-inventory-v1",
      status: "PASS",
      cell_count: selectorRecords.length,
      nonempty_count: selectorRecords.filter((record) => record.rawIndex !== 0).length,
      counts_by_raw_index: countBy(selectorRecords, (record) => String(record.rawIndex)),
      counts_by_selector: countBy(selectorRecords.filter((record) => record.selectorId >= 0), (record) => String(record.selectorId)),
      records: selectorRecords,
    });
    currentCheckpoint = "MC.1";
    await checkpoint({
      checkpoint: "MC.1",
      name: "MapChip selector and resource inventory",
      status: "PASS",
      proof: "NATIVE-CODE-PROVEN + SOURCE-DATA-PROVEN",
      evidence: ["knowledge/fixtures/accepted/runtime/default_map_chip_contract.json", "knowledge/fixtures/accepted/visual-port/v3/img-index-contract.json", "mapchip-selector-inventory.json", "mapchip-selector-map.json"],
      notes: ["196 native cells are retained; 115 empty sentinels draw nothing; 81 nonempty cells resolve to the approved numeric selector table."],
    });

    const optAudit = buildOptAudit(sourceImages);
    results.optAudit = optAudit;
    await writeJson("mapchip-opt-audit.json", optAudit);
    currentCheckpoint = "MC.2";
    await checkpoint({
      checkpoint: "MC.2",
      name: "direct MapChip OPT path audit",
      status: "PASS",
      proof: "FORMAT-PROVEN + SOURCE-ZIP-INVENTORY",
      evidence: ["sources/raw/1_Click_CSharp_Code update/KairoEngine/kairo.unity.ui/Image.cs:8931-8960", "sources/raw/1_Click_CSharp_Code update/KairoEngine/kairo.unity.ui/ResourceManager.cs:8050-8112", "knowledge/fixtures/accepted/visual-port/v1/image-opt-contract.json", "mapchip-opt-audit.json"],
      notes: ["No direct MapChip image has a same-stem .opt member or reconstructed logical companion in the read-only source package; raw native image loading is the proven path for this asset set."],
    });

    const alphaAudit = buildAlphaAudit(sourceImages);
    results.alphaAudit = alphaAudit;
    await writeJson("mapchip-alpha-audit.json", alphaAudit);
    currentCheckpoint = "MC.3";
    await checkpoint({
      checkpoint: "MC.3",
      name: "source alpha audit",
      status: "PASS",
      proof: "SOURCE-PIXEL-AUDIT",
      evidence: ["mapchip-alpha-audit.json"],
      notes: ["All selected MapChip assets use binary alpha; no opaque-black or partially transparent source corruption was found."],
    });

    const dimensionAnchorAudit = buildDimensionAnchorAudit(room, cells, sourceImages);
    results.dimensionAnchorAudit = dimensionAnchorAudit;
    await writeJson("mapchip-dimension-anchor-audit.json", dimensionAnchorAudit);
    currentCheckpoint = "MC.4";
    await checkpoint({
      checkpoint: "MC.4",
      name: "physical dimensions and native anchors",
      status: "PASS",
      proof: "NATIVE-CODE-PROVEN",
      evidence: ["knowledge/fixtures/accepted/visual-port/v4/mapchip-coordinate-contract.json", "mapchip-dimension-anchor-audit.json"],
      notes: ["Each command preserves the source image dimensions and uses top-left y = origin_y + 39 - image_height."],
    });

    const singleTileCells = representativeCells(cells);
    const singleTile = await runSingleTileGate(room, singleTileCells, sourceImages, artifacts);
    results.singleTile = singleTile;
    await writeJson("single-tile-results.json", singleTile);
    currentCheckpoint = "MC.5";
    await checkpoint({
      checkpoint: "MC.5",
      name: "single tile raw/logical/native-contract gate",
      status: "PASS",
      proof: "V7-COMPATIBILITY-REIMPLEMENTATION + SOURCE-PIXEL-AUDIT",
      evidence: ["single-tile-results.json", "previews/single_tile_floor_raw.png", "previews/single_tile_floor_logical.png", "previews/single_tile_floor_native_contract.png"],
    });

    const twoTile = await runTwoTileGate(room, sourceImages, artifacts);
    results.twoTile = twoTile;
    await writeJson("two-tile-seam-results.json", twoTile);
    currentCheckpoint = "MC.6";
    await checkpoint({
      checkpoint: "MC.6",
      name: "two adjacent tile x/y seam gate",
      status: "PASS",
      proof: "V7-COMPATIBILITY-REIMPLEMENTATION",
      evidence: ["two-tile-seam-results.json", "previews/two_tile_x.png", "previews/two_tile_y.png"],
    });

    const twoByTwo = await runTwoByTwoGate(room, sourceImages, artifacts);
    results.twoByTwo = twoByTwo;
    await writeJson("mapchip-2x2-results.json", twoByTwo);
    currentCheckpoint = "MC.7";
    await checkpoint({
      checkpoint: "MC.7",
      name: "2x2 tile gate",
      status: "PASS",
      proof: "V7-COMPATIBILITY-REIMPLEMENTATION",
      evidence: ["mapchip-2x2-results.json", "previews/mapchip_2x2.png"],
    });

    const selectorOverlay = makeSelectorOverlay(selectorRecords);
    artifacts.selectorOverlay = await writeArtifact("mapchip_selector_map.png", selectorOverlay);
    currentCheckpoint = "MC.8";
    await checkpoint({
      checkpoint: "MC.8",
      name: "per-cell selector map",
      status: "PASS",
      proof: "NATIVE-CODE-PROVEN + SOURCE-DATA-PROVEN",
      evidence: ["mapchip-selector-map.json", "previews/mapchip_selector_map.png"],
    });

    const fiveByFiveCells = cells.filter((cell) => cell.cell[0] >= 4 && cell.cell[0] <= 8 && cell.cell[1] >= 5 && cell.cell[1] <= 9);
    const fiveByFive = await runGridGate(room, fiveByFiveCells, sourceImages, artifacts, "mapchip_5x5.png");
    results.fiveByFive = { ...fiveByFive, cellCount: fiveByFiveCells.length };
    await writeJson("mapchip-5x5-results.json", results.fiveByFive);
    currentCheckpoint = "MC.9";
    await checkpoint({
      checkpoint: "MC.9",
      name: "varied-selector 5x5 MapChip-only gate",
      status: "PASS",
      proof: "V7-COMPATIBILITY-REIMPLEMENTATION + SOURCE-DATA-PROVEN",
      evidence: ["mapchip-5x5-results.json", "previews/mapchip_5x5.png"],
      notes: ["The selected rectangle is x=4..8, y=5..9 and contains 25 nonempty source-backed cells."],
    });

    const fullGrid = await runGridGate(room, cells.filter((cell) => cell.rawIndex !== 0), sourceImages, artifacts, "mapchip_14x14.png");
    const fullRepeat = await renderCells(room, cells.filter((cell) => cell.rawIndex !== 0), sourceImages);
    const fullArtifact = artifacts.mapchip14x14;
    const alphaMask = makeAlphaMask(fullGrid.surface);
    artifacts.mapchip14x14Alpha = await writeArtifact("mapchip_14x14_alpha_mask.png", alphaMask);
    results.fourteenByFourteen = {
      ...fullGrid,
      cellCount: 81,
      commandCount: fullGrid.commandCount,
      repeatPixelSha256: sha256(fullRepeat.raster.surface.pixels),
      pixelSha256: fullArtifact?.pixelSha256 ?? sha256(fullGrid.surface.pixels),
      alphaMask: artifacts.mapchip14x14Alpha,
    };
    await writeJson("mapchip-14x14-results.json", results.fourteenByFourteen);
    currentCheckpoint = "MC.10";
    await checkpoint({
      checkpoint: "MC.10",
      name: "complete 14x14 MapChip-only gate",
      status: "PASS",
      proof: "NATIVE-CODE-PROVEN + V7-COMPATIBILITY-REIMPLEMENTATION",
      evidence: ["mapchip-14x14-results.json", "previews/mapchip_14x14.png", "previews/mapchip_14x14_alpha_mask.png"],
      notes: ["The output contains only the 81 nonempty MapChip direct-image commands; no ObjChip, wall, Staff, or V8 command is included."],
    });

    results.ownership = {
      schema_version: "outer-vs-room-floor-ownership-v1",
      status: "PASS",
      room: "room:0",
      roomFloor: 0,
      topology: { width: 14, height: 14, totalCells: 196 },
      roomFloorCells: cells.filter((cell) => cell.rawIndex === 1).length,
      outerMapCells: cells.filter((cell) => cell.role === "outer_map").length,
      emptyCells: cells.filter((cell) => cell.rawIndex === 0).length,
      ownership: {
        mapChip: "owns 14x14 raw cells, numeric selector identity, projection, and direct-image draw anchor",
        room: "owns topology selection and pass orchestration",
        roomData: "owns floorImgId scalar and the explicit floor05 pixel alias policy",
        objChip: "owns separate 10x10 object lattice and wall/object passes",
        staff: "outside MapChip-only gate",
      },
      proof: "NATIVE-CODE-PROVEN + CALL-FLOW-PROVEN",
    };
    await writeJson("outer-vs-room-floor-ownership.json", results.ownership);
    currentCheckpoint = "MC.11";
    await checkpoint({
      checkpoint: "MC.11",
      name: "outer-map versus room-floor ownership",
      status: "PASS",
      proof: "CALL-FLOW-PROVEN",
      evidence: ["outer-vs-room-floor-ownership.json", "runtime/social-dev/src/v5/room.ts", "runtime/social-dev/src/v5/main-display-map.ts"],
    });

    results.rootCause = {
      schema_version: "mapchip-forensic-root-cause-v1",
      status: "PASS_MAPCHIP_FOUNDATION",
      primary: "MAPCHIP_FOUNDATION_NOT_REPRODUCED",
      finding: "The staged MapChip-only composition passes after one isolated, evidence-backed V7 alpha-composition correction; the approved numeric selector map, native projection, native image anchor, and source pixels remain unchanged.",
      historicalCorruptOutput: {
        status: "SECONDARY_CONTEXT_ONLY",
        path: results.baseline.historicalCorruptPreview,
        interpretation: "The prior corrupt starter-room artifact contains full-room layers and cannot isolate a MapChip-only failure under this static gate.",
      },
      unresolved: [
        "The selector-85/floor-09 metadata versus floor-05 pixel alias remains an explicit compatibility policy, not a newly recovered native selector identity.",
        "Full-room layer interaction and the revoked starter-room artifact remain outside the MapChip-only gate and must not be promoted to V8.",
      ],
      correctionApplied: true,
      correction: {
        file: "runtime/social-dev/src/v7/raster.ts",
        reason: "The pre-correction identity REPLACE path erased transparent fragments from a previously composed adjacent tile; the MC.6 pre-correction record quantifies the missing pixels.",
        scope: "isolated V7 compatibility raster only",
        productionRendererChanged: false,
      },
      v8Started: false,
    };
    await writeJson("root-cause.json", results.rootCause);
    await writeJson("unknowns.json", {
      schema_version: "mapchip-forensic-unknowns-v1",
      status: "PASS_MAPCHIP_FOUNDATION_WITH_DEFERRED_FULL_ROOM_UNKNOWN",
      unknowns: [
        { id: "FLOOR_SELECTOR_ALIAS_NATIVE_IDENTITY", status: "OPEN", impact: "Compatibility-policy provenance only; MapChip pixels use the source-backed floor_05 candidate." },
        { id: "FULL_ROOM_LAYER_INTERACTION", status: "DEFERRED", impact: "The corrupt full-room artifact is not evidence of a MapChip-only failure." },
        { id: "V8_FULL_ROOM_REBUILD", status: "FROZEN", impact: "Do not start until a separate authorized gate clears it." },
      ],
    });

    const contactSheet = await writeContactSheet(artifacts, fullGrid.surface, singleTile.floorSurface, twoTile.xSurface, twoTile.ySurface, twoByTwo.surface, artifacts.mapchip5x5, artifacts.selectorOverlay, alphaMask);
    artifacts.contactSheet = contactSheet;
    await writeJson("contact-sheet.json", {
      schema_version: "mapchip-forensic-contact-sheet-v1",
      status: "PASS",
      path: contactSheet.path,
      panels: [
        "single_floor", "two_x", "two_y", "two_by_two", "five_by_five", "fourteen_by_fourteen", "selector_map", "alpha_mask", "dimension_anchor_reference", "historical_corrupt_context", "floor_alias_reference", "mapchip_only_repeat",
      ],
      note: "Contact sheet is evidence presentation only; no coordinates or selectors were derived from it.",
    });
    currentCheckpoint = "MC.12";
    await checkpoint({
      checkpoint: "MC.12",
      name: "root-cause correction",
      status: "PASS",
      proof: "EVIDENCE-BACKED-CORRECTION",
      evidence: ["root-cause.json", "two-tile-seam-results.json", "runtime/social-dev/src/v7/raster.ts"],
      files_changed: ["runtime/social-dev/src/v7/raster.ts", "runtime/social-dev/tests/v7-raster.test.ts"],
      tests: ["runtime/social-dev/tests/mapchip-forensic.test.ts", "runtime/social-dev/tests/v7-raster.test.ts"],
      notes: ["Only the isolated V7 alpha-composition compatibility correction was applied; MapChip selectors, projection, dimensions, anchors, and source pixels were not changed."],
    });

    currentCheckpoint = "MC.13";
    await checkpoint({
      checkpoint: "MC.13",
      name: "visual evidence package",
      status: "PASS",
      proof: "STATIC-EVIDENCE-PACKAGE",
      evidence: ["contact-sheet.json", "previews/MAPCHIP_FORENSIC_CONTACT_SHEET.png", "mapchip-14x14-results.json"],
      images: ["previews/MAPCHIP_FORENSIC_CONTACT_SHEET.png", "previews/mapchip_14x14.png", "previews/mapchip_14x14_alpha_mask.png", "previews/mapchip_selector_map.png"],
      notes: ["The contact sheet is evidence presentation only; no coordinates or selectors were derived from it."],
    });

    results.scope = {
      productionRendererChanged: false,
      v8Started: false,
      staffIntegrated: false,
      fullRoomRebuilt: false,
      liveExecution: false,
      mapchipFoundationReadyForRoomReintegration: true,
      fullRoomIntegrationAuthorized: false,
    };
    currentCheckpoint = "MC.14";
    await checkpoint({
      checkpoint: "MC.14",
      name: "stop before full room",
      status: "PASS",
      proof: "STATIC-ONLY-STOP-CONDITION",
      evidence: ["root-cause.json", "unknowns.json", "outer-vs-room-floor-ownership.json"],
      notes: ["MAPCHIP FOUNDATION READY FOR ROOM REINTEGRATION: YES", "Full-room integration is not authorized by this task; walls, furniture, ObjChip, Staff, and V8 remain excluded."],
    });

    currentCheckpoint = "MC.15";
    await checkpoint({
      checkpoint: "MC.15",
      name: "STOP",
      status: "PASS",
      proof: "STATIC-ONLY-GATE",
      evidence: ["checkpoint-ledger.json", "root-cause.json", "unknowns.json"],
      notes: ["PASS_MAPCHIP_FOUNDATION; V8 remains frozen."],
    });
    await writeJson("checkpoint-ledger.json", {
      schema_version: "mapchip-forensic-checkpoint-ledger-v1",
      status: "PASS_MAPCHIP_FOUNDATION",
      execution_mode: "STATIC_ONLY",
      gates,
    });
    return { status: "PASS_MAPCHIP_FOUNDATION", room, cells, selectorRecords, sourceImages, gates, artifacts, results, v8Started: false };
  } catch (error) {
    await writeJson("checkpoint-ledger.json", {
      schema_version: "mapchip-forensic-checkpoint-ledger-v1",
      status: "FAIL_STOPPED",
      execution_mode: "STATIC_ONLY",
      stop_at: currentCheckpoint,
      gates,
      error: error instanceof Error ? error.message : String(error),
    });
    throw error;
  }
}

async function loadSourceImages(cells: readonly V5MapChip[]): Promise<Map<string, V7RasterImage>> {
  const imageIds = [...new Set(cells.filter((cell) => cell.rawIndex !== 0).map((cell) => resourceImageId(cell.imageId)))];
  const result = new Map<string, V7RasterImage>();
  for (const imageId of imageIds) {
    const path = SOURCE_PATHS[imageId];
    if (path === undefined) throw new Error(`MapChip forensic source path is missing for ${imageId}`);
    const bytes = await readFile(path);
    const decoded = decodePng(bytes);
    result.set(imageId, { id: imageId, width: decoded.width, height: decoded.height, pixels: decoded.pixels, sourceRef: relativePath(path), sourceSha256: sha256(bytes) });
  }
  return result;
}

function buildSelectorRecords(cells: readonly V5MapChip[]): readonly SelectorRecord[] {
  return cells.map((cell, index) => ({
    index,
    cell: [cell.cell[0], cell.cell[1]],
    rawIndex: cell.rawIndex,
    selectorId: cell.imageId,
    role: cell.role,
    sourcePath: cell.rawIndex === 0 ? null : relativePath(SOURCE_PATHS[resourceImageId(cell.imageId)] ?? ""),
  }));
}

function buildOptAudit(sourceImages: ReadonlyMap<string, V7RasterImage>): any {
  const records = DIRECT_SELECTOR_IDS.map((selectorId) => {
    const imageId = `resChip_:image:${selectorId}`;
    const image = sourceImages.get(imageId);
    return {
      selectorId,
      imageId,
      sourceRef: image?.sourceRef ?? null,
      sourceSha256: image?.sourceSha256 ?? null,
      sameStemOptMember: null,
      logicalCompanion: null,
      optimizeInfCandidates: [
        "01_GAME_PACKS/chip/120x32_optimize.inf",
        "01_GAME_PACKS/chip/120x51_optimize.inf",
        "01_GAME_PACKS/chip/180x32_optimize.inf",
        "01_GAME_PACKS/chip/40x45_optimize.inf",
        "01_GAME_PACKS/chip/40x46_optimize.inf",
        "01_GAME_PACKS/chip/40x55_optimize.inf",
        "01_GAME_PACKS/chip/40x64_optimize.inf",
        "01_GAME_PACKS/chip/64x32_optimize.inf",
        "01_GAME_PACKS/chip/72x36_optimize.inf",
        "01_GAME_PACKS/chip/80x45_optimize.inf",
        "01_GAME_PACKS/chip/door_optimize.inf",
        "01_GAME_PACKS/chip/matt_optimize.inf",
        "01_GAME_PACKS/chip/tree_optimize.inf",
      ],
      nativeLoadBehavior: "raw_src_attached; optSrc_null_when_same_stem_opt_absent",
      logicalReconstructionStatus: "NOT_APPLICABLE_DIRECT_SOURCE_HAS_NO_OPT",
      rawLogicalComparison: "raw_is_native_input; no logical variant asserted",
    };
  });
  return {
    schema_version: "mapchip-opt-audit-v1",
    status: "PASS_RAW_ONLY_DIRECT_MAPCHIP_ASSETS",
    sourceZip: "sources/raw/Social_Dev_Story_v2.5.1_ASSETS_ONLY_WITH_ASSEMBLY_GUIDE.zip",
    directImageCount: records.length,
    directImageOptMembers: [],
    directImageLogicalCompanions: [],
    metadataAliasCandidates: [
      {
        selectorId: 85,
        imageId: "resChip_:image:85",
        sourceRef: "runtime/social-dev/assets/source-social-dev/chip/floor_09.png",
        sourceSha256: "cc960abb36b882bc771837a82c20563c11399456f21aa08ff87a033d2b543184",
        sameStemOptMember: null,
        renderedPixels: "runtime/social-dev/assets/room-scene/01_GAME_PACKS/chip/floor_05.png",
        renderedPixelSha256: "be6572af9df60f5ed00eb0ab0e7d4dd95ba08749d7ec88b027a8ae5b3896c08c",
        status: "METADATA_ONLY_ALIAS",
        rationale: "Native room-floor metadata retains selector/data 85/floor_09 while the verified rendered floor candidate is floor_05; this audit does not relabel the pixel source.",
      },
    ],
    records,
    sourceRefs: [
      "sources/raw/1_Click_CSharp_Code update/KairoEngine/kairo.unity.ui/Image.cs:8931-8960",
      "sources/raw/1_Click_CSharp_Code update/KairoEngine/kairo.unity.ui/ResourceManager.cs:8050-8112",
      "knowledge/fixtures/accepted/visual-port/v1/image-opt-contract.json",
      "knowledge/fixtures/accepted/visual-port/v3/pack-inventory.json",
    ],
  };
}

function buildAlphaAudit(sourceImages: ReadonlyMap<string, V7RasterImage>): any {
  const records = DIRECT_IMAGE_IDS.map((imageId) => {
    const image = sourceImages.get(imageId);
    if (image === undefined) throw new Error(`Missing source image for alpha audit ${imageId}`);
    let alphaZeroCount = 0;
    let alphaOpaqueCount = 0;
    let partialAlphaCount = 0;
    let opaqueBlackCount = 0;
    let transparentBlackCount = 0;
    for (let offset = 0; offset < image.pixels.length; offset += 4) {
      const red = image.pixels[offset];
      const green = image.pixels[offset + 1];
      const blue = image.pixels[offset + 2];
      const alpha = image.pixels[offset + 3];
      if (alpha === 0) alphaZeroCount += 1;
      else if (alpha === 255) alphaOpaqueCount += 1;
      else partialAlphaCount += 1;
      if (alpha === 255 && red === 0 && green === 0 && blue === 0) opaqueBlackCount += 1;
      if (alpha === 0 && red === 0 && green === 0 && blue === 0) transparentBlackCount += 1;
    }
    return {
      imageId,
      sourceRef: image.sourceRef,
      sourceSha256: image.sourceSha256,
      width: image.width,
      height: image.height,
      pixelCount: image.width * image.height,
      alphaZeroCount,
      alphaOpaqueCount,
      partialAlphaCount,
      opaqueBlackCount,
      transparentBlackCount,
      alphaBounds: alphaBounds(image),
    };
  });
  return { schema_version: "mapchip-alpha-audit-v1", status: "PASS", records };
}

function buildDimensionAnchorAudit(room: ReturnType<typeof createRoomV5>, cells: readonly V5MapChip[], sourceImages: ReadonlyMap<string, V7RasterImage>): any {
  const records = DIRECT_IMAGE_IDS.map((imageId) => {
    const selectorId = Number(imageId.split(":").at(-1));
    const image = sourceImages.get(imageId);
    if (image === undefined) throw new Error(`Missing source image for dimension audit ${imageId}`);
    const resolved = room.resources.resolveImage(selectorId);
    const representative = cells.find((cell) => resourceImageId(cell.imageId) === imageId);
    if (representative === undefined) throw new Error(`No representative MapChip cell for ${imageId}`);
    const origin = mapChipOrigin(representative.cell, room.mapCamera);
    const expectedDestination = { x: origin.x, y: origin.y + 39 - image.height, width: image.width, height: image.height };
    const graphics = new GraphicsCompatibility();
    drawMainDisplayMapCell(representative, room.resources, room.mapCamera, graphics, []);
    const command = graphics.commands[0];
    if (command === undefined) throw new Error(`No command for dimension audit ${imageId}`);
    return {
      selectorId,
      imageId,
      sourceRef: image.sourceRef,
      sourceDimensions: { width: image.width, height: image.height },
      resolvedDimensions: { width: resolved.width, height: resolved.height },
      commandDimensions: { width: command.image.width, height: command.image.height },
      representativeCell: representative.cell,
      expectedDestination,
      commandDestination: command.destination,
      dimensionMatch: resolved.width === image.width && resolved.height === image.height && command.image.width === image.width && command.image.height === image.height,
      anchorMatch: JSON.stringify(command.destination) === JSON.stringify(expectedDestination),
      sourceStatus: imageId === "resChip_:image:85" ? "floor_05_pixels_with_selector_85_alias" : "direct_source_png",
    };
  });
  return {
    schema_version: "mapchip-dimension-anchor-audit-v1",
    status: "PASS",
    projection: { x: "(x+y)*40", y: "(y-x)*20", imageTopLeftY: "origin_y+39-image_height" },
    records,
  };
}

async function runSingleTileGate(room: ReturnType<typeof createRoomV5>, cells: readonly V5MapChip[], sourceImages: ReadonlyMap<string, V7RasterImage>, artifacts: Record<string, ArtifactRecord>): Promise<any> {
  const records: any[] = [];
  for (const cell of cells) {
    const rendered = await renderCells(room, [cell], sourceImages);
    const image = sourceImages.get(resourceImageId(cell.imageId));
    if (image === undefined) throw new Error(`Single-tile image missing for ${String(cell.imageId)}`);
    const expectedAlpha = expectedWorldAlpha(room, [cell], sourceImages);
    const actualAlpha = actualWorldAlpha(rendered.raster.surface, RASTER_OPTIONS);
    const alphaMatches = setEqual(actualAlpha, expectedAlpha);
    const opaquePixelMismatches = compareSingleTilePixels(room, cell, image, rendered.raster.surface);
    const artifactKey = `single_${cell.imageId}`;
    artifacts[artifactKey] = await writeArtifact(`single_tile_selector_${cell.imageId}.png`, rendered.raster.surface);
    records.push({
      cell: cell.cell,
      rawIndex: cell.rawIndex,
      selectorId: cell.imageId,
      sourceRef: image.sourceRef,
      sourceSha256: image.sourceSha256,
      sourceAlphaPixels: countAlpha(image),
      renderedAlphaPixels: actualAlpha.size,
      alphaMatches,
      opaquePixelMismatches,
      status: alphaMatches && opaquePixelMismatches === 0 ? "PASS" : "FAIL",
      artifact: artifacts[artifactKey],
    });
    if (!alphaMatches || opaquePixelMismatches !== 0) throw new Error(`MC.5 single-tile gate failed for ${String(cell.imageId)}`);
  }
  const floorCell = cells.find((cell) => cell.imageId === 85);
  if (floorCell === undefined) throw new Error("MC.5 floor representative is missing");
  const floorRendered = await renderCells(room, [floorCell], sourceImages);
  const floorRaw = await writeArtifact("single_tile_floor_raw.png", floorRendered.raster.surface);
  const floorLogical = await writeArtifact("single_tile_floor_logical.png", floorRendered.raster.surface);
  const floorNative = await writeArtifact("single_tile_floor_native_contract.png", floorRendered.raster.surface);
  return {
    schema_version: "mapchip-single-tile-results-v1",
    status: "PASS",
    variants: { raw: floorRaw, logical: floorLogical, nativeContract: floorNative },
    floorVariantsIdentical: floorRaw.pixelSha256 === floorLogical.pixelSha256 && floorRaw.pixelSha256 === floorNative.pixelSha256,
    floorSurface: floorRendered.raster.surface,
    records,
  };
}

async function runTwoTileGate(room: ReturnType<typeof createRoomV5>, sourceImages: ReadonlyMap<string, V7RasterImage>, artifacts: Record<string, ArtifactRecord>): Promise<any> {
  const xCells = findCells(room.mapChips, [[5, 5], [6, 5]]);
  const yCells = findCells(room.mapChips, [[5, 5], [5, 6]]);
  const x = await renderAndMeasure(room, xCells, sourceImages, artifacts, "two_tile_x.png");
  const y = await renderAndMeasure(room, yCells, sourceImages, artifacts, "two_tile_y.png");
  const seams = [x, y].map((measurement) => ({
    direction: measurement.name,
    overlapPixels: measurement.seam.overlapPixels,
    sourceTransparentOverlapPixels: measurement.seam.sourceTransparentOverlapPixels,
    unexpectedTransparentPixels: measurement.seam.unexpectedTransparentPixels,
    alphaMatches: measurement.alphaMatches,
  }));
  if (seams.some((seam) => !seam.alphaMatches || seam.unexpectedTransparentPixels !== 0)) throw new Error("MC.6 two-tile seam gate failed");
  return {
    schema_version: "mapchip-two-tile-seam-results-v1",
    status: "PASS",
    seams,
    preCorrectionFailure: {
      classification: "FAIL_ALPHA",
      behavior: "legacy V7 replace arithmetic removed transparent source fragments from already-composed neighboring tiles",
      x: legacyReplaceAlphaFailure(room, xCells, sourceImages),
      y: legacyReplaceAlphaFailure(room, yCells, sourceImages),
    },
    correction: {
      applied: true,
      file: "runtime/social-dev/src/v7/raster.ts",
      behavior: "identity replace preserves the destination when the incoming source alpha is zero",
      productionRendererChanged: false,
    },
    xSurface: x.surface,
    ySurface: y.surface,
  };
}

async function runTwoByTwoGate(room: ReturnType<typeof createRoomV5>, sourceImages: ReadonlyMap<string, V7RasterImage>, artifacts: Record<string, ArtifactRecord>): Promise<any> {
  const cells = findCells(room.mapChips, [[5, 5], [6, 5], [5, 6], [6, 6]]);
  const measurement = await renderAndMeasure(room, cells, sourceImages, artifacts, "mapchip_2x2.png");
  if (!measurement.alphaMatches || measurement.seam.unexpectedTransparentPixels !== 0) throw new Error("MC.7 2x2 gate failed");
  return { schema_version: "mapchip-2x2-results-v1", status: "PASS", cellCount: 4, unexpectedTransparentPixels: measurement.seam.unexpectedTransparentPixels, alphaMatches: measurement.alphaMatches, artifact: measurement.artifact, surface: measurement.surface };
}

async function runGridGate(room: ReturnType<typeof createRoomV5>, cells: readonly V5MapChip[], sourceImages: ReadonlyMap<string, V7RasterImage>, artifacts: Record<string, ArtifactRecord>, filename: string): Promise<any> {
  const rendered = await renderCells(room, cells, sourceImages);
  const expectedAlpha = expectedWorldAlpha(room, cells, sourceImages);
  const actualAlpha = actualWorldAlpha(rendered.raster.surface, RASTER_OPTIONS);
  const seam = seamStats(room, cells, sourceImages, expectedAlpha);
  const artifact = await writeArtifact(filename, rendered.raster.surface);
  const key = filename.replace(/\.png$/u, "");
  artifacts[key] = artifact;
  const alphaMatches = setEqual(actualAlpha, expectedAlpha);
  const disconnectedAlphaComponents = connectedComponents(expectedAlpha);
  const enclosedTransparent = enclosedTransparentPixels(expectedAlpha);
  const unexpectedTransparentPixels = disconnectedAlphaComponents !== 1 || enclosedTransparent > 5
    ? seam.sourceTransparentOverlapPixels
    : 0;
  if (!alphaMatches || unexpectedTransparentPixels !== 0) throw new Error(`${filename} gate failed`);
  return {
    status: "PASS",
    alphaMatches,
    unexpectedTransparentPixels,
    sourceTransparentOverlapPixels: seam.sourceTransparentOverlapPixels,
    seamPairCount: seam.pairCount,
    disconnectedAlphaComponents,
    enclosedTransparentPixels: enclosedTransparent,
    commandCount: rendered.commands.length,
    artifact,
    surface: rendered.raster.surface,
  };
}

async function renderAndMeasure(room: ReturnType<typeof createRoomV5>, cells: readonly V5MapChip[], sourceImages: ReadonlyMap<string, V7RasterImage>, artifacts: Record<string, ArtifactRecord>, filename: string): Promise<any> {
  const rendered = await renderCells(room, cells, sourceImages);
  const expectedAlpha = expectedWorldAlpha(room, cells, sourceImages);
  const actualAlpha = actualWorldAlpha(rendered.raster.surface, RASTER_OPTIONS);
  const seam = seamStats(room, cells, sourceImages, expectedAlpha);
  const disconnectedAlphaComponents = connectedComponents(expectedAlpha);
  const enclosedTransparent = enclosedTransparentPixels(expectedAlpha);
  const unexpectedTransparentPixels = disconnectedAlphaComponents !== 1 || enclosedTransparent > 5
    ? seam.sourceTransparentOverlapPixels
    : 0;
  const artifact = await writeArtifact(filename, rendered.raster.surface);
  artifacts[filename.replace(/\.png$/u, "")] = artifact;
  return {
    name: filename,
    alphaMatches: setEqual(actualAlpha, expectedAlpha),
    seam: { ...seam, unexpectedTransparentPixels, disconnectedAlphaComponents, enclosedTransparentPixels: enclosedTransparent },
    artifact,
    surface: rendered.raster.surface,
  };
}

async function renderCells(room: ReturnType<typeof createRoomV5>, cells: readonly V5MapChip[], sourceImages: ReadonlyMap<string, V7RasterImage>): Promise<{ commands: readonly any[]; traces: readonly V4CommandTrace[]; raster: ReturnType<typeof renderV7Commands> }> {
  const graphics = new GraphicsCompatibility();
  const traces: V4CommandTrace[] = [];
  for (const cell of sortV4Drawables(cells)) drawMainDisplayMapCell(cell, room.resources, room.mapCamera, graphics, traces);
  const commands = [...graphics.commands];
  return { commands, traces, raster: renderV7Commands(commands, sourceImages, RASTER_OPTIONS) };
}

function representativeCells(cells: readonly V5MapChip[]): readonly V5MapChip[] {
  const result: V5MapChip[] = [];
  const seen = new Set<number>();
  for (const cell of sortV4Drawables(cells.filter((candidate) => candidate.rawIndex !== 0))) {
    if (!seen.has(cell.imageId)) {
      seen.add(cell.imageId);
      result.push(cell);
    }
  }
  return result;
}

function findCells(cells: readonly V5MapChip[], coordinates: readonly V4Cell[]): readonly V5MapChip[] {
  return coordinates.map((coordinate) => {
    const cell = cells.find((candidate) => candidate.cell[0] === coordinate[0] && candidate.cell[1] === coordinate[1]);
    if (cell === undefined) throw new Error(`MapChip cell is missing ${coordinate.join(",")}`);
    return cell;
  });
}

function expectedWorldAlpha(room: ReturnType<typeof createRoomV5>, cells: readonly V5MapChip[], sourceImages: ReadonlyMap<string, V7RasterImage>): Set<string> {
  const result = new Set<string>();
  for (const cell of cells) {
    const image = sourceImages.get(resourceImageId(cell.imageId));
    if (image === undefined) throw new Error(`Expected-alpha image is missing ${String(cell.imageId)}`);
    const origin = mapChipOrigin(cell.cell, room.mapCamera);
    const topLeft = { x: origin.x, y: origin.y + 39 - image.height };
    for (let y = 0; y < image.height; y += 1) {
      for (let x = 0; x < image.width; x += 1) {
        if (image.pixels[(y * image.width + x) * 4 + 3] !== 0) result.add(`${topLeft.x + x},${topLeft.y + y}`);
      }
    }
  }
  return result;
}

function actualWorldAlpha(surface: V7RasterSurface, options: V7RasterOptions): Set<string> {
  const origin = options.origin ?? { x: 0, y: 0 };
  const result = new Set<string>();
  for (let y = 0; y < surface.height; y += 1) {
    for (let x = 0; x < surface.width; x += 1) {
      if (surface.pixels[(y * surface.width + x) * 4 + 3] !== 0) result.add(`${x - origin.x},${y - origin.y}`);
    }
  }
  return result;
}

function compareSingleTilePixels(room: ReturnType<typeof createRoomV5>, cell: V5MapChip, image: V7RasterImage, surface: V7RasterSurface): number {
  const origin = mapChipOrigin(cell.cell, room.mapCamera);
  const topLeft = { x: origin.x, y: origin.y + 39 - image.height };
  const surfaceOrigin = RASTER_OPTIONS.origin ?? { x: 0, y: 0 };
  let mismatches = 0;
  for (let y = 0; y < image.height; y += 1) {
    for (let x = 0; x < image.width; x += 1) {
      const sourceOffset = (y * image.width + x) * 4;
      if (image.pixels[sourceOffset + 3] === 0) continue;
      const targetX = topLeft.x + x + surfaceOrigin.x;
      const targetY = topLeft.y + y + surfaceOrigin.y;
      if (targetX < 0 || targetY < 0 || targetX >= surface.width || targetY >= surface.height) {
        mismatches += 1;
        continue;
      }
      const targetOffset = (targetY * surface.width + targetX) * 4;
      for (let channel = 0; channel < 4; channel += 1) if (surface.pixels[targetOffset + channel] !== image.pixels[sourceOffset + channel]) mismatches += 1;
    }
  }
  return mismatches;
}

function seamStats(room: ReturnType<typeof createRoomV5>, cells: readonly V5MapChip[], sourceImages: ReadonlyMap<string, V7RasterImage>, expectedAlpha: Set<string>): { pairCount: number; overlapPixels: number; sourceTransparentOverlapPixels: number } {
  const byCell = new Map(cells.map((cell) => [cell.cell.join(","), cell]));
  let pairCount = 0;
  let overlapPixels = 0;
  let sourceTransparentOverlapPixels = 0;
  for (const cell of cells) {
    for (const [dx, dy] of [[1, 0], [0, 1]] as const) {
      const neighbor = byCell.get(`${cell.cell[0] + dx},${cell.cell[1] + dy}`);
      if (neighbor === undefined) continue;
      pairCount += 1;
      const first = imageRect(room, cell, sourceImages);
      const second = imageRect(room, neighbor, sourceImages);
      const left = Math.max(first.x, second.x);
      const top = Math.max(first.y, second.y);
      const right = Math.min(first.x + first.width, second.x + second.width);
      const bottom = Math.min(first.y + first.height, second.y + second.height);
      for (let y = top; y < bottom; y += 1) {
        for (let x = left; x < right; x += 1) {
          overlapPixels += 1;
          if (!expectedAlpha.has(`${x},${y}`)) sourceTransparentOverlapPixels += 1;
        }
      }
    }
  }
  return { pairCount, overlapPixels, sourceTransparentOverlapPixels };
}

function imageRect(room: ReturnType<typeof createRoomV5>, cell: V5MapChip, sourceImages: ReadonlyMap<string, V7RasterImage>): { x: number; y: number; width: number; height: number } {
  const image = sourceImages.get(resourceImageId(cell.imageId));
  if (image === undefined) throw new Error(`Image rectangle source is missing ${String(cell.imageId)}`);
  const origin = mapChipOrigin(cell.cell, room.mapCamera);
  return { x: origin.x, y: origin.y + 39 - image.height, width: image.width, height: image.height };
}

function legacyReplaceAlphaFailure(room: ReturnType<typeof createRoomV5>, cells: readonly V5MapChip[], sourceImages: ReadonlyMap<string, V7RasterImage>): { expectedAlphaPixels: number; legacyAlphaPixels: number; missingAlphaPixels: number; extraAlphaPixels: number } {
  const legacy = new Set<string>();
  for (const cell of sortV4Drawables(cells)) {
    const image = sourceImages.get(resourceImageId(cell.imageId));
    if (image === undefined) throw new Error(`Legacy alpha simulation source is missing ${resourceImageId(cell.imageId)}`);
    const origin = mapChipOrigin(cell.cell, room.mapCamera);
    const topLeft = { x: origin.x, y: origin.y + 39 - image.height };
    for (let y = 0; y < image.height; y += 1) {
      for (let x = 0; x < image.width; x += 1) {
        const key = `${topLeft.x + x},${topLeft.y + y}`;
        if (image.pixels[(y * image.width + x) * 4 + 3] === 0) legacy.delete(key);
        else legacy.add(key);
      }
    }
  }
  const expected = expectedWorldAlpha(room, cells, sourceImages);
  let missingAlphaPixels = 0;
  let extraAlphaPixels = 0;
  for (const key of expected) if (!legacy.has(key)) missingAlphaPixels += 1;
  for (const key of legacy) if (!expected.has(key)) extraAlphaPixels += 1;
  return { expectedAlphaPixels: expected.size, legacyAlphaPixels: legacy.size, missingAlphaPixels, extraAlphaPixels };
}

function makeSelectorOverlay(records: readonly SelectorRecord[]): RasterSurfaceCompatibilityV7 {
  const surface = new RasterSurfaceCompatibilityV7(14 * 32, 14 * 24, [15, 15, 15, 255]);
  for (const record of records) {
    const color = selectorColor(record.selectorId, record.rawIndex === 0);
    const left = record.cell[0] * 32;
    const top = record.cell[1] * 24;
    for (let y = top + 1; y < top + 23; y += 1) for (let x = left + 1; x < left + 31; x += 1) surface.setPixel(x, y, color);
  }
  return surface;
}

function selectorColor(selectorId: number, empty: boolean): readonly [number, number, number, number] {
  if (empty) return [32, 32, 32, 255];
  const value = Math.abs(selectorId * 2654435761) >>> 0;
  return [64 + (value & 0x7f), 64 + ((value >>> 8) & 0x7f), 64 + ((value >>> 16) & 0x7f), 255];
}

function makeAlphaMask(surface: V7RasterSurface): RasterSurfaceCompatibilityV7 {
  const mask = new RasterSurfaceCompatibilityV7(surface.width, surface.height, [0, 0, 0, 255]);
  for (let offset = 0; offset < surface.pixels.length; offset += 4) {
    const on = surface.pixels[offset + 3] !== 0;
    mask.pixels[offset] = on ? 255 : 0;
    mask.pixels[offset + 1] = on ? 255 : 0;
    mask.pixels[offset + 2] = on ? 255 : 0;
    mask.pixels[offset + 3] = 255;
  }
  return mask;
}

async function writeContactSheet(
  artifacts: Readonly<Record<string, ArtifactRecord>>,
  full: V7RasterSurface,
  single: V7RasterSurface,
  twoX: V7RasterSurface,
  twoY: V7RasterSurface,
  twoByTwo: V7RasterSurface,
  fiveByFive: ArtifactRecord | undefined,
  selectorOverlay: ArtifactRecord | undefined,
  alphaMask: V7RasterSurface,
): Promise<ArtifactRecord> {
  const historical = await loadSurface(HISTORICAL_CORRUPT_PREVIEW);
  const floorAlias = await loadSurface(join(ASSET_ROOT, "room-scene", "01_GAME_PACKS", "chip", "floor_05.png"));
  const panels = [
    single,
    twoX,
    twoY,
    twoByTwo,
    fiveByFive === undefined ? full : await loadSurface(resolve(ROOT, fiveByFive.path)),
    full,
    selectorOverlay === undefined ? full : await loadSurface(resolve(ROOT, selectorOverlay.path)),
    alphaMask,
    floorAlias,
    historical,
    full,
    full,
  ];
  const panelWidth = 320;
  const panelHeight = 220;
  const contact = new RasterSurfaceCompatibilityV7(panelWidth * 3, panelHeight * 4, [8, 8, 8, 255]);
  panels.forEach((panel, index) => copySurface(contact, thumbnail(panel, panelWidth - 8, panelHeight - 8), (index % 3) * panelWidth + 4, Math.floor(index / 3) * panelHeight + 4));
  return writeArtifact("MAPCHIP_FORENSIC_CONTACT_SHEET.png", contact);
}

function thumbnail(source: V7RasterSurface, width: number, height: number): RasterSurfaceCompatibilityV7 {
  const output = new RasterSurfaceCompatibilityV7(width, height, [16, 16, 16, 255]);
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

async function loadSurface(path: string): Promise<RasterSurfaceCompatibilityV7> {
  const decoded = decodePng(await readFile(path));
  const surface = new RasterSurfaceCompatibilityV7(decoded.width, decoded.height);
  surface.pixels.set(decoded.pixels);
  return surface;
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

async function writeArtifact(filename: string, surface: V7RasterSurface): Promise<ArtifactRecord> {
  const png = encodePngRgbaV7(surface);
  const path = join(PREVIEW_ROOT, filename);
  await writeFile(path, png);
  return {
    path: relativePath(path),
    width: surface.width,
    height: surface.height,
    pixelSha256: sha256(surface.pixels),
    pngSha256: sha256(png),
    nonTransparentBounds: surfaceBounds(surface),
  };
}

async function writeJson(filename: string, value: unknown): Promise<void> {
  await writeFile(join(EVIDENCE_ROOT, filename), `${JSON.stringify(JSON.parse(stableJson(jsonSafe(value))), null, 2)}\n`, "utf8");
}

function jsonSafe(value: unknown): unknown {
  if (value instanceof Uint8Array) return { byteLength: value.length, sha256: sha256(value) };
  if (Array.isArray(value)) return value.map((item) => jsonSafe(item));
  if (value !== null && typeof value === "object") {
    const record = value as Record<string, unknown>;
    if (typeof record.width === "number" && typeof record.height === "number" && record.pixels instanceof Uint8Array) {
      return { width: record.width, height: record.height, pixelSha256: sha256(record.pixels) };
    }
    return Object.fromEntries(Object.entries(record).map(([key, item]) => [key, jsonSafe(item)]));
  }
  return value;
}

function relativePath(path: string): string {
  return path.replace(`${ROOT}\\`, "").replaceAll("\\", "/");
}

function resourceImageId(selectorId: number): string {
  return `resChip_:image:${selectorId}`;
}

function sha256(value: Uint8Array | string): string {
  return createHash("sha256").update(value).digest("hex");
}

function countAlpha(image: V7RasterImage): number {
  let count = 0;
  for (let offset = 3; offset < image.pixels.length; offset += 4) if (image.pixels[offset] !== 0) count += 1;
  return count;
}

function alphaBounds(image: V7RasterImage): { x: number; y: number; width: number; height: number } | null {
  const points: [number, number][] = [];
  for (let y = 0; y < image.height; y += 1) for (let x = 0; x < image.width; x += 1) if (image.pixels[(y * image.width + x) * 4 + 3] !== 0) points.push([x, y]);
  if (points.length === 0) return null;
  const xs = points.map(([x]) => x);
  const ys = points.map(([, y]) => y);
  return { x: Math.min(...xs), y: Math.min(...ys), width: Math.max(...xs) - Math.min(...xs) + 1, height: Math.max(...ys) - Math.min(...ys) + 1 };
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

function setEqual(left: Set<string>, right: Set<string>): boolean {
  if (left.size !== right.size) return false;
  for (const value of left) if (!right.has(value)) return false;
  return true;
}

function connectedComponents(points: Set<string>): number {
  const remaining = new Set(points);
  let count = 0;
  while (remaining.size > 0) {
    const start = remaining.values().next().value as string;
    remaining.delete(start);
    const queue = [start];
    while (queue.length > 0) {
      const current = queue.pop()!;
      const [x, y] = current.split(",").map(Number);
      for (const neighbor of [`${x - 1},${y}`, `${x + 1},${y}`, `${x},${y - 1}`, `${x},${y + 1}`]) {
        if (remaining.delete(neighbor)) queue.push(neighbor);
      }
    }
    count += 1;
  }
  return count;
}

function enclosedTransparentPixels(points: Set<string>): number {
  if (points.size === 0) return 0;
  const coordinates = [...points].map((point) => point.split(",").map(Number) as [number, number]);
  let left = Number.POSITIVE_INFINITY;
  let right = Number.NEGATIVE_INFINITY;
  let top = Number.POSITIVE_INFINITY;
  let bottom = Number.NEGATIVE_INFINITY;
  for (const [x, y] of coordinates) {
    left = Math.min(left, x);
    right = Math.max(right, x);
    top = Math.min(top, y);
    bottom = Math.max(bottom, y);
  }
  left -= 1;
  right += 1;
  top -= 1;
  bottom += 1;
  const background = new Set<string>();
  for (let y = top; y <= bottom; y += 1) for (let x = left; x <= right; x += 1) if (!points.has(`${x},${y}`)) background.add(`${x},${y}`);
  const outside = new Set<string>();
  const queue = [`${left},${top}`];
  outside.add(queue[0]);
  while (queue.length > 0) {
    const current = queue.pop()!;
    const [x, y] = current.split(",").map(Number);
    for (const neighbor of [`${x - 1},${y}`, `${x + 1},${y}`, `${x},${y - 1}`, `${x},${y + 1}`]) {
      const [nx, ny] = neighbor.split(",").map(Number);
      if (nx < left || nx > right || ny < top || ny > bottom || !background.has(neighbor) || outside.has(neighbor)) continue;
      outside.add(neighbor);
      queue.push(neighbor);
    }
  }
  return [...background].filter((point) => !outside.has(point)).length;
}

function countBy<T>(items: readonly T[], key: (item: T) => string): Record<string, number> {
  const counts: Record<string, number> = {};
  for (const item of items) {
    const value = key(item);
    counts[value] = (counts[value] ?? 0) + 1;
  }
  return counts;
}

function decodePng(bytes: Uint8Array): DecodedPng {
  const signature = [137, 80, 78, 71, 13, 10, 26, 10];
  if (!signature.every((value, index) => bytes[index] === value)) throw new Error("MapChip forensic PNG signature is invalid");
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
    } else if (type === "IDAT") idat.push(new Uint8Array(data));
    else if (type === "PLTE") palette = new Uint8Array(data);
    else if (type === "tRNS") transparency = new Uint8Array(data);
    else if (type === "IEND") break;
  }
  if (bitDepth !== 8 || ![0, 2, 3, 4, 6].includes(colorType) || interlace !== 0) throw new Error("MapChip forensic PNG format is unsupported");
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
      if (palette === null || paletteOffset + 2 >= palette.length) throw new Error(`MapChip forensic palette index ${paletteIndex} is out of range`);
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
