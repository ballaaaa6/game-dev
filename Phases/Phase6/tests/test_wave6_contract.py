import json
from pathlib import Path
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[3]
PHASE6 = ROOT / "Phases" / "Phase6"


class Wave6ContractTests(unittest.TestCase):
    def read(self, name):
        return json.loads((PHASE6 / "artifacts" / name).read_text(encoding="utf-8"))

    def test_task_contract_is_adapter_scoped(self):
        contract = self.read("wave6_task_contract.json")
        self.assertEqual(contract["schema_version"], "wave6-task-contract-v1")
        self.assertEqual(contract["task_statuses"], ["queued", "working", "blocked", "done"])
        self.assertFalse(contract["legacy_equivalence"])
        self.assertEqual(contract["persistence"]["storage_key"], "phase6.task_state.v1")

    def test_repository_contract_has_migration_and_conflict_policy(self):
        contract = self.read("wave6_repository_contract.json")
        self.assertEqual(contract["envelope_schema"], "wave6-task-repository-v1")
        self.assertEqual(contract["migration"]["to"], "wave6-task-repository-v1 envelope with revision 0")
        self.assertEqual(contract["conflict_policy"]["runtime_status"], "conflict_needs_reload")

    def test_permission_policy_is_explicit_and_local(self):
        policy = self.read("wave6_permission_policy.json")
        self.assertEqual(policy["operator_ids"], ["operator"])
        self.assertIn("assign", policy["operator_actions"])
        self.assertNotIn("assign", policy["agent_actions"])
        self.assertEqual(policy["authentication"], "out_of_scope_local_identity_only")

    def test_migration_fixture_matches_repository_envelope(self):
        fixture = self.read("wave6_migration_fixture.json")
        self.assertEqual(fixture["expected_envelope"]["revision"], 0)
        self.assertEqual(fixture["expected_first_write_revision"], 1)

    def test_assignment_rules_are_explicit(self):
        rules = self.read("wave6_assignment_rules.json")
        self.assertEqual(rules["queue_order"], ["priority_rank", "created_at_tick_ascending", "task_id_ascending"])
        self.assertIn("one_active_task_per_agent", {item["id"] for item in rules["rules"]})
        self.assertIn("moving_agent_guard", {item["id"] for item in rules["rules"]})

    def test_events_and_notifications_are_separate_from_wave5(self):
        events = self.read("wave6_event_catalog.json")
        notifications = self.read("wave6_notification_contract.json")
        self.assertIn("task.created", events["events"])
        self.assertEqual(notifications["expiry_policy"], "no_automatic_logical_expiry")
        self.assertEqual(notifications["separation"]["message_graph"], "not_reinterpreted")

    def test_queue_fixture_is_deterministic(self):
        fixture = self.read("wave6_queue_fixture.json")
        self.assertEqual(fixture["expected_queue_order"], [
            "task.fixture.urgent",
            "task.fixture.high",
            "task.fixture.blocked",
            "task.fixture.done",
        ])

    def test_build_manifest_tracks_existing_files(self):
        manifest = self.read("wave6_build_manifest.json")
        self.assertEqual(manifest["stage"], "W6-C0..C7+W6.1-task-system-dashboard-hardening")
        self.assertFalse(manifest["legacy_equivalence"])
        self.assertTrue(all(item["exists"] and item["sha256"] for item in manifest["files"]))
        paths = {item["path"] for item in manifest["files"]}
        self.assertIn("Phases/Phase6/runtime/task_system.js", paths)
        self.assertIn("Phases/Phase5/runtime/app.js", paths)

    def test_gap_register_keeps_backend_and_camera_open(self):
        gaps = self.read("wave6_gap_register.json")
        self.assertEqual(gaps["status"], "complete_with_known_limitations")
        by_id = {item["id"]: item for item in gaps["gaps"]}
        self.assertEqual(by_id["W6-GAP-001"]["status"], "local_adapter_only")
        self.assertEqual(by_id["W6-GAP-004"]["status"], "highlight_only")
        self.assertEqual(by_id["W6-GAP-005"]["status"], "false")

    def test_browser_interaction_report_is_clean(self):
        report = self.read("wave6_interaction_report.json")
        self.assertEqual(report["status"], "browser_smoke_pass")
        self.assertEqual(report["browser"]["console_errors"], 0)
        self.assertEqual(report["browser"]["console_warnings"], 0)
        self.assertTrue(report["browser"]["refresh_persistence"] == "passed")
        self.assertEqual(report["browser"]["task_notification_dismiss"], "passed")
        self.assertEqual(report["browser"]["lifecycle_button_guards"], "passed")
        self.assertEqual(report["browser"]["task_description_render"], "passed")
        self.assertTrue(report["cleanup"]["local_server_stopped_after_verification"])

    def test_js_task_system(self):
        result = subprocess.run(
            ["node", str(PHASE6 / "tests" / "test_wave6_task_system.js")],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Wave 6 task system tests passed: 18 scenarios", result.stdout)


if __name__ == "__main__":
    unittest.main()
