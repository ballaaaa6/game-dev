# Start-game call flow

## Terminal caller

The completed start-game form is owned by `form.TitleForm.Update()` (`sources/raw/1_Click_CSharp_Code update/form/TitleForm.cs:804`, native `RVA 0x1207E44`). The pinned native scan found one direct call to `AppData.NewGame` at `0x01208248`, targeting `AppData.NewGame(string,int,FastVector)` at `RVA 0x1263A70`.

The call is in the title form's normal-state branch. The branch checks the result of `startGameForm_`, reads the selected string/value/vector fields, invokes `NewGame`, and sets title state `3` for fade-out. There is no direct `EventData.StartEvent` call in this branch.

After fade-out reaches state `4`, the native path sets `AppData.frmGame_` flag `0x20` (`FLAG_FROM_TITLE`), calls `FormManager.ChangeCurrentForm(GameForm,false)`, and installs the menu and real-time forms. `GameForm.Init()` consumes `FLAG_FROM_TITLE`; its source path is `sources/raw/1_Click_CSharp_Code update/form/GameForm.cs:667`.

## Start-game subform

`SubForm` form type `73` is the start-game form. `SubForm.Init()` dispatches to `InitStartGame()` (`RVA 0x112A27C`, dispatch site `0x0111EF34`; source line `5452`). `SubForm.Update()` dispatches to `UpdateStartGame()` (`RVA 0x119EF6C`, dispatch site `0x01182794`; source line `6010`).

The recovered start form initializes its selection/value arrays and callbacks. During update it processes the frame/timeout and key state, advances selection, and on a valid selection writes the selected entry id to `value3_` (`0x148`) and sets `select_` to `1` before returning completion through the form manager. Neither recovered body directly calls `AppData.NewGame` or `EventData.StartEvent`.

## Recovered field contract

`SubForm` fields used by the handoff are `type_ 0xF0`, `select_ 0xFC`, `value1_–value5_ 0x140–0x150`, `ary1_ 0x1A8`, and `ary2_ 0x1B0`. The title form reads the completed result at `startGameForm_ + 0xD0`, the selected string at `+0x20`, the selected entry id at `+0x148`, and the vector at `+0x1B0`.

The complete call contract is recorded in [newgame-caller-contract.json](../../../knowledge/fixtures/accepted/visual-port/first-visible-transition/newgame-caller-contract.json) and [startgame-control-flow.json](../../../knowledge/fixtures/accepted/visual-port/first-visible-transition/startgame-control-flow.json).
