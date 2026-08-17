# V5 Preview Boundary

The supplemental preview harness is a command-only artifact: `createRoom00StaticPreview()` constructs room:0, runs the isolated RoomV5 pass schedule, and records a stable manifest. It starts no development server and uses no screenshot as proof.

The preview boundary deliberately excludes live application state, viewport behavior, emulator/ADB observation, network evidence, framebuffer comparison, gameplay, and Staff/Avatar rendering. It exists to make Room orchestration inspectable and deterministic before any later phase considers a broader runtime integration.
