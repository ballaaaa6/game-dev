import type { RuntimeCatalogs } from "../../catalog/load-contracts";
import { cellToActorWorld } from "../../scene/coordinates";
import { calculateMaxHp, furnitureRecovery, furnitureRecord, furnitureType, i0Catalog, skillRecord, staffJobAndSkill, staffRecord } from "./catalog";
import { GoalFlag, MoveMode, ObjChipType, StaffFlag, StaffState } from "./constants";
import { searchRoute } from "./astar";
import {
  completeAction,
  getUsersNum,
  releaseReservation,
  removeFurniture as removeFurnitureState,
  reserveUse,
  startAction,
} from "./furniture";
import { buildRoom, cloneRoom, findDesk, findEquipment, findFurniture, removeRoomFurniture } from "./room";
import { endPlanning, startPlanning, updatePlanning } from "./planning";
import { createRngFromSnapshot, ReplayRng, type ReplayRngOptions } from "./rng";
import { clearRoute, installRoute, mutableStaff, onArriveNextNode, type MutableStaff } from "./movement";
import { TraceRecorder } from "./trace";
import type {
  LivingCell,
  LivingCommand,
  LivingFurniture,
  LivingPlayer,
  LivingRoom,
  LivingSnapshot,
  LivingStaff,
  LivingTrace,
} from "./types";

export interface LivingRuntimeOptions {
  readonly initialStaffDataIds?: readonly number[];
  readonly scenarioEquipment?: boolean;
  readonly appDataReplay?: readonly number[];
  readonly libReplay?: readonly number[];
  readonly rng?: ReplayRng;
  readonly room?: LivingRoom;
  readonly snapshot?: LivingSnapshot;
}

export interface LivingStaffPatch {
  readonly state?: StaffState;
  readonly moveMode?: MoveMode;
  readonly flags?: number;
  readonly cell?: LivingCell;
  readonly hp?: number;
  readonly deskId?: number;
  readonly equipmentId?: number;
  readonly colleagueId?: number;
  readonly frame?: number;
  readonly talkFrame?: number;
}

function cloneCell(cell: LivingCell): LivingCell {
  return [cell[0], cell[1]];
}

function cloneStaff(staff: LivingStaff): LivingStaff {
  return {
    ...staff,
    cell: cloneCell(staff.cell),
    world: { ...staff.world },
    route: staff.route.map(cloneCell),
    lastNode: staff.lastNode ? cloneCell(staff.lastNode) : null,
    goalCell: staff.goalCell ? cloneCell(staff.goalCell) : null,
  };
}

function clonePlayer(player: LivingPlayer): LivingPlayer {
  return { ...player };
}

function beforeState(staff: LivingStaff): Partial<LivingStaff> {
  return {
    state: staff.state,
    moveMode: staff.moveMode,
    flags: staff.flags,
    cell: cloneCell(staff.cell),
    route: staff.route.map(cloneCell),
    deskId: staff.deskId,
    equipmentId: staff.equipmentId,
    colleagueId: staff.colleagueId,
    hp: staff.hp,
    recoveryStock: staff.recoveryStock,
  };
}

function staffName(catalogs: RuntimeCatalogs, staffDataId: number): string {
  const record = staffRecord(catalogs, staffDataId);
  const data = record.fields as Record<string, unknown>;
  return `${String(data.firstName_ ?? "Staff")} ${String(data.lastName_ ?? staffDataId)}`;
}

export class LivingRuntime {
  public readonly catalogs: RuntimeCatalogs;
  private roomState: LivingRoom;
  private staffState: LivingStaff[];
  private playerState: LivingPlayer;
  private tickFrame: number;
  private readonly rng: ReplayRng;
  private readonly recorder: TraceRecorder;
  private meetingGauge: number;
  private readonly replayAppData: readonly number[];
  private readonly replayLib: readonly number[];
  private initialSnapshotState: LivingSnapshot;

  public constructor(catalogs: RuntimeCatalogs, options: LivingRuntimeOptions = {}) {
    this.catalogs = catalogs;
    this.replayAppData = options.appDataReplay ?? [];
    this.replayLib = options.libReplay ?? [];
    if (options.snapshot) {
      this.roomState = cloneRoom(options.snapshot.room);
      this.staffState = options.snapshot.staffs.map(cloneStaff);
      this.playerState = clonePlayer(options.snapshot.player);
      this.tickFrame = options.snapshot.frame;
      this.meetingGauge = options.snapshot.meetingPointGauge;
      this.recorder = new TraceRecorder(options.snapshot.traces);
      this.rng = createRngFromSnapshot(options.snapshot.rngState, options.snapshot.rngDraws, options.snapshot.rngReplay);
      this.initialSnapshotState = options.snapshot;
      return;
    }
    this.roomState = options.room ? cloneRoom(options.room) : buildRoom(catalogs, { scenarioEquipment: options.scenarioEquipment });
    this.staffState = [];
    this.playerState = { planning: false, completed: false, elapsedPlanning: 0 };
    this.tickFrame = 0;
    this.meetingGauge = 0;
    this.recorder = new TraceRecorder();
    this.rng = options.rng ?? new ReplayRng({ appData: this.replayAppData, lib: this.replayLib });
    for (const staffDataId of options.initialStaffDataIds ?? []) {
      this.addStaff(staffDataId);
    }
    this.initialSnapshotState = this.snapshot();
  }

