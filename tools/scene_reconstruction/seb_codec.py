"""Bounds-aware, evidence-preserving parser for legacy SEB descriptors.

The format-0 layout is retained from ``APK_Toolkit/decode_seb.py``.  This
module deliberately models missing bytes as missing values: it never pads a
record, invents reverse flags, or treats a compact selector as format 0.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
from typing import Iterable


FORMAT0_FIELD_NAMES = (
    "frame",
    "texture_id",
    "u",
    "v",
    "w",
    "h",
    "trans_x",
    "trans_y",
    "reverse_u",
    "reverse_v",
)
FORMAT0_RECORD_BYTES = len(FORMAT0_FIELD_NAMES) * 2


def _hex(data: bytes) -> str:
    return data.hex()


def _sha256(data: bytes) -> str:
    return sha256(data).hexdigest()


@dataclass(frozen=True)
class SebHeader:
    offset: int
    raw_bytes: bytes
    selector: int | None
    group_count: int | None
    max_frame: int | None

    def to_dict(self) -> dict:
        return {
            "offset": self.offset,
            "raw_hex": _hex(self.raw_bytes),
            "selector": self.selector,
            "group_count": self.group_count,
            "max_frame": self.max_frame,
        }


@dataclass(frozen=True)
class SebRecord:
    index: int
    offset: int
    raw_bytes: bytes
    raw_tail: bytes
    complete: bool
    frame: int | None = None
    texture_id: int | None = None
    u: int | None = None
    v: int | None = None
    w: int | None = None
    h: int | None = None
    trans_x: int | None = None
    trans_y: int | None = None
    reverse_u: int | None = None
    reverse_v: int | None = None

    def to_dict(self) -> dict:
        values = {name: getattr(self, name) for name in FORMAT0_FIELD_NAMES}
        return {
            "index": self.index,
            "offset": self.offset,
            "expected_bytes": FORMAT0_RECORD_BYTES,
            "available_bytes": len(self.raw_bytes),
            "raw_hex": _hex(self.raw_bytes),
            "raw_tail_hex": _hex(self.raw_tail),
            "complete": self.complete,
            "fields": values,
        }


@dataclass(frozen=True)
class SebGroup:
    index: int
    offset: int
    header_end_offset: int
    raw_header: bytes
    declared_record_count: int | None
    group_id: int | None
    records: tuple[SebRecord, ...]
    status: str

    @property
    def parsed_complete_count(self) -> int:
        return sum(record.complete for record in self.records)

    def to_dict(self) -> dict:
        return {
            "index": self.index,
            "offset": self.offset,
            "header_end_offset": self.header_end_offset,
            "raw_header_hex": _hex(self.raw_header),
            "declared_record_count": self.declared_record_count,
            "group_id": self.group_id,
            "parsed_complete_count": self.parsed_complete_count,
            "status": self.status,
            "records": [record.to_dict() for record in self.records],
        }


@dataclass(frozen=True)
class SebFile:
    source_ref: str
    size_bytes: int
    sha256: str
    format_code: int | None
    format_decision: str
    header: SebHeader
    groups: tuple[SebGroup, ...]
    bytes_consumed: int
    expected_bytes: int | None
    partial_tail: bytes
    tail_shortfall: int
    status: str
    errors: tuple[str, ...] = ()

    def to_dict(self) -> dict:
        return {
            "source_ref": self.source_ref,
            "size_bytes": self.size_bytes,
            "sha256": self.sha256,
            "format_code": self.format_code,
            "format_decision": self.format_decision,
            "header": self.header.to_dict(),
            "groups": [group.to_dict() for group in self.groups],
            "bytes_consumed": self.bytes_consumed,
            "expected_bytes": self.expected_bytes,
            "partial_tail_hex": _hex(self.partial_tail),
            "tail_shortfall": self.tail_shortfall,
            "status": self.status,
            "errors": list(self.errors),
        }


def _read_short(data: bytes, offset: int) -> tuple[int | None, int]:
    if offset + 2 > len(data):
        return None, len(data)
    return int.from_bytes(data[offset : offset + 2], "big", signed=True), offset + 2


def _missing_record(index: int, offset: int) -> SebRecord:
    return SebRecord(index=index, offset=offset, raw_bytes=b"", raw_tail=b"", complete=False)


def _format0_record(data: bytes, offset: int, index: int) -> tuple[SebRecord, int]:
    start = offset
    values: list[int | None] = []
    for _ in FORMAT0_FIELD_NAMES:
        value, offset = _read_short(data, offset)
        values.append(value)
    raw = data[start:offset]
    complete = len(raw) == FORMAT0_RECORD_BYTES
    return (
        SebRecord(
            index=index,
            offset=start,
            raw_bytes=raw,
            # Keep the complete raw record separately.  ``raw_tail`` is the
            # final four bytes observed before EOF, matching the known
            # shortfall evidence without presenting them as reverse fields.
            raw_tail=b"" if complete else raw[-4:],
            complete=complete,
            **dict(zip(FORMAT0_FIELD_NAMES, values)),
        ),
        offset,
    )


def _empty_file(source_ref: str, data: bytes, decision: str, error: str) -> SebFile:
    return SebFile(
        source_ref=source_ref,
        size_bytes=len(data),
        sha256=_sha256(data),
        format_code=None,
        format_decision=decision,
        header=SebHeader(0, data, None, None, None),
        groups=(),
        bytes_consumed=len(data),
        expected_bytes=None,
        partial_tail=data,
        tail_shortfall=0,
        status="unknown",
        errors=(error,),
    )


def parse_seb_bytes(data: bytes, source_ref: str) -> SebFile:
    """Parse one SEB payload while preserving its bytes and EOF boundaries."""
    if len(data) < 1:
        return _empty_file(source_ref, data, "missing_selector", "missing_format_selector")
    if data[0] & 0x80:
        return _empty_file(source_ref, data, "compact_variant", "compact_variant_not_format0")
    if len(data) < 4:
        return _empty_file(source_ref, data, "format0", "truncated_format0_header")

    group_count = int.from_bytes(data[0:2], "big", signed=False)
    max_frame = int.from_bytes(data[2:4], "big", signed=True)
    header = SebHeader(0, data[0:4], data[0], group_count, max_frame)
    offset = 4
    expected_bytes = 4
    groups: list[SebGroup] = []
    errors: list[str] = []
    partial_tail = b""

    for group_index in range(group_count):
        group_offset = offset
        declared_count, offset = _read_short(data, offset)
        group_id, offset = _read_short(data, offset)
        raw_header = data[group_offset:offset]
        if declared_count is None or group_id is None:
            groups.append(
                SebGroup(group_index, group_offset, offset, raw_header, declared_count, group_id, (), "unknown")
            )
            errors.append(f"group_{group_index}_header_truncated")
            break
        if declared_count < 0:
            groups.append(
                SebGroup(group_index, group_offset, offset, raw_header, declared_count, group_id, (), "unknown")
            )
            errors.append(f"group_{group_index}_negative_record_count")
            break
        expected_bytes += 4 + declared_count * FORMAT0_RECORD_BYTES
        records: list[SebRecord] = []
        group_status = "verified"
        for record_index in range(declared_count):
            if offset >= len(data):
                records.extend(_missing_record(index, len(data)) for index in range(record_index, declared_count))
                group_status = "candidate"
                break
            record, offset = _format0_record(data, offset, record_index)
            records.append(record)
            if not record.complete:
                partial_tail = record.raw_tail
                records.extend(_missing_record(index, len(data)) for index in range(record_index + 1, declared_count))
                group_status = "candidate"
                break
        groups.append(
            SebGroup(group_index, group_offset, min(offset, len(data)), raw_header, declared_count, group_id, tuple(records), group_status)
        )
        if group_status != "verified":
            break

    tail_shortfall = max(0, expected_bytes - len(data))
    if errors:
        status = "unknown"
    elif tail_shortfall:
        status = "candidate"
    elif len(data) > expected_bytes:
        # Format-0 consumes no bytes beyond the declared group records.  Keep
        # an observed suffix, but do not promote this non-exact payload to a
        # complete recovery candidate.
        status = "candidate"
        partial_tail = data[expected_bytes:]
    else:
        status = "verified"
    return SebFile(
        source_ref=source_ref,
        size_bytes=len(data),
        sha256=_sha256(data),
        format_code=0,
        format_decision="format0",
        header=header,
        groups=tuple(groups),
        bytes_consumed=min(offset, len(data)),
        expected_bytes=expected_bytes,
        partial_tail=partial_tail,
        tail_shortfall=tail_shortfall,
        status=status,
        errors=tuple(errors),
    )


@dataclass(frozen=True)
class SebCandidate:
    source_kind: str
    source_ref: str
    data: bytes | None
    read_error: str | None = None
    declared_sha256: str | None = None
    archive_member_path: str | None = None
    archive_path: str | None = None


@dataclass(frozen=True)
class SebCandidateResult:
    source_kind: str
    source_ref: str
    classification: str
    sha256: str | None
    size_bytes: int | None
    parsed: SebFile | None
    read_error: str | None
    declared_sha256: str | None
    archive_member_path: str | None
    archive_path: str | None

    def to_dict(self) -> dict:
        return {
            "source_kind": self.source_kind,
            "source_ref": self.source_ref,
            "classification": self.classification,
            "sha256": self.sha256,
            "size_bytes": self.size_bytes,
            "read_error": self.read_error,
            "declared_sha256": self.declared_sha256,
            "archive_member_path": self.archive_member_path,
            "archive_path": self.archive_path,
            "parsed": self.parsed.to_dict() if self.parsed else None,
        }


@dataclass(frozen=True)
class SebComparison:
    candidates: tuple[SebCandidateResult, ...]
    outcome: str
    best_complete: SebCandidateResult | None

    def to_dict(self) -> dict:
        return {
            "outcome": self.outcome,
            "best_complete": self.best_complete.source_ref if self.best_complete else None,
            "candidates": [candidate.to_dict() for candidate in self.candidates],
        }


def compare_seb_sources(candidates: Iterable[SebCandidate]) -> SebComparison:
    """Classify source candidates without conflating unavailable bytes with data."""
    candidate_list = list(candidates)
    payloads = [candidate for candidate in candidate_list if candidate.data is not None]
    baseline = next((candidate for candidate in payloads if candidate.source_kind == "sprite"), None)
    if baseline is None and payloads:
        baseline = payloads[0]
    baseline_hash = _sha256(baseline.data) if baseline and baseline.data is not None else None
    results: list[SebCandidateResult] = []
    for candidate in candidate_list:
        if candidate.read_error is not None:
            classification, digest, parsed, size = "unreadable", None, None, None
        elif candidate.data is None:
            digest = candidate.declared_sha256
            parsed = None
            size = None
            if digest is not None and baseline_hash is not None:
                classification = "byte-identical" if digest == baseline_hash else "distinct"
            else:
                classification = "absent"
        else:
            digest = _sha256(candidate.data)
            parsed = parse_seb_bytes(candidate.data, candidate.source_ref)
            size = len(candidate.data)
            classification = "byte-identical" if baseline_hash is not None and digest == baseline_hash else "distinct"
        results.append(
            SebCandidateResult(
                candidate.source_kind,
                candidate.source_ref,
                classification,
                digest,
                size,
                parsed,
                candidate.read_error,
                candidate.declared_sha256,
                candidate.archive_member_path,
                candidate.archive_path,
            )
        )

    current = next((item for item in results if item.source_kind == "sprite" and item.parsed), None)
    recovery_complete = [
        item
        for item in results
        if item.source_kind in {"apk", "zip", "archive", "fresh"}
        and item.classification == "distinct"
        and item.parsed
        and item.parsed.status == "verified"
    ]
    best_complete = recovery_complete[0] if recovery_complete else None
    if best_complete and current and current.parsed and current.parsed.status != "verified":
        current_bytes = next(candidate.data for candidate in candidate_list if candidate.source_ref == current.source_ref)
        complete_bytes = next(candidate.data for candidate in candidate_list if candidate.source_ref == best_complete.source_ref)
        outcome = "recovered_full_payload" if complete_bytes.startswith(current_bytes) else "recovered_different_payload"
    elif best_complete:
        outcome = "recovered_different_payload"
    elif current and current.parsed and current.parsed.status == "verified":
        outcome = "not_needed"
    else:
        outcome = "no_full_payload_found"
    return SebComparison(tuple(results), outcome, best_complete)
