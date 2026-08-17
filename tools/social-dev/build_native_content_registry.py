"""Build a native-faithful Social Dev content registry and evidence graph.

The registry preserves the game's separate identity spaces instead of collapsing
them into one synthetic integer ID:

* DataManager record IDs, such as ``FurnitureData.id_``.
* Resource selector IDs, such as ``seb_``, ``subSeb_`` and ``img_``.
* Source/derived asset identities, including archive path and SHA-256.
* Runtime consumer and lifecycle edges discovered from the C# evidence.

The decompiled C# is evidence only. This tool parses the staged source and the
read-only asset index/archive; it does not execute the game code.
"""

from __future__ import annotations

import csv
import hashlib
import json
import posixpath
import re
import zipfile
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[2]
DATA_UPDATE_ROOT = ROOT / "knowledge/sources/data/csharp_update"
RAW_CSHARP_ROOT = ROOT / "knowledge/sources/csharp_raw_20260813/1_Click_CSharp_Code"
CSHARP_INVENTORY_ROOT = ROOT / "knowledge/fixtures/accepted/csharp_inventory"
ASSET_INDEX_PATH = ROOT / "knowledge/sources/asset_guide_20260813/00_INDEX/ASSET_INDEX.csv"
ASSET_ZIP_PATH = ROOT / "sources/raw/Social_Dev_Story_v2.5.1_ASSETS_ONLY_WITH_ASSEMBLY_GUIDE.zip"
DATA_CROSSCHECK_PATH = ROOT / "knowledge/fixtures/accepted/data_text_crosscheck.json"
DEFAULT_MAP_CONTRACT_PATH = ROOT / "knowledge/fixtures/accepted/runtime/default_map_chip_contract.json"
OUTPUT_PATH = ROOT / "knowledge/fixtures/accepted/native_content_registry.json"
GRAPH_OUTPUT_PATH = ROOT / "knowledge/fixtures/accepted/native_content_connection_graph.json"
CONTRACT_PATH = ROOT / "knowledge/fixtures/accepted/runtime/native_content_registry_contract.json"
GRAPH_CONTRACT_PATH = ROOT / "knowledge/fixtures/accepted/runtime/native_content_connection_contract.json"
REPORT_PATH = ROOT / "docs/reports/social-dev_native_content_registry.md"
GRAPH_REPORT_PATH = ROOT / "docs/reports/social-dev_native_content_connection_graph.md"

ASSET_ZIP_PREFIX = "Social_Dev_Story_v2.5.1_ASSETS_ONLY/"

DATA_MANAGER_ARRAY_RE = re.compile(
    r"^\s*public\s+(?P<element>[A-Za-z_][A-Za-z0-9_.]*)\[\]\s+(?P<field>[A-Za-z_][A-Za-z0-9_]*)\s*;",
    re.MULTILINE,
)
FIELD_RE = re.compile(
    r"^\s*(?:public|private|protected|internal)\s+"
    r"(?:(?:static|readonly|virtual|override|const|volatile)\s+)*"
    r"(?P<type>[A-Za-z_][A-Za-z0-9_.]*(?:<[^;{}=]+>)?(?:\[\s*,?\s*\])*)\s+"
    r"(?P<name>[A-Za-z_][A-Za-z0-9_]*)\s*(?:;|=)",
    re.MULTILINE,
)
CALL_RE = re.compile(r"\bsas\.(?P<method>Get[A-Za-z_][A-Za-z0-9_]*)\s*\(")
INT_RE = re.compile(r"^[+-]?\d+$")
TOKEN_RE_TEMPLATE = r"\b{token}\b"

TRACE_DATA_FIELDS = {
    "seb_": "resource_selector:chip:seb",
    "subSeb_": "resource_selector:chip:subseb",
    "floorImgId_": "resource_selector:chip:img:floor",
    "wallImgId_": "resource_selector:chip:img:wall",
    "doorImgId_": "resource_selector:chip:img:door",
    "passMap_": "scene_semantics:pass_map",
    "objMap_": "scene_semantics:object_map",
    "objDir_": "scene_semantics:object_direction",
}

LIFECYCLE_METHOD_NAMES = {
    "Load",
    "NewGame",
    "Serialize",
    "Deserialize",
    "Deserialized",
    "Init",
    "InitMapChips",
    "InitObjChips",
    "SetupBigChipsParent",
    "PlaceDoor",
    "PlaceDesk",
    "Draw",
    "DrawFloor",
    "DrawExtentionFloor",
    "DrawWall",
    "Update",
}

KNOWN_FIELD_ORDERS = {
    "RoomData": [
        "id_", "name_", "costMoney_", "costCoin_", "deskNum_", "equipSmallNum_", "equipBigNum_",
        "objMap_", "objDir_", "floorImgId_", "wallImgId_", "doorImgId_", "flag_", "costMax_",
    ],
    "FurnitureData": [
        "id_", "name_", "category_", "type_", "price_", "priceRise_", "explain_", "terms_",
        "seb_", "subSeb_", "img_", "paramType_", "paramValue_", "paramTarget_", "flag_",
        "recovery_", "buildTime_", "useBonus_", "passMap_", "costMaxUpValue_", "stockMaxUpValue_",
    ],
    "StaffData": [
        "id_", "lastName_", "firstName_", "sortId_", "img_", "rank_", "jobId_", "favorite_", "hobby_",
        "defParams_", "employmentFukidashi_", "dismissalFukidashi_", "area_", "extraRate_", "flag_",
        "evolveMaxNum_", "cost_", "skill_", "hitRate_", "bonusTerms_", "bonusRate_",
    ],
    "HelperData": [
        "id_", "name_", "explain_", "term_", "rate_", "rank_", "costType_", "cost_", "img_", "bigImg_",
        "helloTalk_", "goodbyeTalk_", "execTalk_", "effectType_", "effect_", "flag_",
    ],
}

