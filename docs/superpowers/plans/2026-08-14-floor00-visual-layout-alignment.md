# Floor00 Visual Layout Alignment Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a deterministic `floor00`-only presentation layout that removes the user-marked glass zones, extends the upper wood wall, keeps one long side glass strip, and shifts the green-circled wall one cell backward without changing native room evidence or other scene modes.

**Architecture:** Load a new typed visual-layout contract beside the existing native contracts. A focused scene-layout adapter will validate and project the contract's final glass trigger cells and wood-wall cell scope only when `room:0` is rendered in `floor00` mode; the existing Canvas passes will consume those projected scopes without raster masking or changes to the native pass order.

**Tech Stack:** TypeScript 5.9, Vite 7, Canvas 2D, Vitest 3, JSON runtime contracts, PowerShell verification, browser screenshot/console smoke.

## Global Constraints

- Keep the native `MapChip`/`ObjChip` evidence and source roots read-only; the new contract is a presentation policy layered on top.
- Apply the override only when `sceneId === "room:0"` and `sceneMode === "floor00"`.
- Reuse only the approved `wall_00.png`/`wall_00.seb` and `wall_01.png`/`wall_ex.seb` assets; do not generate replacement raster artwork.
- Preserve all `wall_00.seb` layers in layer order `0 → 1`, including the 2px thin layer.
- Do not infer FurnitureData identity, change collision rules, promote the unresolved red/black prop, or modify rooms 1–17.
- Keep the nine native render-pass identifiers and the existing asset lifecycle gate unchanged.
- Write new project-owned prose, comments, tests, contracts, and reports in English.
- Put generated screenshots/JSON under `knowledge/fixtures/accepted/`; do not create generated artifacts at the repository root.

---

## File map

| File | Responsibility |
| --- | --- |
| `knowledge/fixtures/accepted/runtime/floor00_visual_layout_contract.json` | Concrete floor00-only glass/wood presentation policy and provenance references. |
| `runtime/social-dev/src/catalog/types.ts` | Type boundary for the new contract. |
| `runtime/social-dev/src/catalog/load-contracts.ts` | Import and cross-validate the contract against native map/assembly/floor00 contracts. |
| `runtime/social-dev/src/scene/extension-wall.ts` | Reuse native wall frame validation while resolving an explicit trigger-cell override. |
| `runtime/social-dev/src/scene/floor00-visual-layout.ts` | Transform native extension/wall scopes into the approved floor00 presentation result. |
| `runtime/social-dev/src/scene/room-resolver.ts` | Apply the result only to the floor00 room projection. |
| `runtime/social-dev/src/scene/projection.ts` | Expose presentation status and final wall/extension scopes. |
| `runtime/social-dev/src/renderer/visual-gate.ts` | Assert removal, continuity, alignment, layer order, and final visibility. |
| `runtime/social-dev/tests/floor00-visual-layout.test.ts` | Contract and adapter unit tests. |
| `runtime/social-dev/tests/floor00-scene.test.ts` | Floor00 projection/bootstrap regression tests. |
| `runtime/social-dev/tests/extension-wall.test.ts` | Native and overridden two-piece glass composition tests. |
| `runtime/social-dev/tests/visual-gate.test.ts` | Gate contract regression tests. |
| `runtime/social-dev/tests/phase3c-strict-browser-visual-gate.test.ts` | Browser-style floor00 final-pixel checks. |

## Interfaces

Add these runtime-owned interfaces in `runtime/social-dev/src/catalog/types.ts`:

