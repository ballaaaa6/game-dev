# R0 Movement, State, Tick, and RNG Contract

The authoritative machine contracts are:

- `movement-route-contract.json`
- `staff-state-machine-contract.json`
- `tick-order-contract-v2.json`
- `rng-autonomy-contract.json`

Movement is cardinal 4-neighbor only. Route head consumption and the full native `OnArriveGoal` table for move modes `1..11` are explicit. The tick contract puts recovery before the low-HP guard, then state dispatch/handler, route/arrival interaction, handler-owned timers, cleanup, and only then visual projection.

RNG uses an injectable replayable PRNG for tests, but preserves native ranges and thresholds. `AppData.Random(n)` is `[0,n)`; the two-argument form is inclusive. Exact UpdateWork cadence details remain `SOURCE_LIMITED` and are not guessed.


R0 execution boundary: inline, static/contract only, no subagents, no emulator/ADB, no network, no server, no V8, no MapChip or Renderer changes, and no living-core implementation.
