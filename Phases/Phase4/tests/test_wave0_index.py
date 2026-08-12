#!/usr/bin/env python3
"""Deterministic smoke tests for Wave 0 index artifacts."""

from __future__ import annotations

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[3]
ARTIFACTS = ROOT / "Phases" / "Phase4" / "artifacts"


def load(name: str):
    return json.loads((ARTIFACTS / name).read_text(encoding="utf-8"))


class Wave0IndexTests(unittest.TestCase):
    def test_expected_artifacts_exist(self):
        names = [
            "field_offset_map.json",
            "function_inventory.json",
            "string_literal_map.json",
            "office_runtime_call_graph.json",
            "translation_coverage.json",
            "wave0_build_manifest.json",
        ]
        for name in names:
            self.assertTrue((ARTIFACTS / name).exists(), name)

    def test_named_gameform_offsets_are_present(self):
        fields = load("field_offset_map.json")["fields_by_class"]["form.GameForm"]
        by_name = {row["name"]: row for row in fields}
        self.assertEqual(by_name["BodyFace"]["offset"], "0x128")
        self.assertEqual(by_name["imgFace"]["offset"], "0x1150")
        self.assertEqual(by_name["imgBody"]["offset"], "0x1158")
        self.assertEqual(by_name["HumanMode"]["offset"], "0xE78")

    def test_script_and_fallback_evidence_are_indexed(self):
        rows = {row["symbol"]: row for row in load("function_inventory.json")["shortlist"]}
        self.assertEqual(rows["form_GameForm__DrawHuman"]["script_method_count"], 2)
        self.assertEqual(rows["form_GameForm__NewGamePara"]["source_status"], "assembly_fallback_only")
        self.assertEqual(rows["form_GameForm__DoEvent"]["source_status"], "assembly_fallback_only")
        self.assertGreater(rows["form_GameForm__NewGamePara"]["assembly_fallback"]["instructions"], 10000)

    def test_string_literal_index_and_references(self):
        data = load("string_literal_map.json")
        self.assertEqual(data["literal_count"], 12647)
        self.assertEqual(data["entries"][833]["value"], ".png.bytes")
        self.assertTrue(data["references"]["referenced_count"] > 0)
        self.assertEqual(data["references"]["missing_from_table"], [])

    def test_graph_contains_core_edges(self):
        graph = load("office_runtime_call_graph.json")
        edges = {(row["caller"], row["callee"]) for row in graph["edges"]}
        self.assertIn(("form_GameForm__DrawObj", "form_GameForm__DrawChair"), edges)
        self.assertIn(("form_GameForm__DrawObj", "form_GameForm__DrawDesk"), edges)
        self.assertIn(("form_GameForm__AddKaiwaTalkData", "form_GameForm__GetTalkIndex"), edges)

    def test_coverage_is_explicit(self):
        coverage = load("translation_coverage.json")
        self.assertGreaterEqual(coverage["summary"]["unit_count"], 70)
        self.assertGreater(coverage["summary"]["evidence_ready_units"], 0)
        actions = coverage["summary"]["by_action"]
        self.assertIn("translate", actions)
        self.assertIn("slice", actions)
        self.assertIn("contract_only", actions)


if __name__ == "__main__":
    unittest.main()
