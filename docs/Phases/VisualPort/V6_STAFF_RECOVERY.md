# V6 Staff visual recovery

Phase V6 is `PASS_STATIC` for the selected Staff display slice. The implementation is additive under `runtime/social-dev/src/v6/` and keeps the production renderer, scene resolver, and simulation unchanged.

The recovered surface is bounded by the native `Staff.Draw` / `DrawStaff` overload family, `StaffData.img_`, the `resHuman_` resource group, V1 SEB records, V2 command recording, and the native nine-pass Room contract. StaffData identity is selected by original numeric IDs; filenames remain catalog evidence rather than runtime authority.

Closed in V6:

- StaffData image selector binding for all 141 Staff records.
- Human wait, move, and typing selector maps for four directions.
- Talk as the source-backed typing display action.
- SEB frame selection, selected frame bounds, alpha visibility, and camera translation.
- Deterministic room:0 actor bootstrap for Staff 0–2 at the verified door position.
- Static insertion into the existing `avatar-primary` pass, before late foreground object passes.

The live Staff-to-Avatar relationship, full Staff.Init transition order, exact update cadence, alternate scale branches, gameplay behavior, and native compositor pixels remain explicitly source-limited or deferred to V7.

Evidence: `knowledge/fixtures/accepted/visual-port/v6/`; focused verification: `runtime/social-dev/tests/v6-staff.test.ts`.
