# Work and Recovery Lifecycle

Room.Update ticks Staff before ObjChip. A sitting Staff enters the readable UpdateWork decision chain: typing, equipment, talk, or sleeping branches. Equipment use has visible frame gates at 20, 40, 60, and 70. At completion the chip reservation is released, use count/stock are updated, FurnitureData.recovery_ may add recovery stock, and Staff returns toward the desk.

Recovery stock starts after a 20-frame delay and is consumed through one `RecoverHp(1)` per stock unit. Home recovery also calls `RecoverHp(1)` directly. The low-HP guard is `GetHpRatio() <= 5`; home return is `>=40`.

The exact work HP drain is **unknown**: no readable ordinary-work decrement was found. The exact sleeping flag cadence is also source-limited. These are preserved as unknowns in the machine contract.
