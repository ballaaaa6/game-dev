# Project State

## Current Status — R3 whole-game CFG repair closed (2026-08-18)

## R3 whole-game CFG repair — complete

- `status`: `PASS_R3_WHOLE_GAME_CFG_REPAIR_CLOSED` with decision `PASS_WITH_EXPLICIT_CFG_DEFERRAL`.
- The canonical R3 profiler reproduced the corrected R1.5/R2 universe: 641 target types, 10,827 methods/queue rows, 2,634 R2 identity blockers, and 2,856 active CFG rows (2,708 direct plus 148 exact source-body identity recoveries).
- All 2,634 identity blockers are root-cause counted: 2,572 routed with exact source-body or ISIL identity evidence and 62 explicitly remain blocked. No first-overload or declaring-type guess was used.
- Every active CFG row has a local evidence bundle with exact source body/hash, R0/R1.5 signals, ISIL facts, callers/callees, field/static references, accepted evidence references, and Roslyn diagnostic availability. Observed families and risks are recorded in `knowledge/brain/acceptance/r3-whole-game-cfg-repair/r3-cfg-family-summary.json`.
- The Roslyn-only family-first transformer library and strict planner authorize zero canaries because semantic binding and graph-equivalence proof are unavailable for this external-reference corpus. `OTHER_CFG` remains explicitly ineligible for generic cleanup.
- All five mandatory negative fixtures reject; the second canonical profiler run reproduces all compact indexes and all 2,856 bundle hashes. The graph delta is zero, the original source roots remain read-only, and no native body lift, Unity, V8/web, runtime, integration, persistence, or backend work was started.
- Compact acceptance evidence and the report are under `knowledge/brain/acceptance/r3-whole-game-cfg-repair/`; heavy bundles remain local-only under `artifacts/r3-preflight/`.
- Next authorized boundary is `R4_NATIVE_ISIL_SEMANTIC_LIFT`; R4 is not started.

## Git-visible current gate

- `current_phase`: `R3_WHOLE_GAME_CFG_REPAIR`
- `status`: `PASS_R3_WHOLE_GAME_CFG_REPAIR_CLOSED`
- `next_authorized_phase`: `R4_NATIVE_ISIL_SEMANTIC_LIFT`
- `next_phase_started`: `false`

## R2 automated whole-corpus repair closed (2026-08-18)

## R2 automated whole-corpus repair — complete

- `status`: `PASS_R2_AUTOMATED_WHOLE_CORPUS_REPAIR_CLOSED`.
- The canonical prework profiler was rerun from the tracked `tools/social-dev/r2_prework_probe.py` against `artifacts/r1-5-metadata-reconciliation/`: 10,827 methods and queue rows; 429 type-repair candidates split into 8 `SAFE_CANARY` and 421 `REVIEW_WAVE_2`.
- The pinned APK, C# archive, `libil2cpp.so`, and `global-metadata.dat` identities match. The source gate remains 5,568 files, 5,504 C# files, and 55,358,557 C# bytes.
- The installed machine has no SDK rows, but the local bundled .NET 10 PowerShell host exposes Roslyn 5.0.0.0. Offline parse and dynamic compilation/emit passed; no network packages were installed and regex was not used for mutation.
- The separate ignored Reference Twin is under `artifacts/r2-reference-twin/`; 442 target-closure files were mirrored without modifying the original C# source roots.
- The strict Roslyn identity gate produced 4 exact syntax-only repairs: two `FieldInitializer.RestoreFields` overloads, `Bundle` construction, and the `MeshManager` constructor. All 4 were applied in batch `r2-type-canary-001` with complete provenance and deterministic replay.
- Final R2 status coverage is exactly 10,827/10,827: 4 `REPAIRED_CSHARP`, 2,327 `BASELINE_READABLE`, 2,708 `DEFER_R3_CFG`, 2,674 `DEFER_R4_NATIVE`, 442 `DEFER_R2_UNPROVEN_MECHANICAL`, 38 `SOURCE_LIMITED`, and 2,634 `BLOCKED_IDENTITY`.
- Static/exporter, decompiler-noise, CFG, and native body repairs were not guessed. The conservative Twin reindex reconciles the accepted R1.5.1 graph split with zero delta. Native lifting, V8/Unity, runtime, and original-source mutation remain untouched.
- Compact acceptance evidence is under `knowledge/brain/acceptance/r2-automated-whole-corpus-repair/`. The next authorized boundary is `R3_WHOLE_GAME_CFG_REPAIR`; stop here.

## Accepted baseline — R1.5 metadata reconciliation complete (2026-08-17)

## R2 accepted baseline gate

- `current_phase`: `R2_AUTOMATED_WHOLE_CORPUS_REPAIR` (historical accepted baseline)
- `status`: `PASS_R2_AUTOMATED_WHOLE_CORPUS_REPAIR_CLOSED`
- `R1.5`: `PASS`
- `R1`: `PASS — superseded by corrected R1.5 metadata identities`
- `V8`: `PASS (prior completed phase)`
- `live_room0`: `true`
- `autonomous_no_task_living`: `true`
- `required_visual_fallback_count`: `0`
- `next_authorized_phase`: `R3_WHOLE_GAME_CFG_REPAIR`
- `next_phase_started`: `false`
- `R1.5.1`: `PASS_R1_5_1_STATE_AND_CLOSURE_SYNC`
- `R2`: `PASS_R2_AUTOMATED_WHOLE_CORPUS_REPAIR_CLOSED`

## R1.5 metadata identity reconciliation and repair-universe correction — complete (2026-08-17)

- Pinned source identity and the attached alternate evidence-pack hashes pass. The evidence pack is `D:/downloads/R1_5_METADATA_RECONCILIATION_EVIDENCE_PACK.zip`; its raw `dump.cs`, `script.json`, and selected DummyDll files are retained as cross-check evidence only. Original Google-derived catalogs remain non-canonical.
- The dnfile contract was confirmed: bracket table indexing is 0-based while RID lookup is 1-based. The old `table[1:]` path discarded the first real metadata row; the corrected builder now consumes the full table sequence and audits every RID/token/list conversion.
- Corrected canonical metadata contains 64 metadata-present assemblies, 8,373 types, 62,945 methods, and 40,668 fields. The corrected target universe is 641 types and 10,827 methods: 198 GAME_FIRST_PARTY types / 4,547 methods and 443 KAIRO_ENGINE types / 6,280 methods. The complete queue covers every target method exactly once; repaired C# bodies remain `0`.
- All 64 assemblies were compared with the independent alternate dump: canonical/alternate totals are 8,373/8,372 types and 62,945/62,943 methods. Discrepancies are explicit: 25 DUMPER_VERSION_DIFFERENCE, 1 GENERATED_TYPE_NAMING_DIFFERENCE, 35 REPRESENTATION_DIFFERENCE, and 3 MATCH rows for both type and method comparisons.
- Core-nine identity is PASS, including normal `main.AppData`, normal `form.GameForm`, and `game.routeSearch.Node` with 3 methods. Ownership, source/R0/ISIL joins, and compiler-generated exclusion were rebuilt after the metadata correction.
- The corrected dependency split is explicit: calls are 13,512 resolved-owned, 8,668 resolved-external, 104,306 owned-unresolved, 5,306 ambiguous, and 0 source-limited; fields are 4,151 resolved-owned, 1,978 resolved-external, 18,246 owned-unresolved, 8,549 ambiguous, and 0 source-limited. The compact R1.5.1 validation summary is `knowledge/brain/acceptance/r1-5-metadata-reconciliation/r1-5-1-dependency-split-summary.json`; unresolved edges remain distinct from external-resolved edges. SCCs: 10,801; recursive SCCs: 348; largest SCC: 4 methods; dependency layers: 19.
- Deterministic rerun, builder validation, source gate, alternate reconciliation, core identity, queue coverage, dependency split, and no-body-repair gates pass. R2, native lifting, runtime/Unity, integrations, persistence/backend, deployment, and source-root mutation remain outside this phase.
- Heavy corrected catalogs are local-only under `artifacts/r1-5-metadata-reconciliation/`. The compact accepted package and report are under `knowledge/brain/acceptance/r1-5-metadata-reconciliation/`.

## R1 whole-corpus ownership index and repair queue — complete (2026-08-17)

The R1 architecture remains retained as historical evidence, but its pre-R1.5 canonical metadata counts, IDs, repair queue, and graph are explicitly `SUPERSEDED_BY_R1_5` (`SUPERSEDED_BY_R1_5_METADATA_RECONCILIATION`) because of the confirmed metadata table first-row defect. The old 8,678-method repair universe is not active; future repair work must consume only the corrected R1.5 queue.

- Pinned APK, C# archive, libil2cpp, and global-metadata identities: MATCH.
- The source gate measured 5,568 files, 5,504 C# files, 64 project files, 55,358,557 C# bytes, and retained all three zero-byte C# files.
- DummyDll authority indexed 64 assemblies, 8,309 types, 62,884 metadata methods, and 40,615 fields. The owned non-generated target catalog contains 557 types and 8,678 methods: 3,081 GAME_FIRST_PARTY and 5,597 KAIRO_ENGINE.
- The exact taxonomy is GAME_FIRST_PARTY, KAIRO_ENGINE, UNITY_BOUNDARY, DOTNET_FRAMEWORK, THIRD_PARTY, COMPILER_GENERATED, and SOURCE_LIMITED_OWNERSHIP; assembly authority exceptions are recorded for namespace/path mismatches.
- Stable method identity uses the pinned APK hash, assembly, declaring type, method name, generic arity, return type, and ordered parameter types, with deterministic metadata-token disambiguation only for duplicate metadata identities.
- Quality, verification, and disposition are separate. The queue covers all 8,678 target methods exactly once, with zero repaired C# bodies.
- The historical graph contains 9,392 owned call edges, 87,175 external/unresolved edges, 8,769 field edges, 9,067 static-data edges, 8,656 SCCs, and 407 recursive SCCs. These pre-R1.5 counts are retained for audit only and are `SUPERSEDED_BY_R1_5`. Fresh ISIL contains 6,682 files and 62,943 method blocks; 5,970 target methods have native/ISIL availability.
- Core-nine validation is PASS; AppData and GameForm are explicit DummyDll compiler-generated identity gaps, not silently promoted aliases.
- Validation passed with the standalone validator, builder --check, source identity checks, deterministic ordering/manifest checks, and git diff --check.
- Heavy artifacts are local-only under artifacts/r1-whole-corpus-index/. The compact accepted package is under knowledge/brain/acceptance/r1-whole-corpus-index/.
- STOP before R2. No C# repair, native lifting, runtime, Unity, V8/V8R, emulator, integration, persistence, backend, deployment, or source-root mutation was performed.

## R1.5.1 state and closure synchronization — complete (2026-08-17)

- The active canonical Twin universe is the corrected R1.5 universe: 641 types and 10,827 methods, with 198 GAME_FIRST_PARTY / 4,547 methods and 443 KAIRO_ENGINE / 6,280 methods; the complete repair queue is 10,827 and repaired C# bodies remain 0.
- The old R1 result and its 8,678-method universe remain retained for audit history only and are marked `SUPERSEDED_BY_R1_5`.
- Closure validation passed for JSON/JSONL parsing, corrected state/count consistency, explicit R1 supersession, exact next phase `R2_AUTOMATED_WHOLE_CORPUS_REPAIR`, graph split reconciliation, and `git diff --check`. No R2, C# repair, runtime/V8/Unity/Unity-MCP, or source-root work was started.

V8 was explicitly authorized in the user request. The prompt was read completely
before the Sol pack was extracted and inspected. The Sol pack was treated as a
detailed implementation hypothesis and reconciled against the current runtime,
the canonical K4/K4.1 brain and artifacts, and pinned local C# evidence. All
nine Sol findings are classified `CONFIRMED_CURRENT_GAP`; none are
`SUPERSEDED_BY_LOCAL_STATE` or `CORRECTED_AFTER_LOCAL_INSPECTION`. The complete
record is `knowledge/brain/acceptance/v8/gap-classification.json`.

The live runtime now boots Room0 directly at `/`, projects the source-backed
three-Staff autonomous living scene, composes the native nine-pass draw order,
uses the complete human character catalog, applies source-backed alpha and
direction selectors, renders both native workstation interleaves, projects
Fukidashi payload/lifetime guards and the exact equipment selector cadence, and
keeps product task state owned by the canonical LivingRuntime. Required visual
fallbacks, unresolved selectors, and duplicate workstation Staff draws are zero.

V8 implementation files are under `runtime/social-dev/src/v8/`, with the live
runtime/compositor integration in the existing app, renderer, visual-gate, and
scene-mask files. Regression coverage is in
`runtime/social-dev/tests/v8-live-room0.test.ts`. Acceptance artifacts and the
closure report are under `knowledge/brain/acceptance/v8/`.

Verification passed: typecheck; Vitest (`49` files / `323` tests); production
build; K2 unified brain; K4 visual closure; K4.1 targeted closure; V7; I1; I2;
and `git diff --check`. The K2/K4/K4.1 validators passed before the V8 state
transition with zero blocking source-limited, source-missing, and
heuristic/assumed findings.

Browser smoke reused the healthy repository Vite server at
`http://127.0.0.1:4173` and recorded no console errors or warnings. `/`,
`/?auto=0`, and `/?auto=0&initialTicks=35` passed; the deterministic frame-35
route reached 63/63 required visibility with zero occlusion, zero fallback
markers, and zero unresolved selectors. A live observation reached the
accepted invitation path and displayed the native English Fukidashi payload.

Source roots, canonical brain bytes, and generated packs remain unchanged by
V8. Backend, persistence, authentication, cloud integrations, deployment,
emulator/ADB, and network integration remain unopened. No next phase is
authorized without an explicit user request.

## R0 Cpp2IL corpus and recovery-mode audit — complete (2026-08-17)

- Pinned APK, libil2cpp.so, global-metadata.dat, and C# RAR identity: `MATCH`.
- Independent corpus: 5,568 files, 5,504 C# files, 64 project files, 3 zero-byte C# files, and 55,358,557 C# bytes.
- Accepted primary method baseline: 41,229 methods; 33,552 CLEAN (81.38%); 4,012 NATIVE_LIFT_REQUIRED (9.73%); readable without native lifting 83.21%. The raw lexical declaration index is 43,103 and is retained separately for traceability.
- Historical invocation was recovered with high confidence: Cpp2IL forced Unity `2022.3.62`, followed by `ilspycmd 11.0.0.9375`. A local fresh `Cpp2IL 2022.1.0` rerun against the pinned native inputs produced IL recovery DLLs, Diffable C#, and ISIL evidence.
- Fresh high-level C# improvement: `0`; method-dump improvement: `0`; intermediate-representation improvement: `14`. Zero-byte files are classified as exporter/generated-type loss, and the metadata/static-data recovery pass is justified.
- Final measured recommendation: `HYBRID` — retain the existing C# skeleton and use fresh ISIL/native/static-data evidence selectively. The R0 package is under `knowledge/brain/acceptance/r0-cpp2il-audit/`.
- Stop boundary: no V8/V8R continuation and no C# repair started. The next authorized boundary is `R1_CORE_CSHARP_REPAIR`, not started.

## Current Status — K4.1 targeted visual closure complete (2026-08-17)

## Git-visible current gate

- `current_phase`: `K4.1`
- `status`: `PASS_K4_1_TARGETED_CLOSURE_READY_FOR_V8`
- `ready_for_v8`: `true`
- `V8`: `NOT_STARTED`
- `brain_revision`: `k4-visual-assembly-r2`

K4.1 independently reproduced the three remaining K4 blockers from the pinned
APK, C# archive/extracted C#, libil2cpp.so, global-metadata.dat, dump,
language resources, accepted Room0 contracts, and native draw consumers. The
canonical brain is revision `k4-visual-assembly-r2` with status
`K4_CLOSED_VISUAL_ASSEMBLY` and final token
`PASS_K4_1_TARGETED_CLOSURE_READY_FOR_V8`.

- Coverage contains 49 reachable consumers and 42 visible consumers:
  39 PROVEN_CANONICAL, 2 PROVEN_NOT_CANONICAL, 8 NO_DISTINCT_VISUAL, 2
  NOT_REACHABLE, 0 SOURCE_LIMITED, 0 SOURCE_MISSING, and 0
  heuristic/assumed records. The required counts are all zero for
  blocking_source_limited, source_missing, and heuristic_or_assumed.
- `room0.door.action-timeline` is `REPRODUCED_WITH_CORRECTION`: Room0's
  installed raw type-5 door has null FurnitureData, so DrawWall keeps the
  fixed door visual consumer; native action/update/fade state is retained
  separately and no door frames were invented.
- `staff.talk.fukidashi-payload` is `REPRODUCED_EXACT`: autonomous and
  invitation speaker roles, timing, five exact native pools, random selection,
  EN/JA APK rows, Language path, [id,40,delay,offsetY] storage, lifetime,
  offset, draw guards, and partner cleanup are closed. The unsupported
  `0x27D7E40` pool is `REJECTED_BY_SOURCE`.
- `workstation.live-interleave` is `REPRODUCED_EXACT`: live Room0 type-2
  drawing is preview=false, with direction-specific desk/chair/Staff.Draw
  ordering, the late foreground chair guard, and the installed-path guard
  preventing duplicate Staff rendering.
- K4.1 artifacts are under `knowledge/brain/acceptance/k4-1/`; 11 canonical
  K4 facts and 10 verified K4 edges are recorded. Original generated
  runtime/data/visual packs, source roots, runtime code, and MapChip pixels
  remain byte-stable/unchanged.
- Verification passed: K4/K4.1 artifact validators, K2 unified brain,
  native registry/catalog/floor/display gates, runtime typecheck, and full
  Vitest (48 files / 314 tests). Source hashes and generated-pack snapshots
  are unchanged.

Next boundary: V8 remains `NOT_STARTED`; readiness is true for a future
explicitly authorized V8 phase. No V8, runtime implementation, pixel tuning,
server, browser, emulator/ADB, live app, network, or subagent work was used.

