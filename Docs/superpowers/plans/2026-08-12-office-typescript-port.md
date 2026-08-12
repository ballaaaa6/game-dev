# Office Runtime TypeScript Port Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Port the bounded office-runtime behavior from the Phase 4 evidence set into executable, tested TypeScript without porting unrelated gameplay.

**Architecture:** Keep recovered C, assembly, JSON evidence, manifests and fixtures read-only. Add a typed runtime under `Phases/Phase5/runtime-ts/`; use `tsc` for type-checking and Node tests, and `esbuild` to create one browser bundle that exposes `window.Wave5Runtime`. Keep the current JavaScript runtime as a compatibility baseline until the TypeScript runtime passes parity and browser gates.

**Dependency:** This is `P0-B`. Start implementation tasks after `Docs/superpowers/plans/2026-08-12-corpus-intelligence-pipeline.md` produces a passing corpus closure report. The corpus plan may generate additional evidence, but it must not overwrite the Phase 4 historical artifacts referenced here.

**Tech Stack:** TypeScript, `tsc`, esbuild, Node.js 24 built-in test runner, existing browser Canvas shell, existing Python contract tests, Phase 4 evidence artifacts and Phase 5/6 fixtures.

## Global Constraints

- Do not modify `game-dev-story-mod_Sprites/`, `game-dev-story-mod_Dumped/`, `game-dev-story-mod_Extracted/` or `game-dev-story-mod_Sprites_fixed/`.
- Do not port gameplay economy, progression, sales, research, ranking, menu, save/load or platform framework code.
- Preserve `legacy_equivalence=false` until a specific behavior has direct evidence and a passing fixture.
- Preserve raw selector/mode/timer values whenever semantic naming is not verified.
- Every ported unit must have a `SourceRef`, an evidence artifact, a focused test and one explicit status.
- `MainProcess`, `NextPoint`, `NewGamePara` and `DoEvent` are evidence sources; none is copied wholesale into TypeScript.
- Existing Phase 2, Phase 4, Phase 5 and Phase 6 tests must remain passing after each integration task.
- Generated browser output is disposable and must not be hand-edited; regenerate it with `npm --prefix Phases/Phase5 run build:browser`.
- P0-B must consume canonical corpus records and promoted evidence; candidate AI summaries alone never qualify as `ts_ported` or `verified`.

## Build and migration contract

`Phases/Phase5/package.json` will use these scripts:

```json
{
  "scripts": {
    "build:ts": "tsc -p tsconfig.json",
    "build:browser": "esbuild runtime-ts/src/browser-entry.ts --bundle --format=iife --outfile=runtime-ts/dist/browser-entry.js",
    "build": "npm run build:ts && npm run build:browser",
    "test:ts": "node --test tests/test_wave5_ts_*.cjs",
    "test": "npm run build && npm run test:ts && node tests/test_wave5_runtime.js"
  }
}
```

The Node build emits CommonJS to `runtime-ts/dist/node/`. The browser build bundles source modules into `runtime-ts/dist/browser-entry.js`; `browser-entry.ts` assigns the public exports to `globalThis.Wave5Runtime`. The existing `app.js` remains a classic script and is loaded after the bundle, so its Phase 6 global dependencies and public method calls remain unchanged.

---

### Task 0: Freeze the JavaScript baseline and add a migration guard

**Files:**
- Create: `Phases/Phase5/artifacts/office_typescript_port_baseline.json`
- Create: `Phases/Phase5/tests/test_wave5_ts_baseline.cjs`
- Read: `Phases/Phase5/runtime/runtime.js`
- Read: `Phases/Phase5/tests/test_wave5_runtime.js`

**Interfaces:**
- Baseline artifact records current runtime public methods, existing scenario count, current runtime source hash and `legacy_equivalence: false`.
- Baseline test proves the old runtime still passes before any TypeScript consumer migration.

- [ ] **Step 1: Write the failing baseline assertion**

```js
const assert = require("node:assert/strict");
const Wave5 = require("../runtime/runtime.js");

assert.equal(typeof Wave5.OfficeRuntime, "function");
assert.equal(typeof Wave5.LocaleStore, "function");
assert.equal(typeof Wave5.OfficeRuntime.prototype.renderCommands, "function");
console.log("TypeScript port baseline contract loaded");
```

