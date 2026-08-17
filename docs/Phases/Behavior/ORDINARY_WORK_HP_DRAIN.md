# Ordinary Work HP Drain

Status: `CLOSED_NO_ORIGINAL_DRAIN`

Native `Staff.UpdateWork` at `0x12D4A7C` contains the original 20-frame work decision gates, typing progression, sleeping flag, equipment choice, and talk choice. It has no write to `hp_` at `0xE8` and no `RecoverHp` call, positive or negative. Ordinary work therefore preserves HP unless another proven system changes it in the same frame.

HP writes remain limited to initialization, recovery/max correction, combat damage, original-record synchronization, and explicit setters. Equipment recovery adds stock; it does not create a work drain.

Evidence: [`ordinary-work-hp-drain-contract.json`](../../../knowledge/fixtures/accepted/living-core-closure/ordinary-work-hp-drain-contract.json), [`hp-native-write-site-catalog.json`](../../../knowledge/fixtures/accepted/living-core-closure/hp-native-write-site-catalog.json ).
