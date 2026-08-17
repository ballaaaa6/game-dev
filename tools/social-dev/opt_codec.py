"""Evidence-bounded reader and reconstructor for Social Dev OPT payloads.

The supported structure is established by exact source-to-derived pixel
matches across the supplied asset pack:

    header: 4 unsigned bytes (cell width, cell height, columns, rows)
    cell: 1 unsigned byte piece count, followed by that many pieces
    piece: seven big-endian shorts (14 bytes)

The first cell byte was previously treated as a record prefix.  The complete
pack shows that it is a per-cell piece count: a value of ``2`` is followed by
two 14-byte crop descriptors, and a value of ``0`` is a valid empty cell.  A
piece's signed source reference remains opaque; the remaining fields are
supported as offsets and source rectangles.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from io import BytesIO
from typing import Any

from PIL import Image


OPT_HEADER_SIZE = 4
OPT_PIECE_SIZE = 14
OPT_RECORD_SIZE = 1 + OPT_PIECE_SIZE


def sha256_bytes(value: bytes) -> str:
    return sha256(value).hexdigest()


def _short(raw: bytes, offset: int) -> int:
    return int.from_bytes(raw[offset : offset + 2], "big", signed=True)


def _ushort(raw: bytes, offset: int) -> int:
    return int.from_bytes(raw[offset : offset + 2], "big", signed=False)


@dataclass(frozen=True)
class OptHeader:
    cell_width: int
    cell_height: int
    columns: int
    rows: int

    @property
    def logical_width(self) -> int:
        return self.cell_width * self.columns

    @property
    def logical_height(self) -> int:
        return self.cell_height * self.rows

    def to_dict(self) -> dict[str, int]:
        return {
            "cell_width": self.cell_width,
            "cell_height": self.cell_height,
            "columns": self.columns,
            "rows": self.rows,
            "logical_width": self.logical_width,
            "logical_height": self.logical_height,
        }


@dataclass(frozen=True)
class OptRecord:
    index: int
    record_prefix: int
    source_reference: int
    offset_x: int
    offset_y: int
    source_x: int
    source_y: int
    width: int
    height: int
    part_index: int = 0
    part_count: int = 1

    def destination(self, header: OptHeader) -> tuple[int, int]:
        column = self.index % header.columns
        row = self.index // header.columns
        return (
            column * header.cell_width + self.offset_x,
            row * header.cell_height + self.offset_y,
        )

    def to_dict(self, header: OptHeader) -> dict[str, int]:
        destination_x, destination_y = self.destination(header)
        return {
            "index": self.index,
            "record_prefix": self.record_prefix,
            "source_reference": self.source_reference,
            "offset_x": self.offset_x,
            "offset_y": self.offset_y,
            "source_x": self.source_x,
            "source_y": self.source_y,
            "width": self.width,
            "height": self.height,
            "part_index": self.part_index,
            "part_count": self.part_count,
            "cell_column": self.index % header.columns,
            "cell_row": self.index // header.columns,
            "destination_x": destination_x,
            "destination_y": destination_y,
        }


@dataclass(frozen=True)
class OptCell:
    index: int
    piece_count: int
    records: tuple[OptRecord, ...]

    def to_dict(self, header: OptHeader) -> dict[str, Any]:
        return {
            "index": self.index,
            "piece_count": self.piece_count,
            "records": [record.to_dict(header) for record in self.records],
        }


@dataclass(frozen=True)
class OptPayload:
    source_ref: str
    size_bytes: int
    sha256: str
    header: OptHeader | None
    records: tuple[OptRecord, ...]
    cells: tuple[OptCell, ...]
    partial_tail_bytes: int
    expected_record_count: int | None
    status: str
    errors: tuple[str, ...]

    @property
    def logical_size(self) -> tuple[int, int] | None:
        if self.header is None:
            return None
        return self.header.logical_width, self.header.logical_height

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_ref": self.source_ref,
            "size_bytes": self.size_bytes,
            "sha256": self.sha256,
            "header": self.header.to_dict() if self.header else None,
            "expected_record_count": self.expected_record_count,
            "partial_tail_bytes": self.partial_tail_bytes,
            "status": self.status,
            "errors": list(self.errors),
            "records": [record.to_dict(self.header) for record in self.records] if self.header else [],
            "cells": [cell.to_dict(self.header) for cell in self.cells] if self.header else [],
        }


@dataclass(frozen=True)
class OptReconstruction:
    source_ref: str
    opt_ref: str
    source_size: tuple[int, int] | None
    logical_size: tuple[int, int] | None
    status: str
    image: Image.Image | None
    parsed: OptPayload
    issues: tuple[str, ...]

    @property
    def pixel_sha256(self) -> str | None:
        return sha256_bytes(self.image.tobytes()) if self.image is not None else None

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_ref": self.source_ref,
            "opt_ref": self.opt_ref,
            "source_size": {
                "width": self.source_size[0],
                "height": self.source_size[1],
            }
            if self.source_size
            else None,
            "logical_size": {
                "width": self.logical_size[0],
                "height": self.logical_size[1],
            }
            if self.logical_size
            else None,
            "status": self.status,
            "pixel_sha256": self.pixel_sha256,
            "issues": list(self.issues),
            "opt": self.parsed.to_dict(),
        }


def parse_opt(raw: bytes, source_ref: str = "<bytes>") -> OptPayload:
    """Parse an OPT payload using its variable-piece cell structure."""

    digest = sha256_bytes(raw)
    if len(raw) < OPT_HEADER_SIZE:
        return OptPayload(
            source_ref,
            len(raw),
            digest,
            None,
            (),
            (),
            len(raw),
            None,
            "truncated_header",
            ("opt_header_truncated",),
        )

    header = OptHeader(*raw[:OPT_HEADER_SIZE])
    expected = header.columns * header.rows
    position = OPT_HEADER_SIZE
    records: list[OptRecord] = []
    errors: list[str] = []
    if header.cell_width <= 0 or header.cell_height <= 0 or header.columns <= 0 or header.rows <= 0:
        errors.append("invalid_logical_grid")

    cells: list[OptCell] = []
    for cell_index in range(expected):
        if position >= len(raw):
            errors.append(f"missing_cell_piece_count:{cell_index}")
            cells.append(OptCell(cell_index, 0, ()))
            continue

        piece_count = raw[position]
        position += 1
        cell_records: list[OptRecord] = []
        for part_index in range(piece_count):
            remaining = len(raw) - position
            if remaining < OPT_PIECE_SIZE:
                errors.append(f"partial_piece_tail:{cell_index}:{part_index}:{remaining}")
                position = len(raw)
                break
            piece = raw[position : position + OPT_PIECE_SIZE]
            position += OPT_PIECE_SIZE
            record = OptRecord(
                index=cell_index,
                record_prefix=piece_count,
                source_reference=_short(piece, 0),
                offset_x=_short(piece, 2),
                offset_y=_short(piece, 4),
                source_x=_short(piece, 6),
                source_y=_short(piece, 8),
                width=_ushort(piece, 10),
                height=_ushort(piece, 12),
                part_index=part_index,
                part_count=piece_count,
            )
            cell_records.append(record)
            records.append(record)
        cells.append(OptCell(cell_index, piece_count, tuple(cell_records)))

    partial_tail = len(raw) - position
    if partial_tail:
        errors.append(f"trailing_opt_bytes:{partial_tail}")

    status = "pass" if not errors else "candidate"
    return OptPayload(
        source_ref,
        len(raw),
        digest,
        header,
        tuple(records),
        tuple(cells),
        partial_tail,
        expected,
        status,
        tuple(errors),
    )


def _paste_clipped(destination: Image.Image, source: Image.Image, x: int, y: int) -> None:
    """Paste an RGBA crop while retaining evidence for negative offsets."""

    left = max(0, -x)
    top = max(0, -y)
    right = min(source.width, destination.width - x)
    bottom = min(source.height, destination.height - y)
    if left >= right or top >= bottom:
        return
    cropped = source.crop((left, top, right, bottom))
    destination.alpha_composite(cropped, (max(0, x), max(0, y)))


def reconstruct_opt(source_png: bytes, opt_raw: bytes, source_ref: str = "<png>", opt_ref: str = "<opt>") -> OptReconstruction:
    """Reconstruct a logical RGBA atlas from source PNG bytes and OPT bytes."""

    parsed = parse_opt(opt_raw, opt_ref)
    if parsed.header is None:
        return OptReconstruction(source_ref, opt_ref, None, None, "blocked", None, parsed, parsed.errors)
    try:
        source = Image.open(BytesIO(source_png)).convert("RGBA")
        source_size = source.size
    except Exception as error:  # pragma: no cover - caller-facing issue is retained
        issue = f"source_png_decode:{error}"
        return OptReconstruction(source_ref, opt_ref, None, parsed.logical_size, "blocked", None, parsed, (issue,))

    issues = list(parsed.errors)
    for record in parsed.records:
        if record.source_x < 0 or record.source_y < 0:
            issues.append(f"negative_source_rect:{record.index}:{record.part_index}")
            continue
        if record.source_x + record.width > source.width or record.source_y + record.height > source.height:
            issues.append(
                f"source_rect_out_of_bounds:{record.index}:{record.part_index}:"
                f"{record.source_x},{record.source_y},{record.width},{record.height}_within_{source.width}x{source.height}"
            )
    if issues:
        return OptReconstruction(source_ref, opt_ref, source_size, parsed.logical_size, "blocked", None, parsed, tuple(issues))

    assert parsed.header is not None
    logical = Image.new("RGBA", parsed.logical_size, (0, 0, 0, 0))
    for cell in parsed.cells:
        # The derived references establish back-to-front composition order:
        # later pieces are drawn underneath earlier pieces for multi-piece cells.
        for record in reversed(cell.records):
            crop = source.crop(
                (
                    record.source_x,
                    record.source_y,
                    record.source_x + record.width,
                    record.source_y + record.height,
                )
            )
            destination_x, destination_y = record.destination(parsed.header)
            _paste_clipped(logical, crop, destination_x, destination_y)

    status = "pass" if parsed.status == "pass" else "candidate"
    return OptReconstruction(
        source_ref,
        opt_ref,
        source_size,
        parsed.logical_size,
        status,
        logical,
        parsed,
        tuple(issues),
    )
