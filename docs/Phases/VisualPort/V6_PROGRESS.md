# V6 progress and handoff

## Status

`PASS_STATIC_STOP_BEFORE_V7`

V6 is complete for the bounded Staff / StaffData / human animation / room:0 integration scope. The work stayed inline-only and static-only. No subagents, emulator, ADB, live app, network, server, screenshot proof, gameplay simulation, or production cutover was used.

## Delivered

- Isolated implementation: `runtime/social-dev/src/v6/`.
- Focused tests: `runtime/social-dev/tests/v6-staff.test.ts`.
- Machine evidence: `knowledge/fixtures/accepted/visual-port/v6/`.
- Static reports: `docs/Phases/VisualPort/V6_*.md`.
- Deterministic room:0 + Staff manifest summary with 77 commands, 62 traces, 791 events, and SHA-256 `bfab918ef5ea04512da380b4d5134c4b02d1d7ca29fd9c6fb47d7b4e40944142`.

## Closed boundary

StaffData image selectors, resHuman_ numeric selection, wait/move/typing directional SEBs, talk-to-typing mapping, raw direction/reverse semantics, selected SEB frame state, source-derived placement, camera offset, room pass placement, rear/foreground occlusion, room:0 bootstrap, and deterministic command output are closed for the selected static fixtures.

## Remaining explicit unknowns

Native Staff.Init hidden initial selector, exact Staff.Update cadence, reserved-SEB transition traces, alternate scale branches, live Staff-to-Avatar linkage, gameplay behavior, and native pixel/compositor output remain source-limited or deferred. None blocks the selected static fixture contract; exact pixels and cadence remain V7 work.

## Stop condition

Do not start V7 automatically. The next phase requires a separate user-directed decision and must preserve the V6 static contracts.
