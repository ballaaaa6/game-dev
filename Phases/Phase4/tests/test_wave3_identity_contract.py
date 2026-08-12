import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
ARTIFACTS = ROOT / "Phases" / "Phase4" / "artifacts"


def load(name: str):
    return json.loads((ARTIFACTS / name).read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


class Wave3IdentityContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.identity = load("wave3_actor_identity_contract.json")
        cls.spawn = load("wave3_spawn_fixture.json")
        cls.manifest = load("wave3_c1_build_manifest.json")

    def test_c1_artifacts_are_present_and_read_only(self):
        for name in (
            "wave3_actor_identity_contract.json",
            "wave3_spawn_fixture.json",
            "wave3_c1_build_manifest.json",
        ):
            self.assertTrue((ARTIFACTS / name).is_file(), name)
        self.assertTrue(self.identity["source_roots_read_only"])
        self.assertTrue(self.manifest["source_roots_read_only"])

    def test_add_syain_parameter_map_is_complete_and_evidence_backed(self):
        contract = self.identity["employee_record_contract"]
        self.assertEqual(contract["stored_parameter_count"], 27)
        rows = {row["parameter"]: row for row in contract["parameter_map"]}
        self.assertEqual(rows["TPoint"]["stored_fields"], ["SyainPointIndex", "SyainPoint"])
        self.assertEqual(rows["TTaikyu"]["transform"], "multiplied_by_10_before_store")
        self.assertEqual(rows["TFaceG"]["stored_fields"], ["SyainFaceG"])
        self.assertEqual(rows["TBodyG"]["stored_fields"], ["SyainBodyG"])
        for row in contract["parameter_map"]:
            self.assertEqual(row["status"], "verified_bounded_parameter_store")
            self.assertTrue(row["evidence"])
            self.assertTrue(all(e.get("line") is not None for e in row["evidence"]))

    def test_call_syain_slot_and_initial_fields_are_explicit(self):
        contract = self.identity["actor_spawn_contract"]
        self.assertEqual(contract["slot_allocation"]["free_slot_array"], "HumanEnabled")
        self.assertEqual(contract["slot_allocation"]["object_slot_allocator"], "AddObjec")
        self.assertEqual(contract["slot_allocation"]["failure_result"], -1)
        fields = {row["field"]: row for row in contract["initial_actor_fields"]}
        self.assertEqual(fields["HumanEnabled"]["initial_value_or_flow"], 1)
        self.assertEqual(fields["HumanStop"]["initial_value_or_flow"], 1)
        self.assertEqual(fields["HumanMode"]["initial_value_or_flow"], 0)
        self.assertEqual(fields["HumanState"]["initial_value_or_flow"], 0)
        self.assertEqual(fields["HumanFaceG"]["initial_value_or_flow"], "SyainFaceG[SyainIndex]")
        self.assertEqual(fields["HumanBodyG"]["initial_value_or_flow"], "SyainBodyG[SyainIndex]")
        for row in contract["initial_actor_fields"]:
            self.assertEqual(row["semantic_status"], "verified_bounded_initial_write")
            self.assertTrue(row["write_evidence"])
            self.assertTrue(all(e.get("line") is not None for e in row["write_evidence"]))

    def test_spawn_fixture_uses_adapter_identity_and_keeps_semantic_state_open(self):
        actor = self.spawn["expected"]["actor_identity"]
        self.assertEqual(actor["actor_id"], "adapter.actor.0")
        self.assertEqual(actor["identity_policy"], "stable_web_adapter_id_not_legacy_array_index")
        self.assertIn("do not interpret HumanMode=0 as idle", self.spawn["non_goals"])
        self.assertIn("do not interpret HumanState=0 as an Agent state", self.spawn["non_goals"])
        self.assertEqual(self.spawn["status"], "spawn_contract_ready_for_state_and_movement_slices")

    def test_failure_cases_are_not_silent_successes(self):
        cases = {row["case"]: row for row in self.spawn["failure_cases"]}
        self.assertEqual(cases["no_free_employee_slot"]["result"], -1)
        self.assertEqual(cases["no_free_actor_slot"]["result"], -1)
        self.assertNotEqual(cases["object_slot_unavailable"]["result"], "success")

    def test_c1_manifest_hashes_current_inputs(self):
        hashes = self.manifest["source_hashes"]
        for relative in (
            "game-dev-story-mod_Dumped/Categorized_Code/Global/form.c",
            "game-dev-story-mod_Dumped/dump.cs",
            "Phases/Phase4/artifacts/wave3_actor_function_map.json",
            "Phases/Phase4/artifacts/wave3_gap_register.json",
            "Phases/Phase4/artifacts/wave3_build_manifest.json",
        ):
            path = ROOT / Path(relative)
            self.assertIn(relative, hashes)
            self.assertEqual(hashes[relative]["bytes"], path.stat().st_size)
            self.assertEqual(hashes[relative]["sha256"], sha256(path))


if __name__ == "__main__":
    unittest.main()
