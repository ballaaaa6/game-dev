# Social Dev C# clean-room reset

Workspace for organizing and rebuilding the Social Dev system from C#/APK/asset-guide evidence, with clear separation between source, evidence, derived models, and runtime.

## Current Structure

- `knowledge/social-dev/` — active Social Dev evidence, candidate schemas, and provenance gates
- `runtime/social-dev/` — active runtime boundary to be built from Social Dev contracts
- `tools/social-dev/` — active Social Dev inventory/validation tools
- `tools/` — active Social Dev tools only
- `docs/` — Social Dev roadmaps and reports only
- `archive/future-ai/` — inactive AI-integration ideas

The active browser entrypoint is the unified Social Dev main runtime at `runtime/social-dev/`. It opens the approved native floor00 scene by default, keeps all current catalogs and room records in one runtime, and exposes room inspection through the in-page selector.

## Read-Only Sources

- `social dev/` — Social Dev source inputs, read-only

`knowledge/social-dev/evidence/` is the active Social Dev evidence boundary. The removed legacy corpus must not be recreated, and `Assembly-CSharp/` must not be recreated.

## Starting Point for the Next Session

Read [AGENTS.md](AGENTS.md), [PROJECT_STATE.md](PROJECT_STATE.md), and [TODO.md](TODO.md), then review the [Social Dev roadmap](docs/roadmap/Roadmap_SocialDev_CSharp_Reset.md).

Primary verification commands:

```powershell
python -B tools/social-dev/stage_data_package.py
python -B tools/social-dev/test_pre_runtime_closure.py
```

Runtime smoke URL:

```text
http://127.0.0.1:4173/?auto=0
```
