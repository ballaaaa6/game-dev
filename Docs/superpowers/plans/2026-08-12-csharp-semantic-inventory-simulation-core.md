# C# Semantic Inventory and Simulation Core Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** สร้าง evidence-backed semantic inventory จาก gameplay-critical C# slice แล้วนำไปสร้าง deterministic Simulation Core ที่จำลอง office ต่อเนื่องและส่ง canonical state ให้ dashboard โดยไม่ execute decompiled C# โดยตรง

**Architecture:** แยกงานเป็นชั้น `C# evidence → inventory register → canonical schema → SimulationCore reducer → OfficeRuntime adapter → dashboard scheduler/renderer`. SimulationCore เป็น source of truth ระยะยาว ส่วน OfficeRuntime รักษา compatibility facade สำหรับ provider และ consumer เดิมระหว่าง migration

**Tech Stack:** Python standard library สำหรับ inventory/contract checks, browser-compatible ES5-style UMD JavaScript, Node.js built-in `assert`/`fs` สำหรับ runtime tests, existing Python `unittest`, existing browser smoke workflow

## Global Constraints

- C# discovery evidence หลักอยู่ที่ `knowledge/csharp/primary/` และมี 85 `.cs` files พร้อม `Assembly-CSharp.csproj`.
- รอบแรกวิเคราะห์เฉพาะ `GameForm`, `Main`, `Anim`, `FormManager`, `MyFormBase` และ data types ที่ actor/scene slice ใช้; ไม่ทำ deep semantic inventory ของ billing/network/install/analytics.
- source/extraction roots เดิมเป็น read-only และห้ามสร้าง `Assembly-CSharp/` กลับ.
- decompiled C# เป็น evidence ไม่ใช่ buildable production runtime; runtime JavaScript เท่านั้นที่ถูก execute ในเว็บ.
- numeric mode/state ที่ยังพิสูจน์ไม่ได้ต้องเก็บเป็น raw value หรือ `unknown`.
- recovered C, assembly fallback และ reverse-engineering reports ใช้เป็น corroborating evidence ไม่ใช่ runtime source.
- canonical schema version ของรอบนี้คือ `simulation-core-v1`.
- `legacy_equivalence` ต้องเป็น `false` จนกว่าจะมีหลักฐาน equivalence ครบ.
- logical tick ต้อง deterministic และ snapshot/digest ต้องทำซ้ำได้.
- หน้าเว็บต้องเริ่มจำลองเองและไม่มี Play, Pause, Step, Reset หรือ speed multiplier สำหรับ simulation.
- ห้ามเพิ่ม npm dependency หรือแก้ source roots เพื่อให้งานนี้ผ่าน.
- ก่อน commit/push หรือ integration ใด ๆ ต้องรอคำสั่งผู้ใช้ใน shared workspace.

---

## File map and ownership

### Evidence and inventory

- Create: `tools/csharp-evidence/semantic_inventory_targets.json` — รายการ input files, deep symbols และ field groups ที่อยู่ใน scope
- Create: `tools/csharp-evidence/semantic_inventory_claims.json` — curated claims ที่มี status/provenance ชัดเจน; ค่าอื่น default เป็น `unknown`/`raw_only`
- Create: `tools/csharp-evidence/semantic_inventory.py` — library สำหรับ target validation, source parsing, access extraction, provenance validation และ fingerprint
- Create: `tools/csharp-evidence/build_semantic_inventory.py` — CLI `build`/`check` สำหรับสร้างและตรวจ generated evidence
- Create: `tools/csharp-evidence/test_semantic_inventory.py` — structural inventory contract tests
- Create: `tools/csharp-evidence/test_semantic_slices.py` — deep access/claim/provenance tests
- Generate: `knowledge/csharp/evidence/semantic_inventory/inventory_manifest.json`
- Generate: `knowledge/csharp/evidence/semantic_inventory/type_catalog.json`
- Generate: `knowledge/csharp/evidence/semantic_inventory/field_catalog.json`
- Generate: `knowledge/csharp/evidence/semantic_inventory/method_catalog.json`
- Generate: `knowledge/csharp/evidence/semantic_inventory/transition_catalog.json`
- Generate: `knowledge/csharp/evidence/semantic_inventory/provenance_index.json`
- Generate: `knowledge/csharp/evidence/semantic_inventory/inventory_report.md`
- Generate: `runtime/office/evidence/semantic_inventory_runtime.json` — runtime-safe status/provenance summary with no C# source body

### Simulation Core

- Create: `runtime/office/app/simulation_schema.js` — constructors, normalizers, validators และ stable serialization ของ canonical state/command/event
- Create: `runtime/office/app/simulation_core.js` — command reducer, actor transitions, logical tick, timers, event log, snapshot, digest และ subscriptions
- Modify: `runtime/office/app/runtime.js` — OfficeRuntime compatibility facade และ adapter/render boundary ที่อ่าน state จาก core
- Create: `runtime/office/tests/test_simulation_schema.js` — schema/validation tests
- Create: `runtime/office/tests/test_simulation_core.js` — reducer/tick/replay tests
- Modify: `runtime/office/tests/test_wave5_runtime.js` — regression assertions for facade behavior and canonical snapshot
- Modify: `runtime/office/tests/test_wave5_contract.py` — contract artifact and schema boundary assertions
- Generate: `runtime/office/evidence/simulation_core_contract.json`
- Create: `runtime/office/reports/simulation_core_architecture.md`

### Dashboard and continuous simulation

- Create: `runtime/office/app/continuous_scheduler.js` — internal wall-clock scheduler with injectable timer functions
- Create: `runtime/office/tests/test_continuous_scheduler.js` — scheduler lifecycle tests without real waiting
- Modify: `runtime/office/app/index.html` — remove simulation playback controls and stale phase/wave label
- Modify: `runtime/office/app/app.js` — consume core snapshot/subscription, start scheduler on boot, expose diagnostics/provenance
- Modify: `runtime/office/app/style.css` — keep toolbar layout valid after playback buttons are removed
- Modify: `runtime/dashboard/tests/test_wave6_task_system.js` — assert task projection reaches canonical actor state
- Modify: `runtime/dashboard/tests/test_wave6_contract.py` — assert task system remains an owner separate from core task projection

