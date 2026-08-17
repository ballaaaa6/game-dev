# I0 Scenario Acceptance

The runtime harness executes the ten frozen fixtures from the generated R0 catalog. It does not branch production behavior on scenario IDs; scenario setup invokes public runtime operations and the same state handlers used by the ordinary runtime.

Evidence is generated under `knowledge/fixtures/accepted/i0-living-runtime/`:

- `scenario-results.json` records initial/final canonical snapshots and assertions.
- `transition-traces/S1.jsonl` through `S10.jsonl` record actual mutation traces.
- `deterministic-rng-replay.json` records the byte-identical S10 replay.
- `checkpoint-ledger.json` records I0.PRE through I0.FINAL.

The independent acceptance tool is `tools/social-dev/test_i0_living_runtime.py`.