## Prior Status — K3 targeted missing-link closure closed (2026-08-16)

K3 closed with status `PASS_K3_TARGETED_MISSING_LINK_CLOSURE_CLOSED`.

- The three queued records in `knowledge/gaps/k3-gap-queue.json` are `CLOSED`: `K3-GAP-FLOOR-DIRECT-SELECTOR`, `K3-GAP-FURNITURE-VISUAL`, and `K3-GAP-CANDIDATE-EDGES`.
- Floor closure is source/native-backed: `RoomData.floorImgId_=5` is retained as `ROOMDATA_FLOOR_IMAGE_INDEX:5`; native `Room.FLOOR_IMAGE_ID_ARRAY[5]` resolves to `IMAGE_SELECTOR_ID:23`, and the pinned `chip/img.inf` row resolves to `floor_05.png`. The runtime compatibility alias `COMPATIBILITY_ALIAS_ID:85` remains separate and no MapChip pixel asset was changed.
- FurnitureData 26 closure is source/native-backed: raw type `1`, `SEB_SELECTOR_ID:21`, secondary sentinel `SEB_SELECTOR_ID:-1`, `IMAGE_SELECTOR_ID:106`, and native initial `SPRITE_FRAME_ID:furniture:26:0` resolve to the accepted `old_printer.png` frame record.
- All `185` candidate semantic-edge records are classified exactly: `1 CONFIRMED` (Staff route) and `184 REJECTED` (sentinel-null or wrong direct HelperData human-selector claims); `0 UNRESOLVED`. Corrected HelperData chains use `STAFF_DATA_ID` and then `StaffData.img_` as `IMAGE_SELECTOR_ID`.
- The canonical brain revision is `k3-targeted-closure-r1`; the accepted native registry/catalog, queue export, semantic graph, K3 runtime closure contracts, query results, evidence manifest, final validation, and closure report are regenerated under the prescribed active topology.
- Verification passed: K3 builder/closure token, K2 unified brain validation, native registry/catalog/floor/display gates, runtime typecheck, full Vitest (`48` files / `314` tests), and `git diff --check`. No V8, network research, deployment, persistence/backend work, integrations, emulator/ADB, live app, local server, or subagent work was started.

Final K3 evidence: `knowledge/brain/acceptance/k3/final-validation.json`, `gap-resolution.json`, `query-results.json`, `evidence-manifest.json`, `K3_CLOSURE_REPORT.md`, the three accepted runtime closure contracts, and the closed queue.

Next boundary: K3 is closed; V8, integrations, deployment, persistence/backend work, and other excluded boundaries remain unopened without a separate user-directed phase.

## Prior Status — K2.5 canonical knowledge promotion and legacy distillation closed (2026-08-16)

K2.5 completed with status `PASS_K2_5_CANONICAL_KNOWLEDGE_PROMOTION_AND_LEGACY_DISTILLATION_CLOSED`.

- At the K2.5 boundary, the canonical topology was active and `knowledge/brain/sqlite/social_dev_brain.sqlite` was byte-identical to the K2 source DB (`6c8883a6f0bf8426d8ace702bbedcd59e9b8b26aadd46dbf2965a2698b894be`). K3 subsequently advanced the active brain revision; original data remains under `knowledge/data/original/`, generated views under `knowledge/generated/`, accepted fixtures under `knowledge/fixtures/accepted/`, and read-only source identities under `knowledge/sources/` and `sources/raw/`.
- The legacy archive is verified and offline-safe: `legacy/MANIFEST.json` records `476` files, the reopened archive/member-hash verification is `pass`, and the active tree has no `knowledge/social-dev/` or `runtime/social-dev/evidence/` directory. The old G1.5 database remains recoverable and byte-identical under `legacy/old-g1-5/`.
- The generated runtime pack and browser mirror are byte-identical (`e7abff5ae6725530cb337a54f30706a76d51359721f594d9ca2dffab09cefb9f`). The accepted fixture manifest contains `682` promoted fixtures, including the C# inventory and first-visible/MapChip proof required by active gates.
- Verification passed: legacy-offline and old-namespace-offline runs; K2, G0/G1, R0 (`2215` checks), I0, I1, I2, living-core (`109`), behavior-first (`118`), data-dependency (`2432`), V1/V3/V7, first-visible recovery, full Vitest (`48` files / `314` tests, including MapChip), typecheck, production build, query/K3-gap smoke, and `git diff --check`.
- Pre-existing K2-preflight TODO/master-manifest drift, inherited R0 metadata/hash drift, and the inherited I2/R0 transitive failure remain separately recorded in `knowledge/brain/acceptance/k2-5-cleanup/baseline-regression.json`; they are not new semantic regressions.
- Rebuildable caches and `runtime/social-dev/dist/` were removed after verification; `16,017,652` bytes were reclaimed. `node_modules` was preserved. At the K2.5 boundary, K3, V8, integrations, deployment, persistence, backend AI, network, emulator/ADB, and subagent work had not started.

K2.5 baseline evidence: `knowledge/brain/acceptance/k2-5-cleanup/final-validation.json`, `reference-scan.json`, `legacy-offline-test.json`, `old-namespace-offline-test.json`, `runtime-mirror-validation.json`, `regression.json`, and `cleanup-bytes-report.json`.

## Current Status — I2 dashboard runtime, in-process API, and control surface complete (2026-08-16)

I2 completed inline with status `PASS_I2_DASHBOARD_RUNTIME_API_AND_CONTROL_SURFACE_CLOSED`.

- Production `runtime/social-dev/src/app/runtime.ts` now owns one persistent canonical `LivingRuntime`, one `DashboardRuntime`, one I1 `AssignmentAdapter`, and one wall-clock scheduler owner. Each scheduled step commits one living tick, observes it once, publishes one combined snapshot, and renders Canvas/DOM from the same committed frame. Product commands publish typed results without ticking living state.
- Added `runtime/social-dev/src/product/dashboard/` with the facade, defensive deterministic snapshot/read model, typed command/query/subscription API, explicit source-backed Staff bootstrap, Bridge C policy, and DOM/CSS task control surface. Product state remains ephemeral in memory; backend/auth/multi-user/queue/fairness/auto-reassign and persistence remain deferred.
- Added D1–D14 focused Vitest coverage, deterministic scenario runner, JSONL transition traces, the I2 evidence/contracts package, nine I2 reports, browser smoke evidence, and `tools/social-dev/test_i2_dashboard_runtime.py`. Browser smoke reused the pre-existing healthy Vite server on port 4173 and recorded no console errors or uncaught promise errors.
- Final verification: D1–D14 `14/14 PASS`; focused I2 Vitest `13/13`; full Vitest `48` files / `314` tests; typecheck; production build (existing nonblocking large-chunk warning); I1 `88` checks / 12 scenarios; I0 S1–S10; R0 `2177` checks; G0/G1; G1.5; behavior-first `118`; data-dependency `2432`; living-core `109`; browser smoke; and `git diff --check` all pass. D14 replay digest: `d6f5f83ffb05f073`.
- R0 contract artifacts and semantic renderer/living/scene roots remain frozen. The independent R0 validator recognizes only the explicit I2 app-shell migration recorded in `knowledge/fixtures/accepted/i2-dashboard-runtime/upstream-hash-lock.json`; no source identity or R0 semantic contract was rewritten.
- Changed I2-owned files include `runtime/social-dev/src/product/dashboard/`, `runtime/social-dev/src/app/runtime.ts`, `runtime/social-dev/src/styles.css`, the I2 Vitest/runner/test tooling, and I2 evidence/reports. Existing user-owned phase changes remain preserved. No V8, emulator/ADB, backend, network, or subagent work was started.

Next boundary: stop after I2. Do not start I3, backend/auth/multi-user/persistence, or additional gameplay/UI expansion without a separate user-directed phase.

## Current Status — I1 assignment adapter complete (2026-08-16)

I1 completed inline with status `PASS_I1_ASSIGNMENT_ADAPTER_NO_TASK_RUNNING_LIFECYCLE_CLOSED`.

- Forensic closure distinguishes `BASELINE_NO_PROJECT`, `PLANNING_ACTIVE`, `DEVELOP_ACTIVE`, and `POST_DEVELOP_BASELINE`. Native `Staff.Update` state 12 dispatch, `Staff.UpdateDevelop` RVA `0x12D3D48`, `developState_` offset `0x188`, the ten-way native target table, Develop HP interaction, clone-vector `developStaffId_`, interruption backup, and completion chain are recorded under `knowledge/fixtures/accepted/i1-assignment-adapter/`.
- The truthful bridge is `PRODUCT_TASK_OVERLAY_WITH_BASELINE_LIVING`. Original Develop is rejected as proposal/step/clone-specific and source-limited for arbitrary external tasks; original Planning is rejected as a player-wide preparatory phase without arbitrary task identity. No native living field is mutated by the product layer.
- Product implementation is under `runtime/social-dev/src/product/assignment/`: explicit AgentBinding/TaskRecord state, deterministic commands/events, conflict and terminal cleanup policy, read-only living interruption observation, side-by-side dashboard read model, and stable replay digest. External IDs and task progress remain outside `LivingStaff` and original save semantics.
- Evidence includes the I1.0–I1.FINAL checkpoint ledger, baseline/I0/R0 hash lock, source reverification, original work/develop contracts, Bridge C decision, product contracts, A1–A12 scenario results and JSONL traces, validation, and ten Runtime reports.
- Final verification: I1 offline acceptance `checks=88 scenarios=12`; full Vitest `47` files / `301` tests; typecheck; production build; G0/G1; G1.5; living-core (`109` checks); behavior-first (`118` checks); data-dependency (`2432` checks); R0 (`2177` checks); and `git diff --check` all pass. A12 replay digest: `22e5573f2b65d339`.
- Boundaries remain closed: no scheduler/fairness/auto-reassignment, backend/LLM/network/server, dashboard UI, save implementation, V8, MapChip, Renderer, emulator/ADB, or subagents. Backend interruption policy remains `PRODUCT_POLICY_PENDING_AFTER_I1`.

Next boundary: stop after I1; do not begin dashboard/API/backend integration without a separate user-directed phase.

## Current Status — I0 original living core runtime complete (2026-08-16)

I0 completed inline with status `PASS_I0_ORIGINAL_LIVING_CORE_RUNTIME_IMPLEMENTED_S1_S10_CLOSED`.

- The authoritative runtime is under `runtime/social-dev/src/core/living/`: canonical Staff/Room/ObjChip state, source-backed cardinal movement and arrival dispatch, raw-order desk ownership, deterministic AppData/Lib RNG replay, equipment/talk detours, HP/recovery/home, planning boundaries, and interruption cleanup.
- The generated runtime catalog contains `141/30/36/103` StaffData/JobData/SkillData/FurnitureData records, `18` RoomData grids, source-backed neutral HP fixtures, and the frozen S1–S10 fixtures. R0 contract files remain hash-locked and unchanged.
- The visual shell receives `SimulationState.living` only through `core/living/projection.ts`; MapChip, Renderer, V8, save compatibility, emulator/server proof, and dashboard/product policy remain outside I0.
- Evidence is under `knowledge/fixtures/accepted/i0-living-runtime/`, including the checkpoint ledger, native spotchecks, tick/RNG closure, scenario results, S1–S10 JSONL traces, replay proof, implementation manifest, and validation.
- Verification passed: the independent I0 acceptance token, phase-aware R0 validator (`2177` checks while retaining the immutable R0 package), runtime typecheck, full Vitest (`46` files / `296` tests), production build with the existing nonblocking large-chunk warning, data-dependency (`2432`) and behavior-first (`118`) regressions, and `git diff --check`.

Next boundary: no work beyond the unified floor00 runtime or V8 starts without a separate user-directed phase.

## Current Status — R0 canonical runtime contract freeze complete (2026-08-16)

R0 completed inline, static-only, and without runtime implementation with status `PASS_CANONICAL_RUNTIME_CONTRACT_FREEZE_READY_FOR_IMPLEMENTATION`. The existing runtime delta audit covers `134` current runtime/evidence entries: `KEEP 2`, `KEEP_VISUAL_ONLY 112`, `EXTEND 3`, `REPLACE 3`, `SUPERSEDED 3`, `PRODUCT_LAYER_ONLY 0`, `OUT_OF_SCOPE 11`, and `UNKNOWN_REVIEW_REQUIRED 0`; implementation blockers are `0`.

- Generated contracts: `knowledge/fixtures/accepted/runtime-contract-freeze/` contains `15` canonical contracts plus the manifest, validation, and checkpoint ledger. Reports are under `docs/Phases/Runtime/`; builders/tests are `tools/social-dev/build_runtime_contract_freeze.py` and `tools/social-dev/test_runtime_contract_freeze.py`.
- Authority: the pinned APK/native/metadata/dump identity remains exact; G1.5, living-core, behavior-first, and data-dependency evidence remain the source authority. Actor/Room/Furniture ownership, 4-neighbor movement, 14 states/12 move modes/11 arrival modes, tick order, RNG ranges, HP/recovery/home, planning, interruption/resume, visual/product, and save boundaries are frozen with provenance.
- Verification: the R0 builder passes; the independent validator passes `2183` checks; G0/G1, living-core (`109` checks), behavior-first (`118` checks), data-dependency (`2432` checks), runtime typecheck, and Vitest (`45/45` files, `284/284` tests) pass. No runtime source, V8, MapChip, or Renderer changes were made.
- Stop boundary: subagents, emulator/ADB, live app, local server, network, and I0 are all `NO`. The next phase, only when explicitly started, is `I0 Original Living Core Runtime Implementation`.

## Current Status — G1.5 canonical KB integrity and static blocker closure passed

G1.5 completed static-only with status `PASS_G1_5_CANONICAL_KB_INTEGRITY_AND_STATIC_BLOCKERS_CLOSED`. The pinned XLS TextAsset source, deterministic decoder, and registry row hashes pass; native `DataManager.Load`/`GetInstance` evidence closes all `43/43` slots; and the canonical SQLite/JSONL/graph outputs were regenerated.

- Core data counts: `StaffData 141`, `JobData 30`, `SkillData 36`, `FurnitureData 103`. The Q1–Q14 demonstrations and the C1–C14 G1.5 query gate pass; C13 reports `0` true static implementation blockers.
- Native `Staff.hp_` graph: `18` direct native accesses across `9` methods (`8` reads, `10` writes), with `Staff.UpdateWork` showing no direct `hp_` access and no negative `RecoverHp` call.
- Planning boundary: `6` actual extracted form call sites feed `Player.StartPlanning → Room.OnStartPlanning → Staff.OnStartPlanning`; update/end chains and the minimal original work-assignment input contract are source-backed.
- Generated outputs: `knowledge/fixtures/accepted/g1_5/`, `knowledge/data/original/`, including `jsonl/gaps_classified.jsonl`, `query_results_g1_5.jsonl`, and the seven G1.5 reports. `build_game_knowledge_g0_g1.py --check` and `test_game_knowledge_g0_g1.py` pass after regeneration.
- Remaining explicit limits: semantic reader-to-column mapping outside the verified core rows is source-limited but nonblocking; floor selector `5` remains visual-deferred; dashboard semantics remain product-policy pending; runtime/V8/MapChip/Renderer/save work remains out of scope. No server, emulator/ADB, network, or source-root mutation was used.

## Current Status — Social Dev Story v2.5.1 game-scoped static knowledge base G0/G1 complete with source limits

The fresh-run static G0/G1 builder completed with status `PARTIAL_GAME_SCOPED_STATIC_KNOWLEDGE_G0_G1_SOURCE_LIMITED`. Pinned APK/native/metadata/dump identity passed exactly; the raw C# Tier-A scope indexed all `89` direct files, and bounded Tier-B/C closure indexed `141` app-adjacent files.

- Canonical output: `knowledge/data/original/`, including SQLite, `20` required JSONL exports, `10` graph exports, `22` required reports, query results, and build manifest.
- Verified counts: `43` DataManager slots/tables, `3,693` rows (`281` verified reader-order / `3,412` source-limited raw rows), `3,542` assets, `3,192` selectors, `5,337` calls, `22,041` field accesses, `83` state edges, `11` native arrival-dispatch entries, and `4` UI command boundaries.
- Canonical reconciliation: `21,878` entities, `22,048` canonical facts, `22,052` raw claims, `2` superseded claims, and `1` unresolved conflict; the SQLite `(entity_id, predicate)` uniqueness constraint prevents duplicate canonical facts.
- Verification passed: `python tools/social-dev/build_game_knowledge_g0_g1.py --check`; `python tools/social-dev/test_game_knowledge_g0_g1.py`; all `Q1`–`Q14` query demonstrations; all generated provenance references resolve.
- Remaining explicit limits: indirect DataManager dispatch/row decoding, floor selector `5` conflict, dashboard product policy, and excluded Tier-D/external/runtime scope. No runtime, V8, MapChip, Renderer, save implementation, server, emulator/ADB, network, or source-root mutation was performed.

## Current Status — Data-dependency forensic phase DD.0–DD.20 complete; stop before runtime/visual/V8

DD.0–DD.20 completed inline, sequentially, and static-only with status `PASS_DATA_DEPENDENCY_FORENSIC_WITH_SOURCE_LIMITS`. The phase closed the pinned APK/ZIP/RAR/C# loader authority chain, retained the complete StaffData/JobData/SkillData/FurnitureData source rows and locales, recovered native job interpolation/max-level bonus/Staff skill lookup and Staff parameter/HP dependencies, and separated source, saved, transient, derived, and PRODUCT_POLICY fields.

