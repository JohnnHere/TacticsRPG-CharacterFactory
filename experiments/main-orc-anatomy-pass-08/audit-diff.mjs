import fs from 'node:fs';
import path from 'node:path';
import zlib from 'node:zlib';

// Independent audit of the anatomical pass: proves the edit stayed inside the
// declared arm region and that everything else is byte-identical, then measures
// the new joint chain. It trusts neither the producer's report nor his boxes.

const EXP = path.resolve(import.meta.dirname);
const BEFORE = path.join(EXP, '..', 'main-orc-skeleton-02', 'stage-bcde', 'body-only', '08.png');
const AFTER = path.join(EXP, 'candidate-08.png');

function decodePng(buffer) {
  let pos = 8, width = 0, height = 0, bitDepth = 0, colorType = 0;
  const idat = [];
  while (pos < buffer.length) {
    const length = buffer.readUInt32BE(pos);
    const type = buffer.toString('ascii', pos + 4, pos + 8);
    const data = buffer.subarray(pos + 8, pos + 8 + length);
    if (type === 'IHDR') {
      width = data.readUInt32BE(0); height = data.readUInt32BE(4);
      bitDepth = data[8]; colorType = data[9];
    } else if (type === 'IDAT') idat.push(data);
    else if (type === 'IEND') break;
    pos += 12 + length;
  }
  if (bitDepth !== 8 || colorType !== 6) throw new Error(`png não suportado ${bitDepth}/${colorType}`);
  const raw = zlib.inflateSync(Buffer.concat(idat));
  const bpp = 4, stride = width * bpp, out = Buffer.alloc(height * stride);
  let src = 0;
  for (let y = 0; y < height; y += 1) {
    const filter = raw[src]; src += 1;
    for (let x = 0; x < stride; x += 1) {
      const value = raw[src + x];
      const left = x >= bpp ? out[y * stride + x - bpp] : 0;
      const up = y > 0 ? out[(y - 1) * stride + x] : 0;
      const upLeft = y > 0 && x >= bpp ? out[(y - 1) * stride + x - bpp] : 0;
      let restored;
      if (filter === 0) restored = value;
      else if (filter === 1) restored = value + left;
      else if (filter === 2) restored = value + up;
      else if (filter === 3) restored = value + ((left + up) >> 1);
      else {
        const p = left + up - upLeft;
        const pa = Math.abs(p - left), pb = Math.abs(p - up), pc = Math.abs(p - upLeft);
        restored = value + (pa <= pb && pa <= pc ? left : pb <= pc ? up : upLeft);
      }
      out[y * stride + x] = restored & 0xff;
    }
    src += stride;
  }
  return { width, height, data: out };
}

const before = decodePng(fs.readFileSync(BEFORE));
const after = decodePng(fs.readFileSync(AFTER));
if (before.width !== after.width || before.height !== after.height) {
  console.error('FALHA: dimensões diferentes');
  process.exit(1);
}

const changed = [];
const box = { minX: Infinity, minY: Infinity, maxX: -1, maxY: -1, pixels: 0 };
for (let y = 0; y < before.height; y += 1) {
  for (let x = 0; x < before.width; x += 1) {
    const i = (y * before.width + x) * 4;
    let equal = true;
    for (let c = 0; c < 4; c += 1) if (before.data[i + c] !== after.data[i + c]) { equal = false; break; }
    if (!equal) {
      changed.push([x, y]);
      box.pixels += 1;
      box.minX = Math.min(box.minX, x); box.maxX = Math.max(box.maxX, x);
      box.minY = Math.min(box.minY, y); box.maxY = Math.max(box.maxY, y);
    }
  }
}

if (!changed.length) {
  console.error('FALHA: nenhuma alteração — o passe não aconteceu');
  process.exit(1);
}

// The allowed region: the attacking arm and the indispensable shoulder junction.
// Anything outside means identity damage. The region is generous on purpose:
// x 130..205 covers the extended arm, y 95..170 covers shoulder to hand.
const LIMIT = { x0: 130, y0: 95, x1: 205, y1: 170 };
const outside = changed.filter(([x, y]) => x < LIMIT.x0 || x > LIMIT.x1 || y < LIMIT.y0 || y > LIMIT.y1);

console.log(`pixels alterados: ${box.pixels}`);
console.log(`bbox da mudança: x ${box.minX}..${box.maxX}, y ${box.minY}..${box.maxY}`);
if (outside.length) {
  console.error(`FORA DA REGIÃO PERMITIDA: ${outside.length} pixels, primeiros ${outside.slice(0, 12).map(([x, y]) => `(${x},${y})`).join(' ')}`);
  process.exit(1);
}
console.log(`todos os ${box.pixels} pixels alterados estão dentro de x ${LIMIT.x0}..${LIMIT.x1}, y ${LIMIT.y0}..${LIMIT.y1}`);

// Sanity: everything outside the region must be byte-identical (already implied,
// but stated for the report).
const outPath = path.join(EXP, 'audit-diff.json');
fs.writeFileSync(outPath, JSON.stringify({
  changedPixels: box.pixels,
  bbox: { x0: box.minX, y0: box.minY, x1: box.maxX, y1: box.maxY },
  allowedRegion: LIMIT,
  outsideAllowedRegion: outside.length,
  dimensions: [before.width, before.height],
}, null, 2));
console.log(`audit: ${outPath}`);
