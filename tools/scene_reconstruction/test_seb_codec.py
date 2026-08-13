import hashlib
import json
import struct
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile

from tools.scene_reconstruction.build_seb_audit import build_seb_audit
from tools.scene_reconstruction.seb_codec import SebCandidate, compare_seb_sources, parse_seb_bytes


def format0_fixture(records, *, max_frame=-9, group_id=-4):
    """Build one hand-checked legacy format-0 group."""
    return struct.pack(
        ">HHhh", 1, max_frame & 0xFFFF, len(records), group_id
    ) + b"".join(struct.pack(">10h", *record) for record in records)


class SebCodecTests(unittest.TestCase):
    def setUp(self):
        self.record = (7, -2, -300, 301, 40, -41, 50, -51, 1, -1)
        self.complete_fixture = format0_fixture([self.record])
        self.truncated_fixture = self.complete_fixture[:-4]

    def test_format0_header_group_and_signed_shorts_are_preserved(self):
        parsed = parse_seb_bytes(self.complete_fixture, "fixture/floor0.seb")

        self.assertEqual(parsed.format_code, 0)
        self.assertEqual(parsed.format_decision, "format0")
        self.assertEqual(parsed.header.group_count, 1)
        self.assertEqual(parsed.header.max_frame, -9)
        self.assertEqual(parsed.groups[0].declared_record_count, 1)
        self.assertEqual(parsed.groups[0].group_id, -4)
        self.assertEqual(parsed.groups[0].offset, 4)
        self.assertEqual(parsed.groups[0].records[0].offset, 8)
        self.assertEqual(parsed.groups[0].records[0].u, -300)
        self.assertEqual(parsed.groups[0].records[0].h, -41)
        self.assertEqual(parsed.groups[0].records[0].reverse_v, -1)

    def test_complete_format0_record_has_all_ten_signed_short_fields(self):
        parsed = parse_seb_bytes(self.complete_fixture, "fixture/floor0.seb")

        record = parsed.groups[0].records[0]
        self.assertTrue(record.complete)
        self.assertEqual(record.raw_bytes, self.complete_fixture[8:])
        self.assertEqual(record.raw_tail, b"")
        self.assertEqual(parsed.tail_shortfall, 0)
        self.assertEqual(parsed.status, "verified")

    def test_truncated_tail_is_not_padded(self):
        parsed = parse_seb_bytes(self.truncated_fixture, "fixture/floor0.seb")

        self.assertEqual(parsed.tail_shortfall, 4)
        self.assertFalse(parsed.groups[0].records[-1].complete)
        self.assertEqual(parsed.groups[0].records[-1].raw_tail, self.truncated_fixture[-4:])
        self.assertIsNone(parsed.groups[0].records[-1].reverse_u)
        self.assertIsNone(parsed.groups[0].records[-1].reverse_v)
        self.assertEqual(parsed.groups[0].parsed_complete_count, 0)
        self.assertEqual(parsed.status, "candidate")

    def test_compact_selector_is_explicitly_not_format0(self):
        parsed = parse_seb_bytes(b"\x80\x00\x01\x00\x00", "fixture/compact.seb")

        self.assertNotEqual(parsed.format_code, 0)
        self.assertEqual(parsed.format_decision, "compact_variant")
        self.assertEqual(parsed.status, "unknown")

    def test_compare_classifies_identical_distinct_absent_and_unreadable(self):
        candidates = [
            SebCandidate("sprite", "sprites/floor0.seb", self.truncated_fixture),
            SebCandidate("archive", "apk::assets/floor0.seb", self.truncated_fixture),
            SebCandidate("extracted", "extracted/floor0.seb", self.complete_fixture),
            SebCandidate("zip", "zip::assets/floor0.seb", None),
            SebCandidate("evidence", "phase1/floor0.seb", None, read_error="bad evidence"),
        ]

        comparison = compare_seb_sources(candidates)

        self.assertEqual(
            [item.classification for item in comparison.candidates],
            ["byte-identical", "byte-identical", "distinct", "absent", "unreadable"],
        )
        self.assertEqual(comparison.outcome, "recovered_full_payload")
        self.assertEqual(comparison.best_complete.source_ref, "extracted/floor0.seb")

    def test_audit_stages_only_a_longer_archive_payload(self):
        root = Path(tempfile.mkdtemp())
        (root / "APK_Toolkit").mkdir()
        (root / "game-dev-story-mod_Sprites" / "office").mkdir(parents=True)
        (root / "knowledge" / "world-assets" / "evidence" / "scene_reconstruction").mkdir(parents=True)
        (root / "game-dev-story-mod_Sprites" / "office" / "floor0.seb").write_bytes(self.truncated_fixture)
        with ZipFile(root / "APK_Toolkit" / "game-dev-story-mod.apk", "w") as archive:
            archive.writestr("assets/office/floor0.seb", self.complete_fixture)
        (root / "APK_Toolkit" / "game-dev-story-mod.zip").write_bytes(
            (root / "APK_Toolkit" / "game-dev-story-mod.apk").read_bytes()
        )
        inventory = {
            "schema": "scene-source-inventory-v1",
            "claim_statuses": ["verified", "candidate", "unknown"],
            "relations": {
                "floor0": {
                    "office_seb": {"status": "verified", "source": "game-dev-story-mod_Sprites/office/floor0.seb"},
                    "all_seb": ["game-dev-story-mod_Sprites/office/floor0.seb"],
                }
            },
            "archives": {
                "APK_Toolkit/game-dev-story-mod.apk": {"path": "APK_Toolkit/game-dev-story-mod.apk", "members": []},
                "APK_Toolkit/game-dev-story-mod.zip": {"path": "APK_Toolkit/game-dev-story-mod.zip", "members": []},
            },
        }
        inventory_path = root / "knowledge" / "world-assets" / "evidence" / "scene_reconstruction" / "source_inventory.json"
        inventory_path.write_text(json.dumps(inventory), encoding="utf-8")

        audit = build_seb_audit(root, inventory_path=inventory_path)

        record = audit.floors[0]
        self.assertEqual(record.outcome, "recovered_full_payload")
        staged = root / record.staged_payload["path"]
        self.assertEqual(staged.read_bytes(), self.complete_fixture)
        self.assertIn(hashlib.sha256(self.complete_fixture).hexdigest(), staged.as_posix())


if __name__ == "__main__":
    unittest.main()
