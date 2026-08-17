# V3 Index and Fixture Report

The original ZIP is pinned at SHA-256 `c4b6ac1b6603eb8e2d7ac78e7dd3b8bffb40b7c30fe036cb644bea701087b283`. Evidence is generated from pack-local `img.inf`/`seb.inf` rows and the existing decoded SEB catalog; source roots remain read-only.

## Declared-group index coverage

The ten source-backed declared packs contain these index sizes:

| Pack | `img.inf` rows | `seb.inf` rows | Notable boundary |
| --- | ---: | ---: | --- |
| chip | 153 | 60 | sparse IDs; furniture and wall/door selectors |
| human | 105 | 35 | human image IDs 0–104; wait-left SEB ID 11 |
| com | 279 | 222 | duplicate `wnd_conner.png` IDs 5 and 19 |
| game | 64 | 57 | image gaps 1, 2, 4 and other sparse IDs |
| effect | 16 | 17 | `effect00` source-indexed image/SEB fixture; other effect payloads remain available in the pack inventory |
| meeting | 14 | 10 | hit-effect image ID 2 / SEB ID 0 |
| avatar_body | 116 | 2 | child image IDs 300–303 remain exact source IDs |
| avatar_head | 168 | absent | image-only source index; dynamic head selector remains partial |
| develop | 47 | 45 | enemy-attack-timing fixture |
| window | 6 | 6 | install-bonus fixture |

`resInterface_` has no proven pack-local index and remains `DECLARED_ONLY`. The generated index files retain every gap; no density repair is performed.

## Real fixtures

The declared-group fixture set includes chip chair/desk/wall/door, human wait-left, common-window, game cloud-day, effect bright, meeting hit-effect, avatar-body wait-right, avatar-head face-m-00, develop enemy-attack-timing, and window install-bonus. Additional named owners include title-menu and recruit-hope-join-back. Each selected SEB carries its decoded source contract and each positive `TexId` resolves within the same pack-local image namespace.

The chip wall fixture also records decoded `TEXID_NONE (-1)` as a sentinel. It is not converted into an image lookup and is not treated as an unexplained missing member. The common-window fixture records the duplicate same-file alias: its selected SEB uses `TexId 19`, while AppData’s `RESCOM_IMG_WNDCORNER` selector is ID 5; both IDs point to the same pack-local filename and remain distinct slots.

Machine-readable outputs:

- `knowledge/fixtures/accepted/visual-port/v3/fixture-manifest.json`
- `knowledge/fixtures/accepted/visual-port/v3/image-seb-association.json`
- `knowledge/fixtures/accepted/visual-port/v3/img-index-contract.json`
- `knowledge/fixtures/accepted/visual-port/v3/seb-index-contract.json`
