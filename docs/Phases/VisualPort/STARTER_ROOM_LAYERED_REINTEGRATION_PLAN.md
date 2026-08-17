# Starter Room Layered Reintegration Plan

Execution is inline-only and static-only. The verified 14x14 MapChip foundation is frozen as the only environment base, and each later layer must pass before the next layer is materialized.

| Stage | Owner | Evidence sources | Expected command family / pass | Test image |
| --- | --- | --- | --- | --- |
| RI.1 / Stage 0 | MapChip foundation | MapChip forensic ledger/results, V4 MapChip contracts, V5 main-display map underlay | 81 nonempty MapChip direct-image commands; foundation underlay pass | `stage0_mapchip_only.png` |
| RI.2 / Stage 1 | Room floor ownership | `outer-vs-room-floor-ownership.json`, Room.Draw flow, `RoomData.floorImgId_`, floor alias contract | No additional commands; Stage 0 already owns the 28 room-floor cells | `stage1_mapchip_plus_room_floor.png`, `stage1_floor_only.png` |
| RI.3 / Stage 2 | ObjChip wall / wall frame / room corner | V4 ObjChip contracts, V5 topology/pass schedule, native wall assembly, coordinate audit | Wall SEB/image layers in rear and late wall passes; no door/furniture/Staff | `stage2_walls_only.png`, `stage2_environment_plus_walls.png`, `stage2_wall_connectivity_overlay.png` |
| RI.4 / Stage 3 | Door | Room:0 door fixture, raw type 5, door SEB/image contract | Door SEB/image in the rear wall pass at `[8,4]` | `stage3_door_only.png`, `stage3_environment_walls_door.png` |
| RI.5 / Stage 4 | Structural / facility objects | Room:0 structural facility contract and V5 furniture orchestration | Explicit type-4 facility bindings in `object-chip-primary` | `stage4_structural_only.png`, `stage4_environment_plus_structural.png` |
| RI.6 / Stage 5 | Furniture bootstrap | V4 furniture binding, V5 room:0 scene/bootstrap evidence | Six explicit FurnitureData instances in `object-chip-primary` | `stage5_furniture_only.png`, `stage5_room_without_staff.png` |
| RI.7 / Stage 6 | Staff integration | V6 Staff contracts, actor bootstrap, room ordering | Three V6 wait/right/frame-0 actors in `avatar-primary` | `stage6_staff_only.png`, `stage6_complete_room_with_staff.png` |
| RI.8 / Stage 7 | Complete starter-room scene | All prior stage ledgers and deterministic V7 raster | Complete structural and Room+Staff streams; two identical renders each | `starter_room_final_structural.png`, `starter_room_final_with_staff.png` |

The final target is the source-backed first-launch / starter main-display static environment: the `AppData.NewGame` room:0 bootstrap with the native 14x14 MapChip, explicit room:0 structural/furniture bindings, and the V6 static Staff fixture, excluding UI/tutorial overlays. Historical screenshots are secondary sanity context only and supply no geometry, selector, or offset values.

All generated evidence belongs under `knowledge/fixtures/accepted/visual-port/starter-room-reintegration/`; the production renderer and V8 remain unchanged.
