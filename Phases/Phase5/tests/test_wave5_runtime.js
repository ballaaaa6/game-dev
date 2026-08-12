const assert = require("assert");
const fs = require("fs");
const path = require("path");
const Wave5 = require(path.join(__dirname, "..", "runtime", "runtime.js"));

const root = path.join(__dirname, "..", "..");
const manifest = JSON.parse(fs.readFileSync(path.join(__dirname, "..", "runtime", "data", "room_manifest.json"), "utf8"));
const bodyface = JSON.parse(fs.readFileSync(path.join(root, "Phase2", "artifacts", "bodyface_analysis.json"), "utf8"));
const records = bodyface.records.map((record) => record.raw_record || record);

function createRuntime(options = {}) {
  return new Wave5.OfficeRuntime({
    manifest,
    bodyfaceRecords: records,
    animationPolicy: options.animationPolicy,
    pathProvider: options.pathProvider || new Wave5.DirectPathProvider({ step: 1 }),
    collisionProvider: options.collisionProvider || new Wave5.ExplicitCollisionProvider(),
    seatProvider: options.seatProvider || new Wave5.SeatProvider([{ id: "seat.0" }]),
    localeStore: options.localeStore || new Wave5.LocaleStore({ th: { "#demo": "ทำงาน <0>" } }, "th")
  });
}

function addAgent(runtime, input = {}) {
  return runtime.addAgent({
    id: input.id || "actor.0",
    name: input.name || "Test actor",
    position: input.position || [0, 0],
    animationId: input.animationId,
    selectors: input.selectors || { TFace: 2, TBody: 3, TMode: 0, TKage: 1 }
  });
}

function testMovement() {
  const runtime = createRuntime();
  addAgent(runtime);
  runtime.requestMove("actor.0", [2, 0]);
  runtime.step(2);
  assert.deepStrictEqual(runtime.getAgent("actor.0").position, [2, 0]);
  assert.strictEqual(runtime.getAgent("actor.0").movement.status, "arrived");
}

function testBlockedMovementDoesNotTeleport() {
  const runtime = createRuntime({
    collisionProvider: new Wave5.ExplicitCollisionProvider({ blocked: [[1, 0]] })
  });
  addAgent(runtime);
  runtime.requestMove("actor.0", [2, 0]);
  runtime.step(1);
  assert.deepStrictEqual(runtime.getAgent("actor.0").position, [0, 0]);
  assert.strictEqual(runtime.getAgent("actor.0").movement.status, "blocked");
}

function testSeatOwnership() {
  const runtime = createRuntime();
  addAgent(runtime);
  addAgent(runtime, { id: "actor.1", position: [1, 0] });
  assert.strictEqual(runtime.occupySeat("actor.0", "seat.0").result, "occupied");
  assert.strictEqual(runtime.occupySeat("actor.1", "seat.0").result, "conflict");
  assert.strictEqual(runtime.releaseSeat("actor.0", "seat.0").result, "released");
  assert.strictEqual(runtime.occupySeat("actor.1", "seat.0").result, "occupied");
  assert.strictEqual(runtime.getAgent("actor.1").state, "sitting");
}

function testLifecycleCleanup() {
  const runtime = createRuntime();
  addAgent(runtime);
  runtime.addBubble({ actorId: "actor.0", text: "hello", lifetimeTicks: 2 });
  runtime.addNotification({ text: "notice", graphId: 1, lifetimeTicks: 2 });
  runtime.step(1);
  assert.strictEqual(runtime.bubbles.size, 1);
  assert.strictEqual(runtime.notifications.size, 1);
  runtime.step(1);
  assert.strictEqual(runtime.bubbles.size, 0);
  assert.strictEqual(runtime.notifications.size, 0);
  assert(runtime.events.records.some((event) => event.type === "bubble.expired"));
  assert(runtime.events.records.some((event) => event.type === "notification.expired"));
}

function testLocaleAndDrawContract() {
  const runtime = createRuntime();
  addAgent(runtime);
  const resolved = runtime.localeStore.resolve("#demo", "th", ["ตอนนี้"]);
  assert.strictEqual(resolved.text, "ทำงาน ตอนนี้");
  runtime.requestDialogue({ actorId: "actor.0", languageId: "#demo", args: ["ตอนนี้"], lifetimeTicks: 4 });
  const draw = runtime.renderCommands().actors[0];
  assert.strictEqual(draw.status, "draw_command_ready");
  assert.deepStrictEqual(draw.commands[0].source_rect, [0, 0, 16, 16]);
  assert.deepStrictEqual(draw.commands[1].source_rect, [48, 0, 16, 15]);

  const unresolved = createRuntime();
  addAgent(unresolved, { selectors: { TFace: 40, TBody: 3, TMode: 0, TKage: 1 } });
  const unresolvedDraw = unresolved.renderCommands().actors[0];
  assert.strictEqual(unresolvedDraw.status, "partial_unresolved_selector");
  assert.strictEqual(unresolvedDraw.unresolved.TFace, 40);
  assert.strictEqual(unresolvedDraw.unresolved_classification.TFace, "index_space_gap");
  assert.strictEqual(unresolvedDraw.commands.some((command) => command.layer === "face"), false);
}

