import json
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tools.scene_reconstruction.csharp_trace import build_seb_semantics_contract
from tools.scene_reconstruction.paths import workspace_root


def main() -> int:
    root = workspace_root()
    output = root / "knowledge/world-assets/evidence/scene_reconstruction/seb_semantics_contract.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    contract = build_seb_semantics_contract(workspace=root)
    output.write_text(json.dumps(contract.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
