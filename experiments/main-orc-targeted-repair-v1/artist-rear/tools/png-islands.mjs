#!/usr/bin/env node
// QA-only: connected-component census of a standalone PNG (8-connectivity).
// Usage: node png-islands.mjs <file.png> [maxArea=8]
import fs from 'node:fs';
import { PNG } from 'pngjs';

const [, , file, maxAreaArg = '8'] = process.argv;
const maxArea = Number(maxAreaArg);
const { width: w, height: h, data } = PNG.sync.read(fs.readFileSync(file));
const A = (x, y) => data[(y * w + x) * 4 + 3];
const seen = new Uint8Array(w * h);
const comps = [];
for (let y = 0; y < h; y += 1) {
  for (let x = 0; x < w; x += 1) {
    const i = y * w + x;
    if (seen[i] || !A(x, y)) continue;
    const st = [[x, y]];
    seen[i] = 1;
    const px = [];
    while (st.length) {
      const [cx, cy] = st.pop();
      px.push([cx, cy]);
      for (let dy = -1; dy <= 1; dy += 1) {
        for (let dx = -1; dx <= 1; dx += 1) {
          if (!dx && !dy) continue;
          const nx = cx + dx;
          const ny = cy + dy;
          if (nx < 0 || ny < 0 || nx >= w || ny >= h) continue;
          const ni = ny * w + nx;
          if (seen[ni] || !A(nx, ny)) continue;
          seen[ni] = 1;
          st.push([nx, ny]);
        }
      }
    }
    const xs = px.map((p) => p[0]);
    const ys = px.map((p) => p[1]);
    const colors = px.map(([px2, py2]) => {
      const s = (py2 * w + px2) * 4;
      return `${data[s]},${data[s + 1]},${data[s + 2]}`;
    });
    comps.push({
      n: px.length,
      bbox: [Math.min(...xs), Math.min(...ys), Math.max(...xs), Math.max(...ys)],
      colors: [...new Set(colors)].slice(0, 4),
    });
  }
}
comps.sort((a, b) => b.n - a.n);
console.log(`${file} ${w}x${h} components=${comps.length}`);
for (const c of comps) {
  if (c.n <= maxArea) console.log(`  SMALL area=${c.n} bbox=${c.bbox.join(',')} colors=${c.colors.join(' ')}`);
}
console.log(`  largest=${comps[0].n} total=${comps.reduce((a, b) => a + b.n, 0)}`);
