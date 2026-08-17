import { GraphicsCompatibility } from "../v2/graphics";
import { drawFurnitureBinding } from "../v4/furniture";
import {
  drawMapChipBoundary,
  drawMapExtension,
  drawMapFloor,
  isMapFloorCellVisible,
} from "../v4/map-chip";
import {
  classifyObjChipWallLayer,
  drawObjChipPrimary,
  drawObjChipWall,
  objChipOrigin,
  type V4ObjChipInput,
} from "../v4/obj-chip";
import { sortV4Drawables, V4NativePassOrder } from "../v4/ordering";
import type { V4Cell, V4CommandTrace } from "../v4/contracts";
import { createV5Camera, createV5FurnitureBinding, createV5MapDrawCamera, createV5ResourceManager, createV5StructuralBinding } from "./fixture-loader";
import { createV5CommandManifest } from "./manifest";
import {
  explicitBindingAt,
  loadRoomDataV5,
  mapImageSelectorForRawIndex,
} from "./room-data";
import type {
  V5CommandEvent,
  V5PassResult,
  V5PassScheduleRecord,
  V5RoomCommandManifest,
  V5RoomData,
  V5RoomOptions,
  V5RoomRenderResult,
  V5RoomTopology,
  V5VisualScope,
} from "./contracts";
import { resolveRoomTopologyV5 } from "./topology";
import { drawMainDisplayMapCell } from "./main-display-map";
import type { V5MapChip, V5MapCellRole } from "./contracts";

const FOREGROUND_WALL_CELLS: readonly V4Cell[] = [[8, 7], [8, 8]];

