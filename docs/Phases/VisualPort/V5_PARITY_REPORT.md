# V5 Static Parity Report

## Result

Phase V5 reaches `PASS_STATIC` for the recovered Room / RoomData constructor surface, native map topology selection, room-owned nine-pass orchestration, selected room:0 furniture and wall/door composition, integer camera forwarding, all-room topology fixtures, and deterministic command manifest generation.

Focused verification passed:

```text
npm exec vitest -- run tests/v5-room.test.ts
1 file, 27 tests passed
```

The room:0 manifest is recorded in `knowledge/fixtures/accepted/visual-port/v5/room-command-parity-results.json`: 74 commands, 59 traces, 788 events, 9 passes, and SHA-256 `4418a7c8a81a705d46a6eefc2a72e635f5e6108d83e4067dc0d638942f39f788`.

## Regression and boundary

The full repository suite remains green at 41 files and 187 tests. TypeScript typecheck, production build, existing V1/V3/asset/scene/floor/render/closure Python gates, JSON validation, Python compilation, and whitespace checks pass. The production renderer is unchanged, and V5 is not imported by the production route.

Exact native framebuffer pixels, live viewport behavior, emulator/ADB observation, server evidence, network evidence, generic object branches, catalogue FurnitureData.Draw, gameplay, and Staff/Avatar behavior remain outside this static gate. Pixel parity remains deferred to the later evidence phase; no V6 work has started.
