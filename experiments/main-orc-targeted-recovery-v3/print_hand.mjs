import fs from 'node:fs';
import path from 'node:path';
import { decode } from '../../src/images.mjs';

const ROOT = process.cwd();

function printHandPixels() {
  const p = path.resolve(ROOT, 'characters/orc-v1/source/complete-v1/front_r/Sword/Attack/layers/handFront/04.png');
  const img = decode(p).image;
  console.log("=== front_r/Sword/Attack handFront frame 4 pixels ===");
  for (let y = 94; y <= 106; y++) {
    let line = `${String(y).padStart(3, '0')}: `;
    for (let x = 92; x <= 105; x++) {
      const idx = (y * 256 + x) * 4;
      const a = img.data[idx + 3];
      if (a === 0) line += ' . ';
      else {
        const r = img.data[idx], g = img.data[idx+1], b = img.data[idx+2];
        line += `${Math.round((r+g+b)/3).toString(16).padStart(2,'0')} `;
      }
    }
    console.log(line);
  }
}

printHandPixels();
