#!/usr/bin/env node
// Side-by-side crop compare of two PNG paths (each 256x256 composite), with
// optional horizontal flip of the second crop.
// Usage: node compare-crop.mjs <out.png> <scale> <x,y,w,h> <pngA> <pngB> <flipB:0|1>
import fs from 'node:fs';
import path from 'node:path';
import { PNG } from 'pngjs';

const [, , outArg, scaleArg, regionArg, pa, pb, flipArg = '0'] = process.argv;
const scale = Number(scaleArg);
const flipB = flipArg === '1';
const [rx, ry, rw, rh] = regionArg.split(',').map(Number);
const imgs = [pa, pb].map(p => PNG.sync.read(fs.readFileSync(p)));
const gap = Number(process.env.GAP ?? 8);
const out = new PNG({ width: 2 * (rw * scale + gap) + gap, height: rh * scale + gap * 2 });
for (const yy of [...Array(out.height).keys()]) for (const xx of [...Array(out.width).keys()]) {
  const s = (yy * out.width + xx) * 4;
  out.data[s] = 24; out.data[s + 1] = 26; out.data[s + 2] = 30; out.data[s + 3] = 255;
}
imgs.forEach((img, n) => {
  for (let y = 0; y < rh; y++) for (let x = 0; x < rw; x++) {
    const sx = (n === 1 && flipB) ? rx + rw - 1 - x : rx + x;
    if (sx < 0 || sx >= img.width) continue;
    const s = ((ry + y) * img.width + sx) * 4;
    if (img.data[s + 3] === 0) continue;
    const dx = gap + n * (rw * scale + gap) + x * scale;
    const dy = gap + y * scale;
    for (let qy = 0; qy < scale; qy++) for (let qx = 0; qx < scale; qx++) {
      const d = ((dy + qy) * out.width + (dx + qx)) * 4;
      out.data[d] = img.data[s]; out.data[d + 1] = img.data[s + 1]; out.data[d + 2] = img.data[s + 2]; out.data[d + 3] = 255;
    }
  }
});
fs.mkdirSync(path.dirname(outArg), { recursive: true });
fs.writeFileSync(outArg, PNG.sync.write(out));
console.log(`out=${outArg} region=${rx},${ry},${rw},${rh} scale=${scale} flipB=${flipB}`);
