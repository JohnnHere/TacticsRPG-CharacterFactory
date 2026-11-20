import fs from 'node:fs';
import path from 'node:path';
import { ROOT, hash } from '../../src/core.mjs';

const absolute = file => path.resolve(ROOT, file);
const digest = file => hash(fs.readFileSync(absolute(file)));
const parentPath = 'characters/orc-v1/source/combat-rescue-v5/candidate28manifest.json';
const rear = JSON.parse(fs.readFileSync(absolute('characters/orc-v1/source/artistic-reconstruction-v6/rear/patch-manifest-stage-d.json'), 'utf8'));
const frontal = JSON.parse(fs.readFileSync(absolute('experiments/main-orc-artistic-reconstruction-v6/frontal/patch-manifest.json'), 'utf8'));

// QA-driven corrections supersede the first delivery of the affected cells.
const escalated = JSON.parse(fs.readFileSync(absolute('experiments/main-orc-artistic-reconstruction-v6/frontal-escalated/patch-manifest.json'), 'utf8'));
const groundfix = JSON.parse(fs.readFileSync(absolute('experiments/main-orc-artistic-reconstruction-v6/rear/back-l-sword-groundfix/patch-manifest.json'), 'utf8'));
const overrides = new Map();
for (const cell of [...escalated.cells, ...groundfix.cells]) {
  const clip = cell.clip ?? cell.clipJson;
  overrides.set(`${cell.direction}/${cell.category ?? cell.action}`, {
    clipJson: clip,
    note: cell.category === undefined
      ? 'QA V6-QA-01 fix: front_l/Sword F03-F04 body-layer axilla geometry rebuilt (58 px total); weapons, pose and timing untouched.'
      : 'QA V6-QA-02 fix: back_l/Sword F07-F09 recovery binding adjusted so the blade tip stays above groundY (tips at y=187/185/173).',
  });
}

const cells = [];
for (const source of [rear.cells, frontal.cells]) {
  for (const cell of source) {
    const action = cell.category ?? cell.action;
    const id = `${cell.direction}/${action}`;
    const override = overrides.get(id);
    const clipJson = override?.clipJson ?? cell.clip ?? cell.clipJson;
    cells.push({
      direction: cell.direction,
      action,
      cellId: id,
      clipJson,
      clipSha256: digest(clipJson),
      provenance: cell.beforeClip
        ? `main-orc-artistic-reconstruction-v6; replaces rejected V5 cell ${cell.beforeClip}`
        : 'main-orc-artistic-reconstruction-v6',
      notes: override?.note ?? (cell.edits !== undefined
        ? `Localized frontal body-layer fix: ${cell.edits} single-pixel edits (floating islands + confirmed bright dots); weapon layers untouched.`
        : 'Rear artistic reconstruction from the V6 reference pipeline; see rear/back-r-stage-d/report.md and rear/report.md.'),
    });
  }
}
const expected = new Set(cells.map(cell => cell.cellId));
if (cells.length !== 8) throw new Error(`Expected 8 cells, got ${cells.length}`);
for (const id of ['front_r/Sword', 'front_l/Sword', 'front_r/Axe', 'front_l/Axe', 'back_r/Sword', 'back_l/Sword', 'back_r/Axe', 'back_l/Axe']) {
  if (!expected.has(id)) throw new Error(`Missing ${id}`);
}

const patch = {
  schemaVersion: 1,
  patchId: 'orc-v1.artistic-reconstruction-v6.weapon-patch',
  characterId: 'orc-v1',
  characterName: 'Verde Warcraft',
  revision: 'main-orc-artistic-reconstruction-v6',
  parentManifest: parentPath,
  parentManifestSha256: digest(parentPath),
  scope: 'Eight reconstructed/localized Sword/Axe attack cycles replacing the creator-rejected V5 cells.',
  technicalStatus: 'TECHNICALLY_COMPLETE',
  artisticStatus: 'VISUAL_REVIEW_REQUIRED',
  artisticApproval: 'PENDING_CREATOR',
  eligibleForIntegration: false,
  weapons: {
    Sword: 'characters/orc-v1/source/combat-rescue-v5/combat/weapons/Sword/weapon.json',
    Axe: 'characters/orc-v1/source/combat-rescue-v5/combat/weapons/Axe/weapon.json',
  },
  cells,
};
const out = 'characters/orc-v1/source/artistic-reconstruction-v6/weapon-patch.json';
fs.writeFileSync(absolute(out), JSON.stringify(patch, null, 2));
console.log(JSON.stringify({ out, cells: cells.length, parentSha: patch.parentManifestSha256 }));
