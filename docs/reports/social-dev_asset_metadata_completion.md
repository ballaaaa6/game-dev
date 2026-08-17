# Social Dev asset metadata completion audit

This is the final audit for the asset-metadata workstream. `pass` means the indexed catalog is deterministic and every known limit is explicit; it does not mean that every catalog row is approved for visual runtime promotion.

## Result

- Gate status: `pass`
- Semantic status: `asset_metadata_catalog_complete_with_runtime_subset_and_explicit_boundaries`
- Gate hash: `ed5d2d858ef0bed93f2c7ffa8887f1feb64a4f3c75ea8ba518404844f36dcd94`
- Runtime contract hash: `6d137759c646e3847881ce957330e968d22ea60dce1553e30c519628847e9934`

## Readiness split

| Surface | Result |
|---|---|
| Catalog metadata | complete_for_all_3542_indexed_rows_with_explicit_status_or_boundary |
| Native identity graph | ready_for_3693_data_rows_and_3192_selector_records |
| Runtime query surface | ready_for_186_explicit_runtime_asset_rows_and_native_catalog_lookup |
| Full visual runtime promotion | not_ready_and_not_claimed_for_catalog_only_rows |

## Counts

| Dimension | Count |
|---|---:|
| Indexed assets | 3,542 |
| Native data records | 3,693 |
| Native selectors | 3,192 |
| Runtime-query asset rows | 186 |
| Catalog-only assets | 3,231 |
| Runtime geometry gaps | 0 |

## Explicit boundaries

- 1 lineup_layout/bg.seb selector has unresolved target identity.
- 11 helper selector-scope fields remain deferred; 1 helper image selector is an explicit -1 sentinel.
- 34 Unity TextAsset/resource rows have APK absence and unresolved nested mapping; they remain provenance-only.
- 21 non-actor families have catalog/provenance metadata but no invented screen/event consumer contract.
- 3,231 indexed assets are cataloged without a current native relation; they remain queryable evidence, not automatic runtime assets.
- Full visual runtime promotion remains limited to the explicit 186-row runtime manifest.

## Verification

The deterministic Python package tests, TypeScript typecheck, Vitest suite, production build, and runtime lookup tests are the handoff gates. The completion gate also scans runtime source imports for archive, APK, C#, and knowledge-root imports.

```powershell
python -B tools/social-dev/build_asset_metadata_completion_gate.py
python -B tools/social-dev/test_asset_metadata_completion_gate.py
```