KNOWN_ARRAY_READERS = {
    "GetIntArray": int,
    "GetIntIntArray": int,
    "GetStringArray": str,
    "GetByteArray": int,
}


def normalize_path(value: str) -> str:
    return value.replace("\\", "/").lstrip("./")


def relative_path(path: Path) -> str:
    return normalize_path(str(path.relative_to(ROOT)))


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_int(value: str | None) -> int | None:
    if value is None:
        return None
    candidate = value.strip()
    return int(candidate) if INT_RE.fullmatch(candidate) else None


def resolve_existing_path(value: str | None) -> Path | None:
    if not value:
        return None
    candidate = Path(value)
    if candidate.is_absolute() and candidate.is_file():
        return candidate
    candidate = ROOT / normalize_path(value)
    return candidate if candidate.is_file() else None


def extract_method_body(source: str, method_name: str) -> str | None:
    marker = re.search(
        rf"\b(?:public|private|protected|internal)\b[^{{}};]*\b{re.escape(method_name)}\s*\([^)]*\)\s*\{{",
        source,
    )
    if not marker:
        return None
    brace = source.find("{", marker.start(), marker.end())
    depth = 0
    for index in range(brace, len(source)):
        if source[index] == "{":
            depth += 1
        elif source[index] == "}":
            depth -= 1
            if depth == 0:
                return source[brace + 1 : index]
    return None


def parse_fields(source: str) -> list[dict[str, str]]:
    return [
        {
            "type": match.group("type"),
            "name": match.group("name"),
        }
        for match in FIELD_RE.finditer(source)
    ]


def parse_reader_contract(source_path: Path | None) -> dict[str, Any]:
    if source_path is None or not source_path.is_file():
        return {
            "source_status": "missing",
            "reader_sequence": [],
            "field_load_hints": [],
        }
    source = source_path.read_text(encoding="utf-8", errors="replace")
    body = extract_method_body(source, "Load")
    if body is None:
        return {
            "source_status": "method_missing_or_unmatched",
            "reader_sequence": [],
            "field_load_hints": [],
        }
    sequence = [match.group("method") for match in CALL_RE.finditer(body)]
    hints = []
    for line_number, line in enumerate(body.splitlines(), start=1):
        match = re.search(
            r"\b(?P<field>[A-Za-z_][A-Za-z0-9_]*)\s*=\s*(?:[A-Za-z_][A-Za-z0-9_]*\s*=\s*)?sas\.(?P<method>Get[A-Za-z_][A-Za-z0-9_]*)\s*\(",
            line,
        )
        if match:
            hints.append(
                {
                    "field": match.group("field"),
                    "reader": match.group("method"),
                    "method_line": line_number,
                }
            )
    return {
        "source_status": "parsed",
        "reader_sequence": sequence,
        "field_load_hints": hints,
    }


def decode_stream_value(columns: list[str], position: int, reader: str) -> tuple[Any, int]:
    """Decode one StringArrayStream value using the closed array framing rules."""

    if position >= len(columns):
        raise ValueError(f"{reader} read past row at token {position}")
    if reader in {"GetInt", "GetShort", "GetLong", "GetByte"}:
        value = parse_int(columns[position])
        if value is None:
            raise ValueError(f"{reader} expected integer token {columns[position]!r}")
        return value, position + 1
    if reader == "GetString":
        return columns[position], position + 1
    if reader in {"GetIntArray", "GetByteArray", "GetStringArray"}:
        length = parse_int(columns[position])
        if length is None:
            raise ValueError(f"{reader} expected array length token {columns[position]!r}")
        position += 1
        if length < 0:
            return None, position
        end = position + length
        if end > len(columns):
            raise ValueError(f"{reader} length {length} exceeds row at token {position}")
        if reader == "GetStringArray":
            return columns[position:end], end
        values = []
        for token in columns[position:end]:
            value = parse_int(token)
            if value is None:
                raise ValueError(f"{reader} expected integer token {token!r}")
            values.append(value)
        return values, end
    if reader == "GetIntIntArray":
        outer_length = parse_int(columns[position])
        if outer_length is None:
            raise ValueError(f"{reader} expected outer length token {columns[position]!r}")
        position += 1
        if outer_length < 0:
            return None, position
        rows = []
        for _ in range(outer_length):
            row_length = parse_int(columns[position]) if position < len(columns) else None
            if row_length is None:
                raise ValueError(f"{reader} expected row length at token {position}")
            position += 1
            if row_length < 0:
                rows.append(None)
                continue
            end = position + row_length
            if end > len(columns):
                raise ValueError(f"{reader} row length {row_length} exceeds row at token {position}")
            row = []
            for token in columns[position:end]:
                value = parse_int(token)
                if value is None:
                    raise ValueError(f"{reader} expected integer token {token!r}")
                row.append(value)
            rows.append(row)
            position = end
        return rows, position
    if reader == "GetTripleIntArray":
        outer_length = parse_int(columns[position])
        if outer_length is None:
            raise ValueError(f"{reader} expected outer length token {columns[position]!r}")
        position += 1
        if outer_length < 0:
            return None, position
        groups = []
        for _ in range(outer_length):
            middle, position = decode_stream_value(columns, position, "GetIntIntArray")
            groups.append(middle)
        return groups, position
    raise ValueError(f"Unsupported reader {reader}")


