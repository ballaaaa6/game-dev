import type { SebContract } from "../v1/contracts";

export interface V3ImageIndexEntry {
  readonly id: number;
  readonly filename: string;
  readonly flags: readonly string[];
  readonly raw_record: string;
  readonly source_index_member: string;
  readonly source_member: string;
  readonly source_sha256: string | null;
  readonly source_bytes: number | null;
  readonly alias_ids: readonly number[];
  readonly status: string;
}

export interface V3SebIndexEntry {
  readonly id: number;
  readonly filename: string;
  readonly flags: readonly string[];
  readonly raw_record: string;
  readonly source_index_member: string;
  readonly source_member: string;
  readonly source_sha256: string | null;
  readonly source_bytes: number | null;
  readonly status: string;
}

export interface V3IndexGroup<TEntry> {
  readonly group_id: string;
  readonly pack: string;
  readonly source_index_member: string;
  readonly count: number;
  readonly max_id: number | null;
  readonly gap_ids: readonly number[];
  readonly entries: readonly TEntry[];
}

export interface V3DecodedSebEntry extends V3SebIndexEntry {
  readonly decoded?: SebContract;
}

export interface V3SebResolution {
  readonly status: "resolved" | "sentinel";
  readonly groupId: string;
  readonly sebId: number;
  readonly frame: number;
  readonly layer: number;
  readonly texId: number;
  readonly image: import("./image").IndexedImage | null;
}
