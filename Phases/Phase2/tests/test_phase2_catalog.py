#!/usr/bin/env python3
"""Small deterministic smoke tests for generated Phase 2 artifacts."""

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[3]
ARTIFACTS = ROOT / "Phases" / "Phase2" / "artifacts"


def load(name):
    return json.loads((ARTIFACTS / name).read_text(encoding="utf-8"))


class Phase2CatalogTests(unittest.TestCase):
    def test_baseline_counts(self):
        audit = load("phase2_input_audit.json")
        self.assertEqual(audit["bodyface_baseline"]["record_count"], 42)
        self.assertEqual(audit["assets_summary"]["body_assets"], 26)
        self.assertEqual(audit["assets_summary"]["face_assets"], 36)

    def test_modes_and_manifests_align(self):
        analysis = load("bodyface_analysis.json")
        character = load("character_manifest.json")
        animation = load("animation_manifest.json")
        self.assertEqual([row["mode"] for row in analysis["records"]], list(range(42)))
        self.assertEqual(len(character["bodyface_mode_compositions"]), 42)
        self.assertEqual(len(animation["frame_descriptors"]), 42)

    def test_unknowns_are_explicit(self):
        animation = load("animation_manifest.json")
        states = load("agent_state_mapping.json")
        self.assertTrue(all(row["semantic_label"] is None for row in animation["frame_descriptors"]))
        self.assertEqual(states["coverage"]["unknown"], 5)
        self.assertEqual(states["coverage"]["probable"], 1)

    def test_composition_contract_and_human_dex_trace(self):
        trace = load("phase2_code_trace.json")
        self.assertEqual(trace["draw_human_call_count"], 106)
        layers = {row["layer"]: row for row in trace["composition_contract"]["selector_to_image_array"]}
        self.assertEqual(layers["body"]["selector"], "TBody")
        self.assertEqual(layers["body"]["image_array_field"], "imgBody")
        self.assertEqual(layers["face"]["selector"], "TFace")
        self.assertEqual(layers["face"]["image_array_field"], "imgFace")
        self.assertEqual(trace["dynamic_selector_trace"]["human_dex_draw_call"]["confidence"], "verified")
        self.assertEqual(trace["composition_contract"]["add_body_face_parameter_map"]["parameters"]["P13"], "shadow_dst_y")

    def test_validation_passes(self):
        report = load("phase2_validation_report.json")
        self.assertEqual(report["status"], "pass")
        self.assertFalse(report["errors"])


if __name__ == "__main__":
    unittest.main()
