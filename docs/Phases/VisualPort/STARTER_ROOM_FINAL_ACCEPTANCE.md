# Starter-room final acceptance

Status: `PASS_STARTER_ROOM_REINTEGRATION`; stop before V8.

## Target state

The accepted state is `B_ROOM_0_AFTER_NEWGAME_BOOTSTRAP / C_STARTER_MAIN_DISPLAY_STATIC_ENVIRONMENT`. It is source-backed and static. UI overlays, tutorial overlays, and gameplay simulation are excluded.

## Final renders

| Artifact | Commands / traces | Pixel SHA-256 | PNG SHA-256 |
| --- | ---: | --- | --- |
| Structural room | 139 / 124 | `f139c65b2b4357b972fbdbca37308060091607d3907593e6893df77803e67288` | `360a0ee328c451a6fc94585f365de96fe721c55d51db04609cc88d5173c27ca9` |
| Room with Staff | 142 / 127 | `c3d82b29a78b827e682b623c94789e34701bd4cfa0369a14ea81fcf2fe2a30b6` | `95bd38298d3b2dce560bcb1e0b9845f9ac0079b2654d1ddecfebce41446d82c5` |

Both renders repeated with identical pixels and zero changed pixels. Their nontransparent bounds are `{ x: 300, y: 214, width: 720, height: 385 }` on the 1200x700 deterministic preview canvas.

## Acceptance checks

- Floor continuous: pass.
- Walls connected: pass; one wall component, with the door bridge separately proven.
- Corners close: pass.
- Door sits in wall: pass.
- Exterior/front scene coherent: pass.
- Furniture remains inside the room: pass.
- Staff spatially coherent: pass.
- No unexplained holes or floating pieces: pass.
- Ten-panel contact sheet: pass, including the previous broken-room comparison as secondary context.
- Six layer-isolation strips: pass for floor, walls, door, structural, furniture, and Staff.

## Verification

- Focused reintegration tests: 28 passed.
- Full Vitest suite: 44 files, 284 tests passed after the focused suite was added.
- Typecheck: passed.
- Production build: passed; only the existing large-chunk warning remains.
- Python/static gates: 52 passed.
- JSON validation: passed for the workspace JSON set used by the gate.
- Python compilation: passed.
- `git diff --check`: passed.

The evidence package is under `knowledge/fixtures/accepted/visual-port/starter-room-reintegration/`; human QA contact sheet: `previews/STARTER_ROOM_LAYERED_REINTEGRATION_CONTACT_SHEET.png`.

## Explicit freeze

V8 started: `NO`. MapChip foundation changed: `NO`. Production renderer changed: `NO`. Staff semantics changed: `NO`. No emulator, ADB, live app, server, network, browser, screenshot geometry tuning, or subagents were used. Remaining unknowns are non-blocking and documented in `unknowns.json`.
