# Social Dev Phase 3 — Display Runtime Report

Date: 2026-08-14
Status: **Phase 3C strict default-map visual closure reopened after native-game screenshot review**
Scope: `display-slice-01`

## Outcome

The approved pre-runtime boundary has been promoted into a Vite/TypeScript browser runtime under `runtime/social-dev/`. The implementation contains a pure deterministic core, a contract-backed room projection, a Canvas 2D renderer, a DOM/CSS diagnostics shell, and browser-trace evidence.

The runtime imports only approved JSON contracts. Decompiled C# and source/extraction roots are not runtime imports.

Phase 3C has a deterministic render contract and strict native-closure package, but the previous image-level default-entry gate is superseded by the supplied native-game screenshots. The source chain proves `AppData.NewGame` selects `roomData_[0]` and constructs a `14×14` room; the `10×10` `objMap_` is the ObjChip occupancy grid, not the complete floor. The current Canvas now keeps those layers separate, uses the source-backed exterior map chips, puts the verified wall/door bindings on the room boundary, and anchors actors through the native door formula. Exact native `MapChip.Draw` boundary composition and a fresh image-level acceptance gate remain before visual closure or baseline approval.

## Default-entry reconstruction

The supplied Gemini explanation was useful as a selector summary but was corrected against the native source evidence. The verified bootstrap is `AppData.NewGame → Room(14,14,0,roomData_[0]) → Room.PlaceDesk(0) → FLAG_INIT_PLACE scan`. `Room.PlaceDesk` scans `FLAG_INIT_DESK=16384` and fills empty raw type-2 cells. The later `FLAG_INIT_PLACE=32768` scan fills the first empty raw type-1 cells. Raw door type `5` is handled separately by `Room.PlaceDoor` with null FurnitureData. `TryPlace` validates a user placement and is not the default bootstrap path.

The resulting strict room:0 binding matrix is Wooden Desk (`furniture:3`) at `[2,4]`, `[3,4]`, and `[6,4]`; Trash Can (`12`) at `[8,5]`; Old Printer (`26`) at `[8,6]`; Calendar (`56`) at `[2,7]`; and the raw door at `[8,4]`. The runtime renders these cells with the verified wall/door records and depth-sorts foreground wall/door sprites after actors at their source-backed depth. The default visual uses source-backed `floor_05.png` pixels with explicit selector/data metadata `85/floor_09.png`; the raw selector remains unresolved and is not relabeled as recovered provenance.

## Implemented boundaries

- Contract loader rejects non-`pass` or non-`approved_for_runtime_contract` inputs and cross-checks catalog/fixture hashes.
- Initial state consumes the source-bounded three-actor spawn fixture at cell `(8,4)` and verifies the derived position `(280,-31)`.
- Fixed tick order follows the approved sequence: increment frame, update actors in stable ID order, update object bindings/reservations, and commit an immutable snapshot.
- The closed route fixture is preserved exactly as `(8,4) → (7,4) → (6,4)`.
- The bounded living trace emits `idle`, `move`, `arrive`, `work_or_equipment`, `talk`, `talk_marker`, and `talk_end` events.
- Snapshot digests are stable for identical tick inputs; UI actor selection changes selection state without advancing the frame.
- Canvas renders the two-grid default map, source-backed floor/exterior chips, native wall/door source records, the native initial furniture matrix, route, selector-backed actor/world frames, animation selector IDs, and talk bubbles. Selector-only objects remain visible in diagnostics rather than being guessed into the room; the debug raw-map overlay is disabled in the default presentation.
- DOM/CSS exposes frame, actor count, digest, selected actor, event trace, and contract status.
- Coordinate and render-plan tests pin the map-chip, object, and actor projections plus the exact source draw-pass identifiers consumed by the runtime.

## Asset/frame gate

The separate gate is `knowledge/fixtures/accepted/display_asset_gate.json`. It is now `pass` / `approved_for_runtime_subset`: `18` entries passed and `0` remain blocked. The runtime manifest at `knowledge/fixtures/accepted/runtime/display_asset_manifest.json` contains only the approved subset, including the four wall/door binaries and the native initial-object entries promoted after strict composition proof.

The runtime now promotes and loads `30` exact source binaries: the previous actor/world subset plus `wall_00.png/.seb`, `door_01.png/door_02.seb`, and the native initial-object assets. Human SEB records are validated against the selected `270×60` character strips. The OPT codec reconstructs exact logical atlases for `desk_00`, `chair_00`, `chair_02`, `chair_04`, and the `door_03` selector through its `door_02` source mapping, matching the supplied comparison images pixel-for-pixel. The browser adapter consumes manifest frame records and the strict native sprite records; selector-only furniture remains outside the room projection.

`furniture:2` is approved because the original `chair_00.opt` is a variable-piece payload with cells `[1,2,1]`; the former 14-byte “tail” is the second crop descriptor of the middle cell. The missing room floor `chip/img.inf` slot is preserved as an unresolved index; the fixed runtime policy borrows selector/data `5 → 85 → floor_09.png` while rendering the complete `floor_05.png` asset. Native initial bindings are now proven for Wooden Desk (`furniture:3`, three type-2 cells), Trash Can (`12`), Old Printer (`26`), and Calendar (`56`). Selector rows `furniture:2` and `furniture:5` have no native room:0 bootstrap placement call and remain explicitly unplaced.

