"""Static DD.19 acceptance checks for the Staff/job/skill/furniture evidence package."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

from build_data_dependency_forensics import EXPECTED_COUNTS, OUT, REPORTS, ROOT, build_all


REQUIRED_JSON = [
    "checkpoint-ledger.json",
    "data-catalog-authority.json",
    "staff-parameter-vocabulary.json",
    "staffdata-canonical-catalog.json",
    "jobdata-canonical-catalog.json",
    "job-level-parameter-contract.json",
    "skilldata-canonical-catalog.json",
    "staff-job-link-contract.json",
    "staff-skill-link-contract.json",
    "staff-derived-parameter-contract.json",
    "staff-runtime-status-contract.json",
    "hp-data-dependency-contract.json",
    "work-status-dependency-contract.json",
    "living-skill-effects-contract.json",
    "furniture-status-effect-contract.json",
    "actor-furniture-dependency-contract.json",
    "canonical-actor-schema.json",
    "canonical-furniture-schema.json",
    "original-staff-profile-catalog.json",
    "dashboard-task-adapter-contract.json",
    "unknowns.json",
]

REQUIRED_REPORTS = [
    "DATA_DEPENDENCY_AUDIT.md",
    "STAFFDATA_MODEL.md",
    "JOBDATA_MODEL.md",
    "SKILLDATA_MODEL.md",
    "DERIVED_STAFF_PARAMETERS.md",
    "HP_DATA_DEPENDENCY.md",
    "FURNITURE_STATUS_EFFECTS.md",
    "CANONICAL_ACTOR_SCHEMA.md",
    "CANONICAL_FURNITURE_SCHEMA.md",
    "DASHBOARD_TASK_ADAPTER.md",
]

REQUIRED_HANDOFFS = ["DATA_DEPENDENCY_HANDOFF.md"]

REGRESSION_SCRIPTS = [
    "tools/social-dev/test_behavior_first_forensics.py",
    "tools/social-dev/test_phase1d_closure.py",
    "tools/social-dev/test_visual_port_v1.py",
    "tools/social-dev/test_visual_port_v3.py",
    "tools/social-dev/test_visual_port_v7.py",
]


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def source_value(catalog: dict, source_id: int, field: str, locale: str = "English"):
    row = next(item for item in catalog["records"] if item["source_id"] == source_id)
    return row["locales"][locale]["parsed_fields"][field]["value"]


def trunc_div(numerator: int, denominator: int) -> int:
    quotient = abs(numerator) // abs(denominator)
    return -quotient if (numerator < 0) != (denominator < 0) else quotient


def expected_job_base(params: list[list[int]], max_level: int, parameter: int, level: int) -> int:
    pair = params[parameter]
    return pair[0] + trunc_div((pair[1] - pair[0]) * (level - 1), max_level - 1)


def run_static_regression(script: str) -> None:
    subprocess.run([sys.executable, script], cwd=ROOT, check=True, capture_output=True, text=True)


def no_source_root_diff() -> bool:
    paths = [
        "sources/raw/1_Click_CSharp_Code update/data/StaffData.cs",
        "sources/raw/1_Click_CSharp_Code update/data/JobData.cs",
        "sources/raw/1_Click_CSharp_Code update/data/SkillData.cs",
        "sources/raw/1_Click_CSharp_Code update/data/FurnitureData.cs",
        "sources/raw/1_Click_CSharp_Code update/game/Staff.cs",
        "sources/raw/1_Click_CSharp_Code update/game/Room.cs",
        "sources/raw/1_Click_CSharp_Code update/game/ObjChip.cs",
        "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code/game/Staff.cs",
    ]
    result = subprocess.run(["git", "diff", "--name-only", "--", *paths], cwd=ROOT, check=True, capture_output=True, text=True)
    return not result.stdout.strip()


def main() -> int:
    build_all()
    checks = 0

    def check(condition: bool, message: str) -> None:
        nonlocal checks
        checks += 1
        if not condition:
            raise AssertionError(f"check {checks} failed: {message}")

    check(OUT.is_dir(), "data-dependency evidence directory exists")
    check(REPORTS.is_dir(), "Behavior reports directory exists")
    check(len(REQUIRED_JSON) == 21, "DD.0-DD.20 machine artifact count")
    check(len(REQUIRED_REPORTS) == 10, "data-dependency report count")
    check(len(REQUIRED_HANDOFFS) == 1, "data-dependency handoff count")

    docs: dict[str, dict] = {}
    for name in REQUIRED_JSON:
        path = OUT / name
        check(path.is_file(), f"required JSON exists: {name}")
        docs[name] = json.loads(path.read_text(encoding="utf-8"))
    for name in REQUIRED_REPORTS:
        path = REPORTS / name
        check(path.is_file(), f"required report exists: {name}")
        check(path.read_text(encoding="utf-8").strip(), f"required report is non-empty: {name}")
    for name in REQUIRED_HANDOFFS:
        path = REPORTS / name
        check(path.is_file(), f"required handoff exists: {name}")
        check(path.read_text(encoding="utf-8").strip(), f"required handoff is non-empty: {name}")

    ledger = docs["checkpoint-ledger.json"]
    check(len(ledger["records"]) == 21, "DD.0-DD.20 checkpoint coverage")
    check({row["Checkpoint"] for row in ledger["records"]} == {f"DD.{n}" for n in range(21)}, "checkpoint IDs are complete")
    check(ledger["records"][-1]["Status"] == "STOP", "DD.20 is the stop checkpoint")
    check(all(value == "NO" for value in ledger["required_stop_literals"].values()), "all prohibited runtime/visual actions remain NO")

    authority = docs["data-catalog-authority.json"]
    check(authority["status"] == "pass_authority_closed", "catalog authority status")
    check(authority["record_counts"] == EXPECTED_COUNTS, "catalog counts are pinned")
    check(authority["pinned_inputs"]["original_data_pack"]["all_members_exact"], "ZIP table roundtrip is exact")
    check(len(authority["table_manifest"]) == 4, "four table manifests")
    check(all(len(locales) == 2 for locales in authority["table_manifest"].values()), "English and Japanese authority rows")
    check(all(len(item["sha256"]) == 64 for locales in authority["table_manifest"].values() for item in locales.values()), "table hashes are pinned")
    check("No decompiled C# was executed." in authority["read_only_boundary"], "read-only execution boundary")

    vocab = docs["staff-parameter-vocabulary.json"]
    staff_params = {item["name"]: item["value"] for item in vocab["staff_parameter_indices"]}
    job_params = {item["name"]: item["value"] for item in vocab["job_parameter_indices"]}
    check(staff_params["PARAM_HP"] == 5, "StaffData.PARAM_HP is 5")
    check(staff_params["PARAM_END"] == 6, "StaffData parameter end sentinel")
    check(job_params["PARAM_END"] == 5 and "PARAM_HP" not in job_params, "JobData has no fabricated named PARAM_HP constant")
    slot_observation = vocab["job_parameter_slot_observation"]
    check(slot_observation["observed_slots"] == [0, 1, 2, 3, 4, 5], "JobData arrays retain six source slots")
    check(slot_observation["slot_5_status"] == "source_data_slot_consumed_by_StaffData.PARAM_HP", "JobData slot 5 is explicitly bounded")
    check(len(vocab["skill_vocabulary"]["type_indices"]) == 14, "SkillData type vocabulary")
    check(len(vocab["skill_vocabulary"]["effect_indices"]) == 13, "SkillData effect vocabulary")
    check(len(vocab["furniture_vocabulary"]["flag_bits"]) == 16, "FurnitureData flag vocabulary")

    catalogs = {
        "StaffData": docs["staffdata-canonical-catalog.json"],
        "JobData": docs["jobdata-canonical-catalog.json"],
        "SkillData": docs["skilldata-canonical-catalog.json"],
        "FurnitureData": docs["furniture-status-effect-contract.json"],
    }
    for type_name in ("StaffData", "JobData", "SkillData"):
        catalog = catalogs[type_name]
        check(catalog["counts"]["records"] == EXPECTED_COUNTS[type_name], f"{type_name} record count")
        check(catalog["counts"]["parse_pass_records"] == EXPECTED_COUNTS[type_name], f"{type_name} parser pass count")
        check(catalog["counts"]["locales_per_record"] == 2, f"{type_name} locale count")
        for row in catalog["records"]:
            check(set(row["locales"]) == {"English", "Japanese"}, f"{type_name} locale pair {row['source_id']}")
            for locale in ("English", "Japanese"):
                locale_row = row["locales"][locale]
                raw_line = locale_row["raw_line"]
                check(locale_row["raw_columns"] == raw_line.split("\t"), f"{type_name} raw columns retained {row['source_id']}/{locale}")
                check(sha256_text(raw_line) == row["provenance"]["data_rows"][locale]["row_sha256"], f"{type_name} row hash provenance {row['source_id']}/{locale}")
                check(locale_row["parse"]["status"] == "pass", f"{type_name} parse status {row['source_id']}/{locale}")
                check(locale_row["parsed_fields"], f"{type_name} parsed fields retained {row['source_id']}/{locale}")

    furniture = catalogs["FurnitureData"]
    check(furniture["counts"]["records"] == 103, "FurnitureData record count")
    check(all(row["status_effects"]["rest_semantics"] == "UNKNOWN_NOT_PROMOTED" for row in furniture["records"]), "Furniture rest role remains unknown")
    check(all(row["status_effects"]["social_semantics"] == "UNKNOWN_NOT_PROMOTED" for row in furniture["records"]), "Furniture social role remains unknown")

    job_catalog = catalogs["JobData"]
    job_contract = docs["job-level-parameter-contract.json"]
    check(len(job_contract["records"]) == 30, "all JobData level contracts")
    check("trunc_toward_zero" in job_contract["formula"]["base"], "job formula integer semantics")
    check(job_contract["formula"]["integer_semantics"].startswith("AArch64 sdiv"), "job formula uses native signed division")
    check(job_contract["records"][4]["hp_slot"]["slot"] == 5, "job level contract preserves HP slot")
    for row in job_contract["records"]:
        source_id = row["job_id"]
        params = source_value(job_catalog, source_id, "params_")
        bonus = source_value(job_catalog, source_id, "bonus_")
        check(len(params) == 6 and len(bonus) == 6, f"JobData six-slot vectors {source_id}")
        for probe in row["probe_levels"]:
            level = probe["level"]
            expected_base = [expected_job_base(params, row["max_level"], parameter, level) for parameter in range(5)]
            expected_hp_base = expected_job_base(params, row["max_level"], 5, level)
            expected_params = [base + (bonus[parameter] if level >= row["max_level"] else 0) for parameter, base in enumerate(expected_base)]
            expected_hp = expected_hp_base + (bonus[5] if level >= row["max_level"] else 0)
            check(probe["base_params"] == expected_base, f"native base interpolation {source_id}/{level}")
            check(probe["params"] == expected_params, f"native max-level bonus {source_id}/{level}")
            check(probe["hp_base"] == expected_hp_base and probe["hp_param"] == expected_hp, f"Staff HP slot formula {source_id}/{level}")

    staff_job = docs["staff-job-link-contract.json"]
    staff_skill = docs["staff-skill-link-contract.json"]
    check(staff_job["link_count"] == 141 and all(link["target_exists"] for link in staff_job["links"]), "all StaffData.jobId_ links resolve")
    check(staff_skill["link_count"] == 141 and all(link["target_exists"] for link in staff_skill["links"]), "all StaffData.skill_ links resolve")
    check(staff_skill["mutation_boundary"]["save_field"] == "skillId_", "runtime skill mutation field")
    check(any(ref.get("symbol") == "public SkillData GetSkill()" and ref["status"] == "evidence_only" for ref in staff_skill["source_refs"]), "Staff.GetSkill source boundary")
    check(any(ref.get("symbol") == "Staff.GetSkill" and ref["status"] == "native_evidence_only" for ref in staff_skill["source_refs"]), "Staff.GetSkill native/source boundary")
    check(any(ref.get("rva") == "0x12D7810" for ref in staff_skill["source_refs"]), "Staff.GetSkill native RVA")

    derived = docs["staff-derived-parameter-contract.json"]
    fixture_expected = {0: 108, 114: 405, 129: 295}
    fixtures = {row["staff_id"]: row for row in derived["three_real_max_hp_fixtures"]}
    check(set(fixtures) == set(fixture_expected), "three real Staff HP fixtures")
    check(derived["staff_get_param"]["formula"].startswith("Staff.GetParam(type, level)"), "Staff.GetParam sum formula")
    check("Room.GetEquipParam" in derived["staff_get_base_param"]["formula"], "room equipment dependency retained")
    for staff_id, expected in fixture_expected.items():
        fixture = fixtures[staff_id]
        staff_job_id = source_value(catalogs["StaffData"], staff_id, "jobId_")
        def_hp = source_value(catalogs["StaffData"], staff_id, "defParams_")[5]
        job = next(row for row in job_contract["records"] if row["job_id"] == staff_job_id)
        level = fixture["level"]
        job_hp = next(probe for probe in job["probe_levels"] if probe["level"] == level)["hp_param"]
        check(fixture["job_id"] == staff_job_id and fixture["staff_data_defParams_HP"] == def_hp, f"source fixture linkage {staff_id}")
        check(fixture["expected_max_hp"] == def_hp + job_hp == expected, f"source-backed neutral MaxHP fixture {staff_id}")
        check(fixture["motivation_multiplier_percent"] == 100, f"neutral motivation fixture {staff_id}")

    runtime = docs["staff-runtime-status-contract.json"]
    check(runtime["counts"]["storage_records"] == 103, "Staff field inventory count")
    saved_names = {item["name"] for item in runtime["fields"] if item["storage_owner"] == "saved_runtime_state"}
    transient_names = {item["name"] for item in runtime["fields"] if item["storage_owner"] == "transient_runtime_state"}
    check({"hp_", "jobId_", "skillId_", "level_", "deskId_", "state_"}.issubset(saved_names), "critical Staff fields are saved")
    check({"params_", "route_", "floor_", "objIndex_", "masterJobIdList_", "itemEffectParams_", "fukidashi_", "cost_"}.issubset(saved_names), "composite serialized Staff fields are saved")
    check("room_" in transient_names and "original_" in transient_names, "object references remain transient")
    check(not any(item["name"] in saved_names for item in runtime["derived_fields"]), "derived outputs are not serialized fields")
    check("hp_" in runtime["save_stream"]["serialized_fields_detected"], "HP direct serialization evidence")
    check("route_" in runtime["save_stream"]["serialized_fields_detected"], "route composite serialization evidence")
    check(runtime["save_stream"]["round_trip_method"] == "Staff.Deserialize(InputStream)", "Staff save/load round trip")

    hp = docs["hp-data-dependency-contract.json"]
    check(hp["field"]["name"] == "hp_" and hp["field"]["offset"] == "0xE8", "HP field authority")
    check(hp["parameter_dependency"]["parameter_value"] == 5, "HP parameter dependency")
    check("GetBaseParam(5, 0)" in hp["hp_ratio_formula"]["formula"], "HP ratio uses data-backed MaxHP")
    check(hp["thresholds"]["low_hp_ratio_percent"] == 5 and hp["thresholds"]["home_return_ratio_percent"] == 40, "HP thresholds")
    check(hp["thresholds"]["recovery_start_delay_frames"] == 20, "equipment recovery delay")
    check(hp["ordinary_work_hp_drain"]["status"] == "UNKNOWN", "ordinary work HP drain remains unknown")
    check(hp["saved_load"]["status"] == "saved_and_restored", "HP save/load contract")
    check(any(item["operation"] == "UpdateStayHome -> RecoverHp(1)" for item in hp["write_and_recovery_chain"]), "home recovery HP write")
    check(any(item["operation"] == "UpdateRecoveryHp -> RecoverHp(1)" for item in hp["write_and_recovery_chain"]), "equipment recovery HP write")

    work = docs["work-status-dependency-contract.json"]
    check(work["status"] == "pass_state_and_consumers_with_work_drain_limit", "work status contract")
    check(work["work_states"]["STATE_STAY_HOME"] == 13 and work["work_states"]["STATE_WORK"] == 4, "work/home state values")
    check(work["ordinary_work_hp_drain"]["status"] == "UNKNOWN", "work contract preserves drain unknown")
    check(any(item["source"] == "FurnitureData.recovery_" for item in work["data_dependencies"]), "work/recovery furniture dependency")
    check(any(item["source"] == "SkillData.effects_" for item in work["data_dependencies"]), "work skill dependency")

    skill_effects = docs["living-skill-effects-contract.json"]
    check(skill_effects["record_count"] == 36, "all SkillData effect records")
    check(all("effects_raw" in row and "aura_rates_raw" in row for row in skill_effects["records"]), "raw skill effects retained")
    type10 = [row for row in skill_effects["records"] if row["type"] == 10]
    type13 = [row for row in skill_effects["records"] if row["type"] == 13]
    check(any(item["effect_index"] == 8 and item["consumer"] == "Staff.OnEndTyping" for row in type10 for item in row["proven_consumers"]), "meeting-point skill consumer")
    check(any(item["effect_index"] == 12 and item["consumer"] == "Staff.AddAuraGauge" for row in type13 for item in row["proven_consumers"]), "aura-charge skill consumer")
    check(any(row["consumer_status"] == "UNKNOWN_NOT_PROMOTED" and not row["proven_consumers"] for row in skill_effects["records"]), "unproven skill semantics remain unknown")

    furniture_counts = furniture["counts"]
    check(furniture_counts["by_interaction_class"] == {"DOOR_RECORD": 1, "EQUIPMENT_NO_HP_EFFECT_PROVEN": 43, "RECOVERY_EQUIPMENT": 49, "WORKSTATION": 10}, "Furniture interaction class counts")
    check(furniture_counts["recovery_records"] == 49 and furniture_counts["workstation_records"] == 10 and furniture_counts["door_records"] == 1, "Furniture status counts")
    check(all(row["passability"]["passMap_present"] for row in furniture["records"]), "all FurnitureData passMap matrices present")
    check(all(row["passability"]["passMap_raw"] == row["raw_fields"]["passMap_"] for row in furniture["records"]), "passMap raw values are not projected away")
    f0 = next(row for row in furniture["records"] if row["furniture_id"] == 0)
    check([len(f0["passability"]["passMap_raw"]), len(f0["passability"]["passMap_raw"][0])] == [9, 9], "real FurnitureData 0 passMap shape")
    check(f0["provenance"]["passMap_fixture_ref"] == "phase1d_passmap_fixture.json", "passMap fixture provenance")
    check(all(row["status_effects"]["param_effect"]["status"] == "verified_native_branch" for row in furniture["records"]), "Furniture parameter effect provenance")
    check(any(row["type"] == 5 and row["status_effects"]["door_record"] for row in furniture["records"]), "door FurnitureData record")
    check(all(row["status_effects"]["equipment_candidate_for_GotoEquip"] == (row["type"] in {1, 4}) for row in furniture["records"]), "equipment candidate type boundary")

    actor_furniture = docs["actor-furniture-dependency-contract.json"]
    check(len(actor_furniture["nodes"]) == 7 and len(actor_furniture["edges"]) >= 11, "actor/furniture dependency graph")
    check(any(edge["from"] == "FurnitureData.passMap_" and edge["status"] == "verified_with_phase1d_fixture" for edge in actor_furniture["edges"]), "passMap graph edge")
    check(actor_furniture["refs"]["route_fixture"] == "phase1d_route_fixture.json", "route graph provenance")
    check("REST" in " ".join(actor_furniture["role_limits"]) and "SOCIAL" in " ".join(actor_furniture["role_limits"]), "actor role limits remain explicit")

    actor_schema = docs["canonical-actor-schema.json"]
    check(len(actor_schema["static_source_fields"]) == 21, "canonical actor source field count")
    check(all(item["status"] == "source_field_no_fabrication" for item in actor_schema["static_source_fields"]), "canonical actor source field provenance")
    check(all(item["status"] == "PRODUCT_POLICY" for item in actor_schema["product_policy_fields"]), "actor product-policy boundary")
    check(any(item["original_field"] == "Staff.hp_" for item in actor_schema["runtime_saved_fields"]), "actor saved HP schema")
    check(any(item["field"] == "max_hp" for item in actor_schema["derived_contract_fields"]), "actor derived HP schema")
    check(all("dashboard" not in item["original_field"].lower() for item in actor_schema["static_source_fields"]), "no dashboard field in source schema")

    furniture_schema = docs["canonical-furniture-schema.json"]
    check(len(furniture_schema["static_source_fields"]) == 21, "canonical furniture source field count")
    check(any(item["original_field"] == "FurnitureData.passMap_" for item in furniture_schema["static_source_fields"]), "canonical furniture passMap field")
    check(all(item["status"] == "derived_contract_only" for item in furniture_schema["derived_contract_fields"]), "furniture projections are derived")
    check(all("REST" not in item["original_field"] and "SOCIAL" not in item["original_field"] for item in furniture_schema["static_source_fields"]), "no fabricated furniture rest/social fields")

    profiles = docs["original-staff-profile-catalog.json"]
    check(profiles["profile_count"] == 141, "all original Staff profiles")
    check({profile["source_id"] for profile in profiles["profiles"]} == set(range(141)), "Staff profile IDs are complete")
    check(all(profile["status"] == "source_profile" and profile["semantic_status"] == "original_static_profile_only" for profile in profiles["profiles"]), "profiles remain static source-only")
    check(profiles["default_actor_boundary"]["known_initial_spawn_staff_ids"] == [0, 1, 2], "known initial actor fixture")
    check("not reconstructed" in profiles["default_actor_boundary"]["note"], "caller selection remains bounded")

    dashboard = docs["dashboard-task-adapter-contract.json"]
    check(all(item["status"] == "PRODUCT_POLICY" for item in dashboard["adapter_fields"]), "dashboard additions are PRODUCT_POLICY")
    check(all(field not in {item["field"] for item in dashboard["adapter_fields"]} for field in {"x_", "y_", "hp_", "objIndex_", "route_"}), "raw runtime fields excluded from dashboard adapter")
    check(any("raw x/y" in item for item in dashboard["forbidden_inputs"]), "dashboard raw coordinate prohibition")
    check(any("raw HP" in item for item in dashboard["forbidden_inputs"]), "dashboard raw HP prohibition")
    check(dashboard["status_unknowns"], "dashboard unknowns are retained")

    unknowns = docs["unknowns.json"]
    check(unknowns["status"] == "tracked", "unknown registry status")
    check(unknowns["retention_policy"]["raw_rows_retained"] and unknowns["retention_policy"]["fabricated_original_values"] is False, "unknown/raw retention policy")
    check(all(item["status"] in {"UNKNOWN", "UNKNOWN_PRODUCT_POLICY"} for item in unknowns["unknowns"]), "unknown rows use explicit statuses")
    check(any(item["topic"] == "ordinary work HP drain" for item in unknowns["unknowns"]), "work HP unknown is registered")
    check(any(item["topic"] == "FurnitureData rest/social roles" for item in unknowns["unknowns"]), "Furniture rest/social unknown is registered")

    check(load_status("phase1d_closure.json") == "pass", "Phase 1D closure regression")
    check(load_status("phase1d_passmap_fixture.json") == "pass", "passMap regression fixture")
    check(load_status("phase1d_route_fixture.json") == "pass", "route regression fixture")
    check(no_source_root_diff(), "read-only source roots untouched")
    check(not any(path.suffix.lower() in {".png", ".jpg", ".jpeg", ".apk", ".aab"} for path in OUT.iterdir() if path.is_file()), "no visual/binary DD artifact")
    check(not any("renderer" in path.name.lower() or "mapchip" in path.name.lower() or "v8" in path.name.lower() for path in OUT.iterdir()), "no renderer/MapChip/V8 artifact")
    check(subprocess.run(["git", "diff", "--check"], cwd=ROOT, check=True, capture_output=True, text=True).stdout == "", "git diff whitespace check")

    for script in REGRESSION_SCRIPTS:
        run_static_regression(script)
        check(True, f"static regression passed: {Path(script).name}")

    check(checks >= 180, "DD.19 static coverage is broad")
    print(f"data_dependency_static_checks_passed checks={checks} json={len(REQUIRED_JSON)} reports={len(REQUIRED_REPORTS)} handoffs={len(REQUIRED_HANDOFFS)} regressions={len(REGRESSION_SCRIPTS)}")
    return 0


def load_status(name: str) -> str:
    return json.loads((ROOT / "knowledge/fixtures/accepted" / name).read_text(encoding="utf-8"))["status"]


if __name__ == "__main__":
    raise SystemExit(main())
