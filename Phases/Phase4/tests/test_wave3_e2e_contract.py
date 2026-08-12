import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
ARTIFACTS = ROOT / "Phases" / "Phase4" / "artifacts"


def load(name):
    return json.loads((ARTIFACTS / name).read_text(encoding="utf-8"))


class Wave3E2EContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = load("wave3_actor_e2e_fixture.json")
        cls.trace = load("wave3_actor_trace.json")
        cls.manifest = load("wave3_c6_build_manifest.json")
        cls.scenarios = {row["id"]: row for row in cls.fixture["scenarios"]}

    def test_c6_artifacts_are_present_and_read_only(self):
        for name in self.manifest["artifact_outputs"]:
            self.assertTrue((ROOT / name).is_file(), name)
        self.assertTrue(self.fixture["source_roots_read_only"])

    def test_c6_inputs_cover_wave2_and_c1_to_c5_boundaries(self):
        inputs = self.fixture["inputs"]
        self.assertIn("wave2_minimum_scene_fixture", inputs)
        self.assertIn("identity_contract", inputs)
        self.assertIn("state_contract", inputs)
        self.assertIn("movement_contract", inputs)
        self.assertIn("interaction_contract", inputs)
        self.assertIn("animation_contract", inputs)
        self.assertEqual(self.fixture["adapter_contract"]["legacy_equivalence"], False)

    def test_required_scenarios_are_present(self):
        required = set(self.fixture["required_scenarios"])
        self.assertEqual(required, set(self.scenarios))
        self.assertEqual(len(required), 6)

    def test_golden_trace_is_spawn_move_arrive_draw(self):
        self.assertEqual(self.trace["trace_id"], "spawn_move_arrive_draw")
        events = self.trace["events"]
        self.assertEqual(events[0]["event"], "spawn")
        self.assertEqual([row["event"] for row in events], ["spawn", "state", "move", "move", "move", "state", "draw"])
        self.assertEqual([row["position"] for row in events if row["event"] == "move"], [[1, 0], [2, 0], [3, 0]])
        self.assertEqual(self.trace["expected"]["movement_status"], "arrived")
        self.assertEqual(self.trace["expected"]["draw_status"], "draw_command_ready")
        self.assertFalse(self.trace["expected"]["legacy_equivalence"])

    def test_blocked_target_never_teleports(self):
        scenario = self.scenarios["blocked_target"]
        moves = [row for row in scenario["trace"] if row["event"] == "move"]
        self.assertEqual(moves[0]["position"], [0, 0])
        self.assertEqual(moves[0]["movement_status"], "blocked")
        self.assertEqual(scenario["expected"]["position_after_block"], [0, 0])
        self.assertFalse(scenario["expected"]["draw_dispatched"])

    def test_seat_conflict_and_release_then_sit_are_explicit_adapter_relations(self):
        conflict = self.scenarios["seat_occupied"]
        self.assertEqual(conflict["expected"]["status"], "seat_conflict")
        self.assertEqual(conflict["expected"]["seat_owner"], "adapter.actor.0")
        self.assertEqual(conflict["trace"][-1]["result"], "conflict")

        release_then_sit = self.scenarios["seat_release_then_sit"]
        self.assertEqual(release_then_sit["expected"]["final_adapter_state"], "sitting")
        self.assertEqual([row["result"] for row in release_then_sit["trace"] if row["event"] == "seat"], ["occupied", "released", "occupied"])
        self.assertEqual(release_then_sit["trace"][-1]["event"], "draw")
        self.assertFalse(release_then_sit["expected"]["legacy_occupancy_equivalence"])

    def test_unknown_animation_uses_no_asset_substitution(self):
        scenario = self.scenarios["animation_unknown_fallback"]
        resolve = next(row for row in scenario["trace"] if row["event"] == "animation_resolve")
        self.assertEqual(resolve["status"], "semantic_animation_unknown")
        self.assertEqual(resolve["policy"], "static_verified_frame_only_no_asset_substitution")
        self.assertFalse(scenario["expected"]["asset_substitution"])
        self.assertIsNone(scenario["expected"]["semantic_state"])

    def test_manifest_and_status_keep_legacy_semantics_open(self):
        summary = self.manifest["artifact_summary"]
        self.assertEqual(summary["scenario_count"], 6)
        self.assertEqual(summary["required_scenario_count"], 6)
        self.assertEqual(summary["golden_trace_event_count"], 7)
        self.assertFalse(summary["legacy_equivalence"])
        self.assertIn("legacy_semantics_open", self.manifest["status"])
        self.assertIn("legacy_semantics_open", self.fixture["status"])


if __name__ == "__main__":
    unittest.main()
