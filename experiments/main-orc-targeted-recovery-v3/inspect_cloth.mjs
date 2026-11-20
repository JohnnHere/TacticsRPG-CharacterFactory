import fs from 'node:fs';
import path from 'node:path';
import { decode } from '../../src/images.mjs';

const ROOT = process.cwd();

function inspectClothShading() {
  const dir = path.resolve(ROOT, 'characters/orc-v1/source/complete-v1/front_r/Walk');
  console.log("=== Inspecting front_r/Walk cloth shading between legs ===");
  // Crotch/cloth tabard area is between x: 110..145, y: 120..155
  for (let f = 0; f < 16; f++) {
    const p = path.join(dir, `${String(f).padStart(2, '0')}.png`);
    const img = decode(p).image;
    // Check pixels in tabard/cloth area between thighs (x: 120..136, y: 130..150)
    let colors = new Set();
    for (let y = 132; y <= 148; y++) {
      for (let x = 122; x <= 134; x++) {
        const idx = (y * 256 + x) * 4;
        if (img.data[idx + 3] > 0) {
          const r = img.data[idx], g = img.data[idx+1], b = img.data[idx+2];
          colors.add(`${r},${g},${b}`);
        }
      }
    }
    // console.log(`Frame ${f}: distinct colors in cloth area=${colors.size}`);
  }
  // Let's print the colors for Frame 08 (which had a bright pixel in diag: f08 1px/1cl)
  const p8 = path.join(dir, '08.png');
  const img8 = decode(p8).image;
  // Diag noted: front_r/Walk f08 1px/1cl bright-edge suspect peak
  // Let's check where that 1px is in Frame 8!
  for (let y = 0; y < 256; y++) {
    for (let x = 0; x < 256; x++) {
      const idx = (y * 256 + x) * 4;
      if (img8.data[idx + 3] > 0) {
        const r = img8.data[idx], g = img8.data[idx+1], b = img8.data[idx+2];
        const lum = Math.round(0.299 * r + 0.587 * g + 0.114 * b);
        if (lum >= 200) {
          console.log(`Frame 08 bright pixel at (${x}, ${y}): rgba(${r},${g},${b},${img8.data[idx+3]}) luma=${lum}`);
        }
      }
    }
  }
}

inspectClothShading();