```ts
export interface Floor00VisualLayoutContract extends ContractHeader {
  readonly catalog_id: "floor00-visual-layout";
  readonly scene_ref: { readonly id: "room:0"; readonly scene_mode: "floor00" };
  readonly refs: Readonly<Record<string, string>>;
  readonly glass: {
    readonly source_asset_id: "map:chip/wall_01.png";
    readonly frame_ids_by_group: Readonly<Record<string, string>>;
    readonly native_trigger_cells_by_group: Readonly<Record<string, readonly (readonly [number, number])[]>>;
    readonly removed_trigger_cells: readonly (readonly [number, number])[];
    readonly final_trigger_cells_by_group: Readonly<Record<string, readonly (readonly [number, number])[]>>;
    readonly strip_axis: "map_x" | "map_y";
    readonly strip_start: readonly [number, number];
    readonly strip_end: readonly [number, number];
  };
  readonly wood_wall: {
    readonly source_asset_id: "asset:01_GAME_PACKS/chip/wall_00.png";
    readonly source_seb_asset_id: "asset:01_GAME_PACKS/chip/wall_00.seb";
    readonly native_cells_by_frame: Readonly<Record<string, readonly (readonly [number, number])[]>>;
    readonly final_cells_by_frame: Readonly<Record<string, readonly (readonly [number, number])[]>>;
    readonly moved_group: "green_circled_side";
    readonly backward_offset: readonly [number, number];
    readonly layer_order: readonly [0, 1];
  };
  readonly alignment: {
    readonly upper_edge_cells: readonly (readonly [number, number])[];
    readonly left_edge_cells: readonly (readonly [number, number])[];
    readonly expected_screen_delta: { readonly x: number; readonly y: number };
  };
  readonly determinism: { readonly algorithm: string; readonly content_hash: string };
}
```

The contract's `removed_trigger_cells` must be the exact union of the three user-marked removal zones. `final_trigger_cells_by_group` must be the exact retained/extended set that produces the long side strip. `final_cells_by_frame` must be the exact wood-wall scope after the one-cell shift and upper-wall extension. The loader will reject overlap between removed and final glass cells, a non-unit backward offset, invalid frame/group IDs, or cells outside the native 10×10/14×14 bounds.

Add this adapter interface in `runtime/social-dev/src/scene/floor00-visual-layout.ts`:

```ts
export interface Floor00VisualLayoutProjection {
  readonly status: "approved_floor00_visual_layout";
  readonly contractId: string;
  readonly extensionWalls: readonly ExtensionWallPiece[];
  readonly wallCellsByFrame: Readonly<Record<string, readonly (readonly [number, number])[]>>;
  readonly removedGlassCells: readonly (readonly [number, number])[];
  readonly finalGlassCellsByGroup: Readonly<Record<string, readonly (readonly [number, number])[]>>;
  readonly backwardOffset: readonly [number, number];
}

export function resolveFloor00VisualLayout(
  layout: Floor00VisualLayoutContract,
  defaultMap: DefaultMapChipContract,
  nativeWallCellsByFrame: Readonly<Record<string, readonly (readonly [number, number])[]>>,
): Floor00VisualLayoutProjection;
```

Add `readonly presentationLayout: Floor00VisualLayoutProjection | null` to `ResolvedRoomScene`, and expose the same result as `SceneProjection.presentationLayout` so the resolver, renderer diagnostics, and visual gate share one exact shape.

### Task 1: Add and validate the presentation contract

**Files:**
- Create: `knowledge/fixtures/accepted/runtime/floor00_visual_layout_contract.json`
- Modify: `runtime/social-dev/src/catalog/types.ts`
- Modify: `runtime/social-dev/src/catalog/load-contracts.ts`
- Create: `runtime/social-dev/tests/floor00-visual-layout.test.ts`

**Interfaces:**
- Consumes: `DefaultMapChipContract.extension_wall`, `Floor00SceneContract.render_composition`, and the room-0 wall scope from `NativeSceneAssemblyContract`.
- Produces: `RuntimeCatalogs.floor00VisualLayout: Floor00VisualLayoutContract` and the validated contract fields used by Task 2.

- [ ] **Step 1: Write failing contract-loader tests.**

Add tests that import `loadRuntimeCatalogs()` and assert the new contract is loaded with:

