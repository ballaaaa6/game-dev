# I0 Tick Order and RNG Autonomy

Room updates Staff in insertion/vector order before ObjChip updates. Staff observes its current frame, updates recovery, applies the low-HP guard, dispatches the current state handler, processes movement/arrival, commits timer and cleanup mutations, and is projected only afterward.

`ReplayRng` implements AppData bounded and inclusive draws plus Lib inclusive draws. Replay values and fallback state are serialized with the canonical snapshot, and every draw is trace-visible. The living core never calls `Math.random` or wall-clock time.

The targeted native anchors for `UpdateWork` (`0x12D4A7C`) and sleeping stock (`0x12D2EC8`) are recorded in `native-implementation-spotchecks.json`. The implementation preserves the frame-20 autonomy gate, native threshold ordering, frame-200 sleeping stock cadence, and ordinary-work no-drain rule.
