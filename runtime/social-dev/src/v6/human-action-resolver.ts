import type {
  CharacterActionCapability,
  CharacterCapabilityProfile,
  CharacterCapabilitySelector,
} from "../catalog/types";
import type { HumanDirection, StaffAction, StaffSelectorResolution } from "./contracts";
import type { StaffFixtureCatalog } from "./fixture-loader";

const DIRECTIONS: readonly HumanDirection[] = ["right", "left", "up", "down"];
const DIRECTION_BY_REVERSE: Readonly<Record<number, HumanDirection>> = {
  0: "right",
  1: "left",
  2: "up",
  3: "down",
};

export interface HumanDirectionInput {
  readonly direction?: HumanDirection;
  readonly rawDirection?: number;
}

export function resolveHumanDirection(
  input: HumanDirectionInput,
  catalog: StaffFixtureCatalog,
): { readonly direction: HumanDirection; readonly rawDirection: number | null; readonly reverseDirection: number | null } {
  if (input.rawDirection !== undefined) {
    const raw = catalog.direction.raw_values[String(input.rawDirection)];
    if (raw === undefined) {
      throw new Error(`V6 native raw direction ${input.rawDirection} is outside the closed 0..3 domain`);
    }
    const direction = DIRECTION_BY_REVERSE[raw.reverse];
    if (direction === undefined) {
      throw new Error(`V6 native reverse direction ${raw.reverse} has no human direction label`);
    }
    return { direction, rawDirection: input.rawDirection, reverseDirection: raw.reverse };
  }
  const direction = input.direction ?? "right";
  if (!DIRECTIONS.includes(direction)) {
    throw new Error(`V6 human direction ${direction} is unsupported`);
  }
  return {
    direction,
    rawDirection: null,
    reverseDirection: DIRECTIONS.indexOf(direction),
  };
}

export function resolveHumanAction(
  action: StaffAction | string,
  directionInput: HumanDirectionInput,
  catalog: StaffFixtureCatalog,
): StaffSelectorResolution {
  const profile = requireHumanStaffProfile(catalog);
  const direction = resolveHumanDirection(directionInput, catalog);
  return resolveActionRecord(profile, action, direction, catalog, new Set<string>());
}

function resolveActionRecord(
  profile: CharacterCapabilityProfile,
  action: string,
  direction: ReturnType<typeof resolveHumanDirection>,
  catalog: StaffFixtureCatalog,
  visited: Set<string>,
): StaffSelectorResolution {
  if (visited.has(action)) {
    return unresolved(action, direction, "V6 action fallback cycle");
  }
  visited.add(action);
  const record = profile.actions[action] ?? profile.native_actions?.[action];
  if (record === undefined) {
    return unresolved(action, direction, "No closed human capability action");
  }
  const selector = selectForDirection(record, direction.direction);
  if (selector !== null) {
    const fallback = record.fallback_action ?? null;
    const sourceAction = record.source_action ?? null;
    return {
      action,
      sourceAction,
      fallbackAction: fallback,
      direction: direction.direction,
      rawDirection: direction.rawDirection,
      reverseDirection: direction.reverseDirection,
      selectorId: selector.selector_id,
      selectorFilename: selector.filename,
      status: record.status === "fallback_ready" ? "fallback" : "resolved",
      proof: record.status === "native_selector_ready" || record.status === "selector_ready"
        ? "SOURCE-DATA-PROVEN"
        : "STATIC-INFERRED",
      note: record.note ?? null,
    };
  }
  if (record.fallback_action !== undefined) {
    const fallback = resolveActionRecord(profile, record.fallback_action, direction, catalog, visited);
    return {
      ...fallback,
      action,
      sourceAction: record.source_action ?? fallback.sourceAction,
      fallbackAction: record.fallback_action,
      status: fallback.selectorId === null ? fallback.status : "fallback",
      note: record.note ?? fallback.note,
    };
  }
  const status = record.status === "deferred" ? "deferred" : "unsupported";
  return {
    action,
    sourceAction: record.source_action ?? null,
    fallbackAction: null,
    direction: direction.direction,
    rawDirection: direction.rawDirection,
    reverseDirection: direction.reverseDirection,
    selectorId: null,
    selectorFilename: null,
    status,
    proof: record.status === "deferred" ? "SOURCE-LIMITED" : "STATIC-INFERRED",
    note: record.note ?? "No directional selector is closed for this action.",
  };
}

function selectForDirection(record: CharacterActionCapability, direction: HumanDirection): CharacterCapabilitySelector | null {
  const byDirection = record.selector_by_direction;
  if (byDirection !== undefined && byDirection !== null) {
    return byDirection[direction] ?? null;
  }
  return record.selector ?? null;
}

function requireHumanStaffProfile(catalog: StaffFixtureCatalog): CharacterCapabilityProfile {
  const profile = catalog.capability.profiles.find((candidate) => candidate.id === "human-staff-v1");
  if (profile === undefined) {
    throw new Error("V6 human-staff-v1 capability profile is missing");
  }
  return profile;
}

function unresolved(
  action: string,
  direction: ReturnType<typeof resolveHumanDirection>,
  note: string,
): StaffSelectorResolution {
  return {
    action,
    sourceAction: null,
    fallbackAction: null,
    direction: direction.direction,
    rawDirection: direction.rawDirection,
    reverseDirection: direction.reverseDirection,
    selectorId: null,
    selectorFilename: null,
    status: "unsupported",
    proof: "STATIC-INFERRED",
    note,
  };
}
