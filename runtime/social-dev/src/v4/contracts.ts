import type { GraphicsCommand, GraphicsCompatibility, GraphicsImageRef } from "../v2/graphics";

export type V4Cell = readonly [number, number];

export interface V4Point {
  readonly x: number;
  readonly y: number;
}

export interface V4ImageDimension {
  readonly id: number;
  readonly width: number;
  readonly height: number;
  readonly role?: string;
}

export interface V4ResourceAddress {
  readonly groupId: string;
  readonly id: number;
}

export type V4TraceKind = "seb" | "image";

export interface V4CommandTrace {
  readonly pass: string;
  readonly kind: V4TraceKind;
  readonly resource: V4ResourceAddress;
  readonly frame?: number;
  readonly layer?: number | null;
  readonly cell?: V4Cell;
  readonly destination: V4Point;
  readonly selectorRole: string;
  readonly commandCount: number;
  readonly proof: "STATIC-COMMAND-PARITY" | "NATIVE-CODE-PROVEN" | "CALL-FLOW-PROVEN";
}

export interface V4RenderBuffer {
  readonly graphics: GraphicsCompatibility;
  readonly traces: V4CommandTrace[];
}

export interface V4RenderResult {
  readonly commands: readonly GraphicsCommand[];
  readonly traces: readonly V4CommandTrace[];
}

export interface V4ResolvedImage {
  readonly address: V4ResourceAddress;
  readonly ref: GraphicsImageRef;
  readonly width: number;
  readonly height: number;
  readonly sourceMember: string;
}

export interface V4SebDrawResult {
  readonly address: V4ResourceAddress;
  readonly frame: number;
  readonly layer: number | null;
  readonly commandCount: number;
  readonly resolvedTextureIds: readonly number[];
}

export interface V4CameraOffset {
  readonly x: number;
  readonly y: number;
}

export interface V4FurnitureSelectors {
  readonly furnitureDataId: number;
  readonly rawType: number;
  readonly primarySeb: number;
  readonly secondarySeb: number;
  readonly dataImage: number;
}

export interface V4ResolvedSelector {
  readonly selector: number;
  readonly status: "resolved" | "sentinel";
  readonly kind: "seb" | "image";
  readonly resource: V4ResourceAddress | null;
}

export interface V4FurnitureBinding extends V4FurnitureSelectors {
  readonly objectId: string;
  readonly renderMode: "primary_seb_plus_secondary_seb" | "direct_image";
  readonly imageSelector?: number;
  readonly imageSource?: { readonly x: number; readonly y: number; readonly width: number; readonly height: number };
  readonly destinationOffset?: V4Point;
  readonly primaryFrame?: number;
  readonly secondaryFrame?: number;
}

export function createRenderBuffer(graphics: GraphicsCompatibility): V4RenderBuffer {
  return { graphics, traces: [] };
}
