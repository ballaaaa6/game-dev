# V1 Native Recovery

## Pinned native inputs

- APK SHA-256: `fa0e9e3a843732258fc05b2611a8e0f5be6f7e95f2141a53f31fb082322fe2bf`
- Native dump SHA-256: `4487CBA6916E159AFEFEC2CD1A9ECF0D12D05B2D76126E7099A5D35323967EB2`
- Native library SHA-256: `364893401FCF7FC2380AE64291783EDF7B95EECEA4775041C3F4C8C081B4D54A`

The claim-level map records 26 recovered method records. Every record includes the pinned APK/dump hashes, C# source reference, C# reliability, fixture or group references, native RVA, proof class, and observed result or explicit deferred status.

## Recovered method families

### Sprite

`Sprite.get_FrameNo`, `get_TexId`, `get_U`, `get_V`, `get_W`, `get_H`, `get_X/get_TransX`, `get_Y/get_TransY`, `get_ReverseU`, `get_ReverseV`, `get_Blend`, and `get_Color` are mapped to native accessor slots and corroborated by the conversion-buffer layout. The source label is `sources/raw/1_Click_CSharp_Code update/KairoEngine/kairo.unity.ui/Sprite.cs:9-367`.

### Seb

`Seb.GetBRect/GetBoundingRect` is `FORMAT-PROVEN` for selected destination-rectangle unions. `Seb.GetPixelRect` is `FORMAT-PROVEN_FALLBACK` when pixel bounding rectangles are absent. `Seb.GetDepthInfo` has a pinned overload set but is `DEFERRED` because the selected SEB payloads do not expose the native depth-line data needed for numeric semantics. The source labels are `sources/raw/1_Click_CSharp_Code update/KairoEngine/kairo.unity.ui/Seb.cs:149-187,4661-6255,7560-7864` and `dump.cs:L203950-L204020,L204847-L205033`.

### Image

`Image.LoadOptimize`, `GetOptimize`, `GetOptimizeSeb`, `Use/Unuse`, `Resize`, and `SetImageAtlasId` are pinned. OPT decoding and logical pixel reconstruction are format-proven for the selected records. `GetOptimizeSeb` is unexercised on the standard OPT-only selection; `Resize` raster parity and atlas region promotion remain deferred. The source label is `sources/raw/1_Click_CSharp_Code update/KairoEngine/kairo.unity.ui/Image.cs:2484-5535,5584-5672,6035,6268-6294,8433-8455,8753-8800`.

### ResourceManager

`ResourceManager.LoadImage/LoadSeb`, `Load`, `LoadReady`, `LoadStart`, and `GetImage` are pinned. Synchronous sparse lookup is format-proven for the source-indexed bindings. Async callback scheduling is deferred because it is not needed for the selected synchronous parity scope. The source labels are `sources/raw/1_Click_CSharp_Code update/KairoEngine/kairo.unity.resource/ResourceManager.cs:2193-2210,2526-2755,2715-2755,3461-3501,7585`.

## Proof classes and limits

Format proof comes from source bytes, selected fixture decoders, stable hashes, and runtime tests. Native proof comes from pinned RVAs and the immutable APK/dump inputs. `FORMAT-PROVEN` and `NATIVE-RVA-PINNED` are separate evidence dimensions; an RVA does not close a missing format payload. Depth, atlas, resize raster behavior, `optimizeSeb`, asynchronous scheduling, and unproven group membership stay deferred or unknown.

## V2 stop decision

V2 has not started. Native recovery should not be extended into deferred branches without a new fixture or native payload that can be independently checked.