const PASS_SCHEDULE: readonly V5PassScheduleRecord[] = [
  {
    index: 0,
    passId: "map-extension-floor",
    ownerClass: "game.MapChip",
    method: "DrawExtentionFloor",
    gridTraversal: "map cells: y ascending, x descending",
    predicate: "main_display full MapChip underlay precommit, then closed V4 extension trigger sets only",
    resourceFamily: "resChip_ original SEB 63 / source image 2",
    depthRole: "map extension under room objects",
    includedRawTypes: ["closed MapChip extension triggers"],
    excludedRawTypes: ["unproven alternate extension branches"],
    cameraState: "logical camera offset plus normalized MapChip draw-space bridge",
    localOrdering: "native row order with V4 MapChip local piece order",
    proof: "NATIVE-CODE-PROVEN",
    sourceRefs: ["Room.Draw:2220", "MapChip.DrawExtentionFloor@0x12A20F4", "floor00_scene_contract.json:render_composition", "v4/map-chip.ts"],
  },
  {
    index: 1,
    passId: "map-chip",
    ownerClass: "game.MapChip",
    method: "Draw",
    gridTraversal: "map cells: y ascending, x descending",
    predicate: "Room.floor_ >= 1 boundary predicates; floor_ < 1 is a no-draw boundary path",
    resourceFamily: "resChip_ original SEB 2 and optional 7",
    depthRole: "map boundary",
    includedRawTypes: ["room boundary cells when floor_ >= 1"],
    excludedRawTypes: ["floor_ < 1 boundary draw"],
    cameraState: "logical camera offset plus normalized MapChip draw-space bridge",
    localOrdering: "MapChip boundary then optional overlay",
    proof: "NATIVE-CODE-PROVEN",
    sourceRefs: ["Room.Draw:2291", "MapChip.Draw@0x12A1B24", "v4/map-chip.ts"],
  },
  {
    index: 2,
    passId: "object-chip-primary",
    ownerClass: "game.ObjChip",
    method: "Draw",
    gridTraversal: "ObjChip cells: y ascending, x descending",
    predicate: "explicit native FurnitureData binding or source-proven structural facility only",
    resourceFamily: "resChip_ original FurnitureData SEB/image selectors",
    depthRole: "primary object/furniture",
    includedRawTypes: [1, 2, 4, "explicit binding raw type"],
    excludedRawTypes: ["unbound raw ObjChip types", 5, 6],
    cameraState: "logical camera offset plus normalized ObjChip draw-space bridge",
    localOrdering: "stable row/column order; FurnitureData subSeb follows V4",
    proof: "CALL-FLOW-PROVEN",
    sourceRefs: ["Room.Draw:2682", "Room.PlaceDesk/PlaceObj", "v4/obj-chip.ts", "v4/furniture.ts"],
  },
  {
    index: 3,
    passId: "object-chip-wall",
    ownerClass: "game.ObjChip",
    method: "DrawWall",
    gridTraversal: "rear ObjChip cells: y ascending, x descending",
    predicate: "closed vertical/horizontal wall predicates plus raw type 5 door",
    resourceFamily: "resChip_ original wall SEB 5 / door SEB 6",
    depthRole: "rear wall and door",
    includedRawTypes: ["non-door wall predicate cells", 5],
    excludedRawTypes: ["approved foreground wall cells [8,7], [8,8]"],
    cameraState: "logical camera offset plus normalized ObjChip draw-space bridge",
    localOrdering: "SEB layer order remains V4 layer order",
    proof: "NATIVE-CODE-PROVEN",
    sourceRefs: ["Room.Draw:2812", "ObjChip.DrawWall@0x12C0698", "native_scene_assembly_contract.json"],
  },
  {
    index: 4,
    passId: "avatar-primary",
    ownerClass: "game.Avatar",
    method: "Draw",
    gridTraversal: "not executed in V5",
    predicate: "Staff/Avatar scope is deferred to V6",
    resourceFamily: "resAvatarBody_ / resAvatarHead_",
    depthRole: "actor primary",
    includedRawTypes: [],
    excludedRawTypes: ["all actor records"],
    cameraState: "actor draw-space bridge reserved for V6 Staff integration",
    localOrdering: "native slot retained, empty V5 implementation",
    proof: "SOURCE-LIMITED",
    sourceRefs: ["Room.Draw:2874", "native_scene_assembly_contract.json:avatar-primary"],
  },
  {
    index: 5,
    passId: "avatar-secondary",
    ownerClass: "game.Avatar",
    method: "DrawSecondary",
    gridTraversal: "not executed in V5",
    predicate: "Staff/Avatar scope is deferred to V6",
    resourceFamily: "resAvatarBody_ / resAvatarHead_",
    depthRole: "actor secondary",
    includedRawTypes: [],
    excludedRawTypes: ["all actor records"],
    cameraState: "actor draw-space bridge reserved for V6 Staff integration",
    localOrdering: "native slot retained, empty V5 implementation",
    proof: "SOURCE-LIMITED",
    sourceRefs: ["Room.Draw:3046", "native_scene_assembly_contract.json:avatar-secondary"],
  },
  {
    index: 6,
    passId: "object-chip-late-preview",
    ownerClass: "game.ObjChip",
    method: "DrawLatePreview",
    gridTraversal: "not executed for the selected static world fixture",
    predicate: "generic preview branch remains source-limited",
    resourceFamily: "resChip_ generic preview selectors",
    depthRole: "late preview",
    includedRawTypes: [],
    excludedRawTypes: ["generic preview branches"],
    cameraState: "logical camera offset plus normalized ObjChip draw-space bridge",
    localOrdering: "native slot retained, empty V5 implementation",
    proof: "SOURCE-LIMITED",
    sourceRefs: ["Room.Draw:3178", "V4 unknown OBJDRAW-GENERAL-BRANCH"],
  },
  {
    index: 7,
    passId: "object-chip-late",
    ownerClass: "game.ObjChip",
    method: "DrawLate",
    gridTraversal: "foreground ObjChip cells: y ascending, x descending",
    predicate: "approved foreground wall cells only",
    resourceFamily: "resChip_ original wall SEB 5",
    depthRole: "foreground wall occlusion",
    includedRawTypes: ["foreground wall predicate cells"],
    excludedRawTypes: ["unproven late object branches"],
    cameraState: "logical camera offset plus normalized ObjChip draw-space bridge",
    localOrdering: "V4 foreground classification and SEB layers",
    proof: "CALL-FLOW-PROVEN",
    sourceRefs: ["Room.Draw:3260", "floor00_scene_contract.json:render_composition", "v4/obj-chip.ts"],
  },
  {
    index: 8,
    passId: "map-floor",
    ownerClass: "game.MapChip",
    method: "DrawFloor",
    gridTraversal: "map cells: y ascending, x descending",
    predicate: "native floor culling window for non-main-display contexts; main_display underlay is committed in pass 0",
    resourceFamily: "resChip_ original map image selectors",
    depthRole: "floor/map underlay native slot retained; main_display underlay committed before objects",
    includedRawTypes: ["mapped raw MapChip indices in culling window"],
    excludedRawTypes: [0, "outside native floor culling window"],
    cameraState: "logical camera offset plus normalized MapChip draw-space bridge",
    localOrdering: "full source image dimensions and native height anchor",
    proof: "NATIVE-CODE-PROVEN",
    sourceRefs: ["Room.Draw:3426", "MapChip.DrawFloor@0x12A1F38", "floor00_scene_contract.json:render_composition", "v4/map-chip.ts"],
  },
] as const;

