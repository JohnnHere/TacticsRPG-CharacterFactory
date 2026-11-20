#!/usr/bin/env node
// QA-only probe: locate the weapon's wooden handle pixels inside a placed frame,
// and the glove pixels of the body/handFront, then report the gap geometry.
// Usage: node grip-probe.mjs <clip.json> <frameIndex>
import fs from 'node:fs';
import { PNG } from 'pngjs';

const [, , clipArg, idxArg] = process.argv;
const clip = JSON.parse(fs.readFileSync(clipArg, 'utf8'));
const f = clip.frames[Number(idxArg)];
const read = (p) => PNG.sync.read(fs.readFileSync(p));
const mask = (img, pred) => {
  const out = [];
  for (let y = 0; y < img.height; y += 1) {
    for (let x = 0; x < img.width; x += 1) {
      const s = (y * img.width + x) * 4;
      if (img.data[s + 3] === 0) continue;
      if (pred(img.data[s], img.data[s + 1], img.data[s + 2])) out.push([x, y]);
    }
  }
  return out;
};
const bbox = (px) =>
  px.length
    ? [Math.min(...px.map((p) => p[0])), Math.min(...px.map((p) => p[1])), Math.max(...px.map((p) => p[0])), Math.max(...px.map((p) => p[1]))]
    : null;
// wooden handle: brown, red-dominant, mid luminance
const wood = (r, g, b) => r > g && g >= b && r >= 50 && r <= 130 && r - b >= 15;
const leather = (r, g, b) => r > g && g >= b && r > 25 && r < 90 && r - b >= 8;
const comps = [];
for (const ln of ['weaponFront', 'weaponBack', 'handFront', 'body']) {
  const img = read(f.layers[ln].png);
  const w = mask(img, ln.startsWith('weapon') ? wood : leather);
  console.log(`${ln} wood/leather px=${w.length} bbox=${bbox(w)}`);
  // connected components of that family
  const seen = new Set();
  const key = (x, y) => `${x},${y}`;
  const set = new Set(w.map(([x, y]) => key(x, y)));
  for (const [x, y] of w) {
    if (seen.has(key(x, y))) continue;
    const st = [[x, y]];
    seen.add(key(x, y));
    const px = [];
    while (st.length) {
      const [cx, cy] = st.pop();
      px.push([cx, cy]);
      for (let dy = -1; dy <= 1; dy += 1) {
        for (let dx = -1; dx <= 1; dx += 1) {
          const k = key(cx + dx, cy + dy);
          if (set.has(k) && !seen.has(k)) {
            seen.add(k);
            st.push([cx + dx, cy + dy]);
          }
        }
      }
    }
    if (px.length >= 6) comps.push({ layer: ln, n: px.length, bbox: bbox(px) });
  }
}
comps.sort((a, b) => b.n - a.n);
for (const c of comps.slice(0, 10)) console.log(`  cluster ${c.layer} n=${c.n} bbox=${c.bbox.join(',')}`);
console.log('grip', f.rightGrip, 'rot', f.rotationDeg, 'handFront bbox', bbox(mask(read(f.layers.handFront.png), () => true)));
