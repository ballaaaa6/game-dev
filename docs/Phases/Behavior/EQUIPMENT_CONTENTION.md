# Equipment Contention

Status: `CLOSED_RESERVED_VECTOR_CONTENTION`

`ObjChip.GetUsersNum` at `0x12C4A70` returns the length of `reservedStaffs_` at `0x70`; it ignores the active-user vector and workstation owner. `Staff.GotoEquip` checks this count before reserving a type-1/type-4 target. `ReserveUse` appends the reservation, and `OnUseComplate` removes it and increments the use counter up to 99.

The native code proves a reservation-based single-thread decision, not a queue, lock, capacity policy, or fairness policy.

Evidence: [`equipment-user-count-contract.json`](../../../knowledge/fixtures/accepted/living-core-closure/equipment-user-count-contract.json), [`equipment-contention-contract.json`](../../../knowledge/fixtures/accepted/living-core-closure/equipment-contention-contract.json ).
