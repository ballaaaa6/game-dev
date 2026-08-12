import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
PHASE = ROOT / "Phases" / "Phase4"
ARTIFACTS = PHASE / "artifacts"
BUILDER = PHASE / "tools" / "build_wave4_hardening.py"


def load(name):
    return json.loads((ARTIFACTS / name).read_text(encoding="utf-8"))


class Wave4HardeningTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = load("wave4_hardening_manifest.json")
        cls.timer = load("wave4_timer_fuki_trace.json")
        cls.talk = load("wave4_talk_speaker_trace.json")
        cls.graph = load("wave4_message_graph_trace.json")
        cls.event = load("wave4_event_mode_candidates.json")

    def test_builder_is_reproducible(self):
        result = subprocess.run(
            [sys.executable, str(BUILDER), "--check"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)

    def test_manifest_preserves_scope_and_legacy_boundary(self):
        self.assertEqual(self.manifest["stage"], "W4.5-evidence-hardening")
        self.assertEqual(self.manifest["status"], "W4.5-hardening_complete_with_remaining_boundaries")
        self.assertFalse(self.manifest["legacy_equivalence"])
        self.assertEqual(set(self.manifest["packages"]), {"W4.5-R1", "W4.5-R2", "W4.5-R3", "W4.5-R4", "W4.5-R5"})

    def test_timer_and_fuki_trace_stops_at_logical_tick_and_cleanup_boundary(self):
        self.assertEqual(self.timer["update_bridge"]["repeat_control"]["observed_candidate_counts"], [1, 2, 16])
        self.assertEqual(self.timer["human_fuki"]["fields"]["HumanFukiIndex"]["all_source_lines"], [16193, 30136, 35628, 40167, 59428])
        self.assertEqual(self.timer["human_fuki"]["cleanup_search"]["status"], "not_found_in_scoped_mainprocess")
        self.assertFalse(self.timer["conclusion"]["wave5_blocker"])

    def test_talk_trace_verifies_raw_speaker_pipeline_without_actor_promotion(self):
        operations = self.talk["pipeline"]["add_kaiwa_talk_data"]["operations"]
        self.assertEqual(operations[0], "GetTalkIndex")
        self.assertIn("Int32.Parse second split token", operations)
        self.assertEqual(self.talk["speaker"]["direct_producer_callers_in_scoped_c_and_assembly"]["callsite_count"], 0)
        self.assertEqual(self.talk["speaker"]["actor_binding"]["status"], "adapter_boundary")
        self.assertEqual(self.talk["literal_refs"]["status"], "values_recorded_but_pointer_name_to_table_index_not_promoted")

    def test_message_graph_trace_records_render_behavior_not_product_labels(self):
        self.assertEqual(self.graph["producer"]["direct_source_callsite_count"], 9)
        self.assertEqual(self.graph["producer"]["graph_expression_counts"], {"0": 7, "1": 1, "2": 1})
        self.assertEqual(self.graph["draw_consumer"]["raw_labels"]["status"], "numeric_graph_labels_not_named")
        self.assertIn("MessageMaxTime - MessageTime == 1", self.graph["audio_consumer"]["operation"])

    def test_event_trace_keeps_target_clusters_candidate_only(self):
        clusters = self.event["consumer"]["target_clusters"]
        self.assertEqual(clusters["0x00f1a908"]["count"], 21)
        self.assertEqual(clusters["0x00f4a714"]["count"], 1)
        self.assertEqual(clusters["0x00f1aa34"]["count"], 13)
        self.assertTrue(all(item["status"] == "candidate_target_cluster_only" for item in clusters.values()))
        self.assertEqual(self.event["candidate_policy"]["status"], "no_numeric_mode_promoted")


if __name__ == "__main__":
    unittest.main()
