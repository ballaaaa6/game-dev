(function (root, factory) {
  if (typeof module === "object" && module.exports) {
    module.exports = factory();
  } else {
    root.Wave6TaskSystem = factory();
  }
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
  "use strict";

  const SCHEMA_VERSION = "wave6-task-state-v1";
  const LEGACY_EQUIVALENCE = false;
  const TASK_STATUSES = ["queued", "working", "blocked", "done"];
  const TASK_PRIORITIES = ["urgent", "high", "normal", "low"];
  const NOTIFICATION_STATUSES = ["unread", "read", "dismissed"];
  const PRIORITY_RANK = { urgent: 0, high: 1, normal: 2, low: 3 };
  const ACTIVE_STATUSES = new Set(["queued", "working", "blocked"]);
  const PERMISSION_ACTIONS = [
    "create",
    "assign",
    "unassign",
    "start",
    "block",
    "resume",
    "complete",
    "read_notification",
    "dismiss_notification",
    "reset",
    "import"
  ];

  function clone(value) {
    return value === undefined ? undefined : JSON.parse(JSON.stringify(value));
  }

  function stableObject(value) {
    if (Array.isArray(value)) return value.map(stableObject);
    if (value && typeof value === "object") {
      return Object.keys(value).sort().reduce((result, key) => {
        result[key] = stableObject(value[key]);
        return result;
      }, {});
    }
    return value;
  }

  function stableJson(value) {
    return JSON.stringify(stableObject(value));
  }

  class TaskSystemError extends Error {
    constructor(code, message) {
      super(message);
      this.name = "TaskSystemError";
      this.code = code;
    }
  }

  class DefaultTaskPermissionPolicy {
    constructor(options = {}) {
      this.operatorIds = new Set((options.operatorIds || ["operator"]).map(String));
      this.agentActions = new Set(options.agentActions || [
        "start",
        "block",
        "resume",
        "complete",
        "read_notification",
        "dismiss_notification"
      ]);
    }

    can(action, actorId, context = {}) {
      const id = String(actorId || "");
      if (!PERMISSION_ACTIONS.includes(action)) return false;
      if (this.operatorIds.has(id)) return true;
      return this.agentActions.has(action) && context.assignee_id !== null &&
        context.assignee_id !== undefined && String(context.assignee_id) === id;
    }
  }

  function fail(code, message) {
    throw new TaskSystemError(code, message);
  }

  function normalizePriority(priority) {
    const value = priority || "normal";
    if (!TASK_PRIORITIES.includes(value)) fail("invalid_priority", `invalid task priority: ${value}`);
    return value;
  }

  function normalizeTitle(title) {
    const value = String(title === undefined || title === null ? "" : title).trim();
    if (!value) fail("invalid_title", "task title must not be empty");
    return value;
  }

  function normalizeDescription(description) {
    return String(description === undefined || description === null ? "" : description).trim();
  }

  function normalizeTick(clock) {
    const value = clock && Number.isInteger(clock.value) ? clock.value : 0;
    return value >= 0 ? value : 0;
  }

  class TaskSystem {
    constructor(options = {}) {
      this.clock = options.clock || { value: 0 };
      this.getAgent = options.getAgent || (() => null);
      this.listAgents = options.listAgents || (() => []);
      this.projectAgent = options.projectAgent || (() => undefined);
      this.setAgentState = options.setAgentState || (() => undefined);
      this.emitRuntimeEvent = options.emitRuntimeEvent || (() => undefined);
      this.repository = options.repository || null;
      this.permissionPolicy = options.permissionPolicy || new DefaultTaskPermissionPolicy();
      this.repositoryRevision = Number.isInteger(options.repositoryRevision) ? options.repositoryRevision : 0;
      this.tasks = new Map();
      this.notifications = new Map();
      this.activityLog = [];
      this.nextTaskNumber = 0;
      this.nextNotificationNumber = 0;
      this.nextActivitySequence = 0;
      this.persistence = {
        status: this.repository ? "ready" : "memory_only",
        storage_kind: this.repository ? this.repository.kind || "custom_repository" : "none",
        revision: this.repositoryRevision,
        migrated_from: null,
        last_error: null
      };
    }

    get taskCount() {
      return this.tasks.size;
    }

    _tick() {
      return normalizeTick(this.clock);
    }

    _taskId() {
      const id = `task.${String(this.nextTaskNumber).padStart(4, "0")}`;
      this.nextTaskNumber += 1;
      return id;
    }

    _notificationId() {
      const id = `task.notification.${String(this.nextNotificationNumber).padStart(4, "0")}`;
      this.nextNotificationNumber += 1;
      return id;
    }

    _getTask(taskId) {
      const task = this.tasks.get(String(taskId));
      if (!task) fail("task_not_found", `unknown task id: ${taskId}`);
      return task;
    }

    _getAgent(agentId) {
      const id = String(agentId);
      let agent;
      try {
        agent = this.getAgent(id);
      } catch (error) {
        agent = null;
      }
      if (!agent) fail("agent_not_found", `unknown agent id: ${id}`);
      return agent;
    }

    _authorize(action, actorId, context = {}) {
      const id = String(actorId || "");
      if (!this.permissionPolicy.can(action, id, context)) {
        fail("permission_denied", `${id || "anonymous"} cannot ${action}`);
      }
      return id;
    }

    _activeTaskForAgent(agentId, excludedTaskId = null) {
      return [...this.tasks.values()].find((task) =>
        task.id !== excludedTaskId && task.assignee_id === String(agentId) && ACTIVE_STATUSES.has(task.status)
      ) || null;
    }

    _record(type, taskId, actorId, payload = {}) {
      const record = {
        sequence: this.nextActivitySequence++,
        tick: this._tick(),
        type,
        task_id: taskId || null,
        actor_id: actorId || null,
        payload: clone(payload),
        source: "phase6_task_system",
        legacy_equivalence: LEGACY_EQUIVALENCE
      };
      this.activityLog.push(record);
      try {
        this.emitRuntimeEvent(type, {
          task_id: record.task_id,
          actor_id: record.actor_id,
          ...clone(payload)
        }, record.source);
      } catch (error) {
        this.persistence.last_error = `runtime_event:${error.message}`;
      }
      return record;
    }

    _persist() {
      if (!this.repository) return;
      try {
        const result = this.repository.save(this.snapshot(), this.repositoryRevision);
        if (!result || !Number.isInteger(result.revision) || result.revision < 0) {
          throw new Error("repository save returned an invalid envelope");
        }
        this.repositoryRevision = result.revision;
        this.persistence.status = "saved";
        this.persistence.revision = this.repositoryRevision;
        this.persistence.last_error = null;
      } catch (error) {
        this.persistence.status = error.code === "repository_conflict"
          ? "conflict_needs_reload"
          : "degraded_memory_only";
        this.persistence.last_error = String(error.message || error);
      }
    }

    _setProjection(agentId, taskId, status) {
      this.projectAgent(String(agentId), taskId, status);
    }

    _setState(agentId, state) {
      try {
        this.setAgentState(String(agentId), state);
      } catch (error) {
        fail("agent_state_update_failed", String(error.message || error));
      }
    }

    _notify(kind, task, recipientId, text, payload = {}) {
      const notification = {
        id: this._notificationId(),
        kind,
        task_id: task.id,
        recipient_id: recipientId ? String(recipientId) : null,
        text: String(text),
        created_at_tick: this._tick(),
        read_at_tick: null,
        dismissed_at_tick: null,
        status: "unread",
        payload: clone(payload),
        source: "phase6_task_system",
        legacy_equivalence: LEGACY_EQUIVALENCE
      };
      this.notifications.set(notification.id, notification);
      this._record("task.notification.created", task.id, recipientId, {
        notification_id: notification.id,
        kind,
        ...clone(payload)
      });
      return notification;
    }

    createTask(input = {}) {
      const now = this._tick();
      const createdBy = String(input.createdBy || "operator");
      this._authorize("create", createdBy, {});
      const task = {
        id: input.id ? String(input.id) : this._taskId(),
        title: normalizeTitle(input.title),
        description: normalizeDescription(input.description),
        priority: normalizePriority(input.priority),
        status: "queued",
        assignee_id: null,
        created_by: createdBy,
        created_at_tick: now,
        updated_at_tick: now,
        blocked_reason: null,
        started_at_tick: null,
        completed_at_tick: null,
        source: "phase6_web_adapter",
        legacy_equivalence: LEGACY_EQUIVALENCE
      };
      if (this.tasks.has(task.id)) fail("duplicate_task_id", `duplicate task id: ${task.id}`);
      this.tasks.set(task.id, task);
      this._record("task.created", task.id, createdBy, {
        title: task.title,
        priority: task.priority
      });
      this._persist();
      return clone(task);
    }

    getTask(taskId) {
      return clone(this._getTask(taskId));
    }

    listTasks(filter = {}) {
      const search = filter.search ? String(filter.search).toLowerCase() : null;
      const tasks = [...this.tasks.values()].filter((task) => {
        if (filter.status && task.status !== filter.status) return false;
        if (filter.assigneeId && task.assignee_id !== String(filter.assigneeId)) return false;
        if (filter.unassigned === true && task.assignee_id !== null) return false;
        if (filter.priority && task.priority !== filter.priority) return false;
        if (search && !`${task.title} ${task.description}`.toLowerCase().includes(search)) return false;
        return true;
      });
      tasks.sort((left, right) =>
        (PRIORITY_RANK[left.priority] - PRIORITY_RANK[right.priority]) ||
        (left.created_at_tick - right.created_at_tick) ||
        left.id.localeCompare(right.id)
      );
      return tasks.map(clone);
    }

    assignTask(taskId, agentId, actorId = "operator") {
      const task = this._getTask(taskId);
      const agent = this._getAgent(agentId);
      const actionActor = this._authorize("assign", actorId, task);
      if (task.status === "done") fail("task_done", "done task cannot be assigned");
      if (task.assignee_id !== null) fail("task_already_assigned", "task already has an assignee");
      const conflict = this._activeTaskForAgent(agent.id, task.id);
      if (conflict) fail("agent_busy", `agent already has active task: ${conflict.id}`);
      task.assignee_id = agent.id;
      task.updated_at_tick = this._tick();
      this._setProjection(agent.id, task.id, task.status);
      this._record("task.assigned", task.id, actionActor, { assignee_id: agent.id });
      this._notify("task.assigned", task, agent.id, `Assigned: ${task.title}`, { assignee_id: agent.id });
      this._persist();
      return clone(task);
    }

    unassignTask(taskId, actorId = "operator") {
      const task = this._getTask(taskId);
      const actionActor = this._authorize("unassign", actorId, task);
      if (task.assignee_id === null) fail("task_unassigned", "task has no assignee");
      if (task.status === "working") fail("working_task_requires_stop", "working task must be blocked or completed before unassigning");
      const previousAssignee = task.assignee_id;
      task.assignee_id = null;
      task.updated_at_tick = this._tick();
      this._setProjection(previousAssignee, null, null);
      this._record("task.unassigned", task.id, actionActor, { previous_assignee_id: previousAssignee });
      this._persist();
      return clone(task);
    }

    startTask(taskId, actorId = null) {
      const task = this._getTask(taskId);
      if (task.status !== "queued" && task.status !== "blocked") {
        fail("invalid_transition", `cannot start task from ${task.status}`);
      }
      if (!task.assignee_id) fail("assignee_required", "task must be assigned before starting");
      const agent = this._getAgent(task.assignee_id);
      const actionActor = this._authorize("start", actorId || agent.id, task);
      if (actorId && String(actorId) !== agent.id && actionActor !== "operator") fail("actor_mismatch", "only the assignee can start this task");
      if (agent.movement && agent.movement.status === "moving") {
        fail("agent_moving", "agent must arrive before starting a task");
      }
      const previous = task.status;
      task.status = "working";
      task.started_at_tick = task.started_at_tick === null ? this._tick() : task.started_at_tick;
      task.blocked_reason = null;
      task.updated_at_tick = this._tick();
      this._setProjection(agent.id, task.id, task.status);
      this._setState(agent.id, "working");
      this._record("task.started", task.id, actionActor, { from: previous, assignee_id: agent.id });
      this._persist();
      return clone(task);
    }

    blockTask(taskId, reason, actorId = null) {
      const task = this._getTask(taskId);
      if (task.status !== "working") fail("invalid_transition", `cannot block task from ${task.status}`);
      if (!task.assignee_id) fail("assignee_required", "working task must have an assignee");
      const agent = this._getAgent(task.assignee_id);
      const actionActor = this._authorize("block", actorId || agent.id, task);
      if (actorId && String(actorId) !== agent.id && actionActor !== "operator") fail("actor_mismatch", "only the assignee can block this task");
      const blockedReason = String(reason === undefined || reason === null ? "" : reason).trim();
      if (!blockedReason) fail("blocked_reason_required", "blocked task must have a reason");
      task.status = "blocked";
      task.blocked_reason = blockedReason;
      task.updated_at_tick = this._tick();
      this._setProjection(agent.id, task.id, task.status);
      this._setState(agent.id, "idle");
      this._record("task.blocked", task.id, actionActor, { reason: blockedReason, assignee_id: agent.id });
      this._notify("task.blocked", task, task.created_by, `Blocked: ${task.title}`, { reason: blockedReason });
      this._persist();
      return clone(task);
    }

    resumeTask(taskId, actorId = null) {
      const task = this._getTask(taskId);
      if (task.status !== "blocked") fail("invalid_transition", `cannot resume task from ${task.status}`);
      if (!task.assignee_id) fail("assignee_required", "blocked task must remain assigned to resume");
      const agent = this._getAgent(task.assignee_id);
      const actionActor = this._authorize("resume", actorId || agent.id, task);
      if (actorId && String(actorId) !== agent.id && actionActor !== "operator") fail("actor_mismatch", "only the assignee can resume this task");
      if (agent.movement && agent.movement.status === "moving") fail("agent_moving", "agent must arrive before resuming a task");
      task.status = "working";
      task.blocked_reason = null;
      task.updated_at_tick = this._tick();
      this._setProjection(agent.id, task.id, task.status);
      this._setState(agent.id, "working");
      this._record("task.resumed", task.id, actionActor, { assignee_id: agent.id });
      this._persist();
      return clone(task);
    }

    completeTask(taskId, actorId = null) {
      const task = this._getTask(taskId);
      if (task.status !== "working") fail("invalid_transition", `cannot complete task from ${task.status}`);
      if (!task.assignee_id) fail("assignee_required", "working task must have an assignee");
      const agent = this._getAgent(task.assignee_id);
      const actionActor = this._authorize("complete", actorId || agent.id, task);
      if (actorId && String(actorId) !== agent.id && actionActor !== "operator") fail("actor_mismatch", "only the assignee can complete this task");
      const completedBy = agent.id;
      task.status = "done";
      task.completed_at_tick = this._tick();
      task.blocked_reason = null;
      task.updated_at_tick = this._tick();
      task.assignee_id = null;
      this._setProjection(completedBy, null, null);
      this._setState(completedBy, "idle");
      this._record("task.completed", task.id, actionActor, { completed_by: completedBy });
      this._notify("task.completed", task, task.created_by, `Completed: ${task.title}`, { completed_by: completedBy });
      this._persist();
      return clone(task);
    }

    getNotifications(filter = {}) {
      return [...this.notifications.values()]
        .filter((item) => !filter.recipientId || item.recipient_id === String(filter.recipientId))
        .filter((item) => !filter.unreadOnly || item.status === "unread")
        .sort((left, right) => (right.created_at_tick - left.created_at_tick) || (right.id.localeCompare(left.id)))
        .map(clone);
    }

    markNotificationRead(notificationId, actorId = "operator") {
      const notification = this.notifications.get(String(notificationId));
      if (!notification) fail("notification_not_found", `unknown notification id: ${notificationId}`);
      const actionActor = this._authorize("read_notification", actorId, { assignee_id: notification.recipient_id });
      if (notification.status === "unread") {
        notification.status = "read";
        notification.read_at_tick = this._tick();
        this._record("task.notification.read", notification.task_id, actionActor, { notification_id: notification.id });
        this._persist();
      }
      return clone(notification);
    }

    dismissNotification(notificationId, actorId = "operator") {
      const notification = this.notifications.get(String(notificationId));
      if (!notification) fail("notification_not_found", `unknown notification id: ${notificationId}`);
      const actionActor = this._authorize("dismiss_notification", actorId, { assignee_id: notification.recipient_id });
      if (notification.status !== "dismissed") {
        notification.status = "dismissed";
        notification.dismissed_at_tick = this._tick();
        this._record("task.notification.dismissed", notification.task_id, actionActor, { notification_id: notification.id });
        this._persist();
      }
      return clone(notification);
    }

    getActivity(filter = {}) {
      return this.activityLog
        .filter((item) => !filter.taskId || item.task_id === String(filter.taskId))
        .filter((item) => !filter.actorId || item.actor_id === String(filter.actorId))
        .filter((item) => !filter.type || item.type === filter.type)
        .map(clone);
    }

    getStats() {
      const stats = { total: 0, queued: 0, working: 0, blocked: 0, done: 0 };
      this.tasks.forEach((task) => {
        stats.total += 1;
        stats[task.status] += 1;
      });
      return stats;
    }

    getAgentTask(agentId) {
      const task = this._activeTaskForAgent(agentId);
      return task ? clone(task) : null;
    }

    syncProjections() {
      const agents = this.listAgents().map((agent) => String(agent.id));
      agents.forEach((agentId) => {
        const task = this._activeTaskForAgent(agentId);
        this._setProjection(agentId, task ? task.id : null, task ? task.status : null);
        if (task && task.status === "working") {
          const agent = this._getAgent(agentId);
          if (!agent.state || agent.state !== "working") this._setState(agentId, "working");
        } else if (task && task.status === "blocked") {
          const agent = this._getAgent(agentId);
          if (agent.state === "working") this._setState(agentId, "idle");
        }
      });
    }

    load() {
      if (!this.repository) return false;
      let envelope;
      try {
        envelope = this.repository.load();
      } catch (error) {
        this.persistence.status = "degraded_memory_only";
        this.persistence.last_error = `load:${error.message || error}`;
        return false;
      }
      if (!envelope) return false;
      try {
        if (envelope.schema_version !== "wave6-task-repository-v1" ||
            !Number.isInteger(envelope.revision) || envelope.revision < 0 || !envelope.snapshot) {
          throw new Error("repository returned an invalid envelope");
        }
        this.restore(envelope.snapshot, { persist: false });
        this.repositoryRevision = envelope.revision;
        this.persistence.revision = this.repositoryRevision;
        this.persistence.migrated_from = envelope.migrated_from || null;
        this.persistence.status = envelope.migrated_from ? "loaded_migrated" : "loaded";
        this.persistence.last_error = null;
        return true;
      } catch (error) {
        this.persistence.status = "degraded_memory_only";
        this.persistence.last_error = `restore:${error.message || error}`;
        return false;
      }
    }

    reloadFromRepository() {
      return this.load();
    }

    restore(snapshot, options = {}) {
      if (!snapshot || snapshot.schema_version !== SCHEMA_VERSION) {
        fail("invalid_snapshot", `expected ${SCHEMA_VERSION}`);
      }
      if (snapshot.legacy_equivalence !== undefined && snapshot.legacy_equivalence !== false) {
        fail("invalid_snapshot", "legacy_equivalence must remain false");
      }
      if (!Array.isArray(snapshot.tasks) || !Array.isArray(snapshot.notifications) || !Array.isArray(snapshot.activity_log)) {
        fail("invalid_snapshot", "snapshot collections must be arrays");
      }
      const tasks = new Map();
      snapshot.tasks.forEach((rawTask) => {
        const task = clone(rawTask);
        if (!task || typeof task !== "object" || Array.isArray(task) ||
            typeof task.id !== "string" || !task.id.trim() ||
            !TASK_STATUSES.includes(task.status) || !TASK_PRIORITIES.includes(task.priority)) {
          fail("invalid_snapshot", "snapshot contains invalid task");
        }
        task.id = task.id.trim();
        if (tasks.has(task.id)) fail("invalid_snapshot", `duplicate task in snapshot: ${task.id}`);
        if (typeof task.title !== "string" || !task.title.trim()) {
          fail("invalid_snapshot", `task ${task.id} has an invalid title`);
        }
        if (task.description !== undefined && typeof task.description !== "string") {
          fail("invalid_snapshot", `task ${task.id} has an invalid description`);
        }
        if (task.assignee_id !== null && task.assignee_id !== undefined &&
            (typeof task.assignee_id !== "string" || !task.assignee_id.trim())) {
          fail("invalid_snapshot", `task ${task.id} has an invalid assignee`);
        }
        ["created_at_tick", "updated_at_tick", "started_at_tick", "completed_at_tick"].forEach((field) => {
          const value = task[field];
          if (value !== null && value !== undefined && (!Number.isInteger(value) || value < 0)) {
            fail("invalid_snapshot", `task ${task.id} has an invalid ${field}`);
          }
        });
        if (task.blocked_reason !== null && task.blocked_reason !== undefined && typeof task.blocked_reason !== "string") {
          fail("invalid_snapshot", `task ${task.id} has an invalid blocked reason`);
        }
        if (task.status === "blocked" && !String(task.blocked_reason || "").trim()) {
          fail("invalid_snapshot", `blocked task ${task.id} must have a reason`);
        }
        if (task.status === "done" && task.assignee_id !== null && task.assignee_id !== undefined) {
          fail("invalid_snapshot", `done task ${task.id} must not have an assignee`);
        }
        task.description = normalizeDescription(task.description);
        if (task.assignee_id === undefined) task.assignee_id = null;
        if (task.blocked_reason === undefined) task.blocked_reason = null;
        tasks.set(task.id, task);
      });

      const notifications = new Map();
      snapshot.notifications.forEach((rawNotification) => {
        const notification = clone(rawNotification);
        if (!notification || typeof notification !== "object" || Array.isArray(notification) ||
            typeof notification.id !== "string" || !notification.id.trim() ||
            !NOTIFICATION_STATUSES.includes(notification.status) ||
            typeof notification.task_id !== "string" || !tasks.has(notification.task_id) ||
            typeof notification.text !== "string") {
          fail("invalid_snapshot", "snapshot contains invalid notification");
        }
        notification.id = notification.id.trim();
        if (notifications.has(notification.id)) {
          fail("invalid_snapshot", `duplicate notification in snapshot: ${notification.id}`);
        }
        if (notification.recipient_id !== null && notification.recipient_id !== undefined &&
            (typeof notification.recipient_id !== "string" || !notification.recipient_id.trim())) {
          fail("invalid_snapshot", `notification ${notification.id} has an invalid recipient`);
        }
        ["created_at_tick", "read_at_tick", "dismissed_at_tick"].forEach((field) => {
          const value = notification[field];
          if (value !== null && value !== undefined && (!Number.isInteger(value) || value < 0)) {
            fail("invalid_snapshot", `notification ${notification.id} has an invalid ${field}`);
          }
        });
        if (notification.recipient_id === undefined) notification.recipient_id = null;
        notifications.set(notification.id, notification);
      });

      const activityLog = [];
      const activitySequences = new Set();
      snapshot.activity_log.forEach((rawEvent) => {
        const event = clone(rawEvent);
        if (!event || typeof event !== "object" || Array.isArray(event) ||
            !Number.isInteger(event.sequence) || event.sequence < 0 ||
            !Number.isInteger(event.tick) || event.tick < 0 ||
            typeof event.type !== "string" || !event.type.trim() ||
            (event.task_id !== null && event.task_id !== undefined && !tasks.has(String(event.task_id))) ||
            (event.actor_id !== null && event.actor_id !== undefined && typeof event.actor_id !== "string")) {
          fail("invalid_snapshot", "snapshot contains invalid activity event");
        }
        if (activitySequences.has(event.sequence)) {
          fail("invalid_snapshot", `duplicate activity sequence: ${event.sequence}`);
        }
        if (event.payload !== undefined && (!event.payload || typeof event.payload !== "object" || Array.isArray(event.payload))) {
          fail("invalid_snapshot", `activity event ${event.sequence} has an invalid payload`);
        }
        activitySequences.add(event.sequence);
        activityLog.push(event);
      });

      const nextIds = snapshot.next_ids || {};
      ["task", "notification", "activity"].forEach((field) => {
        if (nextIds[field] !== undefined && (!Number.isInteger(nextIds[field]) || nextIds[field] < 0)) {
          fail("invalid_snapshot", `snapshot next_ids.${field} must be a non-negative integer`);
        }
      });

      this.tasks = tasks;
      this.notifications = notifications;
      this.activityLog = activityLog;
      this.nextTaskNumber = Number.isInteger(nextIds.task) ? nextIds.task : this.tasks.size;
      this.nextNotificationNumber = Number.isInteger(nextIds.notification) ? nextIds.notification : this.notifications.size;
      this.nextActivitySequence = Number.isInteger(nextIds.activity) ? nextIds.activity : this.activityLog.length;
      this.syncProjections();
      if (options.persist !== false) this._persist();
      return this.snapshot();
    }

    clear(options = {}) {
      this._authorize("reset", options.actorId || "operator", {});
      this.tasks.clear();
      this.notifications.clear();
      this.activityLog = [];
      this.nextTaskNumber = 0;
      this.nextNotificationNumber = 0;
      this.nextActivitySequence = 0;
      this.syncProjections();
      if (this.repository) {
        try {
          this.repository.clear();
          this.repositoryRevision = 0;
          this.persistence.status = "cleared";
          this.persistence.revision = 0;
          this.persistence.migrated_from = null;
          this.persistence.last_error = null;
        } catch (error) {
          this.persistence.status = "degraded_memory_only";
          this.persistence.last_error = `clear:${error.message || error}`;
        }
      }
      if (options.record !== false) {
        this._record("task.state.cleared", null, options.actorId || "operator", {});
        this._persist();
      }
    }

    exportData() {
      return {
        schema_version: "wave6-task-export-v1",
        exported_at_tick: this._tick(),
        task_state: this.snapshot(),
        legacy_equivalence: LEGACY_EQUIVALENCE
      };
    }

    importData(data, options = {}) {
      const actorId = options.actorId || "operator";
      this._authorize("import", actorId, {});
      const snapshot = data && data.schema_version === "wave6-task-export-v1"
        ? data.task_state
        : data;
      this.restore(snapshot, { persist: false });
      this._persist();
      return this.snapshot();
    }

    getPersistenceStatus() {
      return {
        ...clone(this.persistence),
        revision: this.repositoryRevision
      };
    }

    snapshot() {
      return {
        schema_version: SCHEMA_VERSION,
        tick: this._tick(),
        tasks: [...this.tasks.values()].map(clone),
        notifications: [...this.notifications.values()].map(clone),
        activity_log: this.activityLog.map(clone),
        next_ids: {
          task: this.nextTaskNumber,
          notification: this.nextNotificationNumber,
          activity: this.nextActivitySequence
        },
        persistence: clone(this.persistence),
        legacy_equivalence: LEGACY_EQUIVALENCE
      };
    }

    digest() {
      return stableJson(this.snapshot());
    }
  }

  return {
    SCHEMA_VERSION,
    LEGACY_EQUIVALENCE,
    TASK_STATUSES,
    TASK_PRIORITIES,
    NOTIFICATION_STATUSES,
    PERMISSION_ACTIONS,
    TaskSystem,
    TaskSystemError,
    DefaultTaskPermissionPolicy,
    stableJson
  };
});