```ts
it("loads the approved floor00 visual layout contract", () => {
  const catalogs = loadRuntimeCatalogs();
  expect(catalogs.floor00VisualLayout.catalog_id).toBe("floor00-visual-layout");
  expect(catalogs.floor00VisualLayout.scene_ref).toEqual({ id: "room:0", scene_mode: "floor00" });
  expect(catalogs.floor00VisualLayout.glass.source_asset_id).toBe("map:chip/wall_01.png");
  expect(catalogs.floor00VisualLayout.wood_wall.layer_order).toEqual([0, 1]);
  expect(catalogs.floor00VisualLayout.glass.removed_trigger_cells.length).toBeGreaterThan(0);
  expect(Object.keys(catalogs.floor00VisualLayout.glass.final_trigger_cells_by_group).sort()).toEqual([
    "horizontal_frame_0",
    "vertical_frame_1",
  ]);
});
```

The test must also compare the contract's final trigger-cell map and final wood-cell map against the concrete arrays in the JSON contract, and must assert that the removed-cell set and final-cell set are disjoint.

Add rejection tests by calling the exported `validateFloor00VisualLayoutContract(...)` with a cloned contract object for:

- `scene_ref.id !== "room:0"`;
- `scene_ref.scene_mode !== "floor00"`;
- a glass final cell that also appears in `removed_trigger_cells`;
- a non-unit `backward_offset`;
- a wood cell outside the 10×10 ObjChip bounds;
- a missing `wall_01` group or `wall_00` frame reference.

- [ ] **Step 2: Run the focused test to verify it fails.**

Run from `runtime/social-dev`:

```powershell
npm test -- --run tests/floor00-visual-layout.test.ts
```

Expected: FAIL because the JSON import, `RuntimeCatalogs.floor00VisualLayout`, and validation checks do not exist yet.

- [ ] **Step 3: Add the contract type, import, catalog field, and validation.**

Import the JSON beside `floor00SceneJson` in `load-contracts.ts`, add the field to `RuntimeCatalogs`, and export this validation function from `load-contracts.ts`:

```ts
export function validateFloor00VisualLayoutContract(
  layout: Floor00VisualLayoutContract,
  defaultMap: DefaultMapChipContract,
  floor00: Floor00SceneContract,
  nativeAssembly: NativeSceneAssemblyContract,
): Floor00VisualLayoutContract;
```

Call it immediately after the existing floor00 contract checks. The validation must cross-check the native glass trigger union and native wood cells from the existing contracts instead of trusting duplicated metadata.

The new JSON must include the concrete user-approved cell arrays, the existing asset IDs, the wall layer order `[0,1]`, alignment cell pairs, and a stable hash basis. Do not modify `default_map_chip_contract.json`, `floor00_scene_contract.json`, or `native_scene_assembly_contract.json`.

- [ ] **Step 4: Run the focused test to verify it passes.**

```powershell
npm test -- --run tests/floor00-visual-layout.test.ts
```

Expected: PASS with the contract loaded and all invalid-contract tests rejected by the loader validation.

- [ ] **Step 5: Commit the contract boundary.**

```powershell
git add runtime/social-dev/src/catalog/types.ts runtime/social-dev/src/catalog/load-contracts.ts runtime/social-dev/tests/floor00-visual-layout.test.ts
git add -f knowledge/fixtures/accepted/runtime/floor00_visual_layout_contract.json
git commit -m "feat: add floor00 visual layout contract"
```

### Task 2: Resolve the final glass and wood scopes

**Files:**
- Modify: `runtime/social-dev/src/scene/extension-wall.ts`
- Create: `runtime/social-dev/src/scene/floor00-visual-layout.ts`
- Modify: `runtime/social-dev/src/scene/room-resolver.ts`
- Modify: `runtime/social-dev/src/scene/projection.ts`
- Modify: `runtime/social-dev/tests/floor00-visual-layout.test.ts`
- Modify: `runtime/social-dev/tests/extension-wall.test.ts`
- Modify: `runtime/social-dev/tests/floor00-scene.test.ts`

