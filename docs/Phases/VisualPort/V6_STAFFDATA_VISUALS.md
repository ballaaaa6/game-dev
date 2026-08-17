# V6 StaffData visual selectors

`StaffData.img_` is the base human image selector. V6 validates the selector against both `render.image_selector.id` in `character_metadata_contract.json` and `staff_bindings[].image_selector_id` in `character_asset_manifest.json`.

The selected `resHuman_` image is substituted only when a human SEB sprite carries `TexId == 0`, matching the native Staff draw surface. Positive texture IDs remain group-local numeric IDs. No human filename is hard-coded in the runtime.

The contract covers all 141 StaffData records and uses Staff 0, 1, 2, 3, and the source-backed variant record 100 as evidence fixtures. Room bootstrap draws Staff 0–2; records outside the selected room fixture remain catalog-addressable without being inserted into the scene.

See `staffdata-visual-contract.json` and `staff-fixture-manifest.json` for the machine-readable contract.
