import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from tools.scene_reconstruction.paths import WorkspacePathError
from tools.scene_reconstruction.source_inventory import build_source_inventory


class SourceInventoryTests(unittest.TestCase):
    def make_fixture(self):
        root = Path(tempfile.mkdtemp())
        (root / "sprites" / "office").mkdir(parents=True)
        (root / "sprites" / "game").mkdir(parents=True)
        (root / "extracted" / "nested").mkdir(parents=True)
        (root / "dumped" / "Categorized_Code").mkdir(parents=True)
        (root / "dumped" / "Failed_Functions_Assembly").mkdir(parents=True)
        (root / "dumped" / "DummyDll").mkdir(parents=True)
        (root / "primary").mkdir()
        (root / "apk").mkdir()
        (root / "archive").mkdir()
        (root / "sprites" / "office" / "floor0.png").write_bytes(b"floor0")
        (root / "sprites" / "office" / "floor0.seb").write_bytes(b"seb0")
        (root / "sprites" / "office" / "floor2.png").write_bytes(b"floor2")
        (root / "sprites" / "office" / "floor13.png").write_bytes(b"floor13")
        (root / "sprites" / "game" / "floor1.png").write_bytes(b"game-floor1")
        (root / "extracted" / "nested" / "floor4.seb").write_bytes(b"seb4")
        (root / "dumped" / "Categorized_Code" / "office.c").write_bytes(b"code")
        (root / "dumped" / "Failed_Functions_Assembly" / "x.s").write_bytes(b"asm")
        (root / "dumped" / "DummyDll" / "Assembly-CSharp.dll").write_bytes(b"dll")
        (root / "primary" / "A.cs").write_bytes(b"class A {}")
        (root / "apk" / "game-dev-story-mod.apk").write_bytes(b"apk")
        with ZipFile(root / "archive" / "game-dev-story-mod.zip", "w", ZIP_DEFLATED) as archive:
            archive.writestr("assets/floor9.png", b"zip-floor9")
            archive.writestr("assets/floor9.seb", b"zip-seb9")
        (root / ".last_extraction.env").write_text(
            "APK_PATH=apk/game-dev-story-mod.apk\n"
            "OUT_FOLDER=extracted\n"
            "DUMP_OUT=dumped\n"
            "SPRITE_OUT=sprites\n",
            encoding="utf-8",
        )
        return root

    def test_sha256_is_stable_and_matches_bytes(self):
        root = self.make_fixture()
        first = build_source_inventory(root)
        second = build_source_inventory(root)
        self.assertEqual(first.to_json(), second.to_json())
        apk = first.files["APK_Toolkit/game-dev-story-mod.apk"]
        self.assertEqual(apk["sha256"], hashlib.sha256(b"apk").hexdigest())

    def test_archive_members_include_name_crc_and_size(self):
        inventory = build_source_inventory(self.make_fixture())
        members = inventory.archives["APK_Toolkit/game-dev-story-mod.zip"]["members"]
        self.assertEqual([member["name"] for member in members], ["assets/floor9.png", "assets/floor9.seb"])
        self.assertEqual(members[0]["size"], len(b"zip-floor9"))
        self.assertIsInstance(members[0]["crc"], int)

    def test_floor_discovery_keeps_missing_pairs_explicit(self):
        inventory = build_source_inventory(self.make_fixture())
        self.assertEqual(inventory.floor_ids, ["floor0", "floor1", "floor2", "floor4", "floor9", "floor13"])
        self.assertEqual(inventory.relations["floor2"]["office_seb"]["status"], "unknown")
        self.assertEqual(inventory.relations["floor13"]["office_seb"]["status"], "unknown")

    def test_rejects_path_outside_configured_workspace(self):
        root = self.make_fixture()
        with self.assertRaises(WorkspacePathError):
            build_source_inventory(root, extra_paths=[root.parent / "outside.bin"])

    def test_preserves_extraction_env_keys_and_raw_declarations(self):
        root = self.make_fixture()
        inventory = build_source_inventory(root)
        declaration = inventory.declared_paths["APK_PATH"]
        self.assertEqual(declaration["key"], "APK_PATH")
        self.assertEqual(declaration["raw_value"], "apk/game-dev-story-mod.apk")
        self.assertEqual(declaration["normalized_path"], "apk/game-dev-story-mod.apk")
        self.assertTrue(declaration["resolved_path"].endswith("\\apk\\game-dev-story-mod.apk"))


if __name__ == "__main__":
    unittest.main()
