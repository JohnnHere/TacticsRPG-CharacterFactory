import fs from 'node:fs';
import path from 'node:path';
import { decode } from '../../src/images.mjs';

const ROOT = process.cwd();

function checkFistBackR() {
  const dir = path.resolve(ROOT, 'characters/orc-v1/source/rear-recovery-v2/back_r/Unarmed');
  console.log(`=== Inspecting back_r/Unarmed frames ===`);
  for (let i = 0; i < 5; i++) {
    const p = path.join(dir, `${String(i).padStart(2, '0')}.png`);
    const img = decode(p).image;
    // Look at right side of character (x > 140 in 256 canvas, or x > 76 in 128 canvas)
    let minX = 256, maxX = 0, minY = 256, maxY = 0, count = 0;
    // Let's find outermost pixels on the right side
    let rightmost = [];
    for (let y = 60; y < 190; y++) {
      for (let x = 140; x < 256; x++) {
        const a = img.data[(y * 256 + x) * 4 + 3];
        if (a > 0) {
          count++;
          if (x > maxX) maxX = x;
          if (x < minX) minX = x;
          if (y > maxY) maxY = y;
          if (y < minY) minY = y;
          rightmost.push({ x, y });
        }
      }
    }
    console.log(`Frame ${i}: right pixels count=${count}, x=[${minX}..${maxX}], y=[${minY}..${maxY}]`);
  }
}

checkFistBackR();
