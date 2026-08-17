# First-Visible Starter-State Forensic Investigation Plan

## Objective

Recover the first stable starter-room state shown after NewGame/tutorial initialization from source-backed call flow and static asset contracts. Keep the accepted MapChip foundation, V6 action/selector semantics, production renderer, and V8 boundary unchanged.

## Investigation sequence

1. Establish the static baseline: rerun V1–V7, MapChip forensic, and starter-room reintegration checks, then typecheck, build, required Python/JSON gates, and `git diff --check`.
2. Enumerate the distinguishable room states from raw `RoomData(0)` through constructor, NewGame bootstrap, AddStaff spawn, tutorial/startup mutations, and first stable `main_display`; record only source-proven transitions.
3. Trace `AppData.NewGame` → `Room` setup → facilities/furniture → Staff → tutorial/main-display preparation, including source line/RVA references and before/after state where recoverable.
4. Build the complete first-visible inventory, then resolve wall family/layers, door identity/state, workstation identities/orientations, equipment, and Staff stable placement. Keep unresolved items explicitly `SOURCE_LIMITED`.
5. Compare the current reintegration manifest with the recovered first-visible manifest. Apply only the smallest source-backed corrections; stop before full-room rendering if workstation orientation or another required identity remains unproven.
6. Generate staged previews and deterministic final renders only after the manifest is justified. Verify MapChip immutability, repeat hashes, structural sanity, production-renderer unchanged, and V8 not started.

## Acceptance boundary

The gate may pass only when the first-visible boundary, wall family, door state, workstation IDs/directions, equipment status, and Staff stable positions are source-backed or explicitly source-limited; no screenshot-derived numeric tuning or hand-authored scene is allowed. The final status will be one of the user-specified first-visible outcomes, and work stops at FS.16.
