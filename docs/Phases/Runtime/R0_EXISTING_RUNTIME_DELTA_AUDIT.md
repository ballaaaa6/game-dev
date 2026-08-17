# R0 Existing Runtime Delta Audit

Status: `PASS_CANONICAL_RUNTIME_CONTRACT_FREEZE_READY_FOR_IMPLEMENTATION`.

The audit compares the current web runtime and legacy runtime contracts with the canonical G1.5/living-core evidence. The machine-readable matrix is `knowledge/fixtures/accepted/runtime-contract-freeze/runtime-delta-matrix.json`.

## Disposition counts

- `EXTEND`: 3
- `KEEP`: 2
- `KEEP_VISUAL_ONLY`: 112
- `OUT_OF_SCOPE`: 11
- `PRODUCT_LAYER_ONLY`: 0
- `REPLACE`: 3
- `SUPERSEDED`: 3
- `UNKNOWN_REVIEW_REQUIRED`: 0

## Explicit legacy behavior findings

- `runtime/social-dev/src/core/simulation.ts` contains a fixed route trace, fixed talk start/end markers, and no injected RNG. It is `SUPERSEDED`.
- `knowledge/fixtures/accepted/runtime/actor_behavior_contract.json` is a bounded display trace, not original Staff autonomy. It is `SUPERSEDED`.
- `knowledge/fixtures/accepted/runtime/tick_order_contract.json` is `REPLACE`: it lacks the native recovery/low-HP/state/arrival positions and assumes stable display-ID order.
- The old display ActorState lacks authoritative HP, recovery stock, desk ownership, active/reserved equipment users, and product-state separation.

No living-runtime entry is `UNKNOWN_REVIEW_REQUIRED`; implementation blockers are zero.


R0 execution boundary: inline, static/contract only, no subagents, no emulator/ADB, no network, no server, no V8, no MapChip or Renderer changes, and no living-core implementation.
