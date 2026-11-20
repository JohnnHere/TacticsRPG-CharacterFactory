import fs from 'node:fs';
import path from 'node:path';
import { decode } from '../../src/images.mjs';

const ROOT = process.cwd();

function inspectRawUnarmedR() {
  const dir = path.resolve(ROOT, 'experiments/main-orc-rear-recovery-v2/raw/frames_unarmed_r');
  console.log(`=== Inspecting raw frames_unarmed_r ===`);
  for (let i = 0; i <= 8; i++) {
    const p = path.join(dir, `frame_${String(i).padStart(2, '0')}.png`);
    if (!fs.existsSync(p)) continue;
    const img = decode(p).image;
    // Find bounding box
    let minX = 128, maxX = 0, minY = 128, maxY = 0;
    for (let y = 0; y < 128; y++) {
      for (let x = 0; x < 128; x++) {
        if (img.data[(y * 128 + x) * 4 + 3] > 0) {
          if (x < minX) minX = x;
          if (x > maxX) maxX = x;
          if (y < minY) minY = y;
          if (y > maxY) maxY = y;
        }
      }
    }
    console.log(`Raw Frame ${i}: bbox=[${minX},${minY} ${maxX-minX+1}x${maxY-minY+1}]`);
  }
}

inspectRawUnarmedR();
