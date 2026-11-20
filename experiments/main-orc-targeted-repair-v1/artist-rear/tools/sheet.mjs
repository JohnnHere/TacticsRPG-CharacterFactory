#!/usr/bin/env node
// QA-only: build a magnified contact sheet from a clip.json.
// Usage: node sheet.mjs <clip.json> <out.png> <scale> [layer]
// layer: "composite" (default) or a layer folder name (body, weaponFront, handFront, weaponBack)
import fs from 'node:fs';
import path from 'node:path';
import { PNG } from 'pngjs';

const [, , clipArg, outPath, scaleArg = '2', layer = 'composite'] = process.argv;
const clip = JSON.parse(fs.readFileSync(clipArg, 'utf8'));
const scale = Number(scaleArg);
const frames = clip.frames.map((f) => {
  const p = layer === 'composite' ? f.png : f.layers[layer]?.png;
  if (!p || !fs.existsSync(p)) throw new Error(`missing ${layer} for frame ${f.index}: ${p}`);
  return PNG.sync.read(fs.readFileSync(p));
});
const w = Math.max(...frames.map((f) => f.width));
const h = Math.max(...frames.map((f) => f.height));
const out = new PNG({ width: w * scale * frames.length, height: h * scale });
out.data.fill(255);
frames.forEach((frame, i) => {
  const baseX = i * w * scale;
  for (let y = 0; y < frame.height; y += 1) {
    for (let x = 0; x < frame.width; x += 1) {
      const s = (y * frame.width + x) * 4;
      const a = frame.data[s + 3];
      if (a === 0) continue;
      const af = a / 255;
      for (let dy = 0; dy < scale; dy += 1) {
        for (let dx = 0; dx < scale; dx += 1) {
          const d = ((y * scale + dy) * out.width + baseX + x * scale + dx) * 4;
          out.data[d] = Math.round(frame.data[s] * af + 255 * (1 - af));
          out.data[d + 1] = Math.round(frame.data[s + 1] * af + 255 * (1 - af));
          out.data[d + 2] = Math.round(frame.data[s + 2] * af + 255 * (1 - af));
          out.data[d + 3] = 255;
        }
      }
    }
  }
});
fs.mkdirSync(path.dirname(outPath), { recursive: true });
fs.writeFileSync(outPath, PNG.sync.write(out));
console.log(outPath, `${out.width}x${out.height}`, `scale=${scale}`, `layer=${layer}`, `frames=${frames.length}`);
