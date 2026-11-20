#!/usr/bin/env node
// QA-only: dump raw RGBA values for given coordinates per frame.
// Usage: node px.mjs <clip.json> <layer> <i0,i1> x,y[,x,y...]
import fs from 'node:fs';
import { PNG } from 'pngjs';

const [, , clipArg, layer, idxArg, coordArg] = process.argv;
const clip = JSON.parse(fs.readFileSync(clipArg, 'utf8'));
const coords = coordArg.split(';').map((s) => s.split(',').map(Number));
for (const i of idxArg.split(',').map(Number)) {
  const f = clip.frames[i];
  const p = layer === 'composite' ? f.png : f.layers[layer].png;
  const { width: w, data } = PNG.sync.read(fs.readFileSync(p));
  const row = coords.map(([x, y]) => {
    const s = (y * w + x) * 4;
    return `(${x},${y}) rgba(${data[s]},${data[s + 1]},${data[s + 2]},${data[s + 3]})`;
  });
  console.log(`f${i} ${layer}: ${row.join('  ')}`);
}
