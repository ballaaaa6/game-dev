# V5 RoomData and Map Topology

`RoomData` is reconstructed from the existing runtime room contract and native scene assembly contract. The 18 records retain their English names, native floor/wall/door numeric fields, raw 10x10 object grids, direction grids, and source-row hashes.

`Room.floor_` is a different field from `RoomData.floorImgId_`. Native evidence selects `MAPCHIP_ARRAY[0]` for floor zero (14x14) and `MAPCHIP_ARRAY[1]` for nonzero floors (4x4). V5 rejects unsupported floor/context/dimension combinations instead of resizing or inventing a map.

The floor image field is resolved separately: room:0 raw value `5` maps to native floor-table selector `23` and the existing runtime compatibility alias selector `85`, rendered with `floor_05.png` pixels. That alias remains labeled `COMPATIBILITY-POLICY`; it is not presented as the original native runtime lookup.

See `knowledge/fixtures/accepted/visual-port/v5/roomdata-topology.json` and `room-map-topology-contract.json` for the complete matrix and rejection policy.
