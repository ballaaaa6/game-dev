# MapChip OPT Audit

Status: `PASS_RAW_ONLY_DIRECT_MAPCHIP_ASSETS`

The direct MapChip source package was audited before any tile composition gate. The 11 direct rendered selectors used by the native room-floor fixture have no same-stem `.opt` member and no direct logical companion in the read-only source ZIP. The native path therefore remains raw image loading for these assets.

## Direct rendered selectors

| Selector | Source asset | OPT status |
| ---: | --- | --- |
| 10 | `ground_00.png` | no same-stem OPT; raw source |
| 11 | `turf_00.png` | no same-stem OPT; raw source |
| 12 | `turf_01.png` | no same-stem OPT; raw source |
| 13 | `road_00.png` | no same-stem OPT; raw source |
| 14 | `road_01.png` | no same-stem OPT; raw source |
| 15 | `road_02.png` | no same-stem OPT; raw source |
| 85 | `floor_05.png` pixels | no same-stem OPT; raw source candidate |
| 105 | `turf_02.png` | no same-stem OPT; raw source |
| 154 | `road_edge_00.png` | no same-stem OPT; raw source |
| 155 | `road_edge_01.png` | no same-stem OPT; raw source |
| 156 | `road_03.png` | no same-stem OPT; raw source |

The available `optimize.inf` records belong to furniture/object-sized chip families such as chairs, doors, mats, and trees. They are not direct MapChip logical companions and were not applied to MapChip tiles.

## Floor alias policy

Selector/data `85/floor_09.png` is retained as a metadata-only alias required by the room-floor contract. Rendering uses the source-backed `floor_05.png` pixels without relabeling their provenance. The alias is recorded in `mapchip-opt-audit.json` as `METADATA_ONLY_ALIAS`; it is not promoted as a discovered OPT reconstruction.

## Evidence and decision

`knowledge/fixtures/accepted/visual-port/mapchip-forensic/mapchip-opt-audit.json` records the source references, hashes, absent OPT members, absent logical companions, and the metadata alias. No logical crop, offset, or anchor was invented from a screenshot or from an unrelated furniture OPT file.
