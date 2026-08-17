# R2 Automated Whole-Corpus Repair

Decision: `PASS_R2_AUTOMATED_WHOLE_CORPUS_REPAIR_CLOSED`

## Canonical input universe

- Types: 641
- Target methods: 10,827
- Queue/status coverage: 10,827
- Pinned source identities: PASS

## Roslyn and Twin

- Offline Roslyn toolchain: PASS (5.0.0.0; SDK rows absent, bundled host validated).
- Twin root: `D:\antigravity\test open ai\artifacts\r2-reference-twin`
- Files materialized: 442
- Original source corpus changed: NO

## Repairs and deferrals

- AUTO_TYPE candidates attempted: 429; exact eligible: 4; repaired: 4; remaining candidates are blocked or explicitly deferred.
- Static/exporter payload repairs: 0; unproven payloads deferred.
- Noise repairs: 0; decompiler markers preserved.
- CFG micro-repairs: 0; deferred to R3 under the deterministic-equivalence boundary.
- Native/ISIL body repairs: 0; deferred to R4.

## Validation

- Batch apply: PASS
- Provenance: 4 complete `REPAIRED_CSHARP` records
- Deterministic replay: PASS
- Twin reindex and graph split: PASS; graph delta is zero
- Final queue coverage: 10,827/10,827

## Boundary

Native lifting: NO. V8/V8R: NO. Unity/Unity-MCP: NO.

Next recommended phase: `R3_WHOLE_GAME_CFG_REPAIR`.

STOP.
