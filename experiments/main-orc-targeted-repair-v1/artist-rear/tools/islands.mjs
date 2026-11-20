#!/usr/bin/env node
// QA-only: connected-component census of a layer/clip. Flags detached islands,
// 1-3 px specks and components whose colour is far from the body's ink ramp.
// Usage: node islands.mjs <clip.json> <layer|composite> [maxArea=6]
import fs from 'node:fs';
import { PNG } from 'pngjs';

const [, , clipArg, layer = 'composite', maxAreaArg = '6'] = process.argv;
const maxArea = Number(maxAreaArg);
const clip = JSON.parse(fs.readFileSync(clipArg, 'utf8'));
const lum = (r, g, b) => 0.2126 * r + 0.7152 * g + 0.0722 * b;

for (const frame of clip.frames) {
  const p = layer === 'composite' ? frame.png : frame.layers?.[layer]?.png;
  if (!p) continue;
  const { width: w, height: h, data } = PNG.sync.read(fs.readFileSync(p));
  const seen = new Uint8Array(w * h);
  const alphaAt = (x, y) => data[(y * w + x) * 4 + 3];
  const comps = [];
  for (let y = 0; y < h; y += 1) {
    for (let x = 0; x < w; x += 1) {
      const idx = y * w + x;
      if (seen[idx] || alphaAt(x, y) === 0) continue;
      const stack = [[x, y]];
      seen[idx] = 1;
      const px = [];
      while (stack.length) {
        const [cx, cy] = stack.pop();
        px.push([cx, cy]);
        for (const [dx, dy] of [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1]]) {
          const nx = cx + dx;
          const ny = cy + dy;
          if (nx < 0 || ny < 0 || nx >= w || ny >= h) continue;
          const ni = ny * w + nx;
          if (seen[ni] || alphaAt(nx, ny) === 0) continue;
          seen[ni] = 1;
          stack.push([nx, ny]);
        }
      }
      const xs = px.map((q) => q[0]);
      const ys = px.map((q) => q[1]);
      let maxL = 0;
      const colors = new Set();
      for (const [qx, qy] of px) {
        const s = (qy * w + qx) * 4;
        maxL = Math.max(maxL, lum(data[s], data[s + 1], data[s + 2]));
        if (px.length <= 12) colors.add(`${data[s]},${data[s + 1]},${data[s + 2]}`);
      }
      comps.push({
        n: px.length,
        bbox: [Math.min(...xs), Math.min(...ys), Math.max(...xs), Math.max(...ys)],
        maxL: +maxL.toFixed(0),
        colors: [...colors].slice(0, 6),
      });
    }
  }
  comps.sort((a, b) => a.n - b.n);
  const main = comps[comps.length - 1];
  const small = comps.filter((c) => c.n <= maxArea);
  console.log(`\n=== f${frame.index} [${layer}] components=${comps.length} mainArea=${main.n}`);
  for (const c of small) {
    console.log(`   area=${c.n} bbox=${c.bbox.join(',')} maxL=${c.maxL} colors=${c.colors.join(' ')}`);
  }
}
