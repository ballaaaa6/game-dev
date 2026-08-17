# Unified Main Floor00 Runtime Cutover Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task with verification checkpoints.

**Goal:** Make / the single Social Dev runtime entrypoint, with the approved floor00 presentation as the canonical main scene while retaining every current approved catalog, room, asset, character, and evidence input.

**Architecture:** Keep loadRuntimeCatalogs() as the one complete data boundary and keep the existing in-page RoomData selector inside the main UI. Replace query-driven scene/context selection with a fixed floor00/main_display route policy, remove the legacy display-slice projection branch and its production-only draw objects, and leave source/evidence contracts intact for provenance and verification.

**Tech Stack:** TypeScript, Vite, Canvas 2D, DOM/CSS, Vitest, JSON runtime contracts, PowerShell, and the existing browser smoke/visual-gate tooling.

## Global Constraints

- The root URL / is the only production runtime entrypoint and defaults to room:0 with the floor00/main policy.
- All currently approved runtime catalogs, room records, character metadata, promoted assets, native contracts, and floor00 contracts remain available through main.
- Historical evidence, contracts, source-derived metadata, and binaries that remain referenced are not deleted or rewritten.
- The unresolved red/black prop remains excluded; no missing FurnitureData/selector binding is invented.
- Native topology, selector provenance, floor alias semantics, and the floor00 static presentation policy do not change during routing cutover.
- Project-owned prose and modified documentation remain English-first.
- Test-first is mandatory: each behavior change gets a failing test before production implementation.

---

### Task 1: Add the canonical main-route contract

**Files:**
- Create: runtime/social-dev/src/app/main-route.ts
- Create: runtime/social-dev/tests/main-route.test.ts

**Interfaces:**
- Produces MainRuntimeRoute with roomId: string, rawOverlayEnabled: boolean, initialTicks: number, auto: boolean, and fixed sceneOptions containing nativeFloorValue: 0, context: "main_display", and sceneMode: "floor00".
- Produces parseMainRuntimeRoute(search: string): MainRuntimeRoute.

- [ ] Step 1: Write the failing route tests.

Create tests that assert the empty search defaults to room:0 and the fixed scene options. Add a second case with room:17, scene=display-slice-01, nativeFloor=1, and context=addition_floor_preview; assert that room:17 is retained but sceneOptions are still floor00, main_display, and nativeFloorValue 0. Also assert that overlay=raw, initialTicks, and auto=0 retain their current control values without changing the fixed scene policy.

- [ ] Step 2: Run the focused test and verify the expected red failure.

Run from runtime/social-dev:

    npm test -- --run tests/main-route.test.ts

Expected: Vitest fails because main-route.ts and parseMainRuntimeRoute do not exist yet.

- [ ] Step 3: Implement the pure route parser.

Implement parseMainRuntimeRoute with URLSearchParams. Read only room, overlay, initialTicks, and auto as main-runtime controls. Ignore scene, nativeFloor, and context as routing inputs and always return the fixed main scene options. Preserve integer validation for initialTicks and return 0 for missing/invalid numeric input rather than creating a second route.

- [ ] Step 4: Run the focused test and verify green.

Run the same Vitest command. Expected: all route-contract assertions pass.

- [ ] Step 5: Commit the isolated route contract.

    git add runtime/social-dev/src/app/main-route.ts runtime/social-dev/tests/main-route.test.ts
    git commit -m "test: define unified main route contract"

### Task 2: Make createSocialDevRuntime use main-only routing

**Files:**
- Modify: runtime/social-dev/src/app/runtime.ts
- Modify: runtime/social-dev/tests/main-route.test.ts

**Interfaces:**
- createSocialDevRuntime(root) consumes parseMainRuntimeRoute(window.location.search).
- The controller continues to expose selectRoom, step, selectActor, and the current catalog/diagnostic APIs; only scene/context selection is removed from the URL surface.

- [ ] Step 1: Extend the failing test to cover runtime-facing route inputs.

