# Original Visual Architecture

## Audit boundary

The original visual subsystem is a data-driven 2D renderer with a native Unity backend. The safe port boundary is below the original resource and composition semantics and above Unity texture/file/render services. The browser runtime is not evidence for the original architecture; it is recorded separately in `ORIGINAL_VS_CURRENT_RUNTIME.md`.

## Original pipeline

```text
asset group / resource files
        ↓
ResourceManager.LoadImage / LoadSeb
        ↓
Image.Load / LoadOptimize / GetOptimize / GetOptimizeSeb
        ↓
OPT image metadata + SEB frame data
        ↓
Seb.GetSprites / GetSprite / Frame
        ↓
Sprite fields: FrameNo, TexId, U, V, W, H, X, Y,
              TransX, TransY, ReverseU, ReverseV, Blend, Color
        ↓
ResourceManager.DrawSeb / DrawSebAnchor / RenderSeb / RenderSebAnchor
        ↓
Graphics.SetClip / SetColor / Scale / DrawImage
        ↓
Unity/native texture and raster output
```

`ImageAtlas` and `ImageAtlasManager` sit beside `Image`: they may compact image pixels into atlas storage and resolve atlas-backed images. Their compaction/packing behavior is not a license to replace source crop/offset/frame values with a new manifest.

## Original scene ownership

`RoomData` supplies floor/object maps and source selectors. `Room.InitMapChips` creates the map grid; `Room.InitObjChips` creates the object grid; `SetupBigChipsParent` connects multi-cell objects; and `PlaceDoor` establishes the door/object relationship. `MapChip` owns floor, extension, and edge visual composition. `ObjChip` owns furniture/object/wall visual state, direction, frame, parent, and source data. `Staff` owns visible character selection, position, direction, alpha/scale, and SEB frame progression. `Camera` owns the visible offset/projection inputs. `Room.Draw` is the orchestration point, but its decompiled body is not reliable.

`AppData` owns the original resource group instances and a large set of draw helpers. `Main`/`GameForm` own platform lifecycle and the outer draw/update boundary. `Player` and route search supply world state and positions; their simulation must not be imported merely because the renderer calls into the owning objects.

## Preserved semantics

The port must retain the identity and meaning of:

- `Sprite` crop, source texture ID, translation, flip, blend, color, and frame fields;
- `Image`/OPT dimensions, pixel ownership, expiration, `Use`/`Unuse`, and SEB association;
- `Seb` frame/layer composition, anchor/bounds/pixel-rect queries, and draw variants;
- `ResourceManager` group identity and image/SEB lookup relationships;
- `MapChip` isometric projection and floor/extension ordering;
- `ObjChip` direction, parent/child, furniture selectors, wall composition, and frame state;
- `Room` grid topology, door binding, object/character ordering, and camera offsets;
- `Staff` source selectors, action/direction frame state, position, scale, and visible alpha.

The native room evidence fixes a bounded nine-pass composition and a 14×14 map grid beside a 10×10 object grid. It does not prove every branch of the general decompiled `Room.Draw` body.

## Backend replacement boundary

The browser may replace these services:

| Unity/platform concern | Browser host boundary | Must remain outside the semantic core |
|---|---|---|
| Texture/image object and pixel upload | `Image` backend adapter | OPT dimensions and source identity remain original. |
| File/stream/resource loading | `ResourceManager` source adapter | Group IDs and `img`/`seb` relationships remain original. |
| Native draw surface | `Graphics` backend | Clip, color, scale, blend, flip, and destination semantics remain observable. |
| Unity lifecycle and screen size | `GameForm`/`Main` host adapter | Scene draw order and camera contract remain explicit. |
| Atlas texture storage | `ImageAtlas` backend | Atlas coordinates cannot rewrite source crop semantics. |

`CanvasRenderingContext2D`, DOM image loading, Vite, and browser route state are implementation services, not a new source of truth for original visual data.

## Evidence confidence

High-confidence facts are the pinned asset/native contracts, `AppData` resource field declarations, class/method declarations, the `MapChip` projection arithmetic visible in the source, and the existing native room closure contracts. Low-confidence facts are bodies containing IL annotations, invalid casts, default/null placeholders, or nonsensical control flow. Those are listed in `DECOMPILER_GAPS.md` and assigned `NEEDS_NATIVE_TRACE` or `UNKNOWN`.