def decode_known_fields(source_type: str, columns: list[str], reader_sequence: list[str]) -> dict[str, Any]:
    field_order = KNOWN_FIELD_ORDERS.get(source_type)
    if not field_order:
        return {"status": "not_mapped"}
    if len(field_order) != len(reader_sequence):
        return {
            "status": "reader_field_count_mismatch",
            "field_count": len(field_order),
            "reader_count": len(reader_sequence),
        }
    position = 0
    values = {}
    try:
        for field_name, reader in zip(field_order, reader_sequence):
            value, position = decode_stream_value(columns, position, reader)
            values[field_name] = value
    except ValueError as exc:
        return {
            "status": "decode_error",
            "error": str(exc),
            "consumed_tokens": position,
            "token_count": len(columns),
        }
    return {
        "status": "verified_reader_order",
        "consumed_tokens": position,
        "token_count": len(columns),
        "fields": values,
    }


def load_method_spans() -> dict[str, list[dict[str, Any]]]:
    path = CSHARP_INVENTORY_ROOT / "method_catalog.json"
    if not path.is_file():
        return {}
    records = read_json(path).get("records", [])
    spans: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        source = record.get("source", {})
        file_name = normalize_path(source.get("file", ""))
        if not file_name:
            continue
        spans[file_name].append(
            {
                "owner": record.get("owner"),
                "name": record.get("name"),
                "symbol": record.get("symbol"),
                "line_start": source.get("line_start"),
                "line_end": source.get("line_end"),
            }
        )
    for values in spans.values():
        values.sort(key=lambda item: (item.get("line_start") or 0, item.get("line_end") or 0))
    return dict(spans)


def method_at_line(spans: list[dict[str, Any]], line_number: int) -> dict[str, Any] | None:
    candidates = [
        span
        for span in spans
        if (span.get("line_start") or 0) <= line_number <= (span.get("line_end") or 0)
    ]
    if not candidates:
        return None
    return max(candidates, key=lambda item: item.get("line_start") or 0)


def parse_data_manager_registry() -> list[dict[str, Any]]:
    path = DATA_UPDATE_ROOT / "DataManager.cs"
    source = path.read_text(encoding="utf-8", errors="replace")
    records = []
    for match in DATA_MANAGER_ARRAY_RE.finditer(source):
        element_type = match.group("element")
        field = match.group("field")
        line = source.count("\n", 0, match.start()) + 1
        records.append(
            {
                "registry_key": f"registry:data_manager:{field}",
                "field": field,
                "element_type": element_type,
                "native_namespace": f"data:{element_type.removesuffix('Data').lower()}",
                "source": {
                    "file": relative_path(path),
                    "line": line,
                },
            }
        )
    return records


def load_data_crosscheck() -> dict[str, dict[str, Any]]:
    payload = read_json(DATA_CROSSCHECK_PATH)
    return {record["registry_field"]: record for record in payload.get("records", [])}


def data_type_source(element_type: str) -> Path | None:
    staged = DATA_UPDATE_ROOT / f"{element_type}.cs"
    if staged.is_file():
        return staged
    raw = RAW_CSHARP_ROOT / "data" / f"{element_type}.cs"
    return raw if raw.is_file() else None


def build_data_registry() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    crosscheck = load_data_crosscheck()
    registry = parse_data_manager_registry()
    records: list[dict[str, Any]] = []
    duplicate_ids: dict[str, list[int]] = {}
    row_count_by_type: Counter[str] = Counter()
    locale_mismatches = []

    for entry in registry:
        element_type = entry["element_type"]
        source_path = data_type_source(element_type)
        source = source_path.read_text(encoding="utf-8", errors="replace") if source_path else ""
        reader = parse_reader_contract(source_path)
        is_base_data = bool(re.search(rf"\bclass\s+{re.escape(element_type)}\b[^{{]*:\s*BaseData\b", source))
        table = crosscheck.get(entry["field"], {})
        locale_tables: dict[str, list[dict[str, Any]]] = {}
        for locale, locale_info in table.get("languages", {}).items():
            table_path = resolve_existing_path(locale_info.get("path"))
            rows = []
            if table_path:
                content = table_path.read_text(encoding="utf-8-sig", errors="replace")
                for row_number, line in enumerate(content.splitlines(), start=1):
                    columns = line.split("\t")
                    rows.append(
                        {
                            "row": row_number,
                            "raw_columns": columns,
                            "raw_row_sha256": sha256_bytes(line.encode("utf-8")),
                        }
                    )
            locale_tables[locale] = rows

        english_rows = locale_tables.get("English.lproj", [])
        japanese_rows = locale_tables.get("Japanese.lproj", [])
        if len(english_rows) != len(japanese_rows) and japanese_rows:
            locale_mismatches.append(
                {
                    "registry_field": entry["field"],
                    "english_rows": len(english_rows),
                    "japanese_rows": len(japanese_rows),
                }
            )
        max_rows = max((len(rows) for rows in locale_tables.values()), default=0)
        ids: list[int] = []
        row_records = []
        for index in range(max_rows):
            localized = {}
            for locale, rows in locale_tables.items():
                if index < len(rows):
                    localized[locale] = rows[index]
            english_columns = localized.get("English.lproj", {}).get("raw_columns", [])
            native_id = parse_int(english_columns[0] if english_columns else None)
            id_status = "native_id_first_column" if is_base_data and native_id is not None else "unresolved"
            if id_status == "native_id_first_column":
                ids.append(native_id)
                catalog_key = f"data:{element_type.removesuffix('Data').lower()}:{native_id}"
            else:
                catalog_key = f"data:{element_type.removesuffix('Data').lower()}:row:{index + 1}"
            decoded = decode_known_fields(
                element_type,
                english_columns,
                reader.get("reader_sequence", []),
            )
            row_records.append(
                {
                    "catalog_key": catalog_key,
                    "native_id": native_id,
                    "id_status": id_status,
                    "row_index": index + 1,
                    "locales": localized,
                    "decoded": decoded,
                }
            )
        counts = Counter(ids)
        duplicated = sorted(value for value, count in counts.items() if count > 1)
        if duplicated:
            duplicate_ids[element_type] = duplicated
        row_count_by_type[element_type] = len(row_records)
        records.append(
            {
                **entry,
                "source_type": element_type,
                "source_file": relative_path(source_path) if source_path else None,
                "source_sha256": sha256_file(source_path) if source_path else None,
                "is_base_data": is_base_data,
                "fields": parse_fields(source),
                "load_contract": reader,
                "table_stem": table.get("expected_stem"),
                "locale_source_status": {
                    locale: {
                        "path": relative_path(resolve_existing_path(info.get("path")))
                        if resolve_existing_path(info.get("path"))
                        else info.get("path"),
                        "status": info.get("status"),
                        "sha256": info.get("sha256"),
                    }
                    for locale, info in table.get("languages", {}).items()
                },
                "row_count": len(row_records),
                "rows": row_records,
            }
        )

    summary = {
        "registry_array_count": len(registry),
        "data_type_count": len(records),
        "total_row_count": sum(row_count_by_type.values()),
        "row_count_by_type": dict(sorted(row_count_by_type.items())),
        "duplicate_native_ids": duplicate_ids,
        "locale_mismatches": locale_mismatches,
        "decoded_row_statuses": dict(
            sorted(
                Counter(
                    row["decoded"]["status"]
                    for record in records
                    for row in record["rows"]
                ).items()
            )
        ),
    }
    return records, summary


