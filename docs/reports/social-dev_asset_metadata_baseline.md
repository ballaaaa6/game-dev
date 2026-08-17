# Social Dev asset metadata baseline

This is the frozen AM-0 evidence baseline for the asset-metadata completion program. It is a reproducible snapshot, not a claim that every asset is runtime-ready.

## Baseline identity

- Baseline content hash: `2ce296a4c47b92e1667cda63d719a433573dc9871172d1978bcd5537cd52d7e7`
- Input manifest hash: `4ea8bde72ca65bb54821b8527dcf95c025428084ad9a9bbbd95b1801c9362105`
- Indexed asset rows: **3,542** (3,542 unique paths)
- Native catalog: **3,542 assets**, **3,192 selectors**, **3,693 data rows**

## Current inventory

| Dimension | Count |
|---|---:|
| Original packed assets | 2,826 |
| Reconstructed/derived image rows |  716 |
| Named packs | 25 |
| Ungrouped rows | 112 |
| Rows with SHA-256 | 3,542 |
| Rows with dimensions | 2,297 |
| Native data-selector relations | 523 |
| Selector/asset/companion relations | 4,596 |

### Pack counts

| Pack | Rows |
|---|---:|
| `__ungrouped__` | 112 |
| `avatar_body` | 284 |
| `avatar_head` | 509 |
| `banner` | 10 |
| `billing` | 32 |
| `chip` | 447 |
| `com` | 972 |
| `connect` | 2 |
| `develop` | 155 |
| `effect` | 49 |
| `event` | 72 |
| `friend` | 48 |
| `game` | 280 |
| `helper` | 57 |
| `human` | 180 |
| `language` | 3 |
| `lineup` | 78 |
| `lineup_layout` | 6 |
| `load` | 22 |
| `mail` | 34 |
| `meeting` | 39 |
| `recruit` | 6 |
| `system` | 5 |
| `title` | 17 |
| `window` | 32 |
| `xls` | 91 |

## Resolution and readiness snapshot

| Area | Current evidence |
|---|---|
| Selector resolution | {'resolved': 3191, 'unresolved_target': 1} |
| Data-row semantic status | {'not_mapped': 3412, 'verified_reader_order': 281} |
| Staff metadata | 141 records; 105 unique human image selectors |
| Helpers | 19 records; image resolution is partial |
| Rooms | 18 rooms; 1,800 ObjChip cells |
| Furniture metadata | 3,693 total data rows in catalog; FurnitureData is a verified reader-order slice inside that catalog |
| Runtime display subset | 34 promoted binary assets across 18 approved entries |

## Known exceptions carried into AM-1

- `selector.unresolved.lineup_layout.bg_seb` — **open**: lineup_layout/seb.inf contains raw bg.seb without a resolved selector id/file target.
- `room.room0.floor_alias` — **explicit_runtime_alias**: room:0 raw floorImgId_=5 resolves through FLOOR_IMAGE_ID_ARRAY to selector 23/floor_05.png; the runtime default alias for metadata remains separate.
- `native_catalog.data_records.not_mapped` — **coverage_gap**: The native catalog retains all data rows, but rows outside the verified reader-order slices remain source-backed and not_mapped until field semantics are classified.
- `room.rooms_without_native_furniture_bindings` — **composition_gap**: Raw ObjChip topology is available for all rooms; explicit native FurnitureData instance bindings are currently closed only for the existing initial-object slice.
- `character.helper_image_resolution` — **partial**: Helper metadata is complete, while helper image usage is resolved for 7 records, deferred for 11, and absent for 1.
- `asset.runtime_promotion_scope` — **partial**: The full 3,542-row index is cataloged; runtime-approved display and room slices are smaller and must not be treated as full-family closure.

## Rebuild and verification

The builder hashes every input by workspace-relative path and computes a stable content hash. If an upstream catalog changes, the baseline test fails until the snapshot is intentionally regenerated.

```powershell
python -B tools/social-dev/build_asset_metadata_baseline.py
python -B tools/social-dev/test_asset_metadata_baseline.py
```

The ten pre-existing targeted contract tests are recorded in the JSON baseline and remain the minimum AM-0 verification set.
