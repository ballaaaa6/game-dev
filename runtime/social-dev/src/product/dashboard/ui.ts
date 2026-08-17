import type { AssignmentCommandResult, TaskRecord } from "../assignment";
import type { DashboardRuntimeCommand, DashboardRuntimeSnapshot, DashboardStaffRosterEntry } from "./types";

export interface DashboardUiElements {
  readonly root: HTMLElement;
  readonly mode: HTMLElement;
  readonly frame: HTMLElement;
  readonly error: HTMLElement;
  readonly unbound: HTMLElement;
  readonly agents: HTMLElement;
  readonly events: HTMLElement;
  readonly history: HTMLElement;
}

export interface DashboardUiCallbacks {
  readonly execute: (command: DashboardRuntimeCommand) => AssignmentCommandResult;
}

function element<K extends keyof HTMLElementTagNameMap>(tag: K, className?: string): HTMLElementTagNameMap[K] {
  const node = document.createElement(tag);
  if (className) node.className = className;
  return node;
}

function clear(node: HTMLElement): void {
  node.replaceChildren();
}

function textRow(label: string, value: string): HTMLElement {
  const row = element("div", "dashboard-detail-row");
  const labelNode = element("span", "dashboard-detail-label");
  labelNode.textContent = label;
  const valueNode = element("span", "dashboard-detail-value");
  valueNode.textContent = value;
  row.append(labelNode, valueNode);
  return row;
}

function field(label: string, name: string, value = "", type = "text"): HTMLInputElement {
  const wrapper = element("label", "dashboard-field");
  wrapper.textContent = label;
  const input = element("input");
  input.type = type;
  input.name = name;
  input.value = value;
  if (type === "number") {
    input.min = "0";
    input.max = "100";
    input.step = "1";
  }
  wrapper.append(input);
  return input;
}

function button(label: string, className = "dashboard-button", testId?: string): HTMLButtonElement {
  const node = element("button", className);
  node.type = "button";
  node.textContent = label;
  if (testId) node.dataset.testid = testId;
  return node;
}

function formButton(label: string, testId?: string): HTMLButtonElement {
  const node = button(label, "dashboard-button dashboard-button-primary", testId);
  node.type = "submit";
  return node;
}

function commandResultText(result: AssignmentCommandResult | null): string {
  if (!result) return "No product command submitted in this session.";
  if (result.accepted) return `Accepted · ${result.code}`;
  return `Rejected · ${result.code}`;
}

function staffLabel(staff: DashboardStaffRosterEntry): string {
  return `${staff.name} · ${staff.jobName} · ${staff.skillName}`;
}

function appendBindForm(parent: HTMLElement, staff: DashboardStaffRosterEntry, execute: DashboardUiCallbacks["execute"]): void {
  const form = element("form", "dashboard-form dashboard-bind-form");
  form.dataset.staffId = String(staff.staffId);
  const input = field("External agent", "externalAgentId");
  input.placeholder = "agent-alpha";
  input.required = true;
  const submit = formButton("Bind agent", `bind-agent-${staff.staffId}`);
  form.append(input, submit);
  form.addEventListener("submit", (event) => {
    event.preventDefault();
    execute({ type: "bind_agent", externalAgentId: input.value.trim(), staffId: staff.staffId });
  });
  parent.append(form);
}

function appendAssignForm(parent: HTMLElement, agentId: string, execute: DashboardUiCallbacks["execute"]): void {
  const form = element("form", "dashboard-form dashboard-task-form");
  const taskId = field("Task id", "externalTaskId");
  taskId.placeholder = "task-001";
  taskId.required = true;
  const label = field("Task label", "label");
  label.placeholder = "Prepare scene brief";
  const submit = formButton("Assign task", `assign-task-${agentId}`);
  form.append(taskId, label, submit);
  form.addEventListener("submit", (event) => {
    event.preventDefault();
    execute({ type: "assign_task", externalTaskId: taskId.value.trim(), externalAgentId: agentId, label: label.value.trim() });
  });
  parent.append(form);
}

