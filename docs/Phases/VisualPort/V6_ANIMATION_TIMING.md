# V6 Staff animation and visibility

V6 uses the V1 `Seb` frame contract and `ResourceManagerV3` numeric lookups. Selected human animations have a frame bound of 20. Frame state is an explicit non-negative integer normalized by `frame % Seb.getMaxFrame()`.

The source-visible typing interval is 3 and the end-typing/wait interval is 1. V6 exposes deterministic command fixtures at frame 0 and a source-bounded frame advance API. Exact native `Staff.Update` cadence and every transition branch remain deferred because the decompiled body is damaged and no live/native trace is permitted in this phase.

Room insertion preserves the native alpha-zero spawn. The isolated visible preview explicitly sets alpha to 255; the Staff fade-in boundary increments alpha by 25 and caps at 255. Partial alpha uses the recovered Graphics add-mode contract. Pixel-level compositor output remains `DEFERRED_TO_V7`.