### State and handoff

- Modify: `runtime/office/README.md` — document SimulationCore/adapter boundary and continuous behavior
- Modify: `runtime/office/reports/simulation_core_architecture.md` — implementation evidence and migration notes
- Modify: `PROJECT_STATE.md` — verified outputs, limitations and next unresolved semantic gaps
- Modify: `TODO.md` — milestone checkboxes after each verified deliverable

## Shared interfaces

The following names and shapes are fixed before implementation. Later tasks must use these exact names unless a failing contract test proves a correction is necessary.

### Inventory library

```python
def load_target_manifest(path: Path) -> dict:
    """Load and validate csharp-semantic-inventory-targets-v1."""

def build_structural_inventory(workspace_root: Path, manifest: dict) -> dict:
    """Return deterministic type/field/method catalogs with 1-based source spans."""

def build_semantic_slices(workspace_root: Path, structural: dict, claims: dict) -> dict:
    """Return access edges, transitions, provenance index and unresolved counts."""

def write_inventory(output_dir: Path, inventory: dict) -> None:
    """Write sorted JSON/Markdown artifacts without touching source roots."""

def check_inventory(workspace_root: Path, manifest_path: Path, output_dir: Path) -> dict:
    """Return a check-pass result or raise a validation error."""

def build_runtime_projection(inventory: dict) -> dict:
    """Return browser-safe evidence/status data without embedding C# source bodies."""
```

### Simulation schema

`runtime/office/app/simulation_schema.js` must export the following through both CommonJS and `window.SimulationSchema`:

```javascript
{
  SCHEMA_VERSION,
  ADAPTER_STATES,
  MOVEMENT_STATUSES,
  createSimulationState,
  createActor,
  createCommand,
  createEvent,
  validateSimulationState,
  validateCommand,
  validateEvent,
  assertValidSimulationState,
  stableJson
}
```

Validators return `{ valid: boolean, errors: string[] }`; assertion throws an `Error` with `code === "invalid_simulation_state"` for invalid state.

### Simulation core

`runtime/office/app/simulation_core.js` must export `{ SimulationCore }` through CommonJS and `window.SimulationCore`:

```javascript
class SimulationCore {
  constructor({ state, adapter }) {}
  dispatch(command) {}       // returns { snapshot, events }
  advance(count = 1) {}      // returns canonical snapshot
  setAdapterState(actorId, state, source = "adapter") {}
  getActor(actorId) {}       // returns a cloned actor
  snapshot() {}              // returns a cloned SimulationState
  digest() {}                // returns stable JSON digest
  subscribe(listener) {}     // returns unsubscribe function
}
```

In Node, `require("./simulation_core.js").SimulationCore` is the class. In the browser, `window.SimulationCore.SimulationCore` is the same class. `simulation_core.js` receives schema helpers as a UMD dependency so Node and browser use the same validators.

The adapter port passed to the constructor has these functions:

```javascript
{
  findPath({ actorId, from, target }),
  checkCollision({ actorId, position }),
  occupySeat({ actorId, seatId }),
  releaseSeat({ actorId, seatId }),
  resolveDialogue({ languageId, locale, args, text })
}
```

### Compatibility facade

`OfficeRuntime` keeps these consumer-facing members working while delegating state mutation to `SimulationCore`:

```text
clock.value
agents: Map
bubbles: Map
notifications: Map
events.records
addAgent / getAgent / setState
requestMove / occupySeat / releaseSeat
addBubble / requestDialogue / addNotification
setAgentTaskProjection / recordAdapterEvent / recordRawEvent
step / snapshot / digest / renderCommands
subscribe
```

The maps and event records are read-only projections of core state; they are not a second source of truth.

---

### Task 1: Lock the inventory input contract and structural parser

**Files:**
- Create: `tools/csharp-evidence/semantic_inventory_targets.json`
- Create: `tools/csharp-evidence/semantic_inventory.py`
- Create: `tools/csharp-evidence/build_semantic_inventory.py`
- Test: `tools/csharp-evidence/test_semantic_inventory.py`
- Generate: `knowledge/csharp/evidence/semantic_inventory/inventory_manifest.json`
- Generate: `knowledge/csharp/evidence/semantic_inventory/type_catalog.json`
- Generate: `knowledge/csharp/evidence/semantic_inventory/field_catalog.json`
- Generate: `knowledge/csharp/evidence/semantic_inventory/method_catalog.json`

**Interfaces:**
- Consumes: `knowledge/csharp/primary/`, workspace root and target manifest
- Produces: deterministic structural catalogs and an input fingerprint for Task 2

- [ ] **Step 1: Write failing target-manifest tests.**

Add tests that require the manifest to name the five gameplay files, the `data/*.cs` structural glob, the deep method symbols and the field groups. Also require that every configured file resolves under the workspace and that a missing file fails with `FileNotFoundError`.

```python
def test_targets_include_gameplay_slice(self):
    manifest = load_target_manifest(TARGETS)
    self.assertIn("form/GameForm.cs", manifest["primary_files"])
    self.assertIn("MainProcess", manifest["deep_symbols"])
    self.assertIn("HumanMode", manifest["field_groups"]["actor_state"])

def test_missing_target_is_rejected(self):
    with self.assertRaises(FileNotFoundError):
        validate_target_manifest(ROOT, {"primary_files": ["missing.cs"]})
```

- [ ] **Step 2: Run the focused test and verify it fails for the missing contract.**

Run:

```powershell
python -m unittest discover -s tools/csharp-evidence -p 'test_semantic_inventory.py' -v
```

Expected: FAIL because the target manifest, loader and validator do not exist yet.

- [ ] **Step 3: Freeze the evidence boundary and capture the input set.**