**Interfaces:**
- Consumes: `RuntimeCatalogs.floor00VisualLayout` from Task 1 and existing native wall/extension contracts.
- Produces: `resolveFloor00VisualLayout(...)` and a `ResolvedRoomScene.presentationLayout` result consumed by the existing renderer.

- [ ] **Step 1: Write failing adapter tests.**

Add tests for the exact approved layout:

```ts
it("removes marked glass cells and creates the continuous side strip", () => {
  const catalogs = loadRuntimeCatalogs();
  const projection = buildSceneProjection(catalogs, "room:0", { sceneMode: "floor00" });
  const layout = projection.presentationLayout;

  expect(layout?.status).toBe("approved_floor00_visual_layout");
  expect(layout?.removedGlassCells).toEqual(catalogs.floor00VisualLayout.glass.removed_trigger_cells);
  expect(layout?.finalGlassCellsByGroup).toEqual(catalogs.floor00VisualLayout.glass.final_trigger_cells_by_group);
  expect(layout?.extensionWalls.every((wall) => !layout.removedGlassCells.some((cell) => cell[0] === wall.triggerCell[0] && cell[1] === wall.triggerCell[1]))).toBe(true);
});

it("uses the shifted and extended wall cell scope only in floor00", () => {
  const catalogs = loadRuntimeCatalogs();
  const floor00 = buildSceneProjection(catalogs, "room:0", { sceneMode: "floor00" });
  const legacy = buildSceneProjection(catalogs, "room:0", { sceneMode: "display-slice-01" });

  expect(floor00.presentationLayout?.backwardOffset).toEqual(catalogs.floor00VisualLayout.wood_wall.backward_offset);
  expect(floor00.sceneAssets.find((asset) => asset.role === "wall")?.cellScope?.cells).toEqual(
    catalogs.floor00VisualLayout.wood_wall.final_cells_by_frame,
  );
  expect(legacy.presentationLayout).toBeNull();
});
```

Extend `extension-wall.test.ts` with a test that resolves the final trigger-cell map using the existing two-piece frame records and verifies each group remains continuous and has exactly two pieces per trigger.

- [ ] **Step 2: Run focused tests to verify they fail.**

```powershell
npm test -- --run tests/floor00-visual-layout.test.ts tests/extension-wall.test.ts tests/floor00-scene.test.ts
```

Expected: FAIL because the adapter, overridden trigger resolution, and `presentationLayout` projection field do not exist.

- [ ] **Step 3: Add explicit trigger-cell override support.**

Refactor `extension-wall.ts` around a shared internal resolver and add:

```ts
export function resolveExtensionWallPiecesForTriggerCells(
  contract: DefaultMapChipContract["extension_wall"],
  sourceAssetId: string,
  triggerCellsByGroup: Readonly<Record<string, readonly Cell[]>>,
): readonly ExtensionWallPiece[];
```

The new function must reuse the existing frame bounds, pair continuity, frame IDs, and piece offsets. It must reject unknown groups and then produce the same `ExtensionWallPiece` shape as the native resolver.

- [ ] **Step 4: Implement `resolveFloor00VisualLayout`.**

The adapter must:

1. verify the contract is for `room:0`/`floor00`;
2. verify the native trigger-cell union matches the current `defaultMap.extension_wall` predicates;
3. resolve only `final_trigger_cells_by_group` into two-piece glass drawables;
4. verify removed glass cells are absent from the final pieces;
5. verify the final wood cells are within the ObjChip grid and preserve the native frame keys;
6. verify `backward_offset` has Manhattan length `1` and matches the moved group metadata;
7. return the final wall scope and alignment metadata without mutating the input contracts.

- [ ] **Step 5: Integrate the adapter into `room-resolver.ts`.**

