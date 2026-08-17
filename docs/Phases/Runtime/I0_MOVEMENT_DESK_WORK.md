# I0 Movement, Desk Ownership, and Work

Movement uses the source-backed 10x10 ObjChip grid, cardinal Manhattan A*, explicit target filtering, FurnitureData passability data, and route-head consumption. Type 6 is rejected and arrival dispatch remains an 11-way move-mode operation.

Room.AddStaff preserves insertion order, door spawn `[8,4]`, alpha zero, speed three, first raw-order installed vacant type-2 desk selection, and owner/staff desk pairing. The generic NORMAL update then enters GOTO_DESK, SIT_DOWN, and STATE_WORK. Ordinary work does not subtract HP.

S1 and S5 cover startup and raw-order desk contention. S7 covers desk destruction cleanup and fallback without stale ownership or a product task payload.
