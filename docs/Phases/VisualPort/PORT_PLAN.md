# Visual Port Plan V0–V9

This plan is deliberately staged. Every phase has a parity gate; the next phase cannot start when the preceding gate is only visually plausible or only covered by current-runtime tests.

## Ordered phases

| Phase | Scope | Original classes/methods | Unity/browser boundary | Parity gate before next phase |
|---|---|---|---|---|
| V0 | Audit and evidence package | All classes in the class/method maps; native method bridge and gaps | No runtime change | JSON parses; all graph endpoints/references resolve; six dispositions are used consistently; source roots remain unchanged; native/asset conflicts are explicit. |
| V1 | Core format recovery | `Sprite` fields/accessors; `Seb.GetSprites`, `GetSprite`, `Frame`, bounds; `Image.LoadOptimize`, `GetOptimize`, `GetOptimizeSeb`; critical `ResourceManager` lookups | Browser byte/image storage may replace Unity objects only behind `Image`/resource adapters | OPT and SEB fixtures reproduce source dimensions, sprite crop, translation, flip, layer order, bounds, and frame selection byte-for-byte or pixel-for-pixel. |
| V2 | Graphics backend | `Graphics.SetClip`, `GetClip`, `SetColor`, `Scale`, `DrawImage`; `Seb.Draw*`/`Render*` | Replace Unity texture, clip, color, scale, blend, and draw calls with a browser backend | Native-vs-browser raster fixtures agree for clip, alpha/color, scale, flip, anchor, and source/destination rectangles. |
| V3 | Resource group parity | `ResourceManager.LoadImage`, `LoadSeb`, `Load`, `LoadReady`, `LoadStart`, `GetImage`, `DrawSeb*`; `ImageAtlas*` | Replace file/stream loading and atlas storage; preserve `resChip_`, `resHuman_`, `resGame_`, and other group identity | A traced group load resolves the same image/SEB IDs and resource lifetime states as the native fixture; no manifest-only shortcut is accepted. |
| V4 | Map/object visual extraction | `MapChip.Draw`, `DrawFloor`, `DrawExtentionFloor`; `ObjChip.DrawWall`, `Draw`, direction/parent/standing methods; `FurnitureData.Draw`; `Camera` methods | Browser scene adapter receives original visual state; backend remains V2/V3 | Native map/object fixtures match projection, floor/extension ordering, wall layers, object direction, parent/child offsets, and furniture frame. |
| V5 | Room orchestration | `Room.InitMapChips`, `InitObjChips`, `SetupBigChipsParent`, `PlaceDoor`, `InitStaffs`, `Draw`, coordinate helpers | `GameForm`/host supplies screen and camera boundary; no gameplay loop required | One native room trace and one multi-cell/door fixture match grid topology, nine-pass order, draw calls, and camera offsets. |
| V6 | Character visual layer | `Staff.Init`, `ChangeSeb`, `Draw`, `DrawScale`, `DrawStaff`, `SetPos`, `AdvanceSebFrame`; `StaffData` selectors | Browser host supplies time tick; no jobs/economy/path planner | One identity’s idle/walk/action/direction/scale/alpha/frame traces match native frames and timing; only then broaden identities. |
| V7 | Golden room closure | Room + map/object + one or more characters through `Main.OnDraw`/`GameForm.Draw` | Replace lifecycle/surface only; reuse current bounded room as a comparison fixture | Native captured frame, recovered pipeline frame, and existing floor00 closure compare at the pixel/resource-call level with documented intentional aliases. |
| V8 | Full visual resource coverage | Remaining resource groups, helper/avatar/effect/window assets, atlas cases, full selector coverage | Browser backend handles the recovered resource surface | Every promoted group has native load evidence, source-format fixture, and raster/call parity; unresolved assets stay `UNKNOWN`. |
| V9 | Thin AI adapter | Recovered visual contracts only; no original gameplay class port | AI supplies scene fixture/state through a stable adapter | AI can provide room/object/staff visual state without owning renderer semantics or bypassing ResourceManager/SEB/Sprite contracts. |

## Native recovery methods

The first recovery set is the pinned bridge in `native-method-map.json`: `Graphics` draw primitives, `Sprite` getters, `Image` OPT methods, `Seb` frame/draw methods, `ResourceManager` load/draw methods, and native `Room`/`ObjChip`/`MapChip`/`Staff` draw entry points. `GameForm`/`Main` lifecycle traces are needed only when they affect visible order or dimensions.

## Artifacts to reuse

- OPT/SEB codecs and catalog builders under `tools/social-dev/`.
- Asset fingerprint and assembly guides under `knowledge/fixtures/accepted/asset_guide_20260813/`.
- Native scene, strict closure, room placement, and render contracts under `knowledge/fixtures/accepted/runtime/`.
- Character metadata/capability contracts and existing bounded runtime tests as fixtures.
- The current two-grid projection and native pass names as comparison evidence, never as replacement authority.

## Runtime components eventually eligible for retirement

Only after V7/V8 gates pass may the direct manifest selector, bounded frame selection helpers, room-specific projection/render plan, and duplicate Canvas draw paths be replaced by the recovered contracts. No current module is deleted or changed by V0.

## Implementation order rule

Do not start V1 while the V0 consistency gate is red. Do not start a later phase because a current browser screenshot looks correct. Each gate must cite the native method trace, source-format fixture, and browser output that establish the specific parity claim.
