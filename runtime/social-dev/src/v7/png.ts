import type { V7RasterImage, V7RasterSurface } from "./contracts";

const PNG_SIGNATURE = new Uint8Array([137, 80, 78, 71, 13, 10, 26, 10]);

/**
 * Encodes RGBA pixels with deterministic filter-zero scanlines and stored
 * DEFLATE blocks. This is a compatibility artifact encoder, not a claim about
 * the original Unity PNG writer.
 */
export function encodePngRgbaV7(input: V7RasterSurface | V7RasterImage): Uint8Array {
  const scanlines = new Uint8Array(input.height * (input.width * 4 + 1));
  for (let y = 0; y < input.height; y += 1) {
    const scanlineOffset = y * (input.width * 4 + 1);
    scanlines[scanlineOffset] = 0;
    scanlines.set(
      input.pixels.subarray(y * input.width * 4, (y + 1) * input.width * 4),
      scanlineOffset + 1,
    );
  }
  const ihdr = new Uint8Array(13);
  writeU32BE(ihdr, 0, input.width);
  writeU32BE(ihdr, 4, input.height);
  ihdr[8] = 8;
  ihdr[9] = 6;
  ihdr[10] = 0;
  ihdr[11] = 0;
  ihdr[12] = 0;
  const idat = zlibStored(scanlines);
  return concatBytes(
    PNG_SIGNATURE,
    pngChunk("IHDR", ihdr),
    pngChunk("IDAT", idat),
    pngChunk("IEND", new Uint8Array(0)),
  );
}

function zlibStored(data: Uint8Array): Uint8Array {
  const chunks: Uint8Array[] = [new Uint8Array([0x78, 0x01])];
  let offset = 0;
  while (offset < data.length) {
    const remaining = data.length - offset;
    const length = Math.min(0xffff, remaining);
    const final = offset + length >= data.length ? 1 : 0;
    const block = new Uint8Array(5 + length);
    block[0] = final;
    block[1] = length & 0xff;
    block[2] = (length >>> 8) & 0xff;
    const inverse = 0xffff - length;
    block[3] = inverse & 0xff;
    block[4] = (inverse >>> 8) & 0xff;
    block.set(data.subarray(offset, offset + length), 5);
    chunks.push(block);
    offset += length;
  }
  if (data.length === 0) {
    chunks.push(new Uint8Array([1, 0, 0, 0xff, 0xff]));
  }
  const adler = new Uint8Array(4);
  writeU32BE(adler, 0, adler32(data));
  chunks.push(adler);
  return concatBytes(...chunks);
}

function pngChunk(type: string, data: Uint8Array): Uint8Array {
  const typeBytes = new TextEncoder().encode(type);
  const length = new Uint8Array(4);
  writeU32BE(length, 0, data.length);
  const crcInput = concatBytes(typeBytes, data);
  const crc = new Uint8Array(4);
  writeU32BE(crc, 0, crc32(crcInput));
  return concatBytes(length, crcInput, crc);
}

function adler32(data: Uint8Array): number {
  let a = 1;
  let b = 0;
  for (const byte of data) {
    a = (a + byte) % 65521;
    b = (b + a) % 65521;
  }
  return ((b << 16) | a) >>> 0;
}

function crc32(data: Uint8Array): number {
  let crc = 0xffffffff;
  for (const byte of data) {
    crc ^= byte;
    for (let bit = 0; bit < 8; bit += 1) {
      crc = (crc >>> 1) ^ ((crc & 1) === 1 ? 0xedb88320 : 0);
    }
  }
  return (crc ^ 0xffffffff) >>> 0;
}

function writeU32BE(target: Uint8Array, offset: number, value: number): void {
  target[offset] = (value >>> 24) & 0xff;
  target[offset + 1] = (value >>> 16) & 0xff;
  target[offset + 2] = (value >>> 8) & 0xff;
  target[offset + 3] = value & 0xff;
}

function concatBytes(...arrays: readonly Uint8Array[]): Uint8Array {
  const length = arrays.reduce((total, array) => total + array.length, 0);
  const result = new Uint8Array(length);
  let offset = 0;
  for (const array of arrays) {
    result.set(array, offset);
    offset += array.length;
  }
  return result;
}
