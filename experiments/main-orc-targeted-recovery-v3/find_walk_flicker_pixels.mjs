import fs from 'node:fs';
import path from 'node:path';
import { decode } from '../../src/images.mjs';

const ROOT = process.cwd();

function analyzeWalkArmFlicker(dir) {
  const clipDir = path.resolve(ROOT, `characters/orc-v1/source/rear-recovery-v2/${dir}/Walk`);
  console.log(`\n=== Detailed Left Arm Flicker Analysis: ${dir}/Walk ===`);
  const imgs = [];
  for (let f = 0; f < 8; f++) {
    imgs.push(decode(path.join(clipDir, `${String(f).padStart(2, '0')}.png`)).image);
  }
  
  // Track each (x, y) pixel in left arm box (x: 85..115, y: 75..145)
  // Check for pixels that turn ON and OFF and ON (flicker)
  for (let y = 75; y <= 145; y++) {
    for (let x = 85; x <= 115; x++) {
      let pattern = '';
      for (let f = 0; f < 8; f++) {
        const a = imgs[f].data[(y * 256 + x) * 4 + 3];
        pattern += a > 0 ? '1' : '0';
      }
      // A flicker pattern is when it changes more than 2 times in 8 frames (e.g., 0101, 1010, or isolated 1)
      const transitions = (pattern.match(/01/g) || []).length + (pattern.match(/10/g) || []).length;
      if (transitions >= 3 || pattern === '00010000' || pattern === '00001000' || pattern === '11101111') {
        console.log(`Flicker pixel at (${x}, ${y}): pattern=${pattern}`);
      }
    }
  }
}

analyzeWalkArmFlicker('back_r');
analyzeWalkArmFlicker('back_l');
