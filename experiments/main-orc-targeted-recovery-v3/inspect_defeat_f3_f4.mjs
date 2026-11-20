import fs from 'node:fs';
import path from 'node:path';
import { decode } from '../../src/images.mjs';

const ROOT = process.cwd();

function inspectDefeatF3F4() {
  const p3 = path.resolve(ROOT, 'characters/orc-v1/source/rear-recovery-v2/front_r/Defeat/03.png');
  const p4 = path.resolve(ROOT, 'characters/orc-v1/source/rear-recovery-v2/front_r/Defeat/04.png');
  const im3 = decode(p3).image;
  const im4 = decode(p4).image;
  
  console.log("F03 collapse impact:");
  for (let y = 125; y <= 190; y += 5) {
    let minX = 256, maxX = 0;
    for (let x = 60; x < 200; x++) {
      if (im3.data[(y * 256 + x) * 4 + 3] > 0) {
        if (x < minX) minX = x;
        if (x > maxX) maxX = x;
      }
    }
    if (maxX >= minX) console.log(`  y=${y}: x=[${minX}..${maxX}] w=${maxX-minX+1}`);
  }
  
  console.log("Current F04 terminal:");
  for (let y = 125; y <= 190; y += 5) {
    let minX = 256, maxX = 0;
    for (let x = 60; x < 200; x++) {
      if (im4.data[(y * 256 + x) * 4 + 3] > 0) {
        if (x < minX) minX = x;
        if (x > maxX) maxX = x;
      }
    }
    if (maxX >= minX) console.log(`  y=${y}: x=[${minX}..${maxX}] w=${maxX-minX+1}`);
  }
}

inspectDefeatF3F4();
