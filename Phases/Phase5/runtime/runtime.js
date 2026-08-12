(function (root, factory) {
  if (typeof module === "object" && module.exports) {
    module.exports = factory();
  } else {
    root.Wave5Runtime = factory();
  }
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
  "use strict";

  const AGENT_STATES = ["idle", "walking", "working", "sitting", "break", "talking"];
  const MOVEMENT_STATUSES = ["idle", "moving", "arrived", "blocked", "no_path", "unavailable"];
  const LEGACY_EQUIVALENCE = false;
  const DEFAULT_ANIMATION_POLICY = {
    fallbackMode: 0,
    status: "static_verified_frame_only",
    semantic_animation_verified: false,
    profiles: {
      "adapter.static.mode.0": {
        mode_sequence: [0],
        tick_period: 1,
        status: "static_verified_frame_only",
        semantic_status: "adapter_defined_not_legacy_recovered"
      },
      "adapter.idle": {
        mode_sequence: [0],
        tick_period: 1,
        status: "adapter_defined_static_profile",
        semantic_status: "adapter_defined_not_legacy_recovered"
      },
      "adapter.walk": {
        mode_sequence: [0, 1],
        tick_period: 4,
        status: "adapter_defined_cycle_profile",
        semantic_status: "adapter_defined_not_legacy_recovered"
      },
      "adapter.talk": {
        mode_sequence: [0, 1],
        tick_period: 6,
        status: "adapter_defined_cycle_profile",
        semantic_status: "adapter_defined_not_legacy_recovered"
      }
    }
  };

  function clone(value) {
    return value === undefined ? undefined : JSON.parse(JSON.stringify(value));
  }

  function positionKey(position) {
    return `${position[0]},${position[1]}`;
  }

  function normalizePosition(position) {
    if (!Array.isArray(position) || position.length !== 2) {
      throw new Error("position must be [x, y]");
    }
    const x = Number(position[0]);
    const y = Number(position[1]);
    if (!Number.isFinite(x) || !Number.isFinite(y)) {
      throw new Error("position values must be finite numbers");
    }
    return [x, y];
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

  function resolveObjectDepth(object) {
    const candidate = object && object.sort_key !== undefined
      ? object.sort_key
      : object && object.y !== undefined
        ? object.y
        : 0;
    const depth = Number(candidate);
    return Number.isFinite(depth) ? depth : 0;
  }

  function resolveObjectDestination(object) {
    if (Array.isArray(object && object.destination) && object.destination.length === 2) {
      return normalizePosition(object.destination);
    }
    return normalizePosition([object && object.x !== undefined ? object.x : 0, object && object.y !== undefined ? object.y : 0]);
  }

  function buildObjectDrawCommand(object) {
    const source = object || {};
    const destination = resolveObjectDestination(source);
    const asset = source.asset && source.asset.url ? clone(source.asset) : null;
    const sourceRect = Array.isArray(source.source_rect) ? clone(source.source_rect) : null;
    const drawSize = Array.isArray(source.draw_size) ? clone(source.draw_size) : null;
    const status = asset
      ? (source.renderer === "bounded_asset_renderer" ? "draw_command_ready" : "asset_preview_ready")
      : "diagnostic_marker_only";
    return {
      id: source.id || `${source.type || "object"}.${destination[0]}.${destination[1]}`,
      type: source.type || "OBJ_TYPE_UNKNOWN",
      renderer: source.renderer || "diagnostic_object_marker",
      status,
      depth: resolveObjectDepth(source),
      transform: {
        coordinate_space: source.coordinate_space || "adapter_canvas_pixels",
        anchor: source.anchor || "top_left",
        destination,
        semantics: source.transform_semantics || "explicit_manifest_destination",
        legacy_status: "not_universal_legacy_transform"
      },
      source_contract: clone(source.source_contract || null),
      crop_contract: clone(source.crop_contract || {
        status: "not_resolved",
        policy: "full_asset_preview_until_legacy_crop_resolved"
      }),
      placement_contract: clone(source.placement_contract || {
        status: "adapter_fixture_not_legacy_verified"
      }),
      commands: asset ? [{
        layer: "furniture",
        asset,
        source_rect: sourceRect,
        destination,
        draw_size: drawSize
      }] : [],
      fallback_marker: {
        x: destination[0],
        y: destination[1],
        label: source.type || "OBJ_TYPE_UNKNOWN"
      },
      source_status: source.status || "adapter_fixture",
      legacy_equivalence: LEGACY_EQUIVALENCE
    };
  }

  class LogicalClock {
    constructor(initialTick = 0) {
      this.tickCount = Number.isInteger(initialTick) ? initialTick : 0;
    }

    tick(delta = 1) {
      if (!Number.isInteger(delta) || delta < 0) {
        throw new Error("logical tick delta must be a non-negative integer");
      }
      this.tickCount += delta;
      return this.tickCount;
    }

    get value() {
      return this.tickCount;
    }
  }

  class EventLog {
    constructor() {
      this.sequence = 0;
      this.records = [];
    }

    append(type, payload, tick, status = "verified_adapter_event", source = "web_adapter") {
      const record = {
        sequence: this.sequence++,
        tick,
        type,
        payload: clone(payload || {}),
        status,
        source,
        legacy_equivalence: LEGACY_EQUIVALENCE
      };
      this.records.push(record);
      return record;
    }

    snapshot() {
      return clone(this.records);
    }
  }

  class DirectPathProvider {
    constructor(options = {}) {
      this.step = Number(options.step || 16);
      this.unavailable = Boolean(options.unavailable);
      this.noPathTargets = new Set((options.noPathTargets || []).map(positionKey));
    }

    findPath(from, to) {
      const start = normalizePosition(from);
      const target = normalizePosition(to);
      if (this.unavailable) return { status: "unavailable", path: [] };
      if (this.noPathTargets.has(positionKey(target))) return { status: "no_path", path: [] };
      if (start[0] === target[0] && start[1] === target[1]) {
        return { status: "path", path: [start] };
      }

      const path = [start];
      let current = start.slice();
      const moveAxis = (axis) => {
        while (current[axis] !== target[axis]) {
          const delta = target[axis] - current[axis];
          current = current.slice();
          current[axis] += Math.sign(delta) * Math.min(Math.abs(delta), this.step);
          path.push(current);
        }
      };
      moveAxis(0);
      moveAxis(1);
      return { status: "path", path };
    }
  }

  class ExplicitCollisionProvider {
    constructor(options = {}) {
      this.blocked = new Set((options.blocked || []).map(positionKey));
    }

    check(position) {
      return this.blocked.has(positionKey(position)) ? "blocked" : "clear";
    }
  }

  class SeatProvider {
    constructor(seats = []) {
      this.seats = new Map();
      seats.forEach((seat) => this.seats.set(seat.id, { id: seat.id, owner: null }));
    }

    occupy(actorId, seatId) {
      const seat = this.seats.get(seatId);
      if (!seat) return { result: "unavailable", seatId };
      if (seat.owner && seat.owner !== actorId) {
        return { result: "conflict", seatId, owner: seat.owner };
      }
      seat.owner = actorId;
      return { result: "occupied", seatId, owner: actorId };
    }

    release(actorId, seatId) {
      const seat = this.seats.get(seatId);
      if (!seat) return { result: "unavailable", seatId };
      if (seat.owner !== actorId) {
        return { result: "not_owner", seatId, owner: seat.owner };
      }
      seat.owner = null;
      return { result: "released", seatId, owner: null };
    }

    query(seatId) {
      const seat = this.seats.get(seatId);
      return seat ? clone(seat) : { id: seatId, owner: null, status: "unavailable" };
    }
  }

  class LocaleStore {
    constructor(locales = {}, defaultLocale = "th") {
      this.locales = clone(locales) || {};
      this.defaultLocale = defaultLocale;
    }

    resolve(id, requestedLocale, args = []) {
      const requested = requestedLocale || this.defaultLocale;
      const requestedTable = this.locales[requested] || {};
      const fallbackTable = this.locales[this.defaultLocale] || {};
      let text = requestedTable[id];
      let resolvedLocale = requested;
      let status = "resolved";
      if (text === undefined) {
        text = fallbackTable[id];
        resolvedLocale = this.defaultLocale;
        status = text === undefined ? "missing" : "fallback";
      }
      if (text === undefined || text === "") {
        return {
          id,
          text: text || "",
          resolved_locale: resolvedLocale,
          placeholder_tokens: [],
          status: text === "" ? "empty" : "missing",
          source: "csv_runtime_artifact"
        };
      }

      const tokens = [...text.matchAll(/<([0-9]+)>/g)].map((match) => `<${match[1]}>`);
      let formatted = text;
      tokens.forEach((token) => {
        const index = Number(token.slice(1, -1));
        if (args[index] !== undefined) formatted = formatted.replaceAll(token, String(args[index]));
      });
      return {
        id,
        text: formatted,
        resolved_locale: resolvedLocale,
        placeholder_tokens: tokens,
        status,
        source: "csv_runtime_artifact"
      };
    }
  }

  function createAgent(input) {
    const selectors = input.selectors || {};
    return {
      id: String(input.id),
      employeeId: input.employeeId ? String(input.employeeId) : undefined,
      name: input.name || String(input.id),
      role: input.role,
      position: normalizePosition(input.position || [0, 0]),
      state: AGENT_STATES.includes(input.state) ? input.state : "idle",
      animationId: input.animationId || "adapter.static.mode.0",
      selectors: {
        TFace: Number.isInteger(selectors.TFace) ? selectors.TFace : 2,
        TBody: Number.isInteger(selectors.TBody) ? selectors.TBody : 3,
        TMode: Number.isInteger(selectors.TMode) ? selectors.TMode : 0,
        TKage: Number.isInteger(selectors.TKage) ? selectors.TKage : 1
      },
      movement: {
        status: "idle",
        target: null,
        path: [],
        reason: null
      },
      seatId: null,
      bubbleId: null,
      taskId: null,
      taskStatus: null,
      raw: clone(input.raw || null),
      legacy_equivalence: LEGACY_EQUIVALENCE
    };
  }

  class OfficeRuntime {
    constructor(options = {}) {
      this.manifest = clone(options.manifest || {});
      this.clock = new LogicalClock(options.initialTick || 0);
      this.events = new EventLog();
      this.pathProvider = options.pathProvider || new DirectPathProvider();
      this.collisionProvider = options.collisionProvider || new ExplicitCollisionProvider();
      this.seatProvider = options.seatProvider || new SeatProvider([]);
      this.localeStore = options.localeStore || new LocaleStore({}, "th");
      this.bodyfaceRecords = options.bodyfaceRecords || [];
      this.assetBaseUrl = options.assetBaseUrl || "/game-dev-story-mod_Sprites/game";
      this.animationPolicy = clone(options.animationPolicy || DEFAULT_ANIMATION_POLICY);
      this.timerPolicy = clone(options.timerPolicy || this.manifest.timer_policy || {
        unit: "logical_tick",
        wall_clock_equivalence: false,
        legacy_unit_status: "unknown",
        expiry_comparison: "expires_at_tick <= clock.value"
      });
      this.agents = new Map();
      this.bubbles = new Map();
      this.notifications = new Map();
      this.nextBubbleId = 0;
      this.nextNotificationId = 0;
    }

    addAgent(input) {
      const agent = createAgent(input);
      if (this.agents.has(agent.id)) throw new Error(`duplicate actor id: ${agent.id}`);
      this.agents.set(agent.id, agent);
      this.events.append("actor.spawned", { actor_id: agent.id, state: agent.state }, this.clock.value);
      return clone(agent);
    }

    getAgent(actorId) {
      const agent = this.agents.get(actorId);
      if (!agent) throw new Error(`unknown actor id: ${actorId}`);
      return agent;
    }

    setAgentTaskProjection(actorId, taskId, taskStatus) {
      const agent = this.getAgent(actorId);
      agent.taskId = taskId === null || taskId === undefined ? null : String(taskId);
      agent.taskStatus = taskStatus === null || taskStatus === undefined ? null : String(taskStatus);
      return clone(agent);
    }

    recordAdapterEvent(type, payload = {}, source = "web_adapter") {
      return this.events.append(type, payload, this.clock.value, "verified_adapter_event", source);
    }

    setState(actorId, state) {
      if (!AGENT_STATES.includes(state)) throw new Error(`invalid adapter state: ${state}`);
      const agent = this.getAgent(actorId);
      const previous = agent.state;
      agent.state = state;
      this.events.append("state.changed", { actor_id: actorId, from: previous, to: state }, this.clock.value);
      return clone(agent);
    }

    requestMove(actorId, target) {
      const agent = this.getAgent(actorId);
      const normalizedTarget = normalizePosition(target);
      const result = this.pathProvider.findPath(agent.position, normalizedTarget, { actor_id: actorId });
      agent.movement.target = normalizedTarget;
      agent.movement.path = clone(result.path || []).slice(1);
      agent.movement.reason = null;

      if (result.status !== "path") {
        agent.movement.status = result.status === "no_path" ? "no_path" : "unavailable";
        agent.state = "idle";
        agent.movement.reason = result.status;
        this.events.append(`actor.move_${result.status}`, {
          actor_id: actorId,
          target: normalizedTarget
        }, this.clock.value);
        return clone(agent);
      }

      if (agent.movement.path.length === 0) {
        agent.movement.status = "arrived";
        agent.state = "idle";
        this.events.append("actor.arrived", { actor_id: actorId, position: agent.position }, this.clock.value);
        return clone(agent);
      }

      agent.movement.status = "moving";
      agent.state = "walking";
      this.events.append("actor.move_requested", {
        actor_id: actorId,
        target: normalizedTarget,
        path_length: agent.movement.path.length
      }, this.clock.value);
      return clone(agent);
    }

    occupySeat(actorId, seatId) {
      const result = this.seatProvider.occupy(actorId, seatId);
      const agent = this.getAgent(actorId);
      if (result.result === "occupied") {
        agent.seatId = seatId;
        agent.state = "sitting";
      }
      this.events.append("seat.occupy", { actor_id: actorId, ...result }, this.clock.value);
      return clone(result);
    }

    releaseSeat(actorId, seatId = this.getAgent(actorId).seatId) {
      const result = this.seatProvider.release(actorId, seatId);
      const agent = this.getAgent(actorId);
      if (result.result === "released") {
        agent.seatId = null;
        if (agent.state === "sitting") agent.state = "idle";
      }
      this.events.append("seat.release", { actor_id: actorId, ...result }, this.clock.value);
      return clone(result);
    }

    addBubble(input) {
      const actor = this.getAgent(input.actorId);
      const bubbleId = input.bubbleId || `bubble.${this.nextBubbleId++}`;
      const textResult = input.text !== undefined
        ? { text: String(input.text), status: "adapter_text", resolved_locale: input.locale || null }
        : this.localeStore.resolve(input.languageId, input.locale, input.args || []);
      const lifetime = Number.isInteger(input.lifetimeTicks) ? input.lifetimeTicks : 24;
      const bubble = {
        id: bubbleId,
        actor_id: actor.id,
        text: textResult.text,
        language_id: input.languageId || null,
        talk_tag: input.talkTag || null,
        raw_speaker_id: input.rawSpeakerId === undefined ? null : input.rawSpeakerId,
        position: clone(actor.position),
        created_at_tick: this.clock.value,
        expires_at_tick: this.clock.value + Math.max(0, lifetime),
        status: "active",
        lookup: textResult,
        legacy_equivalence: LEGACY_EQUIVALENCE
      };
      this.bubbles.set(bubbleId, bubble);
      actor.bubbleId = bubbleId;
      this.events.append("bubble.attached", { bubble_id: bubbleId, actor_id: actor.id }, this.clock.value);
      return clone(bubble);
    }

    requestDialogue(input) {
      this.events.append("dialogue.requested", {
        actor_id: input.actorId,
        talk_tag: input.talkTag || null,
        language_id: input.languageId || null,
        locale: input.locale || this.localeStore.defaultLocale
      }, this.clock.value);
      const bubble = this.addBubble(input);
      this.events.append("talk.resolved", {
        actor_id: input.actorId,
        talk_tag: input.talkTag || null,
        status: bubble.lookup.status
      }, this.clock.value);
      this.setState(input.actorId, "talking");
      return bubble;
    }

    addNotification(input) {
      const id = input.id || `notification.${this.nextNotificationId++}`;
      const lifetime = Number.isInteger(input.lifetimeTicks) ? input.lifetimeTicks : 96;
      const notification = {
        id,
        text: String(input.text || ""),
        graph_id: input.graphId === undefined ? -1 : input.graphId,
        created_at_tick: this.clock.value,
        expires_at_tick: this.clock.value + Math.max(0, lifetime),
        status: "active",
        graph_semantics: "raw_graph_id_not_decoded",
        legacy_equivalence: LEGACY_EQUIVALENCE
      };
      this.notifications.set(id, notification);
      this.events.append("notification.created", {
        notification_id: id,
        graph_id: notification.graph_id
      }, this.clock.value);
      return clone(notification);
    }

    step(count = 1) {
      if (!Number.isInteger(count) || count < 0) throw new Error("step count must be a non-negative integer");
      for (let index = 0; index < count; index += 1) {
        this.clock.tick(1);
        this.agents.forEach((agent) => this.stepAgent(agent));
        this.expireBubbles();
        this.expireNotifications();
      }
      return this.snapshot();
    }

    stepAgent(agent) {
      if (agent.movement.status !== "moving" || agent.movement.path.length === 0) return;
      const nextPosition = agent.movement.path[0];
      const collision = this.collisionProvider.check(nextPosition, { actor_id: agent.id });
      if (collision !== "clear") {
        agent.movement.status = collision === "blocked" ? "blocked" : "unavailable";
        agent.movement.reason = collision;
        agent.state = "idle";
        this.events.append(`actor.move_${agent.movement.status}`, {
          actor_id: agent.id,
          position: agent.position,
          attempted_position: nextPosition
        }, this.clock.value);
        return;
      }
      agent.position = normalizePosition(agent.movement.path.shift());
      this.events.append("actor.moved", { actor_id: agent.id, position: agent.position }, this.clock.value);
      if (agent.movement.path.length === 0) {
        agent.movement.status = "arrived";
        agent.state = "idle";
        this.events.append("actor.arrived", { actor_id: agent.id, position: agent.position }, this.clock.value);
      }
    }

    expireBubbles() {
      this.bubbles.forEach((bubble, bubbleId) => {
        if (bubble.status === "active" && bubble.expires_at_tick <= this.clock.value) {
          bubble.status = "expired";
          const agent = this.agents.get(bubble.actor_id);
          if (agent && agent.bubbleId === bubbleId) agent.bubbleId = null;
          this.events.append("bubble.expired", { bubble_id: bubbleId, actor_id: bubble.actor_id }, this.clock.value);
          this.bubbles.delete(bubbleId);
        }
      });
    }

    expireNotifications() {
      this.notifications.forEach((notification, notificationId) => {
        if (notification.status === "active" && notification.expires_at_tick <= this.clock.value) {
          notification.status = "expired";
          this.events.append("notification.expired", { notification_id: notificationId }, this.clock.value);
          this.notifications.delete(notificationId);
        }
      });
    }

    recordRawEvent(input = {}) {
      const record = this.events.append("legacy.event.raw", {
        mode: clone(input.mode),
        args: clone(input.args || []),
        source_tag: input.sourceTag || null
      }, this.clock.value, "raw_opaque_event");
      return clone(record);
    }

    resolveAnimationSelector(agent) {
      const profile = this.animationPolicy.profiles && this.animationPolicy.profiles[agent.animationId];
      if (!profile || !Array.isArray(profile.mode_sequence) || profile.mode_sequence.length === 0) {
        return {
          requestedMode: agent.selectors.TMode,
          profileId: null,
          frameIndex: 0,
          policy: "explicit_selector"
        };
      }
      const tickPeriod = Number.isInteger(profile.tick_period) && profile.tick_period > 0 ? profile.tick_period : 1;
      const frameIndex = Math.floor(this.clock.value / tickPeriod) % profile.mode_sequence.length;
      const selectedMode = profile.mode_sequence[frameIndex];
      return {
        requestedMode: Number.isInteger(selectedMode) ? selectedMode : agent.selectors.TMode,
        profileId: agent.animationId,
        frameIndex,
        policy: profile.status || "adapter_defined_profile"
      };
    }

    buildActorDrawCommand(agent) {
      const animation = this.resolveAnimationSelector(agent);
      const requestedMode = animation.requestedMode;
      const record = this.bodyfaceRecords.find((item) => item.mode === requestedMode);
      const resolvedRecord = record || this.bodyfaceRecords.find((item) => item.mode === this.animationPolicy.fallbackMode);
      if (!resolvedRecord) {
        return {
          actor_id: agent.id,
          status: "unresolved_bodyface_record",
          selectors: clone(agent.selectors),
          legacy_equivalence: LEGACY_EQUIVALENCE
        };
      }
      const faceResolved = Number.isInteger(agent.selectors.TFace) && agent.selectors.TFace >= 0 && agent.selectors.TFace <= 35;
      const bodyResolved = Number.isInteger(agent.selectors.TBody) && agent.selectors.TBody >= 0 && agent.selectors.TBody <= 25;
      const bodyBase = this.assetBaseUrl.replace(/\/$/, "");
      const commands = [];
      if (bodyResolved) {
        commands.push({
          layer: "body",
          image_array: "imgBody",
          asset: { asset_id: `body_${agent.selectors.TBody}`, url: `${bodyBase}/body${agent.selectors.TBody}.png`, status: "verified_filename_family" },
          source_rect: [resolvedRecord.body_src_x, resolvedRecord.body_src_y, resolvedRecord.body_width, resolvedRecord.body_height],
          destination: [agent.position[0] + resolvedRecord.body_dst_x, agent.position[1] + resolvedRecord.body_dst_y]
        });
      }
      if (faceResolved) {
        commands.push({
          layer: "face",
          image_array: "imgFace",
          asset: { asset_id: `face_${agent.selectors.TFace}`, url: `${bodyBase}/face_${agent.selectors.TFace}.png`, status: "verified_filename_family" },
          source_rect: [resolvedRecord.face_src_x, resolvedRecord.face_src_y, resolvedRecord.face_width, resolvedRecord.face_height],
          destination: [agent.position[0] + resolvedRecord.face_dst_x, agent.position[1] + resolvedRecord.face_dst_y]
        });
      }
      return {
        actor_id: agent.id,
        status: faceResolved && bodyResolved ? "draw_command_ready" : "partial_unresolved_selector",
        animation_policy: animation.policy === "explicit_selector"
          ? (requestedMode === resolvedRecord.mode ? "explicit_selector" : this.animationPolicy.status)
          : animation.policy,
        animation_profile: animation.profileId,
        animation_frame_index: animation.frameIndex,
        depth: agent.position[1],
        transform: {
          coordinate_space: "adapter_canvas_pixels",
          anchor: "bodyface_destination",
          semantics: "agent_position_plus_bodyface_offset",
          legacy_status: "not_universal_legacy_transform"
        },
        selectors: clone(agent.selectors),
        record_mode: resolvedRecord.mode,
        commands,
        unresolved: {
          TFace: faceResolved ? null : agent.selectors.TFace,
          TBody: bodyResolved ? null : agent.selectors.TBody
        },
        unresolved_classification: {
          TFace: faceResolved
            ? null
            : ([40, 41].includes(agent.selectors.TFace) ? "index_space_gap" : "unsupported_selector"),
          TBody: bodyResolved ? null : "unsupported_selector"
        },
        shadow: [resolvedRecord.shadow_dst_x, resolvedRecord.shadow_dst_y],
        legacy_equivalence: LEGACY_EQUIVALENCE
      };
    }

    renderCommands() {
      const objects = (this.manifest.objects || [])
        .map((object) => buildObjectDrawCommand(object))
        .sort((a, b) => (a.depth - b.depth) || a.id.localeCompare(b.id));
      const actors = [...this.agents.values()]
        .sort((a, b) => (a.position[1] - b.position[1]) || a.id.localeCompare(b.id))
        .map((agent) => this.buildActorDrawCommand(agent));
      const drawOrder = [
        ...objects.map((object) => ({ kind: "object", id: object.id, depth: object.depth })),
        ...actors.map((actor) => ({ kind: "actor", id: actor.actor_id, depth: actor.depth }))
      ].sort((a, b) => (a.depth - b.depth) || a.kind.localeCompare(b.kind) || a.id.localeCompare(b.id));
      return {
        room_id: this.manifest.room_id || "office.floor0.adapter",
        background: this.manifest.background || null,
        objects,
        actors,
        draw_order: drawOrder,
        bubbles: [...this.bubbles.values()].map(clone),
        notifications: [...this.notifications.values()].map(clone),
        timer_policy: clone(this.timerPolicy),
        legacy_equivalence: LEGACY_EQUIVALENCE
      };
    }

    snapshot() {
      return {
        tick: this.clock.value,
        office: {
          room_id: this.manifest.room_id || "office.floor0.adapter",
          agents: [...this.agents.values()].map(clone),
          bubbles: [...this.bubbles.values()].map(clone),
          notifications: [...this.notifications.values()].map(clone),
          legacy_equivalence: LEGACY_EQUIVALENCE
        },
        event_log: this.events.snapshot()
      };
    }

    digest() {
      return stableJson(this.snapshot());
    }
  }

  return {
    AGENT_STATES,
    MOVEMENT_STATUSES,
    LEGACY_EQUIVALENCE,
    DEFAULT_ANIMATION_POLICY,
    LogicalClock,
    EventLog,
    DirectPathProvider,
    ExplicitCollisionProvider,
    SeatProvider,
    LocaleStore,
    OfficeRuntime,
    createAgent,
    stableJson
  };
});
