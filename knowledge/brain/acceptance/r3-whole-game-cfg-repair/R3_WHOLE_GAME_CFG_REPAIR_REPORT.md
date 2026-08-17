# R3 Whole-Game CFG Repair

Acceptance token: `PASS_R3_WHOLE_GAME_CFG_REPAIR_CLOSED`

## Decision

R3 is **accepted with explicit CFG deferral**. The canonical universe contains 641 target types and 10,827 methods. The profiler found 2,856 active CFG rows: 2,708 directly deferred by R2 and 148 recovered from blocked identity using exact R1.5 line spans and body hashes.

No R3 source body was changed. No native body lift, Unity work, V8 work, or guessed graph edge was performed. No family met the semantic binding and graph-equivalence gates, so no canary or expansion was authorized.

## Identity recovery

R2's 2,634 identity blockers were fully root-cause counted. 2572 routed with exact source-body or ISIL identity evidence; 62 remain explicitly blocked. The full routed status universe is recorded in `r3-method-status-summary.json`.

## CFG evidence and families

All 2856 active CFG rows have local evidence bundles containing the exact source body/hash, R0/R1.5 signals, ISIL facts, graph edges, accepted evidence references, and Roslyn diagnostics availability. Observed families: `DECOMPILER_TYPE_CFG_DAMAGE` (177), `LOCAL_GOTO_BRANCH_CFG` (62), `LOOP_CFG_COLLAPSE` (18), `OTHER_CFG` (714), `STRUCTURED_CONTROL_SUSPECT` (10), `SWITCH_OR_JUMP_TABLE_COLLAPSE` (1858), `SWITCH_STRUCTURAL_DAMAGE` (5), `TYPE_EROSION_PLUS_HEAVY_GOTO` (12).

The transformer library is Roslyn-based and proof-gated. `LOCAL_GOTO_BRANCH_CFG` is the only narrow syntax-node transformer shape implemented, but the corpus has no semantic proof available for a canary. `OTHER_CFG` is explicitly ineligible for generic cleanup.

## Negative fixtures and graph

All 5 mandatory negative fixtures reject. The rejected edits include orphan identifier consumers, declaring-type local guesses, syntax-only proof, and an unproven invariant generic-cast removal.

The graph delta is zero: the accepted R2 call/field split is retained unchanged, with no guessed edges. The original source roots remain read-only and unchanged.

The second canonical profiler run reproduced the compact indexes and all 2,856 evidence-bundle hashes.

Next authorized boundary: **R4 native/ISIL semantic lift**. Stop after R3; do not start R4, Unity, V8/web, integrations, or persistence in this task.