- Machine evidence: `knowledge/fixtures/accepted/data-dependency/` with `21` JSON contracts, complete raw/provenance catalogues, explicit unknowns, canonical actor/furniture schemas, original 141-profile catalogue, and the DD.0–DD.20 ledger.
- Reports: `docs/Phases/Behavior/` with `10` data-dependency reports plus `1` handoff document.
- Verified counts: StaffData `141`, JobData `30`, SkillData `36`, FurnitureData `103`; every table row has English/Japanese raw retention, loader mapping, parse pass, row hash, and source/archive provenance. JobData six-element vector slot 5 is retained as the source slot consumed by `StaffData.PARAM_HP=5`; no named JobData HP constant was invented.
- Closed contracts: Staff→Job and Staff→Skill links, Staff parameter components, MaxHP/HP ratio/recovery chain, work/state data consumers, all SkillData raw effects with proven consumers, all FurnitureData type/recovery/passMap effects, actor/furniture dependency edges, saved/transient/derived Staff status, and dashboard PRODUCT_POLICY separation.
- Remaining unknowns: Room.GetEquipParam filter semantics, motivation bound meaning, ordinary work HP drain, sleeping cadence, exact desk vacancy/fairness, arrival dispatch, type-4 furniture direction, rest/social furniture roles, full meeting dispatch, caller-selected initial staff breadth, and dashboard task assignment policy.
- Verification: `python tools/social-dev/build_data_dependency_forensics.py --check` passed; `python tools/social-dev/test_data_dependency_forensics.py` passed `2432` static checks, `21` JSON files, `10` reports plus `1` handoff, and five static regressions; source-root diff, JSON parsing, and `git diff --check` passed.
- Constraints honored: no runtime implementation, visual correction, renderer/MapChip change, V8, subagents, emulator/ADB/live app, server, network, browser automation, or new screenshots. Do not begin implementation or visual work from this handoff.

## Current Status — Behavior-first Staff living-system forensic phase complete; stop before visual work

BF.0–BF.19 completed inline, sequentially, and static-only with status `PASS_BEHAVIOR_MODEL_WITH_SOURCE_LIMITS`. The phase re-read the prior closure/candidate artifacts, matched `103` Staff storage declarations (`97` mutable) to pinned IL2CPP offsets, reverified state/move/flag constants and native RVAs, closed the readable HP/recovery/home/equipment/workstation/movement/talk/idle/contention contracts, and classified all `103` FurnitureData records without inferring rest/social roles from names or sprites.

- Machine evidence: `knowledge/fixtures/accepted/behavior-first/` with `22` JSON contracts, the BF.0–BF.19 checkpoint ledger, explicit unknowns, and the dashboard preservation boundary.
- Reports: `docs/Phases/Behavior/` with the `11` required behavior-first reports.
- Verification: `python tools/social-dev/build_behavior_first_forensics.py --check`; `python tools/social-dev/test_behavior_first_forensics.py` passed `118` static checks, `22` JSON files, and `11` reports; read-only source-root diff gate passed.
- Regression gates: visual-port V1/V3/V7 evidence checks passed; full Vitest passed `45/45` files and `284/284` tests; typecheck, production build, and `git diff --check` passed. The build retained its existing non-blocking large-chunk warning.
- Remaining source limits: damaged indirect `Staff.Update`/`OnArriveGoal` dispatch, ordinary work HP drain, sleeping-stock cadence, exact desk-vacancy predicate, exact reservation count semantics, full meeting dispatch, GetSkill lookup, and exact FurnitureData rest/social roles.
- Constraints honored: V8 not started, no visual work, no production renderer or MapChip change, no subagents, no emulator/ADB/live app/server/network/browser work, no new screenshots, and no source-root edits. Do not begin visual correction or renderer cutover from this handoff.

## Current Status — First-visible transition recovery source-limited boundary

The recovery package is in `knowledge/fixtures/accepted/visual-port/first-visible-transition/` with reports under `docs/Phases/VisualPort/`. Static native analysis identifies `form.TitleForm.Update()` (`RVA 0x1207E44`) as the owning start-game caller; its direct call at `0x01208248` invokes `AppData.NewGame` (`0x1263A70`), then sets title state `3` (fade-out). Event 0 is recovered as `SCR_TALK(0,0)` followed by `SCR_DELAY(10)`, and the GameForm draw-entry predicate is recovered. The complete post-event automatic queue order and stable Staff pose remain source-limited, so no preview, full room reintegration, or V8 is allowed. Final verification passes: 53 Python/static gates, 334 JSON files, 119 Python AST files, focused Vitest 5/5 files and 124/124 tests, full Vitest 45/45 files and 284/284 tests, typecheck, build, and diff checks.

- Constraints remain active: inline/sequential/static-only; no subagents, emulator/ADB/live app, server, network/browser smoke, new screenshots, source-root edits, production cutover, or V8.

## Current Status — First-visible starter-state forensic gate stopped at FS.16; FIX_REQUIRED before V8

FS.0–FS.16 completed inline and static-only. The NewGame bootstrap is source-backed, including room 0 wall/door, Wooden Desk cells and native directions, initial Trash Can/Old Printer/Calendar, and Staff spawn coordinates. The first stable post-tutorial main-display boundary is not source-closed, so no first-visible final scene or corrective render is claimed. V8 has not started.

- Baseline: focused V5–V7/MapChip/reintegration `5/5` files / `124/124` tests; full Vitest `45/45` files / `284/284` tests; typecheck; production build with the existing non-blocking large-chunk warning; all `52` Python/static gates; `300` active evidence/runtime/data JSON files before this gate; and `git diff --check` pass.
- Evidence: `knowledge/fixtures/accepted/visual-port/first-visible-starter/`; reports: `docs/Phases/VisualPort/FIRST_VISIBLE_*.md`; plan: `docs/Phases/VisualPort/FIRST_VISIBLE_STARTER_STATE_PLAN.md`.
- Problem: FS-U01 through FS-U06 remain open for the start-game caller, tutorial/event mutations, first stable display predicate, first-visible workstation identity, equipment persistence, and Staff stable pose. Required staged/final PNGs were intentionally not generated.
- Constraints honored: no subagents, emulator/ADB/live app, server, network, browser smoke, or new screenshots; source roots remain read-only; MapChip, V6 Staff semantics, and production renderer unchanged.
- Next: recover the missing source/native transition, then rerun the first-visible manifest/render gate from FS.1. Do not start V8.

## Current Status — Starter-room layered reintegration gate passes; stop before V8

The user-directed inline/static reintegration gate passes RI.0–RI.11. The required plan is `docs/Phases/VisualPort/STARTER_ROOM_LAYERED_REINTEGRATION_PLAN.md`; the accepted MapChip forensic foundation remains frozen and Stage 1 adds no duplicate floor plane. The staged evidence package is `knowledge/fixtures/accepted/visual-port/starter-room-reintegration/`, with seven reports under `docs/Phases/VisualPort/`.

- Final structural stream: `139` commands / `124` traces; final Room+Staff stream: `142` commands / `127` traces. Structural pixel SHA-256 is `f139c65b2b4357b972fbdbca37308060091607d3907593e6893df77803e67288`; Room+Staff pixel SHA-256 is `c3d82b29a78b827e682b623c94789e34701bd4cfa0369a14ea81fcf2fe2a30b6`. Both final renders repeat identically.
- Verification passes: full Vitest `45/45` files and `284/284` tests, focused reintegration `28/28`, typecheck, production build, `52` Python/static gates, JSON validation (`305` files), Python compilation, and `git diff --check`.
- Constraints honored: inline-only, sequential, static/offline, no subagents, no emulator/ADB/live app/server/network/browser proof, no screenshot-derived numeric tuning, production renderer unchanged, MapChip foundation unchanged, Staff semantics unchanged.
- Target classification: `B_ROOM_0_AFTER_NEWGAME_BOOTSTRAP / C_STARTER_MAIN_DISPLAY_STATIC_ENVIRONMENT`; UI/tutorial overlays and gameplay simulation excluded. V8 remains not started.

## Current Status — MapChip forensic foundation passes; full room and V8 remain frozen

The user-directed static-only MapChip forensic gate supersedes and revokes the earlier starter-room correction PASS. The staged MC.0–MC.15 ledger is `PASS_MAPCHIP_FOUNDATION`: the direct MapChip selector/OPT/alpha/dimension/anchor/projection gates pass, and the complete 14x14 MapChip-only fixture renders 81 nonempty commands with one connected alpha component, zero unexpected transparent pixels, and a repeat-identical digest.

- The first staged failure was MC.6 `FAIL_ALPHA`: legacy V7 `REPLACE` arithmetic cleared 380 expected alpha pixels in each adjacent x/y pair. The isolated compatibility-raster correction in `runtime/social-dev/src/v7/raster.ts` preserves the destination under incoming alpha-zero `REPLACE` fragments; explicit arithmetic and the production renderer remain unchanged.
- Selector/data `85/floor_09.png` remains a metadata-only alias while the rendered floor candidate remains `floor_05.png`; no direct MapChip OPT or logical companion was invented.
- Evidence: `knowledge/fixtures/accepted/visual-port/mapchip-forensic/`; reports: `docs/Phases/VisualPort/MAPCHIP_*.md`; focused gate: `runtime/social-dev/tests/mapchip-forensic.test.ts`.
- Final verification: full Vitest `44/44` files / `256/256` tests, focused MapChip `18/18` tests, typecheck, production build, V1/V3/V7/OPT/native/Phase 3 static gates, 15 MapChip JSON files, `git diff --check`, and production-renderer diff audit all pass. The existing non-blocking Vite large-chunk warning remains.
- Constraints honored: inline-only, static/offline, no subagents, no emulator/ADB/live app/server/network/browser proof, historical screenshots used only as secondary context, and V8 not started.
- Current boundary: full-room integration is not authorized by this gate and remains frozen pending a separate user-directed phase.

## Superseded Status — Starter-room semantic correction is complete; freeze before V8

The static-only starter-room correction pass is `PASS_STATIC_STARTER_ROOM_CORRECTION`. The first broken semantic layer was main-display pass assembly: the source-backed floor0 14x14 topology contained 196 cells, but the pre-correction stream emitted only the central floor subset. A second coordinate-bridge defect kept MapChip and ObjChip/Staff on one origin. The corrected stream commits all 81 non-empty MapChip cells before object composition and preserves the source-backed 360-pixel normalized object/actor delta (canvas bases 82 and 442).

- Corrected V5 room:0 stream: `139` commands / `124` traces / `788` events; command SHA-256 `0b8132b8ab45eda3d8bb344e65304e0c4d32717a9638c2789efd9223d9df5d60`; manifest SHA-256 `48a1827c94c15394d38e872b243c398d8c6e6f47b66099bf26b44f22ee79e047`.
- Corrected V6 room:0 + Staff stream: `142` commands / `127` traces / `791` events; manifest SHA-256 `1e2b1d47922f8e274bfdf40a5c1c9aff85780441ad244f92de641e5cc5de1e7a`.
- Corrected structural PNG: `knowledge/fixtures/accepted/visual-port/starter-room-correction/previews/starter_room_structural_corrected.png`, SHA-256 `b55d701ba74bd6212701a6623d5de667d824c00c604bfebfc2d416f7d5fd447a`.
- Corrected room + Staff PNG: `knowledge/fixtures/accepted/visual-port/starter-room-correction/previews/starter_room_with_staff_corrected.png`, SHA-256 `f5c2db1052ee55b6256208b164107bc123f58634f533ce621f46871acb60c1cd`.
- Machine evidence and SR.0–SR.14 ledger: `knowledge/fixtures/accepted/visual-port/starter-room-correction/`; reports: `docs/Phases/VisualPort/STARTER_ROOM_*.md`.
- Verification: full Vitest `43/43` files / `237/237` tests, typecheck, production build, V1/V3/V7 gates, native/Phase 3 static gates, JSON validation (`158` files), `git diff --check`, and production renderer diff audit pass. The existing non-blocking Vite large-chunk warning remains.
- Constraints honored: inline-only, sequential, static/offline, no subagents, no emulator/ADB/live app/server/network/live browser, no runtime screenshot proof, source roots read-only, production renderer unchanged.
- Stop condition: V8 has not started and remains intentionally frozen pending a separate user-directed phase.

## Current Status — Phase V7.5 visual acceptance is complete; stop before V8

V7.5 reaches `ACCEPT_FOR_V8` over the existing V1–V7 static contracts. The additive builder is `tools/social-dev/build_visual_acceptance_v7_5.ts`; it uses RoomV5, StaffV6, RasterCompatibilityV7, original numeric resource IDs, and deterministic presentation composition only. No production renderer or route was changed, and no V8 work started.

- Fourteen required PNGs and `V7_5_VISUAL_ACCEPTANCE_CONTACT_SHEET.png` are present under `knowledge/fixtures/accepted/visual-port/v7_5/previews/`. The room structural and room + Staff outputs preserve the V7 PNG hashes `574492baa161e195fabe16bb7848da2c392f5ad4102d8806a828e67648471b3d` and `3793515941d6dc6c10079cf20e1d0908f9c1b55619c9c0a97019908ebed9e6ff`.
- Staff direction selectors are wait `10/11/12/13`, move `1/2/3/4`, and typing `23/24/25/26` in right/left/up/down order. The direction/action sheets use StaffData `0`, frame `0`, exact V6 source selectors, and presentation-only nearest-neighbor scaling.
- All 14 individual images plus the contact sheet rerendered twice with byte-identical PNGs and `0` changed pixels. The machine record is `knowledge/fixtures/accepted/visual-port/v7_5/visual-acceptance.json`; the report is `docs/Phases/VisualPort/V7_5_VISUAL_ACCEPTANCE.md`.
- Visual inspection found no obvious crop, pivot, layer-order, alpha, clipping, transform, or unexpected-blur corruption. No visual semantics were tuned or changed; the contact sheet remains presentation-only and the individual PNGs/contracts remain authoritative.
- Verification: V7 Python gate, V7.5 artifact/hash verifier, full Vitest `43/43` files / `234/234` tests, runtime typecheck, production build, standalone V7.5 tool typecheck, and `git diff --check` pass. The existing non-blocking Vite large-chunk warning remains.
- Constraints honored: inline-only, sequential, static/offline, no subagents, no emulator/ADB/live app/network/server/live browser, no historical geometry authority, no source-root mutation, and no production cutover.
- Stop condition: V7.5 is complete with `ACCEPT_FOR_V8`; V8 has not started and still requires a separate user-directed phase.

## Completed Status — Phase V7 static raster compatibility is complete; stop before V8

V7 reaches `PASS_STATIC_STOP_BEFORE_V8` for the selected graphics/raster compatibility, golden fixture, room:0 structural, and room:0 + Staff static scope. The implementation is isolated under `runtime/social-dev/src/v7/`; the production renderer and route remain unchanged. Fourteen source-referenced golden fixtures, deterministic PNG previews, both room renders, and classified pixel diffs are present under `knowledge/fixtures/accepted/visual-port/v7/`; all required V7 reports are under `docs/Phases/VisualPort/`.

- V5 identity remains 74 commands / 59 traces / 788 events, command SHA-256 `51f69c307338fa7fe89a3d9785bc9e76e20a8863ce3f79bb74b2b8d4fc458fd6`, manifest SHA-256 `4418a7c8a81a705d46a6eefc2a72e635f5e6108d83e4067dc0d638942f39f788`.
- V6 identity remains 77 commands / 62 traces / 791 events, manifest SHA-256 `bfab918ef5ea04512da380b4d5134c4b02d1d7ca29fd9c6fb47d7b4e40944142`.
- Structural room PNG SHA-256: `574492baa161e195fabe16bb7848da2c392f5ad4102d8806a828e67648471b3d`; room:0 + Staff PNG SHA-256: `3793515941d6dc6c10079cf20e1d0908f9c1b55619c9c0a97019908ebed9e6ff`.
- Final verification: full Vitest `43/43` files / `234/234` tests, typecheck, production build, `52` Python gates including V7, `255` JSON files, Python compilation over `tools` and `social dev`, and `git diff --check` pass. The existing non-blocking Vite large-chunk warning remains.
- The stale Phase 3B floor-recovery gate was aligned with the already-completed legacy archive deletion policy; no deleted source was restored.
- Constraints honored: inline-only, static-only, no subagents, emulator/ADB/live app/network/server/live browser/runtime screenshot proof, source-root mutation, or production cutover. Native shader/framebuffer bytes and complete live Staff cadence remain explicitly nonblocking unknowns.
- Stop condition: V7.14 is complete. V8 has not started and must require a separate user-directed phase.

## Current Status — Phase V6 Staff visual integration is complete for the selected static scope

Phase V6 reaches `PASS_STATIC` from the green V1–V5 baseline. The implementation is additive and isolated under `runtime/social-dev/src/v6/`; it recovers the bounded StaffData identity, `resHuman_` numeric resource selection, human SEB frame composition, source-derived door placement, integer camera forwarding, and the existing native `avatar-primary` room seam. The native live Staff-to-Avatar relationship remains explicitly source-limited; no production renderer cutover was performed.

- V6.0 baseline gate: PASS_STATIC. Full Vitest, focused V1–V5 regressions, typecheck, production build, JSON/Python validation, source-boundary audit, and `git diff --check` are green.
- V6 implementation: `runtime/social-dev/src/v6/`; focused tests: `runtime/social-dev/tests/v6-staff.test.ts` with `23/23` tests passed.
- V6 evidence: `knowledge/fixtures/accepted/visual-port/v6/`; reports: `docs/Phases/VisualPort/V6_*.md`.
- Final verification: full Vitest `42/42` files / `210/210` tests, focused V1–V5 `16/16` files / `108/108` tests, TypeScript typecheck, production build, `127` JSON files, `121` Python files, `25` Python/static gates, V6 runtime source-boundary/trailing-whitespace checks, and `git diff --check` pass. The existing non-blocking Vite large-chunk warning remains.
- Room:0 + Staff static manifest: `77` commands, `62` traces, `791` events, stable SHA-256 `bfab918ef5ea04512da380b4d5134c4b02d1d7ca29fd9c6fb47d7b4e40944142`.
- V6 boundary: inline-only, static evidence only, no subagents, emulator/ADB/live-app/network/server proof, source-root mutation, gameplay AI, production cutover, or exact pixel claims. Exact framebuffer parity and exact native cadence remain deferred to V7.
- Stop condition: V6.14 is complete with `PASS_STATIC`; do not start V7 automatically.

