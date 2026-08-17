# Social Dev asset surface and provenance closure

Track X/A closes the metadata boundary for UI, event/effect, localization, configuration, data, system, and platform families. It records what the source package proves and refuses to invent screen/event call sites from filenames.

## Identity

- Surface package hash: `5cfe64f8dad9c6b3032493db2a5b716a2ea917a773a28920da82bb6c7e5501f9`
- Runtime contract hash: `31e52a89179153ba7e7a492a6b5beb24a210ee8ce8e3544cfef342bbbaafdd3a`

## Counts

| Dimension | Count |
|---|---:|
| Indexed assets | 3,542 |
| Structural families | 27 |
| Non-actor families with explicit boundary | 21 |
| Non-actor assets | 1,785 |
| ZIP-exact assets | 3,542 |
| APK entries present | 3,508 |
| APK entries missing | 34 |
| Exact pack round-trips | 25 |
| Unity TextAsset rows | 34 |
| Unity TextAsset rows with APK gap | 34 |
| Unresolved selector identities | 1 |

## Surface policy

| Family boundary | Rows | Runtime policy |
|---|---:|---|
| `config.connection` — support_family_cataloged_provenance_only | 2 | `provenance_only_until_runtime_consumer_contract` |
| `data.table` — support_family_cataloged_provenance_only | 91 | `provenance_only_until_runtime_consumer_contract` |
| `data.unity_textasset` — support_family_cataloged_provenance_only | 34 | `provenance_only_until_runtime_consumer_contract` |
| `effect.visual` — event_visual_cataloged_no_closed_event_consumer_contract | 49 | `catalog_only_until_event_consumer_contract` |
| `event.visual` — event_visual_cataloged_no_closed_event_consumer_contract | 72 | `catalog_only_until_event_consumer_contract` |
| `platform.android` — support_family_cataloged_provenance_only | 78 | `provenance_only_until_runtime_consumer_contract` |
| `system.game` — support_family_cataloged_provenance_only | 5 | `provenance_only_until_runtime_consumer_contract` |
| `text.localization` — localization_cataloged_no_closed_text_consumer_contract | 3 | `catalog_only_until_text_consumer_contract` |
| `ui.banner` — ui_surface_cataloged_no_closed_screen_consumer_contract | 10 | `catalog_only_until_screen_consumer_contract` |
| `ui.billing` — ui_surface_cataloged_no_closed_screen_consumer_contract | 32 | `catalog_only_until_screen_consumer_contract` |
| `ui.common` — ui_surface_cataloged_no_closed_screen_consumer_contract | 972 | `catalog_only_until_screen_consumer_contract` |
| `ui.develop` — ui_surface_cataloged_no_closed_screen_consumer_contract | 155 | `catalog_only_until_screen_consumer_contract` |
| `ui.lineup` — ui_surface_cataloged_no_closed_screen_consumer_contract | 78 | `catalog_only_until_screen_consumer_contract` |
| `ui.lineup.layout` — ui_surface_cataloged_no_closed_screen_consumer_contract | 6 | `catalog_only_until_screen_consumer_contract` |
| `ui.load` — ui_surface_cataloged_no_closed_screen_consumer_contract | 22 | `catalog_only_until_screen_consumer_contract` |
| `ui.mail` — ui_surface_cataloged_no_closed_screen_consumer_contract | 34 | `catalog_only_until_screen_consumer_contract` |
| `ui.meeting` — ui_surface_cataloged_no_closed_screen_consumer_contract | 39 | `catalog_only_until_screen_consumer_contract` |
| `ui.recruit` — ui_surface_cataloged_no_closed_screen_consumer_contract | 6 | `catalog_only_until_screen_consumer_contract` |
| `ui.social.friend` — ui_surface_cataloged_no_closed_screen_consumer_contract | 48 | `catalog_only_until_screen_consumer_contract` |
| `ui.title` — ui_surface_cataloged_no_closed_screen_consumer_contract | 17 | `catalog_only_until_screen_consumer_contract` |
| `ui.window` — ui_surface_cataloged_no_closed_screen_consumer_contract | 32 | `catalog_only_until_screen_consumer_contract` |

## Explicit gaps

- The 34 Unity TextAsset/resource rows are retained by asset ID and ZIP-relative path, but their APK entry/nested Unity mapping is not closed. They remain provenance-only.
- `lineup_layout/bg.seb` remains one unresolved selector identity. The runtime must return an unresolved status rather than guess a filename or selector ID.
- The 21 non-actor families are cataloged and traceable, but screen/event consumer timing, layer order, and placement are not fabricated. A future screen contract can promote a family deliberately.

## Verification

```powershell
python -B tools/social-dev/build_asset_surface_provenance.py
python -B tools/social-dev/test_asset_surface_provenance.py
```
