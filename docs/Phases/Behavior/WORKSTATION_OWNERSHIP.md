# Workstation Ownership and Reservation

Room.AddStaff finds a type-2 staff slot, writes `Staff.deskId_`, and writes the desk chip's `staffId_`. Staff occupancy is maintained through ObjChip staffs lists as grid cells change. Room.PlaceDesk fills empty type-2 slots from FurnitureData records carrying `FLAG_INIT_DESK` (`16384`).

Equipment and door use reservations are stored in ObjChip.reservedStaffs_. `ReserveUse` appends; `OnUseComplate` removes and caps use count at 99. Removal notifies reserved Staff and desk removal calls OnDeskDestroyed.

The exact vacancy predicate in GetStaffEmptyObjTypeOf and exact GetUsersNum semantics are unknown. No fairness or queue policy is inferred.
