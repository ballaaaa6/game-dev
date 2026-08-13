import unittest
from pathlib import Path

from tools.scene_reconstruction.csharp_trace import build_seb_semantics_contract, trace_symbol


ROOT = Path(".")
TRACE_ROOTS = [
    ROOT / "knowledge/csharp/primary",
    ROOT / "game-dev-story-mod_Dumped/Categorized_Code",
    ROOT / "game-dev-story-mod_Dumped/Failed_Functions_Assembly",
    ROOT / "game-dev-story-mod_Dumped/dump.cs",
    ROOT / "game-dev-story-mod_Dumped/DummyDll/Assembly-CSharp.dll",
]


class CSharpTraceTests(unittest.TestCase):
    def test_missing_consumer_is_unknown_not_verified(self):
        result = trace_symbol("Floor0DirectCallerThatDoesNotExist", TRACE_ROOTS)

        self.assertEqual(result.status, "unknown")
        self.assertEqual(result.source_refs, [])

    def test_trace_returns_bounded_sorted_source_refs(self):
        result = trace_symbol("GetSprites", TRACE_ROOTS)

        self.assertEqual(result.status, "verified")
        self.assertGreater(len(result.source_refs), 0)
        self.assertEqual(
            result.source_refs,
            sorted(result.source_refs, key=lambda ref: (ref.source_path, ref.line or -1, ref.offset or -1, ref.excerpt)),
        )
        for ref in result.source_refs:
            self.assertLessEqual(len(ref.excerpt), 140)
            self.assertTrue(ref.source_path)
            self.assertIsNotNone(ref.source_hash)

    def test_semantics_contract_keeps_field_categories_separate(self):
        contract = build_seb_semantics_contract(TRACE_ROOTS)

        self.assertEqual(contract.status, "consumer_boundary_verified")
        self.assertEqual(contract.field_table["u"]["category"], "local crop")
        self.assertEqual(contract.field_table["trans_x"]["category"], "local translation")
        self.assertEqual(contract.field_table["texture_id"]["category"], "texture/selector")
        self.assertEqual(contract.field_table["ObjecX"]["category"], "external object/base coordinate")
        self.assertEqual(contract.field_table["camX_"]["category"], "screen/camera coordinate")
        self.assertEqual(contract.field_table["ObjecSY"]["category"], "sort/depth")
        self.assertEqual(contract.field_table["ObjecZX"]["status"], "candidate")
        self.assertEqual(contract.field_table["ObjecZY"]["status"], "candidate")


if __name__ == "__main__":
    unittest.main()
