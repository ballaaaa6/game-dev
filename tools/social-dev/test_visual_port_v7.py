"""Static acceptance gate for V7 raster compatibility and golden PNG evidence."""

from __future__ import annotations

import hashlib
import json
import struct
import sys
import zlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
V7 = ROOT / "knowledge" / "fixtures" / "accepted" / "visual-port" / "v7"

REQUIRED = [
    "graphics-raster-contract.json",
    "sampling-contract.json",
    "transform-raster-contract.json",
    "blend-alpha-contract.json",
    "selected-path-closure.json",
    "staff-cadence-contract.json",
    "golden-fixture-manifest.json",
    "golden-fixture-results.json",
    "room00-structural-render.json",
    "room00-with-staff-render.json",
    "pixel-diff-results.json",
    "fidelity-manifest.json",
    "unknowns.json",
    "checkpoint-ledger.json",
]

EXPECTED_FIXTURES = {
    "floor.direct_image": (
        "4046565574bb8860b260470834eda2d3dc3299330747e513b56a6bc08ed5287b",
        "ba243e35a05df863e8d5f1e10bf8e0191c6063202b491d789ac4075eeabee6b8",
        360,
        220,
    ),
    "wall.seb": (
        "515b4d322f9d8facd5d4bba7063fcad85b83a1892f47e0ef4a269d2bd46f197e",
        "83022357a157a222bbe2fee2d49a0b03643792369bfc0f03d0c41f1c76b863b2",
        360,
        220,
    ),
    "door.seb": (
        "dc98c3763abc6d0fcb3e2802f265f35456791b77fefbc0ee8eec35f9e3781992",
        "f0d1a1d0d237fa296f69e355ee973238afabc94a94c0032421c27ca7cc4b417f",
        360,
        220,
    ),
    "furniture.3_desk_chair": (
        "099ba358b2615f2cca302dc67e65c726d75ab8a9029f67c0c60d6544586b7604",
        "fa751a1afc149ff7c76204c08a7d6094aab55b70c5ab3c5e942ea1cfa8930642",
        360,
        220,
    ),
    "furniture.12": (
        "1163e18f960b0cac3669478e89ec6a2b486a6da5b0b798f8b54ab22075077d67",
        "a9188f4f5e3ee0e9338971c5a78eaf64b23cf0dbaf88f0d09484f8d929c34faa",
        360,
        220,
    ),
    "furniture.26": (
        "257324da2d90263bfa13045a43d76ccb46c5bbbd3d76b98105631ba099585992",
        "fc8e71ad97a650f5f16ca4ce5be1cf84927f38189b55a678baf6ba8d92fd5f30",
        360,
        220,
    ),
    "furniture.56": (
        "d0caa1b027844d36e5b0f77b457ebbce15e0ad395cb12b447ff6738345167c0d",
        "7f803211a2a6ff0f0467e770eab6963b254906ea9bfde8f323b60612883298a9",
        360,
        220,
    ),
    "staff.0_wait_right": (
        "58a760847df408119823a10886d9420817a57a4cb2c2ace5a79016f8063299cf",
        "b0e788da838fb5ea7799f9f398d2bdd21b2edd5290559e1e19e05cc4c0cfed09",
        360,
        220,
    ),
    "staff.0_wait_left": (
        "cc13c6d614743e78cc7959470872b6a0eb63da70fb45e88bc0440798b6c8c9b1",
        "ca8713a728e29961a7d2ebbb12aa97bf9f75e6504c44f106dae6ea5d70389d66",
        360,
        220,
    ),
    "staff.0_typing_right": (
        "289963667d5e16ab59334865bdd1a8d1579e728f88be9e6c2ed233ef6222b2a3",
        "9dcee15c64813966212f3e5f6b0dd26c29a7bfa99e7bec1ab1a6697ec501d322",
        360,
        220,
    ),
    "graphics.selected_horizontal_flip": (
        "3a36a87130b57bf01e4faa0258414e3e68ba0260aaa33f0e2e7fe9356c074532",
        "74bc5966e8992a1b12310dbe404b718092c9c1ef4a2530ef09d023a2ea4e9038",
        360,
        220,
    ),
    "staff.alpha_128": (
        "1a4670d62edbe8e302fdae4e6c169b6aae7bacf76e202d56fbe6a24e4495cc68",
        "eb339f78c3b665db27baa7651d7f5a88b2e2cfc9f261aca6c8253fced4396a48",
        360,
        220,
    ),
    "graphics.clipped_draw": (
        "6288e31a6a5e970c94c0031d23812fe5b1acc47297954fd3221bf870add7b019",
        "f1c0c47dfb9dd0044269a81bd86c26a47513e6c369ec29d1cd3e84e02e8d1365",
        360,
        220,
    ),
    "graphics.transformed_draw": (
        "2583f6927546bf4a01a70e46f059b7295068639ec5479ae957a8cda69c44e379",
        "55861a17683ea3f654d64f33990175bf503958ed9a2118ab22469bbe95418733",
        240,
        200,
    ),
}


