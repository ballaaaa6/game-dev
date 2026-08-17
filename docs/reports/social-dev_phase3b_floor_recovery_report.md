# Phase 3B Floor Selector Recovery Report

## Outcome

The recovery pass is complete and passed 22/22 checks. The final classification is **`source_limited_unresolved`**.

`RoomData(0).floorImgId_` is raw selector `5`, but the supplied current package has no authoritative `chip/img.inf` entry for id `5`. The decrypted APK `img.inf` is byte-identical to the supplied asset ZIP `img.inf` (`5f37934c43bc86c3139d7415f1ae2c9315b4aef7bc81746b95db558a077e5310`), so this is not an extraction mismatch between the two current package sources. The source filename remains unresolved; the recorded runtime decision aliases selector `5` to selector `85` / `floor_09.png`.

This closes the Phase 3B recovery gate as a source limitation plus an explicit runtime decision. The source evidence remains unchanged: `img.inf` still has no id `5` entry, and `floor_05.png` remains mapped to selector `23`. Phase 3C may render `floor_09.png` for raw selector `5` only through the recorded fallback alias; it must not present that alias as recovered original provenance.

## Evidence chain

- Room selector: `room:0.floorImgId_ = 5`.
- ZIP `chip/img.inf`: `3395 bytes`, `5f37934c43bc86c3139d7415f1ae2c9315b4aef7bc81746b95db558a077e5310`, no id `5`.
- APK `chip/img.inf`: `3395 bytes`, `5f37934c43bc86c3139d7415f1ae2c9315b4aef7bc81746b95db558a077e5310`, no id `5`.
- APK chip scan: exactly one `chip` TextAsset across `1147` data entries; decrypted pack has `333` records.
- Native/source trace: selector is passed as a raw positive value into `MapChip`; the reviewed evidence proves no positive id-5 alias or fallback.
- Runtime decision: raw selector `5` → indexed selector `85` → `floor_09.png`.

## Alternate package provenance

- `2.4.9`: `missing_in_workspace` — `Social+Dev+Story_2.4.9_APKPure.apk`
- `2.5.0`: `missing_in_workspace` — `Social+Dev+Story_2.5.0_APKPure.apk`
- `2.5.1_current`: `matching_current_chip_boundary` — `sources/raw/Social_Dev_Story_v2.5.1.apk`
- `archive_game_dev_story_mod`: `removed_with_legacy_archive` — `archive/pre-social-reset (removed)`

The named 2.4.9 and 2.5.0 APK files are absent from the workspace and remain outside the current package comparison.

## Required runtime policy

- Retain raw selector `5` for provenance.
- Keep source resolution for selector `5` marked `unresolved`.
- Use the explicit runtime alias `5 → 85 → floor_09.png` when the room renderer needs a floor image.
- Do not relabel `floor_09.png` as the recovered original for selector `5`.
- Re-open source recovery only when an exact alternate Social Dev package or an authoritative source/native mapping is supplied.

## Artifacts

- Source audit: `knowledge/fixtures/accepted/phase3b_floor_recovery_source_audit.json` (`fca1f75cfa6b4cb6af773fe48f9a7f1540c57f30c26cae116ea7036d28d0ae9d`).
- Deterministic fixture: `knowledge/fixtures/accepted/phase3b_floor_recovery_fixture.json` (`e361a76278a7201168fa7d905885f8b33e56beaeb494106c95cdbf4f7c84a519`).
- Validation: `knowledge/fixtures/accepted/phase3b_floor_recovery_validation.json` (`fef7d81fe38ad8486102edc2e4f5a09b03c573c8ddcfd7bb5d615b187e3a1f03`).
