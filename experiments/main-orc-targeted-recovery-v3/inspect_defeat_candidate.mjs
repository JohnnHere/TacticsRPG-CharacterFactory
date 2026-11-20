import fs from 'node:fs';
import path from 'node:path';
import { decode } from '../../src/images.mjs';

const ROOT = process.cwd();

function checkDefeatCandidate() {
  const p = path.resolve(ROOT, 'experiments/main-orc-rear-recovery-v2/raw/defeat_front_r_04_candidate.png');
  const img = decode(p).image;
  console.log(`defeat_front_r_04_candidate: size=${img.width}x${img.height}`);
  let minX = img.width, maxX = 0, minY = img.height, maxY = 0;
  for (let y = 0; y < img.height; y++) {
    for (let x = 0; x < img.width; x++) {
      if (img.data[(y * img.width + x) * 4 + 3] > 0) {
        if (x < minX) minX = x;
        if (x > maxX) maxX = x;
        if (y < minY) minY = y;
        if (y > maxY) maxY = y;
      }
    }
  }
  console.log(`bbox: [${minX}, ${minY} ${maxX-minX+1}x${maxY-minY+1}]`);
}

checkDefeatCandidate();
