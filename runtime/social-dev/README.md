# Social Dev runtime boundary

This directory is contract-first and is not a copy of the archived Office runtime. The unified main runtime uses the approved native catalogs, room assembly, character metadata, spawn, camera, behavior, tick-order, floor00, and pre-runtime contracts.

Raw decompiled C# and source/extraction roots remain evidence only. The browser imports promoted JSON contracts, owns mutable TypeScript state, and renders immutable snapshots.

## Web runtime stack

- TypeScript source compiled to browser JavaScript with Vite;
- Canvas 2D for the scene/map/actor renderer;
- DOM/CSS for panels, text, bubbles, menus, and diagnostics;
- pure TypeScript core with no DOM or Canvas dependency;
- JSON catalogs and versioned contracts imported from the approved evidence boundary;
- Python remains an extraction/validation tool only and is not imported by the browser runtime.

## Runtime layout

```text
runtime/social-dev/
  assets/         promoted source binaries from the approved display subset
  generated/      generated original runtime pack mirror
  (contracts)     approved contracts live under knowledge/fixtures/accepted/runtime/
  src/assets/     manifest validation, image loading, and frame selection
  src/catalog/    contract types and runtime boundary checks
  src/core/       immutable state, fixed ticks, routes, events, digest
  src/scene/      contract-backed room projection and coordinates
  src/renderer/   Canvas scene plus DOM/CSS diagnostics
  src/app/        browser controller and fixed-step wall-clock driver
  tests/          deterministic and browser-trace evidence gates
```

The core is independent of DOM and Canvas. The renderer never mutates simulation state. The wall-clock driver only requests fixed logical steps; it does not enter the core's state calculations.

## Unified main runtime

The root URL is the single production entrypoint:

```text
http://127.0.0.1:4173/?auto=0
```

It defaults to the approved native `floor00` bootstrap at `room:0` and keeps all current catalog data in the same runtime. The in-page RoomData selector reaches every current room record without creating a second route.

The unified main scene includes:

- the native 14×14 MapChip topology (`196` cells) and 10×10 ObjChip topology (`100` cells);
- the native door at `[8,4]`, six native FurnitureData instances, two structural facility pads, and three static display actors;
- all 18 RoomData records, their raw cells, native wall/door compositions, directions, and room selector assets;
- the complete approved native content catalog, asset metadata, human character layer, and diagnostics;
- the floor00 visual-layout contract, nine native render passes, final-pixel visibility gate, and explicit floor alias policy.

## Native floor00 main scene

`floor00` is the native `AppData.NewGame → roomData_[0] → Room.floor_=0` bootstrap, not the literal `floor_00.png` texture. The runtime uses the exact native dimensions and initial bindings from `knowledge/fixtures/accepted/runtime/floor00_scene_contract.json`:

- `14×14` shared `MapChip` topology (`196` cells);
- `10×10` raw `ObjChip` topology (`100` cells);
- six native `FurnitureData` instances: three `furniture:3` desks, one `furniture:12` trash can, one `furniture:26` old printer, and one `furniture:56` calendar;
- two raw `type 4` facility centers at `[4,2]` and `[7,2]`, rendered as static `big_base00.seb` structural compositions at explicit MapChip visual anchors `[4,5]` and `[7,5]`;
- one native door at `[8,4]` with no `FurnitureData` binding;
- exactly three native entry actors at `[8,4]`, using the native initial position `[280,-31]` in the evidence contract;
- a separate display policy reserves `[4,6]`, `[5,6]`, and `[7,6]` for those same three actors and keeps them idle so the room map is easy to inspect.

The native entry positions remain evidence-only in this presentation mode; the visual gate checks the three reserved display cells, the six native furniture compositions, both structural facility pads, and final canvas visibility. Historical display-slice labels remain only in retained evidence and asset-package provenance; they are not production routes.

## Commands

Run from this directory:

```powershell
npm install
npm run typecheck
npm test -- --run
npm run build
npm run dev
```

The deterministic browser fixture uses `http://127.0.0.1:4173/?auto=0`. The screenshot and behavior-trace evidence are stored under `knowledge/fixtures/accepted/`.
The asset gate is `knowledge/fixtures/accepted/display_asset_gate.json`; the runtime imports only the generated pack facade and the exact binaries under `assets/display-slice-01/`.

The single floor policy is `raw 5 → selector/metadata 85/floor_09.png → render floor_05.png`. The `floor_05.png` asset is complete and remains the actual rendered image; `floor_09.png` supplies the borrowed selector/data identity. The composition is explicitly labeled synthetic because the original `img.inf` binding for raw id `5` remains unresolved.

## Native Room.floor_ topology

`knowledge/fixtures/accepted/runtime/native_room_floor_usage_contract.json` is the runtime bridge for the native `Room.floor_` selector. It records the direct constructor call sites and the exact native dimensions:

- `floor == 0` selects `MAPCHIP_ARRAY[0]` and the full `14×14` topology;
- `floor != 0` selects `MAPCHIP_ARRAY[1]` and the native `4×4` preview topology;
- `RoomData.floorImgId_` remains an independent `FLOOR_IMAGE_ID_ARRAY` lookup;
- the resolver rejects a nonzero floor requested at `14×14` instead of expanding the native `4×4` row.

The native environment scope is also fixed in the retained contract evidence under `knowledge/fixtures/accepted/runtime/`:

| Runtime context | Native topology | Outer MapChip scope |
|---|---|---|
| `main_display` | `floor_0`, `14×14` | present, native |
| `persistent_room` | `floor_0`, `4×4` | not present |
| `addition_floor_preview` | `floor_nonzero`, `4×4` | not present |

Non-main contexts never receive a synthetic `14×14` garden/road surround. The unified production route fixes `main_display` with `nativeFloor=0`; persistent-room and addition-floor-preview remain evidence-contract contexts rather than alternate browser routes.

A UI framework is intentionally not required. A framework may be added around the presentation shell later without changing the simulation core.
