import fs from 'node:fs';
import path from 'node:path';
import zlib from 'node:zlib';
import { ROOT } from '../../src/core.mjs';

// Independent uniformity audit: every cell is measured from its own pixels,
// never from the report written by the agent that produced it.

const cells = [
  ['front_r', 'Sword', 'combat-recovery-v8/frontal-inbetween/front_r-sword'],
  ['front_l', 'Sword', 'combat-recovery-v8/frontal-inbetween/front_l-sword'],
  ['back_r', 'Sword', 'combat-recovery-v8/rear-arc/back_r-sword'],
  ['back_l', 'Sword', 'combat-recovery-v8/rear-arc/back_l-sword'],
  ['front_r', 'Axe', 'combat-recovery-v7/frontal/front_r-Axe-full'],
  ['front_l', 'Axe', 'combat-recovery-v7/frontal/front_l-Axe-full'],
  ['back_r', 'Axe', 'combat-recovery-v8/rear/back_r-axe'],
  ['back_l', 'Axe', 'combat-recovery-v8/rear/back_l-axe'],
];

const read = file => JSON.parse(fs.readFileSync(path.resolve(ROOT, file), 'utf8'));

// Minimal PNG decoder for 8-bit RGBA, non-interlaced: enough for factory exports.
function decodePng(buffer) {
  let pos = 8;
  let width = 0, height = 0, bitDepth = 0, colorType = 0;
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
  const bpp = 4, stride = width * bpp;
  const out = Buffer.alloc(height * stride);
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

function measure(layerPng) {
  const { width, height, data } = decodePng(fs.readFileSync(path.resolve(ROOT, layerPng)));
  let sx = 0, sy = 0, area = 0, bright = 0, top = 0, bottom = 0;
  for (let y = 0; y < height; y += 1) {
    for (let x = 0; x < width; x += 1) {
      const i = (y * width + x) * 4;
      if (data[i + 3] === 0) continue;
      sx += x; sy += y; area += 1;
      if (y < top || top === 0) top = y;
      if (y > bottom) bottom = y;
      const l = 0.2126 * data[i] + 0.7152 * data[i + 1] + 0.0722 * data[i + 2];
      if (l >= 160) bright += 1;
    }
  }
  return area ? { cx: sx / area, cy: sy / area, area, bright, top, bottom } : null;
}

const report = [];
for (const [direction, action, dir] of cells) {
  const clip = read(`characters/orc-v1/source/${dir}/clip.json`);
  const armed = clip.frames.filter(f => f.weaponVisible === true);
  const durations = clip.frames.map(f => Math.round(f.durationMs));
  const steps = [];
  let prev = null;
  for (const frame of clip.frames) {
    const m = frame.weaponVisible ? measure(frame.layers.weaponFront.png) : null;
    if (!m) { prev = null; continue; }
    if (prev) steps.push({ from: prev.index, to: frame.index, px: Math.hypot(m.cx - prev.cx, m.cy - prev.cy) });
    prev = { ...m, index: frame.index };
  }
  const maxStep = steps.reduce((a, b) => (b.px > a.px ? b : a), steps[0]);
  const median = [...steps].map(s => s.px).sort((a, b) => a - b)[Math.floor(steps.length / 2)];
  const elapsed = index => clip.frames.slice(0, index).reduce((sum, f) => sum + f.durationMs, 0);
  report.push({
    cell: `${direction}/${action}`,
    frames: clip.frames.length,
    totalMs: clip.totalDurationMs,
    durations,
    armedInterval: [armed[0].index, armed.at(-1).index],
    bookendsUnarmed: clip.frames[0].weaponVisible === false && clip.frames.at(-1).weaponVisible === false,
    brightestFrame: clip.frames.map(f => (f.weaponVisible ? measure(f.layers.weaponFront.png)?.bright ?? 0 : 0)),
    maxStep, medianStep: median,
    stepRatio: +(maxStep.px / median).toFixed(2),
    stepFrom: maxStep.from,
    stepTo: maxStep.to,
    armedDuplicates: steps.filter(s => s.px === 0).map(s => s.from + '=' + s.to),
    contactEventFrame: clip.contactEvent.frame,
    impactMs: clip.contactEvent.timeMs,
    impactPercent: +(clip.contactEvent.timeMs / clip.totalDurationMs * 100).toFixed(2),
    provenance: dir,
  });
}

for (const family of ['Sword', 'Axe']) {
  const group = report.filter(r => r.cell.endsWith(family));
  console.log(`\n=== ${family} ===`);
  console.log('cell              frames  totalMs  armed     bookends  impactMs  impact%  medianStep  maxStep');
  for (const r of group) {
    console.log(
      `${r.cell.padEnd(17)} ${String(r.frames).padStart(6)} ${String(r.totalMs).padStart(8)}  ` +
      `${String(r.armedInterval.join('-')).padStart(7)}  ${String(r.bookendsUnarmed).padStart(8)}  ` +
      `${String(r.impactMs).padStart(8)}  ${String(r.impactPercent).padStart(7)}  ` +
      `${String(r.medianStep.toFixed(1)).padStart(10)}  ${r.maxStep.px.toFixed(1).padStart(7)} (#${r.maxStep.from}->${r.maxStep.to})`,
    );
  }
  const unique = key => new Set(group.map(r => JSON.stringify(r[key]))).size;
  console.log(`distinct frame counts: ${unique('frames')} | distinct totals: ${unique('totalMs')} | distinct durations: ${unique('durations')} | distinct impactMs: ${unique('impactMs')}`);
}

fs.writeFileSync(path.resolve(ROOT, 'experiments/main-orc-combat-recovery-v8/uniformity-audit.json'), `${JSON.stringify(report, null, 2)}\n`);
console.log('\nwrote experiments/main-orc-combat-recovery-v8/uniformity-audit.json');
