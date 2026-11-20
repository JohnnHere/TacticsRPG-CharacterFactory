import fs from 'node:fs';
import path from 'node:path';
import { decode } from '../../src/images.mjs';

const ROOT = process.cwd();

function inspectDefeats() {
  const dirs = [
    'characters/orc-v1/source/complete-v1/back_r/Defeat',
    'characters/orc-v1/source/rear-recovery-v2/front_r/Defeat'
  ];
  for (const d of dirs) {
    console.log(`\n=== Defeat: ${d} ===`);
    const p = path.resolve(ROOT, d);
    for (let f = 0; f < 5; f++) {
      const imP = path.join(p, `${String(f).padStart(2, '0')}.png`);
      const img = decode(imP).image;
      let minX = 256, maxX = 0, minY = 256, maxY = 0;
      for (let y = 0; y < 256; y++) {
        for (let x = 0; x < 256; x++) {
          if (img.data[(y * 256 + x) * 4 + 3] > 0) {
            if (x < minX) minX = x;
            if (x > maxX) maxX = x;
            if (y < minY) minY = y;
            if (y > maxY) maxY = y;
          }
        }
      }
      console.log(`Frame ${f}: bbox=[${minX},${minY} ${maxX-minX+1}x${maxY-minY+1}] (ground at maxY=${maxY})`);
    }
  }
}

inspectDefeats();
