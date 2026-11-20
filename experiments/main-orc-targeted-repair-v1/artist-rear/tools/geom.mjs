#!/usr/bin/env node
// QA-only: per-frame, per-layer geometry report: bbox, lowest opaque row vs groundY,
// and the alpha neighbourhood around each frame's declared rightGrip.
// Usage: node geom.mjs <clip.json>
import fs from 'node:fs';
import { PNG } from 'pngjs';

const [, , clipArg] = process.argv;
const clip = JSON.parse(fs.readFileSync(clipArg, 'utf8'));
const groundY = clip.groundY ?? 190;
const layers = ['weaponBack', 'body', 'weaponFront', 'handFront'];

const bboxOf = (data, w, h) => {
  let x0 = 1e9; let y0 = 1e9; let x1 = -1; let y1 = -1; let n = 0;
  for (let y = 0; y < h; y += 1) {
    for (let x = 0; x < w; x += 1) {
      if (data[(y * w + x) * 4 + 3] === 0) continue;
      n += 1;
      if (x < x0) x0 = x;
      if (y < y0) y0 = y;
      if (x > x1) x1 = x;
      if (y > y1) y1 = y;
    }
  }
  return n ? [x0, y0, x1, y1, n] : null;
};

console.log(`clip=${clipArg} groundY=${groundY} durations=${clip.durationsMs}`);
for (const f of clip.frames) {
  const rows = [];
  for (const ln of layers) {
    const p = f.layers?.[ln]?.png;
    if (!p) continue;
    const { width: w, height: h, data } = PNG.sync.read(fs.readFileSync(p));
    const bb = bboxOf(data, w, h);
    rows.push(`${ln}:${bb ? `x${bb[0]}-${bb[2]} y${bb[1]}-${bb[3]} n${bb[4]}${bb[3] > groundY ? ' !LOW' : ''}` : 'empty'}`);
  }
  const comp = PNG.sync.read(fs.readFileSync(f.png));
  const cb = bboxOf(comp.data, comp.width, comp.height);
  let gripNote = '';
  if (f.weaponVisible && f.rightGrip) {
    const [gx, gy] = f.rightGrip;
    const cells = [];
    for (let dy = -2; dy <= 2; dy += 1) {
      let row = '';
      for (let dx = -2; dx <= 2; dx += 1) {
        const x = gx + dx;
        const y = gy + dy;
        const inside = x >= 0 && y >= 0 && x < comp.width && y < comp.height;
        row += inside && comp.data[(y * comp.width + x) * 4 + 3] > 0 ? '#' : '.';
      }
      cells.push(row);
    }
    gripNote = `grip=${gx},${gy} ${cells.join('/')}`;
  }
  console.log(
    `f${f.index} ${String(f.durationMs).padStart(3)}ms comp:x${cb[0]}-${cb[2]} y${cb[1]}-${cb[3]}${cb[3] > groundY ? ' !LOW' : ''} | ${rows.join(' | ')} ${gripNote}`,
  );
}
