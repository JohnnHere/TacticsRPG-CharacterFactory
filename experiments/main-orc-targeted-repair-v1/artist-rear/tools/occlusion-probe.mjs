#!/usr/bin/env node
// QA-only: measure hand occlusion. For each weapon-visible frame, count body (hand)
// pixels near the declared grip that are covered by the weapon layer and NOT restored
// by handFront. Those are the pixels where the handle is painted over the fist.
// Usage: node occlusion-probe.mjs <clip.json> [radius=7]
import fs from 'node:fs';
import { PNG } from 'pngjs';

const [, , clipArg, radiusArg = '7'] = process.argv;
const radius = Number(radiusArg);
const clip = JSON.parse(fs.readFileSync(clipArg, 'utf8'));
const read = (p) => PNG.sync.read(fs.readFileSync(p));
const opaque = (img, x, y) =>
  x >= 0 && y >= 0 && x < img.width && y < img.height && img.data[(y * img.width + x) * 4 + 3] > 0;

console.log(`clip=${clipArg} radius=${radius}`);
for (const f of clip.frames) {
  if (!f.weaponVisible) {
    console.log(`f${f.index} unarmed`);
    continue;
  }
  const body = read(f.layers.body.png);
  const wf = read(f.layers.weaponFront.png);
  const wb = read(f.layers.weaponBack.png);
  const hf = read(f.layers.handFront.png);
  const [gx, gy] = f.rightGrip;
  let hand = 0;
  let covered = 0;
  let restored = 0;
  let missing = 0;
  const missingPx = [];
  for (let dy = -radius; dy <= radius; dy += 1) {
    for (let dx = -radius; dx <= radius; dx += 1) {
      if (dx * dx + dy * dy > radius * radius) continue;
      const x = gx + dx;
      const y = gy + dy;
      if (!opaque(body, x, y)) continue;
      hand += 1;
      const wCover = opaque(wf, x, y) || opaque(wb, x, y);
      if (!wCover) continue;
      covered += 1;
      if (opaque(hf, x, y)) restored += 1;
      else {
        missing += 1;
        missingPx.push(`${x},${y}`);
      }
    }
  }
  console.log(
    `f${f.index} grip=${gx},${gy} handPx=${hand} coveredByWeapon=${covered} restoredByHandFront=${restored} STILL_COVERED=${missing} ${missingPx.slice(0, 12).join(' ')}`,
  );
}
