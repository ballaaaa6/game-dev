(function (root, factory) {
  if (typeof module === "object" && module.exports) {
    module.exports = factory();
  } else {
    root.Wave6TaskStorage = factory();
  }
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
  "use strict";

  function clone(value) {
    return value === undefined ? undefined : JSON.parse(JSON.stringify(value));
  }

  class MemoryTaskStorage {
    constructor(initialValue = null) {
      this.value = clone(initialValue);
      this.kind = "memory";
    }

    load() {
      return clone(this.value);
    }

    save(value) {
      this.value = clone(value);
    }

    clear() {
      this.value = null;
    }
  }

  class LocalStorageTaskStorage {
    constructor(options = {}) {
      this.key = options.key || "phase6.task_state.v1";
      this.storage = options.storage || (typeof localStorage !== "undefined" ? localStorage : null);
      this.kind = "local_storage";
    }

    load() {
      if (!this.storage) return null;
      const raw = this.storage.getItem(this.key);
      if (!raw) return null;
      return JSON.parse(raw);
    }

    save(value) {
      if (!this.storage) throw new Error("localStorage is unavailable");
      this.storage.setItem(this.key, JSON.stringify(value));
    }

    clear() {
      if (!this.storage) return;
      this.storage.removeItem(this.key);
    }
  }

  return {
    MemoryTaskStorage,
    LocalStorageTaskStorage
  };
});
