import fs from 'node:fs';
import path from 'node:path';
import { ROOT, hash } from '../../src/core.mjs';

const absolute = file => path.resolve(ROOT, file);
const digest = file => hash(fs.readFileSync(absolute(file)));

// Frontals stay on the V7 cells on purpose: they are the creator-protected
// choreography (plus the armpit repair). The V8 frontal candidate was rejected
// because it flattened legitimate armour highlights on five frames.
const sources = [
  ['front_r', 'Sword', 'combat-recovery-v8/frontal-inbetween/front_r-sword', 'Apex descent frame authored so the blade no longer teleports: the 76 px jump is now two steps of about 38 px, timing unchanged at 730 ms and contact still on frame 8.'],
  ['front_l', 'Sword', 'combat-recovery-v8/frontal-inbetween/front_l-sword', 'Armpit junction re-lit on 70 px, zero RGB decreased, plus the authored apex descent frame.'],
  ['front_r', 'Axe', 'combat-recovery-v7/frontal/front_r-Axe-full', 'Protected V7 frontal carried forward unchanged.'],
  ['front_l', 'Axe', 'combat-recovery-v7/frontal/front_l-Axe-full', 'Protected V7 frontal carried forward unchanged.'],
  ['back_r', 'Sword', 'combat-recovery-v8/rear-arc/back_r-sword', 'Rebuilt without duplicated armed frames, then given the same authored apex descent frame so all four Sword directions share one cadence and one arc.'],
  ['back_r', 'Axe', 'combat-recovery-v8/rear/back_r-axe', 'Rebased on the frontal timing grid; corrected glove grip preserved.'],
  ['back_l', 'Sword', 'combat-recovery-v8/rear-arc/back_l-sword', 'Manual reconstruction rebased on the shared grid, with the authored apex descent frame.'],
  ['back_l', 'Axe', 'combat-recovery-v8/rear/back_l-axe', 'Manual reconstruction rebased on the shared grid, with the authored apex descent frame.'],
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
  patchId: 'orc-v1.combat-recovery-v8.weapon-patch',
  characterId: 'orc-v1',
  characterName: 'Verde Warcraft',
  revision: 'main-orc-combat-recovery-v8',
  parentManifest: 'characters/orc-v1/source/combat-recovery-v7/candidate28manifest.json',
  parentManifestSha256: digest('characters/orc-v1/source/combat-recovery-v7/candidate28manifest.json'),
  scope: 'V8: the four rear cells are rebased on the frontal timing grid so all four directions share one cadence and one impact instant; frontals carried forward unchanged from V7.',
  technicalStatus: 'TECHNICALLY_COMPLETE',
  artisticStatus: 'VISUAL_REVIEW_REQUIRED',
  artisticApproval: 'PENDING_CREATOR',
  eligibleForIntegration: false,
  creatorRejectedCandidate: 'combat-recovery-v7 fde1fe23f2d637589b6abef6b9b946b6c4370cc8ae5f3927525fb038397b2579',
  weapons: {
    Sword: 'characters/orc-v1/source/combat-rescue-v5/combat/weapons/Sword/weapon.json',
    Axe: 'characters/orc-v1/source/combat-rescue-v5/combat/weapons/Axe/weapon.json',
  },
  cells,
};
const out = 'characters/orc-v1/source/combat-recovery-v8/weapon-patch.json';
fs.mkdirSync(path.dirname(absolute(out)), { recursive: true });
fs.writeFileSync(absolute(out), `${JSON.stringify(patch, null, 2)}\n`);
console.log(JSON.stringify({ out, cells: cells.length, parent: patch.parentManifestSha256.slice(0, 12) }));
for (const c of cells) console.log(`${c.cellId} ${c.frameCount}f ${c.totalDurationMs}ms armed=${c.visibleInterval.join('-')} ${c.clipSha256.slice(0, 10)}`);
