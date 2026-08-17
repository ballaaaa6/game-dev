import type { MoveMode, StaffState } from "./constants";

export type LivingCell = readonly [number, number];

export interface LivingWorldPosition {
  readonly x: number;
  readonly y: number;
}

export interface LivingFurniture {
  readonly instanceId: number;
  readonly rawIndex: number;
  readonly rawType: number;
  readonly rawDirection: number;
  readonly cell: LivingCell;
  readonly furnitureDataId: number | null;
  readonly installed: boolean;
  readonly ownerStaffId: number;
  readonly activeUserIds: readonly number[];
  readonly reservedUserIds: readonly number[];
  readonly useFrame: number;
  readonly actionStarted: boolean;
  readonly actionId: number;
  readonly recovery: number;
  readonly removed: boolean;
}

export interface LivingStaff {
  readonly id: number;
  readonly actorId: string;
  readonly staffDataId: number;
  readonly jobId: number;
  readonly skillId: number;
  readonly level: number;
  readonly motivation: number;
  readonly hp: number;
  readonly maxHp: number;
  readonly state: StaffState;
  readonly moveMode: MoveMode;
  readonly flags: number;
  readonly cell: LivingCell;
  readonly world: LivingWorldPosition;
  readonly alpha: number;
  readonly speed: number;
  readonly route: readonly LivingCell[];
  readonly lastNode: LivingCell | null;
  readonly goalCell: LivingCell | null;
  readonly goalFlags: number;
  readonly objIndex: number;
  readonly deskId: number;
  readonly equipmentId: number;
  readonly colleagueId: number;
  readonly frame: number;
  readonly moveFrame: number;
  readonly typingFrame: number;
  readonly talkFrame: number;
  readonly recoveryEffectFrame: number;
  readonly frameToStartRecovery: number;
  readonly frameToHideHpGauge: number;
  readonly recoveryStock: number;
  readonly delay: number;
  readonly meetingPointGauge: number;
  readonly actionId: number;
  readonly removed: boolean;
}

export interface LivingRoom {
  readonly roomDataId: number;
  readonly roomKey: string;
  readonly width: number;
  readonly height: number;
  readonly objMap: readonly (readonly number[])[];
  readonly objDir: readonly (readonly number[])[];
  readonly furniture: readonly LivingFurniture[];
  readonly staffIds: readonly number[];
}

export interface LivingPlayer {
  readonly planning: boolean;
  readonly completed: boolean;
  readonly elapsedPlanning: number;
}

export interface RngDraw {
  readonly sequence: number;
  readonly stream: "AppData" | "Lib";
  readonly method: string;
  readonly min: number;
  readonly max: number;
  readonly exclusiveMax: boolean;
  readonly value: number;
}

export interface LivingTrace {
  readonly sequence: number;
  readonly tick: number;
  readonly staffId: number | null;
  readonly event: string;
  readonly beforeState: number | null;
  readonly afterState: number | null;
  readonly beforeMoveMode: number | null;
  readonly afterMoveMode: number | null;
  readonly flags: number | null;
  readonly cell: LivingCell | null;
  readonly route: readonly LivingCell[];
  readonly deskId: number | null;
  readonly equipmentId: number | null;
  readonly colleagueId: number | null;
  readonly hp: number | null;
  readonly recoveryStock: number | null;
  readonly rngSequence: number | null;
  readonly evidenceContractId: string;
}

export interface LivingSnapshot {
  readonly frame: number;
  readonly room: LivingRoom;
  readonly staffs: readonly LivingStaff[];
  readonly player: LivingPlayer;
  readonly traces: readonly LivingTrace[];
  readonly rngDraws: readonly RngDraw[];
  readonly rngState: {
    readonly appDataIndex: number;
    readonly libIndex: number;
    readonly fallbackState: number;
  };
  readonly rngReplay: {
    readonly appData: readonly number[];
    readonly lib: readonly number[];
  };
  readonly meetingPointGauge: number;
}

export interface LivingCommand {
  readonly type: "add_staff" | "remove_furniture" | "start_planning" | "end_planning" | "goto_equip" | "goto_talk";
  readonly staffId?: number;
  readonly staffDataId?: number;
  readonly furnitureInstanceId?: number;
}
