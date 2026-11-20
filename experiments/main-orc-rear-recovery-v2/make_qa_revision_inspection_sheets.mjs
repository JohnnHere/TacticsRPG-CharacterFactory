// QA-only nearest-neighbor crops from canonical body-layer PNGs; no source art is changed.
import fs from 'node:fs';
import path from 'node:path';
import { PNG } from 'pngjs';
import { ROOT } from '../../src/core.mjs';
import { decode } from '../../src/images.mjs';

const out = path.join(ROOT, 'experiments/main-orc-rear-recovery-v2/E/qa-revision-1-inspection');
const scale = 3, cellW = 256 * scale, cellH = 256 * scale;
fs.mkdirSync(out, { recursive: true });
function sheet(key, direction, action, indices) {
  const width = cellW * 4, height = cellH * 2, dst = new PNG({ width, height });
  const srcDir = `characters/orc-v1/source/rear-recovery-v2/${direction}/${action}/Attack-representative-v1/layers/body`;
  for (let i = 0; i < indices.length; i++) {
    const n = String(indices[i]).padStart(2, '0'), src = decode(path.join(ROOT, `${srcDir}/${n}.png`)).image;
    const ox = (i % 4) * cellW, oy = Math.floor(i / 4) * cellH;
    for (let y = 0; y < 256; y++) for (let x = 0; x < 256; x++) {
      const si = (y * 256 + x) * 4, alpha = src.data[si + 3];
      const bg = ((Math.floor(x / 8) + Math.floor(y / 8)) % 2) ? 80 : 108;
      for (let sy = 0; sy < scale; sy++) for (let sx = 0; sx < scale; sx++) {
        const di = ((oy + y * scale + sy) * width + ox + x * scale + sx) * 4;
        if (alpha) {
          const a = alpha / 255;
          for (let c = 0; c < 3; c++) dst.data[di + c] = Math.round(src.data[si + c] * a + bg * (1 - a));
        } else dst.data[di] = dst.data[di + 1] = dst.data[di + 2] = bg;
        dst.data[di + 3] = 255;
      }
    }
  }
  fs.writeFileSync(path.join(out, `${key}-body-3x.png`), PNG.sync.write(dst));
}
sheet('swordL', 'back_l', 'Sword', [0,1,2,3,4,5,6,7]);
sheet('axeR', 'back_r', 'Axe', [0,1,2,3,4,5,6,7]);
sheet('axeL', 'back_l', 'Axe', [0,1,2,3,4,5,6,7]);
console.log(JSON.stringify({ status: 'PASS', qaOnly: true, scale: '3x nearest neighbor', output: path.relative(ROOT, out), sources: 24 }, null, 2));
