import { GraphicsCompatibility } from "../v2/graphics";
import { mapChipOrigin } from "../v4/map-chip";
import type { V4CommandTrace } from "../v4/contracts";
import type { V5MapChip } from "./contracts";
import type { V4CameraBoundary, V4ResourceManager } from "../v4";

/**
 * The main-display Room owns a source-backed 14x14 map underlay in addition
 * to the generic Room.Draw slots.  The production scene contract commits this
 * underlay before extension/object pixels so the starter room is not reduced
 * to the central 4x4 floor culling window.
 */
export function drawMainDisplayMapCell(
  input: V5MapChip,
  resources: V4ResourceManager,
  camera: V4CameraBoundary,
  graphics: GraphicsCompatibility,
  traces: V4CommandTrace[],
): void {
  if (input.roomFloor !== 0 || input.roomWidth !== 14 || input.roomHeight !== 14 || input.role === "empty") {
    return;
  }
  if (input.imageId < 0) {
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
  traces.push({
    pass: "main-display-map-underlay",
    kind: "image",
    resource: image.address,
    cell: input.cell,
    destination,
    selectorRole: `Room.main_display.MapChip.raw_index_${input.rawIndex}:${input.role}`,
    commandCount: 1,
    proof: "NATIVE-CODE-PROVEN",
  });
}
