#!/usr/bin/env node
// Stack a narrow region vertically across clip frames for flicker inspection.
// Usage: node vstack.mjs <out.png> <scale> <x,y,w,h> <clip.json> [frameIdxCsv|all]
import fs from 'node:fs';
import path from 'node:path';
import { PNG } from 'pngjs';

const [, , outArg, scaleArg, regionArg, clipArg, idxArg = 'all'] = process.argv;
const scale = Number(scaleArg);
const [rx, ry, rw, rh] = regionArg.split(',').map(Number);
const clip = JSON.parse(fs.readFileSync(clipArg, 'utf8'));
let idx = clip.frames.map((f, i) => i);
if (idxArg !== 'all') idx = idxArg.split(',').map(Number);
const frames = idx.map((i) => {
  const p = clip.frames[i].nativePng || clip.frames[i].png;
  return { i, p, img: PNG.sync.read(fs.readFileSync(p)) };
});
const gap = Number(process.env.GAP ?? 8);
const out = new PNG({ width: rw * scale + gap * 2, height: frames.length * (rh * scale + gap) + gap });
for (let y = 0; y < out.height; y++) for (let x = 0; x < out.width; x++) {
  const s = (y * out.width + x) * 4;
  out.data[s] = 24; out.data[s + 1] = 26; out.data[s + 2] = 30; out.data[s + 3] = 255;
}
frames.forEach((f, n) => {
  for (let y = 0; y < rh; y++) for (let x = 0; x < rw; x++) {
    const sx = rx + x, sy = ry + y;
    if (sx >= f.img.width || sy >= f.img.height) continue;
    const s = (sy * f.img.width + sx) * 4;
    if (f.img.data[s + 3] === 0) continue;
    const dx = gap + x * scale;
    const dy = gap + n * (rh * scale + gap) + y * scale;
    for (let qy = 0; qy < scale; qy++) for (let qx = 0; qx < scale; qx++) {
      const d = ((dy + qy) * out.width + (dx + qx)) * 4;
      out.data[d] = f.img.data[s]; out.data[d + 1] = f.img.data[s + 1]; out.data[d + 2] = f.img.data[s + 2]; out.data[d + 3] = 255;
    }
  }
});
fs.mkdirSync(path.dirname(outArg), { recursive: true });
fs.writeFileSync(outArg, PNG.sync.write(out));
console.log(`out=${outArg} region=${rx},${ry},${rw},${rh} scale=${scale} frames=${frames.length}`);
