# V3 Native ResourceManager Contract

## Managed and native shape

The pinned `ResourceManager` declaration owns `Image[] img`, `Seb[] seb`, `CustomImages`, `loaded_`, `loadNum_`, and the list/directory/record selectors. Existing native recovery pins `img` at `this+0x10`, `seb` at `this+0x18`, and `CustomImages` at `this+0x60`.

`GetImage(texId)` probes `CustomImages` first, then the group-owned sparse `img[]` slot. V3 preserves that order but does not populate `CustomImages`, because population callers are not statically proven. A null or out-of-range slot is a typed lookup failure; the ID is never shifted into another slot or group.

## Loading

The static overload surface is recorded in `load-semantics.json`:

- `LoadImage(byte[]/InputStream)` delegates to the native `Image.Load` surface.
- `LoadSeb(byte[]/InputStream)` constructs a `Seb` from source bytes/stream.
- `Load(byte[]/JarInflater/directory/RecordStore/Assembly)` enters `LoadReady` then `LoadStart`.
- `LoadTask` owns field assignment and RecordStore/resource-directory selection; external scheduling and completion timing remain deferred.

The V3 fixture layer uses deterministic source-indexed preloading. `loadReady()` and `loadStart()` expose the recovered boundary without inventing a scheduler, callback timing, GPU upload, or async completion event.

## Sparse arrays

Each pack-local INF contract records its original IDs, raw records, flags, source member, source hash, and all gaps through `max_id`. The compatibility layer allocates `max_id + 1` slots and leaves every gap `null`. This preserves the native namespace for furniture, human, avatar, UI, and effect resources.

## Lifetime and atlas boundary

`IndexedImage` retains source identity and a bounded `use()/unuse()` counter. `imageAtlasId` remains `-1` and `atlasRegion` remains `null` for the V3 metadata layer. `getAtlas()` is explicitly deferred. No GPU disposal or atlas ownership is invented.

## Compatibility boundary

`ResourceManagerV3` is imported only by V3 tests and fixture helpers. Existing V1 contracts/parsers remain reused for decoded SEB objects. No production renderer, scene route, gameplay path, or current browser manifest is changed to depend on V3.
