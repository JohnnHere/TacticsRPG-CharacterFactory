#!/usr/bin/env node
// QA-only diagnostic: luminance histogram of silhouette-boundary pixels.
// Compares a clip's outline darkness profile against a reference clip.
// Usage: node edge-profile.mjs <clip.json> [layer]
import fs from 'node:fs';
import { PNG } from 'pngjs';

const [, , clipArg, layer = 'composite'] = process.argv;
const clip = JSON.parse(fs.readFileSync(clipArg, 'utf8'));
const lum = (r, g, b) => 0.2126 * r + 0.7152 * g + 0.0722 * b;
const buckets = [0, 20, 40, 60, 80, 100, 120, 140, 180, 255];

for (const frame of clip.frames) {
  const p = layer === 'composite' ? frame.png : frame.layers[layer]?.png;
  if (!p) continue;
  const { width: w, height: h, data } = PNG.sync.read(fs.readFileSync(p));
  const at = (x, y) => (y * w + x) * 4;
  const alpha = (x, y) => data[at(x, y) + 3];
  const hist = new Array(buckets.length - 1).fill(0);
  let edge = 0;
  let maxL = 0;
  let maxAt = null;
  for (let y = 0; y < h; y += 1) {
    for (let x = 0; x < w; x += 1) {
      if (alpha(x, y) === 0) continue;
      const isEdge =
        (x > 0 && alpha(x - 1, y) < 128) ||
        (x < w - 1 && alpha(x + 1, y) < 128) ||
        (y > 0 && alpha(x, y - 1) < 128) ||
        (y < h - 1 && alpha(x, y + 1) < 128);
      if (!isEdge) continue;
      edge += 1;
      const L = lum(data[at(x, y)], data[at(x, y) + 1], data[at(x, y) + 2]);
      if (L > maxL) {
        maxL = L;
        maxAt = [x, y, data[at(x, y)], data[at(x, y) + 1], data[at(x, y) + 2]];
      }
      for (let i = 0; i < buckets.length - 1; i += 1) {
        if (L >= buckets[i] && L < buckets[i + 1] + (i === buckets.length - 2 ? 1 : 0)) {
          hist[i] += 1;
          break;
        }
      }
    }
  }
  const pct = hist.map((n) => ((n / edge) * 100).toFixed(1).padStart(5));
  console.log(
    `f${frame.index} edge=${String(edge).padStart(4)} maxL=${maxL.toFixed(0).padStart(3)} at[${maxAt}] buckets ${pct.join(' ')}`,
  );
}
console.log('buckets', buckets.join(' | '));
