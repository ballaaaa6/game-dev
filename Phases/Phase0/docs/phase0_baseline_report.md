# Phase 0 Baseline Report

Generated: `2026-08-11T09:39:49.892342Z`

Status: **complete_with_known_limitations**

Phase 0 freezes the current extraction set for later comparison. The source roots were read only; no extracted asset, dump, APK or Ghidra project was modified.

## Source roots

| Root | Exists | Files | Bytes | Newest file (UTC) |
|---|---:|---:|---:|---|
| `game-dev-story-mod_Sprites` | True | 445 | 12,376,079 | `2026-08-11T08:28:34.467746Z` |
| `game-dev-story-mod_Dumped` | True | 208 | 2,452,540,798 | `2026-08-11T08:12:22.105081Z` |
| `game-dev-story-mod_Extracted` | True | 1,226 | 96,455,046 | `2026-03-16T17:55:42Z` |

## Observed baseline

- Sprites output: **445 files**, including 347 PNG and 12 CSV files.
- Language tables: **12 locales**.
- Character assets: **26 body** and **36 face** PNG files.
- Body-face records: **42**.
- IL2CPP C export: main **110,819/110,824**, recovery added **1**, canonical combined C **110,820/110,824**; C-only remaining: **4**.
- Assembly fallback: **5/5** functions marked `ok`; effective C/assembly coverage: **110,824/110,824**.
- Ghidra symbols: `88702` addresses and `115211` labels created.

## Validation checks

| Check | Status | Details |
|---|---|---|
| `source_roots_present` | **pass** | All three current source roots exist. |
| `asset_report_errors` | **pass** | extraction_report.json errors=0. |
| `asset_report_output_path` | **attention** | Report says 'D:\\antigravity\\test open ai\\game-dev-story-mod_Sprites_fixed'; current root is 'D:\\antigravity\\test open ai\\game-dev-story-mod_Sprites'. |
| `asset_report_input_path` | **pass** | Report input path matches the current extracted root. |
| `language_files_valid` | **pass** | Validated 12 CSV files for BOM and strict UTF-8 bytes. |
| `language_id_shape` | **attention** | Found 1 non-canonical/duplicate language ID row issue(s); source CSV was not changed. |
| `extractor_warning_provenance` | **attention** | Extractor report retains 3 warning record(s); current CSV bytes are validated separately. |
| `asset_file_count_reconciles` | **pass** | Current files=445; report extracted=436, raw=8, report-file=1. |
| `code_export_baseline` | **pass** | Main export=110819/110824; recovery added=1; combined C=110820/110824; C-only remaining=4. |
| `code_decompile_completeness` | **attention** | Canonical recovered C has 110820/110824 function headers; 4 function(s) remain assembly-only. |
| `assembly_fallback_coverage` | **pass** | Assembly fallback covers 5 functions; status ok=5; C-only remaining=4. |
| `tool_log_provenance` | **attention** | Logs contain legacy APK_Toolkit absolute paths: ghidra_export.log, ghidra_recovery.log, ghidra_assembly.log |

## Extraction report reconciliation

- Report input: `D:\antigravity\test open ai\game-dev-story-mod_Extracted\assets\bin\Data`
- Current input: `game-dev-story-mod_Extracted/assets/bin/Data`
- Report output: `D:\antigravity\test open ai\game-dev-story-mod_Sprites_fixed`
- Current output: `game-dev-story-mod_Sprites`
- Reported extracted files: `436`; raw assets: `8`; report warnings: `3`; errors: `0`.

## Known limitations carried forward

- The extraction report output path points to game-dev-story-mod_Sprites_fixed while the current source root is game-dev-story-mod_Sprites.
- The extraction report retains three repaired trailing UTF-8 warning records; current CSV bytes pass strict UTF-8/BOM validation.
- The main C export originally had five failures; recovery added one function, leaving four functions without C decompile. All five failed-function assembly fallbacks are present and marked ok.
- Some Ghidra logs contain legacy absolute paths under APK_Toolkit; these are provenance notes, not current source roots.
- No semantic meaning is assigned to character modes or animation states in Phase 0.

## Generated artifacts

- `Phases/Phase0/artifacts/asset_manifest.json` — every file under the current sprites root, dimensions for PNG files, modification time and SHA-256.
- `Phases/Phase0/artifacts/language_manifest.json` — locale metadata, IDs, placeholder tokens, duplicate/malformed row checks and SHA-256 for each CSV.
- `Phases/Phase0/artifacts/phase0_baseline.json` — source-root summary, report reconciliation, code baseline and validation checks.
- `Phases/Phase0/artifacts/code_coverage_manifest.json` — separates the original five export failures, the one recovered C function, the four remaining C gaps and all assembly fallbacks.
- `Phases/Phase0/artifacts/phase0_checksums.sha256` — reproducible checksum list for all sprite files and selected key dump/input files.

## Next phase

Phase 1 can now inventory the office/game/com/system assets and create the visual office map. The path mismatch and extractor warning records should remain visible until the extraction pipeline is either rerun or explicitly documented as historical provenance.
