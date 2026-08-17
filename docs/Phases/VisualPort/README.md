# Phase V0 — Original Visual Subsystem Audit

Status: **audit complete; Phase V1 is gated**.

This package records the original Unity/IL2CPP visual subsystem before any port implementation. It is an evidence map, not a replacement renderer and not a gameplay port. No file under `runtime/social-dev/` was changed for this audit.

## Scope

The audit follows the original visual path named in the brief, but records the control flow as two connected branches so ownership is not misread:

```text
resource branch: asset files → ResourceManager → Image → OPT/SEB → Sprite
scene branch:    RoomData → Room → MapChip/ObjChip/Staff → ResourceManager draw wrappers
                 → Seb/Sprite composition → Graphics backend
```

`ResourceManager` is both a loader/group owner and the public draw-wrapper boundary; it is not a stage that runs only after `Sprite` has already been produced.

It also covers `Camera`, `GameForm`, `AppData`, `Main`, and the minimum `Player`/route-search dependencies needed to distinguish visible state from simulation. The required visual classes were inspected in both the cleaned C# update and the pinned native dump. Damaged decompiler bodies are recorded as evidence gaps; they are not treated as source code.

## Repository path adaptation

The pasted brief names `Phases/VisualPort/`. The repository has no root `Phases/` directory, and `AGENTS.md` requires authored reports/roadmaps under `docs/` and generated active-project evidence under `knowledge/fixtures/accepted/`. The audit therefore lives at:

- prose: `docs/Phases/VisualPort/`
- machine-readable evidence: `knowledge/fixtures/accepted/visual-port/`

This preserves the requested artifact set without creating a second generated evidence root.

## Source priority and boundaries

1. Pinned APK/asset data.
2. Native IL2CPP dump and native scene traces.
3. Unity serialized/resource evidence and OPT/SEB catalogues.
4. Decompiled C# declarations and call-site structure.
5. Existing reverse-engineering contracts.
6. Current TypeScript/browser runtime, used only for comparison.

The cleaned C# update remains read-only discovery evidence. The native dump is tied to APK SHA-256 `fa0e9e3a843732258fc05b2611a8e0f5be6f7e95f2141a53f31fb082322fe2bf`; native RVAs in this package are not portable to another build.

## Artifact index

| Artifact | Purpose |
|---|---|
| [VISUAL_CLASS_MAP.md](./VISUAL_CLASS_MAP.md) | Class responsibilities and six-way disposition. |
| [VISUAL_METHOD_MAP.md](./VISUAL_METHOD_MAP.md) | Critical method-level boundary and call notes. |
| [VISUAL_ARCHITECTURE.md](./VISUAL_ARCHITECTURE.md) | Original resource/render architecture and backend boundary. |
| [GAMEPLAY_CUT_LIST.md](./GAMEPLAY_CUT_LIST.md) | Simulation systems to cut or defer while retaining visible outputs. |
| [DECOMPILER_GAPS.md](./DECOMPILER_GAPS.md) | Damaged or missing proof with next investigation. |
| [ORIGINAL_VS_CURRENT_RUNTIME.md](./ORIGINAL_VS_CURRENT_RUNTIME.md) | Structural comparison with the existing browser runtime. |
| [PORT_PLAN.md](./PORT_PLAN.md) | Ordered V0–V9 plan and parity gate for every phase. |
| `knowledge/fixtures/accepted/visual-port/class-disposition.json` | Machine-readable class dispositions. |
| `knowledge/fixtures/accepted/visual-port/method-disposition.json` | Machine-readable critical method dispositions. |
| `knowledge/fixtures/accepted/visual-port/visual-dependency-graph.json` | Class/data dependency graph. |
| `knowledge/fixtures/accepted/visual-port/visual-call-graph.json` | Character, object, and room call traces. |
| `knowledge/fixtures/accepted/visual-port/visual-data-flow.json` | End-to-end resource and render flows. |
| `knowledge/fixtures/accepted/visual-port/resource-groups.json` | Original `AppData`/`ResourceManager` group topology. |
| `knowledge/fixtures/accepted/visual-port/native-method-map.json` | Pinned native RVA bridge and unresolved native lookups. |

## Disposition meanings

- `KEEP_EXACT`: preserve the original data/semantic contract; only a host boundary may change.
- `PORT_BACKEND`: preserve behavior while replacing Unity/platform services.
- `VISUAL_EXTRACT`: retain the visible subset and source-derived data, not the full gameplay class.
- `CUT_GAMEPLAY`: remove or defer behavior with no proven visual output.
- `NEEDS_NATIVE_TRACE`: declaration or call shape is known, but behavior requires native/fixture proof.
- `UNKNOWN`: evidence is insufficient to choose a safe implementation boundary.

## V0 decision

The audit is internally cross-referenced and the required JSON is intended to parse as one package. Phase V1 must not start until the consistency checks in the handoff are rerun against the checked-in artifact paths. The most important unresolved items are the empty `Graphics.cs`, IL-invalid `Sprite`/`Seb`/`Image` bodies, general-room `Room.Draw`/`ObjChip.Draw` behavior, and full character animation parity.

## Verification commands

```powershell
python -B tools/social-dev/test_csharp_system_extraction.py
Get-ChildItem -LiteralPath knowledge/fixtures/accepted/visual-port -Filter *.json | ForEach-Object { Get-Content $_.FullName -Raw | ConvertFrom-Json | Out-Null }
git diff --check
git diff -- runtime/social-dev
```

The existing runtime tests remain useful bounded regression gates, but passing them does not establish original visual parity.

## Input fingerprints

The selected source/evidence inputs were hashed during this audit. The highest-value anchors are:

| Input | SHA-256 |
|---|---|
| `Sprite.cs` | `E1DE47B0DBF2887B32B28F4F7B10032326C31E7A54229957E9EF1ED01C7E345A` |
| `Seb.cs` | `933793D58F94C02985FDA9D1BEE0E925B4AE86CD80CAC89CCEC38A8F81760324` |
| `Image.cs` | `24902EC83FE02A386DE846EBA58E87CF23A586AC5C30D478CA5C5B703A9ED217` |
| `ResourceManager.cs` | `D3C3EA9B8367C89EA51F2FFCDA4DB04794C2E238D92DBE8D588B53E65216F736` |
| `Graphics.cs` | `E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855` (zero bytes) |
| `Room.cs` | `E8C8916C12F2902898C0DE6CE8AA59F8CA0C738DD5C482AA64919B775D90662F` |
| `ObjChip.cs` | `49ED2D780CDDCC6CFDA40DE07206DA59B54D5BE5D0BFCB6FF03F479877D13947` |
| `Staff.cs` | `9EAF34D6FAD6265F69D6B10CA9B3C5BAA60F1AD932E4CA7059C7C131292F9D37` |
| `dump.cs` | `4487CBA6916E159AFEFEC2CD1A9ECF0D12D05B2D76126E7099A5D35323967EB2` |
| `SOURCE_FINGERPRINT.json` | `D1A55B8DAD633A4FEA34ABC486CBB6E76B135C3133B54FA42E9CA743137C340B` |

The complete selected input list and byte sizes are retained in the `input_hashes` metadata object of the machine-readable audit files.
