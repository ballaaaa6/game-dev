# Starter-room Staff reintegration

Status: `PASS` at RI.7.

The unchanged V6 static Staff fixture contributes three actors for StaffData IDs 0, 1, and 2. Every actor uses `wait`, direction `right`, frame `0`, alpha `255`, the existing `avatar-primary` pass, and the source-backed human selectors 86, 87, and 88. All three share the source placement cell `[8,4]`, world `{ x: 280, y: -31 }`, and screen `{ x: 640, y: -31 }`.

The Staff-only isolation contains three commands and three traces. The complete Room+Staff stream contains 142 commands and 127 traces. The final Room+Staff render repeats deterministically with pixel SHA-256 `c3d82b29a78b827e682b623c94789e34701bd4cfa0369a14ea81fcf2fe2a30b6`.

No Staff semantics were changed. The source-backed occlusion ordering remains `object-chip-wall < Staff avatar-primary < object-chip-late < map-floor`.

Evidence: `knowledge/fixtures/accepted/visual-port/starter-room-reintegration/stage6-staff.json`, `coordinate-bridge-audit.json`, and `previews/stage6_staff_only.png` / `previews/stage6_complete_room_with_staff.png`.
