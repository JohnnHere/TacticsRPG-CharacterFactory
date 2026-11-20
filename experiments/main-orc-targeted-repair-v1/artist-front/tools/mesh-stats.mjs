#!/usr/bin/env node
// Count bright desaturated (chainmail dot) pixels and mid-gray cloth pixels
// in a region per frame, to detect material flflicker between legs.
// Usage: node mesh-stats.mjs <clip.json> <x,y,w,h>
import fs from 'node:fs';
import { PNG } from 'pngjs';

const [, , clipArg, regionArg] = process.argv;
const [rx, ry, rw, rh] = regionArg.split(',').map(Number);
const clip = JSON.parse(fs.readFileSync(clipArg, 'utf8'));
for (const f of clip.frames) {
  const img = PNG.sync.read(fs.readFileSync(f.nativePng || f.png));
  let bright = 0, mid = 0, dark = 0, opaque = 0, maxLum = 0;
  for (let y = ry; y < ry + rh; y++) for (let x = rx; x < rx + rw; x++) {
    const s = (y * img.width + x) * 4;
    if (img.data[s + 3] === 0) continue;
    opaque++;
    const [r, g, b] = [img.data[s], img.data[s + 1], img.data[s + 2]];
    const lum = 0.2126 * r + 0.7152 * g + 0.0722 * b;
    const sat = Math.max(r, g, b) - Math.min(r, g, b);
    if (lum > maxLum) maxLum = lum;
    if (lum > 90 && sat < 12) bright++;
    else if (lum > 40 && lum <= 90) mid++;
    else dark++;
  }
  console.log(`f${f.index} opaque=${opaque} brightMesh=${bright} midShade=${mid} dark=${dark} maxLum=${maxLum.toFixed(0)}`);
}
