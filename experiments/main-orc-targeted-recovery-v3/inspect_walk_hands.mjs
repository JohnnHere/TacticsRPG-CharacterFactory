import fs from 'node:fs';
import path from 'node:path';
import { decode } from '../../src/images.mjs';

const ROOT = process.cwd();

function inspectWalkHands(dirName) {
  const dir = path.resolve(ROOT, `characters/orc-v1/source/rear-recovery-v2/${dirName}/Walk`);
  console.log(`\n=== Inspecting ${dirName}/Walk Hand/Gauntlet positions ===`);
  for (let i = 0; i < 8; i++) {
    const p = path.join(dir, `${String(i).padStart(2, '0')}.png`);
    const img = decode(p).image;
    // Let's find lower pixels on both sides (y: 110..150):
    // Left hand: x: 80..115, y: 110..150
    // Right hand: x: 140..175, y: 110..150
    let leftHandPx = [], rightHandPx = [];
    for (let y = 110; y <= 150; y++) {
      for (let x = 80; x <= 115; x++) {
        if (img.data[(y * 256 + x) * 4 + 3] > 0) {
          leftHandPx.push({ x, y });
        }
      }
      for (let x = 140; x <= 175; x++) {
        if (img.data[(y * 256 + x) * 4 + 3] > 0) {
          rightHandPx.push({ x, y });
        }
      }
    }
    const lMinX = leftHandPx.length ? Math.min(...leftHandPx.map(p => p.x)) : -1;
    const lMaxX = leftHandPx.length ? Math.max(...leftHandPx.map(p => p.x)) : -1;
    const lMinY = leftHandPx.length ? Math.min(...leftHandPx.map(p => p.y)) : -1;
    const lMaxY = leftHandPx.length ? Math.max(...leftHandPx.map(p => p.y)) : -1;
    
    const rMinX = rightHandPx.length ? Math.min(...rightHandPx.map(p => p.x)) : -1;
    const rMaxX = rightHandPx.length ? Math.max(...rightHandPx.map(p => p.x)) : -1;
    const rMinY = rightHandPx.length ? Math.min(...rightHandPx.map(p => p.y)) : -1;
    const rMaxY = rightHandPx.length ? Math.max(...rightHandPx.map(p => p.y)) : -1;
    
    console.log(`Frame ${i}: Left Hand px=${leftHandPx.length} [${lMinX}..${lMaxX}, ${lMinY}..${lMaxY}] | Right Hand px=${rightHandPx.length} [${rMinX}..${rMaxX}, ${rMinY}..${rMaxY}]`);
  }
}

inspectWalkHands('back_r');
inspectWalkHands('back_l');
