# K3 Targeted Missing-Link Closure

Status: **CLOSED**

Final validation token: `PASS_K3_TARGETED_MISSING_LINK_CLOSURE_CLOSED`

This closure is limited to the three queued K3 gaps. V8, deployment, network
research, persistence/backend work, live app/server work, integrations, and
MapChip pixel changes were not started.

## Closed evidence

- Floor: `ROOMDATA_FLOOR_IMAGE_INDEX:5` loads `RoomData.floorImgId_` at native
  field offset `0x48`; `Room.FLOOR_IMAGE_ID_ARRAY[5]` is
  `IMAGE_SELECTOR_ID:23`, which resolves through `chip/img.inf` to
  `floor_05.png`. The runtime compatibility alias `COMPATIBILITY_ALIAS_ID:85`
  remains explicit and separate.
- FurnitureData 26: raw row 26 is a type-1 object with
  `SEB_SELECTOR_ID:21`, `IMAGE_SELECTOR_ID:106`, secondary sentinel `-1`, and
  accepted native initial frame `SPRITE_FRAME_ID:furniture:26:0`.
- Candidates: all 185 candidate records are
  classified exactly `CONFIRMED` or `REJECTED`; unresolved count is
  0. The HelperData
  130–140-looking claims are rejected as direct human-selector claims and
  corrected through `STAFF_DATA_ID` to `StaffData.img_`.

## Artifacts

- `knowledge/brain/acceptance/k3/gap-resolution.json`
- `knowledge/brain/acceptance/k3/evidence-manifest.json`
- `knowledge/brain/acceptance/k3/query-results.json`
- `knowledge/brain/acceptance/k3/final-validation.json`
- `knowledge/fixtures/accepted/runtime/k3_floor_selector_closure.json`
- `knowledge/fixtures/accepted/runtime/k3_furniture_visual_closure.json`
- `knowledge/fixtures/accepted/runtime/k3_candidate_edge_classification.json`

## Regression boundary

- K2 unified brain validation remains `PASS_K2_UNIFIED_WHOLE_GAME_BRAIN_AND_RUNTIME_PACK_CLOSED`.
- The K2.5 baseline remains archived as a zero-semantic-delta, legacy-offline-safe snapshot; the original-data database hash is preserved.
- Native registry/catalog/floor/display gates, runtime typecheck, and the full Vitest suite (`48` files / `314` tests) pass.
- The active semantic change is limited to these three K3 gaps. Legacy material remains inactive, and V8, deployment, integrations, persistence/backend work, network research, emulator/ADB/live app, local server, subagents, and MapChip pixel modification remain unopened.
