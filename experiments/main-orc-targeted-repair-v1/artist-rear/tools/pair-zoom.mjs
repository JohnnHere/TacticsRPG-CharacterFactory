#!/usr/bin/env node
// QA-only layout: same crop box from several PNGs, magnified, side by side.
// Usage: node pair-zoom.mjs <out.png> <scale> <x,y,w,h> <a.png> <b.png> [...]
import fs from 'node:fs';
import path from 'node:path';
import { PNG } from 'pngjs';

const [, , outPath, scaleArg, boxArg, ...inputs] = process.argv;
const scale = Number(scaleArg);
const [x0, y0, bw, bh] = boxArg.split(',').map(Number);
const frames = inputs.map((f) => PNG.sync.read(fs.readFileSync(f)));
const out = new PNG({ width: bw * scale * frames.length + 8 * (frames.length - 1), height: bh * scale });
out.data.fill(255);
const gap = 8;
frames.forEach((img, i) => {
  const baseX = i * (bw * scale + gap);
  for (let y = 0; y < bh; y += 1) {
    for (let x = 0; x < bw; x += 1) {
      const sx = x0 + x;
      const sy = y0 + y;
      if (sx < 0 || sy < 0 || sx >= img.width || sy >= img.height) continue;
      const s = (sy * img.width + sx) * 4;
      const a = img.data[s + 3];
      if (a === 0) continue;
      const af = a / 255;
      for (let dy = 0; dy < scale; dy += 1) {
        for (let dx = 0; dx < scale; dx += 1) {
          const d = ((y * scale + dy) * out.width + baseX + x * scale + dx) * 4;
          out.data[d] = Math.round(img.data[s] * af + 255 * (1 - af));
          out.data[d + 1] = Math.round(img.data[s + 1] * af + 255 * (1 - af));
          out.data[d + 2] = Math.round(img.data[s + 2] * af + 255 * (1 - af));
          out.data[d + 3] = 255;
        }
      }
    }
  }
});
fs.mkdirSync(path.dirname(outPath), { recursive: true });
fs.writeFileSync(outPath, PNG.sync.write(out));
console.log(outPath, `${out.width}x${out.height}`, `scale=${scale}`, `box=${boxArg}`);
