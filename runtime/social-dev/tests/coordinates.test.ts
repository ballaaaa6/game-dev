import { describe, expect, it } from "vitest";
import { loadRuntimeCatalogs } from "../src/catalog/load-contracts";
import {
  actorToCanvas,
  mapChipToCanvas,
  mapChipWorldOrigin,
  objectToCanvas,
  objectWorldOrigin,
  structuralFacilityMapCell,
  structuralFacilityToCanvas,
} from "../src/scene/coordinates";

describe("Phase 3C native coordinate adapters", () => {
  it("keeps the room, map-chip, object, and actor probes distinct", () => {
    const catalogs = loadRuntimeCatalogs();
    expect(mapChipWorldOrigin([8, 4])).toEqual({ x: 480, y: -80 });
    expect(objectWorldOrigin([8, 4])).toEqual({ x: 240, y: -31 });
    expect(actorToCanvas({ x: 280, y: -31 }, catalogs.camera)).toEqual({ x: 722, y: 229 });
    expect(objectToCanvas([8, 4], catalogs.camera)).toEqual({ x: 682, y: 229 });
    expect(mapChipToCanvas([8, 4], catalogs.camera)).toEqual({ x: 562, y: 180 });
  });

  it("maps the raw type-4 centers into the native 3x3 MapChip facility band", () => {
    const catalogs = loadRuntimeCatalogs();
    expect(structuralFacilityMapCell([4, 2])).toEqual([4, 5]);
    expect(structuralFacilityMapCell([7, 2])).toEqual([7, 5]);
    expect(structuralFacilityToCanvas(structuralFacilityMapCell([4, 2]), catalogs.camera)).toEqual({ x: 442, y: 280 });
    expect(structuralFacilityToCanvas(structuralFacilityMapCell([7, 2]), catalogs.camera)).toEqual({ x: 562, y: 220 });
  });
});
