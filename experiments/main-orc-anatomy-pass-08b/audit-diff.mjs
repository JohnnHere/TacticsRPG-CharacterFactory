import fs from 'node:fs';
import path from 'node:path';
import zlib from 'node:zlib';

// Independent audit of pass 08b: proves the edit stayed inside the arm region,
// measures the new limb's thickness profile against the previous thin connector,
// and checks for orphan pixels in the edited area. Trusts only the PNGs.

const EXP = path.resolve(import.meta.dirname);
const BEFORE = path.join(EXP, '..', 'main-orc-skeleton-02', 'stage-bcde', 'body-only', '08.png');
const AFTER = path.join(EXP, 'candidate-08b.png');

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

const LIMIT = { x0: 128, y0: 92, x1: 208, y1: 172 };
const outside = changed.filter(([x, y]) => x < LIMIT.x0 || x > LIMIT.x1 || y < LIMIT.y0 || y > LIMIT.y1);

// Thickness profile of the new limb: vertical opaque runs inside the arm area,
// scanning columns from the pauldron to the hand.
const profile = [];
for (let x = 148; x <= Math.min(box.maxX, 200); x += 2) {
  let best = 0, cur = 0, bestY = -1, curY = -1;
  for (let y = LIMIT.y0; y <= LIMIT.y1; y += 1) {
    const i = (y * after.width + x) * 4;
    if (after.data[i + 3] > 0) {
      if (cur === 0) curY = y;
      cur += 1;
      if (cur > best) { best = cur; bestY = curY; }
    } else cur = 0;
  }
  profile.push({ x, thickness: best, y: bestY });
}

// Orphan check in the edited bbox: opaque pixels with zero opaque neighbours.
const orphans = [];
for (let y = box.minY; y <= box.maxY; y += 1) {
  for (let x = box.minX; x <= box.maxX; x += 1) {
    const i = (y * after.width + x) * 4;
    if (after.data[i + 3] === 0) continue;
    let neighbours = 0;
    for (let dy = -1; dy <= 1; dy += 1) for (let dx = -1; dx <= 1; dx += 1) {
      if (!dx && !dy) continue;
      const nx = x + dx, ny = y + dy;
      if (nx < 0 || ny < 0 || nx >= after.width || ny >= after.height) continue;
      if (after.data[(ny * after.width + nx) * 4 + 3] > 0) neighbours += 1;
    }
    if (neighbours === 0) orphans.push([x, y]);
  }
}

console.log(`pixels alterados: ${box.pixels} | bbox x ${box.minX}..${box.maxX}, y ${box.minY}..${box.maxY}`);
console.log(`fora da região permitida x ${LIMIT.x0}..${LIMIT.x1}, y ${LIMIT.y0}..${LIMIT.y1}: ${outside.length}`);
console.log(`pixels órfãos no bbox editado: ${orphans.length}${orphans.length ? ' ' + orphans.slice(0, 10).map(([x, y]) => `(${x},${y})`).join(' ') : ''}`);
console.log('perfil de espessura do novo membro (coluna: px):');
console.log(profile.map(p => `${p.x}:${p.thickness}`).join('  '));

const thin = profile.filter(p => p.thickness > 0 && p.thickness <= 7);
console.log(`trechos com espessura <= 7 px (o defeito antigo): ${thin.length}${thin.length ? ' -> ' + thin.map(p => `${p.x}:${p.thickness}`).join(' ') : ' nenhum'}`);

fs.writeFileSync(path.join(EXP, 'audit-diff.json'), JSON.stringify({
  changedPixels: box.pixels,
  bbox: { x0: box.minX, y0: box.minY, x1: box.maxX, y1: box.maxY },
  allowedRegion: LIMIT,
  outsideAllowedRegion: outside.length,
  orphanPixels: orphans.length,
  thicknessProfile: profile,
  thinSpots: thin,
}, null, 2));
console.log('audit: experiments/main-orc-anatomy-pass-08b/audit-diff.json');
if (outside.length) process.exit(1);
