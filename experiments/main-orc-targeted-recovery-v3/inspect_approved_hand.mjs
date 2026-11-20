import fs from 'node:fs';
import path from 'node:path';
import { decode } from '../../src/images.mjs';

const ROOT = process.cwd();

function inspectApprovedHandFront() {
  const dir = path.resolve(ROOT, 'characters/orc-v1/source/complete-v1/front_r/Sword/Attack/layers/handFront');
  console.log("=== Inspecting APPROVED front_r/Sword/Attack handFront ===");
  for (let f = 0; f < 13; f++) {
    const p = path.join(dir, `${String(f).padStart(2, '0')}.png`);
    if (!fs.existsSync(p)) continue;
    const img = decode(p).image;
    let minX = 256, maxX = 0, minY = 256, maxY = 0, count = 0;
    for (let y = 0; y < 256; y++) {
      for (let x = 0; x < 256; x++) {
        if (img.data[(y * 256 + x) * 4 + 3] > 0) {
          count++;
          if (x < minX) minX = x;
          if (x > maxX) maxX = x;
          if (y < minY) minY = y;
          if (y > maxY) maxY = y;
        }
      }
    }
    if (count > 0) {
      console.log(`Frame ${f}: handFront px=${count} bbox=[${minX},${minY} ${maxX-minX+1}x${maxY-minY+1}]`);
    } else {
      console.log(`Frame ${f}: handFront empty`);
    }
  }
}

inspectApprovedHandFront();
