import type { ResourceManagerV3 } from "./resource-manager";
import { V3LookupError } from "./errors";

export class VisualAppDataV3 {
  public constructor(
    public readonly resChip_: ResourceManagerV3,
    public readonly resInterface_: ResourceManagerV3,
    public readonly resHuman_: ResourceManagerV3,
    public readonly resCom_: ResourceManagerV3,
    public readonly resGame_: ResourceManagerV3,
    public readonly resEffect_: ResourceManagerV3,
    public readonly resMeeting_: ResourceManagerV3,
    public readonly resAvatarBody_: ResourceManagerV3,
    public readonly resAvatarHead_: ResourceManagerV3,
    public readonly resDevelop_: ResourceManagerV3,
    public readonly resWindow_: ResourceManagerV3,
  ) {}

  public getResourceManager(groupId: string): ResourceManagerV3 {
    const manager = (this as unknown as Record<string, ResourceManagerV3>)[groupId];
    if (manager === undefined) {
      throw new V3LookupError("RESOURCE_GROUP_NOT_FOUND", `Declared AppData group ${groupId} is not available`);
    }
    return manager;
  }
}
