import { GraphicsCompatibility } from "../v2/graphics";
import { V4ContractError } from "./errors";
import type {
  V4CommandTrace,
  V4FurnitureBinding,
  V4FurnitureSelectors,
  V4Point,
  V4ResolvedSelector,
} from "./contracts";
import { V4ResourceManager } from "./resources";

export function resolveFurnitureSelectors(
  resources: V4ResourceManager,
  selectors: V4FurnitureSelectors,
): readonly V4ResolvedSelector[] {
  return [
    resolveSelector(resources, selectors.primarySeb, "seb"),
    resolveSelector(resources, selectors.secondarySeb, "seb"),
    resolveSelector(resources, selectors.dataImage, "image"),
  ];
}

export function drawFurnitureBinding(
  binding: V4FurnitureBinding,
  anchor: V4Point,
  resources: V4ResourceManager,
  graphics: GraphicsCompatibility,
  traces: V4CommandTrace[],
): void {
  if (!Number.isSafeInteger(binding.furnitureDataId) || binding.furnitureDataId < 0) {
    throw new V4ContractError("V4_INPUT_MALFORMED", "FurnitureData ID is malformed");
  }
  if (!Number.isSafeInteger(binding.rawType) || binding.rawType < 0) {
    throw new V4ContractError("V4_INPUT_MALFORMED", "Raw ObjChip type is malformed");
  }
  if (binding.renderMode === "direct_image") {
    drawDirectImageBinding(binding, anchor, resources, graphics, traces);
    return;
  }
  if (binding.renderMode !== "primary_seb_plus_secondary_seb") {
    throw new V4ContractError("V4_UNSUPPORTED_BRANCH", `Furniture binding ${binding.objectId} has no V4 render mode`);
  }

  if (binding.primarySeb >= 0) {
    const result = resources.drawSeb(graphics, anchor.x, anchor.y, binding.primarySeb, {
      frame: binding.primaryFrame ?? 0,
    });
    appendTrace(traces, {
      pass: "object-chip-primary",
      kind: "seb",
      resource: result.address,
      frame: result.frame,
      layer: result.layer,
      destination: anchor,
      selectorRole: "FurnitureData.seb_",
      commandCount: result.commandCount,
      proof: "STATIC-COMMAND-PARITY",
    });
  }
  if (binding.secondarySeb >= 0) {
    const result = resources.drawSeb(graphics, anchor.x, anchor.y, binding.secondarySeb, {
      frame: binding.secondaryFrame ?? 0,
    });
    appendTrace(traces, {
      pass: "object-chip-primary",
      kind: "seb",
      resource: result.address,
      frame: result.frame,
      layer: result.layer,
      destination: anchor,
      selectorRole: "FurnitureData.subSeb_",
      commandCount: result.commandCount,
      proof: "STATIC-COMMAND-PARITY",
    });
  }
}

function drawDirectImageBinding(
  binding: V4FurnitureBinding,
  anchor: V4Point,
  resources: V4ResourceManager,
  graphics: GraphicsCompatibility,
  traces: V4CommandTrace[],
): void {
  const imageSelector = binding.imageSelector ?? binding.dataImage;
  if (imageSelector < 0 || binding.imageSource === undefined || binding.destinationOffset === undefined) {
    throw new V4ContractError("V4_UNSUPPORTED_SELECTOR", `Furniture binding ${binding.objectId} has no direct-image record`);
  }
  const destination = {
    x: anchor.x + binding.destinationOffset.x,
    y: anchor.y + binding.destinationOffset.y,
  };
  const commandCount = resources.drawImage(graphics, imageSelector, destination.x, destination.y, binding.imageSource);
  const image = resources.resolveImage(imageSelector);
  appendTrace(traces, {
    pass: "object-chip-primary",
    kind: "image",
    resource: image.address,
    destination,
    selectorRole: "FurnitureData.img_:native_direct_image",
    commandCount,
    proof: "STATIC-COMMAND-PARITY",
  });
}

function resolveSelector(
  resources: V4ResourceManager,
  selector: number,
  kind: "seb" | "image",
): V4ResolvedSelector {
  if (!Number.isSafeInteger(selector)) {
    throw new V4ContractError("V4_INPUT_MALFORMED", "Furniture selector is malformed");
  }
  if (selector < 0) {
    return { selector, status: "sentinel", kind, resource: null };
  }
  if (kind === "seb") {
    resources.getSeb(selector);
  } else {
    resources.getImage(selector);
  }
  return {
    selector,
    status: "resolved",
    kind,
    resource: { groupId: resources.groupId, id: selector },
  };
}

function appendTrace(traces: V4CommandTrace[], trace: V4CommandTrace): void {
  if (trace.commandCount > 0) {
    traces.push(trace);
  }
}
