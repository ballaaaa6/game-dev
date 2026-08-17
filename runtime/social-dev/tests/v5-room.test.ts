import { createHash } from "node:crypto";
import { describe, expect, it } from "vitest";
import {
  createRoom00StaticPreview,
  createRoomV5,
  loadAllRoomDataV5,
  loadRoomDataV5,
  mapImageSelectorForRawIndex,
  resolveRoomTopologyV5,
  roomDataV5Keys,
  stableJson,
  v5ForegroundWallCells,
  v5PassSchedule,
} from "../src/v5";
import { V4NativePassOrder, sortV4Drawables } from "../src/v4/ordering";

describe("V5 Room / RoomData static orchestration", () => {
  it("loads the complete native 18-room RoomData key set", () => {
    expect(roomDataV5Keys()).toEqual(Array.from({ length: 18 }, (_, index) => `room:${index}`));
    expect(loadAllRoomDataV5()).toHaveLength(18);
  });

  it("preserves English RoomData names and native numeric selectors", () => {
    const rooms = loadAllRoomDataV5();
    expect(rooms.map((room) => room.name)).toEqual([
      "Floor A", "Floor B", "Floor C", "Floor D", "Floor E", "Floor F",
      "Floor G", "Floor H", "Floor I", "Floor J", "Floor K", "Floor L",
      "Floor M", "Floor N", "Floor O", "Floor P", "Floor Q", "Floor R",
    ]);
    expect(rooms.map((room) => room.floorImgId)).toEqual([5, 0, 1, 2, 3, 7, 6, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 9]);
  });

  it("validates native ObjChip grids as rectangular 10x10 data", () => {
    for (const room of loadAllRoomDataV5()) {
      expect(room.objMap).toHaveLength(10);
      expect(room.objDir).toHaveLength(10);
      expect(room.objMap.every((row) => row.length === 10)).toBe(true);
      expect(room.objDir.every((row) => row.length === 10)).toBe(true);
      expect(room.rawObjChips).toHaveLength(100);
    }
  });

  it("keeps raw ObjChip identity separate from FurnitureData binding", () => {
    const room0 = loadRoomDataV5("room:0");
    const door = room0.rawObjChips.find((chip) => chip.cell[0] === 8 && chip.cell[1] === 4);
    expect(door).toMatchObject({ rawType: 5, rawDirection: 0 });
    expect(room0.nativeBindings.map((binding) => binding.object_id)).toEqual([
      "furniture:3", "furniture:3", "furniture:3", "furniture:12", "furniture:26", "furniture:56",
    ]);
    expect(loadRoomDataV5("room:1").nativeBindings).toHaveLength(0);
  });

  it("retains the native room-owned constructor trace", () => {
    const room = createRoomV5("room:0");
    expect(room.initializationTrace).toEqual([
      "Room.InitMapChips",
      "Room.InitObjChips",
      "Room.SetupBigChipsParent",
      "Room.PlaceDoor",
      "Room.PlaceDesk/PlaceObj explicit bindings",
    ]);
  });

  it("selects the native floor_0 14x14 topology for main display", () => {
    const topology = resolveRoomTopologyV5(0, { context: "main_display" });
    expect(topology).toMatchObject({ variantId: "floor_0", width: 14, height: 14, proof: "NATIVE-CODE-PROVEN" });
    expect(topology.rows).toHaveLength(14);
    expect(topology.rows.every((row) => row.length === 14)).toBe(true);
    expect(topology.rows.flat()).toContain(11);
  });

  it("selects the native floor_nonzero 4x4 topology for addition preview", () => {
    const topology = resolveRoomTopologyV5(1, { context: "addition_floor_preview" });
    expect(topology).toMatchObject({ variantId: "floor_nonzero", width: 4, height: 4, proof: "NATIVE-CODE-PROVEN" });
    expect(topology.rows.flat()).toEqual(Array(16).fill(1));
  });

  it("supports the separate persistent-room 4x4 floor_0 context", () => {
    const topology = resolveRoomTopologyV5(0, { context: "persistent_room" });
    expect(topology).toMatchObject({ variantId: "floor_0", width: 4, height: 4, environmentScope: "native_room_topology_only" });
  });

  it("rejects native Room floor/context dimension mismatches", () => {
    expect(() => resolveRoomTopologyV5(1, { context: "main_display" })).toThrow(/MAPCHIP_ARRAY\[1\] is 4x4/);
    expect(() => resolveRoomTopologyV5(0, { context: "addition_floor_preview" })).toThrow(/addition_floor_preview requires floor!=0/);
    expect(() => resolveRoomTopologyV5(0, { dimensions: { width: 5, height: 5 } })).toThrow(/approved constructor dimensions/);
    expect(() => resolveRoomTopologyV5(1, { dimensions: { width: 14, height: 14 } })).toThrow(/MAPCHIP_ARRAY\[1\] is 4x4/);
  });

  it("maps raw MapChip indices through the approved numeric selector table", () => {
    expect([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11].map(mapImageSelectorForRawIndex)).toEqual([
      -1, 85, 10, 11, 12, 13, 14, 15, 105, 154, 155, 156,
    ]);
  });

  it("keeps Room.floor_ independent from RoomData.floorImgId", () => {
    const room = createRoomV5("room:0", { roomFloor: 1, context: "addition_floor_preview" });
    expect(room.floor).toBe(1);
    expect(room.roomData.floorImgId).toBe(5);
    expect(room.topology.variantId).toBe("floor_nonzero");
  });

  it("exposes the recovered native Room.Draw pass order", () => {
    expect(v5PassSchedule().map((pass) => pass.passId)).toEqual([...V4NativePassOrder]);
    expect(v5PassSchedule().map((pass) => pass.index)).toEqual([0, 1, 2, 3, 4, 5, 6, 7, 8]);
    expect(v5PassSchedule().every((pass) => pass.sourceRefs.length > 0)).toBe(true);
  });

  it("preserves row-ascending and x-descending map traversal", () => {
    const room = createRoomV5("room:0");
    const ordered = sortV4Drawables(room.mapChips);
    expect(ordered.slice(0, 4).map((input) => input.cell)).toEqual([[13, 0], [12, 0], [11, 0], [10, 0]]);
    expect(ordered.slice(-4).map((input) => input.cell)).toEqual([[3, 13], [2, 13], [1, 13], [0, 13]]);
  });

  it("retains every source-backed floor0 MapChip cell and classifies the main-display underlay", () => {
    const room = createRoomV5("room:0", { context: "main_display", visualScope: "full_static" });
    expect(room.mapChips).toHaveLength(196);
    expect(room.mapChips.filter((input) => input.rawIndex !== 0)).toHaveLength(81);
    expect(room.mapChips.filter((input) => input.role === "room_floor_central")).toHaveLength(16);
    expect(room.mapChips.filter((input) => input.role === "room_floor_fill")).toHaveLength(12);
    expect(room.mapChips.filter((input) => input.role === "outer_map")).toHaveLength(53);
    expect(room.mapChips.find((input) => input.cell[0] === 4 && input.cell[1] === 10)).toMatchObject({ rawIndex: 8, imageId: 105, role: "outer_map" });
    expect(room.mapChips.find((input) => input.cell[0] === 5 && input.cell[1] === 5)).toMatchObject({ rawIndex: 1, imageId: 85, role: "room_floor_central" });
  });

  it("emits a continuous 81-cell main-display underlay before structural objects", () => {
    const room = createRoomV5("room:0", { context: "main_display", visualScope: "full_static" });
    const render = room.draw();
    const expected = new Set(room.mapChips.filter((input) => input.rawIndex !== 0).map((input) => input.cell.join(",")));
    const underlay = render.traces.filter((trace) => trace.pass === "main-display-map-underlay");
    expect(new Set(underlay.map((trace) => trace.cell?.join(",")))).toEqual(expected);
    expect(underlay).toHaveLength(81);
    expect(render.passes[0]?.commandEnd).toBeGreaterThan(underlay.length);
    expect(render.passes[2]?.commandStart).toBeGreaterThanOrEqual(render.passes[0]?.commandEnd ?? 0);
    expect(render.passes[8]?.commandStart).toBe(render.passes[7]?.commandEnd);
    expect(render.passes[8]?.commandEnd).toBe(render.passes[8]?.commandStart);
  });

  it("preserves row-ascending and x-descending ObjChip traversal", () => {
    const render = createRoomV5("room:0").draw();
    const objectEvents = render.events.filter((event) => event.passId === "object-chip-primary");
    expect(objectEvents).toHaveLength(100);
    expect(objectEvents.slice(0, 4).map((event) => event.cell)).toEqual([[9, 0], [8, 0], [7, 0], [6, 0]]);
    expect(objectEvents.slice(-4).map((event) => event.cell)).toEqual([[3, 9], [2, 9], [1, 9], [0, 9]]);
  });

  it("executes the complete nine-slot static pass schedule", () => {
    const render = createRoomV5("room:0").draw();
    expect(render.passes.map((pass) => pass.passId)).toEqual([...V4NativePassOrder]);
    expect(render.passes.map((pass) => pass.inputCount)).toEqual([196, 196, 100, 98, 0, 0, 0, 2, 196]);
    expect(render.passes.every((pass) => pass.commandStart <= pass.commandEnd && pass.traceStart <= pass.traceEnd)).toBe(true);
    expect(render.commands.length).toBeGreaterThan(0);
    expect(render.traces.length).toBeGreaterThan(0);
  });

  it("preserves the room:0 native wall and door cells", () => {
    const room = createRoomV5("room:0");
    expect(room.doorCells).toEqual([[8, 4]]);
    expect(room.wallCellsByFrame.vertical_frame_1).toEqual([
      [8, 1], [8, 2], [8, 3], [8, 5], [8, 6], [8, 7], [8, 8],
    ]);
    expect(room.wallCellsByFrame.horizontal_frame_0).toEqual([
      [1, 1], [2, 1], [3, 1], [4, 1], [5, 1], [6, 1], [7, 1], [8, 1],
    ]);
  });

  it("emits the source-proven door trace in the rear wall slot", () => {
    const render = createRoomV5("room:0").draw();
    expect(render.traces.some((trace) =>
      trace.pass === "object-chip-wall"
      && trace.selectorRole === "ObjChip.DrawWall:raw_type_5_door"
      && trace.cell?.[0] === 8
      && trace.cell?.[1] === 4,
    )).toBe(true);
  });

  it("limits the late wall slot to the two approved foreground cells", () => {
    const render = createRoomV5("room:0").draw();
    expect(v5ForegroundWallCells()).toEqual([[8, 7], [8, 8]]);
    const lateCells = new Set(render.traces
      .filter((trace) => trace.pass === "object-chip-late")
      .map((trace) => trace.cell?.join(",")));
    expect(lateCells).toEqual(new Set(["8,7", "8,8"]));
  });

  it("keeps the recovered wall path connected through the door cell", () => {
    const room = createRoomV5("room:0");
    const wallCells = [
      ...room.wallCellsByFrame.vertical_frame_1,
      ...room.wallCellsByFrame.horizontal_frame_0,
      ...room.doorCells,
    ];
    const unique = new Set(wallCells.map((cell) => cell.join(",")));
    const visited = new Set<string>();
    const queue = ["1,1"];
    while (queue.length > 0) {
      const current = queue.shift()!;
      if (visited.has(current) || !unique.has(current)) continue;
      visited.add(current);
      const [x, y] = current.split(",").map(Number);
      for (const next of [[x - 1, y], [x + 1, y], [x, y - 1], [x, y + 1]]) {
        queue.push(next.join(","));
      }
    }
    expect(visited).toEqual(unique);
    const render = room.draw();
    expect(render.traces.filter((trace) => trace.pass === "main-display-map-underlay")).toHaveLength(81);
    expect(render.traces.filter((trace) => trace.pass === "object-chip-wall" || trace.pass === "object-chip-late").some((trace) => trace.cell?.join(",") === "8,4")).toBe(true);
  });

  it("draws only explicit native FurnitureData bindings in the primary object slot", () => {
    const render = createRoomV5("room:0").draw();
    const primaryFurniture = render.traces.filter((trace) =>
      trace.pass === "object-chip-primary" && trace.selectorRole === "FurnitureData.seb_",
    );
    const directFurniture = render.traces.filter((trace) =>
      trace.pass === "object-chip-primary" && trace.selectorRole === "FurnitureData.img_:native_direct_image",
    );
    expect(primaryFurniture.length).toBeGreaterThanOrEqual(3);
    expect(directFurniture).toHaveLength(3);
    expect(directFurniture.map((trace) => trace.resource.id).sort((a, b) => a - b)).toEqual([106, 109, 127]);
  });

  it("draws both source-proven room:0 structural facilities without inventing catalogue data", () => {
    const room = createRoomV5("room:0");
    expect(room.roomData.structuralFacilities).toHaveLength(2);
    expect(room.roomData.structuralFacilities.map((facility) => facility.anchor)).toEqual([[4, 2], [7, 2]]);
    expect(room.roomData.structuralFacilities.every((facility) => facility.objectId === "furniture:0" && facility.rawType === 4)).toBe(true);
    const render = room.draw();
    expect(render.traces.filter((trace) => trace.resource.id === 11 && trace.pass === "object-chip-primary").length).toBe(2);
    expect(render.commands.some((command) => command.image.id === "resChip_:image:18")).toBe(true);
  });

  it("keeps non-room:0 rooms topology-only by default", () => {
    const room = createRoomV5("room:1");
    const render = room.draw();
    expect(room.visualScope).toBe("topology_only");
    expect(render.traces.some((trace) => trace.pass === "object-chip-primary")).toBe(false);
    expect(render.traces.some((trace) => trace.pass === "object-chip-wall")).toBe(false);
    expect(render.traces.some((trace) => trace.pass === "object-chip-late")).toBe(false);
  });

  it("supports the nonzero-floor topology-only addition preview fixture", () => {
    const room = createRoomV5("room:1", { roomFloor: 1, context: "addition_floor_preview" });
    expect(room.topology).toMatchObject({ variantId: "floor_nonzero", width: 4, height: 4 });
    expect(room.draw().passes[1]?.inputCount).toBe(16);
  });

  it("forwards one integer camera offset to map and object destinations", () => {
    const baseline = createRoomV5("room:0").draw();
    const shifted = createRoomV5("room:0", { cameraOffset: { x: 7, y: -3 } }).draw();
    const baselineFloor = baseline.commands.find((command) => command.image.id === "resChip_:image:85");
    const shiftedFloor = shifted.commands.find((command) => command.image.id === "resChip_:image:85");
    expect(baselineFloor?.destination.width).toBe(80);
    expect(baselineFloor?.destination.height).toBe(39);
    expect(shiftedFloor?.destination.x).toBe((baselineFloor?.destination.x ?? 0) + 7);
    expect(shiftedFloor?.destination.y).toBe((baselineFloor?.destination.y ?? 0) - 3);
    expect(shifted.camera.offset).toEqual({ x: 7, y: -3 });
  });

  it("keeps the resolved floor_0 raw selector separate from the runtime alias", () => {
    const manifest = createRoomV5("room:0").commandManifest();
    expect(manifest.floorSelectorPolicy).toEqual({
      rawRoomDataSelector: 5,
      nativeTableSelector: 23,
      runtimeSelector: 85,
      renderedFilename: "floor_05.png",
      status: "COMPATIBILITY-POLICY",
    });
  });

  it("creates a command-only preview with no server or screenshot proof", () => {
    const preview = createRoom00StaticPreview();
    expect(preview.kind).toBe("static-room-command-preview");
    expect(preview.serverStarted).toBe(false);
    expect(preview.screenshotUsedAsProof).toBe(false);
    expect(preview.manifest.roomKey).toBe("room:0");
    expect(() => JSON.parse(preview.stableSerialization)).not.toThrow();
  });

  it("serializes manifests deterministically with sorted object keys", () => {
    expect(stableJson({ b: 2, a: 1, optional: undefined })).toBe('{"a":1,"b":2}');
    const first = createRoom00StaticPreview().stableSerialization;
    const second = createRoom00StaticPreview().stableSerialization;
    expect(first).toBe(second);
    const hash = createHash("sha256").update(first).digest("hex");
    expect(hash).toBe("48a1827c94c15394d38e872b243c398d8c6e6f47b66099bf26b44f22ee79e047");
    expect(first.length).toBe(248764);
  });

  it("records command, trace, pass, and event streams in the manifest", () => {
    const manifest = createRoomV5("room:0").commandManifest();
    expect(manifest.commands).toHaveLength(139);
    expect(manifest.traces).toHaveLength(124);
    expect(manifest.passes).toHaveLength(9);
    expect(manifest.events.length).toBe(788);
    expect(manifest.commands).toEqual(manifest.commands);
  });
});
