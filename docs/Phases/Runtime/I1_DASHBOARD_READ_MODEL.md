# I1 Dashboard Read Model

Status: `PASS_I1_10_DASHBOARD_READ_MODEL`

The read model keeps `task` and `living` namespaces side by side. Valid examples include `IDLE_NO_TASK + STATE_WORK`, `ASSIGNED + STATE_TALK`, `RUNNING + STATE_WORK`, `RUNNING + STATE_USE_EQUIPMENT`, `RUNNING + STATE_STAY_HOME`, and terminal task + baseline Staff state.

`living.state`, `moveMode`, HP, desk, equipment, colleague, cell, and derived display status remain visible. Clients read product status from `task.status`; they never infer it from `STATE_WORK`, `STATE_DEVELOP`, equipment, talk, or home.
