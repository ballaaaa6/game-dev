# Floor00 Visual Layout Alignment Design

**Status:** Proposed implementation design based on the user-approved visual target.

## Goal

Adjust only the `floor00` presentation layout so it more closely matches the supplied game screenshot:

- remove the blue-marked glass area on the left;
- remove the purple-marked translucent panel;
- remove the blue-marked glass area on the right;
- extend the upper wood wall instead of using glass there;
- keep a long, continuous glass wall along the remaining side edge;
- move the green-circled wood wall one cell backward so the upper and left wall edges align.

## Context and evidence

The current runtime already separates the native 14×14 `MapChip` grid from the 10×10 `ObjChip` grid. The pale glass visual comes from the `wall_01.png` / `wall_ex.seb` extension-wall composition, while the brown room wall comes from the `wall_00.png` / `wall_00.seb` `ObjChip.DrawWall` composition.

The native contracts and raw scene evidence remain authoritative for topology, raw cell values, FurnitureData identity, wall SEB layers, and draw-pass order. The requested change is a presentation adjustment to the explicit `floor00` comparison scene, not a claim that the recovered native room data is different.

## Design decisions

### 1. Use a floor00-only visual layout contract

Create `knowledge/fixtures/accepted/runtime/floor00_visual_layout_contract.json`. It will reference the existing native scene and asset contracts and contain concrete, deterministic cell arrays for:

- glass extension pieces to remove in the left blue zone, purple panel zone, and right blue zone;
- the remaining glass trigger cells that form the long side strip;
- any additional adjacent trigger cells needed to make that strip continuous;
- the selected upper/green-circled wood wall cells;
- the one-cell backward offset for that wall group;
- the extra wood wall cells needed to make the upper wall continuous;
- the required edge-alignment relationship between the upper and left wall endpoints.

The contract will use existing `wall_01` frame records and existing `wall_00` SEB layer records. It will not introduce new raster artwork, mutate raw room evidence, or use screen-space paint masks.

The contract must record the final resolved cell arrays and offset explicitly. Runtime code must not infer the layout from colors, screenshot pixels, or an unconstrained heuristic.

### 2. Apply the override only to the floor00 scene projection

The runtime loader will validate the new contract against the existing catalog and expose a resolved presentation layout only when both conditions are true:

```text
sceneId === "room:0"
sceneMode === "floor00"
```

`display-slice-01`, other room selections, persistent-room contexts, and addition-floor previews will continue to use their existing native projections.

The resolver/projection boundary will apply the override as follows:

- filter the native extension-wall pieces using the contract's removal list;
- add only the contract-approved adjacent glass pieces for the long strip;
- replace the floor00 wall cell scope with the explicit shifted/extended wood-wall cell scope while preserving every `wall_00.seb` layer and layer order `0 → 1`;
- leave raw ObjChip placements, collision classifications, furniture bindings, door binding, actor cells, structural facilities, and map-floor assets unchanged.

### 3. Preserve native render-pass semantics

The nine existing pass identifiers remain unchanged. The resulting draw order remains:

```text
background
map-chip-and-map-floor-underlay
map-extension-floor-pale-boundary
object-chip-wall-rear-door-and-wall
object-chip-primary-native-furniture
avatar-primary-static-floor00-display-actors
object-chip-late-foreground-wall
diagnostic-overlay
```

Glass remains in `map-extension-floor`; shifted/extended wood remains in the existing wall pass. The foreground wall split and all native wall layers remain explicit so the change cannot hide furniture or actors through a global sort change.

### 4. Keep the existing asset lifecycle gate

The floor00 route will continue to wait for approved PNG/SEB assets. If the new contract references a missing asset or an out-of-bounds frame, the route must report a pending/blocked asset state and draw no guessed replacement. The existing `wall_00.png`, `wall_00.seb`, `wall_01.png`, and `wall_ex.seb` assets are the only visual inputs for this change.

## Runtime data flow