Before generating any artifact, read `AGENTS.md`, `PROJECT_STATE.md` and `TODO.md`, resolve the workspace root, enumerate the five primary files plus `data/*.cs`, and compute SHA-256 hashes. The builder must reject a target path outside the workspace and must never write beneath `knowledge/csharp/primary/`. Record the resolved files and hashes in `inventory_manifest.json`.

- [ ] **Step 4: Add the target manifest with explicit scope.**

Use this shape and exact deep symbol list:

```json
{
  "schema_version": "csharp-semantic-inventory-targets-v1",
  "primary_files": [
    "knowledge/csharp/primary/form/GameForm.cs",
    "knowledge/csharp/primary/main/Main.cs",
    "knowledge/csharp/primary/main/Anim.cs",
    "knowledge/csharp/primary/form/FormManager.cs",
    "knowledge/csharp/primary/form/MyFormBase.cs"
  ],
  "structural_globs": ["knowledge/csharp/primary/data/*.cs"],
  "deep_symbols": [
    "Main.OnUpdate", "FormManager.PreUpdate", "FormManager.Updated",
    "GameForm.Update", "GameForm.MainProcess", "GameForm.DoEvent",
    "GameForm.ProcessEvent", "GameForm.AddEvent", "GameForm.CallSyain",
    "GameForm.NextTarget", "GameForm.AddTarget", "GameForm.CallFuki",
    "GameForm.AddKaiwa", "GameForm.AddMessage", "GameForm.DrawObj",
    "GameForm.DrawHuman"
  ],
  "field_groups": {
    "actor_state": ["HumanMode", "HumanState", "HumanAnime", "HumanTime"],
    "actor_identity": ["HumanSyain", "HumanFaceG", "HumanBodyG", "HumanX", "HumanY"],
    "movement": ["HumanNowPoint", "HumanGoalPoint", "HumanPX", "HumanPY"],
    "bubble": ["HumanFukiTime", "HumanFukiIndex"],
    "event": ["EventMode", "EventTemp", "EventTemp2"],
    "message": ["MessageText", "MessageTime", "MessageGraph"]
  },
  "supporting_evidence_roots": [
    "knowledge/characters/evidence",
    "knowledge/reverse-engineering/evidence",
    "knowledge/reverse-engineering/reports"
  ]
}
```

- [ ] **Step 5: Implement the structural parser with source-span preservation.**

Implement `load_target_manifest`, `validate_target_manifest` and `build_structural_inventory` in `semantic_inventory.py`. Read UTF-8 source with `Path.read_text`, keep line numbers 1-based, sort paths and symbols lexicographically, and use brace depth plus declaration regexes only for cataloging. Do not infer compile-time types beyond the declaration text.

Each type/field/method record must include `symbol`, `kind`, `source.file`, `source.line_start`, `source.line_end`, `raw_declaration` and `source_hash`. The top-level result must include `schema_version`, `inputs`, `types`, `fields`, `methods` and `content_fingerprint`.

- [ ] **Step 6: Add the CLI and generate the first artifacts.**

Implement these commands:

```powershell
python tools/csharp-evidence/build_semantic_inventory.py build
python tools/csharp-evidence/build_semantic_inventory.py check
```

`build` writes only under `knowledge/csharp/evidence/semantic_inventory/`; `check` rebuilds in memory and compares the output fingerprint without changing source files.

- [ ] **Step 7: Run the focused tests and artifact check.**

Run:

```powershell
python -m unittest discover -s tools/csharp-evidence -p 'test_semantic_inventory.py' -v
python tools/csharp-evidence/build_semantic_inventory.py check
```

Expected: all structural tests pass, `GameForm`, `MainProcess`, `DoEvent`, `HumanMode`, `CallSyain` and `DrawObj` appear with valid source spans, and the CLI prints `check_pass` with a stable fingerprint.

### Task 2: Add deep access slices, claims and provenance

**Files:**
- Create: `tools/csharp-evidence/semantic_inventory_claims.json`
- Modify: `tools/csharp-evidence/semantic_inventory.py`
- Modify: `tools/csharp-evidence/build_semantic_inventory.py`
- Test: `tools/csharp-evidence/test_semantic_slices.py`
- Generate: `knowledge/csharp/evidence/semantic_inventory/field_catalog.json`
- Generate: `knowledge/csharp/evidence/semantic_inventory/method_catalog.json`
- Generate: `knowledge/csharp/evidence/semantic_inventory/transition_catalog.json`
- Generate: `knowledge/csharp/evidence/semantic_inventory/provenance_index.json`
- Generate: `knowledge/csharp/evidence/semantic_inventory/inventory_report.md`
- Generate: `runtime/office/evidence/semantic_inventory_runtime.json`

**Interfaces:**
- Consumes: Task 1 structural catalogs, C# source spans, recovered-C reports, assembly fallback reports and character evidence
- Produces: access edges, transition records, claim status counts and provenance records for Task 3

- [ ] **Step 1: Write failing deep-slice tests.**

Require the access catalog to identify reads/writes/calls for `HumanMode`, `HumanFukiTime`, `HumanFukiIndex`, `EventMode`, `MessageTime`, `CallFuki`, `AddEvent`, `MainProcess` and `DoEvent`. Require `DoEvent` to retain assembly-fallback status and forbid a semantic name for `HumanMode`.

```python
def test_raw_mode_has_no_guessed_semantic_name(self):
    record = self.field_records["HumanMode"]
    self.assertIn(record["semantic_status"], {"unknown", "raw_only"})
    self.assertNotIn("semantic_name", record)

def test_fuki_timer_has_provenance(self):
    record = self.field_records["HumanFukiTime"]
    self.assertEqual(record["semantic_status"], "verified")
    self.assertTrue(record["evidence_refs"])
    self.assertTrue(any("mainprocess_lifecycle_01.md" in ref["file"] for ref in record["evidence_refs"]))

def test_do_event_is_bounded_assembly_fallback(self):
    method = self.method_records["GameForm.DoEvent"]
    self.assertEqual(method["semantic_status"], "assembly_fallback_bounded_slice_required")
```