## Completed Status — Phase V5 Room orchestration is complete for the selected static scope

Phase V5 reaches `PASS_STATIC`. The isolated RoomV5 layer recovers the original Room / RoomData constructor surface, all 18 RoomData topologies, native floor selection, the nine Room.Draw pass slots, selected room:0 furniture/structural/wall/door composition, integer camera forwarding, and a command-only static preview. The production renderer remains unchanged and no production cutover was performed.

- V5 implementation: `runtime/social-dev/src/v5/`; focused regression: `runtime/social-dev/tests/v5-room.test.ts` with `27/27` tests passed.
- V5 evidence: `knowledge/fixtures/accepted/visual-port/v5/`; reports: `docs/Phases/VisualPort/V5_*.md`.
- Final verification: full Vitest `41/41` files / `187/187` tests, TypeScript typecheck, production build, V1/V3/asset/scene/floor/render/closure Python gates, V5/all-runtime JSON validation (`61` files), Python compilation, source-boundary audit, and `git diff --check` pass. The existing non-blocking Vite large-chunk warning remains.
- Room:0 static manifest: `74` commands, `59` traces, `788` events, stable SHA-256 `4418a7c8a81a705d46a6eefc2a72e635f5e6108d83e4067dc0d638942f39f788`.
- Required boundary honored: inline-only, static evidence only, no subagents, emulator/ADB/live-app/network/server proof, source-root mutation, gameplay, Staff/Avatar production cutover, or production renderer change. Exact framebuffer pixels remain deferred.
- Stop condition: V5.15 completed and handed off to the user-directed V6 static investigation.

## Completed Status — Phase V4 visual port is complete for the selected static scope

Phase V4 is `PASS_STATIC_V4_STOP_BEFORE_V5`. The selected MapChip, ObjChip wall/door/object routes, FurnitureData visual bindings, minimum Camera translation, local ordering boundary, fixture matrix, command parity, and regression package are complete under the static-only boundary. Exact native framebuffer/shader/sample pixels remain `DEFERRED_TO_V7`; generic/catalogue/viewport/Room-wide unknowns are nonblocking and explicitly recorded for V5.

- V4 checkpoint ledger: `knowledge/fixtures/accepted/visual-port/v4/checkpoint-ledger.json`; progress and parity reports are under `docs/Phases/VisualPort/V4_*.md`.
- V4 evidence: `knowledge/fixtures/accepted/visual-port/v4/` contains the native maps, coordinate/draw contracts, binding/camera/ordering contracts, fixture manifest, command parity results, and eight-entry nonblocking unknowns ledger.
- V4 implementation is isolated to `runtime/social-dev/src/v4/`; focused tests are `runtime/social-dev/tests/v4-*.test.ts`. The production renderer does not import V4 and was not changed.
- Final verification: Vitest `40/40` files / `160/160` tests, focused V4 `4/4` files / `20/20` tests, TypeScript typecheck, production build, V1/V3 Python evidence gates, asset metadata gate (`13` checks, `3542` assets, `186` runtime query assets), closure gates, Python compilation, JSON validation (`13` V4 JSON files), source-boundary audit, and `git diff --check` pass. The existing non-blocking Vite large-chunk warning remains.
- Constraints honored: inline-only, no subagents, no ADB/emulator/live-app/network evidence, no local server, source roots read-only, no V5 start, and no production cutover.

## Completed Status — V3 original resource recovery is complete and V4-ready

The superseding V2 acceptance record is `PASS_STATIC` with `V2 ENTRY GATE FOR V3: PASS`. Exact native framebuffer/shader/sample pixels remain explicitly `DEFERRED_TO_V7`; this does not authorize runtime, emulator, ADB, network, or live-app evidence. The earlier V2 blocked/deferred raster-gate status is preserved as historical evidence rather than rewritten.

V3 is `PASS` under the static-only boundary. It covers original resource-group ownership, sparse `img[]`/`seb[]` indexing, `img.inf`/`seb.inf` binding, load relationships, same-group `Sprite.TexId` resolution, real multi-group fixtures, and an additive isolated compatibility layer. No scene/gameplay renderer cutover is permitted. Its handoff opened V4 to request proven resources by group and original numeric ID without filenames.

- V3 checkpoint ledger: `knowledge/fixtures/accepted/visual-port/v3/checkpoint-ledger.json` and `docs/Phases/VisualPort/V3_PROGRESS.md`.
- V3 verification: full Vitest `36/36` files / `140/140` tests, focused V3 `8/8` tests, TypeScript typecheck, production build, V1 Python evidence gate, V3 Python evidence gate, Python compilation, deterministic JSON hash audit, and `git diff --check` all pass. The existing non-blocking Vite large-chunk warning remains.
- V3 evidence includes all 11 declared AppData visual groups, ten source-backed packs, explicit `resInterface_`/event/async/CustomImages/atlas unknowns, source ZIP/INF hashes, sentinel/alias records, and selected Image/SEB fixtures. Positive TexIds remain group-local; sparse gaps remain null.
- Changed V3-owned paths: `runtime/social-dev/src/v3/`, `runtime/social-dev/tests/v3-resource-manager.test.ts`, `tools/social-dev/build_visual_port_v3.py`, `tools/social-dev/test_visual_port_v3.py`, `docs/Phases/VisualPort/V3_*.md`, and generated `knowledge/fixtures/accepted/visual-port/v3/` evidence.
- Changed V4-owned paths: `runtime/social-dev/src/v4/`, `runtime/social-dev/tests/v4-*.test.ts`, `docs/Phases/VisualPort/V4_*.md`, and generated `knowledge/fixtures/accepted/visual-port/v4/` evidence. The baseline-only metadata gate import allowlist was narrowed in the ignored `tools/social-dev/build_asset_metadata_completion_gate.py`; its generated gate hash and counts are unchanged.
- Constraints remain: inline-only, no subagents, no ADB/emulator/live-app/network evidence, no local server, source roots read-only, and V2 exact raster parity deferred to V7.

## Current Status — Phase V1 core visual recovery is complete for the selected scope (inline execution)

The V0 consistency gate passed and the additive V1 recovery work remains isolated to the `runtime/social-dev/src/v1/`, `runtime/social-dev/tests/v1-*`, and `knowledge/fixtures/accepted/visual-port/v1/` paths. Tasks 1–9 are implemented and verified: deterministic real SEB/OPT fixture contracts, the twelve-slot Sprite contract/native map, source-ordered SEB projection, format-proven geometry, explicit native-depth deferral, the contract-only Image/OPT boundary, source-index-backed ResourceManager group lookup, a 26-record native recovery ledger, scoped parity evidence, four V1 reports, and the final full verification matrix are complete. Existing renderer code and source roots remain unchanged; no commit or merge has been made.

- Current V1 checkpoint ledger: `.superpowers/sdd/2026-08-14-visual-format-recovery-v1/progress.md`.
- Current verification: repository-wide Vitest passes 32/32 files and 115/115 tests; typecheck, production build, Phase 0 extraction regression, V1 builder/evidence gate, Python compilation, diff check, and the final eight-artifact hash audit all pass. The build retains the existing non-blocking large-chunk warning.
- Constraints: preserve the user-owned `.gitignore`, `AGENTS.md`, `PROJECT_STATE.md`, and `TODO.md` edits; keep generated evidence under the documented ignored paths; do not start a server for this work.

## Historical Prior Status — Phase V2 Graphics recovery was statically recovered and raster parity was deferred

V2 was executed inline-only and sequentially with no subagents. The additive `runtime/social-dev/src/v2/` layer recovers the pinned native Graphics state, clip, DrawImage geometry, center-based flip branches, scale, color, render/blend, Seb composition, and ResourceManager wrapper boundaries. Static native audit also records optimized-image/atlas dispatch, hidden/synthetic SEB sentinel paths, custom-image lookup precedence, and anchor/depth wrapper flow in `graphics-static-recovery.json`. The production renderer, V1 contracts, source roots, and manifest-driven runtime were not replaced or cut over.

- V2 focused verification passes: 3 V2 test files / 17 tests; the full runtime passes 35/35 files and 132/132 tests, TypeScript typecheck, production build, all relevant Python evidence gates, V1 hash preservation, and `git diff --check`. The build retains the existing non-blocking large-chunk warning.
- Historical prior record: `V2 STATUS: BLOCKED/DEFERRED` at the raster gate. The superseding V2 static acceptance record now says `PASS_STATIC` and opens V3; the exact `_drawBitmap` shader/sample/compositor pixels remain intentionally null and deferred to V7. Runtime, emulator, ADB, network, and live-app proof remain out of scope.
- Selected available furniture and human fixtures compose through V1 `Seb`/`ResourceManager` records and validated source-slot dimensions. `TEXID_NONE`, `TEXID_HIDELINE`, and `TEXID_HIDERECT` are no-draw paths; synthetic primitive calls, depth-aware RenderSeb, anchors, custom-image injection, and the unavailable avatar-body source image remain deferred at the adapter boundary.
- V1 starting hashes are recorded in `knowledge/fixtures/accepted/visual-port/v2/native-raster-map.json`; V1 source/evidence content remains unchanged. No local server was started.
- Historical next-work wording is superseded by the V3 PASS handoff. Do not seek runtime/framebuffer proof; V4 is not started automatically.

## Repository Cleanup — Historical GameDev Archive Removed

The user-approved legacy archive `archive/pre-social-reset/` was permanently removed on 2026-08-14. It contained 8,195 files across 802 directories (approximately 10.9 GB). The active project now contains Social Dev evidence, runtime, tools, and the separate inactive `archive/future-ai/` directory only. The removed corpus is not a valid source for future work and must not be recreated.

## Current Status — Asset metadata and native floor00 composition closure are complete; one live prop is explicitly excluded

The runtime now has a runtime-approved native content catalog, a native lifecycle/assembly contract, all-room selector assets, an evidence-backed resolver, explicit native direction mapping, generic native wall/door composition for all 18 rooms, and nine ordered render passes. It separates the 14x14 MapChip topology from the 10x10 ObjChip occupancy grid and never infers MapChip or FurnitureData identity from ObjChip. Browser smoke covers room:0 through room:17 with ready assets, zero unresolved entries, zero console errors/warnings, and native wall/door draw traces. The historical visual baseline is intentionally preserved by an explicit comparison policy; it is not silently replaced.

## Latest Verified Update — Phase V0 original visual subsystem audit

The original Unity/IL2CPP visual subsystem was audited before any port implementation. The audit covers `Sprite`, `Seb`, `Image`, `ImageAtlas`, `ImageAtlasManager`, `ResourceManager`, `Graphics`, `MapChip`, `ObjChip`, `FurnitureData`, `RoomData`, `Room`, `StaffData`, `Staff`, `Camera`, `GameForm`, `AppData`, `Main`, and the discovered Avatar/world/lifecycle dependencies. It records the exact six-way class/method dispositions, native RVA bridge, resource-group topology, character/furniture/room call and data flows, decompiler gaps, gameplay cut boundary, current-runtime comparison, and staged V0–V9 port plan.

- Audit prose is under `docs/Phases/VisualPort/`; machine-readable evidence is under `knowledge/fixtures/accepted/visual-port/`. The requested root `Phases/` path was absent, so this follows the repository rule that reports live under `docs/` and generated evidence under `knowledge/fixtures/accepted/`.
- The audit is evidence-only: `sources/raw/` and existing evidence remain read-only, `runtime/social-dev/` has no diff, and no Phase V1 implementation was started. Native RVAs are pinned to APK SHA-256 `fa0e9e3a843732258fc05b2611a8e0f5be6f7e95f2141a53f31fb082322fe2bf`.
- Verification: all seven visual-port JSON files parse; disposition/graph/call/data-flow consistency passes; `python -B tools/social-dev/test_csharp_system_extraction.py` passes (`82` types / `3430` fields / `1685` methods); runtime typecheck passes; Vitest passes `25/25` files / `79/79` tests; production build passes; `git diff --check` passes.
- V1 is gated until the V0 consistency check is rerun from the final artifact paths and the unresolved `Graphics.cs`, `Sprite`/`Seb`/`Image` bodies, general `Room.Draw`/`ObjChip.Draw`, and character animation gaps are closed by native/fixture evidence.

## Latest Verified Update — Unified main floor00 runtime cutover

The production runtime is consolidated into one main route. The root URL now resolves through a fixed `floor00` / `main_display` / `nativeFloor=0` policy, while the in-page RoomData selector retains access to all 18 room records and the complete current catalog data. The legacy `display-slice-01` projection branch, production scene/context query routing, legacy render-object list, and comparison-mode UI wording have been removed from active runtime code. Historical evidence, contracts, catalog identifiers, and asset-package paths remain intact for provenance and verification.

- Verification: full Vitest `25/25` files / `79/79` tests, TypeScript typecheck, production build, pre-runtime closure (`21` items, `13` verified, `0` deferred, `2` quarantined), and `git diff --check` pass.
- Browser smoke at `http://127.0.0.1:4173/?auto=0` reports `room:0 · floor00`, `18` selectable rooms, visual gate `pass`, `6/6` approved furniture asset draws, zero browser warnings/errors, and byte-identical fixed-frame screenshots with SHA-256 `02283c7d6dd4d5d98e2bc927b71d760b8c1135c4c9ccf5a366486f3d9266881d`. The existing healthy Vite server on port `4173` was reused.
- Git cleanup: `main` is now the only local branch; the two pre-reset corpus branches were deleted. The detached legacy worktree remains untouched because it contains untracked corpus artifacts.
- The unresolved red/black prop remains excluded and the raw floor `5` → selector/data `85/floor_09.png` → rendered `floor_05.png` alias remains unchanged.

## Latest Verified Update — Approved floor00 visual layout alignment

The user-approved floor00 presentation policy is now implemented as `knowledge/fixtures/accepted/runtime/floor00_visual_layout_contract.json`. It is scoped only to `room:0` with `scene_mode=floor00`, preserves the native evidence contracts, removes the eight marked glass trigger cells, renders the approved 9-cell glass scope with a continuous `[4,7]`–`[4,11]` side strip, extends the upper wood wall to `[9,1]`, shifts the side wall by exactly `[1,0]`, and moves the foreground wall split to `[9,7]`/`[9,8]` with layer order `0 → 1` retained.

- The legacy `display-slice-01` projection and non-floor00 room paths remain unmodified by the presentation override.
- The dedicated visual gate passes layout identity, glass removal/continuity, wall alignment, foreground occlusion order, final-pixel visibility, and asset lifecycle checks. Browser console errors and warnings are empty.
- Two fixed-frame browser captures are byte-identical with SHA-256 `02283c7d6dd4d5d98e2bc927b71d760b8c1135c4c9ccf5a366486f3d9266881d`. The gate record is stored at `knowledge/fixtures/accepted/floor00_visual_layout_browser_gate_20260814.json`.
- Verification: Vitest `24/24` files / `75/75` tests, TypeScript typecheck, production build, and browser gate pass. The existing healthy Vite server on port `4173` was reused.

## Current Boundary — One gameplay prop still lacks a closed binding

The floor00 operation-level audit is now closed for the verified bootstrap subset. The remaining red/black room prop seen in the live save capture does not have a closed FurnitureData/selector binding, so it is deliberately excluded from the NewGame bootstrap by user decision. It must not be guessed or added later without a proven live-state trace. The raw RoomData, MapChip, ObjChip, and SEB evidence remains authoritative.

## Latest Verified Update — Native computer is static

The reported computer flicker was traced to the default `display-slice-01` route passing the simulation frame into native `furniture:3`. Its `desk_00.seb` records change both the source crop and destination offset at frames `1/2`, which made the computer appear to flip or move even though the real room prop is static. `furnitureFrameForScene` now pins only native `furniture:3` (desk/computer plus its `chair_00` subcomposition) to frame `0` in every scene mode; actor animation and other furniture frame behavior remain unchanged.

- Regression: `runtime/social-dev/tests/display-assets.test.ts` now requires `furniture:3` frame/subframe `0` and source crops `desk=0`, `chair=60` for both `floor00` and `display-slice-01`.
- Verification: Vitest `23/23` files / `65/65` tests, typecheck, production build, and `git diff --check` pass. Browser `floor00` screenshots remain byte-identical across 350 ms (`f417028e969ff2b57a67957a9b1c22f734391caf4d44e012bfb7496e0fa08198`) with visual gate pass and no console errors/warnings.

## Historical Runtime Evidence — Excluded from Current Static V2 Proof

The following earlier-session runtime observation is retained only as historical provenance. It is not used as evidence for the current V2 task, and no additional ADB, emulator, APK, live-app, network, or runtime work is permitted under the current static-only boundary.

ADB is connected to `emulator-5554`; the foreground activity is `net.kairosoft.android.snsdev_en/main.Main`. Captures are stored under `knowledge/fixtures/accepted/adb-gameplay-20260814/`: one baseline PNG, eight consecutive burst frames, and contact sheets focused on the room objects. The real gameplay burst shows the red direct-image equipment crop is byte-identical across all eight frames, while staff sprites and speech/work indicators change. The desk/monitor/chair composition remains spatially stable in the observed burst. This confirms that the current web-side computer flicker is not native furniture animation evidence; it must be traced as an incorrect frame, crop, duplicate draw, or render-route issue. No runtime source was changed during the ADB observation.

The longer camera sweep confirms two visible `big_base00`-family facility pads, three desk/computer/chair compositions, three promoted direct props, one door gap, and the 15-cell wooden wall structure. The two facility pads correspond to the two raw `type 4` anchors and are now rendered as separate static structural compositions with explicit MapChip visual anchors `[4,5]` and `[7,5]`. The sweep also shows one additional red/black room prop that does not match the three promoted direct PNGs, so its live FurnitureData/save-state binding remains unresolved and must not be guessed.

