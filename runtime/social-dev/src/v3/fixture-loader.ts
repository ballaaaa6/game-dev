import {
  fixtureManifestV3Json as fixtureManifestJson,
  groupMapV3Json as groupMapJson,
  imgIndexV3Json as imgIndexJson,
  sebIndexV3Json as sebIndexJson,
  packInventoryV3Json as packInventoryJson,
  sebCatalogJson,
} from "../catalog/load-original-runtime-pack";
import type { SebContract } from "../v1/contracts";
import { VisualAppDataV3 } from "./app-data";
import type { V3DecodedSebEntry, V3ImageIndexEntry, V3IndexGroup, V3SebIndexEntry } from "./contracts";
import { ResourceManagerV3 } from "./resource-manager";

type JsonRecord = Record<string, unknown>;

const fixtureManifest = fixtureManifestJson as unknown as JsonRecord & { fixtures: readonly JsonRecord[] };
const groupMap = groupMapJson as unknown as JsonRecord & { groups: readonly JsonRecord[] };
const imgIndex = imgIndexJson as unknown as { groups: readonly V3IndexGroup<V3ImageIndexEntry>[] };
const sebIndex = sebIndexJson as unknown as { groups: readonly V3IndexGroup<V3SebIndexEntry>[] };
const packInventory = packInventoryJson as unknown as { packs: Record<string, JsonRecord> };
const sebCatalog = sebCatalogJson as unknown as { assets: readonly (JsonRecord & { member: string; status: string; decode?: SebContract })[] };

export function createResourceManager(groupId: string): ResourceManagerV3 {
  const group = groupMap.groups.find((candidate) => candidate.group_id === groupId) as (JsonRecord & { source_pack: string | null }) | undefined;
  if (group === undefined) {
    throw new Error(`Unknown V3 group: ${groupId}`);
  }
  const imageGroup = imgIndex.groups.find((candidate) => candidate.group_id === groupId) ?? null;
  const rawSebGroup = sebIndex.groups.find((candidate) => candidate.group_id === groupId) ?? null;
  const decodedSebByMember = buildDecodedSebMap();
  const decodedEntries: V3DecodedSebEntry[] = rawSebGroup === null
    ? []
    : rawSebGroup.entries.map((entry) => ({
      ...entry,
      decoded: decodedSebByMember.get(entry.source_member),
    }));
  return ResourceManagerV3.fromEvidence({
    groupId,
    pack: group.source_pack,
    imageIndex: imageGroup,
    sebIndex: rawSebGroup === null ? null : { ...rawSebGroup, entries: decodedEntries },
    decodedSebByMember,
  });
}

export function createAdditionalResourceManager(ownerId: string): ResourceManagerV3 {
  const owners = groupMapJson.additional_resource_manager_owners as readonly (JsonRecord & { owner_id: string; pack: string | null })[];
  const owner = owners.find((candidate) => candidate.owner_id === ownerId);
  if (owner === undefined || owner.pack === null) {
    throw new Error(`Unknown or non-visual V3 owner: ${ownerId}`);
  }
  const pack = packInventory.packs[owner.pack] as JsonRecord & { indexes: { img: JsonRecord | null; seb: JsonRecord | null } };
  const imageIndex = pack.indexes.img === null ? null : toPackIndex(ownerId, owner.pack, pack.indexes.img) as unknown as V3IndexGroup<V3ImageIndexEntry>;
  const rawSeb = pack.indexes.seb === null ? null : toPackIndex(ownerId, owner.pack, pack.indexes.seb) as unknown as V3IndexGroup<V3SebIndexEntry>;
  const decodedSebByMember = buildDecodedSebMap();
  const decodedEntries = rawSeb === null ? [] : rawSeb.entries.map((entry) => ({ ...entry, decoded: decodedSebByMember.get(entry.source_member) }));
  return ResourceManagerV3.fromEvidence({
    groupId: ownerId,
    pack: owner.pack,
    imageIndex,
    sebIndex: rawSeb === null ? null : { ...rawSeb, entries: decodedEntries },
    decodedSebByMember,
  });
}

export function createVisualAppData(): VisualAppDataV3 {
  return new VisualAppDataV3(
    createResourceManager("resChip_"),
    createResourceManager("resInterface_"),
    createResourceManager("resHuman_"),
    createResourceManager("resCom_"),
    createResourceManager("resGame_"),
    createResourceManager("resEffect_"),
    createResourceManager("resMeeting_"),
    createResourceManager("resAvatarBody_"),
    createResourceManager("resAvatarHead_"),
    createResourceManager("resDevelop_"),
    createResourceManager("resWindow_"),
  );
}

export function getFixture(fixtureId: string): JsonRecord {
  const fixture = fixtureManifest.fixtures.find((candidate) => candidate.fixture_id === fixtureId);
  if (fixture === undefined) {
    throw new Error(`Unknown V3 fixture: ${fixtureId}`);
  }
  return fixture;
}

function buildDecodedSebMap(): Map<string, SebContract> {
  const result = new Map<string, SebContract>();
  for (const asset of sebCatalog.assets) {
    if (asset.status === "pass" && asset.decode?.status === "pass") {
      result.set(asset.member, asset.decode);
    }
  }
  return result;
}

function toPackIndex(groupId: string, pack: string, index: JsonRecord): V3IndexGroup<JsonRecord> {
  return {
    group_id: groupId,
    pack,
    source_index_member: index.source_index_member as string,
    count: index.count as number,
    max_id: index.max_id as number | null,
    gap_ids: index.gap_ids as readonly number[],
    entries: index.rows as readonly JsonRecord[],
  };
}
