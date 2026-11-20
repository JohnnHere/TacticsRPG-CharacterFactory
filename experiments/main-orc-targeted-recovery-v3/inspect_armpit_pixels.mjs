import fs from 'node:fs';
import path from 'node:path';
import { decode } from '../../src/images.mjs';

const ROOT = process.cwd();

function inspectArmpitPixels() {
  const dir = path.resolve(ROOT, 'characters/orc-v1/source/complete-v1/front_l/Sword/Attack/layers/body');
  for (let f = 0; f < 13; f++) {
    const p = path.join(dir, `${String(f).padStart(2, '0')}.png`);
    if (!fs.existsSync(p)) continue;
    const img = decode(p).image;
    // Inspect around the attacking arm (in front_l, the attacking right arm swings on the right or left?
    // front_l looks SW, right arm is on image-right/back, swinging forward to image-left).
    // Let's look for isolated pixels (pixels with alpha > 0 where most 8-neighbors have alpha == 0)
    const isolated = [];
    for (let y = 60; y < 150; y++) {
      for (let x = 80; x < 180; x++) {
        const idx = (y * 256 + x) * 4;
        if (img.data[idx + 3] === 0) continue;
        let opaqueNeighbors = 0;
        for (let dy = -1; dy <= 1; dy++) {
          for (let dx = -1; dx <= 1; dx++) {
            if (dx === 0 && dy === 0) continue;
            const nx = x + dx, ny = y + dy;
            if (img.data[(ny * 256 + nx) * 4 + 3] > 0) opaqueNeighbors++;
          }
        }
        if (opaqueNeighbors <= 2) {
          isolated.push({ x, y, r: img.data[idx], g: img.data[idx+1], b: img.data[idx+2], a: img.data[idx+3], neighbors: opaqueNeighbors });
        }
      }
    }
    if (isolated.length > 0) {
      console.log(`Frame ${f}: ${isolated.length} isolated/thin pixels in arm/torso area:`);
      for (const ip of isolated) {
        console.log(`  (${ip.x}, ${ip.y}): rgba(${ip.r},${ip.g},${ip.b},${ip.a}) neighbors=${ip.neighbors}`);
      }
    }
  }
}

inspectArmpitPixels();
