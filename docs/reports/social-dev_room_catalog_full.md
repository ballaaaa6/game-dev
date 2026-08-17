# Social Dev complete RoomData catalog

All RoomData rows are cataloged from the native reader order. The 10x10 ObjChip grid is kept separate from the 14x14 MapChip topology.

## Summary

- Rooms: `18` (`room:0` through `room:17`)
- ObjChip cells: `1800`
- MapChip floor-image links: `18/18`
- Native FLOOR_IMAGE_ID_ARRAY entries: `11`
- Explicit selector gaps: `0`

## Room index

| Room | Name | ObjChip | Desk slots | Small slots | Big slots | Door cells | MapChip status |
|---|---|---:|---:|---:|---:|---|---|
| `room:0` | Floor A | 10×10 | 6 | 8 | 18 | 1 | `linked_shared_native_contract` |
| `room:1` | Floor B | 10×10 | 6 | 13 | 9 | 1 | `linked_shared_native_contract` |
| `room:2` | Floor C | 10×10 | 8 | 8 | 18 | 1 | `linked_shared_native_contract` |
| `room:3` | Floor D | 10×10 | 8 | 13 | 18 | 1 | `linked_shared_native_contract` |
| `room:4` | Floor E | 10×10 | 10 | 9 | 18 | 1 | `linked_shared_native_contract` |
| `room:5` | Floor F | 10×10 | 10 | 17 | 9 | 1 | `linked_shared_native_contract` |
| `room:6` | Floor G | 10×10 | 10 | 6 | 27 | 1 | `linked_shared_native_contract` |
| `room:7` | Floor H | 10×10 | 12 | 15 | 18 | 1 | `linked_shared_native_contract` |
| `room:8` | Floor I | 10×10 | 12 | 30 | 0 | 1 | `linked_shared_native_contract` |
| `room:9` | Floor J | 10×10 | 12 | 3 | 36 | 1 | `linked_shared_native_contract` |
| `room:10` | Floor K | 10×10 | 12 | 15 | 18 | 1 | `linked_shared_native_contract` |
| `room:11` | Floor L | 10×10 | 12 | 30 | 0 | 1 | `linked_shared_native_contract` |
| `room:12` | Floor M | 10×10 | 12 | 3 | 36 | 1 | `linked_shared_native_contract` |
| `room:13` | Floor N | 10×10 | 12 | 15 | 18 | 1 | `linked_shared_native_contract` |
| `room:14` | Floor O | 10×10 | 12 | 30 | 0 | 1 | `linked_shared_native_contract` |
| `room:15` | Floor P | 10×10 | 12 | 3 | 36 | 1 | `linked_shared_native_contract` |
| `room:16` | Floor Q | 10×10 | 12 | 15 | 18 | 1 | `linked_shared_native_contract` |
| `room:17` | Floor R | 10×10 | 12 | 30 | 0 | 1 | `linked_shared_native_contract` |

## Resolution policy

RoomData `wallImgId_` and `doorImgId_` values are direct `chip/img.inf` selector IDs. `floorImgId_` is an index into the native `Room.FLOOR_IMAGE_ID_ARRAY`; all 18 RoomData rows now resolve that table index to a selector and source asset.

MapChip topology is not synthesized from the object grid. The shared native MapChip contract is selected by `Room.floor_`; the RoomData catalog carries the floor-image table link for every room while preserving the existing room:0 runtime alias as a separate policy.

Registry hash: `4d246aee6098ff0b70fc7ffeedfd85df08e6ebcc00dc9260b9e8faa1d60f53b4`
Catalog hash: `a840a6917af272133970c53910e3f3a937dd7a9c7863577f52fbebc4e16483e8`
