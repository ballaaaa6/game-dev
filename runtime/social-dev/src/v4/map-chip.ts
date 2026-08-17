import { GraphicsCompatibility } from "../v2/graphics";
import { V4CameraBoundary } from "./camera";
import { V4ContractError } from "./errors";
import type {
  V4Cell,
  V4CommandTrace,
  V4Point,
  V4RenderResult,
} from "./contracts";
import { V4ResourceManager } from "./resources";

export interface V4MapChipInput {
  readonly cell: V4Cell;
  readonly imageId: number;
  readonly roomFloor: number;
  readonly roomWidth: number;
  readonly roomHeight: number;
}

const VERTICAL_EXTENSION_CELLS: readonly V4Cell[] = [[4, 5], [4, 6], [8, 9], [8, 10], [8, 11]];
const HORIZONTAL_EXTENSION_CELLS: readonly V4Cell[] = [[2, 5], [3, 5], [4, 5], [7, 9], [8, 9]];

export function mapChipOrigin(cell: V4Cell, camera: V4CameraBoundary): V4Point {
  validateCell(cell);
  return camera.transform({
    x: (cell[0] + cell[1]) * 40,
    y: (cell[1] - cell[0]) * 20,
  });
}

export function isMapFloorCellVisible(cell: V4Cell, roomWidth: number, roomHeight: number): boolean {
  validateRoomSize(roomWidth, roomHeight);
  validateCell(cell);
  const xStart = (roomWidth - 4) >> 1;
  const yStart = (roomHeight - 4) >> 1;
  return cell[0] >= xStart
    && cell[0] <= xStart + 4
    && cell[1] >= yStart
    && cell[1] < yStart + 4;
}

export function drawMapExtension(
  input: V4MapChipInput,
  resources: V4ResourceManager,
  camera: V4CameraBoundary,
  graphics: GraphicsCompatibility,
  traces: V4CommandTrace[],
): void {
  const origin = mapChipOrigin(input.cell, camera);
  const group = cellIn(input.cell, VERTICAL_EXTENSION_CELLS)
    ? { frame: 1, name: "vertical_frame_1", offsets: [[20, -1], [40, 9]] as const }
    : cellIn(input.cell, HORIZONTAL_EXTENSION_CELLS)
      ? { frame: 0, name: "horizontal_frame_0", offsets: [[20, -1], [4, 9]] as const }
      : null;
  if (group === null) {
    return;
  }
  if (!resources.hasSeb(63)) {
    throw new V4ContractError("V4_UNSUPPORTED_SELECTOR", "Selected MapChip extension SEB 63 is unavailable");
  }
  for (const [x, y] of group.offsets) {
    const destination = { x: origin.x + x, y: origin.y + y };
    const result = resources.drawSeb(graphics, destination.x, destination.y, 63, { frame: group.frame });
    appendTrace(traces, {
      pass: "map-extension-floor",
      kind: "seb",
      resource: result.address,
      frame: result.frame,
      layer: result.layer,
      cell: input.cell,
      destination,
      selectorRole: `MapChip.DrawExtentionFloor:${group.name}`,
      commandCount: result.commandCount,
      proof: "NATIVE-CODE-PROVEN",
    });
  }
}

export function drawMapChipBoundary(
  input: V4MapChipInput,
  resources: V4ResourceManager,
  camera: V4CameraBoundary,
  graphics: GraphicsCompatibility,
  traces: V4CommandTrace[],
): void {
  if (input.roomFloor < 1) {
    return;
  }
  validateRoomSize(input.roomWidth, input.roomHeight);
  const origin = mapChipOrigin(input.cell, camera);
  if (input.cell[0] === 0) {
    drawBoundarySeb(input, resources, graphics, traces, origin, 2, input.cell[1] === 0 ? 2 : 0, { x: origin.x, y: origin.y + 20 });
    drawOptionalBoundaryOverlay(input, resources, graphics, traces, origin, input.cell[1] === 0 ? 0 : 2, { x: origin.x, y: origin.y + 38 });
  }
  if (input.cell[1] === input.roomHeight - 1) {
    drawBoundarySeb(input, resources, graphics, traces, origin, 2, input.cell[0] === input.roomWidth - 1 ? 3 : 1, { x: origin.x, y: origin.y + 20 });
    drawOptionalBoundaryOverlay(input, resources, graphics, traces, origin, input.cell[0] === input.roomWidth - 1 ? 1 : 3, { x: origin.x, y: origin.y + 38 });
  }
}

