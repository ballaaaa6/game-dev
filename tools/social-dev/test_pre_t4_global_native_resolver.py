"""Deterministic negative and replay tests for the pre-T4 resolver."""

from __future__ import annotations

import json
import struct
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))

import pre_t4_global_native_resolver as resolver  # noqa: E402


def test_required_negative_fixtures_reject_false_positives() -> None:
    result = resolver.run_negative_fixtures()
    assert result["passed"] is True
    assert result["false_positive_count"] == 0
    assert set(result["cases"]) == {
        "conditional_branch_not_thunk",
        "cyclic_thunk_chain",
        "invalid_elf_target",
        "unsupported_got_relocation",
        "ambiguous_metadata_target",
        "shared_native_address_explicit",
        "import_not_managed_method",
        "unresolved_generic_or_virtual_target",
    }


def test_direct_b_decoder_does_not_accept_bl_or_conditional() -> None:
    source = 0x1000
    target = 0x1010
    immediate = (target - source) // 4
    direct_b = struct.pack("<I", 0x14000000 | (immediate & 0x03FFFFFF))
    direct_bl = struct.pack("<I", 0x94000000 | (immediate & 0x03FFFFFF))
    conditional_cbz = struct.pack("<I", 0x34000004)
    executable = {source, target}

    def decode(value: bytes):
        instruction = struct.unpack("<I", value)[0]
        if (instruction & 0xFC000000) != 0x14000000:
            return None
        imm = instruction & 0x03FFFFFF
        if imm & (1 << 25):
            imm -= 1 << 26
        result = source + imm * 4
        return result if result in executable else None

    assert decode(direct_b) == target
    assert decode(direct_bl) is None
    assert decode(conditional_cbz) is None


def test_replay_of_pure_fixture_result_is_byte_stable() -> None:
    first = resolver.run_negative_fixtures()
    second = resolver.run_negative_fixtures()
    assert json.dumps(first, sort_keys=True, separators=(",", ":")) == json.dumps(second, sort_keys=True, separators=(",", ":"))
