# P0-A0 Corpus Baseline Report

- Schema: `p0-a0.corpus-baseline.v1`
- Snapshot fingerprint: `ce92294f66da1d85a1cc476c7a01fb01a07a0956d418683afdd85658e0b7bceb`
- Generated at UTC: `2026-08-12T05:01:46.120313+00:00`

## Source roots

| Root | Files | Bytes | Lines | Tree SHA-256 | Status |
|---|---:|---:|---:|---|---|
| `game-dev-story-mod_Sprites` | 445 | 12376079 | 25141 | `e9d9651ac5eeb53e0e0d7f558c2b0283143047cc620faac617d438c035cf84df` | pass |
| `game-dev-story-mod_Dumped` | 208 | 2452540798 | 15904864 | `a9570adac035bf99df5ba13d63c4d39c9558efcee74db33328065a11092a9520` | pass |
| `game-dev-story-mod_Extracted` | 1226 | 96455046 | 1 | `c60fd2f889904830eee41f8283eaeb602d43a4d77f2d220ee8064be6eb1fd62d` | pass |

## Derived counts

- `artifact_file_count`: `112` (current_scan)
- `assembly_fallback_functions`: `5` (observed_counts)
- `assembly_files`: `7` (observed_counts)
- `assembly_ok_functions`: `5` (observed_counts)
- `body_assets`: `26` (observed_counts)
- `bodyface_records`: `42` (observed_counts)
- `categorized_code_files`: `126` (observed_counts)
- `code_combined_c_functions`: `110820` (observed_counts)
- `code_function_headers`: `110820` (observed_counts)
- `code_main_failed_functions`: `5` (observed_counts)
- `code_main_successful_functions`: `110819` (observed_counts)
- `code_recovery_added_functions`: `1` (observed_counts)
- `code_remaining_c_functions`: `4` (observed_counts)
- `code_total_functions`: `110824` (observed_counts)
- `face_assets`: `36` (observed_counts)
- `ghidra_address_count`: `88702` (observed_counts)
- `ghidra_labels_created`: `115211` (observed_counts)
- `language_files`: `12` (observed_counts)
- `phase4_evidence_ready_units`: `85` (translation_coverage.summary.evidence_ready_units)
- `phase4_shortlist_units`: `88` (function_inventory.shortlist)
- `phase4_unit_count`: `88` (translation_coverage.summary.unit_count)
- `source_file_count`: `1879` (current_scan)
- `sprites_csv`: `12` (observed_counts)
- `sprites_files`: `445` (observed_counts)
- `sprites_png`: `347` (observed_counts)
- `sprites_total_bytes`: `12376079` (observed_counts)

## External tools

- `ghidra_headless_script`: `available`
- `ghidra_export_c_script`: `available`
- `Cpp2IL`: `not_available`
- `Cpp2IL.exe`: `not_available`

## Checks

- `source_roots_present`: `pass` — All declared source roots were scanned.
- `artifact_inputs_present`: `pass` — All declared artifact roots were scanned.
- `source_roots_read_only`: `pass` — The builder only reads source roots.
- `output_excluded`: `pass` — Corpus output is excluded from artifact input records.
- `historical_manifest_inputs_present`: `pass` — Phase 0/4/5/6 manifests are present.
- `function_count_provenance`: `pass` — Function counts are sourced from the Phase 0 observed-count baseline.

## Known limitations

- Baseline records current filesystem facts; it does not assign semantic meaning.
- The extraction report output path points to game-dev-story-mod_Sprites_fixed while the current source root is game-dev-story-mod_Sprites.
- The extraction report retains three repaired trailing UTF-8 warning records; current CSV bytes pass strict UTF-8/BOM validation.
- The main C export originally had five failures; recovery added one function, leaving four functions without C decompile. All five failed-function assembly fallbacks are present and marked ok.
- Some Ghidra logs contain legacy absolute paths under APK_Toolkit; these are provenance notes, not current source roots.
- No semantic meaning is assigned to character modes or animation states in Phase 0.
