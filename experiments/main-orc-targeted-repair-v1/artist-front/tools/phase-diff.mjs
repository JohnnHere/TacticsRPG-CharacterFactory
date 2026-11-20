#!/usr/bin/env node
// Compare first-half frames (mirror-flipped) against second-half frames in a
// region, reporting min pixel-diff per pair to test material/coat consistency.
// Usage: node phase-diff.mjs <clip.json> <x,y,w,h>
import fs from 'node:fs';
import { PNG } from 'pngjs';

const [, , clipArg, regionArg] = process.argv;
const [rx, ry, rw, rh] = regionArg.split(',').map(Number);
const clip = JSON.parse(fs.readFileSync(clipArg, 'utf8'));
const load = (i) => {
  const f = clip.frames[i];
  return PNG.sync.read(fs.readFileSync(f.nativePng || f.png));
};
const diff = (a, b, mirrorA) => {
  let d = 0, n = 0;
  for (let y = ry; y < ry + rh; y++) for (let x = rx; x < rx + rw; x++) {
    const ax = mirrorA ? rx + rw - 1 - (x - rx) : x;
    const s = (y * (a.width > 128 ? a.width : 128) + ax) * 4;
    // frames are 128x128 native
    const sa = (y * 128 + ax) * 4;
    const sb = (y * 128 + x) * 4;
    n++;
    if (a.data[sa + 3] === 0 && b.data[sb + 3] === 0) continue;
    if (a.data[sa + 3] === 0 || b.data[sb + 3] === 0) { d += 255; continue; }
    d += Math.abs(a.data[sa] - b.data[sb]) + Math.abs(a.data[sa + 1] - b.data[sb + 1]) + Math.abs(a.data[sa + 2] - b.data[sb + 2]);
  }
  return d / (n * 3);
};
for (let i = 0; i < 8; i++) {
  const a = load(i);
  let best = null, bestJ = -1, worst = 999, worstJ = -1;
  const rows = [];
  for (let j = 8; j < 16; j++) {
    const v = diff(a, load(j), true);
    rows.push(`j${j}:${v.toFixed(1)}`);
    if (!best || v < best) { best = v; bestJ = j; }
    if (v > worst) { worst = v; worstJ = j; }
  }
  console.log(`f${i}: best=f${bestJ}(${best.toFixed(1)}) worst=f${worstJ}(${worst.toFixed(1)})  ${rows.join(' ')}`);
}
