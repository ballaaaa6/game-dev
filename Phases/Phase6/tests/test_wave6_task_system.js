const assert = require("assert");
const path = require("path");
const Wave5 = require(path.join(__dirname, "..", "..", "Phase5", "runtime", "runtime.js"));
const Wave6 = require(path.join(__dirname, "..", "runtime", "task_system.js"));
const Repository = require(path.join(__dirname, "..", "runtime", "task_repository.js"));

function createHost(repository = new Repository.MemoryTaskRepository()) {
  const runtime = new Wave5.OfficeRuntime();
  runtime.addAgent({ id: "actor.0", name: "Aoi", position: [0, 0] });
  runtime.addAgent({ id: "actor.1", name: "Mika", position: [1, 0] });
  const tasks = new Wave6.TaskSystem({
    clock: runtime.clock,
    getAgent: (id) => runtime.getAgent(id),
    listAgents: () => [...runtime.agents.values()],
    projectAgent: (id, taskId, status) => runtime.setAgentTaskProjection(id, taskId, status),
    setAgentState: (id, state) => runtime.setState(id, state),
    emitRuntimeEvent: (type, payload, source) => runtime.recordAdapterEvent(type, payload, source),
    repository
  });
  return { runtime, tasks, repository };
}

function expectError(fn, code) {
  assert.throws(fn, (error) => error && error.code === code, `expected ${code}`);
}

function testCreateAndDeterministicQueue() {
  const { tasks } = createHost();
  const normal = tasks.createTask({ title: "Normal task", priority: "normal" });
  const urgent = tasks.createTask({ title: "Urgent task", priority: "urgent" });
  const high = tasks.createTask({ title: "High task", priority: "high" });
  assert.deepStrictEqual(tasks.listTasks().map((task) => task.id), [urgent.id, high.id, normal.id]);
  assert.deepStrictEqual(tasks.getStats(), { total: 3, queued: 3, working: 0, blocked: 0, done: 0 });
}

function testAssignmentRules() {
  const { tasks } = createHost();
  const first = tasks.createTask({ title: "First" });
  const second = tasks.createTask({ title: "Second" });
  tasks.assignTask(first.id, "actor.0");
  expectError(() => tasks.assignTask(second.id, "actor.0"), "agent_busy");
  expectError(() => tasks.assignTask(first.id, "actor.1"), "task_already_assigned");
  assert.strictEqual(tasks.getTask(first.id).assignee_id, "actor.0");
}

function testStartRequiresAssignmentAndProjectsAgent() {
  const { runtime, tasks } = createHost();
  const task = tasks.createTask({ title: "Startable" });
  expectError(() => tasks.startTask(task.id), "assignee_required");
  tasks.assignTask(task.id, "actor.0");
  tasks.startTask(task.id, "actor.0");
  assert.strictEqual(tasks.getTask(task.id).status, "working");
  assert.strictEqual(runtime.getAgent("actor.0").taskId, task.id);
  assert.strictEqual(runtime.getAgent("actor.0").taskStatus, "working");
  assert.strictEqual(runtime.getAgent("actor.0").state, "working");
}

function testMovingAgentCannotStart() {
  const { runtime, tasks } = createHost();
  const task = tasks.createTask({ title: "Wait for arrival" });
  tasks.assignTask(task.id, "actor.0");
  runtime.requestMove("actor.0", [2, 0]);
  expectError(() => tasks.startTask(task.id, "actor.0"), "agent_moving");
  assert.strictEqual(tasks.getTask(task.id).status, "queued");
}

function testBlockResumeRequiresReason() {
  const { tasks } = createHost();
  const task = tasks.createTask({ title: "Blockable" });
  tasks.assignTask(task.id, "actor.0");
  tasks.startTask(task.id, "actor.0");
  expectError(() => tasks.blockTask(task.id, ""), "blocked_reason_required");
  tasks.blockTask(task.id, "Waiting for input", "actor.0");
  assert.strictEqual(tasks.getTask(task.id).blocked_reason, "Waiting for input");
  assert.strictEqual(tasks.getTask(task.id).status, "blocked");
  tasks.resumeTask(task.id, "actor.0");
  assert.strictEqual(tasks.getTask(task.id).status, "working");
}

function testWorkingTaskCannotUnassign() {
  const { tasks } = createHost();
  const task = tasks.createTask({ title: "Keep ownership" });
  tasks.assignTask(task.id, "actor.0");
  tasks.startTask(task.id, "actor.0");
  expectError(() => tasks.unassignTask(task.id), "working_task_requires_stop");
}

