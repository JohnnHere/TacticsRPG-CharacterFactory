#!/usr/bin/env node
// QA-only zoom tool: crops a region of selected clip frames and tiles them with
// nearest-neighbour magnification. Never writes production art.
// Usage: node crop.mjs <clip.json> <out.png> <scale> <x,y,w,h> <layer|composite> <i0,i1,...>
import fs from 'node:fs';
import path from 'node:path';
import { PNG } from 'pngjs';

const [, , clipArg, outPath, scaleArg, boxArg, layer = 'composite', idxArg] = process.argv;
const clip = JSON.parse(fs.readFileSync(clipArg, 'utf8'));
const scale = Number(scaleArg);
const [bx, by, bw, bh] = boxArg.split(',').map(Number);
const idx = idxArg ? idxArg.split(',').map(Number) : clip.frames.map((f) => f.index);
const srcs = idx.map((i) => {
  const f = clip.frames[i];
  const p = layer === 'composite' ? f.png : f.layers[layer].png;
  return PNG.sync.read(fs.readFileSync(p));
});
const out = new PNG({ width: bw * scale * srcs.length, height: bh * scale });
out.data.fill(255);
srcs.forEach((src, k) => {
  const baseX = k * bw * scale;
  for (let y = 0; y < bh; y += 1) {
    for (let x = 0; x < bw; x += 1) {
      const sx = bx + x;
      const sy = by + y;
      if (sx < 0 || sy < 0 || sx >= src.width || sy >= src.height) continue;
      const s = (sy * src.width + sx) * 4;
      const a = src.data[s + 3];
      if (a === 0) continue;
      const af = a / 255;
      for (let dy = 0; dy < scale; dy += 1) {
        for (let dx = 0; dx < scale; dx += 1) {
          const d = ((y * scale + dy) * out.width + baseX + x * scale + dx) * 4;
          out.data[d] = Math.round(src.data[s] * af + 255 * (1 - af));
          out.data[d + 1] = Math.round(src.data[s + 1] * af + 255 * (1 - af));
          out.data[d + 2] = Math.round(src.data[s + 2] * af + 255 * (1 - af));
          out.data[d + 3] = 255;
        }
      }
    }
  }
});
fs.mkdirSync(path.dirname(outPath), { recursive: true });
fs.writeFileSync(outPath, PNG.sync.write(out));
console.log(outPath, `${out.width}x${out.height}`, `crop=${boxArg}`, `layer=${layer}`, `frames=${idx.join(',')}`);