## Latest Verified Update — Layered wall SEB fidelity and deterministic verification

The floor00 wall renderer now follows the native `ObjChip.DrawWall → AppData.DrawSeb(frame, lineNo=-1)` semantics. The strict closure and native scene assembly contracts retain every selected `wall_00.seb` layer: 15 room wall cells × 2 layers = 30 wall sprite draws, including the 2px thin layer with its verified source crop and `destination_y=-34`. The older `sprite_records` field remains a layer-0 compatibility view; the runtime prefers `sprite_layers` and preserves layer order `0 → 1`.

- The floor00 route is asset-ready gated: it does not paint a fallback room while approved PNG/SEB assets are unavailable. Structural pads, native furniture, native wall frames, and the fixed actor display cells are deterministic; two consecutive browser screenshots share SHA-256 `f417028e969ff2b57a67957a9b1c22f734391caf4d44e012bfb7496e0fa08198`.
- Final browser smoke at `?scene=floor00&auto=0` reports visual gate `pass`, `2` structural facility draws, `6/6` furniture asset draws, `3` actor asset draws, `30` wall layer draws, final visibility `pass`, and `occluded_ids=[]`; browser warnings/errors are empty. The screenshot is stored at `knowledge/fixtures/accepted/adb-gameplay-20260814/floor00-web-final-20260814.jpg`.
- The generated evidence chain was rebuilt after the floor00 structural-facility and static-frame changes: 23 Vitest files / 65 tests pass, `npm run typecheck`, `npm run build`, `python tools/social-dev/test_pre_runtime_closure.py`, and `git diff --check` pass. `test_pre_runtime_closure.py` validates without rewriting timestamped contracts, so the baseline input hash remains reproducible.
- The native source boundary remains explicit: the room floor selector `5` is unresolved in the source table, so the approved runtime policy renders `floor_05.png` while retaining selector/data metadata `85/floor_09.png`. This is a fixed, documented alias—not inferred from the screenshot.

## Completed Work — Native `floor00` bootstrap scene

The native `floor00`/`room:0` NewGame bootstrap is implemented and gated as an explicit comparison route. The runtime uses `196` MapChip cells, `100` ObjChip cells, `6` initial FurnitureData instances (`3× furniture:3`, `furniture:12`, `furniture:26`, `furniture:56`), and exactly `3` initial actors (`StaffData 0–2`) entering through door cell `(8,4)` at the closed AddStaff position. The literal `floor_00.png` is not substituted; `room:0` keeps its approved `floorImgId_=5` / `floor_05.png` render policy. The historical `display-slice-01` route and screenshots remain unchanged.

- The runtime contract is `knowledge/fixtures/accepted/runtime/floor00_scene_contract.json`; the loader cross-checks its bootstrap, topology, raw ObjChip histogram, native furniture matrix, door null-FurnitureData binding, and three-actor spawn fixture against the existing catalogs.
- `?scene=floor00&auto=0` projects the native 14×14 MapChip, separate 10×10 ObjChip occupancy, native wall/door, two raw type-4 structural facilities, six exact FurnitureData instances, and three static actors reserved at verified raw type-0 cells `[4,6]`, `[5,6]`, and `[7,6]`. It omits selector-only `furniture:2`/`furniture:5`, the unresolved live red/black prop, and the door surrogate from this mode. The native co-located `[8,4]` spawn remains preserved in the evidence contract.
- Visible diagnostics expose the scene mode, `196/100/6/3` counts, FurnitureData IDs/cells, door cell with `FurnitureData=null`, static display cells, floor alias policy, native furniture draw count, nine-pass render trace, and visual-gate status. The floor00 route does not advance the living simulation; the legacy route keeps the approved behavior trace unchanged.
- Verification passes: `npm run typecheck`, Vitest `23/23` files and `65/65` tests, `npm run build`, `python tools/social-dev/test_pre_runtime_closure.py`, browser static `floor00` frame-0 visual gate, deterministic screenshot comparison, zero browser console errors/warnings, and `git diff --check`. The existing local Vite server on port `4173` was reused and was not started or stopped by this task.

## Completed Work — Native floor00 compositing, collision, and visibility closure

The floor00 comparison route now closes the native visual composition instead of relying on draw-attempt counts. The renderer commits the MapChip/floor underlay before room content, draws the pale `wall_01.png` extension boundary above the underlay, composes rear `ObjChip.DrawWall`/door pixels before the two static structural facility pads and six native FurnitureData instances, keeps the three static display actors on verified empty walkable cells, and draws the lower foreground wall cells `[8,7]` and `[8,8]` after actors. The nine native pass identifiers remain visible in the trace while their logical per-cell order is enforced by the floor00 render-composition contract.

- `floor00_scene_contract.json` now records the approved logical order, native row traversal (`y` ascending then `x` descending), rear/foreground wall split, boundary-wall collision policy, both raw type-4 facility footprints, their explicit MapChip visual anchors, and the source basis. The loader and floor00 tests reject drift in these values.
- Native collision classification is explicit: raw type `0` is empty walkable, type `5` is the traversable entry door, unbound placement/desk slots remain reservable, installed furniture/footprints are blocked, and boundary walls are non-passable. No raw ObjChip value is promoted to FurnitureData identity.
- `?scene=floor00&auto=0` passes the fixed-camera final-pixel gate: both structural facility IDs, six furniture IDs, three actor IDs, the tree, all extension-wall sprites, all room wall frames, and the door retain final canvas pixels; `occluded_ids=[]`. Browser diagnostics show `2` structural facility draws, `6/6` furniture asset draws, `0` fallbacks, `3` approved actor asset draws, and `Visual gate pass`.
- Verification after this closure: `npm run typecheck`, full Vitest `23/23` files and `65/65` tests, `npm run build`, `python tools/social-dev/test_pre_runtime_closure.py`, `git diff --check`, and browser reload/capture with zero reported final-visibility occlusions. The existing Vite server on port `4173` was reused and was not started or stopped by this task.

- The native Room.floor_ connection is now closed in `knowledge/fixtures/accepted/native_room_floor_usage_catalog.json` and `knowledge/fixtures/accepted/runtime/native_room_floor_usage_contract.json`. Native evidence proves the boolean selector `floor == 0 → MAPCHIP_ARRAY[0]` / `floor != 0 → MAPCHIP_ARRAY[1]`, with `floor_0` materialized as `14×14` (`196` cells) and `floor_nonzero` as `4×4` (`16` cells); the old `1×16` presentation shape was corrected to the native row shape.
- The constructor usage catalog records `8` direct `new Room(...)` call sites across the main display, persistent player-room, and addition-floor preview paths, and connects all `18` RoomData keys without treating RoomData as the source of Room.floor_. The runtime resolver and projection accept explicit `nativeFloorValue`/context options; the browser query paths are `?nativeFloor=0&context=persistent_room` and `?nativeFloor=1&context=addition_floor_preview`.
- Native policy boundaries are explicit: floor values `2–5` select the same nonzero row because native selection is boolean; nonzero `14×14` requests are rejected; the existing 14×14 extension-wall predicates are never applied to a 4×4 topology. The approved floor alias remains unchanged: source selector/data `85/floor_09.png`, rendered pixels `floor_05.png`.
- The final native environment policy is explicit: only `main_display` receives the native `14×14` outer MapChip scope; `persistent_room` and `addition_floor_preview` remain `4×4` room topology only. No synthetic garden, road, or outer map is promoted when the native constructor does not provide one.
- The topology closure gates pass: the deterministic Python package test, all `18` Vitest files / `48` tests, TypeScript typecheck, production Vite build, and browser smoke for both the original `room:0` display and the native nonzero preview (zero console errors/warnings; visual gate pass).

- Item 6 is implemented for Room R (`room:17`): the raw fixture preserves all `100` ObjChip cells, raw type/direction values, the door at `(8,3)`, and `0` native FurnitureData bindings. The runtime exposes it through `room_r_scene_contract.json` and a diagnostic-only raw overlay; native wall/door composition is supplied separately by the closed all-room assembly contract.
- Item 7 is superseded by the completed `phase3d_all_room_assembly_gate`: room:0 frame `0/1/2` retains the existing frame/asset/furniture evidence, Room R cross-checks `100/100` overlay cells, and all 18 rooms pass the same native composition, asset, metadata, and trace gates.
- The gate also exposed and fixed a real direct-image fallback bug: native furniture frames with `source_status=pass_native_img_asset` but no `runtime_status` are now accepted as approved runtime images. The renderer diagnostics and content-addressed screenshots record the corrected result.