export class RoomV5 {
  public readonly roomData: V5RoomData;
  public readonly floor: number;
  public readonly topology: V5RoomTopology;
  public readonly camera = createV5Camera();
  public readonly mapCamera = createV5MapDrawCamera();
  public readonly resources = createV5ResourceManager();
  public readonly visualScope: V5VisualScope;
  public readonly mapChips: readonly V5MapChip[];
  public readonly objChips: readonly V4ObjChipInput[];
  public readonly initializationTrace = [
    "Room.InitMapChips",
    "Room.InitObjChips",
    "Room.SetupBigChipsParent",
    "Room.PlaceDoor",
    "Room.PlaceDesk/PlaceObj explicit bindings",
  ] as const;

  public constructor(roomData: V5RoomData, options: V5RoomOptions = {}) {
    this.roomData = roomData;
    this.floor = options.roomFloor ?? 0;
    this.topology = resolveRoomTopologyV5(this.floor, options);
    this.visualScope = options.visualScope ?? (roomData.roomKey === "room:0" ? "full_static" : "topology_only");
    const cameraOffset = options.cameraOffset ?? { x: 0, y: 0 };
    this.camera.setPosition(cameraOffset.x, cameraOffset.y);
    this.mapCamera.setPosition(cameraOffset.x, cameraOffset.y);
    this.mapChips = this.buildMapChips();
    this.objChips = this.buildObjChips();
  }

  public get doorCells(): readonly V4Cell[] {
    return this.roomData.assembly.door.cells;
  }

  public get wallCellsByFrame(): Readonly<Record<string, readonly V4Cell[]>> {
    return this.roomData.assembly.wall.cells_by_frame;
  }

  public get initialFurnitureBindings() {
    return this.roomData.nativeBindings;
  }

  public draw(): V5RoomRenderResult {
    const graphics = new GraphicsCompatibility();
    const traces: V4CommandTrace[] = [];
    const events: V5CommandEvent[] = [];
    const passes: V5PassResult[] = [];

    const orderedMapChips = this.orderedMapChips();
    this.runPass(passes, events, traces, graphics, PASS_SCHEDULE[0], orderedMapChips, (input) => {
      drawMapExtension(input, this.resources, this.mapCamera, graphics, traces);
    }, () => {
      if (!this.mainDisplayUnderlayEnabled()) {
        return;
      }
      for (const input of orderedMapChips) {
        drawMainDisplayMapCell(input, this.resources, this.mapCamera, graphics, traces);
      }
    });
    this.runPass(passes, events, traces, graphics, PASS_SCHEDULE[1], orderedMapChips, (input) => {
      drawMapChipBoundary(input, this.resources, this.mapCamera, graphics, traces);
    });
    const orderedObjects = this.orderedObjChips();
    this.runPass(passes, events, traces, graphics, PASS_SCHEDULE[2], orderedObjects, (input) => {
      if (this.visualScope !== "full_static") {
        return;
      }
      const binding = explicitBindingAt(this.roomData, input.cell);
      if (binding !== undefined) {
        drawObjChipPrimary({ ...input, furnitureBinding: createV5FurnitureBinding(binding.object_id) }, this.resources, this.camera, graphics, traces);
      } else {
        drawObjChipPrimary(input, this.resources, this.camera, graphics, traces);
      }
      const structural = this.roomData.structuralFacilities.find((facility) => sameCell(facility.anchor, input.cell));
      if (structural !== undefined) {
        drawFurnitureBinding(
          createV5StructuralBinding(structural),
          objChipOrigin(input.cell, this.camera),
          this.resources,
          graphics,
          traces,
        );
      }
    });
    const rearObjects = orderedObjects.filter((input) => classifyObjChipWallLayer(input.cell, FOREGROUND_WALL_CELLS) === "rear");
    this.runPass(passes, events, traces, graphics, PASS_SCHEDULE[3], rearObjects, (input) => {
      if (this.visualScope === "full_static") {
        drawObjChipWall(input, this.resources, this.camera, graphics, traces);
      }
    });
    this.runPass(passes, events, traces, graphics, PASS_SCHEDULE[4], [], () => undefined);
    this.runPass(passes, events, traces, graphics, PASS_SCHEDULE[5], [], () => undefined);
    this.runPass(passes, events, traces, graphics, PASS_SCHEDULE[6], [], () => undefined);
    const foregroundObjects = orderedObjects.filter((input) => classifyObjChipWallLayer(input.cell, FOREGROUND_WALL_CELLS) === "foreground");
    this.runPass(passes, events, traces, graphics, PASS_SCHEDULE[7], foregroundObjects, (input) => {
      if (this.visualScope === "full_static") {
        drawObjChipWall(input, this.resources, this.camera, graphics, traces);
      }
    });
    this.runPass(passes, events, traces, graphics, PASS_SCHEDULE[8], orderedMapChips, (input) => {
      if (!this.mainDisplayUnderlayEnabled()) {
        drawMapFloor(input, this.resources, this.mapCamera, graphics, traces);
      }
    });
    return { commands: graphics.commands, traces, passes, events, camera: this.camera, resources: this.resources, graphics };
  }

