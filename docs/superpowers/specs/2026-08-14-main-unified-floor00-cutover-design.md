# Unified Main Runtime Cutover Design

**Status:** Draft for user review

## Goal

Make `main` the single active Social Dev runtime stream. The current approved
data, catalogs, assets, character metadata, room records, native contracts, and
floor00 presentation must be available through that one runtime. `floor00` is
the canonical main presentation; the old comparison/preview entrypoints and
their duplicate routing branches are removed.

## Scope interpretation

“Bring every current data set into main” means consolidate the existing
approved runtime inputs and capabilities into one application entrypoint. It
does not mean drawing all 18 rooms simultaneously or deleting provenance.
Evidence, contracts, source-derived metadata, and binaries that the unified
runtime or its verification gates use remain intact. The deletion boundary is
the redundant route/mode/task surface, not the data itself.

## Design

### 1. One canonical entrypoint

The root URL `/` always creates the main runtime with the following fixed
context:

```text
scene = floor00
room = room:0 by default
nativeFloor = 0
context = main_display
```

The existing in-page room selector remains part of main so all current room
records can be inspected without creating a second route or workstream. The
full catalog loader remains the single data boundary; no current approved
catalog is replaced by a floor00-only subset.

### 2. Remove alternate runtime streams

Remove the production routing and behavior branches that make
`display-slice-01`, persistent-room, addition-floor-preview, or explicit
scene-mode query paths separate runtime streams. Main owns the renderer,
diagnostics, room selection, character/asset lookup, and current contract
projection.

Historical labels may remain inside evidence filenames and reports when they
are needed for provenance. They must not remain as selectable production
entrypoints or as the default scene policy.

### 3. Preserve approved data and native boundaries

The cutover must preserve:

- the complete native content/catalog data already loaded by
  `loadRuntimeCatalogs`;
- all 18 room records and their raw ObjChip/MapChip/native wall-door data;
- the full human/HelperData metadata boundaries and promoted assets;
- the approved floor00 scene, visual-layout, lifecycle, render-order, and
  asset contracts;
- the unresolved red/black prop exclusion and floor-selector alias policy.

No missing binding is guessed and no raw evidence is rewritten. The floor00
route remains static where its current contract requires a static comparison
presentation; preserving the current simulation APIs does not silently change
that native policy.

### 4. Delete only redundant code and checks

After reference scanning, remove or collapse only code, UI controls, tests,
and documentation whose sole purpose is the deleted alternate runtime stream.
Assets and contracts are removed only when the scan proves that the unified
main runtime and all retained gates no longer reference them. Existing
evidence is retained rather than recreated or silently discarded.

### 5. Verification-first migration

Before implementation code changes, add failing regression assertions for:

1. `/` resolving to the floor00/main projection;
2. the unified runtime retaining the current catalog/room counts;
3. old scene/context query values not creating alternate production streams;
4. the in-page room data remaining reachable from main;
5. the unresolved prop and floor alias boundaries remaining unchanged.

Then implement the smallest cutover, run the focused tests, and run the full
runtime test suite, TypeScript typecheck, production build, browser smoke, and
visual gate. The browser gate must report no console errors or warnings.

## Acceptance criteria

- Opening `/` displays the approved floor00 main scene without a special query.
- All currently approved runtime data remains loaded and queryable through the
  main runtime/catalog boundary.
- There is one production runtime stream; `display-slice-01` and preview
  modes are no longer selectable alternate entrypoints.
- The main in-page room selector still reaches all current room records.
- No source/evidence/provenance contract required by main is deleted or
  rewritten.
- The intentional unresolved red/black prop exclusion remains explicit.
- Focused regression tests, full Vitest, typecheck, build, browser smoke, and
  the floor00 visual gate pass.

## Non-goals

- Do not render every room at once.
- Do not delete the native evidence boundary or reconstruct the removed legacy
  archive.
- Do not invent the unresolved prop binding.
- Do not change raw native topology, selector provenance, or floor alias
  semantics as part of the routing cutover.
