# R0 Visual, Product, and Save Boundary

The authoritative machine contracts are:

- `visual-projection-boundary.json`
- `product-policy-boundary.json`
- `save-boundary-contract.json`

Behavior owns state, movement, targets, ownership/reservation, HP, and timers. Visual code consumes a projection and cannot mutate living state. Product policy is separate and explicitly pending for backend task behavior. The save contract classifies source-backed Staff fields as `ORIGINAL_SAVED`, `ORIGINAL_TRANSIENT`, `DERIVED`, `PRODUCT_ONLY`, or `UNKNOWN_SOURCE_LIMITED`; it does not implement serialization.

V8, MapChip, and Renderer semantics remain frozen.


R0 execution boundary: inline, static/contract only, no subagents, no emulator/ADB, no network, no server, no V8, no MapChip or Renderer changes, and no living-core implementation.