When `roomId === "room:0"` and `options?.sceneMode === "floor00"`, call the adapter and use its glass pieces and wall cell scope. For every other mode/context, retain the current `buildExtensionWalls(...)` result and native assembly wall cells. Add an explicit `presentationLayout` field to `ResolvedRoomScene` with `null` for unaffected routes.

- [ ] **Step 6: Expose the result through `SceneProjection`.**

Add:

```ts
readonly presentationLayout: Floor00VisualLayoutProjection | null;
```

Populate it from `runtimeRoom.presentationLayout`; keep `sceneAssets.wall.cellScope.cells` pointed at the final floor00 scope so the existing wall renderer draws the shifted/extended wall.

- [ ] **Step 7: Run focused tests to verify they pass.**

```powershell
npm test -- --run tests/floor00-visual-layout.test.ts tests/extension-wall.test.ts tests/floor00-scene.test.ts
```

Expected: PASS, including unchanged legacy projection assertions.

- [ ] **Step 8: Commit the projection change.**

```powershell
git add runtime/social-dev/src/scene/extension-wall.ts runtime/social-dev/src/scene/floor00-visual-layout.ts runtime/social-dev/src/scene/room-resolver.ts runtime/social-dev/src/scene/projection.ts runtime/social-dev/tests/floor00-visual-layout.test.ts runtime/social-dev/tests/extension-wall.test.ts runtime/social-dev/tests/floor00-scene.test.ts
git commit -m "feat: project floor00 visual wall layout"
```

### Task 3: Extend the visual gate and browser-level regression checks

**Files:**
- Modify: `runtime/social-dev/src/renderer/visual-gate.ts`
- Modify: `runtime/social-dev/tests/visual-gate.test.ts`
- Modify: `runtime/social-dev/tests/phase3c-strict-browser-visual-gate.test.ts`
- Modify: `runtime/social-dev/tests/floor00-scene.test.ts`

**Interfaces:**
- Consumes: `SceneProjection.presentationLayout`, final wall/extension scopes, and existing `RenderDiagnostics.final_visibility`.
- Produces: deterministic `floor00_visual_layout`, `floor00_glass_continuity`, and `floor00_wall_alignment` checks in `VisualGateSnapshot.checks`.

- [ ] **Step 1: Write failing gate assertions.**

Add a floor00 snapshot test that expects:

```ts
expect(snapshot.checks.floor00_visual_layout.status).toBe("pass");
expect(snapshot.checks.floor00_glass_continuity.status).toBe("pass");
expect(snapshot.checks.floor00_wall_alignment.status).toBe("pass");
expect(snapshot.checks.floor00_visual_layout.details).toContain("approved_floor00_visual_layout");
```

Add a legacy-route test that expects the same checks to be `not_applicable` and the legacy render-pass list/digest behavior to remain unchanged.

- [ ] **Step 2: Run focused tests to verify they fail.**

```powershell
npm test -- --run tests/visual-gate.test.ts tests/phase3c-strict-browser-visual-gate.test.ts tests/floor00-scene.test.ts
```

Expected: FAIL because the new checks are not present.

- [ ] **Step 3: Implement the layout checks.**

In `buildVisualGateSnapshot`:

- compare `projection.presentationLayout.removedGlassCells` against every extension-wall `triggerCell` and fail if any removed cell draws;
- compare the actual final glass trigger sets against the contract final sets and verify adjacent strip continuity using the same native cell ordering used by `extension-wall.ts`;
- compare the wall cell scope against the contract final scope and verify the backward offset has unit length;
- verify the wall layer IDs for every final cell remain in sorted order `[0,1]`;
- keep the existing furniture, structural facility, actor, wall/door ordering, final visibility, and fallback checks intact.

The checks must return `not_applicable` for every route without `projection.presentationLayout`.

- [ ] **Step 4: Run focused tests to verify they pass.**

