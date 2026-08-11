#!/usr/bin/env python3
"""Regression tests for the evidence-first SEB decoder."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from decode_seb import parse_seb_bytes  # noqa: E402


WORKSPACE = Path(__file__).resolve().parents[1]
SPRITES = WORKSPACE / "game-dev-story-mod_Sprites"


class SebDecoderTests(unittest.TestCase):
    def test_floor0_preserves_final_record_shortfall(self) -> None:
        path = SPRITES / "office" / "floor0.seb"
        result = parse_seb_bytes(path.read_bytes(), "office/floor0.seb")
        self.assertEqual(result["format_code"], 0)
        self.assertEqual(result["header"]["group_count"], 1)
        self.assertEqual(result["header"]["max_frame"], 1)
        self.assertEqual(result["expected_bytes"], 28)
        self.assertEqual(result["size_bytes"], 24)
        self.assertEqual(result["tail_shortfall_bytes"], 4)
        record = result["groups"][0]["records"][0]
        self.assertFalse(record["complete"])
        self.assertEqual(record["missing_fields"], ["reverse_u", "reverse_v"])
        self.assertEqual(result["status"], "truncated_final_record")

    def test_floor17_group_headers_and_frame_records(self) -> None:
        path = SPRITES / "office" / "floor17.seb"
        result = parse_seb_bytes(path.read_bytes(), "office/floor17.seb")
        self.assertEqual(result["header"]["group_count"], 8)
        self.assertEqual(result["header"]["max_frame"], 36)
        self.assertEqual(
            [(group["record_count"], group["group_id"]) for group in result["groups"]],
            [(2, 36), (10, 36), (2, 0), (2, 0), (2, 0), (2, 0), (2, 36), (2, 36)],
        )
        self.assertEqual(result["tail_shortfall_bytes"], 4)
        self.assertEqual(result["errors"], [])

    def test_every_current_target_is_structurally_accounted_for(self) -> None:
        paths = sorted(
            path
            for group in ("office", "game", "com", "system")
            for path in (SPRITES / group).rglob("*.seb")
        )
        self.assertEqual(len(paths), 53)
        for path in paths:
            result = parse_seb_bytes(path.read_bytes(), path.relative_to(SPRITES).as_posix())
            self.assertEqual(result["format_code"], 0, path)
            self.assertEqual(result["status"], "truncated_final_record", path)
            self.assertEqual(result["tail_shortfall_bytes"], 4, path)
            self.assertEqual(result["errors"], [], path)


if __name__ == "__main__":
    unittest.main(verbosity=2)
