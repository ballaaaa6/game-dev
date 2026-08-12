(function (root, factory) {
  if (typeof module === "object" && module.exports) {
    module.exports = factory();
  } else {
    root.Wave6TaskRepository = factory();
  }
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
  "use strict";

  const REPOSITORY_SCHEMA_VERSION = "wave6-task-repository-v1";
  const TASK_STATE_SCHEMA_VERSION = "wave6-task-state-v1";

  function clone(value) {
    return value === undefined ? undefined : JSON.parse(JSON.stringify(value));
  }

  class TaskRepositoryError extends Error {
    constructor(code, message) {
      super(message);
      this.name = "TaskRepositoryError";
      this.code = code;
    }
  }

  class RepositoryConflictError extends TaskRepositoryError {
    constructor(expectedRevision, actualRevision) {
      super("repository_conflict", `repository revision conflict: expected ${expectedRevision}, actual ${actualRevision}`);
      this.expectedRevision = expectedRevision;
      this.actualRevision = actualRevision;
    }
  }

  function normalizeEnvelope(value) {
    if (!value) return null;
    if (value.schema_version === REPOSITORY_SCHEMA_VERSION) {
      if (!Number.isInteger(value.revision) || value.revision < 0 || !value.snapshot) {
        throw new TaskRepositoryError("invalid_repository_envelope", "repository envelope is invalid");
      }
      return clone(value);
    }
    if (value.schema_version === TASK_STATE_SCHEMA_VERSION) {
      return {
        schema_version: REPOSITORY_SCHEMA_VERSION,
        revision: 0,
        updated_at_tick: Number.isInteger(value.tick) ? value.tick : 0,
        migrated_from: TASK_STATE_SCHEMA_VERSION,
        snapshot: clone(value)
      };
    }
    throw new TaskRepositoryError("invalid_repository_envelope", "unsupported task repository schema");
  }

  class TaskRepository {
    constructor(kind = "abstract") {
      this.kind = kind;
    }

    load() {
      throw new TaskRepositoryError("not_implemented", "TaskRepository.load must be implemented");
    }

    save() {
      throw new TaskRepositoryError("not_implemented", "TaskRepository.save must be implemented");
    }

    clear() {
      throw new TaskRepositoryError("not_implemented", "TaskRepository.clear must be implemented");
    }
  }

  class MemoryTaskRepository extends TaskRepository {
    constructor(initialValue = null) {
      super("memory_repository");
      this.envelope = normalizeEnvelope(initialValue);
    }

    load() {
      return clone(this.envelope);
    }

    save(snapshot, expectedRevision = null) {
      const actualRevision = this.envelope ? this.envelope.revision : 0;
      if (expectedRevision !== null && expectedRevision !== actualRevision) {
        throw new RepositoryConflictError(expectedRevision, actualRevision);
      }
      this.envelope = {
        schema_version: REPOSITORY_SCHEMA_VERSION,
        revision: actualRevision + 1,
        updated_at_tick: Number.isInteger(snapshot && snapshot.tick) ? snapshot.tick : 0,
        migrated_from: null,
        snapshot: clone(snapshot)
      };
      return clone(this.envelope);
    }

    clear() {
      this.envelope = null;
    }
  }

  class LocalStorageTaskRepository extends TaskRepository {
    constructor(options = {}) {
      super("local_storage_repository");
      this.key = options.key || "phase6.task_state.v1";
      this.storage = options.storage || (typeof localStorage !== "undefined" ? localStorage : null);
    }

    load() {
      if (!this.storage) throw new TaskRepositoryError("storage_unavailable", "localStorage is unavailable");
      const raw = this.storage.getItem(this.key);
      if (!raw) return null;
      return normalizeEnvelope(JSON.parse(raw));
    }

    save(snapshot, expectedRevision = null) {
      if (!this.storage) throw new TaskRepositoryError("storage_unavailable", "localStorage is unavailable");
      const current = this.load();
      const actualRevision = current ? current.revision : 0;
      if (expectedRevision !== null && expectedRevision !== actualRevision) {
        throw new RepositoryConflictError(expectedRevision, actualRevision);
      }
      const envelope = {
        schema_version: REPOSITORY_SCHEMA_VERSION,
        revision: actualRevision + 1,
        updated_at_tick: Number.isInteger(snapshot && snapshot.tick) ? snapshot.tick : 0,
        migrated_from: current && current.migrated_from ? current.migrated_from : null,
        snapshot: clone(snapshot)
      };
      this.storage.setItem(this.key, JSON.stringify(envelope));
      return clone(envelope);
    }

    clear() {
      if (!this.storage) throw new TaskRepositoryError("storage_unavailable", "localStorage is unavailable");
      this.storage.removeItem(this.key);
    }
  }

  return {
    REPOSITORY_SCHEMA_VERSION,
    TASK_STATE_SCHEMA_VERSION,
    TaskRepository,
    TaskRepositoryError,
    RepositoryConflictError,
    MemoryTaskRepository,
    LocalStorageTaskRepository
  };
});
