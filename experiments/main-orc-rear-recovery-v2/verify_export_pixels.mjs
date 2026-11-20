import fs from 'node:fs';
import path from 'node:path';
import { ROOT, hash } from '../../src/core.mjs';
import { decode } from '../../src/images.mjs';
import { PNG } from 'pngjs';

console.log("=== Pixel-by-Pixel Verification of Re-Exported Sheet Frames ===");

const buildDir = path.join(ROOT, 'dist/editor/main-orc-rear-recovery-v2-export/663e379bdd42e17b8cba');
const jobs = [
  { id: 'walk-back_r', candDir: 'characters/orc-v1/source/rear-recovery-v2/back_r/Walk', frames: 8 },
  { id: 'walk-back_l', candDir: 'characters/orc-v1/source/rear-recovery-v2/back_l/Walk', frames: 8 },
  { id: 'unarmed-back_r', candDir: 'characters/orc-v1/source/rear-recovery-v2/back_r/Unarmed', frames: 5 },
  { id: 'unarmed-back_l', candDir: 'characters/orc-v1/source/rear-recovery-v2/back_l/Unarmed', frames: 5 },
  { id: 'defeat-front_r', candDir: 'characters/orc-v1/source/rear-recovery-v2/front_r/Defeat', frames: 5 },
  { id: 'defeat-front_l', candDir: 'characters/orc-v1/source/rear-recovery-v2/front_l/Defeat', frames: 5 }
];

let totalPixelMatches = 0;
let totalFrames = 0;

for (const job of jobs) {
  const sheetPng = path.join(buildDir, 'jobs', job.id, 'sheet.png');
  const raster = decode(sheetPng).image;
  
  for (let i = 0; i < job.frames; i++) {
    totalFrames++;
    const candPngPath = path.join(ROOT, job.candDir, `${String(i).padStart(2, '0')}.png`);
    const candRaster = decode(candPngPath).image;
    
    // Extract slice from sheet: x = i * 256, y = 0, w = 256, h = 256
    const slice = new PNG({ width: 256, height: 256 });
    PNG.bitblt(raster, slice, i * 256, 0, 256, 256, 0, 0);
    
    // Compare buffers
    let diff = 0;
    for (let p = 0; p < slice.data.length; p++) {
      if (slice.data[p] !== candRaster.data[p]) diff++;
    }
    
    if (diff === 0) {
      totalPixelMatches++;
      console.log(`[PASS] ${job.id} frame ${String(i).padStart(2, '0')}: 100% byte-identical pixel match`);
    } else {
      console.error(`[FAIL] ${job.id} frame ${String(i).padStart(2, '0')}: ${diff} differing bytes`);
    }
  }
}

console.log(`\nPixel Verification Summary: ${totalPixelMatches}/${totalFrames} frames byte-for-byte identical.`);