  public static fromSnapshot(catalogs: RuntimeCatalogs, snapshot: LivingSnapshot): LivingRuntime {
    return new LivingRuntime(catalogs, { snapshot });
  }

  public get frame(): number {
    return this.tickFrame;
  }

  public get room(): LivingRoom {
    return this.roomState;
  }

  public get staffs(): readonly LivingStaff[] {
    return this.staffState;
  }

  public get player(): LivingPlayer {
    return this.playerState;
  }

  public get traces(): readonly LivingTrace[] {
    return this.recorder.all();
  }

  public initialSnapshot(): LivingSnapshot {
    return this.initialSnapshotState;
  }

  public addStaff(staffDataId: number, explicitId?: number): LivingStaff {
    const id = explicitId ?? (this.staffState.length === 0 ? 0 : Math.max(...this.staffState.map((staff) => staff.id)) + 1);
    const data = staffRecord(this.catalogs, staffDataId);
    const dataFields = data.fields as Record<string, unknown>;
    const jobId = Number(dataFields.jobId_);
    const skillId = Number(dataFields.skill_);
    staffJobAndSkill(this.catalogs, staffDataId);
    skillRecord(this.catalogs, skillId);
    const spawn = i0Catalog(this.catalogs).bootstrap.staff_spawn;
    const spawnCell = cloneCell([spawn.cell[0], spawn.cell[1]]);
    const staff: LivingStaff = {
      id,
      actorId: `actor:staff:${id}`,
      staffDataId,
      jobId,
      skillId,
      level: 0,
      motivation: 0,
      hp: 100,
      maxHp: calculateMaxHp(this.catalogs, staffDataId, 0, 0),
      state: StaffState.NORMAL,
      moveMode: MoveMode.STAY,
      flags: this.playerState.planning ? StaffFlag.PLANNING : 0,
      cell: spawnCell,
      world: cellToActorWorld(spawnCell, this.catalogs.camera),
      alpha: spawn.alpha,
      speed: spawn.speed,
      route: [],
      lastNode: null,
      goalCell: null,
      goalFlags: 0,
      objIndex: -1,
      deskId: -1,
      equipmentId: -1,
      colleagueId: -1,
      frame: 0,
      moveFrame: 0,
      typingFrame: 0,
      talkFrame: 0,
      recoveryEffectFrame: -1,
      frameToStartRecovery: -1,
      frameToHideHpGauge: 0,
      recoveryStock: 0,
      delay: 0,
      meetingPointGauge: 0,
      actionId: -1,
      removed: false,
    };
    this.staffState.push(staff);
    const room = this.roomState as unknown as { staffIds: number[] };
    room.staffIds.push(id);
    this.record("staff-data-bind", staff);

    const desk = findDesk(this.roomState);
    if (desk) {
      const mutableDesk = desk as unknown as { ownerStaffId: number };
      mutableDesk.ownerStaffId = id;
      const mutableStaff = mutableStaffFor(staff);
      mutableStaff.deskId = desk.instanceId;
      mutableStaff.objIndex = desk.instanceId;
      this.record("desk-select", staff, { deskId: -1 });
      this.record("desk-owner-acquired", staff, { deskId: -1 });
    }
    this.record("room-add-staff", staff);
    return staff;
  }

  public configureStaff(staffId: number, patch: LivingStaffPatch): LivingStaff {
    const staff = this.requireStaff(staffId);
    const mutable = mutableStaffFor(staff);
    const before = beforeState(staff);
    if (patch.state !== undefined) mutable.state = patch.state;
    if (patch.moveMode !== undefined) mutable.moveMode = patch.moveMode;
    if (patch.flags !== undefined) mutable.flags = patch.flags;
    if (patch.cell !== undefined) {
      mutable.cell = cloneCell(patch.cell);
      mutable.world = cellToActorWorld(mutable.cell, this.catalogs.camera);
    }
    if (patch.hp !== undefined) mutable.hp = Math.max(0, Math.min(mutable.maxHp, patch.hp));
    if (patch.deskId !== undefined) {
      mutable.deskId = patch.deskId;
      mutable.objIndex = patch.deskId;
    }
    if (patch.equipmentId !== undefined) mutable.equipmentId = patch.equipmentId;
    if (patch.colleagueId !== undefined) mutable.colleagueId = patch.colleagueId;
    if (patch.frame !== undefined) mutable.frame = patch.frame;
    if (patch.talkFrame !== undefined) mutable.talkFrame = patch.talkFrame;
    this.record("configure-staff", staff, before);
    return staff;
  }

