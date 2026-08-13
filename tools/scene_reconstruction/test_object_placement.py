import unittest

from tools.scene_reconstruction.build_object_placement_contract import (
    build_object_placement_contract,
    classify_placement,
)


class ObjectPlacementTests(unittest.TestCase):
    def _assert_only_allowed_status_values(self, value):
        allowed = {"verified", "candidate", "unknown"}

        if isinstance(value, dict):
            for key, item in value.items():
                if key == "status":
                    self.assertIn(item, allowed)
                self._assert_only_allowed_status_values(item)
        elif isinstance(value, list):
            for item in value:
                self._assert_only_allowed_status_values(item)

    def test_asset_fixture_is_not_real_room_placement(self):
        result = classify_placement(
            asset_ref="reception_000",
            x=236,
            y=286,
            source_kind="runtime_adapter_fixture",
        )

        self.assertEqual(result.status, "unknown")
        self.assertEqual(result.authority, "diagnostic_only")

    def test_adapter_fixture_is_not_promoted_to_original_room_state(self):
        result = classify_placement(
            asset_ref="desk_000",
            x=360,
            y=338,
            source_kind="runtime_adapter_fixture",
        )

        self.assertEqual(result.status, "unknown")
        self.assertEqual(result.authority, "diagnostic_only")

    def test_explicit_producer_lineage_with_coordinate_field_is_verified(self):
        result = classify_placement(
            asset_ref="desk_000",
            x=46,
            y=61,
            source_kind="producer_to_consumer_lineage",
            coordinate_field="ObjecX",
        )

        self.assertEqual(result.status, "verified")
        self.assertEqual(result.authority, "producer_lineage")

    def test_contract_preserves_multiple_candidate_records_and_keeps_floor0_unknown(self):
        contract = build_object_placement_contract()
        contract_dict = contract.to_dict()

        self.assertEqual(contract.status, "unknown")
        self.assertEqual(contract.authority, "diagnostic_only")
        self.assertEqual(contract.floor0_snapshot["status"], "unknown")
        self.assertIn("classification", contract.summary)
        self.assertNotIn("status", contract.summary)
        self.assertEqual({record["id"] for record in contract.records}, {
            "reception.fixture.0",
            "desk.fixture.0",
            "chair.fixture.0",
        })
        self.assertTrue(all(record["asset_identity"]["status"] == "verified" for record in contract.records))
        self.assertTrue(all(record["placement"]["status"] == "unknown" for record in contract.records))
        self.assertGreaterEqual(len(contract.candidate_records), 2)
        self.assertTrue(any(candidate["status"] == "candidate" for candidate in contract.candidate_records))
        self.assertTrue(any(candidate["status"] == "verified" for candidate in contract.candidate_records))
        self.assertIn("three fixture objects", contract.explanation)
        self.assertIn("no persisted floor0 room-state record", contract.absence_scope)
        self.assertTrue(any(
            evidence.get("needle") == "internal static int[] OfficeObjecList;"
            for evidence in contract.evidence
        ))
        self.assertEqual(contract.summary["classification"], "asset_identity_verified_placement_unknown")
        self._assert_only_allowed_status_values(contract_dict)


if __name__ == "__main__":
    unittest.main()