- The Pre-runtime Closure Sweep is complete for the historical Phase 0 through Phase 1C review boundary. Its active authority is `knowledge/fixtures/accepted/runtime/pre_runtime_closure_contract.json` with status `pass` / `closed_before_runtime`.
- AM-0 of the asset-metadata completion roadmap is complete. The deterministic baseline is `knowledge/fixtures/accepted/asset_metadata_baseline.json`, its non-runtime contract is `knowledge/fixtures/accepted/runtime/asset_metadata_baseline_contract.json`, and the report is `docs/reports/social-dev_asset_metadata_baseline.md`. It freezes the 3,542-row asset index, 3,542 native assets, 3,192 selectors, 3,693 data rows, source hashes, current contract counts, verification commands, and six explicit exceptions. The baseline builder/test pass and all ten pre-existing native/character/room/display gates pass.
- AM-1 is complete as a coverage audit. `knowledge/fixtures/accepted/asset_metadata_coverage.json` contains all 3,542 indexed assets, 3,192 selectors, 1,063 catalog fields, 523 data-selector relations, 250 consumer edges, 43 lifecycle edges, and 197 runtime manifest asset entries. `asset_metadata_orphan_report.json` separates 3,231 currently unreferenced catalog rows, 1 unresolved selector (`lineup_layout/bg.seb`), 88 explicit `-1` sentinels, 11 helper selector-scope gaps, and 1,055 fields needing semantic classification; no indexed/native or runtime manifest identity mismatch remains.
- AM-2 is complete. `asset_family_taxonomy.json` assigns all 3,542 rows to 27 stable structural families and 78 extension-based subfamilies with explicit lineage and runtime policy; no asset remains unclassified.
- AM-3 is complete. `asset_selector_usage_matrix.json` closes 3,192 selector records and `data_field_semantics_matrix.json` classifies all 1,063 catalog fields, including the eight selector-bearing fields, sentinel policy, consumer methods, lifecycle status, and nine deferred selector-scope fields.
- AM-4 is complete. `asset_composition_catalog.json` contains 47 composition entries and `asset_geometry_catalog.json` contains 3,546 geometry rows; all 186 runtime-relevant rows have zero runtime geometry gaps, while source-limited/catalog-only geometry remains explicitly labeled.
- Track W is complete. `furniture_asset_metadata.json` records all 103 FurnitureData rows, selector status, composition/geometry references, 18 rooms, six native instances, and four native-bound FurnitureData IDs without inferring identity from ObjChip values.
- Track H is complete for its declared boundaries. `character_visual_asset_metadata.json` records 141 StaffData, 19 HelperData, 105 unique human images, 35 human animations, 284 avatar-body rows, 509 avatar-head rows, and 72 event-visual rows; helper pixel gaps and avatar/event runtime promotion boundaries remain explicit.
- AM-5 is complete. `asset_usage_lifecycle_placement_matrix.json` connects all 3,542 rows to 3,495 usage edges, 43 lifecycle edges, 27 families, 21 non-actor-family boundaries, placement status, and runtime query status. It preserves the 34 Unity TextAsset/APK provenance gap instead of guessing a nested mapping.
- Track X/A is complete for current evidence. `asset_surface_provenance.json` records UI/event/text/config/data/platform family boundaries, ZIP/APK identity status, 25 exact pack round-trips, the 34 Unity TextAsset gap, and the one unresolved `lineup_layout/bg.seb` selector. No screen/event consumer contract is invented.
- Runtime metadata lookup is integrated through `knowledge/fixtures/accepted/runtime/asset_metadata_runtime_manifest.json` and `runtime/social-dev/src/catalog/asset-metadata.ts`: 186 explicit runtime rows are lazy-queryable by asset ID, selector key, family, or FurnitureData ID while the native 3,542-asset/3,192-selector catalog remains available for evidence lookup.
- The final audit is `knowledge/fixtures/accepted/asset_metadata_completion_gate.json`, `knowledge/fixtures/accepted/runtime/asset_metadata_completion_contract.json`, and `docs/reports/social-dev_asset_metadata_completion.md`. It passes 13 completion checks and distinguishes complete catalog metadata from the 186-row runtime promotion surface.
- Final verification passes: all 21 targeted Python metadata/native gates, `npm run typecheck`, Vitest `18/18` files and `48/48` tests, `npm run build`, and `git diff --check`. Runtime source-import scanning reports no archive/APK/C#/knowledge-root imports in `runtime/social-dev/src`; remaining knowledge-root imports are test-only historical evidence fixtures.
- A native-faithful content registry and connection graph were added before any renderer changes. The registry covers `43` DataManager arrays, `43` staged data types, `3,693` raw data rows, `3,542` indexed source/derived assets, `3,192` `img.inf`/`seb.inf` selector records, `523` data-to-selector edges, `250` C# consumer edges, and `43` lifecycle edges; deterministic validation passes.
- The full character metadata catalog is now implemented at `knowledge/fixtures/accepted/runtime/character_metadata_contract.json`: `141` StaffData records, `19` separate HelperData records, `30` JobData records, and `36` SkillData records. All StaffData image selectors resolve to `105` unique human assets; runtime metadata is compact while field-level provenance remains in the evidence fixture. Mutable actor state remains owned by `ActorState` and is created lazily.
- The shared character capability layer is now implemented at `knowledge/fixtures/accepted/runtime/character_capability_contract.json`: four explicit family profiles, one shared `human-staff-v1` profile bound to all `141` StaffData records (including special/assistant templates), a separate `helper-record-v1`, and reserved avatar/event-only boundaries. The runtime `character-resolver.ts` resolves every staff/helper template lazily, including `16` filename-derived native action groups covering all `35` human SEB selectors. Native human `wait`, `move`, and `typing` are closed in four directions, talk/work/equipment fallbacks and deferred actions remain explicit, and unsupported native directions return a visible no-selector status.
- The full human character asset package is now closed separately from the bounded world/display manifest at `knowledge/fixtures/accepted/runtime/character_asset_manifest.json`: `105` PNGs and `35` SEBs are promoted byte-for-byte, decoded into `48` layers / `334` records with `30` explicit no-texture control records, and bound to all `141` StaffData image selectors. `runtime/social-dev/src/assets/character-assets.ts` provides lazy image loading and frame selection; Canvas and the visual gate use the generic path for any approved character outside the five-actor display slice. The browser imports generated contracts and promoted assets only; it does not parse source binaries or recovered C#.
- The registry preserves native DataManager IDs, resource selector IDs, archive-relative asset identities, raw rows/selector lines, locale fallback resolution, `-1` sentinels, and derived-asset provenance. `knowledge/fixtures/accepted/runtime/native_content_catalog.json` promotes that identity graph to the runtime boundary with `3,693` records, `3,542` assets, `3,192` selectors, and all consumer/lifecycle edges; decoded fields retain their source status and are not renamed by inference.
- The runtime ID bridge is callable through `runtime/social-dev/src/catalog/native-content.ts`: data records, selector keys, asset IDs, and all bidirectional connection edges resolve from `RuntimeCatalogs` without reopening source roots or guessing an identity.
- A complete RoomData catalog now covers `room:0` through `room:17` with `1,800` decoded 10x10 ObjChip cells, native `objMap`/`objDir`, raw type counts, door cells, floor/wall/door references, and source row hashes. All `18/18` `floorImgId_` values resolve through the native `Room.FLOOR_IMAGE_ID_ARRAY` (`11` entries), and every room links the shared MapChip contract without inferring topology from ObjChip.
- The native connection graph records `RoomData.floorImgId_` as `Room.FLOOR_IMAGE_ID_ARRAY[index] → chip/img selector`, including `room:0` index `5 → selector 23 → floor_05.png` and `room:17` index `9 → selector 85 → floor_09.png`. The runtime resolver consumes the full catalog, preserves raw ObjChip direction values, and exposes the native vector/reverse mapping verified from `libil2cpp.so`: `0→(0,1)`, `1→(0,-1)`, `2→(1,0)`, `3→(-1,0)` with reverse table `[1,0,3,2]`.
- The closure matrix covers `21/21` historical review items: `13 verified`, `6 derived`, and `2 quarantine`; `open_items=0`, `pending_review_items=0`, and `blocking_items_remaining=0`.
- Canonical pre-runtime contracts are `knowledge/fixtures/accepted/load_contract_closure.json`, `knowledge/fixtures/accepted/semantic_review_closure.json`, `knowledge/fixtures/accepted/phase1_supersession.json`, `knowledge/fixtures/accepted/runtime/data_contract.json`, `knowledge/fixtures/accepted/runtime/entity_contract.json`, and `knowledge/fixtures/accepted/runtime/save_contract.json`.
- Original candidate evidence retains its historical `pending_review`/`unknown` labels for provenance; the closure matrix is the current lifecycle authority and prevents those historical candidates from being treated as active blockers.
- The repeatable closure gate is `python tools/social-dev/test_pre_runtime_closure.py`; it passed with `21` closed items and no blocking items remaining.
- The semantic diff disposition covers all `72` declared files (`44` data, `23` game, `2` route-search, `3` lifecycle): `12` exact and `60` marker-only after normalization. Decompiler bodies remain quarantined and are not copied into runtime.
- The first Vite/TypeScript display runtime is implemented under `runtime/social-dev/`: contract loader, deterministic fixed-tick core, route/event trace, room projection, Canvas renderer, DOM/CSS diagnostics, and browser fixture controls.
- The deterministic behavior trace remains valid at frame `136` (`idle → move → arrive → work_or_equipment → talk`, talk markers at `20/70/110`, `talk_end` at `130`, digest `1fe49b91bd27c5fa`). The original screenshot baseline and behavior trace remain `knowledge/fixtures/accepted/display_slice_01_screenshot_baseline.png` and `knowledge/fixtures/accepted/display_slice_01_behavior_trace.json`; the previous strict screenshot is retained only as superseded provenance.
- Phase 3C strict closure is materialized in `knowledge/fixtures/accepted/phase3c_strict_closure.json`, `knowledge/fixtures/accepted/runtime/phase3c_strict_closure_contract.json`, and `knowledge/fixtures/accepted/phase3c_strict_closure_validation.json`; the strict builder/test passes `10/10` checks. Package hash is `7a7073f27e72ed87509080ac7f2526736a476101794a2ce012aaddb872a3dbd5`; runtime strict-contract hash is `451634318765b2f99c456435ec2a83d21f4b0fec2e18904f62b6d288370677e1`. The package records the native `ObjChip.DrawWall` RVA `0x12C0698`, wall/door predicates, exact room cells, source sprite rectangles, `Room.PlaceDoor` null-FurnitureData binding, and the native initial FurnitureData bindings.
- The native wall/door and initial-furniture evidence is present in contracts and assets, and the Canvas now realizes the two-grid topology: `Room(14,14,0,roomData_[0])` supplies the MapChip floor while `RoomData.objMap_` remains the 10x10 ObjChip occupancy grid. The default visual uses the source-backed exterior chips, the boundary wall/door bindings, and native actor spawn coordinates. Selector-only `furniture:2`/`furniture:5` remain separate from the native room:0 bootstrap; no identity is inferred for those two.
- The default visual floor composition is explicit rather than strict provenance: raw selector `5` remains source-unresolved, selector/data identity is borrowed from `85/floor_09.png`, and the rendered pixels use the complete source-backed `floor_05.png` asset. The runtime loader cross-checks the borrowed selector/data record against `room_placement_contract.json`, pins the floor05 render hash, and keeps the composition clearly marked as borrowed rather than recovered native selector identity; there is one fixed policy, not a selectable fallback or hybrid mode.
- The display asset gate is now `knowledge/fixtures/accepted/display_asset_gate.json`: status `pass` / `approved_for_runtime_subset`, with `18` approved entries, `0` blocked entries, and `34` promoted runtime binaries. Four OPT-derived logical PNGs are materialized under the runtime boundary, and every manifest frame rectangle is checked against the physical runtime PNG actually loaded by the browser.
- The supplied Gemini explanation was reconciled against native source: selector flags are correct, but `TryPlace` is not the bootstrap; the verified chain is `AppData.NewGame → Room(14,14,0,roomData_[0]) → PlaceDesk → FLAG_INIT_PLACE scan`, with raw door type `5` handled separately. No source/data loss was found for the scoped default layout.
- `knowledge/fixtures/accepted/phase3c_visual_fidelity_gate.json` and its screenshots are retained as superseded evidence: they prove the old runtime was visible and deterministic, but not that it matches the native default map. The native-map acceptance gate is now closed by `phase3d_all_room_assembly_gate`; the historical baseline remains unchanged.
- `knowledge/fixtures/accepted/phase3c_visual_gate_v2.json` and `knowledge/fixtures/accepted/runtime/phase3c_visual_gate_v2_contract.json` remain superseded provenance for the earlier room:0/Room R structural gate. The active closure artifact is `knowledge/fixtures/accepted/phase3d_all_room_assembly_gate.json` and its runtime counterpart; it records `18/18` room composition and browser gates as pass.
- Phase 3A is closed as `approved`: the variable-piece OPT reconstruction consumes the exact `chair_00.opt` payload and its `[1, 2, 1]` piece-count cells without speculative bytes. The closure reason is `chair_00_opt_variable_piece_reconstruction_verified`.
- Phase 3A evidence is `knowledge/fixtures/accepted/phase3a_asset_composition_source_audit.json`, `knowledge/fixtures/accepted/phase3a_asset_composition_closure.json`, and `docs/reports/social-dev_phase3a_asset_composition_report.md`; the current stable audit hash is `77efba7c386cac9bed2d9944b84b984fa07bf411605f23cfa42834d7cbc91689`, and the closure hash is `1bddc93c4e08c8b4dba149ad7ace2e55d75ff4155be673d396b59dc72a2063b8`.
- The pinned APK was re-extracted through the `JarInflater` length-prefix path for `chair_00` through `chair_04`: all `15` PNG/OPT/SEB outputs are complete and match the supplied asset ZIP byte-for-byte. The extraction audit is `knowledge/sources/phase3a_apk_probe/chair_extraction_audit.json` with stable hash `50db4ec9b0017f13e7697efabaf52ad635ee14448fc84884df93b5b2217540c7`; the extracted triplets are retained under `knowledge/sources/phase3a_apk_probe/chair_entries/`.
- The APK probe confirms the same source bytes across the selected chair assets; the variable-piece parser now validates `chair_00`/`chair_01` with `[1, 2, 1]` cells, `chair_02`/`chair_03` with `[1, 1, 1]`, and `chair_04` with `[1, 2, 0]`. Runtime promotion uses only the source-backed outputs accepted by the Phase 3A closure.
- A three-version comparison now covers the supplied `2.4.9`, `2.5.0`, and `2.5.1` APKs. All three decrypt to the same `333`-entry chip pack plaintext and all `15` selected chair outputs are byte-identical across versions and match the supplied ZIP. The comparison audit is `knowledge/sources/phase3a_apk_probe/chair_version_comparison.json` with stable hash `255e0e34960511341d50450c42c1a7eee6fd30f50e4b2014974d581addf7a892`.
- The three-version result rules out an extraction/container or version-specific asset-loss explanation. The same bytes are sufficient after validating the variable-piece OPT grammar; no alternate payload is required, and compile-time erasure is not supported as the direct cause.
- Three historical non-authoritative `chair_00` visual variants remain for comparison: source-backed approximations, a complete `chair_02` substitute, and a hybrid. The variant audit is `knowledge/sources/phase3a_apk_probe/chair_variants/chair_00_variant_audit.json` with stable hash `a9312268c349b03057b774a8ac5b88b204e711c7e6476ee8743501f7e9e9473b`; they are superseded by the exact source-backed reconstruction for runtime.
- A structure comparison across `chair_00`–`chair_04` confirms one shared SEB animation scaffold (same one-layer/three-frame layout, source rectangles, and destination offsets; chair-specific `image_id` only) but different PNG dimensions and OPT crop/offset geometry. The audit is `knowledge/sources/phase3a_apk_probe/chair_structure_comparison.json` with stable hash `703863d1f12dd6626ada56b7e6e51ef583e08a276bad6e66e539b10a1704784c`.
- The exact `chair_00` reconstruction audit is `knowledge/sources/phase3a_apk_probe/chair_00_reconstruction_audit.json` with stable hash `68fa8a46ba92d8dfa9e6f7bace73f00e1ec391dd21ba0f2d75455d04b7a87c18`: `411/411` OPT payloads pass the variable-piece parser, `89/89` available derived logical references match pixel-for-pixel, and `chair_00` reconstructs from its original bytes with pixel SHA-256 `23d8e732fa2000f18f8fd9649b5fbe2b190d95aff86475b8befd09cfbe8afeef`.
- `knowledge/fixtures/accepted/runtime/display_asset_manifest.json` is `pass` / `approved_for_runtime_subset` with the approved actor/world subset plus native wall/door binaries. The adapter renders the approved human SEB crops, verified source-backed world chips, and strict native wall/door records; selector-only furniture remains outside the room projection. The runtime imports no archive, APK, C#, or unapproved binary.
- The OPT codec gate now proves exact pixel reconstruction for `chair_00`, `desk_00`, `chair_02`, `chair_04`, and the `door_03 → door_02` selector composition. The source bytes were not repaired or padded; the parser was corrected to model variable-piece cells. Asset-gate, adapter, and build checks pass without changing the historical placeholder baseline evidence.
- Phase 3B is closed for the native `room:0` placement contract: validation passes `20/20` checks, with native initialization order, raw map assignment, door `(8,4)`, type-4 footprint/passability, coordinate/camera boundaries, selector classification, and source-bounded draw order captured in a deterministic package.
- Phase 3B artifacts are `knowledge/fixtures/accepted/phase3b_room_placement_source_audit.json`, `knowledge/fixtures/accepted/phase3b_room_placement_fixture.json`, `knowledge/fixtures/accepted/phase3b_room_placement_validation.json`, and `knowledge/fixtures/accepted/runtime/room_placement_contract.json`; the builder/test are `tools/social-dev/build_phase3b_room_placement.py` and `tools/social-dev/test_phase3b_room_placement.py`.
- The Phase 3B package was re-materialized against the approved Phase 3A closure. The current contract hash is `b3992838276e00e6e381bb526c794283fee8d19a861143634dc0686bab646505`; `furniture:2` is approved as a display composition but remains unbound to a native room:0 FurnitureData placement. The floor selector remains source-unresolved because `chip/img.inf` has no id `5` entry; the fixed runtime policy borrows selector/data `85/floor_09.png` while rendering the valid `floor_05.png` asset. The strict Phase 3C package supersedes the earlier Phase 3B evidence-only boundary for wall/door runtime composition.
- The Phase 3B floor recovery pass is complete with `22/22` checks and semantic status `source_limited_unresolved_recovery_complete`. Its artifacts are `knowledge/fixtures/accepted/phase3b_floor_recovery_source_audit.json`, `knowledge/fixtures/accepted/phase3b_floor_recovery_fixture.json`, `knowledge/fixtures/accepted/phase3b_floor_recovery_validation.json`, and `docs/reports/social-dev_phase3b_floor_recovery_report.md`; the builder/test are `tools/social-dev/build_phase3b_floor_recovery.py` and `tools/social-dev/test_phase3b_floor_recovery.py`.
- Recovery conclusion: `RoomData(0).floorImgId_=5`, the supplied ZIP `chip/img.inf`, and the decrypted current APK `chip/img.inf` agree that id `5` has no authoritative filename. The APK scan found exactly one `chip` TextAsset across `1147` data entries and parsed a complete `333`-record pack; APK/ZIP `img.inf` is byte-identical with SHA-256 `5f37934c43bc86c3139d7415f1ae2c9315b4aef7bc81746b95db558a077e5310`. `floor_05.png` exists as an asset mapped to selector `23`, not selector `5`; the fixed runtime policy borrows selector/data `85/floor_09.png` while rendering the valid floor05 asset, preserving source status `unresolved` and exposing no alternate fallback/hybrid mode.
- Recovery hashes are source audit `88be12fe9e756b1abb33d6a2131d0638f343ef59922dd566acfee713320b1780`, fixture `9d7a5b29cefc6b3b9acffb03f773cc3ab1d597535fc482596327ed79a0099585`, and validation `48cd954b42f6c8e51803aebde4375bff122aac763a24bccd54d44379bee423b1`. The floor05 render asset is SHA-256 `be6572af9df60f5ed00eb0ab0e7d4dd95ba08749d7ec88b027a8ae5b3896c08c`; the fixed floor09 selector/data borrowing is an explicit product decision, not recovered source provenance.
- The runtime loader now requires the approved room-placement, Phase 3C render, strict closure, room-scene asset, room-scene runtime, native direction, native content catalog, and native scene assembly contracts. It validates 18 rooms, 23 exact room selector assets, 18 shared MapChip links, explicit room:0 native bindings, no ObjChip→FurnitureData inference, native direction mapping, 18/18 wall/door compositions, the nine-pass renderer order, and the render trace schema. Runtime typecheck, tests, production build, Python gates, and browser smoke pass.
- Wave 3/4/5 implementation artifacts are `knowledge/fixtures/accepted/runtime/native_content_catalog.json`, `knowledge/fixtures/accepted/runtime/native_scene_assembly_contract.json`, `knowledge/fixtures/accepted/runtime/phase3d_all_room_assembly_gate_contract.json`, `knowledge/fixtures/accepted/runtime/room_scene_runtime_contract.json`, `knowledge/fixtures/accepted/runtime/native_direction_contract.json`, `runtime/social-dev/src/scene/room-resolver.ts`, and `runtime/social-dev/src/renderer/canvas-renderer.ts`. The room selector exposes all 18 rooms and the resolver connects every selector to a runtime asset and native composition record.
- The Wave 3/4/5 implementation report is `docs/reports/social-dev_waves_3_4_5_runtime_report.md`; it records the logical/physical asset boundary, full native lifecycle/assembly bridge, all-room resolver flow, nine-pass renderer topology, render trace, and final verification output.
- The Phase 3C comparison policy is closed: the historical baseline remains preserved and the active runtime is not written over it. Any future visual replacement is a new explicit product decision, not a hidden acceptance gap. Completed 3A/3B records remain authoritative.

- Phase 2C is complete: the canonical ActorCatalog contract is `pass` / `approved_for_runtime_contract`, its validation passed `35/35` checks, and the readiness package passed `12/12` checks.
- The actor slice contains `5` StaffData records (`0–4`), `1` JobData record (`4`), `1` SkillData record (`1`), `5` resolved human image selectors (`86–90`), and `8` resolved wait/typing selectors (`10–13` / `23–26`).
- The bounded living-scene profile contains `35` source constants, `3` route mappings, `4` transition/timing records, and the selected SkillData type `10` / effect index `8` / value `150` / passive flag `1` contract.
- Canonical artifacts are `knowledge/fixtures/accepted/runtime/actor_catalog_contract.json`, `knowledge/fixtures/accepted/actor_catalog_fixture.json`, `knowledge/fixtures/accepted/actor_catalog_validation.json`, and `knowledge/fixtures/accepted/display_slice_contract.json`; the builder/test are `tools/social-dev/build_actor_catalog.py` and `tools/social-dev/test_actor_catalog.py`.
- ActorCatalog provenance includes `25` manifest inputs and `15` source slices. Stable hashes are fixture `322b68ea77f0c5567ba6470ae63e70fa95e689e104b9e7c87973611a1967f553`, contract `1268382df3f052096c2f648688d08feb0d38f868e4772a8ace1d2c97207c7a14`, and input `f58dc7f973388c5b63ad3d22f32da4951f3a13ea305b90484e488246c2a8090f`.
- The Phase 2C readiness package adds `knowledge/fixtures/accepted/actor_spawn_fixture.json`, `knowledge/fixtures/accepted/actor_spawn_validation.json`, `knowledge/fixtures/accepted/runtime/actor_spawn_contract.json`, `knowledge/fixtures/accepted/runtime/camera_coordinate_contract.json`, `knowledge/fixtures/accepted/runtime/actor_behavior_contract.json`, and `knowledge/fixtures/accepted/runtime/tick_order_contract.json`; its builder/test are `tools/social-dev/build_phase2c_readiness.py` and `tools/social-dev/test_phase2c_readiness.py`.
- The readiness package closes a source-bounded spawn fixture for `3` actors through `room:0` door `(8,4)`, producing position `(280,-31)`, `alpha_=0`, `speed_=3`, and `objIndex_=(8,4)` without inventing free cells. Stable hashes are spawn contract `5e8d0e7cffbcbf1145acbf976a7d1f568a098bef138b8fdc2af69f501f09abd6`, camera/coordinate `094429870c590de4253d9ef0986a7c969a00cf42c624f9b495535848d1726663`, behavior `3af31b5781833a204ce59a4e1b26b0191445d7ecb5856454d13179b3c13de91f`, and tick `d0fc4c8afc2834ee94494f9ad4d9abdce3a6b04c15974959863d609e3f5f1fad`.
- The Phase 2C implementation report is `docs/reports/social-dev_phase2c_actor_catalog_report.md`; the Vite/TypeScript core and renderer have not been created before this gate.

- Phase 2B is complete: the canonical ObjectCatalog contract is `pass` / `approved_for_runtime_contract`, and its validation passed `29/29` checks.
- The locked display slice contains `4` FurnitureData records (`0,1,2,5`), `7` raw ObjChip types (`0..6`), `3` scene bindings, `8` resolved selectors, and `4` explicit `-1` selector sentinels.
- Canonical artifacts are `knowledge/fixtures/accepted/runtime/object_catalog_contract.json`, `knowledge/fixtures/accepted/object_catalog_fixture.json`, and `knowledge/fixtures/accepted/object_catalog_validation.json`; the builder/test are `tools/social-dev/build_object_catalog.py` and `tools/social-dev/test_object_catalog.py`.
- The type-4 anchor at `(4,2)` is a verified `FurnitureData(0)` fixture with a `9`-cell footprint and the closed `3×3` passability matrix. The door at `(8,4)` is retained as a raw type-5 binding with installed flag `1`; its FurnitureData(1) identity remains a selector candidate because native `Room.PlaceDoor` passes `FurnitureData=null`.
- Selector identity (`seb_`/`subSeb_`/`img_`) remains indexed and provenance-backed. The bounded gate closes direct `big_base00`, `door_03 → door_02`, `desk_00`, `chair_02`, and now `chair_00` compositions; native room floor/wall/door placement was deferred at the Phase 2B boundary and is now covered by the Phase 3B contract.
- ObjectCatalog provenance is closed against the approved SceneCatalog/Phase 1D authority, `11` source slices, `17` manifest inputs, the pinned APK, and the asset ZIP. Stable hashes are fixture `9eb615bcabe36d31c04f39821a38361cda828f1bebd5ad082c267db21f8cca3d`, contract `2608e809a7769dd98eb5ff64ae5514a9998cd063abe80f51cf4335446bb1dd14`, and input `bed8ef38c1c4b26123232fef6597fce706146958138a07d6274c28786fac8c39`.
- The Phase 2B implementation report is `docs/reports/social-dev_phase2b_object_catalog_report.md`; the next active contract is `ActorCatalog`.

