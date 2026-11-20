#!/usr/bin/env node
// QA-only: crop a fixed-size window centered on each frame's rightGrip, then tile
// with nearest-neighbour magnification. Read/measure only.
// Usage: node grip-zoom.mjs <clip.json> <out.png> <scale> <w,h> <layer|composite> <i0,...>
import fs from 'node:fs';
import path from 'node:path';
import { PNG } from 'pngjs';

const [, , clipArg, outPath, scaleArg, sizeArg, layer = 'composite', idxArg] = process.argv;
const clip = JSON.parse(fs.readFileSync(clipArg, 'utf8'));
const scale = Number(scaleArg);
const [bw, bh] = sizeArg.split(',').map(Number);
const idx = idxArg.split(',').map(Number);
const tiles = idx.map((i) => {
  const f = clip.frames[i];
  const p = layer === 'composite' ? f.png : f.layers[layer].png;
  const img = PNG.sync.read(fs.readFileSync(p));
  const [gx, gy] = f.rightGrip || [128, 128];
  const ox = Math.round(gx - bw / 2);
  const oy = Math.round(gy - bh / 2);
  return { img, ox, oy, grip: [gx, gy] };
});
const out = new PNG({ width: bw * scale * tiles.length, height: bh * scale });
out.data.fill(255);
tiles.forEach((t, k) => {
  const { img, ox, oy } = t;
  const baseX = k * bw * scale;
  for (let y = 0; y < bh; y += 1) {
    for (let x = 0; x < bw; x += 1) {
      const sx = ox + x;
      const sy = oy + y;
      if (sx < 0 || sy < 0 || sx >= img.width || sy >= img.height) continue;
      const s = (sy * img.width + sx) * 4;
      const a = img.data[s + 3];
      if (a === 0) continue;
      const af = a / 255;
      const isGrip = sx === t.grip[0] && sy === t.grip[1];
      for (let dy = 0; dy < scale; dy += 1) {
        for (let dx = 0; dx < scale; dx += 1) {
          const d = ((y * scale + dy) * out.width + baseX + x * scale + dx) * 4;
          if (isGrip) {
            out.data[d] = 255;
            out.data[d + 1] = 0;
            out.data[d + 2] = 255;
          } else {
            out.data[d] = Math.round(img.data[s] * af + 255 * (1 - af));
            out.data[d + 1] = Math.round(img.data[s + 1] * af + 255 * (1 - af));
            out.data[d + 2] = Math.round(img.data[s + 2] * af + 255 * (1 - af));
          }
          out.data[d + 3] = 255;
        }
      }
    }
  }
});
fs.mkdirSync(path.dirname(outPath), { recursive: true });
fs.writeFileSync(outPath, PNG.sync.write(out));
console.log(outPath, `tiles=${idx.join(',')}`, `grips=${tiles.map((t) => t.grip.join(':')).join(' ')}`, `layer=${layer}`);
