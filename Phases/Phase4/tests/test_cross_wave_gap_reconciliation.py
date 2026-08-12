import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
ARTIFACT = ROOT / "Phases" / "Phase4" / "artifacts" / "cross_wave_gap_reconciliation.json"
BUILDER = ROOT / "Phases" / "Phase4" / "tools" / "build_cross_wave_gap_reconciliation.py"


class CrossWaveGapReconciliationTests(unittest.TestCase):
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

    def test_reconciliation_has_current_and_historical_views(self):
        self.assertEqual(self.value["schema_version"], "phase4-cross-wave-gap-reconciliation-v1")
        self.assertEqual(self.value["status"], "reconciled_with_open_gaps")
        self.assertTrue(self.value["source_roots_read_only"])
        self.assertEqual(self.value["historical_registers"]["register_count"], 6)

    def test_later_evidence_supersedes_stale_selector_and_placement_statuses(self):
        keys = {row["gap_key"] for row in self.value["resolved_later"]}
        self.assertTrue(
            {
                "selector_base_values",
                "imgface_prefix_suffix",
                "bihin_filename_metadata_join",
                "floorparts_selector_join",
                "seb_consumer_local_placement",
                "png_room_screen_placement",
                "object_producer_field_provenance",
            }.issubset(keys)
        )

    def test_material_open_gaps_are_not_falsely_closed(self):
        keys = {row["gap_key"] for row in self.value["open_recoverable"]}
        self.assertTrue(
            {
                "newgamepara_branch_semantics",
                "doevent_dispatch_lifecycle",
                "tface_40_41_namespace",
                "universal_room_transform",
                "seb_room_caller_mapping",
            }.issubset(keys)
        )
        self.assertEqual(self.value["summary"]["open_recoverable_count"], 9)

    def test_all_referenced_evidence_files_exist(self):
        rows = self.value["resolved_later"] + self.value["open_recoverable"] + self.value["open_not_found_scoped"] + self.value["product_boundaries"]
        refs = [ref for row in rows for ref in row["evidence"]]
        self.assertGreater(len(refs), 20)
        self.assertTrue(all(ref["exists"] for ref in refs))

    def test_wave6_is_classified_as_product_boundary(self):
        keys = {row["gap_key"] for row in self.value["product_boundaries"]}
        self.assertIn("phase6_persistence_backend", keys)
        self.assertIn("phase6_ai_and_navigation", keys)


if __name__ == "__main__":
    unittest.main()
