# V7 room:0 render

## Status

`PASS_STATIC`

The deterministic V7 scene canvas is `640 x 480`, transparent RGBA, with world origin offset `{ x: 160, y: 160 }`. The renderer consumes the existing V5/V6 command streams and uses source-backed selected images only.

## Structural room:0

- Source phase: V5.
- Stream: 74 commands, 59 traces, 788 events.
- Raster draw count: 53; skipped transparent/off-canvas draw count: 21.
- Nontransparent bounds: `x=196, y=74, width=444, height=165`.
- Pixel SHA-256: `ecb9ec7d5f56a75b6e29044896ba1e3036bf92a9a2fee3c97833842bb168f27b`.
- PNG SHA-256: `574492baa161e195fabe16bb7848da2c392f5ad4102d8806a828e67648471b3d`.
- V5 command SHA-256: `51f69c307338fa7fe89a3d9785bc9e76e20a8863ce3f79bb74b2b8d4fc458fd6`.
- V5 manifest SHA-256: `4418a7c8a81a705d46a6eefc2a72e635f5e6108d83e4067dc0d638942f39f788`.

## room:0 + Staff

- Source phase: V6.
- Selected state: `wait`, `right`, frame `0`, alpha `255`.
- Stream: 77 commands, 62 traces, 791 events.
- Raster draw count: 56; skipped transparent/off-canvas draw count: 21.
- Nontransparent bounds remain `x=196, y=74, width=444, height=165`.
- Pixel SHA-256: `9f9d6df2828aa99e94c9158789bb5cf03bef680e5fcca67968cd8d89e295685c`.
- PNG SHA-256: `3793515941d6dc6c10079cf20e1d0908f9c1b55619c9c0a97019908ebed9e6ff`.
- V6 manifest SHA-256: `bfab918ef5ea04512da380b4d5134c4b02d1d7ca29fd9c6fb47d7b4e40944142`.

The complete records are [room00-structural-render.json](../../../knowledge/fixtures/accepted/visual-port/v7/room00-structural-render.json) and [room00-with-staff-render.json](../../../knowledge/fixtures/accepted/visual-port/v7/room00-with-staff-render.json). The PNGs are generated static artifacts under `knowledge/fixtures/accepted/visual-port/v7/previews/`; they are not runtime screenshots.

## Selector boundary

The floor is recorded as raw selector `5`, selected runtime alias `85`, and `floor_05.png`. This remains an explicit `PRODUCT_POLICY` compatibility alias, as required by the V5 evidence chain.
