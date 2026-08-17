# First-visible final acceptance

Status: `FIX_REQUIRED`; stop at FS.16 and do not start V8.

Accepted in this gate:

- Static baseline remains green: focused V1–V7/MapChip/reintegration checks, full Vitest, typecheck, build, Python/static gates, JSON validation, and `git diff --check`.
- MapChip foundation is unchanged.
- V6 Staff semantics and the production renderer are unchanged.
- Room 0 bootstrap wall, door, workstation IDs/cells/directions, equipment IDs/cells, and Staff spawn coordinates are source-backed.
- No emulator, ADB, live app, local server, network, browser smoke test, new screenshot, subagent, or V8 work was used.

Not accepted:

- The tutorial/startup transition to the first stable `main_display` is not source-closed.
- Final first-visible workstation identity and post-bootstrap equipment persistence are not proven.
- Stable Staff action/direction/frame/alpha are not proven.
- Required first-visible staged previews, final structural PNG, final Staff PNG, contact sheet, and repeat hashes were not generated.

The correct disposition is `FIX_REQUIRED`, not a visual correction. The next permitted work is to recover FS-U01 through FS-U06 from source/native evidence, then rerun the manifest and render gate. V8 remains unopened.

Evidence: [checkpoint-ledger.json](../../../knowledge/fixtures/accepted/visual-port/first-visible-starter/checkpoint-ledger.json), [first-visible-semantic-diff.json](../../../knowledge/fixtures/accepted/visual-port/first-visible-starter/first-visible-semantic-diff.json), and [unknowns.json](../../../knowledge/fixtures/accepted/visual-port/first-visible-starter/unknowns.json).
