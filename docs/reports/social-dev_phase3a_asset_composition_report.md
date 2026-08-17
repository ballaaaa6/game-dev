# Social Dev Phase 3A asset-composition closure

This report is generated from the read-only asset ZIP/APK and canonical selector evidence.

## Outcome

- Phase 3A status: `approved`
- Source audit status: `approved`
- Target: `furniture:2`
- Reason code: `chair_00_opt_variable_piece_reconstruction_verified`
- Source audit content hash: `500468601ccdcbb66b9ff077cbc33ece743dea0db57c207d369a2cc6dcb3b780`
- Closure content hash: `94ea69f9c124ec3e18e155faf118560f77970bbc50193c28073a9a0911046344`
- Display gate content hash: `a9b5b2f9076dc3f05fde9ab64d88f96ef5dea27fd467ec045025d2fb2472dd08`
- Runtime manifest content hash: `aad85bbd7113712b0517ed2555f1e88c4f0227ef8e46ee56e1cd23e2e67db5a4`

## APK re-extraction result

- APK loader probe: `complete_for_selected_chair_triplets` for `chair_00, chair_01, chair_02, chair_03, chair_04`.
- Recovered triplet count: `15`; all outputs match the supplied ZIP: `True`.
- The APK therefore confirms the supplied chair bytes rather than providing a second byte variant.
- The variable-piece OPT parser now consumes all selected chair payloads exactly; `chair_00`/`chair_01` use piece counts [1, 2, 1], `chair_02`/`chair_03` use [1, 1, 1], and `chair_04` uses [1, 2, 0].

## Three-version APK comparison

- Compared APK versions: `2.4.9, 2.5.0, 2.5.1`.
- All three chip plaintexts are byte-identical: `True`; pack size is `333` entries.
- All 15 selected chair outputs are byte-identical across versions: `True`; each matches the supplied ZIP: `True`.
- The version comparison rules out extraction/container loss and confirms that the same source bytes are present in all three builds; it does not need to provide alternate bytes because the variable-piece grammar resolves chair_00 from its own payload.
- Comparison audit: `knowledge/sources/phase3a_apk_probe/chair_version_comparison.json`; content hash `255e0e34960511341d50450c42c1a7eee6fd30f50e4b2014974d581addf7a892`.

## Derived chair_00 approximation probe

- Three historical non-authoritative previews were generated before the variable-piece grammar was identified: a duplicated-cell fallback, a complete chair_02 substitute, and a mixed chair_00/chair_02 hybrid.
- Those previews remain derived comparisons only; the exact chair_00 reconstruction now uses the original PNG/OPT bytes and supersedes them for runtime.
- Variant audit: `knowledge/sources/phase3a_apk_probe/chair_variants/chair_00_variant_audit.json`; content hash `a9312268c349b03057b774a8ac5b88b204e711c7e6476ee8743501f7e9e9473b`.
- Visual comparison sheet: `knowledge/sources/phase3a_apk_probe/chair_variants/chair_00_variant_comparison.png`.

## Chair structure comparison

- All five chair SEB files share the same one-layer, three-frame animation scaffold, the same 60×32 source rectangles, and the same destination offsets; only the chair-specific `image_id` changes.
- All five OPT headers share the same 180×32 logical canvas, but PNG dimensions and OPT crop/offset geometry differ. The assets are not pixel-only recolors.
- The OPT first byte is a per-cell piece count. `chair_00`/`chair_01` therefore have complete [1, 2, 1] cells, and the former 14-byte tail is the second piece of cell 1 rather than missing data.
- Structure comparison audit: `knowledge/sources/phase3a_apk_probe/chair_structure_comparison.json`; content hash `703863d1f12dd6626ada56b7e6e51ef583e08a276bad6e66e539b10a1704784c`.

## Exact chair_00 reconstruction

- The original `chair_00.png` and `chair_00.opt` reconstruct an exact 180×32 logical atlas with cell piece counts [1, 2, 1].
- The complete asset-pack validation passes all `411/411` OPT payloads and all `89/89` available derived logical references pixel-for-pixel.
- Reconstruction audit: `knowledge/sources/phase3a_apk_probe/chair_00_reconstruction_audit.json`; content hash `68fa8a46ba92d8dfa9e6f7bace73f00e1ec391dd21ba0f2d75455d04b7a87c18`.
- Logical image: `knowledge/sources/phase3a_apk_probe/derived_previews/chair_00.logical.png`; pixel SHA-256 `23d8e732fa2000f18f8fd9649b5fbe2b190d95aff86475b8befd09cfbe8afeef`.
- Crop map: `knowledge/sources/phase3a_apk_probe/derived_previews/chair_00.source_crop_map.png`.

## Current source facts

- `chair_00.opt` is the indexed 63-byte source payload.
- Its header declares a 60×32 cell, 3 columns, and 1 row; its variable-piece cells are [1, 2, 1].
- The four crop pieces consume the payload exactly and all source rectangles fit the 34×15 `chair_00.png`.
- The exact logical reconstruction is source-backed; no alternate filename-level chair_00 source is required.

## Runtime decision

- `furniture:2` is approved by this closure because the original chair_00 bytes now pass variable-piece OPT reconstruction.
- `chair_00.png`, `chair_00.opt`, and `chair_00.seb` are eligible for the runtime asset boundary through the display gate.
- Phase 3C may render `furniture:2` subject to the display gate and room-placement boundaries.
- The historical screenshot baseline remains unchanged.

## Evidence files

- Source audit: `knowledge/fixtures/accepted/phase3a_asset_composition_source_audit.json`
- Closure: `knowledge/fixtures/accepted/phase3a_asset_composition_closure.json`
- Display gate: `knowledge/fixtures/accepted/display_asset_gate.json`
- Runtime manifest: `knowledge/fixtures/accepted/runtime/display_asset_manifest.json`
- APK chair extraction audit: `knowledge/sources/phase3a_apk_probe/chair_extraction_audit.json`
- Three-version APK comparison: `knowledge/sources/phase3a_apk_probe/chair_version_comparison.json`
- Derived chair_00 variant audit: `knowledge/sources/phase3a_apk_probe/chair_variants/chair_00_variant_audit.json`
- Chair structure comparison: `knowledge/sources/phase3a_apk_probe/chair_structure_comparison.json`
- Exact chair_00 reconstruction audit: `knowledge/sources/phase3a_apk_probe/chair_00_reconstruction_audit.json`
