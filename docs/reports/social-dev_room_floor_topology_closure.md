# Social Dev Room.floor_ and MapChip topology closure

## Result

The native Room floor connection is closed for the reviewed APK.

- `Room.floor_ == 0` selects `MAPCHIP_ARRAY[0]`, a 196-value 14x14 topology.
- `Room.floor_ != 0` selects `MAPCHIP_ARRAY[1]`, a 16-value 4x4 topology.
- `RoomData.floorImgId_` remains an independent `FLOOR_IMAGE_ID_ARRAY` index.
- The runtime rejects a nonzero floor request with 14x14 dimensions instead of silently borrowing ground data.
- Only the native main-display path receives the 14x14 outer MapChip scope; persistent and addition-floor paths remain 4x4 room topology only.
- A non-main request never receives a synthetic 14x14 garden/road surround when the native constructor does not provide one.

## Verified construction paths

| Path | Native constructor | Topology | Status |
|---|---|---|---|
| Main display | `Room(14,14,0,roomData_[0],false)` | `floor_0`, 14x14 | pass |
| Persistent room | `Room(4,4,0,roomData,false)` | `floor_0`, 4x4 slice | pass |
| Addition-floor preview | `Room(4,4,1,roomData3,true)` | `floor_nonzero`, 4x4 | pass |

## Explicit boundaries

- There is no native evidence in the reviewed `Room.MAPCHIP_ARRAY` for distinct topology arrays for floor values 2, 3, 4, or 5; the selector is boolean `floor != 0`.
- A full upper 14x14 map is not a native contract in this APK. Promoting the 4x4 nonzero row to 14x14 would be incorrect.
- The 18 RoomData rows are catalog keys. Their MapChip topology is selected by the Room constructor context, not by the RoomData row itself.

Catalog hash: `91d009764eb7628cd28061e0e34c4c8ca4875fa421bbbc0d7eaa20176d358a88`
Runtime contract hash: `f1477ed112767b1e123de180d288a224fc35cc5eef6ed2852a5f12f38fe33830`