  public commandManifest(): V5RoomCommandManifest {
    return createV5CommandManifest(this, this.draw());
  }

  public mainDisplayUnderlayEnabled(): boolean {
    return this.visualScope === "full_static"
      && this.topology.context === "main_display"
      && this.topology.width === 14
      && this.topology.height === 14
      && this.floor === 0;
  }

  private buildMapChips(): readonly V5MapChip[] {
    const cells: V5MapChip[] = [];
    for (let y = 0; y < this.topology.height; y += 1) {
      const row = this.topology.rows[y];
      if (row === undefined) {
        throw new Error(`V5 MapChip topology is missing row ${y}`);
      }
      for (let x = 0; x < this.topology.width; x += 1) {
        const rawIndex = row[x];
        if (rawIndex === undefined) {
          throw new Error(`V5 MapChip topology is missing cell ${x},${y}`);
        }
        const role: V5MapCellRole = rawIndex === 0
          ? "empty"
          : rawIndex === 1
            ? isMapFloorCellVisible([x, y], this.topology.width, this.topology.height)
              ? "room_floor_central"
              : "room_floor_fill"
            : "outer_map";
        cells.push({
          cell: [x, y],
          imageId: mapImageSelectorForRawIndex(rawIndex),
          rawIndex,
          role,
          roomFloor: this.floor,
          roomWidth: this.topology.width,
          roomHeight: this.topology.height,
        });
      }
    }
    return cells;
  }

  private buildObjChips(): readonly V4ObjChipInput[] {
    return this.roomData.rawObjChips.map((raw) => ({
      cell: raw.cell,
      rawType: raw.rawType,
      rawDirection: raw.rawDirection,
      roomWidth: this.roomData.objMapWidth,
      roomHeight: this.roomData.objMapHeight,
      wallImageId: this.roomData.wallImgId,
      doorImageId: this.roomData.doorImgId,
    }));
  }

  private orderedMapChips(): readonly V5MapChip[] {
    return sortV4Drawables(this.mapChips);
  }

  private orderedObjChips(): readonly V4ObjChipInput[] {
    return sortV4Drawables(this.objChips);
  }

  private runPass<T extends { readonly cell: V4Cell }>(
    passes: V5PassResult[],
    events: V5CommandEvent[],
    traces: V4CommandTrace[],
    graphics: GraphicsCompatibility,
    schedule: V5PassScheduleRecord,
    inputs: readonly T[],
    draw: (input: T) => void,
    before?: () => void,
  ): void {
    const commandStart = graphics.commands.length;
    const traceStart = traces.length;
    before?.();
    for (const input of inputs) {
      const inputCommandStart = graphics.commands.length;
      const inputTraceStart = traces.length;
      draw(input);
      events.push({
        passId: schedule.passId,
        cell: input.cell,
        rawType: "rawType" in input ? (input as T & { readonly rawType: number }).rawType : undefined,
        role: schedule.depthRole,
        commandStart: inputCommandStart,
        commandEnd: graphics.commands.length,
        traceStart: inputTraceStart,
        traceEnd: traces.length,
        proof: schedule.proof,
      });
    }
    passes.push({
      ...schedule,
      inputCount: inputs.length,
      commandStart,
      commandEnd: graphics.commands.length,
      traceStart,
      traceEnd: traces.length,
    });
  }
}

export function createRoomV5(roomKey = "room:0", options: V5RoomOptions = {}): RoomV5 {
  return new RoomV5(loadRoomDataV5(roomKey), options);
}

export function v5PassSchedule(): readonly V5PassScheduleRecord[] {
  return PASS_SCHEDULE;
}

export function v5ForegroundWallCells(): readonly V4Cell[] {
  return FOREGROUND_WALL_CELLS;
}

function sameCell(left: V4Cell, right: V4Cell): boolean {
  return left[0] === right[0] && left[1] === right[1];
}
