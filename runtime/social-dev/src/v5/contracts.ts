import type { GraphicsCommand, GraphicsCompatibility } from "../v2/graphics";
import type {
  NativeSceneAssemblyRoom,
  RoomRuntimeNativeBinding,
  RoomSceneRuntimeRecord,
} from "../catalog/types";
import type {
  V4CameraBoundary,
  V4Cell,
  V4CommandTrace,
  V4FurnitureBinding,
  V4MapChipInput,
  V4ObjChipInput,
  V4ResourceManager,
} from "../v4";

export type V5Proof =
  | "NATIVE-CODE-PROVEN"
  | "CALL-FLOW-PROVEN"
  | "SOURCE-DATA-PROVEN"
  | "STATIC-INFERRED"
  | "COMPATIBILITY-POLICY"
  | "SOURCE-LIMITED";

export type V5RoomContext = "main_display" | "persistent_room" | "addition_floor_preview";
export type V5VisualScope = "full_static" | "topology_only";

export interface V5RawObjChip {
  readonly instanceId: string;
  readonly cell: V4Cell;
  readonly rawType: number;
  readonly rawDirection: number;
}

export type V5MapCellRole =
  | "empty"
  | "room_floor_central"
  | "room_floor_fill"
  | "outer_map";

export interface V5MapChip extends V4MapChipInput {
  readonly rawIndex: number;
  readonly role: V5MapCellRole;
}

export interface V5StructuralFacility {
  readonly objectId: string;
  readonly furnitureDataId: number;
  readonly anchor: V4Cell;
  readonly mapAnchor: V4Cell;
  readonly rawType: 4;
  readonly footprintCells: readonly V4Cell[];
  readonly primarySeb: number;
  readonly secondarySeb: number;
  readonly imageSelector: number;
  readonly spriteRecord: Readonly<Record<string, unknown>>;
  readonly sourceStatus: string;
}

export interface V5RoomData {
  readonly roomKey: string;
  readonly dataKey: string;
  readonly roomId: number;
  readonly name: string;
  readonly floorImgId: number;
  readonly wallImgId: number;
  readonly doorImgId: number;
  readonly objMap: readonly (readonly number[])[];
  readonly objDir: readonly (readonly number[])[];
  readonly objMapWidth: number;
  readonly objMapHeight: number;
  readonly rawObjChips: readonly V5RawObjChip[];
  readonly nativeBindings: readonly RoomRuntimeNativeBinding[];
  readonly structuralFacilities: readonly V5StructuralFacility[];
  readonly assembly: NativeSceneAssemblyRoom;
  readonly runtimeRecord: RoomSceneRuntimeRecord;
  readonly source: {
    readonly englishRawRowSha256: string;
    readonly runtimeContract: string;
    readonly nativeAssemblyContract: string;
  };
}

export interface V5RoomTopology {
  readonly roomFloor: number;
  readonly variantId: "floor_0" | "floor_nonzero";
  readonly width: number;
  readonly height: number;
  readonly rows: readonly (readonly number[])[];
  readonly context: V5RoomContext;
  readonly environmentScope: "native_main_14x14_outer_map" | "native_room_topology_only";
  readonly proof: V5Proof;
}

export interface V5PassScheduleRecord {
  readonly index: number;
  readonly passId: string;
  readonly ownerClass: string;
  readonly method: string;
  readonly gridTraversal: string;
  readonly predicate: string;
  readonly resourceFamily: string;
  readonly depthRole: string;
  readonly includedRawTypes: readonly (number | string)[];
  readonly excludedRawTypes: readonly (number | string)[];
  readonly cameraState: string;
  readonly localOrdering: string;
  readonly proof: V5Proof;
  readonly sourceRefs: readonly string[];
}

export interface V5PassResult extends V5PassScheduleRecord {
  readonly inputCount: number;
  readonly commandStart: number;
  readonly commandEnd: number;
  readonly traceStart: number;
  readonly traceEnd: number;
}

export interface V5CommandEvent {
  readonly passId: string;
  readonly cell?: V4Cell;
  readonly rawType?: number;
  readonly role: string;
  readonly commandStart: number;
  readonly commandEnd: number;
  readonly traceStart: number;
  readonly traceEnd: number;
  readonly proof: V5Proof;
}

export interface V5RoomRenderResult {
  readonly commands: readonly GraphicsCommand[];
  readonly traces: readonly V4CommandTrace[];
  readonly passes: readonly V5PassResult[];
  readonly events: readonly V5CommandEvent[];
  readonly camera: V4CameraBoundary;
  readonly resources: V4ResourceManager;
  readonly graphics: GraphicsCompatibility;
}

export interface V5RoomOptions {
  readonly roomFloor?: number;
  readonly context?: V5RoomContext;
  readonly dimensions?: { readonly width: number; readonly height: number };
  readonly cameraOffset?: { readonly x: number; readonly y: number };
  readonly visualScope?: V5VisualScope;
}

export interface V5RoomCommandManifest {
  readonly schemaVersion: 1;
  readonly phase: "V5";
  readonly roomKey: string;
  readonly dataKey: string;
  readonly roomFloor: number;
  readonly floorImgId: number;
  readonly topology: {
    readonly variantId: V5RoomTopology["variantId"];
    readonly width: number;
    readonly height: number;
    readonly context: V5RoomContext;
  };
  readonly cameraOffset: { readonly x: number; readonly y: number };
  readonly visualScope: V5VisualScope;
  readonly passes: readonly V5PassResult[];
  readonly events: readonly V5CommandEvent[];
  readonly traces: readonly V4CommandTrace[];
  readonly commands: readonly GraphicsCommand[];
  readonly nativeBindings: readonly RoomRuntimeNativeBinding[];
  readonly structuralFacilities: readonly V5StructuralFacility[];
  readonly floorSelectorPolicy: {
    readonly rawRoomDataSelector: number;
    readonly nativeTableSelector: number | null;
    readonly runtimeSelector: number;
    readonly renderedFilename: string;
    readonly status: "COMPATIBILITY-POLICY" | "NATIVE-CODE-PROVEN";
  };
}

export interface V5EvidenceRoomSummary {
  readonly roomKey: string;
  readonly roomId: number;
  readonly name: string;
  readonly floor: number;
  readonly floorImgId: number;
  readonly wallImgId: number;
  readonly doorImgId: number;
  readonly objMapShape: readonly [number, number];
  readonly objDirShape: readonly [number, number];
  readonly doorCells: readonly V4Cell[];
  readonly wallCellsByFrame: Readonly<Record<string, readonly V4Cell[]>>;
  readonly rawTypeCounts: Readonly<Record<string, number>>;
  readonly directionCounts: Readonly<Record<string, number>>;
  readonly initialFurnitureCount: number;
  readonly initialFurnitureBindingStatus: string;
  readonly sourceHash: string;
  readonly status: "FULL_STATIC_SCENE_PROVEN" | "TOPOLOGY_ONLY" | "SOURCE_LIMITED" | "UNKNOWN_BLOCKING";
}

export type V5ObjChip = V4ObjChipInput;
export type V5FurnitureBinding = V4FurnitureBinding;
