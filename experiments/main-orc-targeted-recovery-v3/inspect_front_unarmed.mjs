import fs from 'node:fs';
import path from 'node:path';
import { decode } from '../../src/images.mjs';

const ROOT = process.cwd();

function checkFrontUnarmed(dirName) {
  const dir = path.resolve(ROOT, `characters/orc-v1/source/rear-recovery-v2/${dirName}/Unarmed`);
  console.log(`\n=== Inspecting ${dirName}/Unarmed ===`);
  for (let i = 0; i < 5; i++) {
    const p = path.join(dir, `${String(i).padStart(2, '0')}.png`);
    const img = decode(p).image;
    // On front_r: punching arm is right arm (image-left/center). Opposite arm is left arm (image-right).
    // Let's inspect both sides of the character (image-left: x < 128, image-right: x > 128)
    let leftPixels = 0, rightPixels = 0;
    let leftBbox = [256, 256, 0, 0], rightBbox = [256, 256, 0, 0];
    for (let y = 60; y < 190; y++) {
      for (let x = 60; x < 200; x++) {
        const a = img.data[(y * 256 + x) * 4 + 3];
        if (a > 0) {
          if (x < 128) {
            leftPixels++;
            if (x < leftBbox[0]) leftBbox[0] = x;
            if (x > leftBbox[2]) leftBbox[2] = x;
            if (y < leftBbox[1]) leftBbox[1] = y;
            if (y > leftBbox[3]) leftBbox[3] = y;
          } else {
            rightPixels++;
            if (x < rightBbox[0]) rightBbox[0] = x;
            if (x > rightBbox[2]) rightBbox[2] = x;
            if (y < rightBbox[1]) rightBbox[1] = y;
            if (y > rightBbox[3]) rightBbox[3] = y;
          }
        }
      }
    }
    console.log(`Frame ${i}: left(x<128) px=${leftPixels} bbox=[${leftBbox[0]},${leftBbox[1]}..${leftBbox[2]},${leftBbox[3]}] | right(x>=128) px=${rightPixels} bbox=[${rightBbox[0]},${rightBbox[1]}..${rightBbox[2]},${rightBbox[3]}]`);
  }
}

checkFrontUnarmed('front_r');
checkFrontUnarmed('front_l');
