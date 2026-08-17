# I0 Runtime Foundation

The living core now has explicit numeric Staff states, move modes, flags, raw ObjChip types, canonical Staff/Room/Furniture state, injectable RNG streams, deterministic mutation traces, and a separate visual projection.

Generated data is consumed from `knowledge/fixtures/accepted/runtime/i0-runtime-catalog.json`. It contains all 141 StaffData, 30 JobData, 36 SkillData, and 103 FurnitureData records plus the 18 RoomData grids and frozen scenario fixtures. No browser runtime module imports C#, archives, or knowledge source roots.

`SimulationState.living` is authoritative. `SimulationState.actors` is projected after the behavior commit so the existing visual shell can continue to render without owning behavior semantics.