- Phase 2A is complete with the canonical `SceneCatalog` from `RoomData(0)`; contract status is `pass` / `approved_for_runtime_contract`, and fixture and validation status are `pass`.
- SceneCatalog validation passed `22/22` checks: scene `room:0`, locale names `Floor A` / `フロアA`, grid `10×10`, door type `5` at `(8,4)`, the type-4 footprint has `9` cells, and the route has `2` steps.
- Canonical artifacts are at `knowledge/fixtures/accepted/runtime/scene_catalog_contract.json`, `knowledge/fixtures/accepted/scene_catalog_fixture.json`, and `knowledge/fixtures/accepted/scene_catalog_validation.json`; the builder/test files are `tools/social-dev/build_scene_catalog.py` and `tools/social-dev/test_scene_catalog.py`.
- Phase 2A provenance is complete: `4` RoomData/FurnitureData English/Japanese row hashes, `11` selected C# source slices, `9` native methods, and a pinned APK hash; input hash `eb23e06212000bb77b86653e41f71291d4b8273a63df191378faafa876d615d2`.
- Stable hashes: fixture `980de8e1d972c0f3d32db6e14c6a0fe3396bd995ccc3b805c0cb356e459871e3`, contract `4f1fcf0665e72b6144dc3109c3b563670439018b6e5114b2ce9087ae467e80a9`.
- Phase 2A intentionally deferred full object-to-furniture placement and visual-asset promotion at that phase boundary; Phase 2C later closed camera/coordinate, bounded behavior, and fixed-tick readiness, and Phase 3 now implements the TypeScript runtime with explicit asset placeholders.
- Plan/report details are in `docs/roadmap/Roadmap_SocialDev_Phase2A_SceneCatalog.md` and `docs/reports/social-dev_phase2a_scene_catalog_report.md`.

- The Phase 1D engineering loop is complete: closure validation passed `18/18` checks, the route fixture has `2` steps, and unresolved selectors are `0`; authoritative status is `closed_for_phase2_entry`. The later Pre-runtime Closure Sweep formally reconciles the historical Phase 0–1C candidate queues to this authority.
- The real type-4 fixture is closed from the `RoomData(0)` anchor `(x=4,y=2)` plus `FurnitureData(0)` (`Huge World`, type `4`, passMap `9×9`); the verified `IsPassable` matrix is `[[true,false,false],[true,false,false],[true,true,true]]`, and zero-cell/all-nonzero probes pass.
- Native Astar neighbor admission and the public goal filter are verified: occupied type-2, `IsPassable=false` type-3/4, and type-6 are rejected; the real route is `(8,4) → (7,4) → (6,4)` with RoomData-row/native/APK provenance; equipment goal `(8,5)` uses `objDir=0 → direction 7`.
- The selector contract is closed from the real ZIP for parsed `103` FurnitureData rows and `141` StaffData rows in both English/Japanese: `seb_`, `img_`, and `subSeb_` (including sentinel `-1`) all resolve, and human typing/wait `seb` selectors resolve.
- The required staff living-scene contract is closed: state/move/flag constants, route-flag dispatch, bounded stay-home/equipment/talk transitions, talk-timing markers, typing/wait animation (`23–26` / `10–13`), and selected `SkillData(1)` type `10`, `effects_[8]=[150]`, and passive flag.
- Authoritative evidence: `phase1d_closure.json`, `phase1d_passmap_fixture.json`, `phase1d_route_fixture.json`, `asset_selector_contract.json`, `staff_semantics_contract.json`, and `phase1d_closure_validation.json`; the test runner is `tools/social-dev/test_phase1d_closure.py`.
- The Phase 1D closure package remains the authority for the native/passability/route/selector gates consumed by SceneCatalog.

- Social Dev is the sole active authority; the former GameDev/Virtual Office corpus was permanently removed after the cutover gates passed.
- The active data store was reorganized at `knowledge/sources/data/csharp_update/`: `44` staged C# data files / `437,881` bytes with a hash manifest; the source under `sources/raw/` remains read-only.
- Legacy C#/reverse-engineering/maintenance/root tools and historical task data were removed; active `tools/` contains Social Dev tools only.
- The R0 provenance pass is complete: the RAR, APK, asset ZIP, and C# update were fingerprinted; original source/extraction roots remain read-only; the derived `VGO_Core` scaffold was removed and was never promoted to runtime.
- The C# RAR baseline was extracted as evidence at `knowledge/sources/csharp_raw_20260813/`; decompiled C# is not executed directly.
- The C# update was compared by canonical path: `exact_match=4980`, `modified=588`, `update_only=586`.
- The Social Dev structural inventory is complete: `72` inputs, `82` types, `3430` fields, `1685` methods, fingerprint `1b2f9396f2768545d4f719022fb1b116df0de9a5347fb46337a8417e1257093a`.
- The candidate diff confirms that the update removes `Cpp2ILHelpers.NoteDecompilerIssue` from `60` gameplay/lifecycle files (`16699 → 0`) while `//IL_...` annotations remain `29030`; raw/update structural counts match, so this is textual cleanup rather than semantic repair.
- Marker-only normalization confirms `60` files are byte-equivalent after removing only marker lines, `12` are already exact, and `0` contain content changes beyond markers; the RAR remains the provenance anchor.
- The evidence-based candidate schema is complete: DataManager registry `43` typed arrays / `44` data classes / `1112` data fields; runtime-entity candidate `14` types / `919` fields / `30` lifecycle hooks / `21` relation candidates, with every semantic status still `unknown`.
- Load-contract candidates are complete: `41` registry entries match `Load(StringArrayStream)`, `2` still have no captured loader; field/load alignment has `38` candidates, `3` count mismatches, and `3` missing loads, so no production model is built from column positions.
- The asset/APK inventory passed the read-only gate: ZIP `3566` members, asset index `3542` rows, `zip_exact=3542`, APK source entries `3508` present / `34` missing (miscellaneous text payloads), matching APK fingerprint, and `25/25` pack-map roundtrip exact.
- Only evidence text/index was extracted from the ZIP: `114` files; the DataManager registry cross-check against XLS passed English `43/43` and Japanese `43/43`, with English extras `Exclusion.txt`, `softkey.txt`, and `text.txt` not promoted.
- The initial boundary is set: `data`/`game`/`game.routeSearch`/`main` are candidate evidence; `form` is presentation; `KairoEngine`/`Dependencies` are engine/dependency.
- `sources/raw/VGO_Core/` was removed: `5` files / `11,647` bytes, along with the scaffold inventory tools; only the historical removal record remains.
- The C# system boundary for new work was surveyed: `DataManager`/data registry, `Room`/scene, `ObjChip`/occupancy, `Staff`/living state, `Astar`/route, the `Player`/`AppData` subset, clock/tick, and visible event/text; `Player`, `AppData`, `DataManager`, `Staff`, and `Astar` must be rewritten as separate contracts rather than ported wholesale.
- The report `docs/reports/social-dev_csharp_system_survey.md` and roadmap `docs/roadmap/Roadmap_SocialDev_CSharp_Rewrite.md` were created, ordering the work as system extraction → normalized data → contracts → deterministic core → renderer.
- The web-app direction is locked as TypeScript source + Vite build + Canvas 2D scene renderer + DOM/CSS UI; Python is extraction/validation-only and there is no runtime package scaffold yet.
- The first plan is `docs/roadmap/Roadmap_SocialDev_Phase0_SystemExtraction.md`: create a machine-readable system inventory, dependency graph, source-slice manifest, and review queue before creating the Vite/TypeScript scaffold.
- Phase 0 has started: `csharp_system_inventory.json`, `csharp_dependency_graph.json`, `csharp_source_slice_manifest.json`, `csharp_semantic_review_queue.json`, and `csharp_extraction_validation.json` were created; structural validation passed with `types=82`, `fields=3430`, `methods=1685`, `systems=11`, `edges=14`, `slices=7`, `review_items=6`.
- All `7` source slices resolve to the type/method/field/constant catalogs (`missing=0`). The historical extraction artifact retains `pending_review` with `5` original blocking labels; the active Pre-runtime Closure Sweep closes those items without promoting damaged evidence.
- The Phase 0 generator/test files were added at `tools/social-dev/build_csharp_system_extraction.py` and `tools/social-dev/test_csharp_system_extraction.py`; tests pass.
- The Phase 1 plan is `docs/roadmap/Roadmap_SocialDev_Phase1_FirstSliceData.md`; it requires raw rows, locale cross-checks, loader boundaries, and provenance before creating a canonical runtime contract.
- The first-slice data candidate is evidence-based: `RoomData(0)`, `FurnitureData(1,2,5)`, `StaffData(0–4)`, `JobData(4)`, and loader-aware `SkillData(1)`, totaling `22` records; the previous skill selection `0` was corrected after parsing array framing.
- `knowledge/fixtures/accepted/first_slice_data_candidate.json` and `first_slice_data_validation.json` were created; validation passed with `types=5`, `records=22`, `missing=0`, `links=6`, `review_items=5`.
- The generator/test files `tools/social-dev/build_first_slice_data_candidate.py` and `tools/social-dev/test_first_slice_data_candidate.py` were added; tests pass and the candidate package remains historical evidence under the active closure authority.
- The Phase 1 report is `docs/reports/social-dev_phase1_first_slice_data_report.md`; `StaffData.jobId_ → JobData(4)` is only an `order_candidate`, while `skill_`, room state/placement, array semantics, and asset selectors are not promoted.
- Phase 1B was planned at `docs/roadmap/Roadmap_SocialDev_Phase1B_SceneBehavior.md`; loader-aware scene/behavior extraction was built from `StringArrayStream` plus field/load evidence without executing C# as runtime.
- `scene_data_candidate.json`, `staff_behavior_candidate.json`, and `scene_behavior_validation.json` were created; structural validation passed: `22` parsed records, RoomData `objMap_/objDir_` `10×10`, scene/behavior source slices `13/15`, `7` transition candidates, and `8` review items.
- Phase 1B confirmed the raw door-code candidate `(x=8,y=4,value=5)` and derived `JobData(4)` / `SkillData(1)` from selected staff; both remain candidate links rather than product relations.
- Phase 1B did not create a route path or room placement/passability contract; map-code semantics, asset selectors, numeric state labels, decompiler bodies, skill lookup, and animation selectors remain in the review queue.
- Phase 1C was planned at `docs/roadmap/Roadmap_SocialDev_Phase1C_SceneSemantics.md` to close scene semantic gates before creating the canonical catalog/runtime.
- `scene_semantics_review.json` and `scene_semantics_validation.json` were created; validation passed with `12` source slices, `9` observations, `103` FurnitureData IDs, `13` non-empty `passMap_` records, `6` route-goal candidates, and `6` review items.
- Phase 1D native evidence was built from the current APK: `scene_native_semantics.json` / `scene_native_semantics_validation.json`; the old package is candidate evidence and the new closure package is authoritative, pinned to the same APK SHA-256.
- Native IL2CPP confirms that `Room.InitObjChips` passes `objMap[y][x]` directly as `ObjChip.type_` and that the flat index is `x + y * width`; raw door `5` therefore closes the map-code assignment/door relation.
- Native `GetStandingPositions` closes the four-point deterministic formula; `ObjChip.PlaceObj`/`Room.PlaceDesk`/`AppData.NewGame` close the bounded furniture-placement model, with initial selection using `FLAG_INIT_DESK=16384` and `FLAG_INIT_PLACE=32768`.
- Native `Astar.AddNeighbor` confirms cardinal 4-neighbor movement only; the old 8-neighbor candidate is superseded and the Phase 1C package was rebuilt accordingly.
- All `103/103` FurnitureData rows were checked in English/Japanese; parse errors/missing locales are `0`; selected Door/Desk/Graphics Workstation (`1/2/5`) have empty `passMap_` arrays while type `4` has `13` non-empty passMap candidates.
- `ObjChip.IsPassable` boolean normalization is closed in the authoritative fixture: the 3×3 window uses `dx_ + dy_ * 3 + 4`, a zero cell returns `true`, and all nine nonzero cells return `false`; the null-furniture branch is closed within the fixture by explicit FurnitureData binding without guessing fallback selector identity.
- The route fixture authority has status `pass`: the path is built from real RoomData and filter probes confirm occupied type-2/type-4 false/type-6; no runtime catalog has been written yet.
- The active-reference scan after root cleanup read `5,820` text files and found `3,774` matches in `57` files; intentional documentation `355`, legacy artifacts `3,419`, active dependency `0` — reference gate passed.
- The post-VGO-removal reference scan covered `5,787` active text files and found `209` matches with `active_dependencies=0`; no VGO source/tool remains in the active tree.
- `runtime/social-dev/` is the active contract-first runtime boundary with an approved binary subset under `runtime/social-dev/assets/display-slice-01/`; the old Office/Dashboard is deleted and no longer participates in the project.
- The product target is locked: preserve the original scene, original characters, and visible living logic; remove player-facing gameplay that is not required for display.
- A data-readiness roadmap was created for `display-slice-01`: field provenance, loader review, selector validation, scene contract, living trace, and runtime-readiness gates.
- The next active-slice work follows `SceneCatalog → ObjectCatalog → ActorCatalog → deterministic fixtures → TypeScript runtime core`; do not return to runtime creation before the canonical evidence contract.

## Removed Historical Baseline

The former GameDev/Virtual Office baseline and its source, runtime, tools, and task records were deleted with the legacy archive. Only current Social Dev evidence and contracts may be used.

## Verified Checks

- Task 2 fix round 1 closes trailing-byte/recovery/staging gates: codec/audit tests passed `9/9`; the Task 1+2 suite passed `14/14`; build audit and `py_compile` passed; source/extraction file hashes for `1,881` items match the Task 1 inventory.
- The primary C# corpus has `85` `.cs` files and `Assembly-CSharp.csproj`; source hashes match the relocation manifest from before the move.
- The C# coverage/semantic checker compiles and references paths inside the new workspace.
- The structural inventory contract passed `3/3`; build/check passed with `types=14`, `fields=926`, `methods=257`.
- The semantic-slice contract passed `5/5`; C# evidence tests total `8/8`.
- The inventory input boundary has `11` files: `5` primary files and `data/*.cs`; the latest structural fingerprint is `24e14f6e7beea8521406aee64e946803c257e5e7c537bc92450ca50ef29207da`.
- The latest semantic fingerprint is `c67de72477df0273f68764f5c02d0a23993ab7ca28c291fda0bb93512ff002ae`; there are `18` bounded access edges.
- Gameplay field claims have statuses `verified=8`, `raw_only=10`, `assembly_fallback_bounded_slice_required=3`; method claims include `DoEvent` as an assembly fallback.
- Historical simulation-core checks belonged to the deleted legacy project and are not part of the active Social Dev verification set.
- SimulationCore tests passed for spawn/move/arrival, blocked collision, invalid-command immutability, deterministic digest/subscriber behavior, and bubble expiry.
- Wave 5 runtime regression passed `11` scenarios after the facade migration; Wave 6 task-system tests passed `18` scenarios.
- The dashboard canonical snapshot/evidence contract passed `12/12`; `app.js` syntax check passed; browser script order was verified as schema → core → runtime.
- Continuous-scheduler tests passed `2` scenarios; `app.js` and scheduler syntax checks passed.
- Python office/dashboard contracts passed `32/32` in total.
- Final regression passed: C# evidence `8/8`, characters `5/5`, reverse-engineering `214/214`, maintenance `4/4`, office Python `20/20`, dashboard Python `12/12`; all Node schema/core/scheduler/office/dashboard tests passed.
- Character tests passed `5/5`.
- The reverse-engineering suite passed `214/214`; corpus A0/A1 checks and the A2 canonical `--check` passed.
- The office runtime passed `11` Node scenarios and the Python Wave 5 contract `20/20`.
- The dashboard runtime passed `18` Node scenarios and Python contract `12`.
- Maintenance tests passed `4/4`; Python compile checks passed; browser smoke passed: READY/tick advanced automatically from `96 → 101` in about `700ms`, canvas `600x800`, diagnostics contained `simulation-core-v1`/evidence, task create/assign passed, there were no console errors/warnings, and the test server was stopped.
- Relocation comparison passed: logical members are complete and protected roots have the same file counts/bytes.
- Test-created cache/temp files were cleaned and no local server remains.
- The original source roots remain read-only; the dumped `Assembly-CSharp.dll` remains in the dump as before.

## Key Decisions

- Use only the current Social Dev evidence boundary for discovery and control-flow evidence; never execute decompiled C# directly.
- The Social Dev web runtime uses TypeScript + Vite + Canvas 2D + DOM/CSS; the core is UI-framework independent, and the browser runs only compiled JavaScript from promoted catalogs/contracts.
- Use recovered C/assembly and evidence contracts as semantic validators when C# contains decompiler artifacts or remains `unknown`.
- The initial runtime is a continuous deterministic simulation without time-acceleration/stop controls; add LLM/task backend later.
- Keep current evidence and source roots read-only; historical GameDev material has been intentionally deleted and must not be recreated.

## Known Limitations

- The floor selector `RoomData(0).floorImgId_=5` has no direct authoritative `chip/img.inf` row. The fixed runtime policy is explicit and closed: selector/data alias `85/floor_09.png` supplies metadata while the approved render pixels come from `floor_05.png`; source provenance remains marked separately.
- Rooms 1–17 have no native initial FurnitureData instance bindings in the recovered `AppData.NewGame` bootstrap evidence. The closed runtime result is to render their raw ObjChip topology plus native wall/door composition and leave unbound furniture slots empty; no FurnitureData identity is inferred.
- The production bundle is intentionally large because the complete runtime content catalog is embedded for queryable native IDs; Vite reports a non-blocking chunk-size warning. The catalog is present for future calls and is not a semantic blocker.
- The APK/ZIP contains Unity data members named by hashes and no direct `floor*.seb`; locating embedded TextAssets requires additional bundle-provenance evidence, so it is not yet proven whether the shortfall is a true source limitation or a nested-extraction defect.
- Semantic names for numeric states and some branches still require multiple C#/C/assembly evidence sources; do not guess while evidence conflicts.
- Several C# decompiler bodies for raw arrays do not show field names directly; the current access edges therefore use bounded reverse-engineering claims with provenance rather than claiming complete C# body parsing.
- `HumanMode`, `HumanState`, `HumanAnime`, `EventMode`, and numeric message/graph labels have not been promoted to product semantics.
- The scheduler is only a wall-clock UI driver; logical tick/snapshot/digest behavior remains deterministic and has no visible stop/pause/speed path.
- `CoreOfficeRuntime` is an exported facade that delegates mutation to the core; old provider contracts and renderer projections still operate through the existing API.
- The C# corpus is decompiler evidence, not a buildable runtime; the project references external outputs and has no compile verdict.
- The current office/dashboard is a deterministic adapter baseline, not a complete game, and has no LLM, backend, auth, or multi-user sync.

