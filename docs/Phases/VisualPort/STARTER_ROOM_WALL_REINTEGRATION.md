# Starter-room wall and corner reintegration

Status: `PASS` at RI.3.

## Source-backed wall set

Stage 2 contains 46 graphics commands across 31 traces. The door is excluded from the isolated wall layer. The wall set is the native frame schedule:

- horizontal frame 0: `[1,1]` through `[8,1]`;
- vertical frame 1: `[8,1]`, `[8,2]`, `[8,3]`, `[8,5]`, `[8,6]`, `[8,7]`, `[8,8]`;
- the raw type-5 door cell `[8,4]` remains a separate Stage 3 bridge;
- MapChip extension-floor traces remain in their native `map-extension-floor` pass;
- the approved foreground wall transition remains in `object-chip-late`.

The wall-plus-door cell path contains 15 cells; the isolated wall set contains 14 and resolves to one connected component. Corner fixtures are source/native-proven, including the shared upper-right intersection, door-wall bridge, foreground transition/end, and extension overlaps.

## Coordinate bridge

The normalized preview uses a 360-pixel object/Staff base delta from the MapChip base. The source formulas remain:

- MapChip: `(x + y) * 40`, `(y - x) * 20`, with the native image-top anchor;
- ObjChip: `(x + y) * 20`, `(y - x) * 10 + 9`;
- Staff spawn: door-relative source formula, yielding world `[280,-31]` at cell `[8,4]`.

The coordinate audit records map cell `[5,5]` at `{ x: 400, y: 0 }` and door cell `[8,4]` at `{ x: 600, y: -31 }`. No screenshot-derived numeric tuning was used.

Evidence: `knowledge/fixtures/accepted/visual-port/starter-room-reintegration/stage2-walls-corners.json`, `coordinate-bridge-audit.json`, and `previews/stage2_wall_connectivity_overlay.png`.