  public gotoDesk(staffId: number): boolean {
    const staff = this.requireStaff(staffId);
    return this.gotoDeskFor(staff);
  }

  public gotoEquip(staffId: number): boolean {
    const staff = this.requireStaff(staffId);
    return this.gotoEquipFor(staff);
  }

  public gotoTalk(staffId: number): boolean {
    const staff = this.requireStaff(staffId);
    return this.gotoTalkFor(staff);
  }

  public removeFurniture(instanceId: number): boolean {
    const furniture = findFurniture(this.roomState, instanceId);
    if (!furniture) return false;
    const affected = this.staffState.filter((staff) => staff.deskId === instanceId || staff.equipmentId === instanceId || furniture.reservedUserIds.includes(staff.id));
    removeRoomFurniture(this.roomState, instanceId);
    for (const staff of affected) {
      const mutable = mutableStaffFor(staff);
      const before = beforeState(staff);
      if (staff.equipmentId === instanceId) {
        mutable.equipmentId = -1;
        mutable.objIndex = -1;
        mutable.state = StaffState.WORK;
        releaseReservation(furniture, staff.id);
      }
      if (staff.deskId === instanceId) {
        mutable.deskId = -1;
        mutable.objIndex = -1;
        mutable.flags &= ~StaffFlag.SITTING;
        clearRoute(staff);
        mutable.state = StaffState.WANDER;
        mutable.moveMode = MoveMode.STAY;
      }
      this.record("furniture-destroy-cleanup", staff, before, null, "LC-6");
      if (staff.deskId < 0 && !staff.removed) this.gotoDeskFor(staff);
    }
    return true;
  }

  public startPlanning(): void {
    startPlanning(this.playerState, this.staffState);
    this.record("planning-start-player", null, {}, null, "C10");
    this.record("planning-start-room", null, {}, null, "C10");
    for (const staff of this.staffState) this.record("planning-start-staff", staff, {}, null, "C10");
  }

  public updatePlanning(elapsed: number): void {
    updatePlanning(this.playerState, this.staffState, elapsed);
    this.record("planning-update", null);
  }

  public endPlanning(completed = true): void {
    if (completed) endPlanning(this.playerState, this.staffState);
    this.record("planning-end-player-completion-predicate", null, {}, null, "C11");
    this.record("planning-end-room", null, {}, null, "C11");
    for (const staff of this.staffState) this.record("planning-end-staff", staff, {}, null, "C11");
  }

  public execute(command: LivingCommand): boolean {
    switch (command.type) {
      case "add_staff":
        this.addStaff(command.staffDataId ?? 0, command.staffId);
        return true;
      case "remove_furniture":
        return this.removeFurniture(command.furnitureInstanceId ?? -1);
      case "start_planning":
        this.startPlanning();
        return true;
      case "end_planning":
        this.endPlanning(true);
        return true;
      case "goto_equip":
        return this.gotoEquip(command.staffId ?? 0);
      case "goto_talk":
        return this.gotoTalk(command.staffId ?? 0);
      default:
        return false;
    }
  }

  public tick(): LivingSnapshot {
    this.tickFrame += 1;
    for (const staffId of [...this.roomState.staffIds]) {
      const staff = this.findStaff(staffId);
      if (!staff || staff.removed) continue;
      this.updateStaff(staff);
    }
    this.updateObjChips();
    return this.snapshot();
  }

  public runTicks(count: number): LivingSnapshot {
    if (!Number.isInteger(count) || count < 0) throw new Error("Living tick count must be a non-negative integer");
    let current = this.snapshot();
    for (let index = 0; index < count; index += 1) current = this.tick();
    return current;
  }

  public snapshot(): LivingSnapshot {
    return {
      frame: this.tickFrame,
      room: cloneRoom(this.roomState),
      staffs: this.staffState.map(cloneStaff),
      player: clonePlayer(this.playerState),
      traces: this.recorder.all(),
      rngDraws: this.rng.draws(),
      rngState: this.rng.state(),
      rngReplay: { appData: [...this.replayAppData], lib: [...this.replayLib] },
      meetingPointGauge: this.meetingGauge,
    };
  }

