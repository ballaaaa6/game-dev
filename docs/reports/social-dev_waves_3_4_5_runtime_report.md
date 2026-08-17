# Social Dev Waves 3/4/5 Runtime Report

## Outcome

Waves 3, 4, and 5 are implemented and connected in the active Social Dev runtime. The implementation is evidence-first: source selector identity, logical reconstruction, physical runtime files, room records, resolver output, and render passes remain separate contracts with explicit provenance.

The runtime now supports all `18` RoomData records through one room selector. It resolves `1,800` native 10x10 ObjChip cells, links every room to the shared MapChip topology, promotes `23` exact room floor/wall/door selector assets, and connects every room to the native wall/door coordinate composition and render trace. It never derives MapChip identity or FurnitureData identity from ObjChip occupancy.

## Wave 3 — Logical and physical asset closure

The display asset gate now distinguishes three identities:

1. The native/source selector and archive member.
2. The logical image reconstructed from OPT/SEB evidence.
3. The physical PNG that the browser actually loads.

OPT-backed furniture is reconstructed into deterministic RGBA PNGs under `runtime/social-dev/assets/display-slice-01/02_DERIVED_READY_IMAGES/opt_reconstructed/chip/`. The manifest records both source and runtime asset IDs, runtime dimensions, runtime status, and derivation provenance. Every frame rectangle is checked against the physical runtime PNG rather than the source descriptor alone, preventing out-of-bounds source crops from causing flicker or silent fallback.

The final display gate is `pass`: `18` approved entries, `0` blocked entries, and `34` promoted runtime binaries. The four derived runtime images are `chair_00.png`, `chair_02.png`, `desk_00.png`, and `door_02.png`.

## Wave 5 — All-room resolver and identity bridge

`tools/social-dev/build_room_scene_asset_manifest.py` promotes exact RoomData floor/wall/door selector PNGs into the runtime boundary. The resulting manifest contains `18` rooms and `23` unique selector assets: `10` floors, `7` walls, and `6` doors.

`tools/social-dev/build_room_scene_runtime_contract.py` produces the runtime room contract. Each room record contains:

- the native RoomData row and source hash;
- the raw `objMap`/`objDir` cells and raw type groups;
- exact floor/wall/door selector identity;
- the shared MapChip contract link;
- explicit native bindings only where native placement evidence exists;
- an explicit current runtime `Room.floor_=0` MapChip selection;
- closed generic native wall/door predicates, SEB records, anchors, and exact room selector assets.

The resolver in `runtime/social-dev/src/scene/room-resolver.ts` applies this policy at runtime. Room `0` uses the closed native furniture bindings. Other rooms expose their raw placements and exact selector assets without inventing FurnitureData IDs or actor placement, while the native direction mapping and generic wall/door composition are applied from `native_scene_assembly_contract.json`.

Direction values are preserved as raw native values and now carry the closed native mapping: `0 → DIRECTION_RIGHT → (0,1)`, `1 → DIRECTION_LEFT → (0,-1)`, `2 → DIRECTION_UP → (1,0)`, and `3 → DIRECTION_DOWN → (-1,0)`, with reverse table `[1,0,3,2]`. Rotation and directional asset selection remain disabled because the native trace closes the vector API, not a separate directional sprite policy.

## Item 6 — Room R raw scene fixture

Room R is `room:17`. Its fixture is generated from the complete native RoomData catalog and runtime room contract, not from a guessed furniture layout. It contains the full `10×10` ObjChip grid (`100` cells), raw type and direction values, raw status values, the door cell at `(8,3)`, and `0` native FurnitureData bindings. The runtime contract keeps the shared `14×14` MapChip topology separate from the raw ObjChip fixture.

`runtime/social-dev/src/scene/room-overlay.ts` cross-checks the fixture against the runtime room record and exposes a diagnostic-only overlay through `?room=room:17&overlay=raw`. Each overlay card retains the raw cell ID and `instance_id=null`; no FurnitureData, direction label, wall coordinate, or door coordinate is inferred from it.

## Item 7 — Structural visual gate

`phase3c_visual_gate_v2` remains the historical room:0/Room R structural artifact. The active `phase3d_all_room_assembly_gate` passes all `18` rooms: every room reaches `asset_status=ready`, `gate_status=pass`, zero unresolved entries, zero console errors/warnings, `16` native wall/door draws, and zero furniture fallbacks. Room R additionally passes the `100/100` raw-overlay cross-check when the diagnostic overlay is enabled.

