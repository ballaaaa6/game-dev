import type { LivingSnapshot } from "../../core/living/types";
import type { AssignmentAdapterSnapshot, DashboardReadModel } from "./types";

export function stableStringify(value: unknown): string {
  if (value === null || typeof value !== "object") return JSON.stringify(value);
  if (Array.isArray(value)) return `[${value.map((entry) => stableStringify(entry)).join(",")}]`;
  const record = value as Record<string, unknown>;
  return `{${Object.keys(record).sort().map((key) => `${JSON.stringify(key)}:${stableStringify(record[key])}`).join(",")}}`;
}

/** Deterministic non-wall-clock digest for acceptance replay comparisons. */
export function assignmentDigest(value: unknown): string {
  const input = stableStringify(value);
  let hash = 14695981039346656037n;
  const mask = 0xffffffffffffffffn;
  for (let index = 0; index < input.length; index += 1) {
    hash ^= BigInt(input.charCodeAt(index));
    hash = (hash * 1099511628211n) & mask;
  }
  return hash.toString(16).padStart(16, "0");
}

export function assignmentReplayDigest(
  adapter: AssignmentAdapterSnapshot,
  dashboard: DashboardReadModel,
  living: LivingSnapshot,
): string {
  return assignmentDigest({ adapter, dashboard, living });
}