  private updateStaff(staff: LivingStaff): void {
    const before = beforeState(staff);
    this.record("staff-update-entry", staff, before, null, "BF-TICK-STAFF");
    this.updateRecovery(staff);
    this.record("recovery-before-low-hp", staff, before, null, "LC-2");
    if (this.getHpRatio(staff) <= 5 && staff.state !== StaffState.MOVE && staff.state !== StaffState.STAY_HOME) {
      this.gotoDoorFor(staff);
      this.incrementStaffFrame(staff);
      return;
    }
    if ((staff.flags & StaffFlag.INVITED) !== 0 && staff.state !== StaffState.MOVE && staff.state !== StaffState.TALK) {
      this.onInvitedTalk(staff);
    }
    switch (staff.state) {
      case StaffState.NORMAL:
        this.gotoDeskFor(staff);
        break;
      case StaffState.MOVE:
        this.updateMove(staff);
        break;
      case StaffState.WORK:
        this.updateWork(staff);
        break;
      case StaffState.USE_EQUIPMENT:
        this.updateUseEquip(staff);
        break;
      case StaffState.TALK:
        this.updateTalk(staff);
        break;
      case StaffState.INVITE_TO_TALK:
        this.updateInviteToTalk(staff);
        break;
      case StaffState.STAY_HOME:
        this.updateStayHome(staff);
        break;
      case StaffState.WAIT_BACK_OF_DOOR:
        this.gotoDeskFor(staff);
        break;
      default:
        break;
    }
    this.incrementStaffFrame(staff);
    this.record("staff-update-exit", staff, before, null, "BF-TICK-STAFF");
  }

  private updateRecovery(staff: LivingStaff): void {
    const mutable = mutableStaffFor(staff);
    if ((staff.flags & StaffFlag.SLEEPING) !== 0 && staff.frame >= 0 && staff.frame % 200 === 0) {
      const stock = Math.max(1, Math.floor((staff.maxHp * 5) / 100));
      mutable.recoveryStock += stock;
      mutable.frameToStartRecovery = 20;
      mutable.flags &= ~StaffFlag.SLEEPING;
      this.record("sleeping-recovery-stock", staff, {}, null, "LC-2");
    }
    if (staff.recoveryStock <= 0) return;
    if (staff.frameToStartRecovery > 0) {
      mutable.frameToStartRecovery -= 1;
      return;
    }
    if (staff.frame >= 0 && staff.frame % 3 === 0) {
      this.recoverHp(staff, 1);
      mutable.recoveryStock = Math.max(0, mutable.recoveryStock - 1);
      mutable.recoveryEffectFrame = 0;
      mutable.frameToHideHpGauge = 40;
      this.record("recovery-stock-consumed", staff, {}, null, "LC-2");
    }
  }

  private recoverHp(staff: LivingStaff, amount: number): void {
    const mutable = mutableStaffFor(staff);
    mutable.hp = Math.max(0, Math.min(staff.maxHp, staff.hp + Math.max(0, amount)));
  }

  private gotoDoorFor(staff: LivingStaff): boolean {
    const mutable = mutableStaffFor(staff);
    const before = beforeState(staff);
    const draw = this.rng.appRandom(101);
    this.record("low-hp-bubble-draw", staff, before, this.rng.draws().length - 1, "LC-1");
    if (draw > 100) return false;
    const door = findFurniture(this.roomState, -1);
    if (!door) return false;
    clearRoute(staff);
    mutable.state = StaffState.MOVE;
    mutable.moveMode = MoveMode.GO_TO_DOOR;
    mutable.objIndex = door.instanceId;
    mutable.goalCell = [door.cell[0], door.cell[1]];
    mutable.goalFlags = 0;
    const path = searchRoute(this.catalogs, staff.cell, door.cell, { goal: { cell: door.cell, allowOccupiedTarget: true } });
    mutable.route = path.slice(1).map(cloneCell);
    this.record("low-hp-go-to-door", staff, before, null, "LC-1");
    return true;
  }

