# `Staff.OnArriveGoal` Dispatch

Status: `CLOSED_11_WAY_NATIVE_DISPATCH`

The native method at `0x12D8420` reads `moveMode_` at offset `0xA8`, subtracts one, rejects unsigned keys above ten, and dispatches through the 16-bit table at rodata `0x636684` with base `0x12D84A8`. All move modes 1 through 11 are decoded and recorded with their native target RVAs and side effects.

Evidence: [`on-arrive-goal-jump-table.json`](../../../knowledge/fixtures/accepted/living-core-closure/on-arrive-goal-jump-table.json), [`on-arrive-goal-dispatch-contract.json`](../../../knowledge/fixtures/accepted/living-core-closure/on-arrive-goal-dispatch-contract.json ).