Add a projection-level assertion:

    const catalogs = loadRuntimeCatalogs();
    const route = parseMainRuntimeRoute("scene=display-slice-01&nativeFloor=1&context=persistent_room");
    const projection = buildSceneProjection(catalogs, route.roomId, route.sceneOptions);
    expect(projection.sceneMode).toBe("floor00");
    expect(projection.roomContext).toBe("main_display");
    expect(projection.nativeFloorValue).toBe(0);

- [ ] Step 2: Run the focused test and verify the expected red failure.

    npm test -- --run tests/main-route.test.ts

Expected: the parser tests pass, but the integration assertion fails until runtime.ts consumes the parser and the projection default is unified.

- [ ] Step 3: Replace query parsing in runtime.ts.

Remove the private parseSceneOptions function and direct URLSearchParams scene/context parsing. Import and use parseMainRuntimeRoute. Keep room validation, raw overlay handling, actor selection, room selection, and catalog loading unchanged. Pass the route fixed sceneOptions to the initial projection and every selectRoom projection. Keep the existing floor00 static policy: step() and the wall-clock timer must not advance the floor00 main scene.

- [ ] Step 4: Run the focused test and verify green.

    npm test -- --run tests/main-route.test.ts

- [ ] Step 5: Commit the main runtime routing change.

    git add runtime/social-dev/src/app/runtime.ts runtime/social-dev/src/app/main-route.ts runtime/social-dev/tests/main-route.test.ts
    git commit -m "feat: route the runtime through unified main"

### Task 3: Remove the legacy display projection branch

**Files:**
- Modify: runtime/social-dev/src/scene/room-resolver.ts
- Modify: runtime/social-dev/src/scene/projection.ts
- Modify: runtime/social-dev/tests/floor00-scene.test.ts
- Modify: runtime/social-dev/tests/render-plan.test.ts
- Modify: runtime/social-dev/tests/floor00-visual-layout.test.ts

**Interfaces:**
- SceneProjectionMode becomes the single literal "floor00" for production projection.
- buildSceneProjection(catalogs, roomId, options?) always returns floor00 scene mode and uses native room bindings/assets for every selected room.
- The legacy projection branch no longer populates renderObjects; Task 3 keeps that list empty as a short-lived compile boundary, and Task 4 removes the obsolete field after renderer/gate consumers are migrated. nativeInitialObjects, structuralFacilities, sceneAssets, and all raw room cells remain available.

- [ ] Step 1: Update tests to describe the unified default and remove legacy-only expectations.

Change default projection tests to assert:

    const projection = buildSceneProjection(loadRuntimeCatalogs());
    expect(projection.sceneMode).toBe("floor00");
    expect(projection.presentationLayout?.status).toBe("approved_floor00_visual_layout");
    expect(projection.structuralFacilities).toHaveLength(2);
    expect(projection.nativeInitialObjects).toHaveLength(6);

Replace renderObjects assertions in render-plan.test.ts with native initial-object and structural-facility assertions. Replace the floor00 visual-layout test that expects the legacy projection to have no layout with an assertion that the main/default projection receives the approved layout. Keep the contract validation test that rejects a non-floor00 scene_ref using a type-safe invalid fixture cast.

- [ ] Step 2: Run the affected tests and verify the expected red failures.

    npm test -- --run tests/floor00-scene.test.ts tests/render-plan.test.ts tests/floor00-visual-layout.test.ts

Expected: tests fail because the default projection still selects display-slice-01 and still exposes legacy render objects.

- [ ] Step 3: Make floor00 the only projection mode.

In room-resolver.ts, make the scene-mode type and presentation policy floor00-only. Keep low-level native topology/context validation for evidence tests, but do not allow production route options to select it. In projection.ts, remove isLegacyDisplaySlice, the legacy strictClosure/render3c object-placement branch, verifiedObject, and cellFromBinding. Always project runtimeRoom.nativeBindings, room assets, raw room cells, room overlay data, and floor00 structural facilities for room:0. Keep renderObjects as an empty typed list until Task 4 so the renderer and visual-gate migration remains a separate green test cycle.

