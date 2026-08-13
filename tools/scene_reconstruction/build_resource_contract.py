"""Build the Task 3 floor/resource/layer identity contract."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tools.scene_reconstruction.paths import workspace_root
from tools.scene_reconstruction.resource_relations import resolve_floor_layers


ROOT = Path(__file__).resolve().parents[2]
INVENTORY = ROOT / "knowledge/world-assets/evidence/scene_reconstruction/source_inventory.json"
SEB_AUDIT = ROOT / "knowledge/world-assets/evidence/scene_reconstruction/seb_audit.json"
OUTPUT = ROOT / "knowledge/world-assets/evidence/scene_reconstruction/resource_contract.json"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _resource_inputs(root: Path) -> dict:
    catalog = _load(root / "knowledge/world-assets/evidence/phase1_asset_catalog.json")
    office = _load(root / "knowledge/world-assets/evidence/office_manifest.json")
    legacy = _load(root / "knowledge/world-assets/evidence/phase1_legacy_asset_map.json")
    seb = _load(root / "knowledge/world-assets/evidence/phase1_seb_manifest.json")
    loader_paths = [
        "knowledge/csharp/primary",
        "game-dev-story-mod_Dumped/Categorized_Code",
        "game-dev-story-mod_Dumped/Failed_Functions_Assembly",
    ]
    matches = []
    for relative in loader_paths:
        path = root / relative
        if not path.exists():
            continue
        for source in path.rglob("*"):
            if not source.is_file() or source.suffix.lower() not in {".cs", ".c", ".h"}:
                continue
            for line_number, line in enumerate(source.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
                if re.search(r"floor|floorparts|\.seb|img\.inf|Load.*(Image|Resource)", line, re.IGNORECASE):
                    matches.append({"path": source.relative_to(root).as_posix(), "line": line_number, "text": line})
    return {
        "catalog_files": catalog.get("files", []),
        "office_assets": office.get("assets", []),
        "evidence_sources": [
            "knowledge/world-assets/evidence/phase1_asset_catalog.json",
            "knowledge/world-assets/evidence/phase1_legacy_asset_map.json",
            "knowledge/world-assets/evidence/phase1_seb_manifest.json",
            "knowledge/world-assets/evidence/office_manifest.json",
            "knowledge/csharp/primary/",
        ],
        "legacy_inf_documents": legacy.get("inf_documents", []),
        "seb_manifest": seb,
        "loader_matches": matches,
    }


def build_contract(root: Path | None = None) -> dict:
    root = workspace_root(root or ROOT)
    inventory = _load(root / INVENTORY.relative_to(ROOT))
    seb_audit = _load(root / SEB_AUDIT.relative_to(ROOT))
    return resolve_floor_layers(inventory, seb_audit, _resource_inputs(root))


def main() -> int:
    root = workspace_root(ROOT)
    contract = build_contract(root)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(contract, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(f"[OK] Wrote {OUTPUT} ({contract['counts']['resources']} resources, {contract['counts']['relations']} relations)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
