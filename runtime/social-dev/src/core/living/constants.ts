export const StaffState = {
  NORMAL: 0,
  MEETING: 1,
  MOVE: 2,
  SIT_DOWN: 3,
  WORK: 4,
  USE_EQUIPMENT: 5,
  TALK: 6,
  INVITE_TO_TALK: 7,
  FLY_AWAY: 8,
  WAIT: 9,
  WANDER: 10,
  WAIT_BACK_OF_DOOR: 11,
  DEVELOP: 12,
  STAY_HOME: 13,
} as const;

export type StaffState = (typeof StaffState)[keyof typeof StaffState];

export const MoveMode = {
  STAY: 0,
  GOTO_EQUIPMENT: 1,
  WANDER: 2,
  GOTO_DESK: 3,
  INTO_EQUIPMENT: 4,
  OUTOF_EQUIPMENT: 5,
  SIT_DOWN: 6,
  TO_STAFF: 7,
  TO_STAND_TALKING: 8,
  TO_BACK_OF_CHAIR: 9,
  GO_TO_DOOR: 10,
  GO_HOME: 11,
} as const;

export type MoveMode = (typeof MoveMode)[keyof typeof MoveMode];

export const StaffFlag = {
  SITTING: 2,
  RESERVED_TALK: 4,
  INVITED: 8,
  TYPING: 16,
  SLEEPING: 32,
  PLANNING: 64,
  FADE_IN: 128,
  FADE_OUT: 256,
  PLANNING_COMPLETED: 512,
  SLIDING: 1024,
  PLATFORM_DEVELOP: 2048,
  NEW: 4096,
  DELETE_NEW: 8192,
  NEW_FUKIDASHI: 16384,
  WAITING_ROOM: 32768,
  LEADER: 65536,
  REINFORCE: 131072,
  SPECIAL_CHALLENGE: 262144,
  FESTIVAL: 524288,
} as const;

export const ObjChipType = {
  PASS: 0,
  EQUIPMENT: 1,
  DESK: 2,
  BIG: 3,
  BIG_CENTER: 4,
  DOOR: 5,
  OUTDOOR: 6,
} as const;

export type ObjChipType = (typeof ObjChipType)[keyof typeof ObjChipType];

export const GoalFlag = {
  DESK: 1,
  EQUIPMENT: 2,
  STAFF: 4,
} as const;

export const STAFF_STATE_VALUES = Object.values(StaffState);
export const MOVE_MODE_VALUES = Object.values(MoveMode);
export const STAFF_FLAG_VALUES = Object.values(StaffFlag);

export function isStaffState(value: number): value is StaffState {
  return STAFF_STATE_VALUES.includes(value as StaffState);
}

export function isMoveMode(value: number): value is MoveMode {
  return MOVE_MODE_VALUES.includes(value as MoveMode);
}
