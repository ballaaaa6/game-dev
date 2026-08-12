import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
ARTIFACTS = ROOT / "Phases" / "Phase4" / "artifacts"


def load(name: str):
    return json.loads((ARTIFACTS / name).read_text(encoding="utf-8"))


class Wave3StateContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract = load("wave3_actor_state_contract.json")
        cls.fixture = load("wave3_state_transition_fixture.json")
        cls.manifest = load("wave3_c2_build_manifest.json")

    def test_c2_artifacts_are_present_and_read_only(self):
        for name in (
            "wave3_actor_state_contract.json",
            "wave3_state_transition_fixture.json",
            "wave3_c2_build_manifest.json",
        ):
            self.assertTrue((ARTIFACTS / name).is_file(), name)
        self.assertTrue(self.contract["source_roots_read_only"])
        self.assertTrue(self.manifest["source_roots_read_only"])

    def test_state_fields_are_raw_evidence_only(self):
        rows = {row["field"]: row for row in self.contract["raw_state_fields"]}
        expected = {
            "HumanMode",
            "HumanTime",
            "HumanStop",
            "HumanWalkLong",
            "HumanSitChair",
            "HumanReaction",
            "HumanWait",
            "HumanState",
            "HumanAnime",
            "HumanDegree",
            "HumanFukiIndex",
            "HumanFukiTime",
        }
        self.assertEqual(set(rows), expected)
        for row in rows.values():
            self.assertEqual(row["access_kind"], "offset_reference_only")
            self.assertEqual(row["semantic_status"], "raw_field_registered_semantic_label_not_closed")
            self.assertIn("reference_samples", row)
            self.assertIn("offset", row)

    def test_transition_table_separates_verified_raw_and_adapter_behavior(self):
        rows = {row["transition_id"]: row for row in self.contract["transition_table"]}
        self.assertEqual(rows["raw_spawn_seed"]["status"], "verified_bounded_raw_seed")
        self.assertIsNone(rows["raw_spawn_seed"]["agent_state"])
        self.assertEqual(rows["adapter_move_requested"]["status"], "web_adapter_decision")
        self.assertFalse(rows["adapter_move_requested"]["legacy_equivalence"])
        self.assertEqual(rows["dialogue_candidate_modes"]["status"], "probable_phase2_mapping")
        self.assertEqual(rows["dialogue_candidate_modes"]["agent_state"], "talking")

    def test_main_process_tick_slices_keep_raw_timer_evidence_separate(self):
        slices = {row["slice_id"]: row for row in self.contract["main_process_tick_slices"]}
        self.assertEqual(len(slices), 4)
        self.assertEqual(slices["human_wait_decrement"]["timer_behavior"], "decrement_by_one_raw_unit")
        self.assertTrue(slices["human_wait_decrement"]["evidence"][2]["line"])
        self.assertIsNone(slices["raw_state_2_to_mode_5"]["agent_state"])
        self.assertIn("unit_unknown", slices["human_anime_counter"]["timer_behavior"])

    def test_fixture_contains_neutral_and_adapter_scenarios(self):
        scenarios = {row["id"]: row for row in self.fixture["scenarios"]}
        self.assertEqual(scenarios["raw_spawn_seed"]["expected"]["status"], "verified_bounded_raw_seed")
        self.assertEqual(scenarios["adapter_walking"]["expected"]["agent_state"], "walking")
        self.assertFalse(scenarios["adapter_walking"]["expected"]["legacy_equivalence"])
        self.assertEqual(scenarios["probable_talking_candidate"]["expected"]["timing"], None)
        self.assertEqual(scenarios["raw_wait_decrement"]["expected"]["human_wait_after"], 1)
        self.assertEqual(scenarios["raw_state_mode_transition"]["expected"]["raw_writes"]["HumanMode"], 5)
        self.assertEqual(scenarios["raw_anime_counter_boundary"]["expected"]["threshold"], 15)
        self.assertIn("HumanMode=0 is idle", self.fixture["not_claimed"])
        self.assertIn("adapter clock equals legacy HumanTime timing", self.fixture["not_claimed"])

    def test_manifest_summary_preserves_open_semantics(self):
        summary = self.manifest["artifact_summary"]
        self.assertEqual(summary["raw_state_field_count"], 12)
        self.assertEqual(summary["transition_count"], 4)
        self.assertEqual(summary["verified_raw_transitions"], 1)
        self.assertEqual(summary["adapter_transitions"], 2)
        self.assertEqual(summary["probable_transitions"], 1)
        self.assertEqual(summary["main_process_tick_slice_count"], 4)
        self.assertEqual(summary["verified_raw_tick_slices"], 4)
        self.assertIn("unit and Agent meaning open", summary["timer_semantics"])
        self.assertIn("semantics_open", summary["semantic_status"])


if __name__ == "__main__":
    unittest.main()
