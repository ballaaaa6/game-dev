# I2 Original App Boundary

Status: PASS_I2_2_ORIGINAL_APP_BOUNDARY

Read-only C# evidence separates the original app loop (`Main.OnUpdate` / `Main.OnDraw` and `FormManagerBase.Execute`), form/input handling (`FormManager`, `GameForm`, `SubForm`), high-level commands (`SubForm.UpdateDevelopStart` to `Player.StartPlanning`), model update (`Room.Update` to `Staff.Update` and `ObjChip.Update`), and draw projection (`GameForm.Draw`, `Room.Draw`). `AppData.ReserveAutoSave` is recorded as a save side effect.

The original develop/planning/window/menu UI is explicitly cut from I2. It is not reintroduced as gameplay controls. The web dashboard operates at product task level and does not execute the C# layer.
