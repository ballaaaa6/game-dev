#!/usr/bin/env python3
"""TDD coverage for the P0-A0 corpus baseline scanner."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
BUILDER_PATH = ROOT / "Phases" / "Phase4" / "tools" / "build_corpus_manifest.py"


def load_builder():
    """Load the implementation when present, while keeping the RED test readable."""

    if not BUILDER_PATH.exists():
        return None
    spec = importlib.util.spec_from_file_location("p0_a0_manifest_under_test", BUILDER_PATH)
    if spec is None or spec.loader is None:
        raise AssertionError(f"Could not load builder from {BUILDER_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


BUILDER = load_builder()


class CorpusManifestScannerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        for relative in (
            "game-dev-story-mod_Sprites",
            "game-dev-story-mod_Dumped",
            "game-dev-story-mod_Extracted",
            "Phases/Phase0/artifacts",
            "Phases/Phase4/artifacts",
            "Phases/Phase5/artifacts",
            "Phases/Phase6/artifacts",
        ):
            (self.root / relative).mkdir(parents=True, exist_ok=True)

        (self.root / "game-dev-story-mod_Sprites/a.txt").write_bytes(b"alpha\n")
        (self.root / "game-dev-story-mod_Dumped/dump.cs").write_bytes(
            b"// Function: demo\n"
        )
        (self.root / "game-dev-story-mod_Extracted/assets/data.bin").parent.mkdir(
            parents=True, exist_ok=True
        )
        (self.root / "game-dev-story-mod_Extracted/assets/data.bin").write_bytes(
            b"\x00\x01\x02"
        )
        (self.root / "Phases/Phase0/artifacts/phase0_baseline.json").write_text(
            '{"schema": 1, "known_limitations": ["fixture limitation"]}\n',
            encoding="utf-8",
        )
        (self.root / "Phases/Phase4/artifacts/wave0_build_manifest.json").write_text(
            '{"schema": "phase4.wave0.index-build.v1"}\n', encoding="utf-8"
        )
        (self.root / "Phases/Phase4/artifacts/corpus/old-output.json").parent.mkdir(
            parents=True, exist_ok=True
        )
        (self.root / "Phases/Phase4/artifacts/corpus/old-output.json").write_text(
            "generated output\n", encoding="utf-8"
        )

    def tearDown(self):
        self.temp.cleanup()

    def require_builder(self):
        if BUILDER is None:
            self.fail("P0-A0 builder is not implemented yet")
        return BUILDER

    def test_scan_uses_declared_roots_and_excludes_corpus_output(self):
        builder = self.require_builder()

        records = builder.scan_inputs(self.root)
        paths = [row["path"] for row in records["artifact_files"]]

        self.assertIn("Phases/Phase4/artifacts/wave0_build_manifest.json", paths)
        self.assertNotIn("Phases/Phase4/artifacts/corpus/old-output.json", paths)
        self.assertEqual(paths, sorted(paths))

    def test_records_use_relative_posix_paths(self):
        builder = self.require_builder()

        records = builder.scan_inputs(self.root)
        all_records = records["source_files"] + records["artifact_files"]

        for row in all_records:
            self.assertFalse(Path(row["path"]).is_absolute(), row["path"])
            self.assertNotIn("\\", row["path"])
            self.assertNotIn(":", row["path"])

    def test_binary_line_count_is_null_and_text_line_count_is_stable(self):
        builder = self.require_builder()

        records = builder.scan_inputs(self.root)["source_files"]
        by_path = {row["path"]: row for row in records}

        self.assertEqual(by_path["game-dev-story-mod_Sprites/a.txt"]["line_count"], 1)
        self.assertIsNone(
            by_path["game-dev-story-mod_Extracted/assets/data.bin"]["line_count"]
        )

    def test_sha256_file_matches_standard_digest(self):
        builder = self.require_builder()

        path = self.root / "game-dev-story-mod_Sprites/a.txt"
        self.assertEqual(builder.sha256_file(path), hashlib.sha256(b"alpha\n").hexdigest())

    def test_manifest_has_schema_root_summaries_and_stable_fingerprint(self):
        builder = self.require_builder()

        first = builder.build_manifest(
            self.root, generated_at_utc="2026-08-12T00:00:00Z"
        )
        second = builder.build_manifest(
            self.root, generated_at_utc="2026-08-12T01:00:00Z"
        )
        roots = {row["id"]: row for row in first["source_roots"]}

        self.assertEqual(first["schema"], "p0-a0.corpus-baseline.v1")
        self.assertEqual(first["snapshot_fingerprint"], second["snapshot_fingerprint"])
        self.assertIn("sprites", roots)
        self.assertEqual(roots["sprites"]["file_count"], 1)
        self.assertEqual(roots["sprites"]["total_bytes"], len(b"alpha\n"))
        self.assertEqual(roots["sprites"]["total_lines"], 1)
        self.assertEqual(roots["sprites"]["by_extension"], {".txt": 1})
        self.assertEqual(roots["sprites"]["status"], "pass")

    def test_tree_fingerprint_separates_record_namespaces(self):
        builder = self.require_builder()
        source_record = {
            "path": "shared/file.txt",
            "root_id": "source_root",
            "role": "source",
            "bytes": 5,
            "sha256": "digest",
        }
        artifact_record = {
            **source_record,
            "root_id": "artifact_root",
            "role": "artifact",
        }

        self.assertNotEqual(
            builder.tree_fingerprint([source_record]),
            builder.tree_fingerprint([artifact_record]),
        )

    def test_artifact_inputs_preserve_schema_status_and_supersession_fields(self):
        builder = self.require_builder()

        manifest = builder.build_manifest(self.root)
        inputs = {row["path"]: row for row in manifest["artifact_inputs"]}
        self.assertIn("Phases/Phase0/artifacts/phase0_baseline.json", inputs)
        self.assertIn("Phases/Phase4/artifacts/wave0_build_manifest.json", inputs)
        phase0 = inputs["Phases/Phase0/artifacts/phase0_baseline.json"]
        wave0 = inputs["Phases/Phase4/artifacts/wave0_build_manifest.json"]

        self.assertEqual(phase0["schema"], 1)
        self.assertEqual(wave0["schema"], "phase4.wave0.index-build.v1")
        for row in (phase0, wave0):
            self.assertEqual(row["role"], "phase_artifact")
            self.assertIn(row["status"], {"unknown", "pass", "attention"})
            self.assertIn("supersedes", row)

    def test_known_limitations_preserve_phase0_provenance(self):
        builder = self.require_builder()

        manifest = builder.build_manifest(self.root)

        self.assertIn("fixture limitation", manifest["known_limitations"])

    def test_manifest_writers_do_not_modify_inputs_and_report_uses_fingerprint(self):
        builder = self.require_builder()
        manifest = builder.build_manifest(self.root)
        manifest_path = self.root / "Phases/Phase4/artifacts/corpus/manifest.json"
        report_path = self.root / "Phases/Phase4/docs/corpus_baseline_report.md"
        source_before = (self.root / "game-dev-story-mod_Sprites/a.txt").read_bytes()

        write_manifest = getattr(builder, "write_manifest", None)
        write_report = getattr(builder, "write_report", None)
        self.assertIsNotNone(write_manifest, "write_manifest is not implemented yet")
        self.assertIsNotNone(write_report, "write_report is not implemented yet")
        write_manifest(manifest_path, manifest)
        write_report(report_path, manifest)

        written = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(written["snapshot_fingerprint"], manifest["snapshot_fingerprint"])
        self.assertIn(manifest["snapshot_fingerprint"], report_path.read_text(encoding="utf-8"))
        self.assertEqual(source_before, (self.root / "game-dev-story-mod_Sprites/a.txt").read_bytes())

    def test_compare_snapshot_passes_without_input_change(self):
        builder = self.require_builder()

        baseline = builder.build_manifest(self.root)
        result = builder.compare_snapshot(self.root, baseline)

        self.assertEqual(result["status"], "pass")
        self.assertEqual(result["added"], [])
        self.assertEqual(result["removed"], [])
        self.assertEqual(result["changed"], [])

    def test_compare_snapshot_reports_changed_file(self):
        builder = self.require_builder()

        baseline = builder.build_manifest(self.root)
        (self.root / "game-dev-story-mod_Sprites/a.txt").write_bytes(b"beta\n")
        result = builder.compare_snapshot(self.root, baseline)

        self.assertEqual(result["status"], "drift")
        self.assertEqual(
            [row["path"] for row in result["changed"]],
            ["game-dev-story-mod_Sprites/a.txt"],
        )
        self.assertNotEqual(result["baseline_fingerprint"], result["current_fingerprint"])

    def test_compare_snapshot_reports_added_and_removed_files(self):
        builder = self.require_builder()

        baseline = builder.build_manifest(self.root)
        (self.root / "game-dev-story-mod_Sprites/a.txt").unlink()
        (self.root / "game-dev-story-mod_Sprites/new.txt").write_bytes(b"new\n")
        result = builder.compare_snapshot(self.root, baseline)

        self.assertEqual(result["status"], "drift")
        self.assertEqual(result["added"], ["game-dev-story-mod_Sprites/new.txt"])
        self.assertEqual(result["removed"], ["game-dev-story-mod_Sprites/a.txt"])
        self.assertIsInstance(result["count_deltas"], list)

    def test_compare_snapshot_ignores_generated_output_changes(self):
        builder = self.require_builder()

        baseline = builder.build_manifest(self.root)
        output = self.root / "Phases/Phase4/artifacts/corpus/old-output.json"
        output.write_text("changed generated output\n", encoding="utf-8")
        result = builder.compare_snapshot(self.root, baseline)

        self.assertEqual(result["status"], "pass")

    def test_main_build_and_check_use_declared_outputs(self):
        builder = self.require_builder()
        output = self.root / "Phases/Phase4/artifacts/corpus"
        report = self.root / "Phases/Phase4/docs/corpus_baseline_report.md"
        arguments = [
            "--root",
            str(self.root),
            "--output",
            str(output),
            "--report",
            str(report),
        ]

        self.assertEqual(builder.main(arguments), 0)
        self.assertTrue((output / "manifest.json").is_file())
        self.assertTrue(report.is_file())
        self.assertEqual(builder.main(arguments + ["--check"]), 0)

    def test_main_returns_three_for_missing_baseline_or_required_root(self):
        builder = self.require_builder()
        output = self.root / "Phases/Phase4/artifacts/corpus"
        report = self.root / "Phases/Phase4/docs/corpus_baseline_report.md"
        arguments = [
            "--root",
            str(self.root),
            "--output",
            str(output),
            "--report",
            str(report),
            "--check",
        ]

        self.assertEqual(builder.main(arguments), 3)
        (self.root / "game-dev-story-mod_Extracted").rename(
            self.root / "game-dev-story-mod_Extracted-missing"
        )
        self.assertEqual(builder.main(arguments[:-1]), 3)

    def test_main_rejects_output_inside_source_root(self):
        builder = self.require_builder()
        output = self.root / "game-dev-story-mod_Sprites/unsafe-output"
        report = self.root / "Phases/Phase4/docs/corpus_baseline_report.md"

        code = builder.main(
            [
                "--root",
                str(self.root),
                "--output",
                str(output),
                "--report",
                str(report),
            ]
        )

        self.assertEqual(code, 4)


if __name__ == "__main__":
    unittest.main()
