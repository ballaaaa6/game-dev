import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
ARTIFACTS = ROOT / "Phases" / "Phase4" / "artifacts"


def load(name):
    return json.loads((ARTIFACTS / name).read_text(encoding="utf-8"))


class Wave3InteractionContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract = load("wave3_interaction_contract.json")
        cls.fixture = load("wave3_seat_fixture.json")
        cls.manifest = load("wave3_c4_build_manifest.json")

    def test_c4_artifacts_are_present_and_read_only(self):
        for name in self.manifest["artifact_outputs"]:
            self.assertTrue((ROOT / name).is_file(), name)
        self.assertTrue(self.contract["source_roots_read_only"])

    def test_relation_roles_keep_raw_and_adapter_namespaces_separate(self):
        roles = {row["field"]: row for row in self.contract["relation_roles"]}
        self.assertEqual(roles["HumanSitChair"]["status"], "raw_index_flow_verified_occupancy_not_closed")
        self.assertEqual(roles["DeskSyain"]["status"], "bounded_scan_assignment_clear_verified")
        self.assertEqual(roles["PCObjec"]["status"], "render_relation_verified_occupancy_not_closed")
        self.assertEqual(roles["seat_occupancy_state"]["status"], "web_adapter_decision")
        self.assertFalse(roles["seat_occupancy_state"]["legacy_equivalence"])

    def test_raw_relation_traces_have_bounded_evidence(self):
        traces = {row["trace_id"]: row for row in self.contract["raw_relation_traces"]}
        self.assertEqual(len(traces), 5)
        self.assertEqual(traces["actor_seat_index_consumed_by_main_process"]["status"], "verified_raw_index_and_relation_flow_occupancy_open")
        self.assertEqual(traces["desk_slot_scan_and_assignment"]["status"], "verified_bounded_desk_relation_flow_occupancy_open")
        self.assertEqual(traces["draw_object_furniture_relations"]["occupancy_state"], None)
        for trace in traces.values():
            self.assertTrue(trace["evidence"])
            self.assertTrue(all(ref["line"] for ref in trace["evidence"]), trace["trace_id"])

    def test_adapter_operations_and_conflict_policy_are_explicit(self):
        operations = self.contract["adapter_contract"]["operations"]
        self.assertEqual(set(operations), {"occupy", "release", "query"})
        self.assertIn("conflict", operations["occupy"]["outputs"])
        self.assertIn("not_owner", operations["release"]["outputs"])
        self.assertIn("one owner per seat", operations["occupy"]["rule"])
        self.assertFalse(self.contract["adapter_contract"]["legacy_equivalence"])

    def test_fixture_covers_success_conflict_release_and_unavailable(self):
        scenarios = {row["id"]: row for row in self.fixture["scenarios"]}
        self.assertEqual(scenarios["occupy_free_seat"]["expected"]["result"], "occupied")
        self.assertEqual(scenarios["occupied_seat_conflict"]["expected"]["result"], "conflict")
        self.assertEqual(scenarios["release_by_owner"]["expected"]["result"], "released")
        self.assertEqual(scenarios["release_by_non_owner"]["expected"]["result"], "not_owner")
        self.assertEqual(scenarios["seat_provider_unavailable"]["expected"]["state_mutation"], None)
        self.assertIsNone(scenarios["raw_human_sit_chair_is_not_occupancy"]["expected"]["occupancy_state"])
        for row in scenarios.values():
            if "legacy_equivalence" in row["expected"]:
                self.assertFalse(row["expected"]["legacy_equivalence"])

    def test_manifest_summary_preserves_open_legacy_occupancy(self):
        summary = self.manifest["artifact_summary"]
        self.assertEqual(summary["relation_field_count"], 7)
        self.assertEqual(summary["raw_trace_count"], 5)
        self.assertEqual(summary["adapter_operation_count"], 3)
        self.assertEqual(summary["scenario_count"], 6)
        self.assertEqual(summary["legacy_occupancy_status"], "not_closed")
        self.assertIn("legacy_occupancy_open", summary["semantic_status"])


if __name__ == "__main__":
    unittest.main()