- [ ] **Step 2: Run the focused tests and confirm the deep catalog is missing.**

Run:

```powershell
python -m unittest discover -s tools/csharp-evidence -p 'test_semantic_slices.py' -v
```

Expected: FAIL because access edges, claims and provenance outputs do not exist.

- [ ] **Step 3: Add the curated claim register with only bounded facts.**

Store claims in this shape:

```json
{
  "schema_version": "csharp-semantic-claims-v1",
  "claims": [
    {
      "claim_id": "actor.face_selector",
      "field_path": "actors[*].identity.face_id",
      "status": "verified",
      "source_refs": [
        {"source_type": "csharp", "file": "knowledge/csharp/primary/form/GameForm.cs", "line_start": 1663, "line_end": 1663, "symbol": "HumanFaceG"},
        {"source_type": "character_evidence", "file": "knowledge/characters/evidence/bodyface_analysis.json", "symbol": "bodyface_records"}
      ],
      "rationale": "C# stores a face selector and the existing body/face evidence resolves selector records."
    },
    {
      "claim_id": "bubble.timer.lifecycle",
      "field_path": "actors[*].interaction.bubble_id",
      "status": "verified",
      "source_refs": [
        {"source_type": "reverse_report", "file": "knowledge/reverse-engineering/reports/wave4_slices/mainprocess_lifecycle_01.md", "symbol": "MainProcess/DrawObj"},
        {"source_type": "reverse_report", "file": "knowledge/reverse-engineering/reports/wave4_slices/timer_fuki_02.md", "symbol": "CallFuki/MainProcess/DrawObj"}
      ],
      "rationale": "Timer decrement and draw gating are bounded; expiry cleanup remains an adapter rule."
    },
    {
      "claim_id": "legacy.human_mode.raw",
      "field_path": "actors[*].state.legacy.human_mode",
      "status": "raw_only",
      "source_refs": [
        {"source_type": "csharp", "file": "knowledge/csharp/primary/form/GameForm.cs", "line_start": 1617, "line_end": 1617, "symbol": "HumanMode"}
      ],
      "rationale": "The field is preserved, but numeric semantic names are not established."
    }
  ]
}
```

- [ ] **Step 4: Implement method-scope access extraction.**

Add `extract_method_body` using the structural method line span and balanced braces. Within that bounded text, emit an access record for each configured field occurrence with `read`, `write`, `compare`, or `call_argument` operation. Emit call edges for configured method names such as `AddEvent`, `CallFuki`, `AddKaiwa`, `AddMessage`, `DrawHuman` and `DrawObj`. Preserve raw expressions; do not normalize numeric constants into names.

- [ ] **Step 5: Implement claim validation and transition catalog generation.**

Add `build_semantic_slices` and `validate_claims`. Reject a claim when its source file is outside the workspace, its source path does not exist, or its cited line is outside the file. Merge claims into field/method records and default uncited records to `unknown` or `raw_only`. Generate transition records with `trigger`, `reads`, `writes`, `effects`, `semantic_status` and `evidence_refs`.

The generated report must show counts by status and explicitly list unresolved `HumanMode`, `HumanState`, `HumanAnime`, `EventMode`, `MessageGraph` and `DoEvent` gaps.

- [ ] **Step 6: Generate the browser-safe evidence projection.**

Implement `build_runtime_projection` so it copies only schema version, status counts, claim IDs, field paths, semantic status, rationale and compact source references. It must not copy C# source text or embed a whole decompiled file:

```json
{
  "schema_version": "csharp-semantic-runtime-evidence-v1",
  "legacy_equivalence": false,
  "status_counts": {"verified": 2, "candidate": 0, "unknown": 4, "raw_only": 3, "adapter_only": 0},
  "claims": [
    {
      "claim_id": "legacy.human_mode.raw",
      "field_path": "actors[*].state.legacy.human_mode",
      "status": "raw_only",
      "source_refs": [{"file": "knowledge/csharp/primary/form/GameForm.cs", "line_start": 1617, "line_end": 1617}]
    }
  ],
  "unresolved": ["HumanMode", "HumanState", "HumanAnime", "EventMode", "MessageGraph", "DoEvent"]
}
```

Write this artifact to `runtime/office/evidence/semantic_inventory_runtime.json` as part of the same deterministic build, and have the `check` command validate its fingerprint too.

- [ ] **Step 7: Rebuild and check all inventory artifacts.**

Run:

```powershell
python tools/csharp-evidence/build_semantic_inventory.py build
python -m unittest discover -s tools/csharp-evidence -p 'test_semantic_slices.py' -v
python tools/csharp-evidence/build_semantic_inventory.py check
```

Expected: tests pass, every deep record has provenance, raw numeric modes remain raw/unknown, repeated `check` returns the same content fingerprint, and `runtime/office/evidence/semantic_inventory_runtime.json` contains only status/provenance summaries suitable for browser fetch.

### Task 3: Implement and validate the canonical Simulation schema

**Files:**
- Create: `runtime/office/app/simulation_schema.js`
- Test: `runtime/office/tests/test_simulation_schema.js`
- Create: `runtime/office/evidence/simulation_core_contract.json`
- Modify: `runtime/office/tests/test_wave5_contract.py`

**Interfaces:**
- Consumes: `simulation-core-v1` design and inventory provenance policy
- Produces: validated state/command/event constructors for Task 4

- [ ] **Step 1: Write failing schema tests.**

Test canonical root fields, actor fields, allowed adapter/movement statuses, unknown preservation, command normalization, event sequence fields and invalid-state errors.

