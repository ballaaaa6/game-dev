import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
ARTIFACTS = ROOT / "Phases" / "Phase4" / "artifacts"


def load(name):
    return json.loads((ARTIFACTS / name).read_text(encoding="utf-8"))


class Wave3AnimationContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract = load("wave3_actor_animation_contract.json")
        cls.fixture = load("wave3_draw_fixture.json")
        cls.manifest = load("wave3_c5_build_manifest.json")

    def test_c5_artifacts_are_present_and_read_only(self):
        for name in self.manifest["artifact_outputs"]:
            self.assertTrue((ROOT / name).is_file(), name)
        self.assertTrue(self.contract["source_roots_read_only"])

    def test_selector_namespaces_are_separate(self):
        namespaces = {row["namespace"]: row for row in self.contract["selector_namespaces"]}
        self.assertEqual(namespaces["legacy_draw_selector"]["fields"], ["TFace", "TBody", "TMode", "TKage"])
        self.assertEqual(namespaces["actor_selector_source"]["status"], "raw_source_only")
        self.assertEqual(namespaces["raw_actor_state"]["status"], "raw_state_not_selector_mapping")
        self.assertEqual(namespaces["bodyface_record"]["status"], "verified_record_only")

    def test_selector_flows_and_composition_are_evidence_backed(self):
        flows = {row["flow_id"]: row for row in self.contract["selector_flows"]}
        self.assertEqual(len(flows), 2)
        self.assertEqual(flows["office_drawobj_actor"]["status"], "verified_bounded_actor_draw_callsite_selector_sources_partial")
        self.assertEqual(flows["human_dex_preview_draw"]["status"], "verified_dynamic_selector_flow_not_agent_semantic_mapping")
        composition = self.contract["composition_contract"]
        self.assertEqual(composition["status"], "verified_with_mode_dependent_branches")
        self.assertEqual(composition["bodyface_record_contract"]["body"]["image_array"], "imgBody")
        self.assertEqual(composition["bodyface_record_contract"]["face"]["image_array"], "imgFace")
        self.assertTrue(all(ref["line"] for ref in composition["drawhuman_evidence"]))

    def test_tface_40_41_are_preserved_as_unresolved(self):
        cases = self.contract["literal_selector_cases"]
        self.assertGreaterEqual(len(cases), 4)
        values = {row["TFace"] for row in cases}
        self.assertIn(40, values)
        self.assertIn(41, values)
        for row in cases:
            self.assertEqual(row["asset_resolution_status"], "extraction_missing_or_index_space_gap")
            self.assertEqual(row["semantic_status"], "unknown")
            self.assertIn("do_not substitute", row["runtime_policy"])

    def test_fixture_has_deterministic_body_face_commands(self):
        scenarios = {row["id"]: row for row in self.fixture["scenarios"]}
        draw = scenarios["actor_draw_mode_0"]["expected"]
        self.assertEqual(draw["status"], "draw_command_ready")
        self.assertEqual(draw["commands"][0]["source_rect"], [0, 0, 16, 16])
        self.assertEqual(draw["commands"][0]["destination"], [100, 214])
        self.assertEqual(draw["commands"][1]["source_rect"], [48, 0, 16, 15])
        self.assertEqual(draw["commands"][1]["destination"], [101, 201])
        self.assertIsNone(draw["semantic_state"])
        self.assertEqual(scenarios["tface_40_unresolved"]["expected"]["fallback_face"], None)
        self.assertEqual(scenarios["tface_41_unresolved"]["expected"]["fallback_face"], None)

    def test_animation_semantics_remain_open(self):
        semantics = self.contract["animation_semantics"]
        self.assertEqual(semantics["verified_semantic_animations"], 0)
        self.assertEqual(semantics["probable_semantic_animations"], 0)
        self.assertEqual(semantics["talking_candidate"]["raw_modes"], [8, 9])
        self.assertIsNone(semantics["talking_candidate"]["timing"])
        self.assertEqual(semantics["raw_anime_tick_boundary"]["threshold"], 15)
        self.assertIsNone(semantics["raw_anime_tick_boundary"]["meaning"])

    def test_manifest_summary_and_mapping_are_not_promoted(self):
        summary = self.manifest["artifact_summary"]
        self.assertEqual(summary["selector_flow_count"], 2)
        self.assertEqual(summary["bodyface_record_count"], 42)
        self.assertEqual(summary["tface_40_41_case_count"], len(self.contract["literal_selector_cases"]))
        self.assertEqual(summary["scenario_count"], 5)
        self.assertEqual(self.contract["phase2_mapping_update"]["updated"], False)
        self.assertIn("semantic_animation_open", summary["semantic_status"])


if __name__ == "__main__":
    unittest.main()
