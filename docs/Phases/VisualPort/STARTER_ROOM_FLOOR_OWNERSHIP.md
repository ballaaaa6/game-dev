# Starter-room floor ownership

Status: `PASS` at RI.2.

## Decision

The 28 `room:0` interior floor cells are already present in the accepted 14x14 MapChip foundation. MapChip owns the raw cells, selector identity, projection, and direct-image anchor. `RoomData.floorImgId_` remains the scalar metadata owner, with the documented compatibility alias from raw floor ID 5 to selector/data 85 and `floor_05.png` pixels.

No second floor plane was added. Stage 1 therefore adds zero commands and its MapChip-plus-room-floor image is byte-identical to Stage 0.

## Evidence

- MapChip topology: 196 cells, 81 nonempty, 115 empty sentinels.
- Room-floor cells: 28.
- Stage 1 floor-only commands: 28.
- Stage 1 MapChip-plus-floor pixel SHA-256: `3ea05bd9edcc5168a14ee1b0e79256e460072be75c018f11f2009d01c215d293`.
- Duplicate floor plane: `false`.

The machine-readable ownership decision is `knowledge/fixtures/accepted/visual-port/starter-room-reintegration/stage1-room-floor.json`. The source audit is `knowledge/fixtures/accepted/visual-port/mapchip-forensic/outer-vs-room-floor-ownership.json`.
