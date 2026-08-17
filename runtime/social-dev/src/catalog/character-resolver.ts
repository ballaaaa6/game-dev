import type {
  CharacterActionCapability,
  CharacterCapabilityProfile,
  CharacterCapabilitySelector,
  CharacterMetadataRecord,
  CharacterMetadataSelector,
} from "./types";
import type { RuntimeCatalogs } from "./load-contracts";

export type CharacterCatalogKind = "staff" | "helper";
export type CharacterDirection = "right" | "left" | "up" | "down";

export interface ResolvedCharacterTemplate {
  readonly catalogKind: CharacterCatalogKind;
  readonly template: CharacterMetadataRecord;
  readonly profile: CharacterCapabilityProfile;
  readonly animationProfileId: string | null;
  readonly behaviorProfileId: string | null;
  readonly imageSelector: CharacterMetadataSelector | null;
  readonly bigImageSelector: CharacterMetadataSelector | null;
}

export interface CharacterActionResolution {
  readonly characterId: string;
  readonly action: string;
  readonly resolvedAction: string | null;
  readonly direction: CharacterDirection;
  readonly status: string;
  readonly selector: CharacterCapabilitySelector | null;
  readonly capability: CharacterActionCapability | null;
}

export interface CharacterSpawnPlan {
  readonly instanceCreation: "lazy_on_spawn_or_scene_use";
  readonly characterId: string;
  readonly catalogKind: CharacterCatalogKind;
  readonly sourceId: number;
  readonly templateId: string;
  readonly profileId: string;
  readonly behaviorProfileId: string | null;
  readonly animationProfileId: string | null;
  readonly imageSelector: CharacterMetadataSelector | null;
  readonly bigImageSelector: CharacterMetadataSelector | null;
  readonly availableActions: readonly string[];
  readonly assetLoading: string;
}

function normalizeCharacterId(characterId: string): string {
  return characterId.startsWith("actor:") ? characterId.slice("actor:".length) : characterId;
}

function findTemplate(catalogs: RuntimeCatalogs, characterId: string): {
  readonly catalogKind: CharacterCatalogKind;
  readonly template: CharacterMetadataRecord;
} | null {
  const normalized = normalizeCharacterId(characterId);
  const staff = catalogs.characterMetadata.staff.find((candidate) => candidate.id === normalized);
  if (staff) {
    return { catalogKind: "staff", template: staff };
  }
  const helper = catalogs.characterMetadata.helpers.find((candidate) => candidate.id === normalized);
  if (helper) {
    return { catalogKind: "helper", template: helper };
  }
  return null;
}

function profileFor(catalogs: RuntimeCatalogs, template: CharacterMetadataRecord): CharacterCapabilityProfile {
  const profileId = template.render?.capability_profile_ref;
  if (!profileId) {
    throw new Error(`Character metadata ${template.id} has no capability profile reference`);
  }
  const profile = catalogs.characterCapabilities.profiles.find((candidate) => candidate.id === profileId);
  if (!profile) {
    throw new Error(`Character capability profile ${profileId} is missing for ${template.id}`);
  }
  return profile;
}

export function resolveCharacter(catalogs: RuntimeCatalogs, characterId: string): ResolvedCharacterTemplate {
  const found = findTemplate(catalogs, characterId);
  if (!found) {
    throw new Error(`Character metadata is missing ${characterId}`);
  }
  const { template } = found;
  const profile = profileFor(catalogs, template);
  const behaviorProfileId = template.render?.behavior_profile_ref ?? profile.behavior.profile_ref;
  return {
    catalogKind: found.catalogKind,
    template,
    profile,
    animationProfileId: template.render?.animation_profile_ref ?? null,
    behaviorProfileId,
    imageSelector: template.render?.image_selector ?? null,
    bigImageSelector: template.render?.big_image_selector ?? null,
  };
}

export function resolveCharacterAction(
  catalogs: RuntimeCatalogs,
  characterId: string,
  action: string,
  direction: CharacterDirection = "right",
): CharacterActionResolution {
  const resolved = resolveCharacter(catalogs, characterId);
  const capability = resolved.profile.actions[action] ?? resolved.profile.native_actions?.[action] ?? null;
  if (!capability) {
    return {
      characterId,
      action,
      resolvedAction: null,
      direction,
      status: "unsupported",
      selector: null,
      capability: null,
    };
  }
  const selector = capability.selector_by_direction?.[direction] ?? capability.selector ?? null;
  return {
    characterId,
    action,
    resolvedAction: capability.source_action ?? action,
    direction,
    status: selector ? capability.status : capability.status === "deferred" ? "deferred" : "no_selector_for_direction",
    selector,
    capability,
  };
}

export function createCharacterSpawnPlan(catalogs: RuntimeCatalogs, characterId: string): CharacterSpawnPlan {
  const resolved = resolveCharacter(catalogs, characterId);
  const assetLoading = typeof resolved.profile.asset_loading === "object"
    && resolved.profile.asset_loading !== null
    && "policy" in resolved.profile.asset_loading
    && typeof resolved.profile.asset_loading.policy === "string"
    ? resolved.profile.asset_loading.policy
    : catalogs.characterCapabilities.runtime_policy.asset_loading;
  return {
    instanceCreation: "lazy_on_spawn_or_scene_use",
    characterId,
    catalogKind: resolved.catalogKind,
    sourceId: resolved.template.source_identity.source_id,
    templateId: resolved.template.id,
    profileId: resolved.profile.id,
    behaviorProfileId: resolved.behaviorProfileId,
    animationProfileId: resolved.animationProfileId,
    imageSelector: resolved.imageSelector,
    bigImageSelector: resolved.bigImageSelector,
    availableActions: [...new Set([
      ...Object.keys(resolved.profile.actions),
      ...Object.keys(resolved.profile.native_actions ?? {}),
    ])],
    assetLoading,
  };
}