  private gotoDeskFor(staff: LivingStaff): boolean {
    const mutable = mutableStaffFor(staff);
    const desk = findFurniture(this.roomState, staff.deskId) ?? findDesk(this.roomState);
    const before = beforeState(staff);
    if (!desk || desk.rawType !== ObjChipType.DESK || !desk.installed) {
      clearRoute(staff);
      mutable.state = StaffState.WANDER;
      mutable.moveMode = MoveMode.STAY;
      mutable.deskId = -1;
      mutable.objIndex = -1;
      this.record("goto-desk-invalid-fallback", staff, before, null, "LC-6");
      return false;
    }
    if (desk.ownerStaffId !== staff.id) {
      const mutableDesk = desk as unknown as { ownerStaffId: number };
      if (desk.ownerStaffId < 0) mutableDesk.ownerStaffId = staff.id;
      mutable.deskId = desk.instanceId;
      mutable.objIndex = desk.instanceId;
    }
    mutable.state = StaffState.MOVE;
    mutable.moveMode = MoveMode.GOTO_DESK;
    mutable.objIndex = desk.instanceId;
    if (staff.state === StaffState.WAIT_BACK_OF_DOOR) mutable.flags |= StaffFlag.FADE_IN;
    const route = searchRoute(this.catalogs, staff.cell, desk.cell, { goal: { cell: desk.cell, allowOccupiedTarget: true, goalType: GoalFlag.DESK } });
    mutable.route = route.slice(1).map(cloneCell);
    mutable.goalCell = [desk.cell[0], desk.cell[1]];
    mutable.goalFlags = GoalFlag.DESK;
    this.record("goto-desk", staff, before, null, "LC-4");
    return true;
  }

  private gotoEquipFor(staff: LivingStaff): boolean {
    const mutable = mutableStaffFor(staff);
    const before = beforeState(staff);
    const targetType = this.rng.appRandom(2) === 0 ? ObjChipType.EQUIPMENT : ObjChipType.BIG_CENTER;
    const candidates = findEquipment(this.roomState, targetType);
    if (candidates.length === 0) {
      this.record("equipment-no-candidate", staff, before, this.rng.draws().length - 1, "LC-2");
      return false;
    }
    const candidateIndex = this.rng.appRandom(candidates.length);
    const candidate = candidates[candidateIndex];
    if (!candidate || getUsersNum(candidate) > 0 || !reserveUse(candidate, staff.id)) {
      this.record("equipment-reservation-rejected", staff, before, this.rng.draws().length - 1, "LC-2");
      return false;
    }
    mutable.equipmentId = candidate.instanceId;
    mutable.objIndex = candidate.instanceId;
    mutable.state = StaffState.MOVE;
    mutable.moveMode = MoveMode.GOTO_EQUIPMENT;
    const route = searchRoute(this.catalogs, staff.cell, candidate.cell, { goal: { cell: candidate.cell, allowOccupiedTarget: true, goalType: GoalFlag.EQUIPMENT } });
    mutable.route = route.slice(1).map(cloneCell);
    mutable.goalCell = [candidate.cell[0], candidate.cell[1]];
    mutable.goalFlags = GoalFlag.EQUIPMENT;
    this.record("equipment-reserved", staff, before, this.rng.draws().length - 1, "LC-2");
    return true;
  }

  private gotoTalkFor(staff: LivingStaff): boolean {
    const mutable = mutableStaffFor(staff);
    const before = beforeState(staff);
    if (this.staffState.length <= 1) return false;
    const candidateIndex = this.rng.appRandom(this.staffState.length);
    const target = this.staffState[candidateIndex];
    if (!target || target.id === staff.id || target.state !== StaffState.WORK || (target.flags & StaffFlag.SITTING) === 0 || (target.flags & 0x840) !== 0 || (target.flags & 6) !== 2) {
      this.record("talk-candidate-rejected", staff, before, this.rng.draws().length - 1, "BF-TALK");
      return false;
    }
    const targetDesk = findFurniture(this.roomState, target.deskId);
    if (!targetDesk || targetDesk.rawType === ObjChipType.OUTDOOR) {
      this.record("talk-candidate-invalid-standing-cell", staff, before, this.rng.draws().length - 1, "BF-TALK");
      return false;
    }
    const mutableTarget = mutableStaffFor(target);
    mutable.flags |= StaffFlag.RESERVED_TALK;
    mutableTarget.flags |= StaffFlag.RESERVED_TALK | StaffFlag.INVITED;
    mutable.colleagueId = target.id;
    mutableTarget.colleagueId = staff.id;
    mutable.state = StaffState.MOVE;
    mutable.moveMode = MoveMode.TO_STAFF;
    const route = searchRoute(this.catalogs, staff.cell, target.cell, { goal: { cell: target.cell, allowOccupiedTarget: true, goalType: GoalFlag.STAFF } });
    mutable.route = route.slice(1).map(cloneCell);
    mutable.goalCell = [target.cell[0], target.cell[1]];
    mutable.goalFlags = GoalFlag.STAFF;
    this.record("talk-reserved-bilateral", staff, before, this.rng.draws().length - 1, "BF-TALK");
    this.record("talk-invited-target", target, { flags: target.flags ^ StaffFlag.INVITED }, null, "BF-TALK");
    return true;
  }

