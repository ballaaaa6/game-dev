import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
PHASE = ROOT / "Phases" / "Phase4"
ARTIFACTS = PHASE / "artifacts"
BUILDER = PHASE / "tools" / "build_wave4_dialogue_contract.py"


def load(name):
    return json.loads((ARTIFACTS / name).read_text(encoding="utf-8"))


class Wave4DialogueContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = load("wave4_build_manifest.json")
        cls.gaps = load("wave4_gap_register.json")
        cls.locale = load("wave4_locale_contract.json")
        cls.locale_fixture = load("wave4_locale_fixture.json")
        cls.talk = load("wave4_talk_contract.json")
        cls.talk_fixture = load("wave4_talk_fixture.json")
        cls.bubble = load("wave4_bubble_contract.json")
        cls.bubble_fixture = load("wave4_bubble_fixture.json")
        cls.event = load("wave4_event_contract.json")
        cls.event_fixture = load("wave4_event_fixture.json")
        cls.actor = load("wave4_actor_dialogue_fixture.json")

    def test_builder_is_reproducible(self):
        result = subprocess.run(
            [sys.executable, str(BUILDER), "--check"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)

    def test_manifest_freezes_read_only_sources_and_wave_scope(self):
        self.assertTrue(self.manifest["source_roots_read_only"])
        self.assertFalse(self.manifest["legacy_equivalence"])
        self.assertEqual(self.manifest["packages"]["W4-C0"], "baseline_manifest_and_gap_register")
        self.assertEqual(
            self.manifest["packages"]["W4-C6"],
            "message_notification_bridge_contract_ready_consumer_slice_open",
        )
        self.assertTrue(self.manifest["source_hashes"])

    def test_locale_contract_covers_current_csvs_without_guessing_english(self):
        self.assertEqual(self.locale["locale_count"], 12)
        self.assertEqual(self.locale["summary"]["duplicate_id_count"], 0)
        self.assertEqual(self.locale["summary"]["bom_failures"], 0)
        self.assertEqual(self.locale["summary"]["strict_utf8_failures"], 0)
        self.assertEqual(self.locale["runtime_contract"]["english_source_status"], "not_present_in_current_language_directory")
        self.assertEqual(self.locale["runtime_contract"]["default_locale"], "th")
        self.assertIn("placeholder_validation", [case["id"] for case in self.locale_fixture["cases"]])

    def test_talk_contract_separates_namespaces_and_raw_speakers(self):
        self.assertEqual(
            self.talk["namespaces"]["talk_tag"],
            "source record lookup key; not a language ID",
        )
        self.assertEqual(self.talk["special_raw_speaker_ids"]["values"], [-5, -4, -3, -2])
        self.assertFalse(self.talk["runtime_contract"]["legacy_equivalence"])
        symbols = [row["symbol"] for row in self.talk["functions"]]
        for symbol in [
            "main_AppData__GetTalkTexts",
            "form_GameForm__GetTalkIndex",
            "form_GameForm__AddKaiwaTalkData",
            "form_GameForm__GetHumanTalkName",
            "form_GameForm__AddKaiwa",
        ]:
            self.assertIn(symbol, symbols)

    def test_bubble_contract_keeps_raw_fields_and_timer_open(self):
        fields = [row["field"] for row in self.bubble["fields"]]
        for field in ["fukiList", "FukiMax", "HumanFukiTime", "HumanFukiIndex"]:
            self.assertIn(field, fields)
        self.assertEqual(self.bubble["runtime_contract"]["expiry_unit"], "unknown_until_MainProcess_consumer_trace")
        self.assertFalse(self.bubble["runtime_contract"]["legacy_equivalence"])
        self.assertEqual(self.bubble_fixture["adapter_clock"]["frame_ms"], 100)

    def test_event_contract_indexes_producers_but_does_not_name_modes(self):
        self.assertEqual(self.event["producer"]["callsite_count"], 53)
        self.assertEqual(self.event["consumer"]["source_status"], "assembly_fallback_only")
        self.assertEqual(self.event["semantic_status"], "event_modes_not_named_without_consumer_evidence")
        self.assertFalse(self.event["legacy_equivalence"])
        self.assertIsNone(self.event_fixture["cases"][1]["expected"]["semantic_label"])

    def test_actor_dialogue_trace_preserves_adapter_boundary(self):
        self.assertFalse(self.actor["legacy_equivalence"])
        events = [row["event"] for row in self.actor["trace"]]
        self.assertEqual(
            events,
            ["spawn", "dialogue_request", "talk_lookup", "bubble_attach", "bubble_draw", "bubble_expire"],
        )
        self.assertIn("talking is not a recovered HumanMode semantic", self.actor["not_claimed"])

    def test_gap_register_has_controlled_statuses(self):
        allowed = set(self.gaps["controlled_statuses"])
        self.assertEqual(self.gaps["summary"]["unclassified_unknown_count"], 0)
        self.assertEqual(len(self.gaps["gaps"]), 7)
        for gap in self.gaps["gaps"]:
            self.assertIn(gap["status"], allowed)
            self.assertTrue(gap["next_action"])
            self.assertTrue(gap["evidence"])


if __name__ == "__main__":
    unittest.main()
