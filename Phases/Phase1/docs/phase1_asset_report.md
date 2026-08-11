# Phase 1 Asset Inventory Report

Generated: `2026-08-11T09:40:11.740519Z`

Status: **pass_with_warnings**

This report is generated from the current extraction roots. Source assets remain read-only.

## Coverage

- Target files: **405**
- Target PNG: **346**
- Target SEB: **53**
- SEB structurally decoded: **53**
- Target INF: **6**
- Office PNG: **146**
- Bonus catalog rows: **146**
- Verified code-trace claims: **18**
- Office manifest assets: **168**

## Checks

| Check | Status | Details |
|---|---|---|
| `catalog_count` | **pass** | catalog=405 expected=405 |
| `catalog_unique_keys` | **pass** | duplicate_paths=0 duplicate_ids=0 |
| `source_hash_integrity` | **pass** | missing=0 catalog_mismatch=0 phase0_mismatch=0 |
| `png_metadata` | **pass** | invalid_png_metadata=0 |
| `seb_manifest_integrity` | **pass** | catalog_seb=53 manifest_seb=53 hash_mismatch=0 parse_issues=0 |
| `seb_structural_decode` | **attention** | decoded=53 tail_shortfall=53 |
| `office_manifest_integrity` | **pass** | catalog_office=168 manifest_office=168 missing=0 extra=0 |
| `code_trace_integrity` | **pass** | functions=14 evidence=18 source_mismatch=0 |
| `preview_artifacts_present` | **pass** | declared=2 missing=0 |
| `inf_referential_integrity` | **pass** | records=358 probable_suffix_recoveries=6 |
| `bonus_referential_integrity` | **pass** | rows=146 placeholders=2 direct_links=144 |
| `known_anomalies_are_recorded` | **pass** | orphan_office_png=2 floor_pair_gaps=4 seb_tail_shortfall=53 |
| `input_audit_status` | **pass** | audit_failures=0 |

## Current known anomalies

- INF missing-extension references: **6**
- Office floor PNGs without same-name SEB: **4**
- Office PNGs without direct bonus reference: **2**
- SEB final-record tail shortfalls: **53**

### INF suffix recoveries

- `{"source": "com/img.inf", "line": 37, "raw_name": "socialShare", "anomaly": "missing_extension_in_source_inf"}`
- `{"source": "com/seb.inf", "line": 29, "raw_name": "socialShare", "anomaly": "missing_extension_in_source_inf"}`
- `{"source": "game/img.inf", "line": 123, "raw_name": "floorCover", "anomaly": "missing_extension_in_source_inf"}`
- `{"source": "game/seb.inf", "line": 2, "raw_name": "backlight", "anomaly": "missing_extension_in_source_inf"}`
- `{"source": "office/img.inf", "line": 146, "raw_name": "reception_036", "anomaly": "missing_extension_in_source_inf"}`
- `{"source": "office/seb.inf", "line": 21, "raw_name": "floor36", "anomaly": "missing_extension_in_source_inf"}`

### Office floor/SEB gaps

- `{"png": "office/floor13.png", "expected_seb": "office/floor13.seb"}`
- `{"png": "office/floor2.png", "expected_seb": "office/floor2.seb"}`
- `{"png": "office/floor4.png", "expected_seb": "office/floor4.seb"}`
- `{"png": "office/floor9.png", "expected_seb": "office/floor9.seb"}`

### Office bonus orphans

- `"office/reception_001.png"`
- `"office/reception_002.png"`

### SEB tail shortfalls

