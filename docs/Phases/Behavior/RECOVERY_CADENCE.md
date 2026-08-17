# Recovery Cadence

Status: `CLOSED_NATIVE_RECOVERY_CADENCE`

`Staff.AddRecoveryHpStock` at `0x12D2EB0` sets a 20-frame start countdown and adds stock. `Staff.UpdateRecoveryHp` at `0x12D2C8C` consumes one stock and calls `RecoverHp(1)` on non-negative frames where `frame_%3==0`. When stock reaches zero, the native effect state writes a 40-frame gauge/effect reset and stock remains zero. `RecoverHp` clamps to the computed maximum and clears `FLAG_SLEEPING` at max.

Home recovery is a separate direct `RecoverHp(1)` path in `UpdateStayHome`.

Evidence: [`recovery-cadence-contract.json`](../../../knowledge/fixtures/accepted/living-core-closure/recovery-cadence-contract.json), [`recovery-cadence-native-trace.json`](../../../knowledge/fixtures/accepted/living-core-closure/recovery-cadence-native-trace.json ).
