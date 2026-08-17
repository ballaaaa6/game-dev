# Starter-room root cause

## Primary

**V5_MAIN_DISPLAY_UNDERLAY_OMISSION** was the first broken semantic layer. The main-display stream emitted the central floor-culling subset but omitted the source-backed outer-map and floor-fill cells. This made a correct RoomData/MapChip topology appear semantically incomplete.

## Secondary

**V5_PER_PASS_ORIGIN_BRIDGE_MISSING** was then exposed by the underlay recovery. The source contract uses map base 82 and object/Staff base 442; the normalized V5 preview must preserve their 360-pixel difference.

## Ruled out

Room identity, RoomData selectors, floor selector policy, wall predicates/frame records, door raw type 5, furniture bootstrap, structural facilities, pass ordering, and the production renderer were not root causes.

Machine detail: [root-cause.json](../../../knowledge/fixtures/accepted/visual-port/starter-room-correction/root-cause.json), [origin-coordinate-audit.json](../../../knowledge/fixtures/accepted/visual-port/starter-room-correction/origin-coordinate-audit.json).
