import fs from 'node:fs';
import path from 'node:path';
import { decode } from '../../src/images.mjs';

const ROOT = process.cwd();

function checkWalkFlicker(dir) {
  console.log(`\n======================================================`);
  console.log(`INSPECTING LEFT ARM IN: ${dir}/Walk`);
  const clipDir = path.resolve(ROOT, `characters/orc-v1/source/rear-recovery-v2/${dir}/Walk`);
  
  for (let f = 0; f < 8; f++) {
    const p = path.join(clipDir, `${String(f).padStart(2, '0')}.png`);
    const img = decode(p).image;
    // Focus on the left arm region (x: 80..110, y: 70..140 in 256 canvas)
    let armPixels = [];
    for (let y = 70; y <= 140; y++) {
      for (let x = 80; x <= 110; x++) {
        const idx = (y * 256 + x) * 4;
        if (img.data[idx + 3] > 0) {
          armPixels.push({ x, y, r: img.data[idx], g: img.data[idx+1], b: img.data[idx+2] });
        }
      }
    }
    // Also check pauldron/shoulder at y: 70..95 and lower arm at y: 96..140
    const upper = armPixels.filter(p => p.y <= 95);
    const lower = armPixels.filter(p => p.y > 95);
    const minX = lower.length ? Math.min(...lower.map(p => p.x)) : -1;
    const maxX = lower.length ? Math.max(...lower.map(p => p.x)) : -1;
    const minY = lower.length ? Math.min(...lower.map(p => p.y)) : -1;
    const maxY = lower.length ? Math.max(...lower.map(p => p.y)) : -1;
    console.log(`Frame ${f}: lower arm pixels=${lower.length} bbox=[${minX}..${maxX}, ${minY}..${maxY}] (upper shoulder px=${upper.length})`);
  }
}

checkWalkFlicker('back_r');
checkWalkFlicker('back_l');
