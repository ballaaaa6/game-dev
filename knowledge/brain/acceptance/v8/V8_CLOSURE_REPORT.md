# V8 Closure Report — Live Room0 Visual Reconstruction

Status: `PASS_V8_LIVE_ROOM0_VISUAL_RECONSTRUCTION`

Date: 2026-08-17

## Authority and reconciliation

`V8_Targeted_Implementation_Prompt.txt` was read in full before the Sol pack was extracted and inspected. The prompt SHA-256 is `652CE3C94C9D711DC6A8CB83D0FEA6DA1D7D2B8FBD4B0AAF41D872D3C81D02A0`. The Sol pack SHA-256 is `662309AD358D882D5633E3546AAD6D93647575A5749D7330AC19A8C9FBD7C077`.

The Sol pack was treated as an implementation hypothesis. All nine proposed gaps were reconciled against the current repository, canonical K4/K4.1 artifacts, and pinned local C# evidence. All nine were classified `CONFIRMED_CURRENT_GAP`; none were superseded or corrected after local inspection. The complete classification is recorded in `gap-classification.json`.

## Delivered V8 behavior

- `/` boots directly into the live Room0 reconstruction with three autonomous Staff, the source-backed door, desks, equipment, structural facilities, and full character catalog.
- The native nine-pass compositor preserves underlay-first ordering, row order, rear/foreground wall placement, fixed door visuals, and live nested workstation ownership.
- Raw directions use the exact prompt authority: `0=left`, `1=right`, `2=down`, `3=up`, with the required wait, typing, and movement selectors.
- Alpha bootstrap, fade-in/fade-out cadence, and hidden back-of-door behavior are projected from the pinned Staff contract.
- Workstation `FurnitureData(3)` uses the exact raw-direction 2 and 3 interleaves with `preview=false` and no duplicate Staff draw.
- Fukidashi payloads use `[id,40,delay,offsetY]`, source-backed pools, English localization, native lifetime/delay/draw guards, and the required `y - 20` anchor.
- Equipment visual phases project selectors `7/8` at frame 20, `15/16` at frame 40, and `11/12` at frame 60; product task ownership remains in the canonical LivingRuntime.
- No required fallback markers, unresolved selectors, comparison compositor path, renderer randomness, or debug route/ring output remain in the V8 Room0 path.

## Acceptance evidence

Browser smoke passed on the healthy existing repository server at `http://127.0.0.1:4173`:

- `/`: direct Room0 boot, visual gate pass, assets/source ready, three Staff, no title/login/tutorial, zero fallback markers, zero unresolved selectors, and zero console errors/warnings.
- `/?auto=0`: deterministic frame 0 with all three Staff at the door, alpha 0 and hidden.
- `/?auto=0&initialTicks=35`: deterministic frame 35 with all three Staff visible at their assigned workstations, exact workstation interleaves, 63/63 required visibility, zero occlusion, and zero fallback markers.
- Live observation reached the accepted invitation path and rendered the native English Fukidashi payload `id=24`, `Yes, yes...`, with the visual gate still passing.

The final local regression gates passed: typecheck, Vitest (`49 files / 323 tests`), production build, K2 unified brain validation, K4 visual closure validation, K4.1 targeted closure validation, V7, I1, I2, and `git diff --check`.

## Closure boundary

V8 changes are limited to the live web runtime, its V8 projection/compositor contracts, tests, and acceptance/state records. Source roots remain unchanged. Backend, persistence, authentication, cloud integrations, deployment, emulator/ADB, and network integration remain outside this phase. No next phase is authorized by this closure.
