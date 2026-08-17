# Starter-room furniture reintegration

Status: `PASS` at RI.5 and RI.6.

## Structural facilities

The two structural/facility anchors are explicit native type-4 fixtures at `[4,2]` and `[7,2]`. They remain in `object-chip-primary`, use primary SEB 11, and are not inferred from a raw type. The isolated structural layer contains two commands.

## FurnitureData bootstrap

Six explicit native bindings are present:

- `furniture:3` at `[2,4]`, `[3,4]`, `[6,4]`;
- `furniture:12` at `[8,5]`;
- `furniture:26` at `[8,6]`;
- `furniture:56` at `[2,7]`.

The furniture-only layer contains nine commands because the `furniture:3` desk/computer plus chair subcomposition is retained as its native compound. All six instances use the strict native initial-binding proof, remain in `object-chip-primary`, and avoid ObjChip raw-type inference.

Evidence: `knowledge/fixtures/accepted/visual-port/starter-room-reintegration/stage4-structural.json`, `stage5-furniture.json`, `previews/stage4_structural_only.png`, and `previews/stage5_furniture_only.png`.
