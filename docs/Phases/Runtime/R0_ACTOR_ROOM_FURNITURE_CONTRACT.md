# R0 Actor, Room, and Furniture Contract

The authoritative machine contracts are:

- `actor-runtime-contract.json`
- `room-runtime-contract.json`
- `furniture-instance-contract.json`

## Actor

The actor contract separates original static identity, original mutable Staff state, derived helpers, and product-only state. `Staff.hp_` is at `0xE8`; `state_` is at `0x70`; `moveMode_` is at `0xA8`; `deskId_` is at `0xB8`; route/target/timer/action fields retain their native identities. Product task identifiers are outside the original state.

## Room and topology

The main-display MapChip is `14x14` (`196` cells) while the Room ObjChip occupancy grid is `10x10` (`100` cells). They remain separate. Room membership and raw ObjChip traversal are preserved. Desk selection is the first raw-order installed type-2 chip with owner `-1`.

## Furniture

The instance contract keeps owner, active users, and reserved users distinct. Role counts are `10` workstation, `49` recovery equipment, `43` equipment without proven HP effect, and `1` door. REST/SOCIAL furniture roles are not invented.


R0 execution boundary: inline, static/contract only, no subagents, no emulator/ADB, no network, no server, no V8, no MapChip or Renderer changes, and no living-core implementation.