function testCompleteClearsProjectionAndNotifiesCreator() {
  const { runtime, tasks } = createHost();
  const task = tasks.createTask({ title: "Complete me", createdBy: "operator" });
  tasks.assignTask(task.id, "actor.0");
  tasks.startTask(task.id, "actor.0");
  tasks.completeTask(task.id, "actor.0");
  const result = tasks.getTask(task.id);
  assert.strictEqual(result.status, "done");
  assert.strictEqual(result.assignee_id, null);
  assert.strictEqual(runtime.getAgent("actor.0").taskId, null);
  assert.strictEqual(runtime.getAgent("actor.0").state, "idle");
  assert(tasks.getNotifications({ unreadOnly: true }).some((item) => item.kind === "task.completed"));
}

function testNotificationReadAndActivity() {
  const { tasks } = createHost();
  const task = tasks.createTask({ title: "Notify me" });
  tasks.assignTask(task.id, "actor.0");
  const unread = tasks.getNotifications({ recipientId: "actor.0", unreadOnly: true });
  assert.strictEqual(unread.length, 1);
  tasks.markNotificationRead(unread[0].id, "actor.0");
  assert.strictEqual(tasks.getNotifications({ recipientId: "actor.0", unreadOnly: true }).length, 0);
  const dismissed = tasks.getNotifications({ recipientId: "actor.0" })[0];
  tasks.dismissNotification(dismissed.id, "actor.0");
  assert.strictEqual(tasks.getNotifications({ recipientId: "actor.0" })[0].status, "dismissed");
  assert(tasks.getActivity({ taskId: task.id }).some((event) => event.type === "task.assigned"));
  assert(tasks.getActivity({ taskId: task.id }).some((event) => event.type === "task.notification.read"));
  assert(tasks.getActivity({ taskId: task.id }).some((event) => event.type === "task.notification.dismissed"));
}

function testDoneIsTerminal() {
  const { tasks } = createHost();
  const task = tasks.createTask({ title: "Terminal" });
  tasks.assignTask(task.id, "actor.0");
  tasks.startTask(task.id, "actor.0");
  tasks.completeTask(task.id, "actor.0");
  expectError(() => tasks.startTask(task.id), "invalid_transition");
  expectError(() => tasks.assignTask(task.id, "actor.1"), "task_done");
}

function testPersistenceAndRestore() {
  const repository = new Repository.MemoryTaskRepository();
  const first = createHost(repository);
  const task = first.tasks.createTask({ title: "Persisted", priority: "high" });
  first.tasks.assignTask(task.id, "actor.1");
  const persisted = first.tasks.snapshot();
  const second = createHost(repository);
  assert.strictEqual(second.tasks.load(), true);
  assert.deepStrictEqual(second.tasks.getTask(task.id).title, "Persisted");
  assert.strictEqual(second.runtime.getAgent("actor.1").taskId, task.id);
  assert.deepStrictEqual(second.tasks.snapshot().tasks, persisted.tasks);
}

function testLegacySnapshotMigration() {
  const legacySnapshot = {
    schema_version: "wave6-task-state-v1",
    tick: 3,
    tasks: [],
    notifications: [],
    activity_log: [],
    next_ids: { task: 0, notification: 0, activity: 0 },
    legacy_equivalence: false
  };
  const repository = new Repository.MemoryTaskRepository(legacySnapshot);
  const { tasks } = createHost(repository);
  assert.strictEqual(tasks.load(), true);
  assert.strictEqual(tasks.getPersistenceStatus().status, "loaded_migrated");
  assert.strictEqual(tasks.getPersistenceStatus().migrated_from, "wave6-task-state-v1");
  tasks.createTask({ title: "After migration" });
  assert.strictEqual(repository.load().schema_version, "wave6-task-repository-v1");
}

function testRevisionConflictAndReload() {
  const repository = new Repository.MemoryTaskRepository();
  const first = createHost(repository);
  const second = createHost(repository);
  first.tasks.load();
  second.tasks.load();
  first.tasks.createTask({ title: "First writer" });
  second.tasks.createTask({ title: "Stale writer" });
  assert.strictEqual(second.tasks.getPersistenceStatus().status, "conflict_needs_reload");
  assert.strictEqual(second.tasks.reloadFromRepository(), true);
  assert.strictEqual(second.tasks.listTasks().length, 1);
  assert.strictEqual(second.tasks.listTasks()[0].title, "First writer");
}

