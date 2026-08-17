# V3 Original Resource-Group Recovery

## Current status

`V3 STATUS: PASS`. The static ownership, index, load-surface, and SEB-to-image contracts are recovered for the declared AppData visual groups, and the real-fixture/regression gate is green. The implementation is additive under `runtime/social-dev/src/v3/`; it is not a production renderer cutover and does not create a competing global asset format.

V2 is accepted at `PASS_STATIC` for V3 entry. Native framebuffer/shader pixels remain `DEFERRED_TO_V7` and are outside this phase.

## Authority and flow

The recovered authority is:

`AppData group field → ResourceManager group instance → pack-local img.inf/seb.inf original ID → Image/Seb object → V1 Seb/Sprite contract → V2 draw boundary`

The group ID and original numeric ID are retained at every step. A filename is descriptive evidence only. No global manifest, browser catalog, or cross-group fallback is used as semantic authority.

## Declared group inventory

| AppData field | Static pack ownership | Coverage | Evidence |
| --- | --- | --- | --- |
| `resChip_` | `01_GAME_PACKS/chip` | `PROVEN_BOTH` | `RESCHIP_*`, ObjChip/MapChip/FurnitureData consumers, `img.inf`, `seb.inf` |
| `resInterface_` | not proven | `DECLARED_ONLY` | AppData declaration and partial consumers only |
| `resHuman_` | `01_GAME_PACKS/human` | `PROVEN_BOTH` | `RESHUMAN_*`, Staff consumers, both indexes |
| `resCom_` | `01_GAME_PACKS/com` | `PROVEN_BOTH` | `RESCOM_*`, common draw consumers, both indexes |
| `resGame_` | `01_GAME_PACKS/game` | `PROVEN_BOTH` | `RESGAME_*`, Room draw consumers, both indexes |
| `resEffect_` | `01_GAME_PACKS/effect` | `PROVEN_BOTH` | `RESEFFECT_*`, effect consumers, both indexes |
| `resMeeting_` | `01_GAME_PACKS/meeting` | `PROVEN_BOTH` | `RESMEETING_*`, Meeting consumers, both indexes |
| `resAvatarBody_` | `01_GAME_PACKS/avatar_body` | `PROVEN_BOTH` | `RESAVATAR_BODY_*`, Avatar consumers, both indexes |
| `resAvatarHead_` | `01_GAME_PACKS/avatar_head` | `PROVEN_SOURCE_INDEXED` | `RESAVATAR_HEAD_*`, Avatar image consumer, image index only |
| `resDevelop_` | `01_GAME_PACKS/develop` | `PROVEN_BOTH` | `RESDEVELOP_*`, Develop consumers, both indexes |
| `resWindow_` | `01_GAME_PACKS/window` | `PROVEN_BOTH` | `RESWINDOW_*`, Window consumers, both indexes |

Additional named ResourceManager owners are inventoried separately: `resTitle_`, `resRecruit_`, `resEvents_`, and `resSound_`. They are not silently assigned to one of the 11 AppData visual groups. Local unnamed managers remain unresolved.

## Checkpoint ledger

| Checkpoint | Result | Evidence |
| --- | --- | --- |
| V3.0 V2 static entry normalization | `PASS` | `knowledge/fixtures/accepted/visual-port/v2/v2-static-acceptance.json` |
| V3.1 group and pack inventory | `PASS_WITH_EXPLICIT_UNRESOLVED_GROUPS` | `resource-group-map.json`, `pack-inventory.json` |
| V3.2 ResourceManager shape and sparse ownership | `PASS_STATIC` | `resource-manager-layout.json`, `img-index-contract.json`, `seb-index-contract.json` |
| V3.3 INF records, gaps, flags, and aliases | `PASS_SOURCE_INDEXED` | `img-index-contract.json`, `seb-index-contract.json` |
| V3.4 load overload surface | `PASS_WITH_ASYNC_DEFERRED` | `load-semantics.json`, `native-recovery-map.json` |
| V3.5 Seb `TexId` association | `PASS_SAME_GROUP_NAMESPACE` | `image-seb-association.json` |
| V3.6 coverage matrix | `PASS_WITH_EXPLICIT_BOUNDARIES` | `group-coverage.json` |
| V3.7 CustomImages/atlas/lifetime boundary | `PASS_WITH_DEFERRED_PATHS` | `resource-manager-layout.json`, V1 Image contracts |
| V3.8 isolated compatibility layer | `PASS_IMPLEMENTED` | `runtime/social-dev/src/v3/` |
| V3.9 real fixtures and regressions | `PASS` | `fixture-manifest.json`, V3 Vitest suite |
| V3.10 final gates and handoff | `PASS` | checkpoint ledger, full verification matrix, PROJECT_STATE.md, TODO.md |

## Scope boundary

V3 does not render a scene, run gameplay, start a local server, execute the original C# extraction, use ADB/emulator/live-app state, or claim raster parity. Source-indexed gaps remain null. Unsupported SEB payloads remain source-limited. V4 may request these resource objects by group and original ID once the final V3 regression gate is green.
