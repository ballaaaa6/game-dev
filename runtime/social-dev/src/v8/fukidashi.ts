import {
  V8_ENGLISH_FUKIDASHI,
  V8_FUKIDASHI_LIFETIME,
  V8_FUKIDASHI_OFFSET_Y,
  type V8FukidashiPayload,
  type V8VisualRngDraw,
} from "./contracts";

export interface V8RandomSource {
  readonly draws: readonly V8VisualRngDraw[];
  random(maxExclusive: number): number;
}

export function selectFukidashiId(
  pool: readonly number[],
  random: V8RandomSource,
  method = "AppData.Random(pool.length)",
): number {
  if (pool.length === 0) throw new Error("V8 Fukidashi pool cannot be empty");
  const index = random.random(pool.length);
  const id = pool[index];
  if (id === undefined) throw new Error(`V8 Fukidashi pool selection failed: ${method}`);
  return id;
}

export function createFukidashi(
  id: number,
  source: V8FukidashiPayload["source"],
  delay = 0,
  offsetY = V8_FUKIDASHI_OFFSET_Y,
): V8FukidashiPayload {
  const text = V8_ENGLISH_FUKIDASHI[id];
  if (!text) throw new Error(`V8 English Fukidashi localization is missing id ${id}`);
  return {
    id,
    lifetime: V8_FUKIDASHI_LIFETIME,
    delay,
    offsetY,
    text,
    source,
  };
}

/** Source order: delay first, lifetime only begins decrementing at delay <= 0. */
export function updateFukidashi(payload: V8FukidashiPayload | null): V8FukidashiPayload | null {
  if (!payload) return null;
  const nextDelay = payload.delay - 1;
  if (nextDelay > 0) {
    return { ...payload, delay: nextDelay };
  }
  return {
    ...payload,
    delay: 0,
    lifetime: payload.lifetime - 1,
  };
}

export function isDrawableFukidashi(payload: V8FukidashiPayload | null): payload is V8FukidashiPayload {
  return Boolean(payload && payload.lifetime >= 1 && payload.delay <= 0);
}

export function cloneFukidashi(payload: V8FukidashiPayload | null): V8FukidashiPayload | null {
  return payload ? { ...payload } : null;
}
