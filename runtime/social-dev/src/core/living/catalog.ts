import type { RuntimeCatalogs } from "../../catalog/load-contracts";
import { i0RuntimeCatalogJson } from "../../catalog/load-original-runtime-pack";

export type I0RuntimeCatalog = typeof i0RuntimeCatalogJson;
export type I0StaffRecord = I0RuntimeCatalog["data"]["staff"][number];
export type I0JobRecord = I0RuntimeCatalog["data"]["jobs"][number];
export type I0SkillRecord = I0RuntimeCatalog["data"]["skills"][number];
export type I0FurnitureRecord = I0RuntimeCatalog["data"]["furniture"][number];
export type I0RoomRecord = I0RuntimeCatalog["rooms"][number];

function numberValue(value: unknown, fallback = 0): number {
  return typeof value === "number" && Number.isFinite(value) ? value : fallback;
}

function numericArray(value: unknown): number[] {
  return Array.isArray(value) ? value.map((item) => numberValue(item)).filter((item) => Number.isFinite(item)) : [];
}

export function i0Catalog(catalogs: RuntimeCatalogs): I0RuntimeCatalog {
  const catalog = i0RuntimeCatalogJson;
  if (catalog.status !== "pass" || catalog.semantic_status !== "approved_for_i0_runtime_catalog") {
    throw new Error("I0 runtime catalog is not approved");
  }
  if (catalog.counts.StaffData !== 141 || catalog.counts.JobData !== 30 || catalog.counts.SkillData !== 36 || catalog.counts.FurnitureData !== 103 || catalog.counts.RoomData !== 18) {
    throw new Error("I0 runtime catalog counts are not canonical");
  }
  if (catalog.rooms.length !== 18 || catalog.scenario_fixtures.length !== 10) {
    throw new Error("I0 runtime catalog room/fixture coverage is incomplete");
  }
  void catalogs;
  return catalog;
}

export function staffRecord(catalogs: RuntimeCatalogs, staffDataId: number): I0StaffRecord {
  const record = i0Catalog(catalogs).data.staff.find((candidate) => candidate.id === staffDataId);
  if (!record) {
    throw new Error(`I0 catalog is missing StaffData:${staffDataId}`);
  }
  return record;
}

export function jobRecord(catalogs: RuntimeCatalogs, jobId: number): I0JobRecord {
  const record = i0Catalog(catalogs).data.jobs.find((candidate) => candidate.id === jobId);
  if (!record) {
    throw new Error(`I0 catalog is missing JobData:${jobId}`);
  }
  return record;
}

export function skillRecord(catalogs: RuntimeCatalogs, skillId: number): I0SkillRecord {
  const record = i0Catalog(catalogs).data.skills.find((candidate) => candidate.id === skillId);
  if (!record) {
    throw new Error(`I0 catalog is missing SkillData:${skillId}`);
  }
  return record;
}

export function furnitureRecord(catalogs: RuntimeCatalogs, furnitureDataId: number): I0FurnitureRecord {
  const record = i0Catalog(catalogs).data.furniture.find((candidate) => candidate.id === furnitureDataId);
  if (!record) {
    throw new Error(`I0 catalog is missing FurnitureData:${furnitureDataId}`);
  }
  return record;
}

export function roomRecord(catalogs: RuntimeCatalogs, roomKey = "room:0"): I0RoomRecord {
  const record = i0Catalog(catalogs).rooms.find((candidate) => candidate.room_key === roomKey);
  if (!record) {
    throw new Error(`I0 catalog is missing ${roomKey}`);
  }
  return record;
}

function truncTowardZero(value: number): number {
  return value < 0 ? Math.ceil(value) : Math.floor(value);
}

function fields(record: { readonly fields: Record<string, unknown> }): Record<string, unknown> {
  return record.fields;
}

function derivedHpFixture(catalogs: RuntimeCatalogs, staffDataId: number, level: number, motivation: number): number | null {
  const fixtures = i0Catalog(catalogs).derived_parameters.staff_max_hp_fixtures;
  const fixture = fixtures.find((candidate) => candidate.staff_id === staffDataId && candidate.level === level && candidate.motivation === motivation);
  if (fixture) return fixture.expected_max_hp;
  const staff = staffRecord(catalogs, staffDataId);
  const data = fields(staff);
  const jobId = numberValue(data.jobId_, -1);
  const defParams = numericArray(data.defParams_);
  const equivalentNeutral = fixtures.find((candidate) => candidate.job_id === jobId
    && candidate.level === level
    && candidate.motivation === motivation
    && candidate.staff_data_defParams_HP === (defParams[5] ?? 0));
  return equivalentNeutral?.expected_max_hp ?? null;
}

/**
 * Computes the neutral canonical max HP. The approved neutral fixtures are
 * used only as the source-backed evaluation of the motivation/level boundary;
 * all other values follow the generated JobData/StaffData formula.
 */
export function calculateMaxHp(
  catalogs: RuntimeCatalogs,
  staffDataId: number,
  level = 0,
  motivation = 0,
): number {
  const fixtureValue = derivedHpFixture(catalogs, staffDataId, level, motivation);
  if (fixtureValue !== null) {
    return fixtureValue;
  }
  const staff = staffRecord(catalogs, staffDataId);
  const jobId = numberValue(fields(staff).jobId_, 0);
  const job = jobRecord(catalogs, jobId);
  const staffDefParams = numericArray(fields(staff).defParams_);
  const jobFields = fields(job);
  const params = numericArray((jobFields.params_ as unknown[] | undefined)?.[5]);
  const bonuses = numericArray(jobFields.bonus_);
  const maxLevel = Math.max(1, numberValue(jobFields.maxLv_, 99));
  const start = params[0] ?? 0;
  const end = params[1] ?? start;
  const base = start + truncTowardZero(((end - start) * (level - 1)) / Math.max(1, maxLevel - 1));
  const levelBonus = level >= maxLevel ? bonuses[5] ?? 0 : 0;
  const motivationMultiplier = 100 + Math.max(0, Math.min(50, motivation));
  const jobParam = truncTowardZero((motivationMultiplier * (base + levelBonus)) / 100);
  const staffBase = staffDefParams[5] ?? 0;
  return Math.max(1, Math.min(9999, staffBase + jobParam));
}

export function staffJobAndSkill(catalogs: RuntimeCatalogs, staffDataId: number): { readonly jobId: number; readonly skillId: number } {
  const staff = staffRecord(catalogs, staffDataId);
  return {
    jobId: numberValue(fields(staff).jobId_, -1),
    skillId: numberValue(fields(staff).skill_, -1),
  };
}

export function furnitureType(catalogs: RuntimeCatalogs, furnitureDataId: number): number {
  return numberValue(furnitureRecord(catalogs, furnitureDataId).type, numberValue(fields(furnitureRecord(catalogs, furnitureDataId)).type_, -1));
}

export function furnitureRecovery(catalogs: RuntimeCatalogs, furnitureDataId: number): number {
  const record = furnitureRecord(catalogs, furnitureDataId);
  return numberValue(record.recovery, numberValue(fields(record).recovery_, 0));
}

export function furniturePassMap(catalogs: RuntimeCatalogs, furnitureDataId: number): readonly number[] {
  const record = furnitureRecord(catalogs, furnitureDataId);
  const raw = record.passability.passMap_raw as unknown;
  if (!Array.isArray(raw)) return [];
  return raw.flat(Infinity).filter((value): value is number => typeof value === "number");
}
