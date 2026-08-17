# R0 Scenario Fixtures

`runtime-scenario-fixtures.json` contains ten contract fixtures: S1 desk work entry, S2 equipment interruption, S3 talk interruption, S4 low-HP home recovery, S5 desk contention, S6 equipment contention, S7 desk destruction, S8 planning start, S9 planning end, and S10 deterministic RNG replay.

The fixtures are not executed against a new living runtime in R0. They assert canonical transitions, ownership/reservation deltas, HP effects, route/arrival milestones, and final invariants. Unsupported exact timing is represented as ordering/invariant assertions rather than invented frame numbers.


R0 execution boundary: inline, static/contract only, no subagents, no emulator/ADB, no network, no server, no V8, no MapChip or Renderer changes, and no living-core implementation.
