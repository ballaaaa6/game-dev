import type { SceneProjection } from "../scene/projection";

export const NATIVE_RENDER_PASS_ORDER = [
  "map-extension-floor",
  "map-chip",
  "object-chip-primary",
  "object-chip-wall",
  "avatar-primary",
  "avatar-secondary",
  "object-chip-late-preview",
  "object-chip-late",
  "map-floor",
] as const;

export type NativeRenderPassId = (typeof NATIVE_RENDER_PASS_ORDER)[number];

export interface RenderPassPlanEntry {
  readonly id: NativeRenderPassId;
  readonly layerRole: string;
}

const LAYER_ROLE_BY_PASS: Readonly<Record<NativeRenderPassId, string>> = {
  "map-extension-floor": "MapChip.DrawExtentionFloor",
  "map-chip": "MapChip.Draw",
  "object-chip-primary": "ObjChip.Draw",
  "object-chip-wall": "ObjChip.DrawWall",
  "avatar-primary": "Avatar.Draw",
  "avatar-secondary": "Avatar.DrawSecondary",
  "object-chip-late-preview": "ObjChip.DrawLatePreview",
  "object-chip-late": "ObjChip.DrawLate",
  "map-floor": "MapChip.DrawFloor",
};

export function createRenderPassPlan(projection: Pick<SceneProjection, "drawPasses">): readonly RenderPassPlanEntry[] {
  const expected = NATIVE_RENDER_PASS_ORDER.join(",");
  const actual = projection.drawPasses.join(",");
  if (actual !== expected) {
    throw new Error(`Scene render pass contract drift: ${actual} !== ${expected}`);
  }
  return NATIVE_RENDER_PASS_ORDER.map((id) => ({ id, layerRole: LAYER_ROLE_BY_PASS[id] }));
}
