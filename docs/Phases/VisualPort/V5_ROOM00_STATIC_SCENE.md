# V5 Room:0 Static Scene

The room:0 fixture is the selected full static scene. It uses Floor A, `Room.floor_ = 0`, the native 14x14 map topology, wall selector `6`, door selector `7`, and the existing integer camera offset `[0,0]`.

Initialization emits six explicit native FurnitureData bindings: three `furniture:3` compound bindings at `[2,4]`, `[3,4]`, and `[6,4]`, then direct-image bindings for `furniture:12` at `[8,5]`, `furniture:26` at `[8,6]`, and `furniture:56` at `[2,7]`. It also emits the two source-proven `furniture:0` structural facilities anchored at `[4,2]` and `[7,2]`, using SEB `11` and image `18`.

The door is the raw type-5 cell `[8,4]`, with FurnitureData `null` and installed flag `1`. Rear wall cells use the recovered vertical/horizontal predicates; the late wall slot contains only `[8,7]` and `[8,8]`.

The deterministic command manifest contains 74 commands, 59 traces, and 788 orchestration events. Its stable serialization is 193,917 bytes with SHA-256 `4418a7c8a81a705d46a6eefc2a72e635f5e6108d83e4067dc0d638942f39f788`. This is static command/call-flow parity, not a screenshot or pixel claim.
