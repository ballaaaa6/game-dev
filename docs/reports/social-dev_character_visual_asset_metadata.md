# Social Dev character visual asset metadata

Track H separates the complete human StaffData visual package from partial HelperData visuals and catalog-only Avatar/Event families.

## Identity

- Catalog hash: `8cadc7b5c2128ee013e89de55e2600ba0d55ce7d1f31b50b218a53bc285c0df0`
- Contract hash: `8ab68c8cd84e1f845e2b683f24abef6970fb720bd93957567ab7377df0481ebf`

## Counts

| Scope | Count |
|---|---:|
| StaffData records | 141 |
| Staff image bindings | 141 |
| Human image assets | 105 |
| Human SEB animations | 35 |
| HelperData records | 19 |
| Avatar body asset rows | 284 |
| Avatar head asset rows | 509 |
| Event visual asset rows | 72 |

## Helper status

- `img_`: `{'absent_by_sentinel': 1, 'deferred': 11, 'resolved': 7}`.
- `bigImg_`: `{'absent_by_sentinel': 1, 'not_promoted': 18}`.
- The 11 helper scope-deferred image references and the unpromoted big-image package remain explicit.

## Boundary

- Human StaffData is ready for lazy image/frame lookup and capability-driven action selection.
- HelperData is metadata-ready but not fully pixel-ready.
- Avatar body/head and event visuals are cataloged and classified, but no runtime actor composition is inferred.

```powershell
python -B tools/social-dev/build_character_visual_asset_metadata.py
python -B tools/social-dev/test_character_visual_asset_metadata.py
```
