# Social Dev asset and APK binary inventory

Read-only inventory. ZIP/APK members were hashed in place; neither archive was extracted or modified.

| Source | Members | Uncompressed bytes | SHA-256 |
|---|---:|---:|---|
| Asset ZIP | 3566 | 16,208,026 | `C4B6AC1B6603EB8E2D7AC78E7DD3B8BFFB40B7C30FE036CB644BEA701087B283` |
| APK | 1411 | 121,882,308 | `FA0E9E3A843732258FC05B2611A8E0F5BE6F7E95F2141A53F31FB082322FE2BF` |

## Asset ZIP groups

| Group | Files |
|---|---:|
| `00_INDEX` | 7 |
| `01_GAME_PACKS` | 2826 |
| `02_DERIVED_READY_IMAGES` | 568 |
| `03_ANDROID_RES_IMAGES` | 78 |
| `04_MISC_TEXTASSETS` | 34 |
| `05_ASSEMBLY_GUIDE` | 16 |
| `90_BROWSE_CATALOG` | 36 |
| `README_ASSETS_TH.md` | 1 |

## APK groups

| Group | Files |
|---|---:|
| `AndroidManifest.xml` | 1 |
| `DebugProbesKt.bin` | 1 |
| `META-INF` | 40 |
| `assets` | 1187 |
| `billing.properties` | 1 |
| `classes.dex` | 1 |
| `classes1.dex` | 1 |
| `classes2.dex` | 1 |
| `classes3.dex` | 1 |
| `classes4.dex` | 1 |
| `classes5.dex` | 1 |
| `client_analytics.proto` | 1 |
| `firebase-analytics.properties` | 1 |
| `firebase-encoders-json.properties` | 1 |
| `firebase-encoders-proto.properties` | 1 |
| `firebase-encoders.properties` | 1 |
| `firebase-iid-interop.properties` | 1 |
| `firebase-iid.properties` | 1 |
| `firebase-measurement-connector.properties` | 1 |
| `kotlin` | 12 |
| `lib` | 7 |
| `messaging_event.proto` | 1 |
| `messaging_event_extension.proto` | 1 |
| `play-services-ads-base.properties` | 1 |
| `play-services-ads-identifier.properties` | 1 |
| `play-services-ads-lite.properties` | 1 |
| `play-services-ads.properties` | 1 |
| `play-services-appset.properties` | 1 |
| `play-services-base.properties` | 1 |
| `play-services-basement.properties` | 1 |
| `play-services-cloud-messaging.properties` | 1 |
| `play-services-location.properties` | 1 |
| `play-services-measurement-api.properties` | 1 |
| `play-services-measurement-base.properties` | 1 |
| `play-services-measurement-impl.properties` | 1 |
| `play-services-measurement-sdk-api.properties` | 1 |
| `play-services-measurement-sdk.properties` | 1 |
| `play-services-measurement.properties` | 1 |
| `play-services-places-placereport.properties` | 1 |
| `play-services-stats.properties` | 1 |
| `play-services-tasks.properties` | 1 |
| `res` | 126 |
| `resources.arsc` | 1 |
| `user-messaging-platform.properties` | 1 |

## Index summaries

The assembly guide/index files are parsed only for shape and counts. Their rows still require cross-checking against C# selectors and APK provenance.

| Index | Summary |
|---|---|
| `00_INDEX/ASSEMBLY_GUIDE_MANIFEST.json` | `{"documents_count": 16, "key_count": 5, "keys": ["documents", "guide_root", "language", "recommended_examples", "recommended_start"], "parse_status": "valid", "recommended_examples_count": 3, "value_type": "dict"}` |
| `00_INDEX/ASSET_INDEX.csv` | `{"header": ["relative_path", "kind", "pack", "original_name", "extension", "size", "width", "height", "format", "has_alpha", "sha256", "apk_source_entry", "semantic_role"], "parse_status": "read", "row_count_including_header": 3543}` |
| `00_INDEX/ASSET_INDEX.json` | `{"first_item_keys": ["apk_source_entry", "extension", "format", "has_alpha", "height", "kind", "original_name", "pack", "relative_path", "semantic_role", "sha256", "size", "width"], "item_count": 3542, "parse_status": "valid", "value_type": "list"}` |
| `00_INDEX/PACK_SOURCE_MAP.csv` | `{"header": ["pack", "semantic_role", "apk_source_entry", "file_count", "png_count", "inf_count", "opt_count", "seb_count", "txt_count", "csv_count", "bin_count", "roundtrip_exact", "encrypted_sha256", "decrypted_sha256"], "parse_status": "read", "row_count_including_header": 26}` |
| `00_INDEX/PACK_SOURCE_MAP.json` | `{"first_item_keys": ["apk_source_entry", "bin_count", "csv_count", "decrypted_sha256", "encrypted_sha256", "file_count", "inf_count", "opt_count", "pack", "png_count", "roundtrip_exact", "seb_count", "semantic_role", "txt_count"], "item_count": 25, "parse_status": "valid", "value_type": "list"}` |
| `00_INDEX/SHA256SUMS.txt` | `{"line_count": 3566, "parse_status": "text"}` |
| `00_INDEX/SOURCE_FINGERPRINT.json` | `{"asset_package_counts_count": 6, "key_count": 14, "keys": ["asset_package_counts", "custom_packs", "engine_classification", "handoff_recorded_source_sha256", "matched_handoff", "notes", "original_pack_extension_counts", "original_pack_files", "pack_roundtrip_exact", "package_guess", "source_apk", "source_apk_sha256", "source_apk_size", "valid_original_pack_images"], "notes_count": 5, "original_pack_extension_counts_count": 7, "parse_status": "valid", "value_type": "dict"}` |

## Gate

No image, animation, `.inf`, `.opt`, or `.seb` member is runtime-approved by this inventory. Promotion waits for identity/selector/relationship validation.
