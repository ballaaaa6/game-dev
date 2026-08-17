"""Regression checks for the complete source SEB inventory."""

from __future__ import annotations

from build_seb_catalog import build_catalog


def test_catalog_decodes_all_observed_layered_members_and_isolates_one_variant() -> None:
    catalog, runtime_contract = build_catalog()

    assert catalog["counts"]["seb_total"] == 554
    assert catalog["counts"]["decoded_pass"] == 553
    assert catalog["counts"]["unsupported"] == 1
    assert catalog["unsupported"][0]["member"] == "01_GAME_PACKS/com/develop_menu_light.seb"
    assert catalog["unsupported"][0]["sha256"]

    explicit = set(catalog["floor00"]["explicit_contract_refs"])
    assert {
        "01_GAME_PACKS/chip/wall_ex.seb",
        "01_GAME_PACKS/chip/wall_00.seb",
        "01_GAME_PACKS/chip/door_02.seb",
        "01_GAME_PACKS/chip/desk_00.seb",
        "01_GAME_PACKS/chip/chair_00.seb",
        "01_GAME_PACKS/chip/equip.seb",
        "01_GAME_PACKS/human/wait_right.seb",
        "01_GAME_PACKS/human/typing_right.seb",
    } <= explicit
    assert catalog["floor00"]["missing_refs"] == []
    assert runtime_contract["status"] == "pass"


def test_catalog_keeps_metadata_anomalies_as_warnings_not_silent_drops() -> None:
    catalog, _ = build_catalog()

    warning_members = {
        entry["member"]
        for entry in catalog["assets"]
        if entry["status"] == "pass" and entry["decode"].get("metadata_warnings")
    }
    assert "01_GAME_PACKS/chip/animal_01.seb" in warning_members
    assert "01_GAME_PACKS/com/develop_bar.seb" in warning_members
    assert len(warning_members) == 7


def test_default_map_metadata_is_carried_into_runtime_floor00_contract() -> None:
    catalog, runtime_contract = build_catalog()

    metadata = runtime_contract["default_map_metadata"]
    assert metadata["scene_ref"] == "room:0"
    assert metadata["room"]["width"] == 14
    assert metadata["room"]["height"] == 14
    assert set(metadata["extension_wall"]["frame_records"]) == {"0", "1", "2", "3"}
    assert metadata["native_wall_door_composition"]["wall"]["seb_filename"] == "wall_00.seb"
    assert catalog["source"]["zip_sha256"] == runtime_contract["source_zip_sha256"]
