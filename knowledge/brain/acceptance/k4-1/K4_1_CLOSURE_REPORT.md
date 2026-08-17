# K4.1 Targeted Closure

Status: complete

Final token: PASS_K4_1_TARGETED_CLOSURE_READY_FOR_V8

K4.1 independently closes the three targeted K4 visual blockers from pinned APK, C# source, IL2CPP metadata, native disassembly, and accepted Room0 contracts. V8 remains NOT_STARTED.

## Required end state

- blocking_source_limited_count: 0
- source_missing_count: 0
- heuristic_or_assumed_count: 0
- ready_for_v8: true

No blocking source-limited relations remain.

## Classifications

- `room0.door.action-timeline`: `REPRODUCED_WITH_CORRECTION`; action/update/fade state is real, but the Room0 null-FurnitureData DrawWall consumer has no distinct visible action timeline.
- `staff.talk.fukidashi-payload`: `REPRODUCED_EXACT`; roles, timing, exact pools, random semantics, EN/JA path, bubble lifetime/offset, draw, and cleanup are proven.
- `workstation.live-interleave`: `REPRODUCED_EXACT`; live type-2 direction-specific desk/chair/Staff.Draw order, preview separation, late chair guard, and duplicate Staff guard are proven.

Every research-pack hypothesis is recorded in `research_findings` with only the allowed classification vocabulary; unsupported extra handle `0x27D7E40` is `REJECTED_BY_SOURCE`.

## Verification

- k2_unified_brain: PASS (python -B tools/social-dev/test_k2_unified_brain.py)
- native_content_registry: PASS (python -B tools/social-dev/test_native_content_registry.py)
- native_content_catalog: PASS (python -B tools/social-dev/test_native_content_catalog.py)
- native_room_floor_closure: PASS (python -B tools/social-dev/test_native_room_floor_closure.py)
- display_asset_gate: PASS (python -B tools/social-dev/test_display_asset_gate.py)
- runtime_typecheck: PASS (npm run typecheck)
- runtime_vitest: PASS (npm test -- --run)
- k4_artifact_validation: PASS (python -B tools/social-dev/test_k4_visual_closure.py)
- k4_1_targeted_validation: PASS (python -B tools/social-dev/test_k4_1_targeted_closure.py)

## Boundary

- Pinned source roots remained read-only.
- Original runtime/data/visual packs remained byte-identical.
- Runtime code, MapChip pixels, server, browser, emulator/ADB, live app, network, subagents, and V8 were not used.
