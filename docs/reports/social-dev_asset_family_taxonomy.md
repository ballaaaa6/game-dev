# Social Dev asset-family taxonomy

AM-2 assigns every indexed asset a structural family, extension-based subfamily, lineage, and explicit runtime boundary. These labels make lookup and filtering deterministic without claiming that pack membership alone proves a gameplay call.

## Identity

- Taxonomy content hash: `5f83e04cbd356b923cfcf4064f59a4f1b41baa40fe61528989ea5712bdd8fd08`
- Coverage content hash: `9d47764ac1964516ceaef3329d178fc284e457d36cc5ccccfb2d7d2e2fedf377`
- Contract content hash: `9b77831f8d469476b51c85705cbbbc32f12898e9c3429ef86a4a0ede38f92960`

## Counts

| Dimension | Count |
|---|---:|
| Assets classified | 3,542 |
| Families | 27 |
| Structural subfamilies | 78 |

## Families

| Family | Category | Rows | Runtime-referenced | Subfamilies |
|---|---|---:|---:|---:|
| `character.avatar.body` | character | 284 | 0 | 4 |
| `character.avatar.head` | character | 509 | 0 | 3 |
| `character.helper` | character | 57 | 0 | 3 |
| `character.staff.human` | character | 180 | 140 | 3 |
| `config.connection` | config | 2 | 0 | 1 |
| `data.table` | data | 91 | 0 | 2 |
| `data.unity_textasset` | data | 34 | 0 | 3 |
| `effect.visual` | effect | 49 | 0 | 4 |
| `event.visual` | event | 72 | 0 | 3 |
| `platform.android` | platform | 78 | 0 | 1 |
| `system.game` | system | 5 | 0 | 1 |
| `text.localization` | text | 3 | 0 | 1 |
| `ui.banner` | ui | 10 | 0 | 2 |
| `ui.billing` | ui | 32 | 0 | 4 |
| `ui.common` | ui | 972 | 0 | 4 |
| `ui.develop` | ui | 155 | 0 | 3 |
| `ui.lineup` | ui | 78 | 0 | 4 |
| `ui.lineup.layout` | ui | 6 | 0 | 3 |
| `ui.load` | ui | 22 | 0 | 3 |
| `ui.mail` | ui | 34 | 0 | 3 |
| `ui.meeting` | ui | 39 | 0 | 3 |
| `ui.recruit` | ui | 6 | 0 | 3 |
| `ui.social.friend` | ui | 48 | 0 | 4 |
| `ui.title` | ui | 17 | 0 | 3 |
| `ui.window` | ui | 32 | 0 | 3 |
| `world.chip` | world | 447 | 42 | 4 |
| `world.gameplay` | world | 280 | 0 | 3 |

## Lineage

| Lineage | Rows |
|---|---:|
| `derived_catalog` | 36 |
| `derived_preview` | 240 |
| `derived_reconstruction` | 328 |
| `original_native` | 2,826 |
| `platform_resource` | 78 |
| `retained_payload` | 34 |

## Boundary

- Family/subfamily/lineage classification is closed for all indexed rows.
- Selector meaning, consumer call timing, frame/layer geometry, placement, and lifecycle remain separate gates.
- The taxonomy does not turn the 3,231 currently unreferenced rows into deletions or runtime assets.

```powershell
python -B tools/social-dev/build_asset_family_taxonomy.py
python -B tools/social-dev/test_asset_family_taxonomy.py
```
