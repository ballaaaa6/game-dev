# V6 static parity report

V6 command parity is `PASS_STATIC`; it is not pixel parity.

The room:0 visible fixture uses three Staff actors with explicit `wait/right/frame0/alpha255` state. The V5 baseline is 74 commands, 59 traces, and 788 events. The integrated V6 manifest is 77 commands, 62 traces, and 791 events. The stable SHA-256 of the generated manifest is:

`bfab918ef5ea04512da380b4d5134c4b02d1d7ca29fd9c6fb47d7b4e40944142`

The added commands use the `resHuman_` group and each selected StaffData image slot. Their order is bounded by the native `avatar-primary` pass. Exact native raster/compositor pixels, full animation cadence, and live Staff-to-Avatar linkage are not claimed.

Focused tests pass with 23 tests. The full V1–V5 regression, typecheck, build, JSON/Python validation, source-boundary audit, and diff checks are recorded in the V6 progress handoff.
