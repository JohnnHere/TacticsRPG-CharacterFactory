#!/usr/bin/env node
// QA-only layout tool: assembles exact copies of production PNG frames into a
// nearest-neighbour magnified contact sheet for human/agent visual review.
// It never edits, recolours, resamples with filtering, or writes production art.
import fs from 'node:fs';
import path from 'node:path';
import { PNG } from 'pngjs';

const [, , outPath, scaleArg, ...inputs] = process.argv;
const scale = Number(scaleArg || 2);
if (!outPath || !inputs.length) {
  console.error('usage: node montage.mjs <out.png> <scale> <frame.png...>');
  process.exit(2);
}

const frames = inputs.map((f) => PNG.sync.read(fs.readFileSync(f)));
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
      const r = frame.data[s];
      const g = frame.data[s + 1];
      const b = frame.data[s + 2];
      for (let dy = 0; dy < scale; dy += 1) {
        for (let dx = 0; dx < scale; dx += 1) {
          const d = (((y * scale + dy)) * out.width + baseX + x * scale + dx) * 4;
          // alpha-over on white background (opaque review sheet)
          const af = a / 255;
          out.data[d] = Math.round(r * af + 255 * (1 - af));
          out.data[d + 1] = Math.round(g * af + 255 * (1 - af));
          out.data[d + 2] = Math.round(b * af + 255 * (1 - af));
          out.data[d + 3] = 255;
        }
      }
    }
  }
});

fs.mkdirSync(path.dirname(outPath), { recursive: true });
fs.writeFileSync(outPath, PNG.sync.write(out));
console.log(outPath, `${out.width}x${out.height}`, `scale ${scale}`, `${frames.length} frames`);