- [ ] Step 4: Run the affected tests and verify green.

    npm test -- --run tests/floor00-scene.test.ts tests/render-plan.test.ts tests/floor00-visual-layout.test.ts tests/room-resolver.test.ts

Expected: all affected tests pass and all 18 rooms still resolve with their 196 MapChip cells and 100 ObjChip placements.

- [ ] Step 5: Commit the unified projection change.

    git add runtime/social-dev/src/scene/room-resolver.ts runtime/social-dev/src/scene/projection.ts runtime/social-dev/tests/floor00-scene.test.ts runtime/social-dev/tests/render-plan.test.ts runtime/social-dev/tests/floor00-visual-layout.test.ts
    git commit -m "refactor: make floor00 the unified scene projection"

### Task 4: Collapse renderer, visual-gate, and UI legacy branches

**Files:**
- Modify: runtime/social-dev/src/renderer/canvas-renderer.ts
- Modify: runtime/social-dev/src/renderer/visual-gate.ts
- Modify: runtime/social-dev/src/renderer/dom-ui.ts
- Modify: runtime/social-dev/tests/visual-gate.test.ts
- Modify: runtime/social-dev/tests/room-r-overlay.test.ts
- Modify: runtime/social-dev/tests/display-assets.test.ts

**Interfaces:**
- Renderer drawables consume only native room assets, native initial FurnitureData, structural facilities, room walls/door, extension walls, and actors from the unified projection.
- Visual-gate diagnostics retain current catalog counts, native binding checks, floor00 visibility checks, and raw room overlay checks without a legacy-mode bypass.
- UI reports floor00 as the active mode and keeps the current 18-room selector and complete catalog metrics.

- [ ] Step 1: Add failing assertions for unified renderer/UI behavior.

Extend visual-gate tests to assert the default projection passes the floor00 bootstrap/layout checks and that the floor00 bootstrap detail contains no legacy-object count. Update the display-assets frame test to use the canonical floor00 scene policy. Do not add a new DOM test harness; verify the rendered mode string through browser smoke in Task 6.

- [ ] Step 2: Run the affected tests and verify the expected red failures.

    npm test -- --run tests/visual-gate.test.ts tests/room-r-overlay.test.ts tests/display-assets.test.ts

Expected: TypeScript/test failures identify remaining projection.renderObjects, legacy-mode comparisons, or display-slice-01 frame-policy references.

- [ ] Step 3: Remove legacy-only renderer and gate references.

In canvas-renderer.ts, remove the projection.renderObjects loop from objectChipPrimaryDrawables; keep structural facilities and native initial objects. In visual-gate.ts, remove legacy object cards/required-asset entries and replace the floor00 detail string with native furniture/actor counts. In dom-ui.ts, set the static mode label to floor00, remove comparison-mode wording, and retain all room/catalog diagnostics. Update frame-selection tests and remaining mode checks to the canonical floor00 policy.

- [ ] Step 4: Run the affected tests and verify green.

    npm test -- --run tests/visual-gate.test.ts tests/room-r-overlay.test.ts tests/display-assets.test.ts tests/floor00-scene.test.ts

- [ ] Step 5: Commit the renderer and UI cleanup.

    git add runtime/social-dev/src/renderer/canvas-renderer.ts runtime/social-dev/src/renderer/visual-gate.ts runtime/social-dev/src/renderer/dom-ui.ts runtime/social-dev/tests/visual-gate.test.ts runtime/social-dev/tests/room-r-overlay.test.ts runtime/social-dev/tests/display-assets.test.ts
    git commit -m "refactor: remove legacy display stream from main renderer"

### Task 5: Update main documentation and perform reference-safe cleanup

**Files:**
- Modify: runtime/social-dev/README.md
- Modify: README.md
- Modify: PROJECT_STATE.md
- Modify: TODO.md
- Delete only files proven by rg to be production-only alternate route code/tests; retain evidence, contracts, reports, roadmaps, and assets still referenced by main.