```javascript
const schema = require(path.join(__dirname, "..", "app", "simulation_schema.js"));

function testInitialState() {
  const state = schema.createSimulationState({ simulationId: "fixture" });
  assert.strictEqual(state.schema_version, "simulation-core-v1");
  assert.strictEqual(state.clock.tick, 0);
  assert.strictEqual(state.legacy_equivalence, false);
  assert.deepStrictEqual(schema.validateSimulationState(state), { valid: true, errors: [] });
}

function testUnknownLegacyStateSurvives() {
  const actor = schema.createActor({ id: "actor.0", raw: { human_mode: 5 } });
  assert.strictEqual(actor.state.semantic, null);
  assert.strictEqual(actor.state.legacy.human_mode, 5);
}

function testInvalidStateIsRejected() {
  const state = schema.createSimulationState({});
  state.clock.tick = -1;
  assert.strictEqual(schema.validateSimulationState(state).valid, false);
  assert.throws(() => schema.assertValidSimulationState(state), (error) => error.code === "invalid_simulation_state");
}
```

- [ ] **Step 2: Run the schema tests and verify they fail.**

Run:

```powershell
node runtime/office/tests/test_simulation_schema.js
```

Expected: FAIL because `simulation_schema.js` and its exports do not exist.

- [ ] **Step 3: Implement the UMD schema module.**

Use the same wrapper style as `runtime/office/app/runtime.js` so both Node tests and browser script loading work:

```javascript
(function (root, factory) {
  if (typeof module === "object" && module.exports) module.exports = factory();
  else root.SimulationSchema = factory();
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
  "use strict";
  const SCHEMA_VERSION = "simulation-core-v1";
  // constructors, validators and stableJson live here
  return { SCHEMA_VERSION, createSimulationState, createActor, createCommand,
    createEvent, validateSimulationState, validateCommand, validateEvent,
    assertValidSimulationState, stableJson };
});
```

Implement deep clone, finite position validation, unique actor IDs, monotonic non-negative clock checks, allowed state lists, event sequence checks, `legacy_equivalence === false`, and provenance record shape validation. Do not use a third-party JSON-schema package.

`createActor({ raw })` must map known raw keys such as `human_mode`, `human_state` and `human_anime` into `actor.state.legacy` and must not create a guessed `state.semantic` value.

- [ ] **Step 4: Write the contract artifact and Python contract assertions.**

Create `simulation_core_contract.json` with schema version, root keys, actor keys, command types, event statuses, adapter states, movement statuses and `legacy_equivalence: false`. Add Python assertions that read this artifact and verify the JavaScript test command is available.

- [ ] **Step 5: Run schema and contract tests.**

Run:

```powershell
node runtime/office/tests/test_simulation_schema.js
python -m unittest runtime/office/tests/test_wave5_contract.py -v
```

Expected: schema tests and all existing Wave 5 contract tests pass.

### Task 4: Build the deterministic SimulationCore reducer

**Files:**
- Create: `runtime/office/app/simulation_core.js`
- Test: `runtime/office/tests/test_simulation_core.js`

**Interfaces:**
- Consumes: `SimulationSchema`, adapter port and Task 3 contract
- Produces: `SimulationCore.dispatch`, `advance`, `snapshot`, `digest`, `subscribe` for Task 5

- [ ] **Step 1: Write failing reducer tests for the first transition slice.**

Cover spawn, state transition, move request, one-tick movement, arrival, blocked movement, invalid command immutability and deterministic digest.

```javascript
function createCore(options = {}) {
  return new SimulationCore({
    state: createSimulationState({ simulationId: "test" }),
    adapter: {
      findPath: options.findPath || (({ from, target }) => ({ status: "path", path: [from, target] })),
      checkCollision: options.checkCollision || (() => "clear"),
      occupySeat: () => ({ result: "occupied" }),
      releaseSeat: () => ({ result: "released" }),
      resolveDialogue: ({ text }) => ({ text: String(text || ""), status: "adapter_text" })
    }
  });
}

function testMoveAndArrival() {
  const core = createCore();
  core.dispatch({ type: "actor.spawn", actor_id: "actor.0", payload: { name: "Aoi", position: [0, 0] } });
  core.dispatch({ type: "actor.move.request", actor_id: "actor.0", payload: { target: [2, 0] } });
  core.advance(2);
  assert.deepStrictEqual(core.getActor("actor.0").position, [2, 0]);
  assert.strictEqual(core.getActor("actor.0").movement.status, "arrived");
}

function testInvalidCommandDoesNotMutate() {
  const core = createCore();
  const before = core.digest();
  assert.throws(() => core.dispatch({ type: "actor.move.request", actor_id: "missing", payload: { target: [1, 1] } }));
  assert.strictEqual(core.digest(), before);
}
```

- [ ] **Step 2: Run the reducer tests and verify they fail.**

Run:

```powershell
node runtime/office/tests/test_simulation_core.js
```

Expected: FAIL because `SimulationCore` is not implemented.

- [ ] **Step 3: Implement command validation and state mutation through one reducer.**

Support these command types:

```text
actor.spawn
actor.move.request
actor.seat.occupy
actor.seat.release
dialogue.request
notification.create
task.projection.update
legacy.event.record
```

Keep `setAdapterState(actorId, state, source)` as a compatibility reducer entry point for existing `TaskSystem` and actor controls. It must emit `state.changed` and use the same transition validation as dispatched commands.

Every successful mutation appends an event with `sequence`, `tick`, `type`, `source`, `status`, `payload` and `provenance`. Every failed mutation validates before cloning/mutating so the digest is unchanged.

- [ ] **Step 4: Implement the logical tick pipeline.**

Implement `advance(count)` with this exact order:

```javascript
for (let index = 0; index < count; index += 1) {
  state.clock.tick += 1;
  advanceMovement();
  advanceActorTimers();
  processQueuedEvents();
  expireBubblesAndNotifications();
  assertValidSimulationState(state);
  notifySubscribers();
}
```

Movement must use `adapter.checkCollision`; bubble/notification expiry uses `expires_at_tick <= clock.tick`; raw legacy event mode/args remain unchanged. `advance(0)` returns a clone without appending an event.

- [ ] **Step 5: Implement subscriptions and stable snapshots.**