def load_asset_index() -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    records = []
    by_path: dict[str, dict[str, Any]] = {}
    with ASSET_INDEX_PATH.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            relative = normalize_path(row.get("relative_path", ""))
            asset_id = f"asset:{relative}"
            record = {
                "asset_id": asset_id,
                "relative_path": relative,
                "kind": row.get("kind") or "unknown",
                "pack": row.get("pack") or "unknown",
                "original_name": row.get("original_name") or None,
                "extension": row.get("extension") or None,
                "size_bytes": parse_int(row.get("size")),
                "width": parse_int(row.get("width")),
                "height": parse_int(row.get("height")),
                "format": row.get("format") or None,
                "has_alpha": row.get("has_alpha") or None,
                "sha256": (row.get("sha256") or "").upper() or None,
                "apk_source_entry": normalize_path(row.get("apk_source_entry", "")) or None,
                "semantic_role": row.get("semantic_role") or None,
                "source_status": "native_source" if row.get("kind") == "original_pack_asset" else "derived_or_catalog",
            }
            records.append(record)
            by_path[relative] = record
    return records, by_path


def load_archive_member_names() -> set[str]:
    if not ASSET_ZIP_PATH.is_file():
        return set()
    with zipfile.ZipFile(ASSET_ZIP_PATH) as archive:
        return {
            normalize_path(name[len(ASSET_ZIP_PREFIX) :])
            for name in archive.namelist()
            if name.startswith(ASSET_ZIP_PREFIX) and not name.endswith("/")
        }


def selector_target_path(selector_path: str, target: str) -> str:
    clean_target = target.split(",", 1)[0].strip().replace("\\", "/")
    parent = posixpath.dirname(selector_path)
    return normalize_path(posixpath.join(parent, clean_target))


def selector_target_candidates(selector_path: str, target: str) -> list[tuple[str, str]]:
    """Return exact and source-backed locale-fallback target candidates."""

    exact = selector_target_path(selector_path, target)
    candidates = [(exact, "exact")]
    locale_segments = {"English.lproj", "Japanese.lproj", "ko", "zh", "zh-CN"}
    parts = exact.split("/")
    for index, part in enumerate(parts):
        if part in locale_segments:
            fallback = "/".join(parts[:index] + parts[index + 1 :])
            candidates.append((fallback, "locale_fallback"))
            break
    return candidates