function testPermissionPolicyAndExportImport() {
  const { tasks } = createHost();
  const task = tasks.createTask({ title: "Permissioned" });
  tasks.assignTask(task.id, "actor.0");
  expectError(() => tasks.assignTask(task.id, "actor.1", "actor.1"), "permission_denied");
  const exportData = tasks.exportData();
  const imported = createHost(new Repository.MemoryTaskRepository());
  imported.tasks.importData(exportData, { actorId: "operator" });
  assert.strictEqual(imported.tasks.getTask(task.id).title, "Permissioned");
  const notification = tasks.getNotifications({ recipientId: "actor.0" })[0];
  expectError(() => tasks.markNotificationRead(notification.id, "actor.1"), "permission_denied");
  tasks.markNotificationRead(notification.id, "actor.0");
}

function testInvalidSnapshotAndFilters() {
  const { tasks } = createHost();
  expectError(() => tasks.restore({ schema_version: "wrong", tasks: [], notifications: [], activity_log: [] }), "invalid_snapshot");
  tasks.createTask({ title: "Unassigned urgent", priority: "urgent" });
  const assigned = tasks.createTask({ title: "Assigned low", priority: "low" });
  tasks.assignTask(assigned.id, "actor.1");
  assert.strictEqual(tasks.listTasks({ unassigned: true }).length, 1);
  assert.strictEqual(tasks.listTasks({ assigneeId: "actor.1" }).length, 1);
  assert.strictEqual(tasks.listTasks({ search: "low" }).length, 1);
}

function testInvalidSnapshotDoesNotReplaceLiveState() {
  const { tasks } = createHost();
  const task = tasks.createTask({ title: "Keep current state" });
  tasks.assignTask(task.id, "actor.0");
  const before = tasks.digest();
  const invalid = tasks.snapshot();
  invalid.notifications[0].status = "unknown";
  expectError(() => tasks.restore(invalid), "invalid_snapshot");
  assert.strictEqual(tasks.digest(), before);
  assert.strictEqual(tasks.getAgentTask("actor.0").id, task.id);
}

function testRepositoryFailuresRemainVisibleAndDoNotEraseMemory() {
  const unavailable = new Repository.LocalStorageTaskRepository({ storage: null });
  assert.throws(() => unavailable.load(), (error) => error && error.code === "storage_unavailable");
  assert.throws(() => unavailable.clear(), (error) => error && error.code === "storage_unavailable");
  const failing = {
    kind: "failing_repository",
    load() { throw new Error("load failed"); },
    save() { throw new Error("save failed"); },
    clear() { throw new Error("clear failed"); }
  };
  const { tasks } = createHost(failing);
  const task = tasks.createTask({ title: "Memory fallback" });
  assert.strictEqual(tasks.getTask(task.id).title, "Memory fallback");
  assert.strictEqual(tasks.getPersistenceStatus().status, "degraded_memory_only");
  assert.strictEqual(tasks.load(), false);
  assert.strictEqual(tasks.getTask(task.id).title, "Memory fallback");
  tasks.clear({ actorId: "operator", record: false });
  assert.strictEqual(tasks.taskCount, 0);
  assert.strictEqual(tasks.getPersistenceStatus().status, "degraded_memory_only");
}

function testRepositorySaveEnvelopeIsValidated() {
  const invalidSave = {
    kind: "invalid_save_repository",
    load() { return null; },
    save() { return { schema_version: "wrong" }; },
    clear() {}
  };
  const { tasks } = createHost(invalidSave);
  tasks.createTask({ title: "Invalid save response" });
  const status = tasks.getPersistenceStatus();
  assert.strictEqual(status.status, "degraded_memory_only");
  assert(status.last_error.includes("invalid envelope"));
}

function testRuntimeEventMirror() {
  const { runtime, tasks } = createHost();
  const task = tasks.createTask({ title: "Mirror" });
  const event = runtime.events.records.find((item) => item.type === "task.created");
  assert(event);
  assert.strictEqual(event.source, "phase6_task_system");
  assert.strictEqual(event.payload.task_id, task.id);
}

testCreateAndDeterministicQueue();
testAssignmentRules();
testStartRequiresAssignmentAndProjectsAgent();
testMovingAgentCannotStart();
testBlockResumeRequiresReason();
testWorkingTaskCannotUnassign();
testCompleteClearsProjectionAndNotifiesCreator();
testNotificationReadAndActivity();
testDoneIsTerminal();
testPersistenceAndRestore();
testLegacySnapshotMigration();
testRevisionConflictAndReload();
testPermissionPolicyAndExportImport();
testInvalidSnapshotAndFilters();
testInvalidSnapshotDoesNotReplaceLiveState();
testRepositoryFailuresRemainVisibleAndDoNotEraseMemory();
testRepositorySaveEnvelopeIsValidated();
testRuntimeEventMirror();
console.log("Wave 6 task system tests passed: 18 scenarios");