function appendTaskControls(parent: HTMLElement, task: TaskRecord, execute: DashboardUiCallbacks["execute"]): void {
  const controls = element("div", "dashboard-control-row");
  if (task.status === "ASSIGNED") {
    const start = button("Start task", "dashboard-button dashboard-button-primary", `start-task-${task.externalTaskId}`);
    start.addEventListener("click", () => execute({ type: "start_task", externalTaskId: task.externalTaskId }));
    controls.append(start);
  }
  if (task.status === "ASSIGNED" || task.status === "RUNNING") {
    const complete = button("Complete", "dashboard-button", `complete-task-${task.externalTaskId}`);
    complete.addEventListener("click", () => execute({ type: "complete_task", externalTaskId: task.externalTaskId }));
    const fail = button("Fail", "dashboard-button dashboard-button-danger", `fail-task-${task.externalTaskId}`);
    fail.addEventListener("click", () => execute({ type: "fail_task", externalTaskId: task.externalTaskId, reason: "failed_from_dashboard" }));
    const cancel = button("Cancel", "dashboard-button", `cancel-task-${task.externalTaskId}`);
    cancel.addEventListener("click", () => execute({ type: "cancel_task", externalTaskId: task.externalTaskId, reason: "cancelled_from_dashboard" }));
    controls.append(complete, fail, cancel);
  }
  if (controls.childElementCount > 0) parent.append(controls);
}

function appendProductSection(parent: HTMLElement, snapshot: DashboardRuntimeSnapshot, agentId: string, execute: DashboardUiCallbacks["execute"]): void {
  const section = element("section", "dashboard-subsection");
  const title = element("h4");
  title.textContent = "PRODUCT";
  section.append(title);
  const agent = snapshot.dashboard.agents.find((candidate) => candidate.externalAgentId === agentId);
  if (!agent) return;
  const taskModel = agent.task;
  section.append(
    textRow("Status", taskModel.status),
    textRow("Task progress", taskModel.externalProgress === null ? "—" : `${taskModel.externalProgress}%`),
    textRow("Bridge", taskModel.bridgeMode),
  );
  if (taskModel.label) section.append(textRow("Label", taskModel.label));
  if (taskModel.terminalReason) section.append(textRow("Terminal reason", taskModel.terminalReason));
  const task = taskModel.externalTaskId ? snapshot.tasks.find((candidate) => candidate.externalTaskId === taskModel.externalTaskId) : null;
  if (task && (task.status === "ASSIGNED" || task.status === "RUNNING")) {
    const progressForm = element("form", "dashboard-form dashboard-progress-form");
    const progress = field("Task progress", "externalProgress", String(task.externalProgress), "number");
    const submit = formButton("Update progress", `progress-task-${task.externalTaskId}`);
    progressForm.append(progress, submit);
    progressForm.addEventListener("submit", (event) => {
      event.preventDefault();
      execute({ type: "update_task_progress", externalTaskId: task.externalTaskId, externalProgress: Number(progress.value) });
    });
    section.append(progressForm);
    appendTaskControls(section, task, execute);
  } else {
    appendAssignForm(section, agentId, execute);
  }
  parent.append(section);
}

function appendLivingSection(parent: HTMLElement, agent: DashboardRuntimeSnapshot["dashboard"]["agents"][number]): void {
  const section = element("section", "dashboard-subsection");
  const title = element("h4");
  title.textContent = "LIVING";
  section.append(title);
  section.append(
    textRow("Display", agent.living.livingDisplayStatus),
    textRow("State", agent.living.stateName),
    textRow("Move mode", agent.living.moveModeName),
    textRow("Cell", agent.living.cell.join(", ")),
    textRow("HP", `${agent.living.hp}/${agent.living.maxHp}`),
    textRow("Route", `${agent.living.routeLength} cells`),
  );
  parent.append(section);
}