- [ ] **Step 2: Run `node Phases/Phase5/tests/test_wave5_ts_baseline.cjs` and `node Phases/Phase5/tests/test_wave5_runtime.js`; record the existing 10-scenario pass**
- [ ] **Step 3: Write the baseline builder or manifest entry with the exact SHA-256 of `Phases/Phase5/runtime/runtime.js` and the method list used by `app.js`**
- [ ] **Step 4: Run the two commands again and confirm the baseline is unchanged**

### Task 1: Add the isolated TypeScript toolchain and provenance/type contracts

**Files:**
- Create: `Phases/Phase5/package.json`
- Create: `Phases/Phase5/tsconfig.json`
- Create: `Phases/Phase5/runtime-ts/src/source-ref.ts`
- Create: `Phases/Phase5/runtime-ts/src/types.ts`
- Create: `Phases/Phase5/runtime-ts/src/index.ts`
- Create: `Phases/Phase5/tests/test_wave5_ts_types.cjs`

**Interfaces:**
- `SourceRef` contains `symbol`, `file`, optional `line`, optional `artifact`, and `confidence: "verified" | "probable" | "unknown"`.
- `AgentStatus` is a web-product status union: `"idle" | "walking" | "working" | "sitting" | "break" | "talking"`.
- `LegacyMode` is only `{ kind: "raw"; value: number }`; a product `AgentStatus` is never presented as a recovered legacy mode.
- `OfficeObject`, `ActorState`, `SelectorSet`, `DrawCommand`, `MovementProvider`, `CollisionProvider`, `SeatProvider`, `DialogueRequest`, and `RuntimeEvent` are exported from `types.ts`.
- `normalizeLegacyMode(value: number): LegacyMode` always preserves an unverified numeric value.

- [ ] **Step 1: Add `package.json` scripts and install only the build tools**

```powershell
npm --prefix Phases/Phase5 install --save-dev typescript esbuild
```

- [ ] **Step 2: Add `tsconfig.json` with `target: ES2022`, `module: CommonJS`, `rootDir: runtime-ts/src`, `outDir: runtime-ts/dist/node`, `strict: true`, `declaration: true`, and `sourceMap: true`; run `npm --prefix Phases/Phase5 run build:ts` and confirm failure because source modules are absent**
- [ ] **Step 3: Write the focused test**

```js
const assert = require("node:assert/strict");
const { normalizeLegacyMode } = require("../runtime-ts/dist/node/index.js");

assert.deepEqual(normalizeLegacyMode(0x27), { kind: "raw", value: 0x27 });
```

- [ ] **Step 4: Implement the exact types and `normalizeLegacyMode`; run `npm --prefix Phases/Phase5 run build:ts` and the focused test and confirm PASS**
- [ ] **Step 5: Confirm `git diff --check` and keep `runtime-ts/dist/` ignored or generated-only**

### Task 2: Port verified resource and selector resolution

**Files:**
- Create: `Phases/Phase5/runtime-ts/src/resource-adapter.ts`
- Create: `Phases/Phase5/runtime-ts/src/generated/resource-data.ts`
- Create: `Phases/Phase5/tools/build_typescript_resource_data.py`
- Create: `Phases/Phase5/tests/test_wave5_ts_resource_adapter.cjs`
- Read: `Phases/Phase5/artifacts/wave5_3_numeric_crop_placement_contract.json`
- Read: `Phases/Phase5/artifacts/wave5_5_img_list_alignment.json`
- Read: `Phases/Phase5/artifacts/wave5_6_floorparts_seb_contract.json`

**Interfaces:**
- `ResourceRecord` contains selector namespace, numeric selector, resource index, filename, optional crop and `SourceRef`.
- `ResourceCatalog.resolveFurniture(selector: "DDPC" | "DDChair" | "DDDesk"): ResourceRecord`.
- `ResourceCatalog.resolveBodyFace(selectors: SelectorSet): BodyFaceResolution`.
- `ResourceCatalog.assetUrl(record: ResourceRecord): string`.
- `resolveBodyFace` returns `status: "resolved" | "partial_unresolved_selector"` for `TFace=40/41` and never substitutes another face.

