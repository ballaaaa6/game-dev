import type { V7Bounds, V7PixelDiffResult, V7RasterSurface } from "./contracts";
import { RasterSurfaceCompatibilityV7 } from "./raster";

export function diffRasterV7(
  left: V7RasterSurface,
  right: V7RasterSurface,
): V7PixelDiffResult {
  if (left.width !== right.width || left.height !== right.height) {
    throw new Error("V7 pixel diff requires equal dimensions");
  }
  let changedPixelCount = 0;
  let totalChannelError = 0;
  let maxChannelError = 0;
  let leftEdge = left.width;
  let topEdge = left.height;
  let rightEdge = -1;
  let bottomEdge = -1;
  for (let y = 0; y < left.height; y += 1) {
    for (let x = 0; x < left.width; x += 1) {
      const offset = (y * left.width + x) * 4;
      let pixelChanged = false;
      for (let channel = 0; channel < 4; channel += 1) {
        const error = Math.abs(left.pixels[offset + channel] - right.pixels[offset + channel]);
        if (error !== 0) {
          pixelChanged = true;
          totalChannelError += error;
          maxChannelError = Math.max(maxChannelError, error);
        }
      }
      if (pixelChanged) {
        changedPixelCount += 1;
        leftEdge = Math.min(leftEdge, x);
        topEdge = Math.min(topEdge, y);
        rightEdge = Math.max(rightEdge, x);
        bottomEdge = Math.max(bottomEdge, y);
      }
    }
  }
  const changedRegion: V7Bounds | null = rightEdge < leftEdge || bottomEdge < topEdge
    ? null
    : { x: leftEdge, y: topEdge, width: rightEdge - leftEdge + 1, height: bottomEdge - topEdge + 1 };
  const changedChannels = changedPixelCount === 0 ? 1 : changedPixelCount * 4;
  return {
    width: left.width,
    height: left.height,
    changedPixelCount,
    maxChannelError,
    meanChannelError: totalChannelError / changedChannels,
    changedRegion,
    identical: changedPixelCount === 0,
  };
}

export function makeDiffSurfaceV7(
  left: V7RasterSurface,
  right: V7RasterSurface,
): RasterSurfaceCompatibilityV7 {
  if (left.width !== right.width || left.height !== right.height) {
    throw new Error("V7 diff surface requires equal dimensions");
  }
  const result = new RasterSurfaceCompatibilityV7(left.width, left.height);
  for (let offset = 0; offset < result.pixels.length; offset += 4) {
    const changed = left.pixels[offset] !== right.pixels[offset]
      || left.pixels[offset + 1] !== right.pixels[offset + 1]
      || left.pixels[offset + 2] !== right.pixels[offset + 2]
      || left.pixels[offset + 3] !== right.pixels[offset + 3];
    if (!changed) {
      continue;
    }
    const error = Math.max(
      Math.abs(left.pixels[offset] - right.pixels[offset]),
      Math.abs(left.pixels[offset + 1] - right.pixels[offset + 1]),
      Math.abs(left.pixels[offset + 2] - right.pixels[offset + 2]),
      Math.abs(left.pixels[offset + 3] - right.pixels[offset + 3]),
    );
    result.pixels[offset] = 255;
    result.pixels[offset + 1] = Math.max(0, 255 - error);
    result.pixels[offset + 2] = 0;
    result.pixels[offset + 3] = 255;
  }
  return result;
}
