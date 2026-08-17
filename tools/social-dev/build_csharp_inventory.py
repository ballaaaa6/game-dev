"""Build the first Social Dev C# structural inventory from immutable evidence."""

from __future__ import annotations

import argparse
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
from semantic_inventory import (
    build_structural_inventory,
    load_target_manifest,
    write_inventory,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--target",
        type=Path,
        default=ROOT / "tools/social-dev/csharp_inventory_targets.json",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "knowledge/fixtures/accepted/csharp_inventory",
    )
    args = parser.parse_args()
    target_path = args.target if args.target.is_absolute() else ROOT / args.target
    output_path = args.output if args.output.is_absolute() else ROOT / args.output
    manifest = load_target_manifest(target_path)
    inventory = build_structural_inventory(ROOT, manifest)
    write_inventory(output_path, inventory)
    print(
        "build_complete "
        f"fingerprint={inventory['content_fingerprint']} "
        f"inputs={len(inventory['inputs'])} "
        f"types={len(inventory['types'])} "
        f"fields={len(inventory['fields'])} "
        f"methods={len(inventory['methods'])}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
