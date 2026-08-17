import { createV5CommandManifest, stableJson } from "./manifest";
import { createRoomV5 } from "./room";

export interface V5StaticPreviewArtifact {
  readonly kind: "static-room-command-preview";
  readonly roomKey: "room:0";
  readonly serverStarted: false;
  readonly screenshotUsedAsProof: false;
  readonly manifest: ReturnType<typeof createV5CommandManifest>;
  readonly stableSerialization: string;
}

/** Supplemental preview harness. It records commands only and starts no server. */
export function createRoom00StaticPreview(): V5StaticPreviewArtifact {
  const room = createRoomV5("room:0", { context: "main_display" });
  const render = room.draw();
  const manifest = createV5CommandManifest(room, render);
  return {
    kind: "static-room-command-preview",
    roomKey: "room:0",
    serverStarted: false,
    screenshotUsedAsProof: false,
    manifest,
    stableSerialization: stableJson(manifest),
  };
}