  private updateMove(staff: LivingStaff): void {
    if (staff.route.length === 0) {
      this.handleArrival(staff);
      return;
    }
    const before = beforeState(staff);
    const arrived = onArriveNextNode(staff, this.catalogs);
    this.record("route-head-consumed", staff, before, null, "BF-ARRIVAL");
    if (arrived) this.handleArrival(staff);
  }

  private handleArrival(staff: LivingStaff): void {
    const mutable = mutableStaffFor(staff);
    const mode = staff.moveMode;
    const before = beforeState(staff);
    clearRoute(staff);
    this.record(`on-arrive-goal-mode-${mode}`, staff, { ...before, moveMode: mode }, null, "LC-4");
    switch (mode) {
      case MoveMode.GOTO_EQUIPMENT:
        mutable.frame = 0;
        mutable.state = StaffState.USE_EQUIPMENT;
        mutable.moveMode = MoveMode.STAY;
        break;
      case MoveMode.WANDER:
        mutable.frame = 0;
        mutable.state = StaffState.WANDER;
        mutable.moveMode = MoveMode.STAY;
        break;
      case MoveMode.GOTO_DESK:
        mutable.frame = 0;
        mutable.moveMode = MoveMode.SIT_DOWN;
        break;
      case MoveMode.INTO_EQUIPMENT:
        mutable.frame = 0;
        mutable.state = StaffState.INVITE_TO_TALK;
        mutable.moveMode = MoveMode.STAY;
        break;
      case MoveMode.OUTOF_EQUIPMENT:
        mutable.frame = 0;
        mutable.moveMode = MoveMode.STAY;
        break;
      case MoveMode.SIT_DOWN:
        mutable.frame = 0;
        mutable.state = StaffState.WORK;
        mutable.flags |= StaffFlag.SITTING;
        mutable.moveMode = MoveMode.STAY;
        break;
      case MoveMode.TO_STAFF: {
        const target = this.findStaff(staff.colleagueId);
        mutable.moveMode = MoveMode.TO_BACK_OF_CHAIR;
        if (target) {
          const route = searchRoute(this.catalogs, staff.cell, target.cell, { goal: { cell: target.cell, allowOccupiedTarget: true, goalType: GoalFlag.STAFF } });
          mutable.route = route.slice(1).map(cloneCell);
          mutable.goalCell = cloneCell(target.cell);
          mutable.goalFlags = GoalFlag.STAFF;
        }
        break;
      }
      case MoveMode.TO_STAND_TALKING:
        mutable.frame = 0;
        mutable.state = StaffState.TALK;
        mutable.moveMode = MoveMode.STAY;
        mutable.talkFrame = 0;
        break;
      case MoveMode.TO_BACK_OF_CHAIR:
        mutable.frame = 0;
        mutable.state = StaffState.INVITE_TO_TALK;
        mutable.moveMode = MoveMode.STAY;
        break;
      case MoveMode.GO_TO_DOOR: {
        const door = findFurniture(this.roomState, -1);
        if (door) {
          reserveUse(door, staff.id);
          const mutableDoor = door as unknown as { actionStarted: boolean; actionId: number; useFrame: number };
          mutableDoor.actionStarted = true;
          mutableDoor.actionId = 0;
          mutableDoor.useFrame = 15;
          mutable.moveMode = MoveMode.GO_HOME;
          mutable.state = StaffState.MOVE;
          mutable.objIndex = door.instanceId;
          mutable.goalCell = cloneCell(door.cell);
        }
        mutable.flags |= StaffFlag.FADE_OUT;
        break;
      }
      case MoveMode.GO_HOME:
        mutable.frame = 0;
        mutable.state = StaffState.STAY_HOME;
        mutable.moveMode = MoveMode.STAY;
        break;
      default:
        this.gotoDeskFor(staff);
        break;
    }
    this.record(`on-arrive-goal-applied-${mode}`, staff, before, null, "LC-4");
  }