## Evidence

- Screenshot baseline: `knowledge/fixtures/accepted/display_slice_01_screenshot_baseline.png`
- Browser behavior trace: `knowledge/fixtures/accepted/display_slice_01_behavior_trace.json`
- Phase 3C render fixture: `knowledge/fixtures/accepted/phase3c_render_fixture.json`
- Phase 3C render contract: `knowledge/fixtures/accepted/runtime/phase3c_render_contract.json`
- Phase 3C browser visual gate: `knowledge/fixtures/accepted/phase3c_browser_visual_gate.json`
- Candidate browser screenshots: `knowledge/fixtures/accepted/phase3c_candidate_frame_6.png` and `knowledge/fixtures/accepted/phase3c_candidate_frame_136.png`
- Strict closure package: `knowledge/fixtures/accepted/phase3c_strict_closure.json` (package hash `7a7073f27e72ed87509080ac7f2526736a476101794a2ce012aaddb872a3dbd5`; `ObjChip.DrawWall` RVA `0x12C0698`)
- Strict closure contract/validation: `knowledge/fixtures/accepted/runtime/phase3c_strict_closure_contract.json` and `knowledge/fixtures/accepted/phase3c_strict_closure_validation.json`
- Superseded strict browser gate (retained for provenance): `knowledge/fixtures/accepted/phase3c_strict_browser_visual_gate.json`
- Image-level default-entry gate: `knowledge/fixtures/accepted/phase3c_visual_fidelity_gate.json`
- Fresh default-entry screenshot: `knowledge/fixtures/accepted/phase3c_default_entry_smoke_frame_0.jpg`
- Fresh frame-136 screenshot: `knowledge/fixtures/accepted/phase3c_visual_fidelity_smoke_frame_136.jpg`
- Browser fixture: `http://127.0.0.1:4173/?initialTicks=136&auto=0`
- Canvas: `980×600`; frame-6 digest `47bf1dfa3d2fbc59`; frame-136 digest `1fe49b91bd27c5fa`
- Default-entry frame: `0`; digest `ceb7009453ac8858`
- Final behavior frame: `136`
- Talk markers: `20`, `70`, `110`
- Talk end: `130`
- Final digest: `1fe49b91bd27c5fa`
- Display asset status: `ready`
- Browser console errors: `0`

## Verification

```text
npm run typecheck       pass
npm test -- --run       10 files / 22 tests passed
npm run build           pass
python tools/social-dev/test_phase3c_strict_closure.py pass (10/10 checks; 6 native initial bindings)
python tools/social-dev/test_phase3c_render_contract.py pass (12/12 checks)
python tools/social-dev/test_phase3b_floor_recovery.py pass (22/22 checks; source-limited unresolved)
python tools/social-dev/test_display_asset_gate.py     pass (10/10 checks; 18 approved; 0 blocked; 30 promoted)
python tools/social-dev/test_pre_runtime_closure.py    pass (21 items; 13 verified; 2 quarantine)
python tools/social-dev/test_opt_codec.py              pass (variable-piece `chair_00` and `chair_04` cases)
python tools/social-dev/test_phase3a_chair_00_reconstruction.py pass (`411/411` OPTs, `89/89` references)
```

The historical image-level default-entry gate remains superseded by the supplied native-game screenshots. A fresh browser smoke now loads the repaired default visual with `display assets ready`, canvas `980×600`, no page error, visible floor/exterior/wall/door/native-initial-furniture composition, and the deterministic frame-0 digest. This is not a replacement image-level gate and no baseline replacement was persisted because comparison-policy approval is not recorded.

The existing Python evidence gates also remain green: pre-runtime closure `21/21`, Phase 1D `18/18`, SceneCatalog `22/22`, ObjectCatalog `29/29`, ActorCatalog `35/35`, and Phase 2C readiness `12/12`.

## Explicit limitation

The scoped native evidence is available, but the remaining strict gate requires exact reconciliation of the `MapChip.Draw` boundary pass and an explicit image-level comparison decision. The historical placeholder baseline must not be overwritten until a comparison-policy approval is recorded. The floor image remains a fixed borrowed-data visual composition rather than recovered selector provenance; no alternate fallback or hybrid mode is exposed. `furniture:2` and `furniture:5` remain selector-only because the reviewed room:0 bootstrap has no native FurnitureData placement call for those rows; no derived chair approximation is represented as an original runtime asset.

## Next boundary

The topology repair is implemented and verified at the contract/runtime level, but strict Phase 3C visual closure is still open. Next: reconcile the remaining native boundary sprites, capture the fresh default-entry gate, and record whether a candidate may replace the historical placeholder baseline. Phase 3A exact reconstruction and Phase 3B native room evidence remain authoritative; expansion beyond `display-slice-01` must wait for that decision.
