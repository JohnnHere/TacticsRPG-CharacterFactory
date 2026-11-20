import fs from 'node:fs';
import { decode } from '../../src/images.mjs';

function inspectArea(filePath, x1, y1, x2, y2, desc) {
  const img = decode(filePath).image;
  console.log(`=== ${filePath} (${desc}) [${x1},${y1}]..[${x2},${y2}] ===`);
  const nonZero = [];
  for (let y = y1; y <= y2; y++) {
    for (let x = x1; x <= x2; x++) {
      const idx = (y * img.width + x) * 4;
      const r = img.data[idx];
      const g = img.data[idx + 1];
      const b = img.data[idx + 2];
      const a = img.data[idx + 3];
      if (a > 0) {
        nonZero.push({ x, y, r, g, b, a, hex: `rgba(${r},${g},${b},${a})` });
      }
    }
  }
  console.log(`  Found ${nonZero.length} non-transparent pixels in area.`);
  if (nonZero.length > 0 && nonZero.length <= 40) {
    nonZero.forEach(p => console.log(`    at (${p.x},${p.y}): ${p.hex}`));
  } else if (nonZero.length > 40) {
    console.log(`    Sample first 10:`, nonZero.slice(0, 10));
    console.log(`    Sample last 10:`, nonZero.slice(-10));
  }
}

// 1. back_l/Sword F07: quadril direito da imagem (x: 135..180, y: 110..160)
inspectArea(
  'characters/orc-v1/source/rear-recovery-v2/back_l/Sword/Attack-representative-v1/layers/body/07.png',
  140, 100, 180, 160,
  'back_l/Sword F07 hip area'
);

// 2. back_l/Sword F05: ombro/pescoço (x: 110..150, y: 70..100)
inspectArea(
  'characters/orc-v1/source/rear-recovery-v2/back_l/Sword/Attack-representative-v1/layers/body/05.png',
  110, 70, 150, 105,
  'back_l/Sword F05 neck/shoulder light band'
);

// 3. back_r/Axe F01: cabeça secundária de machado junto ao braço erguido
// Where is the raised arm in back_r? In NW / NE rear view, raised arm is around x: 130..190, y: 40..100
inspectArea(
  'characters/orc-v1/source/rear-recovery-v2/back_r/Axe/Attack-representative-v1/layers/body/01.png',
  130, 40, 190, 110,
  'back_r/Axe F01 raised arm axe head'
);

// 4. back_l/Axe F02-F03: filamento/gancho claro à direita da ombreira distante
inspectArea(
  'characters/orc-v1/source/rear-recovery-v2/back_l/Axe/Attack-representative-v1/layers/body/02.png',
  135, 65, 175, 100,
  'back_l/Axe F02 right of shoulder filament'
);
