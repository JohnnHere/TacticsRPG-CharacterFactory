#!/usr/bin/env node
// QA-only: zoom a window centred on an arbitrary coordinate of one clip frame.
// Usage: node zoom-at.mjs <clip.json> <out.png> <i> <x,y> <w,h> <scale> <layer|composite>
import fs from 'node:fs';
import path from 'node:path';
import { PNG } from 'pngjs';

const [, , clipArg, outPath, iArg, xyArg, whArg, scaleArg, layer = 'composite'] = process.argv;
const clip = JSON.parse(fs.readFileSync(clipArg, 'utf8'));
const f = clip.frames[Number(iArg)];
const [cx, cy] = xyArg.split(',').map(Number);
const [bw, bh] = whArg.split(',').map(Number);
const scale = Number(scaleArg);
const p = layer === 'composite' ? f.png : f.layers[layer].png;
const img = PNG.sync.read(fs.readFileSync(p));
const ox = cx - Math.floor(bw / 2);
const oy = cy - Math.floor(bh / 2);
const out = new PNG({ width: bw * scale, height: bh * scale });
out.data.fill(255);
for (let y = 0; y < bh; y += 1) {
  for (let x = 0; x < bw; x += 1) {
    const sx = ox + x;
    const sy = oy + y;
    if (sx < 0 || sy < 0 || sx >= img.width || sy >= img.height) continue;
    const s = (sy * img.width + sx) * 4;
    const a = img.data[s + 3];
    if (a === 0) continue;
    const af = a / 255;
    for (let dy = 0; dy < scale; dy += 1) {
      for (let dx = 0; dx < scale; dx += 1) {
        const d = ((y * scale + dy) * out.width + x * scale + dx) * 4;
        out.data[d] = Math.round(img.data[s] * af + 255 * (1 - af));
        out.data[d + 1] = Math.round(img.data[s + 1] * af + 255 * (1 - af));
        out.data[d + 2] = Math.round(img.data[s + 2] * af + 255 * (1 - af));
        out.data[d + 3] = 255;
      }
    }
  }
}
fs.mkdirSync(path.dirname(outPath), { recursive: true });
fs.writeFileSync(outPath, PNG.sync.write(out));
console.log(outPath, `frame=${iArg} centre=${xyArg} window=${whArg} scale=${scale} layer=${layer}`);