- `{"path": "com/back00_240.seb", "bytes": 4, "expected_bytes": 28, "actual_bytes": 24}`
- `{"path": "com/banana.seb", "bytes": 4, "expected_bytes": 132, "actual_bytes": 128}`
- `{"path": "com/banana_number01.seb", "bytes": 4, "expected_bytes": 208, "actual_bytes": 204}`
- `{"path": "com/base.seb", "bytes": 4, "expected_bytes": 48, "actual_bytes": 44}`
- `{"path": "com/chinpan.seb", "bytes": 4, "expected_bytes": 48, "actual_bytes": 44}`
- `{"path": "com/chinpan_chari.seb", "bytes": 4, "expected_bytes": 68, "actual_bytes": 64}`
- `{"path": "com/chinpan_labo.seb", "bytes": 4, "expected_bytes": 28, "actual_bytes": 24}`
- `{"path": "com/chinpanlabo_button.seb", "bytes": 4, "expected_bytes": 68, "actual_bytes": 64}`
- `{"path": "com/cm.seb", "bytes": 4, "expected_bytes": 28, "actual_bytes": 24}`
- `{"path": "com/cm_amazon.seb", "bytes": 4, "expected_bytes": 48, "actual_bytes": 44}`
- `{"path": "com/delivery_back.seb", "bytes": 4, "expected_bytes": 48, "actual_bytes": 44}`
- `{"path": "com/kumax.seb", "bytes": 4, "expected_bytes": 48, "actual_bytes": 44}`
- `{"path": "com/lock.seb", "bytes": 4, "expected_bytes": 48, "actual_bytes": 44}`
- `{"path": "com/new.seb", "bytes": 4, "expected_bytes": 48, "actual_bytes": 44}`
- `{"path": "com/office_cover.seb", "bytes": 4, "expected_bytes": 128, "actual_bytes": 124}`
- `{"path": "com/ranking_arrow.seb", "bytes": 4, "expected_bytes": 28, "actual_bytes": 24}`
- `{"path": "com/ranking_back.seb", "bytes": 4, "expected_bytes": 28, "actual_bytes": 24}`
- `{"path": "com/ranking_button.seb", "bytes": 4, "expected_bytes": 48, "actual_bytes": 44}`
- `{"path": "com/ranking_confetti.seb", "bytes": 4, "expected_bytes": 28, "actual_bytes": 24}`
- `{"path": "com/ranking_frame.seb", "bytes": 4, "expected_bytes": 260, "actual_bytes": 256}`
- `{"path": "com/ranking_glory.seb", "bytes": 4, "expected_bytes": 28, "actual_bytes": 24}`
- `{"path": "com/ranking_icons.seb", "bytes": 4, "expected_bytes": 48, "actual_bytes": 44}`
- `{"path": "com/ranking_title_icons.seb", "bytes": 4, "expected_bytes": 108, "actual_bytes": 104}`
- `{"path": "com/ranking_window.seb", "bytes": 4, "expected_bytes": 136, "actual_bytes": 132}`
- `{"path": "com/saveload.seb", "bytes": 4, "expected_bytes": 48, "actual_bytes": 44}`
- `{"path": "com/socialAchievement.seb", "bytes": 4, "expected_bytes": 48, "actual_bytes": 44}`
- `{"path": "com/socialRanking.seb", "bytes": 4, "expected_bytes": 48, "actual_bytes": 44}`
- `{"path": "com/socialShare.seb", "bytes": 4, "expected_bytes": 48, "actual_bytes": 44}`
- `{"path": "com/trophyicon.seb", "bytes": 4, "expected_bytes": 28, "actual_bytes": 24}`
- `{"path": "game/backlight.seb", "bytes": 4, "expected_bytes": 48, "actual_bytes": 44}`
- `{"path": "game/cameraman.seb", "bytes": 4, "expected_bytes": 168, "actual_bytes": 164}`
- `{"path": "office/floor.seb", "bytes": 4, "expected_bytes": 272, "actual_bytes": 268}`
- `{"path": "office/floor0.seb", "bytes": 4, "expected_bytes": 28, "actual_bytes": 24}`
- `{"path": "office/floor1.seb", "bytes": 4, "expected_bytes": 272, "actual_bytes": 268}`
- `{"path": "office/floor11.seb", "bytes": 4, "expected_bytes": 296, "actual_bytes": 292}`
- `{"path": "office/floor12.seb", "bytes": 4, "expected_bytes": 296, "actual_bytes": 292}`
- `{"path": "office/floor14.seb", "bytes": 4, "expected_bytes": 252, "actual_bytes": 248}`
- `{"path": "office/floor15.seb", "bytes": 4, "expected_bytes": 320, "actual_bytes": 316}`
- `{"path": "office/floor16.seb", "bytes": 4, "expected_bytes": 296, "actual_bytes": 292}`
- `{"path": "office/floor17.seb", "bytes": 4, "expected_bytes": 516, "actual_bytes": 512}`
- `{"path": "office/floor18.seb", "bytes": 4, "expected_bytes": 276, "actual_bytes": 272}`
- `{"path": "office/floor19.seb", "bytes": 4, "expected_bytes": 296, "actual_bytes": 292}`
- `{"path": "office/floor21.seb", "bytes": 4, "expected_bytes": 296, "actual_bytes": 292}`
- `{"path": "office/floor3.seb", "bytes": 4, "expected_bytes": 276, "actual_bytes": 272}`
- `{"path": "office/floor31.seb", "bytes": 4, "expected_bytes": 276, "actual_bytes": 272}`
- `{"path": "office/floor33.seb", "bytes": 4, "expected_bytes": 296, "actual_bytes": 292}`
- `{"path": "office/floor34.seb", "bytes": 4, "expected_bytes": 296, "actual_bytes": 292}`
- `{"path": "office/floor35.seb", "bytes": 4, "expected_bytes": 296, "actual_bytes": 292}`
- `{"path": "office/floor36.seb", "bytes": 4, "expected_bytes": 300, "actual_bytes": 296}`
- `{"path": "office/floor5.seb", "bytes": 4, "expected_bytes": 276, "actual_bytes": 272}`
- `{"path": "office/floor6.seb", "bytes": 4, "expected_bytes": 296, "actual_bytes": 292}`
- `{"path": "office/floor7.seb", "bytes": 4, "expected_bytes": 276, "actual_bytes": 272}`
- `{"path": "office/floor8.seb", "bytes": 4, "expected_bytes": 252, "actual_bytes": 248}`

