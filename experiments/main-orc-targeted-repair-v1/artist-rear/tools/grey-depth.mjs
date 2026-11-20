#!/usr/bin/env node
// QA-only: distance-to-silhouette histogram for a colour family in a layer.
// Usage: node grey-depth.mjs <clip.json> <layer> <minL> <maxL> [maxChroma]
import fs from 'node:fs';
import { PNG } from 'pngjs';

const [, , clipArg, layer, minLArg, maxLArg, chromaArg = '8'] = process.argv;
const minL = Number(minLArg);
const maxL = Number(maxLArg);
const maxChroma = Number(chromaArg);
const clip = JSON.parse(fs.readFileSync(clipArg, 'utf8'));
const lum = (r, g, b) => 0.2126 * r + 0.7152 * g + 0.0722 * b;

const all = new Map();
for (const f of clip.frames) {
  const p = layer === 'composite' ? f.png : f.layers?.[layer]?.png;
  if (!p) continue;
  const { width: w, height: h, data } = PNG.sync.read(fs.readFileSync(p));
  const alpha = (x, y) => (x < 0 || y < 0 || x >= w || y >= h ? 0 : data[(y * w + x) * 4 + 3]);
  // BFS distance to transparent from each pixel (4-neighbour), limited to 4
  for (let y = 0; y < h; y += 1) {
    for (let x = 0; x < w; x += 1) {
      if (alpha(x, y) === 0) continue;
      const s = (y * w + x) * 4;
      const r = data[s];
      const g = data[s + 1];
      const b = data[s + 2];
      const L = lum(r, g, b);
      const chroma = Math.max(r, g, b) - Math.min(r, g, b);
      if (L < minL || L > maxL || chroma > maxChroma) continue;
      let dist = 99;
      for (let d = 1; d <= 4; d += 1) {
        let hit = false;
        for (let k = -d; k <= d && !hit; k += 1) {
          if (alpha(x + k, y - d) === 0 || alpha(x + k, y + d) === 0) hit = true;
          if (alpha(x - d, y + k) === 0 || alpha(x + d, y + k) === 0) hit = true;
        }
        if (hit) {
          dist = d;
          break;
        }
      }
      const key = `${r},${g},${b}`;
      if (!all.has(key)) all.set(key, [0, 0, 0, 0, 0]);
      all.get(key)[Math.min(dist, 4)] += 1;
    }
  }
}
const rows = [...all.entries()].sort((a, b) => b[1].reduce((p, c) => p + c, 0) - a[1].reduce((p, c) => p + c, 0));
console.log('color          total  d1(edge)  d2   d3   d4+');
for (const [k, v] of rows.slice(0, 14)) {
  console.log(`${k.padEnd(14)} ${String(v.reduce((a, b) => a + b, 0)).padStart(5)} ${String(v[1]).padStart(8)} ${String(v[2]).padStart(4)} ${String(v[3]).padStart(4)} ${String(v[4]).padStart(4)}`);
}
