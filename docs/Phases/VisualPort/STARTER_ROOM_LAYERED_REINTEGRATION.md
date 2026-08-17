# Starter-room layered reintegration

Status: `PASS_STARTER_ROOM_REINTEGRATION`
Execution: inline, sequential, static-only
Scope: `room:0` after NewGame bootstrap, starter main-display static environment, excluding UI, tutorial overlays, and gameplay simulation.

## Gate result

The reintegration gate passed RI.0 through RI.11. The accepted 14x14 MapChip foundation was frozen first, then the room floor owner, walls/corners, door, structural facilities, FurnitureData bootstrap, and the Staff fixture were reintegrated in source pass order. V8 was not started.

The short plan is recorded in `STARTER_ROOM_LAYERED_REINTEGRATION_PLAN.md`. The isolated selector/range adapter is `runtime/social-dev/src/v7/starter-room-reintegration.ts`; the production renderer and V5/V6 routes were not changed.

## Layer ledger

| Layer | Owner | Commands added | Evidence |
| --- | --- | ---: | --- |
| Stage 0 MapChip foundation | `MAPCHIP_FOUNDATION` | 81 | `stage0-mapchip.json` |
| Stage 1 room floor | `ROOM_FLOOR_OWNER` | 0 | `stage1-room-floor.json` |
| Stage 2 walls/corners | `OBJCHIP_WALL` | 46 | `stage2-walls-corners.json` |
| Stage 3 door | `DOOR` | 1 | `stage3-door.json` |
| Stage 4 structural/facility | `STRUCTURAL` | 2 | `stage4-structural.json` |
| Stage 5 furniture bootstrap | `FURNITURE_BOOTSTRAP` | 9 | `stage5-furniture.json` |
| Stage 6 Staff | `STAFF_INTEGRATION` | 3 | `stage6-staff.json` |
| Stage 7 final render acceptance | `ROOM_PASS` | 0 additional | `final-scene-manifest.json` |

The structural stream contains 139 commands and 124 traces. The complete Room+Staff stream contains 142 commands, 127 traces, and 791 events.

## Deterministic render anchors

- Stage 0 MapChip pixel SHA-256: `3ea05bd9edcc5168a14ee1b0e79256e460072be75c018f11f2009d01c215d293`
- Stage 0 PNG SHA-256: `fb40142389fe963bba46a93a122f961dc21fe8a85d0abac75b1a68fd3d4ecaed`
- Final structural pixel SHA-256: `f139c65b2b4357b972fbdbca37308060091607d3907593e6893df77803e67288`
- Final structural PNG SHA-256: `360a0ee328c451a6fc94585f365de96fe721c55d51db04609cc88d5173c27ca9`
- Final Room+Staff pixel SHA-256: `c3d82b29a78b827e682b623c94789e34701bd4cfa0369a14ea81fcf2fe2a30b6`
- Final Room+Staff PNG SHA-256: `95bd38298d3b2dce560bcb1e0b9845f9ac0079b2654d1ddecfebce41446d82c5`

Both final renders repeated with identical pixels and zero changed pixels. The normalized preview uses a 1200x700 canvas, origin `{ x: 100, y: 300 }`, and the existing source-backed coordinate bridge; no screenshot geometry tuning was used.

## Evidence package

Machine evidence is under `knowledge/fixtures/accepted/visual-port/starter-room-reintegration/`. It includes the checkpoint ledger, one JSON contract per stage, final-scene manifest, coordinate bridge audit, pass-membership audit, visual acceptance, explicit unknowns, previews, six layer-isolation strips, and the ten-panel contact sheet with the previous broken-room comparison as a secondary panel.

Remaining unknowns are explicitly non-blocking: native shader/framebuffer/premultiplied-alpha parity, complete live Staff cadence, and whether historical screenshots contain UI/tutorial overlays outside this static target.

## Freeze

`V8 started: NO`. MapChip foundation: unchanged. Staff semantics: unchanged. Production renderer: unchanged. Emulator, ADB, live app, local server, network, browser, screenshot-derived numeric tuning, and subagents: not used.
