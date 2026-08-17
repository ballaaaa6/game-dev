#!/usr/bin/env python3
"""Validate the staged K2 unified brain and generated original runtime packs."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sqlite3
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "knowledge/brain/acceptance/k2"
BRAIN = ROOT / "knowledge/brain"
DERIVED = ROOT / "knowledge/generated"
DB = BRAIN / "sqlite/social_dev_brain.sqlite"
ORIGINAL_DATA_DB = ROOT / "knowledge/data/original/sqlite/social_dev_original_data.sqlite"
RUNTIME_PACK = ROOT / "runtime/social-dev/generated/original-runtime-pack.json"
OLD_DB_SHA = "9d561f7d5708c73b6b8a80acca10681f0323ec5a001145ed9c63215987d79d37"
EXPECTED_CHECKPOINTS = [
    "K2.PRE", "K2.0", "K2.1", "K2.2", "K2.3", "K2.4", "K2.5", "K2.6",
    "K2.7", "K2.8", "K2.9", "K2.10", "K2.11", "K2.12", "K2.FINAL",
]
REQUIRED_EXTENSIONS = {
    "artifact_blobs", "artifact_instances", "artifact_lineage", "artifact_references",
    "id_namespaces", "identity_values", "entity_aliases", "semantic_edges", "edge_claims",
    "edge_sources", "edge_revisions", "implementation_bindings", "acceptance_bindings",
    "usage_classification", "derived_artifacts", "gap_queue",
}
REQUIRED_RUNTIME_KEYS = {
    "actorCatalogJson", "actorBehaviorJson", "actorSpawnJson", "cameraCoordinateJson",
    "characterCapabilityJson", "characterAssetManifestJson", "characterMetadataJson",
    "displayAssetManifestJson", "objectCatalogJson", "preRuntimeClosureJson", "phase3cRenderJson",
    "roomPlacementJson", "sceneCatalogJson", "strictClosureJson", "tickOrderJson", "defaultMapChipJson",
    "roomSceneRuntimeJson", "nativeDirectionJson", "roomSceneAssetManifestJson", "roomRSceneJson",
    "nativeContentCatalogJson", "nativeSceneAssemblyJson", "nativeRoomFloorUsageJson",
    "assetMetadataRuntimeManifestJson", "i0RuntimeCatalogJson", "floor00SceneJson", "floor00DisplayPolicyJson",
    "floor00VisualLayoutJson", "fixtureManifestV1Json", "imageOptContractV1Json",
    "resourceLookupContractV1Json", "sebContractV1Json", "rasterFixtureManifestV2Json",
    "fixtureManifestV3Json", "groupMapV3Json", "imgIndexV3Json", "sebIndexV3Json",
    "packInventoryV3Json", "sebCatalogJson", "fixtureManifestV4Json",
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def fail(message: str, errors: list[str]) -> None:
    errors.append(message)


def validate_db(errors: list[str]) -> None:
    if not DB.exists():
        fail("canonical brain database missing", errors)
        return
    if not ORIGINAL_DATA_DB.exists() or sha256_file(ORIGINAL_DATA_DB).lower() != OLD_DB_SHA:
        fail("original G1.5 data database hash changed", errors)
    connection = sqlite3.connect(DB)
    try:
        tables = {row[0] for row in connection.execute("select name from sqlite_master where type='table'")}
        missing = sorted(REQUIRED_EXTENSIONS - tables)
        if missing:
            fail(f"missing K2 extension tables: {', '.join(missing)}", errors)
        expected = {
            "methods": 4478, "fields": 9147, "assets": 3542, "selectors": 3192,
            "calls": 5355, "field_access": 22059, "state_transitions": 83,
            "native_dispatch": 54, "event_edges": 79, "save_refs": 8010,
            "data_tables": 43, "data_rows": 3693,
        }
        for table, count in expected.items():
            actual = connection.execute(f'SELECT COUNT(*) FROM "{table}"').fetchone()[0]
            if actual < count:
                fail(f"{table} count {actual} is below required {count}", errors)
        namespaces = {row[0] for row in connection.execute("select namespace_id from id_namespaces")}
        required_namespaces = {"STAFF_DATA_ID", "JOB_DATA_ID", "SKILL_DATA_ID", "FURNITURE_DATA_ID", "ROOM_DATA_ID", "ROOM_FLOOR_ARGUMENT", "ROOMDATA_FLOOR_IMAGE_INDEX", "NATIVE_INDIRECTION_INDEX", "IMAGE_SELECTOR_ID", "SEB_SELECTOR_ID", "ASSET_ID", "SPRITE_ID", "SPRITE_FRAME_ID", "COMPATIBILITY_ALIAS_ID", "PRODUCT_AGENT_ID", "PRODUCT_TASK_ID", "PRODUCT_BINDING_ID"}
        if not required_namespaces.issubset(namespaces):
            fail("required namespaced identity domains are missing", errors)
        if connection.execute("select count(*) from legacy_row_migrations").fetchone()[0] < 50000:
            fail("legacy row migration ledger is unexpectedly small", errors)
        floor_edge = connection.execute("select count(*) from semantic_edges where subject_id='ROOMDATA_FLOOR_IMAGE_INDEX:5' and object_id='IMAGE_SELECTOR_ID:23' and status='verified'").fetchone()[0]
        if floor_edge != 1:
            fail("floor index 5 -> selector 23 namespaced edge missing", errors)
        unresolved = connection.execute("select count(*) from semantic_edges where subject_id='selector:floor:5' and status='unresolved'").fetchone()[0]
        rejected_direct = connection.execute("select count(*) from semantic_edges where subject_id='selector:floor:5' and status='rejected'").fetchone()[0]
        if unresolved != 1 and not (unresolved == 0 and rejected_direct >= 1):
            fail("direct selector 5 claim is neither retained as K2 unresolved nor explicitly rejected by the K3 closure", errors)
        product_mutations = connection.execute("select count(*) from product_bindings where mutation_allowed != 0").fetchone()[0]
        if product_mutations != 0:
            fail("product namespace contains a mutation binding", errors)
    finally:
        connection.close()


def validate_runtime_imports(errors: list[str]) -> None:
    allowed = "runtime/social-dev/src/catalog/load-original-runtime-pack.ts"
    direct = []
    for path in (ROOT / "runtime/social-dev/src").rglob("*.ts"):
        text = path.read_text(encoding="utf-8", errors="replace")
        if re.search(r"(?:from\s+|import\s*\()(['\"]).*\.json\1", text):
            relative = path.relative_to(ROOT).as_posix()
            if relative != allowed:
                direct.append(relative)
    if direct:
        fail("direct JSON imports remain outside the K2 pack facade: " + ", ".join(sorted(direct)), errors)
    facade = ROOT / allowed
    if not facade.exists():
        fail("runtime pack facade missing", errors)


def validate_outputs(pre_final: bool, errors: list[str]) -> None:
    required_files = [
        EVIDENCE / "source-reverification.json", EVIDENCE / "baseline.json", EVIDENCE / "preflight-current-delta.json", EVIDENCE / "upstream-authority-hash-lock.json", EVIDENCE / "checkpoint-ledger.json", EVIDENCE / "artifact-registry.json", EVIDENCE / "runtime-pack-cutover-scan.json", EVIDENCE / "post-cutover-regression-matrix.json", EVIDENCE / "pre-cutover-equivalence.json", EVIDENCE / "runtime-value-delta.json", EVIDENCE / "visual-value-delta.json",
        BRAIN / "schema/k2-unified-brain-v2.sql", BRAIN / "schema/id-namespaces.json", BRAIN / "graphs/semantic-edges.json", BRAIN / "reconciliation/reference-normalization.json", BRAIN / "reconciliation/family-ingestion.json", BRAIN / "reconciliation/entity-resolution.json", BRAIN / "reconciliation/reconciliation-status.json", BRAIN / "acceptance/query-results.json", BRAIN / "acceptance/acceptance-matrix.json", BRAIN / "exports/active-knowledge-surface.json", BRAIN / "exports/duplicate-content-map.json", BRAIN / "exports/retired-active-views.json", BRAIN / "exports/production-distillation-candidates.json", BRAIN / "exports/k3-gap-queue.json",
        DERIVED / "original-data-pack/manifest.json", DERIVED / "original-data-pack/schema.json", DERIVED / "original-data-pack/data.json", DERIVED / "original-runtime-pack/manifest.json", DERIVED / "original-runtime-pack/runtime-pack.json", DERIVED / "original-visual-pack/manifest.json", DERIVED / "original-visual-pack/visual-pack.json", RUNTIME_PACK,
    ]
    for path in required_files:
        if not path.exists():
            fail(f"required K2 output missing: {path.relative_to(ROOT).as_posix()}", errors)
    if (EVIDENCE / "source-reverification.json").exists() and load(EVIDENCE / "source-reverification.json").get("status") != "pass":
        fail("source reverification did not pass", errors)
    if (EVIDENCE / "baseline.json").exists() and load(EVIDENCE / "baseline.json").get("status") != "pass":
        fail("baseline regression matrix did not pass", errors)
    if (EVIDENCE / "post-cutover-regression-matrix.json").exists() and load(EVIDENCE / "post-cutover-regression-matrix.json").get("status") != "pass":
        fail("post-cutover regression matrix did not pass", errors)
    if RUNTIME_PACK.exists():
        pack = load(RUNTIME_PACK)
        if pack.get("status") != "pass" or pack.get("semantic_status") != "approved_for_runtime_catalog":
            fail("runtime pack is not approved", errors)
        if set(pack.get("runtime_catalogs", {})) != REQUIRED_RUNTIME_KEYS:
            fail("runtime pack contract key set differs from the frozen facade", errors)
    data_manifest = DERIVED / "original-data-pack/manifest.json"
    if data_manifest.exists():
        manifest = load(data_manifest)
        if manifest.get("table_count") != 43 or manifest.get("row_count") != 3693 or manifest.get("status") != "pass":
            fail("original data pack does not contain all 43 tables and 3693 rows", errors)
        for table, count in {"StaffData": 141, "JobData": 30, "SkillData": 36, "FurnitureData": 103}.items():
            if manifest.get("core_counts", {}).get(table) != count:
                fail(f"core data count missing for {table}", errors)
    queries = BRAIN / "acceptance/query-results.json"
    if queries.exists():
        values = load(queries).get("queries", {})
        for query_id in ("Q1_staffdata_to_render", "Q3_room_to_mapchip_objchip", "Q4_hp_home", "Q6_source_to_implementation_test", "Q7_product_isolation"):
            if values.get(query_id, {}).get("status") != "pass":
                fail(f"acceptance query {query_id} did not pass", errors)
        if values.get("Q2_furnituredata_to_render", {}).get("status") != "source_limited":
            fail("FurnitureData visual limitation was not retained", errors)
    active = BRAIN / "exports/active-knowledge-surface.json"
    if active.exists() and load(active).get("implementation_blockers") != []:
        fail("implementation blocker remains in active knowledge surface", errors)
    ledger_path = EVIDENCE / "checkpoint-ledger.json"
    if ledger_path.exists():
        ledger = load(ledger_path).get("checkpoints", [])
        by_name = {item.get("checkpoint"): item for item in ledger}
        needed = EXPECTED_CHECKPOINTS[:-1] if pre_final else EXPECTED_CHECKPOINTS
        for name in needed:
            if by_name.get(name, {}).get("status") != "pass":
                fail(f"checkpoint {name} is not pass", errors)
    else:
        fail("checkpoint ledger missing", errors)
    if not pre_final:
        final_path = EVIDENCE / "final-validation.json"
        if not final_path.exists() or load(final_path).get("final_validation_token") != "PASS_K2_UNIFIED_WHOLE_GAME_BRAIN_AND_RUNTIME_PACK_CLOSED":
            fail("final K2 pass token is missing", errors)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pre-final", action="store_true", help="validate all K2 outputs except the final token")
    args = parser.parse_args()
    errors: list[str] = []
    validate_db(errors)
    validate_runtime_imports(errors)
    validate_outputs(args.pre_final, errors)
    if errors:
        print("FAIL_K2_UNIFIED_WHOLE_GAME_BRAIN_AND_RUNTIME_PACK_CLOSED")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PASS_K2_UNIFIED_WHOLE_GAME_BRAIN_AND_RUNTIME_PACK_CLOSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
