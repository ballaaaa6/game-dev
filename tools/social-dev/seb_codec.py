"""Evidence-bounded decoder for the layered SEB sprite container.

The runtime must not parse SEB files.  This module is used by extraction and
contract builders so the binary layout is decoded once, with every raw field
retained for provenance.  The observed game assets use a four-word big-endian
header, a 20-byte record format, and a four-byte record-count marker before
each layer after layer zero.
"""

from __future__ import annotations

import struct
from typing import Any


SEB_HEADER_FORMAT = ">HHHH"
SEB_HEADER_SIZE = struct.calcsize(SEB_HEADER_FORMAT)
SEB_RECORD_FORMAT = ">HHHHhhhhHH"
SEB_RECORD_SIZE = struct.calcsize(SEB_RECORD_FORMAT)
SEB_LAYER_MARKER_FORMAT = ">HH"
SEB_LAYER_MARKER_SIZE = struct.calcsize(SEB_LAYER_MARKER_FORMAT)


class SebDecodeError(ValueError):
    """Raised when a SEB member does not match the observed layered grammar."""


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise SebDecodeError(message)


def signed_texture_id(raw_value: int) -> int:
    """Preserve the unsigned field and expose the native signed texture id."""

    return raw_value - 0x10000 if raw_value >= 0x8000 else raw_value


def decode_seb(raw: bytes, member: str = "<memory>") -> dict[str, Any]:
    """Decode a layered SEB member without resolving its referenced textures.

    The first layer's record count is stored in the header.  Every later layer
    starts with a ``>HH`` marker; its first word is the layer record count and
    its second word is retained as raw evidence because the source assets use
    it as an operation-specific value rather than a universal frame bound.
    """

    _require(len(raw) >= SEB_HEADER_SIZE, f"SEB {member} is shorter than its header")
    layer_count, global_frame_count, record_count, frame_bound = struct.unpack(
        SEB_HEADER_FORMAT, raw[:SEB_HEADER_SIZE]
    )
    _require(layer_count > 0, f"SEB {member} has no layers")
    _require(layer_count <= 1024, f"SEB {member} layer count is outside the layered grammar")
    _require(global_frame_count > 0, f"SEB {member} has no global frames")
    _require(record_count > 0, f"SEB {member} layer 0 has no records")
    _require(record_count <= 8192, f"SEB {member} record count is outside the layered grammar")

    metadata_warnings: list[str] = []
    if frame_bound == 0:
        metadata_warnings.append("header_frame_bound_zero")
    elif frame_bound < global_frame_count:
        metadata_warnings.append("header_frame_bound_shorter_than_global_frames")

    offset = SEB_HEADER_SIZE
    layers: list[dict[str, Any]] = []
    records: list[dict[str, Any]] = []

    for layer_index in range(layer_count):
        marker: dict[str, int] | None = None
        if layer_index == 0:
            layer_record_count = record_count
        else:
            _require(
                offset + SEB_LAYER_MARKER_SIZE <= len(raw),
                f"SEB {member} is missing layer {layer_index} marker",
            )
            marker_record_count, marker_value = struct.unpack(
                SEB_LAYER_MARKER_FORMAT,
                raw[offset : offset + SEB_LAYER_MARKER_SIZE],
            )
            offset += SEB_LAYER_MARKER_SIZE
            _require(
                marker_record_count > 0,
                f"SEB {member} layer {layer_index} marker has no records",
            )
            layer_record_count = marker_record_count
            marker = {
                "record_count": marker_record_count,
                "raw_value": marker_value,
            }

        layer_records: list[dict[str, Any]] = []
        for layer_record_index in range(layer_record_count):
            _require(
                offset + SEB_RECORD_SIZE <= len(raw),
                f"SEB {member} layer {layer_index} record {layer_record_index} is truncated",
            )
            values = struct.unpack(
                SEB_RECORD_FORMAT,
                raw[offset : offset + SEB_RECORD_SIZE],
            )
            offset += SEB_RECORD_SIZE
            (
                start_frame,
                image_id_raw,
                source_x,
                source_y,
                width,
                height,
                destination_x,
                destination_y,
                flags,
                reserved,
            ) = values
            frame_limit = max(frame_bound, global_frame_count, 1)
            frame_status = "in_header_frame_bound" if frame_bound > 0 and start_frame < frame_bound else "outside_header_frame_bound"
            if start_frame >= frame_limit:
                metadata_warnings.append(
                    f"record_{layer_index}_{layer_record_index}_start_frame_outside_global_frame_count"
                )
            decoded: dict[str, Any] = {
                "layer": layer_index,
                "layer_record_index": layer_record_index,
                "start_frame": start_frame,
                "image_id": signed_texture_id(image_id_raw),
                "image_id_raw": image_id_raw,
                "source_x": source_x,
                "source_y": source_y,
                "width": width,
                "height": height,
                "destination_x": destination_x,
                "destination_y": destination_y,
                "flags": flags,
                "reserved": reserved,
                "frame_status": frame_status,
            }
            layer_records.append(decoded)
            records.append(decoded)

        layers.append(
            {
                "index": layer_index,
                "layer": layer_index,
                "record_count": layer_record_count,
                "frame_bound": frame_bound,
                "marker": marker,
                "records": layer_records,
            }
        )

    trailing_bytes = len(raw) - offset
    _require(
        trailing_bytes == 0,
        f"SEB {member} has {trailing_bytes} trailing bytes after multilayer decode",
    )
    return {
        "status": "pass",
        "grammar": "seb-layered-v1",
        "byte_length": len(raw),
        "header": {
            "layer_count": layer_count,
            "global_frame_count": global_frame_count,
            "record_count": record_count,
            "frame_bound": frame_bound,
        },
        "layers": layers,
        "records": records,
        "trailing_bytes": trailing_bytes,
        "metadata_warnings": sorted(set(metadata_warnings)),
    }
