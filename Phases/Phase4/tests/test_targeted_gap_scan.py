import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
ARTIFACT = ROOT / "Phases" / "Phase4" / "artifacts" / "targeted_gap_scan.json"
BUILDER = ROOT / "Phases" / "Phase4" / "tools" / "build_targeted_gap_scan.py"


class TargetedGapScanTests(unittest.TestCase):
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

    def test_wave0_uncovered_function_inventory_is_explicit(self):
        symbols = {row["symbol"] for row in self.value["wave0_uncovered_functions"]}
        self.assertEqual(
            symbols,
            {
                "form_GameForm__NewGamePara",
                "form_GameForm__DoEvent",
                "kairo_unity_util_JarInflater__GetInputStream",
                "form_GameForm__GameScreenLayout",
                "form_GameForm__RenderGameScreen",
            },
        )
        by_symbol = {row["symbol"]: row for row in self.value["wave0_uncovered_functions"]}
        self.assertEqual(by_symbol["form_GameForm__NewGamePara"]["assembly_structure"]["instruction_count"], 13671)
        self.assertEqual(by_symbol["form_GameForm__DoEvent"]["assembly_structure"]["instruction_count"], 15569)

    def test_tface_scan_keeps_40_41_unresolved(self):
        scan = self.value["tface_scan"]
        self.assertEqual(scan["symbol_reference_count"], 106)
        self.assertEqual(scan["parsed_callsite_count"], 36)
        self.assertEqual(scan["unparsed_symbol_reference_count"], 70)
        self.assertEqual(scan["literal_tface_40_callsite_count"], 9)
        self.assertEqual(scan["literal_tface_41_callsite_count"], 1)
        self.assertIn("remains unresolved", scan["asset_boundary"]["status"])

    def test_room_scan_preserves_no_direct_floor0_seb_caller_claim(self):
        room = self.value["room_seb_scan"]
        self.assertEqual(room["direct_floor0_seb_occurrence_count_in_scoped_sources"], 0)
        self.assertEqual(room["known_later_contracts"]["object_producer"]["direct_floor0_seb_drawobj_callsite_count"], 0)
        self.assertEqual(room["known_later_contracts"]["object_producer"]["named_camera_symbol_reference_count_in_c"], 0)

    def test_event_scan_is_inventory_not_semantic_promotion(self):
        self.assertIn("form_GameForm__AddMessage", self.value["event_touch_scan"]["calls"])
        self.assertEqual(self.value["event_touch_scan"]["policy"]["status"], "no_numeric_mode_promoted")
        statuses = {row["status"] for row in self.value["conclusions"]}
        self.assertIn("evidence_collected_not_closed", statuses)
        self.assertIn("unresolved", statuses)


if __name__ == "__main__":
    unittest.main()
