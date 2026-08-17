# V4 MapChip Recovery

Phase V4 recovers the selected MapChip visual contract from the read-only C# slices, native method evidence, V3 numeric resource catalog, and a bounded `room:0` fixture. The result is an isolated adapter under `runtime/social-dev/src/v4/`; the production renderer is unchanged.

## Closed native surface

`MapChip` owns `index_`, `imageId_`, and `room_`, with native dimensions `WIDTH=80` and `HEIGHT=39`. The recovered native methods are `Draw` (`0x12A1B24`), `DrawFloor` (`0x12A1F38`), and `DrawExtentionFloor` (`0x12A20F4`). Image and SEB ownership remains with the `resChip_` resource group through V3 `ResourceManagerV3` and the original numeric IDs.

## Coordinate and floor contract

For cell `[x,y]` and Camera offset `[ofx,ofy]`, the MapChip origin is:

```text
origin.x = ofx + (x + y) * 40
origin.y = ofy + (y - x) * 20
```

The floor image is drawn at `origin.y + 39 - image.height`, preserving the native height anchor. The selected `14×14` floor window is `x=5..9` inclusive and `y=5..8` inclusive. The explicit source/data selector remains `85`; V4 does not relabel it as selector `5`.

## Selected visual resources

- Boundary `Draw` uses SEB selector `2`; the optional overlay selector `7` is retained in the contract and safely skipped when absent from the selected V3 fixture.
- The selected extension family uses SEB selector `63`, with frame `1` for verified vertical triggers and frame `0` for verified horizontal triggers.
- Each selected extension trigger emits two pieces with the native local offsets recorded in `mapchip-draw-contract.json`.
- Floor rendering uses a direct numeric image lookup and the explicit dimension fixture; no filename inference is introduced.

## Evidence and boundary

Machine-readable evidence is in `knowledge/fixtures/accepted/visual-port/v4/mapchip-native-map.json`, `mapchip-coordinate-contract.json`, `mapchip-draw-contract.json`, `fixture-manifest.json`, and `command-parity-results.json`. The full Room orchestration mode and damaged alternate extension branches are listed in `unknowns.json` and remain deferred to V5.
