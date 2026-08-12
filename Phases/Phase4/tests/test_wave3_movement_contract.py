import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
ARTIFACTS = ROOT / "Phases" / "Phase4" / "artifacts"


def load(name):
    return json.loads((ARTIFACTS / name).read_text(encoding="utf-8"))


class Wave3MovementContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract = load("wave3_movement_contract.json")
        cls.fixture = load("wave3_movement_fixture.json")
        cls.manifest = load("wave3_c3_build_manifest.json")

    def test_c3_artifacts_are_present_and_read_only(self):
        for name in self.manifest["artifact_outputs"]:
            self.assertTrue((ROOT / name).is_file(), name)
        self.assertTrue(self.contract["source_roots_read_only"])

    def test_raw_target_position_flow_is_explicit(self):
        trace = self.contract["raw_field_flow"]
        self.assertEqual(trace["producer"]["status"], "verified_bounded_raw_writes")
        self.assertEqual(trace["consumer"]["status"], "verified_bounded_array_copies")
        steps = trace["producer"]["steps"] + trace["consumer"]["steps"]
        self.assertEqual([row["step"] for row in steps], [1, 2, 3, 4, 5, 6])
        self.assertEqual(steps[0]["from"] if "from" in steps[0] else steps[0]["raw_array"], "TargetX")
        self.assertEqual(steps[2]["from"], "TargetX[TPos]")
        self.assertEqual(steps[2]["to"], "HumanX[THumanIndex]")
        self.assertEqual(steps[4]["to"], "HumanPX[THumanIndex]")

    def test_coordinate_spaces_keep_open_semantics(self):
        spaces = {row["space_id"]: row for row in self.contract["coordinate_spaces"]}
        self.assertEqual(spaces["legacy_target_array"]["status"], "verified_raw_storage_flow")
        self.assertEqual(spaces["legacy_actor_position_arrays"]["status"], "verified_writes_role_open")
        self.assertFalse(spaces["legacy_actor_position_arrays"]["legacy_equivalence"])
        self.assertEqual(spaces["adapter_world_position"]["status"], "web_adapter_decision")

    def test_provider_contract_preserves_wave2_boundary(self):
        provider = self.contract["provider_contract"]
        self.assertIn("path | no_path | unavailable", provider["path"]["outputs"])
        self.assertIn("blocked | clear | unavailable", provider["collision"]["outputs"])
        self.assertEqual(provider["seat"]["output"], "seat_occupancy_state")
        self.assertEqual(self.contract["adapter_tick_policy"]["status"], "web_adapter_decision")

    def test_fixture_has_deterministic_success_and_failure_cases(self):
        scenarios = {row["id"]: row for row in self.fixture["scenarios"]}
        self.assertEqual(scenarios["raw_target_to_position_trace"]["expected"]["positions_by_tick"], [[1, 0], [2, 0], [3, 0]])
        self.assertEqual(scenarios["blocked_target_does_not_teleport"]["expected"]["positions_by_tick"], [[0, 0]])
        self.assertEqual(scenarios["no_path_preserves_position"]["expected"]["final_status"], "no_path")
        self.assertEqual(scenarios["provider_unavailable_preserves_position"]["expected"]["final_status"], "provider_unavailable")
        for row in self.fixture["scenarios"][:4]:
            self.assertFalse(row["expected"]["legacy_equivalence"])

    def test_manifest_summary_and_non_claims(self):
        summary = self.manifest["artifact_summary"]
        self.assertEqual(summary["target_field_count"], 2)
        self.assertEqual(summary["position_field_count"], 4)
        self.assertEqual(summary["raw_flow_step_count"], 6)
        self.assertEqual(summary["scenario_count"], 5)
        self.assertEqual(summary["legacy_movement_semantics"], "open")
        self.assertTrue(any("previous position" in item for item in self.contract["semantic_limits"]))


if __name__ == "__main__":
    unittest.main()
