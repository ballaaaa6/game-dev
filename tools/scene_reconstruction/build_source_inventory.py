import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tools.scene_reconstruction.paths import workspace_root
from tools.scene_reconstruction.source_inventory import build_source_inventory


def main():
    root = workspace_root()
    output = root / "knowledge/world-assets/evidence/scene_reconstruction/source_inventory.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(build_source_inventory(root).to_json(), encoding="utf-8", newline="\n")
    print(output)


if __name__ == "__main__":
    main()
