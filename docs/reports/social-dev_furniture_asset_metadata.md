# Social Dev furniture and world asset metadata

Track W binds all 103 FurnitureData records to selector identities, composition/geometry references, and explicit room-placement status. Raw ObjChip topology remains separate from FurnitureData identity.

## Identity

- Catalog hash: `2cd803df2a5abeba810118900d78c1734dc2ab7b27647a6a0cec3b4984db0f38`
- Contract hash: `8b1e6926bb61e4420aa3cd2ac6f0995b75b9f3beaaf9c04988ab4bc4364fa73d`

## Counts

| Dimension | Count |
|---|---:|
| FurnitureData records | 103 |
| World/chip asset rows | 447 |
| Rooms | 18 |
| Rooms with explicit native furniture bindings | 1 |
| Explicit native binding instances | 6 |

## Selector statuses

| Field/status | Count |
|---|---:|
| `img_:absent_by_sentinel` | 7 |
| `img_:resolved` | 96 |
| `seb_:resolved` | 103 |
| `subSeb_:absent_by_sentinel` | 80 |
| `subSeb_:resolved` | 23 |

## Placement boundary

- Room:0 retains the explicit native FurnitureData bindings and six initial instances.
- Rooms 1–17 retain raw 10x10 ObjChip cells and wall/door composition but have no inferred FurnitureData bindings.
- A furniture lookup is repeatable by `data:furniture:<id>` plus selector field keys; placement is repeatable only where a native binding record exists.

```powershell
python -B tools/social-dev/build_furniture_asset_metadata.py
python -B tools/social-dev/test_furniture_asset_metadata.py
```
