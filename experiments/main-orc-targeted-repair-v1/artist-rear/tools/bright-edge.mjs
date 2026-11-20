#!/usr/bin/env node
// QA-only diagnostic: bright silhouette-edge census for a clip.
// Reads only. Reports opaque boundary pixels whose luminance is high, plus
// near-white pixels anywhere, grouped into connected clusters.
// Usage: node bright-edge.mjs <clip.json> [layer] [--lum=140] [--white=210]
import fs from 'node:fs';
import { PNG } from 'pngjs';

const args = process.argv.slice(2);
const clipArg = args[0];
const layer = args[1] && !args[1].startsWith('--') ? args[1] : 'composite';
const opt = Object.fromEntries(
  args.filter((a) => a.startsWith('--')).map((a) => a.replace(/^--/, '').split('=')),
);
const LUM = Number(opt.lum ?? 140);
const WHITE = Number(opt.white ?? 210);

const clip = JSON.parse(fs.readFileSync(clipArg, 'utf8'));
const lum = (r, g, b) => 0.2126 * r + 0.7152 * g + 0.0722 * b;

for (const frame of clip.frames) {
  const p = layer === 'composite' ? frame.png : frame.layers[layer]?.png;
  if (!p) continue;
  const img = PNG.sync.read(fs.readFileSync(p));
  const { width: w, height: h, data } = img;
  const at = (x, y) => (y * w + x) * 4;
  const alpha = (x, y) => data[at(x, y) + 3];
  const edge = [];
  const nearWhite = [];
  for (let y = 0; y < h; y += 1) {
    for (let x = 0; x < w; x += 1) {
      const a = alpha(x, y);
      if (a === 0) continue;
      const r = data[at(x, y)];
      const g = data[at(x, y) + 1];
      const b = data[at(x, y) + 2];
      const L = lum(r, g, b);
      if (L >= WHITE) nearWhite.push({ x, y, r, g, b, L: +L.toFixed(1) });
      const isEdge =
        (x > 0 && alpha(x - 1, y) < 128) ||
        (x < w - 1 && alpha(x + 1, y) < 128) ||
        (y > 0 && alpha(x, y - 1) < 128) ||
        (y < h - 1 && alpha(x, y + 1) < 128);
      if (isEdge && L >= LUM) edge.push({ x, y, r, g, b, L: +L.toFixed(1) });
    }
  }
  const cluster = (pts) => {
    const set = new Set(pts.map((p2) => `${p2.x},${p2.y}`));
    const seen = new Set();
    const out = [];
    for (const p2 of pts) {
      const k = `${p2.x},${p2.y}`;
      if (seen.has(k)) continue;
      const stack = [p2];
      seen.add(k);
      const group = [];
      while (stack.length) {
        const c = stack.pop();
        group.push(c);
        for (let dy = -1; dy <= 1; dy += 1) {
          for (let dx = -1; dx <= 1; dx += 1) {
            const nk = `${c.x + dx},${c.y + dy}`;
            if (set.has(nk) && !seen.has(nk)) {
              seen.add(nk);
              stack.push(pts.find((q) => q.x === c.x + dx && q.y === c.y + dy));
            }
          }
        }
      }
      const xs = group.map((c) => c.x);
      const ys = group.map((c) => c.y);
      out.push({
        n: group.length,
        bbox: [Math.min(...xs), Math.min(...ys), Math.max(...xs), Math.max(...ys)],
        maxL: Math.max(...group.map((c) => c.L)),
        sample: group.slice(0, 4).map((c) => `${c.x},${c.y}#${c.r},${c.g},${c.b}`),
      });
    }
    return out;
  };
  const edgeClusters = cluster(edge).sort((a, b) => b.n - a.n);
  const whiteClusters = cluster(nearWhite).sort((a, b) => b.n - a.n);
  console.log(`\n=== frame ${frame.index} ${frame.phase ?? ''} [${layer}] ===`);
  console.log(`  bright edge px (L>=${LUM}): ${edge.length} in ${edgeClusters.length} clusters`);
  for (const c of edgeClusters.slice(0, 8)) {
    console.log(`    n=${c.n} bbox=${c.bbox.join(',')} maxL=${c.maxL} ${c.sample.join(' ')}`);
  }
  console.log(`  near-white px (L>=${WHITE}): ${nearWhite.length} in ${whiteClusters.length} clusters`);
  for (const c of whiteClusters.slice(0, 6)) {
    console.log(`    n=${c.n} bbox=${c.bbox.join(',')} maxL=${c.maxL} ${c.sample.join(' ')}`);
  }
}