## Renderer evidence and office map

- Renderer functions indexed: **14**
- Verified renderer claims: **18**
- Unresolved contracts retained: **3**
- Office manifest assets: **168** (146 PNG + 22 SEB)

| Evidence | Confidence | Source | Claim |
|---|---|---|---|
| `drawobj_dispatches_human` | **verified** | `game-dev-story-mod_Dumped/Categorized_Code/Global/form.c:16325` | DrawObj contains a direct branch that calls DrawHuman with computed integer coordinates. |
| `drawobj_dispatches_chair` | **verified** | `game-dev-story-mod_Dumped/Categorized_Code/Global/form.c:16490` | DrawObj dispatches object rendering to DrawChair. |
| `drawobj_dispatches_desk` | **verified** | `game-dev-story-mod_Dumped/Categorized_Code/Global/form.c:16609` | DrawObj dispatches object rendering to DrawDesk. |
| `drawobj_dispatches_ceo_desk` | **verified** | `game-dev-story-mod_Dumped/Categorized_Code/Global/form.c:16638` | DrawObj has a distinct DrawCeoDesk branch. |
| `drawobj_dispatches_reception` | **verified** | `game-dev-story-mod_Dumped/Categorized_Code/Global/form.c:16674` | DrawObj dispatches reception rendering with computed x/y plus source-rectangle arguments. |
| `drawobj_sort_comparison` | **verified** | `game-dev-story-mod_Dumped/Categorized_Code/Global/form.c:15976` | DrawObj performs an ordering comparison over two AppData-backed integer arrays before swapping entries. |
| `floor_cover_source_rect` | **verified** | `game-dev-story-mod_Dumped/Categorized_Code/Global/form.c:24170` | DrawFloorCover selects an entry from an AppData array at offset +0x78 and passes its x/y/w/h fields to DrawImage with caller offsets. |
| `chair_image_source` | **verified** | `game-dev-story-mod_Dumped/Categorized_Code/Global/form.c:55982` | DrawChair reads the furniture image list at AppData +0x1110 and uses its +0x28 image slot with caller source rectangle fields. |
| `desk_image_source` | **verified** | `game-dev-story-mod_Dumped/Categorized_Code/Global/form.c:56028` | DrawDesk reads the furniture image list at AppData +0x1110 and uses its +0x30 image slot. |
| `reception_image_source` | **verified** | `game-dev-story-mod_Dumped/Categorized_Code/Global/form.c:56108` | DrawReception reads the reception image at AppData +0x1128 and uses caller source rectangle fields. |
| `desk_index_lookup` | **verified** | `game-dev-story-mod_Dumped/Categorized_Code/Global/form.c:24589` | GetDeskImgData maps an integer index by quotient/remainder into an AppData array at +0x488. |
| `chair_index_lookup` | **verified** | `game-dev-story-mod_Dumped/Categorized_Code/Global/form.c:24633` | GetChairImgData maps an integer index by quotient/remainder into an AppData array at +0x490. |
| `scale_clamp` | **verified** | `game-dev-story-mod_Dumped/Categorized_Code/Global/form.c:15748` | SetScale clamps the requested scale through GetScaleRange/AppData Clamp and stores the result at GameForm +0x108. |
| `game_width_formula` | **verified** | `game-dev-story-mod_Dumped/Categorized_Code/Global/form.c:15786` | GetGameWidth derives a scaled width from surface_GameView.GetGameWidth and the stored scale. |
| `game_height_formula` | **verified** | `game-dev-story-mod_Dumped/Categorized_Code/Global/form.c:15835` | GetGameHeight derives a scaled height from surface_GameView.GetGameHeight and subtracts the decompiled constant 0x898 before division. |
| `setorigin_empty_export` | **verified** | `game-dev-story-mod_Dumped/Categorized_Code/Global/form.c:41019` | The exported form_GameForm__SetOrigin body is an empty return. |
| `bihin_image_loading` | **verified** | `game-dev-story-mod_Dumped/Categorized_Code/Global/form.c:56715` | LoadBihinImage builds image names from AppData name entries plus a suffix and stores loaded images in the furniture image container. |
| `seb_eof_behavior` | **verified** | `game-dev-story-mod_Dumped/Categorized_Code/Global/Method.c:107167` | The shared StreamUtil.Read loop raises EOFException when a requested read returns fewer bytes. |

