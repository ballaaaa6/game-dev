# Visual Class Map

The table separates semantic ownership from implementation status. `KEEP_EXACT` and `PORT_BACKEND` refer to the original contract; `VISUAL_EXTRACT` refers to retaining a bounded visible subset. Native RVAs and source references are machine-readable in `native-method-map.json` and `class-disposition.json`.

| Class | Source anchor | Visual responsibility | Disposition | Evidence status |
|---|---|---|---|---|
| `kairo.unity.ui.Sprite` | `KairoEngine/kairo.unity.ui/Sprite.cs` | One decoded sprite record: crop, source texture, translation, flip, blend, color, frame. | `KEEP_EXACT` | Field layout is clear; getters and `get_Item` are damaged. |
| `kairo.unity.ui.Seb` | `KairoEngine/kairo.unity.ui/Seb.cs` | SEB frame/layer composition, bounds, anchors, and draw variants. | `KEEP_EXACT` | Declarations and native methods exist; several bodies are unsafe to port. |
| `kairo.unity.ui.Image` | `KairoEngine/kairo.unity.ui/Image.cs` | OPT/image ownership, dimensions, pixels, SEB association, use count. | `PORT_BACKEND` | Semantic surface is known; Unity image backend is replaceable. |
| `kairo.unity.ui.ImageAtlas` | `KairoEngine/kairo.unity.ui/ImageAtlas.cs` | Atlas packing, compaction, atlas-to-image resolution. | `PORT_BACKEND` | Native declarations and asset evidence exist; packing needs fixtures. |
| `kairo.unity.ui.ImageAtlasManager` | `KairoEngine/kairo.unity.ui/ImageAtlasManager.cs` | Atlas lifecycle and lookup singleton. | `PORT_BACKEND` | Method surface and native entry points are known. |
| `kairo.unity.ui.ResourceManager` | `KairoEngine/kairo.unity.ui/ResourceManager.cs` | Grouped image/SEB loading and render wrappers. | `KEEP_EXACT` | `AppData` group fields and native render methods confirm topology. |
| `kairo.unity.ui.Graphics` | `KairoEngine/kairo.unity.ui/Graphics.cs` | Clip, color, scale, image draw backend. | `PORT_BACKEND` | Update source is zero bytes; native dump is the primary contract. |
| `data.RoomData` | `data/RoomData.cs` | Floor image selector, map/object topology, room source data. | `VISUAL_EXTRACT` | Data fields are useful; gameplay fields remain out of scope. |
| `data.FurnitureData` | `data/FurnitureData.cs` | Furniture SEB/image selectors, category/frame and pass-map metadata. | `VISUAL_EXTRACT` | Loader and selectors are visible; draw bodies contain IL damage. |
| `data.StaffData` | `data/StaffData.cs` | Character identity, source IDs, action/skill metadata used by visible selection. | `VISUAL_EXTRACT` | Data contract is available; full simulation fields are not needed. |
| `game.MapChip` | `game/MapChip.cs` | Isometric floor, extension, edge, and map-chip effects. | `VISUAL_EXTRACT` | Projection arithmetic and native draw RVAs are available. |
| `game.ObjChip` | `game/ObjChip.cs` | Furniture/object/wall draw, direction, parent/child, frame, placement projection. | `VISUAL_EXTRACT` | Native draw/wall evidence is strong for bounded room; general body is damaged. |
| `game.Room` | `game/Room.cs` | Grid construction, door binding, draw ordering, object and staff ownership. | `VISUAL_EXTRACT` | Native bounded room contracts exist; general draw body is damaged. |
| `game.Staff` | `game/Staff.cs` | Character position, SEB selection, frame progression, alpha/scale, draw. | `VISUAL_EXTRACT` | Native draw methods and resource access are known; animation needs fixtures. |
| `game.Camera` | `game/Camera.cs` | Camera position/base offsets and target projection inputs. | `KEEP_EXACT` | Native getters/setters and source declarations are available. |
| `form.GameForm` | `form/GameForm.cs` | Screen size and outer draw host. | `PORT_BACKEND` | Platform surface is replaceable; `Draw` native entry exists. |
| `main.AppData` | `KairoEngine/main/AppData.cs` | Resource group ownership and shared draw helpers. | `VISUAL_EXTRACT` | Resource fields are clear; class also contains broad gameplay/UI state. |
| `main.Main` | `KairoEngine/main/Main.cs` | Lifecycle boundary around create/update/draw. | `PORT_BACKEND` | Native lifecycle RVAs exist; Unity host must be replaced. |
| `game.Player` | `game/Player.cs` | World/room/staff state consumed by visible scene. | `VISUAL_EXTRACT` | Retain only scene state; simulation is cut. |
| `game.GameObject` | `game/GameObject.cs` | Shared visible object/state base used by scene objects. | `VISUAL_EXTRACT` | Raw/update source is evidence; only visible fields are in scope. |
| `game.routeSearch.Astar` | `game.routeSearch/Astar.cs` | Optional route output that can change visible staff position. | `VISUAL_EXTRACT` | Native node construction exists; full planner semantics are not required. |
| `game.routeSearch.Node` | `game.routeSearch/Node.cs` | Position/path node data if a visual movement trace needs it. | `VISUAL_EXTRACT` | Small data surface; no renderer ownership. |
| `data.JobData` | `data/JobData.cs` | Character/job labels and selectors that may affect visible identity. | `VISUAL_EXTRACT` | Keep only source-derived visible selectors. |
| `data.SkillData` | `data/SkillData.cs` | Action/skill visual selector metadata. | `VISUAL_EXTRACT` | Keep only proven action/SEB/frame dependencies. |
| `util.Vector2D` | `util/Vector2D.cs` | Source coordinate primitive used by map/object/camera projection. | `KEEP_EXACT` | Primitive semantics are directly consumed by visual code. |

## Dependency boundary

The dependency graph intentionally stops at data and backend interfaces. It does not promote `Player`, `Astar`, `JobData`, or `SkillData` into renderer authorities; they are retained only where a field or method is proven to affect visible output.
