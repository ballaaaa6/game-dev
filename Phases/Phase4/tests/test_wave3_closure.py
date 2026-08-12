import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
ARTIFACTS = ROOT / "Phases" / "Phase4" / "artifacts"
REPORT = ROOT / "Phases" / "Phase4" / "docs" / "wave3_closure_report.md"


def load(name):
    return json.loads((ARTIFACTS / name).read_text(encoding="utf-8"))


class Wave3ClosureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.decision = load("wave3_legacy_occupancy_decision.json")
        cls.manifest = load("wave3_c7_build_manifest.json")
        cls.report = REPORT.read_text(encoding="utf-8")

    def test_c7_outputs_are_present_and_read_only(self):
        for name in self.manifest["artifact_outputs"]:
            self.assertTrue((ROOT / name).is_file(), name)
        self.assertTrue(self.decision["source_roots_read_only"])

    def test_occupancy_decision_is_adapter_only_not_legacy_equivalence(self):
        occupancy = self.decision["legacy_occupancy_decision"]
        self.assertEqual(occupancy["status"], "adapter_only_for_current_wave3_scope_legacy_producer_not_closed")
        self.assertIn("HumanSitChair", " ".join(occupancy["raw_findings"]))
        self.assertIn("DeskSyain", " ".join(occupancy["raw_findings"]))
        self.assertIn("reopen_condition", self.decision["legacy_occupancy_decision"])

    def test_c2_mapping_remains_unpromoted(self):
        mapping = self.decision["c2_semantic_mapping_decision"]
        self.assertEqual(mapping["status"], "not_closed_no_phase2_mapping_update")
        self.assertEqual(mapping["verified_semantic_agent_states"], 0)
        self.assertFalse(mapping["phase2_mapping_updated"])
        self.assertEqual(mapping["verified_raw_tick_slices"], 4)

    def test_open_gaps_have_controlled_status(self):
        self.assertEqual(self.decision["open_gap_ids"], ["W3-GAP-001", "W3-GAP-002", "W3-GAP-003", "W3-GAP-004", "W3-GAP-005", "W3-GAP-006", "W3-GAP-007"])
        self.assertEqual(self.decision["controlled_out_of_scope"], ["W3-GAP-008"])

    def test_c0_to_c6_are_declared_ready_for_handoff(self):
        self.assertEqual(self.manifest["artifact_summary"]["contract_packages_ready"], ["W3-C0", "W3-C1", "W3-C2", "W3-C3", "W3-C4", "W3-C5", "W3-C6"])
        self.assertEqual(self.manifest["artifact_summary"]["legacy_equivalence"], False)
        self.assertIn("phase5", self.manifest["status"])

    def test_report_contains_handoff_restrictions(self):
        for phrase in [
            "complete_with_known_limitations",
            "legacy seat occupancy producer",
            "Phase 5",
            "TFace=40/41",
            "HumanMode",
            "W3-GAP-006",
        ]:
            self.assertIn(phrase, self.report)

    def test_phase2_mapping_and_animation_are_explicitly_open(self):
        self.assertFalse(self.manifest["artifact_summary"]["phase2_mapping_updated"])
        self.assertEqual(self.decision["animation_decision"]["verified_semantic_animations"], 0)
        self.assertIsNone(self.decision["animation_decision"]["timing"])
        self.assertIsNone(self.decision["animation_decision"]["direction"])


if __name__ == "__main__":
    unittest.main()
