import fs from 'node:fs';
import path from 'node:path';
import { decode } from '../../src/images.mjs';

const ROOT = process.cwd();

function inspectFrame3Region() {
  const p = path.resolve(ROOT, 'characters/orc-v1/source/complete-v1/front_l/Sword/Attack/layers/body/03.png');
  const img = decode(p).image;
  console.log("=== Frame 3 Body around armpit (x: 155..175, y: 88..105) ===");
  for (let y = 88; y <= 105; y++) {
    let line = `${String(y).padStart(3, '0')}: `;
    for (let x = 155; x <= 175; x++) {
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

inspectFrame3Region();