`subscribe(listener)` adds a listener and returns an unsubscribe function. Call listeners with `(snapshot, events_since_previous_notification)`. `snapshot()` deep-clones canonical state; `digest()` calls schema `stableJson(snapshot())`.

- [ ] **Step 6: Run core behavior and regression tests.**

Run:

```powershell
node runtime/office/tests/test_simulation_schema.js
node runtime/office/tests/test_simulation_core.js
node runtime/office/tests/test_wave5_runtime.js
```

Expected: new core scenarios pass and existing runtime tests remain green before the facade migration.

### Task 5: Migrate OfficeRuntime to the core without breaking providers

**Files:**
- Modify: `runtime/office/app/runtime.js`
- Modify: `runtime/office/app/index.html` — load schema/core before the runtime facade
- Modify: `runtime/office/tests/test_wave5_runtime.js`
- Modify: `runtime/office/tests/test_wave5_contract.py`
- Modify: `runtime/office/evidence/simulation_core_contract.json`

**Interfaces:**
- Consumes: `SimulationCore`, `SimulationSchema`, existing manifest/bodyface/path/collision/seat/locale providers
- Produces: compatibility `OfficeRuntime` facade whose state mutation is delegated to core

- [ ] **Step 1: Add a failing facade ownership assertion.**

Add a test that creates `OfficeRuntime`, adds an actor, calls `requestMove`, advances two ticks and asserts that `runtime.snapshot().actors[0]` and `runtime.core.snapshot().actors[0]` have identical canonical data. Also assert that `runtime.agents`, `runtime.bubbles` and `runtime.events.records` are projections, not independently mutated stores.

```javascript
function testRuntimeDelegatesToCore() {
  const runtime = createRuntime();
  runtime.addAgent({ id: "actor.0", position: [0, 0] });
  runtime.requestMove("actor.0", [2, 0]);
  runtime.step(2);
  assert.deepStrictEqual(runtime.snapshot().actors, runtime.core.snapshot().actors);
  assert.strictEqual(runtime.clock.value, runtime.snapshot().clock.tick);
}
```

- [ ] **Step 2: Run the facade test and verify it fails against the current split state.**

Run:

```powershell
node runtime/office/tests/test_wave5_runtime.js
```

Expected: FAIL because the current runtime has no `core` and its snapshot uses the old office-only shape.

- [ ] **Step 3: Construct SimulationCore from existing providers.**

In `OfficeRuntime` constructor, build the adapter port from the current providers:

```javascript
this.core = new SimulationCore({
  state: createSimulationState({
    simulationId: options.simulationId || "office-demo",
    evidence: options.evidence || {},
    scene: { scene_id: this.manifest.scene_id || "office.floor0", room_id: this.manifest.room_id || "office.floor0.adapter", objects: this.manifest.objects || [] }
  }),
  adapter: {
    findPath: ({ actorId, from, target }) => this.pathProvider.findPath(from, target, { actor_id: actorId }),
    checkCollision: ({ actorId, position }) => this.collisionProvider.check(position, { actor_id: actorId }),
    occupySeat: ({ actorId, seatId }) => this.seatProvider.occupy(actorId, seatId),
    releaseSeat: ({ actorId, seatId }) => this.seatProvider.release(actorId, seatId),
    resolveDialogue: (input) => this.localeStore.resolve(input.languageId, input.locale, input.args || [])
  }
});
```

Preserve manifest, bodyface, animation policy and asset base on the facade for rendering.

- [ ] **Step 4: Replace mutating methods with core delegates.**

Change the runtime UMD wrapper so Node injects `require("./simulation_schema.js")` and `require("./simulation_core.js")`, while the browser injects `root.SimulationSchema` and `root.SimulationCore`. Inside the factory use `schema.createSimulationState(...)` and `coreExports.SimulationCore`; do not reach into browser globals from the core implementation.

Add these script tags before `runtime.js` so the browser resolves the same UMD exports used by Node tests:

```html
<script src="./simulation_schema.js"></script>
<script src="./simulation_core.js"></script>
<script src="./runtime.js"></script>
```

Map `addAgent`, `requestMove`, `occupySeat`, `releaseSeat`, `addBubble`, `requestDialogue`, `addNotification`, `setState`, `setAgentTaskProjection`, `recordAdapterEvent`, `recordRawEvent`, `step`, `snapshot` and `digest` to core commands or core methods. Do not leave a second actor/bubble/notification mutation path in `runtime.js`.

- [ ] **Step 5: Add read-only compatibility projections.**

Expose `clock.value`, `agents`, `bubbles`, `notifications` and `events.records` as getters built from the latest canonical snapshot. `runtime.agents` must remain a `Map` because `app.js` and `TaskSystem` iterate it; the map values are clones. `runtime.events.records` must remain an array for existing event-log rendering.

- [ ] **Step 6: Adapt render commands to canonical actors while preserving draw contracts.**

Keep body/face lookup, animation policy, object draw ordering and asset URLs unchanged. Make `renderCommands()` read actor/bubble/notification projections from `core.snapshot()` and retain `legacy_equivalence: false` in its output.

- [ ] **Step 7: Run the full office/dashboard regression set.**

Run:

```powershell
node --check runtime/office/app/simulation_schema.js
node --check runtime/office/app/simulation_core.js
node --check runtime/office/app/runtime.js
node runtime/office/tests/test_simulation_schema.js
node runtime/office/tests/test_simulation_core.js
node runtime/office/tests/test_wave5_runtime.js
python -m unittest runtime/office/tests/test_wave5_contract.py -v
node runtime/dashboard/tests/test_wave6_task_system.js
python -m unittest runtime/dashboard/tests/test_wave6_contract.py -v
```

Expected: old Wave 5/Wave 6 behavior remains green and new canonical ownership assertions pass.

### Task 6: Connect task projection and provenance to the dashboard diagnostics

**Files:**
- Modify: `runtime/dashboard/tests/test_wave6_task_system.js`
- Modify: `runtime/dashboard/tests/test_wave6_contract.py`
- Modify: `runtime/office/app/app.js`
- Modify: `runtime/office/app/index.html`
- Modify: `runtime/office/evidence/simulation_core_contract.json`

