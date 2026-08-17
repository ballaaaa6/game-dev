"""Validate the independent K4.1 targeted-closure artifacts."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
K4 = ROOT / "knowledge/brain/acceptance/k4"
K41 = ROOT / "knowledge/brain/acceptance/k4-1"
DB = ROOT / "knowledge/brain/sqlite/social_dev_brain.sqlite"
MANIFEST = ROOT / "knowledge/brain/MANIFEST.json"
TOKEN = "PASS_K4_1_TARGETED_CLOSURE_READY_FOR_V8"
ALLOWED = {"REPRODUCED_EXACT", "REPRODUCED_WITH_CORRECTION", "REJECTED_BY_SOURCE"}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def check(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def main() -> int:
    errors: list[str] = []
    required = [
        "fukidashi-payload-closure.json",
        "fukidashi-localization-catalog.json",
        "autonomous-talk-timeline.json",
        "room0-door-visual-consumer-graph.json",
        "room0-door-action-vs-visual-contract.json",
        "workstation-native-cfg.json",
        "room0-workstation-pass-interleave.json",
        "workstation-direction-fixtures.json",
        "research-findings-classification.json",
        "final-validation.json",
        "K4_1_CLOSURE_REPORT.md",
    ]
    for name in required:
        check((K41 / name).exists(), f"missing K4.1 artifact: {name}", errors)
    if errors:
        print("FAIL_K4_1_TARGETED_VALIDATION")
        for error in errors:
            print(f"- {error}")
        return 1

    payload = load(K41 / "fukidashi-payload-closure.json")
    catalog = load(K41 / "fukidashi-localization-catalog.json")
    timeline = load(K41 / "autonomous-talk-timeline.json")
    door = load(K41 / "room0-door-action-vs-visual-contract.json")
    workstation = load(K41 / "workstation-native-cfg.json")
    interleave = load(K41 / "room0-workstation-pass-interleave.json")
    fixtures = load(K41 / "workstation-direction-fixtures.json")
    findings = load(K41 / "research-findings-classification.json")
    final = load(K41 / "final-validation.json")
    coverage = load(K4 / "reachable-visual-consumers.json")
    matrix = load(K4 / "visual-assembly-coverage-matrix.json")

    check(payload["status"] == "PROVEN_CANONICAL" and payload["classification"] == "REPRODUCED_EXACT", "Fukidashi payload is not canonical exact", errors)
    pools = {item["handle"]: item["values"] for item in payload["native_proof"].get("fukidashi_pools", [])}
    if not pools:
        pools = {item["handle"]: item["values"] for item in load(K41 / "workstation-native-cfg.json").get("fukidashi_pools", [])}
    # The canonical payload artifact carries the pool records under native metadata proof.
    native_pools = payload.get("autonomous_talk", {})
    check(native_pools["frame_20"]["pool"]["values"] == [30, 31, 32, 33, 34], "frame-20 autonomous pool differs", errors)
    check(native_pools["frame_70"]["pool"]["values"] == [35, 36, 37, 38, 39, 40, 41, 42, 43], "frame-70 autonomous pool differs", errors)
    check(payload["invitation"]["opening_frame_20"]["pool"]["values"] == [25, 26, 27, 28, 29, 68], "invite opening pool differs", errors)
    check(payload["invitation"]["frame_60_busy_or_reject"]["pool"]["values"] == [44, 45, 46], "invite busy pool differs", errors)
    check(payload["invitation"]["frame_60_response"]["pool"]["values"] == [22, 23, 24], "invite response pool differs", errors)
    check(payload["payload_storage_and_lifetime"]["add_single"]["writes"]["frame_lifetime"] == 40, "bubble lifetime is not 40", errors)
    check(payload["payload_storage_and_lifetime"]["draw"]["guards"] == ["frame_lifetime > 0", "delay <= 0"], "bubble draw guards differ", errors)
    check(payload["payload_storage_and_lifetime"]["cleanup"]["behavior"].startswith("frame_=0"), "partner cleanup is not proven", errors)

    check(catalog["status"] == "PROVEN_CANONICAL" and len(catalog["entries"]) == 26, "localization catalog does not contain all 26 closed IDs", errors)
    expected_locale = {22: ("Yeees", "はーい"), 23: ("What could it be?", "何かな？"), 24: ("Yes, yes...", "はいはい"), 25: ("Hey, listen...", "ねぇねぇ"), 26: ("Umm...", "あのー"), 27: ("Is now a good time?", "いま大丈夫？"), 28: ("Sorry", "すいません"), 29: ("Hey you", "チミチミ"), 30: ("About this...", "これがさぁ"), 31: ("In that case...", "それでさぁ"), 32: ("And then...", "でさぁ"), 33: ("...", "ペラペラ"), 34: ("By the way...", "ところで"), 35: ("Hmm", "ふむふむ"), 36: ("Yep yep", "うんうん"), 37: ("Of course!", "なるほど！"), 38: ("Huh?", "えぇ！"), 39: ("Amazing!", "すごい！"), 40: ("As expected!", "さすが！"), 41: ("Wow!", "わーぉ"), 42: ("Hmm...", "ふーん"), 43: ("I dunno...", "うーん…"), 44: ("I'm busy", "今忙しい"), 45: ("Sorry...", "ごめんね"), 46: ("Later!", "またあとで！"), 68: ("...", "…")}
    for row in catalog["entries"]:
        check((row["english"], row["japanese"]) == expected_locale.get(row["id"]), f"localization value differs for ID {row['id']}", errors)
    check(catalog["language_path"]["Language.LT"] == "0x1BC85D0", "Language.LT path is missing", errors)
    check(catalog["source_identity"]["raw_entry_sha256"]["en"] == "2b19fdbafac7346e40d7910645e1a4402f6ce8cfbb0a9cbca30d91f1924c7196", "EN language entry hash differs", errors)
    check(catalog["source_identity"]["raw_entry_sha256"]["ja"] == "7588aa84f6d97f5db23f12459f2e54ad1e5a623151173da717e1e87b8a375a94", "JA language entry hash differs", errors)

    check(timeline["status"] == "PROVEN_CANONICAL" and timeline["timeline"]["frame_20"]["random"]["bound"] == 101, "autonomous frame-20 timing/random differs", errors)
    check(timeline["completion"]["frame_130_or_more"].startswith("clear"), "autonomous cleanup timing is missing", errors)

    check(door["status"] == "NO_DISTINCT_VISUAL" and not door["blocking"], "Room0 door conclusion remains blocking", errors)
    check(door["visual_baseline"]["furnitureData"] is None, "Room0 door FurnitureData is not null", errors)
    check(door["native_proof"]["furnitureData_null_guard"] == "0x12C08A8/0x12C08AC", "DrawWall null guard is not recorded", errors)

    check(workstation["status"] == "PROVEN_CANONICAL", "workstation native CFG is not canonical", errors)
    check(workstation["live_normal_path"]["preview"] is False, "live normal workstation path is not preview=false", errors)
    check(all(item["preview"] is True for item in workstation["preview_paths"]), "preview paths are not separated", errors)
    down = [item["operation"] for item in workstation["directional_sequences"]["DIRECTION_DOWN_3"]]
    up = [item["operation"] for item in workstation["directional_sequences"]["DIRECTION_UP_2"]]
    check(down == ["desk primary Seb/AppData.DrawSeb", "chair subSeb ResourceManager.DrawSeb", "Staff.Draw offset overload", "late chair subSeb foreground ResourceManager.DrawSeb"], "direction-3 workstation sequence differs", errors)
    check(up == ["chair subSeb ResourceManager.DrawSeb", "Staff.Draw offset overload", "desk primary Seb/AppData.DrawSeb"], "direction-2 workstation sequence differs", errors)
    check(workstation["late_foreground"]["guard"] == "staffId_ != -1", "late chair guard differs", errors)
    check("installed true bypasses outer uninstalled Staff loop" in workstation["live_normal_path"]["installed_guard"], "duplicate Staff guard differs", errors)
    check(len(fixtures["fixtures"]) == 3 and {tuple(item["cell"]) for item in fixtures["fixtures"]} == {(2, 4), (3, 4), (6, 4)}, "direction fixtures do not cover three Room0 desks", errors)
    check(interleave["status"] == "PROVEN_CANONICAL", "interleave artifact is not canonical", errors)

    labels = [item["classification"] for item in findings["findings"]]
    check(set(labels).issubset(ALLOWED), "research classification vocabulary contains an unapproved label", errors)
    check("REPRODUCED_WITH_CORRECTION" in labels and "REJECTED_BY_SOURCE" in labels and "REPRODUCED_EXACT" in labels, "research classifications are incomplete", errors)
    check(any(item["finding_id"] == "talk.extra-handle-0x27D7E40" and item["classification"] == "REJECTED_BY_SOURCE" for item in findings["findings"]), "unsupported extra handle was not rejected", errors)

    check(coverage["status"] == "closed" and coverage["metrics"]["blocking_source_limited_count"] == 0, "K4 coverage still has a blocker", errors)
    check(matrix["blocking_consumers"] == [] and matrix["status"] == "closed", "K4 coverage matrix is not closed", errors)
    check(final["final_token"] == TOKEN and final["status"] == "complete", "K4.1 final validation token/status differs", errors)
    check(final["coverage"]["blocking_source_limited_count"] == 0 and final["coverage"]["source_missing_count"] == 0 and final["coverage"]["heuristic_or_assumed_count"] == 0, "K4.1 final coverage counts are not zero", errors)
    check(final["boundary"]["v8"] == "NOT_STARTED", "V8 boundary changed", errors)
    check(all(item["status"] == "PASS" for item in final["regressions"]), "a recorded K4.1 regression is not PASS", errors)

    evidence = load(K4 / "source-native-evidence-manifest.json")
    check(evidence["source_roots_read_only"] is True and evidence["source_hashes_unchanged"] is True, "source roots are not recorded unchanged", errors)
    check(evidence["artifacts"] == evidence["source_hashes_rechecked_after_build"], "source hash before/after records differ", errors)
    pack_delta = load(K4 / "generated-pack-delta.json")
    check(not any(pack_delta[key] for key in ("runtime_pack_changed", "visual_pack_changed", "data_pack_changed", "runtime_mirror_changed")), "an original generated pack changed", errors)

    connection = sqlite3.connect(DB)
    try:
        metadata = dict(connection.execute("select key,value_json from brain_metadata"))
        check(json.loads(metadata["brain_revision"]) == "k4-visual-assembly-r2", "canonical brain revision differs", errors)
        check(json.loads(metadata["status"]) == "K4_CLOSED_VISUAL_ASSEMBLY", "canonical brain status differs", errors)
        check(json.loads(metadata["k4_final_token"]) == TOKEN, "canonical brain final token differs", errors)
        facts = connection.execute("select count(*) from canonical_facts where fact_id like 'fact:k4:%'").fetchone()[0]
        edges = connection.execute("select count(*) from semantic_edges where edge_id like 'edge-k4:%' or edge_id like 'edge-k4-1:%'").fetchone()[0]
        check(facts >= 11 and edges >= 10, "canonical brain did not receive K4.1 facts/edges", errors)
    finally:
        connection.close()

    manifest = load(MANIFEST)
    check(manifest["status"] == "K4_CLOSED_VISUAL_ASSEMBLY", "brain manifest is not closed", errors)
    check(manifest["scope"]["k4"] == "CLOSED" and manifest["scope"]["v8"] == "NOT_STARTED", "brain manifest scope differs", errors)
    check(manifest["k4"]["ready_for_v8"] is True and manifest["k4"]["blocking_source_limited_count"] == 0, "brain manifest readiness differs", errors)

    if errors:
        print("FAIL_K4_1_TARGETED_VALIDATION")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PASS_K4_1_TARGETED_VALIDATION blocking_source_limited=0 source_missing=0 heuristic_or_assumed=0 ready_for_v8=true v8=NOT_STARTED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
