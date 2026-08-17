# Furniture Behavior Model

All 103 FurnitureData records were classified using `type_`, `recovery_`, flags, and actual Staff/Room/ObjChip consumers. Counts: EQUIPMENT_NO_HP_EFFECT_PROVEN=43, DOOR_RECORD=1, WORKSTATION=10, RECOVERY_EQUIPMENT=49.

- Type 2 is the workstation/desk slot class used by Room.PlaceDesk and Staff desk ownership.
- Type 1 and type 4 are the equipment candidate classes used by GotoEquip.
- `recovery_ >= 1` has one proven autonomous consequence: use completion adds recovery stock.
- Type 5 is the door chip class scanned by Room.GetDoorIndex.
- `passMap_` is a data field consumed by native ObjChip.IsPassable; raw topology is not used to infer FurnitureData identity.
- No record is promoted as REST or SOCIAL from names, sprites, or asset selectors. Social goals use pass chips and Staff colleague logic.

The full per-record catalog is `furniture-behavior-catalog.json`. Records preserve exact source-derived names without turning them into unproven semantic roles.
