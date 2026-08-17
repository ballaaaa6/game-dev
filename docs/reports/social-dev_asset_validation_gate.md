# Social Dev asset validation gate

Evidence-only consistency check. No asset is runtime-approved because selector/semantic validation is still pending.

## ZIP index consistency

| Status | Files |
|---|---:|
| `zip_exact` | 3542 |

## APK source-entry consistency

| Status | Files |
|---|---:|
| `apk_entry_missing` | 34 |
| `apk_entry_present` | 3508 |

## Asset kinds

| Kind | Files | Runtime policy |
|---|---:|---|
| `android_raster_resource` | 78 | derived/catalog; blocked from identity promotion |
| `contact_sheet_catalog` | 36 | derived/catalog; blocked from identity promotion |
| `opt_reconstructed_image` | 328 | derived/catalog; blocked from identity promotion |
| `original_pack_asset` | 2826 | candidate after selector review |
| `plain_textasset_payload` | 34 | derived/catalog; blocked from identity promotion |
| `seb_preview_image` | 240 | derived/catalog; blocked from identity promotion |

## Source fingerprint

- Recorded APK SHA-256: `FA0E9E3A843732258FC05B2611A8E0F5BE6F7E95F2141A53F31FB082322FE2BF`
- Actual APK SHA-256: `FA0E9E3A843732258FC05B2611A8E0F5BE6F7E95F2141A53F31FB082322FE2BF`
- Match: `True`
- Guide matched handoff: `Social_Dev_Story_v2.5.1.zip`

## Gate result

ZIP/APK references are structurally consistent only when their statuses are exact/present. Every row remains `blocked_selector_unverified` until C# selectors and asset relationships are proven.
