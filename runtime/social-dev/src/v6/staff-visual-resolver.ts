import type { CharacterAssetStaffBinding, CharacterMetadataRecord } from "../catalog/types";
import type { HumanDirectionInput } from "./human-action-resolver";
import { getStaffAssetBinding, getStaffMetadata, loadStaffFixtureCatalog, type StaffFixtureCatalog } from "./fixture-loader";
import { resolveHumanAction } from "./human-action-resolver";
import type { StaffAction, StaffSelectorResolution } from "./contracts";

export interface StaffVisualSurfaceV6 {
  readonly metadata: CharacterMetadataRecord;
  readonly assetBinding: CharacterAssetStaffBinding;
  readonly imageSelectorId: number;
  readonly selector: StaffSelectorResolution;
}

export class StaffVisualResolverV6 {
  public constructor(private readonly catalog: StaffFixtureCatalog = loadStaffFixtureCatalog()) {}

  public resolve(
    sourceStaffId: number,
    action: StaffAction | string,
    direction: HumanDirectionInput,
  ): StaffVisualSurfaceV6 {
    const metadata = getStaffMetadata(sourceStaffId, this.catalog);
    const assetBinding = getStaffAssetBinding(sourceStaffId, this.catalog);
    const imageSelectorId = metadata.render?.image_selector?.id;
    if (imageSelectorId === undefined || imageSelectorId !== assetBinding.image_selector_id) {
      throw new Error(`V6 StaffData and character asset image selectors diverge for ${metadata.id}`);
    }
    return {
      metadata,
      assetBinding,
      imageSelectorId,
      selector: resolveHumanAction(action, direction, this.catalog),
    };
  }
}
