# V4 Fixture Matrix

The V4 matrix is static-only and uses original numeric resource IDs from the V3 `resChip_` catalog plus explicit dimensions and source rectangles. Every row below is covered by the focused V4 tests and/or the command parity ledger.

| fixture | input | expected static result | proof |
| --- | --- | --- | --- |
| MapChip floor | cell `[5,5]`, image `85`, room `14×14` | one direct image command at `[400,0]`, `80×39` | native code + command parity |
| MapChip vertical extension | cell `[4,5]` | two SEB `63` calls, frame `1` | native code + focused test |
| MapChip horizontal extension | cell `[2,5]` | two SEB `63` calls, frame `0` | native code + focused test |
| ObjChip wall intersection | cell `[8,1]`, raw type `0` | SEB `5`, frames `[1,0]`, four image commands | native code + focused test |
| ObjChip door | cell `[8,4]`, raw type `5` | SEB `6`, image `7`, one command, no FurnitureData | native code + focused test |
| Furniture 3 | cell `[2,4]`, raw type `2` | SEB `1` + SEB `3`, images `3` + `4`, two commands | static command parity |
| Furniture 12 | cell `[8,5]`, raw type `1` | direct image `109`, crop `24×22`, offset `[-12,-19]` | static command parity |
| Furniture 26 | cell `[8,6]`, raw type `1` | direct image `106`, crop `23×26`, offset `[-11,-23]` | static command parity |
| Furniture 56 | cell `[2,7]`, raw type `1` | direct image `127`, crop `24×28`, offset `[-12,-25]` | static command parity |
| Directions | raw `0..3` | exact vector/reverse table preserved | native code + focused test |
| Camera | offset `[7,-9]` | integer translation only | call-flow proof + focused test |
| Selector sentinels | catalogue fixtures `0`, `1`, `2`, `5` | negative `subSeb_`/`img_` remain sentinels | source-data proof + focused test |

The complete numeric records and provenance are in `knowledge/fixtures/accepted/visual-port/v4/fixture-manifest.json`; observed commands are in `command-parity-results.json`. The matrix is intentionally not a full-room or full-catalogue acceptance set.
