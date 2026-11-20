#!/usr/bin/env node
// QA-only: for each requested frame box, emit a 3-panel image
// (published | candidate | candidate dimmed with changed pixels in amber).
// Usage: node diffcrop.mjs <baseDir> <candDir> <outDir> <scale> <i:x,y,w,h> [...]
import fs from 'node:fs';
import path from 'node:path';
import { PNG } from 'pngjs';

const [, , baseDir, candDir, outDir, scaleArg, ...specs] = process.argv;
const scale = Number(scaleArg);
const GAP = 8;
fs.mkdirSync(outDir, { recursive: true });
const read = (p) => PNG.sync.read(fs.readFileSync(p));

for (const spec of specs) {
  const [i, box] = spec.split(':');
  const [bx, by, bw, bh] = box.split(',').map(Number);
  const a = read(`${baseDir}/${String(i).padStart(2, '0')}.png`);
  const b = read(`${candDir}/${String(i).padStart(2, '0')}.png`);
  const width = bw * scale * 3 + GAP * 2;
  const out = new PNG({ width, height: bh * scale });
  out.data.fill(255);

  // blit one magnified source pixel at exact output coordinates
  const blit = (ox, oy, r, g, bl) => {
    for (let dy = 0; dy < scale; dy += 1) {
      for (let dx = 0; dx < scale; dx += 1) {
        const tx = ox + dx;
        const ty = oy + dy;
        if (tx < 0 || ty < 0 || tx >= width || ty >= out.height) continue;
        const d = (ty * width + tx) * 4;
        out.data[d] = r;
        out.data[d + 1] = g;
        out.data[d + 2] = bl;
        out.data[d + 3] = 255;
      }
    }
  };

  let diffCount = 0;
  for (const [panel, img] of [[0, a], [1, b]]) {
    const ox = panel * (bw * scale + GAP);
    for (let y = 0; y < bh; y += 1) {
      for (let x = 0; x < bw; x += 1) {
        const s = ((by + y) * img.width + (bx + x)) * 4;
        const al = img.data[s + 3] / 255;
        blit(ox + x * scale, y * scale,
          Math.round(img.data[s] * al + 246 * (1 - al)),
          Math.round(img.data[s + 1] * al + 246 * (1 - al)),
          Math.round(img.data[s + 2] * al + 246 * (1 - al)));
      }
    }
  }
  const ox = 2 * (bw * scale + GAP);
  for (let y = 0; y < bh; y += 1) {
    for (let x = 0; x < bw; x += 1) {
      const s = ((by + y) * a.width + (bx + x)) * 4;
      const t = ((by + y) * b.width + (bx + x)) * 4;
      const diff = a.data[s] !== b.data[s] || a.data[s + 1] !== b.data[s + 1] || a.data[s + 2] !== b.data[s + 2] || a.data[s + 3] !== b.data[t + 3];
      if (diff) diffCount += 1;
      const al = (b.data[t + 3] / 255) * (diff ? 1 : 0.3);
      const base = 246 * (1 - al);
      blit(ox + x * scale, y * scale,
        diff ? 255 : Math.round(b.data[t] * al + base),
        diff ? 176 : Math.round(b.data[t + 1] * al + base),
        diff ? 64 : Math.round(b.data[t + 2] * al + base));
    }
  }
  const name = `PREVIEW-f${String(i).padStart(2, '0')}-published-candidate-diff-${scale}x.png`;
  fs.writeFileSync(path.join(outDir, name), PNG.sync.write(out));
  console.log(`${name} box=${box} changedPixels=${diffCount} size=${width}x${out.height}`);
}
