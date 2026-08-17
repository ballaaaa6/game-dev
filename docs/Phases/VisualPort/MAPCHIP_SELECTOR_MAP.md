# MapChip Selector Map

Status: `PASS`

The selector map is derived from the native 14x14 MapChip topology and the approved numeric mapping contract. It is not derived from screenshots. The fixture retains all 196 cells, including 115 empty sentinels and 81 nonempty source-backed cells.

| Raw index | Runtime selector | Asset or policy |
| ---: | ---: | --- |
| 0 | -1 | empty sentinel; draw nothing |
| 1 | 85 | floor sentinel; retain `floor_09.png` metadata identity and render `floor_05.png` pixels |
| 2 | 10 | `ground_00.png` |
| 3 | 11 | `turf_00.png` |
| 4 | 12 | `turf_01.png` |
| 5 | 13 | `road_00.png` |
| 6 | 14 | `road_01.png` |
| 7 | 15 | `road_02.png` |
| 8 | 105 | `turf_02.png` |
| 9 | 154 | `road_edge_00.png` |
| 10 | 155 | `road_edge_01.png` |
| 11 | 156 | `road_03.png` |

The ownership audit records 53 outer-map cells and 28 room-floor cells. MapChip owns the 14x14 raw cells, selector identity, projection, and direct-image draw anchor. ObjChip owns the separate 10x10 object lattice and wall/object passes; Room owns topology selection and pass orchestration; Staff is outside this gate.

Evidence: `knowledge/fixtures/accepted/visual-port/mapchip-forensic/mapchip-selector-inventory.json`, `mapchip-selector-map.json`, and `outer-vs-room-floor-ownership.json`.