function renderUnbound(elements: DashboardUiElements, snapshot: DashboardRuntimeSnapshot, execute: DashboardUiCallbacks["execute"]): void {
  clear(elements.unbound);
  if (snapshot.unboundStaff.length === 0) {
    const empty = element("p", "dashboard-empty");
    empty.textContent = "All source-backed Staff are explicitly bound.";
    elements.unbound.append(empty);
    return;
  }
  for (const staff of snapshot.unboundStaff) {
    const card = element("article", "dashboard-roster-card");
    card.dataset.staffId = String(staff.staffId);
    const heading = element("div", "dashboard-card-heading");
    const name = element("strong");
    name.textContent = staffLabel(staff);
    const source = element("span", "dashboard-card-meta");
    source.textContent = `Staff ${staff.staffId} · ${staff.living.livingDisplayStatus}`;
    heading.append(name, source);
    card.append(heading);
    appendBindForm(card, staff, execute);
    elements.unbound.append(card);
  }
}

function renderAgents(elements: DashboardUiElements, snapshot: DashboardRuntimeSnapshot, execute: DashboardUiCallbacks["execute"]): void {
  clear(elements.agents);
  if (snapshot.dashboard.agents.length === 0) {
    const empty = element("p", "dashboard-empty");
    empty.textContent = "No bindings yet. Bind an explicit external agent to a source-backed Staff above.";
    elements.agents.append(empty);
    return;
  }
  for (const agent of snapshot.dashboard.agents) {
    const card = element("article", "dashboard-agent-card");
    card.dataset.agentId = agent.externalAgentId;
    const heading = element("div", "dashboard-card-heading");
    const name = element("strong");
    name.textContent = agent.externalAgentId;
    const status = element("span", "dashboard-status");
    status.textContent = agent.task.status;
    status.dataset.taskStatus = agent.task.status;
    heading.append(name, status);
    card.append(heading);
    appendProductSection(card, snapshot, agent.externalAgentId, execute);
    appendLivingSection(card, agent);
    const bindingControls = element("div", "dashboard-control-row");
    const active = agent.task.status === "ASSIGNED" || agent.task.status === "RUNNING";
    const unbind = button("Unbind agent", "dashboard-button", `unbind-agent-${agent.externalAgentId}`);
    unbind.disabled = active;
    unbind.title = active ? "Complete, fail, or cancel the active task before unbinding." : "Remove this external binding.";
    unbind.addEventListener("click", () => execute({ type: "unbind_agent", externalAgentId: agent.externalAgentId }));
    bindingControls.append(unbind);
    card.append(bindingControls);
    elements.agents.append(card);
  }
}

function renderEvents(elements: DashboardUiElements, snapshot: DashboardRuntimeSnapshot): void {
  clear(elements.events);
  const events = snapshot.events.slice(-14).reverse();
  if (events.length === 0) {
    const empty = element("p", "dashboard-empty");
    empty.textContent = "No product events yet.";
    elements.events.append(empty);
    return;
  }
  for (const event of events) {
    const row = element("div", "dashboard-event-row");
    const sequence = element("span", "dashboard-event-sequence");
    sequence.textContent = `#${event.sequence}`;
    const description = element("span");
    const subject = [event.externalAgentId, event.externalTaskId].filter(Boolean).join(" · ");
    description.textContent = `${event.type}${subject ? ` · ${subject}` : ""}${event.reason ? ` · ${event.reason}` : ""}`;
    row.append(sequence, description);
    elements.events.append(row);
  }
}

