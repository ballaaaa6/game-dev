import { existsSync, readFileSync } from "node:fs";
import { resolve } from "node:path";

import { describe, expect, it } from "vitest";

const root = resolve(process.cwd(), "../..");
const evidenceRoot = resolve(root, "knowledge/fixtures/accepted/visual-port/v1");
const reportsRoot = resolve(root, "docs/Phases/VisualPort");

const requiredJson = [
  "sprite-contract.json",
  "seb-contract.json",
  "image-opt-contract.json",
  "resource-lookup-contract.json",
  "fixture-manifest.json",
  "native-recovery-map.json",
  "parity-results.json",
  "unknowns.json",
] as const;

describe("V1 evidence contracts", () => {
  it("parses all eight required artifacts with stable provenance hashes", () => {
    for (const name of requiredJson) {
      const artifact = readArtifact(name);
      expect(artifact.schema_version).toEqual(expect.any(String));
      expect(artifact.status).toEqual(expect.any(String));
      expect(artifact.determinism).toMatchObject({
        algorithm: "stable-json-sha256 excluding determinism.content_hash",
        content_hash: expect.stringMatching(/^[0-9a-f]{64}$/),
      });
      expect(artifact.source ?? artifact.source_refs).toBeTruthy();
      // Canonical content hashes are validated by the Python gate. Keep this
      // runtime check focused on the artifact contract and hash shape because
      // JSON serializer ordering differs between the two runtimes.
      expect(artifact.determinism.content_hash).toMatch(/^[0-9a-f]{64}$/);
    }
  });

  it("requires native provenance, parity domains, exact groups, and explicit unknown fields", () => {
    const native = readArtifact("native-recovery-map.json");
    expect(native.apk_sha256).toMatch(/^[0-9a-f]{64}$/i);
    expect(native.dump_sha256).toMatch(/^[0-9a-f]{64}$/i);
    expect(native.records.length).toBeGreaterThan(15);
    for (const record of native.records) {
      expect(record.native_rva).toMatch(/0x[0-9A-Fa-f]+/);
      expect(record.apk_sha256).toMatch(/^[0-9a-f]{64}$/i);
      expect(record.dump_sha256).toMatch(/^[0-9a-f]{64}$/i);
      expect(record.fixture_refs).toEqual(expect.any(Array));
      expect(record.proof_class).toEqual(expect.any(String));
    }

    const resource = readArtifact("resource-lookup-contract.json");
    expect(resource.group_ids).toEqual([
      "resChip_",
      "resInterface_",
      "resHuman_",
      "resCom_",
      "resGame_",
      "resEffect_",
      "resMeeting_",
      "resAvatarBody_",
      "resAvatarHead_",
      "resDevelop_",
      "resWindow_",
    ]);
    expect(resource.atlas_contract.status).toBe("deferred");

    const parity = readArtifact("parity-results.json");
    expect(parity.parity_results.length).toBeGreaterThan(0);
    expect(parity.boundaries).toEqual(
      expect.arrayContaining([
        expect.objectContaining({
          source_member: "01_GAME_PACKS/develop/develop_menu_light.seb",
          status: "NON_SELECTED_UNSUPPORTED",
        }),
      ]),
    );

    const unknowns = readArtifact("unknowns.json");
    for (const item of unknowns.unknowns) {
      expect(item).toEqual(expect.objectContaining({
        id: expect.any(String),
        class: expect.any(String),
        method: expect.any(String),
        question: expect.any(String),
        known_evidence: expect.anything(),
        missing_evidence: expect.anything(),
        affected_fixtures: expect.any(Array),
        impact: expect.any(String),
        next_investigation: expect.any(String),
      }));
    }
  });

  it("contains the four V1 reports and an explicit V2 stop decision", () => {
    for (const name of [
      "V1_CORE_FORMAT_RECOVERY.md",
      "V1_FIXTURE_MATRIX.md",
      "V1_NATIVE_RECOVERY.md",
      "V1_PARITY_REPORT.md",
    ]) {
      const path = resolve(reportsRoot, name);
      expect(existsSync(path)).toBe(true);
      const report = readFileSync(path, "utf8");
      expect(report).toMatch(/V1/);
      expect(report).toMatch(/deferred|unknown/i);
      expect(report).toMatch(/V2/);
    }
  });
});

function readArtifact(name: string): Record<string, any> {
  return JSON.parse(readFileSync(resolve(evidenceRoot, name), "utf8")) as Record<string, any>;
}
