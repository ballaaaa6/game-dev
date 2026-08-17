"""Tests for the evidence-bounded, layered SEB reader."""

from __future__ import annotations

import struct
import zipfile
from pathlib import Path

import pytest

from seb_codec import SEB_RECORD_FORMAT, decode_seb


ROOT = Path(__file__).resolve().parents[2]
ASSET_ZIP = ROOT / "sources/raw/Social_Dev_Story_v2.5.1_ASSETS_ONLY_WITH_ASSEMBLY_GUIDE.zip"
ARCHIVE_PREFIX = "Social_Dev_Story_v2.5.1_ASSETS_ONLY/"


def record(
    start_frame: int,
    image_id: int,
    source_x: int = 0,
    source_y: int = 0,
    width: int = 1,
    height: int = 1,
    destination_x: int = 0,
    destination_y: int = 0,
    flags: int = 0,
    reserved: int = 0,
) -> bytes:
    return struct.pack(
        SEB_RECORD_FORMAT,
        start_frame,
        image_id,
        source_x,
        source_y,
        width,
        height,
        destination_x,
        destination_y,
        flags,
        reserved,
    )


def test_decode_seb_reads_layer_markers_and_preserves_layer_order() -> None:
    raw = (
        struct.pack(">HHHH", 2, 4, 2, 4)
        + record(0, 6, width=24, height=43, destination_x=-4, destination_y=-24)
        + record(1, 6, source_x=72, width=24, height=43, destination_y=-24)
        + struct.pack(">HH", 2, 7)
        + record(0, 7, width=13, height=31, destination_y=-24)
        + record(1, 7, source_x=13, width=13, height=31, destination_x=23, destination_y=-23)
    )

    decoded = decode_seb(raw, "synthetic.seb")

    assert decoded["status"] == "pass"
    assert decoded["header"] == {
        "layer_count": 2,
        "global_frame_count": 4,
        "record_count": 2,
        "frame_bound": 4,
    }
    assert [layer["layer"] for layer in decoded["layers"]] == [0, 1]
    assert [layer["record_count"] for layer in decoded["layers"]] == [2, 2]
    assert decoded["layers"][1]["marker"] == {"record_count": 2, "raw_value": 7}
    assert decoded["records"][2]["layer"] == 1
    assert decoded["records"][2]["image_id"] == 7
    assert decoded["trailing_bytes"] == 0


def test_decode_floor00_seb_assets_uses_all_wall_ex_frames_and_wall_layers() -> None:
    with zipfile.ZipFile(ASSET_ZIP) as archive:
        wall_ex = decode_seb(
            archive.read(ARCHIVE_PREFIX + "01_GAME_PACKS/chip/wall_ex.seb"),
            "01_GAME_PACKS/chip/wall_ex.seb",
        )
        wall_00 = decode_seb(
            archive.read(ARCHIVE_PREFIX + "01_GAME_PACKS/chip/wall_00.seb"),
            "01_GAME_PACKS/chip/wall_00.seb",
        )

    assert wall_ex["status"] == "pass"
    assert wall_ex["header"]["layer_count"] == 1
    assert [record["start_frame"] for record in wall_ex["records"]] == [0, 1, 2, 3]
    assert [(record["source_x"], record["width"], record["destination_x"]) for record in wall_ex["records"]] == [
        (52, 20, 0),
        (72, 20, 20),
        (48, 24, -4),
        (72, 24, 20),
    ]

    assert wall_00["status"] == "pass"
    assert wall_00["header"]["layer_count"] == 2
    assert [layer["record_count"] for layer in wall_00["layers"]] == [4, 4]
    assert len(wall_00["records"]) == 8
    assert wall_00["records"][4]["layer"] == 1


def test_decode_seb_rejects_truncated_layer_marker() -> None:
    raw = struct.pack(">HHHH", 2, 1, 1, 1) + record(0, 1) + b"\x00\x01"

    with pytest.raises(ValueError, match="layer 1 marker"):
        decode_seb(raw, "truncated.seb")