The gate also caught a renderer defect: direct native image frames carrying `source_status=pass_native_img_asset` but no `runtime_status` were treated as fallback images. The renderer now accepts either approved runtime status or the approved native-image source status, and the furniture diagnostics prove the corrected room:0 path. The evidence package includes content-addressed screenshots for room:0 frames `0/1/2` and the Room R raw overlay; the historical visual baseline remains preserved.

## Wave 4 — Render topology and ordering

`runtime/social-dev/src/renderer/render-plan.ts` defines the nine native render pass IDs and rejects contract drift. Canvas rendering now executes passes explicitly:

1. Map extension floor
2. MapChip
3. Primary ObjectChip
4. Wall ObjectChip
5. Primary avatar
6. Secondary avatar
7. Late preview ObjectChip
8. Late ObjectChip
9. Map floor

Map extension walls are drawn in their declared pass. The previous global cross-layer sort is removed; sorting is limited to the individual pass that owns the drawables. Background rendering is anchored to the source-backed day strip instead of an ad-hoc opaque fill.

## Connected runtime flow

```text
RoomData / native registry
        ↓
room-scene asset manifest + room-scene runtime contract
        ↓
room-resolver(roomId)
        ↓
SceneProjection + explicit render-pass plan
        ↓
Canvas renderer + room selector UI
```

`load-contracts.ts` validates and exposes all contracts through `RuntimeCatalogs`. `display-assets.ts` loads both the approved display subset and the exact all-room selector assets. The UI can switch among `room:0` through `room:17`; rooms without native actor bindings remain actor-free rather than receiving invented actors.

The complete runtime identity bridge is `knowledge/fixtures/accepted/runtime/native_content_catalog.json`: it exposes `3,693` native data records, `3,542` assets, `3,192` selectors, `523` data-selector links, `4,596` selector/companion links, `250` consumer links, and `43` lifecycle links. The assembly bridge is `knowledge/fixtures/accepted/runtime/native_scene_assembly_contract.json`; it maps those identities into the native `DataManager → AppData.NewGame → Room → MapChip/ObjChip → PlaceDoor/PlaceDesk → Draw/Update/Serialize` chain.

`runtime/social-dev/src/catalog/native-content.ts` provides the runtime lookup surface for a native data ID, selector key, or asset ID and returns the connected graph edges for that identity. This is the callable handoff for later user-directed changes; callers do not need to parse source files or search the catalog manually.

## Verification

- `display_asset_gate_test_passed checks=10 approved=18 blocked=0 promoted=34`
- `room_scene_asset_manifest_test_passed rooms=18 assets=23`
- `room_catalog_test_passed rooms=18 objchip_cells=1800 mapchip_linked=18`
- `phase3b_room_placement_test_passed checks=20`
- `phase3c_render_contract_test_passed checks=12/12`
- `native_content_registry_test_passed data_rows=3693 assets=3542 selectors=3192 consumer_edges=250`
- `native_content_catalog_test_passed records=3693 assets=3542 selectors=3192`
- `native_direction_contract_test_passed domain=4 vectors=4 reverse_table=1,0,3,2`
- `native_scene_assembly_contract_test_passed rooms=18 cells=1800 passes=9`
- `phase3d_all_room_assembly_gate_test_passed rooms=18`
- TypeScript typecheck passed.
- Vitest passed: `13` files, `30` tests.
- Vite production build passed; the remaining bundle-size warning is non-blocking.
- Browser smoke verified room `0` through room `17`; every room loaded its selector assets, passed the native composition gate, emitted the expected wall/door trace, had zero unresolved entries and zero console errors/warnings. The v2 evidence test also verifies all four historical screenshot hashes.

## Remaining closure gates

The requested Wave 3/4/5 connection closure has no remaining runtime gate. The historical baseline is explicitly preserved and is not overwritten. Any future baseline replacement or additional FurnitureData placement is a new user-directed product decision; it is outside the completed assembly chain.

The current runtime retains the raw/source provenance boundaries deliberately: the floor selector `5` uses the fixed `85/floor_09` metadata alias with `floor_05` render pixels, and rooms without native initial FurnitureData bindings remain empty in those slots. Neither condition is an unresolved connection or a silent fallback.
