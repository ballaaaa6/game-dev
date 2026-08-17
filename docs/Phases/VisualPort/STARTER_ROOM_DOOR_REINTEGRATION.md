# Starter-room door reintegration

Status: `PASS` at RI.4.

The door is a single source-backed ObjChip wall command at cell `[8,4]`:

- raw type: `5`;
- direction: `0`;
- SEB selector: `6`;
- image selector: `7`;
- frame: `0`;
- pass: `object-chip-wall`;
- destination: `{ x: 600, y: -31 }`.

The isolated door render contains one command and one trace. Its pixel SHA-256 is `958cd535aef2a05c99ed9a61cebe593e0f7d35a51c9384c80370c9569a07d114`; its PNG SHA-256 is `b96f366643c344891cf518facd09a6b335853ebcb5d237add05dd5c34cde5465`.

The door remains the intentional wall-path bridge between the vertical wall segments. Evidence: `knowledge/fixtures/accepted/visual-port/starter-room-reintegration/stage3-door.json` and `previews/stage3_door_only.png`.
