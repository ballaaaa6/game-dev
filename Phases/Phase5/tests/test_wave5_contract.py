import json
from pathlib import Path
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[3]
PHASE5 = ROOT / "Phases" / "Phase5"


class Wave5ContractTests(unittest.TestCase):
    def test_room_manifest_keeps_partial_seb_and_adapter_boundary(self):
        manifest = json.loads((PHASE5 / "runtime" / "data" / "room_manifest.json").read_text(encoding="utf-8"))
        self.assertFalse(manifest["legacy_equivalence"])
        self.assertEqual(manifest["seb"]["tail_shortfall_bytes"], 4)
        self.assertIn("non_legacy", manifest["movement"]["walkable_status"])

    def test_locale_runtime_artifact_matches_current_csv_contract(self):
        artifact = json.loads((PHASE5 / "artifacts" / "wave5_locale_runtime.json").read_text(encoding="utf-8"))
        self.assertEqual(artifact["locale_count"], 12)
        self.assertEqual(artifact["union_record_count"], 2420)
        self.assertEqual(artifact["default_locale"], "th")
        self.assertEqual(artifact["qa"]["duplicate_id_count"], 0)
        self.assertEqual(artifact["qa"]["strict_utf8_failures"], 0)
        self.assertFalse(artifact["legacy_equivalence"])

    def test_js_runtime_contract(self):
        result = subprocess.run(
            ["node", str(PHASE5 / "tests" / "test_wave5_runtime.js")],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Wave 5 runtime tests passed", result.stdout)

    def test_visual_smoke_artifact_exists(self):
        screenshot = PHASE5 / "artifacts" / "wave5_smoke.jpg"
        self.assertTrue(screenshot.is_file())
        self.assertEqual(screenshot.read_bytes()[:3], b"\xff\xd8\xff")

    def test_w51_furniture_manifest_uses_real_source_families(self):
        artifact = json.loads((PHASE5 / "artifacts" / "wave5_1_furniture_manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(artifact["renderer_status"], "bounded_asset_renderer")
        self.assertEqual(len(artifact["records"]), 3)
        self.assertEqual({record["source_family"] for record in artifact["records"]}, {"reception", "desk", "chair"})
        self.assertTrue(all(record["placement_status"] == "adapter_fixture_not_legacy_verified" for record in artifact["records"]))

    def test_w51_transform_and_timer_contracts_keep_legacy_gaps_open(self):
        transform = json.loads((PHASE5 / "artifacts" / "wave5_1_transform_depth_contract.json").read_text(encoding="utf-8"))
        timer = json.loads((PHASE5 / "artifacts" / "wave5_1_timer_contract.json").read_text(encoding="utf-8"))
        self.assertEqual(transform["coordinate_profile"]["status"], "adapter_verified_fixture_specific")
        self.assertIn("universal world/object/crop/screen transform", transform["open_semantics"])
        self.assertEqual(timer["unit"], "logical_tick")
        self.assertEqual(timer["legacy_evidence"]["unit"], "unknown")

    def test_w51_build_manifest_tracks_bounded_inputs(self):
        manifest = json.loads((PHASE5 / "artifacts" / "wave5_build_manifest.json").read_text(encoding="utf-8"))
        self.assertIn("W5.2-furniture-mapping", manifest["stage"])
        self.assertEqual(len(manifest["files"]), 34)
        required = {
            "game-dev-story-mod_Sprites/office/reception_000.png",
            "game-dev-story-mod_Sprites/office/desk_000.png",
            "game-dev-story-mod_Sprites/office/chair_000.png",
            "Phases/Phase5/artifacts/wave5_1_furniture_manifest.json",
            "Phases/Phase5/artifacts/wave5_4_img_list_loader_bridge.json",
            "Phases/Phase5/artifacts/wave5_5_img_list_alignment.json",
            "Phases/Phase5/artifacts/wave5_6_floorparts_seb_contract.json",
            "Phases/Phase5/artifacts/wave5_7_seb_consumer_contract.json",
            "Phases/Phase5/artifacts/wave5_8_room_caller_contract.json",
            "Phases/Phase5/artifacts/wave5_9_object_producer_contract.json",
        }
        self.assertTrue(required.issubset({item["path"] for item in manifest["files"]}))
        self.assertTrue(all(item["exists"] and item["sha256"] for item in manifest["files"]))

    def test_w51_animation_selector_and_event_policies_are_explicit(self):
        animation = json.loads((PHASE5 / "artifacts" / "wave5_1_animation_policy.json").read_text(encoding="utf-8"))
        selectors = json.loads((PHASE5 / "artifacts" / "wave5_1_selector_gap_contract.json").read_text(encoding="utf-8"))
        events = json.loads((PHASE5 / "artifacts" / "wave5_1_event_mode_policy.json").read_text(encoding="utf-8"))
        self.assertFalse(animation["semantic_animation_verified"])
        self.assertEqual(animation["profiles"]["adapter.walk"]["mode_sequence"], [0, 1])
        self.assertEqual([item["classification"] for item in selectors["selectors"]], ["index_space_gap", "index_space_gap"])
        self.assertEqual(events["status"], "raw_only")
        self.assertEqual(events["raw_mode_storage"], "preserve_mode_and_args_without_semantic_name")

    def test_w52_furniture_mapping_separates_bihin_from_floor_parts(self):
        artifact = json.loads((PHASE5 / "artifacts" / "wave5_2_furniture_mapping_contract.json").read_text(encoding="utf-8"))
        slots = {item["family"]: item for item in artifact["load_contract"]["imgBihin_slots"]}
        self.assertEqual(slots["chair"]["slot"], 1)
        self.assertEqual(slots["desk"]["slot"], 2)
        self.assertEqual(artifact["load_contract"]["floor_parts_slot"]["image_field"], "imgFloorParts")
        self.assertEqual(artifact["load_contract"]["floor_parts_slot"]["selector_offset"], "0x1188")
        self.assertEqual(artifact["draw_contract"]["crop_status"], "field_flow_verified_numeric_crop_unresolved")
        self.assertEqual(artifact["status"], "mapping_contract_verified_with_selector_crop_placement_open")

    def test_w52_draw_fixture_keeps_crop_and_placement_boundaries_explicit(self):
        fixture = json.loads((PHASE5 / "artifacts" / "wave5_2_furniture_draw_fixture.json").read_text(encoding="utf-8"))
        self.assertEqual(len(fixture["objects"]), 3)
        self.assertTrue(all(item["source_rect"] is None for item in fixture["objects"]))
        self.assertEqual({item["legacy_image_slot"] for item in fixture["objects"]}, {"imgBihin_[1]", "imgBihin_[2]", "imgFloorParts"})
        self.assertIn("not recovered room placement", fixture["runtime_policy"]["placement"])

    def test_w53_numeric_selectors_floor_parts_and_crop_placement_contract(self):
        artifact = json.loads((PHASE5 / "artifacts" / "wave5_3_numeric_crop_placement_contract.json").read_text(encoding="utf-8"))
        fields = {item["name"]: item["value"] for item in artifact["selector_decode"]["fields"]}
        self.assertEqual({name: fields[name] for name in ("DDBody", "DDChair", "DDDesk", "DDPC")}, {
            "DDBody": 0,
            "DDChair": 25,
            "DDDesk": 26,
            "DDPC": 77,
        })
        self.assertEqual(artifact["floor_parts_selector"]["initial_value"], -1)
        self.assertEqual(len(artifact["image_data_tables"]["desk"]["metadata_rows"]), 3)
        self.assertEqual(len(artifact["image_data_tables"]["chair"]["metadata_rows"]), 3)
        self.assertEqual(artifact["crop_contract"]["draw_obj_fields"]["source_rect"], ["ObjecCX", "ObjecCY", "ObjecWX", "ObjecWY"])
        branches = {item["param_2"]: item["objects"] for item in artifact["placement_contract"]["call_hikkosi_branches"]}
        self.assertEqual([item["source_rect"] for item in branches[0]], [[100, 0, 33, 46], [133, 0, 17, 46]])
        self.assertEqual(len(branches[1]), 3)
        self.assertEqual(len(branches[2]), 4)
        self.assertEqual(artifact["img_list_namespace"]["asset_join_status"], "unresolved_namespace_join")
        self.assertFalse(artifact["legacy_equivalence"])

    def test_w54_img_list_loader_bridge_keeps_selector_namespaces_separate(self):
        artifact = json.loads((PHASE5 / "artifacts" / "wave5_4_img_list_loader_bridge.json").read_text(encoding="utf-8"))
        self.assertEqual(artifact["status"], "superseded_by_w5_5_label_alignment")
        self.assertEqual(artifact["superseded_by"], "Phases/Phase5/artifacts/wave5_5_img_list_alignment.json")
        self.assertEqual(artifact["verified_loader_bridge"]["appdata_get_image"]["resource_manager_fields"]["resGame_field"], "AppData+0x38")
        self.assertEqual(artifact["verified_loader_bridge"]["img_list_storage"]["length"], 80)
        selectors = {item["field"]: item for item in artifact["selector_namespace_probe"]["selectors"]}
        self.assertEqual({name: selectors[name]["selector_index"] for name in ("DDChair", "DDDesk", "DDPC")}, {
            "DDChair": 25,
            "DDDesk": 26,
            "DDPC": 77,
        })
        self.assertTrue(all(not item["manifest_matches"] for item in selectors.values()))
        self.assertTrue(all(item["status"] == "manifest_index_only" for item in artifact["manifest_candidates_not_promoted"]))
        self.assertEqual(artifact["cross_source_consistency"]["status"], "conflicting_evidence")
        self.assertEqual(artifact["cross_source_consistency"]["apk_global_metadata_table"]["first_observed_value_mismatch_literal_id"], 2395)
        self.assertTrue(any("Do not hardcode" in guardrail for guardrail in artifact["runtime_guardrails"]))
        self.assertFalse(artifact["legacy_equivalence"])

    def test_w55_corrects_literal_label_base_and_closes_bihin_filename_join(self):
        artifact = json.loads((PHASE5 / "artifacts" / "wave5_5_img_list_alignment.json").read_text(encoding="utf-8"))
        self.assertEqual(artifact["status"], "exact_bihin_selector_join_verified")
        self.assertEqual(artifact["parser_correction"]["correct_index_rule"], "zero_based_script_index = literal_label - 1")
        self.assertTrue(artifact["native_scriptstring"]["script_string_and_stringliteral_values_equal"])
        self.assertTrue(artifact["native_scriptstring"]["script_string_and_stringliteral_addresses_equal"])
        self.assertEqual(artifact["active_apk_global_metadata"]["metadata_join_count"], 80)
        self.assertEqual(artifact["active_apk_global_metadata"]["suffix_literal"]["native_value"], ".png")
        self.assertEqual(artifact["active_apk_global_metadata"]["face_prefix_literal"]["native_value"], "face_")
        self.assertEqual(artifact["summary"]["img_list_entry_count"], 80)
        self.assertEqual(artifact["summary"]["manifest_exact_filename_join_count"], 77)
        self.assertEqual(artifact["summary"]["manifest_normalized_face_join_count"], 3)
        self.assertEqual(artifact["summary"]["manifest_unresolved_join_count"], 0)
        self.assertEqual(artifact["summary"]["bihin_selector_exact_join_count"], 3)
        fields = artifact["selector_fields"]
        self.assertEqual({name: fields[name]["native_value"] for name in ("DDChair", "DDDesk", "DDPC")}, {
            "DDChair": "chair0_origin",
            "DDDesk": "desk0_origin",
            "DDPC": "pc",
        })
        self.assertEqual({name: fields[name]["manifest_resource_index"] for name in ("DDChair", "DDDesk", "DDPC")}, {
            "DDChair": 29,
            "DDDesk": 30,
            "DDPC": 117,
        })
        self.assertTrue(all(fields[name]["status"] == "verified_exact" for name in ("DDChair", "DDDesk", "DDPC")))
        self.assertFalse(artifact["legacy_equivalence"])

    def test_w56_closes_floorparts_selector_and_keeps_seb_room_semantics_open(self):
        artifact = json.loads((PHASE5 / "artifacts" / "wave5_6_floorparts_seb_contract.json").read_text(encoding="utf-8"))
        self.assertEqual(artifact["status"], "floorparts_selector_exact_seb_structure_verified_room_placement_open")
        selector = artifact["index_img_floor_parts"]
        self.assertEqual(selector["initial_value"], -1)
        self.assertEqual(selector["event_g_change"]["mode_1_branch"]["request"], "IMG_LIST[param_3] + StringLiteral_833")
        initial = selector["initial_callsite_resolution"]
        self.assertEqual(initial["field_value"], 39)
        self.assertEqual(initial["resolved_selector"], 42)
        self.assertEqual(initial["requested_filename"], "floorparts0.png")
        self.assertEqual(initial["manifest_resource_index"], 79)
        self.assertEqual(initial["callsite_count_resolved"], 2)
        floor_main = artifact["index_img_floor_main"]["verified_input_range_probe"]
        self.assertEqual([item["requested_filename"] for item in floor_main], ["floor0.png", "floor1.png", "floor2.png"])
        seb = artifact["seb_sample"]["independent_decode"]
        self.assertEqual(seb["group_count"], 1)
        self.assertEqual(seb["groups"][0]["record_count"], 1)
        self.assertEqual(seb["tail_shortfall_bytes"], 4)
        self.assertEqual(artifact["seb_loader"]["optional_tail"]["ascii_marker_value"], "RECT")
        self.assertEqual(artifact["room_placement"]["status"], "not_closed")
        self.assertFalse(artifact["legacy_equivalence"])

    def test_w57_closes_seb_crop_and_bounded_base_placement(self):
        artifact = json.loads((PHASE5 / "artifacts" / "wave5_7_seb_consumer_contract.json").read_text(encoding="utf-8"))
        self.assertEqual(artifact["status"], "seb_local_crop_and_external_base_placement_verified_room_world_transform_open")
        constants = artifact["seb_record_contract"]["constants"]
        self.assertEqual({name: constants[name] for name in ("SP_TEX_ID", "SP_U", "SP_V", "SP_W", "SP_H", "SP_TRANS_X", "SP_TRANS_Y")}, {
            "SP_TEX_ID": 1,
            "SP_U": 2,
            "SP_V": 3,
            "SP_W": 4,
            "SP_H": 5,
            "SP_TRANS_X": 6,
            "SP_TRANS_Y": 7,
        })
        draw = artifact["seb_draw_contract"]["core_consumer"]
        self.assertEqual(draw["source_formula"], "(u, v, w, h)")
        self.assertEqual(artifact["bounding_anchor_contract"]["external_base"]["status"], "bounded_external_base_placement_verified")
        self.assertEqual(artifact["floor0_probe"]["record_status"], "partial_final_record")
        self.assertEqual(artifact["floor0_probe"]["effective_local_draw"]["source_rect_u_v_w_h"], [0, 0, 600, 600])
        self.assertIn("universal world/object/crop/screen or isometric transform", artifact["room_placement"]["open"])
        self.assertFalse(artifact["legacy_equivalence"])

    def test_w58_closes_room_png_screen_placement_and_separates_seb_callers(self):
        artifact = json.loads((PHASE5 / "artifacts" / "wave5_8_room_caller_contract.json").read_text(encoding="utf-8"))
        self.assertEqual(artifact["status"], "room_png_screen_placement_verified_seb_room_mapping_open")
        screen = artifact["game_screen_entry"]
        self.assertEqual(screen["function"], "Method_form_GameForm_RenderGameScreen")
        self.assertEqual(screen["source_address"], "0x00f16edc")
        self.assertLess(screen["source_lines"]["set_origin"], screen["source_lines"]["draw_obj_call"])
        self.assertLess(screen["source_lines"]["draw_obj_call"], screen["source_lines"]["reset_origin"])
        self.assertEqual(screen["depth_boundary"]["draw_obj_set_depth_call_count"], 0)

        room = artifact["room_draw_path"]
        self.assertEqual(room["direct_img_floor_parts_branch"]["formula"], "DrawImage(ObjecX + ObjecZX, ObjecY + ObjecZY, GameForm.imgFloorParts, ObjecCX, ObjecCY, ObjecWX, ObjecWY, 0)")
        self.assertEqual(room["image_slots"]["imgFloorParts"]["offset"], "0x1128")
        self.assertEqual(room["image_slots"]["IndexImgFloorParts"]["offset"], "0x1188")
        self.assertEqual(room["seb_separation"]["resource_manager_seb_call_count_in_draw_obj"], 0)
        self.assertGreater(artifact["seb_caller_inventory"]["call_site_count"], 0)
        self.assertEqual(artifact["room_placement"]["status"], "png_room_screen_placement_bounded_seb_room_mapping_open")
        self.assertIn("direct caller or mapping from office/floor0.seb to the room floor renderer", artifact["room_placement"]["open"])
        self.assertFalse(artifact["legacy_equivalence"])

    def test_w59_closes_object_provenance_and_keeps_camera_world_seb_gaps_open(self):
        artifact = json.loads((PHASE5 / "artifacts" / "wave5_9_object_producer_contract.json").read_text(encoding="utf-8"))
        self.assertEqual(artifact["status"], "object_producer_bounded_camera_world_transform_open_seb_room_mapping_open")

        add_objec = artifact["add_objec_contract"]
        self.assertEqual(add_objec["source_address"], "0x00f33b54")
        self.assertEqual(add_objec["direct_call_site_count"], 9)
        parameter_map = add_objec["parameter_map"]
        self.assertEqual({name: parameter_map[name]["field"] for name in ("param_2", "param_3", "param_4", "param_5", "param_6", "param_7", "param_8", "param_9")}, {
            "param_2": "ObjecSyurui",
            "param_3": "ObjecX",
            "param_4": "ObjecY",
            "param_5": "ObjecCX",
            "param_6": "ObjecCY",
            "param_7": "ObjecWX",
            "param_8": "ObjecWY",
            "param_9": "ObjecSY",
        })
        self.assertEqual({name: add_objec["default_local_offsets"][name]["value"] for name in ("ObjecZX", "ObjecZY")}, {
            "ObjecZX": 0,
            "ObjecZY": 0,
        })

        producers = artifact["producer_inventory"]
        main_process = producers["main_process_xy_average_update"]
        self.assertEqual(set(main_process["source_assignment_lines"]), {"ObjecX", "ObjecY"})
        self.assertEqual(main_process["semantic_status"], "observed_arithmetic_update; source_array_semantics_not_recovered")
        self.assertEqual(set(main_process["source_fields"]), {"GameForm+0xE40", "GameForm+0xF50", "GameForm+0xF58"})
        for function in ("CallPCChange", "CallDeskChange", "CallChairChange"):
            update = producers["furniture_update_functions"][function]
            self.assertEqual(set(update["verified_update_fields"]), {"ObjecX", "ObjecY", "ObjecCX", "ObjecCY", "ObjecWX", "ObjecWY", "ObjecSY"})
            self.assertEqual(update["local_offset_write_count"], {"ObjecZX": 0, "ObjecZY": 0})
        callers = {item["caller_function"] for item in producers["call_graph"]["CallHikkosi"]["external_call_sites"]}
        self.assertEqual(callers, {"form_GameForm__LoadGameData", "form_SubForm__EventEnd"})
        self.assertEqual(producers["nonzero_local_offset_producer_scan"]["direct_writes_observed_outside_AddObjec"], 0)

        camera = artifact["camera_transform_boundary"]
        self.assertEqual(camera["c_evidence"]["OnTouchCamera"]["body_status"], "no_op_return")
        self.assertEqual(camera["c_evidence"]["SetOrigin"]["body_status"], "no_op_return")
        self.assertEqual(camera["status"], "producer_camera_world_isometric_transform_not_recovered")
        self.assertEqual(camera["named_camera_symbol_reference_count_in_c"], 0)

        seb = artifact["seb_mapping"]
        self.assertEqual(seb["draw_obj_resource_manager_seb_call_count"], 0)
        self.assertEqual(seb["direct_floor0_seb_drawobj_callsite_count"], 0)
        self.assertEqual(seb["literal_floor0_seb_count_in_c_sources"], 0)
        self.assertEqual(seb["generic_loadseb_bridge"]["status"], "generic_loadseb_bridge_not_room_mapping")
        self.assertFalse(artifact["legacy_equivalence"])


if __name__ == "__main__":
    unittest.main()
