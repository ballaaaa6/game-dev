"""Evidence-first floor/resource/layer identity resolution.

Names that merely share a numeric suffix remain candidates.  This module is
deliberately small and data-shaped so it can consume the reviewed inventories
without importing any source/extraction code.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from pathlib import PurePosixPath


CLAIM_STATUSES = ("verified", "candidate", "unknown")
_FLOOR_RE = re.compile(r"^(?P<stem>floor(?:parts)?\d+|floor)\.(?P<ext>png|seb)$", re.IGNORECASE)


@dataclass(frozen=True)
class Relation:
    source: str | None
    target: str | None
    status: str
    reason: str
    evidence: tuple[dict, ...] = ()

    def to_dict(self) -> dict:
        return asdict(self) | {"evidence": list(self.evidence)}


def _stem(path: str | None) -> str | None:
    if not path:
        return None
    return PurePosixPath(path.replace("\\", "/")).stem.lower()


def resolve_relation(
    source: str | None,
    target: str | None,
    *,
    exact_identity: bool = False,
    loader_match: bool = False,
    selector: str | None = None,
    conflict: bool = False,
) -> Relation:
    """Resolve one relation using the brief's fixed priority order."""

    evidence = []
    if exact_identity:
        evidence.append({"kind": "exact_archive_resource_identity", "status": "verified"})
    if loader_match:
        evidence.append({"kind": "loader_selector_identity", "selector": selector, "status": "verified"})
    if source and target and _stem(source) == _stem(target):
        evidence.append({"kind": "same_stem", "status": "candidate"})

    if conflict or (exact_identity and loader_match is False and source and target and _stem(source) != _stem(target)):
        return Relation(source, target, "unknown", "conflicting_evidence", tuple(evidence))
    if not source or not target:
        return Relation(source, target, "unknown", "missing_resource", tuple(evidence))
    if exact_identity:
        return Relation(source, target, "verified", "exact_archive_resource_identity", tuple(evidence))
    if loader_match:
        return Relation(source, target, "verified", "loader_selector_identity", tuple(evidence))
    if _stem(source) == _stem(target):
        return Relation(source, target, "candidate", "same_stem_only", tuple(evidence))
    return Relation(source, target, "unknown", "no_identity_evidence", tuple(evidence))


def _file_record(inventory: dict, path: str) -> dict:
    return dict(inventory.get("files", {}).get(path, {}))


def _catalog_by_path(resource_inputs: dict) -> dict[str, dict]:
    result = {}
    for row in resource_inputs.get("catalog_files", resource_inputs.get("catalog", [])) or []:
        source = row.get("source", {}) if isinstance(row, dict) else {}
        path = source.get("path") or row.get("path")
        if path:
            result[path] = row
    return result


def _role_for(path: str, catalog: dict[str, dict], office_assets: dict[str, dict]) -> tuple[str, str, dict]:
    row = catalog.get(path) or office_assets.get(path.replace("game-dev-story-mod_Sprites/", ""), {})
    role = row.get("role") or row.get("semantics", {}).get("visual_role")
    confidence = row.get("confidence") or row.get("semantics", {}).get("visual_role_confidence")
    if role:
        return role, confidence or "unknown", row
    name = PurePosixPath(path).name.lower()
    if name.startswith("floorparts") or name == "floorcover.png":
        return "room_parts_or_cover", "unknown", row
    if name.endswith(".seb"):
        return "sprite_descriptor", "unknown", row
    return "unknown", "unknown", row


def _resource_paths(inventory: dict) -> list[str]:
    paths = set()
    for path in inventory.get("files", {}):
        if _FLOOR_RE.match(PurePosixPath(path.replace("\\", "/")).name):
            paths.add(path)
    for relation in inventory.get("relations", {}).values():
        paths.update(relation.get("all_png", []))
        paths.update(relation.get("all_seb", []))
    return sorted(paths)


def resolve_floor_layers(inventory: dict, seb_audit: dict, resource_inputs: dict | None = None) -> dict:
    """Build a source-preserving contract of floor resources and relations."""

    resource_inputs = resource_inputs or {}
    catalog = _catalog_by_path(resource_inputs)
    office_assets = {
        row.get("path"): row for row in resource_inputs.get("office_assets", []) if row.get("path")
    }
    resources = []
    by_floor: dict[str, list[dict]] = {}
    for path in _resource_paths(inventory):
        name = PurePosixPath(path.replace("\\", "/")).name
        match = _FLOOR_RE.match(name)
        if not match:
            continue
        stem = match.group("stem").lower()
        floor_id = "floor" + re.search(r"\d+", stem).group(0) if re.search(r"\d+", stem) else "unknown"
        record = _file_record(inventory, path)
        role, role_confidence, role_row = _role_for(path, catalog, office_assets)
        node = {
            "id": f"resource.{path}",
            "floor_id": floor_id,
            "layer_key": stem,
            "source_path": path,
            "extension": match.group("ext").lower(),
            "size_bytes": record.get("size", role_row.get("source", {}).get("size_bytes")),
            "sha256": record.get("sha256", role_row.get("source", {}).get("sha256")),
            "dimensions": role_row.get("dimensions"),
            "role": role,
            "role_status": role_confidence if role_confidence in CLAIM_STATUSES else "unknown",
            "source_record": record,
            "catalog_record": role_row,
            "selectors": role_row.get("legacy", {}).get("inf", role_row.get("inf", [])),
        }
        resources.append(node)
        by_floor.setdefault(floor_id, []).append(node)

    relations = []
    for floor_id, nodes in sorted(by_floor.items()):
        pngs = [node for node in nodes if node["extension"] == "png"]
        sebs = [node for node in nodes if node["extension"] == "seb"]
        for png in pngs:
            for seb in sebs:
                rel = resolve_relation(png["source_path"], seb["source_path"])
                relations.append({"floor_id": floor_id, "kind": "png_to_seb", **rel.to_dict()})

    audit_by_floor = {row.get("floor_id"): row for row in seb_audit.get("floors", [])}
    gaps = []
    for floor_id, row in sorted(inventory.get("relations", {}).items()):
        pngs = row.get("all_png", [])
        sebs = row.get("all_seb", [])
        office_pngs = [path for path in pngs if "/office/" in path.lower()]
        office_sebs = [path for path in sebs if "/office/" in path.lower()]
        if office_pngs and not office_sebs:
            gaps.append({
                "floor_id": floor_id,
                "png": office_pngs,
                "expected_seb": f"office/{floor_id}.seb",
                "status": "unknown",
                "reason": "missing_resource",
                "seb_audit": audit_by_floor.get(floor_id),
            })

    counts = {status: 0 for status in CLAIM_STATUSES}
    for relation in relations:
        counts[relation["status"]] += 1
    return {
        "schema": "scene-resource-contract-v1",
        "claim_statuses": list(CLAIM_STATUSES),
        "relation_priority": [
            "exact_archive_resource_identity",
            "loader_selector_identity",
            "same_stem_only",
            "unknown_for_absence_or_conflict",
        ],
        "resources": resources,
        "relations": relations,
        "known_gaps": gaps,
        "seb_audit_outcomes": seb_audit.get("counts", {}),
        "counts": {"resources": len(resources), "relations": counts, "known_gaps": len(gaps)},
        "evidence_sources": resource_inputs.get("evidence_sources", []),
        "loader_evidence": {
            "status": "verified" if resource_inputs.get("loader_matches") else "unknown",
            "matches": resource_inputs.get("loader_matches", []),
            "note": "Loader text matches are retained as discovery evidence; no match is promoted to ownership without an explicit selector identity.",
        },
    }
