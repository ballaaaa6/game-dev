# V4 ObjChip Recovery

Phase V4 recovers the selected ObjChip visual surface and keeps raw object identity separate from FurnitureData identity. The implementation is an additive adapter under `runtime/social-dev/src/v4/obj-chip.ts`; it is not wired into the production renderer.

## Native surface and direction

The recovered ObjChip fields include `type_`, `direction_`, `seb_`, `subSeb_`, `img_`, position/room fields, and the native wall draw surface. `DrawWall` is mapped to `0x12C0698`; the selected Draw overloads are `0x12C0E00`, `0x12C1664`, `0x12C166C`, and `0x12C5188`.

The raw direction domain is preserved exactly:

| raw | native label | vector | reverse |
| ---: | --- | --- | ---: |
| 0 | `DIRECTION_RIGHT` | `[0,1]` | 1 |
| 1 | `DIRECTION_LEFT` | `[0,-1]` | 0 |
| 2 | `DIRECTION_UP` | `[1,0]` | 3 |
| 3 | `DIRECTION_DOWN` | `[-1,0]` | 2 |

The object origin is `x=ofx+(x+y)*20`, `y=ofy+(y-x)*10+9`. This is intentionally distinct from the MapChip projection.

## Wall and door semantics

The selected wall path uses SEB selector `5` and the native wall image selector `6`. A verified intersection cell emits vertical frame `1` followed by horizontal frame `0`. Raw type `5` is a door path: it uses the installed door record, SEB selector `6`, and image selector `7`, without consulting FurnitureData.

The selected local ordering places rear wall passes before foreground cells `[8,7]` and `[8,8]`; the comparator is isolated in `ordering.ts`.

## Furniture boundary

V4 only draws a FurnitureData binding when it is explicitly supplied and its `rawType` matches the ObjChip input. A raw ObjChip type never infers a FurnitureData ID. Generic damaged Draw branches, alternate wall branches, and unproven direction-specific asset selection are recorded in `unknowns.json` and deferred to V5.

Evidence: `objchip-native-map.json`, `objchip-direction-contract.json`, `objchip-draw-contract.json`, `local-ordering-contract.json`, and `command-parity-results.json`.