- [ ] **Step 1: Write tests for `DDChair=25 → chair0_origin.png/index29`, `DDDesk=26 → desk0_origin.png/index30`, `DDPC=77 → pc.png/index117`, `DDFloor+3=42 → floorparts0.png/index79`, and unresolved `TFace=40/41`**
- [ ] **Step 2: Run `npm --prefix Phases/Phase5 run build:ts` and the focused resource test; confirm failure because the catalog is absent**
- [ ] **Step 3: Implement `build_typescript_resource_data.py` to read only the verified Phase 5 artifacts and generate a small typed table; do not read raw recovered C from the browser**
- [ ] **Step 4: Implement `ResourceCatalog` over the generated table and attach a `SourceRef` to every entry**
- [ ] **Step 5: Run the focused resource test and `python -m unittest Phases/Phase5/tests/test_wave5_contract.py`; confirm both pass**

### Task 3: Port room, furniture and draw-command behavior

**Files:**
- Create: `Phases/Phase5/runtime-ts/src/scene-runtime.ts`
- Create: `Phases/Phase5/runtime-ts/src/draw-commands.ts`
- Create: `Phases/Phase5/tests/test_wave5_ts_scene_runtime.cjs`
- Read: `Phases/Phase4/artifacts/wave2_minimum_scene_fixture.json`
- Read: `Phases/Phase5/artifacts/wave5_2_furniture_draw_fixture.json`
- Read: `Phases/Phase5/artifacts/wave5_8_room_caller_contract.json`
- Read: `Phases/Phase5/artifacts/wave5_9_object_producer_contract.json`

**Interfaces:**
- `OfficeScene.addObject(input: AddObjectInput): OfficeObject`.
- `OfficeScene.updateObject(id: string, patch: ObjectPatch): OfficeObject`.
- `OfficeScene.renderObjects(): DrawCommand[]`.
- `buildFurnitureDrawCommand(object: OfficeObject, resources: ResourceCatalog): DrawCommand`.
- PNG placement uses verified `ObjecX/Y + ObjecZX/ZY`; crop uses verified `ObjecCX/CY/WX/WY` fields.
- Draw sorting remains an explicit adapter policy and carries `semantic_status: "adapter_sort_only"`.

- [ ] **Step 1: Write a test for `AddObjec` field provenance, crop, placement, missing selector status and deterministic ordering**

```js
const command = scene.renderObjects()[0];
assert.deepEqual(command.destination, { x: 100 + 4, y: 200 + 6 });
assert.deepEqual(command.crop, { x: 2, y: 3, width: 16, height: 20 });
assert.equal(command.semantic_status, "adapter_sort_only");
```

- [ ] **Step 2: Run the focused scene test and confirm failure before implementation**
- [ ] **Step 3: Implement the typed object record and verified PNG/crop/placement formulas from the Phase 5 contracts**
- [ ] **Step 4: Preserve explicit `unknown` fields for source-array, pivot, depth and universal transform semantics**
- [ ] **Step 5: Run the focused scene test plus `node Phases/Phase5/tests/test_wave5_runtime.js`; confirm PASS**

### Task 4: Port actor identity, body/face composition and movement/seat boundaries

**Files:**
- Create: `Phases/Phase5/runtime-ts/src/movement-seat.ts`
- Create: `Phases/Phase5/runtime-ts/src/actor-runtime.ts`
- Create: `Phases/Phase5/tests/test_wave5_ts_actor_runtime.cjs`
- Read: `Phases/Phase2/artifacts/bodyface_analysis.json`
- Read: `Phases/Phase4/artifacts/wave3_actor_identity_contract.json`
- Read: `Phases/Phase4/artifacts/wave3_movement_contract.json`
- Read: `Phases/Phase4/artifacts/wave3_actor_animation_contract.json`
- Read: `Phases/Phase4/artifacts/wave3_actor_e2e_fixture.json`

