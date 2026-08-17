export type NativeCollisionKind =
  | "empty_walkable"
  | "entry_door"
  | "unbound_place_slot"
  | "installed_furniture"
  | "footprint_wall"
  | "footprint_anchor"
  | "boundary_wall";

export interface NativeCollision {
  readonly passable: boolean;
  readonly kind: NativeCollisionKind;
}

/**
 * Bounded ObjChip collision policy for the room data we have closed.
 *
 * Raw type 1/2 is not allowed to imply a FurnitureData identity.  It stays a
 * traversable placement slot until the resolver has an explicit native
 * binding; only then does it become an occupied furniture cell.
 */
export function classifyNativeCollision(rawType: number, hasNativeBinding: boolean): NativeCollision {
  switch (rawType) {
    case 0:
      return { passable: true, kind: "empty_walkable" };
    case 5:
      return { passable: true, kind: "entry_door" };
    case 1:
    case 2:
      return hasNativeBinding
        ? { passable: false, kind: "installed_furniture" }
        : { passable: true, kind: "unbound_place_slot" };
    case 3:
      return { passable: false, kind: "footprint_wall" };
    case 4:
      return { passable: false, kind: "footprint_anchor" };
    case 6:
      return { passable: false, kind: "boundary_wall" };
    default:
      return { passable: false, kind: "boundary_wall" };
  }
}
