import {
  fixtureManifestV1Json as fixtureManifestJson,
  imageOptContractV1Json as imageOptContractJson,
  resourceLookupContractV1Json as resourceLookupContractJson,
  sebContractV1Json as sebContractJson,
} from "../catalog/load-original-runtime-pack";

import type {
  ImageContract,
  ImageOptEvidenceContract,
  ResourceLookupEvidenceContract,
  ResourceLookupFixture,
  SebContract,
  SebEvidenceContract,
  SebEvidenceRecord,
  SebRecordContract,
} from "./contracts";
import { V1LookupError } from "./errors";
import { Image } from "./image";
import { ResourceManager } from "./resource-manager";
import { Seb } from "./seb";

export interface SebFixtureSprite {
  readonly layer: number;
  readonly layerRecordIndex: number;
  readonly FrameNo: number;
  readonly TexId: number;
  readonly TexIdRaw: number;
  readonly U: number;
  readonly V: number;
  readonly W: number;
  readonly H: number;
  readonly TransX: number;
  readonly TransY: number;
  readonly ReverseU: number;
  readonly ReverseV: number;
  readonly Blend: number;
  readonly Color: number;
}

export interface SebFixtureFrame {
  readonly sprites: readonly SebFixtureSprite[];
  readonly sourceLayerOrder: readonly number[];
  readonly sourceRecordIndices: readonly number[];
}

export interface SebFixture {
  readonly category: string;
  readonly sourceMember: string;
  readonly markerRawValues: readonly (number | null)[];
  readonly frames: Readonly<Record<string, SebFixtureFrame>>;
}

interface FixtureManifest {
  readonly fixture_records: readonly { readonly category: string; readonly seb_contract_member: string }[];
}

const fixtureManifest = fixtureManifestJson as FixtureManifest;
const sebEvidence = sebContractJson as SebEvidenceContract;
const imageEvidence = imageOptContractJson as unknown as ImageOptEvidenceContract;
const resourceEvidence = resourceLookupContractJson as unknown as ResourceLookupEvidenceContract;

export function loadImageFixture(stem: string): { readonly image: Image; readonly contract: ImageContract } {
  const contract = imageEvidence.records.find(
    (candidate) => candidate.fixture_stem === stem || candidate.fixture_stem.endsWith(`/${stem}`),
  );
  if (!contract) {
    throw new V1LookupError("IMAGE_FIXTURE_NOT_FOUND");
  }
  return { image: Image.fromContract(contract), contract };
}

export function loadResourceGroup(groupId: string): {
  readonly manager: ResourceManager;
  readonly fixture: ResourceLookupFixture | null;
} {
  const group = resourceEvidence.groups.find((candidate) => candidate.group_id === groupId);
  if (!group) {
    throw new V1LookupError("RESOURCE_GROUP_NOT_FOUND");
  }
  return {
    manager: ResourceManager.fromContract(group),
    fixture: group.fixtures[0] ?? null,
  };
}

export function loadSebFixture(category: string): { readonly seb: Seb; readonly fixture: SebFixture } {
  const fixtureRecord = fixtureManifest.fixture_records.find((entry) => entry.category === category);
  if (!fixtureRecord) {
    throw new V1LookupError("SEB_FIXTURE_NOT_FOUND");
  }
  const evidenceRecord = sebEvidence.records.find((entry) => entry.source_member === fixtureRecord.seb_contract_member);
  if (!evidenceRecord) {
    throw new V1LookupError("SEB_FIXTURE_CONTRACT_NOT_FOUND");
  }
  return {
    seb: Seb.fromContract(evidenceRecord.decoded),
    fixture: projectFixture(category, evidenceRecord),
  };
}

function projectFixture(category: string, evidenceRecord: SebEvidenceRecord): SebFixture {
  const contract = evidenceRecord.decoded;
  const frames: Record<string, SebFixtureFrame> = {};
  for (let frame = 0; frame < contract.header.frame_bound; frame += 1) {
    const selected = contract.layers.map((layer) => selectFixtureRecord(layer.records, frame));
    if (selected.some((record) => record === null)) {
      throw new V1LookupError("SEB_FIXTURE_FRAME_RECORD_NOT_FOUND");
    }
    const records = selected as SebRecordContract[];
    frames[String(frame)] = {
      sprites: records.map(toFixtureSprite),
      sourceLayerOrder: contract.layers.map((layer) => layer.layer),
      sourceRecordIndices: records.map((record) => record.layer_record_index),
    };
  }
  return {
    category,
    sourceMember: evidenceRecord.source_member,
    markerRawValues: contract.layers.map((layer) => layer.marker?.raw_value ?? null),
    frames,
  };
}

function selectFixtureRecord(records: readonly SebRecordContract[], frame: number): SebRecordContract | null {
  const explicitFrame = frame % 10000;
  let selected: SebRecordContract | null = null;
  for (const record of records) {
    if (record.start_frame <= explicitFrame) {
      selected = record;
    }
  }
  return selected;
}

function toFixtureSprite(record: SebRecordContract): SebFixtureSprite {
  return {
    layer: record.layer,
    layerRecordIndex: record.layer_record_index,
    FrameNo: record.start_frame,
    TexId: record.image_id,
    TexIdRaw: record.image_id_raw,
    U: record.source_x,
    V: record.source_y,
    W: record.width,
    H: record.height,
    TransX: record.destination_x,
    TransY: record.destination_y,
    ReverseU: record.flags & 1,
    ReverseV: (record.flags >> 1) & 1,
    Blend: (record.flags >> 2) & 0xF,
    Color: record.reserved,
  };
}