**Interfaces:**
- Documentation describes / as the canonical floor00/main entrypoint and the in-page RoomData selector as the single way to inspect all rooms.
- State files record the cutover, preserved evidence boundary, and explicit unresolved prop/floor alias constraints.

- [ ] Step 1: Scan before deleting anything.

Run:

    rg -n "display-slice-01|scene=floor00|nativeFloor=|context=persistent_room|context=addition_floor_preview|renderObjects" runtime/social-dev/src runtime/social-dev/tests runtime/social-dev/README.md README.md

Classify each match as retained provenance/contract data or unreachable production route code. Do not delete files under knowledge/fixtures/accepted/, knowledge/fixtures/accepted/runtime/, or runtime/social-dev/assets/ solely because a filename contains the historical display-slice label.

- [ ] Step 2: Write documentation/state regression expectations.

Update the runtime README and root README so the canonical command is:

    http://127.0.0.1:4173/?auto=0

State that floor00 is now the main scene, all current catalogs/rooms remain available in the single runtime, and historical evidence remains preserved. Mark the single open expansion task as future user-directed scope after the unified gate passes.

- [ ] Step 3: Remove only confirmed unreachable route artifacts.

Use git rm only for files whose sole production purpose is the removed alternate route and which are not imported by retained tests, evidence builders, or main assets. Do not remove display_asset_manifest.json, promoted binaries, native contracts, or historical browser evidence if floor00 or a verification gate references them.

- [ ] Step 4: Verify documentation and cleanup references.

Run:

    rg -n "display-slice-01|scene=floor00|nativeFloor=|context=persistent_room|context=addition_floor_preview|renderObjects" runtime/social-dev/src runtime/social-dev/tests runtime/social-dev/README.md README.md
    git diff --check

Expected: remaining historical labels are limited to retained evidence/tests whose purpose is provenance, and no production main route selects an alternate stream.

- [ ] Step 5: Commit the state/documentation cleanup.

    git add runtime/social-dev/README.md README.md PROJECT_STATE.md TODO.md
    git add -u runtime/social-dev/src runtime/social-dev/tests
    git commit -m "docs: record unified main floor00 cutover"

### Task 6: Run full verification and browser smoke

**Files:**
- Verify: runtime/social-dev package, knowledge/fixtures/accepted/, and the final git diff.
- Update PROJECT_STATE.md and TODO.md with the exact observed verification results and final status.

**Interfaces:**
- Final main route is / with floor00, main_display, and nativeFloor=0 policy.
- All current room/catalog diagnostics remain visible from the main UI.

- [ ] Step 1: Inspect existing listeners before starting local tooling.

Run PowerShell listener/process checks for port 4173 and inspect command lines for this repository. Reuse a healthy repository Vite server if present; do not start a duplicate or rely on a fallback port.

- [ ] Step 2: Run the complete deterministic test suite.

From runtime/social-dev:

    npm test -- --run
    npm run typecheck
    npm run build

Expected: Vitest has zero failed tests, typecheck exits 0, and the production build exits 0.

- [ ] Step 3: Run pre-runtime and repository checks.

From the repository root:

    python tools/social-dev/test_pre_runtime_closure.py
    git diff --check

Expected: the pre-runtime contract gate passes and git diff --check reports no whitespace errors.

- [ ] Step 4: Run browser smoke against the canonical main URL.

Reuse or start only the verified port 4173 server, then load:

    http://127.0.0.1:4173/?auto=0

Verify the page reports floor00, room room:0, all current catalog/room counts, visual gate pass, no unresolved approved assets, and zero browser console errors/warnings. Capture two fixed-frame screenshots and compare their SHA-256 hashes for determinism. Select at least room:17 through the in-page selector to confirm all-room data remains reachable from main.

- [ ] Step 5: Clean up only task-started processes and record evidence.

If this task started Vite or browser tooling, stop its process tree after verification. Do not terminate Codex-owned processes. Store generated evidence under knowledge/fixtures/accepted/, update PROJECT_STATE.md/TODO.md with exact observed counts and hashes, inspect the final diff, and report any remaining explicit boundary instead of claiming completion without evidence.
