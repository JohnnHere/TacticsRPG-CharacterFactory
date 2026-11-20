#!/usr/bin/env node
// QA-only previews for the candidate: full-cycle strips and paired grip crops with a
// diff highlight for the frames the repair actually changed.
// Writes PNGs into the diagnostics dir; never touches production art.
import fs from 'node:fs';
import path from 'node:path';
import { PNG } from 'pngjs';

const ROOT = process.cwd();
const BASE = 'characters/orc-v1/source/rear-recovery-v2/back_r/Sword/Attack-representative-v2';
const CAND = 'experiments/main-orc-targeted-repair-v1/artist-rear/candidate/clip/back_r/Sword/Attack-representative-v2-occlusion-v1';
const OUT = 'experiments/main-orc-targeted-repair-v1/artist-rear/diagnostics';
const baseClip = JSON.parse(fs.readFileSync(path.join(ROOT, BASE, 'clip.json'), 'utf8'));
const candClip = JSON.parse(fs.readFileSync(path.join(ROOT, CAND, 'clip.json'), 'utf8'));
const read = (p) => PNG.sync.read(fs.readFileSync(path.join(ROOT, p)));
const put = (img, x, y, r, g, b, a = 255) => {
  const d = (y * img.width + x) * 4;
  img.data[d] = r; img.data[d + 1] = g; img.data[d + 2] = b; img.data[d + 3] = a;
};
const over = (dst, img, ox, oy, scale, bg = [246, 246, 248]) => {
  for (let y = 0; y < img.height; y += 1) {
    for (let x = 0; x < img.width; x += 1) {
      const s = (y * img.width + x) * 4;
      const a = img.data[s + 3] / 255;
      if (a === 0) continue;
      const r = Math.round(img.data[s] * a + bg[0] * (1 - a));
      const g = Math.round(img.data[s + 1] * a + bg[1] * (1 - a));
      const b = Math.round(img.data[s + 2] * a + bg[2] * (1 - a));
      for (let dy = 0; dy < scale; dy += 1) {
        for (let dx = 0; dx < scale; dx += 1) {
          const tx = ox + x * scale + dx;
          const ty = oy + y * scale + dy;
          if (tx < 0 || ty < 0 || tx >= dst.width || ty >= dst.height) continue;
          put(dst, tx, ty, r, g, b);
        }
      }
    }
  }
};

// 1) full cycle strips, baseline over candidate, 1x of the 256 composite canvas
const W = 256 * 8;
const strip = new PNG({ width: W, height: 256 * 2 + 8 });
strip.data.fill(255);
for (let i = 0; i < 8; i += 1) {
  over(strip, read(baseClip.frames[i].png), i * 256, 0, 1, [246, 246, 248]);
  over(strip, read(candClip.frames[i].png), i * 256, 264, 1, [246, 246, 248]);
}
fs.writeFileSync(path.join(ROOT, OUT, 'PREVIEW-cycle-baseline-top-candidate-bottom.png'), PNG.sync.write(strip));

// 2) paired grip crops + diff overlay for changed frames
const changed = [1, 4, 5, 6];
const boxes = { 1: [156, 90, 34, 30], 4: [168, 84, 28, 26], 5: [166, 110, 28, 24], 6: [154, 112, 30, 30] };
const scale = 8;
for (const i of changed) {
  const [bx, by, bw, bh] = boxes[i];
  const a = read(baseClip.frames[i].png);
  const b = read(candClip.frames[i].png);
  const out = new PNG({ width: bw * scale * 3 + 16, height: bh * scale });
  out.data.fill(255);
  const crop = (img, ox) => {
    for (let y = 0; y < bh; y += 1) {
      for (let x = 0; x < bw; x += 1) {
        const s = ((by + y) * img.width + (bx + x)) * 4;
        const al = img.data[s + 3] / 255;
        const r = Math.round(img.data[s] * al + 246 * (1 - al));
        const g = Math.round(img.data[s + 1] * al + 246 * (1 - al));
        const bl = Math.round(img.data[s + 2] * al + 246 * (1 - al));
        for (let dy = 0; dy < scale; dy += 1) {
          for (let dx = 0; dx < scale; dx += 1) put(out, ox + x * scale + dx, y * scale + dy, r, g, bl);
        }
      }
    }
  };
  crop(a, 0);
  crop(b, bw * scale + 8);
  // diff panel: candidate dimmed with changed pixels in amber
  const ox = (bw * scale + 8) * 2;
  for (let y = 0; y < bh; y += 1) {
    for (let x = 0; x < bw; x += 1) {
      const s = ((by + y) * a.width + (bx + x)) * 4;
      const t = ((by + y) * b.width + (bx + x)) * 4;
      const diff = a.data[s] !== b.data[s] || a.data[s + 1] !== b.data[s + 1] || a.data[s + 2] !== b.data[s + 2] || a.data[s + 3] !== b.data[t + 3];
      const al = b.data[t + 3] / 255;
      const dim = diff ? 1 : 0.25;
      const r = diff ? 255 : Math.round(b.data[t] * al * dim + 246 * (1 - al * dim));
      const g = diff ? 176 : Math.round(b.data[t + 1] * al * dim + 246 * (1 - al * dim));
      const bl = diff ? 64 : Math.round(b.data[t + 2] * al * dim + 246 * (1 - al * dim));
      for (let dy = 0; dy < scale; dy += 1) {
        for (let dx = 0; dx < scale; dx += 1) put(out, ox + x * scale + dx, y * scale + dy, r, g, bl);
      }
    }
  }
  fs.writeFileSync(path.join(ROOT, OUT, `PREVIEW-f${String(i).padStart(2, '0')}-baseline-candidate-diff-${scale}x.png`), PNG.sync.write(out));
  console.log(`f${i} box=${bx},${by},${bw},${bh} -> PREVIEW-f${String(i).padStart(2, '0')}-baseline-candidate-diff-${scale}x.png`);
}
console.log(`strip ${W}x${strip.height} -> PREVIEW-cycle-baseline-top-candidate-bottom.png`);
