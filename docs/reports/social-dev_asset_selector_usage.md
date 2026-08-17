# Social Dev selector usage and data-field semantics

AM-3 converts selector IDs and data fields into explicit lookup/call contracts. It preserves native IDs, `-1` sentinels, unresolved helper scope, and the Room floor indirection instead of flattening them into guessed asset names.

## Identity

- Selector matrix hash: `0c0c04da2c4eb3ec3acd86c3f14f0d42af4a65b688e8cfade38b0995811ed4b2`
- Field matrix hash: `e2f2f5880a198261f182cc8fef8792151e3bf32b5a586e68b3673bec909aa8ad`
- Contract hash: `43a7ceac713e29e6d3a121fba47f11e2e72f2030dda8a9b980e921d376778590`

## Counts

| Dimension | Count |
|---|---:|
| Selectors | 3,192 |
| Selectors with data relations | 267 |
| Selectors with consumer methods | 66 |
| Unresolved selectors | 1 |
| Data fields | 1,063 |
| Selector-bearing fields | 8 |
| Fields with consumer evidence | 8 |
| Fields with deferred selector scope | 9 |

## Closed field contracts

| Field | Role | Disposition | Call contract | Sentinel/indirection policy |
|---|---|---|---|---|
| `FurnitureData.img_` | furniture_direct_image_selector | `direct_selector` | `furniture_direct_image` | -1 means absent_by_sentinel; nonnegative values require resolution |
| `FurnitureData.seb_` | furniture_primary_animation_selector | `direct_selector` | `furniture_primary_animation` | nonnegative_requires_resolution; -1 is not present in the closed FurnitureData seb_ rows |
| `FurnitureData.subSeb_` | furniture_secondary_animation_selector | `direct_selector` | `furniture_secondary_animation` | -1 means absent_by_sentinel; nonnegative values require resolution |
| `HelperData.img_` | helper_image_selector | `direct_selector` | `helper_image` | -1 may be absent; human-scope values require an explicit helper selector-scope contract |
| `RoomData.doorImgId_` | room_door_image_selector | `direct_selector` | `room_door_image` | nonnegative requires resolution |
| `RoomData.floorImgId_` | room_floor_indirect_selector | `indirect_selector` | `room_floor_image_indirection` | nonnegative value indexes Room.FLOOR_IMAGE_ID_ARRAY; no silent direct-id interpretation |
| `RoomData.wallImgId_` | room_wall_image_selector | `direct_selector` | `room_wall_image` | nonnegative requires resolution |
| `StaffData.img_` | staff_human_image_selector | `direct_selector` | `staff_human_image` | nonnegative requires resolution; all closed StaffData rows resolve |

## Usage statuses

| Status | Count |
|---|---:|
| `resolved_data_referenced_not_runtime_promoted` | 129 |
| `resolved_runtime_referenced` | 138 |
| `resolved_unreferenced_by_closed_data_relations` | 2,924 |
| `unresolved_identity` | 1 |

## Boundary

- Selector lookup is now deterministic by `(resource_scope, selector_kind, selector_id)`.
- Selector lookup does not authorize drawing; composition/frame/geometry remains AM-4.
- Fields without a current selector relation have an explicit disposition, including candidate visual fields whose selector scope remains open.

```powershell
python -B tools/social-dev/build_asset_selector_usage_matrix.py
python -B tools/social-dev/test_asset_selector_usage_matrix.py
```
