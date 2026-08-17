# Social Dev asset usage, lifecycle, placement, and provenance

AM-5 gives every indexed asset an explicit usage status, lifecycle status, placement status, runtime-query status, and source-provenance boundary.

## Identity

- Matrix hash: `bea8a2372257bbe52122ca74f3e852ab7bc498acb31bb79641395caca492cf9a`
- Contract hash: `96010e0d2c701079962e9a6bc32a3a6a5b0e3719e29b868b267e0ea67fe428bc`

## Counts

| Dimension | Count |
|---|---:|
| Assets | 3,542 |
| Usage edges | 3,495 |
| Lifecycle edges | 43 |
| Families | 27 |
| Non-actor/UI/event/text families | 21 |

## Runtime query statuses

| Status | Count |
|---|---:|
| `evidence_catalog_only` | 1,527 |
| `queryable_by_native_selector_and_asset_id` | 1,833 |
| `queryable_by_runtime_manifest_and_asset_id` | 182 |

## Source/provenance boundary

- Asset ZIP rows: `{'zip_exact': 3542}`.
- APK source statuses: `{'apk_entry_missing': 34, 'apk_entry_present': 3508}`.
- The 34 Unity TextAsset/APK-missing rows remain explicit provenance gaps; they are not deleted or silently promoted.
- UI, effect, event, text, system, platform, config, and data families are cataloged but require screen/event consumer contracts before runtime promotion.

```powershell
python -B tools/social-dev/build_asset_usage_lifecycle_placement.py
python -B tools/social-dev/test_asset_usage_lifecycle_placement.py
```
