#!/usr/bin/env node
// Montage native frames of a clip.
// Usage: node clip-montage.mjs <out.png> <scale> <clip.json> [frameIdxCsv|all]
import fs from 'node:fs';
import path from 'node:path';
import { PNG } from 'pngjs';

const [, , outArg, scaleArg, clipArg, idxArg = 'all'] = process.argv;
const scale = Number(scaleArg);
const clip = JSON.parse(fs.readFileSync(clipArg, 'utf8'));
let idx = clip.frames.map((f, i) => i);
if (idxArg !== 'all') idx = idxArg.split(',').map(Number);
const frames = idx.map((i) => {
  const p = clip.frames[i].nativePng || clip.frames[i].png;
  return { i, p, img: PNG.sync.read(fs.readFileSync(p)) };
});
function bbox(img) {
  const { width: w, height: h, data } = img;
  let x0 = w, y0 = h, x1 = -1, y1 = -1;
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
    if (data[(y * w + x) * 4 + 3] > 0) {
      if (x < x0) x0 = x; if (x > x1) x1 = x;
      if (y < y0) y0 = y; if (y > y1) y1 = y;
    }
  }
  if (x1 < 0) return null;
  return { x0, y0, x1, y1 };
}
const boxes = frames.map(f => bbox(f.img));
let gx0 = Math.min(...boxes.map(b => b.x0)), gx1 = Math.max(...boxes.map(b => b.x1));
let gy0 = Math.min(...boxes.map(b => b.y0)), gy1 = Math.max(...boxes.map(b => b.y1));
const gw = gx1 - gx0 + 1, gh = gy1 - gy0 + 1;
const gap = Number(process.env.GAP ?? 6);
const out = new PNG({ width: frames.length * (gw * scale + gap) + gap, height: gh * scale + gap * 2 });
for (let y = 0; y < out.height; y++) for (let x = 0; x < out.width; x++) {
  const s = (y * out.width + x) * 4;
  out.data[s] = 24; out.data[s + 1] = 26; out.data[s + 2] = 30; out.data[s + 3] = 255;
}
frames.forEach((f, n) => {
  for (let y = gy0; y <= gy1; y++) for (let x = gx0; x <= gx1; x++) {
    const s = (y * f.img.width + x) * 4;
    if (f.img.data[s + 3] === 0) continue;
    const dx = gap + n * (gw * scale + gap) + (x - gx0) * scale;
    const dy = gap + (y - gy0) * scale;
    for (let sy = 0; sy < scale; sy++) for (let sx = 0; sx < scale; sx++) {
      const d = ((dy + sy) * out.width + (dx + sx)) * 4;
      out.data[d] = f.img.data[s]; out.data[d + 1] = f.img.data[s + 1]; out.data[d + 2] = f.img.data[s + 2]; out.data[d + 3] = 255;
    }
  }
});
fs.mkdirSync(path.dirname(outArg), { recursive: true });
fs.writeFileSync(outArg, PNG.sync.write(out));
console.log(`out=${outArg} frames=${frames.map(f=>f.i).join(',')} globalBBox=${gw}x${gh} scale=${scale}`);
