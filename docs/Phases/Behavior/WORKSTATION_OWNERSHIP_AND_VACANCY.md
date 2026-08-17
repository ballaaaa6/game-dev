# Workstation Ownership and Vacancy

Status: `CLOSED_OWNER_BASED_RAW_ORDER`

`ObjChip.Init` initializes `staffId_` at `0x78` to `-1`. `Room.GetStaffEmptyObjTypeOf` at `0x12CF178` scans the raw chip vector and returns the first installed type-2 chip whose owner is `-1`. `Room.AddStaff` writes both the staff `deskId_` and the chip owner. The original selector contains no fairness queue, randomization, or rotation.

`Room.ThereIsEmptyDesk` is only a broad boolean and is not a substitute for the exact selector.

Evidence: [`workstation-vacancy-ownership-contract.json`](../../../knowledge/fixtures/accepted/living-core-closure/workstation-vacancy-ownership-contract.json), [`desk-selection-fixtures.json`](../../../knowledge/fixtures/accepted/living-core-closure/desk-selection-fixtures.json ).
