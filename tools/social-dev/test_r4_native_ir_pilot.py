import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ACCEPTANCE = ROOT / "knowledge" / "brain" / "acceptance" / "r4-0-native-ir-csharp-pilot"
ARTIFACTS = ROOT / "artifacts" / "r4-0-native-ir-pilot"


def test_r4_pilot_final_decision_is_go():
    decision = json.loads((ACCEPTANCE / "final-decision.json").read_text(encoding="utf-8"))
    assert decision["decision"] == "GO"
    assert decision["go_token"] == "PASS_R4_0_NATIVE_IR_CSHARP_FEASIBILITY_PILOT_GO"
    assert decision["full_r4_native_lift_authorized"] is True
    assert all(decision["gates"].values())


def test_required_positive_and_negative_gates():
    positive = json.loads((ACCEPTANCE / "positive-validation.json").read_text(encoding="utf-8"))
    negative = json.loads((ACCEPTANCE / "negative-validation.json").read_text(encoding="utf-8"))
    assert positive["summary"] == {"all_verified": True, "required": 6, "source_writes": 0, "verified": 6}
    assert negative["summary"]["all_rejected"] is True
    assert negative["summary"]["rejected"] == 5
    assert negative["summary"]["source_writes"] == 0


def test_hard_cohort_and_replay_artifacts_are_deterministic():
    hard = json.loads((ACCEPTANCE / "hard-cohort.json").read_text(encoding="utf-8"))
    replay = json.loads((ACCEPTANCE / "deterministic-replay.json").read_text(encoding="utf-8"))
    assert hard["summary"]["count"] == 100
    assert hard["summary"]["verified"] >= 50
    assert replay["deterministic"] is True
    first = (ARTIFACTS / "reproduction-pass-1.jsonl").read_bytes()
    second = (ARTIFACTS / "reproduction-pass-2.jsonl").read_bytes()
    assert first == second
    assert all(json.loads(line)["source_write"] is False for line in first.splitlines() if line.strip())