**Interfaces:**
- Consumes: `OfficeRuntime.subscribe`, `SimulationState.task_projection`, existing `TaskSystem` lifecycle
- Produces: dashboard view that shows canonical actor/task/scene/event/evidence state without duplicating task ownership

- [ ] **Step 1: Write failing task-projection integration tests.**

Extend the Wave 6 host fixture so `TaskSystem.assignTask` and `startTask` are followed by assertions against `runtime.snapshot().actors[0].activity` and the core event log.

```javascript
const task = tasks.createTask({ title: "Canonical projection" });
tasks.assignTask(task.id, "actor.0");
assert.deepStrictEqual(runtime.getAgent("actor.0").taskId, task.id);
assert.strictEqual(runtime.snapshot().actors[0].activity.task_id, task.id);
tasks.startTask(task.id, "actor.0");
assert.strictEqual(runtime.snapshot().actors[0].activity.task_status, "working");
assert(runtime.snapshot().event_log.some((event) => event.type === "task.projection.updated"));
```

- [ ] **Step 2: Run the focused dashboard test and verify the canonical projection is absent.**

Run:

```powershell
node runtime/dashboard/tests/test_wave6_task_system.js
```

Expected: FAIL because the current runtime projection is not represented in `SimulationState.activity`.

- [ ] **Step 3: Route `TaskSystem` projection calls through the facade.**

Keep the existing callbacks in `createTaskSystem`, but make `runtime.setAgentTaskProjection` dispatch the canonical projection update. Keep full task objects, persistence and notifications owned by `TaskSystem`; only actor-facing `task_id` and `task_status` enter SimulationState.

Load `runtime/office/evidence/semantic_inventory_runtime.json` during boot, keep it in `window.SEMANTIC_EVIDENCE`, and pass it as `evidence` when `resetRuntime()` constructs `OfficeRuntime`. The browser may fetch this generated summary but must not fetch or execute any C# source file.

- [ ] **Step 4: Subscribe diagnostics to canonical snapshots.**

Change `updatePanels(commands)` to obtain `const snapshot = runtime.snapshot()` and include these exact sections in diagnostics:

```javascript
simulation: {
  schema_version: snapshot.schema_version,
  tick: snapshot.clock.tick,
  scene: snapshot.scene,
  actor: snapshot.actors.find((item) => item.id === selectedId) || null,
  task_projection: snapshot.task_projection,
  evidence: snapshot.evidence,
  legacy_equivalence: snapshot.legacy_equivalence
}
```

Keep the existing draw diagnostics and event list, but make the canonical state the displayed source. Do not import C# files in browser code.

- [ ] **Step 5: Add a visible evidence/provenance panel without adding playback controls.**

Add `<pre id="evidencePanel">—</pre>` under Diagnostics and render selected actor provenance plus unresolved status counts. Keep task management buttons such as Create, Assign, Start and Complete; only simulation playback controls are removed in Task 7.

- [ ] **Step 6: Run dashboard contract tests.**

Run:

```powershell
node runtime/dashboard/tests/test_wave6_task_system.js
python -m unittest runtime/dashboard/tests/test_wave6_contract.py -v
```

Expected: task lifecycle remains 18 scenarios, task ownership remains in `TaskSystem`, and canonical actor projection is visible through the runtime snapshot.

### Task 7: Replace playback UI with an internal continuous scheduler

**Files:**
- Create: `runtime/office/app/continuous_scheduler.js`
- Create: `runtime/office/tests/test_continuous_scheduler.js`
- Modify: `runtime/office/app/index.html`
- Modify: `runtime/office/app/app.js`
- Modify: `runtime/office/app/style.css`
- Modify: `runtime/office/tests/test_wave5_contract.py`

**Interfaces:**
- Consumes: `OfficeRuntime.step(1)`/`subscribe` and browser timer APIs
- Produces: automatic simulation start with no visible playback controls

- [ ] **Step 1: Write failing scheduler tests with injected timer functions.**

Use fake `setInterval`/`clearInterval` functions so the test never sleeps:

```javascript
function testSchedulerStartsOnceAndStopsInternally() {
  let callback = null;
  let cleared = null;
  let ticks = 0;
  const scheduler = new ContinuousScheduler({
    intervalMs: 160,
    tick: () => { ticks += 1; },
    setIntervalFn: (fn, ms) => { callback = { fn, ms }; return 7; },
    clearIntervalFn: (id) => { cleared = id; }
  });
  scheduler.start();
  scheduler.start();
  assert.strictEqual(callback.ms, 160);
  callback.fn();
  assert.strictEqual(ticks, 1);
  scheduler.stop();
  assert.strictEqual(cleared, 7);
}
```

- [ ] **Step 2: Run the scheduler test and verify it fails.**

Run:

```powershell
node runtime/office/tests/test_continuous_scheduler.js
```

Expected: FAIL because the scheduler module does not exist.

- [ ] **Step 3: Implement `ContinuousScheduler`.**

Export a UMD module with:

```javascript
class ContinuousScheduler {
  constructor({ intervalMs = 160, tick, onError, setIntervalFn, clearIntervalFn }) {}
  start() {}
  stop() {}
  isRunning() {}
}
```

`start()` must be idempotent; `stop()` must clear the exact timer ID; `tick` exceptions must be caught and forwarded to an optional `onError` callback without creating a second timer.

- [ ] **Step 4: Remove simulation playback controls from the HTML.**

Delete only the scene toolbar elements with IDs `playButton`, `stepButton` and `resetButton`; keep task management `taskResetButton` because it resets task data, not simulation time. Replace the toolbar with the tick label and a static `continuous` status. Change the stale `PHASE 6 / WAVE 6` eyebrow to `C#-FIRST OFFICE SIMULATION`.

- [ ] **Step 5: Start the scheduler automatically in `app.js`.**

