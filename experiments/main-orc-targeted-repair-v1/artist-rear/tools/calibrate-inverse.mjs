#!/usr/bin/env node
// Calibrate the weapon placement inverse for a clip: finds the integer sprite-space
// anchor offset that maximises colour agreement between the sprite and the composite at
// the pixels the weapon layer covers. Proves the band audit uses the real transform.
// Usage: node calibrate-inverse.mjs <clip.json> <weapon.png> <guessX,guessY>
import fs from 'node:fs';
import { PNG } from 'pngjs';

const [, , clipArg, weaponArg, guessArg] = process.argv;
const clip = JSON.parse(fs.readFileSync(clipArg, 'utf8'));
const weapon = PNG.sync.read(fs.readFileSync(weaponArg));
const [g0x, g0y] = guessArg.split(',').map(Number);
const read = (p) => PNG.sync.read(fs.readFileSync(p));
const A = (img, x, y) => img.data[(y * img.width + x) * 4 + 3];

const samples = [];
for (const f of clip.frames) {
  if (!f.weaponVisible) continue;
  const wf = read(f.layers.weaponFront.png);
  const comp = read(f.png);
  const [gx, gy] = f.rightGrip;
  for (let y = 0; y < comp.height; y += 1) {
    for (let x = 0; x < comp.width; x += 1) {
      if (!A(wf, x, y)) continue;
      const s = (y * comp.width + x) * 4;
      samples.push({ x, y, gx, gy, angle: f.rotationDeg, r: comp.data[s], g: comp.data[s + 1], b: comp.data[s + 2] });
    }
  }
}
console.log(`samples=${samples.length}`);

const score = (ax, ay) => {
  let hit = 0;
  for (const sp of samples) {
    const r = (sp.angle * Math.PI) / 180;
    const cos = Math.cos(r);
    const sin = Math.sin(r);
    const dx = sp.x - sp.gx;
    const dy = sp.y - sp.gy;
    const u = Math.floor(cos * dx + sin * dy + ax + 0.5);
    const v = Math.floor(-sin * dx + cos * dy + ay + 0.5);
    if (u < 0 || v < 0 || u >= weapon.width || v >= weapon.height) continue;
    const ws = (v * weapon.width + u) * 4;
    if (weapon.data[ws + 3] < 128) continue;
    if (weapon.data[ws] === sp.r && weapon.data[ws + 1] === sp.g && weapon.data[ws + 2] === sp.b) hit += 1;
  }
  return hit;
};

let best = { ax: g0x, ay: g0y, hit: -1 };
for (let ax = g0x - 10; ax <= g0x + 10; ax += 1) {
  for (let ay = g0y - 10; ay <= g0y + 10; ay += 1) {
    const hit = score(ax, ay);
    if (hit > best.hit) best = { ax, ay, hit };
  }
}
console.log(`best anchor=${best.ax},${best.ay} colourAgreement=${best.hit}/${samples.length} (${((best.hit / samples.length) * 100).toFixed(1)}%)`);
