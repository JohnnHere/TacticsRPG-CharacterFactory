import fs from 'node:fs';
import { decode } from '../../src/images.mjs';

function inspectFrame(label, dir, frameIdx) {
  const filePath = `${dir}/${String(frameIdx).padStart(2, '0')}.png`;
  if (!fs.existsSync(filePath)) {
    console.log(`Frame not found: ${filePath}`);
    return;
  }
  const img = decode(filePath).image;
  // Find bounding box and arm region
  let minX = 128, maxX = 0, minY = 128, maxY = 0;
  let opaqueCount = 0;
  for (let y = 0; y < 128; y++) {
    for (let x = 0; x < 128; x++) {
      const a = img.data[(y * 128 + x) * 4 + 3];
      if (a > 0) {
        opaqueCount++;
        if (x < minX) minX = x;
        if (x > maxX) maxX = x;
        if (y < minY) minY = y;
        if (y > maxY) maxY = y;
      }
    }
  }
  console.log(`${label} f${frameIdx} (128x128): opaque=${opaqueCount} bbox=[${minX},${minY}]..[${maxX},${maxY}]`);
}

console.log('=== axe-r-cleaned-native ===');
for (let i = 0; i < 7; i++) {
  inspectFrame('axe-r', 'experiments/main-orc-rear-recovery-v2/axe-r-cleaned-native', i);
}

console.log('=== back_l-sword-cleaned-native ===');
for (let i = 0; i < 7; i++) {
  inspectFrame('sword-l', 'experiments/main-orc-rear-recovery-v2/back_l-sword-cleaned-native', i);
}

console.log('=== back_l-axe-repaired-native ===');
for (let i = 0; i < 7; i++) {
  inspectFrame('axe-l', 'experiments/main-orc-rear-recovery-v2/back_l-axe-repaired-native', i);
}