Remove `playing`, `timer`, the three playback event listeners and all button references. Add:

```javascript
let scheduler;

function startSimulationLoop() {
  scheduler = new window.ContinuousScheduler({
    intervalMs: 160,
    tick: () => runtime.step(1),
    onError: (error) => {
      $("runtimeStatus").textContent = "SIMULATION ERROR";
      $("diagnostics").textContent = String(error.stack || error);
    }
  });
  scheduler.start();
}
```

Load `continuous_scheduler.js` before `app.js`, call `startSimulationLoop()` after the initial runtime/task setup, and render from the latest snapshot on every tick. Do not expose `scheduler.stop()` in the DOM.

- [ ] **Step 6: Update browser/static contract tests.**

Assert that `index.html` has no `playButton`, `stepButton` or simulation `resetButton`, `app.js` has no playback listener references, `continuous_scheduler.js` is loaded, and the task reset control still exists. Keep the scheduler interval at 160 ms and do not add speed controls.

- [ ] **Step 7: Run runtime and browser smoke checks.**

Run:

```powershell
node --check runtime/office/app/continuous_scheduler.js
node --check runtime/office/app/app.js
node runtime/office/tests/test_continuous_scheduler.js
node runtime/office/tests/test_wave5_runtime.js
python -m unittest runtime/office/tests/test_wave5_contract.py -v
```

Then serve the workspace root on the configured local port only after checking listeners, open `runtime/office/app/index.html`, and verify:

```text
runtime status becomes READY · tick N with N increasing without clicks
scene and actors render
task create/assign still works
diagnostics contains simulation schema/tick/evidence
browser console errors is []
```

Stop the exact server process started for this smoke test and verify no listener remains.

### Task 8: Final verification, reports and handoff

**Files:**
- Modify: `runtime/office/README.md`
- Modify: `runtime/office/reports/simulation_core_architecture.md`
- Modify: `PROJECT_STATE.md`
- Modify: `TODO.md`
- Verify: all generated inventory/core evidence artifacts

**Interfaces:**
- Consumes: outputs from Tasks 1–7 and all regression suites
- Produces: verified handoff state with explicit unresolved semantic gaps

- [ ] **Step 1: Add the implementation architecture report.**

Document the final ownership boundary, command/event contract, compatibility facade, tick order, provenance policy, continuous scheduler and known non-equivalence. Include exact test commands and observed counts; do not describe tests as passing until they have been run in this task.

- [ ] **Step 2: Run inventory verification and source immutability checks.**

Run:

```powershell
python tools/csharp-evidence/build_semantic_inventory.py check
git status --short -- game-dev-story-mod_Sprites game-dev-story-mod_Dumped game-dev-story-mod_Extracted APK_Toolkit ghidra_11.0.1_PUBLIC viewer
```

Expected: inventory check passes and protected source roots have no changes.

- [ ] **Step 3: Run the complete regression suite.**

Run:

```powershell
python -m unittest discover -s tools/csharp-evidence -p 'test_*.py' -v
python -m unittest discover -s knowledge/characters/tests -p 'test_*.py' -v
python -m unittest discover -s tools/reverse-engineering/tests -p 'test_*.py' -v
python -m unittest tools/maintenance/test_workspace_layout.py -v
python -m unittest discover -s runtime/office/tests -p 'test_*.py' -v
python -m unittest discover -s runtime/dashboard/tests -p 'test_*.py' -v
node runtime/office/tests/test_simulation_schema.js
node runtime/office/tests/test_simulation_core.js
node runtime/office/tests/test_continuous_scheduler.js
node runtime/office/tests/test_wave5_runtime.js
node runtime/dashboard/tests/test_wave6_task_system.js
```

Expected: existing baselines remain green, new inventory/schema/core/scheduler tests pass, and no test creates a long-running process.

- [ ] **Step 4: Run Python compile and JavaScript syntax checks.**

Run:

```powershell
python -m py_compile tools/csharp-evidence/semantic_inventory.py tools/csharp-evidence/build_semantic_inventory.py tools/csharp-evidence/test_semantic_inventory.py tools/csharp-evidence/test_semantic_slices.py
node --check runtime/office/app/simulation_schema.js
node --check runtime/office/app/simulation_core.js
node --check runtime/office/app/runtime.js
node --check runtime/office/app/continuous_scheduler.js
node --check runtime/office/app/app.js
```

- [ ] **Step 5: Update state only with observed facts.**

In `PROJECT_STATE.md`, record generated artifact paths, exact test counts, browser smoke result, continuous scheduler behavior and remaining unknowns. In `TODO.md`, check only milestones whose commands passed; leave LLM/backend/auth/multi-user work unchecked.

- [ ] **Step 6: Perform final diff/path/cache hygiene.**

Run `git -c core.whitespace=cr-at-eol diff --check`, active stale-path scans, required-path scans and explicit cleanup of only task-created `__pycache__`, `.corpus.*.tmp` and report temp files under the workspace. Confirm no local server remains and no protected root appears in the diff.

## Self-review checklist for the implementer

Before claiming completion, verify:

- Every spec section maps to at least one task above.
- The inventory output never writes under `knowledge/csharp/primary/`.
- `HumanMode`, `HumanState`, `HumanAnime`, `EventMode` and `MessageGraph` remain raw/unknown unless a new source-backed claim is added.
- `SimulationCore` owns mutation and `OfficeRuntime` exposes projections only.
- `TaskSystem` still owns full task lifecycle and persistence.
- `SimulationState`, command and event function names match the shared interfaces exactly.
- The UI removes only simulation playback controls, not task-management controls.
- The scheduler has no visible stop/pause/speed path.
- All success claims are backed by fresh command output from the final workspace.

## Execution handoff

Plan complete and saved to `docs/superpowers/plans/2026-08-12-csharp-semantic-inventory-simulation-core.md`. Implementation should start at Task 1 and stop after each task's focused test plus regression checkpoint. In this shared workspace, do not commit, push or create a PR until the user explicitly requests integration.