```text
native scene/asset contracts
        ↓
floor00_visual_layout_contract.json
        ↓
validated floor00 resolver output
        ↓
SceneProjection wall/extension scopes
        ↓
existing Canvas render passes
        ↓
visual gate + browser screenshot
```

The raw native contracts remain the source of truth for evidence. The new contract is a user-approved presentation policy layered on top of that evidence.

## Candidate approaches considered

1. **Modify the native room or MapChip contracts directly.** This would be shorter, but it would overwrite evidence-backed topology and could change all-room behavior. Rejected.

2. **Add a floor00-only visual layout contract.** This isolates the requested comparison-scene change, preserves native provenance, reuses the existing SEB crops, and gives the visual gate concrete IDs to verify. Recommended.

3. **Mask or repaint pixels directly in Canvas.** This would be quick for a single screenshot but would be fragile under scaling, break visibility diagnostics, and make wall/furniture occlusion incorrect. Rejected.

## File-level design surface

### Create

- `knowledge/fixtures/accepted/runtime/floor00_visual_layout_contract.json` — deterministic presentation override and provenance references.

### Modify

- `runtime/social-dev/src/catalog/types.ts` — typed contract boundary.
- `runtime/social-dev/src/catalog/load-contracts.ts` — load and validate the contract.
- `runtime/social-dev/src/scene/room-resolver.ts` — resolve the floor00 glass selection and wall cell scope.
- `runtime/social-dev/src/scene/projection.ts` — expose the resolved presentation layout without changing raw room cells.
- `runtime/social-dev/src/renderer/canvas-renderer.ts` — consume the resolved scopes through the existing render passes; no raster masking.
- `runtime/social-dev/src/renderer/visual-gate.ts` — verify removal, continuity, alignment, final visibility, and unchanged lifecycle behavior.
- Relevant room/extension/visual-gate tests under `runtime/social-dev/tests/`.

### Generated evidence

After implementation, store browser screenshots and visual-gate output under `knowledge/fixtures/accepted/` using the existing Social Dev evidence boundary. Do not create generated PNG/JSON artifacts at the repository root.

## Acceptance criteria

The implementation is accepted when all of the following are true for `?scene=floor00&auto=0`:

1. No glass pixels or glass draw-trace IDs remain in the three user-marked removal zones.
2. The purple translucent panel is absent.
3. The upper wall is rendered with the brown `wall_00` composition and extends continuously across the requested span.
4. The remaining glass is a continuous long side strip made from approved `wall_01` two-piece compositions.
5. The green-circled wall is displaced exactly one contract-defined cell backward and its endpoint alignment with the upper/left wall passes the visual alignment check.
6. All wall SEB layers, including the 2px thin layer, remain drawn in layer order `0 → 1`.
7. Furniture, structural facilities, actors, door, tree, floor, and foreground-wall occlusion remain visible and deterministic.
8. The legacy `display-slice-01` route and non-floor00 room projections remain unchanged.
9. Vitest, TypeScript typecheck, production build, `git diff --check`, and the browser visual gate pass with zero console errors or warnings.

## Verification strategy

- Add unit assertions for the contract's concrete remove/retain/add cell sets and the one-cell wall offset.
- Add projection assertions that floor00 receives the override while the legacy route does not.
- Add render-trace assertions for the new glass and wood IDs, including their pass and layer order.
- Capture two consecutive fixed-frame floor00 screenshots and compare their content hashes for determinism.
- Inspect the resulting browser capture against the supplied reference image for the three removals, the continuous upper wood wall, the long side glass strip, and the one-cell alignment.
- Run the complete runtime test/typecheck/build suite before handoff.

## Non-goals

- No recovery or rewriting of missing native source bindings.
- No promotion of the unresolved red/black live-game prop.
- No change to FurnitureData identity or collision rules.
- No change to the historical display baseline.
- No change to rooms 1–17 or to non-floor00 contexts.
