import type {
  GraphicsCommand,
  GraphicsRect,
  GraphicsStateSnapshot,
} from "../v2/graphics";

export type V7ProofClass =
  | "PROVEN"
  | "INFERRED_STRONG"
  | "COMPATIBILITY_REIMPLEMENTATION"
  | "PRODUCT_POLICY"
  | "SOURCE_LIMITED";

export type V7DifferenceClass =
  | "A_SOURCE_COMMAND_BUG"
  | "B_RASTER_CONTRACT_BUG"
  | "C_COMPATIBILITY_BACKEND_DIFFERENCE"
  | "D_PRODUCT_POLICY_DIFFERENCE"
  | "E_HISTORICAL_CONTEXT_DIFFERENCE"
  | "F_UNKNOWN";

export type V7FlipMode = 0 | 1 | 2 | 3 | 4 | 5;

export interface V7Point {
  readonly x: number;
  readonly y: number;
}

export interface V7RasterImage {
  readonly id: string | number;
  readonly width: number;
  readonly height: number;
  readonly pixels: Uint8Array;
  readonly sourceRef?: string;
  readonly sourceSha256?: string;
}

export interface V7RasterSurface {
  readonly width: number;
  readonly height: number;
  readonly pixels: Uint8Array;
}

export interface V7SurfaceOrigin {
  readonly x: number;
  readonly y: number;
}

export interface V7RasterTransform {
  readonly scaleX?: number;
  readonly scaleY?: number;
  readonly rotationDegrees?: number;
  readonly pivot?: V7Point;
}

export interface V7RasterClip {
  readonly rect: GraphicsRect;
  readonly transformed?: V7RasterTransform;
}

export interface V7DrawRequest {
  readonly image: V7RasterImage;
  readonly destination: GraphicsRect;
  readonly source: GraphicsRect;
  readonly state: GraphicsStateSnapshot;
  readonly clip?: V7RasterClip | null;
  readonly transform?: V7RasterTransform;
  readonly flipMode?: V7FlipMode;
}

export interface V7RasterOptions {
  readonly width: number;
  readonly height: number;
  readonly origin?: V7SurfaceOrigin;
  readonly background?: readonly [number, number, number, number];
}

export interface V7RenderResult {
  readonly surface: V7RasterSurface;
  readonly commands: readonly GraphicsCommand[];
  readonly drawCount: number;
  readonly skippedDrawCount: number;
  readonly nonTransparentBounds: V7Bounds | null;
}

export interface V7Bounds {
  readonly x: number;
  readonly y: number;
  readonly width: number;
  readonly height: number;
}

export interface V7PixelDiffResult {
  readonly width: number;
  readonly height: number;
  readonly changedPixelCount: number;
  readonly maxChannelError: number;
  readonly meanChannelError: number;
  readonly changedRegion: V7Bounds | null;
  readonly identical: boolean;
}

export interface V7GoldenFixtureRecord {
  readonly fixtureId: string;
  readonly category: "asset" | "graphics" | "staff" | "scene";
  readonly sourceRefs: readonly string[];
  readonly commandHash: string;
  readonly outputWidth: number;
  readonly outputHeight: number;
  readonly pixelSha256: string;
  readonly nonTransparentBounds: V7Bounds | null;
  readonly proofClass: V7ProofClass;
  readonly compatibilityAssumptions: readonly string[];
}