  private updateWork(staff: LivingStaff): void {
    const mutable = mutableStaffFor(staff);
    if ((staff.flags & StaffFlag.SITTING) === 0) {
      this.gotoDeskFor(staff);
      return;
    }
    if (staff.frame < 0 || staff.frame % 20 !== 0) return;
    if ((staff.flags & 0x20860) === 0 && (staff.flags & StaffFlag.TYPING) === 0) {
      const typingDraw = this.rng.appRandom(101);
      this.record("work-typing-gate", staff, {}, this.rng.draws().length - 1, "BF-AUTONOMY");
      if (typingDraw < 41) {
        mutable.flags |= StaffFlag.TYPING;
        mutable.typingFrame = 0;
        const bubbleDraw = this.rng.appRandom(101);
        this.record("work-typing-bubble", staff, {}, this.rng.draws().length - 1, "BF-AUTONOMY");
        if (bubbleDraw <= 50) this.record("work-typing-visual-event", staff, {}, null, "BF-AUTONOMY");
        return;
      }
    }
    if ((staff.flags & StaffFlag.TYPING) !== 0) {
      mutable.typingFrame += 1;
      if (mutable.typingFrame >= 3) mutable.flags &= ~StaffFlag.TYPING;
      return;
    }
    if (this.getHpRatio(staff) <= 99) {
      const sleepDraw = this.rng.appRandom(101);
      this.record("work-sleep-gate", staff, {}, this.rng.draws().length - 1, "BF-AUTONOMY");
      if (sleepDraw <= 25) {
        mutable.flags |= StaffFlag.SLEEPING;
        this.record("work-sleep-selected", staff, {}, null, "BF-AUTONOMY");
        return;
      }
    }
    if ((staff.flags & 0x14) === 0) {
      const equipmentDraw = this.rng.appRandom(101);
      this.record("work-equipment-gate", staff, {}, this.rng.draws().length - 1, "BF-AUTONOMY");
      if (equipmentDraw < 21) {
        this.gotoEquipFor(staff);
        return;
      }
    }
    if ((staff.flags & 0x14) === 0) {
      const talkDraw = this.rng.appRandom(101);
      this.record("work-talk-gate", staff, {}, this.rng.draws().length - 1, "BF-AUTONOMY");
      if (talkDraw <= 10) this.gotoTalkFor(staff);
    }
  }

  private updateUseEquip(staff: LivingStaff): void {
    const mutable = mutableStaffFor(staff);
    const equipment = findFurniture(this.roomState, staff.equipmentId);
    if (!equipment || equipment.removed) {
      mutable.equipmentId = -1;
      this.gotoDeskFor(staff);
      return;
    }
    const equipmentMutable = equipment as unknown as { useFrame: number };
    equipmentMutable.useFrame = staff.frame;
    if (staff.frame < 20) return;
    if (staff.frame === 20) this.record("equipment-action-facing", staff, {}, null, "LC-2");
    if (staff.frame === 40 && !equipment.actionStarted) {
      startAction(equipment, staff.id);
      mutable.actionId = 0;
      this.record("equipment-start-action", staff, {}, null, "LC-2");
    }
    if (staff.frame >= 60) this.record("equipment-action-complete-phase", staff, {}, null, "LC-2");
    if (staff.frame < 70) return;
    const recovery = furnitureRecovery(this.catalogs, equipment.furnitureDataId ?? -1);
    completeAction(equipment, staff.id);
    if (staff.hp < staff.maxHp && recovery >= 1) {
      mutable.frameToStartRecovery = 20;
      mutable.recoveryStock += recovery;
      this.record("equipment-recovery-stock-added", staff, {}, null, "LC-2");
    }
    mutable.equipmentId = -1;
    mutable.objIndex = -1;
    mutable.state = StaffState.MOVE;
    mutable.moveMode = MoveMode.GOTO_DESK;
    this.gotoDeskFor(staff);
    this.record("equipment-complete-release-return", staff, {}, null, "LC-2");
  }

  private updateInviteToTalk(staff: LivingStaff): void {
    const mutable = mutableStaffFor(staff);
    const target = this.findStaff(staff.colleagueId);
    if (!target) {
      this.cleanupTalk(staff);
      return;
    }
    mutable.state = StaffState.MOVE;
    mutable.moveMode = MoveMode.TO_STAND_TALKING;
    const route = searchRoute(this.catalogs, staff.cell, target.cell, { goal: { cell: target.cell, allowOccupiedTarget: true, goalType: GoalFlag.STAFF } });
    mutable.route = route.slice(1).map(cloneCell);
    mutable.goalCell = cloneCell(target.cell);
    mutable.goalFlags = GoalFlag.STAFF;
    this.record("talk-invite-accepted", staff, {}, null, "BF-TALK");
  }

  private onInvitedTalk(staff: LivingStaff): void {
    const mutable = mutableStaffFor(staff);
    const inviter = this.findStaff(staff.colleagueId);
    if (!inviter) {
      mutable.flags &= ~StaffFlag.INVITED;
      return;
    }
    const before = beforeState(staff);
    mutable.state = StaffState.MOVE;
    mutable.objIndex = inviter.deskId;
    mutable.moveMode = MoveMode.TO_STAND_TALKING;
    const route = searchRoute(this.catalogs, staff.cell, inviter.cell, { goal: { cell: inviter.cell, allowOccupiedTarget: true, goalType: GoalFlag.STAFF } });
    mutable.route = route.slice(1).map(cloneCell);
    mutable.goalCell = cloneCell(inviter.cell);
    mutable.goalFlags = GoalFlag.STAFF;
    this.record("on-invited-talk", staff, before, null, "BF-TALK");
  }

