import type { RngDraw } from "./types";

export interface ReplayRngOptions {
  readonly appData?: readonly number[];
  readonly lib?: readonly number[];
  readonly seed?: number;
  readonly appDataIndex?: number;
  readonly libIndex?: number;
  readonly fallbackState?: number;
  readonly previousDraws?: readonly RngDraw[];
}

export interface RngState {
  readonly appDataIndex: number;
  readonly libIndex: number;
  readonly fallbackState: number;
}

/** Injectable equivalent of the two native random APIs. */
export class ReplayRng {
  private readonly appData: readonly number[];
  private readonly lib: readonly number[];
  private appDataIndex: number;
  private libIndex: number;
  private fallbackState: number;
  private readonly drawLog: RngDraw[];

  public constructor(options: ReplayRngOptions = {}) {
    this.appData = options.appData ?? [];
    this.lib = options.lib ?? [];
    this.appDataIndex = options.appDataIndex ?? 0;
    this.libIndex = options.libIndex ?? 0;
    this.fallbackState = (options.fallbackState ?? options.seed ?? 0x6d2b79f5) >>> 0;
    this.drawLog = [...(options.previousDraws ?? [])];
  }

  public appRandom(maxExclusive: number): number {
    if (!Number.isInteger(maxExclusive) || maxExclusive <= 0) {
      throw new Error(`AppData.Random requires n > 0, received ${maxExclusive}`);
    }
    const value = this.next("AppData", "AppData.Random(int)", 0, maxExclusive, true);
    if (value < 0 || value >= maxExclusive) {
      throw new Error(`Replay AppData.Random(${maxExclusive}) value ${value} is outside [0,${maxExclusive})`);
    }
    return value;
  }

  public appRandomInclusive(min: number, max: number): number {
    if (!Number.isInteger(min) || !Number.isInteger(max) || min > max) {
      throw new Error(`AppData.Random inclusive range is invalid: ${min},${max}`);
    }
    const value = this.next("AppData", "AppData.Random(int,int)", min, max, false);
    if (value < min || value > max) {
      throw new Error(`Replay AppData.Random(${min},${max}) value ${value} is outside inclusive range`);
    }
    return value;
  }

  public libRandomInclusive(min: number, max: number): number {
    if (!Number.isInteger(min) || !Number.isInteger(max) || min > max) {
      throw new Error(`Lib.Random inclusive range is invalid: ${min},${max}`);
    }
    const value = this.next("Lib", "Lib.Random(int,int)", min, max, false);
    if (value < min || value > max) {
      throw new Error(`Replay Lib.Random(${min},${max}) value ${value} is outside inclusive range`);
    }
    return value;
  }

  public draws(): readonly RngDraw[] {
    return this.drawLog.map((draw) => ({ ...draw }));
  }

  public state(): RngState {
    return {
      appDataIndex: this.appDataIndex,
      libIndex: this.libIndex,
      fallbackState: this.fallbackState >>> 0,
    };
  }

  private next(
    stream: "AppData" | "Lib",
    method: string,
    min: number,
    max: number,
    exclusiveMax: boolean,
  ): number {
    const sequence = this.drawLog.length;
    const source = stream === "AppData" ? this.appData : this.lib;
    const sourceIndex = stream === "AppData" ? this.appDataIndex : this.libIndex;
    let value: number;
    if (sourceIndex < source.length) {
      value = source[sourceIndex] ?? 0;
      if (stream === "AppData") this.appDataIndex += 1;
      else this.libIndex += 1;
    } else {
      const width = exclusiveMax ? max - min : max - min + 1;
      value = min + (this.nextFallback() % width);
    }
    this.drawLog.push({
      sequence,
      stream,
      method,
      min,
      max,
      exclusiveMax,
      value,
    });
    return value;
  }

  private nextFallback(): number {
    let x = this.fallbackState >>> 0;
    x ^= x << 13;
    x ^= x >>> 17;
    x ^= x << 5;
    this.fallbackState = x >>> 0;
    return this.fallbackState;
  }
}

export function createRngFromSnapshot(
  state: RngState,
  previousDraws: readonly RngDraw[],
  options: Pick<ReplayRngOptions, "appData" | "lib"> = {},
): ReplayRng {
  return new ReplayRng({
    ...options,
    ...state,
    previousDraws,
  });
}
