import path from 'node:path';
import { ROOT } from '../../src/core.mjs';
import { inspectAseprite } from '../../src/aseprite.mjs';

const masters = [
  // Native 128x128
  'characters/orc-v1/source/aseprite/rear-recovery-v2/native/walk-back_r.aseprite',
  'characters/orc-v1/source/aseprite/rear-recovery-v2/native/walk-back_l.aseprite',
  'characters/orc-v1/source/aseprite/rear-recovery-v2/native/unarmed-back_r.aseprite',
  'characters/orc-v1/source/aseprite/rear-recovery-v2/native/unarmed-back_l.aseprite',
  'characters/orc-v1/source/aseprite/rear-recovery-v2/native/defeat-front_r.aseprite',
  'characters/orc-v1/source/aseprite/rear-recovery-v2/native/defeat-front_l.aseprite',
  'characters/orc-v1/source/aseprite/rear-recovery-v2/native/sword-back_r.aseprite',
  'characters/orc-v1/source/aseprite/rear-recovery-v2/native/sword-back_l.aseprite',
  'characters/orc-v1/source/aseprite/rear-recovery-v2/native/axe-back_r.aseprite',
  'characters/orc-v1/source/aseprite/rear-recovery-v2/native/axe-back_l.aseprite',
  // Composite 256x256
  'characters/orc-v1/source/aseprite/rear-recovery-v2/composite/back_r/walk-unarmed.aseprite',
  'characters/orc-v1/source/aseprite/rear-recovery-v2/composite/back_l/walk-unarmed.aseprite',
  'characters/orc-v1/source/aseprite/rear-recovery-v2/composite/back_r/unarmed-attack.aseprite',
  'characters/orc-v1/source/aseprite/rear-recovery-v2/composite/back_l/unarmed-attack.aseprite',
  'characters/orc-v1/source/aseprite/rear-recovery-v2/composite/front_r/defeat.aseprite',
  'characters/orc-v1/source/aseprite/rear-recovery-v2/composite/front_l/defeat.aseprite',
  'characters/orc-v1/source/aseprite/rear-recovery-v2/composite/back_r/sword-attack.aseprite',
  'characters/orc-v1/source/aseprite/rear-recovery-v2/composite/back_l/sword-attack.aseprite',
  'characters/orc-v1/source/aseprite/rear-recovery-v2/composite/back_r/axe-attack.aseprite',
  'characters/orc-v1/source/aseprite/rear-recovery-v2/composite/back_l/axe-attack.aseprite'
];

console.log(`=== Validating All ${masters.length} Candidate Aseprite Masters ===`);
for (const rel of masters) {
  const full = path.join(ROOT, rel);
  const info = inspectAseprite(full);
  console.log(`[PASS] ${rel}:`);
  console.log(`       size=${info.width}x${info.height}, frames=${info.frames}, durationsMs=${JSON.stringify(info.durationsMs)}`);
}
console.log("All candidate masters 100% valid.");
