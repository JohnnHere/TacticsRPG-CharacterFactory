#!/usr/bin/env node
// QA-only: ASCII map of a region showing layer occupancy and composite luminance class.
// Usage: node ascii.mjs <clip.json> <frame> <x0,y0,w,h>
// chars: '.' empty, '#' ink(L<20), '+' dark(L<60), '-' mid(L<100), '=' light(L<160), '@' bright
// two maps: composite classes, then layer occupancy (B body, F weaponFront, K weaponBack, H handFront)
import fs from 'node:fs';
import { PNG } from 'pngjs';

const [, , clipArg, iArg, boxArg] = process.argv;
const clip = JSON.parse(fs.readFileSync(clipArg, 'utf8'));
const f = clip.frames[Number(iArg)];
const [x0, y0, bw, bh] = boxArg.split(',').map(Number);
const read = (p) => PNG.sync.read(fs.readFileSync(p));
const layers = {
  K: read(f.layers.weaponBack.png),
  B: read(f.layers.body.png),
  F: read(f.layers.weaponFront.png),
  H: read(f.layers.handFront.png),
};
const comp = read(f.png);
const lum = (r, g, b) => 0.2126 * r + 0.7152 * g + 0.0722 * b;
const cls = (l) => (l < 20 ? '#' : l < 60 ? '+' : l < 100 ? '-' : l < 160 ? '=' : '@');
const a = (img, x, y) => img.data[(y * img.width + x) * 4 + 3];
let hdr = '    ';
for (let x = x0; x < x0 + bw; x += 1) hdr += String(x % 10);
console.log(`frame=${iArg} composite classes (L buckets)`);
console.log(hdr);
for (let y = y0; y < y0 + bh; y += 1) {
  let row = `${String(y).padStart(3)} `;
  for (let x = x0; x < x0 + bw; x += 1) {
    if (!a(comp, x, y)) {
      row += '.';
      continue;
    }
    const s = (y * comp.width + x) * 4;
    row += cls(lum(comp.data[s], comp.data[s + 1], comp.data[s + 2]));
  }
  console.log(row);
}
console.log('\nlayer occupancy (topmost of H,F,B,K = one letter, lowercase when 2+ layers)');
console.log(hdr);
for (let y = y0; y < y0 + bh; y += 1) {
  let row = `${String(y).padStart(3)} `;
  for (let x = x0; x < x0 + bw; x += 1) {
    const present = ['H', 'F', 'B', 'K'].filter((k) => a(layers[k], x, y));
    if (!present.length) row += '.';
    else if (present.length === 1) row += present[0];
    else row += present[0].toLowerCase();
  }
  console.log(row);
}
