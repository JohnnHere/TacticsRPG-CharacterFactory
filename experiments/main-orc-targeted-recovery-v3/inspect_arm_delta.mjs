import fs from 'node:fs';
import path from 'node:path';
import { decode } from '../../src/images.mjs';

const ROOT = process.cwd();

function inspectSilhouetteDelta(dir) {
  console.log(`\n=== Silhouette Delta for ${dir}/Walk ===`);
  const clipDir = path.resolve(ROOT, `characters/orc-v1/source/rear-recovery-v2/${dir}/Walk`);
  const imgs = [];
  for (let f = 0; f < 8; f++) {
    imgs.push(decode(path.join(clipDir, `${String(f).padStart(2, '0')}.png`)).image);
  }
  for (let f = 0; f < 8; f++) {
    const fNext = (f + 1) % 8;
    const im1 = imgs[f], im2 = imgs[fNext];
    // Compare in left arm region (x: 80..115, y: 70..140)
    let added = 0, removed = 0, changedColor = 0;
    for (let y = 70; y <= 140; y++) {
      for (let x = 80; x <= 115; x++) {
        const idx = (y * 256 + x) * 4;
        const a1 = im1.data[idx + 3], a2 = im2.data[idx + 3];
        if (a1 === 0 && a2 > 0) added++;
        else if (a1 > 0 && a2 === 0) removed++;
        else if (a1 > 0 && a2 > 0) {
          if (im1.data[idx] !== im2.data[idx] || im1.data[idx+1] !== im2.data[idx+1] || im1.data[idx+2] !== im2.data[idx+2]) {
            changedColor++;
          }
        }
      }
    }
    console.log(`F${f} -> F${fNext}: added=${added} px, removed=${removed} px, changedColor=${changedColor} px`);
  }
}

inspectSilhouetteDelta('back_r');
inspectSilhouetteDelta('back_l');
