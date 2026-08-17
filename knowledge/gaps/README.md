# Explicit gaps

`k3-gap-queue.json` is the active, read-only queue of unresolved source-limited or candidate claims. It contains three preserved entries:

- `K3-GAP-FLOOR-DIRECT-SELECTOR` — `SOURCE_LIMITED`, `selector:floor:5`.
- `K3-GAP-FURNITURE-VISUAL` — `SOURCE_LIMITED`, `data:FurnitureData:26`.
- `K3-GAP-CANDIDATE-EDGES` — `CANDIDATE`, `semantic-edge-candidates`.

These gaps remain explicit and are not promoted into implementation. K3/V8 work has not started.
