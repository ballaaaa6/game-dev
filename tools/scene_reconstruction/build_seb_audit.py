"""Audit every discovered floor SEB against direct archive/extraction candidates."""

from __future__ import annotations

import json
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from zipfile import BadZipFile, ZipFile, is_zipfile

try:
    from .paths import relative_path, workspace_root
    from .seb_codec import SebCandidate, SebComparison, compare_seb_sources
except ImportError:  # Supports ``python tools/scene_reconstruction/build_seb_audit.py``.
    from paths import relative_path, workspace_root
    from seb_codec import SebCandidate, SebComparison, compare_seb_sources


SOURCE_INVENTORY = Path("knowledge/world-assets/evidence/scene_reconstruction/source_inventory.json")
AUDIT_OUTPUT = Path("knowledge/world-assets/evidence/scene_reconstruction/seb_audit.json")
LEGACY_EVIDENCE = Path("knowledge/world-assets/evidence/phase1_seb_manifest.json")
REEXTRACT_ROOT = Path("knowledge/world-assets/evidence/scene_reconstruction/reextract")


@dataclass(frozen=True)
class SebAuditFloor:
    floor_id: str
    pair: dict
    comparison: SebComparison
    staged_payload: dict | None

    @property
    def outcome(self) -> str:
        return self.comparison.outcome

    def to_dict(self) -> dict:
        return {
            "floor_id": self.floor_id,
            "pair": self.pair,
            "outcome": self.outcome,
            "staged_payload": self.staged_payload,
            "source_comparison": self.comparison.to_dict(),
        }


@dataclass(frozen=True)
class SebAudit:
    workspace: str
    inventory_path: str
    floors: tuple[SebAuditFloor, ...]

    def to_dict(self) -> dict:
        outcomes: dict[str, int] = {}
        for floor in self.floors:
            outcomes[floor.outcome] = outcomes.get(floor.outcome, 0) + 1
        return {
            "schema": "scene-seb-audit-v1",
            "claim_statuses": ["verified", "candidate", "unknown"],
            "source_inventory": self.inventory_path,
            "source_policy": "Read-only source/extraction inputs; a payload is staged only when a direct archive candidate is longer or distinct.",
            "counts": {"floors": len(self.floors), "outcomes": outcomes},
            "floors": [floor.to_dict() for floor in self.floors],
        }


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _read_file_candidate(root: Path, source_kind: str, relative: str) -> SebCandidate:
    path = root / relative
    source_ref = relative_path(root, path) if path.exists() else f"{relative} (absent)"
    try:
        return SebCandidate(source_kind, source_ref, path.read_bytes())
    except FileNotFoundError:
        return SebCandidate(source_kind, source_ref, None)
    except OSError as exc:
        return SebCandidate(source_kind, source_ref, None, read_error=str(exc))


def _archive_candidates(root: Path, archive_relative: str, filename: str) -> list[SebCandidate]:
    archive_path = root / archive_relative
    source_ref = f"{archive_relative}::{filename}"
    if not archive_path.exists():
        return [SebCandidate("apk" if archive_relative.endswith(".apk") else "zip", source_ref, None)]
    if not is_zipfile(archive_path):
        return [SebCandidate("apk" if archive_relative.endswith(".apk") else "zip", source_ref, None, read_error="not_a_zip_archive")]
    source_kind = "apk" if archive_relative.endswith(".apk") else "zip"
    try:
        with ZipFile(archive_path) as archive:
            members = [info for info in archive.infolist() if Path(info.filename).name.lower() == filename.lower()]
            if not members:
                return [SebCandidate(source_kind, source_ref, None)]
            result = []
            for info in members:
                member_ref = f"{archive_relative}::{info.filename}"
                result.append(
                    SebCandidate(
                        source_kind,
                        member_ref,
                        archive.read(info),
                        archive_member_path=info.filename,
                        archive_path=archive_relative,
                    )
                )
            return result
    except (BadZipFile, OSError, KeyError) as exc:
        return [SebCandidate(source_kind, source_ref, None, read_error=str(exc))]


def _evidence_hashes(root: Path) -> dict[str, str]:
    path = root / LEGACY_EVIDENCE
    if not path.exists():
        return {}
    try:
        return {
            str(entry.get("relative_path")): str(entry["sha256"])
            for entry in _load_json(path).get("files", [])
            if entry.get("relative_path") and entry.get("sha256")
        }
    except (OSError, ValueError, TypeError):
        return {}


def _floor_number(value: str) -> int:
    return int(value[5:])


