# Task 3 report: resolve floor, resource, and layer identity

Status: DONE_WITH_CONCERNS

## Scope and output

Task 3 added an evidence-first resolver and generated:

- `tools/scene_reconstruction/resource_relations.py`
- `tools/scene_reconstruction/build_resource_contract.py`
- `tools/scene_reconstruction/test_resource_relations.py`
- `knowledge/world-assets/evidence/scene_reconstruction/resource_contract.json`

The resolver uses the required priority, in order:

1. exact archive/resource identity → `verified`
2. loader/selector identity → `verified`
3. same-stem-only relation → `candidate`
4. absence or conflict → `unknown`

All generated claims use exactly `verified`, `candidate`, or `unknown`.

## Resolved inventory

The generated contract contains 51 distinct resources:

- 3 `game/` base room backgrounds, each with verified catalog role and dimensions
- 22 office SEB sprite-descriptor nodes, retained as independent resources
- 25 office room-background atlas nodes, each with verified catalog/INF role and dimensions
- 1 `game/floorparts0.png` room-parts/cover node, retained separately from both floor0 PNG nodes

The contract preserves source member paths, source inventory size/hash/mtime records, catalog records, dimensions where available, and legacy INF selector records. It does not infer collision, walkability, seats, pivots, anchors, depth, placement, or world transforms.

## Relation results

There are 24 generated PNG-to-SEB relations:

- 23 `candidate / same_stem_only`
- 1 `unknown / no_identity_evidence` for the unnumbered `office/floor.seb` node
- 0 promoted to `verified` from a same-name join

This deliberately keeps these nodes separate: `game/floor0.png`, `game/floorparts0.png`, `office/floor0.png`, and `office/floor0.seb`. The verified roles of the PNGs come from catalog/INF evidence, not from a name-only PNG-to-SEB join. The SEB audit remains preserved on the contract; its discovered floor SEBs are incomplete four-byte-short candidates and did not supply an exact complete archive/resource identity.

## Known gaps and conflicts

The contract records the four known office floor PNGs without same-name SEB resources:

- `office/floor13.png` → missing `office/floor13.seb`
- `office/floor2.png` → missing `office/floor2.seb`
- `office/floor4.png` → missing `office/floor4.seb`
- `office/floor9.png` → missing `office/floor9.seb`

No missing pair was promoted from the shared numeric suffix. No current evidence proves that a same-stem office SEB is the unique owner of an office PNG; that relation remains a candidate pending exact archive/resource or explicit loader/selector evidence.

## Evidence inputs

The builder consumes and records:

- `knowledge/world-assets/evidence/scene_reconstruction/source_inventory.json`
- `knowledge/world-assets/evidence/scene_reconstruction/seb_audit.json`
- `knowledge/world-assets/evidence/phase1_asset_catalog.json`
- `knowledge/world-assets/evidence/phase1_legacy_asset_map.json`
- `knowledge/world-assets/evidence/phase1_seb_manifest.json`
- `knowledge/world-assets/evidence/office_manifest.json`
- loader/resource-name discovery matches under `knowledge/csharp/primary/` and the read-only dumped code roots

The generated contract retains loader text matches as discovery evidence, but does not promote them to ownership unless the caller supplies an explicit selector identity.

## Verification

Focused tests pass: 6 tests. The test-first RED run was captured before implementation as an import failure for the missing resolver module. The focused suite, full Python unittest discovery, `py_compile`, and contract generation were then run successfully.

No local server was started. Runtime files, source/extraction roots, manifests, and animation code were not modified.