```powershell
npm test -- --run tests/visual-gate.test.ts tests/phase3c-strict-browser-visual-gate.test.ts tests/floor00-scene.test.ts
```

Expected: PASS with the new floor00 checks and unchanged legacy behavior.

- [ ] **Step 5: Commit the visual gate changes.**

```powershell
git add runtime/social-dev/src/renderer/visual-gate.ts runtime/social-dev/tests/visual-gate.test.ts runtime/social-dev/tests/phase3c-strict-browser-visual-gate.test.ts runtime/social-dev/tests/floor00-scene.test.ts
git commit -m "test: gate floor00 visual wall alignment"
```

### Task 4: Run full verification, capture evidence, and update state

**Files:**
- Create: `knowledge/fixtures/accepted/floor00-visual-layout-20260814.png` (generated screenshot)
- Create: `knowledge/fixtures/accepted/floor00-visual-layout-20260814.json` (generated visual-gate snapshot)
- Modify: `PROJECT_STATE.md`
- Modify: `TODO.md` if the matching user-directed item changes status

**Interfaces:**
- Consumes: all runtime changes and tests from Tasks 1–3.
- Produces: verified browser evidence, clean diagnostics, and a concise English project-state handoff.

- [ ] **Step 1: Inspect existing listeners before using a dev server.**

Run:

```powershell
Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue | Where-Object LocalPort -eq 4173
Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -match 'test open ai|runtime[\\/]social-dev|vite' } | Select-Object ProcessId,CommandLine
```

Reuse a healthy repository Vite server on port `4173`; do not start a duplicate process or use an automatic fallback port. If a new process is required, record its PID and stop its process tree after browser verification.

- [ ] **Step 2: Run the complete deterministic suite.**

From `runtime/social-dev`:

```powershell
npm test -- --run
npm run typecheck
npm run build
```

From the repository root:

```powershell
python tools/social-dev/test_pre_runtime_closure.py
git diff --check
```

Expected: all Vitest files/tests pass, typecheck/build pass, pre-runtime closure passes, and `git diff --check` produces no output.

- [ ] **Step 3: Capture two fixed floor00 browser frames.**

Open:

```text
http://127.0.0.1:4173/?scene=floor00&auto=0
```

Capture two screenshots without advancing the static scene. Read `canvas.dataset.renderDiagnostics` and the visible visual-gate diagnostics. Save the screenshot and JSON under `knowledge/fixtures/accepted/` with the exact filenames listed above. Confirm:

- the blue-left, purple, and blue-right glass zones are absent;
- the upper wood wall is continuous;
- the long side glass strip is continuous;
- the green-circled wall is one cell backward and endpoint-aligned;
- no required drawable is occluded;
- console errors and warnings are empty;
- both screenshots have the same SHA-256.

- [ ] **Step 4: Inspect process cleanup.**

If Task 4 started a server, verify no duplicate Vite/Vite-preview process remains and stop only the process tree created by this task. Do not terminate Codex-owned `mcp/server.mjs`, `node_repl`, or processes under `OpenAI\\Codex\\runtimes`.

- [ ] **Step 5: Update project state and commit the verified handoff.**

Update `PROJECT_STATE.md` with the completed visual-layout change, evidence paths, verification commands, and any explicit remaining boundary. Keep the entry concise and in English. Update only the matching `TODO.md` item if its status materially changed.

```powershell
git add PROJECT_STATE.md TODO.md
git commit -m "docs: record floor00 visual layout verification"
```

## Final self-review checklist

- [ ] Every design requirement has a corresponding task and test.
- [ ] No raw native evidence contract is rewritten.
- [ ] The contract contains concrete cell arrays and a unit backward offset.
- [ ] The adapter interfaces and projection field names match across Tasks 1–3.
- [ ] The visual gate checks both draw-attempt scope and final canvas visibility.
- [ ] Legacy/non-floor00 routes remain covered by regression assertions.
- [ ] Browser evidence is saved only under the approved evidence directory.
