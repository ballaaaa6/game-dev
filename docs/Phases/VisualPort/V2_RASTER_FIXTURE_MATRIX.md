# V2 Raster Fixture Matrix

The fixture matrix separates deterministic command composition from pixel parity. Source membership comes from the V1 resource/SEB contracts. Static/native dispatch is the accepted proof for this continuation; final pixel parity remains deferred because `_drawBitmap` output is not present in the static evidence and runtime proof is out of scope.

| Fixture | Group / SEB | Source image evidence | Command composition | Static pixel proof |
| --- | --- | --- | --- | --- |
| chair_00 | `resChip_` / id `3` | V1 logical Image id `4`, source `chair_00.png` | `PASS`; multi-frame and translation exercised | `DEFERRED` |
| desk_00 | `resChip_` / id `1` | V1 logical Image id `3`, source `desk_00.png` | `PASS`; translation fixture | `DEFERRED` |
| wall_00 | `resChip_` / id `5` | source-slot id `6`, source PNG `96x43` | `PASS`; multi-layer order and `TEXID_NONE` skip | `DEFERRED` |
| door_02 | `resChip_` / id `6` | source-slot id `7`, proven association to `door_01.png` | `PASS`; one-layer fixture | `DEFERRED` |
| wait_left | `resHuman_` / id `11` | source-slot id `0`, `chara00.png` `270x60` | `PASS`; ReverseU state/reset | `DEFERRED` |
| wait_right | `resAvatarBody_` / id `0` | `m_00.png` source membership known, promoted image/dimensions unavailable | `DEFERRED` | `DEFERRED` |

## Fixture proof classes

- `PASS` means the runtime emits the native-proven command/state sequence from V1 records.
- `DEFERRED` in the pixel-proof column means the static evidence does not contain final backend pixels and runtime proof is outside the current scope.
- `DEFERRED` in the command column means a required source image or native payload is not available; no placeholder image is introduced.

The machine manifest is `knowledge/fixtures/accepted/visual-port/v2/raster-fixture-manifest.json`. It records image dimensions only where they are proven by a V1 logical contract or extracted source PNG. It does not claim that those dimensions reproduce native shader sampling.

## Static-only continuation boundary

The available fixtures remain useful for source membership, dimensions, SEB layer order, translation, flip state, and command geometry. Do not capture native or browser frames for this phase. Continue only by reconciling decompiled call sites, pinned native disassembly, dump/metadata layouts, and static SEB/OPT/PNG/INF formats. Keep native/browser output hashes null and do not promote Canvas sampling, filtering, alpha, transformed clipping, primitive, depth, anchor, or rotated-pixel behavior.
