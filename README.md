# Social Dev C# clean-room reset

Workspace for organizing and rebuilding the Social Dev system from C#/APK/asset-guide evidence, with clear separation between source, evidence, derived models, and runtime.

## Current Structure

- `knowledge/social-dev/` — active Social Dev evidence, candidate schemas, and provenance gates
- `archive/pre-social-reset/knowledge/` — legacy/historical GameDev evidence removed from the active tree
- `runtime/social-dev/` — active runtime boundary to be built from Social Dev contracts
- `archive/pre-social-reset/runtime/` — legacy Office/Dashboard runtime that no longer receives new semantics
- `tools/social-dev/` — active Social Dev inventory/validation tools
- `tools/` — active Social Dev tools only; legacy tools are under `archive/pre-social-reset/tools/`
- `docs/` — Social Dev roadmaps and reports only
- `archive/` — legacy tools, historical GameDev work, and AI-integration ideas that are not active

## Read-Only Sources

- `social dev/` — Social Dev source inputs, read-only
- `archive/pre-social-reset/root-sources/` — archived GameDev source/extraction roots, APK toolkit, Ghidra bundle, and viewer

`knowledge/social-dev/evidence/` is the active Social Dev evidence boundary; the legacy GameDev corpus is under `archive/pre-social-reset/knowledge/`, and `Assembly-CSharp/` must not be recreated.

## Starting Point for the Next Session

Read [AGENTS.md](AGENTS.md), [PROJECT_STATE.md](PROJECT_STATE.md), and [TODO.md](TODO.md), then review the [Social Dev roadmap](docs/roadmap/Roadmap_SocialDev_CSharp_Reset.md).

Primary verification commands:

```powershell
python -B tools/social-dev/stage_data_package.py
python -B tools/social-dev/build_legacy_reference_scan.py
```
