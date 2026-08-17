# V4 FurnitureData Visual Binding

V4 recovers the visual selector binding boundary between `FurnitureData.Load`, ObjChip records, and the selected native world composition. The recovered binding is explicit and fixture-backed; the damaged catalogue `FurnitureData.Draw` body is not treated as world-render proof.

## Load and selector contract

`FurnitureData.Load` assigns fields in this order: `id_`, `name_`, `category_`, `seb_`, `subSeb_`, `img_`, `width_`, `height_`, `offsetX_`, `offsetY_`, `price_`, `sellPrice_`, `isBuy_`, `isSell_`, `description_`, and `passMap_`. V4 preserves the three visual selectors independently:

- `seb_` selects the primary SEB.
- `subSeb_` selects the optional secondary SEB.
- `img_` selects the data image, including its negative sentinel.

The static metadata contains 103 resolved primary SEBs, 23 resolved secondary SEBs, and 96 resolved data images; negative sentinels remain explicit. Numeric resource lookup is group-local to `resChip_`.

## Selected native bindings

| object | cells | raw type | primary | secondary | data image | visual route |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| furniture 3 | `[2,4]`, `[3,4]`, `[6,4]` | 2 | 1 | 3 | 148 | primary SEB + secondary SEB |
| furniture 12 | `[8,5]` | 1 | 21 | -1 | 109 | direct image 109 |
| furniture 26 | `[8,6]` | 1 | 21 | -1 | 106 | direct image 106 |
| furniture 56 | `[2,7]` | 1 | 21 | -1 | 127 | direct image 127 |

Furniture 3 is closed with primary image 3 and secondary image 4 frame records and their exact destination offsets. Furniture 12, 26, and 56 are closed with direct image crops and offsets from `fixture-manifest.json`.

## Safety boundary

V4 preserves selector identity and sentinels, rejects unsupported generic composition, and never maps a raw ObjChip type directly to a FurnitureData record. Catalogue/UI rendering remains unknown and is deferred to V5. Evidence is in `furniture-visual-binding.json`, `fixture-manifest.json`, and `command-parity-results.json`.