def load(name: str) -> dict:
    return json.loads((V7 / name).read_text(encoding="utf-8"))


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def decode_rgba_png(path: Path) -> tuple[int, int, bytes]:
    data = path.read_bytes()
    assert data[:8] == b"\x89PNG\r\n\x1a\n", f"invalid PNG signature: {path}"
    offset = 8
    width = height = bit_depth = color_type = interlace = 0
    idat = bytearray()
    while offset < len(data):
        length = struct.unpack(">I", data[offset : offset + 4])[0]
        kind = data[offset + 4 : offset + 8]
        chunk = data[offset + 8 : offset + 8 + length]
        offset += 12 + length
        if kind == b"IHDR":
            width, height = struct.unpack(">II", chunk[:8])
            bit_depth, color_type, _, _, interlace = chunk[8:13]
        elif kind == b"IDAT":
            idat.extend(chunk)
        elif kind == b"IEND":
            break
    assert bit_depth == 8 and color_type == 6 and interlace == 0, f"unsupported PNG format: {path}"
    decoded = zlib.decompress(bytes(idat))
    row_size = width * 4
    assert len(decoded) == height * (row_size + 1), f"unexpected PNG payload size: {path}"
    pixels = bytearray(width * height * 4)
    source_offset = 0
    for y in range(height):
        filter_type = decoded[source_offset]
        source_offset += 1
        assert filter_type == 0, f"V7 PNG is not deterministic filter-zero output: {path}"
        row = decoded[source_offset : source_offset + row_size]
        source_offset += row_size
        pixels[y * row_size : (y + 1) * row_size] = row
    return width, height, bytes(pixels)


def assert_png_record(record: dict, expected_pixel: str, expected_png: str, expected_width: int, expected_height: int) -> None:
    assert record["pixelSha256"] == expected_pixel
    assert record["pngSha256"] == expected_png
    assert record["outputWidth"] == expected_width
    assert record["outputHeight"] == expected_height
    assert record["nonTransparentBounds"] is not None, f"transparent-only fixture: {record['fixtureId']}"
    png_path = ROOT / record["pngPath"]
    png_bytes = png_path.read_bytes()
    assert sha256_bytes(png_bytes) == expected_png
    width, height, pixels = decode_rgba_png(png_path)
    assert (width, height) == (expected_width, expected_height)
    assert sha256_bytes(pixels) == expected_pixel
    assert len(pixels) == record["pixelByteLength"]