**Interfaces:**
- `ActorRuntime.spawn(input: SpawnActorInput): ActorState`.
- `ActorRuntime.requestMove(actorId: string, target: Point): MovementResult`.
- `ActorRuntime.step(ticks: number): void`.
- `ActorRuntime.occupySeat(actorId: string, seatId: string): SeatResult`.
- `ActorRuntime.releaseSeat(actorId: string, seatId: string): void`.
- `ActorRuntime.drawActor(actorId: string): DrawCommand`.
- `DirectPathProvider`, `ExplicitCollisionProvider` and `SeatProvider` remain injected dependencies.

- [ ] **Step 1: Write tests for spawn, direct movement, blocked movement, seat ownership, release/reacquire, verified body/face composition and unresolved face selectors**
- [ ] **Step 2: Run the focused actor test and confirm failure**
- [ ] **Step 3: Implement actor identity and selector composition from Phase 2/3 contracts without inventing animation semantics; use `AgentStatus` only as product state**
- [ ] **Step 4: Implement movement and seat providers using the existing Phase 5 adapter policy; blocked movement must not teleport the actor**
- [ ] **Step 5: Run the focused actor test, Phase 4 actor contract tests and the existing 10-scenario runtime test**

### Task 5: Port locale, talk, bubble, notification and raw-event bridge

**Files:**
- Create: `Phases/Phase5/runtime-ts/src/dialogue-runtime.ts`
- Create: `Phases/Phase5/runtime-ts/src/event-bridge.ts`
- Create: `Phases/Phase5/tests/test_wave5_ts_dialogue_runtime.cjs`
- Read: `Phases/Phase4/artifacts/wave4_locale_contract.json`
- Read: `Phases/Phase4/artifacts/wave4_talk_contract.json`
- Read: `Phases/Phase4/artifacts/wave4_bubble_contract.json`
- Read: `Phases/Phase4/artifacts/wave4_notification_contract.json`
- Read: `Phases/Phase4/artifacts/wave4_event_contract.json`

**Interfaces:**
- `LocaleStore.resolve(id: string, locale: string | undefined, args: string[]): ResolvedText`.
- `DialogueRuntime.requestDialogue(input: DialogueRequest): BubbleRecord`.
- `DialogueRuntime.step(ticks: number): void`.
- `EventBridge.recordNamed(type: NamedEventType, payload: unknown): RuntimeEvent`.
- `EventBridge.recordRaw(mode: number, args: number[], source: SourceRef): RuntimeEvent`.

- [ ] **Step 1: Write tests for `<0>` placeholder preservation, locale fallback to configured `th`, bubble expiry, notification expiry and raw event mode preservation**

```js
const resolved = locale.resolve("#demo", "xx", ["ตอนนี้"]);
assert.equal(resolved.status, "fallback");
assert.equal(resolved.text, "ทำงาน ตอนนี้");
const raw = events.recordRaw(0x14, [7, 9], source);
assert.equal(raw.type, "legacy.event.raw");
assert.equal(raw.mode, 0x14);
```

- [ ] **Step 2: Run the focused dialogue test and confirm failure**
- [ ] **Step 3: Port the generated locale lookup contract; runtime must receive locale data as an injected object and must not read CSV or raw C**
- [ ] **Step 4: Implement explicit logical ticks, bubble/notification cleanup and named web events while preserving unknown graph/mode/speaker values**
- [ ] **Step 5: Run the focused dialogue test and the existing Phase 4/5/6 regression suites**

### Task 6: Compose `OfficeRuntime` and add the browser bundle

**Files:**
- Create: `Phases/Phase5/runtime-ts/src/office-runtime.ts`
- Create: `Phases/Phase5/runtime-ts/src/browser-entry.ts`
- Create: `Phases/Phase5/tests/test_wave5_ts_office_runtime.cjs`
- Modify: `Phases/Phase5/runtime/index.html:145-149`
- Read: `Phases/Phase5/runtime/app.js:4-12,430-450`
- Read: `Phases/Phase6/runtime/task_system.js`

**Interfaces:**
- `OfficeRuntime` preserves the public methods used by `app.js`: `addAgent`, `step`, `requestMove`, `occupySeat`, `requestDialogue`, `addNotification`, `renderCommands`, `setState`, `setAgentTaskProjection`, `recordAdapterEvent` and `getAgent`.
- `browser-entry.ts` assigns `globalThis.Wave5Runtime = { OfficeRuntime, LocaleStore, DirectPathProvider, ExplicitCollisionProvider, SeatProvider, ... }`.
- Phase 6 global scripts remain loaded before `app.js`; `OfficeRuntime` continues to emit the event shape consumed by `TaskSystem`.