  private updateTalk(staff: LivingStaff): void {
    const mutable = mutableStaffFor(staff);
    mutable.talkFrame = staff.frame;
    if (staff.frame === 20 && (staff.flags & StaffFlag.INVITED) === 0) {
      const draw = this.rng.appRandom(101);
      this.record("talk-frame-20-bubble", staff, {}, this.rng.draws().length - 1, "BF-TALK");
      if (draw <= 100) this.record("talk-frame-20-visual-event", staff, {}, null, "BF-TALK");
    }
    if (staff.frame === 70 && (staff.flags & StaffFlag.INVITED) !== 0) {
      const draw = this.rng.appRandom(101);
      this.record("talk-frame-70-bubble", staff, {}, this.rng.draws().length - 1, "BF-TALK");
      if (draw <= 100) this.record("talk-frame-70-visual-event", staff, {}, null, "BF-TALK");
    }
    if (staff.frame === 110) {
      const gauge = this.rng.libRandomInclusive(0, 4);
      this.meetingGauge += gauge;
      mutable.meetingPointGauge += gauge;
      this.record("talk-frame-110-meeting-point", staff, {}, this.rng.draws().length - 1, "BF-TALK");
    }
    if (staff.frame < 130) return;
    this.cleanupTalk(staff);
  }

  private cleanupTalk(staff: LivingStaff): void {
    const colleague = this.findStaff(staff.colleagueId);
    const mutable = mutableStaffFor(staff);
    const before = beforeState(staff);
    mutable.flags &= ~(StaffFlag.INVITED | StaffFlag.RESERVED_TALK);
    mutable.colleagueId = -1;
    mutable.talkFrame = 0;
    if (colleague) {
      const mutableColleague = mutableStaffFor(colleague);
      mutableColleague.flags &= ~(StaffFlag.INVITED | StaffFlag.RESERVED_TALK);
      mutableColleague.colleagueId = -1;
      mutableColleague.talkFrame = 0;
      if (colleague.state === StaffState.TALK || colleague.state === StaffState.INVITE_TO_TALK) this.gotoDeskFor(colleague);
    }
    this.gotoDeskFor(staff);
    this.record("talk-cleanup-return", staff, before, null, "BF-TALK");
  }

  private updateStayHome(staff: LivingStaff): void {
    this.recoverHp(staff, 1);
    this.record("stay-home-recover", staff, {}, null, "LC-1");
    if (this.getHpRatio(staff) < 40) return;
    const door = findFurniture(this.roomState, -1);
    if (door) releaseReservation(door, staff.id);
    const mutable = mutableStaffFor(staff);
    mutable.state = StaffState.WAIT_BACK_OF_DOOR;
    mutable.moveMode = MoveMode.GOTO_DESK;
    mutable.flags |= StaffFlag.FADE_IN;
    this.record("stay-home-return-threshold", staff, {}, null, "LC-1");
    this.gotoDeskFor(staff);
  }

  private updateObjChips(): void {
    for (const furniture of this.roomState.furniture) {
      if (furniture.actionStarted) {
        const mutable = furniture as unknown as { useFrame: number };
        mutable.useFrame += 1;
      }
    }
  }

  private incrementStaffFrame(staff: LivingStaff): void {
    const mutable = mutableStaffFor(staff);
    mutable.frame += 1;
    mutable.moveFrame += 1;
  }

  private getHpRatio(staff: LivingStaff): number {
    return Math.trunc((staff.hp * 100) / Math.max(1, staff.maxHp));
  }

  private findStaff(id: number): LivingStaff | null {
    return this.staffState.find((staff) => staff.id === id) ?? null;
  }

  private requireStaff(id: number): LivingStaff {
    const staff = this.findStaff(id);
    if (!staff) throw new Error(`Living Staff:${id} is missing`);
    return staff;
  }

  private record(
    event: string | null,
    staff: LivingStaff | null | undefined,
    before: Partial<LivingStaff> = {},
    rngSequence: number | null = null,
    evidenceContractId = "LC-6",
  ): void {
    if (event === null) return;
    this.recorder.record(this.tickFrame, event, staff ?? null, before, rngSequence, evidenceContractId);
  }
}

function mutableStaffFor(staff: LivingStaff): MutableStaff {
  return mutableStaff(staff);
}

export function createLivingRuntime(catalogs: RuntimeCatalogs, options: LivingRuntimeOptions = {}): LivingRuntime {
  return new LivingRuntime(catalogs, options);
}

export function createLivingRuntimeFromSnapshot(catalogs: RuntimeCatalogs, snapshot: LivingSnapshot): LivingRuntime {
  return LivingRuntime.fromSnapshot(catalogs, snapshot);
}
