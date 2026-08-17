# V2 Native Graphics Contract

## Pinned inputs

- APK package: `net.kairosoft.android.snsdev_en`
- APK SHA-256: `fa0e9e3a843732258fc05b2611a8e0f5be6f7e95f2141a53f31fb082322fe2bf`
- Native dump SHA-256: `4487CBA6916E159AFEC2CD1A9ECF0D12D05B2D76126E7099A5D35323967EB2`
- Native library SHA-256: `364893401FCF7FC2380AE64291783EDF7B95EECEA4775041C3F4C8C081B4D54A`
- Native binary: `knowledge/sources/phase3a_apk_probe/raw/libil2cpp.so`
- Dump: `knowledge/sources/phase3a_apk_probe/il2cpp_dump/dump.cs`

The managed `Graphics.cs` update file is empty, so the pinned native dump, disassembly, and call sites are authoritative for this phase. The machine-readable method and field contracts are in `knowledge/fixtures/accepted/visual-port/v2/`.

## Method surface

| Surface | Native RVAs | Recovered claim |
| --- | --- | --- |
| Clip | `0x1C07F5C`, `0x1C080E4`, `0x1C0812C`, `0x1C082A8`, `0x1C08694`, `0x1C088C0`, `0x1C09A74` | Stack, set, intersect, clear, and active integer-return path |
| DrawImage | `0x1C0D87C`, `0x1C0EF98` | Full-image and crop overload command mapping |
| DrawScaledImage | `0x1C0F0C8` | Independent source/destination geometry |
| Internal raster boundary | `0x1C0DAC4`, `0x1C10388` | Matrix/flip/culling/optimization dispatch and bitmap backend entry; final pixels deferred |
| Color | `0x1C09D60`, `0x1C0CF3C`, `0x1C1B19C`, `0x1C1B544` | AARRGGBB packing, clamping, and storage |
| Flip/scale/filter | `0x1C1B54C`, `0x1C07C6C`, `0x1C1C0B4`, `0x1C1C0BC`, `0x1C1C0C8` | State stores, percent scale, and filter flag |
| Render mode | `0x1C07C74`, `0x1C17278`, `0x1C17BDC`, `0x1C1BF20` | Replace/Add/Subtract defaults and stacks |
| Blend mode | `0x1C1BE18`, `0x1C1D0D0`, `0x1C1D198`, `0x1C1D1A0`, `0x1C1D1A8`, `0x1C1D3E4` | Mode/color stores and stack |
| Origin/matrix | `0x1C1B778`, `0x1C1DC6C`, `0x1C1DDA4`, `0x1C1DF10`, `0x1C1C3A0`, `0x1C1013C`, `0x1C1C55C`, `0x1C085E8` | Native transform surface pinned; runtime promotion deferred |

## State layout and defaults

The key native fields are `flipmode_` at `0x40`, `linearFilter_` at `0x44`, `color_` at `0x58`, `scale_` at `0x5C`, translation at `0x60/0x64`, render operator/source/destination at `0x150/0x154/0x158`, blend mode/color at `0x170/0x178`, and clip state at `0x188` onward. `ResetRender` restores black `0xFF000000`, scale 100, flip none, Replace `(255,0)`, blend none, and cleared clip. The filter bool is zero-initialized false; the reset routine does not explicitly write it.

## DrawImage and flip

The crop overload passes source `(sx, sy, width, height)` and destination `(dx, dy, width, height)` to `_drawImage`. The scaled overload passes independent source dimensions. The pinned `_drawImage` body makes the flip matrix explicit: mode 1 calls `Matrix.ScaleTemporary(-1,+1,sourceWidth/2,sourceHeight/2)`, mode 2 calls `(+1,-1)`, and mode 3 calls `(-1,-1)`, all around the source center. Modes 4 and 5 both call `Matrix.RotateTemporary(-90 degrees, sourceWidth/2, sourceHeight/2)` in this binary; their final backend pixel orientation remains deferred.

The full-image overload is not always a single backend call. When `Image.optimizePass_` and block metadata are active, `DrawImage` enumerates optimized rows and columns and routes each block through the internal crop path. `_drawImage` also contains atlas/custom-image dispatch before `_drawBitmap`. The V2 adapter retains a logical-image command and records this native block/asset boundary instead of claiming that one logical command is a native backend call sequence.

## Color, render, and blend

`GetColorOfRGB` returns `0xFFRRGGBB`; the alpha overload returns `0xAARRGGBB`. Seb sprite blend flags are not treated as generic browser blend guesses: the native per-sprite path pushes `Add(alphaRatio, 255-alphaRatio)`, `Add(alphaRatio, 255)`, or `Subtract(alphaRatio, 255)` for flags 1, 2, and 3 respectively, then pops the render mode. Alpha scaling uses the recovered integer rounding path recorded in `color-blend-contract.json`.

## Static Seb and ResourceManager call flow

The pinned wrappers and `Seb.cs` call sites recover the composition path without executing the game:

- `ResourceManager.DrawSeb` overloads at `0x1C52E2C`, `0x1C52F18`, and `0x1C5299C` select the current or explicit frame, apply signed `frame % maxFrame` for explicit frames, and tail-call the common `Seb._draw` path at `0x1C5E448`.
- `Seb._draw` selects `GetSpritesLocal` for `lineNo=-1` or `GetSpriteLocal` for a requested layer, then calls the per-record routine at `0x1C61714` in source layer order.
- Positive texture IDs resolve through `Seb.GetImage(Image[], texId)` and reach the crop `DrawImage` overload. The destination adds `TransX/TransY`; source geometry remains `(U,V,W,H)`.
- `TEXID_NONE`, `TEXID_HIDELINE`, and `TEXID_HIDERECT` are no-draw cleanup paths. `TEXID_FRECT`, `TEXID_RECT`, and `TEXID_LINE` call native `FillRect`, `DrawRect`, and `DrawLine`; the command adapter defers their primitive backend output.
- `ResourceManager.GetImage` at `0x1C53DA0` probes `CustomImages` at `this+0x60` before the sparse `img` array at `this+0x10`. The V1 contract loader exposes only the proven sparse slots, so custom-image injection remains a static boundary.
- Anchor wrappers derive an offset through `GetSebAnchorPosition` at `0x1C53140`, set `Seb.offset_` at `0x1C5324C`, draw, and clear it at `0x1C62328`. `RenderSeb` additionally obtains `DepthInfo[]` at `0x1C61CE0`; V2 keeps depth and anchor command emission deferred.

The complete machine-readable static call-flow record is `knowledge/fixtures/accepted/visual-port/v2/graphics-static-recovery.json`.

## Matrix and clip boundary

`SetClip` and `ClipRect` transform through `GetTransRect` before native clip storage. `Matrix.MapPoints` uses the affine mapping `x' = x*m[0] + y*m[3] + m[6]` and `y' = x*m[1] + y*m[4] + m[7]`. `ClipRect` then intersects the transformed rectangle with the active clip; `GetClip` uses `fcvtzs` truncation toward zero. The V2 command schema preserves caller geometry and implements the proven identity/no-transform intersection path; it does not invent a browser matrix for deferred transform state.

## Limits

The static source proves state transitions, call flow, matrix dispatch, and command geometry, not the final framebuffer. `_drawBitmap` shader behavior, texture sampling/filtering, premultiplied-alpha handling, pixel-edge clipping, and final blend/primitive/rotated pixels remain deferred in `unknowns.json`. Per the current task boundary, no emulator, ADB, live-app, network, or runtime capture is used to close those gaps.
