# V1 Parity Report

## Selected parity scope

The V1 parity ledger covers the selected real ZIP fixtures and synchronous runtime contracts. It records expected and actual stable evidence hashes, the test name, fixture references, status, and proof class in `parity-results.json`.

| Domain | Test | Expected = actual hash | Status |
| --- | --- | --- | --- |
| Sprite | `runtime/social-dev/tests/v1-sprite.test.ts` | `03ab4b23524da70b1955294b6f8399527aa40d61dad48cf1964d64958ac7264a` | `PASS` |
| Seb | `runtime/social-dev/tests/v1-seb.test.ts` | `9684a7710b3db9dc0574127df948c81717b615f4bf1517113ce3afe8fc3f21d6` | `PASS` |
| Image | `runtime/social-dev/tests/v1-image.test.ts` | `51f48cc2c29484583ef55319b91a6aaf7efbdd80d6ba6150e1eb1b9e92eb1ef5` | `PASS` |
| ResourceManager | `runtime/social-dev/tests/v1-resource-manager.test.ts` | `1a8979a178422fe809d3f20eea01c120307bb8715d9ce422fba0eda27782e2db` | `PASS` |

`PASS` is scoped to the selected evidence and contract behavior. It does not mean every native branch or every archive member is recovered.

## Checks performed

The Python evidence gate verifies canonical JSON hashes, real ZIP membership and source hashes, selected SEB/OPT contract hashes, native APK/dump provenance, parity boundaries, and the nine-field unknown register. The focused Vitest evidence test verifies that all eight JSON artifacts parse, native records carry provenance, the exact 11 resource groups remain present, the unsupported source boundary is explicit, and all four reports contain the V1/deferred/unknown/V2 disclosures.

## Deferred and unknown items

The parity scope deliberately leaves Seb depth-line payloads, Image `optimizeSeb`, Image raster `Resize`, Image atlas membership/regions, ResourceManager async scheduling, and unproven resource memberships as deferred or unknown. The selected standard OPT fixtures do not justify promoting `optimizeSeb`, and selected Image contracts retain atlas ID `-1` with no region.

The archive member `01_GAME_PACKS/develop/develop_menu_light.seb` is explicitly `NON_SELECTED_UNSUPPORTED`. This is a source boundary, not a hidden failure and not a claim that the member is invalid.

## Changed files and reproducibility

The V1 additions are isolated under `runtime/social-dev/src/v1/`, `runtime/social-dev/tests/`, `tools/social-dev/`, `knowledge/fixtures/accepted/visual-port/v1/`, and this report set. Existing renderer/source behavior is unchanged. Re-running the builder and Python gate must preserve the recorded deterministic hashes.

## V2 stop decision

V2 has not started. The next phase requires new evidence for at least one deferred or unknown branch; no deferred branch is treated as proven by this report.
