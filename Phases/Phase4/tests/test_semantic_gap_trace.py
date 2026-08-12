import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
ARTIFACT = ROOT / "Phases" / "Phase4" / "artifacts" / "semantic_gap_trace.json"
BUILDER = ROOT / "Phases" / "Phase4" / "tools" / "build_semantic_gap_trace.py"


class SemanticGapTraceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.value = json.loads(ARTIFACT.read_text(encoding="utf-8"))

    def test_builder_is_reproducible(self):
        result = subprocess.run(
            [sys.executable, str(BUILDER), "--check"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)

    def test_newgame_object_setup_is_bounded_without_semantic_promotion(self):
        trace = self.value["newgamepara"]
        self.assertEqual(trace["structural"]["instruction_count"], 13671)
        cluster = next(row for row in trace["clusters"] if row["cluster_id"] == "NGP-OBJECT-CONSTRUCTION")
        self.assertEqual(cluster["object_setup"]["call_count"], 29)
        self.assertTrue(cluster["object_setup"]["returned_w0_writeback_all_calls"])
        self.assertEqual(cluster["object_setup"]["array_field_refs"]["ObjecPoint"]["offset"], "0x308")
        self.assertIn("complete NewGamePara lifecycle", cluster["not_claimed"])

    def test_doevent_clusters_keep_numeric_modes_unnamed(self):
        trace = self.value["doevent"]
        self.assertEqual(trace["structural"]["instruction_count"], 15569)
        clusters = {row["cluster_id"]: row for row in trace["clusters"]}
        self.assertEqual(
            [clusters[key]["comparison_value"] for key in ("DE-KIKAKU-5-DIALOGUE", "DE-KIKAKU-7-DIALOGUE", "DE-KIKAKU-8-DIALOGUE")],
            [5, 7, 8],
        )
        self.assertIsNone(clusters["DE-EVENTMODE-2"]["semantic_mode_name"])
        self.assertEqual(trace["target_inventory"]["0x00f1a908"]["count"], 21)

    def test_tface_literals_are_not_actor_field_producers(self):
        trace = self.value["tface_producer_trace"]
        self.assertEqual(len(trace["literal_hits"]), 10)
        self.assertEqual(trace["classification_counts"]["literal_direct_non_actor_dynamic_callsite"], 10)
        self.assertEqual(trace["classification_counts"]["actor_dynamic_or_unknown_literal_producer"], 0)
        self.assertEqual(trace["direct_literal_producer_search"]["status"], "not_found_in_scoped_actor_producers")
        selectors = {row["selector"] for row in trace["selector_namespaces"]}
        self.assertEqual(selectors, {"HumanFaceG", "HumanBodyG", "HumanDexFaceG", "SyainFaceG"})

    def test_trace_preserves_open_status(self):
        self.assertFalse(self.value["legacy_equivalence"])
        self.assertEqual(self.value["status"], "bounded_branch_and_selector_trace_open")
        self.assertGreaterEqual(len(self.value["next_recoverable_slices"]), 3)


if __name__ == "__main__":
    unittest.main()
