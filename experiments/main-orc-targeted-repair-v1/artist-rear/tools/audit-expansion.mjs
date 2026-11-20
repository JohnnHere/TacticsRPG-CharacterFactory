#!/usr/bin/env node
// QA-only semantic audit of the handFront expansion.
// For every pixel the candidate added, invert the weapon placement transform to the
// weapon sprite's own space and report which part of the weapon it hides:
// blade / guard / grip / pommel. Self-validates the inverse by comparing the recovered
// sprite colour with the baseline composite colour at that pixel.
// Usage: node audit-expansion.mjs <clip.json> <weapon.png> <gx0,gy0> <anglePerFrame...>
import fs from 'node:fs';
import { PNG } from 'pngjs';

const [, , clipArg, weaponArg, anchorArg, anglesArg] = process.argv;
const clip = JSON.parse(fs.readFileSync(clipArg, 'utf8'));
const weapon = PNG.sync.read(fs.readFileSync(weaponArg));
const [ax, ay] = anchorArg.split(',').map(Number);
const read = (p) => PNG.sync.read(fs.readFileSync(p));
const A = (img, x, y) => img.data[(y * img.width + x) * 4 + 3];

const baseDir = process.env.BASELINE_DIR;
const candDir = process.env.CANDIDATE_DIR;
const angles = anglesArg.split(',').map(Number);
const bands = { blade: [0, 54], guard: [55, 59], grip: [60, 70], pommel: [71, 90] };
const bandOf = (v) => Object.entries(bands).find(([, r]) => v >= r[0] && v <= r[1])?.[0] ?? 'outside';

const totals = {};
for (let i = 0; i < 8; i += 1) {
  const b = read(`${baseDir}/${String(i).padStart(2, '0')}.png`);
  const c = read(`${candDir}/${String(i).padStart(2, '0')}.png`);
  const angle = angles[i];
  const changed = [];
  for (let y = 0; y < b.height; y += 1) {
    for (let x = 0; x < b.width; x += 1) {
      const s = (y * b.width + x) * 4;
      if (b.data[s] !== c.data[s] || b.data[s + 1] !== c.data[s + 1] || b.data[s + 2] !== c.data[s + 2] || b.data[s + 3] !== c.data[s + 3]) changed.push([x, y]);
    }
  }
  if (!changed.length) {
    console.log(`f${i}: no composite change`);
    continue;
  }
  const [gx, gy] = clip.frames[i].rightGrip;
  const r = (angle * Math.PI) / 180;
  const cos = Math.cos(r);
  const sin = Math.sin(r);
  const rows = [];
  let validated = 0;
  for (const [x, y] of changed) {
    const dx = x - gx;
    const dy = y - gy;
    const u = Math.floor(cos * dx + sin * dy + ax + 0.5);
    const v = Math.floor(-sin * dx + cos * dy + ay + 0.5);
    const inSprite = u >= 0 && v >= 0 && u < weapon.width && v < weapon.height;
    let matches = false;
    if (inSprite && A(weapon, u, v) >= 128) {
      const ws = (v * weapon.width + u) * 4;
      const bs = (y * b.width + x) * 4;
      matches = weapon.data[ws] === b.data[bs] && weapon.data[ws + 1] === b.data[bs + 1] && weapon.data[ws + 2] === b.data[bs + 2];
    }
    if (matches) validated += 1;
    rows.push({ x, y, u, v, band: bandOf(v), inSprite, matches });
  }
  const byBand = {};
  for (const row of rows) byBand[row.band] = (byBand[row.band] ?? 0) + 1;
  for (const [k, n] of Object.entries(byBand)) totals[k] = (totals[k] ?? 0) + n;
  console.log(
    `f${i} angle=${angle} changed=${changed.length} inverseValidated=${validated}/${changed.length} bands=${JSON.stringify(byBand)}`,
  );
  const odd = rows.filter((row) => !row.matches).slice(0, 8);
  if (odd.length) console.log('   unresolved samples:', JSON.stringify(odd));
}
console.log(`TOTAL by band: ${JSON.stringify(totals)}`);
