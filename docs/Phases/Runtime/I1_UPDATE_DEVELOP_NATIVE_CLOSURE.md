# I1 UpdateDevelop Native Closure

Status: `PASS_I1_3_MINIMAL_DEVELOP_SEMANTICS`

Native `Staff.UpdateDevelop` is at RVA `0x12D3D48`. `developState_` is at offset `0x188`, and the ten-way table at `0x636660` maps 0..9 to:

`0x12D3ECC, 0x12D3F68, 0x12D4150, 0x12D420C, 0x12D4288, 0x12D464C, 0x12D4398, 0x12D464C, 0x12D43EC, 0x12D44AC`.

State 6 reads HP at offset `0xE8` and `stepFinished_` at `0x190`, selecting Develop-specific down/wait/finish behavior. Enemy interruption uses `developStateBackup_` at `0x1B0` and temporary state 10. Ordinary `Staff.Update` state 12 returns before office recovery and low-HP routing.

Evidence: `update-develop-native-map.json`, `update-develop-state-machine.json`, `develop-hp-interaction.json`, and `develop-interruption-contract.json`.
