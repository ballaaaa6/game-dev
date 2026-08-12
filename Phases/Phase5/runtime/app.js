(function () {
  "use strict";

  const {
    OfficeRuntime,
    DirectPathProvider,
    ExplicitCollisionProvider,
    SeatProvider,
    LocaleStore
  } = window.Wave5Runtime;
  const { TaskSystem } = window.Wave6TaskSystem;
  const { LocalStorageTaskRepository } = window.Wave6TaskRepository;

  const $ = (id) => document.getElementById(id);
  const canvas = $("officeCanvas");
  const ctx = canvas.getContext("2d");
  ctx.imageSmoothingEnabled = false;
  const imageCache = new Map();
  let manifest;
  let runtime;
  let backgroundImage;
  let playing = false;
  let timer = null;
  let taskSystem;
  let taskRepository;
  let selectedTaskId = null;
  let taskErrorMessage = "";

  function loadImage(url) {
    if (!imageCache.has(url)) {
      const image = new Image();
      image.onload = render;
      image.src = url;
      imageCache.set(url, image);
    }
    return imageCache.get(url);
  }

  function drawObject(objectCommand) {
    const drawCommand = (objectCommand.commands || [])[0];
    const asset = drawCommand && drawCommand.asset;
    if (asset && asset.url) {
      const image = loadImage(asset.url);
      if (image.complete && image.naturalWidth > 0) {
        const [dx, dy] = drawCommand.destination;
        if (Array.isArray(drawCommand.source_rect) && drawCommand.source_rect.length === 4) {
          const [sx, sy, sw, sh] = drawCommand.source_rect;
          const [dw, dh] = Array.isArray(drawCommand.draw_size) ? drawCommand.draw_size : [sw, sh];
          ctx.drawImage(image, sx, sy, sw, sh, dx, dy, dw, dh);
        } else if (Array.isArray(drawCommand.draw_size) && drawCommand.draw_size.length === 2) {
          ctx.drawImage(image, dx, dy, drawCommand.draw_size[0], drawCommand.draw_size[1]);
        } else {
          ctx.drawImage(image, dx, dy);
        }
        return;
      }
    }

    const marker = objectCommand.fallback_marker || { x: 0, y: 0, label: objectCommand.type || "OBJECT" };
    ctx.save();
    ctx.fillStyle = "rgba(15, 23, 42, .75)";
    ctx.strokeStyle = "rgba(103, 232, 249, .8)";
    ctx.fillRect(marker.x - 12, marker.y - 10, 24, 18);
    ctx.strokeRect(marker.x - 12, marker.y - 10, 24, 18);
    ctx.fillStyle = "#d9f9ff";
    ctx.font = "10px ui-monospace, monospace";
    ctx.textAlign = "center";
    ctx.fillText(marker.label.replace("OBJ_TYPE_", ""), marker.x, marker.y + 3);
    ctx.restore();
  }

  function drawActor(actorCommand, actor) {
    const x = actor.position[0];
    const y = actor.position[1];
    const record = actorCommand;
    ctx.save();
    const focusedTask = selectedTask();
    if (focusedTask && focusedTask.assignee_id && focusedTask.assignee_id !== actor.id) {
      ctx.globalAlpha = 0.36;
    }
    if (focusedTask && focusedTask.assignee_id === actor.id) {
      ctx.strokeStyle = "rgba(103, 232, 249, .9)";
      ctx.lineWidth = 2;
      ctx.strokeRect(x - 7, y - 14, 48, 62);
    }
    ctx.fillStyle = "rgba(0, 0, 0, .24)";
    ctx.beginPath();
    ctx.ellipse(x + 9, y + 29, 12, 4, 0, 0, Math.PI * 2);
    ctx.fill();

    for (const command of record.commands || []) {
      const image = loadImage(command.asset.url);
      if (image.complete && image.naturalWidth > 0) {
        const [sx, sy, sw, sh] = command.source_rect;
        const [dx, dy] = command.destination;
        ctx.drawImage(image, sx, sy, sw, sh, dx, dy, sw, sh);
      } else {
        ctx.fillStyle = command.layer === "face" ? "#f7c99b" : "#6c8cff";
        const [dx, dy] = command.destination;
        const [, , sw, sh] = command.source_rect;
        ctx.fillRect(dx, dy, sw, sh);
      }
    }

    ctx.fillStyle = "#ffffff";
    ctx.font = "11px ui-monospace, monospace";
    ctx.textAlign = "left";
    ctx.fillText(actor.name, x - 4, y - 6);
    if (record.status !== "draw_command_ready") {
      ctx.fillStyle = "#fbbf24";
      ctx.fillText(record.status, x - 4, y + 44);
    }
    ctx.restore();
  }

  function drawBubble(bubble) {
    const actor = runtime.getAgent(bubble.actor_id);
    const x = actor.position[0] - 30;
    const y = actor.position[1] - 54;
    const width = Math.min(230, Math.max(100, bubble.text.length * 7 + 20));
    ctx.save();
    ctx.fillStyle = "rgba(255, 255, 255, .94)";
    ctx.strokeStyle = "#162338";
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.roundRect(x, y, width, 30, 7);
    ctx.fill();
    ctx.stroke();
    ctx.fillStyle = "#162338";
    ctx.font = "12px sans-serif";
    ctx.textAlign = "left";
    ctx.fillText(bubble.text.slice(0, 34), x + 9, y + 19);
    ctx.restore();
  }

  function drawNotifications(notifications) {
    notifications.slice(-3).forEach((notification, index) => {
      const x = 12;
      const y = 12 + index * 32;
      ctx.save();
      ctx.fillStyle = "rgba(15, 23, 42, .9)";
      ctx.fillRect(x, y, 240, 25);
      ctx.strokeStyle = "rgba(110, 231, 183, .8)";
      ctx.strokeRect(x, y, 240, 25);
      ctx.fillStyle = "#d1fae5";
      ctx.font = "11px ui-monospace, monospace";
      ctx.textAlign = "left";
      ctx.fillText(`[graph:${notification.graph_id}] ${notification.text}`.slice(0, 36), x + 7, y + 16);
      ctx.restore();
    });
  }

  function render() {
    if (!runtime) return;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    if (backgroundImage && backgroundImage.complete && backgroundImage.naturalWidth > 0) {
      ctx.drawImage(backgroundImage, 0, 0, canvas.width, canvas.height);
    } else {
      ctx.fillStyle = "#273548";
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      ctx.fillStyle = "#9fb0c6";
      ctx.font = "14px sans-serif";
      ctx.fillText("Loading floor0.png…", 20, 30);
    }

    const commands = runtime.renderCommands();
    const agents = [...runtime.agents.values()];
    const objectById = new Map(commands.objects.map((command) => [command.id, command]));
    const actorById = new Map(commands.actors.map((command) => [command.actor_id, command]));
    commands.draw_order.forEach((item) => {
      if (item.kind === "object") {
        const object = objectById.get(item.id);
        if (object) drawObject(object);
        return;
      }
      const command = actorById.get(item.id);
      const actor = agents.find((candidate) => candidate.id === item.id);
      if (command && actor) drawActor(command, actor);
    });
    commands.bubbles.forEach(drawBubble);
    drawNotifications(commands.notifications);
    updatePanels(commands);
    updateTaskPanels();
  }

  function updatePanels(commands) {
    $("tickLabel").textContent = `tick ${runtime.clock.value}`;
    $("runtimeStatus").textContent = `READY · tick ${runtime.clock.value}`;
    const selectedId = $("actorSelect").value || "adapter.actor.0";
    const actor = runtime.getAgent(selectedId);
    const command = commands.actors.find((item) => item.actor_id === selectedId);
    $("diagnostics").textContent = JSON.stringify({
      actor: {
        id: actor.id,
        state: actor.state,
        position: actor.position,
        movement: actor.movement,
        task_id: actor.taskId,
        task_status: actor.taskStatus,
        selectors: actor.selectors
      },
      furniture: commands.objects.map((object) => ({
        id: object.id,
        type: object.type,
        status: object.status,
        source_contract: object.source_contract,
        crop_contract: object.crop_contract,
        placement_contract: object.placement_contract
      })),
      draw: command,
      policy: {
        legacy_equivalence: false,
        timer: commands.timer_policy,
        animation: runtime.animationPolicy
      }
    }, null, 2);
    const log = $("eventLog");
    log.innerHTML = "";
    runtime.events.records.slice(-18).reverse().forEach((event) => {
      const item = document.createElement("li");
      item.textContent = `t${event.tick} #${event.sequence} ${event.type}`;
      log.appendChild(item);
    });
    $("stateSelect").value = actor.state;
  }

  function rebuildActorSelect() {
    const select = $("actorSelect");
    select.innerHTML = "";
    runtime.agents.forEach((agent) => {
      const option = document.createElement("option");
      option.value = agent.id;
      option.textContent = `${agent.name} (${agent.id})`;
      select.appendChild(option);
    });
  }

  function selectedActor() {
    return runtime.getAgent($("actorSelect").value || "adapter.actor.0");
  }

  function selectedTask() {
    if (!taskSystem || !selectedTaskId) return null;
    try {
      return taskSystem.getTask(selectedTaskId);
    } catch (error) {
      return null;
    }
  }

  function setTaskError(error) {
    taskErrorMessage = error ? String(error.message || error) : "";
  }

  function runTaskAction(action) {
    const task = selectedTask();
    if (!task) {
      setTaskError(new Error("select a task first"));
      render();
      return;
    }
    try {
      if (action === "assign") {
        const assignee = $("taskAssigneeSelect").value;
        if (!assignee) throw new Error("select an Agent before assigning");
        taskSystem.assignTask(task.id, assignee);
      } else if (action === "unassign") {
        taskSystem.unassignTask(task.id);
      } else if (action === "start") {
        taskSystem.startTask(task.id, task.assignee_id);
      } else if (action === "block") {
        taskSystem.blockTask(task.id, $("taskBlockReasonInput").value, task.assignee_id);
      } else if (action === "resume") {
        taskSystem.resumeTask(task.id, task.assignee_id);
      } else if (action === "complete") {
        taskSystem.completeTask(task.id, task.assignee_id);
      }
      setTaskError(null);
    } catch (error) {
      setTaskError(error);
    }
    render();
  }

  function updateTaskPanels() {
    if (!taskSystem) return;
    const stats = taskSystem.getStats();
    const statsPanel = $("taskStats");
    statsPanel.innerHTML = "";
    ["total", "queued", "working", "blocked", "done"].forEach((key) => {
      const item = document.createElement("div");
      item.className = "task-stat";
      const value = document.createElement("strong");
      value.textContent = String(stats[key]);
      item.appendChild(value);
      item.appendChild(document.createTextNode(key));
      statsPanel.appendChild(item);
    });
    const persistence = taskSystem.getPersistenceStatus();
    $("taskPersistenceStatus").textContent = `persistence: ${persistence.status} · revision ${persistence.revision}` +
      (persistence.last_error ? ` · ${persistence.last_error}` : "");

    const filter = $("taskFilterSelect").value;
    const tasks = taskSystem.listTasks(filter === "all" ? {} : filter === "unassigned" ? { unassigned: true } : { status: filter });
    if (!selectedTaskId && tasks.length) selectedTaskId = tasks[0].id;
    if (selectedTaskId && !taskSystem.listTasks().some((task) => task.id === selectedTaskId)) selectedTaskId = tasks[0] ? tasks[0].id : null;

    const queue = $("taskQueue");
    queue.innerHTML = "";
    tasks.forEach((task) => {
      const row = document.createElement("li");
      const priority = document.createElement("span");
      priority.className = "task-priority";
      priority.textContent = task.priority;
      const button = document.createElement("button");
      button.type = "button";
      button.textContent = `${task.status} · ${task.title}`;
      if (task.id === selectedTaskId) button.classList.add("selected");
      button.addEventListener("click", () => { selectedTaskId = task.id; taskErrorMessage = ""; render(); });
      row.appendChild(priority);
      row.appendChild(button);
      queue.appendChild(row);
    });

    const task = selectedTask();
    const detail = $("taskDetail");
    const assigneeSelect = $("taskAssigneeSelect");
    let assignedAgent = null;
    if (task && task.assignee_id) {
      try { assignedAgent = runtime.getAgent(task.assignee_id); } catch (error) { assignedAgent = null; }
    }
    const agentMoving = Boolean(assignedAgent && assignedAgent.movement && assignedAgent.movement.status === "moving");
    const controls = {
      taskAssignButton: Boolean(task && task.status !== "done" && !task.assignee_id),
      taskUnassignButton: Boolean(task && task.assignee_id && task.status !== "working"),
      taskStartButton: Boolean(task && task.assignee_id && (task.status === "queued" || task.status === "blocked") && !agentMoving),
      taskBlockButton: Boolean(task && task.assignee_id && task.status === "working"),
      taskResumeButton: Boolean(task && task.assignee_id && task.status === "blocked" && !agentMoving),
      taskCompleteButton: Boolean(task && task.assignee_id && task.status === "working"),
    };
    Object.keys(controls).forEach((id) => { $(id).disabled = !controls[id]; });
    assigneeSelect.disabled = !task || task.status === "done" || Boolean(task.assignee_id);
    $("taskBlockReasonInput").disabled = !task || task.status !== "working";
    assigneeSelect.innerHTML = "";
    const unassignedOption = document.createElement("option");
    unassignedOption.value = "";
    unassignedOption.textContent = "unassigned";
    assigneeSelect.appendChild(unassignedOption);
    runtime.agents.forEach((agent) => {
      const option = document.createElement("option");
      option.value = agent.id;
      option.textContent = `${agent.name} (${agent.id})`;
      assigneeSelect.appendChild(option);
    });
    if (!task) {
      detail.textContent = "No task selected.";
      assigneeSelect.value = "";
    } else {
      detail.textContent = [
        `${task.id} · ${task.status} · ${task.priority}`,
        task.title,
        task.description ? `description: ${task.description}` : "",
        task.assignee_id ? `assignee: ${task.assignee_id}` : "assignee: unassigned",
        task.blocked_reason ? `blocked: ${task.blocked_reason}` : ""
      ].filter(Boolean).join("\n");
      assigneeSelect.value = task.assignee_id || "";
    }
    $("taskError").textContent = taskErrorMessage;

    const notifications = $("taskNotifications");
    notifications.innerHTML = "";
    taskSystem.getNotifications().slice(0, 12).forEach((notification) => {
      const item = document.createElement("li");
      item.textContent = `t${notification.created_at_tick} ${notification.status} ${notification.text}`;
      const addNotificationAction = (label, handler) => {
        const button = document.createElement("button");
        button.type = "button";
        button.textContent = label;
        button.setAttribute("aria-label", `${label} notification ${notification.id}`);
        button.addEventListener("click", () => {
          try { handler(); setTaskError(null); } catch (error) { setTaskError(error); }
          render();
        });
        item.appendChild(document.createTextNode(" "));
        item.appendChild(button);
      };
      if (notification.status === "unread") {
        addNotificationAction("read", () => taskSystem.markNotificationRead(notification.id));
      }
      if (notification.status !== "dismissed") {
        addNotificationAction("dismiss", () => taskSystem.dismissNotification(notification.id));
      }
      notifications.appendChild(item);
    });

    const activity = $("taskActivityLog");
    activity.innerHTML = "";
    taskSystem.getActivity().slice(-24).reverse().forEach((event) => {
      const item = document.createElement("li");
      item.textContent = `t${event.tick} #${event.sequence} ${event.type}${event.task_id ? ` ${event.task_id}` : ""}`;
      activity.appendChild(item);
    });
  }

  function createTaskSystem(previousState = null) {
    if (!taskRepository) taskRepository = new LocalStorageTaskRepository({ key: "phase6.task_state.v1" });
    const system = new TaskSystem({
      clock: runtime.clock,
      getAgent: (id) => runtime.getAgent(id),
      listAgents: () => [...runtime.agents.values()],
      projectAgent: (id, taskId, status) => runtime.setAgentTaskProjection(id, taskId, status),
      setAgentState: (id, state) => runtime.setState(id, state),
      emitRuntimeEvent: (type, payload, source) => runtime.recordAdapterEvent(type, payload, source),
      repository: taskRepository,
      repositoryRevision: previousState ? previousState.revision : 0
    });
    if (previousState) {
      system.restore(previousState.snapshot, { persist: false });
    } else {
      system.load();
    }
    system.syncProjections();
    return system;
  }

  function resetRuntime() {
    const previousTasks = taskSystem
      ? { snapshot: taskSystem.snapshot(), revision: taskSystem.getPersistenceStatus().revision }
      : null;
    runtime = new OfficeRuntime({
      manifest,
      bodyfaceRecords: window.BODYFACE_RECORDS || [],
      assetBaseUrl: "/game-dev-story-mod_Sprites/game",
      pathProvider: new DirectPathProvider({ step: manifest.movement.step }),
      collisionProvider: new ExplicitCollisionProvider(manifest.movement.collision),
      seatProvider: new SeatProvider(manifest.seats || []),
      localeStore: new LocaleStore(window.WAVE5_LOCALES || {}, "th")
    });
    runtime.addAgent({ id: "adapter.actor.0", employeeId: "adapter.employee.0", name: "Aoi", role: "worker", position: [220, 326], selectors: { TFace: 2, TBody: 3, TMode: 0, TKage: 1 } });
    runtime.addAgent({ id: "adapter.actor.1", employeeId: "adapter.employee.1", name: "Mika", role: "designer", position: [336, 354], selectors: { TFace: 30, TBody: 19, TMode: 0, TKage: 1 } });
    taskSystem = createTaskSystem(previousTasks);
    rebuildActorSelect();
    render();
  }

  async function boot() {
    manifest = await fetch("./data/room_manifest.json").then((response) => response.json());
    const localeArtifact = await fetch("../artifacts/wave5_locale_runtime.json").then((response) => response.json());
    window.WAVE5_LOCALES = localeArtifact.locales || {};
    const bodyfaceArtifact = await fetch("../../Phase2/artifacts/bodyface_analysis.json").then((response) => response.json());
    window.BODYFACE_RECORDS = (bodyfaceArtifact.records || []).map((record) => record.raw_record || record);
    backgroundImage = loadImage(manifest.background.url);
    resetRuntime();
    $("playButton").addEventListener("click", () => {
      playing = !playing;
      $("playButton").textContent = playing ? "Pause" : "Play";
      if (playing) {
        timer = window.setInterval(() => { runtime.step(1); render(); }, 160);
      } else if (timer) {
        window.clearInterval(timer);
        timer = null;
      }
    });
    $("stepButton").addEventListener("click", () => { runtime.step(1); render(); });
    $("resetButton").addEventListener("click", () => { playing = false; if (timer) window.clearInterval(timer); timer = null; resetRuntime(); });
    $("actorSelect").addEventListener("change", render);
    $("stateSelect").addEventListener("change", (event) => {
      const actor = selectedActor();
      const activeTask = taskSystem.getAgentTask(actor.id);
      if (activeTask) {
        setTaskError(new Error("use the task action while this Agent has an active task"));
      } else {
        try { runtime.setState(actor.id, event.target.value); setTaskError(null); } catch (error) { setTaskError(error); }
      }
      render();
    });
    $("moveButton").addEventListener("click", () => { runtime.requestMove(selectedActor().id, [420, 326]); render(); });
    $("seatButton").addEventListener("click", () => { runtime.occupySeat(selectedActor().id, "adapter.seat.0"); render(); });
    $("dialogueButton").addEventListener("click", () => { runtime.requestDialogue({ actorId: selectedActor().id, talkTag: "wave5.demo", text: "adapter dialogue", lifetimeTicks: 24 }); render(); });
    $("notificationButton").addEventListener("click", () => { runtime.addNotification({ text: "adapter notification", graphId: 1, lifetimeTicks: 96 }); render(); });
    $("taskForm").addEventListener("submit", (event) => {
      event.preventDefault();
      try {
        const task = taskSystem.createTask({
          title: $("taskTitleInput").value,
          description: $("taskDescriptionInput").value,
          priority: $("taskPriorityInput").value
        });
        selectedTaskId = task.id;
        $("taskTitleInput").value = "";
        $("taskDescriptionInput").value = "";
        setTaskError(null);
      } catch (error) {
        setTaskError(error);
      }
      render();
    });
    $("taskFilterSelect").addEventListener("change", () => render());
    $("taskAssignButton").addEventListener("click", () => runTaskAction("assign"));
    $("taskUnassignButton").addEventListener("click", () => runTaskAction("unassign"));
    $("taskStartButton").addEventListener("click", () => runTaskAction("start"));
    $("taskBlockButton").addEventListener("click", () => runTaskAction("block"));
    $("taskResumeButton").addEventListener("click", () => runTaskAction("resume"));
    $("taskCompleteButton").addEventListener("click", () => runTaskAction("complete"));
    $("taskResetButton").addEventListener("click", () => {
      try {
        taskSystem.clear({ actorId: "operator" });
        selectedTaskId = null;
        setTaskError(null);
      } catch (error) {
        setTaskError(error);
      }
      render();
    });
    $("taskExportButton").addEventListener("click", () => {
      const blob = new Blob([JSON.stringify(taskSystem.exportData(), null, 2)], { type: "application/json" });
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = "wave6-task-export.json";
      link.click();
      URL.revokeObjectURL(url);
    });
    $("taskImportButton").addEventListener("click", () => $("taskImportInput").click());
    $("taskImportInput").addEventListener("change", async (event) => {
      const file = event.target.files && event.target.files[0];
      if (!file) return;
      try {
        const data = JSON.parse(await file.text());
        taskSystem.importData(data, { actorId: "operator" });
        selectedTaskId = null;
        setTaskError(null);
      } catch (error) {
        setTaskError(error);
      } finally {
        event.target.value = "";
      }
      render();
    });
    $("taskReloadButton").addEventListener("click", () => {
      try {
        if (!taskSystem.reloadFromRepository()) throw new Error("no saved task state found");
        selectedTaskId = null;
        setTaskError(null);
      } catch (error) {
        setTaskError(error);
      }
      render();
    });
    render();
  }

  boot().catch((error) => {
    $("runtimeStatus").textContent = "BOOT ERROR";
    $("diagnostics").textContent = String(error.stack || error);
  });
})();
