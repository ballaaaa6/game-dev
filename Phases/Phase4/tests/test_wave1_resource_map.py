import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
ARTIFACTS = ROOT / "Phases" / "Phase4" / "artifacts"


def load(name: str):
    return json.loads((ARTIFACTS / name).read_text(encoding="utf-8"))


class Wave1ResourceMapTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.resource_map = load("resource_selector_map.json")
        cls.branch_index = load("wave1_branch_index.json")
        cls.manifest = load("wave1_build_manifest.json")

    def manifest_for(self, suffix: str):
        return next(row for row in self.resource_map["manifests"] if row["manifest"].endswith(suffix))

    def record_for(self, manifest, filename: str):
        return next(row for row in manifest["records"] if row["filename"] == filename)

    def test_wave1_artifacts_are_present_and_read_only_contract_is_explicit(self):
        self.assertTrue(self.resource_map["source_roots_read_only"])
        self.assertTrue(self.manifest["source_roots_read_only"])
        self.assertEqual(self.resource_map["summary"]["manifest_count"], 4)
        for name in (
            "resource_selector_map.json",
            "wave1_branch_index.json",
            "wave1_build_manifest.json",
        ):
            self.assertTrue((ARTIFACTS / name).is_file(), name)

    def test_initial_gap_register_has_no_unclassified_unknowns(self):
        gap_register = load("wave1_gap_register.json")
        self.assertEqual(gap_register["stage"], "W1-C4-bounded-slices")
        self.assertEqual(
            gap_register["summary"]["current_wave1_gate"],
            "ready_for_wave2_with_known_limitations",
        )
        self.assertTrue(gap_register["source_roots_read_only"])
        self.assertEqual(gap_register["summary"]["unclassified_unknown_count"], 0)
        self.assertEqual(gap_register["summary"]["gap_count"], len(gap_register["gaps"]))
        allowed = set(gap_register["controlled_statuses"])
        self.assertTrue(all(row["status"] in allowed for row in gap_register["gaps"]))

    def test_selector_resolution_records_write_provenance_without_guessing_values(self):
        resolution = load("wave1_selector_resolution.json")
        self.assertEqual(resolution["summary"]["write_provenance_found"], 5)
        self.assertEqual(resolution["summary"]["numeric_selector_values_decoded"], 0)
        self.assertEqual(resolution["address_namespace"]["export_to_raw_delta"], "-0x100000")
        for selector in resolution["selectors"]:
            self.assertEqual(selector["resolution_status"], "dynamic_value_with_preconditions")
            self.assertEqual(selector["value_status"], "selector_index_not_decoded")
            self.assertRegex(selector["write_site"]["raw_elf_address"], r"^0x[0-9a-f]+$")

    def test_imgface_conflict_is_confirmed_by_raw_loop_and_not_silently_corrected(self):
        conflict = load("wave1_imgface_conflict.json")
        self.assertEqual(conflict["verdict"]["status"], "conflicting_evidence")
        self.assertEqual(conflict["raw_trace"]["loop"]["prefix_pointer_load"]["literal_symbol"], "PTR_StringLiteral_7514")
        self.assertFalse(conflict["literal_values"]["7513"]["raw_loop_reference"])
        self.assertEqual(conflict["literal_values"]["7514"]["value"], "false")
        self.assertEqual(conflict["asset_evidence"]["family"], "face")

    def test_asset_gap_audit_classifies_manifest_and_tface_gaps(self):
        audit = load("wave1_asset_gap_audit.json")
        self.assertEqual(audit["summary"]["manifest_records_audited"], 291)
        self.assertEqual(audit["summary"]["manifest_records_missing"], 0)
        self.assertEqual(audit["tface_40_41"]["status"], "index_space_mismatch")
        self.assertEqual(audit["tface_40_41"]["imgFace_array_length"], 36)
        self.assertEqual(audit["summary"]["unclassified_unknown_count"], 0)
        for row in audit["manifest_audit"]:
            self.assertEqual(row["status"], "asset_verified")

    def test_game_manifest_preserves_lexical_manifest_order_as_resource_indices(self):
        game = self.manifest_for("game/img.inf")
        self.assertEqual(self.record_for(game, "body0.png")["resource_index"], 1)
        self.assertEqual(self.record_for(game, "body1.png")["resource_index"], 2)
        self.assertEqual(self.record_for(game, "body10.png")["resource_index"], 3)
        self.assertNotEqual(
            self.record_for(game, "body10.png")["resource_index"],
            10,
            "resource lookup must not infer an index from the filename suffix",
        )

    def test_office_unindexed_entries_use_lowest_unused_index(self):
        office = self.manifest_for("office/img.inf")
        self.assertEqual(self.record_for(office, "chair_000.png")["resource_index"], 10)
        self.assertEqual(self.record_for(office, "chair_001.png")["resource_index"], 20)
        self.assertEqual(self.record_for(office, "chair_000.png")["assignment"], "lowest_unused_index")

    def test_static_img_list_and_selector_gaps_are_recorded(self):
        static_list = self.resource_map["gameform_img_list"]
        self.assertEqual(static_list["status"], "verified_from_recovered_c")
        self.assertEqual(static_list["length"], 80)
        body1 = static_list["entries"][0]
        self.assertEqual(body1["base_name"], "body1")
        self.assertEqual(body1["manifest_matches"][0]["resource_index"], 2)
        floor_cover = static_list["entries"][41]
        self.assertEqual(floor_cover["mapping_status"], "resolved")
        self.assertEqual(floor_cover["manifest_matches"][0]["asset_path"], "game-dev-story-mod_Sprites/game/floorCover.png")

        face = next(row for row in self.resource_map["selector_contracts"] if row["family"] == "face")
        self.assertEqual(face["count"], 36)
        self.assertEqual(face["prefix_value"], "false")
        self.assertEqual(face["mapping_status"], "unknown")

        body = next(row for row in self.resource_map["selector_contracts"] if row["family"] == "body")
        self.assertEqual(body["mapping_status"], "base_selector_value_unknown")

    def test_fixtures_cover_expected_extracted_asset_families(self):
        self.assertEqual(self.resource_map["summary"]["fixture_count"], 10)
        self.assertTrue(
            {
                "body",
                "face",
                "floor",
                "event",
                "chair",
                "desk",
                "pc",
                "reception",
            }.issubset(self.resource_map["summary"]["fixture_families"])
        )
        for fixture in self.resource_map["fixtures"]:
            self.assertRegex(fixture["expected"]["sha256"], r"^[0-9a-f]{64}$")
            self.assertGreater(fixture["expected"]["bytes"], 0)

    def test_assembly_index_has_structural_entries_for_both_wave1_targets(self):
        for symbol in ("form_GameForm__NewGamePara", "form_GameForm__DoEvent"):
            function = self.branch_index["functions"][symbol]
            self.assertEqual(function["status"], "structural_assembly_index")
            self.assertEqual(function["raw_address_delta"], -0x100000)
            self.assertEqual(
                int(function["entry"], 16) - int(function["raw_entry"], 16),
                0x100000,
            )
            self.assertGreater(function["instruction_count"], 10000)
            self.assertGreater(function["branch_count"], 0)
            self.assertGreater(function["basic_block_count"], 0)
            self.assertGreater(len(function["branches"]), 0)

    def test_bounded_assembly_slices_cover_both_wave1_targets(self):
        slices = load("wave1_slices.json")
        self.assertEqual(slices["stage"], "W1-C4-bounded-slices")
        self.assertTrue(slices["source_roots_read_only"])
        self.assertEqual(slices["address_namespace"]["export_to_raw_delta"], "-0x100000")
        self.assertEqual(slices["summary"]["slice_count"], 2)
        self.assertEqual(slices["summary"]["unclassified_unknown_count"], 0)
        functions = {row["function"] for row in slices["slices"]}
        self.assertEqual(
            functions,
            {"form.GameForm$$NewGamePara", "form.GameForm$$DoEvent"},
        )
        for row in slices["slices"]:
            self.assertTrue((ROOT / row["document"]).is_file(), row["document"])
            self.assertGreater(len(row["basic_blocks"]), 0)
            self.assertGreater(len(row["calls"]), 0)
            self.assertRegex(row["export_range"][0], r"^0x[0-9a-f]+$")
            self.assertRegex(row["raw_range"][0], r"^0x[0-9a-f]+$")

    def test_bounded_slices_keep_unresolved_helpers_explicit(self):
        slices = load("wave1_slices.json")
        unresolved = [
            call
            for row in slices["slices"]
            for call in row["calls"]
            if call["status"] == "unresolved_helper"
        ]
        self.assertEqual(len(unresolved), 2)
        self.assertTrue(all(call["symbol"] is None for call in unresolved))
        mapped = [
            call
            for row in slices["slices"]
            for call in row["calls"]
            if call["status"] == "mapped_from_script_json"
        ]
        self.assertEqual(len(mapped), 4)


if __name__ == "__main__":
    unittest.main()