### Unresolved runtime contracts

- `grid_contract`: A tile grid, A*, or fixed furniture footprint is not established by this trace. (No direct occupancy/pathfinding/seat contract was identified in the selected renderer entry points.)
- `collision_contract`: Collision, walkable, seat, and interaction zones remain unverified. (The selected draw functions consume arrays and image data but do not name a collision schema.)
- `depth_field_semantics`: The sort key used by DrawObj is not named as y/depth/z by the decompiler. (The compare-and-swap pattern is visible, but array offsets are not recovered field names.)

## Interpretation rules

- A unique basename extension match is adapter metadata and remains `probable`; the INF source is unchanged.
- Alpha bounds are visual diagnostics only. They do not establish pivot, seat, collision, or depth semantics.
- SEB fields are structurally decoded from decompiled loader evidence; all current extracted files end four bytes before the declared final record is complete. This may be a legacy variant or an extraction/archive boundary issue and remains unresolved; runtime semantics are not trusted.
- `reception_001` and `reception_002` remain unresolved until code evidence maps the two `-1` catalog rows.

## Generated artifacts

- `Phases/Phase1/artifacts/phase1_input_audit.json`
- `Phases/Phase1/artifacts/phase1_asset_catalog.json`
- `Phases/Phase1/artifacts/phase1_seb_manifest.json`
- `Phases/Phase1/artifacts/phase1_code_trace.json`
- `Phases/Phase1/artifacts/office_manifest.json`
- `Phases/Phase1/artifacts/phase1_preview_manifest.json`
- `Phases/Phase1/docs/phase1_office_preview.png`
- `Phases/Phase1/docs/phase1_office_floor_contact_sheet.png`
- `Phases/Phase1/artifacts/phase1_legacy_asset_map.json`
- `Phases/Phase1/artifacts/phase1_validation_report.json`
