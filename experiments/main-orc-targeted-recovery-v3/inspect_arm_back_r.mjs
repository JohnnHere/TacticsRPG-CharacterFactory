import fs from 'node:fs';
import path from 'node:path';
import { decode } from '../../src/images.mjs';

const ROOT = process.cwd();

function checkFramesDetail() {
  const dir = path.resolve(ROOT, 'characters/orc-v1/source/rear-recovery-v2/back_r/Unarmed');
  console.log("=== back_r Unarmed Detailed Frame Inspection ===");
  for (let i = 0; i < 5; i++) {
    const p = path.join(dir, `${String(i).padStart(2, '0')}.png`);
    const img = decode(p).image;
    // Inspect right arm area (x: 150..200, y: 80..140 in 256 canvas)
    let pixels = [];
    for (let y = 80; y <= 140; y++) {
      for (let x = 150; x <= 200; x++) {
        const idx = (y * 256 + x) * 4;
        const a = img.data[idx + 3];
        if (a > 0) {
          pixels.push({ x, y, r: img.data[idx], g: img.data[idx+1], b: img.data[idx+2] });
        }
      }
    }
    let minX = 256, maxX = 0, minY = 256, maxY = 0;
    for (const px of pixels) {
      if (px.x < minX) minX = px.x;
      if (px.x > maxX) maxX = px.x;
      if (px.y < minY) minY = px.y;
      if (px.y > maxY) maxY = px.y;
    }
    console.log(`Frame ${i}: arm/fist pixels=${pixels.length}, bbox=[${minX},${minY} .. ${maxX},${maxY}]`);
  }
}

checkFramesDetail();
