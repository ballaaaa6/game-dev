# V7 animation fidelity

## Status

`PASS_STATIC_BOUNDARY`

V7 carries forward the V6 Staff static contract. The selected fixture is three Staff actors in `room:0`, action `wait`, direction `right`, frame `0`, alpha `255`. The source-proven selected variants include wait, typing, left/right direction resolution, frame selection, and the deterministic alpha-128 compatibility fixture.

## Closed static facts

- Wait interval is `1`; typing interval is `3`.
- Action and direction changes reset the selected frame state.
- The integrated room fixture contains actor IDs `actor:staff:0`, `actor:staff:1`, and `actor:staff:2`.
- The selected Staff draw is in the V5/V6 `avatar-primary` placement slot.
- The V6 integrated manifest remains `bfab918ef5ea04512da380b4d5134c4b02d1d7ca29fd9c6fb47d7b4e40944142`.

These facts are recorded in [staff-cadence-contract.json](../../../knowledge/fixtures/accepted/visual-port/v7/staff-cadence-contract.json) and the V6 evidence under `knowledge/fixtures/accepted/visual-port/v6/`.

## Source-limited boundary

The complete native `Staff.Update` cadence, gameplay route/talk/work transitions, hidden initial SEB state, and live timing remain `SOURCE_LIMITED`. V7 does not infer those values from historical screenshots or simulate gameplay. The selected frame/action fixtures are deterministic and nonblocking for the static room:0 + Staff render.

## Raster evidence

The fixture set includes `staff.0_wait_right`, `staff.0_wait_left`, `staff.0_typing_right`, and `staff.alpha_128`. Their exact pixel and PNG hashes are recorded in [golden-fixture-results.json](../../../knowledge/fixtures/accepted/visual-port/v7/golden-fixture-results.json). Native timing and native compositor bytes remain separate proof classes.
