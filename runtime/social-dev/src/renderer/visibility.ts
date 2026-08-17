export interface VisibilityImageDraw {
  readonly destination_x: number;
  readonly destination_y: number;
  readonly width: number;
  readonly height: number;
  readonly source_x?: number;
  readonly source_y?: number;
  readonly source_width?: number;
  readonly source_height?: number;
}

export interface FinalVisibilityDiagnostics {
  readonly status: "pass" | "blocked" | "not_available";
  readonly required_ids: readonly string[];
  readonly visible_ids: readonly string[];
  readonly occluded_ids: readonly string[];
  readonly pixel_counts: Readonly<Record<string, number>>;
}

export function emptyFinalVisibilityDiagnostics(): FinalVisibilityDiagnostics {
  return {
    status: "not_available",
    required_ids: [],
    visible_ids: [],
    occluded_ids: [],
    pixel_counts: {},
  };
}

export interface VisibilityTracker {
  readonly drawImage: (ownerId: string, image: CanvasImageSource, draw: VisibilityImageDraw) => void;
  readonly markRect: (ownerId: string, x: number, y: number, width: number, height: number) => void;
  readonly finish: (requiredIds: readonly string[]) => FinalVisibilityDiagnostics;
}

function ownerColor(owner: number): string {
  return `rgb(${owner & 0xff},${(owner >> 8) & 0xff},${(owner >> 16) & 0xff})`;
}

function ownerFromPixel(red: number, green: number, blue: number): number {
  return red | (green << 8) | (blue << 16);
}

export function createVisibilityTracker(canvas: HTMLCanvasElement): VisibilityTracker | null {
  const ownerCanvas = canvas.ownerDocument?.createElement("canvas");
  const scratchCanvas = canvas.ownerDocument?.createElement("canvas");
  if (!ownerCanvas || !scratchCanvas) {
    return null;
  }
  ownerCanvas.width = canvas.width;
  ownerCanvas.height = canvas.height;
  scratchCanvas.width = canvas.width;
  scratchCanvas.height = canvas.height;
  const ownerContext = ownerCanvas.getContext("2d");
  const scratchContext = scratchCanvas.getContext("2d");
  if (!ownerContext || !scratchContext) {
    return null;
  }
  const owner = ownerContext;
  const scratch = scratchContext;
  owner.clearRect(0, 0, ownerCanvas.width, ownerCanvas.height);
  owner.imageSmoothingEnabled = false;
  scratch.imageSmoothingEnabled = false;

  const owners = new Map<string, number>();
  let nextOwner = 1;

  function ownerNumber(ownerId: string): number {
    const existing = owners.get(ownerId);
    if (existing !== undefined) {
      return existing;
    }
    const assigned = nextOwner;
    nextOwner += 1;
    owners.set(ownerId, assigned);
    return assigned;
  }

  function clippedBounds(x: number, y: number, width: number, height: number): readonly [number, number, number, number] | null {
    const left = Math.max(0, Math.floor(x) - 1);
    const top = Math.max(0, Math.floor(y) - 1);
    const right = Math.min(ownerCanvas.width, Math.ceil(x + width) + 1);
    const bottom = Math.min(ownerCanvas.height, Math.ceil(y + height) + 1);
    return right > left && bottom > top ? [left, top, right, bottom] : null;
  }

  function commitScratch(ownerId: string, draw: () => void, x: number, y: number, width: number, height: number): void {
    const bounds = clippedBounds(x, y, width, height);
    if (!bounds) {
      return;
    }
    const [left, top, right, bottom] = bounds;
    scratch.clearRect(left, top, right - left, bottom - top);
    scratch.save();
    scratch.globalCompositeOperation = "source-over";
    draw();
    scratch.globalCompositeOperation = "source-in";
    scratch.fillStyle = ownerColor(ownerNumber(ownerId));
    scratch.fillRect(x, y, width, height);
    scratch.restore();
    owner.drawImage(scratchCanvas, left, top, right - left, bottom - top, left, top, right - left, bottom - top);
  }

  const drawImage = (ownerId: string, image: CanvasImageSource, draw: VisibilityImageDraw): void => {
    commitScratch(ownerId, () => {
      if (
        draw.source_x !== undefined
        && draw.source_y !== undefined
        && draw.source_width !== undefined
        && draw.source_height !== undefined
      ) {
        scratch.drawImage(
          image,
          draw.source_x,
          draw.source_y,
          draw.source_width,
          draw.source_height,
          draw.destination_x,
          draw.destination_y,
          draw.width,
          draw.height,
        );
      } else {
        scratch.drawImage(image, draw.destination_x, draw.destination_y, draw.width, draw.height);
      }
    }, draw.destination_x, draw.destination_y, draw.width, draw.height);
  };

  const markRect = (ownerId: string, x: number, y: number, width: number, height: number): void => {
    commitScratch(ownerId, () => {
      scratch.fillStyle = ownerColor(ownerNumber(ownerId));
      scratch.fillRect(x, y, width, height);
    }, x, y, width, height);
  };

  const finish = (requiredIds: readonly string[]): FinalVisibilityDiagnostics => {
    const pixelCounts = new Map<number, number>();
    let pixels: Uint8ClampedArray;
    try {
      pixels = owner.getImageData(0, 0, ownerCanvas.width, ownerCanvas.height).data;
    } catch {
      return {
        status: "not_available",
        required_ids: [...requiredIds],
        visible_ids: [],
        occluded_ids: [...requiredIds],
        pixel_counts: {},
      };
    }
    for (let index = 0; index < pixels.length; index += 4) {
      if (pixels[index + 3] === 0) {
        continue;
      }
      const owner = ownerFromPixel(pixels[index], pixels[index + 1], pixels[index + 2]);
      pixelCounts.set(owner, (pixelCounts.get(owner) ?? 0) + 1);
    }
    const counts: Record<string, number> = {};
    for (const id of requiredIds) {
      const count = pixelCounts.get(owners.get(id) ?? -1) ?? 0;
      counts[id] = count;
    }
    const visibleIds = requiredIds.filter((id) => (counts[id] ?? 0) > 0);
    const occludedIds = requiredIds.filter((id) => (counts[id] ?? 0) === 0);
    return {
      status: occludedIds.length === 0 ? "pass" : "blocked",
      required_ids: [...requiredIds],
      visible_ids: visibleIds,
      occluded_ids: occludedIds,
      pixel_counts: counts,
    };
  };

  return { drawImage, markRect, finish };
}
