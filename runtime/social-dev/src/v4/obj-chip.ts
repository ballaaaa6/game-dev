import { GraphicsCompatibility } from "../v2/graphics";
import { V4CameraBoundary } from "./camera";
import { V4ContractError } from "./errors";
import { drawFurnitureBinding } from "./furniture";
import type {
  V4Cell,
  V4CommandTrace,
  V4FurnitureBinding,
  V4Point,
  V4RenderResult,
} from "./contracts";
import { V4ResourceManager } from "./resources";

export interface V4ObjChipInput {
  readonly cell: V4Cell;
  readonly rawType: number;
  readonly rawDirection: number;
  readonly roomWidth: number;
  readonly roomHeight: number;
  readonly wallImageId: number;
  readonly doorImageId: number;
  readonly furnitureBinding?: V4FurnitureBinding;
}

export interface V4DirectionInfo {
  readonly raw: number;
  readonly label: "DIRECTION_RIGHT" | "DIRECTION_LEFT" | "DIRECTION_UP" | "DIRECTION_DOWN";
  readonly vector: readonly [number, number];
  readonly reverse: number;
}

const DIRECTIONS: readonly V4DirectionInfo[] = [
  { raw: 0, label: "DIRECTION_RIGHT", vector: [0, 1], reverse: 1 },
  { raw: 1, label: "DIRECTION_LEFT", vector: [0, -1], reverse: 0 },
  { raw: 2, label: "DIRECTION_UP", vector: [1, 0], reverse: 3 },
  { raw: 3, label: "DIRECTION_DOWN", vector: [-1, 0], reverse: 2 },
];

export function getDirectionInfo(rawDirection: number): V4DirectionInfo {
  if (!Number.isSafeInteger(rawDirection) || rawDirection < 0 || rawDirection >= DIRECTIONS.length) {
    throw new V4ContractError("V4_DIRECTION_OUT_OF_RANGE", `Unsupported ObjChip direction ${rawDirection}`);
  }
  return DIRECTIONS[rawDirection];
}

export function objChipOrigin(cell: V4Cell, camera: V4CameraBoundary): V4Point {
  validateCell(cell);
  return camera.transform({
    x: (cell[0] + cell[1]) * 20,
    y: (cell[1] - cell[0]) * 10 + 9,
  });
}

export function wallFramesFor(input: Pick<V4ObjChipInput, "cell" | "rawType" | "roomWidth" | "roomHeight">): readonly number[] {
  validateRoomSize(input.roomWidth, input.roomHeight);
  validateCell(input.cell);
  if (input.rawType === 5) {
    return [0];
  }
  const frames: number[] = [];
  if (input.cell[1] >= 1 && input.cell[1] < input.roomHeight - 1 && input.cell[0] === input.roomWidth - 2) {
    frames.push(1);
  }
  if (input.cell[0] >= 1 && input.cell[1] === 1 && input.cell[0] < input.roomWidth - 1) {
    frames.push(0);
  }
  return frames;
}

export function classifyObjChipWallLayer(
  cell: V4Cell,
  foregroundCells: readonly V4Cell[] = [[8, 7], [8, 8]],
): "rear" | "foreground" {
  validateCell(cell);
  return foregroundCells.some((candidate) => candidate[0] === cell[0] && candidate[1] === cell[1])
    ? "foreground"
    : "rear";
}

export function drawObjChipWall(
  input: V4ObjChipInput,
  resources: V4ResourceManager,
  camera: V4CameraBoundary,
  graphics: GraphicsCompatibility,
  traces: V4CommandTrace[],
): void {
  getDirectionInfo(input.rawDirection);
  const origin = objChipOrigin(input.cell, camera);
  if (input.rawType === 5) {
    if (input.doorImageId < 0 || !resources.hasImage(input.doorImageId)) {
      return;
    }
    requireSeb(resources, 6, "ObjChip.DrawWall door");
    const result = resources.drawSeb(graphics, origin.x, origin.y, 6, { frame: 0 });
    appendTrace(traces, {
      pass: "object-chip-wall",
      kind: "seb",
      resource: result.address,
      frame: result.frame,
      layer: result.layer,
      cell: input.cell,
      destination: origin,
      selectorRole: "ObjChip.DrawWall:raw_type_5_door",
      commandCount: result.commandCount,
      proof: "NATIVE-CODE-PROVEN",
    });
    return;
  }
  if (input.wallImageId < 0 || !resources.hasImage(input.wallImageId)) {
    return;
  }
  for (const frame of wallFramesFor(input)) {
    requireSeb(resources, 5, "ObjChip.DrawWall wall");
    const result = resources.drawSeb(graphics, origin.x, origin.y, 5, { frame });
    appendTrace(traces, {
      pass: classifyObjChipWallLayer(input.cell) === "foreground" ? "object-chip-late" : "object-chip-wall",
      kind: "seb",
      resource: result.address,
      frame: result.frame,
      layer: result.layer,
      cell: input.cell,
      destination: origin,
      selectorRole: frame === 1 ? "ObjChip.DrawWall:vertical_frame_1" : "ObjChip.DrawWall:horizontal_frame_0",
      commandCount: result.commandCount,
      proof: "NATIVE-CODE-PROVEN",
    });
  }
}

export function drawObjChipPrimary(
  input: V4ObjChipInput,
  resources: V4ResourceManager,
  camera: V4CameraBoundary,
  graphics: GraphicsCompatibility,
  traces: V4CommandTrace[],
): void {
  getDirectionInfo(input.rawDirection);
  if (input.furnitureBinding === undefined) {
    return;
  }
  if (input.furnitureBinding.rawType !== input.rawType) {
    throw new V4ContractError("V4_INPUT_MALFORMED", "Furniture binding raw type does not match ObjChip raw type");
  }
  drawFurnitureBinding(
    input.furnitureBinding,
    objChipOrigin(input.cell, camera),
    resources,
    graphics,
    traces,
  );
}

export function renderObjChip(
  input: V4ObjChipInput,
  resources: V4ResourceManager,
  camera: V4CameraBoundary,
): V4RenderResult {
  const graphics = new GraphicsCompatibility();
  const traces: V4CommandTrace[] = [];
  drawObjChipPrimary(input, resources, camera, graphics, traces);
  drawObjChipWall(input, resources, camera, graphics, traces);
  return { commands: graphics.commands, traces };
}

function requireSeb(resources: V4ResourceManager, id: number, role: string): void {
  if (!resources.hasSeb(id)) {
    throw new V4ContractError("V4_UNSUPPORTED_SELECTOR", `${role} SEB ${id} is unavailable`);
  }
}

function appendTrace(traces: V4CommandTrace[], trace: V4CommandTrace): void {
  if (trace.commandCount > 0) {
    traces.push(trace);
  }
}

function validateCell(cell: V4Cell): void {
  if (!Number.isSafeInteger(cell[0]) || !Number.isSafeInteger(cell[1])) {
    throw new V4ContractError("V4_CELL_OUT_OF_RANGE", "V4 object cell must contain integer coordinates");
  }
}

function validateRoomSize(width: number, height: number): void {
  if (!Number.isSafeInteger(width) || width <= 0 || !Number.isSafeInteger(height) || height <= 0) {
    throw new V4ContractError("V4_INPUT_MALFORMED", "V4 object room dimensions are malformed");
  }
}
