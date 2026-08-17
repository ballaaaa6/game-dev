# V5 Room Fixture Matrix

The fixture matrix covers all 18 native RoomData records. Room:0 is the full static scene because its constructor and structural facility bindings are closed by the available evidence. Rooms 1-17 load their complete raw topology and selectors but stay `topology_only`; their constructor evidence contains zero native furniture bindings.

The matrix includes:

- all 18 English room names and native floor/wall/door selectors;
- all 18 door cells and raw type/direction counts;
- source-row SHA-256 values;
- the room:0 full-static, persistent 4x4, and room:1 nonzero-floor addition-preview fixtures;
- rejection cases for unsupported native floor/context dimensions.

The source of truth is `knowledge/fixtures/accepted/visual-port/v5/roomdata-topology.json`; the fixture execution manifest is `room-fixture-manifest.json`.