def main() -> None:
    for name in REQUIRED:
        assert (V7 / name).is_file(), f"missing V7 evidence: {name}"

    results = load("golden-fixture-results.json")
    assert {item["fixtureId"] for item in results} == set(EXPECTED_FIXTURES)
    for item in results:
        assert item["proofClass"] == "COMPATIBILITY_REIMPLEMENTATION"
        assert_png_record(item, *EXPECTED_FIXTURES[item["fixtureId"]])

    structural = load("room00-structural-render.json")
    assert structural["status"] == "pass_static"
    assert structural["room_key"] == "room:0"
    assert structural["commands"] == 139 and structural["traces"] == 124 and structural["events"] == 788
    assert structural["command_sha256"] == "0b8132b8ab45eda3d8bb344e65304e0c4d32717a9638c2789efd9223d9df5d60"
    assert structural["command_manifest_sha256"] == "48a1827c94c15394d38e872b243c398d8c6e6f47b66099bf26b44f22ee79e047"
    assert structural["pixel_sha256"] == "dcc4357c38e7d48a0d33e2d29a7fbda6f643b834f22393285bc3733a5f0143a0"
    assert structural["png_sha256"] == "b55d701ba74bd6212701a6623d5de667d824c00c604bfebfc2d416f7d5fd447a"
    assert structural["dimensions"] == {"width": 980, "height": 600}

    staff = load("room00-with-staff-render.json")
    assert staff["status"] == "pass_static"
    assert staff["room_key"] == "room:0"
    assert staff["commands"] == 142 and staff["traces"] == 127 and staff["events"] == 791
    assert staff["v6_manifest_sha256"] == "1e2b1d47922f8e274bfdf40a5c1c9aff85780441ad244f92de641e5cc5de1e7a"
    assert staff["pixel_sha256"] == "950a2478e1daa84d47fd89b7927271d913a5ef75f0e05e0b889bdbfae54c16b4"
    assert staff["png_sha256"] == "f5c2db1052ee55b6256208b164107bc123f58634f533ce621f46871acb60c1cd"
    assert staff["dimensions"] == {"width": 980, "height": 600}
    assert staff["action"] == "wait" and staff["direction"] == "right" and staff["frame"] == 0

    diff = load("pixel-diff-results.json")
    assert diff["status"] == "pass_static"
    repeats = [item for item in diff["comparisons"] if item["class"] == "deterministic_repeat"]
    assert len(repeats) == 2 and all(item["result"]["identical"] for item in repeats)
    assert diff["comparisons"][2]["result"]["changedPixelCount"] == 830
    assert diff["comparisons"][2]["difference_class"] == "C_COMPATIBILITY_BACKEND_DIFFERENCE"
    diff_png = ROOT / diff["diff_png"]["path"]
    assert sha256_bytes(diff_png.read_bytes()) == diff["diff_png"]["sha256"]

    fidelity = load("fidelity-manifest.json")
    assert fidelity["status"] == "PASS_STATIC_FIDELITY"
    assert fidelity["production_renderer_changed"] is False
    assert fidelity["v8_readiness"]["entry"] == "NO"
    assert fidelity["baseline"]["v5_manifest_sha256"] == "48a1827c94c15394d38e872b243c398d8c6e6f47b66099bf26b44f22ee79e047"
    assert fidelity["baseline"]["v6_manifest_sha256"] == "1e2b1d47922f8e274bfdf40a5c1c9aff85780441ad244f92de641e5cc5de1e7a"

    unknowns = load("unknowns.json")
    assert unknowns["status"] == "pass_static_nonblocking_unknowns"
    assert unknowns["blocking_unknowns"] == []

    ledger = load("checkpoint-ledger.json")
    assert ledger["status"] == "pass_static_fidelity"
    assert ledger["static_only"] is True and ledger["subagents"] is False
    assert ledger["execution_mode"] == "INLINE_EXECUTION_ONLY"
    assert [item["id"] for item in ledger["checkpoints"]] == [f"V7.{index}" for index in range(15)]
    assert all(item["status"] in {"PASS", "PASS_STATIC_BOUNDARY"} for item in ledger["checkpoints"])
    print("visual_port_v7_evidence_passed")


if __name__ == "__main__":
    try:
        main()
    except (AssertionError, KeyError, OSError, ValueError, zlib.error) as error:
        print(f"visual_port_v7_evidence_failed: {error}", file=sys.stderr)
        raise
