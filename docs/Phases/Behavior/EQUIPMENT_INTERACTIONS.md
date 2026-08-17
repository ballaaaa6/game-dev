# Equipment Interactions

GotoEquip randomly chooses type 1 or type 4, requests a random installed candidate, and accepts it only when `GetUsersNum() <= 0`. It then calls `ReserveUse`, writes the target object index, and enters move mode 1.

UseEquip has readable phase boundaries at frames 20, 40, 60, and 70. Completion calls `OnUseComplate`; if the FurnitureData recovery value is at least 1 and HP is below max, that value is added to recovery stock with a 20-frame delay. The action then returns toward the desk.

RemoveObj notifies reserved Staff with OnEquipDestroyed. Exact type-4 parent/child target handling, direction vectors, and reservation-count internals remain source-limited.
