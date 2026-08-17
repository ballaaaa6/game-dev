# Original Architecture vs Current Browser Runtime

The current runtime is a successful bounded contract-first browser scene. It is not structurally equivalent to the original visual subsystem. This comparison is descriptive only; V0 does not refactor or retire runtime modules.

| Original responsibility | Current runtime implementation | Structural difference | V0 conclusion |
|---|---|---|---|
| `Sprite` field record and implicit accessors | `DisplayFrameRecord` and selected crop/destination fields in `src/assets/display-assets.ts` | Current records are curated display metadata, not a general Sprite/SEB interpreter. | Reuse as comparison fixtures only. |
| `Seb` frame/layer composition | Direct frame-record selection and browser image draw | Layer composition, anchors, bounds, and variant draw semantics are bypassed. | Must recover SEB before claiming parity. |
| `Image` + OPT decode and pixel ownership | JSON manifests plus `HTMLImageElement` loading | No original OPT ownership/use/expiration/SEB association exists in the runtime path. | Replace only after V1 core recovery. |
| `ImageAtlas` / `ImageAtlasManager` | No equivalent semantic atlas subsystem in the scene path | Browser image objects are loaded directly. | Treat current raster assets as fixtures, not an atlas contract. |
| `ResourceManager` resource groups | `display_asset_manifest`, room/character manifests, and explicit asset IDs | Group identity such as `resChip_`/`resHuman_` is not authoritative in the runtime. | Resource groups must be rebuilt before broad coverage. |
| `Graphics` | Canvas 2D calls in `canvas-renderer.ts` and related renderer modules | Browser context is a backend, but current calls are hand-authored around bounded contracts. | Keep current renderer unchanged during V0. |
| `MapChip` | `projection.ts`, room resolver, and explicit render passes | Projection/data are contract-derived rather than original MapChip objects. | Existing formulas/contracts are valuable evidence, not source replacement. |
| `ObjChip` / `FurnitureData` | Scene cell projections and `furnitureFrameForScene` | Current runtime selects approved furniture frame records and freezes `furniture:3` to frame 0. | Preserve this as a bounded gate; do not generalize it. |
| `Room` | Room resolver, scene projection, render plan, and `native-render-order.ts` | The nine pass names are preserved as an explicit contract, but original Room orchestration is absent. | Reuse native order evidence; later compare to recovered Room. |
| `Staff` / `StaffData` | `character-resolver.ts`, `character-assets.ts`, actor metadata, and direct frame assets | Character identity/frame selection is manifest-driven, without Staff animation state or ResourceManager ownership. | Native character trace remains required. |
| `Camera` | Browser scene coordinates and fixed route/layout state | Camera object/setter lifecycle is not present as the original class. | Preserve source camera formulas at the eventual adapter boundary. |
| `GameForm` / `Main` / `AppData` | Vite route, DOM shell, Canvas 2D, and app entry modules | Unity lifecycle and shared draw helper ownership are replaced by browser modules. | Port backend only after lifecycle trace. |
| Gameplay systems | Current bounded fixtures and source-derived contracts | Current runtime intentionally excludes simulation, economy, jobs, and save behavior. | This boundary is compatible with `GAMEPLAY_CUT_LIST.md`. |

## Existing runtime strengths

The current runtime has useful evidence-backed pieces: explicit two-grid room projection, native pass naming, bounded asset manifests, character metadata, floor alias handling, and regression gates. Those pieces may be reused as fixtures and acceptance checks. They are not proof that the original `Sprite`/`Seb`/`ResourceManager` semantics have been ported.

## Structural gaps before retirement

The direct manifest selector, projection helper, room-specific render plan, and selected Canvas draw code can only be retired or replaced after the recovered core produces identical source/fixture output and the scene pass order matches native traces. V0 does not delete or alter any of them.