function testDeterministicReplay() {
  const run = () => {
    const runtime = createRuntime();
    addAgent(runtime);
    runtime.requestMove("actor.0", [2, 0]);
    runtime.addBubble({ actorId: "actor.0", text: "replay", lifetimeTicks: 3 });
    runtime.step(2);
    return runtime.digest();
  };
  assert.strictEqual(run(), run());
}

function testFurnitureAndDepthContract() {
  const runtime = createRuntime();
  addAgent(runtime, { id: "actor.0", position: [220, 326] });
  addAgent(runtime, { id: "actor.1", position: [336, 354] });
  const commands = runtime.renderCommands();
  assert.strictEqual(commands.objects.length, 3);
  assert(commands.objects.every((object) => object.status === "draw_command_ready"));
  assert(commands.objects.every((object) => object.commands[0].asset.url.includes("/office/")));
  assert.deepStrictEqual(commands.objects.map((object) => object.id), [
    "reception.fixture.0",
    "desk.fixture.0",
    "chair.fixture.0"
  ]);
  assert.deepStrictEqual(commands.draw_order.map((item) => item.id), [
    "reception.fixture.0",
    "actor.0",
    "actor.1",
    "desk.fixture.0",
    "chair.fixture.0"
  ]);
  assert.strictEqual(commands.objects[0].transform.coordinate_space, "adapter_canvas_pixels");
  assert.strictEqual(commands.objects[0].transform.legacy_status, "not_universal_legacy_transform");
  assert.strictEqual(commands.objects.find((object) => object.type === "OBJ_TYPE_CHAIR").source_contract.legacy_image_slot, "imgBihin_[1]");
  assert.strictEqual(commands.objects.find((object) => object.type === "OBJ_TYPE_DESK").source_contract.selector_field, "DDDesk");
  assert.strictEqual(commands.objects.find((object) => object.type === "OBJ_TYPE_RECEPTION").source_contract.legacy_image_slot, "imgFloorParts");
  assert.strictEqual(commands.objects[0].crop_contract.status, "field_flow_verified_numeric_crop_unresolved");
}

function testTimerPolicyContract() {
  const runtime = createRuntime();
  addAgent(runtime);
  const initial = runtime.renderCommands().timer_policy;
  assert.strictEqual(initial.unit, "logical_tick");
  assert.strictEqual(initial.wall_clock_equivalence, false);
  runtime.addBubble({ actorId: "actor.0", text: "zero", lifetimeTicks: 0 });
  runtime.step(1);
  assert.strictEqual(runtime.bubbles.size, 0);
}

function testAdapterAnimationProfile() {
  const runtime = createRuntime({
    animationPolicy: {
      fallbackMode: 0,
      status: "static_verified_frame_only",
      semantic_animation_verified: false,
      profiles: {
        "adapter.test.walk": {
          mode_sequence: [0, 1],
          tick_period: 4,
          status: "adapter_defined_cycle_profile"
        }
      }
    }
  });
  addAgent(runtime, { animationId: "adapter.test.walk" });
  assert.strictEqual(runtime.renderCommands().actors[0].record_mode, 0);
  runtime.step(4);
  const command = runtime.renderCommands().actors[0];
  assert.strictEqual(command.record_mode, 1);
  assert.strictEqual(command.animation_profile, "adapter.test.walk");
  assert.strictEqual(command.animation_policy, "adapter_defined_cycle_profile");
}

function testRawEventModePreservation() {
  const runtime = createRuntime();
  const event = runtime.recordRawEvent({ mode: 0x14, args: [7, 9], sourceTag: "test" });
  assert.strictEqual(event.type, "legacy.event.raw");
  assert.strictEqual(event.status, "raw_opaque_event");
  assert.strictEqual(event.payload.mode, 0x14);
  assert.deepStrictEqual(event.payload.args, [7, 9]);
}

testMovement();
testBlockedMovementDoesNotTeleport();
testSeatOwnership();
testLifecycleCleanup();
testLocaleAndDrawContract();
testDeterministicReplay();
testFurnitureAndDepthContract();
testTimerPolicyContract();
testAdapterAnimationProfile();
testRawEventModePreservation();
console.log("Wave 5 runtime tests passed: 10 scenarios");
