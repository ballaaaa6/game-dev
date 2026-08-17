# Social Dev Full Character Asset Runtime Report

## Result

The full native human character asset path is implemented and verified. The previous bounded `display_asset_manifest` remains unchanged as a display-slice contract; full character PNG/SEB data now has a dedicated approved runtime catalog and a generic lazy renderer path.

## Closed evidence

| Gate | Result |
| --- | --- |
| StaffData image coverage | `141/141` bindings |
| Native human image promotion | `105/105` PNG selectors, exact bytes |
| Native human animation promotion | `35/35` SEB selectors, exact bytes |
| Multilayer decoding | `48` layers / `334` records |
| Explicit native control records | `30` `control_no_texture` records |
| Drawable rectangle bounds | `0` invalid rectangles |
| Native callable action inventory | `16` action groups / `35` selectors |
| Capability regression | `14/14` checks |
| Asset regression | `10/10` checks |
| TypeScript typecheck | pass |
| Vitest | `38/38` tests |
| Vite production build | pass |

The current contract hashes are:

- capability contract: `af8aa15f6d5daa4f066bd541b91804f19f04535dfd2d1daf67a9e72759885a1f`;
- character asset contract: `2a663405c511f4862e4016c4540737f2611ee6e90eef88c20c147594db2c5908`.

## Runtime call path

`resolveCharacter(catalogs, characterId)` returns the static template and shared profile. `resolveCharacterAction(...)` first checks semantic actions and then the filename-derived native action map. `characterDisplayFrame(...)` resolves the human PNG asset and decoded SEB records for the selected frame. The loader resolves each frame image slot independently: native slot `0` is substituted with the active StaffData image, while non-zero slots such as `head.seb`'s slot `1` use their own promoted image. `preloadCharacterFrameImages(...)` loads only the assets required by that frame when they are not already cached. Canvas then draws the active resolved record from each layer; native control records are skipped as no-texture instructions.

Examples now covered by regression tests:

- `staff:114`, `wait`, `left` → selector `11`;
- `staff:114`, `talk`, `right` → the explicit `typing_right.seb` alias, selector `23`;
- `staff:114`, `banzai`, `right` → selector `19`, with three-layer composition;
- `staff:114`, `head`, any direction → selector `100`;
- `staff:114`, `banzai`, `left` → explicit `no_selector_for_direction`.

## Loading and memory policy

Metadata and decoded frame JSON are compact catalog data. Character PNGs are not loaded for all `141` templates at startup. The browser maps an asset ID to a runtime URL only when an active actor needs it, and concurrent requests for the same image share one promise/cache entry. The raw SEB binaries are retained for provenance and future extensions; the current browser draw path consumes the generated decoded frame contract instead of parsing binary files at runtime.

## Scope boundary

All `141` StaffData templates, including the special range, are covered by the human package. The `19` HelperData records remain a separate metadata family, and avatar body/head and event-only assets remain explicit future packages. The current simulation continues to show the bounded scene actor set; the full catalog is prepared for lazy scene use rather than instantiating all characters simultaneously.

## Reproduction

```text
python tools/social-dev/build_character_capabilities.py
python tools/social-dev/build_character_asset_manifest.py
python tools/social-dev/test_character_capabilities.py
python tools/social-dev/test_character_asset_manifest.py
cd runtime/social-dev
npm run typecheck
npm test -- --run
npm run build
```

The source asset archive and recovered C# roots remain read-only. Runtime imports are limited to generated JSON contracts and promoted runtime assets.
