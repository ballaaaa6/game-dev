import unittest

from tools.scene_reconstruction.resource_relations import resolve_floor_layers, resolve_relation


class ResourceRelationTests(unittest.TestCase):
    def test_same_stem_without_loader_evidence_is_candidate(self):
        relation = resolve_relation("floor0.png", "floor0.seb", loader_match=False)
        self.assertEqual(relation.status, "candidate")
        self.assertEqual(relation.reason, "same_stem_only")

    def test_loader_selector_identity_is_verified(self):
        relation = resolve_relation(
            "office/floor0.png",
            "office/floor0.seb",
            loader_match=True,
            selector="floor0",
        )
        self.assertEqual(relation.status, "verified")
        self.assertEqual(relation.reason, "loader_selector_identity")

    def test_exact_archive_resource_identity_precedes_loader(self):
        relation = resolve_relation(
            "office/floor0.png",
            "office/floor0.seb",
            exact_identity=True,
            loader_match=False,
        )
        self.assertEqual(relation.status, "verified")
        self.assertEqual(relation.reason, "exact_archive_resource_identity")

    def test_conflict_is_unknown(self):
        relation = resolve_relation(
            "office/floor0.png",
            "office/floor0.seb",
            exact_identity=True,
            loader_match=True,
            conflict=True,
        )
        self.assertEqual(relation.status, "unknown")
        self.assertEqual(relation.reason, "conflicting_evidence")

    def test_missing_pair_is_unknown(self):
        relation = resolve_relation("office/floor13.png", None)
        self.assertEqual(relation.status, "unknown")
        self.assertEqual(relation.reason, "missing_resource")

    def test_floor_layers_keep_same_suffix_nodes_separate(self):
        inventory = {
            "floor_ids": ["floor0"],
            "relations": {
                "floor0": {
                    "all_png": [
                        "game-dev-story-mod_Sprites/game/floor0.png",
                        "game-dev-story-mod_Sprites/office/floor0.png",
                    ],
                    "all_seb": ["game-dev-story-mod_Sprites/office/floor0.seb"],
                }
            },
            "files": {
                "game-dev-story-mod_Sprites/game/floor0.png": {
                    "size": 10,
                    "sha256": "game-hash",
                },
                "game-dev-story-mod_Sprites/game/floorparts0.png": {
                    "size": 11,
                    "sha256": "parts-hash",
                },
                "game-dev-story-mod_Sprites/office/floor0.png": {
                    "size": 12,
                    "sha256": "office-hash",
                },
                "game-dev-story-mod_Sprites/office/floor0.seb": {
                    "size": 13,
                    "sha256": "seb-hash",
                },
            },
        }
        contract = resolve_floor_layers(inventory, {"floors": []}, {})
        node_paths = {node["source_path"] for node in contract["resources"]}
        self.assertIn("game-dev-story-mod_Sprites/game/floor0.png", node_paths)
        self.assertIn("game-dev-story-mod_Sprites/game/floorparts0.png", node_paths)
        self.assertIn("game-dev-story-mod_Sprites/office/floor0.png", node_paths)
        self.assertIn("game-dev-story-mod_Sprites/office/floor0.seb", node_paths)


if __name__ == "__main__":
    unittest.main()
