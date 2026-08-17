# V1 Fixture Matrix

## Source identity

The matrix uses the real archive recorded by `fixture-manifest.json`. Its ZIP SHA-256 is `c4b6ac1b6603eb8e2d7ac78e7dd3b8bffb40b7c30fe036cb644bea701087b283`. Each row is checked against the archive member and its extracted source hash.

| Fixture ID | Exact source member | V1 evidence exercised | Result |
| --- | --- | --- | --- |
| `simple_one_layer` | `01_GAME_PACKS/chip/door_02.seb` | SEB single-layer record, Sprite fields, geometry bounds, pixel-rectangle fallback | `FORMAT-PROVEN`; depth deferred |
| `multi_layer` | `01_GAME_PACKS/chip/wall_00.seb` | SEB record/layer ordering and Sprite projection | `FORMAT-PROVEN`; depth deferred |
| `multi_frame` | `01_GAME_PACKS/chip/chair_00.seb` | SEB multi-frame source order and Sprite frame fields | `FORMAT-PROVEN`; depth deferred |
| `translation` | `01_GAME_PACKS/chip/desk_00.seb` | translated Sprite coordinates and source association | `FORMAT-PROVEN`; depth deferred |
| `flip` | `01_GAME_PACKS/human/wait_left.seb` | reverse-U/reverse-V Sprite flags | `FORMAT-PROVEN`; depth deferred |
| `character` | `01_GAME_PACKS/avatar_body/wait_right.seb` | character SEB source association and resource group binding | `FORMAT-PROVEN`; depth deferred |
| `furniture` | `01_GAME_PACKS/chip/chair_00.seb` plus `chair_00.opt` | Image/OPT header, cells, logical pixels, source-region lookup | exact pixel hash; resize/atlas deferred |

## Image/OPT selected set

The Image contract selects `chair_00`, `chair_02`, `desk_00`, and `door_02` OPT records. All four use the standard OPT path in the selected evidence, so `Image.GetOptimizeSeb` is explicitly deferred rather than fabricated. Each selected record has a `PROMOTED_PIXEL_EXACT` logical reconstruction and a source PNG pixel hash.

## Resource lookup coverage

Proven source-indexed bindings include `resChip_`, `resHuman_`, and `resAvatarBody_`. The remaining declared groups are preserved as declarations without invented memberships. The door SEB source binding resolves to source image slot 7, `door_01.png`; it is not guessed to `door_02.png` merely because `door_02.seb` is a selected geometry fixture.

## Explicit source boundary

`01_GAME_PACKS/develop/develop_menu_light.seb` is a real archive member and is recorded in `parity-results.json` as `NON_SELECTED_UNSUPPORTED`. It is outside the selected V1 fixture matrix. This boundary is an unknown/deferred investigation item, not a parity failure and not evidence for a new decoder branch.

## V2 stop decision

V2 has not started. The matrix is sufficient for the selected V1 format contracts, but it is not a claim that every archive asset, atlas path, depth line, or asynchronous resource path is supported.