def _staged_payload(root: Path, comparison: SebComparison) -> dict | None:
    best = comparison.best_complete
    if comparison.outcome not in {"recovered_full_payload", "recovered_different_payload"} or best is None:
        return None
    if best.source_kind not in {"apk", "zip", "fresh"} or best.parsed is None:
        return None
    source_data = next(
        item.parsed for item in comparison.candidates if item.source_ref == best.source_ref and item.parsed is not None
    )
    # ``SebFile`` carries the checksum, while the original payload is obtained
    # from the archive candidate by reopening its exact member below.
    if best.archive_path is None or best.archive_member_path is None:
        return None
    archive = root / best.archive_path
    try:
        with ZipFile(archive) as container:
            data = container.read(best.archive_member_path)
    except (BadZipFile, KeyError, OSError):
        return None
    digest = sha256(data).hexdigest()
    if digest != source_data.sha256:
        return None
    destination = root / REEXTRACT_ROOT / digest / Path(best.archive_member_path).name
    destination.parent.mkdir(parents=True, exist_ok=True)
    if not destination.exists():
        destination.write_bytes(data)
    return {
        "status": "verified",
        "path": relative_path(root, destination),
        "sha256": digest,
        "size_bytes": len(data),
        "archive_path": best.archive_path,
        "archive_member_path": best.archive_member_path,
    }


def _candidate_paths(root: Path, floor_id: str, relation: dict, hashes: dict[str, str]) -> list[SebCandidate]:
    filename = f"{floor_id}.seb"
    candidates: list[SebCandidate] = []
    seb_paths = relation.get("all_seb", [])
    sprite_paths = [path for path in seb_paths if path.startswith("game-dev-story-mod_Sprites/")]
    if sprite_paths:
        candidates.extend(_read_file_candidate(root, "sprite", path) for path in sprite_paths)
    else:
        candidates.append(SebCandidate("sprite", f"game-dev-story-mod_Sprites/**/{filename}", None))
    extracted_matches = sorted((root / "game-dev-story-mod_Extracted").rglob(filename)) if (root / "game-dev-story-mod_Extracted").exists() else []
    if extracted_matches:
        for path in extracted_matches:
            candidates.append(_read_file_candidate(root, "extracted", relative_path(root, path)))
    else:
        candidates.append(SebCandidate("extracted", f"game-dev-story-mod_Extracted/**/{filename}", None))
    for archive_relative in ("APK_Toolkit/game-dev-story-mod.apk", "APK_Toolkit/game-dev-story-mod.zip"):
        candidates.extend(_archive_candidates(root, archive_relative, filename))
    for sprite_path in sprite_paths:
        rel = Path(sprite_path).relative_to("game-dev-story-mod_Sprites").as_posix()
        candidates.append(
            SebCandidate(
                "evidence",
                f"{LEGACY_EVIDENCE.as_posix()}::{rel}",
                None,
                declared_sha256=hashes.get(rel),
            )
        )
    return candidates


def build_seb_audit(workspace=None, *, inventory_path=None) -> SebAudit:
    root = workspace_root(workspace)
    inventory_file = Path(inventory_path) if inventory_path else root / SOURCE_INVENTORY
    if not inventory_file.is_absolute():
        inventory_file = root / inventory_file
    inventory = _load_json(inventory_file)
    hashes = _evidence_hashes(root)
    floors: list[SebAuditFloor] = []
    for floor_id, relation in sorted(inventory.get("relations", {}).items(), key=lambda item: _floor_number(item[0])):
        if not relation.get("all_seb"):
            continue
        candidates = _candidate_paths(root, floor_id, relation, hashes)
        comparison = compare_seb_sources(candidates)
        pair = {
            "png": {
                "status": "verified" if relation.get("all_png") else "unknown",
                "sources": relation.get("all_png", []),
            },
            "seb": {
                "status": "verified" if relation.get("all_seb") else "unknown",
                "sources": relation.get("all_seb", []),
            },
        }
        floors.append(SebAuditFloor(floor_id, pair, comparison, _staged_payload(root, comparison)))
    return SebAudit(relative_path(root, root), relative_path(root, inventory_file), tuple(floors))


def main() -> int:
    root = workspace_root()
    audit = build_seb_audit(root)
    output = root / AUDIT_OUTPUT
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes((json.dumps(audit.to_dict(), indent=2, sort_keys=True) + "\n").encode("utf-8"))
    print(f"[OK] Audited {len(audit.floors)} floor SEB files: {audit.to_dict()['counts']['outcomes']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
