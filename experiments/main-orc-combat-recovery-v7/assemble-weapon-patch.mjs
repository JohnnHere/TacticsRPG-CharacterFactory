import fs from 'node:fs';
import path from 'node:path';
import { ROOT, hash } from '../../src/core.mjs';

const absolute = file => path.resolve(ROOT, file);
const digest = file => hash(fs.readFileSync(absolute(file)));

const sources = [
  ['front_r', 'Sword', 'combat-recovery-v7/frontal/full-front-r-sword', 'Frontal protected choreography preserved; only confirmed body-layer axilla/bright-pixel cleanup where measured.'],
  ['front_l', 'Sword', 'combat-recovery-v7/frontal/front_l-Sword-full', 'V7-QA-01 armpit: 19 px restored to native colours (ink plate, retrograde step, orphan pixel, island removed).'],
  ['front_r', 'Axe', 'combat-recovery-v7/frontal/front_r-Axe-full', 'Frontal preserved; light-contour census returned NO CONFIRMED ARTIFACT against the V5 palette.'],
  ['front_l', 'Axe', 'combat-recovery-v7/frontal/front_l-Axe-full', 'Frontal preserved; light-contour census returned NO CONFIRMED ARTIFACT against the V5 palette.'],
  ['back_r', 'Sword', 'combat-recovery-v7/rear-r-flashfixed/back_r-sword', 'Refined back_r sword plus normalised bookends (bright pixels 67->7 at F00, 67->5 at F11).'],
  ['back_r', 'Axe', 'combat-recovery-v7/rear-r-flashfixed/back_r-axe', 'Underhand grip corrected on the glove itself; bookends normalised identically.'],
  ['back_l', 'Sword', 'combat-recovery-v7/rear-alt/back_l-sword', 'Full manual Aseprite reconstruction: elevated apex, vertical descent, authored palm chain. Zero generations.'],
  ['back_l', 'Axe', 'combat-recovery-v7/rear-alt/back_l-axe', 'Full manual Aseprite reconstruction with axe-specific weight; bookends consistent. Zero generations.'],
];

const cells = sources.map(([direction, action, dir, notes]) => {
  const clipJson = `characters/orc-v1/source/${dir}/clip.json`;
  const clip = JSON.parse(fs.readFileSync(absolute(clipJson), 'utf8'));
  if (clip.direction !== direction) throw new Error(`direction mismatch ${clipJson}`);
  if (clip.category !== action) throw new Error(`category mismatch ${clipJson}`);
  const vis = clip.frames.filter(f => f.weaponVisible === true).map(f => f.index);
  if (!vis.length) throw new Error(`no armed frame ${clipJson}`);
  if (clip.frames[0].weaponVisible || clip.frames.at(-1).weaponVisible) throw new Error(`armed bookend ${clipJson}`);
  return {
    direction,
    action,
    cellId: `${direction}/${action}`,
    clipJson,
    clipSha256: digest(clipJson),
    frameCount: clip.frames.length,
    totalDurationMs: clip.totalDurationMs,
    visibleInterval: [Math.min(...vis), Math.max(...vis)],
    provenance: dir,
    notes,
  };
});

const patch = {
  schemaVersion: 1,
  patchId: 'orc-v1.combat-recovery-v7.weapon-patch',
  characterId: 'orc-v1',
  characterName: 'Verde Warcraft',
  revision: 'main-orc-combat-recovery-v7',
  parentManifest: 'characters/orc-v1/source/artistic-reconstruction-v6/candidate28manifest.json',
  parentManifestSha256: digest('characters/orc-v1/source/artistic-reconstruction-v6/candidate28manifest.json'),
  scope: 'V7: back_l Sword/Axe reconstructed manually; back_r refined and bookend-flash corrected; frontal armpit repaired; frontal light contours verified negative.',
  technicalStatus: 'TECHNICALLY_COMPLETE',
  artisticStatus: 'VISUAL_REVIEW_REQUIRED',
  artisticApproval: 'PENDING_CREATOR',
  eligibleForIntegration: false,
  creatorRejectedCandidate: 'artistic-reconstruction-v6 5d68b52d3e2b2a0931d689afb5a9dd438c178835d05efb02a5fb2bcf0c64b7ca',
  weapons: {
    Sword: 'characters/orc-v1/source/combat-rescue-v5/combat/weapons/Sword/weapon.json',
    Axe: 'characters/orc-v1/source/combat-rescue-v5/combat/weapons/Axe/weapon.json',
  },
  cells,
};
const out = 'characters/orc-v1/source/combat-recovery-v7/weapon-patch.json';
fs.mkdirSync(path.dirname(absolute(out)), { recursive: true });
fs.writeFileSync(absolute(out), `${JSON.stringify(patch, null, 2)}\n`);
console.log(JSON.stringify({ out, cells: cells.length, parent: patch.parentManifestSha256.slice(0, 12) }));
for (const c of cells) console.log(`${c.cellId} ${c.frameCount}f ${c.totalDurationMs}ms armed=${c.visibleInterval.join('-')} ${c.clipSha256.slice(0, 10)}`);
