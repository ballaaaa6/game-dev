# R0 HP, Work, and Interruption Contract

The authoritative machine contracts are:

- `hp-recovery-home-runtime-contract.json`
- `work-planning-runtime-contract.json`
- `interruption-resume-contract.json`

Ordinary work has no proven HP drain. Recovery starts after `20` frames, consumes one stock unit on native `frame % 3 == 0`, calls `RecoverHp(1)`, and resets the gauge/effect path at exhaustion with `frameToHideHpGauge_=40`. Low HP is `<=5%`; home recovery returns at `>=40%`.

Planning uses the source-backed `Player -> Room -> Staff` boundary. Equipment, talk, home, and desk-destruction paths preserve or clear only the fields supported by the canonical evidence. No dashboard task id is included.


R0 execution boundary: inline, static/contract only, no subagents, no emulator/ADB, no network, no server, no V8, no MapChip or Renderer changes, and no living-core implementation.
