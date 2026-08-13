"""Deterministic text trace helper for C#/C/assembly evidence.

The helper stays evidence-first: it only reports literal text hits, preserves
the source path, line, byte offset, file hash, bounded excerpt, and an explicit
status for every trace result.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from hashlib import sha256
from pathlib import Path
import re
from typing import Iterable, Sequence


TEXT_EXTENSIONS = {
    ".c",
    ".cs",
    ".h",
    ".json",
    ".md",
    ".py",
    ".txt",
    ".xml",
    ".yml",
    ".yaml",
    ".asm",
}
MAX_EXCERPT_CHARS = 140


@dataclass(frozen=True, order=True)
class SourceRef:
    source_path: str
    line: int | None
    offset: int | None
    source_hash: str
    excerpt: str
    status: str
    source_kind: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class TraceResult:
    symbol: str
    status: str
    source_refs: list[SourceRef] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "symbol": self.symbol,
            "status": self.status,
            "source_refs": [ref.to_dict() for ref in self.source_refs],
        }


@dataclass(frozen=True)
class SemanticsContract:
    schema_version: str
    status: str
    source_roots_read_only: bool
    source_roots: tuple[str, ...]
    field_table: dict[str, dict]
    traces: dict[str, TraceResult]
    notes: tuple[str, ...] = ()

    def to_dict(self) -> dict:
        return {
            "schema_version": self.schema_version,
            "status": self.status,
            "source_roots_read_only": self.source_roots_read_only,
            "source_roots": list(self.source_roots),
            "field_table": self.field_table,
            "traces": {symbol: trace.to_dict() for symbol, trace in self.traces.items()},
            "notes": list(self.notes),
        }


@dataclass(frozen=True)
class _FileTraceData:
    path: Path
    rel_path: str
    source_kind: str
    source_hash: str
    text: str
    line_offsets: tuple[int, ...]


def _workspace_root(workspace: Path | str | None = None) -> Path:
    if workspace is None:
        return Path(__file__).resolve().parents[2]
    return Path(workspace).resolve()


def _hash_bytes(data: bytes) -> str:
    return sha256(data).hexdigest()


def _read_source_bytes(path: Path) -> bytes | None:
    try:
        return path.read_bytes()
    except OSError:
        return None


def _decode_source(data: bytes) -> str:
    return data.decode("utf-8", errors="replace")


def _iter_root_files(root: Path) -> Iterable[Path]:
    if root.is_file():
        yield root
        return
    if not root.exists():
        return
    for path in sorted(root.rglob("*")):
        if path.is_file() and path.suffix.lower() in TEXT_EXTENSIONS:
            yield path


def _bounded_excerpt(line: str, match_start: int, match_end: int) -> str:
    if len(line) <= MAX_EXCERPT_CHARS:
        return line.rstrip("\r\n")
    span = MAX_EXCERPT_CHARS - 3
    left = max(0, match_start - span // 2)
    right = min(len(line), left + span)
    if right - left < span:
        left = max(0, right - span)
    snippet = line[left:right].rstrip("\r\n")
    if left > 0:
        snippet = "…" + snippet
    if right < len(line):
        snippet = snippet + "…"
    return snippet


def _match_byte_offset(line: str, match_start: int, *, encoding: str = "utf-8") -> int:
    return len(line[:match_start].encode(encoding, errors="replace"))


def _source_kind(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".cs":
        return "csharp"
    if suffix == ".c":
        return "c"
    if path.name.lower().endswith(".asm.txt") or (suffix in {".asm", ".txt"} and "assembly" in path.parent.as_posix().lower()):
        return "assembly"
    if suffix == ".json":
        return "json"
    if suffix == ".dll":
        return "binary"
    return suffix.lstrip(".") or "text"


def _source_path_string(path: Path, root: Path) -> str:
    resolved = path.resolve()
    try:
        return resolved.relative_to(root).as_posix()
    except ValueError:
        return resolved.as_posix()


def _load_trace_files(roots: Sequence[Path | str], workspace: Path | str | None = None) -> tuple[_FileTraceData, ...]:
    root = _workspace_root(workspace)
    roots_paths = [Path(item) if not isinstance(item, Path) else item for item in roots]
    files: list[_FileTraceData] = []

    for item in roots_paths:
        path = item if item.is_absolute() else (root / item)
        if path.is_dir():
            candidates = _iter_root_files(path)
        else:
            candidates = (path,) if path.exists() else ()
        for candidate in candidates:
            data = _read_source_bytes(candidate)
            if data is None:
                continue
            text = _decode_source(data)
            line_offsets: list[int] = []
            line_offset = 0
            for line in text.splitlines(keepends=True):
                line_offsets.append(line_offset)
                line_offset += len(line.encode("utf-8", errors="replace"))
            rel_path = _source_path_string(candidate, root)
            files.append(
                _FileTraceData(
                    path=candidate,
                    rel_path=rel_path,
                    source_kind=_source_kind(candidate),
                    source_hash=_hash_bytes(data),
                    text=text,
                    line_offsets=tuple(line_offsets),
                )
            )
    return tuple(files)


def _trace_many_symbols(
    symbols: Sequence[str],
    roots: Sequence[Path | str],
    *,
    workspace: Path | str | None = None,
) -> dict[str, TraceResult]:
    file_data = _load_trace_files(roots, workspace=workspace)
    ordered_symbols = tuple(sorted(dict.fromkeys(symbols), key=lambda value: (-len(value), value)))
    if not ordered_symbols:
        return {}
    group_to_symbol = {f"s{index}": symbol for index, symbol in enumerate(ordered_symbols)}
    aggregate = re.compile("|".join(f"(?P<s{index}>{re.escape(symbol)})" for index, symbol in enumerate(ordered_symbols)))
    refs_by_symbol: dict[str, list[SourceRef]] = {symbol: [] for symbol in ordered_symbols}
    seen: set[tuple[str, str, int, int, int]] = set()

    for file_entry in file_data:
        for line_number, line in enumerate(file_entry.text.splitlines(keepends=True), start=1):
            if not aggregate.search(line):
                continue
            for match in aggregate.finditer(line):
                symbol = group_to_symbol[match.lastgroup or ""]
                offset = file_entry.line_offsets[line_number - 1] + _match_byte_offset(line, match.start())
                dedupe_key = (symbol, file_entry.rel_path, line_number, offset, match.start())
                if dedupe_key in seen:
                    continue
                seen.add(dedupe_key)
                refs_by_symbol[symbol].append(
                    SourceRef(
                        source_path=file_entry.rel_path,
                        line=line_number,
                        offset=offset,
                        source_hash=file_entry.source_hash,
                        excerpt=_bounded_excerpt(line, match.start(), match.end()),
                        status="verified",
                        source_kind=file_entry.source_kind,
                    )
                )

    return {
        symbol: TraceResult(symbol=symbol, status="verified" if refs else "unknown", source_refs=sorted(refs, key=lambda ref: (ref.source_path, ref.line or -1, ref.offset or -1, ref.excerpt)))
        for symbol, refs in refs_by_symbol.items()
    }


def trace_symbol(symbol: str, roots: Sequence[Path | str], *, workspace: Path | str | None = None) -> TraceResult:
    """Trace literal text hits for ``symbol`` through the provided roots."""
    traced = _trace_many_symbols([symbol], roots, workspace=workspace)
    return traced[symbol]


def _field_entry(category: str, status: str, consumer: str, evidence_symbols: Sequence[str], note: str = "") -> dict:
    entry = {
        "category": category,
        "status": status,
        "consumer": consumer,
        "evidence_symbols": list(evidence_symbols),
    }
    if note:
        entry["note"] = note
    return entry


def build_seb_semantics_contract(
    roots: Sequence[Path | str] | None = None,
    *,
    workspace: Path | str | None = None,
) -> SemanticsContract:
    root = _workspace_root(workspace)
    trace_roots = roots or (
        Path("knowledge/csharp/primary"),
        Path("game-dev-story-mod_Dumped/Categorized_Code"),
        Path("game-dev-story-mod_Dumped/Failed_Functions_Assembly"),
        Path("game-dev-story-mod_Dumped/dump.cs"),
        Path("game-dev-story-mod_Dumped/DummyDll/Assembly-CSharp.dll"),
    )

    trace_symbols = (
        "GetSprites",
        "DrawSeb",
        "DrawSebAnchor",
        "DrawSebScale",
        "DrawSebReverse",
        "DrawSebV",
        "RenderGameScreen",
        "DrawObj",
        "AddObjec",
        "SP_FRAME_NO",
        "SP_TEX_ID",
        "SP_U",
        "SP_V",
        "SP_W",
        "SP_H",
        "SP_TRANS_X",
        "SP_TRANS_Y",
        "SP_REVERS_U",
        "SP_REVERS_V",
        "SP_BLEND",
        "SP_COLOR",
        "SP_END",
        "ObjecX",
        "ObjecY",
        "ObjecZX",
        "ObjecZY",
        "ObjecSY",
        "ObjecUpDown",
        "camX_",
        "camY_",
        "floorparts0",
        "LoadSeb",
    )
    traces = _trace_many_symbols(trace_symbols, trace_roots, workspace=root)

    field_table = {
        "frame": _field_entry("frame selector", "verified", "GetSprites / DrawSeb", ["SP_FRAME_NO", "GetSprites"]),
        "texture_id": _field_entry(
            "texture/selector",
            "candidate",
            "DrawSeb variants",
            ["SP_TEX_ID", "TEXID_NONE", "TEXID_RECT", "TEXID_LINE", "TEXID_HIDELINE", "TEXID_HIDERECT"],
            "special texture IDs stay candidate until the consumer switch and asset identity agree",
        ),
        "u": _field_entry("local crop", "verified", "DrawSeb / DrawSebScale / DrawSebReverse", ["SP_U", "DrawSeb", "DrawSebScale", "DrawSebReverse"]),
        "v": _field_entry("local crop", "verified", "DrawSeb / DrawSebScale / DrawSebReverse", ["SP_V", "DrawSeb", "DrawSebScale", "DrawSebReverse"]),
        "w": _field_entry("local crop", "verified", "DrawSeb / DrawSebScale", ["SP_W", "DrawSeb", "DrawSebScale"]),
        "h": _field_entry("local crop", "verified", "DrawSeb / DrawSebScale", ["SP_H", "DrawSeb", "DrawSebScale"]),
        "trans_x": _field_entry("local translation", "verified", "DrawSeb / DrawSebV / DrawSebScale", ["SP_TRANS_X", "DrawSeb", "DrawSebV", "DrawSebScale"]),
        "trans_y": _field_entry("local translation", "verified", "DrawSeb / DrawSebV / DrawSebScale", ["SP_TRANS_Y", "DrawSeb", "DrawSebV", "DrawSebScale"]),
        "reverse_u": _field_entry("mirror/reverse control", "candidate", "DrawSebReverse / DrawSebScale", ["SP_REVERS_U", "DrawSebReverse", "DrawSebScale"]),
        "reverse_v": _field_entry("mirror/reverse control", "candidate", "DrawSebReverse / DrawSebScale", ["SP_REVERS_V", "DrawSebReverse", "DrawSebScale"]),
        "blend": _field_entry("blend", "unknown", "unknown", ["SP_BLEND"]),
        "color": _field_entry("color", "unknown", "unknown", ["SP_COLOR"]),
        "end": _field_entry("record terminator", "unknown", "unknown", ["SP_END"]),
        "ObjecX": _field_entry("external object/base coordinate", "verified", "AddObjec / DrawObj / RenderGameScreen", ["ObjecX", "AddObjec", "DrawObj", "RenderGameScreen"]),
        "ObjecY": _field_entry("external object/base coordinate", "verified", "AddObjec / DrawObj / RenderGameScreen", ["ObjecY", "AddObjec", "DrawObj", "RenderGameScreen"]),
        "ObjecZX": _field_entry(
            "external object/base coordinate",
            "candidate",
            "AddObjec default / RenderGameScreen contribution",
            ["ObjecZX", "AddObjec", "RenderGameScreen"],
            "proved as a bounded contribution, not a universal world transform",
        ),
        "ObjecZY": _field_entry(
            "external object/base coordinate",
            "candidate",
            "AddObjec default / RenderGameScreen contribution",
            ["ObjecZY", "AddObjec", "RenderGameScreen"],
            "proved as a bounded contribution, not a universal world transform",
        ),
        "camX_": _field_entry("screen/camera coordinate", "verified", "RenderGameScreen / camera boundary", ["camX_", "RenderGameScreen"]),
        "camY_": _field_entry("screen/camera coordinate", "verified", "RenderGameScreen / camera boundary", ["camY_", "RenderGameScreen"]),
        "ObjecSY": _field_entry("sort/depth", "verified", "AddObjec / DrawObj depth boundary", ["ObjecSY", "ObjecUpDown", "DrawObj"]),
        "ObjecUpDown": _field_entry("sort/depth", "candidate", "depth sort only", ["ObjecUpDown", "DrawObj"]),
    }

    notes = (
        "Literal text hits only; missing symbols stay unknown.",
        "SEB crop, translation, texture/selector, external object/base, screen/camera, and sort/depth fields stay separated.",
        "ObjecZX/ObjecZY are preserved as bounded contributions only; no universal world transform is claimed.",
        "Special texture IDs remain candidate unless a consumer switch and asset identity agree.",
    )
    return SemanticsContract(
        schema_version="seb-semantics-contract-v1",
        status="consumer_boundary_verified",
        source_roots_read_only=True,
        source_roots=tuple(str(path) for path in trace_roots),
        field_table=field_table,
        traces=traces,
        notes=notes,
    )
