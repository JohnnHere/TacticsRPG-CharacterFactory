#!/usr/bin/env node
// QA-only: measure a weapon sprite's handle geometry around a declared grip anchor.
// Reports the wooden-handle vertical span, its midpoint, the guard row and the pommel.
// Usage: node weapon-anchor.mjs <sprite.png> <gx,gy> [id]
import fs from 'node:fs';
import { PNG } from 'pngjs';

const [, , file, anchorArg, id = 'weapon'] = process.argv;
const [gx, gy] = anchorArg.split(',').map(Number);
const { width: w, height: h, data } = PNG.sync.read(fs.readFileSync(file));
const at = (x, y) => {
  const s = (y * w + x) * 4;
  return { r: data[s], g: data[s + 1], b: data[s + 2], a: data[s + 3] };
};
const rows = [];
for (let y = 0; y < h; y += 1) {
  let opaque = 0;
  let wood = 0;
  let steel = 0;
  let xs = [];
  for (let x = 0; x < w; x += 1) {
    const p = at(x, y);
    if (p.a === 0) continue;
    opaque += 1;
    xs.push(x);
    const chroma = Math.max(p.r, p.g, p.b) - Math.min(p.r, p.g, p.b);
    if (chroma > 10 && p.r > p.b) wood += 1;
    else steel += 1;
  }
  if (opaque) rows.push({ y, opaque, wood, steel, x0: Math.min(...xs), x1: Math.max(...xs) });
}
console.log(`weapon=${id} size=${w}x${h} anchor=${gx},${gy}`);
console.log('row  opaque wood steel  xspan');
for (const r of rows) console.log(`${String(r.y).padStart(3)} ${String(r.opaque).padStart(6)} ${String(r.wood).padStart(4)} ${String(r.steel).padStart(5)}  ${r.x0}-${r.x1}`);
// anchor column profile
console.log(`\nanchor column x=${gx} colours by row:`);
for (const r of rows) {
  const p = at(gx, r.y);
  if (p.a) console.log(`  y=${r.y} rgba(${p.r},${p.g},${p.b},${p.a})`);
}