export function drawMapFloor(
  input: V4MapChipInput,
  resources: V4ResourceManager,
  camera: V4CameraBoundary,
  graphics: GraphicsCompatibility,
  traces: V4CommandTrace[],
): void {
  if (input.imageId < 0 || !isMapFloorCellVisible(input.cell, input.roomWidth, input.roomHeight)) {
    return;
  }
  const origin = mapChipOrigin(input.cell, camera);
  const image = resources.resolveImage(input.imageId);
  const destination = { x: origin.x, y: origin.y + 39 - image.height };
  resources.drawImage(graphics, input.imageId, destination.x, destination.y, {
    x: 0,
    y: 0,
    width: image.width,
    height: image.height,
  });
  appendTrace(traces, {
    pass: "map-floor",
    kind: "image",
    resource: image.address,
    cell: input.cell,
    destination,
    selectorRole: "MapChip.DrawFloor:imageId_",
    commandCount: 1,
    proof: "NATIVE-CODE-PROVEN",
  });
}

export function renderMapChip(
  input: V4MapChipInput,
  resources: V4ResourceManager,
  camera: V4CameraBoundary,
): V4RenderResult {
  const graphics = new GraphicsCompatibility();
  const traces: V4CommandTrace[] = [];
  drawMapExtension(input, resources, camera, graphics, traces);
  drawMapChipBoundary(input, resources, camera, graphics, traces);
  drawMapFloor(input, resources, camera, graphics, traces);
  return { commands: graphics.commands, traces };
}

function drawBoundarySeb(
  input: V4MapChipInput,
  resources: V4ResourceManager,
  graphics: GraphicsCompatibility,
  traces: V4CommandTrace[],
  _origin: V4Point,
  sebId: number,
  frame: number,
  destination: V4Point,
): void {
  if (!resources.hasSeb(sebId)) {
    return;
  }
  const result = resources.drawSeb(graphics, destination.x, destination.y, sebId, { frame });
  appendTrace(traces, {
    pass: "map-chip",
    kind: "seb",
    resource: result.address,
    frame: result.frame,
    layer: result.layer,
    cell: input.cell,
    destination,
    selectorRole: "MapChip.Draw:boundary",
    commandCount: result.commandCount,
    proof: "NATIVE-CODE-PROVEN",
  });
}

function drawOptionalBoundaryOverlay(
  input: V4MapChipInput,
  resources: V4ResourceManager,
  graphics: GraphicsCompatibility,
  traces: V4CommandTrace[],
  _origin: V4Point,
  frame: number,
  destination: V4Point,
): void {
  // Selector 7 is retained in the native contract, but it is not present in
  // the selected static resChip_ V3 fixture. Safe behavior is no command.
  drawBoundarySeb(input, resources, graphics, traces, _origin, 7, frame, destination);
}

function appendTrace(traces: V4CommandTrace[], trace: V4CommandTrace): void {
  if (trace.commandCount > 0) {
    traces.push(trace);
  }
}

function cellIn(cell: V4Cell, cells: readonly V4Cell[]): boolean {
  return cells.some((candidate) => candidate[0] === cell[0] && candidate[1] === cell[1]);
}

function validateCell(cell: V4Cell): void {
  if (!Number.isSafeInteger(cell[0]) || !Number.isSafeInteger(cell[1])) {
    throw new V4ContractError("V4_CELL_OUT_OF_RANGE", "V4 map cell must contain integer coordinates");
  }
}

function validateRoomSize(width: number, height: number): void {
  if (!Number.isSafeInteger(width) || width <= 0 || !Number.isSafeInteger(height) || height <= 0) {
    throw new V4ContractError("V4_INPUT_MALFORMED", "V4 map room dimensions are malformed");
  }
}