function renderHistory(elements: DashboardUiElements, snapshot: DashboardRuntimeSnapshot): void {
  clear(elements.history);
  if (snapshot.tasks.length === 0) {
    const empty = element("p", "dashboard-empty");
    empty.textContent = "No task history yet.";
    elements.history.append(empty);
    return;
  }
  for (const task of snapshot.tasks) {
    const row = element("div", "dashboard-history-row");
    const subject = element("strong");
    subject.textContent = `${task.externalTaskId} · ${task.externalAgentId}`;
    const status = element("span", "dashboard-status");
    status.textContent = `${task.status} · ${task.externalProgress}%`;
    status.dataset.taskStatus = task.status;
    const reason = element("span", "dashboard-card-meta");
    reason.textContent = task.terminalReason ?? task.label ?? "No terminal reason";
    row.append(subject, status, reason);
    elements.history.append(row);
  }
}

export function createDashboardUi(root: HTMLElement, callbacks: DashboardUiCallbacks): DashboardUiElements {
  const panel = element("section", "panel dashboard-panel");
  panel.dataset.testid = "dashboard-panel";
  panel.innerHTML = `
    <div class="dashboard-heading">
      <div>
        <p class="eyebrow">Product control surface</p>
        <h2>Dashboard runtime</h2>
      </div>
      <span class="dashboard-runtime-mode" data-dashboard-mode>Bridge C · in memory</span>
    </div>
    <p class="dashboard-policy">PRODUCT task lifecycle overlays BASELINE LIVING. Backend not connected; RUNNING is product state only.</p>
    <div class="dashboard-result" data-dashboard-error role="status" aria-live="polite"></div>
    <section class="dashboard-section"><div class="dashboard-section-heading"><h3>Unbound Staff</h3><span data-dashboard-unbound-count></span></div><div data-dashboard-unbound></div></section>
    <section class="dashboard-section"><div class="dashboard-section-heading"><h3>Agents</h3><span>Product + living</span></div><div data-dashboard-agents></div></section>
    <section class="dashboard-section"><div class="dashboard-section-heading"><h3>Activity feed</h3><span>Product events</span></div><div class="dashboard-feed" data-dashboard-events></div></section>
    <section class="dashboard-section"><div class="dashboard-section-heading"><h3>Task history</h3><span>Ephemeral session</span></div><div class="dashboard-feed" data-dashboard-history></div></section>
  `;
  root.querySelector(".side-column")?.append(panel);
  const mode = panel.querySelector<HTMLElement>("[data-dashboard-mode]");
  const frame = panel.querySelector<HTMLElement>("[data-dashboard-unbound-count]");
  const error = panel.querySelector<HTMLElement>("[data-dashboard-error]");
  const unbound = panel.querySelector<HTMLElement>("[data-dashboard-unbound]");
  const agents = panel.querySelector<HTMLElement>("[data-dashboard-agents]");
  const events = panel.querySelector<HTMLElement>("[data-dashboard-events]");
  const history = panel.querySelector<HTMLElement>("[data-dashboard-history]");
  if (!mode || !frame || !error || !unbound || !agents || !events || !history) throw new Error("Dashboard UI elements were not created");
  return { root: panel, mode, frame, error, unbound, agents, events, history };
}

export function renderDashboardUi(elements: DashboardUiElements, snapshot: DashboardRuntimeSnapshot, callbacks: DashboardUiCallbacks): void {
  elements.mode.textContent = `${snapshot.bridgeMode} · frame ${snapshot.frame}`;
  elements.frame.textContent = `${snapshot.unboundStaff.length} available`;
  elements.error.textContent = commandResultText(snapshot.lastCommandResult);
  elements.error.dataset.commandAccepted = snapshot.lastCommandResult ? String(snapshot.lastCommandResult.accepted) : "none";
  elements.error.classList.toggle("is-error", snapshot.lastCommandResult?.accepted === false);
  elements.error.classList.toggle("is-success", snapshot.lastCommandResult?.accepted === true);
  renderUnbound(elements, snapshot, callbacks.execute);
  renderAgents(elements, snapshot, callbacks.execute);
  renderEvents(elements, snapshot);
  renderHistory(elements, snapshot);
}
