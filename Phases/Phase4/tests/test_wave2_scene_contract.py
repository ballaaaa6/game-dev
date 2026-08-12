import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
ARTIFACTS = ROOT / "Phases" / "Phase4" / "artifacts"


def load(name: str):
    return json.loads((ARTIFACTS / name).read_text(encoding="utf-8"))


class Wave2SceneContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.adapter = load("wave2_selector_adapter.json")
        cls.scene = load("scene_contract.json")
        cls.room = load("wave2_room_contract.json")
        cls.coordinate = load("wave2_coordinate_contract.json")
        cls.coordinate_fixture = load("wave2_coordinate_fixture.json")
        cls.draw_order = load("wave2_draw_order_contract.json")
        cls.draw_order_fixture = load("wave2_draw_order_fixture.json")
        cls.furniture = load("wave2_furniture_contract.json")
        cls.placement = load("wave2_placement_fixture.json")
        cls.minimum_scene = load("wave2_minimum_scene_fixture.json")
        cls.movement_interface = load("wave2_wave3_movement_interface.json")
        cls.gaps = load("wave2_gap_register.json")
        cls.manifest = load("wave2_build_manifest.json")

    def test_wave2_artifacts_are_read_only_and_present(self):
        for name in (
            "wave2_selector_adapter.json",
            "scene_contract.json",
            "wave2_room_contract.json",
            "wave2_coordinate_contract.json",
            "wave2_coordinate_fixture.json",
            "wave2_draw_order_contract.json",
            "wave2_draw_order_fixture.json",
            "wave2_furniture_contract.json",
            "wave2_placement_fixture.json",
            "wave2_minimum_scene_fixture.json",
            "wave2_wave3_movement_interface.json",
            "wave2_gap_register.json",
            "wave2_build_manifest.json",
        ):
            self.assertTrue((ARTIFACTS / name).is_file(), name)
        self.assertTrue(self.adapter["source_roots_read_only"])
        self.assertTrue(self.scene["source_roots_read_only"])
        self.assertTrue(self.gaps["source_roots_read_only"])

    def test_symbolic_selector_policy_preserves_wave1_gaps(self):
        self.assertEqual(self.adapter["summary"]["static_selector_count"], 5)
        self.assertEqual(self.adapter["summary"]["numeric_static_values_decoded"], 0)
        self.assertEqual(
            self.adapter["policy"]["imgface_conflict_policy"],
            "retain StringLiteral_7514=false and face asset evidence as conflicting_evidence",
        )
        self.assertEqual(self.adapter["drawhuman_audit"]["tface_40_41_audit"]["status"], "index_space_mismatch")
        self.assertGreater(self.adapter["summary"]["tface_40_41_call_count"], 0)

    def test_selector_namespaces_are_explicit(self):
        names = {row["name"] for row in self.adapter["namespaces"]}
        self.assertEqual(
            names,
            {"selector_index", "resource_index", "img_array_slot", "filename_numeric_id"},
        )
        for selector in self.adapter["static_selectors"]:
            self.assertEqual(selector["resolution_status"], "dynamic_value_with_preconditions")
            self.assertEqual(selector["value_status"], "selector_index_not_decoded")
            self.assertEqual(selector["adapter_policy"], "symbolic_only_until_direct_numeric_value_is_recovered")

    def test_object_type_constants_and_required_fields_are_verified(self):
        constants = {row["name"]: row["value"] for row in self.scene["object_type_constants"]}
        self.assertEqual(
            constants,
            {
                "OBJ_TYPE_PARTS": 0,
                "OBJ_TYPE_HUMAN": 1,
                "OBJ_TYPE_DISPLAY": 3,
                "OBJ_TYPE_CHAIR": 4,
                "OBJ_TYPE_DESK": 5,
                "OBJ_TYPE_DESK_CEO": 6,
                "OBJ_TYPE_RECEPTION": 7,
            },
        )
        required = {
            "ObjecX", "ObjecY", "ObjecCX", "ObjecCY", "ObjecWX", "ObjecWY", "ObjecZX", "ObjecZY",
            "ObjecSY", "ObjecEnabled", "ObjecVisible", "ObjecSyurui", "ObjecMax", "ObjecIndex",
            "OfficeObjecList", "DeskZahyou", "DeskSyain", "DeskObjec", "ChairMainObjec", "ChairSubObjec", "PCObjec",
        }
        self.assertTrue(required.issubset(self.scene["field_map"]))
        self.assertEqual(self.scene["summary"]["field_count"], len(self.scene["field_map"]))

    def test_add_objec_argument_contract_is_explicit(self):
        mapping = {
            row["argument"]: row["field"]
            for row in self.scene["add_objec_contract"]["argument_to_field"]
        }
        self.assertEqual(
            mapping,
            {
                "param_2": "ObjecSyurui",
                "param_3": "ObjecX",
                "param_4": "ObjecY",
                "param_5": "ObjecCX",
                "param_6": "ObjecCY",
                "param_7": "ObjecWX",
                "param_8": "ObjecWY",
                "param_9": "ObjecSY",
            },
        )
        defaults = {row["field"]: row["value"] for row in self.scene["add_objec_contract"]["default_writes"]}
        self.assertEqual(defaults, {"ObjecEnabled": 1, "ObjecVisible": 1, "ObjecZX": 0, "ObjecZY": 0})

    def test_gap_register_has_no_unclassified_unknowns(self):
        allowed = set(self.gaps["controlled_statuses"])
        self.assertEqual(self.gaps["summary"]["unclassified_unknown_count"], 0)
        self.assertTrue(all(row["status"] in allowed for row in self.gaps["gaps"]))
        self.assertGreaterEqual(self.gaps["summary"]["gap_count"], 15)
        self.assertEqual(self.gaps["summary"]["current_wave2_gate"], "not_ready_for_wave2_scene_closure")

    def test_build_manifest_contains_source_hashes(self):
        hashes = self.manifest["source_hashes"]
        for path in (
            "game-dev-story-mod_Dumped/Categorized_Code/Global/form.c",
            "game-dev-story-mod_Dumped/dump.cs",
            "Phases/Phase4/artifacts/resource_selector_map.json",
        ):
            self.assertIn(path, hashes)
            self.assertRegex(hashes[path]["sha256"], r"^[0-9a-f]{64}$")

    def test_room_contract_uses_verified_floor_and_preserves_seb_limitation(self):
        fixture = self.room["room_fixture"]
        self.assertEqual(fixture["floor"]["path"], "office/floor0.png")
        self.assertEqual(fixture["seb"]["path"], "office/floor0.seb")
        self.assertEqual(fixture["floor"]["status"], "asset_verified")
        self.assertEqual(fixture["seb"]["tail_shortfall_bytes"], 4)
        self.assertEqual(fixture["placement_status"], "not_yet_resolved")
        self.assertGreaterEqual(self.room["summary"]["furniture_fixture_count"], 4)

    def test_coordinate_contract_keeps_transform_semantics_open(self):
        spaces = {row["name"]: row["status"] for row in self.coordinate["coordinate_spaces"]}
        self.assertEqual(len(spaces), 5)
        self.assertIn("object_record", spaces)
        self.assertEqual(self.coordinate["summary"]["transform_status"], "not_closed")
        self.assertEqual(self.coordinate["policy"]["isometric_label"], "do_not_assign_without direct transform evidence")

    def test_coordinate_fixture_covers_only_verified_center_origin_arithmetic(self):
        self.assertEqual(self.coordinate_fixture["expected"]["graphics_origin"], {"x": 280, "y": 180})
        self.assertEqual(self.coordinate_fixture["expected"]["width"]["selected_candidate"], 560)
        self.assertEqual(self.coordinate_fixture["expected"]["height"]["selected_candidate"], 360)
        self.assertEqual(self.coordinate_fixture["status"], "verified_formula_fixture_transform_semantics_still_open")
        self.assertIn("isometric projection", self.coordinate_fixture["not_claimed"])

    def test_draw_order_contract_contains_verified_dispatch_and_neutral_sort_semantics(self):
        dispatch = {row["object_type"]: row["renderer"] for row in self.draw_order["dispatch"]}
        self.assertEqual(dispatch["OBJ_TYPE_HUMAN"], "form.GameForm.DrawHuman")
        self.assertEqual(dispatch["OBJ_TYPE_CHAIR"], "form.GameForm.DrawChair")
        self.assertEqual(dispatch["OBJ_TYPE_DESK"], "form.GameForm.DrawDesk")
        self.assertEqual(dispatch["OBJ_TYPE_RECEPTION"], "form.GameForm.DrawReception")
        self.assertEqual(self.draw_order["summary"]["sort_pattern"], "compare_and_swap_verified")
        self.assertEqual(self.draw_order["summary"]["depth_semantics"], "not_closed")

    def test_draw_order_fixture_is_deterministic_but_semantically_neutral(self):
        self.assertEqual(self.draw_order_fixture["expected_draw_order"], [1, 2, 0])
        self.assertEqual(
            self.draw_order_fixture["sort_policy"]["candidate_key"],
            "ObjecSY + ObjecY",
        )
        self.assertEqual(
            self.draw_order_fixture["semantic_status"],
            "neutral_sort_probe_depth_meaning_not_closed",
        )

    def test_furniture_contract_traces_accessors_relations_and_open_semantics(self):
        self.assertEqual(self.furniture["summary"]["accessor_count"], 3)
        self.assertEqual(self.furniture["summary"]["relation_trace_count"], 4)
        self.assertEqual(
            {row["array_field"] for row in self.furniture["image_data_accessors"]},
            {"PCImgData", "DeskImgData", "ChairImgData"},
        )
        self.assertTrue(all(row["status"] == "verified_accessor_and_slot_normalization" for row in self.furniture["image_data_accessors"]))
        self.assertEqual(self.furniture["seat_contract"]["status"], "not_closed")
        self.assertEqual(self.furniture["collision_contract"]["status"], "not_found_in_scoped_scene_functions")
        self.assertEqual(self.furniture["walkable_contract"]["status"], "not_found_in_scoped_scene_functions")

    def test_placement_fixture_preserves_bounded_trace_without_guessed_room_values(self):
        self.assertEqual(self.placement["input"]["CallHikkosi_param_2"], 0)
        self.assertEqual(self.placement["expected"]["source_array"], "DeskImgData")
        self.assertEqual(self.placement["expected"]["result_written_to"], "OfficeObjecList")
        self.assertIn("selected office record numeric value", self.placement["unresolved"])
        self.assertEqual(self.placement["status"], "relation_contract_fixture_only")

    def test_minimum_scene_fixture_connects_room_object_coordinate_and_draw_boundaries(self):
        self.assertEqual(self.minimum_scene["room"]["floor"]["path"], "office/floor0.png")
        self.assertEqual(self.minimum_scene["coordinate"]["graphics_origin"], {"x": 280, "y": 180})
        bounded = self.minimum_scene["objects"]["bounded_placement_record"]
        self.assertEqual(bounded["candidate_sort_key"], 93)
        self.assertEqual(bounded["object_type_status"], "symbolic_only_selected_desk_record_plus_5")
        probe = self.minimum_scene["objects"]["known_dispatch_probe"]
        self.assertEqual(probe["renderer"], "form.GameForm.DrawReception")
        self.assertEqual(probe["draw_command"]["crop"], [100, 0, 33, 46])
        self.assertEqual(self.minimum_scene["status"], "minimum_scene_contract_ready_with_symbolic_room_object_type")

    def test_wave3_movement_interface_exposes_adapter_boundary_without_legacy_claims(self):
        self.assertEqual(self.movement_interface["seat"]["output"], "seat_occupancy_state")
        self.assertEqual(self.movement_interface["collision"]["output"], "blocked | clear | unavailable")
        self.assertEqual(self.movement_interface["walkable"]["output"], "path | no_path | unavailable")
        self.assertEqual(self.movement_interface["status"], "wave3_interface_ready_with_legacy_semantics_open")
        self.assertTrue(self.movement_interface["non_goals"])


if __name__ == "__main__":
    unittest.main()
