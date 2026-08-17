"""Regression checks for the static Social Dev G0/G1 knowledge-base build."""

from __future__ import annotations

import json
import sqlite3
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_game_knowledge_g0_g1 as builder  # noqa: E402


def read_jsonl(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def main() -> int:
    identity = json.loads((builder.KB / "source_identity.json").read_text(encoding="utf-8"))
    assert identity["status"] == "PASS_SOURCE_IDENTITY"
    assert identity["hashes"]["apk"] == builder.EXPECTED_APK_SHA256
    assert identity["hashes"]["libil2cpp"] == builder.EXPECTED_NATIVE_SHA256
    assert identity["hashes"]["global_metadata"] == builder.EXPECTED_METADATA_SHA256
    assert identity["hashes"]["dump"] == builder.EXPECTED_DUMP_SHA256
    assert identity["source_counts"]["tier_a_files"] == 89
    assert identity["source_counts"]["raw_total_files"] == 5568
    assert identity["source_counts"]["raw_cs_files"] == 5504

    check = builder.check_outputs()
    assert check["status"] == "PASS_GAME_KNOWLEDGE_OUTPUT_CHECK"

    key_by_file = {
        "source_scope.jsonl": "source_id", "types.jsonl": "entity_id", "fields.jsonl": "entity_id", "methods.jsonl": "entity_id",
        "calls.jsonl": "call_id", "field_access.jsonl": "access_id", "data_table_slot_map.jsonl": "slot_id", "data_rows.jsonl": "row_id",
        "save_refs.jsonl": "save_ref_id", "assets.jsonl": "asset_id", "ui_commands.jsonl": "command_id", "native_dispatch.jsonl": "dispatch_id",
        "unknown_gaps.jsonl": "gap_id", "canonical_entities.jsonl": "entity_id", "canonical_facts.jsonl": "fact_id", "fact_claims.jsonl": "claim_id",
        "fact_sources.jsonl": "fact_source_id", "fact_revisions.jsonl": "revision_id", "superseded_facts.jsonl": "superseded_fact_id", "conflicts.jsonl": "conflict_id",
    }
    for name in builder.REQUIRED_JSONL:
        rows = read_jsonl(builder.JSONL / name)
        key = key_by_file[name]
        if rows:
            assert len({row[key] for row in rows}) == len(rows), (name, key)

    connection = sqlite3.connect(builder.SQLITE_PATH)
    assert connection.execute("SELECT COUNT(*) FROM data_table_slot_map").fetchone()[0] == 43
    assert connection.execute("SELECT COUNT(*) FROM data_tables").fetchone()[0] == 43
    assert connection.execute("SELECT SUM(row_count) FROM data_tables").fetchone()[0] == 3693
    assert connection.execute("SELECT COUNT(*) FROM data_rows").fetchone()[0] == 3693
    assert connection.execute("SELECT field_offset FROM fields WHERE owner='Staff' AND name='hp_'").fetchone()[0] == "0xE8"
    assert connection.execute("SELECT COUNT(*) FROM native_dispatch").fetchone()[0] == 54
    assert connection.execute("SELECT COUNT(*) FROM native_dispatch WHERE method_symbol='Staff.OnArriveGoal'").fetchone()[0] == 11
    assert connection.execute("SELECT COUNT(*) FROM native_dispatch WHERE method_symbol='data.DataManager.GetInstance'").fetchone()[0] == 43
    assert connection.execute("SELECT MIN(move_mode), MAX(move_mode) FROM native_dispatch WHERE method_symbol='Staff.OnArriveGoal'").fetchone() == (1, 11)
    assert connection.execute("SELECT status FROM data_table_slot_map WHERE table_slot=42").fetchone()[0] == "CONFIRMED_NATIVE_SLOT_DISPATCH"
    assert dict(connection.execute("SELECT element_type, COUNT(*) FROM data_rows WHERE element_type IN ('StaffData','JobData','SkillData','FurnitureData') GROUP BY element_type").fetchall()) == {"FurnitureData": 103, "JobData": 30, "SkillData": 36, "StaffData": 141}
    assert dict(connection.execute("SELECT access_origin || ':' || operation, COUNT(*) FROM field_access WHERE field_symbol='game.Staff.hp_' GROUP BY access_origin, operation").fetchall()) == {"NATIVE:read": 8, "NATIVE:write": 10}
    assert connection.execute("SELECT COUNT(*) FROM canonical_facts").fetchone()[0] == check["canonical_fact_count"]
    assert not connection.execute("SELECT entity_id, predicate, COUNT(*) FROM canonical_facts GROUP BY entity_id, predicate HAVING COUNT(*) > 1").fetchall()
    assert connection.execute("SELECT COUNT(*) FROM superseded_facts").fetchone()[0] == 2
    assert connection.execute("SELECT COUNT(*) FROM conflicts").fetchone()[0] == 1
    connection.close()

    query_results = read_jsonl(builder.KB / "query_results.jsonl")
    assert [row["query_id"] for row in query_results] == [f"Q{index}" for index in range(1, 15)]
    g1_5_queries = read_jsonl(builder.KB / "query_results_g1_5.jsonl")
    assert [row["query_id"] for row in g1_5_queries] == [f"C{index}" for index in range(1, 15)]
    assert all(row["status"] == "PASS" and row["provenance"] for row in g1_5_queries)
    assert json.loads((builder.KB / "build_manifest.json").read_text(encoding="utf-8"))["status"] == "PASS_G1_5_CANONICAL_KB_INTEGRITY_AND_STATIC_BLOCKERS_CLOSED"
    final_report = (builder.REPORTS / "G0_G1_FINAL_STATUS.md").read_text(encoding="utf-8")
    assert "PARTIAL_GAME_SCOPED_STATIC_KNOWLEDGE_G0_G1_SOURCE_LIMITED" in final_report
    print(json.dumps({"status": "PASS_GAME_KNOWLEDGE_G0_G1_REGRESSION", "source_identity": identity["status"], "canonical_facts": check["canonical_fact_count"], "queries": len(query_results)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
