import {
  imageOptContractV1Json as imageOptContractJson,
  sebContractV1Json as sebContractJson,
} from "../catalog/load-original-runtime-pack";

import type {
  ImageOptEvidenceContract,
  ResourceLookupGroupContract,
  SebEvidenceContract,
} from "./contracts";
import { V1ContractError, V1DeferredError, V1LookupError } from "./errors";
import { Image } from "./image";
import { Seb } from "./seb";

const imageEvidence = imageOptContractJson as unknown as ImageOptEvidenceContract;
const sebEvidence = sebContractJson as unknown as SebEvidenceContract;

export class ResourceManager {
  public readonly img: readonly (Image | null)[];

  public readonly seb: readonly (Seb | null)[];

  public readonly groupId: string;

  public readonly fixtures: ResourceLookupGroupContract["fixtures"];

  public readonly atlasStatus = "deferred" as const;

  private constructor(group: ResourceLookupGroupContract) {
    this.groupId = group.group_id;
    this.fixtures = group.fixtures;
    this.img = Object.freeze(loadImages(group));
    this.seb = Object.freeze(loadSebs(group));
  }

  public static fromContract(group: ResourceLookupGroupContract): ResourceManager {
    validateGroupContract(group);
    return new ResourceManager(group);
  }

  public getImage(id: number): Image {
    const validId = requireLookupId(id);
    const image = this.img[validId];
    if (image === undefined || image === null) {
      throw new V1LookupError("RESOURCE_IMAGE_NOT_FOUND");
    }
    return image;
  }

  public getSeb(id: number): Seb {
    const validId = requireLookupId(id);
    const seb = this.seb[validId];
    if (seb === undefined || seb === null) {
      throw new V1LookupError("RESOURCE_SEB_NOT_FOUND");
    }
    return seb;
  }

  public loadImage(id: number): Image {
    return this.getImage(id);
  }

  public loadSeb(id: number): Seb {
    return this.getSeb(id);
  }

  public getAtlas(_id: number): never {
    throw new V1DeferredError(
      "RESOURCE_ATLAS_DEFERRED",
      "The selected V1 fixtures have no proven atlas-backed relationship; ImageAtlas remains deferred.",
    );
  }
}

function loadImages(group: ResourceLookupGroupContract): (Image | null)[] {
  const maxId = group.image_bindings.reduce((maximum, binding) => Math.max(maximum, binding.id), -1);
  const images: (Image | null)[] = new Array(maxId + 1).fill(null);
  for (const binding of group.image_bindings) {
    if (binding.image_contract_stem === null) {
      continue;
    }
    const contract = imageEvidence.records.find(
      (candidate) => candidate.fixture_stem === binding.image_contract_stem,
    );
    if (contract === undefined) {
      throw new V1ContractError("RESOURCE_IMAGE_CONTRACT_NOT_FOUND");
    }
    const image = Image.fromContract(contract);
    if (image.sourceMember !== binding.source_member) {
      throw new V1ContractError("RESOURCE_IMAGE_SOURCE_MISMATCH");
    }
    images[binding.id] = image;
  }
  return images;
}

function loadSebs(group: ResourceLookupGroupContract): (Seb | null)[] {
  const maxId = group.seb_bindings.reduce((maximum, binding) => Math.max(maximum, binding.id), -1);
  const sebs: (Seb | null)[] = new Array(maxId + 1).fill(null);
  for (const binding of group.seb_bindings) {
    if (binding.seb_contract_member === null) {
      continue;
    }
    const evidence = sebEvidence.records.find(
      (candidate) => candidate.source_member === binding.seb_contract_member,
    );
    if (evidence === undefined) {
      throw new V1ContractError("RESOURCE_SEB_CONTRACT_NOT_FOUND");
    }
    if (evidence.source_member !== binding.source_member) {
      throw new V1ContractError("RESOURCE_SEB_SOURCE_MISMATCH");
    }
    sebs[binding.id] = Seb.fromContract(evidence.decoded);
  }
  return sebs;
}

function validateGroupContract(group: ResourceLookupGroupContract): void {
  if (
    group === null
    || typeof group !== "object"
    || typeof group.group_id !== "string"
    || group.group_id.length === 0
    || !Array.isArray(group.image_bindings)
    || !Array.isArray(group.seb_bindings)
    || !Array.isArray(group.fixtures)
  ) {
    throw new V1ContractError("RESOURCE_GROUP_CONTRACT_MALFORMED");
  }
}

function requireLookupId(id: number): number {
  if (!Number.isSafeInteger(id) || id < 0) {
    throw new V1LookupError("RESOURCE_ID_MALFORMED");
  }
  return id;
}