def parse_selector_files(
    asset_by_path: dict[str, dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    selectors: list[dict[str, Any]] = []
    relations: list[dict[str, Any]] = []
    if not ASSET_ZIP_PATH.is_file():
        return selectors, relations
    with zipfile.ZipFile(ASSET_ZIP_PATH) as archive:
        for archive_name in archive.namelist():
            if not archive_name.startswith(ASSET_ZIP_PREFIX):
                continue
            relative = normalize_path(archive_name[len(ASSET_ZIP_PREFIX) :])
            base_name = posixpath.basename(relative).lower()
            if base_name not in {"img.inf", "seb.inf"}:
                continue
            selector_kind = base_name.removesuffix(".inf")
            text = archive.read(archive_name).decode("utf-8-sig", errors="replace")
            scope = posixpath.dirname(relative).removeprefix("01_GAME_PACKS/")
            for line_number, raw_line in enumerate(text.splitlines(), start=1):
                if not raw_line.strip():
                    continue
                columns = raw_line.split("\t")
                selector_id = parse_int(columns[0] if columns else None)
                raw_target = columns[1].strip() if len(columns) > 1 else None
                target = raw_target.split(",", 1)[0].strip() if raw_target else None
                declared_target_path = selector_target_path(relative, target) if target else None
                target_path = None
                target_resolution = None
                target_record = None
                if target:
                    for candidate_path, resolution_mode in selector_target_candidates(relative, target):
                        candidate_record = asset_by_path.get(candidate_path)
                        if candidate_record:
                            target_path = candidate_path
                            target_resolution = resolution_mode
                            target_record = candidate_record
                            break
                selector_key = f"ref:{scope}:{selector_kind}:{selector_id}" if selector_id is not None else None
                record = {
                    "selector_key": selector_key,
                    "selector_kind": selector_kind,
                    "selector_id": selector_id,
                    "resource_scope": scope,
                    "source_file": relative,
                    "source_row": line_number,
                    "raw_line": raw_line,
                    "target_filename": target,
                    "declared_target_relative_path": declared_target_path,
                    "target_relative_path": target_path,
                    "target_asset_id": target_record.get("asset_id") if target_record else None,
                    "status": "resolved" if target_record else "unresolved_target",
                    "resolution_mode": target_resolution,
                }
                selectors.append(record)
                if selector_key and target_record:
                    relations.append(
                        {
                            "relation": "selector_targets_asset",
                            "from": selector_key,
                            "to": target_record["asset_id"],
                            "source": {
                                "file": relative,
                                "line": line_number,
                            },
                        }
                    )
    return selectors, relations


def build_asset_relations(assets: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_parent_stem: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for asset in assets:
        path = asset["relative_path"]
        if not path.startswith("01_GAME_PACKS/"):
            continue
        parent = posixpath.dirname(path)
        stem = posixpath.basename(path).split(".", 1)[0]
        by_parent_stem[(parent, stem)].append(asset)
    relations = []
    for values in by_parent_stem.values():
        by_extension = defaultdict(list)
        for asset in values:
            by_extension[asset.get("extension") or ""].append(asset)
        for source_ext, target_ext in ((".opt", ".png"), (".seb", ".png"), (".seb", ".opt")):
            for source in by_extension.get(source_ext, []):
                for target in by_extension.get(target_ext, []):
                    relations.append(
                        {
                            "relation": "same_stem_companion",
                            "from": source["asset_id"],
                            "to": target["asset_id"],
                            "source": {
                                "path": source["relative_path"],
                                "path_pair": target["relative_path"],
                            },
                        }
                    )
    return relations


def load_native_floor_image_table() -> dict[str, Any]:
    """Load the source-backed Room.FLOOR_IMAGE_ID_ARRAY evidence."""

    if not DEFAULT_MAP_CONTRACT_PATH.is_file():
        raise ValueError(f"missing native floor-image table contract: {DEFAULT_MAP_CONTRACT_PATH}")
    contract = read_json(DEFAULT_MAP_CONTRACT_PATH)
    table = contract.get("native_static_arrays", {}).get("floor_image_id_array")
    if not isinstance(table, dict) or not isinstance(table.get("values"), list):
        raise ValueError("native MapChip contract has no FLOOR_IMAGE_ID_ARRAY values")
    return {
        "field": "Room.FLOOR_IMAGE_ID_ARRAY",
        "element_type": table.get("element_type"),
        "length": table.get("length", len(table["values"])),
        "values": table["values"],
        "metadata_offset": table.get("metadata_offset"),
        "metadata_hash": table.get("metadata_hash"),
        "source_contract": relative_path(DEFAULT_MAP_CONTRACT_PATH),
        "source_status": "verified_native_static_array_contract",
    }


DATA_SELECTOR_FIELDS = {
    ("FurnitureData", "seb_"): ("chip", "seb"),
    ("FurnitureData", "subSeb_"): ("chip", "seb"),
    ("FurnitureData", "img_"): ("chip", "img"),
    ("RoomData", "floorImgId_"): ("chip", "img"),
    ("RoomData", "wallImgId_"): ("chip", "img"),
    ("RoomData", "doorImgId_"): ("chip", "img"),
    ("StaffData", "img_"): ("human", "img"),
}

# HelperData.img_ is consumed as a StaffData ID by Staff.CreateStaff.  It is
# not a human IMAGE_SELECTOR_ID, even when the numeric value happens to be in
# the range of the human selector table.
DATA_ID_REFERENCE_FIELDS = {
    ("HelperData", "img_"): ("StaffData", "STAFF_DATA_ID"),
}


def build_data_selector_relations(
    data_registry: list[dict[str, Any]],
    selectors: list[dict[str, Any]],
    floor_image_table: dict[str, Any],
) -> list[dict[str, Any]]:
    selector_by_key = {
        item["selector_key"]: item
        for item in selectors
        if item.get("selector_key")
    }
    data_row_by_type_and_id = {
        (data_type["source_type"], row.get("native_id")): row["catalog_key"]
        for data_type in data_registry
        for row in data_type["rows"]
        if row.get("native_id") is not None
    }
    relations = []
    for data_type in data_registry:
        source_type = data_type["source_type"]
        for row in data_type["rows"]:
            decoded = row.get("decoded", {})
            fields = decoded.get("fields") if decoded.get("status") == "verified_reader_order" else None
            if not fields:
                continue
            for (mapped_type, field_name), (target_type, target_namespace) in DATA_ID_REFERENCE_FIELDS.items():
                if mapped_type != source_type or field_name not in fields:
                    continue
                native_value = fields[field_name]
                from_node = row["catalog_key"]
                if not isinstance(native_value, int):
                    relations.append(
                        {
                            "relation": "data_field_data_id_unresolved",
                            "from": from_node,
                            "field": field_name,
                            "native_value": native_value,
                            "target_type": target_type,
                            "target_namespace": target_namespace,
                            "to": None,
                            "status": "non_scalar_value",
                        }
                    )
                    continue
                if native_value < 0:
                    relations.append(
                        {
                            "relation": "data_field_data_id_sentinel",
                            "from": from_node,
                            "field": field_name,
                            "native_value": native_value,
                            "target_type": target_type,
                            "target_namespace": target_namespace,
                            "to": None,
                            "status": "absent_by_sentinel",
                        }
                    )
                    continue
                target_node = data_row_by_type_and_id.get((target_type, native_value))
                relations.append(
                    {
                        "relation": "data_field_references_data_id",
                        "from": from_node,
                        "field": field_name,
                        "native_value": native_value,
                        "target_type": target_type,
                        "target_namespace": target_namespace,
                        "to": target_node,
                        "status": "resolved" if target_node else "data_id_target_unresolved",
                        "semantics": "HelperData.img_ is a STAFF_DATA_ID consumed by Staff.CreateStaff; it is not a human IMAGE_SELECTOR_ID.",
                    }
                )
            for (mapped_type, field_name), (scope, selector_kind) in DATA_SELECTOR_FIELDS.items():
                if mapped_type != source_type or field_name not in fields:
                    continue
                native_value = fields[field_name]
                from_node = row["catalog_key"]
                if not isinstance(native_value, int):
                    relations.append(
                        {
                            "relation": "data_field_selector_unresolved",
                            "from": from_node,
                            "field": field_name,
                            "native_value": native_value,
                            "to": None,
                            "status": "non_scalar_value",
                        }
                    )
                    continue
                if native_value < 0:
                    relations.append(
                        {
                            "relation": "data_field_selector_sentinel",
                            "from": from_node,
                            "field": field_name,
                            "native_value": native_value,
                            "to": None,
                            "status": "absent_by_sentinel",
                        }
                    )
                    continue
                if source_type == "RoomData" and field_name == "floorImgId_":
                    table_values = floor_image_table["values"]
                    if native_value >= len(table_values):
                        relations.append(
                            {
                                "relation": "data_field_indirect_selector_unresolved",
                                "from": from_node,
                                "field": field_name,
                                "native_value": native_value,
                                "indirection_table": floor_image_table["field"],
                                "table_index": native_value,
                                "to": None,
                                "status": "indirection_table_index_unresolved",
                            }
                        )
                        continue
                    native_selector_id = table_values[native_value]
                    selector_key = f"ref:{scope}:{selector_kind}:{native_selector_id}"
                    selector = selector_by_key.get(selector_key)
                    relations.append(
                        {
                            "relation": "data_field_indirect_selector",
                            "from": from_node,
                            "field": field_name,
                            "native_value": native_value,
                            "indirection_table": floor_image_table["field"],
                            "table_index": native_value,
                            "native_selector_id": native_selector_id,
                            "to": selector_key,
                            "target_asset_id": selector.get("target_asset_id") if selector else None,
                            "status": "resolved" if selector else "selector_scope_unresolved",
                            "semantics": "RoomData.floorImgId_ is a native floor-table index, not a direct resource selector id.",
                        }
                    )
                    continue
                selector_key = f"ref:{scope}:{selector_kind}:{native_value}"
                selector = selector_by_key.get(selector_key)
                relations.append(
                    {
                        "relation": "data_field_references_selector",
                        "from": from_node,
                        "field": field_name,
                        "native_value": native_value,
                        "to": selector_key,
                        "target_asset_id": selector.get("target_asset_id") if selector else None,
                        "status": "resolved" if selector else "selector_scope_unresolved",
                    }
                )
    return relations


def build_consumer_graph(data_registry: list[dict[str, Any]]) -> dict[str, Any]:
    method_spans = load_method_spans()
    registry_fields = {
        record["field"]: record["registry_key"]
        for record in parse_data_manager_registry()
    }
    token_targets = {
        **{field: f"field:{field}" for field in TRACE_DATA_FIELDS},
        **{field: registry_key for field, registry_key in registry_fields.items()},
    }
    token_pattern = re.compile(
        r"\b(?:" + "|".join(sorted((re.escape(token) for token in token_targets), key=len, reverse=True)) + r")\b"
    )
    edge_counts: Counter[tuple[str, str, str]] = Counter()
    edge_samples: dict[tuple[str, str, str], dict[str, Any]] = {}
    file_count = 0
    occurrence_count = 0
    for source_path in RAW_CSHARP_ROOT.rglob("*.cs"):
        source_file = relative_path(source_path)
        spans = method_spans.get(source_file, [])
        lines = source_path.read_text(encoding="utf-8", errors="replace").splitlines()
        file_count += 1
        for line_number, line in enumerate(lines, start=1):
            for token_match in token_pattern.finditer(line):
                token = token_match.group(0)
                from_node = token_targets[token]
                method = method_at_line(spans, line_number)
                if method:
                    consumer = f"consumer:{method.get('symbol') or method.get('owner') + '.' + method.get('name')}"
                    method_name = method.get("symbol")
                else:
                    consumer = f"consumer:file:{source_file}"
                    method_name = None
                relation = "registry_field_read" if token in registry_fields else "field_consumer_read"
                key = (from_node, consumer, relation)
                edge_counts[key] += 1
                edge_samples.setdefault(
                    key,
                    {
                        "relation": relation,
                        "from": from_node,
                        "to": consumer,
                        "token": token,
                        "source": {
                            "file": source_file,
                            "line": line_number,
                            "method": method_name,
                        },
                    },
                )
                occurrence_count += 1
    edges = []
    for key, count in sorted(edge_counts.items()):
        edge = dict(edge_samples[key])
        edge["occurrence_count"] = count
        edges.append(edge)

    lifecycle_edges = []
    for edge in edges:
        method_name = edge.get("source", {}).get("method") or ""
        short_name = method_name.rsplit(".", 1)[-1]
        if short_name in LIFECYCLE_METHOD_NAMES:
            lifecycle_edges.append(
                {
                    "relation": "used_during_lifecycle",
                    "from": edge["from"],
                    "to": edge["to"],
                    "phase": short_name,
                    "source": edge["source"],
                    "evidence_occurrences": edge["occurrence_count"],
                }
            )
    return {
        "scan_root": relative_path(RAW_CSHARP_ROOT),
        "source_file_count": file_count,
        "field_occurrence_count": occurrence_count,
        "consumer_edges": edges,
        "lifecycle_edges": lifecycle_edges,
        "trace_tokens": sorted(token_targets),
        "data_registry_count": len(data_registry),
    }


def build_payload() -> dict[str, Any]:
    data_registry, data_summary = build_data_registry()
    assets, asset_by_path = load_asset_index()
    archive_members = load_archive_member_names()
    for asset in assets:
        asset["archive_member_present"] = asset["relative_path"] in archive_members
    selectors, selector_relations = parse_selector_files(asset_by_path)
    floor_image_table = load_native_floor_image_table()
    data_selector_relations = build_data_selector_relations(data_registry, selectors, floor_image_table)
    asset_relations = build_asset_relations(assets)
    graph = build_consumer_graph(data_registry)

    duplicate_asset_ids = [asset_id for asset_id, count in Counter(item["asset_id"] for item in assets).items() if count > 1]
    duplicate_selector_keys = [
        selector_key
        for selector_key, count in Counter(
            item["selector_key"] for item in selectors if item.get("selector_key")
        ).items()
        if count > 1
    ]
    unresolved_selectors = [item for item in selectors if item["status"] != "resolved"]
    source_archive = {
        "asset_zip": relative_path(ASSET_ZIP_PATH),
        "asset_zip_sha256": None,
    }
    existing_binary_inventory = ROOT / "knowledge/fixtures/accepted/asset_binary_inventory.json"
    if existing_binary_inventory.is_file():
        inventory = read_json(existing_binary_inventory)
        source_archive["asset_zip_sha256"] = inventory.get("archives", {}).get("asset_zip", {}).get("sha256")

    payload = {
        "schema_version": "social-dev-native-content-registry-v1",
        "status": "pass" if not duplicate_asset_ids and not duplicate_selector_keys else "blocked_duplicate_identity",
        "semantic_status": "evidence_registry_not_runtime_approved",
        "policy": {
            "native_numeric_ids_are_preserved": True,
            "numeric_ids_are_namespaced_by_data_or_resource_scope": True,
            "raw_rows_and_raw_selector_lines_are_retained": True,
            "unknown_and_minus_one_values_are_not_inferred": True,
            "source_roots_are_read_only": True,
            "decompiled_csharp_is_evidence_only": True,
        },
        "source_archive": source_archive,
        "data_manager_registry": parse_data_manager_registry(),
        "data_registry_summary": data_summary,
        "data_types": data_registry,
        "native_indirection_tables": {
            floor_image_table["field"]: floor_image_table,
        },
        "assets": assets,
        "selectors": selectors,
        "data_selector_relations": data_selector_relations,
        "relations": data_selector_relations + selector_relations + asset_relations,
        "consumer_graph": graph,
        "identity_validation": {
            "duplicate_asset_ids": duplicate_asset_ids,
            "duplicate_selector_keys": duplicate_selector_keys,
            "unresolved_selector_count": len(unresolved_selectors),
            "unresolved_selector_samples": unresolved_selectors[:50],
            "missing_archive_member_count": sum(1 for asset in assets if not asset["archive_member_present"]),
        },
        "counts": {
            "data_manager_arrays": len(payload_registry := parse_data_manager_registry()),
            "data_types": len(data_registry),
            "data_rows": data_summary["total_row_count"],
            "assets": len(assets),
            "selectors": len(selectors),
            "data_selector_relations": len(data_selector_relations),
            "selector_asset_relations": len(selector_relations),
            "asset_companion_relations": len(asset_relations),
            "consumer_edges": len(graph["consumer_edges"]),
            "lifecycle_edges": len(graph["lifecycle_edges"]),
        },
    }
    # Keep the assignment explicit so the registry remains easy to inspect in a debugger.
    payload["data_manager_registry"] = payload_registry
    serialized = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    payload["content_hash"] = sha256_bytes(serialized.encode("utf-8"))
    return payload


def write_outputs(payload: dict[str, Any]) -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    data_record_nodes = [
        row["catalog_key"]
        for data_type in payload["data_types"]
        for row in data_type["rows"]
    ]
    selector_nodes = [item["selector_key"] for item in payload["selectors"] if item.get("selector_key")]
    asset_nodes = [item["asset_id"] for item in payload["assets"]]
    consumer_nodes = sorted(
        {
            edge["to"]
            for edge in payload["consumer_graph"]["consumer_edges"]
            if edge.get("to")
        }
    )
    connection_graph = {
        "schema_version": "social-dev-native-content-connection-graph-v1",
        "status": payload["status"],
        "semantic_status": payload["semantic_status"],
        "registry_content_hash": payload["content_hash"],
        "nodes": {
            "data_registry": [item["registry_key"] for item in payload["data_manager_registry"]],
            "data_records": data_record_nodes,
            "selectors": selector_nodes,
            "assets": asset_nodes,
            "consumers": consumer_nodes,
        },
        "edges": {
            "data_selector": payload["data_selector_relations"],
            "selector_asset_and_companion": payload["relations"],
            "consumer": payload["consumer_graph"]["consumer_edges"],
            "lifecycle": payload["consumer_graph"]["lifecycle_edges"],
        },
        "lifecycle_phases": [
            "load",
            "bootstrap",
            "resolve",
            "draw",
            "update",
            "persist",
        ],
        "query_policy": "Every unresolved edge remains explicit; absence of a consumer edge is not silently treated as unused until the source scan is complete.",
    }
    graph_serialized = json.dumps(connection_graph, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    connection_graph["content_hash"] = sha256_bytes(graph_serialized.encode("utf-8"))
    GRAPH_OUTPUT_PATH.write_text(
        json.dumps(connection_graph, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    contract = {
        "schema_version": "social-dev-native-content-registry-contract-v1",
        "package": "social-dev-native-content-registry",
        "status": payload["status"],
        "semantic_status": payload["semantic_status"],
        "registry_path": relative_path(OUTPUT_PATH),
        "registry_content_hash": payload["content_hash"],
        "counts": payload["counts"],
        "identity_validation": payload["identity_validation"],
        "native_namespaces": [
            "data:{DataManager element type}:{native id}",
            "ref:{resource scope}:{img|seb}:{selector id}",
            "asset:{archive-relative path}",
            "object:{scene}:{native object id}@{x}:{y}",
        ],
        "lifecycle_policy": {
            "load": "DataManager.Load and per-type Load(StringArrayStream)",
            "bootstrap": "AppData.NewGame and Room initialization methods",
            "resolve": "ResourceManager/ResChip/ResHuman selector consumers",
            "draw": "MapChip, ObjChip, Staff and UI Draw consumers",
            "persist": "Canonical IDs and state only; presentation binaries excluded",
        },
        "source_boundaries": {
            "data": relative_path(DATA_UPDATE_ROOT),
            "csharp_evidence": relative_path(RAW_CSHARP_ROOT),
            "asset_index": relative_path(ASSET_INDEX_PATH),
            "asset_archive": relative_path(ASSET_ZIP_PATH),
        },
        "open_items": [
            "Semantic field names outside the closed selector/scene slices remain evidence-backed and may be unknown.",
            "The registry records selector targets; runtime promotion still requires per-consumer composition validation.",
            "RoomData.floorImgId_ is resolved through Room.FLOOR_IMAGE_ID_ARRAY; MapChip topology remains separate and is selected by Room.floor_.",
        ],
    }
    CONTRACT_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONTRACT_PATH.write_text(json.dumps(contract, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    graph_contract = {
        "schema_version": "social-dev-native-content-connection-contract-v1",
        "package": "social-dev-native-content-connection-graph",
        "status": connection_graph["status"],
        "semantic_status": connection_graph["semantic_status"],
        "graph_path": relative_path(GRAPH_OUTPUT_PATH),
        "graph_content_hash": connection_graph["content_hash"],
        "registry_content_hash": payload["content_hash"],
        "node_counts": {key: len(value) for key, value in connection_graph["nodes"].items()},
        "edge_counts": {key: len(value) for key, value in connection_graph["edges"].items()},
        "lifecycle_phases": connection_graph["lifecycle_phases"],
        "query_examples": [
            "data:furniture:3 → chip selector refs → desk/chair source assets → ObjChip.Draw",
            "data:room:17 → floor/wall/door selector refs → MapChip/ObjChip consumers",
            "data:staff:0 → human image selector → Staff.Draw",
        ],
        "open_items": [
            "Some decompiler method bodies remain evidence-only; ambiguous field semantics stay marked unknown.",
            "Runtime promotion still requires composition/frame validation for each asset family.",
        ],
    }
    GRAPH_CONTRACT_PATH.write_text(
        json.dumps(graph_contract, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    counts = payload["counts"]
    lines = [
        "# Social Dev native content registry",
        "",
        "This registry preserves the game's separate DataManager IDs, resource selector IDs, source/derived asset identities, and C# evidence consumer edges.",
        "",
        "The decompiled C# and source archive are read-only evidence. This package is not runtime-approved; it is the identity and connection layer that later room/runtime catalogs consume.",
        "",
        "## Counts",
        "",
        "| Item | Count |",
        "|---|---:|",
    ]
    for key, value in counts.items():
        lines.append(f"| `{key}` | {value} |")
    lines.extend(
        [
            "",
            "## Identity validation",
            "",
            f"- Registry status: `{payload['status']}`",
            f"- Duplicate asset IDs: `{len(payload['identity_validation']['duplicate_asset_ids'])}`",
            f"- Duplicate selector keys: `{len(payload['identity_validation']['duplicate_selector_keys'])}`",
            f"- Unresolved selector targets: `{payload['identity_validation']['unresolved_selector_count']}`",
            f"- Missing archive members: `{payload['identity_validation']['missing_archive_member_count']}`",
            "",
            "## Native identity policy",
            "",
            "1. Numeric DataManager IDs remain scoped to their data type.",
            "2. `seb_`, `subSeb_`, and `img_` remain resource selector references, not filenames.",
            "3. Source/derived assets retain archive-relative paths, hashes, and provenance.",
            "4. A runtime instance ID is separate from its source FurnitureData or selector ID.",
            "5. Unknown values and `-1` sentinels are retained rather than guessed.",
            "",
            "## Trace chain",
            "",
            "`data tables → StringArrayStream readers → DataManager arrays → native indirection tables (when applicable) → selector fields → resource selector files → source/derived assets → C# consumers → lifecycle phase`",
            "",
            f"Content hash: `{payload['content_hash']}`",
            "",
        ]
    )
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")

    graph_lines = [
        "# Social Dev native content connection graph",
        "",
        "This graph connects native data records, resource selectors, source/derived assets, C# consumers, and lifecycle phases.",
        "",
        "It intentionally keeps unresolved or decompiler-ambiguous edges visible instead of converting them into guessed semantics.",
        "",
        "## Node counts",
        "",
        "| Node type | Count |",
        "|---|---:|",
    ]
    for key, value in graph_contract["node_counts"].items():
        graph_lines.append(f"| `{key}` | {value} |")
    graph_lines.extend(
        [
            "",
            "## Edge counts",
            "",
            "| Edge type | Count |",
            "|---|---:|",
        ]
    )
    for key, value in graph_contract["edge_counts"].items():
        graph_lines.append(f"| `{key}` | {value} |")
    graph_lines.extend(
        [
            "",
            "## Query path",
            "",
            "`data record → native field value → native indirection table (when applicable) → selector reference → source/derived asset → consumer method → lifecycle phase`",
            "",
            f"Registry hash: `{payload['content_hash']}`",
            f"Graph hash: `{connection_graph['content_hash']}`",
            "",
        ]
    )
    GRAPH_REPORT_PATH.write_text("\n".join(graph_lines), encoding="utf-8")


def main() -> int:
    payload = build_payload()
    write_outputs(payload)
    print(json.dumps({"status": payload["status"], "counts": payload["counts"], "content_hash": payload["content_hash"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
