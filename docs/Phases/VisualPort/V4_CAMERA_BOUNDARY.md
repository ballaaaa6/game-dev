# V4 Camera Boundary

V4 closes the minimum Camera transform required by the selected visual fixture without claiming a live camera implementation.

## Recovered fields and calls

The static C# and native evidence identify `ofx_`, `ofy_`, and `currentFloor_`. The recovered native calls are `SetPosition` (`0x1299BC8`, `0x1299BD0`), `GetX` (`0x1299DC0`), `GetY` (`0x1299ABC`), `GetBaseX` (`0x1299EAC`), and `GetBaseY` (`0x1299F30`).

The V4 boundary is integer translation only:

```text
screen.x = world.x + ofx_
screen.y = world.y + ofy_
```

The selected fixture uses offset `[0,0]`, identity scale, and zero rotation. A static test moves the offset to `[7,-9]` and verifies `[10,-4] → [17,-13]`.

## Deliberate limit

Viewport clamping, easing, dynamic floor transitions, scale, rotation, and other live camera state are not proven by the selected evidence. They are recorded as `CAMERA-VIEWPORT` in `knowledge/fixtures/accepted/visual-port/v4/unknowns.json` and deferred to V5. No camera behavior was added to the production renderer.
