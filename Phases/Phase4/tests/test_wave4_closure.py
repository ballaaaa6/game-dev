import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
PHASE = ROOT / "Phases" / "Phase4"
ARTIFACTS = PHASE / "artifacts"
BUILDER = PHASE / "tools" / "build_wave4_closure.py"


def load(name):
    return json.loads((ARTIFACTS / name).read_text(encoding="utf-8"))


class Wave4ClosureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = load("wave4_c7_build_manifest.json")
        cls.slices = load("wave4_lifecycle_slices.json")
        cls.gaps = load("wave4_gap_register.json")

    def test_closure_builder_is_reproducible(self):
        result = subprocess.run(
            [sys.executable, str(BUILDER), "--check"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)

    def test_manifest_closes_wave_without_claiming_legacy_equivalence(self):
        self.assertEqual(self.manifest["stage"], "W4-C7-closure-and-handoff")
        self.assertEqual(self.manifest["status"], "W4-C0-C7-closure_complete_with_known_limitations")
        self.assertFalse(self.manifest["legacy_equivalence"])
        self.assertIn("W4-C7", self.manifest["packages"])
        self.assertTrue(self.manifest["source_hashes"])

    def test_mainprocess_and_drawobj_consumer_boundaries_are_indexed(self):
        main = self.slices["mainprocess"]
        self.assertEqual(main["source_status"], "categorized_c")
        self.assertEqual(main["call_summary"]["by_call"]["form_GameForm__AddEvent"], 55)
        self.assertEqual(main["call_summary"]["same_line_add_event_call_count"], 53)
        self.assertEqual(
            [item["id"] for item in main["consumer_slices"]],
            [
                "human_fuki_time_tick",
                "message_timer_tick_branch_a",
                "message_compaction",
                "message_timer_tick_branch_b",
                "message_max_timer_sound_threshold",
            ],
        )
        draw = self.slices["drawobj"]
        self.assertEqual(draw["span"], {"start_line": 15847, "end_line": 17616})
        self.assertEqual(draw["call_summary"]["by_call"]["form_GameForm__DrawFukidashi"], 1)
        self.assertEqual(draw["field_offset_refs"]["0xe70"]["field"], "HumanFukiIndex")

    def test_doevent_keeps_target_map_bounded_and_modes_raw(self):
        do_event = self.slices["do_event"]
        self.assertEqual(do_event["source_status"], "assembly_fallback_only")
        self.assertEqual(do_event["target_counts"]["0x00f1a908"], 21)
        self.assertEqual(do_event["target_counts"]["0x00f1a98c"], 12)
        self.assertEqual(do_event["target_counts"]["0x00f4b038"], 2)
        self.assertEqual(do_event["target_counts"]["0x00f4a714"], 1)
        self.assertEqual(do_event["event_queue_field_refs"]["0xff8"]["field"], "EventMode")
        self.assertIn("numeric event modes are not assigned names", do_event["not_claimed"])

    def test_open_gaps_are_reworded_to_reflect_closed_bounded_slices(self):
        gaps = {gap["id"]: gap for gap in self.gaps["gaps"]}
        self.assertIn("MainProcess decrements HumanFukiTime", gaps["W4-GAP-004"]["impact"])
        self.assertIn("W4.5 target clusters", gaps["W4-GAP-005"]["next_action"])
        self.assertIn("decrement/compaction", gaps["W4-GAP-007"]["impact"])
        self.assertEqual(self.gaps["summary"]["status"], "controlled_open_gaps_ready_for_phase5_targeted_traces")


if __name__ == "__main__":
    unittest.main()
