import fs from 'node:fs';
import path from 'node:path';
import { decode } from '../../src/images.mjs';

const ROOT = process.cwd();

function inspectUnarmedBackL() {
  const dir = path.resolve(ROOT, 'characters/orc-v1/source/rear-recovery-v2/back_l/Unarmed');
  const clip = JSON.parse(fs.readFileSync(path.join(dir, 'clip.json'), 'utf8').replace(/^\uFEFF/, ''));
  console.log(`=== back_l/Unarmed ===`);
  console.log(`Frames: ${clip.frames.length}`);
  
  const imgs = [];
  for (let i = 0; i < clip.frames.length; i++) {
    const f = clip.frames[i];
    const p = path.resolve(ROOT, f.png || f.file);
    const dec = decode(p);
    imgs.push(dec.image);
    console.log(`Frame ${i}: dur=${f.durationMs || f.duration}ms phase=${f.phase || ''}`);
  }

  // Compare delta between each pair
  for (let i = 0; i < imgs.length; i++) {
    for (let j = i + 1; j < imgs.length; j++) {
      let diffCount = 0;
      const im1 = imgs[i], im2 = imgs[j];
      for (let k = 0; k < im1.data.length; k += 4) {
        if (im1.data[k] !== im2.data[k] ||
            im1.data[k+1] !== im2.data[k+1] ||
            im1.data[k+2] !== im2.data[k+2] ||
            im1.data[k+3] !== im2.data[k+3]) {
          diffCount++;
        }
      }
      const pct = (diffCount / (im1.width * im1.height) * 100).toFixed(2);
      console.log(`  Delta F${i} -> F${j}: ${diffCount} px (${pct}%)`);
    }
  }
}

inspectUnarmedBackL();
