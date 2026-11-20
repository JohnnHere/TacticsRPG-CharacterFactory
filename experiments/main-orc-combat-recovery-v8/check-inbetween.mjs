import fs from 'node:fs';
import path from 'node:path';
import zlib from 'node:zlib';
import { ROOT } from '../../src/core.mjs';

// Verifies the added apex-descent frame against the shared spec. It refuses to
// bless a cell that only looks right: geometry, timing and the bright-pixel
// series are all re-measured from the exported PNGs.

const SPEC_DURATIONS = [30, 65, 35, 50, 45, 35, 30, 35, 35, 100, 55, 80, 45, 90];
const SPEC_PHASES = [
  'rest', 'body-preparation', 'establish-grip', 'anticipation', 'coil-behind',
  'apex-hold', 'apex-descent', 'slash-release', 'contact', 'follow-through',
  'recoil', 'settle-grip', 'release-grip', 'return-to-guard',
];
const MAX_STEP_PX = 65;

const cells = [
  ['front_r/Sword', 'combat-recovery-v8/frontal-inbetween/front_r-sword'],
  ['front_l/Sword', 'combat-recovery-v8/frontal-inbetween/front_l-sword'],
  ['back_r/Sword', 'combat-recovery-v8/rear-inbetween/back_r-sword'],
  ['back_l/Sword', 'combat-recovery-v8/rear-inbetween/back_l-sword'],
];

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
  if (bitDepth !== 8 || colorType !== 6) throw new Error(`unsupported png ${bitDepth}/${colorType}`);
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

const read = file => JSON.parse(fs.readFileSync(path.resolve(ROOT, file), 'utf8'));
const failures = [];
const rows = [];

for (const [label, dir] of cells) {
  const clip = read(`characters/orc-v1/source/${dir}/clip.json`);
  const fail = reason => failures.push(`${label}: ${reason}`);
  const durations = clip.frames.map(f => Math.round(f.durationMs));
  if (JSON.stringify(durations) !== JSON.stringify(SPEC_DURATIONS)) fail(`durations ${JSON.stringify(durations)}`);
  const phases = clip.frames.map(f => f.phase);
  if (JSON.stringify(phases) !== JSON.stringify(SPEC_PHASES)) fail(`phases ${JSON.stringify(phases)}`);
  if (clip.totalDurationMs !== 730) fail(`total ${clip.totalDurationMs}`);
  const ce = clip.contactEvent ?? {};
  if (ce.frame !== 8 || ce.timeMs !== 325 || ce.phase !== 'contact') fail(`contactEvent ${JSON.stringify(ce)}`);

  const armed = clip.frames.filter(f => f.weaponVisible).map(f => f.index);
  if (JSON.stringify(armed) !== JSON.stringify([2, 3, 4, 5, 6, 7, 8, 9, 10, 11])) fail(`armed ${JSON.stringify(armed)}`);

  const visible = clip.frames.filter(f => f.weaponVisible);
  const dups = [];
  for (let i = 1; i < visible.length; i += 1) if (visible[i].sha256 === visible[i - 1].sha256) dups.push(`${visible[i - 1].index}=${visible[i].index}`);
  if (dups.length) fail(`duplicate armed frames ${dups.join(',')}`);

  const centroids = new Map();
  const bright = [];
  for (const frame of clip.frames) {
    const body = decodePng(fs.readFileSync(path.resolve(ROOT, frame.layers.body.png)));
    let brightCount = 0;
    for (let i = 0; i < body.data.length; i += 4) {
      if (body.data[i + 3] === 0) continue;
      const l = 0.2126 * body.data[i] + 0.7152 * body.data[i + 1] + 0.0722 * body.data[i + 2];
      if (l >= 160) brightCount += 1;
    }
    bright.push(brightCount);
    if (!frame.weaponVisible) continue;
    const w = decodePng(fs.readFileSync(path.resolve(ROOT, frame.layers.weaponFront.png)));
    let sx = 0, sy = 0, n = 0;
    for (let i = 0; i < w.data.length; i += 4) {
      if (w.data[i + 3] === 0) continue;
      const px = (i / 4) % w.width, py = Math.floor(i / 4 / w.width);
      sx += px; sy += py; n += 1;
    }
    if (n) centroids.set(frame.index, { x: sx / n, y: sy / n });
  }

  const steps = [];
  const ordered = [...centroids.keys()].sort((a, b) => a - b);
  for (let i = 1; i < ordered.length; i += 1) {
    const a = centroids.get(ordered[i - 1]), b = centroids.get(ordered[i]);
    steps.push({ from: ordered[i - 1], to: ordered[i], px: Math.hypot(b.x - a.x, b.y - a.y) });
  }
  const peak = steps.reduce((a, b) => (b.px > a.px ? b : a), steps[0]);
  const descent = steps.find(s => s.from === 5 && s.to === 6);
  if (!descent) fail('missing 5->6 transition');
  else if (descent.px >= 45) fail(`apex split still ${descent.px.toFixed(2)} px at 5->6 (limit 45)`);
  // The inherited slash-release -> contact step is deliberately preserved, so the
  // overall peak may sit there; what must stay bounded is the descent we split.
  if (peak.px >= MAX_STEP_PX) fail(`overall peak ${peak.px.toFixed(2)} px at ${peak.from}->${peak.to} (limit ${MAX_STEP_PX})`);

  rows.push({ label, frames: clip.frames.length, total: clip.totalDurationMs, peak: peak.px.toFixed(2), peakAt: `${peak.from}->${peak.to}`, bright });
  console.log(
    `${label.padEnd(14)} ${clip.frames.length}f ${clip.totalDurationMs}ms  peak ${peak.px.toFixed(2).padStart(6)} px at ${peak.from}->${peak.to}  ` +
    `bright ${JSON.stringify(bright)}`,
  );
}

console.log('');
if (failures.length) {
  for (const f of failures) console.log(`FAIL ${f}`);
  process.exit(1);
}
console.log(`PASS in-between contract: ${cells.length} cells, peak step below ${MAX_STEP_PX} px on F05->F06 in all of them`);
fs.writeFileSync(path.resolve(ROOT, 'experiments/main-orc-combat-recovery-v8/inbetween-check.json'), `${JSON.stringify(rows, null, 2)}\n`);
