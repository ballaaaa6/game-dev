# Visual Method Map

This is the human-readable index of critical methods. The complete machine-readable records include source references, native addresses, callers, callees, reliability, and next investigation. A decompiled body containing IL annotations is not considered a safe implementation.

## Core resource and composition methods

| Class / methods | Disposition | Why |
|---|---|---|
| `Sprite.FrameNo`, `TexId`, `U`, `V`, `W`, `H`, `TransX`, `TransY`, `ReverseU`, `ReverseV`, `Blend`, `Color`, `get_Item`, `set_Item` | `KEEP_EXACT` / `NEEDS_NATIVE_TRACE` at method level | The field indexes and names are the original format contract; several accessors are IL-invalid and have native getters. |
| `Seb.GetSprites`, `GetSprite`, `GetMaxFrame`, `Frame`, `GetBoundingRect`, `GetPixelRect` | `KEEP_EXACT` / `NEEDS_NATIVE_TRACE` | Frame/layer and bounds semantics are essential to parity; native entry points exist. |
| `Seb.Render*`, `Draw*`, `DrawAnchor`, `DrawRatio`, `DrawRepeat` | `NEEDS_NATIVE_TRACE` | Overload shape is known, but draw math and layer order cannot be recovered from damaged bodies alone. |
| `Image.Load`, `LoadOptimize`, `GetOptimize`, `GetOptimizeSeb`, `Use`, `Unuse`, `Resize`, `SetImageAtlasId` | `PORT_BACKEND` / `NEEDS_NATIVE_TRACE` | Preserve OPT/image semantics while replacing Unity storage; use native and binary fixtures for ambiguous branches. |
| `ImageAtlas.*`, `ImageAtlasManager.*` | `PORT_BACKEND` | Atlas storage is a backend concern, but atlas identity and lookup semantics remain original. |
| `ResourceManager.LoadImage`, `LoadSeb`, `Load`, `GetImage`, `RenderSeb*`, `DrawSeb*` | `KEEP_EXACT` / `NEEDS_NATIVE_TRACE` | Group identity and wrapper semantics are visual contracts; implementation bodies are damaged in key overloads. |
| `Graphics.SetClip`, `GetClip`, `SetColor`, `Scale`, `DrawImage` | `PORT_BACKEND` / `NEEDS_NATIVE_TRACE` | `Graphics.cs` is empty in the update; native dump and output fixtures are required. |

## Scene methods

| Class / methods | Disposition | Why |
|---|---|---|
| `MapChip.Draw`, `DrawFloor`, `DrawExtentionFloor` | `VISUAL_EXTRACT` with native verification | These are direct room visual passes; source projection constants and native RVAs are available. |
| `ObjChip.DrawWall`, `Draw`, `GetDirectionVector`, `GetStandingPositions`, `IsPassable` | `VISUAL_EXTRACT` / `NEEDS_NATIVE_TRACE` | Retain object/wall composition and visible placement; do not import interaction/update branches. |
| `Room.InitMapChips`, `InitObjChips`, `SetupBigChipsParent`, `PlaceDoor`, `InitStaffs`, `Draw`, `GetXbyIndex`, `GetYbyIndex` | `VISUAL_EXTRACT` / `NEEDS_NATIVE_TRACE` | Construction and coordinate contracts are needed; `Draw` has a heavily damaged body. |
| `FurnitureData.Load`, `Draw`, `DrawParamIcon*` | `VISUAL_EXTRACT` / `NEEDS_NATIVE_TRACE` | Selectors are useful; the visual draw overloads must be checked against furniture fixtures. |
| `Camera.SetPosition`, `GetX`, `GetY`, `GetBaseX`, `GetBaseY`, `SetTargetPos` | `KEEP_EXACT` | Camera arithmetic is a semantic boundary shared by scene and host. |

## Character and lifecycle methods

| Class / methods | Disposition | Why |
|---|---|---|
| `Staff.Init`, `ChangeSeb`, `Draw`, `DrawScale`, `DrawStaff`, `SetPos`, `AdvanceSebFrame` | `VISUAL_EXTRACT` / `NEEDS_NATIVE_TRACE` | Keep visible source/frame/position behavior; prove animation timing with native or captured fixtures. |
| `Staff.Update`, `SearchRoute`, `Talk` | `CUT_GAMEPLAY` or `NEEDS_NATIVE_TRACE` by branch | Only animation/position output may survive; job, dialogue, reservation, and planning logic is not part of the visual port. |
| `AppData.DrawSeb`, `DrawSebLine`, `DrawSebFlip`, `DrawSebScale` | `VISUAL_EXTRACT` / `NEEDS_NATIVE_TRACE` | These are shared draw helpers and native bridge points, not a reason to port all of `AppData`. |
| `GameForm.Draw`, `Main.OnCreate`, `OnUpdate`, `OnDraw` | `PORT_BACKEND` / `NEEDS_NATIVE_TRACE` | Replace Unity lifecycle/surface services while preserving visible order and screen dimensions. |
| `Player.NewGame`, `Update`, `Astar.AddNodeArray` | `CUT_GAMEPLAY` or `VISUAL_EXTRACT` | Retain only scene initialization and proven visible position outputs. |

## Reading rule

If a source method contains `//IL_...`, invalid casts, default/null placeholders, or an empty body, the method record must point to native/asset/fixture evidence instead of copying the decompiled body into a browser implementation.
