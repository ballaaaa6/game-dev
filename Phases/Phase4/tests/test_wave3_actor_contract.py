import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
PHASE = ROOT / "Phases" / "Phase4"
ARTIFACTS = PHASE / "artifacts"
DOCS = PHASE / "docs" / "wave3_slices"


def load(name: str):
    return json.loads((ARTIFACTS / name).read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


class Wave3ActorContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.actor_map = load("wave3_actor_function_map.json")
        cls.gaps = load("wave3_gap_register.json")
        cls.manifest = load("wave3_build_manifest.json")
        cls.movement = load("wave2_wave3_movement_interface.json")

    def test_w3c0_artifacts_and_slices_are_present(self):
        for name in (
            "wave3_actor_function_map.json",
            "wave3_gap_register.json",
            "wave3_build_manifest.json",
        ):
            self.assertTrue((ARTIFACTS / name).is_file(), name)
        for name in ("actor_spawn_01.md", "actor_tick_01.md"):
            self.assertTrue((DOCS / name).is_file(), name)
        self.assertTrue(self.actor_map["source_roots_read_only"])
        self.assertTrue(self.gaps["source_roots_read_only"])

    def test_function_scope_contains_actor_boundaries(self):
        rows = {row["symbol"]: row for row in self.actor_map["scope"]["functions"]}
        expected = {
            "form_GameForm__AddSyain",
            "form_GameForm__CallSyain",
            "form_GameForm__NextTarget",
            "form_GameForm__AddTarget",
            "form_GameForm__MainProcess",
            "form_GameForm__DoEvent",
            "form_GameForm__DrawHuman",
            "form_GameForm__DrawObj",
            "form_GameForm__CallHikkosi",
            "form_GameForm__ProcessEvent",
        }
        self.assertEqual(set(rows), expected)
        self.assertEqual(rows["form_GameForm__DoEvent"]["source_status"], "assembly_fallback_only")
        self.assertEqual(len(rows["form_GameForm__DoEvent"]["c_definitions"]), 0)
        self.assertEqual(len(rows["form_GameForm__DrawHuman"]["c_definitions"]), 2)
        self.assertTrue(rows["form_GameForm__CallSyain"]["c_definitions"])

    def test_field_groups_and_offsets_are_registered_without_semantic_promotion(self):
        field_map = self.actor_map["scope"]["field_map"]
        expected_groups = {
            "identity_binding",
            "position",
            "target_points",
            "state_timing",
            "composition",
            "interaction_relations",
        }
        self.assertEqual(set(self.actor_map["scope"]["field_groups"]), expected_groups)
        self.assertEqual(self.actor_map["summary"]["field_count"], len(field_map))
        for field in field_map.values():
            self.assertEqual(field["status"], "verified_dump_field_declaration")
            self.assertEqual(field["semantic_status"], "field_declared_offset_references_only")
            self.assertIn("offset_reference_samples", field)
            self.assertEqual(
                field["semantic_policy"],
                "do_not_assign Agent meaning from field name or offset alone",
            )
        self.assertIn("form_GameForm__NextTarget", field_map["HumanX"]["offset_reference_functions"])
        self.assertIn("form_GameForm__NextTarget", field_map["HumanY"]["offset_reference_functions"])
        self.assertIn("form_GameForm__CallSyain", field_map["HumanSyain"]["offset_reference_functions"])

    def test_call_graph_keeps_spawn_target_and_draw_edges(self):
        pairs = {
            (edge["caller"], edge["callee"])
            for edge in self.actor_map["call_graph_edges"]
        }
        self.assertIn(("form_GameForm__CallSyain", "form_GameForm__AddObjec"), pairs)
        self.assertIn(("form_GameForm__CallSyain", "form_GameForm__NextTarget"), pairs)
        self.assertIn(("form_GameForm__DrawObj", "form_GameForm__DrawHuman"), pairs)
        self.assertIn(("form_GameForm__MainProcess", "form_GameForm__NextTarget"), pairs)

    def test_gap_register_has_controlled_statuses_and_no_unclassified_unknowns(self):
        allowed = set(self.gaps["controlled_statuses"])
        self.assertEqual(self.gaps["summary"]["unclassified_unknown_count"], 0)
        self.assertTrue(all(row["status"] in allowed for row in self.gaps["gaps"]))
        self.assertEqual(self.gaps["summary"]["gap_count"], len(self.gaps["gaps"]))
        self.assertEqual(
            self.gaps["summary"]["current_wave3_gate"],
            "w3_c0_baseline_ready_for_bounded_spawn_and_state_slices",
        )
        statuses = {row["status"] for row in self.gaps["gaps"]}
        self.assertIn("recoverable", statuses)
        self.assertIn("not_found_in_scoped_functions", statuses)
        self.assertIn("out_of_scope", statuses)

    def test_manifest_contains_current_source_hashes(self):
        hashes = self.manifest["source_hashes"]
        for relative in (
            "game-dev-story-mod_Dumped/Categorized_Code/Global/form.c",
            "game-dev-story-mod_Dumped/dump.cs",
            "game-dev-story-mod_Dumped/script.json",
            "Phases/Phase4/artifacts/function_inventory.json",
            "Phases/Phase4/artifacts/wave2_build_manifest.json",
            "Phases/Phase4/artifacts/wave2_wave3_movement_interface.json",
        ):
            self.assertIn(relative, hashes)
            path = ROOT / Path(relative)
            self.assertEqual(hashes[relative]["bytes"], path.stat().st_size)
            self.assertEqual(hashes[relative]["sha256"], sha256(path))

    def test_inherited_movement_boundary_is_explicitly_non_legacy(self):
        self.assertEqual(self.movement["status"], "wave3_interface_ready_with_legacy_semantics_open")
        self.assertEqual(self.movement["collision"]["output"], "blocked | clear | unavailable")
        self.assertEqual(self.movement["walkable"]["output"], "path | no_path | unavailable")
        self.assertEqual(self.movement["seat"]["output"], "seat_occupancy_state")
        self.assertTrue(self.movement["non_goals"])

    def test_slices_preserve_stop_rules_and_source_boundaries(self):
        spawn = (DOCS / "actor_spawn_01.md").read_text(encoding="utf-8")
        tick = (DOCS / "actor_tick_01.md").read_text(encoding="utf-8")
        self.assertIn("form_GameForm__CallSyain", spawn)
        self.assertIn("ยังไม่ claim ว่า `HumanMode=0` คือ `idle`", spawn)
        self.assertIn("form_GameForm__DoEvent", tick)
        self.assertIn("assembly fallback", tick)
        self.assertIn("ไม่ขยาย `MainProcess`", tick)


if __name__ == "__main__":
    unittest.main()
