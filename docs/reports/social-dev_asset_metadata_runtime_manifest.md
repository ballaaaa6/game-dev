# Social Dev runtime asset metadata manifest

This is the runtime query boundary for explicit asset metadata. It is lazy: the browser loads the native catalog and this small runtime-relevant manifest, then resolves by stable IDs without importing source archives or C#.

## Identity

- Manifest hash: `05e4d724451d009c2220d6dc8d9e1ee0451c0fbbdc9ad497aadf0e3a75db8fd9`
- Contract hash: `4d423aece5c8195f67275e7815d9433637701616eb7b56a00d532d450fdf8221`

## Counts

| Dimension | Count |
|---|---:|
| Runtime asset metadata rows | 186 |
| Native catalog assets | 3,542 |
| Native selectors | 3,192 |
| Family manifests | 27 |
| Furniture records | 103 |
| Staff records | 141 |
| Helper records | 19 |
| Rooms | 18 |

## Query rules

- Asset: `asset_id` → lazy runtime metadata row.
- Selector: `(resource_scope, selector_kind, selector_id)` → native selector → target asset ID.
- Furniture: `data:furniture:<id>` → selector fields → target assets/composition.
- Character: `staff:<id>` or `helper:<id>` → existing character resolver and capability contract.
- Missing/unresolved records return explicit status; no filename or selector guessing is permitted.

```powershell
python -B tools/social-dev/build_asset_metadata_runtime_manifest.py
python -B tools/social-dev/test_asset_metadata_runtime_manifest.py
```
