#!/usr/bin/env node
// QA-only diagnostic: highlights suspicious silhouette-edge pixels on a magnified
// crop. Detection only; writes nothing to production art.
// Usage: node mark-edges.mjs <clip.json> <out.png> <scale> <x,y,w,h> <layer|composite> <i0,...> [--lo=110] [--hi=200]
import fs from 'node:fs';
import path from 'node:path';
import { PNG } from 'pngjs';

const a = process.argv.slice(2);
const [clipArg, outPath, scaleArg, boxArg, layer = 'composite', idxArg] = a;
const opt = Object.fromEntries(a.filter((x) => x.startsWith('--')).map((x) => x.replace(/^--/, '').split('=')));
const lo = Number(opt.lo ?? 110);
const hi = Number(opt.hi ?? 200);
const scale = Number(scaleArg);
const [bx, by, bw, bh] = boxArg.split(',').map(Number);
const clip = JSON.parse(fs.readFileSync(clipArg, 'utf8'));
const idx = idxArg.split(',').map(Number);
const lum = (r, g, b) => 0.2126 * r + 0.7152 * g + 0.0722 * b;

const srcs = idx.map((i) => {
  const f = clip.frames[i];
  const p = layer === 'composite' ? f.png : f.layers[layer].png;
  return PNG.sync.read(fs.readFileSync(p));
});
const out = new PNG({ width: bw * scale * srcs.length, height: bh * scale });
out.data.fill(255);
let flagged = 0;
srcs.forEach((src, k) => {
  const { width: w, height: h, data } = src;
  const alpha = (x, y) => data[(y * w + x) * 4 + 3];
  const baseX = k * bw * scale;
  for (let y = 0; y < bh; y += 1) {
    for (let x = 0; x < bw; x += 1) {
      const sx = bx + x;
      const sy = by + y;
      if (sx < 0 || sy < 0 || sx >= w || sy >= h) continue;
      const s = (sy * w + sx) * 4;
      const al = data[s + 3];
      if (al === 0) continue;
      const af = al / 255;
      let r = data[s] * af + 255 * (1 - af);
      let g = data[s + 1] * af + 255 * (1 - af);
      let b = data[s + 2] * af + 255 * (1 - af);
      const isEdge =
        (sx > 0 && alpha(sx - 1, sy) < 128) ||
        (sx < w - 1 && alpha(sx + 1, sy) < 128) ||
        (sy > 0 && alpha(sx, sy - 1) < 128) ||
        (sy < h - 1 && alpha(sx, sy + 1) < 128);
      const L = lum(data[s], data[s + 1], data[s + 2]);
      if (isEdge && L >= lo && L <= hi) {
        r = 255; g = 0; b = 255;
        flagged += 1;
      }
      for (let dy = 0; dy < scale; dy += 1) {
        for (let dx = 0; dx < scale; dx += 1) {
          const d = ((y * scale + dy) * out.width + baseX + x * scale + dx) * 4;
          out.data[d] = r;
          out.data[d + 1] = g;
          out.data[d + 2] = b;
          out.data[d + 3] = 255;
        }
      }
    }
  }
});
fs.mkdirSync(path.dirname(outPath), { recursive: true });
fs.writeFileSync(outPath, PNG.sync.write(out));
console.log(outPath, `flagged=${flagged}`, `crop=${boxArg}`, `layer=${layer}`, `range=${lo}..${hi}`);
