import fs from 'node:fs';
import path from 'node:path';
import { decode } from '../../src/images.mjs';

const ROOT = process.cwd();

function checkWalkArms(dirName) {
  const dir = path.resolve(ROOT, `characters/orc-v1/source/rear-recovery-v2/${dirName}/Walk`);
  console.log(`\n=== Inspecting ${dirName}/Walk (left arm & right arm) ===`);
  for (let i = 0; i < 8; i++) {
    const p = path.join(dir, `${String(i).padStart(2, '0')}.png`);
    const img = decode(p).image;
    // Left arm (image-left x < 128) vs Right arm (image-right x >= 128)
    // Specifically looking at arm height range y: 80..150
    let leftArmPx = 0, rightArmPx = 0;
    let leftBbox = [256, 256, 0, 0], rightBbox = [256, 256, 0, 0];
    for (let y = 80; y <= 150; y++) {
      for (let x = 60; x <= 196; x++) {
        const a = img.data[(y * 256 + x) * 4 + 3];
        if (a > 0) {
          if (x < 128) {
            leftArmPx++;
            if (x < leftBbox[0]) leftBbox[0] = x;
            if (x > leftBbox[2]) leftBbox[2] = x;
            if (y < leftBbox[1]) leftBbox[1] = y;
            if (y > leftBbox[3]) leftBbox[3] = y;
          } else {
            rightArmPx++;
            if (x < rightBbox[0]) rightBbox[0] = x;
            if (x > rightBbox[2]) rightBbox[2] = x;
            if (y < rightBbox[1]) rightBbox[1] = y;
            if (y > rightBbox[3]) rightBbox[3] = y;
          }
        }
      }
    }
    console.log(`Frame ${i}: left(x<128) px=${leftArmPx} bbox=[${leftBbox[0]},${leftBbox[1]}..${leftBbox[2]},${leftBbox[3]}] | right(x>=128) px=${rightArmPx} bbox=[${rightBbox[0]},${rightBbox[1]}..${rightBbox[2]},${rightBbox[3]}]`);
  }
}

checkWalkArms('back_r');
checkWalkArms('back_l');
