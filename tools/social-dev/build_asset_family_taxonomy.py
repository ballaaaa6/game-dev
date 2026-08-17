"""Build the structural asset-family taxonomy for the Social Dev catalog.

The taxonomy uses authoritative pack, archive group, extension, and existing
semantic-role evidence. It intentionally labels structural families without
pretending that a filename alone proves a gameplay call site.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "knowledge/fixtures/accepted"
RUNTIME_EVIDENCE = ROOT / "knowledge/fixtures/accepted/runtime"

COVERAGE_PATH = EVIDENCE / "asset_metadata_coverage.json"
TAXONOMY_PATH = EVIDENCE / "asset_family_taxonomy.json"
CONTRACT_PATH = RUNTIME_EVIDENCE / "asset_family_taxonomy_contract.json"
REPORT_PATH = ROOT / "docs/reports/social-dev_asset_family_taxonomy.md"

PACK_FAMILIES = {
    "avatar_body": ("character.avatar.body", "character", "Avatar body and pose source package."),
    "avatar_head": ("character.avatar.head", "character", "Avatar head and face-part source package."),
    "banner": ("ui.banner", "ui", "Promotional and banner presentation package."),
    "billing": ("ui.billing", "ui", "Billing, shop, coin, and purchase presentation package."),
    "chip": ("world.chip", "world", "World, room, furniture, floor, wall, door, and map-chip package."),
    "com": ("ui.common", "ui", "Shared common UI, gauges, labels, panels, and status package."),
    "connect": ("config.connection", "config", "Connection and configuration package."),
    "develop": ("ui.develop", "ui", "Development and production-screen package."),
    "effect": ("effect.visual", "effect", "Visual effects and effect-animation package."),
    "event": ("event.visual", "event", "Event, award, world-map, and event-scene package."),
    "friend": ("ui.social.friend", "ui", "Friend and social presentation package."),
    "game": ("world.gameplay", "world", "Core gameplay, room, background, cursor, and world presentation package."),
    "helper": ("character.helper", "character", "Helper and support-character package."),
    "human": ("character.staff.human", "character", "Human StaffData image and animation package."),
    "language": ("text.localization", "text", "Localized string and language-table package."),
    "lineup": ("ui.lineup", "ui", "Lineup and catalog thumbnail package."),
    "lineup_layout": ("ui.lineup.layout", "ui", "Lineup layout and animation metadata package."),
    "load": ("ui.load", "ui", "Loading and save/load presentation package."),
    "mail": ("ui.mail", "ui", "Mail and inbox presentation package."),
    "meeting": ("ui.meeting", "ui", "Meeting and idea-scene presentation package."),
    "recruit": ("ui.recruit", "ui", "Recruitment presentation package."),
    "system": ("system.game", "system", "Small system-facing game graphics package."),
    "title": ("ui.title", "ui", "Title screen, logo, menu, and title-animation package."),
    "window": ("ui.window", "ui", "Window, dialog, and localized festival package."),
    "xls": ("data.table", "data", "Game data-table package retained as source text."),
}

GROUP_FAMILIES = {
    "03_ANDROID_RES_IMAGES": ("platform.android", "platform", "Android platform and launcher resources."),
    "04_MISC_TEXTASSETS": ("data.unity_textasset", "data", "Unity TextAsset/data payload retained for provenance."),
}

EXTENSION_ROLES = {
    ".png": ("raster", "Raster image payload."),
    ".seb": ("animation_timeline", "SEB animation/timeline payload."),
    ".opt": ("logical_composition", "OPT logical composition payload."),
    ".inf": ("selector_index", "INF selector index payload."),
    ".txt": ("text_or_data", "Text or data payload."),
    ".csv": ("text_or_data", "CSV data payload."),
    ".json": ("text_or_data", "JSON data payload."),
    ".bin": ("binary_payload", "Binary payload."),
    ".resource": ("unity_resource", "Unity resource payload."),
}

LINEAGE_BY_KIND = {
    "original_pack_asset": ("original_native", "Present in the original game asset pack."),
    "opt_reconstructed_image": ("derived_reconstruction", "Derived from a native OPT/composition workflow."),
    "seb_preview_image": ("derived_preview", "Derived preview for browsing or inspection."),
    "android_raster_resource": ("platform_resource", "Android platform resource, separate from game pack family."),
    "contact_sheet_catalog": ("derived_catalog", "Browse/catalog derivative, not an original packed asset."),
    "plain_textasset_payload": ("retained_payload", "Retained payload with unresolved or non-visual Unity provenance."),
}


def stable_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def family_for_row(row: dict[str, Any]) -> tuple[str, str, str, str, str]:
    pack = row["pack"]
    if pack in PACK_FAMILIES:
        family_id, category, purpose = PACK_FAMILIES[pack]
    else:
        path = row["relative_path"]
        group = path.split("/", 1)[0]
        if group not in GROUP_FAMILIES:
            raise ValueError(f"unclassified asset pack/group: {pack} / {path}")
        family_id, category, purpose = GROUP_FAMILIES[group]
    extension = row["extension"]
    if extension not in EXTENSION_ROLES:
        raise ValueError(f"unclassified extension: {extension} ({row['relative_path']})")
    structural_subfamily, subfamily_purpose = EXTENSION_ROLES[extension]
    return family_id, category, purpose, structural_subfamily, subfamily_purpose


def build_payload() -> dict[str, Any]:
    coverage = load_json(COVERAGE_PATH)
    assets = coverage["assets"]
    taxonomy_rows = []
    family_rows: dict[str, dict[str, Any]] = {}
    status_counters: Counter[str] = Counter()
    lineage_counters: Counter[str] = Counter()
    for asset in assets:
        family_id, category, purpose, subfamily, subfamily_purpose = family_for_row(asset)
        lineage, lineage_purpose = LINEAGE_BY_KIND[asset["kind"]]
        taxonomy_status = "classified_structural_family"
        status_counters[taxonomy_status] += 1
        lineage_counters[lineage] += 1
        family_rows.setdefault(
            family_id,
            {
                "family_id": family_id,
                "category": category,
                "purpose": purpose,
                "taxonomy_confidence": "structural_pack_extension",
                "subfamilies": {},
                "row_count": 0,
                "runtime_referenced_count": 0,
                "coverage_statuses": Counter(),
                "lineages": Counter(),
                "semantic_roles": set(),
            },
        )
        family = family_rows[family_id]
        family["row_count"] += 1
        family["runtime_referenced_count"] += int(asset["runtime_reference_count"] > 0)
        family["coverage_statuses"][asset["coverage_status"]] += 1
        family["lineages"][lineage] += 1
        family["semantic_roles"].add(asset["semantic_role"])
        family["subfamilies"].setdefault(subfamily, {"row_count": 0, "extensions": set()})
        family["subfamilies"][subfamily]["row_count"] += 1
        family["subfamilies"][subfamily]["extensions"].add(asset["extension"])

        taxonomy_rows.append(
            {
                "asset_id": asset["asset_id"],
                "relative_path": asset["relative_path"],
                "pack": asset["pack"],
                "kind": asset["kind"],
                "extension": asset["extension"],
                "family_id": family_id,
                "category": category,
                "family_purpose": purpose,
                "subfamily_id": f"{family_id}.{subfamily}",
                "subfamily": subfamily,
                "subfamily_purpose": subfamily_purpose,
                "lineage": lineage,
                "lineage_purpose": lineage_purpose,
                "taxonomy_status": taxonomy_status,
                "taxonomy_confidence": "structural_pack_extension",
                "semantic_role_evidence": asset["semantic_role"],
                "native_source_status": asset["native_source_status"],
                "coverage_status": asset["coverage_status"],
                "runtime_families": asset["runtime_families"],
                "native_relation_count": asset["native_relation_count"],
                "geometry_status": asset["geometry_status"],
                "runtime_policy": "eligible_for_later_family_gate" if asset["runtime_reference_count"] else "catalog_only_until_usage_gate",
            }
        )

    family_definitions = []
    for family_id, family in sorted(family_rows.items()):
        subfamilies = []
        for subfamily, values in sorted(family["subfamilies"].items()):
            subfamilies.append({"subfamily": subfamily, "row_count": values["row_count"], "extensions": sorted(values["extensions"])})
        family_definitions.append(
            {
                "family_id": family_id,
                "category": family["category"],
                "purpose": family["purpose"],
                "taxonomy_confidence": family["taxonomy_confidence"],
                "row_count": family["row_count"],
                "runtime_referenced_count": family["runtime_referenced_count"],
                "subfamilies": subfamilies,
                "coverage_statuses": dict(sorted(family["coverage_statuses"].items())),
                "lineages": dict(sorted(family["lineages"].items())),
                "semantic_role_count": len(family["semantic_roles"]),
            }
        )

    payload = {
        "schema_version": "social-dev-asset-family-taxonomy-v1",
        "package": "social-dev",
        "status": "pass",
        "semantic_status": "structural_taxonomy_not_runtime_approval",
        "coverage_ref": {"path": "knowledge/fixtures/accepted/asset_metadata_coverage.json", "content_hash": coverage["determinism"]["content_hash"]},
        "classification_policy": {
            "family_source": "pack name or authoritative archive group",
            "subfamily_source": "file extension structural role",
            "lineage_source": "asset index kind",
            "semantic_role_preserved": True,
            "filename_alone_proves_gameplay_usage": False,
            "runtime_promotion_requires_usage_and_composition_gates": True,
        },
        "counts": {
            "assets": len(taxonomy_rows),
            "families": len(family_definitions),
            "subfamilies": sum(len(item["subfamilies"]) for item in family_definitions),
            "taxonomy_statuses": dict(sorted(status_counters.items())),
            "lineages": dict(sorted(lineage_counters.items())),
        },
        "families": family_definitions,
        "assets": sorted(taxonomy_rows, key=lambda item: item["asset_id"]),
        "open_classification_boundary": [
            "Structural family labels are closed for all indexed rows.",
            "Gameplay consumer, call timing, placement, frame semantics, and visual composition remain separate AM-3/AM-4/AM-5 gates.",
            "The 11 helper selector-scope gaps and one lineup_layout unresolved selector remain explicit and are not reclassified by taxonomy.",
        ],
    }
    payload["determinism"] = {"algorithm": "stable-json-sha256 excluding determinism.content_hash", "content_hash": sha256_bytes(stable_json(payload).encode("utf-8"))}
    return payload


def build_contract_payload(taxonomy: dict[str, Any]) -> dict[str, Any]:
    payload = {
        "schema_version": "social-dev-asset-family-taxonomy-contract-v1",
        "package": "social-dev",
        "status": "pass",
        "semantic_status": "structural_taxonomy_contract_not_runtime_approval",
        "taxonomy_path": "knowledge/fixtures/accepted/asset_family_taxonomy.json",
        "taxonomy_content_hash": taxonomy["determinism"]["content_hash"],
        "coverage_content_hash": taxonomy["coverage_ref"]["content_hash"],
        "counts": taxonomy["counts"],
        "runtime_policy": {
            "may_be_used_for_family_lookup": True,
            "may_be_used_to_promote_assets": False,
            "requires_selector_semantics_before_call": True,
            "requires_composition_geometry_before_draw": True,
            "next_gate": "asset_selector_usage_matrix",
        },
        "acceptance": {
            "every_asset_has_family": taxonomy["counts"]["assets"] == 3542,
            "every_asset_has_subfamily": all(item["subfamily"] for item in taxonomy["assets"]),
            "every_asset_has_lineage": all(item["lineage"] for item in taxonomy["assets"]),
            "unknown_taxonomy_rows": sum(1 for item in taxonomy["assets"] if item["taxonomy_status"] != "classified_structural_family"),
        },
    }
    payload["determinism"] = {"algorithm": "stable-json-sha256 excluding determinism.content_hash", "content_hash": sha256_bytes(stable_json(payload).encode("utf-8"))}
    return payload


def markdown_report(taxonomy: dict[str, Any], contract: dict[str, Any]) -> str:
    lines = [
        "# Social Dev asset-family taxonomy",
        "",
        "AM-2 assigns every indexed asset a structural family, extension-based subfamily, lineage, and explicit runtime boundary. These labels make lookup and filtering deterministic without claiming that pack membership alone proves a gameplay call.",
        "",
        "## Identity",
        "",
        f"- Taxonomy content hash: `{taxonomy['determinism']['content_hash']}`",
        f"- Coverage content hash: `{taxonomy['coverage_ref']['content_hash']}`",
        f"- Contract content hash: `{contract['determinism']['content_hash']}`",
        "",
        "## Counts",
        "",
        "| Dimension | Count |",
        "|---|---:|",
        f"| Assets classified | {taxonomy['counts']['assets']:,} |",
        f"| Families | {taxonomy['counts']['families']:,} |",
        f"| Structural subfamilies | {taxonomy['counts']['subfamilies']:,} |",
        "",
        "## Families",
        "",
        "| Family | Category | Rows | Runtime-referenced | Subfamilies |",
        "|---|---|---:|---:|---:|",
    ]
    for family in taxonomy["families"]:
        lines.append(f"| `{family['family_id']}` | {family['category']} | {family['row_count']:,} | {family['runtime_referenced_count']:,} | {len(family['subfamilies']):,} |")
    lines.extend(
        [
            "",
            "## Lineage",
            "",
            "| Lineage | Rows |",
            "|---|---:|",
        ]
    )
    for lineage, count in taxonomy["counts"]["lineages"].items():
        lines.append(f"| `{lineage}` | {count:,} |")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- Family/subfamily/lineage classification is closed for all indexed rows.",
            "- Selector meaning, consumer call timing, frame/layer geometry, placement, and lifecycle remain separate gates.",
            "- The taxonomy does not turn the 3,231 currently unreferenced rows into deletions or runtime assets.",
            "",
            "```powershell",
            "python -B tools/social-dev/build_asset_family_taxonomy.py",
            "python -B tools/social-dev/test_asset_family_taxonomy.py",
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    taxonomy = build_payload()
    contract = build_contract_payload(taxonomy)
    write_json(TAXONOMY_PATH, taxonomy)
    write_json(CONTRACT_PATH, contract)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(markdown_report(taxonomy, contract), encoding="utf-8", newline="\n")
    print(json.dumps({"taxonomy_content_hash": taxonomy["determinism"]["content_hash"], "assets": taxonomy["counts"]["assets"], "families": taxonomy["counts"]["families"], "subfamilies": taxonomy["counts"]["subfamilies"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
