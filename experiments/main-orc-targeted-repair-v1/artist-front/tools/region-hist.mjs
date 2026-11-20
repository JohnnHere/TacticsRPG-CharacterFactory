#!/usr/bin/env node
// Color histogram of a fixed region for a clip's native frames.
// Usage: node region-hist.mjs <clip.json> <x,y,w,h>
import fs from 'node:fs';
import { PNG } from 'pngjs';

const [, , clipArg, regionArg] = process.argv;
const [rx, ry, rw, rh] = regionArg.split(',').map(Number);
const clip = JSON.parse(fs.readFileSync(clipArg, 'utf8'));
for (const f of clip.frames) {
  const img = PNG.sync.read(fs.readFileSync(f.nativePng || f.png));
  const counts = new Map();
  for (let y = ry; y < ry + rh; y++) for (let x = rx; x < rx + rw; x++) {
    const s = (y * img.width + x) * 4;
    if (img.data[s + 3] === 0) continue;
    const key = `${img.data[s]},${img.data[s + 1]},${img.data[s + 2]}`;
    counts.set(key, (counts.get(key) || 0) + 1);
  }
  let lum = 0, n = 0;
  for (const [rgb, c] of counts) {
    const [r, g, b] = rgb.split(',').map(Number);
    lum += (0.2126 * r + 0.7152 * g + 0.0722 * b) * c;
    n += c;
  }
  const top = [...counts.entries()].sort((a, b) => b[1] - a[1]).slice(0, 8)
    .map(([rgb, c]) => `${rgb}x${c}`).join(' ');
  console.log(`f${f.index} avgLum=${(lum / n).toFixed(1)} px=${n} top: ${top}`);
}
