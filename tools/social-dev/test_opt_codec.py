"""Deterministic checks for the evidence-bounded OPT codec."""

from __future__ import annotations

import io
from pathlib import Path
from zipfile import ZipFile

from PIL import Image

import opt_codec


ROOT = Path(__file__).resolve().parents[2]
ZIP_PATH = ROOT / "sources/raw/Social_Dev_Story_v2.5.1_ASSETS_ONLY_WITH_ASSEMBLY_GUIDE.zip"
PREFIX = "Social_Dev_Story_v2.5.1_ASSETS_ONLY/"


def image_pixel_sha256(raw: bytes) -> str:
    return opt_codec.sha256_bytes(Image.open(io.BytesIO(raw)).convert("RGBA").tobytes())


def main() -> int:
    with ZipFile(ZIP_PATH) as archive:
        def read(member: str) -> bytes:
            return archive.read(PREFIX + member)

        cases = (
            ("desk_00", "desk_00", "46707c4c651480c84721cc9a9d7a1d3a9a23eb6a8238e0dc8c81654c2f49ec47"),
            ("chair_02", "chair_02", "caf40e4a94974d85520fae1eb06f93a615af76dd11973118185598fafbf7dcde"),
            ("door_02", "door_02", "94811eb5d4b55342652c985c849f93d7ac643797b8eef9624bbbed0c936ff97b"),
        )
        for stem, reference_stem, expected_pixels in cases:
            result = opt_codec.reconstruct_opt(
                read(f"01_GAME_PACKS/chip/{stem}.png"),
                read(f"01_GAME_PACKS/chip/{stem}.opt"),
                f"{stem}.png",
                f"{stem}.opt",
            )
            assert result.status == "pass", result.to_dict()
            assert result.image is not None
            assert result.logical_size in {(120, 32), (180, 32), (26, 31)}
            reference = read(f"02_DERIVED_READY_IMAGES/opt_reconstructed/chip/{reference_stem}.logical.png")
            assert result.pixel_sha256 == expected_pixels
            assert result.pixel_sha256 == image_pixel_sha256(reference)
            assert list(result.image.getdata()) == list(Image.open(io.BytesIO(reference)).convert("RGBA").getdata())

        chair00 = opt_codec.parse_opt(read("01_GAME_PACKS/chip/chair_00.opt"), "chair_00.opt")
        assert chair00.status == "pass"
        assert chair00.partial_tail_bytes == 0
        assert chair00.errors == ()
        assert [cell.piece_count for cell in chair00.cells] == [1, 2, 1]
        assert len(chair00.records) == 4
        recovered = opt_codec.reconstruct_opt(
            read("01_GAME_PACKS/chip/chair_00.png"),
            read("01_GAME_PACKS/chip/chair_00.opt"),
            "chair_00.png",
            "chair_00.opt",
        )
        assert recovered.status == "pass"
        assert recovered.image is not None
        assert recovered.pixel_sha256 == "23d8e732fa2000f18f8fd9649b5fbe2b190d95aff86475b8befd09cfbe8afeef"

        chair04 = opt_codec.reconstruct_opt(
            read("01_GAME_PACKS/chip/chair_04.png"),
            read("01_GAME_PACKS/chip/chair_04.opt"),
            "chair_04.png",
            "chair_04.opt",
        )
        assert chair04.status == "pass"
        assert chair04.image is not None
        assert chair04.pixel_sha256 == "bbb7a50bfe171a629639d779fc989868f95a8b5a420fd0bb943ca27d051b0dd6"

    print("opt_codec_test_passed cases=3 variable_piece_chairs=chair_00,chair_04")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
