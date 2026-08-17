# Social Dev asset composition and geometry catalogs

AM-4 records runtime-relevant SEB/OPT composition, native destination offsets, frame/layer bounds, physical raster dimensions, and explicit pending statuses for catalog-only families.

## Identity

- Composition hash: `a4cda2ba4c8e4e8be03802563efec975f4abb12ee05eb7b4ac5aa0df8428619f`
- Geometry hash: `5d1c2103a123681a88b8e41a7315f35762e6bd99802d53257bc52d441535fb6b`
- Contract hash: `9950fb9c070fcd952ee08ecd0a8554b7649f5708c26a1d05f54cbe3e0516aa85`

## Counts

| Dimension | Count |
|---|---:|
| Composition entries | 47 |
| Character SEB compositions | 35 |
| Furniture object compositions | 4 |
| Native initial object compositions | 4 |
| Logical OPT reconstructions | 4 |
| Geometry rows | 3,546 |
| Runtime-relevant geometry rows | 186 |
| Runtime geometry gaps | 0 |

## Geometry statuses

| Status | Count |
|---|---:|
| `composition_and_geometry_closed` | 55 |
| `derived_runtime_geometry_closed` | 4 |
| `manifest_only_not_bound_to_active_composition` | 2 |
| `not_applicable_nonvisual_or_payload` | 130 |
| `physical_dimensions_closed` | 2,287 |
| `source_geometry_not_closed` | 1,068 |

## Boundary

- Runtime-relevant composition and geometry gaps are closed for the current display, room, and full human character contracts.
- Catalog-only SEB/OPT families remain explicit rather than receiving guessed frames or anchors.
- Native destination offsets are preserved as the anchor policy; no center/pivot inference is applied.

```powershell
python -B tools/social-dev/build_asset_composition_geometry.py
python -B tools/social-dev/test_asset_composition_geometry.py
```