## Important Files

- `knowledge/sources/data/csharp_update/` and `knowledge/sources/data/data_package_manifest.json` — active organized Social Dev data package
- `runtime/social-dev/package.json`, `runtime/social-dev/tsconfig.json`, and `runtime/social-dev/vite.config.ts` — active Vite/TypeScript runtime scaffold
- `runtime/social-dev/src/catalog/` — approved-contract loader, native ID lookup bridge, and type boundary
- `tools/social-dev/build_native_room_floor_closure.py` and `tools/social-dev/test_native_room_floor_closure.py` — deterministic native `Room.floor_` call-site/array catalog builder and regression gate
- `knowledge/fixtures/accepted/native_room_floor_usage_catalog.json`, `knowledge/fixtures/accepted/runtime/native_room_floor_usage_contract.json`, and `docs/reports/social-dev_room_floor_topology_closure.md` — native floor selector, dimensions, usage paths, and explicit topology boundary
- `knowledge/fixtures/accepted/runtime/character_metadata_contract.json` and `knowledge/fixtures/accepted/runtime/character_capability_contract.json` — full static character catalog plus shared family/action capability contract
- `runtime/social-dev/src/catalog/character-resolver.ts` — lazy template, action selector, and spawn-plan resolver for StaffData/HelperData
- `tools/social-dev/build_asset_metadata_baseline.py` and `tools/social-dev/test_asset_metadata_baseline.py` — deterministic AM-0 input/hash/count baseline builder and gate
- `tools/social-dev/build_asset_metadata_coverage.py` and `tools/social-dev/test_asset_metadata_coverage.py` — AM-1 per-asset/selector/field/relation/runtime-entry coverage matrix and orphan audit
- `knowledge/fixtures/accepted/asset_metadata_baseline.json`, `knowledge/fixtures/accepted/runtime/asset_metadata_baseline_contract.json`, and `docs/reports/social-dev_asset_metadata_baseline.md` — frozen AM-0 snapshot
- `knowledge/fixtures/accepted/asset_metadata_coverage.json`, `knowledge/fixtures/accepted/asset_metadata_orphan_report.json`, `knowledge/fixtures/accepted/runtime/asset_metadata_coverage_contract.json`, and `docs/reports/social-dev_asset_metadata_coverage.md` — AM-1 coverage and gap artifacts
- `tools/social-dev/build_asset_family_taxonomy.py`, `tools/social-dev/build_asset_selector_usage_matrix.py`, `tools/social-dev/build_asset_composition_geometry.py`, and `tools/social-dev/build_asset_usage_lifecycle_placement.py` — AM-2 through AM-5 deterministic builders
- `knowledge/fixtures/accepted/asset_family_taxonomy.json`, `asset_selector_usage_matrix.json`, `data_field_semantics_matrix.json`, `asset_composition_catalog.json`, `asset_geometry_catalog.json`, and `asset_usage_lifecycle_placement_matrix.json` — complete family, selector, field, composition, geometry, and usage evidence
- `tools/social-dev/build_furniture_asset_metadata.py` and `tools/social-dev/build_character_visual_asset_metadata.py` — Track W/H builders and gates
- `knowledge/fixtures/accepted/furniture_asset_metadata.json`, `character_visual_asset_metadata.json`, `knowledge/fixtures/accepted/runtime/furniture_asset_metadata_contract.json`, and `knowledge/fixtures/accepted/runtime/character_visual_asset_metadata_contract.json` — world/character metadata contracts
- `tools/social-dev/build_asset_surface_provenance.py` and `tools/social-dev/build_asset_metadata_completion_gate.py` — Track X/A provenance and final audit builders
- `knowledge/fixtures/accepted/asset_surface_provenance.json`, `knowledge/fixtures/accepted/asset_metadata_completion_gate.json`, `knowledge/fixtures/accepted/runtime/asset_surface_provenance_contract.json`, `knowledge/fixtures/accepted/runtime/asset_metadata_completion_contract.json`, and `docs/reports/social-dev_asset_surface_provenance.md` — source boundary and final completion artifacts
- `runtime/social-dev/src/catalog/asset-metadata.ts` and `knowledge/fixtures/accepted/runtime/asset_metadata_runtime_manifest.json` — stable runtime metadata query surface
- `runtime/social-dev/src/catalog/floor-resolution.ts` and `knowledge/fixtures/accepted/runtime/default_map_chip_contract.json` — single explicit floor09 selector/data plus floor05 render composition
- `runtime/social-dev/src/core/` — deterministic state, fixed tick, route, event, and digest implementation
- `runtime/social-dev/src/assets/display-assets.ts` — approved manifest loader, frame selector, browser image adapter, and single floor05 render binding
- `runtime/social-dev/src/scene/` and `runtime/social-dev/src/renderer/` — room projection, coordinates, Canvas, and DOM/CSS presentation
- `runtime/social-dev/tests/` — deterministic, contract, route, and browser-trace gates
- `tools/social-dev/build_display_asset_gate.py` and `tools/social-dev/test_display_asset_gate.py` — source-bounded SEB/PNG gate and regression checks
- `tools/social-dev/build_phase3a_asset_composition.py` and `tools/social-dev/test_phase3a_asset_composition.py` — Phase 3A source audit, quarantine closure, and deterministic checks
- `tools/social-dev/build_phase3a_chair_00_reconstruction.py` and `tools/social-dev/test_phase3a_chair_00_reconstruction.py` — exact variable-piece `chair_00` logical reconstruction, crop-map evidence, and full-pack/reference validation
- `tools/social-dev/extract_phase3a_chairs_from_apk.py` and `tools/social-dev/test_phase3a_apk_chair_extraction.py` — APK loader-path chair extraction, ZIP byte comparison, and semantic checks
- `tools/social-dev/compare_phase3a_chair_apk_versions.py` and `tools/social-dev/test_phase3a_chair_apk_versions.py` — three-version APK pack/triplet comparison and semantic regression gate
- `tools/social-dev/build_phase3a_chair_00_variants.py` and `tools/social-dev/test_phase3a_chair_00_variants.py` — non-authoritative chair_00 approximation previews and boundary checks
- `tools/social-dev/compare_phase3a_chair_structures.py` and `tools/social-dev/test_phase3a_chair_structures.py` — cross-chair PNG/OPT/SEB pattern comparison and regression gate
- `tools/social-dev/opt_codec.py` and `tools/social-dev/test_opt_codec.py` — evidence-backed OPT parser, logical reconstruction, and pixel-match checks
- `knowledge/fixtures/accepted/display_asset_gate.json`, `knowledge/fixtures/accepted/runtime/display_asset_manifest.json`, and `docs/reports/social-dev_display_asset_gate.md` — asset promotion evidence and runtime subset contract
- `knowledge/fixtures/accepted/phase3a_asset_composition_source_audit.json`, `knowledge/fixtures/accepted/phase3a_asset_composition_closure.json`, and `docs/reports/social-dev_phase3a_asset_composition_report.md` — Phase 3A closure evidence
- `knowledge/fixtures/accepted/phase3b_room_placement_source_audit.json`, `knowledge/fixtures/accepted/phase3b_room_placement_fixture.json`, `knowledge/fixtures/accepted/phase3b_room_placement_validation.json`, and `knowledge/fixtures/accepted/runtime/room_placement_contract.json` — Phase 3B native room-placement contract
- `tools/social-dev/build_phase3b_room_placement.py` and `tools/social-dev/test_phase3b_room_placement.py` — Phase 3B deterministic builder and regression gate
- `docs/reports/social-dev_phase3b_room_placement_report.md` — Phase 3B closure report
- `knowledge/sources/phase3a_apk_probe/chair_extraction_audit.json` and `knowledge/sources/phase3a_apk_probe/chair_entries/` — pinned-APK chair triplet extraction evidence
- `knowledge/sources/phase3a_apk_probe/chair_version_comparison.json` — `2.4.9`/`2.5.0`/`2.5.1` chair pack comparison evidence
- `knowledge/sources/phase3a_apk_probe/chair_variants/` — three derived chair_00 previews, comparison sheet, and variant audit
- `knowledge/sources/phase3a_apk_probe/chair_structure_comparison.json` — shared animation scaffold and per-chair geometry comparison
- `knowledge/sources/phase3a_apk_probe/chair_00_reconstruction_audit.json` and `knowledge/sources/phase3a_apk_probe/derived_previews/chair_00.logical.png` — exact source-backed `chair_00` reconstruction and pixel proof
- `docs/roadmap/Roadmap_SocialDev_Phase3A_AssetComposition.md` — detailed Phase 3A recovery/quarantine plan, evidence matrix, and acceptance gates
- `docs/reports/social-dev_phase3_display_runtime_report.md` — bounded Phase 3 display runtime and Phase 3C gate report
- `knowledge/fixtures/accepted/display_slice_01_screenshot_baseline.png` and `display_slice_01_behavior_trace.json` — historical browser gate evidence
- `knowledge/fixtures/accepted/phase3c_browser_visual_gate.json`, `phase3c_candidate_frame_6.png`, and `phase3c_candidate_frame_136.png` — Phase 3C browser visual evidence
- `knowledge/fixtures/accepted/phase3c_render_fixture.json`, `phase3c_render_validation.json`, and `knowledge/fixtures/accepted/runtime/phase3c_render_contract.json` — Phase 3C render-contract evidence
- `knowledge/fixtures/accepted/phase3c_strict_closure.json`, `phase3c_strict_closure_validation.json`, and `knowledge/fixtures/accepted/runtime/phase3c_strict_closure_contract.json` — strict native wall/door and initial-furniture closure evidence
- `knowledge/fixtures/accepted/phase3c_strict_browser_visual_gate.json` and `phase3c_strict_browser_smoke_frame_136.png` — superseded strict native browser smoke evidence retained for provenance
- `knowledge/fixtures/accepted/phase3c_visual_fidelity_gate.json`, `phase3c_default_entry_smoke_frame_0.jpg`, and `phase3c_visual_fidelity_smoke_frame_136.jpg` — superseded image-level default-entry/frame-136 browser evidence; native-map acceptance is covered by the active `phase3d_all_room_assembly_gate`
- `knowledge/fixtures/accepted/phase3c_visual_gate_v2.json`, `phase3c_visual_gate_v2_room0_frame0.png`, `phase3c_visual_gate_v2_room0_frame1.png`, `phase3c_visual_gate_v2_room0_frame2.png`, and `phase3c_visual_gate_v2_room17_raw_overlay.png` — superseded structural visual gate evidence retained for provenance
- `tools/social-dev/build_phase3c_visual_gate_v2.py` and `tools/social-dev/test_phase3c_visual_gate_v2.py` — deterministic visual-gate builder and content-addressed screenshot regression gate
- `docs/roadmap/Roadmap_SocialDev_Phase2B_ObjectCatalog.md` — completed Phase 2B implementation plan and closure record

## Living-Core Final Closure (2026-08-15)

- The static native pass is complete with status `PASS_ORIGINAL_LIVING_CORE_CLOSED`.
- Pinned v2.5.1 identity passed: APK `fa0e9e3a843732258fc05b2611a8e0f5be6f7e95f2141a53f31fb082322fe2bf`; `lib/arm64-v8a/libil2cpp.so` `364893401fcf7fc2380ae64291783edf7b95eecea4775041c3f4c8c081b4d54a`; `assets/bin/Data/Managed/Metadata/global-metadata.dat` `f65f3a00675f35cfa28fef53c37ed7a2dc01e143b6d59c6014a286fa84e4a579`.
- LC-1 closed as `CLOSED_NO_ORIGINAL_DRAIN`: native `Staff.UpdateWork` has no `hp_` write or `RecoverHp` call.
- LC-2 closed as `CLOSED_NATIVE_RECOVERY_CADENCE`: `AddRecoveryHpStock` starts at `20` frames, `UpdateRecoveryHp` consumes one HP stock on native `frame_%3==0`, and exhaustion resets the gauge/effect state to `40` with stock `0`.
- LC-3 closed as `CLOSED_OWNER_BASED_RAW_ORDER`: an installed type-2 chip with `staffId_ == -1` is vacant; `Room.GetStaffEmptyObjTypeOf` returns the first raw-order match. No fairness queue is present in the original selector.
- LC-4 closed as `CLOSED_11_WAY_NATIVE_DISPATCH`: `Staff.OnArriveGoal` table at rodata `0x636684`, base `0x12D84A8`, key `moveMode_` offset `0xA8`, modes `1..11` decoded.
- LC-5 closed as `CLOSED_EXACT_NATIVE_ROLES`: `103` FurnitureData records classify as `10` workstations, `49` recovery equipment, `43` non-recovery equipment, and `1` door; no REST/SOCIAL furniture role was invented.
- LC-6 closed as `CLOSED_ORIGINAL_AUTONOMOUS_PATH_WITH_UI_CUT_LATER`: StaffData binding, room/desk attach, planning gate, Staff.Update, and autonomous UpdateWork are connected. Exposed `SetJobId`, `ChangeSkill`, and `EvolveJob` have no recovered extracted-C# callers. Original UI remains `CUT_LATER`; future dashboard policy is `PRODUCT_POLICY_PENDING`.
- Evidence and reports are under `knowledge/fixtures/accepted/living-core-closure/` and `docs/Phases/Behavior/`; the builder/test are `tools/social-dev/build_living_core_final_closure.py` and `tools/social-dev/test_living_core_final_closure.py`.
- Verified static checks: Living-Core `109` checks; behavior-first regression `118` checks; data-dependency regression `2432` checks; pre-runtime closure `21` items / `13` verified / `0` deferred.
- Scope stop is explicit: visual work `NO`, V8 `NO`, renderer/MapChip unchanged, subagents `NO`, emulator/ADB/live app `NO`, local server `NO`, network `NO`. Source roots remain read-only and no runtime implementation was changed.

## Next Work — Social Dev

## Historical K2 Unified Whole-Game Brain (2026-08-16, complete)

- The primary K2 execution contract and companion guide were read completely before repository changes. The companion guide SHA-256 is `7da012a4f46e9302e7185f7478d5c20601f9b3c3402922aa24b9ddff753dabec`.
- K2.PRE passed after re-verification of the pinned APK, native binary, metadata, C# archive, dump, pre-K2 compact, old G1.5 database, Unity TextAsset payloads, C# Tier-A inventory, MapChip hashes, and the supported baseline/regression matrix.
- The pre-K2 compact still matches its pinned SHA-256. One current-evidence drift is recorded rather than rewritten: `knowledge/fixtures/accepted/i2-dashboard-runtime/validation.json` was regenerated by the required I2 baseline scenario and differs from the stale preflight manifest hash; no other preflight input changed.
- K2 builder/validator/query tooling is present at `tools/social-dev/build_k2_unified_brain.py`, `tools/social-dev/test_k2_unified_brain.py`, and `tools/social-dev/query_k2_brain.py`. No subagents, server starts, deployment, K3, V8, Cloudflare, Oracle, persistence, or backend AI work has been started.
- K2.0 through K2.FINAL completed in order. The side-by-side `knowledge/brain/sqlite/social_dev_brain.sqlite` preserves the G1.5 tables and adds the required artifact/reference, namespace/identity, semantic-edge, implementation/acceptance, usage, derived-artifact, and gap-queue tables. The old `knowledge/data/original/sqlite/social_dev_original_data.sqlite` remains byte-identical at SHA-256 `9d561f7d5708c73b6b8a80acca10681f0323ec5a001145ed9c63215987d79d37`.
- K2.10 cut the production runtime over to `runtime/social-dev/src/catalog/load-original-runtime-pack.ts`; only that facade imports the generated runtime JSON pack. K2.11 full regressions and K2.12 active-surface/gap closure passed. Final token: `PASS_K2_UNIFIED_WHOLE_GAME_BRAIN_AND_RUNTIME_PACK_CLOSED`.
- K2 stopped at the required boundary. K3, V8, Cloudflare, Oracle, persistence, backend AI, and deployment remain explicitly unstarted.

The requested native assembly/connection closure is complete. The runtime is ready for later user-directed content changes through the native record, selector, asset, room, and render-trace IDs. The historical baseline remains intentionally preserved; a future baseline replacement would be a separate explicit product decision.

Phase V4 is deliberately stopped at its final gate. V5 and V6 are complete for their selected static scopes; V7 is not started automatically. Exact raster/framebuffer parity remains a separate V7 boundary.

The asset-metadata workstream is complete for the supplied package. Future work is deliberately user-directed: add a screen/event consumer contract before promoting any of the 21 non-actor families, close the 34 Unity TextAsset/APK gaps if the nested source becomes available, resolve `lineup_layout/bg.seb` if its target is recovered, or expand the runtime manifest beyond the current 186 explicit rows.

The full human character layer is ready for metadata lookup, native action selection, decoded frame composition, and lazy pixel rendering. The bounded `display_asset_manifest` remains intentionally unchanged; the separate character asset contract is the authority for all `141` StaffData image bindings. Remaining character work is limited to separate HelperData/avatar/event-only asset packages and any future scene that chooses to spawn the full catalog.

## Previous Work Boundary

- Historical GameDev/Office material is deleted and is not a source for current work.
- Backend/auth/multi-user and LLM work waits until the Social Dev baseline passes contract tests.
