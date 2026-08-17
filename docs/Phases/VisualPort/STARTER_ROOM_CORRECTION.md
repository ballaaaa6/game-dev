# Starter-room semantic correction

Status: **PASS_STATIC_STARTER_ROOM_CORRECTION**

V8 started: **NO**. Execution was inline-only and static-only; no subagents, emulator, ADB, live app, server, network, or live browser were used. The production renderer is unchanged.

## Result

The first broken semantic layer was main-display pass assembly: the source-backed floor0 14x14 topology existed, but only the central native floor-culling subset reached the V5 command stream. A second coordinate-bridge defect kept the map and object/Staff lattices on one origin. The correction adds the 81-cell source-backed underlay before object composition and applies the proven 360-pixel normalized object/actor delta.

## Evidence

- structural: knowledge/fixtures/accepted/visual-port/starter-room-correction/previews/starter_room_structural_corrected.png (PNG SHA-256 b55d701ba74bd6212701a6623d5de667d824c00c604bfebfc2d416f7d5fd447a)
- staff: knowledge/fixtures/accepted/visual-port/starter-room-correction/previews/starter_room_with_staff_corrected.png (PNG SHA-256 f5c2db1052ee55b6256208b164107bc123f58634f533ce621f46871acb60c1cd)
- floor: knowledge/fixtures/accepted/visual-port/starter-room-correction/previews/starter_room_floor_only.png (PNG SHA-256 3969af8ebc8ac20b0bc4d817494bfc9853e44de31551626a605d57d6f5628697)
- wallsCorners: knowledge/fixtures/accepted/visual-port/starter-room-correction/previews/starter_room_walls_corners_only.png (PNG SHA-256 74a0e665ff760cddfd28f65943db6a85619e3596d083f5324c4e3f66ed1e6619)
- outerMap: knowledge/fixtures/accepted/visual-port/starter-room-correction/previews/starter_room_outer_map_only.png (PNG SHA-256 3eb041fd6016a5082ba8fdfb4b4c1b249c323573ee761975bf0d348dddc977cb)
- furnitureStructural: knowledge/fixtures/accepted/visual-port/starter-room-correction/previews/starter_room_furniture_structural_only.png (PNG SHA-256 ea8ada05b6820046ad8fcb8e5770aefeeedaa5b1b3241242a55837a0bd02abc6)
- before/after contact sheet: knowledge/fixtures/accepted/visual-port/starter-room-correction/previews/starter_room_before_after_contact_sheet.png (PNG SHA-256 276c954eb19b8db84fc281bd61bb14cdae1b2eb7609af7ceca1b4af495cd1073)

Machine evidence is under knowledge/fixtures/accepted/visual-port/starter-room-correction/. The corrected room uses the source-backed 980x600 viewport contract. Repeat renders are pixel-identical.

## Gates

The corrected command stream is 139 commands / 124 traces / 788 events; the integrated room+Staff stream is 142 / 127 / 791. The 14x14 floor population is 196 cells with 81 non-empty cells; wall and door cells form one connected path; the selector 5 -> 85 compatibility policy remains separate from topology.

See [STARTER_ROOM_ROOT_CAUSE.md](STARTER_ROOM_ROOT_CAUSE.md), [STARTER_ROOM_TOPOLOGY.md](STARTER_ROOM_TOPOLOGY.md), [STARTER_ROOM_WALL_CONNECTIVITY.md](STARTER_ROOM_WALL_CONNECTIVITY.md), [STARTER_ROOM_OUTER_MAP.md](STARTER_ROOM_OUTER_MAP.md), and [STARTER_ROOM_BEFORE_AFTER.md](STARTER_ROOM_BEFORE_AFTER.md).
