import hashlib
import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from zipfile import ZipFile, is_zipfile

from .paths import relative_path, within_workspace, workspace_root


FLOOR_RE = re.compile(r"^floor(?P<number>\d+)\.(?P<kind>seb|png)$", re.IGNORECASE)
STAT_FIELDS = ("size", "modified_time_ns", "sha256")


def _sha256_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _record(path, root):
    stat = path.stat()
    if path.is_file():
        checksum = _sha256_file(path)
        size = stat.st_size
    else:
        children = []
        size = 0
        for child in sorted(path.rglob("*"), key=lambda item: item.as_posix().lower()):
            if child.is_file():
                child_size = child.stat().st_size
                size += child_size
                children.append((child.relative_to(path).as_posix(), child_size, _sha256_file(child)))
        checksum = hashlib.sha256(json.dumps(children, separators=(",", ":")).encode()).hexdigest()
    return {
        "path": relative_path(root, path),
        "kind": "file" if path.is_file() else "directory",
        "size": size,
        "modified_time_ns": stat.st_mtime_ns,
        "sha256": checksum,
    }


def _status(path_record):
    if path_record is None:
        return {"status": "unknown", "source": None}
    return {"status": "verified", "source": path_record["path"]}


@dataclass(frozen=True)
class SourceInventory:
    roots: list
    files: dict
    archives: dict
    floor_ids: list
    relations: dict
    declared_paths: list

    def to_dict(self):
        return {
            "schema": "scene-source-inventory-v1",
            "claim_statuses": ["verified", "candidate", "unknown"],
            "roots": self.roots,
            "declared_paths": self.declared_paths,
            "files": self.files,
            "archives": self.archives,
            "floor_ids": self.floor_ids,
            "relations": self.relations,
        }

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2, sort_keys=True) + "\n"


def _fixture_candidates(root, actual, aliases):
    candidates = [root / actual]
    candidates.extend(root / alias for alias in aliases)
    return next((path for path in candidates if path.exists()), None)


def _env_paths(root):
    env = root / "APK_Toolkit" / ".last_extraction.env"
    if not env.exists():
        env = root / ".last_extraction.env"
    if not env.exists():
        return []
    paths = []
    for line in env.read_text(encoding="utf-8").splitlines():
        if "=" not in line or not line.strip() or line.lstrip().startswith("#"):
            continue
        _, value = line.split("=", 1)
        path = Path(value.strip())
        paths.append(path if path.is_absolute() else root / path)
    return paths


def _floor_entries(root, source_paths, archives):
    entries = {}
    for source in source_paths:
        if source.is_dir():
            iterator = (item for item in source.rglob("*") if item.is_file())
            for item in iterator:
                match = FLOOR_RE.match(item.name)
                if match:
                    floor_id = f"floor{int(match.group('number'))}"
                    entries.setdefault(floor_id, {}).setdefault(match.group("kind").lower(), []).append(relative_path(root, item))
    for archive in archives.values():
        for member in archive["members"]:
            match = FLOOR_RE.match(Path(member["name"]).name)
            if match:
                floor_id = f"floor{int(match.group('number'))}"
                entries.setdefault(floor_id, {}).setdefault(match.group("kind").lower(), []).append(member["path"])
    return entries


def build_source_inventory(fixtures=None, extra_paths=None):
    root = workspace_root(fixtures)
    requested = list(extra_paths or [])
    for path in requested:
        within_workspace(root, path)

    specs = [
        ("APK_Toolkit/game-dev-story-mod.apk", "apk/game-dev-story-mod.apk", "apk"),
        ("APK_Toolkit/game-dev-story-mod.zip", "archive/game-dev-story-mod.zip", "archive"),
        ("game-dev-story-mod_Extracted", "extracted", "extraction"),
        ("game-dev-story-mod_Dumped", "dumped", "dump"),
        ("game-dev-story-mod_Sprites", "sprites", "sprites"),
        ("knowledge/csharp/primary", "primary", "csharp"),
        ("game-dev-story-mod_Dumped/Categorized_Code", "dumped/Categorized_Code", "categorized_code"),
        ("game-dev-story-mod_Dumped/Failed_Functions_Assembly", "dumped/Failed_Functions_Assembly", "assembly"),
        ("game-dev-story-mod_Dumped/DummyDll/Assembly-CSharp.dll", "dumped/DummyDll/Assembly-CSharp.dll", "assembly_dll"),
    ]
    records = {}
    physical_paths = {}
    roots = []
    source_paths = []
    for logical, actual, role in specs:
        aliases = [actual]
        path = _fixture_candidates(root, logical, aliases)
        if path is None:
            continue
        path = within_workspace(root, path)
        record = _record(path, root)
        if path.is_file():
            record["path"] = logical
            physical_paths[logical] = path
        roots.append({"logical_path": logical, "role": role, **record})
        source_paths.append(path)
        if path.is_file():
            records[record["path"]] = record
        else:
            for child in path.rglob("*"):
                if child.is_file():
                    child_record = _record(child, root)
                    records[child_record["path"]] = child_record

    for path in _env_paths(root):
        path = within_workspace(root, path)
        if path.exists() and path not in source_paths:
            source_paths.append(path)
        if path.exists():
            record = _record(path, root)
            records.setdefault(record["path"], record)

    archives = {}
    for record in list(records.values()):
        if record["path"].lower().endswith((".zip", ".apk")):
            path = physical_paths.get(record["path"], root / record["path"])
            members = []
            if is_zipfile(path):
                with ZipFile(path) as archive:
                    for info in archive.infolist():
                        members.append({"path": f"{record['path']}::{info.filename}", "name": info.filename, "crc": info.CRC, "size": info.file_size, "compressed_size": info.compress_size})
            archives[record["path"]] = {"path": record["path"], "members": members}

    entries = _floor_entries(root, source_paths, archives)
    floor_ids = sorted(entries, key=lambda value: int(value[5:]))
    relations = {}
    for floor_id in floor_ids:
        floor = entries[floor_id]
        pngs = floor.get("png", [])
        sebs = floor.get("seb", [])
        office_png = next((value for value in pngs if "/office/" in value.lower() or "::" in value and "/office/" in value.lower()), None)
        office_seb = next((value for value in sebs if "/office/" in value.lower() or "::" in value and "/office/" in value.lower()), None)
        relations[floor_id] = {
            "office_png": {"status": "verified" if office_png else "unknown", "source": office_png},
            "office_seb": {"status": "verified" if office_seb else "unknown", "source": office_seb},
            "all_png": sorted(pngs),
            "all_seb": sorted(sebs),
        }
    return SourceInventory(
        roots=sorted(roots, key=lambda item: item["logical_path"]),
        files={key: records[key] for key in sorted(records)},
        archives={key: archives[key] for key in sorted(archives)},
        floor_ids=floor_ids,
        relations=relations,
        declared_paths=sorted(relative_path(root, path) for path in _env_paths(root)),
    )
