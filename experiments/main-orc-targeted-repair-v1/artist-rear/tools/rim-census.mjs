#!/usr/bin/env node
// QA-only diagnostic: compare the colour vocabulary used on silhouette-boundary
// pixels between an attack clip and a protected baseline clip of the same view.
// Usage: node rim-census.mjs <attackClip> <baselineClip> [layer]
import fs from 'node:fs';
import { PNG } from 'pngjs';

const [, , atkArg, baseArg, layer = 'composite'] = process.argv;
const load = (arg) => {
  const clip = JSON.parse(fs.readFileSync(arg, 'utf8'));
  const census = new Map();
  let edgeTotal = 0;
  for (const f of clip.frames) {
    const p = layer === 'composite' ? f.png : f.layers?.[layer]?.png;
    if (!p) continue;
    const { width: w, height: h, data } = PNG.sync.read(fs.readFileSync(p));
    const alpha = (x, y) => data[(y * w + x) * 4 + 3];
    for (let y = 0; y < h; y += 1) {
      for (let x = 0; x < w; x += 1) {
        if (alpha(x, y) === 0) continue;
        const isEdge =
          (x > 0 && alpha(x - 1, y) < 128) ||
          (x < w - 1 && alpha(x + 1, y) < 128) ||
          (y > 0 && alpha(x, y - 1) < 128) ||
          (y < h - 1 && alpha(x, y + 1) < 128);
        if (!isEdge) continue;
        edgeTotal += 1;
        const s = (y * w + x) * 4;
        const key = `${data[s]},${data[s + 1]},${data[s + 2]}`;
        census.set(key, (census.get(key) ?? 0) + 1);
      }
    }
  }
  return { census, edgeTotal };
};
const lum = (k) => {
  const [r, g, b] = k.split(',').map(Number);
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
};
const atk = load(atkArg);
const base = load(baseArg);
const rows = [...atk.census.entries()]
  .map(([k, n]) => ({
    color: k,
    L: +lum(k).toFixed(0),
    attack: n,
    attackPct: +((n / atk.edgeTotal) * 100).toFixed(2),
    baseline: base.census.get(k) ?? 0,
    baselinePct: +(((base.census.get(k) ?? 0) / base.edgeTotal) * 100).toFixed(2),
  }))
  .sort((a, b) => b.attack - a.attack);
console.log(`attack edge px=${atk.edgeTotal} baseline edge px=${base.edgeTotal}`);
console.log('color           L   attack  atk%   base  base%');
for (const r of rows.slice(0, 26)) {
  console.log(
    `${r.color.padEnd(15)} ${String(r.L).padStart(3)} ${String(r.attack).padStart(7)} ${String(r.attackPct).padStart(6)} ${String(r.baseline).padStart(6)} ${String(r.baselinePct).padStart(6)}`,
  );
}