- [ ] **Step 1: Write a test that constructs `OfficeRuntime`, adds one actor and asserts all existing public method names are callable**
- [ ] **Step 2: Run `npm --prefix Phases/Phase5 run build:browser` and the focused office-runtime test; confirm failure because the bundle and class do not exist**
- [ ] **Step 3: Compose `OfficeRuntime` from scene, actor, dialogue and event modules without duplicating their logic**
- [ ] **Step 4: Build the IIFE bundle and change `index.html` to load `./runtime-ts/dist/browser-entry.js` instead of `./runtime.js`; leave the old runtime file untouched as rollback baseline**
- [ ] **Step 5: Run the existing Node runtime test and browser smoke; require console error/warning count `0` before moving on**

### Task 7: Add typed-port coverage manifest and closure tests

**Files:**
- Create: `Phases/Phase4/tools/build_office_typescript_port_manifest.py`
- Create: `Phases/Phase4/tests/test_office_typescript_port_manifest.py`
- Create: `Phases/Phase4/artifacts/office_typescript_port_manifest.json`
- Create: `Phases/Phase4/docs/office_typescript_port_closure.md`
- Read: `Phases/Phase4/artifacts/function_inventory.json`
- Read: `Phases/Phase4/artifacts/translation_coverage.json`
- Read: `Phases/Phase5/runtime-ts/src/*.ts`

**Interfaces:**
- Manifest units are product-scope symbols mapped to `module`, `source_refs`, `evidence_artifacts`, `tests` and exactly one status: `evidence_ready`, `contract_ready`, `ts_ported`, `verified` or `blocked`.
- Manifest summary reports recovered-C audit lines, assembly evidence instructions, measured TypeScript lines, measured test lines and counts by status.
- `unknown_boundaries`, `legacy_facts` and `web_adapter_decisions` are separate arrays.

- [ ] **Step 1: Write tests requiring every product-scope unit to have a source symbol, at least one evidence artifact and an allowed status; reject `ts_ported` without a TypeScript module and test**
- [ ] **Step 2: Run `python -m unittest Phases/Phase4/tests/test_office_typescript_port_manifest.py` and confirm failure because the manifest does not exist**
- [ ] **Step 3: Implement the deterministic builder using `function_inventory.json`, module source refs, existing Wave 2–5 contracts and SHA-256 hashes; do not modify historical manifests**
- [ ] **Step 4: Run the manifest test and confirm the measured coverage and line counts are stable across two builder runs**
- [ ] **Step 5: Run full Phase 2/4/5/6 regression and record exact pass counts in the new manifest and closure report**

### Task 8: Update roadmap, handoff and the Phase 7 gate

**Files:**
- Modify: `Docs/AI_Agent_Office_Roadmap.md`
- Modify: `TODO.md`
- Modify: `PROJECT_STATE.md`
- Modify: `Phases/Phase4/README.md`
- Modify: `Phases/Phase5/README.md`
- Modify: `Phases/README.md`

- [ ] **Step 1: Record the final source-to-module matrix, measured TypeScript/test line counts and test results**
- [ ] **Step 2: Document every remaining unknown with evidence path and the feature dependency that would reopen it**
- [ ] **Step 3: Mark the P0 port gate complete only when the compiled browser runtime, all regression suites and browser smoke pass**
- [ ] **Step 4: Keep Phase 7 AI model work blocked on the port gate and Phase 6 task regression; preserve `legacy_equivalence=false`**
- [ ] **Step 5: Run `git diff --check` and verify all source roots remain unchanged**

## Verification commands

```powershell
npm --prefix Phases/Phase5 run build
npm --prefix Phases/Phase5 test
python -m unittest discover -s Phases/Phase4/tests -p "test_*.py"
python -m unittest discover -s Phases/Phase2/tests -p "test_*.py"
python -m unittest discover -s Phases/Phase5/tests -p "test_*.py"
python -m unittest discover -s Phases/Phase6/tests -p "test_*.py"
git diff --check
```
